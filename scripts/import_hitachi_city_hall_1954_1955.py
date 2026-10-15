#!/usr/bin/env python3
"""1954・1955年の歴史Excelを月別YAMLへ採録する。

1953年専用処理のセル配置をそのまま流用せず、各月の見出しを照合する。
原ZIPと内部XLSを検証し、LibreOfficeで作った読取用XLSXだけを解析する。
"""

from __future__ import annotations

import argparse
import calendar
import hashlib
import shutil
import subprocess
import urllib.request
import zipfile
from dataclasses import dataclass
from datetime import datetime, time, timedelta
from functools import lru_cache
from pathlib import Path
from typing import Any

import openpyxl
import xlrd
import yaml
from openpyxl.utils.datetime import to_excel

import import_hitachi_city_hall_1953 as common


ROOT = Path(__file__).resolve().parents[1]
ELEMENTS = (
    "temperature", "humidity", "precipitation", "pressure",
    "sunshine_duration", "wind_speed", "wind_direction", "weather_code",
)
FOUR_TIMES = [6, 9, 14, 22]
ALL_HOURS = list(range(1, 25))
DAYLIGHT_HOURS = list(range(4, 21))
SEA_LEVEL_SCHEDULES = {
    1954: {month: ([6, 9, 14, 22] if month <= 7 else [3, 9, 15, 21])
           for month in range(1, 13)},
    1955: {month: [3, 9, 15, 21] for month in range(1, 13)},
}


class CellAdapter:
    """openpyxlのセルを1953年処理が使う読み取り専用形式に合わせる。"""

    def __init__(self, cell):
        value = cell.value
        self.source_value = value
        if value is None:
            self.ctype, self.value = xlrd.XL_CELL_EMPTY, ""
        elif isinstance(value, bool):
            self.ctype, self.value = xlrd.XL_CELL_BOOLEAN, int(value)
        elif isinstance(value, (datetime, time)):
            self.ctype, self.value = xlrd.XL_CELL_DATE, float(to_excel(value))
        elif isinstance(value, timedelta):
            self.ctype, self.value = xlrd.XL_CELL_DATE, value.total_seconds() / 86400
        elif isinstance(value, (int, float)):
            self.ctype, self.value = xlrd.XL_CELL_NUMBER, float(value)
        elif isinstance(value, str):
            self.ctype, self.value = xlrd.XL_CELL_TEXT, value
        else:
            raise TypeError(f"Unsupported converted Excel value: {value!r} at {cell.coordinate}")


class SheetAdapter:
    def __init__(self, sheet):
        self.sheet = sheet
        self.name = sheet.title
        self.nrows = sheet.max_row
        self.ncols = sheet.max_column

    def cell(self, row: int, column: int):
        return CellAdapter(self.sheet.cell(row + 1, column + 1))

    def cell_value(self, row: int, column: int):
        return self.sheet.cell(row + 1, column + 1).value


class WorkbookAdapter:
    datemode = 0

    def __init__(self, path: Path):
        self.workbook = openpyxl.load_workbook(path, data_only=True, read_only=False)
        self.nsheets = len(self.workbook.worksheets)

    def sheet_by_index(self, index: int):
        return SheetAdapter(self.workbook.worksheets[index])

    def sheet_by_name(self, name: str):
        return SheetAdapter(self.workbook[name])


@dataclass(frozen=True)
class PreservedSourceCell:
    value: Any
    flag: str | None = None
    raw_value: Any = None
    has_raw_value: bool = False


original_source_cell = common.source_cell
common.SourceCell = PreservedSourceCell


def source_cell_with_original_spelling(cell, *, integer: bool = False):
    """1954–55用に空白・記号・原文字列を残すセル変換。"""

    raw = getattr(cell, "source_value", cell.value)
    if isinstance(raw, str):
        normalized = raw.strip()
        if normalized == "欠測":
            return PreservedSourceCell(None, "source_missing", raw, True)
        if normalized == "" and raw:
            return PreservedSourceCell(None, "source_whitespace", raw, True)
    converted = original_source_cell(cell, integer=integer)
    preserve_raw = raw is not None and (
        converted.flag is not None or (isinstance(raw, str) and raw != converted.value)
    )
    return PreservedSourceCell(
        converted.value,
        converted.flag,
        raw if preserve_raw else None,
        preserve_raw,
    )


