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
import verify_1996_source_cells as oracle
from hitachi_historical_layout import THREE_HOURLY, detect_observation_layout

ELEMENTS = {
    "temperature": ("temperature_c", ("日平均", "最高", "時刻1", "最低", "時刻2")),
    "humidity": ("relative_humidity_percent", ("日平均", "最小", "時刻1")),
    "dew_point_temperature": ("dew_point_temperature_c",
                              ("日平均", "最高", "時刻1", "最低", "時刻2")),
    "station_pressure": ("station_pressure_hpa", ("日平均", "最高", "時刻1")),
    "sea_level_pressure": ("sea_level_pressure_hpa", ()),
}


def run(year, months, source_directory, download_missing, verify_canonical=False):
    manifest_path, manifest = historical.load_manifest(year)
    paths, verified_members, verified_archives = historical.prepare_source_files(
        manifest, source_directory, download_missing)
    results = {"year": year, "months": [], "verified_workbooks": verified_members,
               "verified_archives": verified_archives, "source_manifest": str(manifest_path)}
    for month in months:
        entry = {"month": month, "elements": {}}
        for key, (element_id, labels) in ELEMENTS.items():
            schedule = (3, 9, 15, 21) if year in range(1986, 1993) and "pressure" in key else THREE_HOURLY
            if year in range(1992, 1996) and key == "dew_point_temperature":
                labels = ("日平均", "最高", "時刻1", "日", "最低", "時刻2")
            if key.startswith("station_") or key.startswith("sea_"):
                source = paths["pressure"]
                fragment = "現地気圧" if key.startswith("station_") else "海面気圧"
            else:
                source = paths[key]
                fragment = None
            sheet = historical.month_sheet(source, month)
            start_row = historical.find_title_row(sheet, fragment) + 1 if fragment else 1
            layout = detect_observation_layout(
                sheet, expected_schedules=(schedule,), start_row=start_row,
                summary_labels=labels)
            extracted = historical.extract_hourly(
                source, year, month, element_id, list(range(1, 25)),
                title_fragment=fragment)
            expected_count = calendar.monthrange(year, month)[1] * len(schedule)
            assert len(extracted.cells) == expected_count, (key, month, len(extracted.cells))
            assert all(hour in schedule for _, hour in extracted.cells)
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
                              for hour in schedule},
                "first_day_summary": {
                    label: str(sheet.cell(layout.header_row + 1, col).value)
                    for label, col in layout.summary_columns.items()
                },
            }
            print(f"PASS {year}-{month:02d} {key}: {expected_count} scheduled cells", flush=True)
        # Compare extracted source summaries with the independently located cells.
        # Pressure summary mapping remains intentionally excluded until verified.
        verified_summaries = historical.extract_verified_1996_three_hour_summaries(paths, month, year)
        for key, expected_labels in (
            ("temperature", ("日平均", "最高", "時刻1", "最低", "時刻2")),
            ("humidity", ("日平均", "最小", "時刻1")),
            ("dew_point_temperature", ("日平均", "最高", "時刻1", "最低", "時刻2")),
            ("station_pressure", ()),
            ("sea_level_pressure", ()),
        ):
            if year in range(1992, 1996) and key == "dew_point_temperature":
                expected_labels = ("日平均", "最高", "時刻1", "日", "最低", "時刻2")
            schedule = (3, 9, 15, 21) if year in range(1986, 1993) and "pressure" in key else THREE_HOURLY
            source_key = "pressure" if "pressure" in key else key
            sheet = historical.month_sheet(paths[source_key], month)
            fragment = ("現地気圧" if key == "station_pressure" else
                        "海面気圧" if key == "sea_level_pressure" else None)
            start = historical.find_title_row(sheet, fragment) + 1 if fragment else 1
            layout = detect_observation_layout(
                sheet, expected_schedules=(schedule,),
                start_row=start, summary_labels=expected_labels)
            day_rows = dict(historical.day_rows(sheet, layout.header_row, year, month))
            assert len(verified_summaries[key]) == calendar.monthrange(year, month)[1]
            for day, row in day_rows.items():
                record = verified_summaries[key][f"{year}-{month:02d}-{day:02d}"]
                mean = (record["mean_percent"] if key == "humidity" else
                        record["mean_hpa"] if "pressure" in key else record["mean_c"])
                assert mean == oracle.number(
                    sheet, row, (6 if year in range(1986, 1993) else 10) if "pressure" in key else layout.summary_columns["日平均"]), (key, month, day)
            entry["elements"][key]["daily_summaries_verified"] = len(day_rows)
        # Verify the entire daily source summary, including pressure extrema,
        # against independently addressed worksheet cells.
        for name in ("temperature", "humidity", "dew_point_temperature",
                     "station_pressure", "sea_level_pressure"):
            schedule = (3, 9, 15, 21) if year in range(1986, 1993) and "pressure" in name else THREE_HOURLY
            source_key = "pressure" if "pressure" in name else name
            sheet = historical.month_sheet(paths[source_key], month)
            fragment = ("現地気圧" if name == "station_pressure" else
                        "海面気圧" if name == "sea_level_pressure" else None)
            start_row = historical.find_title_row(sheet, fragment) + 1 if fragment else 1
            layout = detect_observation_layout(
                sheet, expected_schedules=(schedule,), start_row=start_row)
            rows = historical.rows_by_day(sheet, layout.header_row, year, month)
            unit = ("percent" if name == "humidity" else
                    "hpa" if "pressure" in name else "c")
            for day, row in rows.items():
                record = verified_summaries[name][f"{year}-{month:02d}-{day:02d}"]
                assert record[f"mean_{unit}"] == oracle.number(
                    sheet, row, 6 if year in range(1986, 1993) and "pressure" in name else 10), (name, month, day, "mean")
                if name != "humidity":
                    assert record["maximum"][f"value_{unit}"] == oracle.number(
                        sheet, row, 7 if year in range(1986, 1993) and "pressure" in name else 11), (name, month, day, "maximum")
                    assert record["maximum"]["time"] == oracle.moment(
                        sheet, row, 8 if year in range(1986, 1993) and "pressure" in name else 12), (name, month, day, "maximum time")
                min_col = 9 if year in range(1986, 1993) and unit == "hpa" else 14 if unit == "hpa" or (year in range(1992, 1996) and name == "dew_point_temperature") else (11 if unit == "percent" else 13)
                min_time_col = 10 if year in range(1986, 1993) and unit == "hpa" else 15 if unit == "hpa" or (year in range(1992, 1996) and name == "dew_point_temperature") else (12 if unit == "percent" else 14)
                assert record["minimum"][f"value_{unit}"] == oracle.number(
                    sheet, row, min_col), (name, month, day, "minimum")
                assert record["minimum"]["time"] == oracle.moment(
                    sheet, row, min_time_col), (name, month, day, "minimum time")
        # Exercise the complete production path, not only the three-hour subset.
        all_elements = historical.extract_all_elements(paths, year, month)
        all_summaries = historical.extract_daily_summaries(paths, year, month)
        assert len(all_elements) == 11
        assert len(all_summaries) == calendar.monthrange(year, month)[1]
        # Independent coordinates from the diagnostic original workbook report.
        fields = {
            "precipitation": ("precipitation", list(range(1, 25)), {
                ("total_mm",): 26,
                ("maximum_one_hour", "value_mm"): 28,
                ("maximum_one_hour", "time"): 29,
                ("maximum_ten_minutes", "value_mm"): 31,
                ("maximum_ten_minutes", "time"): 32}),
            "wind_speed": ("wind", list(range(1, 25)), {
                ("mean_speed_m_s",): 26,
                ("maximum_10_minute", "direction"): 29,
                ("maximum_10_minute", "speed_m_s"): 30,
                ("maximum_10_minute", "time"): 31,
                ("maximum_instantaneous", "direction"): 32,
                ("maximum_instantaneous", "speed_m_s"): 33,
                ("maximum_instantaneous", "time"): 34}),
            "solar_radiation": ("global_solar_radiation", list(range(4, 21)), {
                ("total_mj_m2",): 19}),
            "sunshine_duration": ("sunshine_duration", list(range(4, 21)), {
                ("total_h",): 19}),
        }
        if year in range(1986, 1996):
            summary_key, hours, mapping = fields["wind_speed"]
            fields["wind_speed"] = (summary_key, hours, {
                keys: column + (1 if column >= 32 else 0)
                for keys, column in mapping.items()
            })
        for source_key, (summary_key, hours, mapping) in fields.items():
            sheet = historical.month_sheet(paths[source_key], month)
            header = historical.find_hour_header_row(sheet, hours)
            rows = historical.rows_by_day(sheet, header, year, month)
            for day, row in rows.items():
                for keys, column in mapping.items():
                    actual = all_summaries[day - 1][summary_key]
                    for key in keys:
                        actual = actual[key]
                    if keys[-1] == "time":
                        expected = oracle.moment(sheet, row, column)
                    elif keys[-1] == "direction":
                        expected = oracle.text_cell(sheet, row, column)
                    else:
                        expected = oracle.number(
                            sheet, row, column,
                            duration=source_key == "sunshine_duration")
                    assert actual == expected, (source_key, month, day, keys)
        entry["independent_observations"] = oracle.verify_extractions(paths, month, all_elements, year)
        print(f"PASS {year}-{month:02d} independent observations: all 11 elements", flush=True)
        if verify_canonical:
            canonical_path = historical.REPOSITORY_ROOT / "data" / "hitachi-city-hall" / str(year) / f"{month:02d}.yaml"
            canonical = yaml.safe_load(canonical_path.read_text(encoding="utf-8"))
            entry["canonical_records_verified"] = oracle.verify_document(paths, month, canonical, year)
            assert canonical["daily_summaries"] == all_summaries
            web_path = historical.REPOSITORY_ROOT / "docs" / "data" / str(year) / f"{month:02d}.json"
            assert json.loads(web_path.read_text(encoding="utf-8")) == canonical
            entry["canonical_web_equal"] = True
            print(f"PASS {year}-{month:02d} canonical source values/flags/schedules and YAML/JSON", flush=True)
        entry["production_path_verified"] = True
        entry["all_element_count"] = len(all_elements)
        entry["complete_daily_summary_count"] = len(all_summaries)
        print(f"PASS {year}-{month:02d} complete production extraction", flush=True)
        results["months"].append(entry)
    return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--year", type=int, default=1996)
    parser.add_argument("--months", type=int, nargs="+", default=[1])
    parser.add_argument("--source-directory", type=Path, default=Path("build/source-1996"))
    parser.add_argument("--download-missing", action="store_true")
    parser.add_argument("--output", type=Path, default=Path("build/integration-results.json"))
    parser.add_argument("--verify-canonical", action="store_true")
    args = parser.parse_args()
    if args.year not in range(1986, 1997):
        raise ValueError("This test explicitly validates the verified 1995/1996 three-hour layouts")
    if len(set(args.months)) != len(args.months) or any(month not in range(1, 13) for month in args.months):
        raise ValueError("Months must be unique integers from 1 to 12")
    result = run(args.year, args.months, args.source_directory, args.download_missing, args.verify_canonical)
    result["full_year_verified"] = set(args.months) == set(range(1, 13))
    result["canonical_verified"] = args.verify_canonical
    result["comparison_basis"] = "Independent coordinates and decoders on checksum-verified originals converted by LibreOffice; no interpolation"

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
                paths, month, args.year)
            for month in args.months
        },
    }
    preview_path = args.output.parent / f"{args.year}-daily-summary-PREVIEW-DO-NOT-PUBLISH.yaml"
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
