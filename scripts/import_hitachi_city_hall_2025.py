#!/usr/bin/env python3
"""日立市役所観測所の2025年Excelを月別YAMLへ変換する。

このスクリプトは、原資料の値を解釈しすぎないことを重視する。
特に、空欄・ハイフン・三連アスタリスクは0とみなさず、YAMLでは
nullと来歴フラグに分けて保存する。
"""

from __future__ import annotations

import argparse
import calendar
import hashlib
import math
import sys
import urllib.request
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any, Iterable

import xlrd
import yaml


# ==========================================
# Repository paths and source definitions
# ==========================================

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SOURCE_MANIFEST_PATH = (
    REPOSITORY_ROOT / "metadata" / "sources" / "hitachi-city-hall-2025.yaml"
)

YEAR = 2025
STATION_ID = "hitachi-city-hall"
GENERATOR_PATH = "scripts/import_hitachi_city_hall_2025.py"

SOURCE_FILE_NAMES = {
    "temperature": "temperature.xls",
    "humidity": "humidity.xls",
    "precipitation": "precipitation.xls",
    "pressure": "pressure.xls",
    "solar_radiation": "solar_radiation.xls",
    "sunshine_duration": "sunshine_duration.xls",
    "wind_speed": "wind_speed.xls",
    "wind_direction": "wind_direction.xls",
    "dew_point_temperature": "dew_point.xls",
    "weather_at_noon": "weather.xls",
}

WIND_DIRECTION_CODES = {
    "北": "N",
    "北北東": "NNE",
    "北東": "NE",
    "東北東": "ENE",
    "東": "E",
    "東南東": "ESE",
    "南東": "SE",
    "南南東": "SSE",
    "南": "S",
    "南南西": "SSW",
    "南西": "SW",
    "西南西": "WSW",
    "西": "W",
    "西北西": "WNW",
    "北西": "NW",
    "北北西": "NNW",
    "静穏": "CALM",
}

WEATHER_CODES = {0, 1, 2, 3, 10, 40, 50, 60, 70, 80, 85, 88, 90}


# ==========================================
# Data structures
# ==========================================

@dataclass(frozen=True)
class SourceCell:
    """原Excelの1セルから得た値と、特殊表現を示すフラグ。"""

    value: Any
    flag: str | None = None


@dataclass(frozen=True)
class ElementExtraction:
    """1観測要素について抽出した日時別セル。"""

    element_id: str
    cells: dict[tuple[int, int], SourceCell]


# ==========================================
# Source acquisition and integrity
# ==========================================

def load_source_manifest() -> dict[str, Any]:
    return yaml.safe_load(SOURCE_MANIFEST_PATH.read_text(encoding="utf-8"))