common.source_cell = source_cell_with_original_spelling


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def prepare_sources(year: int, source_directory: Path, download_missing: bool):
    manifest_path = ROOT / "metadata" / "sources" / f"hitachi-city-hall-{year}.yaml"
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    source_directory.mkdir(parents=True, exist_ok=True)
    original_dir = source_directory / "original"
    converted_dir = source_directory / "converted"
    original_dir.mkdir(exist_ok=True)
    converted_dir.mkdir(exist_ok=True)
    source_paths: dict[str, Path] = {}
    rows: list[dict[str, str]] = []

    for entry in manifest["files"]:
        element = entry["element"]
        archive_path = source_directory / f"{element}.zip"
        if not archive_path.exists():
            if not download_missing:
                raise FileNotFoundError(f"Missing archive: {archive_path}; use --download-missing")
            urllib.request.urlretrieve(entry["url"], archive_path)
        actual_archive_hash = sha256_path(archive_path)
        if actual_archive_hash != entry["archive_sha256"]:
            raise ValueError(f"ZIP SHA-256 mismatch: {archive_path.name}")
        with zipfile.ZipFile(archive_path) as archive:
            original_bytes = archive.read(entry["archive_member"])
        actual_member_hash = sha256_bytes(original_bytes)
        if actual_member_hash != entry["member_sha256"]:
            raise ValueError(f"Internal XLS SHA-256 mismatch: {entry['archive_member']}")

        original_path = original_dir / entry["archive_member"]
        if not original_path.exists() or sha256_path(original_path) != actual_member_hash:
            original_path.write_bytes(original_bytes)
        converted_path = converted_dir / f"{Path(entry['archive_member']).stem}.xlsx"
        if not converted_path.exists():
            office = shutil.which("soffice") or shutil.which("libreoffice")
            if office is None:
                raise FileNotFoundError("LibreOffice is required for legacy XLS conversion")
            profile = converted_dir / f"profile-{element}"
            profile.mkdir(exist_ok=True)
            subprocess.run(
                [office, "--headless", f"-env:UserInstallation={profile.resolve().as_uri()}",
                 "--convert-to", "xlsx", "--outdir", str(converted_dir), str(original_path)],
                check=True, timeout=180, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                text=True,
            )
        if not converted_path.exists():
            raise ValueError(f"LibreOffice did not create {converted_path.name}")
        source_paths[element] = converted_path
        rows.append({
            "element": element,
            "archive": archive_path.name,
            "member": entry["archive_member"],
            "archive_sha256": actual_archive_hash,
            "member_sha256": actual_member_hash,
            "status": "verified",
        })

    # These two archives are checked too: absence of an annual workbook is not a blank observation.
    for element in ("global_solar_radiation", "dew_point_temperature"):
        catalog = yaml.safe_load((ROOT / "metadata/sources/hitachi-city-hall-historical-archives.yaml").read_text(encoding="utf-8"))
        catalog_element = "solar_radiation" if element == "global_solar_radiation" else element
        archive_entry = next(item for item in catalog["archives"] if item["element"] == catalog_element)
        archive_path = source_directory / archive_entry["file_name"]
        if not archive_path.exists():
            if not download_missing:
                raise FileNotFoundError(f"Missing archive: {archive_path}; use --download-missing")
            urllib.request.urlretrieve(archive_entry["url"], archive_path)
        if sha256_path(archive_path) != archive_entry["sha256"]:
            raise ValueError(f"ZIP SHA-256 mismatch: {archive_path.name}")
        with zipfile.ZipFile(archive_path) as archive:
            expected_member = f"{'sunF' if element == 'global_solar_radiation' else 'dewp'}{year}.xls"
            if any(Path(member).name.casefold() == expected_member.casefold() for member in archive.namelist()):
                raise ValueError(f"Unexpected {expected_member} found; update availability metadata")
        rows.append({"element": element, "archive": archive_path.name,
                     "member": f"{expected_member} (not present)",
                     "archive_sha256": archive_entry["sha256"],
                     "member_sha256": "not_applicable", "status": "archive_verified_member_absent"})
    return manifest, source_paths, rows


