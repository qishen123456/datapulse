"""Capabilities exposed by the two current pipelines, not a plugin executor.

Bindings are server-owned. Editing a label/instruction never disables SQL/RLS gates.
"""
from copy import deepcopy

SHARED_GUARDS = [
    {'key':'organization_scope','label':'组织范围校验','stage':'stability.row_security','toolType':'dataset','enabled':True,'order':1,'description':'沿用组织树与账号授权，在数据集准入和 SQL 执行前强制校验。'},
    {'key':'schema_link','label':'字段关联与剪枝','stage':'stability.context','toolType':'dataset','enabled':True,'order':2,'description':'局部向量检索字段，保留组织、时间及关联键；完整元数据继续参与确定性校验。','config':{'fieldLimit':80}},
    {'key':'semantic_align','label':'指标口径对齐','stage':'stability.semantic','toolType':'dataset','enabled':True,'order':3,'description':'读取指标定义与业务口径，将消歧要求传给主理人和查询专家。'},
    {'key':'explain_guard','label':'执行计划预检','stage':'stability.explain','toolType':'sql','enabled':True,'order':4,'description':'执行前进行只读、方言与 EXPLAIN 预检，拒绝高风险关联。'},
    {'key':'result_assertions','label':'数据合理性断言','stage':'stability.assert','toolType':'fact','enabled':True,'order':5,'description':'检查空结果、全空字段、非有限数值和结果规模，不把无记录解释成业务值为零。'},
]
SHARED_KEYS = {s['key'] for s in SHARED_GUARDS}
# These instructions are explicitly appended at existing role prompt boundaries.
PROMPT_ROLES = {'dataset_route':(1,), 'asset_pack':(2,), 'route_guard':(1,), 'semantic_align':(1,2),
                'planner':(1,), 'golden_sql':(2,), 'sql_generate':(2,), 'sql_review':(3,), 'report_compose':(4,)}
ADVANCED_ONLY = {'planner','sql_quality','template_policy','pandas_analyze','self_check','answer_contract','conclusion_advice','evidence_vote'}


def binding_for(key, custom=False):
    scope = ['advanced'] if key in ADVANCED_ONLY or custom else ['basic','advanced']
    return {'flows':scope, 'promptEditable':key in PROMPT_ROLES and not custom,
            'parameterEditable':key == 'schema_link',
            'executor':'archive' if custom else 'deterministic' if key in SHARED_KEYS-{'semantic_align'} or key == 'sql_execute' else 'prompt' if key in PROMPT_ROLES else 'diagnostic',
            'roles':list(PROMPT_ROLES.get(key,()))}


def instructions_for(config, agent_no, flow):
    parts=[]
    for skill in config.get('skills',[]):
        key=skill.get('key')
        if agent_no not in PROMPT_ROLES.get(key,()) or flow not in binding_for(key).get('flows',[]):
            continue
        if not skill.get('enabled',True):
            continue
        text=str(skill.get('prompt') or skill.get('instructions') or '').strip()
        if text:
            parts.append(f"[{skill.get('label') or key}]\n{text[:6000]}")
    return '\n\n'.join(parts)


def field_limit(config):
    skill=next((s for s in config.get('skills',[]) if s.get('key')=='schema_link'),{})
    return int((skill.get('config') or {}).get('fieldLimit',80))
