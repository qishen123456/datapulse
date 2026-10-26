"""Curated gas semantics tied to the current warehouse, not generated answers."""
from knowledge_assets import bundle, GRAINS
VERSION='gas-semantics-20261025'
GRAINS['v_gas_growth']='一行=月份×销售服务中心×客户类型；10个服务中心×4类×33个月=1320行。org_id为中心编码，不能按网格下钻或与网格事实明细直连。'

# canonical term, actual spoken aliases, definition / caveat
TERMS={
'GAS_BIZ':[
('销气量','售气量|销售气量|卖了多少气','已计入销售统计的气量；v_gas_sales.volume_m3，原始单位方，不是采购入口量。'),
('销气收入','售气收入|气费销售额|卖气收入','v_gas_sales.revenue_yuan，单位元；与本期回款、期末应收不同。'),
('加权销气均价','平均售气价|每方卖价|平均气价','SUM(revenue_yuan)/SUM(volume_m3)，元/方；采购均价需另用采购成本/入口量。'),
('估抄率','估表率|估算抄表占比|估抄气量占比','SUM(estimated_meter_m3)/SUM(volume_m3)；不是估抄户数占比。'),
('实抄量','实表气量|实际抄表气量','actual_meter_m3；与estimated_meter_m3之和为volume_m3。'),
('边界入口气量','进气量|入口量|采购气量','v_gas_supply_balance.inlet_m3；组织边界计量，不能直接叫终端用量。'),
('供销差率','购销差率|产销差率|气差率','(总入口量-总销气量)/总入口量；包括计量与抄表时差等可能因素，不能直接认定物理漏损。'),
('供销差量','气差量|购销差量','入口量减销气量，单位方；先按同月同中心对齐。'),
('购气均价','采购均价|平均采购单价','SUM(purchase_cost_yuan)/SUM(inlet_m3)，元/方；按气源金额气量加权。'),
('采购成本','买气成本|购气支出','采购成本，不包含全部经营费用，不能等同总成本。'),
('模拟税前利润','税前利润|利润总额','v_gas_profit.pretax_profit_yuan；无所得税字段，不可答税后净利润。'),
('新增通气户数','新开通户数|新接通用户|新装通气','connected_users；与报装applied_users不同。'),
('报装户数','申请接气户数|新增报装','applied_users，为申请量，不能当已通气。'),
('期末户数','在用用户数|月末用户数','ending_users，为月末快照，不跨月累加。'),
('销气环比','销售环比|比上月气量','本月与紧邻上一自然月同范围气量比较；同时给差量和比例。'),
('同期间同比','同期增幅|气量同比','同月比较上年同月；2026年前三季度只能与2025年1至9月比较。'),
],
'GAS_AR':[
('期末应收','月末欠费|应收余额|还欠多少气费','closing_yuan，月末余额；不是本月账单或期间总欠费。'),
('期初应收','上期结转欠费|月初应收','opening_yuan，与上月期末按同一customer_id衔接。'),
('本期应收','本月出账金额|当期气费账单','billed_yuan，期间新增应收，不是余额。'),
('本期回款','实收气费|到账气费|收回气费','collected_yuan，包括历史欠款回收；并非只收当月账单。'),
('气费回收率','收缴率|回款率|气费实收率','期间总回款/期间总出账，可能超过100%；不是当期发票逐单回收率。'),
('长账龄应收','半年以上欠费|超过180天欠款','aging_181_365_yuan+aging_365_plus_yuan；月末快照。'),
('一年以上应收','365天以上欠费|超一年欠款','aging_365_plus_yuan；按出账日至快照日计龄，不等同合同逾期。'),
('账龄分布','欠费年龄结构|应收分层','0–30、31–90、91–180、181–365、365天以上五档。'),
('逾期天数','超期欠费天数|合同到期天数','缺逐笔合同到期日，不能把账龄直接称逾期天数；需澄清。'),
('演示计提余额','应收计提|坏账准备演示','provision_yuan；1/3/10/30/70%为演示假设，不作为企业正式会计政策。'),
('稽核差异字段','系统稽核差异|登记稽核金额','audit_difference_yuan为已登记差异；可与收入减理论收入不一致，需分别展示核验。'),
('重算量价差异','账单与理论差额|重新核算气费','revenue_yuan-theoretical_revenue_yuan；不能用四舍五入均价反推。'),
('工商客户名单','欠费企业名单|欠费大户','仅object_kind=模拟客户；居民与公共机构汇总对象不得当企业。'),
('应收滚动校验','应收勾稽|收支滚动平衡','期初+出账-回款+调整=期末；按对象逐月核对。'),
('欠费集中度','前十大户欠费占比|头部应收占比','同月同范围、同对象类型下TopN余额/总余额，明确是否只看工商客户。'),
('账龄迁移','欠款迁徙|账龄滚动','可比较同一customer_id各月账龄余额；缺发票ID，不能证明逐张发票迁徙。'),
],
'GAS_SAFE':[
('安检覆盖率','入户安检率|安检完成率|入户检查完成率','SUM(inspected)/SUM(due_inspect)，不是相邻网格比例均值。'),
('应检户次','计划安检量|应入户数量','due_inspect，月度计划过程计数，不能当全部燃气用户。'),
('已检户次','完成安检量|已入户数量','inspected，月度已完成过程计数。'),
('到访不遇户次','上门无人|入户不遇|到访未遇','not_at_home为当月过程计数，不代表去重客户或历史待复访存量。'),
('当月三件套安装户数','三件套新增安装|三件套装了多少户','three_piece_installed为当月计数；无累计已装户基数，不能答三件套普及率。'),
('抢修及时率','及时处置率|应急到场及时率','SUM(emergency_on_time)/SUM(emergency_total)，未提供分钟级到场时长。'),
('泄漏次数','漏气事件数|燃气泄漏事件','leak_count为当月次数，不能自动判定严重程度。'),
('每千公里泄漏次数','管网泄漏强度|千公里漏气次数','期间泄漏次数/截至日管网公里×1000，单位次/千公里，不是百分比。'),
('管网里程','管线长度|燃气管道公里数','SUM(length_km)，按laid_date<=截止日筛选；不同工单关联同管段不得重复累加。'),
('GIS入库率','GIS覆盖率|管网上图率|管线入图比例','截至日已GIS入库里程/有效总里程，采用里程口径；若问管段数比例须另算。'),
('未入库管段','GIS缺口|未上图管线','gis_loaded_date为空或晚于截止日，且laid_date不晚于截止日。'),
('老旧管网','超20年管线|二十年以上管道','按用户截止日减20年，筛laid_date早于阈值；“超过”与“满20年”边界需说明。'),
('未闭环隐患','未完成整改|未销项工单','发现日<=截止日，完成日为空或>截止日；不能直接用当前status代替历史。'),
('超期未闭环隐患','逾期整改|超期未销项','未闭环且due_date<截止日；到期当日不算已超期。'),
('隐患闭环率','整改完成率|隐患销项率','需要明确截至日全部发现工单还是当期新发现工单，分母不同。'),
('重大隐患','重大风险工单|重大隐患清单','severity=重大；不把一般工单自行上调等级，无事故/伤亡字段。'),
]}

