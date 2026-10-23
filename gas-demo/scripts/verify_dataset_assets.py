"""Verify management APIs see committed gas assets; never print auth credentials."""
import json
from pathlib import Path
import requests
from controllers.auth import _admin_config
ROOT=Path(__file__).resolve().parents[1]
BASE='http://127.0.0.1:5002'
cfg=_admin_config();session=requests.Session()
r=session.post(BASE+'/api/auth/login',json={'username':cfg['username'],'password':cfg['password']},timeout=10);r.raise_for_status()
session.headers['X-Auth-Token']=r.json()['token']
rows=[]
try:
    for dataset_id,code,nmetrics in [(64,'GAS_BIZ',12),(65,'GAS_AR',9),(66,'GAS_SAFE',8)]:
        r=session.get(BASE+f'/api/bookshelves/datasets/{dataset_id}/full',timeout=20);r.raise_for_status();data=r.json()
        assert data['dataset']['dataset_code']==code
        assert len([x for x in data['agent_prompts'] if x['is_active']])==4
        assert len([x for x in data['regression_cases'] if x['is_active']])==4
        assert len([x for x in data['common_questions'] if x['is_active']])==12
        assert len([x for x in data['golden_sql_samples'] if x['is_active']])==12
        assert data['quality_summary']['score']==100
        r=session.get(BASE+f'/api/datasets/{dataset_id}/report-config',timeout=10);r.raise_for_status();report=r.json()
        assert report['is_default'] is False and report['config']['profile']=='generic'
        assert len(report['config']['metrics'])==nmetrics
        rows.append(dict(id=dataset_id,code=code,fields=len(data['data_dictionary']),metrics=nmetrics,
                         prompts=4,standard_cases=4,common_questions=12,sql_samples=12,
                         asset_coverage_score=data['quality_summary']['score']))
    result=dict(status='passed',datasets=rows,note='资产覆盖度不等于AI准确率；本次未执行36题的完整AI链路。')
    (ROOT/'generated/dataset_asset_api_checks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(result,ensure_ascii=False))
finally:session.post(BASE+'/api/auth/logout',timeout=10)
