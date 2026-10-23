from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy
import sqlite3
import threading
import time

import pytest

from ask_runtime import AskCancelled, bind_run, checkpoint, create_run, get_run, scope_key
from ask_stability import result_assertions, validate_sql
from ask_workflow import business_event, catalog
from config_manager import write_json
from datasource_router import DataSourceRouter
from datapulse_advanced.config_store import normalize_config
from datapulse_advanced.research import ResearchAskService
from datapulse_basic.service import BasicAskService
from ask_flow.contracts import AskRequest, ConfirmRequest
from ask_flow.controller import AskFlowController, DEFAULT_ASK_FLOW_CONFIG

USER = {'id':777,'role':'super_admin','organization_node_ids':[9]}


def test_basic_request_engine_reaches_ask_without_confirmation(monkeypatch):
    # Exercise the production wrapper branch; injected delegate-only tests miss
    # Python's function-local imports shadowing scope_key before its first use.
    from types import SimpleNamespace
    import datapulse_basic.service as module
    calls = []
    engine = SimpleNamespace(repository=SimpleNamespace(),ask=lambda **kwargs: calls.append(kwargs) or {'dataset_results':[]})
    monkeypatch.setattr(module, 'FourAgentAskService', lambda: engine)
    service = BasicAskService()
    assert service.ask(question='本月收入',current_user=USER,allowed_dataset_ids=[1]) == {'dataset_results':[]}
    assert len(calls) == 1


def test_generic_report_has_no_inherited_attainment_contract():
    from dataset_report_config import get_generic_config, merge_with_default_config
    from report_spec_builder import build_report_spec
    config = merge_with_default_config(get_generic_config())
    assert config['metrics'] == [] and config['signalRules'] == []
    report = build_report_spec('销气排名',{'id':64},[{'分公司':'滨江','销气量_方':25}],['分公司','销气量_方'],config)
    assert report['layoutTemplate'] == 'answer_canvas'
    assert '达成率' not in str(report)


def test_model_failure_keeps_facts_without_html_error_in_business_report():
    from four_agent_ask import FourAgentAskService
    from dataset_report_config import get_generic_config
    engine = FourAgentAskService.__new__(FourAgentAskService)
    context = {'dataset':{'dataset_name':'燃气'},'report_config':get_generic_config()}
    text = engine._build_fallback_analysis('销气量',context,{},
        {'rows':[{'分公司':'滨江','销气量_方':25}],'columns':['分公司','销气量_方'],'row_count':1},
        '<html>ACCESS DENIED</html>')
    assert '25' in text and 'ACCESS DENIED' not in text
    assert context['analysis_status'] == 'model_unavailable'
    assert '达成率' not in text


def test_exact_golden_cannot_bypass_ai_pipeline(monkeypatch):
    from types import SimpleNamespace
    import datapulse_basic.service as module
    calls = []
    def direct_lookup(*args):
        pytest.fail('Exact golden must not bypass the AI pipeline')
    engine = SimpleNamespace(repository=SimpleNamespace(find_exact_golden_sql=direct_lookup))
    def ask(**kwargs):
        assert engine._require_ai is True
        calls.append(kwargs)
        return {'analysis_status':'model_generated'}
    engine.ask = ask
    monkeypatch.setattr(module, 'FourAgentAskService', lambda: engine)
    service = BasicAskService()
    for _ in range(2):
        assert service.ask(question='收入',current_user=USER,allowed_dataset_ids=[1])['analysis_status']=='model_generated'
    assert len(calls)==2


def _ai_test_engine():
    from four_agent_ask import FourAgentAskService
    engine=FourAgentAskService.__new__(FourAgentAskService)
    engine._require_ai=True
    engine._get_agent_prompt=lambda *args:'model prompt'
    engine._get_lld_content=lambda *args:''
    engine._build_report_config_prompt=lambda *args:''
    engine._build_sql_output_contract_prompt=lambda *args:''
    engine._build_context_blob=lambda *args:''
    engine._resolved_entity_names=lambda *args:[]
    engine._append_trace=lambda *args,**kwargs:None
    return engine


def test_sql_model_is_required_even_when_rule_sql_is_available():
    engine=_ai_test_engine()
    engine._build_rule_based_sql=lambda *args:'SELECT 99 AS amount'
    calls=[]
    engine._chat_json=lambda *args,**kwargs:calls.append(kwargs['stage']) or {'sql':'SELECT 7 AS amount'}
    result=engine._agent2_generate_sql('收入',{}, {'dataset':{'dataset_code':'facts'}},'')
    assert result['sql']=='SELECT 7 AS amount'
    assert calls==['agent2.sql_generate']


def test_failed_sql_model_cannot_fall_back_to_golden_seed():
    engine=_ai_test_engine()
    engine._build_rule_based_sql=lambda *args:'SELECT 99 AS amount'
    calls=[]
    engine._chat_json=lambda *args,**kwargs:calls.append(kwargs['stage']) or {'sql':''}
    result=engine._agent2_generate_sql('收入',{}, {'dataset':{'dataset_code':'facts'}},'',seed_sql='SELECT 99 AS amount')
    assert result['sql']==''
    assert calls==['agent2.sql_generate','agent2.sql_generate.retry']