EXAMPLES={
'GAS_BIZ':[
('2026年9月各分公司销气量比8月增减多少',"WITH a AS (SELECT branch_id,branch_name,SUM(volume_m3) FILTER(WHERE month='2026-09') current_m3,SUM(volume_m3) FILTER(WHERE month='2026-08') previous_m3 FROM v_gas_sales WHERE month IN ('2026-08','2026-09') GROUP BY branch_id,branch_name) SELECT *,current_m3-previous_m3 AS 差量_方,(current_m3-previous_m3)::numeric/NULLIF(previous_m3,0) AS 环比 FROM a ORDER BY 差量_方"),
('临港分公司2026年8月和9月按客户类型看销气变化',"SELECT month,user_type,SUM(volume_m3) AS 销气量_方,SUM(revenue_yuan) AS 销气收入_元 FROM v_gas_sales WHERE branch_id='LINGANG' AND month IN ('2026-08','2026-09') GROUP BY month,user_type ORDER BY user_type,month"),
('2026年前三季度各分公司销气量同期间同比',"SELECT branch_name,SUM(volume_m3) FILTER(WHERE month BETWEEN '2025-01' AND '2025-09') AS 上年同期_方,SUM(volume_m3) FILTER(WHERE month BETWEEN '2026-01' AND '2026-09') AS 本年同期_方 FROM v_gas_sales WHERE month BETWEEN '2025-01' AND '2026-09' GROUP BY branch_name"),
('2026年9月滨江沿江营业所各网格估抄情况',"SELECT org_id,org_name,SUM(estimated_meter_m3) AS 估抄量_方,SUM(volume_m3) AS 销气量_方,SUM(estimated_meter_m3)::numeric/NULLIF(SUM(volume_m3),0) AS 估抄率 FROM v_gas_sales WHERE month='2026-09' AND center_id='BINJIANG-S1' GROUP BY org_id,org_name"),
('2026年9月各气源采购气量和加权均价',"SELECT source,SUM(inlet_m3) AS 采购量_方,SUM(purchase_cost_yuan) AS 采购成本_元,SUM(purchase_cost_yuan)/NULLIF(SUM(inlet_m3),0) AS 购气均价_元每方 FROM v_gas_supply_sources WHERE month='2026-09' GROUP BY source"),
('沙湖分公司2026年各月供销差量和供销差率',"SELECT month,SUM(inlet_m3) AS 入口_方,SUM(sales_m3) AS 销气_方,SUM(inlet_m3)-SUM(sales_m3) AS 差量_方,(SUM(inlet_m3)-SUM(sales_m3))/NULLIF(SUM(inlet_m3),0) AS 供销差率 FROM v_gas_supply_balance WHERE branch_id='SHAHU' AND month BETWEEN '2026-01' AND '2026-09' GROUP BY month ORDER BY month"),
('2026年9月各服务中心报装、通气和净增用户',"SELECT org_id,org_name,SUM(applied_users) AS 报装户数,SUM(connected_users) AS 通气户数,SUM(churn_users) AS 销户数,SUM(connected_users-churn_users) AS 净增户数 FROM v_gas_growth WHERE month='2026-09' GROUP BY org_id,org_name"),
('2026年9月各分公司每方采购与配气成本',"SELECT branch_name,SUM(sales_m3) AS 销气量_方,SUM(purchase_cost_yuan)/NULLIF(SUM(sales_m3),0) AS 每销气方采购成本,SUM(distribution_cost_yuan)/NULLIF(SUM(sales_m3),0) AS 每销气方配气成本 FROM v_gas_profit WHERE month='2026-09' GROUP BY branch_name"),
('2026年9月各分公司税前利润的收入与费用构成',"SELECT branch_name,SUM(sales_revenue_yuan) AS 销气收入,SUM(installation_revenue_yuan) AS 安装收入,SUM(value_added_revenue_yuan) AS 增值收入,SUM(purchase_cost_yuan) AS 采购成本,SUM(distribution_cost_yuan) AS 配气成本,SUM(admin_expense_yuan) AS 管理费用,SUM(finance_expense_yuan) AS 财务费用,SUM(impairment_yuan) AS 减值费用,SUM(pretax_profit_yuan) AS 模拟税前利润 FROM v_gas_profit WHERE month='2026-09' GROUP BY branch_name"),
('2026年10月销气量有数据吗',"SELECT month,SUM(volume_m3) AS 销气量_方 FROM v_gas_sales WHERE month='2026-10' GROUP BY month"),
],
'GAS_AR':[
('2026年9月末沙湖分公司欠费企业前十名',"SELECT customer_id,customer_name,org_name,closing_yuan,aging_365_plus_yuan FROM v_gas_ar WHERE month='2026-09' AND branch_id='SHAHU' AND object_kind='模拟客户' AND closing_yuan>0 ORDER BY closing_yuan DESC,customer_id LIMIT 10"),
('2026年9月末望江路服务网格应收账龄结构',"SELECT user_type,SUM(closing_yuan) AS 期末应收_元,SUM(aging_0_30_yuan) AS 三十天内_元,SUM(aging_31_90_yuan) AS 三十一至九十天_元,SUM(aging_91_180_yuan) AS 九十一至一百八十天_元,SUM(aging_181_365_yuan) AS 一百八十一至一年_元,SUM(aging_365_plus_yuan) AS 一年以上_元 FROM v_gas_ar WHERE month='2026-09' AND org_id='BINJIANG-S1-W1' GROUP BY user_type"),
('2026年前三季度各分公司累计气费回收率',"SELECT branch_name,SUM(billed_yuan) AS 期间出账_元,SUM(collected_yuan) AS 期间回款_元,SUM(collected_yuan)/NULLIF(SUM(billed_yuan),0) AS 累计回收率 FROM v_gas_ar WHERE month BETWEEN '2026-01' AND '2026-09' GROUP BY branch_name"),
('2026年各月应收滚动不平衡的对象',"SELECT month,customer_id,customer_name,opening_yuan,billed_yuan,collected_yuan,adjustment_yuan,closing_yuan,opening_yuan+billed_yuan-collected_yuan+adjustment_yuan-closing_yuan AS 差额_元 FROM v_gas_ar WHERE month BETWEEN '2026-01' AND '2026-09' AND ABS(opening_yuan+billed_yuan-collected_yuan+adjustment_yuan-closing_yuan)>0.01 ORDER BY month,customer_id"),
('望江路恒拓精密制造有限公司2026年应收余额趋势',"SELECT month,customer_id,customer_name,closing_yuan,aging_365_plus_yuan FROM v_gas_ar WHERE customer_id='DEMO-BINJIANG-S1-W1-工业-1' AND month BETWEEN '2026-01' AND '2026-09' ORDER BY month"),
('2026年9月末工商客户前十大欠费占比',"WITH a AS (SELECT customer_id,customer_name,closing_yuan,ROW_NUMBER() OVER(ORDER BY closing_yuan DESC,customer_id) rn FROM v_gas_ar WHERE month='2026-09' AND object_kind='模拟客户') SELECT SUM(closing_yuan) FILTER(WHERE rn<=10) AS 前十应收_元,SUM(closing_yuan) AS 工商总应收_元,SUM(closing_yuan) FILTER(WHERE rn<=10)/NULLIF(SUM(closing_yuan),0) AS 集中度 FROM a"),
('2026年9月末各分公司账龄五档与余额能否勾稽',"SELECT branch_name,SUM(closing_yuan) AS 应收余额_元,SUM(aging_0_30_yuan+aging_31_90_yuan+aging_91_180_yuan+aging_181_365_yuan+aging_365_plus_yuan) AS 账龄合计_元 FROM v_gas_ar WHERE month='2026-09' GROUP BY branch_name"),
('登记稽核差异与重算量价差异有哪些不一致',"SELECT month,org_id,org_name,user_type,audit_difference_yuan AS 登记差异_元,revenue_yuan-theoretical_revenue_yuan AS 重算差异_元 FROM v_gas_sales WHERE ABS(audit_difference_yuan-(revenue_yuan-theoretical_revenue_yuan))>0.01 ORDER BY month,org_id"),
('2026年9月按网格与客户类型核对出账和销售收入',"WITH a AS (SELECT org_id,user_type,SUM(billed_yuan) billed FROM v_gas_ar WHERE month='2026-09' GROUP BY org_id,user_type),b AS (SELECT org_id,user_type,SUM(revenue_yuan) revenue FROM v_gas_sales WHERE month='2026-09' GROUP BY org_id,user_type) SELECT a.org_id,a.user_type,billed,revenue,billed-revenue AS 差额_元 FROM a FULL JOIN b USING(org_id,user_type) ORDER BY a.org_id,a.user_type"),
('2026年10月末应收有记录吗',"SELECT month,SUM(closing_yuan) AS 期末应收_元 FROM v_gas_ar WHERE month='2026-10' GROUP BY month"),
],
'GAS_SAFE':[
('2026年9月各服务网格应检、实检和到访不遇',"SELECT org_id,org_name,due_inspect,inspected,not_at_home,inspected::numeric/NULLIF(due_inspect,0) AS 安检覆盖率 FROM v_gas_safety WHERE month='2026-09' ORDER BY branch_id,org_id"),
('截至2026年9月底GIS未入库管段按分公司汇总',"SELECT branch_name,COUNT(*) AS 未入库管段数,SUM(length_km) AS 未入库里程_公里 FROM v_gas_network WHERE laid_date<='2026-09-30' AND (gis_loaded_date IS NULL OR gis_loaded_date>'2026-09-30') GROUP BY branch_name"),
('截至2026年9月底各分公司超过20年的管网有多少',"SELECT branch_name,COUNT(*) AS 超二十年管段数,SUM(length_km) AS 超二十年里程_公里 FROM v_gas_network WHERE laid_date<'2006-09-30' GROUP BY branch_name"),
('截至2026年9月底各类隐患超期未闭环情况',"SELECT severity,hazard_type,COUNT(*) AS 超期未闭环工单数 FROM v_gas_hazards WHERE found_date<='2026-09-30' AND due_date<'2026-09-30' AND (completed_date IS NULL OR completed_date>'2026-09-30') GROUP BY severity,hazard_type"),
('东环干线运维班组截至2026年9月底有哪些未闭环隐患',"SELECT hazard_id,hazard_type,severity,found_date,due_date,network_id FROM v_gas_hazards WHERE org_id='GYSP-S1-W1' AND found_date<='2026-09-30' AND (completed_date IS NULL OR completed_date>'2026-09-30') ORDER BY due_date,hazard_id"),
('2026年9月新发现隐患截至月底闭环率',"SELECT branch_name,COUNT(*) AS 当月发现数,COUNT(*) FILTER(WHERE completed_date<='2026-09-30') AS 月底已闭环数,COUNT(*) FILTER(WHERE completed_date<='2026-09-30')::numeric/NULLIF(COUNT(*),0) AS 当月批次闭环率 FROM v_gas_hazards WHERE found_date BETWEEN '2026-09-01' AND '2026-09-30' GROUP BY branch_name"),
('截至2026年6月底与9月底未闭环隐患数对比',"SELECT t.cutoff,COUNT(h.hazard_id) AS 未闭环数 FROM (VALUES (DATE '2026-06-30'),(DATE '2026-09-30')) t(cutoff) LEFT JOIN v_gas_hazards h ON h.found_date<=t.cutoff AND (h.completed_date IS NULL OR h.completed_date>t.cutoff) GROUP BY t.cutoff ORDER BY t.cutoff"),
('截至2026年9月底关联隐患的管段去重里程',"SELECT n.branch_name,COUNT(*) AS 关联管段数,SUM(n.length_km) AS 去重里程_公里 FROM v_gas_network n WHERE n.laid_date<='2026-09-30' AND EXISTS(SELECT 1 FROM v_gas_hazards h WHERE h.network_id=n.network_id AND h.found_date<='2026-09-30') GROUP BY n.branch_name"),
('2026年9月高压输配的入户安检覆盖率',"SELECT branch_name,SUM(due_inspect) AS 应检户次,SUM(inspected) AS 实检户次,SUM(inspected)::numeric/NULLIF(SUM(due_inspect),0) AS 安检覆盖率 FROM v_gas_safety WHERE month='2026-09' AND branch_id='GYSP' GROUP BY branch_name"),
('截至2026年9月底按材质和压力等级看管网里程',"SELECT material,pressure_level,COUNT(*) AS 管段数,SUM(length_km) AS 里程_公里 FROM v_gas_network WHERE laid_date<='2026-09-30' GROUP BY material,pressure_level ORDER BY material,pressure_level"),
]}

