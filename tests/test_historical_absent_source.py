"""原ファイルなしを空欄・欠測・非観測時刻と混同しないための回帰検証。"""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile
import yaml
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import discover_hitachi_city_hall_historical_sources as discovery
import import_hitachi_city_hall_historical_year as historical
import verify_1996_source_cells as oracle

class AbsentSourceTests(unittest.TestCase):
    def test_verified_absence_is_limited_to_inspected_years(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / 'source'; source.mkdir()
            (root / 'metadata/sources').mkdir(parents=True)
            archive = source / 'dew_point_temperature.zip'
            with zipfile.ZipFile(archive, 'w') as z:
                z.writestr('dewp1983.xls', b'placeholder original')
            catalog = root / 'catalog.yaml'
            catalog.write_text(yaml.safe_dump({'source_collection': {'landing_page': 'https://example.test/'}, 'archives': [{
                'file_name': archive.name, 'element': 'dew_point_temperature',
                'url': 'https://example.test/dew.zip', 'member_prefix': 'dewp',
                'sha256': discovery.sha256_path(archive)}]}))
            with patch.object(discovery, 'REPOSITORY_ROOT', root), patch.object(discovery, 'CATALOG_PATH', catalog):
                # Keep the catalog inside the repository so its provenance path is serializable.
                inside = root / 'metadata/sources/catalog.yaml'; inside.write_text(catalog.read_text())
                with patch.object(discovery, 'CATALOG_PATH', inside):
                    manifest = yaml.safe_load(discovery.discover_year(1982, source).read_text())
                    self.assertEqual(manifest['files'][0]['status'], 'not_available_for_period')
                    with self.assertRaises(ValueError): discovery.discover_year(1980, source)
            paths, _, archives = historical.prepare_source_files(manifest, source, False)
            self.assertEqual(paths, {})
            self.assertEqual(archives[0]['status'], 'verified')
            with zipfile.ZipFile(archive, 'a') as z: z.writestr('dewp1982.xls', b'unexpected')
            manifest['files'][0]['archive_sha256'] = discovery.sha256_path(archive)
            with self.assertRaises(AssertionError): historical.prepare_source_files(manifest, source, False)

    def test_absence_cannot_be_interpolated_or_relabelled_blank(self):
        year, month = 1982, 1
        extraction = historical.unavailable_dew_point(year, month)
        self.assertEqual(len(extraction.cells), 744)
        self.assertTrue(all(c.value is None and c.flag == 'source_file_unavailable' for c in extraction.cells.values()))
        with self.assertRaises(ValueError): historical.unavailable_dew_point(1983, month)
        specs = oracle.table_specs(year)
        expected = {element: {(day, hour): (1., None, None, False)
                             for day in range(1,32) for hour in spec[1]}
                    for element, spec in specs.items()}
        expected['dew_point_temperature_c'] = {key: (None,'source_file_unavailable',None,False) for key in extraction.cells}
        extractions = [historical.common.ElementExtraction(e, {key: historical.common.SourceCell(*cell) for key,cell in cells.items()}) for e,cells in expected.items()]
        with patch.object(historical.common,'YEAR',year): document=historical.common.assemble_month_document(month,extractions)
        document['dataset']['observation_schedules']={e:list(spec[1]) for e,spec in specs.items()}
        document['dataset']['element_availability']={'dew_point_temperature_c':{'status':'not_available_for_period'}}
        document['daily_summaries']=[]
        for row in document['observations']:
            for e,spec in specs.items():
                if e not in ('weather_code','dew_point_temperature_c') and row['source_hour'] not in spec[1]:row.setdefault('flags',{})[e]='not_scheduled'
        with patch.object(oracle,'expected_cells',return_value=(expected,{})):
            self.assertEqual(oracle.verify_document({},month,document,year),744)
            for flag,value in [('source_blank',None),('not_scheduled',None),('source_file_unavailable',1.)]:
                bad=copy.deepcopy(document);bad['observations'][0]['flags']['dew_point_temperature_c']=flag;bad['observations'][0]['values']['dew_point_temperature_c']=value
                with self.assertRaises(AssertionError):oracle.verify_document({},month,bad,year)
