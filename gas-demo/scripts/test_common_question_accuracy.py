"""Live AI acceptance for the 48 displayed common gas questions.

Uses current PG for independent reference results, new session per question,
Up to 4 concurrent requests, no prompt/credential logging. Never returns gold SQL as AI.
"""
import argparse,datetime,decimal,json,math,os,re,threading,time
from concurrent.futures import ThreadPoolExecutor,as_completed
from pathlib import Path
from uuid import uuid4
import requests
from controllers.auth import _admin_config
from bookshelf_repository import BookshelfRepository
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'generated'/os.environ.get('GAS_COMMON_QA_OUT','common_accuracy_20261026');OUT.mkdir(parents=True,exist_ok=True)
BASE='http://127.0.0.1:5002'

def clean(v):
 if isinstance(v,decimal.Decimal):return float(v)
 if isinstance(v,(datetime.datetime,datetime.date)):return v.isoformat()[:10]
 if isinstance(v,dict):return {k:clean(x) for k,x in v.items()}
 if isinstance(v,(list,tuple)):return [clean(x) for x in v]
 return v

def query(cur,text):
 cur.execute(text);cols=[d.name for d in cur.description]
 return [dict(zip(cols,clean(row))) for row in cur.fetchall()]

def normalize(value):
 text=str(value).strip()
 if text in ENTITIES:return ENTITIES[text]
 text=re.sub(r'(\d{4})年(\d{1,2})月',lambda m:f'{m[1]}-{int(m[2]):02}',text)
 return text[:10] if re.match(r'^\d{4}-\d\d-\d\d',text) else text

def number(value,key):
 if value is None or isinstance(value,bool):return None
 try:
  v=float(str(value).replace(',','').replace('%',''))
 except (ValueError,TypeError):return None
 scale=1
 if '%' in str(value) or '%' in key or '百分' in key:scale=.01
 elif '亿元' in key or '亿方' in key:scale=1e8
 elif '万元' in key or '万方' in key:scale=1e4
 return v*scale

def equal_number(expected,actual,key):
 if expected is None:return actual is None
 actual=number(actual,key)
 if actual is None:return False
 # Only allow scaled units when explicitly named, never guess magnitude.
 tolerance=.02
 if '万' in key:tolerance=50.01
 if '亿' in key:tolerance=500000.01
 if abs(expected)<1:tolerance=.000051
 elif abs(expected)<10:tolerance=.0051
 return math.isclose(float(expected),actual,rel_tol=1e-8,abs_tol=tolerance)

def compare_rows(actual,expected,dims,metrics):
 if len(actual)!=len(expected):return False,f'结果行数 {len(actual)}，参考 {len(expected)}'
 used=set()
 for erow in expected:
  ekeys=list(erow)
  identities={normalize(erow[ekeys[i]]) for i in dims}
  candidates=[(j,a) for j,a in enumerate(actual) if j not in used and identities.issubset({normalize(v) for v in a.values() if v is not None and not isinstance(v,(int,float))})]
  matched=None
  for j,arow in candidates:
   values=list(arow.items());taken=set();good=True
   for idx in metrics:
    value=erow[ekeys[idx]]
    found=next((k for k,(key,v) in enumerate(values) if k not in taken and equal_number(value,v,key)),None)
    if found is None:good=False;break
    taken.add(found)
   if good:matched=j;break
  if matched is None:
   return False,'未匹配参考对象/指标：'+json.dumps({ekeys[i]:erow[ekeys[i]] for i in dims+metrics},ensure_ascii=False)
  used.add(matched)
 return True,'对象范围及必要指标与PG一致'

# Row identities and required business measures, not arbitrary SQL alias spellings.
SPECS={
'GAS_BIZ':[
([0],[4,5]),([0,1],[2]),([0],[3]),([0],[4]),([0],[1,3]),([0],[3,4]),([0],[2,3,5]),([0],[2,3]),
([0],[1]),([0],[1]),([],[0]),([0],[1]),([0],[1]),([0],[1]),([0],[1]),([0],[2,4])],
'GAS_AR':[
([0],[3]),([0],[2,3,4,5,6]),([0],[3]),([0,1],[8]),([0],[3]),([],[2]),([0],[1,2]),([0,1,3],[4,5]),
([],[0]),([0],[1]),([],[0]),([0],[1]),([0],[1]),([0,1],[2]),([],[0,1,2,3,4]),([],[0,1])],
'GAS_SAFE':[
([0],[2,3,4]),([0],[1,2]),([0],[1,2]),([0,1],[2]),([0],[]),([0],[3]),([0],[1]),([0],[1,2]),
([0],[1]),([0],[]),([0],[1]),([],[0]),([],[0]),([],[0]),([0],[1,2]),([0],[3])]}