def test_empty_query_result_still_passes_through_ai_interpretation():
    engine=_ai_test_engine()
    calls=[]
    engine._chat=lambda *args,**kwargs:calls.append(kwargs['stage']) or '当前范围没有返回记录，不能认定收入为零。'
    engine._auto_build_detail_table=lambda *args:''
    context={'dataset':{},'report_config':{'profile':'generic'}}
    text=engine._agent4_analysis('收入',context,{}, {'rows':[],'columns':['收入'],'row_count':0})
    assert '不能认定' in text
    assert calls==['agent4.analysis']
    assert context['analysis_status']=='model_generated'


def test_empty_ai_body_is_not_masked_by_an_automatic_table():
    engine=_ai_test_engine()
    engine._chat=lambda *args,**kwargs:'<think>internal</think>'
    engine._auto_build_detail_table=lambda *args:'| automatically generated table |'
    context={'dataset':{},'report_config':{'profile':'generic'}}
    text=engine._agent4_analysis('收入',context,{}, {'rows':[{'收入':5}],'columns':['收入'],'row_count':1})
    assert context['analysis_status']=='model_unavailable'
    assert 'automatically generated table' not in text
    assert 'internal' not in text

@pytest.fixture(autouse=True)
def reset_config():
    write_json('data_permissions.json',{'rules':{}})
    write_json('organization_trees.json',{})
    write_json('advanced_capabilities.json',{})
    write_json('ask_flow.json',{})

@pytest.mark.parametrize('sql',["DELETE FROM t", "WITH x AS (DELETE FROM t RETURNING *) SELECT * FROM x", "SELECT 1; SELECT 2", "SELECT * INTO x FROM t", "SELECT * FROM t CROSS JOIN b", "SELECT * FROM t JOIN b ON 1=1", "SELECT pg_sleep(50)"])
def test_unsafe_sql_is_blocked(sql):
    with pytest.raises(ValueError): validate_sql(sql)


def test_literals_are_not_verbs():
    validate_sql("SELECT 'update', 'a;b' AS label")


def test_result_assertions_do_not_turn_null_or_empty_into_zero():
    assert result_assertions([])['status']=='empty'
    assert result_assertions([{'x':None}])['status']=='warning'
    with pytest.raises(ValueError): result_assertions([{'x':float('inf')}])


def test_retry_budget_shared_across_threads():
    run=create_run(USER,[1],'advanced',{'maxRetries':2})
    with ThreadPoolExecutor(max_workers=8) as pool:
        claims=list(pool.map(lambda _:run.claim_retry(),range(20)))
    assert sum(claims)==2


def test_cancel_blocks_next_tool_and_foreign_owner():
    run=create_run(USER,[1],'basic',{})
    with pytest.raises(PermissionError):get_run(run.id,{'id':888},[1])
    run.cancel()
    with pytest.raises(AskCancelled):
        with bind_run(run):checkpoint()


def test_policy_and_org_changes_invalidate_pending_task():
    run=create_run(USER,[1],'basic',{})
    write_json('organization_trees.json',{'revision':2})
    with pytest.raises(PermissionError):get_run(run.id,USER,[1])


def test_business_projection_never_exposes_sql_or_reasoning():
    run=create_run(USER,[1],'advanced',{})
    e=business_event({'event':{'stage':'agent2.sql_generate','status':'response','sql':'secret','thought':'private','response_text':'private','branch_id':'b2'}},run)
    assert e['branch_id']=='b2' and e['node_id']=='R19'
    assert not {'sql','thought','response_text'}.intersection(e)
    assert len(catalog('advanced'))==42 and len(catalog('basic'))==15


def sqlite_router(tmp_path):
    path=tmp_path/'facts.sqlite'
    conn=sqlite3.connect(path)
    conn.execute('CREATE TABLE facts (org TEXT, amount REAL)')
    conn.executemany('INSERT INTO facts VALUES (?,?)',[('allowed',10),('denied',999)])
    conn.commit();conn.close()
    router=DataSourceRouter()
    router.data_sources={1:{'config':{'type':'sqlite','sqlite_path':str(path)}}}
    return router,path


def test_guarded_sql_preflight_scope_readonly(tmp_path):
    router,path=sqlite_router(tmp_path)
    events=[]
    run=create_run(USER,[1],'basic',{'queryTimeoutSeconds':3,'maxResultRows':100})
    with bind_run(run):
        data=router.execute_guarded_sql(1,"SELECT amount FROM facts WHERE org='allowed'",on_preflight=lambda:events.append('explain'))
    assert data.to_dict('records')==[{'amount':10.0}] and events==['explain']
    with pytest.raises(ValueError):router.execute_guarded_sql(1,'DELETE FROM facts')
    assert sqlite3.connect(path).execute('SELECT count(*) FROM facts').fetchone()[0]==2


