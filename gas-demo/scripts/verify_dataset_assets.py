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
    for dataset_id,code,nmetrics,nsql,nterms in [(64,'GAS_BIZ',12,22,55),(65,'GAS_AR',9,21,51),(66,'GAS_SAFE',8,22,51)]:
        r=session.get(BASE+f'/api/bookshelves/datasets/{dataset_id}/full',timeout=20);r.raise_for_status();data=r.json()
        assert data['dataset']['dataset_code']==code
        assert len([x for x in data['agent_prompts'] if x['is_active']])==4
        assert len([x for x in data['regression_cases'] if x['is_active']])==12
        assert len([x for x in data['common_questions'] if x['is_active']])==16
        assert len([x for x in data['golden_sql_samples'] if x['is_active']])==nsql
        assert data['quality_summary']['score']==100
        glossary=next(x['config_value'] for x in data['external_configs'] if x['config_key']=='business_glossary')
        assert len(glossary)==nterms
        assert all(t['canonical'] and t['definition'] for t in glossary)
        assert any(t['alias']!=t['canonical'] for t in glossary)
        active_docs=[x for x in data['lld_documents'] if x['is_active']]
        assert len(active_docs)==1 and 'gas-semantics-20261025' in active_docs[0]['content']
        assert all('样例' in x['extraction_rule'] for x in data['data_dictionary'])
        r=session.get(BASE+f'/api/datasets/{dataset_id}/report-config',timeout=10);r.raise_for_status();report=r.json()
        assert report['is_default'] is False and report['config']['profile']=='generic'
        assert len(report['config']['metrics'])==nmetrics
        rows.append(dict(id=dataset_id,code=code,fields=len(data['data_dictionary']),metrics=nmetrics,
                         prompts=4,standard_cases=12,common_questions=16,sql_samples=nsql,glossary=nterms,
                         asset_coverage_score=data['quality_summary']['score']))
    result=dict(status='passed',datasets=rows,note='资产覆盖度不等于AI准确率；本次已执行65条SQL，未执行全部问题的完整AI链路。')
    (ROOT/'generated/dataset_asset_api_checks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(result,ensure_ascii=False))
finally:session.post(BASE+'/api/auth/logout',timeout=10)
