# DataPulse 智能问数 100 大经典错题库与标准答案及改进方案

> **题库版本**：v2.0 终极实战版  
> **编制依据**：`DataPulse全域数据资产与业务口径深度学习手册.md` & `DataPulse业务数据资产与NL2SQL深度学习手册.md`  
> **数据对账源**：`exports/csv/` 真实全量数据库（PostgreSQL 16）  
> **适用场景**：问数质量自检、NL2SQL 评测基准、Prompt 调优对账、回归自动化测试  
> **核心原则**：**保持代码冻结，沉淀完整题目、易错陷阱、标准答案数值、标准 SQL 与精准改进方案**  

---

## 目录
- [一、组织层级跨级混加与大盘防重类错题（001~020）](#一组织层级跨级混加与大盘防重类错题001020)
- [二、四大业务板块与细分行业线拆解类错题（021~040）](#二四大业务板块与细分行业线拆解类错题021040)
- [三、TopN 排名、极值对比与层级隔离类错题（041~055）](#三topn-排名极值对比与层级隔离类错题041055)
- [四、动态时间序列（Q1~Q4/环比/同比）类错题（056~070）](#四动态时间序列q1q4环比同比类错题056070)
- [五、多轮对话、省略指代与多主体对标类错题（071~080）](#五多轮对话省略指代与多主体对标类错题071080)
- [六、比率 HAVING 过滤、零除保护与空值边界类错题（081~090）](#六比率-having-过滤零除保护与空值边界类错题081090)
- [七、任务派发对账、预留额审计与父子勾稽类错题（091~100）](#七任务派发对账预留额审计与父子勾稽类错题091100)

---

## 一、组织层级跨级混加与大盘防重类错题（001~020）

### 001. 企业服务事业部 2026 年大盘开单总额
- **用户提问**：`企业服务事业部今年总共开了多少单？`
- **常见错误表现**：算出 `29.04 亿元`（翻了 3 倍）。错误地在 `feishu_tbl_xioafeizhe` 上直接 `SUM(actual_billing_amount)`，把事业部总部、13 个分公司、69 个城市分公司三级汇总行全部相加。
- **标准答案 (Ground Truth)**：**`968,183,304.53 元`（约 `9.68 亿元` / `96,818.33 万元`）**，总任务 `17.8971 亿元`，达成率 `54.10%`。
- **标准 SQL (Ground Truth SQL)**：
  ```sql
  SELECT 
      target_amount AS 总任务金额,
      actual_billing_amount AS 年度开单金额,
      ROUND(completion_rate * 100, 2) AS 达成率
  FROM public.smart_sales_performance
  WHERE region_name IS NULL OR region_name = '';
  ```
- **改进方案**：在 Agent 2 Prompt 中强化“企业服务事业部总体判定规则：`region_name IS NULL OR region_name=''`”，禁止对全表无脑 SUM。

### 002. 消费电子事业部 2026 年大盘年度开单总额
- **用户提问**：`消费电子事业部2026年大盘开单总额是多少？`
- **常见错误表现**：算出 `1.70 亿元` 或 `2.12 亿元`。原因：查大盘未加 `business_line = '总额(未拆分)'`，将总盘与餐饮、办公、医疗分板块重复累加；或误路由至旧版 Dataset 3。
- **标准答案**：**`85,437,688.57 元`（`8,543.77 万元`）**，大盘target_amount约 `1.50 亿元`。
- **标准 SQL**：
  ```sql
  SELECT 
      '消费电子事业部' AS 组织名称,
      SUM(target_amount) AS target_amount,
      SUM(actual_billing_amount) AS actual_billing_amount,
      CASE WHEN SUM(target_amount)>0 THEN ROUND(SUM(actual_billing_amount)/SUM(target_amount)*100, 2) ELSE 0 END AS 达成率
  FROM public.smart_sales_performance
  WHERE year = '2026' AND node_level = '事业部' AND business_line = '总额(未拆分)';
  ```
- **改进方案**：Agent 1 将“商用”强绑定至 Dataset 63；Agent 2 大盘查询必须强制注入 `business_line = '总额(未拆分)'`。

### 003. 华东分公司大盘开单总额
- **用户提问**：`华东分公司今年开单总额是多少？`
- **常见错误表现**：算出 `5,343 万元`。原因：把华东分公司本级行与下辖各代表处明细行累加。
- **标准答案**：**`26,715,362.05 元`（`2,671.54 万元`）**，总任务 `9,500 万元`，达成率 `28.12%`。
- **标准 SQL**：
  ```sql
  SELECT region_name, SUM(target_amount) AS target_amount, SUM(actual_billing_amount) AS actual_billing_amount
  FROM public.smart_sales_performance
  WHERE year='2026' AND node_level='分公司' AND region_name='华东分公司' AND business_line='总额(未拆分)'
  GROUP BY region_name;
  ```
- **改进方案**：遵守 Truth of Source 原则，直接读取分公司预存汇总行。

### 004. 华南分公司大盘销售与达成率
- **用户提问**：`华南分公司今年销售业绩和达成率是多少？`
- **常见错误表现**：达成率显示为 45.51%（Dataset 3 旧口径）或把餐饮业务部加了进去。
- **标准答案**：target_amount `8,200.00 万元`，年度开单 **`2,460.00 万元`（`24,600,009.09 元`）**，达成率 **`30.00%`**。
- **标准 SQL**：
  ```sql
  SELECT region_name, SUM(target_amount) AS target_amount, SUM(actual_billing_amount) AS actual_billing_amount,
         ROUND(SUM(actual_billing_amount)/SUM(target_amount)*100, 2) AS 达成率
  FROM public.smart_sales_performance
  WHERE year='2026' AND node_level='分公司' AND region_name='华南分公司' AND business_line='总额(未拆分)'
  GROUP BY region_name;
  ```
- **改进方案**：锁定 `node_level='分公司' AND business_line='总额(未拆分)'`。

### 005. 华北分公司大盘销售与达成率
- **用户提问**：`华北分公司今年完成了多少任务？`
- **常见错误表现**：开单漏算或跨月重复计算。
- **标准答案**：target_amount `6,360.00 万元`，开单 **`1,813.96 万元`（`18,139,582.54 元`）**，达成率 **`28.52%`**。
- **标准 SQL**：
  ```sql
  SELECT region_name, SUM(target_amount) AS target_amount, SUM(actual_billing_amount) AS actual_billing_amount,
         ROUND(SUM(actual_billing_amount)/SUM(target_amount)*100, 2) AS 达成率
  FROM public.smart_sales_performance
  WHERE year='2026' AND node_level='分公司' AND region_name='华北分公司' AND business_line='总额(未拆分)'
  GROUP BY region_name;
  ```
- **改进方案**：严格限定 `year='2026'` 与单一region_name。

### 006. 西南分公司大盘销售与达成率
- **用户提问**：`西南分公司2026年开单和指标是多少？`
- **常见错误表现**：误将“西南分公司”识别为“西南分公司”。
- **标准答案**：target_amount `6,940.00 万元`，开单 **`1,598.27 万元`（`15,982,734.89 元`）**，达成率 **`23.03%`**（四大区中最低）。
- **标准 SQL**：
  ```sql
  SELECT region_name, SUM(target_amount) AS target_amount, SUM(actual_billing_amount) AS actual_billing_amount,
         ROUND(SUM(actual_billing_amount)/SUM(target_amount)*100, 2) AS 达成率
  FROM public.smart_sales_performance
  WHERE year='2026' AND node_level='分公司' AND region_name='西南分公司' AND business_line='总额(未拆分)'
  GROUP BY region_name;
  ```
- **改进方案**：同义词映射库明确“西南分公司”属于商用，“西南分公司”属于消费者。

### 007. 消费者华北分公司大盘开单
- **用户提问**：`企业服务事业部华北分公司开单多少？`
- **常见错误表现**：把郑州、洛阳等城市公司加在一起算成 2 亿以上。
- **标准答案**：target_amount `20,200.00 万元` (2.02 亿)，开单 **`10,478.90 万元` (1.0479 亿)**，达成率 **`51.88%`**。
- **标准 SQL**：
  ```sql
  SELECT region_name AS 分公司,
         ROUND(target_amount/10000, 2) AS target_amount_万,
         ROUND(actual_billing_amount/10000, 2) AS actual_billing_amount_万
  FROM public.smart_sales_performance
  WHERE region_name='华北分公司' AND department_name IS NULL;
  ```
- **改进方案**：查分公司必须限定 `department_name IS NULL`。

### 008. 消费者华中分公司大盘开单
- **用户提问**：`华中分公司完成了多少开单金额？`
- **常见错误表现**：未限定分公司层级。
- **标准答案**：target_amount `21,904.00 万元`，开单 **`9,576.01 万元`**，达成率 **`43.72%`**。
- **标准 SQL**：
  ```sql
  SELECT region_name AS 分公司,
         ROUND(actual_billing_amount/10000, 2) AS 开单_万
  FROM public.smart_sales_performance
  WHERE region_name='华中分公司' AND department_name IS NULL;
  ```
- **改进方案**：分公司查询强约束过滤下级字段为空。

### 009. 消费者华南分公司业绩
- **用户提问**：`华南分公司今年指标和实际是多少？`
- **常见错误表现**：城市公司混入导致指标翻倍。
- **标准答案**：target_amount `19,735.00 万元`，开单 **`9,287.71 万元`**，达成率 **`47.06%`**。
- **标准 SQL**：
  ```sql
  SELECT region_name AS 分公司,
         ROUND(target_amount/10000, 2) AS 任务_万,
         ROUND(actual_billing_amount/10000, 2) AS 开单_万
  FROM public.smart_sales_performance
  WHERE region_name='华南分公司' AND department_name IS NULL;
  ```
- **改进方案**：同上。

### 010. 消费者华东分公司业绩
- **用户提问**：`华东分公司今年开了多少单？`
- **常见错误表现**：错将“赣闽”匹配为商用“华东分公司”。
- **标准答案**：target_amount `14,798.00 万元`，开单 **`6,567.16 万元`**，达成率 **`44.38%`**。
- **标准 SQL**：
  ```sql
  SELECT region_name AS 分公司,
         ROUND(actual_billing_amount/10000, 2) AS 开单_万
  FROM public.smart_sales_performance
  WHERE region_name='华东分公司' AND department_name IS NULL;
  ```
- **改进方案**：消歧路由配置增加赣闽 $\to$ 企业服务事业部。

### 011~020. 消费者其余分公司基准表（西北/湖南/云贵渝/河北/山东/川藏/京津/江浙沪/黑吉辽/电商大盘）
- **011. 西北分公司**：任务 `13,360.00 万`，开单 **`6,466.50 万元`**，达成率 **`48.40%`**。
- **012. 湖南分公司**：任务 `13,987.00 万`，开单 **`6,232.53 万元`**，达成率 **`44.56%`**。
- **013. 云贵渝分公司**：任务 `12,733.00 万`，开单 **`6,185.34 万元`**，达成率 **`48.58%`**。
- **014. 河北分公司**：任务 `11,099.00 万`，开单 **`5,572.61 万元`**，达成率 **`50.21%`**。
- **015. 山东分公司**：任务 `10,042.00 万`，开单 **`5,413.89 万元`**，达成率 **`53.91%`**（达成率第一）。
- **016. 西南分公司**：任务 `13,180.00 万`，开单 **`4,994.46 万元`**，达成率 **`37.89%`**。
- **017. 京津分公司**：任务 `7,872.00 万`，开单 **`3,822.38 万元`**，达成率 **`48.56%`**。
- **018. 江浙沪分公司**：任务 `11,740.00 万`，开单 **`3,798.26 万元`**，达成率 **`32.35%`**（达成率最低）。
- **019. 华北分公司**：任务 `8,321.00 万`，开单 **`3,792.51 万元`**，达成率 **`45.58%`**（开单最低）。
- **020. 跨境电商事业部大盘**：年度目标营收与实际达成从 `v_feishu_tbldianshang WHERE 层级级别='事业部'` 独立提取，严禁与业务部混加。

---

## 二、四大业务板块与细分行业线拆解类错题（021~040）

### 021. 企业服务事业部线下主业务actual_billing_amount
- **用户提问**：`企业服务事业部线下业务总共开单多少？`
- **常见错误表现**：误以为线下业务等于全部开单。
- **标准答案**：**`821,882,529.09 元`（`82,188.25 万元` / `8.22 亿元`）**，占大盘 84.89%。
- **标准 SQL**：
  ```sql
  SELECT COALESCE(NULLIF(regexp_replace(fields->>'线下-actual_billing_amount', '[^0-9.-]', '', 'g'), ''), '0')::NUMERIC AS 线下开单
  FROM public.smart_sales_performance
  WHERE region_name IS NULL OR region_name = '';
  ```
- **改进方案**：针对板块查询准确提取对应板块列，严禁直接取actual_billing_amount。

### 022. 企业服务事业部新零售板块开单
- **用户提问**：`新零售板块今年贡献了多少开单金额？`
- **常见错误表现**：误报为 0（误将分公司新零售为 0 当作事业部总部为 0）。
- **标准答案**：**`104,732,835.71 元`（`10,473.28 万元` / `1.05 亿元`）**，占大盘 10.82%。
- **标准 SQL**：
  ```sql
  SELECT COALESCE(NULLIF(regexp_replace(fields->>'新零售-actual_billing_amount', '[^0-9.-]', '', 'g'), ''), '0')::NUMERIC AS 新零售开单
  FROM public.smart_sales_performance
  WHERE region_name IS NULL OR region_name = '';
  ```
- **改进方案**：总部层级新零售有数，分公司新零售为 0，需分层说明。

### 023. 企业服务事业部地产配套开单
- **用户提问**：`地产业务今年完成了多少？`
- **常见错误表现**：去分公司表里查导致查出为 0。
- **标准答案**：**`28,317,155.18 元`（`2,831.72 万元`）**，target_amount `4,000 万元`，达成率 `70.79%`。
- **标准 SQL**：
  ```sql
  SELECT COALESCE(NULLIF(regexp_replace(fields->>'地产-actual_billing_amount', '[^0-9.-]', '', 'g'), ''), '0')::NUMERIC AS 地产开单
  FROM public.smart_sales_performance
  WHERE region_name IS NULL OR region_name = '';
  ```
- **改进方案**：Prompt 中强调地产配套仅在事业部总体有数。

### 024. 企业服务事业部燃气定制业务开单
- **用户提问**：`燃气定制业务今年做了多少业绩？`
- **常见错误表现**：万元与元单位混淆。
- **标准答案**：**`13,250,784.55 元`（`1,325.08 万元`）**，target_amount `2,418 万元`，达成率 `54.80%`。
- **标准 SQL**：
  ```sql
  SELECT COALESCE(NULLIF(regexp_replace(fields->>'燃气定制-actual_billing_amount', '[^0-9.-]', '', 'g'), ''), '0')::NUMERIC AS 燃气开单
  FROM public.smart_sales_performance
  WHERE region_name IS NULL OR region_name = '';
  ```
- **改进方案**：规范字段提取。

### 025. 华北分公司线下业务开单
- **用户提问**：`华北分公司的线下业务完成了多少？`
- **标准答案**：**`10,478.90 万元`**，任务 `17,360.00 万元`。
- **标准 SQL**：
  ```sql
  SELECT region_name AS 分公司,
         ROUND(COALESCE(NULLIF(regexp_replace(fields->>'线下-actual_billing_amount', '[^0-9.-]', '', 'g'), ''), '0')::NUMERIC/10000, 2) AS 线下开单_万
  FROM public.smart_sales_performance
  WHERE region_name='华北分公司' AND department_name IS NULL;
  ```

### 026. 华北分公司燃气定制与新零售开单
- **用户提问**：`华北分公司的新零售和燃气定制开单是多少？`
- **标准答案**：新零售实际 **`0 元`**，燃气定制实际 **`0 元`**（分公司业绩全部由线下贡献）。
- **改进方案**：系统需如实告知为 0，不能返回空表。

### 027. 商用餐饮业务部大盘业绩
- **用户提问**：`消费电子事业部餐饮业务部今年完成情况如何？`
- **常见错误表现**：去区域分公司里查“餐饮分公司”。
- **标准答案**：属于垂直**行业条线**，target_amount `10,500.00 万元` (1.05亿)，开单 **`4,530.25 万元`**，达成率 **`43.15%`**。
- **标准 SQL**：
  ```sql
  SELECT region_name, SUM(target_amount) AS 任务, SUM(actual_billing_amount) AS 开单,
         ROUND(SUM(actual_billing_amount)/SUM(target_amount)*100, 2) AS 达成率
  FROM public.smart_sales_performance
  WHERE year='2026' AND 条线='行业条线' AND region_name='餐饮业务部' AND 行业线='餐饮部'
  GROUP BY region_name;
  ```
- **改进方案**：Agent 1 识别“餐饮业务部”必须设置 `line_type='行业条线'`。

### 028. 商用公共办公业务部业绩
- **用户提问**：`公共办公业务部今年开单多少？`
- **标准答案**：锁定行业条线 `公共办公业务部`。
- **标准 SQL**：`WHERE year='2026' AND 条线='行业条线' AND region_name='公共办公业务部' AND 行业线='公共办公'`。

### 029. 商用工业医疗业务部业绩
- **用户提问**：`工业医疗业务部今年业绩如何？`
- **标准答案**：锁定行业条线 `工业医疗业务部`。
- **标准 SQL**：`WHERE year='2026' AND 条线='行业条线' AND region_name='工业医疗业务部' AND 行业线='工业医疗'`。

### 030. 商用大盘 5 月公共办公板块开单
- **用户提问**：`5月份全公司公共办公板块开了多少单？`
- **常见错误表现**：算成了全年办公累计。
- **标准答案**：从 `v_feishu_tblshangyongv2` 过滤 `月份=5 AND 行业线='公共办公' AND 层级='事业部'`。

### 031~040. 行业线占比与交叉渗透（31~40 题口径规范）
- **031. 湖北代表处办公板块开单占比**：分子取 `行业线='公共办公'` 开单，分母取该代表处 `business_line='总额(未拆分)'` 开单，必须除零保护。
- **032. 南区分公司餐饮板块占比**：取南区分公司下属餐饮开单占南区总额比。
- **033. 东区分公司医疗板块贡献**：过滤 `上级名称='华东分公司' AND 行业线='工业医疗'`。
- **034~040. 涉及各业务板块的交叉查询**：全部严格使用 CTE 隔离分子分母，禁止在单表交叉 SUM 产生笛卡尔积。

---

## 三、TopN 排名、极值对比与层级隔离类错题（041~055）

### 041. 企业服务事业部开单 Top 3 分公司
- **用户提问**：`企业服务事业部开单排名前三的分公司是哪几个？`
- **常见错误表现**：把郑州城市分公司（4507万）排了进去，导致分公司层级失真。
- **标准答案**：
  1. **华北分公司**：`10,478.90 万元` (1.0479 亿)
  2. **华中分公司**：`9,576.01 万元`
  3. **华南分公司**：`9,287.71 万元`
- **标准 SQL**：
  ```sql
  SELECT region_name AS 分公司,
         ROUND(actual_billing_amount/10000, 2) AS 开单_万
  FROM public.smart_sales_performance
  WHERE region_name IS NOT NULL AND department_name IS NULL
  ORDER BY 开单_万 DESC LIMIT 3;
  ```
- **改进方案**：排名必须限定同层级（`department_name IS NULL`）。

### 042. 企业服务事业部达成率最高与最低分公司
- **用户提问**：`企业服务事业部哪个分公司达成率最高？哪个最低？`
- **标准答案**：最高为 **山东分公司（53.91%）**；最低为 **江浙沪分公司（32.35%）**。
- **标准 SQL**：
  ```sql
  WITH branch_data AS (
      SELECT region_name AS 分公司,
             ROUND(completion_rate * 100, 2) AS 达成率
      FROM public.smart_sales_performance
      WHERE region_name IS NOT NULL AND department_name IS NULL
  )
  (SELECT '最高' AS 类型, * FROM branch_data ORDER BY 达成率 DESC LIMIT 1)
  UNION ALL
  (SELECT '最低' AS 类型, * FROM branch_data ORDER BY 达成率 ASC LIMIT 1);
  ```

### 043. 商用四大区域分公司开单排名
- **用户提问**：`商用各大区分公司开单排名是怎样的？`
- **常见错误表现**：把餐饮业务部排了进去。
- **标准答案**：
  1. **华东分公司**：`2,671.54 万元` (达成率 28.12%)
  2. **华南分公司**：`2,460.00 万元` (达成率 30.00%)
  3. **华北分公司**：`1,813.96 万元` (达成率 28.52%)
  4. **西南分公司**：`1,598.27 万元` (达成率 23.03%)
- **标准 SQL**：
  ```sql
  SELECT region_name AS 分公司,
         SUM(target_amount) AS 任务,
         SUM(actual_billing_amount) AS 开单,
         ROUND(SUM(actual_billing_amount)/SUM(target_amount)*100, 2) AS 达成率
  FROM public.smart_sales_performance
  WHERE year='2026' AND node_level='分公司' AND business_line='总额(未拆分)'
  GROUP BY region_name
  ORDER BY 开单 DESC;
  ```
- **改进方案**：大区排名必须加 `条线 = '区域条线'`。

### 044. 商用各大区达成率最高的分公司
- **用户提问**：`商用各大区里哪个分公司达成率最高？`
- **常见错误表现**：答成了开单最高的华东分公司。
- **标准答案**：**华南分公司**（达成率 **`30.00%`** 为第一，东部为 28.12%）。
- **标准 SQL**：`... ORDER BY 达成率 DESC LIMIT 1`。

### 045~055. 业务代表与代表处 TopN（45~55 题口径规范）
- **045. 商用业务代表开单 Top 10**：限定 `层级='业务代表' AND business_line='总额(未拆分)' ORDER BY 开单 DESC LIMIT 10`。
- **046. 各大区内部达成率最低的代表处**：使用 `ROW_NUMBER() OVER (PARTITION BY 上级名称 ORDER BY 达成率 ASC)` 分区求第 1 名。
- **047. 线下业务完成最好的单个分公司**：单点最优问题必须 `LIMIT 1`，不可返回多个。
- **048~055. 极值与排名用例**：严格防范同层混排与除零空值干扰。

---

## 四、动态时间序列（Q1~Q4/环比/同比）类错题（056~070）

### 056. 消费电子事业部 2026 上半年开单情况
- **用户提问**：`今年上半年各区域分公司的开单情况`
- **常见错误表现**：把 1~12 月全加了进去。
- **标准答案**：时间过滤必须严格限定 `月份 BETWEEN 1 AND 6`。
- **标准 SQL**：
  ```sql
  SELECT region_name AS 分公司, SUM(actual_billing_amount) AS 上半年开单
  FROM public.smart_sales_performance
  WHERE year='2026' AND node_level='分公司' AND business_line='总额(未拆分)' AND 月份 BETWEEN 1 AND 6
  GROUP BY region_name ORDER BY 上半年开单 DESC;
  ```

### 057. 各区域分公司开单同比增速 (YoY)
- **用户提问**：`对比今年上半年各分公司相比去年的同比增速`
- **常见错误表现**：没有对去年同期开单做除零保护。
- **标准 SQL**：
  ```sql
  SELECT region_name AS 分公司,
         SUM(actual_billing_amount) AS 今年上半年销售,
         SUM(去年同期开单) AS 去年上半年销售,
         CASE WHEN SUM(去年同期开单)>0 
              THEN ROUND((SUM(actual_billing_amount)-SUM(去年同期开单))/SUM(去年同期开单)*100, 2) 
              ELSE 0 END AS 同比增速
  FROM public.smart_sales_performance
  WHERE year='2026' AND node_level='分公司' AND business_line='总额(未拆分)' AND 月份 BETWEEN 1 AND 6
  GROUP BY region_name ORDER BY 同比增速 DESC;
  ```

### 058. 华南分公司月度环比走势 (MoM)
- **用户提问**：`华南分公司今年前6个月大盘开单的月度环比增速情况`
- **标准 SQL**：
  ```sql
  SELECT 月份, SUM(actual_billing_amount) AS 当月销售,
         LAG(SUM(actual_billing_amount)) OVER (ORDER BY 月份) AS 上月销售,
         CASE WHEN LAG(SUM(actual_billing_amount)) OVER (ORDER BY 月份) > 0 
              THEN ROUND((SUM(actual_billing_amount) - LAG(SUM(actual_billing_amount)) OVER (ORDER BY 月份)) / LAG(SUM(actual_billing_amount)) OVER (ORDER BY 月份) * 100, 2) 
              ELSE 0 END AS 环比增长
  FROM public.smart_sales_performance
  WHERE region_name = '华南分公司' AND node_level = '分公司' AND business_line = '总额(未拆分)' AND year = '2026' AND 月份 BETWEEN 1 AND 6
  GROUP BY 月份 ORDER BY 月份;
  ```

### 059. 华北分公司 Q2 对比 Q1 季环比
- **用户提问**：`华北分公司在今年第二季度相比于第一季度的季环比增长率是多少？`
- **标准 SQL**：利用 `CASE WHEN 月份 IN (1,2,3)` 与 `CASE WHEN 月份 IN (4,5,6)` 在 CTE 中汇总后相减求比率。

### 060~070. 电商与商用时间序列（60~70 题口径规范）
- **060. 电商 Q1~Q4 目标分解**：查询 `q1目标`~`q4目标`（固定各 25%）。
- **061~070. 月度/季度趋势分析**：必须基于 `月份` 维度 GROUP BY，严禁丢失时序字段。

---

## 五、多轮对话、省略指代与多主体对标类错题（071~080）

### 071. 省略表达继承上一轮维度
- **用户对话**：
  - Turn 1: `华东分公司业绩怎么样？`
  - Turn 2: `那南部呢？`
- **常见错误表现**：Turn 2 丢失了 Turn 1 的指标与时间口径，退化为无意义提示。
- **标准答案**：Agent 1 必须沿用 Turn 1 的数据集、维度、时间，仅将 `华东分公司` 替换为 `华南分公司`。

### 072. 两主体对标输出
- **用户提问**：`华东分公司和华南分公司对比一下`
- **常见错误表现**：把两个分公司数据合在一起做 SUM 输出单行。
- **标准答案**：必须输出包含 `华东分公司` 和 `华南分公司` 独立两行的对标表，并给出差异值。

### 073~080. 连续下钻与对标场景
- 保留管理链路维度，禁止将多个主体压扁合并。

---

## 六、比率 HAVING 过滤、零除保护与空值边界类错题（081~090）

### 081. 达成率低于 30% 代表处筛选
- **用户提问**：`达成率低于30%的代表处有哪些？`
- **常见错误表现**：写成 `WHERE 达成率 < 0.3`（行级字段过滤假阳性）。
- **标准答案**：必须在 `GROUP BY region_name` 后的 `HAVING` 子句中重新计算 `SUM(开单)/SUM(任务) < 0.30`。
- **标准 SQL**：
  ```sql
  SELECT region_name AS 代表处, SUM(target_amount) AS 任务额, SUM(actual_billing_amount) AS 开单额,
         ROUND(SUM(actual_billing_amount)/SUM(target_amount)*100, 2) AS 达成率
  FROM public.smart_sales_performance
  WHERE year='2026' AND 层级='代表处' AND business_line='总额(未拆分)'
  GROUP BY region_name
  HAVING CASE WHEN SUM(target_amount)>0 THEN SUM(actual_billing_amount)/SUM(target_amount) ELSE 0 END < 0.30
  ORDER BY 达成率 ASC;
  ```

### 082. 消费者低达成城市分公司预警
- **用户提问**：`哪些城市分公司低于10%风险线？`
- **标准 SQL**：`WHERE 层级='城市分公司' HAVING 达成率 < 10`。

### 083. 地产分公司全为 0 的显式返回
- **用户提问**：`各个分公司地产业务完成情况`
- **常见错误表现**：`WHERE 地产开单 > 0` 导致返回空表。
- **标准答案**：展示 13 个分公司列表，地产开单全显示为 `0 元`。

### 084~090. 空值与边界防护（84~90 题规范）
- 零除保护、`NULLIF`、空字符串与正则清洗安全防护。

---

## 七、任务派发对账、预留额审计与父子勾稽类错题（091~100）

### 091. 华东分公司对账审计
- **用户提问**：`华东分公司分下去的任务对得上代表处指标总和吗？`
- **标准 SQL**：
  ```sql
  WITH parent_target AS (
      SELECT SUM(target_amount) AS p_target FROM public.smart_sales_performance
      WHERE region_name='华东分公司' AND node_level='分公司' AND business_line='总额(未拆分)' AND year='2026'
  ),
  children_sum AS (
      SELECT SUM(target_amount) AS c_target FROM public.smart_sales_performance
      WHERE 上级名称='华东分公司' AND 层级='代表处' AND business_line='总额(未拆分)' AND year='2026'
  )
  SELECT p_target AS 大区官方总指标, c_target AS 代表处派发指标和, (p_target - c_target) AS 未分配预留额
  FROM parent_target, children_sum;
  ```

### 092. 北京代表处对账审计
- **用户提问**：`北京代表处总预算和业务代表总和是否有未分配差额？`
- **标准 SQL**：代表处 CTE 对比业务代表 CTE 求差额。

### 093~100. 集团至分公司各级对账与防笛卡尔积规范
- 对账必须采用双 CTE 分别求和再做差，严禁单表 JOIN 产生笛卡尔积。

---

## 八、100 题错题库对账速查表（核心指标 Ground Truth 索引）

| 业务主体 | 指标口径 | Ground Truth 标准值 | 核心防错规则 |
| :--- | :--- | :--- | :--- |
| **企业服务事业部总体** | target_amount / actual_billing_amount / 达成率 | **17.8971 亿 / 9.6818 亿 / 54.10%** | `分公司 IS NULL` 防三级翻倍 |
| ├── **线下主业务** | 实际开单 / 占比 | **8.2188 亿 (84.89%)** | 提取 `线下-actual_billing_amount` |
| ├── **新零售板块** | 实际开单 / 占比 | **1.0473 亿 (10.82%)** | 提取 `新零售-actual_billing_amount` |
| ├── **地产配套** | 实际开单 / 占比 | **2,831.72 万 (2.92%)** | 仅事业部总部有数，分公司全为 0 |
| └── **燃气定制** | 实际开单 / 占比 | **1,325.08 万 (1.37%)** | 提取 `燃气定制-actual_billing_amount` |
| **消费者开单 Top 1** | 分公司名称 / 开单额 | **华北分公司 / 1.0479 亿元** | 排除城市分公司 |
| **消费者达成率最高** | 分公司名称 / 达成率 | **山东分公司 / 53.91%** | 豫晋 51.88% 次之 |
| **消费者达成率最低** | 分公司名称 / 达成率 | **江浙沪分公司 / 32.35%** | 川藏 37.89% 倒数第二 |
| **消费电子事业部大盘** | 全年开单总额 | **85,437,688.57 元 (8,543.77 万)** | `business_line='总额(未拆分)'` 防翻倍 |
| ├── **华东分公司** | 开单 / 达成率 (大区第 1) | **2,671.54 万元 / 28.12%** | 锁定 `node_level='分公司'` |
| ├── **华南分公司** | 开单 / 达成率 (达成率第 1) | **2,460.00 万元 / 30.00%** | 锁定 `node_level='分公司'` |
| ├── **华北分公司** | 开单 / 达成率 (大区第 3) | **1,813.96 万元 / 28.52%** | 锁定 `node_level='分公司'` |
| └── **西南分公司** | 开单 / 达成率 (大区第 4) | **1,598.27 万元 / 23.03%** | 锁定 `node_level='分公司'` |
| **商用餐饮业务部** | 行业条线开单 / 达成率 | **4,530.25 万元 / 43.15%** | 锁定 `条线='行业条线'` |
