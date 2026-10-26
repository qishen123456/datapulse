"""Reproducible gas demo model. JSON is the intermediate for CSV authoring.

Run: python3 gas-demo/scripts/generate_demo.py
All quantities are m³, all money is CNY. No external dependencies or real users.
"""
from __future__ import annotations

import calendar
import json
import math
from collections import defaultdict
from datetime import date, timedelta
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = "gas-demo-v1"
TREE = "gas_jc_tree"
D = Decimal


def money(value):
    return float(D(str(value)).quantize(D("0.01"), rounding=ROUND_HALF_UP))


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def generate():
    tables = defaultdict(list)
    orgs = {}

    def node(code, name, parent="", sales=True):
        ancestor = orgs.get(parent)
        row = dict(business_key=code, org_id=code, org_name=name, parent_id=parent,
                   org_level=ancestor["org_level"] + 1 if ancestor else 1,
                   org_path=(ancestor["org_path"] if ancestor else "") + code + "/",
                   org_name_path=(ancestor["org_name_path"] + "/" if ancestor else "") + name,
                   sales_enabled=int(sales), data_version=VERSION)
        orgs[code] = row
        tables["gas_org"].append(row)

    node("JC-GROUP", "江城燃气集团")
    branches = [("BINJIANG", "滨江", .22), ("SHAHU", "沙湖", .20),
                ("JINGKAI", "经开", .24), ("LINGANG", "临港", .15),
                ("GAOXIN", "高新", .19), ("GYSP", "高压输配", 0)]
    for code, name, share in branches:
        node(code, name + "分公司", "JC-GROUP", share > 0)
        for c in (1, 2):
            center = f"{code}-S{c}"
            node(center, f"{name}第{c}服务中心", code, share > 0)
            for g in (1, 2):
                node(f"{center}-W{g}", f"{name}{c}中心第{g}网格", center, share > 0)

    def scoped(code):
        n = orgs[code]
        path = n["org_path"].strip("/").split("/")
        return dict(org_id=code, org_name=n["org_name"], org_path=n["org_path"],
                    branch_id=path[1] if len(path) > 1 else code,
                    branch_name=orgs[path[1]]["org_name"] if len(path) > 1 else n["org_name"],
                    center_id=path[2] if len(path) > 2 else "", data_version=VERSION)

    months = [f"{y}-{m:02}" for y in (2024, 2025, 2026)
              for m in range(1, 13) if y != 2026 or m <= 9]
    types = [("居民", .49, 2.55), ("商业", .20, 3.60), ("工业", .30, 3.60), ("公益机构", .01, 2.58)]
    centers = [n for n in orgs if orgs[n]["org_level"] == 3]
    grids = [n for n in orgs if orgs[n]["org_level"] == 4]
    # Seasonal weights are normalized against all 12 months, even for partial 2026.
    seasonal = {t: [1 + (.28 if t == "居民" else .05) * math.cos((m-1)/12*2*math.pi)
                    for m in range(1, 13)] for t, _, _ in types}
    sales_by_center = defaultdict(list)
    sales_by_grid = defaultdict(list)
    exceptions = []
    for month in months:
        year, m = map(int, month.split("-"))
        for branch, _, branch_share in branches:
            if not branch_share:
                continue
            for c in (1, 2):
                for g in (1, 2):
                    code = f"{branch}-S{c}-W{g}"
                    for typ, share, price in types:
                        volume = round(1_850_000_000 * 1.03 ** (year-2024) * share * branch_share / 4
                                       * seasonal[typ][m-1] / sum(seasonal[typ]))
                        theoretical = money(D(volume) * D(str(price)))
                        anomaly = month == "2025-08" and code == "SHAHU-S1-W1" and typ == "商业"
                        difference = 80000.0 if anomaly else 0.0
                        estimated = round(volume * (.12 if branch == "SHAHU" else .025))
                        row = dict(business_key=f"{month}:{code}:{typ}", month=month, **scoped(code),
                                   user_type=typ, volume_m3=volume, price_yuan_m3=price,
                                   theoretical_revenue_yuan=theoretical, revenue_yuan=money(theoretical+difference),
                                   audit_difference_yuan=difference, actual_meter_m3=volume-estimated,
                                   estimated_meter_m3=estimated, tax_basis="不含税演示口径",
                                   exception_code="AUDIT_PRICE_01" if anomaly else "")
                        tables["gas_sales_monthly"].append(row)
                        sales_by_center[(month, f"{branch}-S{c}")].append(row)
                        sales_by_grid[(month, code)].append(row)
                        if anomaly:
                            exceptions.append(dict(code="AUDIT_PRICE_01", table="gas_sales_monthly",
                                                   business_key=row["business_key"], expected_difference_yuan=difference,
                                                   explanation="模拟账单录入差异；不是计价公式错误"))

    loss_rates = dict(BINJIANG=.032, SHAHU=.058, JINGKAI=.038, LINGANG=.042, GAOXIN=.031)
    for month in months:
        year, m = map(int, month.split("-"))
        for center in centers:
            branch = orgs[center]["parent_id"]
            sales = sales_by_center[(month, center)]
            volume = sum(r["volume_m3"] for r in sales)
            rate = loss_rates.get(branch, 0)
            inlet = round(volume / (1-rate)) if volume else 0
            threshold = .045 if branch in {"LINGANG", "GAOXIN"} else .035
            if volume:
                lng_share = .20 if m in (1, 2, 12) else .10
                source_shares = [("长协管道气", .80-lng_share, 0), ("气源干网", .20, .02), ("LNG现货", lng_share, .18)]
                remaining = inlet
                for i, (source, share, extra) in enumerate(source_shares):
                    source_volume = remaining if i == 2 else round(inlet*share)
                    remaining -= source_volume
                    price = money(2.45 + {2024: 0, 2025: -.02, 2026: .04}[year]
                                  + .05*math.cos((m-1)/12*2*math.pi) + extra)
                    tables["gas_supply_monthly"].append(dict(
                        business_key=f"{month}:{center}:{source}", month=month, **scoped(center), source=source,
                        inlet_m3=source_volume, purchase_price_yuan_m3=price,
                        purchase_cost_yuan=money(D(source_volume)*D(str(price))), loss_threshold=threshold,
                        measurement_basis="模拟组织边界入口计量", allocation_basis="采购价按气源合同分摊；不重复计管输费"))
            # All 12 centers have expenses. GYSP's transport cost is retained in its own rows.
            weight = dict((b, s) for b, _, s in branches)[branch] / 2 if branch != "GYSP" else 0
            allocation = .95 * weight if branch != "GYSP" else .025
            tables["gas_profit_monthly"].append(dict(
                business_key=f"{month}:{center}", month=month, **scoped(center),
                installation_revenue_yuan=money(50_000_000*allocation),
                installation_cost_yuan=money(29_166_666.67*allocation),
                value_added_revenue_yuan=money(5_000_000*allocation),
                value_added_cost_yuan=money(833_333.33*allocation),
                distribution_cost_yuan=money(volume*.55), admin_expense_yuan=money(15_000_000*allocation),
                finance_expense_yuan=money(4_000_000*allocation), impairment_yuan=money(5_000_000*allocation),
                pretax_profit_target_yuan=money(-5_000_000*allocation)))

    # 120 objects = 20 sales grids × (resident/public buckets + 4 named business customers).
    # Every sales bill is assigned once, so receivable bills reconcile to all sales.
    ar_state = {}
    user_state = {}
    for mi, month in enumerate(months):
        for grid in grids:
            for sales in sales_by_grid[(month, grid)]:
                typ = sales["user_type"]
                count = 2 if typ in {"商业", "工业"} else 1
                left = sales["revenue_yuan"]
                for k in range(count):
                    customer_id = f"DEMO-{grid}-{typ}-{k+1}"
                    billed = left if k == count-1 else money(sales["revenue_yuan"]/count)
                    left = money(left-billed)
                    risk = grid.startswith("SHAHU") and typ == "工业" and k == 0
                    opening = ar_state.get(customer_id, money(billed*(.9 if risk else .15)))
                    collection = money(billed*(.91 if risk else .995 if typ == "居民" else .98))
                    closing = money(D(str(opening))+D(str(billed))-D(str(collection)))
                    ar_state[customer_id] = closing
                    weights = [.25, .18, .17, .20, .20] if risk else [.75, .15, .06, .03, .01]
                    age = [money(closing*w) for w in weights[:4]]
                    age.append(money(closing-sum(age)))
                    provision = money(sum(v*w for v, w in zip(age, [.01, .03, .10, .30, .70])))
                    tables["gas_ar_monthly"].append(dict(
                        business_key=f"{month}:{customer_id}", month=month, **scoped(grid), customer_id=customer_id,
                        customer_name=(f"{orgs[grid]['org_name']}{typ}汇总桶" if typ in {"居民", "公益机构"}
                                       else f"模拟{orgs[grid]['org_name']}{typ}客户{k+1}"),
                        object_kind="汇总桶" if typ in {"居民", "公益机构"} else "模拟客户",
                        user_type=typ, opening_yuan=opening, billed_yuan=billed, collected_yuan=collection,
                        adjustment_yuan=0, closing_yuan=closing, aging_0_30_yuan=age[0], aging_31_90_yuan=age[1],
                        aging_91_180_yuan=age[2], aging_181_365_yuan=age[3], aging_365_plus_yuan=age[4],
                        provision_yuan=provision, collection_status="重点催收" if risk else "正常",
                        aging_basis="模拟月末账龄分布；非逐张发票迁徙"))
        for center in centers:
            if not orgs[center]["sales_enabled"]:
                continue
            branch = orgs[center]["parent_id"]
            weight = dict((b,s) for b,_,s in branches)[branch]/2
            for typ, _, _ in types:
                key = (center, typ)
                base = 3_100_000 if typ == "居民" else 18000 * {"商业": .6, "工业": .35, "公益机构": .05}[typ]
                opening = user_state.get(key, round(base*weight))
                applied = round((900 if typ == "居民" else 8)*weight*10)
                connected = round(applied*.85)
                churn = round(connected*.1)
                closing = opening+connected-churn
                user_state[key] = closing
                tables["gas_growth_monthly"].append(dict(
                    business_key=f"{month}:{center}:{typ}", month=month, **scoped(center), user_type=typ,
                    opening_users=opening, applied_users=applied, connected_users=connected, churn_users=churn,
                    ending_users=closing, bottle_conversion_users=round(connected*.2) if typ == "居民" else 0,
                    potential_users=round(base*weight*1.25+mi*applied)))
        for gi, grid in enumerate(grids):
            due = 1400 + gi*13
            inspected = round(due*(.85+mi*.003))
            emergency = 15+gi%9
            tables["gas_safety_monthly"].append(dict(
                business_key=f"{month}:{grid}", month=month, **scoped(grid), due_inspect=due,
                inspected=inspected, not_at_home=due-inspected, three_piece_installed=round(inspected*.65),
                emergency_total=emergency, emergency_on_time=emergency-(2 if grid.startswith("SHAHU") else 1),
                leak_count=3 if grid.startswith("SHAHU") else 1))

    # Exact total network length: 17000 km. Every asset maps to one grid.
    for gi, grid in enumerate(grids):
        for k in range(10):
            index = gi*10+k
            old = grid.startswith("SHAHU")
            length = 70.83 if index < 239 else 17000-70.83*239
            tables["gas_network_assets"].append(dict(
                business_key=f"PIPE-{index+1:04}", network_id=f"PIPE-{index+1:04}", **scoped(grid),
                pressure_level="高压" if grid.startswith("GYSP") else "中压" if k < 2 else "低压",
                length_km=money(length), material="钢管" if old or k < 2 else "PE",
                laid_date=f"{1998 if old else 2015+k%7}-06-01",
                gis_loaded_date="2023-12-01" if k < 6 else f"202{4 if k < 8 else 5}-09-01"))
    cutoff = date(2026, 9, 30)
    for i in range(120):
        grid = grids[i % len(grids)]
        found = date(2024, 1, 15)+timedelta(days=i*8)
        due = found+timedelta(days=30)
        overdue = i in {117, 118}
        if overdue:
            grid = "SHAHU-S1-W1" if i == 117 else "SHAHU-S2-W2"
        completed = "" if overdue else (found+timedelta(days=15)).isoformat()
        if completed and date.fromisoformat(completed) > cutoff:
            completed = ""
        asset = next(a for a in tables["gas_network_assets"] if a["org_id"] == grid)
        tables["gas_hazard_orders"].append(dict(
            business_key=f"HZ-{i+1:04}", hazard_id=f"HZ-{i+1:04}", **scoped(grid),
            network_id=asset["network_id"], found_date=found.isoformat(), due_date=due.isoformat(),
            completed_date=completed, severity="重大" if overdue else "一般",
            hazard_type="立管腐蚀" if i == 117 else "管线占压" if i == 118 else "阀门或连接点隐患",
            status="已闭环" if completed else "未闭环", as_of_date=cutoff.isoformat()))

    org_config = {"version": 1, "tree_types": [dict(id=TREE, code="GAS_JC", name="江城燃气组织树",
                  description="模拟数据唯一组织来源，43节点", enabled=True, sort_order=100)],
                  "nodes": [dict(id=r["org_id"], code=r["org_id"], name=r["org_name"],
                            parent_id=r["parent_id"], tree_type_id=TREE, enabled=True,
                            sort_order=i, level=r["org_level"],
                            path_ids=r["org_path"].strip("/").split("/"),
                            path_names=r["org_name_path"].split("/")) for i,r in enumerate(orgs.values())]}
    from realistic_scenarios import apply
    apply(tables, money)
    from business_names import apply_names
    apply_names(tables, org_config)
    return dict(tables), org_config, exceptions


