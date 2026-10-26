"""Exact arithmetic hints for AI interpretation; never a replacement AI answer.

Facts describe returned rows only. Totals are withheld for rates/prices, mixed
periods, identifiers, and signed-value shares. No business risk/causal inference.
"""
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
import re

NON_ADDITIVE=re.compile(r'率|比例|占比|均价|单价|每方|每千|同比|环比|百分|%|ratio|rate|price|average|avg|rank|名次|序号',re.I)
IDENTIFIER=re.compile(r'(^id$|_id$|编码|编号|层级|org_level)',re.I)
TIME_FIELD=re.compile(r'month|date|月份|日期|季度|年份|截止日|cutoff',re.I)

def decimal_value(value):
 if isinstance(value,bool) or value is None:return None
 if not isinstance(value,(int,float,Decimal)):return None
 try:
  number=Decimal(str(value))
  return number if number.is_finite() else None
 except InvalidOperation:return None

def display(value):
 d=Decimal(str(value))
 return {'raw':str(d),'div_10000_1dp':str((d/10000).quantize(Decimal('.1'),rounding=ROUND_HALF_UP)),
         'div_100000000_2dp':str((d/100000000).quantize(Decimal('.01'),rounding=ROUND_HALF_UP))}

def build_numeric_facts(rows):
 rows=[r for r in (rows or []) if isinstance(r,dict)]
 if not rows:return {'scope':'当前返回0行，不等于指标为0','row_count':0,'columns':[]}
 keys=list(dict.fromkeys(k for r in rows for k in r))
 periods={k:{str(r.get(k)) for r in rows if r.get(k) is not None} for k in keys if TIME_FIELD.search(k)}
 mixed_periods=any(len(v)>1 for v in periods.values())
 def identities(row):
  return {k:str(v) for k,v in row.items() if isinstance(v,str) and not TIME_FIELD.search(k)}
 columns=[]
 for key in keys:
  if IDENTIFIER.search(key):continue
  entries=[(i,decimal_value(r.get(key))) for i,r in enumerate(rows)]
  values=[(i,v) for i,v in entries if v is not None]
  if not values:continue
  low=min(v for _,v in values);high=max(v for _,v in values)
  column={'column':key,'minimum':str(low),'maximum':str(high),
          'minimum_objects':[identities(rows[i]) for i,v in values if v==low][:3],
          'maximum_objects':[identities(rows[i]) for i,v in values if v==high][:3]}
  if len(values)==len(rows) and not mixed_periods and not NON_ADDITIVE.search(key):
   total=sum((v for _,v in values),Decimal(0));column['returned_rows_total']=display(total)
   if total>0 and all(v>=0 for _,v in values) and len(values)>1:
    ranked=sorted(values,key=lambda t:t[1],reverse=True)
    column['top_group_shares']=[]
    for n in [1,2,3]:
     if n>=len(values):continue
     selected=ranked[:n];subtotal=sum((v for _,v in selected),Decimal(0))
     column['top_group_shares'].append({'n':n,'objects':[identities(rows[i]) for i,_ in selected],
        'subtotal':str(subtotal),'share_of_returned_rows_percent':str((subtotal/total*100).quantize(Decimal('.01'),rounding=ROUND_HALF_UP))})
  elif mixed_periods:column['total_withheld']='含多个时间点，未推定跨期可加总性'
  else:column['total_withheld']='比率/单价等非可加总指标或含空值'
  columns.append(column)
  if len(columns)>=10:break
 return {'scope':'仅本次查询返回行的算术核对，不证明样本覆盖全部对象；除万/除亿数值仅是换算，须沿用原指标单位。','row_count':len(rows),'mixed_periods':mixed_periods,'columns':columns}
