"""Create view DDL, field dictionary and dataset catalog from the validated model."""
import json
from pathlib import Path
from generate_demo import ROOT, save, TREE, VERSION

LABELS = dict(
    business_key="业务唯一键", month="月份", org_id="组织编码", org_name="组织名称", org_path="组织编码路径",
    branch_id="分公司编码", branch_name="分公司名称", center_id="服务中心编码", data_version="模拟版本",
    parent_id="上级组织编码", org_level="组织层级", org_name_path="组织名称路径", sales_enabled="是否有销售职责",
    user_type="客户类型", volume_m3="销气量_方", price_yuan_m3="销售均价_元每方",
    theoretical_revenue_yuan="理论量价收入_元", revenue_yuan="账单销气收入_元",
    audit_difference_yuan="量价稽核差异_元", actual_meter_m3="实抄量_方", estimated_meter_m3="估抄量_方",
    tax_basis="税口径", exception_code="预置异常编号", source="气源", inlet_m3="边界入口气量_方",
    purchase_price_yuan_m3="采购均价_元每方", purchase_cost_yuan="采购成本_元",
    loss_threshold="演示供销差阈值_小数", measurement_basis="计量依据", allocation_basis="成本分摊依据",
    installation_revenue_yuan="安装工程收入_元", installation_cost_yuan="安装工程直接成本_元",
    value_added_revenue_yuan="增值收入_元", value_added_cost_yuan="增值直接成本_元",
    distribution_cost_yuan="配气成本_元", admin_expense_yuan="管理费用_元", finance_expense_yuan="财务费用_元",
    impairment_yuan="当期减值费用_元", pretax_profit_target_yuan="模拟税前利润目标_元",
    customer_id="模拟客户编码", customer_name="模拟客户名称", object_kind="客户对象类型",
    opening_yuan="期初应收_元", billed_yuan="本期应收_元", collected_yuan="本期回款_元",
    adjustment_yuan="应收调整_元", closing_yuan="期末应收_元", provision_yuan="期末计提余额_元",
    aging_0_30_yuan="账龄0至30天_元", aging_31_90_yuan="账龄31至90天_元",
    aging_91_180_yuan="账龄91至180天_元", aging_181_365_yuan="账龄181至365天_元",
    aging_365_plus_yuan="账龄超过365天_元", collection_status="催收状态", aging_basis="账龄生成口径",
    opening_users="期初户数", applied_users="报装户数", connected_users="新增通气户数", churn_users="销户数",
    ending_users="期末户数", bottle_conversion_users="瓶改管户数", potential_users="潜在可接入户数",
    due_inspect="当月应检户数", inspected="当月已检户数", not_at_home="到访不遇户数",
    three_piece_installed="当月三件套安装户数", emergency_total="抢修次数", emergency_on_time="及时到场次数",
    leak_count="泄漏次数", network_id="管段编号", pressure_level="压力等级", length_km="管段里程_公里",
    material="管材", laid_date="敷设日期", gis_loaded_date="GIS入库日期", hazard_id="隐患编号",
    found_date="发现日期", due_date="整改截止日期", completed_date="整改完成日期", severity="隐患级别",
    hazard_type="隐患类型", status="隐患状态", as_of_date="快照截止日期")
BASE_VIEWS = dict(gas_org="v_gas_org", gas_sales_monthly="v_gas_sales", gas_supply_monthly="v_gas_supply_sources",
                  gas_profit_monthly="v_gas_profit_inputs", gas_ar_monthly="v_gas_ar", gas_growth_monthly="v_gas_growth",
                  gas_safety_monthly="v_gas_safety", gas_network_assets="v_gas_network", gas_hazard_orders="v_gas_hazards")


def column_type(key, value):
    if key.endswith("_date"):
        return "date"
    if isinstance(value, int):
        return "bigint"
    if isinstance(value, float):
        return "numeric"
    return "text"


