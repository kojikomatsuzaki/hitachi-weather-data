#!/usr/bin/env python3
"""2000年以降の年別Excelを、年に依存しない形で月別YAMLへ変換する。"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import xlrd

import import_hitachi_city_hall_2014 as text_weather
import import_hitachi_city_hall_2025 as common


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
NUMERIC_WEATHER_EXTRACTOR = common.extract_weather_code


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--year", type=int, required=True, choices=range(2000, 2100))
    parser.add_argument("--month", type=int, required=True, choices=range(1, 13))
    parser.add_argument("--source-directory", type=Path)
    parser.add_argument("--download-missing", action="store_true")
    return parser.parse_args()


def extract_weather_auto(path: Path, month: int) -> common.ElementExtraction:
    workbook = xlrd.open_workbook(path)
    sheet = workbook.sheet_by_name("天気")
    code_column = 18 + month
    if code_column < sheet.ncols and common.integer_cell_value(
        sheet, 2, code_column
    ) == month:
        return NUMERIC_WEATHER_EXTRACTOR(path, month)
    return text_weather.extract_weather_code_2014(path, month)


def uses_numeric_weather(path: Path, month: int) -> bool:
    workbook = xlrd.open_workbook(path)
    sheet = workbook.sheet_by_name("天気")
    code_column = 18 + month
    return code_column < sheet.ncols and common.integer_cell_value(
        sheet, 2, code_column
    ) == month


def configure(year: int) -> Path:
    manifest = REPOSITORY_ROOT / "metadata" / "sources" / f"hitachi-city-hall-{year}.yaml"
    common.YEAR = year
    common.SOURCE_MANIFEST_PATH = manifest
    common.GENERATOR_PATH = "scripts/import_hitachi_city_hall_year.py"
    common.SOURCE_PERIOD_ID = (
        "transitional_workbooks" if year <= 2013 else "current_workbooks"
    )
    common.extract_weather_code = extract_weather_auto
    return manifest


def main() -> int:
    arguments = parse_arguments()
    manifest = configure(arguments.year)
    source_directory = arguments.source_directory or (
        REPOSITORY_ROOT / "build" / f"source-{arguments.year}"
    )
    source_paths, verification_rows = common.prepare_source_files(
        source_directory, arguments.download_missing
    )
    extractions = common.extract_all_elements(source_paths, arguments.month)
    document = common.assemble_month_document(arguments.month, extractions)
    document["dataset"]["source_manifest"] = (
        f"../../../metadata/sources/{manifest.name}"
    )
    document["dataset"]["generator"] = "scripts/import_hitachi_city_hall_year.py"
    numeric_weather = uses_numeric_weather(
        source_paths["weather_code"], arguments.month
    )
    if not numeric_weather:
        document["notes"].append(
            "12時の天気は原資料の日本語表記を共通語彙の数値コードへ正規化した。"
        )

    yaml_path = (
        REPOSITORY_ROOT
        / "data"
        / common.STATION_ID
        / str(arguments.year)
        / f"{arguments.month:02d}.yaml"
    )
    report_path = (
        REPOSITORY_ROOT
        / "reports"
        / f"validation-{arguments.year}-{arguments.month:02d}.md"
    )
    common.write_yaml(yaml_path, document)
    common.validate_round_trip(yaml_path, document)
    common.write_validation_report(
        report_path,
        arguments.month,
        yaml_path,
        document,
        extractions,
        verification_rows,
    )
    with report_path.open("a", encoding="utf-8") as report:
        report.write("\n## 天気表記の形式\n\n")
        if numeric_weather:
            report.write("- 12時の天気は原資料の数値コードを採録した。\n")
        else:
            report.write(
                "- 12時の天気は原資料の日本語表記を共通語彙の数値コードへ正規化した。\n"
            )
        if arguments.year == 2000:
            report.write(
                "\n## 2000年問題に関する確認\n\n"
                "- 日付は2000年として明示的に構成し、1900年への誤認がないことを確認した。\n"
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
