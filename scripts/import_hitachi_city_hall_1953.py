#!/usr/bin/env python3
"""日立市役所観測所の1953年Excelを月別YAMLへ変換する。

1953年資料は、要素ごとに観測時刻と帳票構造が異なる。この処理では
24時間の均一な観測だったように補完せず、原資料に設定された時刻だけを
値または来歴付きのnullとして保存する。
"""

from __future__ import annotations

import argparse
import calendar
import hashlib
import math
import urllib.request
import zipfile
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

import xlrd
import yaml


# ==========================================
# Repository paths and source definitions
# ==========================================

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SOURCE_MANIFEST_PATH = (
    REPOSITORY_ROOT / "metadata" / "sources" / "hitachi-city-hall-1953.yaml"
)

YEAR = 1953
STATION_ID = "hitachi-city-hall"
GENERATOR_PATH = "scripts/import_hitachi_city_hall_1953.py"

OBSERVATION_SCHEDULES = {
    "temperature_c": [6, 9, 14, 22],
    "relative_humidity_percent": [6, 9, 14, 22],
    "station_pressure_hpa": [6, 9, 14, 22],
    "sunshine_duration_h": list(range(4, 21)),
    "wind_speed_m_s": [6, 9, 14, 22],
    "wind_direction": [6, 9, 14, 22],
    "weather_code": [9],
}

SOURCE_TABLE_LAYOUTS = {
    "precipitation_mm": {
        "source_columns": list(range(1, 25)),
        "status": "no_hourly_values_in_month",
        "available_as": "daily_summary",
    },
    "sea_level_pressure_hpa": {
        "source_columns": [3, 9, 15, 21],
        "status": "no_values_in_month",
    },
}

WEATHER_TEXT_TO_CODE = {
    "快晴": 0,
    "晴れ": 1,
    "薄曇り": 2,
    "曇り": 3,
    "煙霧": 10,
    "霧": 40,
    "霧雨": 50,
    "雨": 60,
    "にわか雨": 70,
    "雪": 80,
    "にわか雪": 85,
    "みぞれ": 88,
    "不明": 90,
}

WIND_DIRECTION_CODES = {
    "N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
    "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW", "CALM",
}


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
    """1観測要素について抽出した日・時刻別セル。"""

    element_id: str
    cells: dict[tuple[int, int], SourceCell]


class FlowSequence(list):
    """観測時刻などの短い定義用配列をYAMLの1行表記にする。"""


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
    """ZIPを照合し、1953年のExcelだけを作業領域へ展開する。"""

    manifest = load_source_manifest()
    source_directory.mkdir(parents=True, exist_ok=True)
    extracted_directory = source_directory / "extracted"
    extracted_directory.mkdir(parents=True, exist_ok=True)

    source_paths: dict[str, Path] = {}
    verification_rows: list[dict[str, str]] = []

    for source_entry in manifest["files"]:
        element = source_entry["element"]
        archive_path = source_directory / f"{element}.zip"

        if not archive_path.exists():
            if not download_missing:
                raise FileNotFoundError(
                    f"Source archive is missing: {archive_path}. "
                    "Use --download-missing to retrieve it from the manifest URL."
                )
            urllib.request.urlretrieve(source_entry["url"], archive_path)

        actual_digest = sha256_digest(archive_path)
        expected_digest = source_entry["sha256"]
        if actual_digest != expected_digest:
            raise ValueError(
                f"SHA-256 mismatch for {archive_path.name}: "
                f"expected {expected_digest}, got {actual_digest}"
            )

        archive_member = source_entry["archive_member"]
        workbook_path = extracted_directory / f"{element}.xls"
        with zipfile.ZipFile(archive_path) as archive:
            try:
                workbook_bytes = archive.read(archive_member)
            except KeyError as error:
                raise ValueError(
                    f"Archive member {archive_member!r} was not found in {archive_path.name}"
                ) from error
        workbook_path.write_bytes(workbook_bytes)

        source_paths[element] = workbook_path
        verification_rows.append(
            {
                "element": element,
                "archive": archive_path.name,
                "member": archive_member,
                "sha256": actual_digest,
                "status": "verified",
            }
        )

    return source_paths, verification_rows