def test_row_limit_blocks_result(tmp_path):
    router,_=sqlite_router(tmp_path)
    run=create_run(USER,[1],'basic',{'maxResultRows':100})
    with bind_run(run),pytest.raises(ValueError,match='100'):
        router.execute_guarded_sql(1,'WITH RECURSIVE x(n) AS (SELECT 1 UNION ALL SELECT n+1 FROM x WHERE n<101) SELECT n FROM x')


class FakeEngine:
    lock=threading.Lock()
    active=0
    peak=0
    calls=[]
    fail_branch=False
    def __init__(self):self.repository=self
    def _new_trace(self,*args,**kwargs):return {}
    def route_with_agent1(self,*args,**kwargs):return {'dataset_ids':[1],'decision':'generate_sql'}
    def get_dataset_context(self,*args):return {'dataset':{'dataset_name':'测试数据'},'data_dictionary':[]}
    def _get_agent_prompt(self,*args):return 'configured expert prompt'
    def _chat_json(self,*args,**kwargs):
        if kwargs.get('stage')=='research.report':return args[2]
        if kwargs.get('stage')=='research.report_review':return {'conclusion':'已核对事实，原因待验证。','findings':[],'limitations':[]}
        return {'branches':[{'title':t,'question':t,'dataset_id':1,'hypothesis':'待验证'} for t in ['基线','结构']]}
    def _run_pipeline(self,question,route,*args,**kwargs):
        with self.lock:
            self.__class__.active+=1
            self.__class__.peak=max(self.__class__.peak,self.__class__.active)
            self.__class__.calls.append((route,kwargs.get('current_user')))
        try:
            time.sleep(.03)
            if self.fail_branch and '结构' in question:raise ValueError('controlled branch failure')
            return {'dataset_results':[{'dataset_id':1,'dataset_name':'测试数据','sql':'SELECT 1', 'columns':['amount'],'rows':[{'amount':10}], 'row_count':1,'analysis':'查询事实','analysis_status':'model_generated','agent3_review':{'approved':True}}]}
        finally:
            with self.lock:self.__class__.active-=1

@pytest.fixture
def research(monkeypatch):
    from datapulse_advanced.service import AdvancedAskService
    monkeypatch.setattr(AdvancedAskService,'_run_result_trace',lambda *a,**k:{})
    FakeEngine.calls=[];FakeEngine.peak=0;FakeEngine.active=0;FakeEngine.fail_branch=False
    return ResearchAskService(FakeEngine)


def planned(research):
    with bind_run(create_run(USER,[1],'advanced',{'maxParallel':2,'maxRetries':2})):
        return research.ask(question='本月收入为什么下降',current_user=USER,allowed_dataset_ids=[1])


def test_failed_planner_does_not_fabricate_research_plan(research,monkeypatch):
    monkeypatch.setattr(FakeEngine,'_chat_json',lambda self,*args,**kwargs:args[2])
    result=planned(research)
    assert result['error_code']=='research_plan_unavailable'
    assert not result.get('research_plan') and not FakeEngine.calls


def test_research_plan_does_not_execute_sql(research):
    result=planned(research)
    assert result['confirmation_type']=='research_plan' and result['requires_confirmation']
    assert FakeEngine.calls==[]


def test_parallel_research_uses_separate_tools_and_preserves_user(research):
    plan=planned(research)
    with bind_run(create_run(USER,[1],'advanced',{'maxParallel':2})):
        result=research.confirm_by_boss(session_id=plan['session_id'],current_user=USER,allowed_dataset_ids=[1],plan_branch_ids=['b1','b2'])
    assert len(result['research']['evidence'])==2 and FakeEngine.peak==2
    assert all(user==USER and route['dataset_ids']==[1] for route,user in FakeEngine.calls)
    assert '因果证明' in result['research']['boundary']
    assert research.confirm_by_boss(session_id=plan['session_id'],current_user=USER,allowed_dataset_ids=[1],plan_branch_ids=['b1']).get('error')


def test_partial_failure_does_not_become_full_success(research):
    plan=planned(research);FakeEngine.fail_branch=True
    with bind_run(create_run(USER,[1],'advanced',{'maxParallel':2})):
        result=research.confirm_by_boss(session_id=plan['session_id'],current_user=USER,allowed_dataset_ids=[1],plan_branch_ids=['b1','b2'])
    assert result['research']['partial'] and result['research']['gaps']==['结构']
    assert len(result['dataset_results'])==1


def test_plan_cannot_be_confirmed_by_another_user_or_scope(research):
    plan=planned(research)
    assert research.confirm_by_boss(session_id=plan['session_id'],current_user={'id':778},allowed_dataset_ids=[1],plan_branch_ids=['b1']).get('error')
    assert research.confirm_by_boss(session_id=plan['session_id'],current_user=USER,allowed_dataset_ids=[],plan_branch_ids=['b1']).get('error')