@lru_cache(maxsize=16)
def workbook(path: Path):
    return WorkbookAdapter(path)


# Reuse the established extractor functions with a narrow adapter for the
# LibreOffice-converted workbooks. The original XLS files remain untouched.
common.xlrd.open_workbook = lambda path, **_kwargs: workbook(Path(path))


def extract_four_time(path: Path, month: int, element: str, *, header_row=1, first_day_row=2):
    columns = dict(zip(FOUR_TIMES, range(1, 5)))
    return common.extract_day_hour_table(path, month, element,
        header_row=header_row, first_day_row=first_day_row, columns_by_hour=columns)


def extract_all_hours(path: Path, month: int, element: str, *, header_row=1, first_day_row=2):
    return common.extract_day_hour_table(path, month, element,
        header_row=header_row, first_day_row=first_day_row,
        columns_by_hour={hour: hour for hour in ALL_HOURS})


def extract_wind_direction(path: Path, month: int):
    raw = extract_all_hours(path, month, "wind_direction", header_row=1, first_day_row=2)
    converted = {}
    for key, cell in raw.cells.items():
        if cell.value is None:
            converted[key] = cell
            continue
        direction = str(cell.value).upper()
        if direction not in common.WIND_DIRECTION_CODES:
            raw_value = cell.raw_value if cell.has_raw_value else cell.value
            converted[key] = PreservedSourceCell(
                None, "unrecognized_source_value", raw_value, True
            )
            continue
        raw_value = cell.raw_value if cell.has_raw_value else cell.value
        has_raw_value = cell.has_raw_value or raw_value != direction
        converted[key] = PreservedSourceCell(
            direction,
            cell.flag,
            raw_value if has_raw_value else None,
            has_raw_value,
        )
    return common.ElementExtraction("wind_direction", converted)


def extract_sea_level_pressure(path: Path, month: int, year: int):
    expected = SEA_LEVEL_SCHEDULES[year][month]
    sheet = workbook(path).sheet_by_index(month - 1)
    header_row, first_day_row = 37, 38
    actual = [common.integer_value(sheet.cell_value(header_row, column)) for column in range(1, 5)]
    if actual != expected:
        raise ValueError(f"Sea-level pressure schedule mismatch {year}-{month:02d}: {actual} != {expected}")
    extraction = common.extract_day_hour_table(
        path, month, "sea_level_pressure_hpa", header_row=header_row,
        first_day_row=first_day_row,
        columns_by_hour=dict(zip(expected, range(1, 5))),
    )
    return extraction


def schedules_for(year: int, month: int):
    return {
        "temperature_c": FOUR_TIMES,
        "relative_humidity_percent": FOUR_TIMES,
        "station_pressure_hpa": FOUR_TIMES,
        "sea_level_pressure_hpa": SEA_LEVEL_SCHEDULES[year][month],
        "sunshine_duration_h": DAYLIGHT_HOURS,
        "wind_speed_m_s": FOUR_TIMES,
        "wind_direction": ALL_HOURS,
        "weather_code": [9],
    }


