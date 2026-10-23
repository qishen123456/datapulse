"""Read-only PG checks and refreshed expected answers for the simulated warehouse."""
import json
from pathlib import Path
from bookshelf_repository import BookshelfRepository
ROOT=Path(__file__).resolve().parents[1]
queries={
 'branch_monthly_sales':"SELECT month,branch_name,SUM(volume_m3) volume_m3 FROM v_gas_sales WHERE month IN ('2026-08','2026-09') GROUP BY month,branch_name ORDER BY branch_name,month",
 'aged_debt':"SELECT branch_name,SUM(closing_yuan) closing_yuan,SUM(aging_365_plus_yuan) aging_365_plus_yuan FROM v_gas_ar WHERE month='2026-09' GROUP BY branch_name ORDER BY branch_name",
 'network':"SELECT COUNT(*) sections,SUM(length_km) length_km,MIN(length_km) min_km,MAX(length_km) max_km,COUNT(*) FILTER(WHERE gis_loaded_date IS NULL) not_in_gis FROM v_gas_network",
 'open_hazards':"SELECT severity,COUNT(*) total,COUNT(*) FILTER(WHERE due_date<'2026-09-30') overdue FROM v_gas_hazards WHERE completed_date IS NULL GROUP BY severity",
 'ar_reconciliation':"SELECT COUNT(*) invalid FROM v_gas_ar WHERE ABS(opening_yuan+billed_yuan-collected_yuan+adjustment_yuan-closing_yuan)>0.01 OR ABS(closing_yuan-aging_0_30_yuan-aging_31_90_yuan-aging_91_180_yuan-aging_181_365_yuan-aging_365_plus_yuan)>0.01",
 'hazard_join':"SELECT COUNT(*) invalid FROM v_gas_hazards h LEFT JOIN v_gas_network n USING(network_id) WHERE n.network_id IS NULL OR n.org_id<>h.org_id"
}
report={'status':'passed','checks':{}};gold=[]
with BookshelfRepository()._connect() as conn,conn.cursor() as cur:
 for name,query in queries.items():
  cur.execute(query);columns=[d.name for d in cur.description];report['checks'][name]=[dict(zip(columns,row)) for row in cur.fetchall()]
 assert report['checks']['ar_reconciliation'][0]['invalid']==0
 assert report['checks']['hazard_join'][0]['invalid']==0
 assert report['checks']['network'][0]['min_km']>0
 for ds in json.loads((ROOT/'generated/datasets.json').read_text()):
  for question,query in ds['questions']:
   cur.execute(query);columns=[d.name for d in cur.description]
   gold.append(dict(dataset=ds['code'],question=question,sql=query,rows=[dict(zip(columns,row)) for row in cur.fetchall()]))
(ROOT/'generated/realism_pg_checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2,default=str)+'\n')
(ROOT/'generated/golden_results.json').write_text(json.dumps(gold,ensure_ascii=False,indent=2,default=str)+'\n')
print(json.dumps(report,ensure_ascii=False,default=str))
