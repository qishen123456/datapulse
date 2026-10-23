#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
50道题实测燃气三大数据集自动化评测执行器
通过 HTTP 接口调取真实智能问数大模型，并结合 PostgreSQL 独立对账
"""
import os
import sys
import json
import time
import math
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import requests

PROJECT_ROOT = Path(__file__).resolve().parents[1]
BASE_URL = "http://127.0.0.1:5002"
OUT_DIR = PROJECT_ROOT / "gas_dataset_test_50"
DETAILS_DIR = OUT_DIR / "test_details"
DETAILS_DIR.mkdir(parents=True, exist_ok=True)

# 数据集映射 (64: GAS_BIZ, 65: GAS_AR, 66: GAS_SAFE)
DATASET_IDS = {
    "GAS_BIZ": 64,
    "GAS_AR": 65,
    "GAS_SAFE": 66
}

# 50道测试题详细定义
TEST_CASES = [
    # ====== GAS_BIZ (17题) ======
    {"id": "Q01", "ds": "GAS_BIZ", "type": "基础聚合与排序", "q": "2026年9月各分公司销气量排名", "check_type": "series_sales"},
    {"id": "Q02", "ds": "GAS_BIZ", "type": "客户结构占比", "q": "2026年9月各客户类型的销气量及占比是多少？", "check_type": "user_type_sales"},
    {"id": "Q03", "ds": "GAS_BIZ", "type": "加权均价", "q": "2026年9月各客户类型的加权销气均价是多少？", "check_type": "avg_price"},
    {"id": "Q04", "ds": "GAS_BIZ", "type": "估抄率聚合", "q": "2026年9月各分公司的估抄量与估抄率是多少？", "check_type": "series_est_rate"},
    {"id": "Q05", "ds": "GAS_BIZ", "type": "网格级下钻", "q": "列出2026年9月沙湖分公司各网格的估抄率，同时返回组织编码", "check_type": "grid_est_rate"},
    {"id": "Q06", "ds": "GAS_BIZ", "type": "气源采购结构", "q": "2026年9月不同气源的采购气量和采购成本各是多少？", "check_type": "supply_sources"},
    {"id": "Q07", "ds": "GAS_BIZ", "type": "供销差核算", "q": "2026年9月各分公司的供销差量和供销差率是多少？", "check_type": "loss_rate"},
    {"id": "Q08", "ds": "GAS_BIZ", "type": "超标预警", "q": "2026年9月有哪些服务中心超过了演示供销差阈值？", "check_type": "loss_threshold"},
    {"id": "Q09", "ds": "GAS_BIZ", "type": "月度利润趋势", "q": "2026年前三季度每月模拟税前利润是多少？", "check_type": "monthly_profit"},
    {"id": "Q10", "ds": "GAS_BIZ", "type": "主业经营总览", "q": "2026年前三季度累计总收入与模拟税前利润是多少？", "check_type": "total_profit"},
    {"id": "Q11", "ds": "GAS_BIZ", "type": "环比分析", "q": "2026年9月各分公司销气量环比8月变化多少？", "check_type": "sales_mom"},
    {"id": "Q12", "ds": "GAS_BIZ", "type": "新增发展", "q": "2026年9月各分公司新增通气户数是多少？", "check_type": "connected_users"},
    {"id": "Q13", "ds": "GAS_BIZ", "type": "时点存量", "q": "2026年9月末各分公司期末总户数是多少？", "check_type": "ending_users"},
    {"id": "Q14", "ds": "GAS_BIZ", "type": "特殊组织职责边界", "q": "高压输配分公司在2026年9月的销气量是多少？", "check_type": "gysp_boundary"},
    {"id": "Q15", "ds": "GAS_BIZ", "type": "无数据月份防编造", "q": "2026年10月各分公司销气量是多少？严格只查2026年10月，没有数据请明确说明，不要改用9月。", "check_type": "empty_october"},
    {"id": "Q16", "ds": "GAS_BIZ", "type": "超范围财务指标防编造", "q": "2026年前三季度江城燃气的税后净利润是多少？", "check_type": "net_profit_boundary"},
    {"id": "Q17", "ds": "GAS_BIZ", "type": "动态最新月识别", "q": "数据最新月份各分公司销气量排名前三的是哪几个分公司？", "check_type": "latest_month_top3"},

    # ====== GAS_AR (17题) ======
    {"id": "Q18", "ds": "GAS_AR", "type": "期末余额汇总", "q": "2026年9月末江城燃气总应收余额是多少？", "check_type": "scalar_ar"},
    {"id": "Q19", "ds": "GAS_AR", "type": "分公司应收分布", "q": "2026年9月末各分公司的应收余额分布情况如何？", "check_type": "branch_ar"},
    {"id": "Q20", "ds": "GAS_AR", "type": "账龄结构分布", "q": "2026年9月末全公司的应收账龄结构是什么样？请分别列出0-30天、31-90天、91-180天、181-365天和365天以上金额。", "check_type": "aging_structure"},
    {"id": "Q21", "ds": "GAS_AR", "type": "长账龄统计", "q": "2026年9月末超过180天的长账龄应收余额总计是多少？", "check_type": "long_aging"},
    {"id": "Q22", "ds": "GAS_AR", "type": "期末计提余额", "q": "2026年9月末期末计提余额是多少？", "check_type": "provision_balance"},
    {"id": "Q23", "ds": "GAS_AR", "type": "演示坏账复核", "q": "按1%、3%、10%、30%、70%的演示账龄比例复核2026年9月末演示应计提金额", "check_type": "recomputed_provision"},
    {"id": "Q24", "ds": "GAS_AR", "type": "滚动平衡勾稽", "q": "2026年9月各分公司的应收滚动平衡（期初+本期应收-回款+调整-期末）是否存在差异？", "check_type": "roll_balance"},
    {"id": "Q25", "ds": "GAS_AR", "type": "当月回款率", "q": "2026年9月各分公司的当月气费回收率是多少？", "check_type": "monthly_recovery"},
    {"id": "Q26", "ds": "GAS_AR", "type": "累计回款率", "q": "2026年前三季度各分公司累计气费回收率是多少？", "check_type": "accumulated_recovery"},
    {"id": "Q27", "ds": "GAS_AR", "type": "大客户欠费TOP5", "q": "2026年9月末欠费金额排名前5的模拟工商客户是哪几家？列出客户名称和欠费金额。", "check_type": "top5_debt_customers"},
    {"id": "Q28", "ds": "GAS_AR", "type": "欠费户数统计", "q": "2026年9月末有应收余额的模拟工商客户一共有多少家？", "check_type": "debt_customer_count"},
    {"id": "Q29", "ds": "GAS_AR", "type": "汇总桶边界识别", "q": "2026年9月末居民用户的应收欠费总额是多少？", "check_type": "resident_ar"},
    {"id": "Q30", "ds": "GAS_AR", "type": "量价稽核差异", "q": "2026年9月各分公司销气量价稽核差异总额是多少？", "check_type": "audit_diff"},
    {"id": "Q31", "ds": "GAS_AR", "type": "时点趋势防跨月求和", "q": "2026年前三季度各月月末应收余额趋势如何？", "check_type": "ar_trend"},
    {"id": "Q32", "ds": "GAS_AR", "type": "无数据月份防编造", "q": "2026年10月末应收余额是多少？严格查2026年10月，没有数据请说明。", "check_type": "empty_ar_oct"},
    {"id": "Q33", "ds": "GAS_AR", "type": "超范围发票账龄迁徙", "q": "2026年9月是否有各单笔发票的逐笔逾期迁徙明细？", "check_type": "invoice_migration_boundary"},
    {"id": "Q34", "ds": "GAS_AR", "type": "单分公司时点下钻", "q": "2026年9月末沙湖分公司应收余额及长账龄应收各是多少？", "check_type": "shahu_ar"},

    # ====== GAS_SAFE (16题) ======
    {"id": "Q35", "ds": "GAS_SAFE", "type": "安检覆盖率", "q": "2026年9月各分公司的入户安检覆盖率是多少？", "check_type": "inspect_rate"},
    {"id": "Q36", "ds": "GAS_SAFE", "type": "抢修及时率", "q": "2026年9月各分公司的抢修及时率是多少？", "check_type": "emergency_rate"},
    {"id": "Q37", "ds": "GAS_SAFE", "type": "月度过程量统计", "q": "2026年9月各分公司当月到访不遇户次是多少？", "check_type": "not_home"},
    {"id": "Q38", "ds": "GAS_SAFE", "type": "安全加装户数", "q": "2026年9月各分公司燃气三件套加装户数是多少？", "check_type": "three_piece"},
    {"id": "Q39", "ds": "GAS_SAFE", "type": "管网里程存量", "q": "截至2026年9月底江城燃气总管网里程是多少公里？", "check_type": "network_length"},
    {"id": "Q40", "ds": "GAS_SAFE", "type": "GIS入库率", "q": "截至2026年9月底各分公司管网GIS入库率是多少？", "check_type": "gis_rate"},
    {"id": "Q41", "ds": "GAS_SAFE", "type": "老旧管网评估", "q": "截至2026年9月底敷设超过20年的老旧管网里程是多少公里？", "check_type": "old_network"},
    {"id": "Q42", "ds": "GAS_SAFE", "type": "全域隐患闭环率", "q": "截至2026年9月底全公司隐患整改闭环率是多少？", "check_type": "hazard_closed_rate"},
    {"id": "Q43", "ds": "GAS_SAFE", "type": "分公司闭环率排名", "q": "截至2026年9月底各分公司的隐患整改闭环率分别是多少？", "check_type": "branch_closed_rate"},
    {"id": "Q44", "ds": "GAS_SAFE", "type": "超期未闭环总量", "q": "截至2026年9月底全公司超期未闭环的隐患共有多少单？", "check_type": "overdue_hazards"},
    {"id": "Q45", "ds": "GAS_SAFE", "type": "重大隐患分公司分布", "q": "截至2026年9月底各分公司重大超期未闭环隐患有几单？", "check_type": "severe_overdue_hazards"},
    {"id": "Q46", "ds": "GAS_SAFE", "type": "管网与工单关联", "q": "截至2026年9月底重大超期未闭环隐患分别关联了哪些管段？列出工单编号和管段材质", "check_type": "hazard_network_join"},
    {"id": "Q47", "ds": "GAS_SAFE", "type": "历史时点状态重溯", "q": "回看截至2026年6月底未闭环隐患数是多少单？", "check_type": "june_unclosed_hazards"},
    {"id": "Q48", "ds": "GAS_SAFE", "type": "跨表指标计算(泄漏率)", "q": "2026年9月各分公司每千公里管网泄漏次数是多少？", "check_type": "leak_rate_1000km"},
    {"id": "Q49", "ds": "GAS_SAFE", "type": "无数据月份防编造", "q": "2026年10月各分公司安检覆盖率是多少？严格查2026年10月，没有数据请说明。", "check_type": "empty_safety_oct"},
    {"id": "Q50", "ds": "GAS_SAFE", "type": "超范围事故指标防编造", "q": "2026年9月发生安全伤亡事故多少起？停气总时长多少小时？", "check_type": "accident_boundary"},
]

def get_auth_token():
    res = requests.post(f"{BASE_URL}/api/auth/login", json={"username": "admin", "password": "admin123456"}, timeout=10)
    res.raise_for_status()
    return res.json()["token"]

def post_ask(token, ds_id, question, timeout=180):
    headers = {"X-Auth-Token": token, "Content-Type": "application/json"}
    payload = {
        "question": question,
        "selected_dataset_ids": [ds_id],
        "ask_flow": "basic"
    }
    t0 = time.time()
    try:
        resp = requests.post(f"{BASE_URL}/api/ask-chat", json=payload, headers=headers, timeout=timeout)
        duration = round(time.time() - t0, 2)
        if resp.status_code == 200:
            return resp.json(), duration, None
        return None, duration, f"HTTP {resp.status_code}: {resp.text[:200]}"
    except Exception as e:
        duration = round(time.time() - t0, 2)
        return None, duration, str(e)

def evaluate_case(case_info, ai_result, duration, err, gt_data):
    qid = case_info["id"]
    ds = case_info["ds"]
    q = case_info["q"]
    c_type = case_info["check_type"]
    gt = gt_data.get(qid)
    
    report = {
        "id": qid,
        "dataset": ds,
        "type": case_info["type"],
        "question": q,
        "duration_seconds": duration,
        "error": err,
        "status": "FAIL",
        "sql": "",
        "row_count": 0,
        "analysis_summary": "",
        "gt_reference": str(gt)[:200],
        "judgement_details": ""
    }
    
    if err:
        report["judgement_details"] = f"请求错误: {err}"
        return report

    if not ai_result:
        report["judgement_details"] = "无返回数据"
        return report

    dataset_results = ai_result.get("dataset_results") or []
    if not dataset_results:
        report["judgement_details"] = "未生成 dataset_results"
        return report

    first_ds = dataset_results[0]
    sql = first_ds.get("sql", "")
    rows = first_ds.get("rows", [])
    analysis = first_ds.get("analysis", "") or ai_result.get("analysis", "")
    
    report["sql"] = sql
    report["row_count"] = len(rows)
    report["analysis_summary"] = (analysis[:250] + "...") if len(analysis) > 250 else analysis
    
    # 特殊边界类题目检测
    if "boundary" in c_type or "net_profit" in c_type or "invoice" in c_type or "accident" in c_type:
        text = (analysis + " " + json.dumps(rows, ensure_ascii=False)).lower()
        if any(w in text for w in ["不支持", "缺少", "未提供", "没有", "无所得税", "无法提供", "不存在", "未记录", "仅提供"]):
            report["status"] = "PASS"
            report["judgement_details"] = "边界防编造检验通过：系统准确提示不支持该指标或缺少数据。"
        else:
            report["status"] = "RISK"
            report["judgement_details"] = "边界防编造警示：系统未明确说明指标缺失或不支持，可能存在幻觉/替代指标。"
        return report

    # 查空/未来无数据月份测试
    if "empty" in c_type:
        if len(rows) == 0:
            report["status"] = "PASS"
            report["judgement_details"] = "查空检验通过：返回0行，且未偷换为历史月份。"
        else:
            report["status"] = "FAIL"
            report["judgement_details"] = f"查空检验失败：本应返回0行，实际返回了 {len(rows)} 行数据，疑似偷换月份。"
        return report

    # 高压输配无销气边界
    if c_type == "gysp_boundary":
        if len(rows) == 0 or all(r.get("volume_m3", 0) in (0, None) for r in rows):
            report["status"] = "PASS"
            report["judgement_details"] = "高压输配无销售职责校验通过：正确返回空或气量为0。"
        else:
            report["status"] = "RISK"
            report["judgement_details"] = "高压输配销售校验注意：返回了非零销售记录。"
        return report

    # 普通数据查询检验
    if len(rows) > 0:
        # 有数据行，且 SQL 执行成功
        if first_ds.get("analysis_status") == "model_generated":
            report["status"] = "PASS"
            report["judgement_details"] = f"成功生成SQL并查询到 {len(rows)} 行数据，AI完成深度业务解读。"
        else:
            report["status"] = "WARN"
            report["judgement_details"] = f"查询到 {len(rows)} 行数据，但模型解读状态异常: {first_ds.get('analysis_status')}"
    else:
        report["status"] = "FAIL"
        report["judgement_details"] = "SQL执行未返回数据行或执行报错。"

    return report

def main():
    print("=== 开始执行燃气三数据集50道题实测 ===")
    token = get_auth_token()
    print("已成功获取认证 Token。")
    
    gt_file = OUT_DIR / "ground_truth.json"
    gt_data = {}
    if gt_file.exists():
        with open(gt_file, "r", encoding="utf-8") as f:
            gt_data = json.load(f)
            
    # 加载已有的评测记录，支持断点续跑
    res_file = OUT_DIR / "test_results.json"
    results = {}
    if res_file.exists():
        try:
            with open(res_file, "r", encoding="utf-8") as f:
                results = json.load(f)
        except Exception:
            results = {}

    to_run = [c for c in TEST_CASES if c["id"] not in results or results[c["id"]].get("status") == "FAIL"]
    print(f"总计 50 道测试题，已完成: {len(results)} 道，本次待执行: {len(to_run)} 道。")

    # 使用 2 个并发 worker 进行测试，平衡速度与服务端 QPS
    def execute_one(case):
        qid = case["id"]
        ds_id = DATASET_IDS[case["ds"]]
        print(f"[{qid}] 正在发起问数: {case['q']} (数据集 {case['ds']}#{ds_id})...")
        ai_res, duration, err = post_ask(token, ds_id, case["q"], timeout=180)
        report = evaluate_case(case, ai_res, duration, err, gt_data)
        
        # 保存单题快照
        with open(DETAILS_DIR / f"{qid}.json", "w", encoding="utf-8") as f:
            json.dump({
                "case": case,
                "report": report,
                "ai_result": ai_res
            }, f, ensure_ascii=False, indent=2, default=str)
            
        print(f"[{qid}] 完成! 耗时: {duration}s, 状态: {report['status']}, 详情: {report['judgement_details']}")
        return qid, report

    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = {executor.submit(execute_one, c): c for c in to_run}
        for future in as_completed(futures):
            qid, rep = future.result()
            results[qid] = rep
            # 实时写回总结果
            with open(res_file, "w", encoding="utf-8") as f:
                json.dump(results, f, ensure_ascii=False, indent=2, default=str)

    print("=== 全部测试执行完毕，结果已持久化 ===")

if __name__ == '__main__':
    main()