def test_required_skills_cannot_be_disabled():
    config=normalize_config({'skills':[{'key':'sql_review','enabled':False},{'key':'pandas_analyze','enabled':False}]})
    skills={s['key']:s for s in config['skills']}
    assert skills['sql_review']['enabled'] and not skills['pandas_analyze']['enabled']
    assert not config['execution']['fallbackToBasicEngine']


def test_explicit_advanced_request_never_falls_back(monkeypatch):
    class ForbiddenBasic:
        def ask(self,**kwargs):raise AssertionError('silent downgrade')
    controller=AskFlowController(basic_service=ForbiddenBasic())
    result=controller.ask(AskRequest('why',current_user=USER,allowed_dataset_ids=[1],requested_flow='advanced'))
    assert result['error_code']=='advanced_disabled'


def test_flow_limits_clamped_and_legacy_fallback_disabled():
    write_json('ask_flow.json',{'maxRetries':99,'maxParallel':99,'queryTimeoutSeconds':0,'fallbackToBasicOnError':True})
    config=AskFlowController().load_config()
    assert config['maxRetries']==2 and config['maxParallel']==4 and config['queryTimeoutSeconds']==3
    assert not config['fallbackToBasicOnError']


def test_history_scope_change_hides_nested_evidence():
    from datapulse_report_history_store import filter_history_dataset_results
    item={'reportSnapshot':{'result':{'workflow':{'flow':'advanced'},'authorization_scope':scope_key(USER,[1]),'research':{'evidence':[{'secret':99}]},'dataset_results':[{'dataset_id':1,'rows':[{'secret':99}]}]}}}
    changed={**USER,'organization_node_ids':[10]}
    result=filter_history_dataset_results([item],[1],current_user=changed)[0]['reportSnapshot']['result']
    assert 'research' not in result and not result['dataset_results']


def test_schema_vector_pruning_preserves_permission_and_relation_keys():
    from ask_stability import schema_link
    fields=[{'table_name':'orders','column_name':f'irrelevant_{i}','semantic_name':f'无关字段{i}'} for i in range(110)]
    fields += [{'table_name':'orders','column_name':'revenue','semantic_name':'销售收入'}, {'table_name':'orders','column_name':'organization_code','semantic_name':'组织编码'}, {'table_name':'orders','column_name':'customer_id','semantic_name':'客户键'}]
    context={'data_dictionary':fields,'table_relations':[{'left_table':'orders','left_key':'customer_id','right_table':'customers','right_key':'id'}]}
    linked=schema_link(context,'销售收入',limit=3)
    names={f['column_name'] for f in linked}
    assert 'revenue' in names and 'organization_code' in names and 'customer_id' in names
    assert len(context['data_dictionary'])==113


def test_immediate_cancel_before_sse_registration():
    from ask_runtime import request_cancel
    execution_id='f'*32
    assert request_cancel(execution_id,USER,[1])=='cancel_requested'
    run=create_run(USER,[1],'basic',{},execution_id)
    with pytest.raises(AskCancelled):
        with bind_run(run):checkpoint()


def test_http_controller_saves_and_clamps_execution_policy(monkeypatch):
    from flask import Flask
    from controllers import ask_flow as api
    monkeypatch.setattr(api,'get_current_user',lambda:USER)
    app=Flask(__name__);app.register_blueprint(api.ask_flow_bp)
    client=app.test_client()
    response=client.put('/api/admin/ask-flow',json={'config':{'maxRetries':99,'maxParallel':4,'queryTimeoutSeconds':19,'maxResultRows':1200,'fallbackToBasicOnError':True}})
    assert response.status_code==200
    config=response.json['data']['config']
    assert config['maxRetries']==2 and config['queryTimeoutSeconds']==19 and config['maxParallel']==4 and not config['fallbackToBasicOnError']
    monkeypatch.setattr(api,'get_current_user',lambda:{'id':778,'role':'user'})
    assert client.put('/api/admin/ask-flow',json={'config':{'maxRetries':0}}).status_code==403


def test_http_capabilities_project_authorized_controls_only(monkeypatch):
    from flask import Flask
    from controllers import ask_chat as api
    monkeypatch.setattr(api,'get_current_user',lambda:USER)
    monkeypatch.setattr(api,'_allowed_dataset_ids',lambda user:[1])
    monkeypatch.setattr(api,'_require_feature',lambda *args:None)
    monkeypatch.setattr(api.ask_flow_controller,'_role_allowed',lambda *args:True)
    write_json('ask_flow.json',{'advancedEnabled':True,'defaultFlow':'advanced','maxParallel':2})
    app=Flask(__name__);app.register_blueprint(api.ask_chat_bp)
    data=app.test_client().get('/api/ask-chat/capabilities').json['data']
    assert data['advancedAvailable'] and data['defaultFlow']=='advanced' and data['limits']['maxParallel']==2
    assert not {'advancedRoles','datasetPolicies','skills','mcp'}.intersection(data)


