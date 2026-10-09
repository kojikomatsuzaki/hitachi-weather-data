#!/usr/bin/env python3
"""正本YAMLからGitHub Pages用のJSONを生成する。"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import yaml


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
CANONICAL_DATA_ROOT = REPOSITORY_ROOT / "data" / "hitachi-city-hall"
WEB_DATA_ROOT = REPOSITORY_ROOT / "docs" / "data"


def generate_month_json(source_path: Path) -> Path:
    """YAMLを読み、意味を変えずに表示用JSONへ変換する。"""

    relative_path = source_path.relative_to(CANONICAL_DATA_ROOT)
    output_path = WEB_DATA_ROOT / relative_path.with_suffix(".json")
    document = yaml.safe_load(source_path.read_text(encoding="utf-8"))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(document, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return output_path


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--year",
        type=int,
        help="指定年のJSONだけを再生成する。index.jsonは全収録年から再構成する。",
    )
    return parser.parse_args()


def main() -> None:
    arguments = parse_arguments()
    source_paths = sorted(CANONICAL_DATA_ROOT.glob("*/*.yaml"))
    if not source_paths:
        raise SystemExit("正本YAMLが見つかりません。")

    generation_paths = [
        source_path
        for source_path in source_paths
        if arguments.year is None or int(source_path.parent.name) == arguments.year
    ]
    for source_path in generation_paths:
        output_path = generate_month_json(source_path)
        print(f"Generated: {output_path.relative_to(REPOSITORY_ROOT)}")

    available_datasets = []
    for source_path in source_paths:
        year = int(source_path.parent.name)
        month = int(source_path.stem)
        output_path = WEB_DATA_ROOT / source_path.relative_to(CANONICAL_DATA_ROOT).with_suffix(".json")
        available_datasets.append(
            {
                "year": year,
                "month": month,
                "label": f"{year}年{month}月",
                "data_path": str(output_path.relative_to(WEB_DATA_ROOT)),
                "yaml_path": str(source_path.relative_to(REPOSITORY_ROOT)),
                "report_path": (
                    f"reports/validation-{year}-{month:02d}.md"
                ),
            }
        )

    index_path = WEB_DATA_ROOT / "index.json"
    index_path.write_text(
        json.dumps(available_datasets, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Generated: {index_path.relative_to(REPOSITORY_ROOT)}")


if __name__ == "__main__":
    main()
