import sys
import unittest
from pathlib import Path
from unittest.mock import patch


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import import_hitachi_city_hall_2025 as importer  # noqa: E402


class FakeSheet:
    def __init__(self, title):
        self.name = "1月"
        self.nrows = 3
        self.ncols = 4
        self._title = title

    def cell_value(self, row, column):
        return self._title if (row, column) == (0, 1) else ""


class FakeWorkbook:
    def __init__(self, title):
        self._sheets = [FakeSheet(title) for _ in range(12)]
        self.nsheets = len(self._sheets)

    def sheet_by_index(self, index):
        return self._sheets[index]


class SourceValueTests(unittest.TestCase):
    def test_blank_and_whitespace_are_distinct(self):
        blank = importer.source_cell("")
        spaces = importer.source_cell(" \t　")

        self.assertEqual((blank.value, blank.flag), (None, "source_blank"))
        self.assertEqual((spaces.value, spaces.flag), (None, "source_whitespace"))
        self.assertTrue(spaces.has_raw_value)
        self.assertEqual(spaces.raw_value, " \t　")

    def test_unknown_numeric_source_text_keeps_raw_value(self):
        cell = importer.numeric_source_cell("****")

        self.assertIsNone(cell.value)
        self.assertEqual(cell.flag, "unrecognized_source_value")
        self.assertEqual(cell.raw_value, "****")

    def test_unknown_wind_direction_keeps_raw_value(self):
        extraction = importer.ElementExtraction(
            "wind_direction",
            {(18, 20): importer.SourceCell("無風", raw_value="無風", has_raw_value=True)},
        )
        with (
            patch.object(importer.xlrd, "open_workbook", return_value=FakeWorkbook("風向")),
            patch.object(importer, "extract_regular_hourly_element", return_value=extraction),
        ):
            result = importer.extract_wind_direction(Path("wind-direction.xls"), 6)

        cell = result.cells[(18, 20)]
        self.assertEqual(cell.flag, "unrecognized_source_value")
        self.assertEqual(cell.raw_value, "無風")
        self.assertIsNone(cell.value)

    def test_wind_speed_workbook_is_rejected_as_wind_direction(self):
        with patch.object(
            importer.xlrd,
            "open_workbook",
            return_value=FakeWorkbook("風速"),
        ):
            with self.assertRaisesRegex(ValueError, "structure mismatch"):
                importer.extract_wind_direction(Path("wind-speed.xls"), 1)


if __name__ == "__main__":
    unittest.main()