def add_daily_summary_source_state(summaries, source_paths, month: int):
    """Attach raw symbols and flags to summary cells without changing values."""

    summary_fields = {
        "temperature": ("temperature", 1, {
            "mean_c": (5, "number"),
            "maximum.value_c": (6, "number"), "maximum.time": (7, "time"),
            "minimum.value_c": (8, "number"), "minimum.time": (9, "time"),
        }),
        "humidity": ("humidity", 1, {
            "mean_percent": (5, "number"), "minimum.value_percent": (6, "number"),
            "minimum.time": (7, "time"),
        }),
        "precipitation": ("precipitation", 2, {
            "total_mm": (25, "number"), "maximum_one_hour.value_mm": (27, "number"),
            "maximum_one_hour.time": (28, "time"),
            "maximum_ten_minutes.value_mm": (30, "number"),
            "maximum_ten_minutes.time": (31, "time"),
        }),
        "station_pressure": ("pressure", 1, {
            "mean_hpa": (5, "number"), "maximum.value_hpa": (6, "number"),
            "maximum.time": (7, "time"), "minimum.value_hpa": (8, "number"),
            "minimum.time": (9, "time"),
        }),
        "sunshine_duration": ("sunshine_duration", 1, {"total_h": (18, "number")}),
        "wind": ("wind_speed", 2, {
            "mean_speed_m_s": (25, "number"),
            "maximum_10_minute.direction": (28, "text"),
            "maximum_10_minute.speed_m_s": (29, "number"),
            "maximum_10_minute.time": (30, "time"),
            "maximum_instantaneous.direction": (32, "text"),
            "maximum_instantaneous.speed_m_s": (33, "number"),
            "maximum_instantaneous.time": (34, "time"),
        }),
    }
    sheets = {
        name: workbook(source_paths[key]).sheet_by_index(month - 1)
        for name, (key, _row_offset, _fields) in summary_fields.items()
    }
    for day, summary in enumerate(summaries, start=1):
        for summary_group, (source_key, row_offset, fields) in summary_fields.items():
            sheet = sheets[summary_group]
            for field_path, (column, value_kind) in fields.items():
                source_excel_cell = sheet.cell(day + row_offset, column)
                source = source_cell_with_original_spelling(source_excel_cell)
                dotted_path = f"{summary_group}.{field_path}"
                flag = source.flag
                raw_value = source.raw_value if source.has_raw_value else None
                if (value_kind == "time"
                        and source_excel_cell.ctype == xlrd.XL_CELL_DATE
                        and source_excel_cell.value >= 1):
                    # Preserve the ambiguous Excel serial alongside its explicit
                    # source_excel_serial display; do not reinterpret it as HH:MM.
                    raw_value = source_excel_cell.value
                if value_kind == "number" and isinstance(source.value, str) and flag is None:
                    flag = "unrecognized_source_value"
                    raw_value = source.value
                if flag is not None:
                    summary.setdefault("flags", {})[dotted_path] = flag
                if raw_value is not None:
                    summary.setdefault("raw_values", {})[dotted_path] = raw_value
            if not summary.get("flags"):
                summary.pop("flags", None)
            if not summary.get("raw_values"):
                summary.pop("raw_values", None)


def extract_month(source_paths, year: int, month: int):
    # The sheet headers are checked against these exact month-specific schedules.
    four = {hour: column for hour, column in zip(FOUR_TIMES, range(1, 5))}
    daylight = {hour: column for hour, column in zip(DAYLIGHT_HOURS, range(1, 18))}
    hourly = {hour: hour for hour in ALL_HOURS}
    if year == 1955 and month == 1:
        temperature_sheet = workbook(source_paths["temperature"]).sheet_by_index(0)
        actual_annotation = str(temperature_sheet.cell_value(0, 2) or "").strip()
        expected_annotation = "(観測時刻注意）"
        if actual_annotation != expected_annotation:
            raise ValueError(
                "1955年1月の気温シート注記が調査記録と一致しません: "
                f"{actual_annotation!r} != {expected_annotation!r}"
            )
    return [
        common.extract_day_hour_table(source_paths["temperature"], month, "temperature_c",
            header_row=1, first_day_row=2, columns_by_hour=four),
        common.extract_day_hour_table(source_paths["humidity"], month, "relative_humidity_percent",
            header_row=1, first_day_row=2, columns_by_hour=four),
        common.extract_day_hour_table(source_paths["precipitation"], month, "precipitation_mm",
            header_row=2, first_day_row=3, columns_by_hour=hourly),
        common.extract_day_hour_table(source_paths["pressure"], month, "station_pressure_hpa",
            header_row=1, first_day_row=2, columns_by_hour=four),
        extract_sea_level_pressure(source_paths["pressure"], month, year),
        common.extract_day_hour_table(source_paths["sunshine_duration"], month,
            "sunshine_duration_h", header_row=1, first_day_row=2, columns_by_hour=daylight),
        common.extract_day_hour_table(source_paths["wind_speed"], month, "wind_speed_m_s",
            header_row=1, first_day_row=3, columns_by_hour=hourly),
        extract_wind_direction(source_paths["wind_direction"], month),
        common.extract_weather(source_paths["weather_code"], month),
    ]


