import copy
import sys
import unittest
from datetime import timedelta
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import verify_1996_source_cells as oracle
import import_hitachi_city_hall_historical_year as historical


class IndependentOracleTests(unittest.TestCase):
    def test_special_values_remain_distinct(self):
        for raw, flag in [(None, 'source_blank'), (' ', 'source_whitespace'),
                          ('-', 'source_dash'), ('***', 'source_triple_asterisk'),
                          ('欠測', 'source_missing'), ('不明語', 'unrecognized_source_value')]:
            self.assertEqual(oracle.decode(raw, 'precipitation_mm')[1], flag)
        self.assertEqual(oracle.decode(0, 'precipitation_mm')[0], 0)
        self.assertEqual(oracle.decode(timedelta(minutes=30), 'sunshine_duration_h')[0], .5)
        self.assertEqual(oracle.decode('北北東', 'wind_direction')[0], 'NNE')
        self.assertEqual(oracle.decode('WNW', 'wind_direction')[0], 'WNW')
        self.assertEqual(oracle.decode(1.5, 'weather_code')[1], 'unrecognized_source_value')

    def test_english_wind_codes_are_only_enabled_for_1996(self):
        raw = historical.common.ElementExtraction('wind_direction', {
            (1, 1): historical.common.source_cell('WNW'),
            (1, 2): historical.common.source_cell('-'),
            (1, 3): historical.common.source_cell(5),
            (1, 4): historical.common.source_cell('北北東'),
        })
        with patch.object(historical, 'extract_hourly', return_value=raw):
            fixed = historical.extract_wind_direction(Path('unused'), 1996, 1).cells
            self.assertEqual(fixed[(1, 1)].value, 'WNW')
            self.assertEqual(fixed[(1, 2)].flag, 'source_dash')
            self.assertEqual(fixed[(1, 3)].raw_value, 5)
            self.assertEqual(fixed[(1, 3)].flag, 'unrecognized_source_value')
            self.assertEqual(fixed[(1, 4)].value, 'NNE')
            later = historical.extract_wind_direction(Path('unused'), 1997, 1).cells
            self.assertEqual(later[(1, 1)].flag, 'unrecognized_source_value')

    def test_rejects_wrong_values_flags_raw_and_schedules(self):
        expected = {element: {(1, spec[1][0]): (None, 'source_missing', '欠測', True)}
                    for element, spec in oracle.TABLES.items()}
        refs = {element: {key: 'test!B3' for key in cells} for element, cells in expected.items()}
        good = [historical.common.ElementExtraction(element, {
            key: historical.common.SourceCell(*cell) for key, cell in cells.items()})
                for element, cells in expected.items()]
        with patch.object(oracle, 'expected_cells', return_value=(expected, refs)):
            oracle.verify_extractions({}, 1, good)
            for index, extraction in enumerate(good):
                key = next(iter(extraction.cells))
                for bad_cell in [historical.common.SourceCell(0),
                                 historical.common.SourceCell(None, 'source_blank'),
                                 historical.common.SourceCell(None, 'source_missing', '***', True)]:
                    bad = copy.deepcopy(good)
                    bad[index].cells[key] = bad_cell
                    with self.assertRaises(AssertionError):
                        oracle.verify_extractions({}, 1, bad)
                bad = copy.deepcopy(good)
                bad[index].cells[(1, 2)] = historical.common.SourceCell(42)
                with self.assertRaises(AssertionError):
                    oracle.verify_extractions({}, 1, bad)

    def test_serialized_nonobserved_hours_cannot_be_filled(self):
        expected = {element: {(day, hour): (1., None, None, False)
                             for day in range(1, 32) for hour in spec[1]}
                    for element, spec in oracle.TABLES.items()}
        extractions = [historical.common.ElementExtraction(element, {
            key: historical.common.SourceCell(*cell) for key, cell in cells.items()})
                      for element, cells in expected.items()]
        with patch.object(historical.common, 'YEAR', 1996):
            document = historical.common.assemble_month_document(1, extractions)
        document['dataset']['observation_schedules'] = {
            element: list(spec[1]) for element, spec in oracle.TABLES.items()}
        for record in document['observations']:
            for element, spec in oracle.TABLES.items():
                if element != 'weather_code' and record['source_hour'] not in spec[1]:
                    record.setdefault('flags', {})[element] = 'not_scheduled'
        with patch.object(oracle, 'expected_cells', return_value=(expected, {})):
            self.assertEqual(oracle.verify_document({}, 1, document), 744)
            for mutation in ('interpolation', 'missing_flag', 'extra_weather', 'duplicate'):
                bad = copy.deepcopy(document)
                row = bad['observations'][0]
                if mutation == 'interpolation':
                    row['values']['temperature_c'] = 1
                elif mutation == 'missing_flag':
                    row['flags']['temperature_c'] = 'source_blank'
                elif mutation == 'extra_weather':
                    row['values']['weather_code'] = 1
                else:
                    bad['observations'].append(copy.deepcopy(row))
                with self.assertRaises(AssertionError):
                    oracle.verify_document({}, 1, bad)


if __name__ == '__main__':
    unittest.main()
