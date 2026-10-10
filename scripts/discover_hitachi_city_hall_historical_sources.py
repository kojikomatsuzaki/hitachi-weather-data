#!/usr/bin/env python3
"""歴史ZIPから指定年の原Excelを同定し、年別マニフェストを作る。

共通目録はZIPそのものの来歴を、年別マニフェストはZIP内の対象XLSを
記録する。両者を分けることで、同じZIPを年ごとに再記述せずに済ませる。
"""

from __future__ import annotations

import argparse
import hashlib
import urllib.request
import zipfile
from datetime import date
from pathlib import Path

import yaml


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = (
    REPOSITORY_ROOT / "metadata" / "sources"
    / "hitachi-city-hall-historical-archives.yaml"
)


def sha256_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source_file:
        for block in iter(lambda: source_file.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def discover_year(year: int, source_directory: Path) -> Path:
    catalog = yaml.safe_load(CATALOG_PATH.read_text(encoding="utf-8"))
    files = []
    source_directory.mkdir(parents=True, exist_ok=True)

    for archive in catalog["archives"]:
        archive_path = source_directory / archive["file_name"]
        if not archive_path.exists():
            urllib.request.urlretrieve(archive["url"], archive_path)
        actual_archive_sha = sha256_path(archive_path)
        if actual_archive_sha != archive["sha256"]:
            raise ValueError(
                f"SHA-256 mismatch for {archive_path.name}: "
                f"expected {archive['sha256']}, got {actual_archive_sha}"
            )

        expected_member = f"{archive['member_prefix']}{year}.xls"
        with zipfile.ZipFile(archive_path) as zip_file:
            matching_members = [
                name for name in zip_file.namelist()
                if Path(name).name.casefold() == expected_member.casefold()
            ]
            if len(matching_members) != 1:
                raise ValueError(
                    f"Expected exactly one {expected_member} in {archive_path.name}; "
                    f"found {matching_members}"
                )
            archive_member = matching_members[0]
            member_content = zip_file.read(archive_member)

        files.append({
            "element": archive["element"],
            "url": archive["url"],
            "archive_sha256": actual_archive_sha,
            "archive_member": archive_member,
            "member_sha256": sha256_bytes(member_content),
        })

    document = {
        "schema_version": "0.2.0",
        "source_collection": {
            "id": f"hitachi-city-hall-{year}",
            "station_id": "hitachi-city-hall",
            "year": year,
            "publisher_ja": "日立市天気相談所",
            "landing_page": catalog["source_collection"]["landing_page"],
            "retrieved_date": date.today().isoformat(),
            "container_format": "application/zip",
            "workbook_format": "application/vnd.ms-excel",
            "archive_catalog": str(CATALOG_PATH.relative_to(REPOSITORY_ROOT)),
            "reading_adapter": {
                "software": "LibreOffice Calc",
                "purpose": "古いBIFFレコードを含む原Excelを、値を抽出できる一時的なXLSXへ変換する。",
                "preservation_rule": "原ExcelおよびZIPは変更せず、変換後XLSXは派生データ生成時だけ使用する。",
            },
        },
        "files": files,
        "notes": [
            f"{year}年は1953–2007年一括ZIPに収録された年別Excelを主原資料とする。",
            "原ZIPと内部Excelの双方についてSHA-256を記録する。",
            "原Excelはリポジトリへ複製しない。",
        ],
    }
    output_path = (
        REPOSITORY_ROOT / "metadata" / "sources"
        / f"hitachi-city-hall-{year}.yaml"
    )
    output_path.write_text(
        yaml.safe_dump(document, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )
    return output_path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--year", type=int, required=True, choices=range(1953, 2000))
    parser.add_argument("--source-directory", type=Path)
    arguments = parser.parse_args()
    source_directory = arguments.source_directory or (
        REPOSITORY_ROOT / "build" / f"source-{arguments.year}"
    )
    output_path = discover_year(arguments.year, source_directory)
    print(f"Generated: {output_path.relative_to(REPOSITORY_ROOT)}")


if __name__ == "__main__":
    main()
