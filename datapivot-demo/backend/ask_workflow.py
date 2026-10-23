"""Business progress protocol. Nodes describe actual tool events, never fake ticks."""
from copy import deepcopy
from analysis_activity import activity_for, stage_summary


def result_outcome(result):
    """Business completion is distinct from a successful HTTP/SSE response."""
    if result.get('aborted'):
        return {'status':'canceled','label':'已停止','description':'本轮任务已经停止，未完成的步骤不会标记为成功。'}
    if result.get('error'):
        return {'status':'failed','label':'查询未完成','description':'本轮执行出现异常，请查看失败阶段后重试。'}
    if result.get('requires_confirmation'):
        return {'status':'waiting','label':'等待确认','description':'确认本次范围与计划后继续执行。'}
    research = result.get('research')
    datasets = result.get('dataset_results') or []
    if research:
        evidence = research.get('evidence') or []
        datasets = [ds for branch in evidence for ds in branch.get('dataset_results') or []]
        if research.get('partial') or (research.get('summary_review') or {}).get('status') != 'completed':
            available = any(branch.get('status') == 'completed' for branch in evidence)
            return {'status':'partial' if available else 'failed','label':'部分证据可用' if available else '研究未完成',
                    'description':'仍有证据或报告复核未完成，请查看待补证方向。'}
    rows = sum(len(ds.get('rows') or []) for ds in datasets)
    failed = [ds for ds in datasets if ds.get('query_status') == 'failed'
              or (ds.get('agent3_review') or {}).get('approved') is False
              or (not ds.get('rows') and ds.get('analysis_status') == 'model_unavailable')]
    incomplete = failed or any(ds.get('analysis_status') in ('model_unavailable','deterministic') for ds in datasets)
    if not datasets or len(failed) == len(datasets):
        status, label, description = 'failed', '查询未完成', '查询生成、审核或执行未完成，不能据此判断业务数据为空。'
    elif incomplete:
        status, label, description = 'partial', '数据已返回，分析未完整完成', '可核对已返回的数据；失败的查询或 AI 解读仍需重试。'
    elif not rows:
        status, label, description = 'empty', '查询完成，无匹配记录', '查询已成功执行，请核对时间、筛选条件与授权范围。'
    else:
        status, label, description = 'completed', '分析已完成', '查询、核验与结果解读已完成，可以查看数据与依据。'
    return {'status':status,'label':label,'description':description,'row_count':rows,'dataset_count':len(datasets)}

BASIC_PHASES = [
    ('L0', '权限与范围', '主理人', '组织树权限'),
    ('L1', '理解问题', '路由专家', '语义口径对齐'),
    ('L2', '匹配数据资产', '数据专家', 'Schema Linking'),
    ('L3', '确认业务口径', '主理人', '歧义消解'),
    ('L4', '检索金标样例', 'SQL专家', 'Golden SQL'),
    ('L5', '生成查询', 'SQL专家', '字段映射'),
    ('L6', '审查查询', '审计专家', '只读与字段校验'),
    ('L7', '注入组织范围', '权限技能', '行级过滤'),
    ('L8', '执行计划预检', '审计专家', 'EXPLAIN'),
    ('L9', '受控执行', '数据专家', '超时与行数上限'),
    ('L10', '数据合理性核验', '审计专家', '空值与规模断言'),
    ('LR', '修复与再核验', 'SQL专家', '全任务最多两次'),
    ('L11', '图表与业务转译', '分析专家', '报告模板'),
    ('L12', '主理人签收', '主理人', '证据完整性'),
    ('L13', '交付答案', '主理人', '结果依据'),
]
# Runtime catalog uses Rxx; the architecture target diagram keeps its Hxx ids.
# Unexecuted nodes remain planned/skipped in the UI.
HIGH_TITLES = [
    '受理研究任务','校验组织权限','界定问题目标','识别指标口径','选择数据域','读取数据资产',
    '关联字段与关系','检查数据可用性','核对比较范围','建立研究基线','检查证据缺口','确定分析方法',
    '形成假设树','审阅研究计划','并行派发任务','分支上下文准备','分支字段对齐','检索金标样例',
    '生成分支查询','审核分支查询','注入行级权限','执行计划预检','受控执行查询','检查空值与规模',
    '异常定位','修复查询','复核修复结果','重试受控查询','提取分支证据','检验假设支持程度',
    '汇合并行证据','检查比较一致性','标记冲突与缺口','选择补证方向','补证与再核验','整理可采信事实',
    '限定归因与预测边界','推荐分析图表','编写研究报告','主理人质量签收','交付研究结果','归档执行依据',
]
HIGH_ROLES = ['总主理人','总主理人 / 权限服务','总主理人','正名 · 语义专家','问津 · 路由专家','问津 · 数据资产专家',
    '问津 · Schema 专家','审衡 · 资产核验专家','正名 · 语义专家','格物 · 基线查询专家','审衡 · 证据核验专家','筹策 · 规划专家',
    '筹策 · 假设规划专家','总主理人 / 用户','总主理人 / 调度器','垂直领域专家','问津 · Schema 专家','格物 · SQL 专家',
    '格物 · SQL 专家','审衡 · SQL 审核专家','既有组织权限服务','审衡 · 执行计划专家','格物 · 数据执行专家','审衡 · 数据质量专家',
    '审衡 · 异常核验专家','格物 · SQL 修复专家','审衡 · 修复审核专家','格物 · 数据执行专家','垂直领域专家','审衡 · 证据核验专家',
    '总主理人','审衡 · 可比性核验专家','审衡 · 缺口核验专家','筹策 · 补证规划专家','格物 · 数据执行专家','析微 · 分析专家',
    '审衡 · 结论边界专家','析微 · 可视化专家','析微 · 业务分析专家','总主理人','总主理人','管家 · 上下文专家']