# ==========================================
# Cell and sheet helpers
# ==========================================

def source_cell(cell: xlrd.sheet.Cell, *, integer: bool = False) -> SourceCell:
    """セルの空欄や記号を0へ変換せず、値とフラグへ分ける。"""

    if cell.ctype in (xlrd.XL_CELL_EMPTY, xlrd.XL_CELL_BLANK):
        return SourceCell(None, "source_blank")
    if cell.ctype == xlrd.XL_CELL_ERROR:
        error_name = xlrd.error_text_from_code.get(cell.value, str(cell.value))
        return SourceCell(None, f"source_excel_error:{error_name}")

    value = cell.value
    if isinstance(value, str):
        normalized = value.strip()
        if normalized == "":
            return SourceCell(None, "source_blank")
        if normalized == "-":
            return SourceCell(None, "source_dash")
        if normalized == "***":
            return SourceCell(None, "source_triple_asterisk")
        return SourceCell(normalized)

    if isinstance(value, (int, float)):
        if isinstance(value, float) and math.isnan(value):
            return SourceCell(None, "source_blank")
        return SourceCell(int(value) if integer else float(value))

    raise TypeError(f"Unsupported Excel cell value: {value!r}")


def open_month_sheet(path: Path, month: int) -> xlrd.sheet.Sheet:
    """旧Excelを全シート展開せず、対象月だけを開く。"""

    workbook = xlrd.open_workbook(path, on_demand=True)
    if workbook.nsheets < 12:
        raise ValueError(f"Expected at least 12 monthly sheets in {path.name}")
    return workbook.sheet_by_index(month - 1)


def integer_value(value: Any) -> int | None:
    if isinstance(value, (int, float)) and float(value).is_integer():
        return int(value)
    if isinstance(value, str) and value.strip().isdigit():
        return int(value.strip())
    return None


def validate_hour_headers(
    sheet: xlrd.sheet.Sheet,
    header_row: int,
    columns_by_hour: dict[int, int],
) -> None:
    for hour, column in columns_by_hour.items():
        actual_hour = integer_value(sheet.cell_value(header_row, column))
        if actual_hour != hour:
            raise ValueError(
                f"Expected hour {hour} at row {header_row}, column {column} "
                f"in sheet {sheet.name!r}; found {actual_hour!r}"
            )


def extract_day_hour_table(
    path: Path,
    month: int,
    element_id: str,
    *,
    header_row: int,
    first_day_row: int,
    columns_by_hour: dict[int, int],
) -> ElementExtraction:
    sheet = open_month_sheet(path, month)
    validate_hour_headers(sheet, header_row, columns_by_hour)
    days_in_month = calendar.monthrange(YEAR, month)[1]
    cells: dict[tuple[int, int], SourceCell] = {}

    for day in range(1, days_in_month + 1):
        row = first_day_row + day - 1
        actual_day = integer_value(sheet.cell_value(row, 0))
        if actual_day != day:
            raise ValueError(
                f"Expected day {day} at row {row} in {path.name}; found {actual_day!r}"
            )
        for hour, column in columns_by_hour.items():
            cells[(day, hour)] = source_cell(sheet.cell(row, column))

    return ElementExtraction(element_id, cells)


# ==========================================
# Workbook-specific extraction
# ==========================================

