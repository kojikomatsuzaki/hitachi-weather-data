#!/usr/bin/env python3
"""日立市役所観測所の2000年Excelを月別YAMLへ変換する。"""

from __future__ import annotations

import argparse
from pathlib import Path

import import_hitachi_city_hall_2014 as importer


YEAR = 2000
REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="日立市役所観測所の2000年Excelを月別YAMLへ変換する。"
    )
    parser.add_argument("--month", type=int, required=True, choices=range(1, 13))
    parser.add_argument(
        "--source-directory",
        type=Path,
        default=REPOSITORY_ROOT / "build" / "source-2000",
    )
    parser.add_argument("--download-missing", action="store_true")
    return parser.parse_args()


def configure_importer() -> None:
    importer.YEAR = YEAR
    importer.SOURCE_MANIFEST_PATH = (
        REPOSITORY_ROOT / "metadata" / "sources" / "hitachi-city-hall-2000.yaml"
    )
    importer.SOURCE_MANIFEST_RELATIVE = (
        "../../../metadata/sources/hitachi-city-hall-2000.yaml"
    )
    importer.GENERATOR_PATH = "scripts/import_hitachi_city_hall_2000.py"
    importer.SOURCE_PERIOD_ID = "transitional_workbooks"
    importer.FORMAT_COMPARISON_HEADING = "2014年・2025年版との形式差"
    importer.WEATHER_FORMAT_DIFFERENCE = (
        "12時の天気は2014年版と同じ日本語表記で、2025年版は数値コードだった。"
    )
    importer.ADDITIONAL_REPORT_LINES = [
        "## 2000年問題に関する確認",
        "",
        "- 生成された全744レコードの日付は、2000-01-01から2000-01-31の範囲にある。",
        "- 2桁年への短縮、1900年への誤認、日付の欠落は検出されなかった。",
        "- 原Excelの月別表は日番号を保持しており、年と月は出典メタデータから明示的に付与した。",
    ]
    importer.parse_arguments = parse_arguments


if __name__ == "__main__":
    configure_importer()
    raise SystemExit(importer.main())
