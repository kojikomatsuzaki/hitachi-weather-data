#!/usr/bin/env python3
"""日立市役所観測所の2014年Excelを月別YAMLへ変換する。

2014年の帳票は、時間観測値については2025年版と同じ基本構造を持つ。
一方、12時の天気は数値コードではなく日本語で記録されているため、
その差だけを明示的に処理し、共通処理は2025年版の取込処理を再利用する。
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import xlrd

import import_hitachi_city_hall_2025 as common


# ==========================================
# 2014 source configuration
# ==========================================

YEAR = 2014
REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SOURCE_MANIFEST_PATH = (
    REPOSITORY_ROOT / "metadata" / "sources" / "hitachi-city-hall-2014.yaml"
)

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


# ==========================================
# 2014 weather representation
# ==========================================

def extract_weather_at_noon_2014(
    path: Path,
    month: int,
) -> common.ElementExtraction:
    """日本語表記の12時天気を共通語彙の数値コードへ正規化する。"""

    workbook = xlrd.open_workbook(path)
    sheet = workbook.sheet_by_name("天気")
    weather_column = month

    header_value = str(sheet.cell_value(2, weather_column)).strip()
    if header_value != str(month):
        raise ValueError(f"Could not locate weather column for month {month}")

    cells: dict[tuple[int, int], common.SourceCell] = {}
    for day, row in common.read_day_rows(sheet, 4, month):
        raw_cell = common.source_cell(sheet.cell_value(row, weather_column))
        if raw_cell.value is None:
            cells[(day, 12)] = raw_cell
            continue

        weather_text = str(raw_cell.value).strip()
        if weather_text not in WEATHER_TEXT_TO_CODE:
            raise ValueError(f"Unknown weather text: {weather_text!r} on day {day}")
        cells[(day, 12)] = common.SourceCell(
            WEATHER_TEXT_TO_CODE[weather_text],
            raw_cell.flag,
        )

    return common.ElementExtraction("weather_at_noon", cells)


# ==========================================
# Command-line interface
# ==========================================

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="日立市役所観測所の2014年Excelを月別YAMLへ変換する。"
    )
    parser.add_argument("--month", type=int, required=True, choices=range(1, 13))
    parser.add_argument(
        "--source-directory",
        type=Path,
        default=REPOSITORY_ROOT / "build" / "source-2014",
    )
    parser.add_argument(
        "--download-missing",
        action="store_true",
        help="不足するExcelをsource manifestのURLから取得する。",
    )
    return parser.parse_args()


def configure_common_processing() -> None:
    """共通処理へ、2014年固有の年・来歴・天気表記を注入する。"""

    common.YEAR = YEAR
    common.SOURCE_MANIFEST_PATH = SOURCE_MANIFEST_PATH
    common.GENERATOR_PATH = "scripts/import_hitachi_city_hall_2014.py"
    common.extract_weather_at_noon = extract_weather_at_noon_2014


def main() -> int:
    arguments = parse_arguments()
    configure_common_processing()

    source_paths, source_verification_rows = common.prepare_source_files(
        arguments.source_directory,
        arguments.download_missing,
    )
    extractions = common.extract_all_elements(source_paths, arguments.month)
    document = common.assemble_month_document(arguments.month, extractions)
    document["dataset"]["source_manifest"] = (
        "../../../metadata/sources/hitachi-city-hall-2014.yaml"
    )
    document["notes"].append(
        "12時の天気は原資料の日本語表記を共通語彙の数値コードへ正規化した。"
    )

    yaml_path = (
        REPOSITORY_ROOT
        / "data"
        / common.STATION_ID
        / str(YEAR)
        / f"{arguments.month:02d}.yaml"
    )
    report_path = REPOSITORY_ROOT / "reports" / f"validation-{YEAR}-{arguments.month:02d}.md"

    common.write_yaml(yaml_path, document)
    common.validate_round_trip(yaml_path, document)
    common.write_validation_report(
        report_path,
        arguments.month,
        yaml_path,
        document,
        extractions,
        source_verification_rows,
    )
    with report_path.open("a", encoding="utf-8") as report_file:
        report_file.write(
            "\n## 2025年版との形式差\n\n"
            "- 時間観測値の月別シートと時刻列は、2025年版の共通処理で抽出できた。\n"
            "- 12時の天気は、2025年版の数値コードに対して、2014年版では日本語表記だった。\n"
            "- 日本語の天気表記は `metadata/elements.yaml` の共通語彙へ対応付けた。\n"
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
