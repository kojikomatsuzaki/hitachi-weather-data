"""成功した原資料検証Actionsの生成物だけを公開用ツリーへ移す。"""
from pathlib import Path
import calendar
import json
import os
import shutil
import urllib.request
import yaml

ROOT = Path(__file__).resolve().parents[1]
INCOMING = ROOT / 'build' / 'verified-1995-artifact'
RUN_ID = int(os.environ['VALIDATION_RUN_ID'])
request = urllib.request.Request(
    f'https://api.github.com/repos/kojikomatsuzaki/hitachi-weather-data/actions/runs/{RUN_ID}',
    headers={'Authorization': 'Bearer ' + os.environ['GH_TOKEN'], 'Accept': 'application/vnd.github+json'})
with urllib.request.urlopen(request, timeout=30) as response:
    run = json.load(response)
assert run['conclusion'] == 'success'
assert run['path'] == '.github/workflows/test-hitachi-1995-originals.yml'
result = json.loads((INCOMING / 'build/canonical-integration-results.json').read_text())
assert result['year'] == 1995 and result['canonical_verified'] and result['full_year_verified']
assert {entry['month'] for entry in result['months']} == set(range(1, 13))
record_count = 0
unresolved = []
for month in range(1, 13):
    relative = Path(f'data/hitachi-city-hall/1995/{month:02}.yaml')
    canonical = yaml.safe_load((INCOMING / relative).read_text())
    web_relative = Path(f'docs/data/1995/{month:02}.json')
    assert canonical == json.loads((INCOMING / web_relative).read_text())
    assert canonical['dataset']['year'] == 1995 and canonical['dataset']['month'] == month
    assert len(canonical['observations']) == calendar.monthrange(1995, month)[1] * 24
    assert len(canonical['daily_summaries']) == calendar.monthrange(1995, month)[1]
    record_count += len(canonical['observations'])
    for observation in canonical['observations']:
        for element, flag in observation.get('flags', {}).items():
            if flag == 'unrecognized_source_value':
                unresolved.append({'date': observation['source_date'], 'hour': observation['source_hour'],
                                   'element': element, 'raw_value': observation.get('raw_values', {}).get(element)})
    report_relative = Path(f'reports/validation-1995-{month:02}.md')
    assert (INCOMING / report_relative).is_file()
assert record_count == 8760
for relative in [Path('metadata/sources/hitachi-city-hall-1995.yaml'),
                 *[Path(f'{root}/1995/{month:02}.{extension}')
                   for root, extension in [('data/hitachi-city-hall', 'yaml'), ('docs/data', 'json')]
                   for month in range(1,13)],
                 *[Path(f'reports/validation-1995-{month:02}.md') for month in range(1,13)]]:
    destination = ROOT / relative
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(INCOMING / relative, destination)
result['actions_run_url'] = run['html_url']
result['validation_code_commit'] = run['head_sha']
result['canonical_records_verified'] = record_count
result['unresolved_source_cells'] = unresolved
(ROOT / 'reports/integration-1995-complete.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
state_path = ROOT / 'metadata/backfill-1997-1953.json'
state = json.loads(state_path.read_text())
state['automation_enabled'] = False
state['next_year'] = 1994
state['years']['1995'] = {'status':'success', 'records':record_count,
                         'validation_report':'reports/integration-1995-complete.json',
                         'validation_actions_url':run['html_url'], 'unrecognized_source_cells':len(unresolved)}
state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2)+'\n')
print(f'Verified publication: {record_count} records, {len(unresolved)} unresolved source cells')
