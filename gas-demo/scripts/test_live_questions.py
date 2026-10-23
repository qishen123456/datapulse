"""Real AI + PG acceptance over simulated gas data. Never saves model prompts or credentials."""
import json
import os
from uuid import uuid4
import math
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import requests
from controllers.auth import _admin_config
from bookshelf_repository import BookshelfRepository

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'generated'/'question_tests'
OUT.mkdir(parents=True,exist_ok=True)
BASE='http://127.0.0.1:5002'
checks={}
FOLLOWUP_ONLY=os.environ.get("GAS_QA_FOLLOWUP_ONLY")=="1"
RETEST=os.environ.get("GAS_QA_RETEST")=="1"
HIGH_ONLY=os.environ.get("GAS_QA_HIGH_ONLY")=="1"
if (FOLLOWUP_ONLY or RETEST or HIGH_ONLY) and (OUT/"results.json").exists():
    checks=json.loads((OUT/"results.json").read_text())
    checks.pop('run_error',None)


def save():
    (OUT/'results.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2,default=str)+'\n')


def snapshot(data):
    return {key:data.get(key) for key in ('question','error','requires_confirmation','confirmation_type','session_id','conversation_session_id','research_plan','research','rows','columns','analysis','dataset_results','ask_flow') if key in data}


def post(path,payload):
    started=time.monotonic()
    model_stages=[]
    result=None
    with requests.post(BASE+path,json=payload,headers=headers,stream=True,timeout=(10,360)) as response:
        response.raise_for_status()
        event=''
        for line in response.iter_lines(decode_unicode=True):
            if line.startswith('event: '):event=line[7:]
            elif line.startswith('data: '):
                data=json.loads(line[6:])
                if event=='trace':
                    entry=data.get('event') or data
                    if entry.get('status')=='response' and str(entry.get('stage','')).startswith(('agent1','agent2','agent3','agent4','research')):
                        model_stages.append(entry['stage'])
                elif event=='result':result=data
    if result is None:raise AssertionError('没有收到结果帧')
    return result,dict(seconds=round(time.monotonic()-started,2),model_responses=model_stages)


def datasets(data):return data.get('dataset_results') or []
def all_rows(data):return [row for ds in datasets(data) for row in ds.get('rows',[])]
def assert_ai(data,meta):
    assert not data.get('error'),data.get('error')
    assert not data.get('requires_confirmation'),'意外要求确认'
    assert datasets(data),'没有结果集'
    assert all(ds.get('analysis_status')=='model_generated' for ds in datasets(data)), 'AI解读未完成'
    assert 'agent2.sql_generate' in meta['model_responses'],'没有SQL生成的真实模型响应'
    assert 'agent4.analysis' in meta['model_responses'],'没有结果解读的真实模型响应'


def number(row,pattern):
    keys=[key for key in row if any(token in key.lower() for token in pattern)]
    values=[row[key] for key in keys if isinstance(row[key],(int,float)) and not isinstance(row[key],bool)]
    if not values:values=[value for value in row.values() if isinstance(value,(int,float)) and not isinstance(value,bool)]
    assert len(values)==1,f'无法唯一识别指标列：{list(row)}'
    return float(values[0])


def series(data,pattern):
    result={}
    for row in all_rows(data):
        names=[value for value in row.values() if isinstance(value,str) and value.endswith('分公司')]
        assert len(names)==1,f'无法唯一识别分公司：{list(row)}'
        assert names[0] not in result,'分公司重复，疑似分组粒度错误'
        result[names[0]]=number(row,pattern)
    return result


def compare(actual,expected,tolerance=.02):
    assert set(actual)==set(expected),f'对象集合不一致：actual={list(actual)} expected={list(expected)}'
    for key,value in expected.items():
        assert math.isclose(actual[key],float(value),abs_tol=tolerance,rel_tol=1e-8),f'{key} 数值错误 actual={actual[key]} expected={value}'


def execute(label,question,code,expected,kind,extra=None):
    result=None
    meta={}
    try:
        payload=dict(question=question,selected_dataset_ids=[ids[code]],ask_flow='basic',**(extra or {}))
        payload.setdefault('session_id','gas-qa-'+uuid4().hex)
        result,meta=post('/api/ask-chat/stream',payload)
        assert_ai(result,meta)
        if kind=='series':compare(series(result,['销气','sales','volume']),expected)
        elif kind=='rate':compare(series(result,['覆盖率','rate']),expected,1e-7)
        elif kind=='scalar':
            rows=all_rows(result)
            assert len(rows)==1,f'预期一个汇总结果，实际{len(rows)}行'
            assert math.isclose(number(rows[0],['应收','closing','余额']),float(expected),abs_tol=.02,rel_tol=1e-8),'汇总值与PG不一致'
        elif kind=='empty':
            assert not all_rows(result),'无数据月份返回了业务记录'
            text='\n'.join(str(ds.get('analysis') or '') for ds in datasets(result))
            assert any(word in text for word in ('无数据','未返回','没有','未匹配','未查询','查无','空','缺少')), '未明确说明数据缺失'
        check=dict(status='passed',question=question,code=code,rows=len(all_rows(result)),**meta)
    except Exception as exc:
        check=dict(status='failed',question=question,code=code,error=str(exc),**meta)
    if result:
        # Keep business evidence only; strip internal prompts/debug/reasoning.
        clean=snapshot(result)
        clean['dataset_results']=[{k:ds.get(k) for k in ('dataset_id','dataset_name','sql','columns','rows','analysis','analysis_status','row_count')} for ds in datasets(result)]
        if clean.get('research'):
            for evidence in clean['research'].get('evidence',[]):
                evidence['dataset_results']=[{k:ds.get(k) for k in ('dataset_id','dataset_name','sql','columns','rows','analysis','analysis_status','row_count')} for ds in evidence.get('dataset_results',[])]
        (OUT/(label+'.json')).write_text(json.dumps(clean,ensure_ascii=False,indent=2,default=str)+'\n')
    return label,check,result


cfg=_admin_config()
login=requests.post(BASE+'/api/auth/login',json={'username':cfg['username'],'password':cfg['password']},timeout=10)
login.raise_for_status()
headers={'X-Auth-Token':login.json()['token']}
try:
    catalog=requests.get(BASE+'/api/bookshelves/datasets',headers=headers,timeout=20).json()['datasets']
    ids={d['dataset_code']:d['id'] for d in catalog if d['dataset_code'].startswith('GAS_')}
    repo=BookshelfRepository()
    with repo._connect() as conn,conn.cursor() as cur:
        cur.execute("SELECT branch_name,SUM(volume_m3) FROM v_gas_sales WHERE month='2026-09' GROUP BY branch_name")
        sales=dict(cur.fetchall())
        cur.execute("SELECT SUM(closing_yuan),SUM(closing_yuan) FILTER(WHERE branch_id='SHAHU') FROM v_gas_ar WHERE month='2026-09'")
        ar,ar_shahu=cur.fetchone()
        cur.execute("SELECT branch_name,SUM(inspected)::numeric/NULLIF(SUM(due_inspect),0) FROM v_gas_safety WHERE month='2026-09' GROUP BY branch_name")
        rates=dict(cur.fetchall())
        cur.execute("SELECT branch_name,SUM(estimated_meter_m3)/NULLIF(SUM(volume_m3),0) FROM v_gas_sales WHERE month='2026-09' GROUP BY branch_name")
        estimate_rates=dict(cur.fetchall())
    cases=[('B01_sales','请列出2026年9月每个分公司的总销气量，按气量从大到小排列','GAS_BIZ',sales,'series'),
           ('B02_ar','2026年9月末应收余额是多少','GAS_AR',ar,'scalar'),
           ('B03_safety','2026年9月各分公司的安检覆盖率是多少？按已检户数合计除以应检户数合计，返回0到1的小数。','GAS_SAFE',rates,'rate'),
           ('B04_empty','2026年10月各分公司销气量是多少？严格只查2026年10月，没有数据请明确说明，不要改用9月。','GAS_BIZ',None,'empty')]
    if FOLLOWUP_ONLY or RETEST:cases=[case for case in cases if case[0]=='B02_ar']
    if HIGH_ONLY:cases=[]
    answers={}
    with ThreadPoolExecutor(max_workers=2) as pool:
        futures=[pool.submit(execute,*case) for case in cases]
        for future in as_completed(futures):
            label,check,result=future.result();checks[label]=check;answers[label]=result;save();print(json.dumps({label:check},ensure_ascii=False),flush=True)
    if not HIGH_ONLY:
        prior=answers.get('B02_ar') or {}
        session=prior.get('conversation_session_id')
        if session:
            label,check,result=execute('B05_followup','只看沙湖分公司，保持刚才的月份和期末应收余额指标。','GAS_AR',ar_shahu,'scalar',dict(session_id=session))
            checks[label]=check;save();print(json.dumps({label:check},ensure_ascii=False),flush=True)
        else:
            checks['B05_followup']={'status':'failed','error':'上一问未返回会话ID，无法核对真实上下文追问'};save()
    if not FOLLOWUP_ONLY:
        active_stage='H01_plan'
        started=time.monotonic()
        plan,meta=post('/api/ask-chat/stream',dict(question='分析2026年9月分公司销气量与估抄率的差异，先分别核验这两个指标，只设计两个研究方向，不要推断盗气原因。',selected_dataset_ids=[ids['GAS_BIZ']],ask_flow='advanced'))
        assert plan.get('confirmation_type')=='research_plan',plan.get('error') or '未返回研究计划'
        assert not datasets(plan),'计划确认前不应执行取证查询'
        checks['H01_plan']=dict(status='passed',branches=len(plan['research_plan']['branches']),**meta);save();print(json.dumps({'H01_plan':checks['H01_plan']},ensure_ascii=False),flush=True)
        active_stage='H02_research'
        branch_ids=[branch['id'] for branch in plan['research_plan']['branches'][:2]]
        result,meta=post('/api/ask-chat/confirm-by-boss/stream',dict(session_id=plan['session_id'],selected_option='确认研究计划',selected_dataset_ids=[ids['GAS_BIZ']],plan_branch_ids=branch_ids,ask_flow='advanced'))
        assert not result.get('error'),result.get('error')
        research=result.get('research') or {}
        evidence=research.get('evidence') or []
        public=json.loads(json.dumps(research,default=str))
        for entry in public.get('evidence',[]):
            entry['dataset_results']=[{k:ds.get(k) for k in ('dataset_id','dataset_name','sql','columns','rows','analysis','analysis_status','row_count')} for ds in entry.get('dataset_results',[])]
        (OUT/'H02_research.json').write_text(json.dumps({'question':result.get('question'),'research':public},ensure_ascii=False,indent=2)+'\n')
        assert {entry['id'] for entry in evidence}==set(branch_ids),'分支证据与确认计划不一致'
        assert all(entry.get('status')=='completed' for entry in evidence),'部分分支未形成可用证据'
        for entry in evidence:
            assert entry.get('dataset_results'),'分支缺少查询结果'
            assert all(ds.get('analysis_status')=='model_generated' for ds in entry['dataset_results']),'分支AI解读未完成'
            for ds in entry['dataset_results']:
                if any('估抄率' in key for key in ds.get('columns',[])):
                    compare(series({'dataset_results':[ds]},['估抄率']),estimate_rates,1e-7)
                else:
                    compare(series({'dataset_results':[ds]},['销气量','volume','sales_m3']),sales)
        assert research.get('summary',{}).get('conclusion'),'没有最终研究结论'
        assert research.get('summary_review',{}).get('status')=='completed','摘要复核未完成'
        assert 'research.report_review' in meta['model_responses'],'未观测到报告复核的真实模型响应'
        clean=dict(question=result.get('question'),research_plan=result.get('research_plan'),research=research)
        for entry in evidence:
            entry['dataset_results']=[{k:ds.get(k) for k in ('dataset_id','dataset_name','sql','columns','rows','analysis','analysis_status','row_count')} for ds in entry.get('dataset_results',[])]
        (OUT/'H02_research.json').write_text(json.dumps(clean,ensure_ascii=False,indent=2,default=str)+'\n')
        checks['H02_research']=dict(status='passed',branches=len(evidence),evidence=[dict(title=e['title'],status=e['status']) for e in evidence],**meta);save();print(json.dumps({'H02_research':checks['H02_research']},ensure_ascii=False),flush=True)
except Exception as exc:
    label=globals().get('active_stage','run_error')
    checks[label]={'status':'failed','error':str(exc)};save();print(json.dumps({label:checks[label]},ensure_ascii=False),flush=True)
finally:
    requests.post(BASE+'/api/auth/logout',headers=headers,timeout=10)
print(json.dumps({'completed':len(checks),'failed':[key for key,value in checks.items() if value['status']!='passed']},ensure_ascii=False),flush=True)
