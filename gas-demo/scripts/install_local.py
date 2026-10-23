"""Install the demo into the local running application's warehouse.

Run inside backend with PYTHONPATH=/app/backend and the gas-demo directory mounted/copied.
Only raw_gas_* and GAS_* assets are managed. Existing non-demo records are never erased.
"""
import json
import shutil
import sys
from datetime import datetime
from pathlib import Path

from psycopg2 import sql
from psycopg2.extras import Json, execute_values

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/"scripts"))
from generate_demo import TREE, VERSION, validate
from prepare_runtime import LABELS
from bookshelf_repository import BookshelfRepository
from config_manager import CONFIG_DIR, get_default_datasource, read_json, write_json
from organization_tree_store import save_organization_trees


def load(name):
    return json.loads((ROOT/"generated"/name).read_text())


def install():
    tables, tree = load("model.json"), load("organization_tree.json")
    validate(tables, tree, load("expected_exceptions.json"))
    datasets = load("datasets.json")
    fields = load("field_dictionary.json")
    source = get_default_datasource()
    if not source or source.get("type") != "postgresql":
        raise RuntimeError("演示安装需要默认 PostgreSQL 数据源，请先核对数据源")
    repo = BookshelfRepository()
    repo.ensure_schema()
    backup = Path(CONFIG_DIR).parent/"backups"/"gas-demo"/datetime.now().strftime("%Y%m%d-%H%M%S")
    backup.mkdir(parents=True, exist_ok=True)
    for name in ("organization_trees.json", "data_permissions.json"):
        if (Path(CONFIG_DIR)/name).exists():
            shutil.copy2(Path(CONFIG_DIR)/name, backup/name)
    installed = []
    results = []
    with repo._connect() as conn, conn.cursor() as cur:
        # Seeding is all-or-nothing across nine tables and all dataset metadata.
        for name, rows in tables.items():
            target = f"raw_{name}"
            cur.execute(sql.SQL('''CREATE TABLE IF NOT EXISTS {} (
                id BIGSERIAL PRIMARY KEY,record_id TEXT UNIQUE,fields JSONB,
                created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                sync_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''').format(sql.Identifier(target)))
            cur.execute(sql.SQL("SELECT count(*),count(*) FILTER (WHERE record_id LIKE 'gas-demo-v1:%%') FROM {}").format(sql.Identifier(target)))
            total, owned = cur.fetchone()
            if total and total != owned:
                raise RuntimeError(f"{target} 已包含非本地模拟记录，拒绝覆盖")
            execute_values(cur, sql.SQL('''INSERT INTO {} (record_id,fields) VALUES %s
                ON CONFLICT(record_id) DO UPDATE SET fields=EXCLUDED.fields,updated_time=NOW(),sync_time=NOW()''').format(sql.Identifier(target)).as_string(cur),
                [(f"{VERSION}:{r['business_key']}", Json(r)) for r in rows])
            cur.execute(sql.SQL("SELECT count(*) FROM {}").format(sql.Identifier(target)))
            assert cur.fetchone()[0] == len(rows), target
        cur.execute((ROOT/"generated/views.sql").read_text())
        for ds in datasets:
            description = ("虚构演示 · 本地模拟预装，尚未连接飞书。时间2024-01至2026-09；金额元，气量方。"
                           "组织树43节点；禁止无证据认定偷盗气；不含税演示税前利润。")
            cur.execute('''INSERT INTO bs_datasets(dataset_code,dataset_name,business_domain,source_id,description,is_active)
                VALUES (%s,%s,%s,%s,%s,FALSE) ON CONFLICT(dataset_code) DO UPDATE SET
                dataset_name=EXCLUDED.dataset_name,business_domain=EXCLUDED.business_domain,
                source_id=EXCLUDED.source_id,description=EXCLUDED.description,updated_at=NOW()
                RETURNING id''', (ds["code"],ds["name"],ds["domain"],source["id"],description))
            dsid = cur.fetchone()[0]
            installed.append(dict(id=dsid,code=ds["code"],name=ds["name"]))
            for table in ("bs_dataset_synonyms","bs_data_dictionary_items","bs_schema_definitions",
                          "bs_golden_sql_samples","bs_common_questions"):
                cur.execute(sql.SQL("DELETE FROM {} WHERE dataset_id=%s").format(sql.Identifier(table)), (dsid,))
            for synonym in ds["synonyms"]:
                cur.execute("INSERT INTO bs_dataset_synonyms(dataset_id,synonym,normalized_synonym) VALUES (%s,%s,%s)",
                            (dsid,synonym,synonym.lower()))
            for view in ds["tables"]:
                cur.execute("SELECT column_name,data_type FROM information_schema.columns WHERE table_schema='public' AND table_name=%s ORDER BY ordinal_position",(view,))
                columns = cur.fetchall()
                column_ddl = ", ".join(f'"{key}" {typ}' for key,typ in columns)
                cur.execute("INSERT INTO bs_schema_definitions(dataset_id,table_name,ddl_sql,description) VALUES (%s,%s,%s,%s)",
                            (dsid,view,f'CREATE TABLE {view} ({column_ddl});',"模拟数据视图；先聚合再关联，避免多对多重复"))
                for key, typ in columns:
                    label = LABELS.get(key,dict(sales_m3="销气量_方",sales_revenue_yuan="销气收入_元",
                        estimated_m3="估抄量_方",loss_m3="供销差量_方",loss_rate="供销差率_小数",
                        pretax_profit_yuan="模拟税前利润_元",total_revenue_yuan="总收入_元",
                        aging_over_180_yuan="超过180天应收_元").get(key,key))
                    cur.execute('''INSERT INTO bs_data_dictionary_items
                        (dataset_id,table_name,column_name,semantic_name,data_type,extraction_rule)
                        VALUES (%s,%s,%s,%s,%s,%s)''', (dsid,view,key,label,typ,
                        "直接读取业务视图；金额元，数量方；比率总分子/总分母；快照不可跨月求和"))
            rules = ["只使用本数据集声明视图；必须按用户组织范围取数后聚合",
                     "最新月2026-09，2026只有前三季度，同比必须同期间",
                     "销售、采购、客户、隐患事实不得明细直接多对多连接",
                     "期末余额/用户数只取选定期末，比例按分子分母加权汇总",
                     "采购为组织边界模拟计量，成本按合同价分摊；阈值仅为演示设定",
                     "估抄与老旧管网是排查线索，不是盗气或漏损因果证据",
                     "工商户排名限模拟客户池，居民为汇总桶；税前利润不能称净利润",
                     "账龄是模拟月末分布，不支持逐发票迁徙；缺三单/追缴/IC卡复核明细时明确缺数据"]
            content = description+"\n"+"\n".join(rules)+"\n高阶问题："+"；".join(ds["deep"])
            cur.execute('''INSERT INTO bs_lld_documents(dataset_id,version,title,content,redline_rules,created_by)
                VALUES (%s,1,%s,%s,%s,'gas-demo') ON CONFLICT(dataset_id,version)
                DO UPDATE SET content=EXCLUDED.content,redline_rules=EXCLUDED.redline_rules,updated_at=NOW()''',
                        (dsid,ds["name"]+"演示口径",content,Json(rules)))
            for order,(question,query) in enumerate(ds["questions"]):
                cur.execute(query)
                columns = [d[0] for d in cur.description]
                expected = [dict(zip(columns,row)) for row in cur.fetchall()]
                results.append(dict(dataset=ds["code"],question=question,sql=query,rows=expected))
                cur.execute('''INSERT INTO bs_golden_sql_samples(dataset_id,intent_type,question,sql_text,tags,quality_score,created_by)
                    VALUES (%s,'aggregate',%s,%s,%s,95,'gas-demo')''',(dsid,question,query,Json(["燃气模拟","2026-09"])))
                cur.execute('''INSERT INTO bs_common_questions(dataset_id,question_text,sort_order,is_active)
                    VALUES (%s,%s,%s,TRUE)''',(dsid,question,order+1))
        cur.execute("SELECT SUM(pretax_profit_yuan) FROM v_gas_profit WHERE month LIKE '2024-%'")
        profit = cur.fetchone()[0]
        assert profit < 0, "模拟2024税前利润应为亏损"
    # Merge only this tree; existing trees and unrelated permission rules are preserved.
    existing = read_json("organization_trees.json") or {"tree_types":[],"nodes":[]}
    existing["tree_types"] = [t for t in existing.get("tree_types",[]) if t.get("id") != TREE]+tree["tree_types"]
    existing["nodes"] = [n for n in existing.get("nodes",[]) if n.get("tree_type_id") != TREE]+tree["nodes"]
    normalized = save_organization_trees(existing, "gas-demo-local-installer")
    actual = {n["id"]:n for n in normalized["nodes"] if n["tree_type_id"] == TREE}
    assert len(actual) == 43
    for n in tree["nodes"]:
        assert actual[n["id"]]["path_ids"] == n["path_ids"]
    perms = read_json("data_permissions.json") or {"rules":{}}
    assert isinstance(perms.get("rules",{}),dict), "旧格式权限需要先转换，拒绝覆盖"
    for ds in installed:
        perms.setdefault("rules",{})[str(ds["id"])] = dict(dataset_id=ds["id"],mode="org_tree",
            tree_type_id=TREE,tree_type_ids=[TREE],organization_node_ids=["JC-GROUP"],
            scope={"organization_field":"org_id","organization_values":[]},
            note="燃气演示组织树；未绑定组织的普通账号不开放；跨组织汇总需验证取数前过滤")
    write_json("data_permissions.json",perms)
    with repo._connect() as conn, conn.cursor() as cur:
        cur.execute("UPDATE bs_datasets SET is_active=TRUE WHERE id=ANY(%s)",([ds["id"] for ds in installed],))
    report = dict(datasets=installed,organization_nodes=43,origin="本地模拟预装，未连接飞书",
                  golden_queries=len(results),profit_2024_yuan=str(profit),backup=str(backup))
    (ROOT/"generated/local_installation.json").write_text(json.dumps(report,ensure_ascii=False,indent=2))
    (ROOT/"generated/golden_results.json").write_text(json.dumps(results,ensure_ascii=False,indent=2,default=str))
    print(json.dumps(report,ensure_ascii=False))


if __name__ == "__main__":
    install()
