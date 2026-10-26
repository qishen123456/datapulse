"""Summarize measured results without treating numeric matching as full AI accuracy."""
import json
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'generated/common_accuracy_20261026'
def summarize():
 results=json.loads((OUT/'results.json').read_text())
 review_file=OUT/'manual_review.json'
 manual=json.loads(review_file.read_text()) if review_file.exists() else {}
 groups={}
 for code in ['GAS_BIZ','GAS_AR','GAS_SAFE']:
  rows=[r for r in results.values() if r['code']==code]
  groups[code]={'planned':16,'completed':len(rows),'measured':dict(Counter(r['status'] for r in rows))}
 issues=[{**r,'manual_review':manual.get(k)} for k,r in results.items() if r['status']!='numeric_match' or manual.get(k,{}).get('status')=='needs_fix']
 summary={'planned':48,'completed':len(results),'numeric_matched':sum(r['status']=='numeric_match' for r in results.values()),'manual_reviews':len(manual),'datasets':groups,'issues':issues,'note':'数值匹配仅证明对象和必要指标与PG一致；完整正确还需核对文字事实、口径和缺数提示。待复核、澄清、失败不记为正确。'}
 (OUT/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
 text=['# 常见问题真实AI准确性验收（2026-10-26）','',f"计划48题，已完成{len(results)}题，其中{summary['numeric_matched']}题通过自动数值核对。",'',summary['note'],'','| 编号 | 问题 | 数值/执行 | 秒 | 人工解读复核 |','| --- | --- | --- | ---: | --- |']
 for key,r in sorted(results.items()):
  m=manual.get(key,{})
  text.append('| '+key+' | '+r['question'].replace('|','/')+' | '+r['status']+' | '+str(r['seconds'])+' | '+str(m.get('note','待复核')).replace('|','/')+' |')
 text+=['','## 参考口径修复','- 同期间同比补齐同比比例；最高估抄率取第一名。','- 居民与工商业分组不混入公益机构。','- 量价重算差异与登记稽核差异分离。','- 到访不遇单位为户次，老旧管网“超过20年”使用严格日期边界。','','## 证据','每题JSON包含用户原问题、独立参考SQL与结果、AI返回SQL/行数据/业务解读；不保存模型提示词、账号密码或密钥。']
 (OUT/'验收报告.md').write_text('\n'.join(text)+'\n')
 print(json.dumps({k:v for k,v in summary.items() if k not in ['issues']},ensure_ascii=False))
if __name__=='__main__':summarize()
