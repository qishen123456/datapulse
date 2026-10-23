"""Complete the existing three gas dataset knowledge assets without replacing data/permissions."""
import json
from datetime import datetime, timezone
from pathlib import Path
from psycopg2 import sql
from psycopg2.extras import Json, RealDictCursor
from bookshelf_repository import BookshelfRepository
from config_manager import CONFIG_DIR
from dataset_report_config import get_generic_config, get_config
from organization_tree_store import load_organization_trees
from data_permission_store import load_data_permissions
from knowledge_assets import ROOT, TAG, GRAINS, bundle
from prepare_runtime import LABELS

EXTRA_LABELS={'sales_m3':'销气量_方','sales_revenue_yuan':'销气收入_元','estimated_m3':'估抄量_方','loss_m3':'供销差量_方','loss_rate':'供销差率_小数','pretax_profit_yuan':'模拟税前利润_元','total_revenue_yuan':'总收入_元','aging_over_180_yuan':'超过180天应收_元','组织编码':'组织编码','组织编码路径':'组织编码路径'}
SNAPSHOT={'opening_yuan','closing_yuan','provision_yuan','opening_users','ending_users','potential_users','aging_over_180_yuan'}
ENUMS={'user_type','status','severity','pressure_level','material','tax_basis','object_kind','collection_status','source','sales_enabled','org_level'}


def dictionary_note(column,view,enum):
    notes=['直接读取已类型化视图列，不再对该列使用fields->>。']
    if column=='business_key':notes.append(GRAINS[view])
    if column=='org_id':notes.append('当前记录所属组织编码，可能是网格或服务中心；不能直接等同分公司编码。')
    if column=='branch_id':notes.append('分公司编码，用于分公司范围筛选，不是网格编码。')
    if column=='center_id':notes.append('服务中心编码，不是分公司编码。')
    if column in {'org_path','组织编码路径'}:notes.append('以/分隔的组织编码祖先路径，和系统组织树一致。')
    if column.endswith('_yuan'):notes.append('金额原始单位元；只在显示为万元时除以10000。')
    if column.endswith('_m3'):notes.append('气量原始单位方/立方米，不是万方，不得作为金额。')
    if column in SNAPSHOT or column.startswith('aging_'):notes.append('时点/余额指标，只取选定期末，不跨月累加。')
    if column in {'loss_rate','loss_threshold'}:notes.append('0–1小数，展示百分比才乘100；阈值是演示假设，非正式核定标准。')
    if column in {'price_yuan_m3','purchase_price_yuan_m3'}:notes.append('元/方；跨记录均价按金额/气量加权，不能简单AVG。')
    if column in {'org_id','branch_id','center_id','customer_id','network_id','hazard_id','business_key','org_level','组织编码'}:notes.append('标识/层级字段，不是可加总业务指标。')
    if column=='month':notes.append('文本YYYY-MM，2024-01至2026-09；最新月用MAX(month)，不偷换用户明确月份。')
    if column=='pretax_profit_yuan':notes.append('模拟税前利润，不含所得税，不能称税后净利润。')
    if column in {'completed_date','status','due_date','found_date','as_of_date'}:notes.append('历史工单状态按发现、完成和截止日期重建，不以当前status替代历史；快照截止2026-09-30。')
    if column=='not_at_home':notes.append('当月到访不遇户次，非待处理历史存量。')
    if column=='length_km':notes.append('公里；和工单关联后不能按工单重复SUM里程。')
    if enum:notes.append('实际枚举：'+json.dumps(enum,ensure_ascii=False))
    return ' '.join(notes)


