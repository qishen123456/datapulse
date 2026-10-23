#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
燃气三数据集50道题 Ground Truth 数据库独立核验脚本
"""
import psycopg2
import json

def get_connection():
    return psycopg2.connect(
        host="127.0.0.1",
        port=5433,
        dbname="postgres",
        user="postgres",
        password="datapulse_password" if False else "6670326"
    )

def run_ground_truth():
    conn = get_connection()
    cur = conn.cursor()
    
    gt_results = {}
    
    # Q01: 2026年9月各分公司销气量排名
    cur.execute("SELECT branch_name, SUM(volume_m3) AS volume FROM v_gas_sales WHERE month='2026-09' GROUP BY branch_name ORDER BY volume DESC")
    gt_results['Q01'] = cur.fetchall()
    
    # Q02: 2026年9月各客户类型的销气量及占比
    cur.execute("SELECT user_type, SUM(volume_m3) AS volume, SUM(volume_m3)::numeric / (SELECT SUM(volume_m3) FROM v_gas_sales WHERE month='2026-09') AS ratio FROM v_gas_sales WHERE month='2026-09' GROUP BY user_type ORDER BY volume DESC")
    gt_results['Q02'] = cur.fetchall()
    
    # Q03: 2026年9月各客户类型的加权销气均价是多少？
    cur.execute("SELECT user_type, SUM(revenue_yuan) / NULLIF(SUM(volume_m3),0) AS avg_price FROM v_gas_sales WHERE month='2026-09' GROUP BY user_type ORDER BY avg_price DESC")
    gt_results['Q03'] = cur.fetchall()
    
    # Q04: 2026年9月各分公司的估抄量与估抄率是多少？
    cur.execute("SELECT branch_name, SUM(estimated_meter_m3) AS est_vol, SUM(volume_m3) AS vol, SUM(estimated_meter_m3)::numeric / NULLIF(SUM(volume_m3), 0) AS est_rate FROM v_gas_sales WHERE month='2026-09' GROUP BY branch_name ORDER BY est_rate DESC")
    gt_results['Q04'] = cur.fetchall()
    
    # Q05: 列出2026年9月沙湖分公司各网格的估抄率
    cur.execute("SELECT org_id, org_name, SUM(estimated_meter_m3)::numeric / NULLIF(SUM(volume_m3), 0) AS est_rate FROM v_gas_sales WHERE month='2026-09' AND branch_id='SHAHU' GROUP BY org_id, org_name ORDER BY est_rate DESC")
    gt_results['Q05'] = cur.fetchall()
    
    # Q06: 2026年9月不同气源的采购气量和采购成本各是多少？
    cur.execute("SELECT source, SUM(inlet_m3) AS vol, SUM(purchase_cost_yuan) AS cost FROM v_gas_supply_sources WHERE month='2026-09' GROUP BY source ORDER BY cost DESC")
    gt_results['Q06'] = cur.fetchall()
    
    # Q07: 2026年9月各分公司的供销差量和供销差率是多少？
    cur.execute("SELECT branch_name, SUM(inlet_m3) - SUM(sales_m3) AS loss_vol, (SUM(inlet_m3) - SUM(sales_m3))::numeric / NULLIF(SUM(inlet_m3), 0) AS loss_rate FROM v_gas_supply_balance WHERE month='2026-09' GROUP BY branch_name ORDER BY loss_rate DESC")
    gt_results['Q07'] = cur.fetchall()
    
    # Q08: 2026年9月有哪些服务中心超过了演示供销差阈值？
    cur.execute("SELECT org_id, org_name, loss_rate, loss_threshold FROM v_gas_supply_balance WHERE month='2026-09' AND loss_rate > loss_threshold ORDER BY loss_rate DESC")
    gt_results['Q08'] = cur.fetchall()
    
    # Q09: 2026年前三季度每月模拟税前利润是多少？
    cur.execute("SELECT month, SUM(pretax_profit_yuan) AS profit FROM v_gas_profit WHERE month BETWEEN '2026-01' AND '2026-09' GROUP BY month ORDER BY month")
    gt_results['Q09'] = cur.fetchall()
    
    # Q10: 2026年前三季度累计总收入与模拟税前利润是多少？
    cur.execute("SELECT SUM(total_revenue_yuan) AS total_rev, SUM(pretax_profit_yuan) AS total_profit FROM v_gas_profit WHERE month BETWEEN '2026-01' AND '2026-09'")
    gt_results['Q10'] = cur.fetchall()
    
    # Q11: 2026年9月各分公司销气量环比8月增长还是下降？
    cur.execute("""
    WITH m AS (
        SELECT month, branch_name, SUM(volume_m3) AS vol 
        FROM v_gas_sales 
        WHERE month IN ('2026-08', '2026-09') 
        GROUP BY month, branch_name
    ),
    diff AS (
        SELECT branch_name, vol AS sep_vol, LAG(vol) OVER(PARTITION BY branch_name ORDER BY month) AS aug_vol
        FROM m
    )
    SELECT branch_name, sep_vol, aug_vol, (sep_vol - aug_vol)::numeric / NULLIF(aug_vol, 0) AS mom_rate
    FROM diff WHERE aug_vol IS NOT NULL ORDER BY mom_rate DESC
    """)
    gt_results['Q11'] = cur.fetchall()
    
    # Q12: 2026年9月各分公司新增通气户数是多少？
    cur.execute("SELECT branch_name, SUM(connected_users) AS users FROM v_gas_growth WHERE month='2026-09' GROUP BY branch_name ORDER BY users DESC")
    gt_results['Q12'] = cur.fetchall()
    
    # Q13: 2026年9月末各分公司期末总户数是多少？
    cur.execute("SELECT branch_name, SUM(ending_users) AS ending_users FROM v_gas_growth WHERE month='2026-09' GROUP BY branch_name ORDER BY ending_users DESC")
    gt_results['Q13'] = cur.fetchall()
    
    # Q14: 高压输配分公司在2026年9月的销气量是多少？
    cur.execute("SELECT branch_name, SUM(volume_m3) FROM v_gas_sales WHERE month='2026-09' AND branch_id='GYSP' GROUP BY branch_name")
    gt_results['Q14'] = cur.fetchall()  # 应为空，高压输配无销气业务
    
    # Q15: 2026年10月各分公司销气量是多少？
    cur.execute("SELECT branch_name, SUM(volume_m3) FROM v_gas_sales WHERE month='2026-10' GROUP BY branch_name")
    gt_results['Q15'] = cur.fetchall()  # 应为空
    
    # Q16: 2026年前三季度江城燃气的税后净利润是多少？
    # 业务边界：无所得税字段
    gt_results['Q16'] = "BOUNDARY: 无所得税字段，系统应明确说明不支持税后净利润，只提供模拟税前利润"
    
    # Q17: 最新月份各分公司销气量排名前三的是哪几个分公司？
    cur.execute("SELECT branch_name, SUM(volume_m3) AS vol FROM v_gas_sales WHERE month=(SELECT MAX(month) FROM v_gas_sales) GROUP BY branch_name ORDER BY vol DESC LIMIT 3")
    gt_results['Q17'] = cur.fetchall()
    
    # Q18: 2026年9月末江城燃气总应收余额是多少？
    cur.execute("SELECT SUM(closing_yuan) FROM v_gas_ar WHERE month='2026-09'")
    gt_results['Q18'] = cur.fetchall()
    
    # Q19: 2026年9月末各分公司的应收余额分布情况
    cur.execute("SELECT branch_name, SUM(closing_yuan) AS closing FROM v_gas_ar WHERE month='2026-09' GROUP BY branch_name ORDER BY closing DESC")
    gt_results['Q19'] = cur.fetchall()
    
    # Q20: 2026年9月末全公司的应收账龄分布结构
    cur.execute("SELECT SUM(aging_0_30_yuan) AS a0_30, SUM(aging_31_90_yuan) AS a31_90, SUM(aging_91_180_yuan) AS a91_180, SUM(aging_181_365_yuan) AS a181_365, SUM(aging_365_plus_yuan) AS a365_plus FROM v_gas_ar WHERE month='2026-09'")
    gt_results['Q20'] = cur.fetchall()
    
    # Q21: 2026年9月末账龄超过180天的长账龄应收总额是多少？
    cur.execute("SELECT SUM(aging_181_365_yuan + aging_365_plus_yuan) FROM v_gas_ar WHERE month='2026-09'")
    gt_results['Q21'] = cur.fetchall()
    
    # Q22: 2026年9月末期末计提余额是多少？
    cur.execute("SELECT SUM(provision_yuan) FROM v_gas_ar WHERE month='2026-09'")
    gt_results['Q22'] = cur.fetchall()
    
    # Q23: 按1%、3%、10%、30%、70%的演示账龄比例复核2026年9月末演示应计提金额
    cur.execute("SELECT SUM(ROUND(aging_0_30_yuan*0.01 + aging_31_90_yuan*0.03 + aging_91_180_yuan*0.10 + aging_181_365_yuan*0.30 + aging_365_plus_yuan*0.70, 2)) FROM v_gas_ar WHERE month='2026-09'")
    gt_results['Q23'] = cur.fetchall()
    
    # Q24: 2026年9月各分公司的应收滚动平衡是否存在差异？
    cur.execute("SELECT branch_name, SUM(opening_yuan + billed_yuan - collected_yuan + adjustment_yuan - closing_yuan) AS roll_diff FROM v_gas_ar WHERE month='2026-09' GROUP BY branch_name")
    gt_results['Q24'] = cur.fetchall()
    
    # Q25: 2026年9月各分公司的当月气费回收率是多少？
    cur.execute("SELECT branch_name, SUM(collected_yuan)::numeric / NULLIF(SUM(billed_yuan), 0) AS recovery_rate FROM v_gas_ar WHERE month='2026-09' GROUP BY branch_name ORDER BY recovery_rate DESC")
    gt_results['Q25'] = cur.fetchall()
    
    # Q26: 2026年前三季度各分公司累计气费回收率是多少？
    cur.execute("SELECT branch_name, SUM(collected_yuan)::numeric / NULLIF(SUM(billed_yuan), 0) AS total_recovery_rate FROM v_gas_ar WHERE month BETWEEN '2026-01' AND '2026-09' GROUP BY branch_name ORDER BY total_recovery_rate DESC")
    gt_results['Q26'] = cur.fetchall()
    
    # Q27: 2026年9月末欠费金额排名前5的模拟工商客户是哪几家？
    cur.execute("SELECT customer_name, customer_id, closing_yuan FROM v_gas_ar WHERE month='2026-09' AND object_kind='模拟客户' ORDER BY closing_yuan DESC LIMIT 5")
    gt_results['Q27'] = cur.fetchall()
    
    # Q28: 2026年9月末有应收余额的模拟工商客户一共有多少家？
    cur.execute("SELECT COUNT(DISTINCT customer_id) FROM v_gas_ar WHERE month='2026-09' AND object_kind='模拟客户' AND closing_yuan > 0")
    gt_results['Q28'] = cur.fetchall()
    
    # Q29: 2026年9月末居民用户的欠费总额是多少？
    cur.execute("SELECT SUM(closing_yuan) FROM v_gas_ar WHERE month='2026-09' AND user_type='居民'")
    gt_results['Q29'] = cur.fetchall()
    
    # Q30: 2026年9月各分公司销气量价稽核差异总额是多少？
    cur.execute("SELECT branch_name, SUM(audit_difference_yuan) AS diff FROM v_gas_sales WHERE month='2026-09' GROUP BY branch_name ORDER BY diff DESC")
    gt_results['Q30'] = cur.fetchall()
    
    # Q31: 2026年前三季度各月月末应收余额趋势如何？
    cur.execute("SELECT month, SUM(closing_yuan) AS closing FROM v_gas_ar WHERE month BETWEEN '2026-01' AND '2026-09' GROUP BY month ORDER BY month")
    gt_results['Q31'] = cur.fetchall()
    
    # Q32: 2026年10月末应收余额是多少？
    cur.execute("SELECT SUM(closing_yuan) FROM v_gas_ar WHERE month='2026-10'")
    gt_results['Q32'] = cur.fetchall()  # 应为 None 或空
    
    # Q33: 2026年9月是否有各单笔发票的逐笔逾期迁徙明细？
    gt_results['Q33'] = "BOUNDARY: 无逐张发票迁徙数据，系统应说明不支持单笔发票到期日迁徙"
    
    # Q34: 2026年9月末沙湖分公司应收余额及长账龄应收是多少？
    cur.execute("SELECT SUM(closing_yuan) AS closing, SUM(aging_181_365_yuan + aging_365_plus_yuan) AS long_aging FROM v_gas_ar WHERE month='2026-09' AND branch_id='SHAHU'")
    gt_results['Q34'] = cur.fetchall()
    
    # Q35: 2026年9月各分公司的入户安检覆盖率是多少？
    cur.execute("SELECT branch_name, SUM(inspected)::numeric / NULLIF(SUM(due_inspect), 0) AS inspect_rate FROM v_gas_safety WHERE month='2026-09' GROUP BY branch_name ORDER BY inspect_rate DESC")
    gt_results['Q35'] = cur.fetchall()
    
    # Q36: 2026年9月各分公司的抢修及时率是多少？
    cur.execute("SELECT branch_name, SUM(emergency_on_time)::numeric / NULLIF(SUM(emergency_total), 0) AS on_time_rate FROM v_gas_safety WHERE month='2026-09' GROUP BY branch_name ORDER BY on_time_rate DESC")
    gt_results['Q36'] = cur.fetchall()
    
    # Q37: 2026年9月各分公司当月到访不遇户次是多少？
    cur.execute("SELECT branch_name, SUM(not_at_home) AS not_home FROM v_gas_safety WHERE month='2026-09' GROUP BY branch_name ORDER BY not_home DESC")
    gt_results['Q37'] = cur.fetchall()
    
    # Q38: 2026年9月各分公司燃气三件套加装户数是多少？
    cur.execute("SELECT branch_name, SUM(three_piece_installed) AS piece FROM v_gas_safety WHERE month='2026-09' GROUP BY branch_name ORDER BY piece DESC")
    gt_results['Q38'] = cur.fetchall()
    
    # Q39: 截至2026年9月底江城燃气总管网里程是多少公里？
    cur.execute("SELECT SUM(length_km) FROM v_gas_network WHERE laid_date <= '2026-09-30'")
    gt_results['Q39'] = cur.fetchall()
    
    # Q40: 截至2026年9月底各分公司管网GIS入库率是多少？
    cur.execute("SELECT branch_name, SUM(CASE WHEN gis_loaded_date <= '2026-09-30' THEN length_km ELSE 0 END)::numeric / NULLIF(SUM(length_km), 0) AS gis_rate FROM v_gas_network WHERE laid_date <= '2026-09-30' GROUP BY branch_name ORDER BY gis_rate DESC")
    gt_results['Q40'] = cur.fetchall()
    
    # Q41: 截至2026年9月底敷设超过20年的老旧管网里程是多少公里？
    cur.execute("SELECT SUM(length_km) FROM v_gas_network WHERE laid_date <= '2006-09-30'")
    gt_results['Q41'] = cur.fetchall()
    
    # Q42: 截至2026年9月底全公司隐患闭环率是多少？
    cur.execute("SELECT COUNT(*) FILTER(WHERE completed_date <= '2026-09-30')::numeric / NULLIF(COUNT(*), 0) AS closed_rate FROM v_gas_hazards WHERE found_date <= '2026-09-30'")
    gt_results['Q42'] = cur.fetchall()
    
    # Q43: 截至2026年9月底各分公司的隐患整改闭环率分别是多少？
    cur.execute("SELECT branch_name, COUNT(*) FILTER(WHERE completed_date <= '2026-09-30')::numeric / NULLIF(COUNT(*), 0) AS closed_rate FROM v_gas_hazards WHERE found_date <= '2026-09-30' GROUP BY branch_name ORDER BY closed_rate DESC")
    gt_results['Q43'] = cur.fetchall()
    
    # Q44: 截至2026年9月底全公司超期未闭环的隐患共有多少单？
    cur.execute("SELECT COUNT(*) FROM v_gas_hazards WHERE found_date <= '2026-09-30' AND due_date < '2026-09-30' AND (completed_date IS NULL OR completed_date > '2026-09-30')")
    gt_results['Q44'] = cur.fetchall()
    
    # Q45: 截至2026年9月底各分公司重大超期未闭环隐患有几单？
    cur.execute("SELECT branch_name, COUNT(*) FROM v_gas_hazards WHERE found_date <= '2026-09-30' AND due_date < '2026-09-30' AND (completed_date IS NULL OR completed_date > '2026-09-30') AND severity='重大' GROUP BY branch_name")
    gt_results['Q45'] = cur.fetchall()
    
    # Q46: 截至2026年9月底重大超期未闭环隐患分别关联了哪些管段？
    cur.execute("SELECT h.hazard_id, h.branch_name, h.network_id, n.material, n.pressure_level FROM v_gas_hazards h LEFT JOIN v_gas_network n ON h.network_id = n.network_id WHERE h.found_date <= '2026-09-30' AND h.due_date < '2026-09-30' AND (h.completed_date IS NULL OR h.completed_date > '2026-09-30') AND h.severity='重大'")
    gt_results['Q46'] = cur.fetchall()
    
    # Q47: 截至2026年6月底未闭环隐患数是多少单？
    cur.execute("SELECT COUNT(*) FROM v_gas_hazards WHERE found_date <= '2026-06-30' AND (completed_date IS NULL OR completed_date > '2026-06-30')")
    gt_results['Q47'] = cur.fetchall()
    
    # Q48: 2026年9月各分公司每千公里管网泄漏次数是多少？
    cur.execute("""
    WITH leaks AS (
        SELECT branch_id, branch_name, SUM(leak_count) AS lk
        FROM v_gas_safety WHERE month='2026-09' GROUP BY branch_id, branch_name
    ),
    nets AS (
        SELECT branch_id, SUM(length_km) AS km
        FROM v_gas_network WHERE laid_date <= '2026-09-30' GROUP BY branch_id
    )
    SELECT leaks.branch_name, leaks.lk, nets.km, (leaks.lk * 1000)::numeric / NULLIF(nets.km, 0) AS leak_rate_per_1000km
    FROM leaks JOIN nets ON leaks.branch_id = nets.branch_id ORDER BY leak_rate_per_1000km DESC
    """)
    gt_results['Q48'] = cur.fetchall()
    
    # Q49: 2026年10月各分公司安检覆盖率是多少？
    cur.execute("SELECT branch_name, SUM(inspected) FROM v_gas_safety WHERE month='2026-10' GROUP BY branch_name")
    gt_results['Q49'] = cur.fetchall()  # 应为空
    
    # Q50: 2026年9月发生安全伤亡事故多少起？停气总时长多少小时？
    gt_results['Q50'] = "BOUNDARY: 无伤亡事故、停气时长字段，系统应明确说明不支持该指标"
    
    cur.close()
    conn.close()
    
    # 格式化输出为可读 JSON
    def serialize(obj):
        if hasattr(obj, '__iter__') and not isinstance(obj, (str, bytes)):
            return [serialize(i) for i in obj]
        return str(obj)

    with open("gas_dataset_test_50/ground_truth.json", "w", encoding="utf-8") as f:
        json.dump({k: serialize(v) for k, v in gt_results.items()}, f, ensure_ascii=False, indent=2)
    
    print(f"成功计算并导出全部 50 道题的 Ground Truth 基准结果，共 {len(gt_results)} 条。")

if __name__ == '__main__':
    run_ground_truth()
