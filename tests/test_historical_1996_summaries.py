"""Regression cells from diagnostic run 38092734697, Artifact 11684925794.

The five three-hour tables have separate original-workbook integration tests.
Here their summaries are stubbed so the remaining source layouts are tested
independently, including the misleading day/distance columns beside extrema.
"""
import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch
from openpyxl import Workbook

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import import_hitachi_city_hall_historical_year as historical


class Historical1996SummaryTests(unittest.TestCase):
    def setUp(self):
        source = json.loads((Path(__file__).parent / "fixtures" /
                             "1996-january-summary-cells.json").read_text())
        self.sheets = {}
        for element, rows in source.items():
            sheet = Workbook().active
            sheet.title = "1月"
            for row in rows:
                for cell in row["cells"]:
                    value = cell["value"]
                    try:
                        value = float(value)
                    except ValueError:
                        pass
                    sheet[cell["cell"]] = value
            self.sheets[element] = sheet

    def extract(self):
        with patch.object(historical, "month_sheet", side_effect=lambda path, month: self.sheets[path]), \
             patch.object(historical, "extract_verified_1996_three_hour_summaries", return_value={}):
            return historical.extract_daily_summaries({key: key for key in self.sheets}, 1996, 1)

    def test_source_extrema_columns_and_original_values(self):
        records = self.extract()
        self.assertEqual(len(records), 31)
        self.assertEqual(records[0]["wind"]["maximum_10_minute"]["speed_m_s"], 7.5)
        self.assertEqual(records[0]["wind"]["maximum_instantaneous"]["speed_m_s"], 14.7)
        self.assertEqual(records[0]["global_solar_radiation"]["total_mj_m2"], 9.36)
        self.assertEqual(records[0]["sunshine_duration"]["total_h"], 8.9)
        self.assertEqual(records[7]["precipitation"]["maximum_ten_minutes"],
                         {"value_mm": 1.0, "time": "15:34"})
        self.assertEqual(records[7]["precipitation"]["maximum_one_hour"],
                         {"value_mm": 2.0, "time": "16:03"})
        self.assertIsNone(records[0]["precipitation"]["total_mm"])

    def test_wrong_rainfall_header_stops_import(self):
        self.sheets["precipitation"]["AE3"] = "日"
        with self.assertRaisesRegex(ValueError, "precipitation summary header mismatch"):
            self.extract()

    def test_wrong_wind_header_stops_import(self):
        self.sheets["wind_speed"]["AD3"] = "全風程"
        with self.assertRaisesRegex(ValueError, "wind_speed summary header mismatch"):
            self.extract()