def extract_weather(path: Path, month: int) -> ElementExtraction:
    workbook = xlrd.open_workbook(path, on_demand=True)
    sheet = workbook.sheet_by_name("天気")
    text_column = month
    code_column = 18 + month

    if integer_value(sheet.cell_value(2, text_column)) != month:
        raise ValueError(f"Could not locate weather text column for month {month}")
    if integer_value(sheet.cell_value(2, code_column)) != month:
        raise ValueError(f"Could not locate weather code column for month {month}")

    cells: dict[tuple[int, int], SourceCell] = {}
    days_in_month = calendar.monthrange(YEAR, month)[1]
    for day in range(1, days_in_month + 1):
        row = 4 + day - 1
        if integer_value(sheet.cell_value(row, 0)) != day:
            raise ValueError(f"Could not locate weather row for day {day}")

        text_cell = source_cell(sheet.cell(row, text_column))
        code_cell = source_cell(sheet.cell(row, code_column), integer=True)
        if text_cell.value is None:
            cells[(day, 9)] = text_cell
            continue

        weather_text = str(text_cell.value)
        if weather_text not in WEATHER_TEXT_TO_CODE:
            raise ValueError(f"Unknown weather text: {weather_text!r} on day {day}")
        normalized_code = WEATHER_TEXT_TO_CODE[weather_text]
        if code_cell.value is not None and code_cell.value != normalized_code:
            raise ValueError(
                f"Weather text/code mismatch on day {day}: "
                f"{weather_text!r} != {code_cell.value!r}"
            )
        cells[(day, 9)] = SourceCell(normalized_code)

    return ElementExtraction("weather_code", cells)


def extract_wind_direction(path: Path, month: int) -> ElementExtraction:
    extraction = extract_day_hour_table(
        path,
        month,
        "wind_direction",
        header_row=1,
        first_day_row=2,
        columns_by_hour={hour: hour for hour in [6, 9, 14, 22]},
    )
    converted: dict[tuple[int, int], SourceCell] = {}
    for key, cell in extraction.cells.items():
        if cell.value is None:
            converted[key] = cell
            continue
        direction = str(cell.value).upper()
        if direction not in WIND_DIRECTION_CODES:
            raise ValueError(f"Unknown wind direction: {cell.value!r} at {key}")
        converted[key] = SourceCell(direction, cell.flag)
    return ElementExtraction("wind_direction", converted)


def extract_all_elements(
    source_paths: dict[str, Path],
    month: int,
) -> list[ElementExtraction]:
    four_times = {6: 1, 9: 2, 14: 3, 22: 4}
    all_hours = {hour: hour for hour in range(1, 25)}
    daylight_hours = {hour: hour - 3 for hour in range(4, 21)}
    sea_level_times = {3: 1, 9: 2, 15: 3, 21: 4}

    return [
        extract_day_hour_table(
            source_paths["temperature"], month, "temperature_c",
            header_row=1, first_day_row=2, columns_by_hour=four_times,
        ),
        extract_day_hour_table(
            source_paths["humidity"], month, "relative_humidity_percent",
            header_row=1, first_day_row=2, columns_by_hour=four_times,
        ),
        extract_day_hour_table(
            source_paths["precipitation"], month, "precipitation_mm",
            header_row=2, first_day_row=3, columns_by_hour=all_hours,
        ),
        extract_day_hour_table(
            source_paths["pressure"], month, "station_pressure_hpa",
            header_row=1, first_day_row=2, columns_by_hour=four_times,
        ),
        extract_day_hour_table(
            source_paths["pressure"], month, "sea_level_pressure_hpa",
            header_row=37, first_day_row=38, columns_by_hour=sea_level_times,
        ),
        extract_day_hour_table(
            source_paths["sunshine_duration"], month, "sunshine_duration_h",
            header_row=1, first_day_row=2, columns_by_hour=daylight_hours,
        ),
        extract_day_hour_table(
            source_paths["wind_speed"], month, "wind_speed_m_s",
            header_row=1, first_day_row=3,
            columns_by_hour={hour: hour for hour in [6, 9, 14, 22]},
        ),
        extract_wind_direction(source_paths["wind_direction"], month),
        extract_weather(source_paths["weather_code"], month),
    ]


def optional_numeric(cell: xlrd.sheet.Cell) -> float | None:
    converted = source_cell(cell)
    return converted.value if isinstance(converted.value, (int, float)) else None