DETAIL={
'GAS_BIZ':[
('指标选择与粒度','销售、估抄用网格×客户类型；采购气源用服务中心×气源；经营利润用服务中心；新增/期末用户用服务中心×客户类型。不同粒度不能强行下钻。'),
('环比与贡献拆解','先确认本月和上月记录齐备；差量=本月-上月，环比=差量/上月。分解各客户类型差量对分公司差量的贡献，分公司总差量为0时贡献率返回空；贡献率可大于100%或为负，不能截断。'),
('量价拆解','金额按实际收入统计；量影响可用(本期量-基期量)×基期加权均价，价影响用本期量×(本期均价-基期均价)，两项合计应等于收入差；注明这是选定分解顺序，不能混用采购单价。'),
('税前利润桥','优先利润汇总视图，分别列销气/安装/增值收入及采购/安装/增值/配气/管理/财务/减值费用；利润减少不等同销量减少。高压输配只承担运维费用，无销气记录。'),
('范围名称解析','滨江沿江营业所=BINJIANG-S1，望江路服务网格=BINJIANG-S1-W1。优先从v_gas_org解析精确名字及路径，再与服务端授权交集；公司名、中心名、网格名不能互相替代。'),
('场景与解释边界','临港工业用气、沙湖估抄与供销差可进行同月/相邻月取证；数据发生变化不自动证明停产、泄漏或舞弊。内部模拟设定必须标记为设定，不能冒充经营人员确认。'),
('不支持的追问','无天气、设备小时、企业产能、营销活动、所得税、居民逐户抄表记录；缺这些证据时可给后续取证建议，不能输出已验证因果或预测准确率。')],
'GAS_AR':[
('对象识别','单月120个统计对象，其中80个虚构工商企业、40个居民/公共机构汇总对象；总数不是实际用户数。object_kind只是类型标记，企业名无“模拟”后缀也仍是演示企业。'),
('改名后的企业过滤','望江路恒拓精密制造有限公司稳定customer_id为DEMO-BINJIANG-S1-W1-工业-1。用名称定位ID，再保持ID跨期比较，不能按“工业1号”猜ID。'),
('回收率口径','期间回款包含冲销历史欠款，可能超过期间出账；当期账单回收率需要逐笔账单分配，不得用当前数据替代。月均回收率与累计回收率不同，默认累计用总回款/总出账。'),
('账龄时间边界','账龄按出账批次到月末的天数分段，0–30/31–90/91–180/181–365/>365，不是客户注册年限。没有合同应付日，因此不能把365天以上直接叫逾期365天。'),
('稽核双轨核验','audit_difference_yuan为登记差异字段，收入减理论收入为可重算差异。两者应分别返回并指出不一致，禁止为了“守恒”直接修改源数或用登记值冒充已核算金额。原始audit_note目前不在v_gas_sales列中，不能生成查询该字段的SQL。'),
('销售应收核对','销售按月×网格×类型，应收明细需先聚合到同样粒度后再关联；三键缺一会重复。比较金额需保留差额，不能把差异行过滤掉后声称完全一致。'),
('风险报告表达','高余额、长账龄占比、连续欠费趋势可作催收优先级线索。无合同、催收履历、诉讼和信用评分，不能认定坏账或给出法律结论。'),
('勾稽与空值','逐客户检查期初+出账-回款+调整-期末，容差0.01元；五档账龄合计与余额同样检查。无异常行代表本轮检查未检出差异，不等于没有客户或账簿为0。')],
'GAS_SAFE':[
('入户与输配分工','高压输配GYSP纳入管网、隐患、泄漏、抢修范围；入户安检分母可为0，返回不适用/无应检计划，不能判0%且排名垫底。'),
('安检计数限制','应检、实检、到访不遇为月度过程计数，缺户ID与访问记录，不能推断去重户数、重复上门次数或拒检原因。三件套安装同理不能回答存量普及率。'),
('截至日与批次','“截至9月底闭环率”默认截至日全部已发现工单，若问9月整改则确认分母是9月新发现还是9月完成；两个指标不可混用。'),
('GIS两种比例','主口径按里程，分子是截至日已入库公里数；按管段数是另一个指标，应在标题写清。既没有入库日期也没有有效里程的记录需返回质量告警，不能默认为已入库。'),
('管龄与材质','管龄从laid_date到用户截止日；按材质/压力/片区分层后看老旧里程。钢管、老旧年限本身不等于存在泄漏或必须报废，无压力试验/腐蚀检测数据。'),
('工单与管段关联','工单network_id多对一管段。要统计涉及管段里程用EXISTS或先DISTINCT network_id；同时保留工单数与管段数，二者不必相等。'),
('整改优先级','可按既有重大等级、是否超期、超期天数排序；截至日超期天数=T-due_date。缺用户密度、事故后果和实时压力，不生成伪量化综合风险分。'),
('工作日与及时性','emergency_on_time是源系统已标注及时数量，缺到场分钟及SLA定义；可以计算源标注及时率，不能声称遵守某国家分钟标准。')],
}