def test_explain_blocks_join_explosion_but_allows_large_scan_aggregation():
    from ask_stability import validate_explain
    with pytest.raises(ValueError):validate_explain([{'Plan':{'Node Type':'Hash Join','Plan Rows':10000001}}])
    validate_explain([{'Plan':{'Node Type':'Aggregate','Plan Rows':1,'Plans':[{'Node Type':'Seq Scan','Plan Rows':10000001}]}}])


def test_duplicate_branch_sql_is_not_counted_as_independent_evidence(research):
    plan=planned(research)
    with bind_run(create_run(USER,[1],'advanced',{'maxParallel':2})):
        result=research.confirm_by_boss(session_id=plan['session_id'],current_user=USER,allowed_dataset_ids=[1],plan_branch_ids=['b1','b2'])
    assert result['research']['partial']
    assert '独立' in result['research']['evidence'][1]['finding']
    assert len(result['dataset_results'])==1


def test_same_client_conversation_id_cannot_cross_user_or_org_scope():
    from memory import ShortTermMemoryStore
    from memory.scoped_memory import ScopedMemoryStore
    store=ShortTermMemoryStore()
    one=ScopedMemoryStore(store,scope_key(USER,[1]))
    other=ScopedMemoryStore(store,scope_key({'id':888,'role':'user'},[1]))
    one.remember_result('same-client-id','问收入',{'dataset_ids':[1]},{'dataset_results':[],'rows':[{'收入':10}]})
    assert one.get('same-client-id')
    assert not other.get('same-client-id')
    changed=ScopedMemoryStore(store,scope_key({**USER,'organization_node_ids':[10]},[1]))
    assert not changed.get('same-client-id')


def test_plan_and_execution_share_a_single_retry_budget(research):
    planning=create_run(USER,[1],'advanced',{'maxParallel':2,'maxRetries':2})
    with bind_run(planning):
        assert planning.claim_retry() and planning.claim_retry()
        plan=research.ask(question='核对收入变化',current_user=USER,allowed_dataset_ids=[1])
    execution=create_run(USER,[1],'advanced',{'maxParallel':2,'maxRetries':2})
    with bind_run(execution):
        research.confirm_by_boss(session_id=plan['session_id'],current_user=USER,allowed_dataset_ids=[1],plan_branch_ids=['b1'])
        assert execution.retries==2
        assert not execution.claim_retry()


def test_console_field_visibility_projects_http_result_without_changing_audit():
    from ask_projection import project_ask_result
    raw={'sql':'SELECT private','diagnostics':{'prompt':'internal'},'confidence':{'score':99},'usage':{'total_tokens':123},'research':{'evidence':[{'dataset_results':[{'dataset_name':'internal-name','sql':'SELECT nested','rows':[{'收入':10}]}],'error':'driver details'}]}}
    public=project_ask_result(raw,USER,feature_check=lambda *args:False)
    assert 'sql' not in public and 'diagnostics' not in public and 'confidence' not in public and 'usage' not in public
    dataset=public['research']['evidence'][0]['dataset_results'][0]
    assert dataset['dataset_name']=='授权数据集' and 'sql' not in dataset and dataset['rows']==[{'收入':10}]
    assert raw['sql']=='SELECT private'


def test_explicit_followup_inherits_month_and_metric_without_a_fixed_company_name():
    from memory import ShortTermMemoryStore
    memory=ShortTermMemoryStore()
    history=[{'question':'2026年9月末应收余额是多少','dataset_id':65}]
    question='只看沙湖分公司，保持刚才的月份和期末应收余额指标。'
    resolved=memory.resolve_followup(question,history)
    assert '2026年9月' in resolved and question in resolved
    assert '只替换或补充' in resolved
    assert memory.resolve_followup('沿用上一问的口径，只看高新分公司',history)
    assert memory.resolve_followup('2026年8月安检覆盖率是多少',[]) is None


def test_generic_ai_prompt_uses_actual_scope_and_does_not_force_legacy_report():
    engine=_ai_test_engine()
    captured=[]
    def chat(system,user,**kwargs):
        captured.append((system,user))
        return '2026年9月末应收余额为356,614,211.92元。'
    engine._chat=chat
    engine._auto_build_detail_table=lambda *args:''
    context={'dataset':{},'report_config':{'profile':'generic'},'row_security':{'principal_scope':'super_admin_full_scope'}}
    engine._agent4_analysis('应收余额',context,{}, {'rows':[{'应收':5}],'columns':['应收'],'row_count':1})
    assert '以下要求优先' in captured[0][0]
    assert 'super_admin_full_scope' in captured[0][1]
    assert '不得因SQL无组织WHERE' in captured[0][0]
    assert '业绩分析报告' not in captured[0][0]