def main():
    assets=bundle(json.loads((ROOT/'generated/datasets.json').read_text()))
    (ROOT/'generated/dataset_knowledge_bundle.json').write_text(json.dumps(assets,ensure_ascii=False,indent=2)+'\n')
    repo=BookshelfRepository()
    permissions_before=load_data_permissions()
    nodes={n['id']:n for n in load_organization_trees()['nodes'] if n['tree_type_id']=='gas_jc_tree'}
    assert len(nodes)==43
    tables=['bs_dataset_synonyms','bs_regression_cases','bs_lld_documents','bs_data_dictionary_items','bs_schema_definitions','bs_table_relations','bs_golden_sql_samples','bs_agent_prompt_fragments','bs_common_questions','bs_dataset_report_config']
    report={'version':TAG,'checked_at':datetime.now(timezone.utc).isoformat(),'datasets':[],'query_checks':0}
    backup=Path(CONFIG_DIR).parent/'backups'/'gas-knowledge'/datetime.now().strftime('%Y%m%d-%H%M%S')
    backup.mkdir(parents=True,exist_ok=True)
    with repo._connect() as conn,conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("SELECT * FROM bs_datasets WHERE dataset_code=ANY(%s) ORDER BY id",([a['code'] for a in assets],))
        existing={r['dataset_code']:dict(r) for r in cur.fetchall()}
        assert len(existing)==3
        ids=[r['id'] for r in existing.values()]
        saved={'bs_datasets':list(existing.values())}
        for table in tables:
            cur.execute(sql.SQL('SELECT * FROM {} WHERE dataset_id=ANY(%s)').format(sql.Identifier(table)),(ids,))
            saved[table]=[dict(r) for r in cur.fetchall()]
        (backup/'metadata.json').write_text(json.dumps(saved,ensure_ascii=False,indent=2,default=str)+'\n')
        for asset in assets:
            ds=existing[asset['code']]; dsid=ds['id']
            rule=permissions_before.get('rules',{}).get(str(dsid)) or {}
            assert rule.get('mode')=='org_tree' and 'gas_jc_tree' in rule.get('tree_type_ids',[rule.get('tree_type_id')])
            cur.execute('SELECT org_id,org_name,org_path FROM v_gas_org')
            orgs={r['org_id']:r for r in cur.fetchall()}
            assert set(orgs)==set(nodes)
            for key,row in orgs.items():
                assert row['org_name']==nodes[key]['name'] and row['org_path'].strip('/').split('/')==nodes[key]['path_ids']
            description=f"虚构燃气演示；本地PG数据2024-01至2026-09；金额元、气量方、比率0–1；组织树43节点；知识版本{TAG}。"+asset['rules'][10]
            cur.execute('UPDATE bs_datasets SET description=%s,updated_at=NOW() WHERE id=%s',(description,dsid))
            for synonym in asset['synonyms']:
                cur.execute('INSERT INTO bs_dataset_synonyms(dataset_id,synonym,normalized_synonym,weight) VALUES(%s,%s,%s,2) ON CONFLICT(dataset_id,normalized_synonym) DO NOTHING',(dsid,synonym,synonym.lower()))
            for order,case in enumerate(asset['regression_cases']):
                cur.execute('SELECT id FROM bs_regression_cases WHERE dataset_id=%s AND case_type=%s AND question_text=%s',(dsid,case['case_type'],case['question_text']))
                found=cur.fetchone()
                if found:cur.execute('UPDATE bs_regression_cases SET expected_focus=%s,expected_intent=%s,sort_order=%s,is_active=TRUE,updated_at=NOW() WHERE id=%s',(case['expected_focus'],case['expected_intent'],order+1,found['id']))
                else:cur.execute('INSERT INTO bs_regression_cases(dataset_id,case_type,question_text,expected_focus,expected_intent,sort_order) VALUES(%s,%s,%s,%s,%s,%s)',(dsid,case['case_type'],case['question_text'],case['expected_focus'],case['expected_intent'],order+1))
            cur.execute('SELECT version,content FROM bs_lld_documents WHERE dataset_id=%s ORDER BY version DESC LIMIT 1',(dsid,))
            old=cur.fetchone()
            version=old['version'] if old and old['content']==asset['content'] else (old['version']+1 if old else 1)
            cur.execute('UPDATE bs_lld_documents SET is_active=FALSE WHERE dataset_id=%s',(dsid,))
            cur.execute('''INSERT INTO bs_lld_documents(dataset_id,version,title,content,redline_rules,is_active,created_by)
                VALUES(%s,%s,%s,%s,%s,TRUE,%s) ON CONFLICT(dataset_id,version) DO UPDATE SET
                title=EXCLUDED.title,content=EXCLUDED.content,redline_rules=EXCLUDED.redline_rules,is_active=TRUE,updated_at=NOW()''',
                (dsid,version,asset['name']+'·指标口径与粒度',asset['content'],Json(asset['rules']),TAG))
            field_count=0
            for view in asset['views']:
                cur.execute("SELECT column_name,data_type FROM information_schema.columns WHERE table_schema='public' AND table_name=%s ORDER BY ordinal_position",(view,))
                columns=cur.fetchall();assert columns,view
                ddl=sql.SQL('CREATE TABLE {} ({})').format(sql.Identifier(view),sql.SQL(', ').join(sql.SQL('{} {}').format(sql.Identifier(c['column_name']),sql.SQL(c['data_type'])) for c in columns)).as_string(cur)+';'
                cur.execute('''INSERT INTO bs_schema_definitions(dataset_id,table_name,ddl_sql,description) VALUES(%s,%s,%s,%s)
                    ON CONFLICT(dataset_id,table_name) DO UPDATE SET ddl_sql=EXCLUDED.ddl_sql,description=EXCLUDED.description,is_active=TRUE,updated_at=NOW()''',(dsid,view,ddl,GRAINS[view]))
                for column in columns:
                    key=column['column_name'];enum={}
                    label=LABELS.get(key,EXTRA_LABELS.get(key,key))
                    assert key in LABELS or key in EXTRA_LABELS,f'字段缺中文含义:{view}.{key}'
                    if key in ENUMS:
                        cur.execute(sql.SQL('SELECT DISTINCT {} AS value FROM {} WHERE {} IS NOT NULL ORDER BY 1 LIMIT 30').format(sql.Identifier(key),sql.Identifier(view),sql.Identifier(key)))
                        enum={str(r['value']):str(r['value']) for r in cur.fetchall()}
                    note=dictionary_note(key,view,enum)
                    cur.execute('SELECT id FROM bs_data_dictionary_items WHERE dataset_id=%s AND table_name=%s AND column_name=%s',(dsid,view,key))
                    matched=cur.fetchall()
                    if matched:
                        cur.execute('UPDATE bs_data_dictionary_items SET semantic_name=%s,data_type=%s,enum_mapping=%s,extraction_rule=%s,is_active=TRUE,updated_at=NOW() WHERE dataset_id=%s AND table_name=%s AND column_name=%s',(label,column['data_type'],Json(enum),note,dsid,view,key))
                    else:
                        cur.execute('INSERT INTO bs_data_dictionary_items(dataset_id,table_name,column_name,semantic_name,data_type,enum_mapping,extraction_rule) VALUES(%s,%s,%s,%s,%s,%s,%s)',(dsid,view,key,label,column['data_type'],Json(enum),note))
                    field_count+=1
            relations=[]
            for view in asset['views']:
                if view=='v_gas_org':continue
                relations.append((view,'org_id','v_gas_org','org_id','left',TAG+'；事实多对一组织维，右侧org_id唯一，不能与其他事实按单键直连。'))
            if asset['code']=='GAS_SAFE':
                relations.append(('v_gas_hazards','network_id','v_gas_network','network_id','left',TAG+'；隐患多对一管段；关联后不能按工单重复累加管段里程。'))
            for left,lk,right,rk,kind,desc in relations:
                cur.execute(sql.SQL('SELECT {} AS key FROM {} GROUP BY {} HAVING count(*)>1 LIMIT 1').format(sql.Identifier(rk),sql.Identifier(right),sql.Identifier(rk)))
                assert not cur.fetchone(),'维表键非唯一'
                cur.execute(sql.SQL('SELECT count(*) AS n FROM {} l LEFT JOIN {} r ON l.{}=r.{} WHERE l.{} IS NOT NULL AND r.{} IS NULL').format(sql.Identifier(left),sql.Identifier(right),sql.Identifier(lk),sql.Identifier(rk),sql.Identifier(lk),sql.Identifier(rk)))
                assert cur.fetchone()['n']==0,'关系存在悬空键'
                cur.execute('SELECT id FROM bs_table_relations WHERE dataset_id=%s AND left_table=%s AND left_key=%s AND right_table=%s AND right_key=%s',(dsid,left,lk,right,rk))
                match=cur.fetchone()
                if match:cur.execute('UPDATE bs_table_relations SET relation_type=%s,description=%s,is_active=TRUE,updated_at=NOW() WHERE id=%s',(kind,desc,match['id']))
                else:cur.execute('INSERT INTO bs_table_relations(dataset_id,left_table,left_key,right_table,right_key,relation_type,description) VALUES(%s,%s,%s,%s,%s,%s,%s)',(dsid,left,lk,right,rk,kind,desc))
            for no,prompt in asset['prompts'].items():
                cur.execute('INSERT INTO bs_agent_prompt_fragments(dataset_id,agent_no,prompt_key,prompt_content,created_by) VALUES(%s,%s,%s,%s,%s) ON CONFLICT(dataset_id,agent_no,prompt_key) DO UPDATE SET prompt_content=EXCLUDED.prompt_content,is_active=TRUE,updated_at=NOW()',(dsid,no,TAG,prompt,TAG))
            for order,item in enumerate(asset['queries']):
                cur.execute('EXPLAIN '+item['sql'])
                cur.execute(item['sql']);rows=cur.fetchall()
                report['query_checks']+=1
                cur.execute('SELECT id FROM bs_golden_sql_samples WHERE dataset_id=%s AND question=%s',(dsid,item['question']))
                match=cur.fetchone()
                if match:cur.execute('UPDATE bs_golden_sql_samples SET sql_text=%s,tags=%s,quality_score=95,is_active=TRUE,updated_at=NOW() WHERE id=%s',(item['sql'],Json(['燃气模拟',TAG,'AI参考']),match['id']))
                else:cur.execute("INSERT INTO bs_golden_sql_samples(dataset_id,intent_type,question,sql_text,tags,quality_score,created_by) VALUES(%s,'aggregate',%s,%s,%s,95,%s)",(dsid,item['question'],item['sql'],Json(['燃气模拟',TAG,'AI参考']),TAG))
                cur.execute('SELECT id FROM bs_common_questions WHERE dataset_id=%s AND question_text=%s',(dsid,item['question']))
                match=cur.fetchone()
                if match:cur.execute('UPDATE bs_common_questions SET sort_order=%s,is_active=TRUE,updated_at=NOW() WHERE id=%s',(order+1,match['id']))
                else:cur.execute('INSERT INTO bs_common_questions(dataset_id,question_text,sort_order) VALUES(%s,%s,%s)',(dsid,item['question'],order+1))
            config=get_generic_config()
            config.update(reportTitle=asset['name']+'·分析简报',businessContext=description,metrics=asset['metrics'],agentReportGuidance='先直接回答本轮问题，保留时间和授权组织范围；气量方、金额元、比率0到1。只展示被查询的指标，不要求整套指标同时出现；余额只选期末，比例按总分子总分母重算；无证据不推断因果；取证失败不是源库无数据。详细指标口径与业务红线以本数据集LLD为准。',sqlOutputContract={'amountUnit':'元','notes':['按问题选择所需指标，禁止强制返回全部指标。气量为方，金额为元，比例0–1。不得将税前利润标为净利润。']})
            cur.execute('INSERT INTO bs_dataset_report_config(dataset_id,config_json) VALUES(%s,%s) ON CONFLICT(dataset_id) DO UPDATE SET config_json=EXCLUDED.config_json,updated_at=NOW()',(dsid,Json(config)))
            report['datasets'].append(dict(id=dsid,code=asset['code'],name=asset['name'],lld_version=version,views=len(asset['views']),fields=field_count,relations=len(relations),metrics=len(asset['metrics']),agent_prompts=4,regression_cases=len(asset['regression_cases']),synonyms=len(asset['synonyms']),queries=len(asset['queries']),common_questions=len(asset['queries']),profile='generic'))
        # Validate semantic equivalence for all periods/branches, not only one sample.
        cur.execute('''WITH a AS (SELECT month,branch_id,SUM(estimated_meter_m3) AS e,SUM(volume_m3) AS v FROM v_gas_sales GROUP BY month,branch_id),
            b AS (SELECT month,branch_id,SUM(estimated_m3) AS e,SUM(sales_m3) AS v FROM v_gas_supply_balance GROUP BY month,branch_id)
            SELECT count(*) AS n FROM a FULL JOIN b USING(month,branch_id) WHERE a.e IS DISTINCT FROM b.e OR a.v IS DISTINCT FROM b.v''')
        assert cur.fetchone()['n']==0,'估抄率等价视图口径不一致'
    # Fresh repository reads prove the app can consume the committed configuration.
    for ds in report['datasets']:
        context=repo.get_dataset_context(ds['id'],'估抄率/账龄/安全指标',80)
        assert all(context['agent_prompts'][n] for n in (1,2,3,4))
        assert len(context['common_questions'])==ds['common_questions']
        assert get_config(ds['id'])['profile']=='generic'
    assert load_data_permissions()==permissions_before,'组织权限配置不应改变'
    report.update(status='passed',organization_nodes=43,permission_changed=False,bottom_tables_changed=False,feishu_connected=False,backup=str(backup))
    (ROOT/'generated/dataset_enrichment_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False),flush=True)

if __name__=='__main__':main()