def build(datasets, organizations):
    result=bundle(datasets)
    for asset in result:
        code=asset['code'];term_rows=[]
        for term,aliases,meaning in TERMS[code]:
            for alias in aliases.split('|'):
                term_rows.append(dict(alias=alias,canonical=term,definition=meaning,weight=4))
        # Canonical terms remain useful routing tokens, with a real definition alongside.
        for term,_,meaning in TERMS[code]:term_rows.append(dict(alias=term,canonical=term,definition=meaning,weight=5))
        asset['glossary']=term_rows
        asset['synonyms']=[r['alias'] for r in term_rows]
        asset['rules'] += [title+'：'+content for title,content in DETAIL[code]]
        asset['rules']=[r.replace('10个服务中心','10个服务中心').replace('80个模拟工商客户+40个居民/公益汇总桶','80个虚构工商企业+40个居民/公益汇总对象') for r in asset['rules']]
        names='\n'.join('- '+n['name']+'：'+n['id']+'；路径 '+' / '.join(n['path_names']) for n in organizations['nodes'])
        content=asset['content'].replace('gas-knowledge-20261022',VERSION).replace('一行=月份×销售网格×客户类型；户数为模拟汇总，期末户数不可跨月累加。',GRAINS['v_gas_growth'])
        content+='\n\n## 业务操作与解释规则\n'+'\n'.join('### '+title+'\n'+body for title,body in DETAIL[code])
        content+='\n\n## 术语词典\n'+'\n'.join('- '+term+'（'+aliases.replace('|','、')+'）：'+meaning for term,aliases,meaning in TERMS[code])
        content+='\n\n## 当前组织名与稳定编码\n'+names
        content+='\n\n## 时间与组织交付契约\n- 返回实际时间范围、授权范围、指标单位和原始粒度。缺上期数据时环比为空，不能把缺失补0。\n- 用户明确选择2026-10时按10月返回无记录；问“最新”先用MAX(month)。截至日问题不得越过2026-09-30推演工单未来状态。\n- 当前数据为演示，企业和片区名称均为虚构；旧会话名称可按稳定ID衔接，不作真实公司识别。'
        asset['content']=content
        for agent in asset['prompts']:
            # Each specialist gets a distinct responsibility and domain-specific checks.
            role={1:'先提取指标、组织层级、时间、粒度、比较基期。解析新组织名，不将行政区与业务网格混淆。只有口径真实有歧义才追问；允许依据授权全集回答。',2:'生成只读PostgreSQL查询。给出选表理由与聚合摘要，比例先加分子分母，快照只取期末。组织条件使用稳定编码与授权路径；禁止查询视图未暴露字段。',3:'核对SQL与实际字段、口径、分母、日期、组织层级、连接基数。登记稽核值与可重算值不一致应标数据质量问题；不能因样例SQL写法不同拒绝等价正确查询。',4:'首段直接回答本题数值和范围；报告明确事实、数据质量提示、待验证假设、行动建议。无查询证据不使用既定场景故事推因果。排名先说明指标和对象范围，不能对零分母做优劣结论。最大增量按绝对差值排序，最大增幅按变化率排序，二者不能混用；金额和气量换算先精确加总再四舍五入，正文近似值必须与后续精确值一致。仅365天以上账龄为0不能推断181天以上长账龄为0；TopN结论仅限所查TopN，不能外推全体。缺总里程分母时，未入库绝对里程最少不等于GIS入库进度最好；短账龄或低余额不能据此判信用风险极低，缺基准也不自行判指标达标。单月或单期间汇总不能声称连续趋势。'}[agent]
            asset['prompts'][agent]=f'知识版本{VERSION}。'+role+'\n'+ '\n'.join(asset['rules'])+'\n本域常见术语：'+'；'.join(t+'='+a.replace('|','/') for t,a,_ in TERMS[code])
        # Keep prior valid samples and add real user-facing questions using the new names.
        by_question={q['question']:q for q in asset['queries']}
        for question,query in EXAMPLES[code]:by_question[question]=dict(question=question,sql=query)
        corrected={
            '2026年前三季度各分公司销气量同期间同比': "WITH a AS (SELECT branch_name,SUM(volume_m3) FILTER(WHERE month BETWEEN '2025-01' AND '2025-09') p,SUM(volume_m3) FILTER(WHERE month BETWEEN '2026-01' AND '2026-09') c FROM v_gas_sales GROUP BY branch_name) SELECT branch_name,p AS 上年同期_方,c AS 本年同期_方,(c-p)::numeric/NULLIF(p,0) AS 同比 FROM a",
            '2026年9月居民和工商业销气收入各多少': "SELECT CASE WHEN user_type='居民' THEN '居民' ELSE '工商业' END AS 客户类别,SUM(revenue_yuan) AS 销气收入_元 FROM v_gas_sales WHERE month='2026-09' AND user_type IN ('居民','商业','工业') GROUP BY 1",
            '2026年9月哪个分公司估抄率最高': "SELECT branch_name,SUM(estimated_meter_m3)::numeric/NULLIF(SUM(volume_m3),0) AS 估抄率 FROM v_gas_sales WHERE month='2026-09' GROUP BY branch_name ORDER BY 估抄率 DESC LIMIT 1",
            '哪些月份账单收入与量价收入存在差异': "SELECT month,branch_name,SUM(revenue_yuan-theoretical_revenue_yuan) AS 重算量价差异_元 FROM v_gas_sales GROUP BY month,branch_name HAVING ABS(SUM(revenue_yuan-theoretical_revenue_yuan))>0.01",
            '2026年9月到访不遇还有多少户': "SELECT SUM(not_at_home) AS 当月到访不遇户次 FROM v_gas_safety WHERE month='2026-09'",
            '沙湖分公司有多少公里超过20年的老旧管网': "SELECT SUM(length_km) AS 老旧管网_公里 FROM v_gas_network WHERE branch_id='SHAHU' AND laid_date<'2006-09-30'",
        }
        for question,sql in corrected.items():
            if question in by_question:by_question[question]['sql']=sql
        asset['queries']=list(by_question.values())
        asset['common']=list(dict.fromkeys([q for q,_ in EXAMPLES[code]][:8]+[q['question'] for q in asset['queries']]))[:16]
        extra_cases=[
          ('same_period',EXAMPLES[code][0][0],'使用已声明视图，限定时间和组织；与EXPLAIN后实际查询结果对齐，不用缓存结论。','generate_sql'),
          ('new_org_name',EXAMPLES[code][1][0],'解析本轮新片区/组织名到稳定ID，不返回已废弃的第1/第2网格名称。','generate_sql'),
          ('empty_month','查询2026年10月本域核心指标','保留用户10月条件；应明确无记录，不能暗换9月或把空聚合标为零。','generate_sql'),
          ('unsupported',{'GAS_BIZ':'分析2026年9月销量下降与气温的因果关系','GAS_AR':'列出欠费企业逐张发票的合同逾期天数','GAS_SAFE':'2026年9月抢修平均到场分钟数'}[code],'说明缺失字段/证据；不编造天气、合同到期日或分钟级日志。','requires_confirmation'),
          ('permission','查看未授权分公司的所有明细','应由服务端组织授权过滤或拒绝，不能只在报告中提示权限；对比范围也必须校验。','generate_sql'),
          ('quality',EXAMPLES[code][-2][0],'核对真实分子分母、粒度和连接；数据质量差异保留，不用解释覆盖错误。','generate_sql'),
          ('entity_type',{'GAS_BIZ':'按网格下钻新增通气户数','GAS_AR':'居民汇总对象是不是单个欠费客户','GAS_SAFE':'高压输配安检覆盖率是0%吗'}[code],'识别不能下钻的服务中心粒度、汇总对象或零分母；解释不适用，不造数据。','requires_confirmation'),
          ('unit','用万元、万方或公里展示本域指标并标单位','只转换相应金额或气量字段，保留比例与计数单位；原始数值不得重复除万。','generate_sql'),
        ]
        asset['regression_cases'] += [dict(case_type=t,question_text=q,expected_focus=f,expected_intent=i) for t,q,f,i in extra_cases]
    return result
