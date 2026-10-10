"""日照時間のExcel時間長を時間単位へ変換する規則を確認する。"""

from datetime import timedelta
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import import_hitachi_city_hall_historical_year as historical


class HistoricalDurationValueTests(unittest.TestCase):
    def test_sunshine_duration_is_converted_from_timedelta_to_hours(self) -> None:
        cell = historical.historical_numeric_cell(
            timedelta(hours=6, minutes=39),
            duration_unit_hours=True,
        )

        self.assertEqual(6.65, cell.value)
        self.assertIsNone(cell.flag)

    def test_other_measurements_do_not_interpret_timedelta_as_hours(self) -> None:
        with self.assertRaises(TypeError):
            historical.historical_numeric_cell(timedelta(hours=6, minutes=39))


if __name__ == "__main__":
    unittest.main()