def test_failed_report_review_does_not_deliver_unreviewed_draft(research,monkeypatch):
    original=FakeEngine._chat_json
    def chat(self,*args,**kwargs):
        if kwargs.get('stage')=='research.report_review':return {'review_failed':True}
        return original(self,*args,**kwargs)
    monkeypatch.setattr(FakeEngine,'_chat_json',chat)
    plan=planned(research)
    with bind_run(create_run(USER,[1],'advanced',{'maxParallel':2})):
        result=research.confirm_by_boss(session_id=plan['session_id'],current_user=USER,allowed_dataset_ids=[1],plan_branch_ids=['b1'])
    assert result['research']['partial']
    assert result['research']['summary_review']['status']=='incomplete'
    assert '研究摘要复核' in result['research']['gaps']
    assert not result['research']['summary']['findings']
    assert result['dataset_results']


def test_ai_sql_rejection_stays_rejected_and_receives_real_schema():
    engine=_ai_test_engine()
    captured=[]
    engine._build_context_blob=lambda *args:'v_facts.amount numeric'
    engine._dataset_field_validation=lambda *args:{'ok':True}
    def chat(*args,**kwargs):
        captured.append(args[1])
        return {'approved':False,'final_sql':'','review_summary':'口径不满足','risks':['wrong scope'],'fixes':[]}
    engine._chat_json=chat
    review=engine._agent3_review('查询收入',{},'SELECT amount FROM v_facts',{'dataset':{}},'')
    assert review['approved'] is False
    assert review['final_sql']==''
    assert 'v_facts.amount numeric' in captured[0]


def test_unavailable_ai_sql_review_does_not_fail_open():
    engine=_ai_test_engine()
    engine._chat_json=lambda *args,**kwargs:dict(args[2])
    review=engine._agent3_review('查询收入',{},'SELECT amount FROM v_facts',{'dataset':{}},'')
    assert review['approved'] is False
    assert '阻断' in review['review_summary']


def test_rejected_sql_is_repaired_then_reaudited_before_use():
    engine=_ai_test_engine()
    reviews=[]
    def audit(*args,**kwargs):
        reviews.append(args[2])
        return {'approved':len(reviews)>1,'final_sql':args[2],'review_summary':'check'}
    engine._agent3_review=audit
    engine._repair_sql_after_execution_error=lambda *args,**kwargs:{'sql':'SELECT amount FROM v_facts'}
    run=create_run(USER,[1],'basic',{'maxRetries':1})
    with bind_run(run):
        query,review=engine._review_sql_with_correction('收入',{},'SELECT wrong FROM v_facts',{},'','')
    assert query=='SELECT amount FROM v_facts' and review['approved']
    assert reviews==['SELECT wrong FROM v_facts','SELECT amount FROM v_facts']
    assert run.retries==1


def test_rejected_sql_correction_shares_the_global_two_retry_budget():
    engine=_ai_test_engine()
    engine._agent3_review=lambda *args,**kwargs:{'approved':False,'final_sql':'','review_summary':'denied'}
    repairs=[]
    engine._repair_sql_after_execution_error=lambda *args,**kwargs:repairs.append(1) or {'sql':'SELECT amount FROM v_facts'}
    run=create_run(USER,[1],'advanced',{'maxRetries':2})
    with bind_run(run):
        query,review=engine._review_sql_with_correction('收入',{},'SELECT x FROM v_facts',{},'','')
    assert review['approved'] is False
    assert len(repairs)==2 and run.retries==2


def test_research_does_not_promote_failed_ai_interpretation_to_completed(research,monkeypatch):
    original=FakeEngine._run_pipeline
    def pipeline(self,*args,**kwargs):
        result=original(self,*args,**kwargs)
        result['dataset_results'][0]['analysis_status']='model_unavailable'
        return result
    monkeypatch.setattr(FakeEngine,'_run_pipeline',pipeline)
    plan=planned(research)
    with bind_run(create_run(USER,[1],'advanced',{'maxParallel':2})):
        result=research.confirm_by_boss(session_id=plan['session_id'],current_user=USER,allowed_dataset_ids=[1],plan_branch_ids=['b1'])
    assert result['research']['partial']
    assert result['research']['evidence'][0]['status']=='insufficient'
    assert 'AI解读未完成' in result['research']['evidence'][0]['error']
    assert not result['dataset_results']


def test_empty_diagnosis_requires_successful_query_for_every_dataset():
    from four_agent_ask import FourAgentAskService
    check=FourAgentAskService._can_diagnose_empty_results
    assert check([{'query_status':'completed','row_count':0}])
    assert not check([])
    assert not check([{'query_status':'failed','row_count':0}])
    assert not check([{'sql':'','agent3_review':{'approved':False},'row_count':0}])
    assert not check([{'query_status':'completed','row_count':0},{'query_status':'failed','row_count':0}])
    assert not check([{'query_status':'completed','row_count':5}])


