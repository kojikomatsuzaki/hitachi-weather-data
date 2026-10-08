#!/usr/bin/env python3
"""公式一覧から日立市役所観測所の年別Excel出典を発見する。"""

from __future__ import annotations

import argparse
import hashlib
import re
import urllib.request
from datetime import date
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin

import yaml


LANDING_PAGE = "https://tenki.city.hitachi.lg.jp/obs/contents/919"
REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
ELEMENTS = [
    "temperature",
    "humidity",
    "precipitation",
    "pressure",
    "solar_radiation",
    "sunshine_duration",
    "wind_speed",
    "wind_direction",
    "dew_point_temperature",
    "weather_code",
]


class TableParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.in_row = False
        self.rows: list[tuple[str, list[str]]] = []
        self.row_text: list[str] = []
        self.row_links: list[str] = []
        self.page_text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "tr":
            self.in_row = True
            self.row_text = []
            self.row_links = []
        elif self.in_row and tag == "a":
            href = dict(attrs).get("href")
            if href:
                self.row_links.append(href)

    def handle_endtag(self, tag: str) -> None:
        if tag == "tr" and self.in_row:
            self.rows.append((" ".join(self.row_text), self.row_links.copy()))
            self.in_row = False

    def handle_data(self, data: str) -> None:
        text = data.strip()
        if not text:
            return
        self.page_text.append(text)
        if self.in_row:
            self.row_text.append(text)


def fetch(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": "hitachi-weather-data/1.0"})
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read()


def parse_listing(html: bytes) -> tuple[dict[int, list[str]], str | None]:
    parser = TableParser()
    parser.feed(html.decode("utf-8", errors="replace"))
    years: dict[int, list[str]] = {}
    for text, links in parser.rows:
        match = re.search(r"(?:^|\s)(20\d{2})(?:\s|$)", text)
        if match and len(links) >= len(ELEMENTS):
            years[int(match.group(1))] = [
                urljoin(LANDING_PAGE, href) for href in links[: len(ELEMENTS)]
            ]
    page_text = " ".join(parser.page_text)
    updated = re.search(r"更新日[：:]\s*(\d{4})/(\d{1,2})/(\d{1,2})", page_text)
    updated_date = (
        f"{int(updated.group(1)):04d}-{int(updated.group(2)):02d}-{int(updated.group(3)):02d}"
        if updated
        else None
    )
    return years, updated_date


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_manifest(year: int, urls: list[str], updated_date: str | None) -> Path:
    files = []
    for element, url in zip(ELEMENTS, urls, strict=True):
        files.append({"element": element, "url": url, "sha256": sha256(fetch(url))})

    path = REPOSITORY_ROOT / "metadata" / "sources" / f"hitachi-city-hall-{year}.yaml"
    previous = (
        yaml.safe_load(path.read_text(encoding="utf-8")) if path.exists() else None
    )
    unchanged_sources = previous and previous.get("files") == files
    previous_collection = previous.get("source_collection", {}) if previous else {}
    retrieved_date = (
        previous_collection.get("retrieved_date")
        if unchanged_sources
        else date.today().isoformat()
    )
    document = {
        "schema_version": "0.2.0",
        "source_collection": {
            "id": f"hitachi-city-hall-{year}",
            "station_id": "hitachi-city-hall",
            "year": year,
            "publisher_ja": "日立市天気相談所",
            "landing_page": LANDING_PAGE,
            "published_update_date": updated_date,
            "retrieved_date": retrieved_date,
            "format": "application/vnd.ms-excel",
        },
        "files": files,
        "notes": [
            "公式の年別観測データ一覧からURLを取得した。",
            "URLのファイル名は内容を示さないため、表の列順によりelementとの対応を記録した。",
            "原Excelは再配布せず、公式URLと取得時のSHA-256を記録する。",
        ],
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        yaml.safe_dump(document, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )
    return path


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--year", type=int, help="省略時は公式ページの最新公開年")
    parser.add_argument("--print-year", action="store_true")
    return parser.parse_args()


def main() -> int:
    arguments = parse_arguments()
    html = fetch(LANDING_PAGE)
    years, updated_date = parse_listing(html)
    if not years:
        raise SystemExit("公式ページから年別Excelの一覧を取得できませんでした。")
    year = arguments.year or max(years)
    if year not in years:
        raise SystemExit(f"{year}年は公式ページにありません。公開年: {min(years)}-{max(years)}")
    if arguments.print_year:
        print(year)
        return 0
    path = write_manifest(year, years[year], updated_date)
    print(f"Discovered {year}: {path.relative_to(REPOSITORY_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
