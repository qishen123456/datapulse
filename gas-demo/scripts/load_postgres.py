"""Load only gas demo warehouse rows; preserve dataset IDs, accounts and permissions.

Run inside the backend environment. Default is read-only verification; --apply
upserts the local snapshot and removes stale locally-owned rows transactionally.
"""
import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from psycopg2 import sql
from psycopg2.extras import Json, execute_values

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from generate_demo import TREE, VERSION, validate
from prepare_runtime import BASE_VIEWS
from bookshelf_repository import BookshelfRepository
from config_manager import get_default_datasource
from organization_tree_store import load_organization_trees


def load(name):
    return json.loads((ROOT / 'generated' / name).read_text())


def run(apply=False):
    tables, tree, datasets = load('model.json'), load('organization_tree.json'), load('datasets.json')
    validate(tables, tree, load('expected_exceptions.json'))
    if set(tables) != set(BASE_VIEWS):
        raise RuntimeError('模型表清单与允许写入的燃气表不一致')
    current_nodes = {n['id']: n for n in load_organization_trees()['nodes'] if n['tree_type_id'] == TREE}
    if set(current_nodes) != {n['id'] for n in tree['nodes']}:
        raise RuntimeError('系统组织树与模拟数据不一致，拒绝写入')
    for node in tree['nodes']:
        actual = current_nodes[node['id']]
        if actual['path_ids'] != node['path_ids'] or actual['name'] != node['name']:
            raise RuntimeError(f"组织路径或名称不一致：{node['id']}")
    source = get_default_datasource()
    repo = BookshelfRepository()
    metadata_source = repo._pick_metadata_datasource()
    def identity(config):
        return (config.get('host'), int(config.get('port') or 5432), config.get('database_name'))
    if not source or source.get('type') != 'postgresql' or identity(source) != identity(metadata_source):
        raise RuntimeError('当前默认问数数据源与燃气表所在 PostgreSQL 不一致，拒绝写入错误数据库')
    report = dict(status='passed',mode='apply' if apply else 'verify',
                  checked_at=datetime.now(timezone.utc).isoformat(),origin='local_simulation',
                  feishu_used=False,organization_nodes=len(current_nodes),tables=[],views=[],datasets=[])
    with repo._connect() as conn, conn.cursor() as cur:
        for name, rows in tables.items():
            target = f'raw_{name}'
            if apply:
                cur.execute(sql.SQL('''CREATE TABLE IF NOT EXISTS {} (
                    id BIGSERIAL PRIMARY KEY,record_id TEXT UNIQUE,fields JSONB,
                    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    sync_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''').format(sql.Identifier(target)))
                cur.execute(sql.SQL('LOCK TABLE {} IN SHARE ROW EXCLUSIVE MODE').format(sql.Identifier(target)))
            cur.execute(sql.SQL('SELECT count(*),count(*) FILTER (WHERE record_id LIKE %s) FROM {}')
                        .format(sql.Identifier(target)), (VERSION + ':%',))
            before, owned = cur.fetchone()
            if before != owned:
                raise RuntimeError(f'{target} 包含非本地模拟记录，拒绝覆盖；请先核对数据来源')
            records = [(f"{VERSION}:{row['business_key']}", Json(row)) for row in rows]
            changed, removed = 0, 0
            if apply:
                execute_values(cur, sql.SQL('''INSERT INTO {} AS existing (record_id,fields) VALUES %s
                    ON CONFLICT(record_id) DO UPDATE SET fields=EXCLUDED.fields,updated_time=NOW(),sync_time=NOW()
                    WHERE existing.fields IS DISTINCT FROM EXCLUDED.fields''').format(sql.Identifier(target)).as_string(cur),
                    records, page_size=max(1, len(records)))
                changed = cur.rowcount
                cur.execute(sql.SQL('DELETE FROM {} WHERE record_id LIKE %s AND NOT(record_id=ANY(%s))')
                            .format(sql.Identifier(target)),(VERSION + ':%', [r[0] for r in records]))
                removed = cur.rowcount
            cur.execute(sql.SQL('SELECT record_id,fields FROM {}').format(sql.Identifier(target)))
            actual_rows = dict(cur.fetchall())
            expected = {key: row for key, row in zip((r[0] for r in records), rows)}
            if actual_rows != expected:
                raise RuntimeError(f'{target} 的实际数据与模拟快照不一致，事务回滚')
            report['tables'].append(dict(table=target,rows=len(actual_rows),before=before,upserted=changed,removed=removed))
        if apply:
            cur.execute((ROOT / 'generated' / 'views.sql').read_text())
        views = sorted(set(BASE_VIEWS.values()) | {'v_gas_supply_balance','v_gas_profit','v_gas_ar_summary'})
        for view in views:
            cur.execute(sql.SQL('SELECT count(*) FROM {}').format(sql.Identifier(view)))
            report['views'].append(dict(view=view,rows=cur.fetchone()[0]))
        for dataset in datasets:
            cur.execute('SELECT id,dataset_name,source_id,is_active FROM bs_datasets WHERE dataset_code=%s',(dataset['code'],))
            record = cur.fetchone()
            if not record or not record[3] or record[2] != source['id']:
                raise RuntimeError(f"{dataset['code']} 未启用或指向错误数据源")
            cur.execute('SELECT table_name FROM bs_schema_definitions WHERE dataset_id=%s',(record[0],))
            if set(row[0] for row in cur.fetchall()) != set(dataset['tables']):
                raise RuntimeError(f"{dataset['code']} 的问数视图映射不一致")
            for question, query in dataset['questions']:
                cur.execute(query)
                cur.fetchall()
            report['datasets'].append(dict(id=record[0],code=dataset['code'],name=record[1],views=dataset['tables'],queries_checked=len(dataset['questions'])))
        cur.execute("SELECT min(month),max(month) FROM v_gas_sales")
        report['period'] = dict(zip(('from','to'),cur.fetchone()))
    report['total_rows'] = sum(t['rows'] for t in report['tables'])
    (ROOT / 'generated' / 'pg_load_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False))
    return report


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply',action='store_true')
    run(parser.parse_args().apply)