def assemble(year: int, month: int, extractions, summaries, manifest, source_paths):
    # Reuse the established schema assembly while supplying the verified monthly schedule.
    original_year = common.YEAR
    original_schedules = common.OBSERVATION_SCHEDULES
    original_layouts = common.SOURCE_TABLE_LAYOUTS
    common.YEAR = year
    common.OBSERVATION_SCHEDULES = schedules_for(year, month)
    common.SOURCE_TABLE_LAYOUTS = {
        "precipitation_mm": {"source_columns": ALL_HOURS,
                              "status": "daily_and_hourly_table", "available_as": "hourly_and_daily_summary"},
        "sea_level_pressure_hpa": {"source_columns": SEA_LEVEL_SCHEDULES[year][month],
                                   "status": "monthly_schedule_verified"},
    }
    try:
        document = common.assemble_month_document(month, extractions, summaries, manifest)
    finally:
        common.YEAR = original_year
        common.OBSERVATION_SCHEDULES = original_schedules
        common.SOURCE_TABLE_LAYOUTS = original_layouts
    document["dataset"]["source_manifest"] = f"../../../metadata/sources/hitachi-city-hall-{year}.yaml"
    document["dataset"]["generator"] = "scripts/import_hitachi_city_hall_1954_1955.py"
    document["dataset"]["observation_schedules"] = {
        key: common.FlowSequence(hours) for key, hours in schedules_for(year, month).items()
    }
    # The 24-cell precipitation and sea-level-pressure tables are present, but
    # every hourly entry is blank in these two years. Daily summaries remain.
    extraction_by_element = {item.element_id: item for item in extractions}
    for element_id in ("precipitation_mm", "sea_level_pressure_hpa"):
        extraction = extraction_by_element[element_id]
        if all(cell.value is None and cell.flag == "source_blank" for cell in extraction.cells.values()):
            layout = document["dataset"]["source_table_layouts"][element_id]
            layout["status"] = "no_hourly_values_in_month"
            if element_id == "precipitation_mm":
                layout["available_as"] = "daily_summary"
        elif element_id == "sea_level_pressure_hpa":
            document["dataset"]["source_table_layouts"][element_id]["status"] = "values_present"

    # Keep the exact original text when normalization is needed to classify a
    # marker such as a padded dash. Ordinary values remain uncluttered.
    for observation in document["observations"]:
        day = int(observation["source_date"][-2:])
        raw_values = {}
        for element_id, extraction in extraction_by_element.items():
            source = extraction.cells.get((day, observation["source_hour"]))
            if source is not None and source.has_raw_value:
                raw_values[element_id] = source.raw_value
        if raw_values:
            observation["raw_values"] = raw_values

    add_daily_summary_source_state(document["daily_summaries"], source_paths, month)
    document["notes"] = [
        "観測要素ごとに異なる原資料上の観測時刻を保持する。",
        "原資料の見出しを月ごとに照合し、記載のない時刻は補完していない。",
        "時刻別観測値と日別集計値を別々に収録する。",
        "全天日射量と露点温度の年別Excelは原資料ZIP内に存在しない。",
    ]
    if year == 1955 and month == 1:
        document["notes"].append("気温シートの原資料注記「（観測時刻注意）」を未解釈のまま記録する。見出しに記載された6・9・14・22時を採録したが、注記の意味は未確認。")
        document["dataset"]["source_annotations"] = {
            "temperature_c": {"source_text": "(観測時刻注意）", "status": "unresolved"}
        }
    return document