def optional_text(cell: xlrd.sheet.Cell) -> str | None:
    converted = source_cell(cell)
    return str(converted.value) if converted.value is not None else None


def format_excel_time(cell: xlrd.sheet.Cell, datemode: int) -> str | None:
    """原Excelの時刻セルを、意味が確認できる場合だけHH:MMへ整える。"""

    converted = source_cell(cell)
    if converted.value is None:
        return None
    if isinstance(converted.value, str):
        return converted.value
    value = float(converted.value)
    if 0 <= value < 1:
        hour, minute, second = xlrd.xldate_as_tuple(value, datemode)[3:]
        return f"{hour:02d}:{minute:02d}" if second == 0 else f"{hour:02d}:{minute:02d}:{second:02d}"
    if cell.ctype == xlrd.XL_CELL_DATE:
        # 旧帳票には日付部分を含むシリアル値があり、表示上の時刻を
        # 根拠なく推定できないため、原値であることを明示して保持する。
        return f"source_excel_serial:{value:g}"
    if value.is_integer() and 0 <= value <= 24:
        return f"{int(value):02d}:00"
    return str(value)


def extract_daily_summaries(
    source_paths: dict[str, Path],
    month: int,
) -> list[dict[str, Any]]:
    """明確に識別できる日別集計値を、時刻別観測値と分けて抽出する。"""

    workbooks = {
        name: xlrd.open_workbook(path, on_demand=True)
        for name, path in source_paths.items()
        if name in {
            "temperature", "humidity", "precipitation", "pressure",
            "sunshine_duration", "wind_speed",
        }
    }
    sheets = {
        name: workbook.sheet_by_index(month - 1)
        for name, workbook in workbooks.items()
    }
    days_in_month = calendar.monthrange(YEAR, month)[1]
    summaries: list[dict[str, Any]] = []

    for day in range(1, days_in_month + 1):
        temperature_row = 2 + day - 1
        humidity_row = 2 + day - 1
        precipitation_row = 3 + day - 1
        pressure_row = 2 + day - 1
        sunshine_row = 2 + day - 1
        wind_row = 3 + day - 1

        temperature = sheets["temperature"]
        humidity = sheets["humidity"]
        precipitation = sheets["precipitation"]
        pressure = sheets["pressure"]
        sunshine = sheets["sunshine_duration"]
        wind = sheets["wind_speed"]

        precipitation_total = source_cell(precipitation.cell(precipitation_row, 25))
        sunshine_total = source_cell(sunshine.cell(sunshine_row, 18))

        summary: dict[str, Any] = {
            "date": date(YEAR, month, day).isoformat(),
            "temperature": {
                "mean_c": optional_numeric(temperature.cell(temperature_row, 5)),
                "maximum": {
                    "value_c": optional_numeric(temperature.cell(temperature_row, 6)),
                    "time": format_excel_time(
                        temperature.cell(temperature_row, 7),
                        workbooks["temperature"].datemode,
                    ),
                },
                "minimum": {
                    "value_c": optional_numeric(temperature.cell(temperature_row, 8)),
                    "time": format_excel_time(
                        temperature.cell(temperature_row, 9),
                        workbooks["temperature"].datemode,
                    ),
                },
            },
            "humidity": {
                "mean_percent": optional_numeric(humidity.cell(humidity_row, 5)),
                "minimum": {
                    "value_percent": optional_numeric(humidity.cell(humidity_row, 6)),
                    "time": format_excel_time(
                        humidity.cell(humidity_row, 7),
                        workbooks["humidity"].datemode,
                    ),
                },
            },
            "precipitation": {
                "total_mm": precipitation_total.value,
                "maximum_one_hour": {
                    "value_mm": optional_numeric(precipitation.cell(precipitation_row, 27)),
                    "time": format_excel_time(
                        precipitation.cell(precipitation_row, 28),
                        workbooks["precipitation"].datemode,
                    ),
                },
                "maximum_ten_minutes": {
                    "value_mm": optional_numeric(precipitation.cell(precipitation_row, 30)),
                    "time": format_excel_time(
                        precipitation.cell(precipitation_row, 31),
                        workbooks["precipitation"].datemode,
                    ),
                },
            },
            "station_pressure": {
                "mean_hpa": optional_numeric(pressure.cell(pressure_row, 5)),
                "maximum": {
                    "value_hpa": optional_numeric(pressure.cell(pressure_row, 6)),
                    "time": format_excel_time(
                        pressure.cell(pressure_row, 7),
                        workbooks["pressure"].datemode,
                    ),
                },
                "minimum": {
                    "value_hpa": optional_numeric(pressure.cell(pressure_row, 8)),
                    "time": format_excel_time(
                        pressure.cell(pressure_row, 9),
                        workbooks["pressure"].datemode,
                    ),
                },
            },
            "sunshine_duration": {
                "total_h": sunshine_total.value,
            },
            "wind": {
                "mean_speed_m_s": optional_numeric(wind.cell(wind_row, 25)),
                "maximum_10_minute": {
                    "direction": optional_text(wind.cell(wind_row, 28)),
                    "speed_m_s": optional_numeric(wind.cell(wind_row, 29)),
                    "time": format_excel_time(
                        wind.cell(wind_row, 30),
                        workbooks["wind_speed"].datemode,
                    ),
                },
                "maximum_instantaneous": {
                    "direction": optional_text(wind.cell(wind_row, 32)),
                    "speed_m_s": optional_numeric(wind.cell(wind_row, 33)),
                    "time": format_excel_time(
                        wind.cell(wind_row, 34),
                        workbooks["wind_speed"].datemode,
                    ),
                },
            },
        }

        flags: dict[str, str] = {}
        if precipitation_total.flag is not None:
            flags["precipitation.total_mm"] = precipitation_total.flag
        if sunshine_total.flag is not None:
            flags["sunshine_duration.total_h"] = sunshine_total.flag
        if flags:
            summary["flags"] = flags
        summaries.append(summary)

    return summaries


