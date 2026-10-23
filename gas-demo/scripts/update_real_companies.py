#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新江城燃气应收客户名称为高度真实的知名企业全称，并同步更新 CSV、PG 数据库及评测资产。
严禁改动任何问数流程！
"""
import os
import sys
import csv
import json
from pathlib import Path
import psycopg2

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SCRIPTS_DIR = Path(__file__).resolve().parent
sys.path.append(str(SCRIPTS_DIR))

from realistic_companies import REAL_COMPANY_NAMES, get_real_customer_name

CSV_FILE = PROJECT_ROOT / "gas-demo" / "data" / "gas_ar_monthly.csv"

def update_csv():
    print(f"正在更新 CSV 文件: {CSV_FILE} ...")
    with open(CSV_FILE, "r", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = list(reader)

    # 找到 customer_id 和 customer_name 所在列索引
    cid_idx = header.index("customer_id")
    cname_idx = header.index("customer_name")
    aging_idx = header.index("aging_basis")

    updated_rows = []
    count = 0
    for row in rows:
        cid = row[cid_idx]
        old_name = row[cname_idx]
        new_name = get_real_customer_name(cid, old_name)
        if new_name != old_name:
            count += 1
            row[cname_idx] = new_name
        if "模拟月末出账批次" in row[aging_idx]:
            row[aging_idx] = "月末账单结算批次，先冲最早欠款；账龄按出账日至快照日，非逾期天数"
        updated_rows.append(row)

    with open(CSV_FILE, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(updated_rows)

    print(f"CSV 文件更新完成！共更新 {count} 行记录中的客户名称。")

def update_postgres():
    print("正在连接 PostgreSQL 更新 raw_gas_ar_monthly 底表 ...")
    conn = psycopg2.connect(
        host="127.0.0.1",
        port=5433,
        dbname="postgres",
        user="postgres",
        password="datapulse_password" if False else "6670326"
    )
    cur = conn.cursor()
    
    cur.execute("SELECT id, fields FROM raw_gas_ar_monthly")
    records = cur.fetchall()
    print(f"读取到 {len(records)} 行底表记录，正在批量应用真实企业名称...")
    
    update_tuples = []
    for rid, fields in records:
        cid = fields.get("customer_id")
        old_name = fields.get("customer_name", "")
        new_name = get_real_customer_name(cid, old_name)
        
        fields["customer_name"] = new_name
        if "模拟月末出账批次" in fields.get("aging_basis", ""):
            fields["aging_basis"] = "月末账单结算批次，先冲最早欠款；账龄按出账日至快照日，非逾期天数"
            
        update_tuples.append((json.dumps(fields, ensure_ascii=False), rid))

    # 批量更新
    from psycopg2.extras import execute_batch
    execute_batch(cur, "UPDATE raw_gas_ar_monthly SET fields = %s::jsonb WHERE id = %s", update_tuples, page_size=500)
    conn.commit()
    print("PostgreSQL 数据库更新提交成功！")
    
    # 验证视图输出
    cur.execute("SELECT customer_name, closing_yuan FROM v_gas_ar WHERE month='2026-09' AND object_kind='模拟客户' ORDER BY closing_yuan DESC LIMIT 5")
    print("=== 更新后 2026年9月欠费最高 TOP 5 真实客户 ===")
    for name, money in cur.fetchall():
        print(f"  {name}: {money:,.2f} 元")
        
    cur.close()
    conn.close()

def update_golden_results():
    golden_path = PROJECT_ROOT / "gas-demo" / "generated" / "golden_results.json"
    if not golden_path.exists():
        return
    print(f"正在同步金标资产: {golden_path} ...")
    with open(golden_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for item in data:
        for r in item.get("rows", []):
            if "customer_name" in r:
                # 遍历替换
                old = r["customer_name"]
                for cid, real in REAL_COMPANY_NAMES.items():
                    # 匹配规则
                    if "沙湖1中心第1网格工业客户1" in old or "沙湖1中心第1网格" in old and "精密制造" in old:
                        r["customer_name"] = REAL_COMPANY_NAMES["DEMO-SHAHU-S1-W1-工业-1"]
                    elif "沙湖1中心第2网格工业客户1" in old or "沙湖1中心第2网格" in old and "精密制造" in old:
                        r["customer_name"] = REAL_COMPANY_NAMES["DEMO-SHAHU-S1-W2-工业-1"]
                    elif "沙湖2中心第1网格工业客户1" in old or "沙湖2中心第1网格" in old and "精密制造" in old:
                        r["customer_name"] = REAL_COMPANY_NAMES["DEMO-SHAHU-S2-W1-工业-1"]
                    elif "沙湖2中心第2网格工业客户1" in old or "沙湖2中心第2网格" in old and "精密制造" in old:
                        r["customer_name"] = REAL_COMPANY_NAMES["DEMO-SHAHU-S2-W2-工业-1"]
                    elif "经开" in old:
                        r["customer_name"] = r["customer_name"].replace("（模拟）", "").replace("客户1", "有限公司").replace("客户2", "分厂")

    with open(golden_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("金标资产同步完成。")

if __name__ == '__main__':
    update_csv()
    update_postgres()
    update_golden_results()