def write_report(path: Path, year: int, month: int, target: Path, document, extractions, source_rows):
    days = calendar.monthrange(year, month)[1]
    lines = [f"# {year}年{month}月データ検証報告", "", "## 検証結果", "",
        "- 判定：合格（原資料に明記された注記がある場合は未解釈事項として併記）",
        f"- YAML：`{target.relative_to(ROOT)}`", f"- 日数：{days}",
        f"- 時刻レコード数：{len(document['observations'])}",
        "- YAML再読込：生成直前のデータ構造と一致", "- 各月の観測時刻見出し：要素別に照合", "",
        "## 抽出セル数", "", "| 要素 | セル数 | 値あり | null | フラグ |", "|---|---:|---:|---:|---|"]
    for extraction in extractions:
        non_null, null_count, flags = common.count_cells(extraction)
        label = ", ".join(f"`{key}`: {value}" for key, value in sorted(flags.items())) or "—"
        lines.append(f"| `{extraction.element_id}` | {len(extraction.cells)} | {non_null} | {null_count} | {label} |")
    lines.extend(["", "## 原資料の同一性", "", "原ZIPと内部ExcelのSHA-256をマニフェスト値と照合した。", "",
        "| 要素 | ZIP | 内部ファイル | ZIP SHA-256 | XLS SHA-256 | 判定 |",
        "|---|---|---|---|---|---|"])
    for row in source_rows:
        lines.append(f"| {row['element']} | `{row['archive']}` | `{row['member']}` | `{row['archive_sha256']}` | `{row['member_sha256']}` | {row['status']} |")
    lines.extend(["", "## レイアウト上の注意", "",
        f"- 海面気圧の見出し時刻：{', '.join(map(str, SEA_LEVEL_SCHEDULES[year][month]))}時。",
        "- 風向は1〜24時、風速は6・9・14・22時の見出しを独立して照合した。",
        "- 数値0、空欄、ハイフン等は原資料上の状態を分けて保持した。",
        "- LibreOfficeで読取用XLSXへ変換して解析。原ZIP・原XLSは変更していない。"])
    if year == 1955 and month == 1:
        lines.extend(["", "## 未解決の原資料注記", "", "- 気温シートに「(観測時刻注意）」とある。見出し行は6・9・14・22時で一致するため、その列見出しに沿って値を採録した。注記の意味は推測せず、注記そのものを正本YAMLにも記録した。"])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--year", type=int, required=True, choices=(1954, 1955))
    parser.add_argument("--month", type=int, choices=range(1, 13))
    parser.add_argument("--source-directory", type=Path)
    parser.add_argument("--download-missing", action="store_true")
    args = parser.parse_args()
    directory = args.source_directory or ROOT / "build" / f"source-{args.year}"
    manifest, source_paths, source_rows = prepare_sources(args.year, directory, args.download_missing)
    months = [args.month] if args.month else range(1, 13)
    for month in months:
        common.YEAR = args.year
        extractions = extract_month(source_paths, args.year, month)
        summaries = common.extract_daily_summaries(source_paths, month)
        document = assemble(args.year, month, extractions, summaries, manifest, source_paths)
        target = ROOT / "data/hitachi-city-hall" / str(args.year) / f"{month:02d}.yaml"
        report = ROOT / "reports" / f"validation-{args.year}-{month:02d}.md"
        common.write_yaml(target, document)
        common.validate_round_trip(target, document)
        write_report(report, args.year, month, target, document, extractions, source_rows)
        print(f"Generated and validated: {target.relative_to(ROOT)}")
        print(f"Report: {report.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