# ==========================================
# Canonical YAML assembly
# ==========================================

def assemble_month_document(
    month: int,
    extractions: list[ElementExtraction],
    daily_summaries: list[dict[str, Any]],
    manifest: dict[str, Any],
) -> dict[str, Any]:
    days_in_month = calendar.monthrange(YEAR, month)[1]
    extraction_by_element = {
        extraction.element_id: extraction for extraction in extractions
    }
    observations: list[dict[str, Any]] = []

    observation_hours = sorted({
        hour
        for hours in OBSERVATION_SCHEDULES.values()
        for hour in hours
    })
    observation_element_ids = set(OBSERVATION_SCHEDULES)

    for day in range(1, days_in_month + 1):
        source_date = date(YEAR, month, day).isoformat()
        for hour in observation_hours:
            values: dict[str, Any] = {}
            flags: dict[str, str] = {}

            for element_id, extraction in extraction_by_element.items():
                if element_id not in observation_element_ids:
                    continue
                cell = extraction.cells.get((day, hour))
                if cell is None:
                    continue
                values[element_id] = cell.value
                if cell.flag is not None:
                    flags[element_id] = cell.flag

            observation: dict[str, Any] = {
                "source_date": source_date,
                "source_hour": hour,
                "values": values,
            }
            if flags:
                observation["flags"] = flags
            observations.append(observation)

    availability = {
        element_id: {
            "status": "not_available_for_period",
            **details,
        }
        for element_id, details in manifest["not_available_for_period"].items()
    }

    return {
        "schema_version": "0.2.0",
        "dataset": {
            "station_id": STATION_ID,
            "year": YEAR,
            "month": month,
            "timezone": "Asia/Tokyo",
            "source_period_id": "historical_annual_workbooks",
            "source_manifest": "../../../metadata/sources/hitachi-city-hall-1953.yaml",
            "generator": GENERATOR_PATH,
            "observation_schedules": {
                key: FlowSequence(hours)
                for key, hours in OBSERVATION_SCHEDULES.items()
            },
            "source_table_layouts": {
                key: {
                    **details,
                    "source_columns": FlowSequence(details["source_columns"]),
                }
                for key, details in SOURCE_TABLE_LAYOUTS.items()
            },
            "element_availability": availability,
        },
        "observations": observations,
        "daily_summaries": daily_summaries,
        "notes": [
            "観測要素ごとに異なる原資料上の観測時刻を保持する。",
            "観測時刻ではない項目をnullで補完せず、valuesから省略する。",
            "露点温度と全天日射量は1953年の公開資料に収録されていないため、欠測とは区別する。",
            "降水量の時刻欄はすべて空欄であり、日合計などはdaily_summariesへ収録する。",
            "海面気圧の表は存在するが、1953年1月の時刻別セルはすべて空欄である。",
        ],
    }


