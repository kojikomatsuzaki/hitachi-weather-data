#!/usr/bin/env python3
"""Read-only integration checks against checksum-verified historical originals."""
import argparse
import calendar
import json
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import import_hitachi_city_hall_historical_year as historical
from hitachi_historical_layout import THREE_HOURLY, detect_observation_layout

ELEMENTS = {
    "temperature": ("temperature_c", ("日平均", "最高", "時刻1", "最低", "時刻2")),
    "humidity": ("relative_humidity_percent", ("日平均", "最小", "時刻1")),
    "dew_point_temperature": ("dew_point_temperature_c",
                              ("日平均", "最高", "時刻1", "最低", "時刻2")),
    "station_pressure": ("station_pressure_hpa", ("日平均", "最高", "時刻1")),
    "sea_level_pressure": ("sea_level_pressure_hpa", ()),
}


def run(year, months, source_directory, download_missing):
    manifest_path, manifest = historical.load_manifest(year)
    paths, verified_members, verified_archives = historical.prepare_source_files(
        manifest, source_directory, download_missing)
    results = {"year": year, "months": [], "verified_workbooks": verified_members,
               "verified_archives": verified_archives, "source_manifest": str(manifest_path)}
    for month in months:
        entry = {"month": month, "elements": {}}
        for key, (element_id, labels) in ELEMENTS.items():
            if key.startswith("station_") or key.startswith("sea_"):
                source = paths["pressure"]
                fragment = "現地気圧" if key.startswith("station_") else "海面気圧"
            else:
                source = paths[key]
                fragment = None
            sheet = historical.month_sheet(source, month)
            start_row = historical.find_title_row(sheet, fragment) + 1 if fragment else 1
            layout = detect_observation_layout(
                sheet, expected_schedules=(THREE_HOURLY,), start_row=start_row,
                summary_labels=labels)
            extracted = historical.extract_hourly(
                source, year, month, element_id, list(range(1, 25)),
                title_fragment=fragment)
            expected_count = calendar.monthrange(year, month)[1] * 8
            assert len(extracted.cells) == expected_count, (key, month, len(extracted.cells))
            assert all(hour in THREE_HOURLY for _, hour in extracted.cells)
            # Independent direct comparison with the original converted worksheet cells.
            for day, row in historical.day_rows(sheet, layout.header_row, year, month):
                for hour, col in zip(layout.hours, layout.columns):
                    expected = historical.historical_numeric_cell(sheet.cell(row, col).value)
                    actual = extracted.cells[(day, hour)]
                    assert actual.value == expected.value and actual.flag == expected.flag, (
                        key, month, day, hour, sheet.cell(row, col).coordinate)
            entry["elements"][key] = {
                "hours": list(layout.hours), "header_row": layout.header_row,
                "observation_cells": len(extracted.cells),
                "first_day": {str(hour): extracted.cells[(1, hour)].value
                              for hour in THREE_HOURLY},
                "first_day_summary": {
                    label: str(sheet.cell(layout.header_row + 1, col).value)
                    for label, col in layout.summary_columns.items()
                },
            }
            print(f"PASS {year}-{month:02d} {key}: {expected_count} scheduled cells", flush=True)
        # Compare extracted source summaries with the independently located cells.
        # Pressure summary mapping remains intentionally excluded until verified.
        verified_summaries = historical.extract_verified_1996_three_hour_summaries(paths, month)
        for key, expected_labels in (
            ("temperature", ("日平均", "最高", "時刻1", "最低", "時刻2")),
            ("humidity", ("日平均", "最小", "時刻1")),
            ("dew_point_temperature", ("日平均", "最高", "時刻1", "最低", "時刻2")),
            ("station_pressure", ()),
            ("sea_level_pressure", ()),
        ):
            source_key = "pressure" if "pressure" in key else key
            sheet = historical.month_sheet(paths[source_key], month)
            fragment = ("現地気圧" if key == "station_pressure" else
                        "海面気圧" if key == "sea_level_pressure" else None)
            start = historical.find_title_row(sheet, fragment) + 1 if fragment else 1
            layout = detect_observation_layout(
                sheet, expected_schedules=(THREE_HOURLY,),
                start_row=start, summary_labels=expected_labels)
            day_rows = dict(historical.day_rows(sheet, layout.header_row, year, month))
            assert len(verified_summaries[key]) == calendar.monthrange(year, month)[1]
            for day, row in day_rows.items():
                record = verified_summaries[key][f"{year}-{month:02d}-{day:02d}"]
                mean = (record["mean_percent"] if key == "humidity" else
                        record["mean_hpa"] if "pressure" in key else record["mean_c"])
                assert mean == historical.numeric_value(
                    sheet, row, 10 if "pressure" in key else layout.summary_columns["日平均"]), (key, month, day)
            entry["elements"][key]["daily_summaries_verified"] = len(day_rows)
        # Verify the entire daily source summary, including pressure extrema,
        # against independently addressed worksheet cells.
        for name in ("temperature", "humidity", "dew_point_temperature",
                     "station_pressure", "sea_level_pressure"):
            source_key = "pressure" if "pressure" in name else name
            sheet = historical.month_sheet(paths[source_key], month)
            fragment = ("現地気圧" if name == "station_pressure" else
                        "海面気圧" if name == "sea_level_pressure" else None)
            start_row = historical.find_title_row(sheet, fragment) + 1 if fragment else 1
            layout = detect_observation_layout(
                sheet, expected_schedules=(THREE_HOURLY,), start_row=start_row)
            rows = historical.rows_by_day(sheet, layout.header_row, year, month)
            unit = ("percent" if name == "humidity" else
                    "hpa" if "pressure" in name else "c")
            for day, row in rows.items():
                record = verified_summaries[name][f"{year}-{month:02d}-{day:02d}"]
                assert record[f"mean_{unit}"] == historical.numeric_value(
                    sheet, row, 10), (name, month, day, "mean")
                if name != "humidity":
                    assert record["maximum"][f"value_{unit}"] == historical.numeric_value(
                        sheet, row, 11), (name, month, day, "maximum")
                    assert record["maximum"]["time"] == historical.time_value(
                        sheet, row, 12), (name, month, day, "maximum time")
                min_col = 14 if unit == "hpa" else (11 if unit == "percent" else 13)
                min_time_col = 15 if unit == "hpa" else (12 if unit == "percent" else 14)
                assert record["minimum"][f"value_{unit}"] == historical.numeric_value(
                    sheet, row, min_col), (name, month, day, "minimum")
                assert record["minimum"]["time"] == historical.time_value(
                    sheet, row, min_time_col), (name, month, day, "minimum time")
        results["months"].append(entry)
    return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--year", type=int, default=1996)
    parser.add_argument("--months", type=int, nargs="+", default=[1])
    parser.add_argument("--source-directory", type=Path, default=Path("build/source-1996"))
    parser.add_argument("--download-missing", action="store_true")
    parser.add_argument("--output", type=Path, default=Path("build/integration-results.json"))
    args = parser.parse_args()
    if args.year != 1996:
        raise ValueError("This test explicitly validates the known 1996 three-hour layout")
    result = run(args.year, args.months, args.source_directory, args.download_missing)
    # A clearly marked partial YAML preview, never the canonical data/ path.
    # Only the five independently checked three-hour elements are included.
    manifest_path, manifest = historical.load_manifest(args.year)
    paths, _, _ = historical.prepare_source_files(
        manifest, args.source_directory, args.download_missing)
    preview = {
        "status": "INCOMPLETE_DO_NOT_PUBLISH",
        "year": args.year,
        "source_manifest": str(manifest_path),
        "months": {
            f"{month:02d}": historical.extract_verified_1996_three_hour_summaries(
                paths, month)
            for month in args.months
        },
    }
    preview_path = args.output.parent / "1996-daily-summary-PREVIEW-DO-NOT-PUBLISH.yaml"
    preview_path.parent.mkdir(parents=True, exist_ok=True)
    preview_path.write_text(
        yaml.safe_dump(preview, allow_unicode=True, sort_keys=False),
        encoding="utf-8")
    print(f"PREVIEW ONLY: {preview_path}", flush=True)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"PASS: wrote {args.output}")


if __name__ == "__main__":
    main()
