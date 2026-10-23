"""Public analysis summaries from executed tools; no model scratchpad or prompts."""
import re


def _sql_shape(sql):
    """Describe syntax only, never expose column names, SQL, or inferred business intent."""
    # Ignore strings/identifiers and comments: SUM in a literal is not aggregation.
    scrubbed = re.sub(r"/\*.*?\*/|--[^\n]*|'(?:''|[^'])*'|\$([A-Za-z_][A-Za-z_0-9]*|)\$.*?\$\1\$|\"(?:\"\"|[^\"])*\"|`[^`]*`|\[[^\]]*\]", ' ', str(sql), flags=re.S)
    methods = list(dict.fromkeys(s.upper() for s in re.findall(r'\b(sum|count|avg|min|max)\s*\(', scrubbed, re.I)))
    aggregation = []
    if re.search(r'\bgroup\s+by\b', scrubbed, re.I):
        aggregation.append('按查询维度分组')
    if re.search(r'\bover\s*\(', scrubbed, re.I):
        aggregation.append('含窗口计算')
    if re.search(r'\bdistinct\b', scrubbed, re.I):
        aggregation.append('含去重处理')
    return methods, aggregation


def _recorded_count(event, key):
    value = event.get(key)
    return {key: value} if isinstance(value, int) and not isinstance(value, bool) and value >= 0 else {}


def asset_activity(context, question):
    fields=context.get('data_dictionary') or []
    return {'kind':'assets','heading':'已准备本次查询依据',
            'dataset_name':(context.get('dataset') or {}).get('dataset_name') or '授权数据集',
            'question':str(question)[:600], 'field_count':len(fields),
            'relation_count':len(context.get('table_relations') or []),
            'reference_count':len(context.get('golden_sql_samples') or []),
            'time_mentions':list(dict.fromkeys(re.findall(r'20\d{2}年(?:\d{1,2}月)?|20\d{2}-\d{2}(?:-\d{2})?|(?<!\d)\d{1,2}月',str(question))))[:8]}


def activity_for(event):
    # Only explicitly supported structured fields may be public, never raw notes.
    value=event.get('activity')
    if isinstance(value,dict):
        allowed={'kind','heading','question','dataset_name','field_count','relation_count','reference_count','time_mentions','approved'}
        return {key:value[key] for key in allowed if key in value}
    stage=str(event.get('stage') or '')
    if stage=='pipeline.agent2_result' and event.get('sql'):
        sql=str(event['sql'])
        methods, aggregation = _sql_shape(sql)
        public_summary=str(event.get('public_summary') or '').strip()[:600]
        if re.search(r'<think|```|\bselect\b|system_prompt',public_summary,re.I):
            public_summary=''
        return {'kind':'query','heading':'已生成查询，进入审核','methods':methods,'aggregation':aggregation,'public_summary':public_summary,
                **({'dataset_name':str(event['dataset_name'])[:160]} if event.get('dataset_name') else {}),
                'checks':['生成的查询还需字段、口径和只读审核；审核通过后注入授权范围。']}
    if stage=='datasource.execute_sql' and event.get('status')=='response':
        columns = event.get('columns') if isinstance(event.get('columns'),list) else None
        return {'kind':'data','heading':'查询已返回数据',**_recorded_count(event,'row_count'),
                **({'dataset_name':str(event['dataset_name'])[:160]} if event.get('dataset_name') else {}),
                **({'columns':[str(v)[:80] for v in columns[:12]], 'column_count':len(columns)} if columns is not None else {})}
    if stage=='stability.assert':
        return {'kind':'checks','heading':'数据合理性核验','checks':[str(event.get('business_summary') or '')[:500]],**_recorded_count(event,'row_count')}
    if stage=='stability.explain' and event.get('status')=='response':
        return {'kind':'preflight','heading':'执行计划预检已通过','checks':['已完成数据库执行计划预检，继续在当前授权范围执行。']}
    return None


def stage_summary(stage, status, fallback):
    if status=='request':
        for fragment,text in [('agent1','正在核对问题范围，并匹配可访问的数据资产。'),('agent2','正在依据字段、关联和业务口径编写查询；完成后继续审核。'),('agent3','正在复核查询的字段来源、只读约束与统计口径。'),('agent4','正在根据已返回的数据整理结论、差异与需关注事项。')]:
            if fragment in stage:
                return text
    return fallback