HIGH_SKILLS = ['研究任务受理','组织树权限 / 数据集准入','任务规格约束','指标与业务口径','授权数据域路由','资产打包',
    '局部向量 / 关系键剪枝','字段资产完备性检查','比较范围约束','受控基线查询','证据缺口检查','分析意图识别',
    '假设树拆解','计划审阅 / 分支选择','Fan-out / 并发预算','授权上下文继承','Schema Linking','Golden SQL 参考',
    'SQL 生成','字段 / 口径 / 只读复核','行级权限过滤','EXPLAIN 预检','超时 / 行数限制','空值 / 规模断言',
    '错误分型','有界 SQL 修复','修复再审核','权限重注入 / 重试','Evidence Ledger','证据充分性边界',
    'Fan-in / 并行汇合','口径可比性检查','缺口 / 重复 SQL 检查','补证预算（规划）','补证再核验（规划）','可引用事实整理',
    '因果 / 预测声明边界','图表与报告模板','故事化转译 / 证据引用','质量签收','答案契约','持久检查点（规划）']
HIGH_PHASES = [(f'R{i:02}', title, HIGH_ROLES[i-1], HIGH_SKILLS[i-1]) for i, title in enumerate(HIGH_TITLES, 1)]


def catalog(flow):
    return [{'id': n, 'title': title, 'role': role, 'skill': skill, 'status': 'planned'} for n,title,role,skill in (HIGH_PHASES if flow == 'advanced' else BASIC_PHASES)]


def phase_for(stage, flow):
    stages = [
        ('permission', 'L0', 'R02'), ('row_security', 'L7', 'R21'),
        ('explain', 'L8', 'R22'), ('assert', 'L10', 'R24'),
        ('repair', 'LR', 'R26'), ('agent1', 'L1', 'R05'), ('route', 'L1', 'R05'),
        ('context', 'L2', 'R16'), ('golden', 'L4', 'R18'), ('agent2', 'L5', 'R19'),
        ('agent3', 'L6', 'R20'), ('execute', 'L9', 'R23'), ('agent4', 'L11', 'R38'),
    ]
    for match, basic, high in stages:
        if match in stage:
            return high if flow == 'advanced' else basic
    return ''


def business_event(payload, run, branch_id=''):
    event = deepcopy(payload.get('event') or {})
    stage = str(event.get('stage') or '')
    node_id = event.get('node_id') or phase_for(stage, run.flow)
    if not node_id:
        return None
    node = next((n for n in catalog(run.flow) if n['id'] == node_id), {})
    raw_status = str(event.get('status') or 'info')
    if raw_status == 'delta':
        return None
    status = {'request':'running', 'response':'completed', 'success':'completed', 'info':'completed', 'warning':'warning', 'error':'failed',
              'retry':'retrying','fallback':'failed','rejected':'failed'}.get(raw_status, raw_status)
    if event.get('approved') is False:
        status = 'failed'
    if stage == 'pipeline.agent2_result' and not str(event.get('sql') or '').strip():
        status = 'failed'
    if event.get('analysis_status') == 'model_unavailable':
        status = 'warning'
    # Only safe, structured fields leave the tool trace for business users.
    return run.record({
        'type': 'workflow', 'node_id': node_id, 'branch_id': event.get('branch_id') or branch_id,
        'title': node.get('title', event.get('title', '分析进展')), 'status': status,
        'role': node.get('role','领域专家'), 'skill': node.get('skill',''),
        'summary': event.get('business_summary') or stage_summary(stage,raw_status,(activity_for(event) or {}).get('heading') or node.get('title','')),
        **({'activity':activity_for(event)} if activity_for(event) else {}),
        'row_count': event.get('row_count'), 'dataset_id':event.get('dataset_id'), 'attempt': event.get('attempt', run.retries),
        'time': event.get('time',''),
        **({'branches':event['branches']} if 'branches' in event else {}),
        **({'plan':event['plan']} if 'plan' in event else {}),
        **({'evidence':{key:event['evidence'].get(key) for key in ('id','title','hypothesis','status','finding','row_count')}} if isinstance(event.get('evidence'),dict) else {}),
    })
