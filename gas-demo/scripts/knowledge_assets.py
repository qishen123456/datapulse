"""Versioned semantic assets for the three PG gas datasets; no credentials."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
TAG='gas-knowledge-20261022'
GRAINS={
 'v_gas_org':'一行一个组织节点，org_id全局唯一；层级1集团/2分公司/3服务中心/4网格，43节点。',
 'v_gas_sales':'一行=月份×销售网格×客户类型；business_key唯一；20个销售网格×4类客户×33个月。',
 'v_gas_supply_sources':'一行=月份×服务中心×气源；同中心同月有多个气源，不能直接连接销售明细。',
 'v_gas_supply_balance':'一行=月份×销售服务中心，month+org_id唯一；采购与销售分别聚合后关联，org_id是服务中心编码。',
 'v_gas_profit':'一行=月份×服务中心，month+org_id唯一；已经带入该中心的销气收入、采购成本，不能再次连接后重复求和。',
 'v_gas_growth':'一行=月份×销售网格×客户类型；户数为模拟汇总，期末户数不可跨月累加。',
 'v_gas_ar':'一行=月份×模拟客户或居民/公益汇总桶；month+customer_id唯一，单月120个对象，非真实全量客户名单。',
 'v_gas_ar_summary':'一行=月份×销售网格×客户类型；已汇总客户记录，不能与v_gas_ar重复叠加。',
 'v_gas_safety':'一行=月份×网格；含高压输配网格；计数为当月流量，不是历史未完成存量。',
 'v_gas_network':'一行=一条管段，network_id唯一；无month字段，按laid_date/gis_loaded_date做截止日判断。',
 'v_gas_hazards':'一行=一张隐患工单，hazard_id唯一；通过network_id多对一关联管段，时间口径必须明确。',
}
COMMON=[
 '全部数据为虚构演示，不代表真实企业。月度事实仅覆盖2024-01至2026-09；“最新月”是数据MAX(month)，不是系统当前月；用户明确问2026-10必须按10月查空，不擅自换成9月。',
 '原始存储单位：气量方/立方米、金额元、里程公里、比例0到1。展示成万元/万方必须显式除10000并标单位；比率百分数展示才乘100。',
 '保留总主理人+领域专家框架。普通问数也实际经过AI，金标只作生成与审核参考，不允许样例直返或缓存答案代替AI。高阶先确认计划，再并行取证。',
 '复用系统gas_jc_tree组织树及现有数据权限。org_id是当前记录所属组织；branch_id是分公司编码、center_id是服务中心编码，不能把分公司编码直接等同网格org_id。跨层级范围用授权组织路径或组织维表解析。',
 '超级管理员可全域汇总，不因SQL没有组织WHERE就认定越权；普通账号权限必须由系统在取数前强制处理，不能由LLM文字代替。未绑定组织普通账号不开放。',
 '分公司：滨江BINJIANG、沙湖SHAHU、经开JINGKAI、临港LINGANG、高新GAOXIN、高压输配GYSP。高压输配没有销气职责；销售榜通常5家，安全/管网可有6家，不补造GYSP销气数据或强行补零。',
 '只使用本数据集声明的业务视图。事实表不得按月份、分公司或org_id单键明细互连；先各自聚合至相同时间与组织粒度，或使用已准备的汇总视图。',
 '组织维表v_gas_org.org_id唯一，事实视图.org_id可多对一关联。任何比例都先加总分子分母，再相除；分母0用NULLIF返回NULL，不补0、不简单平均比例。',
 '空结果不等于业务值0；取证失败不等于源库没有数据。AI/审核失败要明确未完成，禁止把规则摘要标作AI结论。',
 '数值差异、单月估抄率和老旧管网只能作为调查线索，不证明因果、偷盗气或系统性管理问题；无正式统计检验不输出正负相关结论。预测需专门模型和回测。',
]

def metric(key,label,view,column,expression,unit='元',aggregation='sum',note=''):
 return dict(key=key,label=label,sourceTable=view,column=column,expression=expression,unit=unit,aggregation=aggregation,format='percent' if unit=='0–1' else 'amount' if unit=='元' else 'number',notes=note)

BIZ=[
 metric('sales_volume','销气量','v_gas_sales','销气量_方','SUM(volume_m3)','方'),
 metric('sales_revenue','销气收入','v_gas_sales','销气收入_元','SUM(revenue_yuan)'),
 metric('average_price','销气均价','v_gas_sales','销气均价_元每方','SUM(revenue_yuan)/NULLIF(SUM(volume_m3),0)','元/方','ratio','收入/销量加权，不能AVG(price_yuan_m3)。'),
 metric('estimated_ratio','估抄率','v_gas_sales','估抄率','SUM(estimated_meter_m3)::numeric/NULLIF(SUM(volume_m3),0)','0–1','ratio'),
 metric('inlet_volume','边界入口气量','v_gas_supply_balance','入口气量_方','SUM(inlet_m3)','方'),
 metric('purchase_cost','采购成本','v_gas_supply_balance','采购成本_元','SUM(purchase_cost_yuan)'),
 metric('loss_volume','供销差量','v_gas_supply_balance','供销差量_方','SUM(inlet_m3)-SUM(sales_m3)','方'),
 metric('loss_ratio','供销差率','v_gas_supply_balance','供销差率','(SUM(inlet_m3)-SUM(sales_m3))/NULLIF(SUM(inlet_m3),0)','0–1','ratio'),
 metric('pretax_profit','模拟税前利润','v_gas_profit','模拟税前利润_元','SUM(pretax_profit_yuan)','元','sum','缺所得税，绝不能称净利润。'),
 metric('total_revenue','总收入','v_gas_profit','总收入_元','SUM(total_revenue_yuan)'),
 metric('connected_users','新增通气户数','v_gas_growth','新增通气户数','SUM(connected_users)','户'),
 metric('ending_users','期末户数','v_gas_growth','期末户数','SUM(ending_users)','户','snapshot','只选定期末，不能跨月累加。'),
]
AR=[
 metric('closing_ar','期末应收','v_gas_ar','期末应收_元','SUM(closing_yuan)','元','snapshot','只选定期末，不跨月求和。'),
 metric('opening_ar','期初应收','v_gas_ar','期初应收_元','SUM(opening_yuan)','元','snapshot'),
 metric('billed_ar','本期应收','v_gas_ar','本期应收_元','SUM(billed_yuan)'),
 metric('collected_ar','本期回款','v_gas_ar','本期回款_元','SUM(collected_yuan)'),
 metric('collection_ratio','气费回收率','v_gas_ar','回收率','SUM(collected_yuan)/NULLIF(SUM(billed_yuan),0)','0–1','ratio','可能含历史欠款回收，不强制截断到100%。'),
 metric('long_aging','超过180天应收','v_gas_ar','长账龄应收_元','SUM(aging_181_365_yuan+aging_365_plus_yuan)','元','snapshot'),
 metric('provision','期末计提余额','v_gas_ar','计提余额_元','SUM(provision_yuan)','元','snapshot'),
 metric('recomputed_provision','演示应计提金额','v_gas_ar','演示应计提_元','SUM(ROUND(aging_0_30_yuan*0.01+aging_31_90_yuan*0.03+aging_91_180_yuan*0.10+aging_181_365_yuan*0.30+aging_365_plus_yuan*0.70,2))','元','snapshot','1/3/10/30/70%仅为演示假设，非准则规定。'),
 metric('billing_difference','量价稽核差异','v_gas_sales','稽核差异_元','SUM(audit_difference_yuan)'),
]
SAFE=[
 metric('inspection_ratio','安检覆盖率','v_gas_safety','安检覆盖率','SUM(inspected)::numeric/NULLIF(SUM(due_inspect),0)','0–1','ratio'),
 metric('emergency_ratio','抢修及时率','v_gas_safety','抢修及时率','SUM(emergency_on_time)::numeric/NULLIF(SUM(emergency_total),0)','0–1','ratio'),
 metric('not_home','当月到访不遇户次','v_gas_safety','到访不遇户次','SUM(not_at_home)','户次','sum','月度过程计数，不能解释成历史待处理存量。'),
 metric('three_piece','当月三件套安装户数','v_gas_safety','三件套安装户数','SUM(three_piece_installed)','户'),
 metric('network_length','截止日管网里程','v_gas_network','管网里程_公里','SUM(length_km)','公里','snapshot','只纳入laid_date不晚于用户截止日的管段。'),
 metric('gis_ratio','截止日GIS入库率','v_gas_network','GIS入库率',"SUM(CASE WHEN gis_loaded_date<='2026-09-30' THEN length_km ELSE 0 END)/NULLIF(SUM(length_km),0)",'0–1','ratio','示例截止日需与用户问题同步修改，并限定laid_date<=截止日。'),
 metric('hazard_closed_ratio','截至日隐患闭环率','v_gas_hazards','隐患闭环率',"COUNT(*) FILTER(WHERE completed_date<='2026-09-30')::numeric/NULLIF(COUNT(*),0)",'0–1','ratio','限定found_date<=截止日；示例日期应同步替换；历史状态按完成日期重建。'),
 metric('overdue_hazards','截至日超期未闭环隐患数','v_gas_hazards','超期未闭环隐患数','COUNT(*)','单','snapshot','found_date<=截止日 AND due_date<截止日 AND (completed_date IS NULL OR completed_date>截止日)。'),
]
EXTRA={
 'GAS_BIZ':[
 ('2026年9月各客户类型的加权销气均价是多少',"SELECT user_type,SUM(revenue_yuan)/NULLIF(SUM(volume_m3),0) AS 销气均价_元每方 FROM v_gas_sales WHERE month='2026-09' GROUP BY user_type"),
 ('2026年9月各分公司的估抄量与估抄率是多少',"SELECT branch_id,branch_name,SUM(estimated_meter_m3) AS 估抄量_方,SUM(volume_m3) AS 销气量_方,SUM(estimated_meter_m3)::numeric/NULLIF(SUM(volume_m3),0) AS 估抄率 FROM v_gas_sales WHERE month='2026-09' GROUP BY branch_id,branch_name"),
 ('2026年9月哪些服务中心超过演示供销差阈值',"SELECT org_id,org_name,loss_rate,loss_threshold FROM v_gas_supply_balance WHERE month='2026-09' AND loss_rate>loss_threshold"),
 ('2026年前三季度每月模拟税前利润是多少',"SELECT month,SUM(pretax_profit_yuan) AS 模拟税前利润_元 FROM v_gas_profit WHERE month BETWEEN '2026-01' AND '2026-09' GROUP BY month ORDER BY month"),
 ('2026年9月各分公司销气量环比8月变化多少',"WITH m AS (SELECT month,branch_name,SUM(volume_m3) AS volume FROM v_gas_sales WHERE month BETWEEN '2026-08' AND '2026-09' GROUP BY month,branch_name), x AS (SELECT *,LAG(volume) OVER(PARTITION BY branch_name ORDER BY month) AS prev FROM m) SELECT branch_name,volume AS 本月销气量_方,prev AS 上月销气量_方,(volume-prev)/NULLIF(prev,0) AS 销气量环比 FROM x WHERE month='2026-09'"),
 ('数据最新月份各分公司销气量是多少',"SELECT month,branch_name,SUM(volume_m3) AS 销气量_方 FROM v_gas_sales WHERE month=(SELECT MAX(month) FROM v_gas_sales) GROUP BY month,branch_name ORDER BY 销气量_方 DESC")],
 'GAS_AR':[
 ('2026年9月末应收账龄结构是什么样',"SELECT SUM(aging_0_30_yuan) AS 账龄0至30天_元,SUM(aging_31_90_yuan) AS 账龄31至90天_元,SUM(aging_91_180_yuan) AS 账龄91至180天_元,SUM(aging_181_365_yuan) AS 账龄181至365天_元,SUM(aging_365_plus_yuan) AS 超过365天_元 FROM v_gas_ar WHERE month='2026-09'"),
 ('按演示账龄比例复核2026年9月末计提金额',"SELECT SUM(provision_yuan) AS 已计提_元,SUM(ROUND(aging_0_30_yuan*0.01+aging_31_90_yuan*0.03+aging_91_180_yuan*0.10+aging_181_365_yuan*0.30+aging_365_plus_yuan*0.70,2)) AS 演示应计提_元 FROM v_gas_ar WHERE month='2026-09'"),
 ('2026年9月各分公司应收滚动平衡有没有差异',"SELECT branch_name,SUM(opening_yuan+billed_yuan-collected_yuan+adjustment_yuan-closing_yuan) AS 应收滚动差异_元 FROM v_gas_ar WHERE month='2026-09' GROUP BY branch_name"),
 ('2026年9月末有应收余额的模拟工商客户有多少个',"SELECT COUNT(DISTINCT customer_id) AS 有余额模拟工商客户数 FROM v_gas_ar WHERE month='2026-09' AND object_kind='模拟客户' AND closing_yuan>0"),
 ('2026年9月末沙湖分公司应收余额是多少',"SELECT SUM(closing_yuan) AS 期末应收_元 FROM v_gas_ar WHERE month='2026-09' AND branch_id='SHAHU'"),
 ('2026年前三季度各分公司累计气费回收率',"SELECT branch_name,SUM(collected_yuan)/NULLIF(SUM(billed_yuan),0) AS 累计气费回收率 FROM v_gas_ar WHERE month BETWEEN '2026-01' AND '2026-09' GROUP BY branch_name")],
 'GAS_SAFE':[
 ('2026年9月各分公司三件套安装和到访不遇情况',"SELECT branch_name,SUM(three_piece_installed) AS 当月三件套安装户数,SUM(not_at_home) AS 当月到访不遇户次 FROM v_gas_safety WHERE month='2026-09' GROUP BY branch_name"),
 ('截至2026年9月底各分公司隐患闭环率',"SELECT branch_name,COUNT(*) AS 已发现工单数,COUNT(*) FILTER(WHERE completed_date<='2026-09-30') AS 截至日已闭环数,COUNT(*) FILTER(WHERE completed_date<='2026-09-30')::numeric/NULLIF(COUNT(*),0) AS 隐患闭环率 FROM v_gas_hazards WHERE found_date<='2026-09-30' GROUP BY branch_name"),
 ('截至2026年9月底重大超期未闭环隐患关联哪些管段',"SELECT h.hazard_id,h.org_id,h.org_name,h.network_id,h.due_date,n.material,n.pressure_level FROM v_gas_hazards h LEFT JOIN v_gas_network n ON h.network_id=n.network_id WHERE h.found_date<='2026-09-30' AND h.due_date<'2026-09-30' AND (h.completed_date IS NULL OR h.completed_date>'2026-09-30') AND h.severity='重大'"),
 ('截至2026年9月底各分公司管网里程和GIS入库率',"SELECT branch_name,SUM(length_km) AS 管网里程_公里,SUM(CASE WHEN gis_loaded_date<='2026-09-30' THEN length_km ELSE 0 END)/NULLIF(SUM(length_km),0) AS GIS入库率 FROM v_gas_network WHERE laid_date<='2026-09-30' GROUP BY branch_name"),
 ('回看截至2026年6月底各分公司未闭环隐患数',"SELECT branch_name,COUNT(*) AS 截至日未闭环数 FROM v_gas_hazards WHERE found_date<='2026-06-30' AND (completed_date IS NULL OR completed_date>'2026-06-30') GROUP BY branch_name"),
 ('2026年9月各分公司每千公里泄漏次数',"WITH l AS (SELECT branch_id,SUM(leak_count) AS leaks FROM v_gas_safety WHERE month='2026-09' GROUP BY branch_id), n AS (SELECT branch_id,SUM(length_km) AS km FROM v_gas_network WHERE laid_date<='2026-09-30' GROUP BY branch_id) SELECT l.branch_id,l.leaks AS 当月泄漏次数,n.km AS 截至日管网公里,l.leaks*1000::numeric/NULLIF(n.km,0) AS 次每千公里 FROM l JOIN n ON l.branch_id=n.branch_id")],
}
SPECIFIC={
 'GAS_BIZ':[
 '经营范围：销气量价、购气成本、供销差、模拟税前利润、用户增长。财务应收/账龄应路由GAS_AR；隐患安检管网应路由GAS_SAFE。',
 '估抄率首选v_gas_sales：SUM(estimated_meter_m3)/SUM(volume_m3)。v_gas_supply_balance中estimated_m3、sales_m3分别来自同月同服务中心销售明细求和；在相同月份、分公司范围按SUM(estimated_m3)/SUM(sales_m3)计算等价，不能仅因使用此已声明汇总视图就判错。网格/客户类型下钻必须回到销售明细；不跨粒度混算。',
 '供销差优先v_gas_supply_balance；它已按month+center_id/org_id聚合采购与销售后关联。inlet_m3-sales_m3为差量，以inlet_m3为分母。loss_threshold只为演示阈值，不是法定或已核定标准；跨中心不取单个MAX阈值当统一标准。',
 'v_gas_profit. pretax_profit_yuan=销气收入+安装收入+增值收入-采购成本-安装成本-增值成本-配气成本-管理费用-财务费用-减值费用。没有所得税字段，不能回答税后净利润；不能称每方均摊成本为实测逐用户成本。',
 'v_gas_growth: ending_users=opening_users+connected_users-churn_users。connected_users是新增通气而非报装；applied_users是报装；potential_users是模拟潜在可接入户，不是法定全部人口基数。'
 ],
 'GAS_AR':[
 '财务范围：应收余额、回款、账龄、演示计提和销气量价稽核。销气利润供销差属GAS_BIZ；管网安检属GAS_SAFE。',
 '余额是时点：closing=opening+billed-collected+adjustment；账龄五段合计=closing。月末应收不能跨月SUM。累计回收率以期间collected总和/billed总和计算，不平均月度比例。',
 '优先v_gas_ar客户明细。v_gas_ar_summary是同月、网格、客户类型的客户聚合，可以用于组织汇总或长账龄应收；不可把明细与汇总重复累加，不能用汇总视图作客户名单。',
 '单月120个对象=80个模拟工商客户+40个居民/公益汇总桶。object_kind=模拟客户才是客户名单；汇总桶不是一个真实用户，不能COUNT桶得到居民户数。只有应收及账龄分布，没有逐张发票到期日，不能声称逐发票逾期迁徙已核验。',
 '按账龄1%、3%、10%、30%、70%计算演示应计提，逐行四舍五入到分后再SUM，与provision_yuan比较；比例只是假设，不是审计准则或实际会计政策。',
 '量价稽核用v_gas_sales的theoretical_revenue_yuan、revenue_yuan和audit_difference_yuan；不能用显示的四舍五入均价反算替代。销售和应收事实按月网格客户类型聚合后再关联，且必须同时匹配month+org_id+user_type；禁止明细多对多。'
 ],
 'GAS_SAFE':[
 '安全范围：月度安检、到访不遇、三件套安装、抢修、泄漏次数，以及管段和隐患工单。无伤亡、停气时长、IC卡基表控制器、三单对账、盗气处罚或追缴明细，问到须明确不支持。',
 '安检覆盖率=SUM(inspected)/SUM(due_inspect)；抢修及时率=SUM(emergency_on_time)/SUM(emergency_total)。not_at_home和three_piece_installed是当月过程计数，不是历史未处理存量或累计安装存量。',
 '管段维表v_gas_network.network_id唯一；工单v_gas_hazards.network_id可多对一连接，不能将连接后的length_km按工单行SUM，否则重复计算里程。月度安检事实与工单/管段只能各自按组织汇总后比较。',
 '历史截至日T：仅纳入found_date<=T的工单；completed_date<=T算已闭环；completed_date为空或>T算当时未闭环；due_date<T且当时未闭环算超期（截止日当天不判已过期）。不能直接拿当前status还原历史。',
 '管网截至日T用laid_date<=T作总里程基数，gis_loaded_date<=T作为已入库条件，日期为空为未入库。以2026-09-30为示例时，老旧20年阈值是2006-09-30；用户换日期必须同步换阈值。工单数据截至2026-09-30，不回答未来状态。',
 '闭环率必须说明是截至日全部已发现工单闭环率还是当期新发现工单闭环率，未说明时先明确口径。泄漏次数每千公里=同期间泄漏次数/截至日有效里程*1000，不能称泄漏率百分比。'
 ]}


def bundle(datasets):
 out=[]
 for ds in datasets:
  code=ds['code']; metrics={'GAS_BIZ':BIZ,'GAS_AR':AR,'GAS_SAFE':SAFE}[code]
  views=list(dict.fromkeys(ds['tables']+['v_gas_org']))
  rules=COMMON+SPECIFIC[code]
  content='\n'.join(['# '+ds['name']+' · 可执行问数口径', '知识版本：'+TAG, '## 业务边界与红线']+['- '+r for r in rules]+['## 视图与粒度']+['- '+v+'：'+GRAINS[v] for v in views]+['## 指标目录（按问题选择，不要求一次返回全部指标）']+['- '+m['label']+'：'+m['sourceTable']+'；'+m['expression']+'；单位'+m['unit']+'；'+m['notes'] for m in metrics]+['## 高阶分析建议']+['- '+q for q in ds['deep']])
  common='\n'.join(SPECIFIC[code])
  prompts={
   1:'本域路由与问题澄清：'+common+'\n最新数据2026-09，保留用户指定的时间/组织/指标。指标缺失明确说明，不拿相邻指标替代。',
   2:'本域SQL专家：'+common+'\nSQL必须以真实字段字典和已声明视图为准，按所问指标选表，不要求输出整个指标目录。金额元、气量方、比率0–1，比例聚合用总分子/总分母。事实关联先聚合，不能多对多。样例仅供本轮AI生成参考。',
   3:'本域审核专家：'+common+'\n审核真实DDL、时间、粒度、单位及用户明确的组织条件。不能凭字段名相似猜测错误，不能因为合法等价视图与样例不同就拒绝。审核拒绝不得放行原SQL；修复后须重新审核。权限以服务端授权上下文和执行阶段为准。',
   4:'本域分析专家：'+common+'\n只回答本轮问题，第一段直接给结论与时间/数值/单位。事实、差异、假设分别说明；缺数据或取证失败如实提示。没有检验不声称相关、没有证据不声称因果。相近且舍入相同的比例不强行做细微排名。',
  }
  queries=[dict(question=q,sql=s) for q,s in ds['questions']+EXTRA[code]]
  detail={'GAS_BIZ':'列出2026年9月沙湖分公司各网格的估抄率，同时返回组织编码','GAS_AR':'列出2026年9月末沙湖分公司有余额的模拟工商客户明细','GAS_SAFE':'列出截至2026年9月底重大超期未闭环隐患及关联管段'}[code]
  trend={'GAS_BIZ':'2026年前三季度各月销气量趋势','GAS_AR':'2026年前三季度各月月末应收余额趋势','GAS_SAFE':'2026年前三季度各月安检覆盖率趋势'}[code]
  clarify={'GAS_BIZ':'计算超标供销差前，请先确认采用每个中心的演示阈值还是另行指定的正式阈值','GAS_AR':'算回收率之前，请先确认按当月还是年累计期间','GAS_SAFE':'算隐患闭环率之前，请先确认按当月新发现还是截至日全部工单'}[code]
  cases=[dict(case_type=t,question_text=q,expected_focus=f,expected_intent=i) for t,q,f,i in [('summary',queries[0]['question'],'限定问题时间和组织，单位正确，先经过AI，数值与PG独立查询一致','generate_sql'),('detail',detail,'保持组织过滤和明细粒度，不能把汇总桶当真实客户或重复累加管段里程','generate_sql'),('trend',trend,'按月分别计算，比例重算分子分母，应收余额不能跨月相加','generate_sql'),('confirmation',clarify,'按用户要求确认统计范围后再生成SQL，不擅自采用其他口径','requires_confirmation')]]
  synonyms=list(dict.fromkeys(ds['synonyms']+[m['label'] for m in metrics]))
  out.append(dict(code=code,name=ds['name'],synonyms=synonyms,regression_cases=cases,views=views,rules=rules,content=content,metrics=metrics,prompts=prompts,queries=queries))
 return out
