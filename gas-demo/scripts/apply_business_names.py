"""Rename owned gas demo rows and organization labels, preserving IDs and facts."""
import json
from pathlib import Path
from datetime import datetime
from psycopg2 import sql
from psycopg2.extras import Json, execute_values
from bookshelf_repository import BookshelfRepository
from organization_tree_store import load_organization_trees, save_organization_trees
from generate_demo import VERSION, TREE, validate
ROOT=Path(__file__).resolve().parents[1]
model=json.loads((ROOT/'generated/model.json').read_text())
tree=json.loads((ROOT/'generated/organization_tree.json').read_text())
# Validate name consistency without regenerating or changing existing scenario facts.
org_names={r['org_id']:r['org_name'] for r in model['gas_org']}
assert len(org_names)==43
for rows in model.values():
 for row in rows: assert row['org_name']==org_names[row['org_id']]
for node in tree['nodes']: assert node['name']==org_names[node['id']]
current=load_organization_trees();old_tree=json.loads(json.dumps(current))
nodes={n['id']:n for n in current['nodes'] if n['tree_type_id']==TREE}
assert set(nodes)=={n['id'] for n in tree['nodes']}
backup={'organization_tree':old_tree,'tables':{}}
changes=[]
try:
 with BookshelfRepository()._connect() as conn,conn.cursor() as cur:
  for name,rows in model.items():
   target='raw_'+name
   cur.execute(sql.SQL('LOCK TABLE {} IN SHARE ROW EXCLUSIVE MODE').format(sql.Identifier(target)))
   cur.execute(sql.SQL('SELECT record_id,fields FROM {}').format(sql.Identifier(target)))
   actual=dict(cur.fetchall());backup['tables'][target]=actual
   expected={VERSION+':'+r['business_key']:r for r in rows}
   assert actual.keys()==expected.keys(),target+' row keys changed'
   records=[]
   for key,row in expected.items():
    before=actual[key]
    assert {k:v for k,v in before.items() if k not in ['org_name','org_name_path','customer_name']}=={k:v for k,v in row.items() if k not in ['org_name','org_name_path','customer_name']},target+' contains non-name changes'
    if before!=row: records.append((key,Json(row)))
   if records:
    execute_values(cur,sql.SQL('UPDATE {} t SET fields=v.fields::jsonb,updated_time=NOW() FROM (VALUES %s) v(record_id,fields) WHERE t.record_id=v.record_id').format(sql.Identifier(target)).as_string(cur),records,page_size=1000)
   changes.append({'table':target,'renamed_rows':len(records)})
  backup_dir=Path('/app/backups/runtime');backup_dir.mkdir(parents=True,exist_ok=True)
  backup_path=backup_dir/('gas_names_'+datetime.now().strftime('%Y%m%d_%H%M%S')+'.json')
  backup_path.write_text(json.dumps(backup,ensure_ascii=False,default=str));backup_path.chmod(0o600)
  for n in tree['nodes']:
   assert nodes[n['id']]['path_ids']==n['path_ids']
   nodes[n['id']]['name']=n['name']
  save_organization_trees(current,operator='gas-demo-business-names')
except Exception:
 save_organization_trees(old_tree,operator='gas-demo-name-rollback')
 raise
print(json.dumps({'status':'passed','backup':str(backup_path),'changes':changes},ensure_ascii=False))
