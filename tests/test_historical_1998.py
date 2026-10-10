"""1998年を、歴史資料期の年次遡及テストとして確認する。"""

import calendar
import unittest
from pathlib import Path

import yaml


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


class Historical1998Test(unittest.TestCase):
    def load_month(self, month: int) -> dict:
        path = REPOSITORY_ROOT / "data" / "hitachi-city-hall" / "1998" / f"{month:02d}.yaml"
        return yaml.safe_load(path.read_text(encoding="utf-8"))

    def test_all_months_have_complete_hourly_and_daily_records(self) -> None:
        total_observations = 0
        for month in range(1, 13):
            document = self.load_month(month)
            days = calendar.monthrange(1998, month)[1]
            self.assertEqual(1998, document["dataset"]["year"])
            self.assertEqual(month, document["dataset"]["month"])
            self.assertEqual(days * 24, len(document["observations"]))
            self.assertEqual(days, len(document["daily_summaries"]))
            total_observations += len(document["observations"])
        self.assertEqual(8760, total_observations)

    def test_representative_source_values_are_preserved(self) -> None:
        january = self.load_month(1)
        observations = {
            (row["source_date"], row["source_hour"]): row
            for row in january["observations"]
        }
        first_hour = observations[("1998-01-01", 1)]["values"]
        noon = observations[("1998-01-01", 12)]["values"]
        self.assertEqual(3.1, first_hour["temperature_c"])
        self.assertEqual("WNW", first_hour["wind_direction"])
        self.assertEqual(-5.0, first_hour["dew_point_temperature_c"])
        self.assertEqual(3, noon["weather_code"])


if __name__ == "__main__":
    unittest.main()