def main():
    tables = json.loads((ROOT/"generated/model.json").read_text())
    ddl, fields, schemas = [], [], {}
    for name, rows in tables.items():
        cols = []
        for key, value in rows[0].items():
            typ = column_type(key, value)
            expression = f"NULLIF(fields->>'{key}', '')" if typ != "text" else f"fields->>'{key}'"
            if typ == "date":
                # Bitable date fields are milliseconds; local seed and CSV use ISO dates.
                expression = (f"CASE WHEN fields->>'{key}' ~ '^[0-9]{{13}}$' "
                              f"THEN (to_timestamp((fields->>'{key}')::numeric/1000) AT TIME ZONE 'Asia/Shanghai')::date "
                              f"ELSE NULLIF(fields->>'{key}', '')::date END")
            cast = "numeric::bigint" if typ == "bigint" else typ
            cols.append(f'  ({expression})::{cast} AS "{key}"')
            fields.append(dict(csv=name+".csv", view=BASE_VIEWS[name], field=key, type=typ,
                               chinese=LABELS[key], required=key in {"business_key","org_id","org_path"}))
        cols += ['  fields->>\'org_id\' AS "组织编码"', '  fields->>\'org_path\' AS "组织编码路径"']
        view_sql = f'CREATE OR REPLACE VIEW {BASE_VIEWS[name]} AS\nSELECT\n' + ',\n'.join(cols) + f'\nFROM raw_{name};'
        ddl.append(view_sql)
        schemas[BASE_VIEWS[name]] = view_sql
    balance = """CREATE OR REPLACE VIEW v_gas_supply_balance AS
WITH s AS (
 SELECT month,center_id,branch_id,branch_name,SUM(volume_m3) AS sales_m3,
 SUM(revenue_yuan) AS sales_revenue_yuan,SUM(estimated_meter_m3) AS estimated_m3
 FROM v_gas_sales GROUP BY month,center_id,branch_id,branch_name
), p AS (
 SELECT month,org_id,org_name,org_path,SUM(inlet_m3) AS inlet_m3,
 SUM(purchase_cost_yuan) AS purchase_cost_yuan,MAX(loss_threshold) AS loss_threshold
 FROM v_gas_supply_sources GROUP BY month,org_id,org_name,org_path
)
SELECT p.*,s.branch_id,s.branch_name,s.sales_m3,s.sales_revenue_yuan,s.estimated_m3,
 p.inlet_m3-s.sales_m3 AS loss_m3,
 (p.inlet_m3-s.sales_m3)/NULLIF(p.inlet_m3,0) AS loss_rate,
 p.org_id AS "组织编码",p.org_path AS "组织编码路径"
FROM p JOIN s ON p.month=s.month AND p.org_id=s.center_id;"""
    profit = """CREATE OR REPLACE VIEW v_gas_profit AS
SELECT f.*,COALESCE(b.sales_m3,0) AS sales_m3,
 COALESCE(b.sales_revenue_yuan,0) AS sales_revenue_yuan,
 COALESCE(b.purchase_cost_yuan,0) AS purchase_cost_yuan,
 COALESCE(b.sales_revenue_yuan,0)+f.installation_revenue_yuan+f.value_added_revenue_yuan AS total_revenue_yuan,
 COALESCE(b.sales_revenue_yuan,0)+f.installation_revenue_yuan+f.value_added_revenue_yuan
 -COALESCE(b.purchase_cost_yuan,0)-f.installation_cost_yuan-f.value_added_cost_yuan
 -f.distribution_cost_yuan-f.admin_expense_yuan-f.finance_expense_yuan-f.impairment_yuan AS pretax_profit_yuan
FROM v_gas_profit_inputs f LEFT JOIN v_gas_supply_balance b ON f.month=b.month AND f.org_id=b.org_id;"""
    summary = """CREATE OR REPLACE VIEW v_gas_ar_summary AS
SELECT month,org_id,org_name,org_path,branch_id,branch_name,user_type,
 SUM(opening_yuan) AS opening_yuan,SUM(billed_yuan) AS billed_yuan,SUM(collected_yuan) AS collected_yuan,
 SUM(closing_yuan) AS closing_yuan,SUM(provision_yuan) AS provision_yuan,
 SUM(aging_181_365_yuan+aging_365_plus_yuan) AS aging_over_180_yuan,
 org_id AS "组织编码",org_path AS "组织编码路径"
FROM v_gas_ar GROUP BY month,org_id,org_name,org_path,branch_id,branch_name,user_type;"""
    for view, sql in [("v_gas_supply_balance",balance),("v_gas_profit",profit),("v_gas_ar_summary",summary)]:
        ddl.append(sql)
        schemas[view] = sql
    (ROOT/"generated/views.sql").write_text('\n\n'.join(ddl)+'\n')
    save(ROOT/"generated/field_dictionary.json", fields)
    header = "# 飞书字段字典\n\n数据均为虚构。数量单位方，金额元，比例用 0–1 小数。月份和组织编码设文本，日期设日期，数值列设数字。\n\n"
    for name in tables:
        header += f"## {name}.csv\n\n| 字段 | 中文含义 | 飞书类型 |\n|---|---|---|\n"
        for f in fields:
            if f["csv"] == name+".csv":
                header += f"| {f['field']} | {f['chinese']} | {dict(text='文本',bigint='数字',numeric='数字',date='日期')[f['type']]} |\n"
        header += "\n"
    (ROOT/"docs/08_字段字典与飞书类型.md").write_text(header)
    datasets = [
      dict(code="GAS_BIZ", name="江城燃气·经营与供销差", domain="燃气经营",
           tables=["v_gas_sales","v_gas_supply_sources","v_gas_supply_balance","v_gas_profit","v_gas_growth"],
           synonyms=["燃气经营","销气","供销差","燃气利润","燃气新增用户"],
           questions=[
             ("2026年9月各分公司销气量排名", "SELECT branch_name,SUM(volume_m3) AS 销气量_方 FROM v_gas_sales WHERE month='2026-09' GROUP BY branch_name ORDER BY 销气量_方 DESC"),
             ("2026年9月各分公司供销差率", "SELECT branch_name,(SUM(inlet_m3)-SUM(sales_m3))/NULLIF(SUM(inlet_m3),0) AS 供销差率 FROM v_gas_supply_balance WHERE month='2026-09' GROUP BY branch_name ORDER BY 供销差率 DESC"),
             ("2026年前三季度模拟税前利润是多少", "SELECT SUM(pretax_profit_yuan) AS 税前利润_元 FROM v_gas_profit WHERE month BETWEEN '2026-01' AND '2026-09'"),
             ("2026年9月居民和工商业销气收入各多少", "SELECT user_type,SUM(revenue_yuan) AS 销气收入_元 FROM v_gas_sales WHERE month='2026-09' GROUP BY user_type"),
             ("2026年9月哪个分公司估抄率最高", "SELECT branch_name,SUM(estimated_meter_m3)::numeric/NULLIF(SUM(volume_m3),0) AS 估抄率 FROM v_gas_sales WHERE month='2026-09' GROUP BY branch_name ORDER BY 估抄率 DESC"),
             ("2026年9月各分公司新增通气多少户", "SELECT branch_name,SUM(connected_users) AS 新增通气户数 FROM v_gas_growth WHERE month='2026-09' GROUP BY branch_name"),
           ], deep=["2026年三季度利润相较去年同期为何变化？拆解量价、采购、损耗和费用贡献", "居民每方提价0.1元，在销量不变假设下2026年前三季度可增收多少？"]),
      dict(code="GAS_AR", name="江城燃气·应收回款与稽核", domain="燃气财务",
           tables=["v_gas_ar","v_gas_ar_summary","v_gas_sales"], synonyms=["燃气欠费","燃气应收","账龄","回款","量价稽核"],
           questions=[
             ("2026年9月末应收余额是多少", "SELECT SUM(closing_yuan) AS 期末应收_元 FROM v_gas_ar WHERE month='2026-09'"),
             ("2026年9月欠费最多的十个模拟工商客户", "SELECT customer_name,closing_yuan FROM v_gas_ar WHERE month='2026-09' AND object_kind='模拟客户' ORDER BY closing_yuan DESC LIMIT 10"),
             ("2026年9月超过180天的应收有多少", "SELECT SUM(aging_181_365_yuan+aging_365_plus_yuan) AS 长账龄应收_元 FROM v_gas_ar WHERE month='2026-09'"),
             ("2026年9月各分公司气费回收率", "SELECT branch_name,SUM(collected_yuan)/NULLIF(SUM(billed_yuan),0) AS 回收率 FROM v_gas_ar WHERE month='2026-09' GROUP BY branch_name"),
             ("2026年9月重点催收的客户有哪些", "SELECT customer_name,closing_yuan,collection_status FROM v_gas_ar WHERE month='2026-09' AND collection_status='重点催收'"),
             ("哪些月份账单收入与量价收入存在差异", "SELECT month,branch_name,SUM(audit_difference_yuan) AS 稽核差异_元 FROM v_gas_sales GROUP BY month,branch_name HAVING SUM(audit_difference_yuan)<>0"),
           ],deep=["沙湖应收恶化是哪些客户和账龄推动的？给出证据和催收建议", "按1%、3%、10%、30%、70%的演示账龄计提比例复核最新月计提是否充分"]),
      dict(code="GAS_SAFE", name="江城燃气·安全与管网治理", domain="燃气安全",
           tables=["v_gas_safety","v_gas_hazards","v_gas_network"], synonyms=["燃气安全","隐患","安检","管网","GIS","抢修"],
           questions=[
             ("2026年9月各分公司安检覆盖率", "SELECT branch_name,SUM(inspected)::numeric/NULLIF(SUM(due_inspect),0) AS 安检覆盖率 FROM v_gas_safety WHERE month='2026-09' GROUP BY branch_name"),
             ("截至2026年9月底有哪些超期未闭环隐患", "SELECT hazard_id,org_name,hazard_type,due_date FROM v_gas_hazards WHERE found_date<='2026-09-30' AND due_date<'2026-09-30' AND (completed_date IS NULL OR completed_date>'2026-09-30')"),
             ("2026年9月各分公司抢修及时率", "SELECT branch_name,SUM(emergency_on_time)::numeric/NULLIF(SUM(emergency_total),0) AS 抢修及时率 FROM v_gas_safety WHERE month='2026-09' GROUP BY branch_name"),
             ("2026年9月到访不遇还有多少户", "SELECT SUM(not_at_home) AS 到访不遇户数 FROM v_gas_safety WHERE month='2026-09'"),
             ("截至2026年9月GIS入库里程占比多少", "SELECT SUM(CASE WHEN gis_loaded_date<='2026-09-30' THEN length_km ELSE 0 END)/NULLIF(SUM(length_km),0) AS GIS入库率 FROM v_gas_network WHERE laid_date<='2026-09-30'"),
             ("沙湖分公司有多少公里超过20年的老旧管网", "SELECT SUM(length_km) AS 老旧管网_公里 FROM v_gas_network WHERE branch_id='SHAHU' AND laid_date<='2006-09-30'"),
           ],deep=["沙湖哪些网格应优先治理？并行检查隐患、管龄、安检覆盖和抢修", "未闭环重大隐患如何安排整改优先级？依据工单截止日和资产信息解释"]),
    ]
    for ds in datasets:
        ds["tables"] = list(dict.fromkeys(ds["tables"] + ["v_gas_org"]))
        ds["schema_definition"] = {t:schemas[t] for t in ds["tables"]}
    save(ROOT/"generated/datasets.json", datasets)
    print("Prepared 12 views, field dictionary, 3 datasets, 18 golden questions and 6 deep questions")


if __name__ == "__main__":
    main()
