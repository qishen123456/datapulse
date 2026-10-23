"""Real HTTP/model smoke check. Run in the local backend container.

This uses the existing admin configuration without printing credentials or tokens.
It executes only the simulated gas data and saves business result snapshots.
"""
import json,time
from pathlib import Path
import requests
from controllers.auth import _admin_config

BASE='http://127.0.0.1:5002'
ROOT=Path(__file__).resolve().parents[1]
ROOT.joinpath('generated').mkdir(parents=True,exist_ok=True)
s=requests.Session();cfg=_admin_config()
r=s.post(BASE+'/api/auth/login',json=dict(username=cfg['username'],password=cfg['password']),timeout=10)
r.raise_for_status();s.headers['X-Auth-Token']=r.json()['token']
checks=[]
def post(path,payload,label):
    started=time.monotonic()
    r=s.post(BASE+path,json=payload,timeout=360)
    r.raise_for_status();data=r.json()
    rowcount=sum(len(d.get('rows') or []) for d in data.get('dataset_results',[]))
    check=dict(label=label,seconds=round(time.monotonic()-started,2),error=data.get('error'),
               flow=(data.get('workflow') or {}).get('flow'),requires_confirmation=data.get('requires_confirmation'),
               rows=rowcount,analysis_status=[d.get('analysis_status') for d in data.get('dataset_results',[])])
    checks.append(check);print(json.dumps(check,ensure_ascii=False),flush=True)
    assert not data.get('error'), check
    return data
try:
    catalog=s.get(BASE+'/api/bookshelves/datasets',timeout=20).json()['datasets']
    dsid=next(d['id'] for d in catalog if d['dataset_code']=='GAS_BIZ')
    basic=post('/api/ask-chat',dict(question='2026年9月各分公司销气量排名',selected_dataset_ids=[dsid],ask_flow='basic'),'普通问数·完整匹配金标')
    assert basic.get('rows') and basic['dataset_results'][0]['analysis_status']=='model_generated'
    free=post('/api/ask-chat',dict(question='请列出2026年9月每个分公司的总销气量，按气量从大到小排列',selected_dataset_ids=[dsid],ask_flow='basic'),'普通问数·自由措辞')
    assert free.get('rows') or free.get('requires_confirmation'), '自由问数既没有结果也没有澄清'
    plan=post('/api/ask-chat',dict(question='分析2026年9月分公司销气量与估抄率的差异，先分别核验这两个指标',selected_dataset_ids=[dsid],ask_flow='advanced'),'高阶研究·制定计划')
    assert plan.get('confirmation_type')=='research_plan'
    assert plan.get('workflow',{}).get('flow')=='advanced'
    branches=plan['research_plan']['branches']
    assert branches
    result=post('/api/ask-chat/confirm-by-boss',dict(session_id=plan['session_id'],selected_option='确认研究计划',
                selected_dataset_ids=[dsid],plan_branch_ids=[b['id'] for b in branches[:2]],ask_flow='advanced'),'高阶研究·确认后取证')
    research=result.get('research') or {}
    assert research.get('evidence'), '没有形成分支证据'
    checks[-1]['evidence']=[dict(title=e['title'],status=e['status']) for e in research['evidence']]
    checks[-1]['gaps']=research.get('gaps',[])
    # Public business snapshots only: no internal reasoning/audit trace.
    snapshot={k:basic.get(k) for k in ('question','columns','rows','row_count','analysis','dataset_results','workflow','ask_flow')}
    for ds in snapshot.get('dataset_results') or []:
        ds.pop('report_debug',None)
    ROOT.joinpath('generated/live_basic_answer.json').write_text(json.dumps(snapshot,ensure_ascii=False,indent=2))
    ROOT.joinpath('generated/live_research_answer.json').write_text(json.dumps({k:result.get(k) for k in ('question','research_plan','research','workflow','ask_flow')},ensure_ascii=False,indent=2))
finally:
    ROOT.joinpath('generated/live_ask_checks.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2))
    s.post(BASE+'/api/auth/logout',timeout=10)
