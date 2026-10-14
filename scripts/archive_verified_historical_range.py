#!/usr/bin/env python3
"""1994→1991を順次照合し、成功した年だけをコミットする。

一括スキップは行わない。途中のエラーで停止し、次の年へは進まない。
原資料の取得、生成、独立照合、公開ファイルの一致を年ごとに完結させる。
"""
from __future__ import annotations
import argparse
import calendar
from collections import Counter
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = ROOT / 'metadata/backfill-1997-1953.json'
RUN_URL = f"https://github.com/kojikomatsuzaki/hitachi-weather-data/actions/runs/{os.environ['GITHUB_RUN_ID']}"

def run(*arguments):
    subprocess.run(arguments, cwd=ROOT, check=True)

def commit(paths, message):
    run('git', 'add', *paths)
    if subprocess.run(['git','diff','--cached','--quiet'], cwd=ROOT).returncode:
        run('git','commit','-m',message)
        run('git','push','origin','HEAD:main')

def check_year(year, result_path):
    result = json.loads(result_path.read_text())
    assert result['year'] == year and result['full_year_verified'] and result['canonical_verified']
    assert {item['month'] for item in result['months']} == set(range(1,13))
    records = days = 0
    unresolved = []
    flags = Counter()
    for month in range(1,13):
        canonical = yaml.safe_load((ROOT / f'data/hitachi-city-hall/{year}/{month:02}.yaml').read_text())
        web = json.loads((ROOT / f'docs/data/{year}/{month:02}.json').read_text())
        assert canonical == web
        assert canonical['dataset']['year'] == year and canonical['dataset']['month'] == month
        expected_days = calendar.monthrange(year,month)[1]
        assert len(canonical['observations']) == expected_days * 24
        assert len(canonical['daily_summaries']) == expected_days
        records += len(canonical['observations'])
        days += expected_days
        for observation in canonical['observations']:
            for element, flag in observation.get('flags',{}).items():
                flags[flag] += 1
                if flag == 'unrecognized_source_value':
                    unresolved.append({'date':observation['source_date'],'hour':observation['source_hour'],
                        'element':element,'raw_value':observation.get('raw_values',{}).get(element)})
    result.update(actions_run_url=RUN_URL, validation_code_commit=os.environ['GITHUB_SHA'],
        canonical_records_verified=records, daily_summary_count=days,
        scheduled_observation_cells_verified=sum(sum(element['observation_cells'] for element in month['independent_observations'].values()) for month in result['months']),
        unresolved_source_cells=unresolved, observation_flag_counts=dict(flags))
    report = ROOT / f'reports/integration-{year}-complete.json'
    report.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    return result

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--start-year', type=int, default=1994)
    parser.add_argument('--end-year', type=int, default=1991)
    arguments = parser.parse_args()
    if not 1986 <= arguments.end_year <= arguments.start_year <= 1994:
        raise ValueError('Requested range must remain within inspected 1986–1994 sources')
    state = json.loads(STATE_PATH.read_text())
    assert state['automation_enabled'] is False and state['next_year'] == arguments.start_year
    run('git','config','user.name','github-actions[bot]')
    run('git','config','user.email','41898282+github-actions[bot]@users.noreply.github.com')
    run(sys.executable,'-m','unittest','discover','-s','tests','-v')
    for year in range(arguments.start_year, arguments.end_year - 1, -1):
        print(f'BEGIN {year}',flush=True)
        source_directory = ROOT / f'build/source-{year}'
        source_directory.mkdir(parents=True,exist_ok=True)
        for archive in (ROOT/'build/historical-archives').glob('*.zip'):
            shutil.copyfile(archive,source_directory/archive.name)
        try:
            run(sys.executable,'scripts/discover_hitachi_city_hall_historical_sources.py','--year',str(year))
            run(sys.executable,'scripts/test_hitachi_1996_originals.py','--year',str(year),
                '--source-directory',str(source_directory),'--months',*map(str,range(1,13)),
                '--download-missing','--output',f'build/source-integration-{year}.json')
            for month in range(1,13):
                run(sys.executable,'scripts/import_hitachi_city_hall_historical_year.py','--year',str(year),'--month',str(month))
            run(sys.executable,'scripts/generate_web_data.py','--year',str(year))
            result_path = ROOT / f'build/canonical-integration-{year}.json'
            run(sys.executable,'scripts/test_hitachi_1996_originals.py','--year',str(year),
                '--source-directory',str(source_directory),'--months',*map(str,range(1,13)),
                '--verify-canonical','--output',str(result_path))
            result = check_year(year,result_path)
            state['years'][str(year)] = {
                'status':'success','records':result['canonical_records_verified'],
                'validation_report':f'reports/integration-{year}-complete.json',
                'validation_actions_url':RUN_URL,
                'validated_observation_cells':result['scheduled_observation_cells_verified'],
                'unrecognized_source_cells':len(result['unresolved_source_cells']),
                'last_validation_at':datetime.now(timezone.utc).isoformat()}
            state['next_year'] = year-1
            state['last_attempt_year'] = year
            state['last_attempt_at'] = datetime.now(timezone.utc).isoformat()
            state['automation_enabled'] = False
            STATE_PATH.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n')
            report_path = ROOT / f'reports/validation-{year}-independent-observations.md'
            report_path.write_text(f'# {year}年・全月原資料照合\n\n'
                f'- 12か月、{result["daily_summary_count"]}日、{result["canonical_records_verified"]}時間レコード。\n'
                f'- 11要素、{result["scheduled_observation_cells_verified"]}観測対象セルを独立照合。\n'
                f'- 未解釈の原表記：{len(result["unresolved_source_cells"])}件。値とフラグと原表記を保持。\n'
                f'- 原ZIP・XLSのチェックサム、生成前後のセル照合、日別集計、YAML/JSON一致を検証。\n'
                f'- 検証Actions：{RUN_URL}\n'
                '- 比較はLibreOfficeで読取用に変換したXLSXを使う。変換自体の完全性を別ソフトで保証するものではない。\n'
                '- 原資料の空欄をゼロへ置換せず、非観測時刻をnot_scheduledで区別する。自動遡及は停止中。\n')
            readme_path = ROOT / 'README.md'
            readme_path.write_text(readme_path.read_text().replace(f'収録済み：{year+1}–',f'収録済み：{year}–'))
            paths=[f'data/hitachi-city-hall/{year}',f'docs/data/{year}','docs/data/index.json',
                f'metadata/sources/hitachi-city-hall-{year}.yaml','metadata/backfill-1997-1953.json','README.md',
                f'reports/integration-{year}-complete.json',f'reports/validation-{year}-independent-observations.md',
                *[f'reports/validation-{year}-{month:02}.md' for month in range(1,13)]]
            commit(paths,f'Publish independently verified {year} archive')
            print(f'COMPLETE {year}: {result["canonical_records_verified"]} records; {len(result["unresolved_source_cells"])} unresolved',flush=True)
        except Exception as error:
            state['automation_enabled'] = False
            state['next_year'] = year
            state['last_attempt_year'] = year
            state['last_attempt_at'] = datetime.now(timezone.utc).isoformat()
            state['years'][str(year)] = {'status':'failed','error':str(error),'validation_actions_url':RUN_URL}
            STATE_PATH.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n')
            commit(['metadata/backfill-1997-1953.json'],f'Record {year} failure and stop bounded backfill')
            raise

if __name__ == '__main__':
    main()
