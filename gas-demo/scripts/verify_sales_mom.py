"""Reproduce the user's MoM question over real AI and compare with PostgreSQL."""
import json
import math
import time
from pathlib import Path
from uuid import uuid4
import requests
from controllers.auth import _admin_config
from bookshelf_repository import BookshelfRepository

question = '2026年9月各分公司销气量环比8月变化多少'
base = 'http://127.0.0.1:5002'
admin = _admin_config()
login = requests.post(base+'/api/auth/login', json={'username':admin['username'], 'password':admin['password']}, timeout=10)
login.raise_for_status()
headers = {'X-Auth-Token':login.json()['token']}
result = None
stages = []
started = time.monotonic()
try:
    with requests.post(base+'/api/ask-chat/stream', headers=headers, json={
        'question':question, 'selected_dataset_ids':[64], 'ask_flow':'basic',
        'session_id':'gas-mom-'+uuid4().hex,
    }, stream=True, timeout=(10,360)) as response:
        response.raise_for_status()
        event = ''
        for line in response.iter_lines(decode_unicode=True):
            if line.startswith('event: '): event = line[7:]
            elif line.startswith('data: '):
                payload = json.loads(line[6:])
                if event == 'result': result = payload
                if event == 'trace':
                    trace = payload.get('event') or payload
                    if trace.get('status') in ('response','error','retry'):
                        stages.append({k:trace.get(k) for k in ('stage','status')})
    assert result is not None, 'No result frame'
    datasets = result.get('dataset_results') or []
    safe = [{k:d.get(k) for k in ('dataset_id','query_status','analysis_status','sql','rows','columns','analysis','agent3_review')} for d in datasets]
    report = {'question':question,'seconds':round(time.monotonic()-started,2),'stages':stages,'datasets':safe}
    with BookshelfRepository()._connect() as conn:
        with conn.cursor() as cur:
            cur.execute("""SELECT branch_name,
                SUM(CASE WHEN month='2026-09' THEN volume_m3 ELSE 0 END) AS current,
                SUM(CASE WHEN month='2026-08' THEN volume_m3 ELSE 0 END) AS previous
                FROM v_gas_sales WHERE month IN ('2026-08','2026-09') GROUP BY branch_name""")
            expected = {name:(float(current),float(previous)) for name,current,previous in cur.fetchall()}
    try:
        assert len(datasets)==1 and datasets[0].get('analysis_status')=='model_generated', 'AI answer incomplete'
        assert datasets[0].get('query_status')=='completed', 'Query did not complete'
        assert all(any(t['stage']==stage and t['status']=='response' for t in stages)
                   for stage in ('agent2.sql_generate','agent3.sql_review','agent4.analysis')), 'Missing real AI stage response'
        rows = datasets[0].get('rows') or []
        assert len(rows)==len(expected)==5, 'Expected five sales branches'
        seen = set()
        for row in rows:
            name = next((v for v in row.values() if isinstance(v,str) and v in expected),None)
            assert name and name not in seen, 'Branch missing or duplicated'
            seen.add(name)
            current,previous = expected[name]
            diff = current-previous
            rate = diff/previous
            numbers = [float(v) for v in row.values() if isinstance(v,(int,float)) and not isinstance(v,bool)]
            assert any(math.isclose(v,diff,abs_tol=.02) or math.isclose(v,rate,abs_tol=1e-5)
                       or math.isclose(v,rate*100,abs_tol=.011) for v in numbers), f'{name}: MoM differs from PG'
        report['status'] = 'passed'
    except AssertionError as error:
        report.update(status='failed',error=str(error))
    out = Path('/tmp/gas-sales-mom-result.json')
    out.write_text(json.dumps(report,ensure_ascii=False,indent=2,default=str))
    print(json.dumps({k:report[k] for k in ('status','seconds','error') if k in report},ensure_ascii=False))
    if report['status'] != 'passed': raise SystemExit(1)
finally:
    requests.post(base+'/api/auth/logout',headers=headers,timeout=10)