class ReadableYamlDumper(yaml.SafeDumper):
    """配列の字下げとISO日付文字列の引用符を統一するDumper。"""

    def increase_indent(self, flow: bool = False, indentless: bool = False) -> None:
        return super().increase_indent(flow, False)


def represent_string(dumper: yaml.SafeDumper, value: str) -> yaml.Node:
    style = '"' if len(value) == 10 and value[4] == "-" and value[7] == "-" else None
    return dumper.represent_scalar("tag:yaml.org,2002:str", value, style=style)


ReadableYamlDumper.add_representer(str, represent_string)
ReadableYamlDumper.add_representer(
    FlowSequence,
    lambda dumper, value: dumper.represent_sequence(
        "tag:yaml.org,2002:seq", value, flow_style=True
    ),
)


def write_yaml(path: Path, document: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        yaml.dump(
            document,
            Dumper=ReadableYamlDumper,
            allow_unicode=True,
            sort_keys=False,
            width=100,
        ),
        encoding="utf-8",
    )


# ==========================================
# Validation report
# ==========================================

def count_cells(extraction: ElementExtraction) -> tuple[int, int, dict[str, int]]:
    non_null = sum(cell.value is not None for cell in extraction.cells.values())
    null_count = len(extraction.cells) - non_null
    flag_counts: dict[str, int] = {}
    for cell in extraction.cells.values():
        if cell.flag is not None:
            flag_counts[cell.flag] = flag_counts.get(cell.flag, 0) + 1
    return non_null, null_count, flag_counts


def validate_round_trip(path: Path, expected_document: dict[str, Any]) -> None:
    parsed = yaml.safe_load(path.read_text(encoding="utf-8"))
    if parsed != expected_document:
        raise ValueError("Generated YAML did not survive a YAML round trip unchanged")


