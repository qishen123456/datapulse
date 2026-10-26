"""Independent read-only checks of representative semantic queries, without AI calls."""
import json
from pathlib import Path
from bookshelf_repository import BookshelfRepository
from semantic_upgrade import EXAMPLES
root=Path(__file__).resolve().parents[1]
report={}
with BookshelfRepository()._connect() as conn,conn.cursor() as cur:
 cur.execute(EXAMPLES['GAS_BIZ'][0][1]);rows=cur.fetchall();assert len(rows)==5
 delta=sum(row[4] for row in rows)
 cur.execute("SELECT SUM(volume_m3) FILTER(WHERE month='2026-09')-SUM(volume_m3) FILTER(WHERE month='2026-08') FROM v_gas_sales WHERE month IN ('2026-08','2026-09')")
 assert delta==cur.fetchone()[0]
 report['mom_difference_reconciles']=True
 cur.execute(EXAMPLES['GAS_AR'][3][1]);assert not cur.fetchall()
 report['ar_rollforward_no_difference']=True
 cur.execute(EXAMPLES['GAS_AR'][7][1]);mismatches=cur.fetchall()
 report['registered_vs_recomputed_audit_difference_rows']=len(mismatches)
 cur.execute(EXAMPLES['GAS_SAFE'][8][1]);row=cur.fetchone();assert row[-1] is None
 report['zero_inspection_denominator_is_null']=True
 cur.execute(EXAMPLES['GAS_SAFE'][7][1]);deduplicated=sum(r[2] for r in cur.fetchall())
 cur.execute("SELECT SUM(length_km) FROM v_gas_network WHERE laid_date<='2026-09-30' AND network_id IN(SELECT network_id FROM v_gas_hazards WHERE found_date<='2026-09-30')")
 assert deduplicated==cur.fetchone()[0]
 report['hazard_linked_network_deduplicated']=True
 for code in ['GAS_BIZ','GAS_AR']:
  cur.execute(EXAMPLES[code][-1][1]);assert not cur.fetchall()
 report['explicit_future_month_not_substituted']=True
report.update(status='passed',ai_calls=0)
(root/'generated/semantic_query_checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False))
