"""Independent research orchestration over the existing specialist tools.

The ordinary service is never called. Each parallel branch owns its engine
instance, model selection and trace; organization filtering remains in the
shared specialist pipeline, immediately before every SQL execution.
"""
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from copy import deepcopy
import json
import threading
import time
from uuid import uuid4

from ask_runtime import bind_run, checkpoint, current_run, owner_key, scope_key
from four_agent_ask import FourAgentAskService
from .config_store import load_config, REQUIRED_SKILLS
from ask_stability import schema_link
from memory import ShortTermMemoryStore
from memory.scoped_memory import ScopedMemoryStore
from .skills.planner import PlannerSkill


class ResearchAskService:
    name = 'advanced'

    def __init__(self, engine_factory=None):
        self.engine_factory = engine_factory or FourAgentAskService
        self._plans = {}
        self._memory = ShortTermMemoryStore(max_rounds=8)
        self._lock = threading.RLock()

    @property
    def repository(self):
        from datapulse_basic.service import basic_ask_service
        return basic_ask_service.repository

    def _engine(self, model_id=None):
        engine = self.engine_factory()
        engine._preferred_model_id = model_id
        engine._skill_flow = 'advanced'
        engine._skill_config = load_config()
        return engine

    @staticmethod
    def _emit(live, node, status, summary, **extra):
        checkpoint()
        if live:
            live({'type':'trace', 'event': {'stage':'research.' + node, 'node_id':node,
                  'status':status, 'business_summary':summary, **extra}})

    @staticmethod
    def _public(plan):
        return {key:deepcopy(plan[key]) for key in ('id','question','branches','created','version','limits')}

    def ask(self, **kwargs):
        config = load_config()
        if not config.get('enabled'):
            return {'error':'高阶研究能力已被控制台关闭。', 'error_code':'research_disabled'}
        enabled = {s['key'] for s in config.get('skills',[]) if s.get('enabled')}
        required = REQUIRED_SKILLS
        if not required.issubset(enabled):
            return {'error':'高阶研究的必要 Skill 已关闭，请管理员检查能力中心。', 'error_code':'research_skills_disabled'}
        user = kwargs.get('current_user') or {}
        allowed = set(int(x) for x in kwargs.get('allowed_dataset_ids') or [])
        if not allowed:
            return {'error':'当前账号没有可用的数据集权限。'}
        question = str(kwargs.get('question') or '').strip()
        memory = ScopedMemoryStore(self._memory, scope_key(user,allowed))
        history = memory.get(kwargs.get('session_id'))
        effective_question = memory.resolve_followup(question,history) or question
        live = kwargs.get('live_callback')
        engine = self._engine(kwargs.get('model_id'))
        trace = engine._new_trace(question, 'research.plan', live_callback=live)
        self._emit(live,'R01','completed','已受理研究目标；取证将在计划确认后启动。')
        self._emit(live,'R02','completed','已按当前账号的组织树授权收窄数据资产。')
        brief = {'question':question,'method':PlannerSkill.infer(question)}
        self._emit(live,'R03','completed','已记录研究问题，后续分支必须保留原始范围。')
        self._emit(live,'R05','running','正在匹配研究所需的数据域。')
        route = engine.route_with_agent1(effective_question, trace=trace, allowed_dataset_ids=sorted(allowed), conversation_context=history, current_question=question)
        checkpoint()
        preferred = [int(x) for x in kwargs.get('preferred_dataset_ids') or [] if int(x) in allowed]
        datasets = preferred or [int(x) for x in route.get('dataset_ids',[]) if int(x) in allowed]
        if not datasets:
            return {'error':'没有找到授权范围内可用于研究的数据集，请先选择数据范围。', 'question':question}
        if route.get('requires_confirmation') and not preferred:
            # Present the engine's actual alternatives; do not arbitrarily select one.
            return {'error':'研究数据范围有歧义，请在输入区选定数据集后重新生成计划。', 'question':question}
        asset_limit = min(4,max(1,int((config.get('execution') or {}).get('assetPreviewLimit',3))))
        if len(datasets) > asset_limit:
            return {'error':f'本次研究命中 {len(datasets)} 个数据域，超过控制台配置的 {asset_limit} 个资产上限，请先收窄数据范围。','question':question}
        self._emit(live,'R06','running','正在读取数据字典、业务口径和报告配置。')
        assets = []
        contexts = {}
        for dataset_id in datasets:
            checkpoint()
            context = engine.repository.get_dataset_context(dataset_id, question)
            contexts[str(dataset_id)] = context
            from analysis_activity import asset_activity
            self._emit(live,'R06','completed','已读取当前数据域的查询依据。',dataset_id=dataset_id,activity=asset_activity(context,question))
            fields = context.get('data_dictionary') or []
            assets.append({'dataset_id':dataset_id, 'name':(context.get('dataset') or {}).get('dataset_name',''),
                           'fields':[{k:item.get(k) for k in ('semantic_name','column_name','jsonb_key','description')} for item in fields[:100] if isinstance(item,dict)]})
        self._emit(live,'R06','completed','已加载授权数据资产。')
        from skill_bindings import field_limit
        linked = {key:schema_link(context,question,limit=field_limit(config)) for key,context in contexts.items()}
        self._emit(live,'R07','completed',f'已用局部向量检索与关系键保留准备 {sum(len(v) for v in linked.values())} 个候选字段。')
        missing = [key for key,context in contexts.items() if not context.get('data_dictionary')]
        self._emit(live,'R08','warning' if missing else 'completed','部分数据域缺少字段字典，执行时仍需通过字段和SQL审核。' if missing else '已检查字段资产完备性；实时数据可用性将在取证时验证。')
        self._emit(live,'R04','completed','已读取各数据域业务口径；报告继续使用控制台维护的指标与单位配置。')
        self._emit(live,'R09','completed','研究计划保留原问题范围，不把不同组织与时间条件视为可直接比较。')
        self._emit(live,'R11','warning' if missing else 'completed',f'已记录 {len(missing)} 个字段资产缺口；假设结论仍待受控数据验证。')
        self._emit(live,'R12','completed',f'本轮按 {brief["method"]["intent"]} 意图制定可查询的验证方向，不预设原因。')
        self._emit(live,'R13','running','正在拆解可检验的研究方向。')
        fallback = {'branches':[], '_planning_failed':True}
        planner_skill = next((s for s in config.get('skills',[]) if s.get('key') == 'planner'),{})
        proposal = engine._chat_json(
            engine._get_agent_prompt(1,'你是研究主理人。') + '\n只输出JSON研究计划，不执行SQL，不生成结论。',
            json.dumps({'question':question,'conversation_context':effective_question,'assets':assets,'constraints':'最多4条独立可查询的假设分支。保留用户的组织、时间和指标条件。只能选择提供的数据集和字段。不编造原因或不存在的维度。每条包含title,question,dataset_id,hypothesis。格式 {"branches":[]}。'},ensure_ascii=False),
            fallback, trace=trace, stage='research.plan.generate', agent_name='研究主理人')
        checkpoint()
        if proposal.get('_planning_failed'):
            return {'error':'模型暂未生成可用研究计划，请检查模型服务后重试。本次未执行取证，也未切换为普通问数。',
                    'error_code':'research_plan_unavailable','question':question}
        branches = []
        for item in (proposal.get('branches') or [])[:4]:
            if not isinstance(item,dict):
                continue
            try:
                dataset_id = int(item.get('dataset_id'))
            except (TypeError,ValueError):
                continue
            if dataset_id not in datasets:
                continue
            branch_question = str(item.get('question') or '').strip()[:1000]
            if not branch_question:
                continue
            branches.append({'id':f'b{len(branches)+1}', 'title':str(item.get('title') or '研究方向')[:80],
                             'question':branch_question,'dataset_id':dataset_id,
                             'hypothesis':str(item.get('hypothesis') or '待证据验证')[:300], 'status':'planned'})
        if not branches:
            return {'error':'模型返回的研究方向未通过资产范围校验，请收窄问题后重新规划。','question':question}
        covered = {b['dataset_id'] for b in branches}
        for dataset_id in datasets:
            if dataset_id not in covered:
                branches.append({'id':f'b{len(branches)+1}','title':f'数据域 {dataset_id} 基线核验', 'question':question,
                                 'dataset_id':dataset_id,'hypothesis':'核对该数据域的事实基线','status':'planned'})
        if len(branches) > 4:
            return {'error':'研究方向超出4个分支预算，请收窄数据范围后重新规划。','question':question}
        run = current_run()
        limits = run.config if run else {'maxParallel':3,'maxRetries':2}
        plan = {'id':'research-' + uuid4().hex, 'question':question, 'branches':branches, 'created':time.time(), 'version':1,
                'owner':owner_key(user),'scope':scope_key(user,allowed),'route':route,'model_id':kwargs.get('model_id'),
                'limits':deepcopy(limits), 'retry_count':run.retries if run else 0, 'execution_question':effective_question, 'state':'pending', 'session':kwargs.get('session_id',''), 'assets':assets, 'contexts':contexts, 'skill_config':deepcopy(config)}
        with self._lock:
            self._plans = {k:v for k,v in self._plans.items() if time.time()-v['created'] < 1800}
            if len(self._plans) >= 300:
                return {'error':'待确认研究计划已满，请稍后再试。'}
            self._plans[plan['id']] = plan
        public = self._public(plan)
        self._emit(live,'R14','waiting','请审阅研究方向；此时尚未执行取证SQL。', plan=public)
        return {'question':question, 'session_id':plan['id'], 'conversation_session_id':plan['session'],
                'requires_confirmation':True,'confirmation_type':'research_plan', 'research_plan':public,
                'confirmation_question':'确认计划后开始并行取证', 'confirmation_options':[],
                'route':{**route,'dataset_ids':datasets}, 'dataset_results':[], 'analysis':''}

    def confirm_by_boss(self, **kwargs):
        plan_id = str(kwargs.get('session_id') or '')
        user = kwargs.get('current_user') or {}
        allowed = set(int(x) for x in kwargs.get('allowed_dataset_ids') or [])
        with self._lock:
            plan = self._plans.get(plan_id)
            if not plan or time.time()-plan['created'] > 1800:
                return {'error':'研究计划已过期或服务已重启，请重新生成计划。'}
            if plan['owner'] != owner_key(user) or plan['scope'] != scope_key(user,allowed):
                return {'error':'账号或组织授权已变化，请重新生成研究计划。'}
            if plan['state'] != 'pending':
                return {'error':'该研究计划已经启动，不能重复派发。'}
            ids = kwargs.get('plan_branch_ids')
            if not isinstance(ids,list) or not ids or not all(isinstance(x,str) for x in ids) or set(ids) - {b['id'] for b in plan['branches']}:
                return {'error':'请至少选择一个有效的研究方向。'}
            branches = [deepcopy(b) for b in plan['branches'] if b['id'] in ids]
            if any(b['dataset_id'] not in allowed for b in branches):
                return {'error':'研究数据集已不在当前授权范围。'}
            plan['state'] = 'running'
            plan = deepcopy(plan)
        latest_config = load_config()
        if not latest_config.get('enabled'):
            return {'error':'控制台已关闭高阶研究，请重新生成计划。'}
        config = plan.get('skill_config') or latest_config
        live = kwargs.get('live_callback')
        run = current_run()
        if run:
            run.retries = plan.get('retry_count',0)
            run.config['skillPolicy'] = {s['key']:bool(s.get('enabled')) for s in config.get('skills',[])}
        self._emit(live,'R15','running',f'已确认 {len(branches)} 个方向，按并发上限派发。', branches=branches)
        evidence = []

        def investigate(branch):
            with bind_run(run):
                checkpoint()
                engine = self._engine(plan['model_id'])
                engine._skill_config = config
                # Original scope is kept explicitly; branch text cannot erase it.
                question = plan['execution_question'] + '\n本分支验证：' + branch['question'] + '\n保留原问题的组织范围、时间与指标口径；无法验证时明确说明证据不足。'
                route = {**{k:v for k,v in deepcopy(plan['route']).items() if not k.startswith('matched_sample_')}, 'dataset_ids':[branch['dataset_id']], 'refined_query':question,
                         'raw_question':plan['question'], 'requires_confirmation':False, 'decision':'generate_sql'}
                def branch_live(payload):
                    payload = deepcopy(payload)
                    if payload.get('event') is not None:
                        payload['event']['branch_id'] = branch['id']
                    if live:
                        live(payload)
                self._emit(branch_live,'R16','running','正在准备分支数据上下文。')
                from skill_bindings import field_limit
                linked_fields = schema_link(plan['contexts'].get(str(branch['dataset_id']),{}),branch['question'],limit=field_limit(config))
                self._emit(branch_live,'R17','completed',f'已为当前分支关联 {len(linked_fields)} 个字段候选；生成后仍按完整字典复核。')
                trace = engine._new_trace(question,'research.branch',live_callback=branch_live)
                result = engine._run_pipeline(question,route,time.time(),[],trace=trace,current_user=user)
                checkpoint()
                # Reuse independently configurable diagnostics, never the old ask/fallback entry.
                from .service import AdvancedAskService
                from .skills.planner import PlannerSkill
                diagnostics = AdvancedAskService()._run_result_trace(
                    question=branch['question'], result=result,
                    advanced_context={'config':config,'skills':[s for s in config['skills'] if s.get('enabled')],
                                      'assets':plan['assets'], 'asset_contexts':plan['contexts'],
                                      'intent':PlannerSkill.infer(branch['question'])}, live_callback=branch_live)
                checkpoint()
                result.setdefault('diagnostics',{})['advanced'] = diagnostics
                data = result.get('dataset_results') or []
                analysis_failed = any(d.get('analysis_status') == 'model_unavailable' for d in data)
                valid = [d for d in data if d.get('rows') and d.get('analysis_status') == 'model_generated' and (d.get('agent3_review') or {}).get('approved') is not False]
                quality = diagnostics.get('sql_quality') or {}
                if quality.get('ok') is False:
                    valid = []
                status = 'completed' if valid and not result.get('error') else 'insufficient'
                entry = {**branch,'status':status, 'finding':'已取得受控查询结果；假设关系仍需结合证据判断。' if valid else '查询数据已返回，但AI解读未完成；本方向不作为已完成的研究证据。' if analysis_failed else '本次取证未完成，不能据此认定源库没有数据。',
                         'row_count':sum(len(d.get('rows') or []) for d in valid), 'dataset_results':valid,
                         'error':'AI解读未完成' if analysis_failed else str(result.get('error') or '')[:300]}
                self._emit(branch_live,'R29','completed' if valid else 'warning',entry['finding'], evidence=entry)
                self._emit(branch_live,'R30','warning','已检查结果与审核状态；描述性查询不等于证明假设的因果关系。')
                return entry

        workers = min(len(branches), max(1,int((run.config if run else plan['limits']).get('maxParallel',3))))
        with ThreadPoolExecutor(max_workers=workers,thread_name_prefix='research') as pool:
            futures = {pool.submit(investigate,b):b for b in branches}
            for future in as_completed(futures):
                checkpoint()
                branch = futures[future]
                try:
                    evidence.append(future.result())
                except Exception as exc:
                    checkpoint()  # Cancellation must propagate rather than become partial success.
                    entry = {**branch,'status':'failed','finding':'该方向未完成，不能作为结论依据。','error':str(exc)[:300], 'dataset_results':[]}
                    evidence.append(entry)
                    self._emit(live,'R29','failed',entry['finding'],branch_id=branch['id'],evidence=entry)
        evidence.sort(key=lambda e:next(i for i,b in enumerate(branches) if b['id']==e['id']))
        self._emit(live,'R31','running','正在汇合各分支已核验的事实与证据缺口。')
        seen_queries = {}
        for entry in evidence:
            signature = tuple(sorted((str(d.get('dataset_id')), ' '.join(str(d.get('sql') or '').split())) for d in entry.get('dataset_results') or []))
            if signature and signature in seen_queries:
                entry['status'] = 'insufficient'
                entry['finding'] = f'与“{seen_queries[signature]}”使用相同查询，尚未形成独立的假设验证证据。'
                self._emit(live,'R33','warning',entry['finding'],branch_id=entry['id'],evidence=entry)
            elif signature:
                seen_queries[signature] = entry['title']
        successful = [e for e in evidence if e['status']=='completed']
        results = [d for e in successful for d in e['dataset_results']]
        gaps = [e['title'] for e in evidence if e['status']!='completed']
        self._emit(live,'R10','completed' if successful else 'warning','已从受控分支查询建立事实基线。' if successful else '未能建立有效事实基线。')
        self._emit(live,'R32','completed','各数据域分别保留报告配置和口径，未跨口径合计或推断贡献率。')
        self._emit(live,'R33','warning' if gaps else 'completed',f'已记录 {len(gaps)} 个待补证方向。')
        self._emit(live,'R39','running','正在基于证据形成研究摘要，明确区分事实与解释。')
        report_engine = self._engine(plan['model_id'])
        report_engine._skill_config = config
        compact_evidence = [{'id':e['id'],'title':e['title'],'status':e['status'], 'data':[{'dataset':d.get('dataset_name'),'columns':d.get('columns'), 'rows':(d.get('rows') or [])[:12]} for d in e['dataset_results']]} for e in successful]
        self._emit(live,'R36','completed',f'已整理 {len(compact_evidence)} 组可引用的查询证据。')
        self._emit(live,'R37','completed','已限制解释边界：描述性事实不构成因果证明，预测须专门模型与回测。')
        summary = report_engine._chat_json(
            report_engine._get_agent_prompt(4,'你是业务分析专家。') + '\n仅根据提供的证据写研究摘要。只描述已查到的数值及差异；没有正式统计检验时，禁止从排名声称正相关、负相关、无相关、反向分布。禁止把单月差异认定为管理异常、系统性偏差或已定位原因。原因只能列为待验证假设，并明确所缺证据；仅在limitations追加免责声明不能抵消结论正文中的越界断言。gaps只代表本次分支未取得可用证据，不等于数据库没有这项数据，必须说本次取证未完成。禁止虚构预测。最终必须只输出JSON对象，字段严格为conclusion字符串、findings数组（每项text字符串和evidence_ids字符串数组）、limitations字符串数组。不要Markdown，不要JSON以外的说明。',
            json.dumps({'question':plan['question'],'evidence':compact_evidence,'gaps':gaps,
                        'contract':{'conclusion':'直接回答，证据不足时明确说明','findings':[{'text':'事实或有限推断','evidence_ids':['b1']}],'limitations':['限制与待验证项']}},ensure_ascii=False,default=str),
            {'conclusion':f'已完成 {len(successful)} 个方向的事实查询，请结合各分支证据判断。','findings':[],'limitations':['描述性证据不构成因果证明。']},
            trace=report_engine._new_trace(plan['question'],'research.report',live_callback=live),
            stage='research.report',agent_name='分析专家')
        checkpoint()
        self._emit(live,'R40','running','正在独立复核研究摘要的数值、排名、引用与因果边界。')
        reviewed = report_engine._chat_json(
            '你是独立的研究报告事实复核专家。依据原始证据复核并改写草稿，不受草稿措辞影响。逐项检查数值、单位、排序、差值与证据引用；删除不受支持的描述。尤其是：舍入后相同或基本相近的数值不要强行区分次高次低，改为说明基本接近；单月横截面没有正式统计检验时，删除正负相关、无相关、无直接线性对应关系等统计结论；不能把数值差异认定为管理异常或系统性原因。原因只能列为待验证假设。未取得证据表示本次取证未完成，不能据此宣称数据库缺少该数据。第一段直接回答原问题，所有陈述均须由本次证据支持。只输出JSON，字段为conclusion字符串、findings数组（每项text和evidence_ids数组）、limitations字符串数组。',
            json.dumps({'question':plan['question'],'evidence':compact_evidence,'draft':summary},ensure_ascii=False,default=str),
            {'review_failed':True},trace=report_engine._new_trace(plan['question'],'research.report_review',live_callback=live),
            stage='research.report_review',agent_name='报告复核专家')
        review_ok = (isinstance(reviewed,dict) and not reviewed.get('review_failed')
                     and isinstance(reviewed.get('conclusion'),str) and bool(reviewed['conclusion'].strip())
                     and isinstance(reviewed.get('findings'),list) and isinstance(reviewed.get('limitations'),list))
        if review_ok:
            summary = reviewed
        else:
            gaps.append('研究摘要复核')
            summary = {'conclusion':'分支事实查询已返回，但研究摘要复核未完成。请核对各分支原始证据，当前不提供已复核的综合结论。',
                       'findings':[],'limitations':['摘要复核未完成，不能使用未经复核的草稿作为决策结论。']}
        self._emit(live,'R39','completed' if review_ok else 'warning','研究摘要已完成独立复核。' if review_ok else '研究摘要未通过完整复核，保留查询证据并明确缺口。')
        valid_ids = {e['id'] for e in successful}
        summary['findings'] = [f for f in (summary.get('findings') or []) if isinstance(f,dict) and isinstance(f.get('evidence_ids'),list) and f['evidence_ids'] and set(f['evidence_ids']).issubset(valid_ids)]
        summary = {'conclusion':str(summary.get('conclusion') or '')[:1200], 'findings':summary['findings'][:8],
                   'limitations':[str(x)[:300] for x in (summary.get('limitations') or [])[:6]]}
        # A report may describe association, never assert proven causation/prediction.
        analysis = '\n\n'.join('### '+e['title']+'\n'+ '\n'.join(d.get('analysis','') for d in e['dataset_results']) for e in successful)
        boundary = '研究边界：以上为受控查询的描述性证据，不构成因果证明。未完成的方向不参与结论；预测需专门模型与回测。'
        analysis += '\n\n'+boundary
        if gaps:
            analysis += '\n\n待补证方向：'+'、'.join(gaps)
        result = {'question':plan['question'], 'conversation_session_id':plan['session'], 'requires_confirmation':False,
                  'route':{**plan['route'],'dataset_ids':sorted({b['dataset_id'] for b in branches})},
                  'research_plan':self._public(plan), 'research':{'evidence':evidence,'gaps':gaps,'boundary':boundary,'partial':bool(gaps),'summary':summary,'summary_review':{'status':'completed' if review_ok else 'incomplete'}},
                  'dataset_results':results, 'analysis':analysis, 'display_title':'研究报告 · '+plan['question'],
                  'columns':[],'rows':[],'row_count':0,'sql':''}
        if results:
            primary = results[0]
            for key in ('report_spec','report_config','columns','rows','row_count','sql'):
                result[key] = primary.get(key)
        else:
            result['error'] = '各研究方向均未形成可采信证据，请调整问题或数据范围。'
        self._emit(live,'R40','warning' if gaps else 'completed','已标记可用证据与未完成方向；不跨口径相加、不推断因果。')
        with self._lock:
            if plan_id in self._plans:
                self._plans[plan_id]['state'] = 'completed'
        if results and plan['session']:
            memory = ScopedMemoryStore(self._memory,scope_key(user,allowed))
            memory.remember_result(plan['session'],plan['question'],result['route'],result)
        self._emit(live,'R41','completed' if results else 'warning','研究结果与证据缺口已整理，准备交付。')
        return result
