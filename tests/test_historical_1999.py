"""1999年テスト取り込みの構造を確認する。"""

from pathlib import Path
import unittest

import yaml


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


class Historical1999Test(unittest.TestCase):
    def load_month(self, month: int) -> dict:
        path = REPOSITORY_ROOT / "data" / "hitachi-city-hall" / "1999" / f"{month:02d}.yaml"
        return yaml.safe_load(path.read_text(encoding="utf-8"))

    def test_all_months_have_complete_calendar(self) -> None:
        expected_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        for month, days in enumerate(expected_days, start=1):
            document = self.load_month(month)
            self.assertEqual(days * 24, len(document["observations"]))
            self.assertEqual(days, len(document["daily_summaries"]))

    def test_source_period_and_schedules(self) -> None:
        dataset = self.load_month(1)["dataset"]
        self.assertEqual("historical_annual_workbooks", dataset["source_period_id"])
        self.assertEqual(list(range(1, 25)), dataset["observation_schedules"]["temperature_c"])
        self.assertEqual(list(range(4, 21)), dataset["observation_schedules"]["sunshine_duration_h"])
        self.assertEqual([12], dataset["observation_schedules"]["weather_code"])

    def test_representative_source_values(self) -> None:
        document = self.load_month(1)
        observations = {
            (item["source_date"], item["source_hour"]): item
            for item in document["observations"]
        }
        first_hour = observations[("1999-01-01", 1)]["values"]
        noon = observations[("1999-01-01", 12)]["values"]
        self.assertEqual(0.2, first_hour["temperature_c"])
        self.assertEqual("N", first_hour["wind_direction"])
        self.assertEqual(-7.4, first_hour["dew_point_temperature_c"])
        self.assertEqual(1, noon["weather_code"])

        first_day = document["daily_summaries"][0]
        self.assertEqual(3.3875, first_day["temperature"]["mean_c"])
        self.assertEqual(11.36, first_day["global_solar_radiation"]["total_mj_m2"])


if __name__ == "__main__":
    unittest.main()
