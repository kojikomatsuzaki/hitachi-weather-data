#!/usr/bin/env python3
"""正本YAMLからGitHub Pages用のJSONを生成する。"""

from __future__ import annotations

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


def main() -> None:
    source_paths = sorted(CANONICAL_DATA_ROOT.glob("*/*.yaml"))
    if not source_paths:
        raise SystemExit("正本YAMLが見つかりません。")

    for source_path in source_paths:
        output_path = generate_month_json(source_path)
        print(f"Generated: {output_path.relative_to(REPOSITORY_ROOT)}")


if __name__ == "__main__":
    main()

