"""Read-only runtime smoke checks. Credentials/tokens never printed or saved."""
import json
from pathlib import Path
import requests
from controllers.auth import _admin_config
from config_manager import read_json
from bookshelf_repository import BookshelfRepository
from organization_tree_store import load_organization_trees
from data_permission_store import is_dataset_allowed

ROOT = Path(__file__).resolve().parents[1]
base = "http://127.0.0.1:5002"
cfg = _admin_config()
s = requests.Session()
login = s.post(base+"/api/auth/login",json=dict(username=cfg["username"],password=cfg["password"]),timeout=10)
login.raise_for_status()
assert login.json().get("success"), "管理员配置登录失败"
s.headers["X-Auth-Token"] = login.json()["token"]
catalog = s.get(base+"/api/bookshelves/datasets",timeout=20)
catalog.raise_for_status()
datasets = [d for d in catalog.json()["datasets"] if d["dataset_code"] in {"GAS_BIZ","GAS_AR","GAS_SAFE"}]
assert len(datasets) == 3
tree = load_organization_trees()
nodes = {n["id"]:n for n in tree["nodes"] if n["tree_type_id"] == "gas_jc_tree"}
assert len(nodes) == 43
repo = BookshelfRepository()
with repo._connect() as conn, conn.cursor() as cur:
    cur.execute("SELECT fields->>'org_id', fields->>'org_path' FROM raw_gas_org")
    source_orgs = dict(cur.fetchall())
    assert set(nodes) == set(source_orgs)
    for code,path in source_orgs.items():
        assert nodes[code]["path_ids"] == path.strip('/').split('/')
    # Verify Bitable's millisecond date representation converts to the same day.
    cur.execute("SELECT (to_timestamp(1789488000000::numeric/1000) AT TIME ZONE 'Asia/Shanghai')::date::text")
    assert cur.fetchone()[0] == "2026-09-16"
checked = 0
for ds in datasets:
    assert not is_dataset_allowed({"role":"user","username":"unbound-test"},ds["id"])
    user = {"role":"user","username":"scope-test","organization_node_ids":["BINJIANG"]}
    assert is_dataset_allowed(user,ds["id"])
    context = repo.get_dataset_context(ds["id"],"演示检查",80)
    assert len(context["common_questions"]) == 12
    for q in context["golden_sql_samples"]:
        result = s.post(base+f"/api/bookshelves/datasets/{ds['id']}/sql-preview",
                        json=dict(sql=q["sql_text"],limit=100),timeout=20)
        result.raise_for_status()
        assert "rows" in result.json()
        checked += 1
report = dict(status="passed",organization_nodes=43,datasets=[d["dataset_code"] for d in datasets],
              golden_queries_via_http=checked,unbound_account="denied",
              organization_binding="BINJIANG scope membership passed",
              limitations=["普通账号聚合前行权限尚需独立验收，不据此开放业务账号",
                           "本次未调用真实LLM，未连接飞书"])
(ROOT/"generated/runtime_checks.json").write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps(report,ensure_ascii=False))
# End the test session rather than leave an extra admin token around.
s.post(base+"/api/auth/logout",timeout=10)
