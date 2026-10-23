"""Deterministic SQL and result gates used by both query paths."""
from __future__ import annotations
import math
import re


def validate_sql(sql):
    # Strip literals before checking verbs so a business label 'update' is safe.
    text = re.sub(r"'(?:''|[^'])*'", "''", str(sql or ''))
    text = re.sub(r'/\*.*?\*/|--[^\n]*',' ',text,flags=re.S).strip().rstrip(';').strip()
    if not re.match(r'^(select|with)\b',text,re.I):
        raise ValueError('只允许 SELECT/WITH 只读查询。')
    if ';' in text or re.search(r'\b(insert|update|delete|drop|alter|create|truncate|grant|revoke|copy|call|exec|execute|merge|into|for\s+update|pg_sleep|dblink|load_file|outfile)\b',text,re.I):
        raise ValueError('查询包含写操作、多语句或不受支持的操作。')
    if re.search(r'\bfrom\s+[\w."`]+(?:\s+(?:as\s+)?\w+)?\s*,\s*[\w."`]+',text,re.I):
        raise ValueError('检测到逗号式多表查询，请使用带明确关联条件的 JOIN。')
    if re.search(r'\bcross\s+join\b|\bjoin\b[^;]*?\bon\s+1\s*=\s*1',text,re.I):
        raise ValueError('检测到笛卡尔积风险，请补充关联条件。')


def result_assertions(rows, max_rows=10000):
    if len(rows) > max_rows:
        raise ValueError(f'查询超过 {max_rows} 行上限，请收窄范围或聚合。')
    if not rows:
        return {'status':'empty','row_count':0,'warnings':['查询返回空结果，不能据此断言业务值为零。']}
    warnings = []
    for column in rows[0]:
        values = [r.get(column) for r in rows]
        if all(v is None for v in values):
            warnings.append(f'{column} 全部为空，不能用于有效结论。')
        if any(isinstance(v,float) and not math.isfinite(v) for v in values):
            raise ValueError(f'{column} 含非有限数值。')
    return {'status':'warning' if warnings else 'passed','row_count':len(rows),'warnings':warnings}


def schema_link(context, question, limit=80):
    """Sparse n-gram vector retrieval plus explicit relationship-key retention.

    Uses local vectors, requiring no new embedding provider. Full metadata stays
    available to deterministic field validation; only model prompt context prunes.
    """
    from collections import Counter
    def vector(text):
        text = re.sub(r'\s+','',str(text).lower())
        return Counter([text[i:i+n] for n in (2,3) for i in range(max(0,len(text)-n+1))])
    target = vector(question)
    target_norm = math.sqrt(sum(v*v for v in target.values())) or 1
    fields = context.get('data_dictionary') or []
    ranked = []
    for index, item in enumerate(fields):
        text = ' '.join(str(item.get(k) or '') for k in ('semantic_name','column_name','jsonb_key','description','synonyms'))
        values = vector(text)
        norm = math.sqrt(sum(v*v for v in values.values())) or 1
        score = sum(v*target.get(k,0) for k,v in values.items()) / (norm*target_norm)
        ranked.append((score,index,item))
    ranked.sort(key=lambda x:(-x[0],x[1]))
    selected = [item for _,_,item in ranked[:limit]]
    chosen = {id(item) for item in selected}
    tables = {str(item.get('table_name') or '') for item in selected}
    relation_keys = set()
    for relation in context.get('table_relations') or []:
        if relation.get('left_table') in tables or relation.get('right_table') in tables:
            relation_keys.add((relation.get('left_table'),relation.get('left_key')))
            relation_keys.add((relation.get('right_table'),relation.get('right_key')))
    for item in fields:
        name = ' '.join(str(item.get(k) or '') for k in ('semantic_name','column_name','jsonb_key'))
        bridge = (item.get('table_name'),item.get('column_name')) in relation_keys
        if id(item) not in chosen and (bridge or re.search(r'组织|编码|日期|时间|年度|月份|路径|权限',name)):
            selected.append(item)
            chosen.add(id(item))
    return selected


def validate_explain(plan, max_join_rows=1000000):
    """Reject estimated join explosions before execution (PostgreSQL JSON plan)."""
    if isinstance(plan,list):
        for item in plan:
            validate_explain(item,max_join_rows)
    elif isinstance(plan,dict):
        node_type = str(plan.get('Node Type') or '')
        if ('Join' in node_type or node_type == 'Nested Loop') and float(plan.get('Plan Rows') or 0) > max_join_rows:
            raise ValueError('执行计划预计产生过大的关联结果，请收窄范围或调整关联粒度。')
        for value in plan.values():
            if isinstance(value,(list,dict)):
                validate_explain(value,max_join_rows)