def validate(tables, org_config, exceptions):
    """Independent assertions, including deliberate corruptions in test_generate_demo.py."""
    orgs = {r["org_id"]: r for r in tables["gas_org"]}
    assert len(orgs) == 43
    assert len({r["id"] for r in org_config["nodes"]}) == 43
    assert {r["id"] for r in org_config["nodes"]} == set(orgs)
    for n in org_config["nodes"]:
        o = orgs[n["id"]]
        assert n["parent_id"] == o["parent_id"]
        assert n["path_ids"] == o["org_path"].strip("/").split("/")
        assert len(n["path_ids"]) == o["org_level"]
    for name, rows in tables.items():
        assert len({r["business_key"] for r in rows}) == len(rows), name
        for r in rows:
            assert r["org_id"] in orgs, (name, r["org_id"])
            o = orgs[r["org_id"]]
            assert r["org_path"] == o["org_path"]
            assert r["org_name"] == o["org_name"]
            if o["parent_id"]:
                assert r["org_path"] == orgs[o["parent_id"]]["org_path"]+r["org_id"]+"/"
    annual = defaultdict(int)
    bills = defaultdict(float)
    for r in tables["gas_sales_monthly"]:
        assert orgs[r["org_id"]]["sales_enabled"]
        assert abs(r["theoretical_revenue_yuan"]-money(D(r["volume_m3"])*D(str(r["price_yuan_m3"])))) < .011
        assert abs(r["revenue_yuan"]-r["theoretical_revenue_yuan"]-r["audit_difference_yuan"]) < .011
        assert r["actual_meter_m3"]+r["estimated_meter_m3"] == r["volume_m3"]
        annual[r["month"][:4]] += r["volume_m3"]
        bills[(r["month"], r["org_id"], r["user_type"])] += r["revenue_yuan"]
    assert abs(annual["2024"]-1_850_000_000) < 100
    supply = defaultdict(float)
    for r in tables["gas_supply_monthly"]:
        assert orgs[r["org_id"]]["org_level"] == 3
        assert abs(r["purchase_cost_yuan"]-money(D(r["inlet_m3"])*D(str(r["purchase_price_yuan_m3"])))) < .011
        supply[(r["month"],r["org_id"])] += r["inlet_m3"]
    sales = defaultdict(float)
    for r in tables["gas_sales_monthly"]:
        sales[(r["month"],r["center_id"])]+=r["volume_m3"]
    for key, inlet in supply.items():
        branch = orgs[key[1]]["parent_id"]
        assert .005 < (inlet-sales[key])/inlet < .09
    state = {}
    ar_bills = defaultdict(float)
    for r in tables["gas_ar_monthly"]:
        assert abs(r["closing_yuan"]-(r["opening_yuan"]+r["billed_yuan"]-r["collected_yuan"]+r["adjustment_yuan"])) < .02
        assert abs(r["closing_yuan"]-sum(r[f"aging_{s}_yuan"] for s in ["0_30", "31_90", "91_180", "181_365", "365_plus"])) < .02
        if r["customer_id"] in state:
            assert r["opening_yuan"] == state[r["customer_id"]]
        state[r["customer_id"]] = r["closing_yuan"]
        ar_bills[(r["month"], r["org_id"], r["user_type"])] += r["billed_yuan"]
    assert set(bills) == set(ar_bills)
    assert all(abs(bills[k]-ar_bills[k]) < .02 for k in bills)
    assert abs(sum(r["length_km"] for r in tables["gas_network_assets"])-17000) < .01
    assets = {r["network_id"]:r for r in tables["gas_network_assets"]}
    for r in tables["gas_hazard_orders"]:
        assert assets[r["network_id"]]["org_id"] == r["org_id"]
    for r in tables["gas_growth_monthly"]:
        assert r["ending_users"] == r["opening_users"]+r["connected_users"]-r["churn_users"]
        assert r["ending_users"] <= r["potential_users"]
    assert sum(1 for r in tables["gas_sales_monthly"] if r["exception_code"]) == len(exceptions) == 1
    return {"status":"passed", "data_version":VERSION, "scenario_revision":"realism-v2", "organization_nodes":43,
            "rows":{k:len(v) for k,v in tables.items()}, "annual_sales_m3":dict(annual),
            "checks":["组织编码/名称/路径/父子关系", "业务主键唯一", "高压输配不落销售",
                      "年度气量锚点", "采购量价及组织供销差", "量价及稽核差异", "实抄估抄守恒", "应收滚动/账龄平衡",
                      "销售与应收账单勾稽", "用户数滚动", "管网里程及隐患组织关联"]}


def main():
    tables, org_config, exceptions = generate()
    report = validate(tables, org_config, exceptions)
    save(ROOT/"generated/model.json", tables)
    save(ROOT/"generated/organization_tree.json", org_config)
    save(ROOT/"generated/expected_exceptions.json", exceptions)
    save(ROOT/"generated/validation_report.json", report)
    save(ROOT/"generated/feishu_sync_templates.json", {"sync_configs":[dict(
        name=f"江城燃气·{name}", description="模拟数据；飞书接通前保持停用",
        target_table=f"raw_{name}", app_id="", app_secret="", base_id="", table_id="", view_id="",
        sync_mode="full", sync_frequency="60", is_active=False) for name in tables]})
    print(json.dumps(report, ensure_ascii=False))


if __name__ == "__main__":
    main()