def test_failed_sql_marks_query_failure_instead_of_empty_business_answer():
    from four_agent_ask import FourAgentAskService
    engine=FourAgentAskService.__new__(FourAgentAskService)
    engine._require_ai=True
    engine._build_fallback_analysis=lambda **kwargs:'fallback'
    result=engine._build_graceful_dataset_result('销气量',{'dataset':{'id':64}},review={'approved':False})
    assert result['query_status']=='failed'
    assert result['analysis_status']=='model_unavailable'
    assert '未完成' in result['analysis']
    assert '没有查到' not in result['analysis']


def test_business_outcome_distinguishes_failure_partial_empty_and_success():
    from ask_workflow import result_outcome
    ds={'query_status':'completed','analysis_status':'model_generated','agent3_review':{'approved':True},'rows':[{'value':3}]}
    assert result_outcome({'dataset_results':[ds]})['status']=='completed'
    assert result_outcome({'dataset_results':[{**ds,'rows':[]}]})['status']=='empty'
    assert result_outcome({'dataset_results':[{**ds,'analysis_status':'model_unavailable'}]})['status']=='partial'
    assert result_outcome({'dataset_results':[{**ds,'query_status':'failed','rows':[]}]})['status']=='failed'
    assert result_outcome({'dataset_results':[ds,{**ds,'query_status':'failed','rows':[]}]})['status']=='partial'
    assert result_outcome({'requires_confirmation':True})['status']=='waiting'
    assert result_outcome({'aborted':True})['status']=='canceled'


def test_review_rejection_and_model_retry_have_explicit_business_status():
    run=create_run(USER,[1],'basic',{})
    with bind_run(run):
        rejected=business_event({'event':{'stage':'pipeline.agent3_result','status':'info','approved':False}},run)
        retry=business_event({'event':{'stage':'agent2.sql_generate','status':'retry'}},run)
    assert rejected['status']=='failed'
    assert retry['status']=='retrying'
    assert rejected['time']


@pytest.mark.parametrize('row_count,analysis_status,expected',[(0,'model_unavailable','failed'),(1,'model_unavailable','partial'),(0,'model_generated','empty'),(1,'model_generated','completed')])
def test_controller_finishes_with_business_outcome_not_transport_success(monkeypatch,row_count,analysis_status,expected):
    from types import SimpleNamespace
    from ask_flow.contracts import FlowDecision
    frames=[]
    ds={'query_status':'completed','analysis_status':analysis_status,'agent3_review':{'approved':True},'rows':[{'v':1}]*row_count}
    service=SimpleNamespace(ask=lambda **kwargs:{'dataset_results':[ds]})
    controller=AskFlowController(basic_service=service)
    monkeypatch.setattr(controller,'decide',lambda **kwargs:FlowDecision('basic','test','basic',DEFAULT_ASK_FLOW_CONFIG))
    monkeypatch.setattr('feature_flags.feature_available',lambda *args:False)
    result=controller.ask(AskRequest(question='test',current_user=USER,allowed_dataset_ids=[1],live_callback=frames.append))
    assert result['outcome']['status']==expected
    assert result['workflow']['status']==expected
    final=[f['event'] for f in frames if f.get('type')=='workflow'][-1]
    assert final['type']=='finished' and final['status']==expected
    assert any(e.get('node_id')=='L13' for e in result['workflow']['events']) == (expected in ('empty','completed'))


def test_empty_generation_and_failed_interpretation_are_not_green_info_events():
    run=create_run(USER,[1],'basic',{})
    empty=business_event({'event':{'stage':'pipeline.agent2_result','status':'info','sql':''}},run)
    partial=business_event({'event':{'stage':'pipeline.agent4_result','status':'info','analysis_status':'model_unavailable'}},run)
    assert empty['status']=='failed'
    assert partial['status']=='warning'


def test_skill_bindings_are_server_owned_and_guards_cannot_be_disabled():
    from skill_bindings import field_limit
    cfg=normalize_config({'skills':[{'key':'schema_link','enabled':False,'config':{'fieldLimit':99999},'runtime':{'executor':'archive'}}, {'key':'organization_scope','enabled':False}]})
    skills={s['key']:s for s in cfg['skills']}
    assert skills['schema_link']['enabled'] and skills['organization_scope']['enabled']
    assert field_limit(cfg)==160
    assert skills['schema_link']['runtime']['executor']=='deterministic'
    assert skills['schema_link']['runtime']['flows']==['basic','advanced']


def test_skill_instructions_bind_only_to_actual_role_and_flow():
    from skill_bindings import instructions_for
    cfg=normalize_config({'skills':[{'key':'planner','prompt':'研究规划指令'}, {'key':'sql_generate','prompt':'查询生成指令'}, {'key':'organization_scope','prompt':'不能改写权限'}, {'key':'custom_test','prompt':'不可执行扩展'}]})
    assert '研究规划指令' not in instructions_for(cfg,1,'basic')
    assert '研究规划指令' in instructions_for(cfg,1,'advanced')
    assert '查询生成指令' in instructions_for(cfg,2,'basic')
    assert '查询生成指令' in instructions_for(cfg,2,'advanced')
    assert '查询生成指令' not in instructions_for(cfg,3,'advanced')
    assert '不能改写权限' not in instructions_for(cfg,1,'advanced')
    assert '不可执行扩展' not in instructions_for(cfg,2,'advanced')