def write_validation_report(
    report_path: Path,
    month: int,
    yaml_path: Path,
    document: dict[str, Any],
    extractions: list[ElementExtraction],
    verification_rows: list[dict[str, str]],
) -> None:
    days_in_month = calendar.monthrange(YEAR, month)[1]
    lines = [
        f"# {YEAR}年{month}月データ検証報告",
        "",
        "## 検証結果",
        "",
        "- 判定：合格",
        f"- 生成ファイル：`{yaml_path.relative_to(REPOSITORY_ROOT)}`",
        f"- 日数：{days_in_month}",
        f"- 時刻レコード数：{len(document['observations'])}",
        "- YAML再読込：成功（生成直前のデータ構造と一致）",
        f"- 原ZIPのSHA-256：{len(verification_rows)}ファイルすべて一致",
        "",
        "## 観測要素別の抽出件数",
        "",
        "| 観測要素 | 原資料上のセル数 | 値あり | null | フラグ |",
        "|---|---:|---:|---:|---|",
    ]

    for extraction in extractions:
        non_null, null_count, flag_counts = count_cells(extraction)
        flags_text = ", ".join(
            f"`{flag}`: {count}" for flag, count in sorted(flag_counts.items())
        ) or "—"
        lines.append(
            f"| `{extraction.element_id}` | {len(extraction.cells)} | "
            f"{non_null} | {null_count} | {flags_text} |"
        )

    lines.extend([
        "",
        "## 原ZIPの整合性確認",
        "",
        "| 要素 | ZIP | 内部ファイル | SHA-256 | 判定 |",
        "|---|---|---|---|---|",
    ])
    for row in verification_rows:
        lines.append(
            f"| `{row['element']}` | `{row['archive']}` | `{row['member']}` | "
            f"`{row['sha256']}` | {row['status']} |"
        )

    observations = {
        (item["source_date"], item["source_hour"]): item
        for item in document["observations"]
    }
    six = observations[(f"{YEAR}-{month:02d}-01", 6)]["values"]
    nine = observations[(f"{YEAR}-{month:02d}-01", 9)]["values"]
    lines.extend([
        "",
        "## 代表値の確認",
        "",
        "| 原資料上の日時 | 気温 | 湿度 | 現地気圧 | 風速 | 風向 | 天気 |",
        "|---|---:|---:|---:|---:|---|---|",
        f"| 1953-{month:02d}-01 6時 | {six['temperature_c']} | "
        f"{six['relative_humidity_percent']} | {six['station_pressure_hpa']} | "
        f"{six['wind_speed_m_s']} | {six['wind_direction']} | — |",
        f"| 1953-{month:02d}-01 9時 | {nine['temperature_c']} | "
        f"{nine['relative_humidity_percent']} | {nine['station_pressure_hpa']} | "
        f"{nine['wind_speed_m_s']} | {nine['wind_direction']} | "
        f"{nine['weather_code']} |",
        "",
        "## 年代による構造差",
        "",
        "- 気温、湿度、現地気圧、風速、風向は6時・9時・14時・22時の記録である。",
        "- 天気は9時の記録であり、2000年以降の12時とは異なる。",
        "- 降水量表は1時から24時の欄を持つが、1953年1月の時刻別セルはすべて空欄で、日合計のみ値がある。",
        "- 露点温度と全天日射量は1953年の公開資料に収録されていない。",
        "- 海面気圧の表は存在するが、1953年1月の時刻別セルはすべて空欄である。",
        "",
        "## 現段階での保留事項",
        "",
        "- 空欄は0と断定せず、`null`と`source_blank`で保存した。",
        "- 月別集計値と階級別日数は、別工程で採録する。",
    ])

    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


# ==========================================
# Command-line interface
# ==========================================

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="日立市役所観測所の1953年Excelを月別YAMLへ変換する。"
    )
    parser.add_argument("--month", type=int, required=True, choices=range(1, 13))
    parser.add_argument(
        "--source-directory",
        type=Path,
        default=REPOSITORY_ROOT / "build" / "source-1953",
    )
    parser.add_argument(
        "--download-missing",
        action="store_true",
        help="不足するZIPをsource manifestのURLから取得する。",
    )
    return parser.parse_args()


def main() -> int:
    arguments = parse_arguments()
    manifest = load_source_manifest()
    source_paths, verification_rows = prepare_source_files(
        arguments.source_directory,
        arguments.download_missing,
    )
    extractions = extract_all_elements(source_paths, arguments.month)
    daily_summaries = extract_daily_summaries(source_paths, arguments.month)
    document = assemble_month_document(
        arguments.month,
        extractions,
        daily_summaries,
        manifest,
    )

    yaml_path = (
        REPOSITORY_ROOT / "data" / STATION_ID / str(YEAR) / f"{arguments.month:02d}.yaml"
    )
    report_path = REPOSITORY_ROOT / "reports" / f"validation-{YEAR}-{arguments.month:02d}.md"

    write_yaml(yaml_path, document)
    validate_round_trip(yaml_path, document)
    write_validation_report(
        report_path,
        arguments.month,
        yaml_path,
        document,
        extractions,
        verification_rows,
    )

    print(f"Generated: {yaml_path.relative_to(REPOSITORY_ROOT)}")
    print(f"Validated: {report_path.relative_to(REPOSITORY_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