def sha256_digest(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source_file:
        for block in iter(lambda: source_file.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def prepare_source_files(
    source_directory: Path,
    download_missing: bool,
) -> tuple[dict[str, Path], list[dict[str, str]]]:
    """必要なExcelを揃え、マニフェストのSHA-256と照合する。"""

    manifest = load_source_manifest()
    source_directory.mkdir(parents=True, exist_ok=True)

    source_paths: dict[str, Path] = {}
    verification_rows: list[dict[str, str]] = []

    for source_entry in manifest["files"]:
        source_element = source_entry["element"]
        source_path = source_directory / SOURCE_FILE_NAMES[source_element]

        if not source_path.exists():
            if not download_missing:
                raise FileNotFoundError(
                    f"Source file is missing: {source_path}. "
                    "Use --download-missing to retrieve it from the manifest URL."
                )
            urllib.request.urlretrieve(source_entry["url"], source_path)

        actual_digest = sha256_digest(source_path)
        expected_digest = source_entry["sha256"]
        if actual_digest != expected_digest:
            raise ValueError(
                f"SHA-256 mismatch for {source_path.name}: "
                f"expected {expected_digest}, got {actual_digest}"
            )

        source_paths[source_element] = source_path
        verification_rows.append(
            {
                "element": source_element,
                "file": source_path.name,
                "sha256": actual_digest,
                "status": "verified",
            }
        )

    return source_paths, verification_rows


# ==========================================
# Cell conversion helpers
# ==========================================

def is_blank(value: Any) -> bool:
    return value is None or value == "" or (
        isinstance(value, float) and math.isnan(value)
    )


def source_cell(value: Any, *, integer: bool = False) -> SourceCell:
    """特殊表現を0へ変換せず、値とフラグへ分離する。"""

    if is_blank(value):
        return SourceCell(None, "source_blank")

    if isinstance(value, str):
        normalized = value.strip()
        if normalized == "-":
            return SourceCell(None, "source_dash")
        if normalized == "***":
            return SourceCell(None, "source_triple_asterisk")
        return SourceCell(normalized)

    if isinstance(value, (int, float)):
        # 観測値は1.0のような小数表現を保ち、コードだけ整数化する。
        numeric_value = int(value) if integer else float(value)
        return SourceCell(numeric_value)

    raise TypeError(f"Unsupported Excel cell value: {value!r}")


def open_first_twelve_sheets(path: Path) -> list[xlrd.sheet.Sheet]:
    workbook = xlrd.open_workbook(path)
    if workbook.nsheets < 12:
        raise ValueError(f"Expected at least 12 monthly sheets in {path.name}")
    return [workbook.sheet_by_index(index) for index in range(12)]


def integer_cell_value(sheet: xlrd.sheet.Sheet, row: int, column: int) -> int | None:
    value = sheet.cell_value(row, column)
    if isinstance(value, (int, float)) and float(value).is_integer():
        return int(value)
    if isinstance(value, str) and value.strip().isdigit():
        return int(value.strip())
    return None


def find_hour_header_row(
    sheet: xlrd.sheet.Sheet,
    expected_hours: list[int],
    *,
    start_row: int = 0,
) -> int:
    for row in range(start_row, min(sheet.nrows, start_row + 8)):
        actual_hours = [integer_cell_value(sheet, row, column) for column in range(1, len(expected_hours) + 1)]
        if actual_hours == expected_hours:
            return row
    raise ValueError(
        f"Could not find hour header {expected_hours[0]}-{expected_hours[-1]} "
        f"in sheet {sheet.name!r}"
    )


def find_title_row(sheet: xlrd.sheet.Sheet, title_fragment: str) -> int:
    for row in range(sheet.nrows):
        for column in range(sheet.ncols):
            if title_fragment in str(sheet.cell_value(row, column)):
                return row
    raise ValueError(f"Could not find title {title_fragment!r} in sheet {sheet.name!r}")


def read_day_rows(
    sheet: xlrd.sheet.Sheet,
    start_row: int,
    month: int,
) -> Iterable[tuple[int, int]]:
    """見出し後から、その月に存在する日だけを見つける。"""

    days_in_month = calendar.monthrange(YEAR, month)[1]
    found_days: set[int] = set()

    for row in range(start_row, sheet.nrows):
        day = integer_cell_value(sheet, row, 0)
        if day is None or not 1 <= day <= days_in_month or day in found_days:
            continue
        found_days.add(day)
        yield day, row
        if len(found_days) == days_in_month:
            return

    raise ValueError(
        f"Expected {days_in_month} daily rows in sheet {sheet.name!r}; "
        f"found {len(found_days)}"
    )


# ==========================================
# Workbook-specific extraction
# ==========================================

def extract_regular_hourly_element(
    path: Path,
    month: int,
    element_id: str,
    expected_hours: list[int],
) -> ElementExtraction:
    sheet = open_first_twelve_sheets(path)[month - 1]
    header_row = find_hour_header_row(sheet, expected_hours)
    cells: dict[tuple[int, int], SourceCell] = {}

    for day, row in read_day_rows(sheet, header_row + 1, month):
        for offset, hour in enumerate(expected_hours, start=1):
            cells[(day, hour)] = source_cell(sheet.cell_value(row, offset))

    return ElementExtraction(element_id, cells)


def extract_pressure_elements(path: Path, month: int) -> list[ElementExtraction]:
    sheet = open_first_twelve_sheets(path)[month - 1]
    expected_hours = list(range(1, 25))
    extractions: list[ElementExtraction] = []

    for title_fragment, element_id in (
        ("現地気圧", "station_pressure_hpa"),
        ("海面気圧", "sea_level_pressure_hpa"),
    ):
        title_row = find_title_row(sheet, title_fragment)
        header_row = find_hour_header_row(
            sheet,
            expected_hours,
            start_row=title_row + 1,
        )
        cells: dict[tuple[int, int], SourceCell] = {}
        for day, row in read_day_rows(sheet, header_row + 1, month):
            for hour in expected_hours:
                cells[(day, hour)] = source_cell(sheet.cell_value(row, hour))
        extractions.append(ElementExtraction(element_id, cells))

    return extractions


def extract_wind_direction(path: Path, month: int) -> ElementExtraction:
    raw = extract_regular_hourly_element(
        path,
        month,
        "wind_direction",
        list(range(1, 25)),
    )
    converted: dict[tuple[int, int], SourceCell] = {}

    for key, cell in raw.cells.items():
        if cell.value is None:
            converted[key] = cell
            continue
        if cell.value not in WIND_DIRECTION_CODES:
            raise ValueError(f"Unknown wind direction: {cell.value!r} at {key}")
        converted[key] = SourceCell(WIND_DIRECTION_CODES[cell.value], cell.flag)

    return ElementExtraction(raw.element_id, converted)


def extract_weather_at_noon(path: Path, month: int) -> ElementExtraction:
    workbook = xlrd.open_workbook(path)
    sheet = workbook.sheet_by_name("天気")
    code_column = 18 + month
    if integer_cell_value(sheet, 2, code_column) != month:
        raise ValueError(f"Could not locate weather code column for month {month}")

    cells: dict[tuple[int, int], SourceCell] = {}
    for day, row in read_day_rows(sheet, 4, month):
        cell = source_cell(sheet.cell_value(row, code_column), integer=True)
        if cell.value is not None and cell.value not in WEATHER_CODES:
            raise ValueError(f"Unknown weather code: {cell.value!r} on day {day}")
        cells[(day, 12)] = cell

    return ElementExtraction("weather_at_noon", cells)


def extract_all_elements(
    source_paths: dict[str, Path],
    month: int,
) -> list[ElementExtraction]:
    full_day_hours = list(range(1, 25))
    daylight_hours = list(range(4, 21))

    extractions = [
        extract_regular_hourly_element(
            source_paths["temperature"], month, "temperature_c", full_day_hours
        ),
        extract_regular_hourly_element(
            source_paths["humidity"], month, "relative_humidity_percent", full_day_hours
        ),
        extract_regular_hourly_element(
            source_paths["precipitation"], month, "precipitation_mm", full_day_hours
        ),
        *extract_pressure_elements(source_paths["pressure"], month),
        extract_regular_hourly_element(
            source_paths["solar_radiation"],
            month,
            "global_solar_radiation_mj_m2",
            daylight_hours,
        ),
        extract_regular_hourly_element(
            source_paths["sunshine_duration"],
            month,
            "sunshine_duration_h",
            daylight_hours,
        ),
        extract_regular_hourly_element(
            source_paths["wind_speed"], month, "wind_speed_m_s", full_day_hours
        ),
        extract_wind_direction(source_paths["wind_direction"], month),
        extract_regular_hourly_element(
            source_paths["dew_point_temperature"],
            month,
            "dew_point_temperature_c",
            full_day_hours,
        ),
        extract_weather_at_noon(source_paths["weather_at_noon"], month),
    ]
    return extractions


# ==========================================
# Canonical YAML assembly
# ==========================================

HOURLY_VALUE_ORDER = [
    "temperature_c",
    "relative_humidity_percent",
    "precipitation_mm",
    "station_pressure_hpa",
    "sea_level_pressure_hpa",
    "global_solar_radiation_mj_m2",
    "sunshine_duration_h",
    "wind_speed_m_s",
    "wind_direction",
    "dew_point_temperature_c",
]


def assemble_month_document(
    month: int,
    extractions: list[ElementExtraction],
) -> dict[str, Any]:
    days_in_month = calendar.monthrange(YEAR, month)[1]
    extraction_by_element = {
        extraction.element_id: extraction for extraction in extractions
    }
    observations: list[dict[str, Any]] = []

    for day in range(1, days_in_month + 1):
        source_date = date(YEAR, month, day).isoformat()
        for hour in range(1, 25):
            values: dict[str, Any] = {}
            flags: dict[str, str] = {}

            for element_id in HOURLY_VALUE_ORDER:
                extraction = extraction_by_element[element_id]
                cell = extraction.cells.get((day, hour), SourceCell(None))
                values[element_id] = cell.value
                if cell.flag is not None:
                    flags[element_id] = cell.flag

            if hour == 12:
                weather_cell = extraction_by_element["weather_at_noon"].cells[(day, hour)]
                values["weather_at_noon"] = weather_cell.value
                if weather_cell.flag is not None:
                    flags["weather_at_noon"] = weather_cell.flag

            observation: dict[str, Any] = {
                "source_date": source_date,
                "source_hour": hour,
                "values": values,
            }
            if flags:
                observation["flags"] = flags
            observations.append(observation)

    return {
        "schema_version": "0.1.0",
        "dataset": {
            "station_id": STATION_ID,
            "year": YEAR,
            "month": month,
            "timezone": "Asia/Tokyo",
            "source_manifest": "../../../metadata/sources/hitachi-city-hall-2025.yaml",
            "generator": GENERATOR_PATH,
        },
        "observations": observations,
        "notes": [
            "原資料の1時から24時という時刻表記をsource_hourへそのまま保存する。",
            "全天日射量と日照時間は、原資料に列がある4時から20時のみ値を収録する。",
            "降水量などの特殊表現は0に変換せず、nullとflagsへ分けて保存する。",
        ],
    }


class QuotedDateStringDumper(yaml.SafeDumper):
    """ISO日付をYAMLのtimestamp型に誤認させないためのDumper。"""

    def increase_indent(self, flow: bool = False, indentless: bool = False) -> None:
        # 配列を親キーより2字下げ、長い月別ファイルを目で追いやすくする。
        return super().increase_indent(flow, False)


def represent_string(dumper: yaml.SafeDumper, value: str) -> yaml.Node:
    style = '"' if len(value) == 10 and value[4] == "-" and value[7] == "-" else None
    return dumper.represent_scalar("tag:yaml.org,2002:str", value, style=style)


QuotedDateStringDumper.add_representer(str, represent_string)


def write_yaml(path: Path, document: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    yaml_text = yaml.dump(
        document,
        Dumper=QuotedDateStringDumper,
        allow_unicode=True,
        sort_keys=False,
        width=100,
    )
    path.write_text(yaml_text, encoding="utf-8")


# ==========================================
# Round-trip validation and report
# ==========================================

def count_element_cells(
    extraction: ElementExtraction,
) -> tuple[int, int, dict[str, int]]:
    non_null = sum(cell.value is not None for cell in extraction.cells.values())
    null_count = len(extraction.cells) - non_null
    flag_counts: dict[str, int] = {}
    for cell in extraction.cells.values():
        if cell.flag is not None:
            flag_counts[cell.flag] = flag_counts.get(cell.flag, 0) + 1
    return non_null, null_count, flag_counts


def validate_round_trip(
    yaml_path: Path,
    expected_document: dict[str, Any],
) -> None:
    parsed_document = yaml.safe_load(yaml_path.read_text(encoding="utf-8"))
    if parsed_document != expected_document:
        raise ValueError("Generated YAML did not survive a YAML round trip unchanged")


def write_validation_report(
    report_path: Path,
    month: int,
    yaml_path: Path,
    document: dict[str, Any],
    extractions: list[ElementExtraction],
    source_verification_rows: list[dict[str, str]],
) -> None:
    days_in_month = calendar.monthrange(YEAR, month)[1]
    record_count = days_in_month * 24

    lines = [
        f"# {YEAR}年{month}月データ検証報告",
        "",
        "## 検証結果",
        "",
        "- 判定：合格",
        f"- 生成ファイル：`{yaml_path.relative_to(REPOSITORY_ROOT)}`",
        f"- 日数：{days_in_month}",
        f"- 時間観測レコード数：{record_count}",
        "- YAML再読込：成功（生成直前のデータ構造と一致）",
        "- 原ExcelのSHA-256：10ファイルすべて一致",
        "",
        "## 観測要素別の抽出件数",
        "",
        "| 観測要素 | 原資料上のセル数 | 値あり | null | フラグ |",
        "|---|---:|---:|---:|---|",
    ]

    for extraction in extractions:
        non_null, null_count, flag_counts = count_element_cells(extraction)
        flags_text = ", ".join(
            f"`{flag}`: {count}" for flag, count in sorted(flag_counts.items())
        ) or "—"
        lines.append(
            f"| `{extraction.element_id}` | {len(extraction.cells)} | "
            f"{non_null} | {null_count} | {flags_text} |"
        )

    observation_index = {
        (observation["source_date"], observation["source_hour"]): observation
        for observation in document["observations"]
    }
    first_hour = observation_index[(f"{YEAR}-{month:02d}-01", 1)]["values"]
    noon = observation_index[(f"{YEAR}-{month:02d}-01", 12)]["values"]

    lines.extend(
        [
            "",
            "## 原Excelの整合性確認",
            "",
            "| 要素 | ファイル | SHA-256 | 判定 |",
            "|---|---|---|---|",
        ]
    )
    for row in source_verification_rows:
        lines.append(
            f"| `{row['element']}` | `{row['file']}` | "
            f"`{row['sha256']}` | {row['status']} |"
        )

    lines.extend(
        [
            "",
            "## 代表値の確認",
            "",
            "次の値は、原Excelと生成YAMLの双方で一致することを確認した。",
            "",
            "| 原資料上の日時 | 気温 | 湿度 | 現地気圧 | 海面気圧 | 風速 | 風向 | 露点 | 天気 |",
            "|---|---:|---:|---:|---:|---:|---|---:|---:|",
            f"| {YEAR}-{month:02d}-01 1時 | {first_hour['temperature_c']} | "
            f"{first_hour['relative_humidity_percent']} | {first_hour['station_pressure_hpa']} | "
            f"{first_hour['sea_level_pressure_hpa']} | {first_hour['wind_speed_m_s']} | "
            f"{first_hour['wind_direction']} | {first_hour['dew_point_temperature_c']} | — |",
            f"| {YEAR}-{month:02d}-01 12時 | {noon['temperature_c']} | "
            f"{noon['relative_humidity_percent']} | {noon['station_pressure_hpa']} | "
            f"{noon['sea_level_pressure_hpa']} | {noon['wind_speed_m_s']} | "
            f"{noon['wind_direction']} | {noon['dew_point_temperature_c']} | "
            f"{noon['weather_at_noon']} |",
            "",
            "## 現段階での保留事項",
            "",
            "- 1時から24時の各値が示す観測・集計区間は、原資料の表記を維持した。",
            "- 降水量の空欄は0と断定せず、`null`と`source_blank`で保存した。",
            "- 日別集計値はこの段階では収録せず、時間観測値とは別の工程で扱う。",
            "",
        ]
    )

    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(lines), encoding="utf-8")


# ==========================================
# Command-line interface
# ==========================================

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="日立市役所観測所の2025年Excelを月別YAMLへ変換する。"
    )
    parser.add_argument("--month", type=int, required=True, choices=range(1, 13))
    parser.add_argument(
        "--source-directory",
        type=Path,
        default=REPOSITORY_ROOT / "build" / "source-2025",
    )
    parser.add_argument(
        "--download-missing",
        action="store_true",
        help="不足するExcelをsource manifestのURLから取得する。",
    )
    return parser.parse_args()


def main() -> int:
    arguments = parse_arguments()
    source_paths, source_verification_rows = prepare_source_files(
        arguments.source_directory,
        arguments.download_missing,
    )
    extractions = extract_all_elements(source_paths, arguments.month)
    document = assemble_month_document(arguments.month, extractions)

    yaml_path = (
        REPOSITORY_ROOT
        / "data"
        / STATION_ID
        / str(YEAR)
        / f"{arguments.month:02d}.yaml"
    )
    report_path = (
        REPOSITORY_ROOT
        / "reports"
        / f"validation-{YEAR}-{arguments.month:02d}.md"
    )

    write_yaml(yaml_path, document)
    validate_round_trip(yaml_path, document)
    write_validation_report(
        report_path,
        arguments.month,
        yaml_path,
        document,
        extractions,
        source_verification_rows,
    )

    print(f"Generated: {yaml_path.relative_to(REPOSITORY_ROOT)}")
    print(f"Validated: {report_path.relative_to(REPOSITORY_ROOT)}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (FileNotFoundError, TypeError, ValueError, xlrd.XLRDError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(1)