def rows_of(ds):
 rows=ds.get('rows') or [];cols=ds.get('columns') or []
 names=[c.get('name') or c.get('key') if isinstance(c,dict) else c for c in cols]
 return [r if isinstance(r,dict) else dict(zip(names,r)) for r in rows]

def run_case(case):
 started=time.monotonic();result=None;stages=[];last_stage='';error=None
 try:
  with requests.post(BASE+'/api/ask-chat/stream',headers=HEADERS,json={'question':case['question'],'selected_dataset_ids':[case['dataset_id']],'ask_flow':'basic','session_id':'common-qa-'+uuid4().hex,**({'model_id':TEST_MODEL_ID} if TEST_MODEL_ID else {})},stream=True,timeout=(15,480)) as response:
   response.raise_for_status();event=''
   for line in response.iter_lines(decode_unicode=True):
    if line.startswith('event:'):event=line[6:].strip()
    elif line.startswith('data:'):
     data=json.loads(line[5:].strip())
     if event=='trace':
      t=data.get('event') or data;last_stage=str(t.get('stage') or last_stage)
      (OUT/(case['id']+'.progress.json')).write_text(json.dumps({'id':case['id'],'stage':last_stage,'status':t.get('status'),'seconds':round(time.monotonic()-started,1)},ensure_ascii=False))
      if t.get('status') in ('response','error','retry'):stages.append({'stage':t.get('stage'),'status':t.get('status'),'duration_seconds':t.get('duration_seconds'),'rate_limited':bool(re.search(r'429|TPM|rate.limit',str(t.get('error') or ''),re.I))})
     elif event=='result':result=data
     elif event=='error':error=str(data.get('error') or data.get('message') or 'stream error')
  if result is None:raise RuntimeError(error or '未收到最终结果帧')
  ds=result.get('dataset_results') or []
  record={'id':case['id'],'question':case['question'],'code':case['code'],'seconds':round(time.monotonic()-started,2),'stages':stages,'expected_rows':len(case['expected']),'requested_model_id':TEST_MODEL_ID}
  if result.get('requires_confirmation'):
   record.update(status='needs_clarification',reason=result.get('confirmation_type') or '需要确认问题范围')
  elif result.get('error') or not ds or any(d.get('query_status') not in ('completed',None) or d.get('analysis_status')!='model_generated' for d in ds):
   record.update(status='execution_failed',reason=str(result.get('error') or [d.get('error') or d.get('analysis_status') or d.get('query_status') for d in ds]))
  elif not any(s['stage']=='agent2.sql_generate' and s['status']=='response' for s in stages):
   record.update(status='unverified_ai',reason='缺少真实SQL生成模型响应记录')
  else:
   actual=[r for d in ds for r in rows_of(d)]
   good,reason=compare_rows(actual,case['expected'],*case['spec'])
   record.update(status='numeric_match' if good else 'needs_review',reason=reason,actual_rows=len(actual))
  evidence={'question':case['question'],'reference_sql':case['reference_sql'],'expected':case['expected'],'result':{k:result.get(k) for k in ['error','requires_confirmation','confirmation_type','analysis','ask_flow']},'datasets':[{k:d.get(k) for k in ['dataset_id','dataset_name','sql','columns','rows','analysis','analysis_status','query_status','error','row_count']} for d in ds]}
  previous=OUT/(case['id']+'.json')
  if previous.exists():
   archive=OUT/'attempts';archive.mkdir(exist_ok=True);previous.rename(archive/(case['id']+'-'+str(time.time_ns())+'.json'))
  previous.write_text(json.dumps(clean(evidence),ensure_ascii=False,indent=2)+'\n')
 except Exception as exc:
  record={'id':case['id'],'question':case['question'],'code':case['code'],'status':'execution_failed','reason':str(exc),'seconds':round(time.monotonic()-started,2),'stages':stages,'last_stage':last_stage}
 return record

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--limit',type=int,default=48);parser.add_argument('--only',default='');parser.add_argument('--workers',type=int,default=2);parser.add_argument('--retry-failed',action='store_true');parser.add_argument('--model-id',type=int);args=parser.parse_args();TEST_MODEL_ID=args.model_id
 config=_admin_config();login=requests.post(BASE+'/api/auth/login',json={'username':config['username'],'password':config['password']},timeout=15);login.raise_for_status();HEADERS={'X-Auth-Token':login.json()['token']}
 try:
  bundle=json.loads((ROOT/'generated/dataset_knowledge_bundle.json').read_text());cases=[]
  with BookshelfRepository()._connect() as conn,conn.cursor() as cur:
   org=query(cur,'SELECT org_id,org_name FROM v_gas_org');customers=query(cur,"SELECT DISTINCT customer_id,customer_name FROM v_gas_ar")
   ENTITIES={r['org_name']:r['org_id'] for r in org};ENTITIES.update({r['customer_name']:r['customer_id'] for r in customers})
   for ds in bundle:
    cur.execute('SELECT id FROM bs_datasets WHERE dataset_code=%s',(ds['code'],));dsid=cur.fetchone()[0]
    live=query(cur,'SELECT question_text FROM bs_common_questions WHERE dataset_id='+str(dsid)+' AND is_active ORDER BY sort_order,id')
    assert len(live)==16
    references={q['question']:q['sql'] for q in ds['queries']}
    for i,item in enumerate(live):
     q=item['question_text'];ref=references[q];code=ds['code']
     # Independent corrections where prior gold is insufficient or semantically wrong.
     if code=='GAS_BIZ' and i==2:
      ref="WITH a AS (SELECT branch_name,SUM(volume_m3) FILTER(WHERE month BETWEEN '2025-01' AND '2025-09') p,SUM(volume_m3) FILTER(WHERE month BETWEEN '2026-01' AND '2026-09') c FROM v_gas_sales GROUP BY branch_name) SELECT branch_name,p,c,(c-p)::numeric/NULLIF(p,0) AS 同比 FROM a"
     if code=='GAS_BIZ' and i==11:
      ref="SELECT CASE WHEN user_type='居民' THEN '居民' ELSE '工商业' END user_type,SUM(revenue_yuan) AS 销气收入_元 FROM v_gas_sales WHERE month='2026-09' AND user_type IN ('居民','商业','工业') GROUP BY 1"
     if code=='GAS_BIZ' and i==12:ref+=' LIMIT 1'
     if code=='GAS_AR' and i==13:
      ref="SELECT month,branch_name,SUM(revenue_yuan-theoretical_revenue_yuan) AS 重算量价差异_元 FROM v_gas_sales GROUP BY month,branch_name HAVING ABS(SUM(revenue_yuan-theoretical_revenue_yuan))>0.01"
     cases.append({'id':code+'-'+str(i+1).zfill(2),'code':code,'dataset_id':dsid,'index':i,'question':q,'reference_sql':ref,'expected':query(cur,ref),'spec':SPECS[code][i]})
  cases.sort(key=lambda c:(c['index'],c['code']))
  if args.only:cases=[c for c in cases if c['id'] in args.only.split(',')]
  else:cases=cases[:args.limit]
  summary_file=OUT/'results.json';results=json.loads(summary_file.read_text()) if summary_file.exists() else {}
  # Resume does not silently rerun completed cases; --only is an explicit retest.
  pending=cases if args.only else [c for c in cases if c['id'] not in results or (args.retry_failed and results[c['id']]['status'] in ('execution_failed','unverified_ai'))]
  (OUT/'manifest.json').write_text(json.dumps(clean(cases),ensure_ascii=False,indent=2)+'\n')
  print(json.dumps({'planned':len(cases),'pending':len(pending),'workers':args.workers}),flush=True)
  with ThreadPoolExecutor(max_workers=max(1,min(4,args.workers))) as pool:
   for future in as_completed([pool.submit(run_case,c) for c in pending]):
    r=future.result()
    if r['id'] in results:
     history_file=OUT/'attempt_history.json'
     history=json.loads(history_file.read_text()) if history_file.exists() else []
     history.append(results[r['id']]);history_file.write_text(json.dumps(history,ensure_ascii=False,indent=2)+'\n')
    results[r['id']]=r
    summary_file.write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:r.get(k) for k in ['id','status','seconds','reason']},ensure_ascii=False),flush=True)
 finally:
  requests.post(BASE+'/api/auth/logout',headers=HEADERS,timeout=15)