def test_engine_consumes_saved_skill_prompt(monkeypatch):
    import four_agent_ask as module
    engine=module.FourAgentAskService.__new__(module.FourAgentAskService)
    engine._skill_config=normalize_config({'skills':[{'key':'sql_generate','prompt':'优先核对数据粒度'}]})
    engine._skill_flow='basic'
    monkeypatch.setattr(module,'get_agent',lambda no:{'system_prompt':'角色原指令','knowledge_base':['业务知识']})
    prompt=engine._get_agent_prompt(2,'fallback')
    assert '优先核对数据粒度' in prompt and '角色原指令' in prompt and '业务知识' in prompt
    assert '优先核对数据粒度' not in engine._get_agent_prompt(3,'fallback')


def test_capability_save_honors_console_feature_gate(monkeypatch):
    from flask import Flask, jsonify
    from controllers import advanced_capabilities as module
    app=Flask(__name__)
    app.register_blueprint(module.advanced_capabilities_bp)
    monkeypatch.setattr(module,'get_current_user',lambda:{'role':'admin','username':'test'})
    seen=[]
    def deny(feature, message):
        seen.append(feature)
        return None,(jsonify({'error':'feature disabled'}),403)
    monkeypatch.setattr(module,'require_feature',deny)
    monkeypatch.setattr(module,'save_config',lambda data:pytest.fail('disabled feature must not write config'))
    assert app.test_client().put('/api/admin/advanced-capabilities',json={'config':{}}).status_code==403
    assert seen==['advanced_capability_save']


def test_capability_read_exposes_entry_policy_without_default_flow_confusion(monkeypatch):
    from flask import Flask
    from controllers import advanced_capabilities as module
    app=Flask(__name__);app.register_blueprint(module.advanced_capabilities_bp)
    monkeypatch.setattr(module,'get_current_user',lambda:{'role':'admin'})
    monkeypatch.setattr(module,'require_feature',lambda *args:({'role':'admin'},None))
    monkeypatch.setattr(module.AskFlowController,'load_config',lambda self:{'advancedEnabled':True,'defaultFlow':'basic','advancedRoles':['super_admin'],'datasetPolicies':{'123':'advanced'}})
    response=app.test_client().get('/api/admin/advanced-capabilities').get_json()
    assert response['data']['entryPolicy']=={'advancedEnabled':True,'defaultFlow':'basic'}
    assert len(response['data']['config']['skills'])>=21


def test_role_path_assignment_is_authoritative_and_still_requires_permission(monkeypatch):
    controller=AskFlowController()
    cfg={**DEFAULT_ASK_FLOW_CONFIG,'advancedEnabled':True,'rolePolicies':{'user':'basic','admin':'advanced'}}
    monkeypatch.setattr(controller,'load_config',lambda:cfg)
    monkeypatch.setattr(controller,'_role_allowed',lambda user,config:user.get('role')=='admin')
    assert controller.decide(user={'role':'user'},requested_flow='advanced').flow=='basic'
    assert controller.decide(user={'role':'admin'},requested_flow='basic').flow=='advanced'
    cfg['advancedEnabled']=False
    assert controller.decide(user={'role':'admin'}).flow=='basic'


def test_public_analysis_activities_never_include_raw_sql_or_model_notes():
    from analysis_activity import activity_for
    event={'stage':'pipeline.agent2_result','sql':'SELECT SUM(volume) FROM gas','notes':'private scratchpad','public_summary':'按分公司汇总指定月份的销气量。'}
    summary=activity_for(event)
    assert summary['methods']==['SUM'] and summary['public_summary'].startswith('按分公司')
    assert 'private scratchpad' not in str(summary) and 'SELECT' not in str(summary)
    event['public_summary']='```sql SELECT * FROM gas'
    assert activity_for(event)['public_summary']==''


def test_public_activity_respects_hidden_dataset_names():
    from ask_projection import project_ask_result
    value={'event':{'activity':{'dataset_name':'internal gas dataset','public_summary':'采用internal gas dataset计算','field_count':64}}}
    projected=project_ask_result(value,{},lambda key,user:key!='ask_field_dataset_hit')
    assert projected['event']['activity']['dataset_name']=='授权数据集'
    assert 'public_summary' not in projected['event']['activity']
    assert projected['event']['activity']['field_count']==64


def test_console_role_policies_are_normalized_and_clearable(monkeypatch):
    from controllers.ask_flow import _normalize_config
    cfg=_normalize_config({'rolePolicies':{'admin':'advanced','user':'basic','unknown':'advanced','super_admin':'arbitrary'}})
    assert cfg['rolePolicies']=={'admin':'advanced','user':'basic'}
    assert _normalize_config({'rolePolicies':{}})['rolePolicies']=={}
