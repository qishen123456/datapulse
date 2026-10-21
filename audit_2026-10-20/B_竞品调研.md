# B. 智能问数 / Agentic Analytics 竞品调研

- 调研日期：2026-10-20
- 调研员：competitor-researcher
- 证据分级约定：**官方确认**（官方文档/官网/官方新闻稿原文）｜**文档可推导**（官方文档内容可直接推出）｜**第三方推测**（社区/媒体/博客）｜**营销口径**（官网宣传语，无机制细节）
- 所有链接均为调研当日可访问的公开页面；文档「更新日期」以页面标注为准。

---

## 0. DataBuddy 身份核验专区（重点）

### 结论：✅ 已确认 = 腾讯云 DataBuddy（大数据智能体工作台，Agent 原生 Data+AI 一体化平台）

**证据链：**

1. **腾讯云官方产品文档（官方确认）**
   - 《大数据智能体工作台 DataBuddy 产品概述》：https://cloud.tencent.cn/document/product/1835/135576 ，页面标注"最近更新时间：2026-09-11"。
   - 摘录：「DataBuddy 是腾讯云推出的 Agent 原生（Agent-Native）、全托管的 Data + AI 一体化数据智能平台……通过统一元数据与语义层，为企业提供从数据接入、数据工程、数据科学、数据分析到数据治理的端到端全链路能力」「三大 Agent：工程 Agent（DataBuddy-Engineering）、治理 Agent（DataBuddy-Governance）、分析 Agent（DataBuddy-Analysis：自然语言问数、分析报告生成、指标波动归因、AI 搭建可视化看板、主动推送）」。
   - 国际站产品功能文档：https://intl.cloud.tencent.com/zh/document/product/1332/83758 ，明确列出「数据分析：智能问数（结合语义层秒级取数）、AI 生成分析报告、主动智能归因、AI 生成看板、数据探索、分析空间」「统一语义层 Unity Semantics：本体建模标准化实体/指标/维度/业务逻辑，NL2SQL 准确率：无语义层 60%~70%，完整语义层 90%+」「Agent 安全防护：双向 Agent Guardrails、OBO 权限强绑定、高危 SQL 拦截」。

2. **官方新闻稿（官方确认，含发布时间线）**
   - 2026-06-05 腾讯云 AI 产业应用峰会宣布面向 Agent 的全栈数据平台升级，三层架构 = DataBuddy（生产级数据智能体）+ WeData（数据智能平台）+ AI 原生数据底座；「今年 5 月开放内测以来，DataBuddy 已吸引超 3000 家企业申请试用」。链接：https://www.tencentcloud.com/dynamic/news-details/101263 ；中文媒体转载（中国日报网财经，2026-06-08）：https://caijing.chinadaily.com.cn/a/202606/08/WS6a26611aa310942cc49b07ed.html
   - 2026-09-23 官方发布稿《Tencent Cloud Launches Tencent Cloud DataBuddy, an Agent-Native Data + AI Workbench》：DataBuddy 是腾讯「继 CodeBuddy、WorkBuddy 之后的第三个助手级产品」，四大 Agent 场景（Data Engineering / Governance / Analytics / Science），三大底座（Unity Semantics 语义层——宣称分析准确率 95.9% vs 纯 NL2SQL 83.5%；Agent Runtime；OneOps）。官方门户：https://databuddy.tencentcloud.com/website ；新闻稿：https://www.tencentcloud.com/dynamic/news-details/101532
   - WeData 官网产品页（DataBuddy 作为其 Agent 入口）：https://wedata.cloud.tencent.com/website ，摘录「Agent 原生 让 Agent 把活儿做完……覆盖工程、治理与分析。从 Copilot 到 Autopilot，再到 Multi-Agent 多智能体协同」「05 数据分析：探索 · 看板 · 智能问数 · 异动归因」。

3. **本地插件旁证（文档可推导，非公开官方资料）**
   - 本机插件 `/Users/ltq/.workbuddy/plugins/marketplaces/experts/plugins/workbuddy-data-expert-team/README.md`：自述「基于 DataBuddy 数据知识库（企业真实数据）」，成员 = DataBuddy 数据分析专家（智能问数、指标统计、趋势对比、归因分析、趋势预测、相关性、异动检测、智能看板、分析报告）+ DataBuddy 数据治理专家（资产盘点、质量规则、剖析、异常检测、敏感分类、语义模型管理、Unity Catalog 元数据治理、血缘）。许可字段写「Proprietary · WeData Team」。
   - `agents/databuddy-analyst.md`：通过 `wedatacli` CLI 与 DataBuddy 平台交互；控制台默认域名 `databuddy.cloud.tencent.com`；分析侧命令 `query-data`（自然语言取数，内部自动完成**语义层 / text2sql 双路路由与降级**）、`predict-data`（Prophet 时序预测）、`correlate-data`（Spearman 相关 + 残差法偏相关）、`attribute-data`（两期对照维度归因 + 自动根因下钻）、`detect-anomaly`（单指标时序 sigma 异常扫描）；看板产物链接格式 `https://<consoleDomain>/dashboard/aiBoard/<AccessKey>`。
   - `agents/databuddy-governor.md`：语义模型/指标/维度管理（semantic-manage）、Unity Catalog 元数据治理、质量规则/剖析/异常检测、敏感分类；治理产出的语义模型可"挂载到分析空间"供分析侧引用。
   - 旁证与官方文档完全互洽：「分析空间」对应官方"分析空间"概念；「Unity Catalog / 语义层 / Unity Semantics」「治理 Agent + 分析 Agent 分工」「看板/归因/预测/异动」均一一对应。**可判定本环境插件即腾讯云 DataBuddy 的 WorkBuddy 侧接入。**

4. **同名歧义检索**：以 `"DataBuddy" -tencent -tencentcloud` 检索，返回结果仍全部为腾讯云 DataBuddy 相关页面，未发现数据分析领域内其他同名主流产品。（检索范围内无歧义；不排除长尾小产品同名。）

### DataBuddy 问数链路还原（官方文档 + 本地插件自述互证）

问题理解（意图识别 + 澄清规则）→ 工作空间/数据知识库（分析空间）选择 → 语义检索（`ll`/`cat table://`/`cat semantic-model/` 召回表、字段、指标）→ 澄清（专用工具调用前的"前置澄清"契约，禁止模糊直传）→ 查询路由（`query-data` 内部"语义层 / text2sql 双路路由与降级"）→ 执行（DLC 等引擎，按用户身份权限）→ 结果复核（返回 `Stmt(SQL)`、`Fallback History`、`Source`/`Metric` 分节，可追溯）→ 可视化（`--draw` 服务端出图，draw_spec DSL + COS 签名链接）→ 解释（findings JSON：`conclusion` + `quant` + `caveats`，归因/相关性强制附"相关≠因果"等 caveat）→ 追问/多轮（Agent maxTurns=100，复杂任务先 Plan）→ 记忆/反馈（官方媒体稿提到"归因分析基于六层知识体系：从底层表结构、统一指标口径，到企业业务术语、**个人使用记忆**，层层递进"——记忆机制仅见此一处表述，属官方媒体口径）→ 质量评估（官方宣称语义层下 NL2SQL 准确率 90%+ / 95.9%，未见公开的评估工具链文档）。

---

## 1. 阿里云 Quick BI 智能小Q

**一句话定位**：BI 平台内的"超级数据分析师"入口，意图识别路由到问数/解读/报告/搭建/搜索等多个子 Agent。

**官方链接与日期：**
- 《Quick BI Intelligent Q》（英文官方帮助，标注 Updated: 2026-04-05）：https://help.aliyun.com/en/quick-bi/user-guide/smart-q-home-page —— 智能小Q整合 **Q-DataQuery（问数）、Q-Insight（数据解读/异动洞察）、Q-Report（报告）、Q-Build（报表搭建）、Q-Search（资源搜索）** 多个 Agent，基于意图识别自动规划路由；各 Agent 为增值模块单独售卖，仅高级版/专业版支持。
- 《轻松上手 Quick BI 智能小Q》（官方新手引导）：https://help.aliyun.com/zh/quick-bi/getting-started/smartq-novice-guide —— 功能亮点表（官方确认）：自然语言解析过程展示（含问数数据集、相关字段、已维护的数据集知识、用户意图）、**SQL 自助取数（可查看取数 SQL 伪代码）**、图表展示与自定义切换、**追加提问（基于上一提问自动补齐维度和度量限定=多轮上下文）**、趋势分析、**趋势预测（统计模型）、波动归因（可配置对比周期、分析业务维度）**、**数据解读（可选不同大模型，输出数据发现/结论/建议）**、占比/排行/明细识别；并提供「问数调优」章节（意图解析偏差/指标取数逻辑错误时的调优手段）。
- 《智能小Q Skill 操作手册》：https://help.aliyun.com/zh/quick-bi/user-guide/quick-bi-open-skill-manual —— 开放 API/Skill 形态：「问数过程中自动完成推理分析、SQL 生成、OLAP 取数以及结果可视化输出」「支持**自动智能选表**（未指定数据集时，自动从用户有权限的数据集中匹配最合适的）」「实时输出推理过程、SQL、图表和分析结论」；权限按用户 token 映射。
- 《AIPro Skill 操作手册》（标注更新时间 2026-09-15）：https://help.aliyun.com/zh/quick-bi/user-guide/aipro-skill —— AIPro Skill 接入企业自有 Agent/第三方 Agent（千问办公、Claude Code、Codex）：问数、AI 报表、报告生成、**会话管理（同一会话多轮追问、保留上下文）**、任务管理（发起/查询状态/取消）、按映射用户身份校验权限。
- 《与智能体对话》：https://help.aliyun.com/document_detail/2876496.html —— 超级框基于意图识别自动路由至官方/自定义 Agent；建议新建智能体时填写功能描述与代表性示例问题以提升路由准确率。
- 解决方案页《分析 Agent 实现一键 AI 数据洞察》：https://cn.aliyun.com/solution/tech-solution-deploy/2929617 —— 四类 Agent 串联演示：小Q搭建 Agent、小Q问数 Agent、小Q解读 Agent、小Q报告 Agent；问数配置含「学习数据集 → 字段质量评估 → 快捷提问（系统推荐）→ 问数权限授权」。

**问数链路还原（官方确认）**：提问（语音/文字/快捷提问）→ 意图识别路由（超级框）→ 数据集选择（用户指定或**自动智能选表**，限定在用户有问数权限的数据集内）→ 自然语言解析（展示数据集/字段/数据集知识/意图）→ SQL 生成（可查看 SQL 伪代码；**未找到"业务 SQL 与执行 SQL 双层展示"的官方表述**，仅有"查看 SQL 伪代码/底层查询语句"）→ OLAP 取数 → 图表展示（自动选型+可切换）→ 数据解读（可选 LLM）→ 波动归因/趋势预测（趋势图上直接触发）→ 追加提问（自动继承上轮维度/度量）→ 点赞/点踩、重新生成、应用到报告。**歧义澄清**：未找到小Q主动向用户反问澄清的官方功能描述（仅有"快捷提问/推荐问题"引导），标注**未找到证据**。**记忆**：未找到跨会话记忆的官方描述（AIPro 会话管理仅限同一会话上下文）。

---

## 2. Databricks AI/BI Genie（Genie Agent）

**一句话定位**：以 Genie space/Agent 为"本地知识库"的对话式分析，强治理（Unity Catalog），强调基准评测与人工复核闭环。

**官方链接与日期：**
- GA 公告《AI/BI Genie is now Generally Available》（2025 年 6 月 Data+AI Summit 期间，官方博客）：https://www.databricks.com/blog/aibi-genie-now-generally-available —— Genie space = 「本地知识库（local knowledge store），打包数据资产 + 语义（指标定义、示例查询、文本指令、认证资产）」；新增 **value dictionaries（值字典，语义匹配字面量）**、Unity Catalog Metric Views 支持、**Benchmarks（基准测试）与 Ask for Review（请求复核）**；预告 **Genie Deep Research**（多步骤"why/how"问题：产出研究计划、并行分析多个假设、结论附引用）。
- AI/BI 2025 Release Notes（官方文档）：https://docs.databricks.com/aws/ai-bi/release-notes/2025 —— **命名变化：「Genie Agents (formerly Genie Spaces)」**（2025-03 起官方文档统一改称 Genie Agent）；Genie Conversation API 进入 Public Preview；「Genie now self-reflects：生成 SQL 时自我反思修正，改善过滤条件编写、减少 SQL 错误」；权限：用户须对空间内 Unity Catalog 对象至少有 SELECT 权限才可返回结果。
- Genie Agents API 文档（官方）：https://docs.databricks.com/aws/en/genie/conversation-api —— `serialized_space` 配置结构：`data_sources`（tables/metric_views，含 column_configs 如 `build_value_dictionary`）、`instructions`（text_instructions、**example_question_sqls（示例问句-SQL，支持参数与 usage_guidance）**、sql_functions、**join_specs（预定义表关联，含关系类型注解如 MANY_TO_ONE）**、**sql_snippets（filters/expressions/measures 可复用 SQL 表达式）**）、**benchmarks（评估用问题 + ground-truth SQL）**。
- Trusted assets 官方文档（Microsoft Learn 镜像/Azure Databricks）：https://learn.microsoft.com/en-my/azure/databricks/genie/trusted-assets —— **Trusted assets = 预定义的参数化示例 SQL 与 UDF（注册在 Unity Catalog），命中时直接执行并标注"trusted asset"**；定位：高频、关键、要求精确一致答案的问题；与普通示例 SQL 的区别：trusted asset 命中即运行既定 SQL，否则示例仅作生成参考。
- Benchmarks 与 Request Review 官方博客：https://www.databricks.com/blog/building-confidence-your-genie-space-benchmarks-and-ask-review —— Benchmarks：作者添加测试问题+标准 SQL，一键运行，判定 Correct / Needs Review（结果集精确匹配），在 Evaluations 页追踪准确率随配置变更的变化；Request Review：终端用户对有疑问的回答发起复核，space 管理员在 History 页核对原始提问与生成 SQL、标注正确或修正，用户收到通知——**形成"用户标记→专家修正→回流指令"闭环**。
- 最佳实践（官方博客）：https://www.databricks.com/blog/how-build-production-ready-genie-spaces-and-build-trust-along-way 与 https://databricks.com/blog/data-dialogue-best-practices-guide-building-high-performing-genie-spaces —— 「先建 10-20 题基准集再开发」「上下文缺口诊断→单变量迭代→重跑基准」方法论；「Genie 不会在上下文不足时强行生成 SQL（防幻觉设计）」。

**问数链路还原（官方确认）**：提问 → space 内语义检索（知识库：表/列描述、值字典、同义词、join 关系、metric views）→ SQL 生成（self-reflection 自纠）→ 执行（继承 Unity Catalog 权限，行/列级安全由 UC 保证）→ 回答附"如何得出答案"的解释与生成的 SQL（可查看）→ 多轮追问 → 反馈（评分 + Request Review）→ 作者侧 Benchmarks 回归评估 + Monitoring 页看常见问题。**歧义澄清**：官方文档未强调主动反问澄清（更靠 value dictionary / 指令消解歧义）；**记忆**：知识提取（knowledge extraction，从对话中提炼语义片段经用户确认后写入知识库）属于"会话→知识库"的学习闭环，官方确认于 GA 公告。

---

## 3. ThoughtSpot Spotter / Spotter Semantics / Agentic Analytics

**一句话定位**：以"确定性查询生成 + 可验证语义层"为底座的多 Agent 分析平台（Spotter/SpotterModel/SpotterViz/SpotterCode）。

**官方链接与日期：**
- Spotter agents 官方文档首页（ThoughtSpot Cloud Docs，当前文档版本流 26.x，2026 年）：https://docs.thoughtspot.com/cloud/10.8.0.cl/index.html —— 四个 Agent 分工：**Spotter（对话式洞察）、SpotterModel（原始数据→语义建模）、SpotterViz（规划叙事并自动搭建 Liveboard）、SpotterCode（IDE 内 AI 编码/嵌入式分析）**；并有「Spotter semantics」语义层专章。
- 《Semantic layer》官方文档：https://docs.thoughtspot.com/cloud/latest/semantic-layer —— Spotter Semantics 三支柱：**Human-verified definitions（人审定义，token 化，业务用户可众包定义而无需 SQL）**、**Built for agents（语义模型以 Agent 可直接消费的格式存储）**、**Deterministic query generation（不用 LLM 直接生成自由 SQL，而是专有的、按数据库方言的查询编译器；行/列级安全强制作用于每条查询；支持 galaxy/多星 schema、自定义日历 4-4-5、cohort、LOD）**。核心主张：「agents can interpret intent probabilistically and return deterministic results」。
- 《Coaching Spotter》官方文档（版本 26.6.0.cl）：https://docs.thoughtspot.com/cloud/26.6.0.cl/spotter-coaching-options —— 调优工具体系：Spotter instructions、Data model instructions、**Reference questions（参考问题，供相似问题推理泛化）**、**Business terms（刚性业务术语定义）**、**Memory（AI 生成的上下文层：从指定的可信 Liveboards 或对话中的定义/纠正自动生成，与既有 coaching 叠加；对话中教的纠正会存为 memory 应用于后续问题）**。官方明确「coaching 不存储答案、不保证相同响应，只影响推理」。
- 产品页（营销口径，含能力清单）：https://www.thoughtspot.com/product/agents —— 「Spotter reasons through each step and shows how it got there（多步推理、过程可追溯）」「Memory keeps your business definitions consistent across every follow-up」「Questions become **verifiable search tokens**, not free-form SQL」「Human in the Loop：只读工具自由执行，**写/删外部应用的动作须用户批准**」「同一语义层 + 同一安全模型服务所有 Agent」；https://thoughtspot.com/product/analytics —— 「Every answer is compiled into governed SQL, so the same question returns the same number every time（同问同答）」「Conversation monitoring（对话监控）+ Coaching and Optimization（反馈闭环）」。
- Spotter Semantics 官方博客：https://www.thoughtspot.com/blog/spotter-semantics —— TML（ThoughtSpot Modeling Language）Analytics-as-Code：版本控制、CI/CD、自动化测试；Open Semantic Interchange（OSI，语义模型开放标准，ThoughtSpot 为创始成员）。

**问数链路还原（官方确认/文档可推导）**：自然语言提问 → Spotter 多步推理（展示每一步逻辑）→ 语义层解析（指标定义、join 逻辑、财务日历、RLS/CLS）→ **确定性查询编译（非自由 SQL 生成）** → 执行（live query 零拷贝，30+ 数据源）→ 结果可下钻到行、可验证（search tokens）→ 追问（Memory 保持业务定义一致）→ 反馈（对话监控 + coaching 回流）；SpotterModel 负责建模、SpotterViz 负责看板叙事规划、SpotterCode 负责嵌入交付。**假设检查/多步骤**：官方宣传 Spotter 3「multi-step reasoning, validates its own work」（营销口径，机制细节未公开）。

---

## 4. Snowflake Cortex Analyst / Cortex Agents / Verified Query Repository

**一句话定位**：语义模型 YAML 驱动的 NL2SQL 服务（Cortex Analyst）+ 结构化/非结构化混合编排（Cortex Agents）+ 已验证问句-SQL 库（VQR）的准确率闭环。

**官方链接与日期：**
- 《Cortex Analyst Verified Query Repository》官方文档：https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-analyst/verified-query-repository —— **VQR：语义模型 YAML 中 `verified_queries` 段维护"问题→已验证 SQL"对**（含 verified_at/verified_by/use_as_onboarding_question 元数据）；命中相似问题时复用该 SQL，API 响应 `confidence` 字段可见使用了哪条 verified query；**已验证 SQL 必须使用语义模型中的逻辑表/列名（逻辑表名前加 `__` 前缀），而非底层物理名**；配套开源 semantic-model-generator Streamlit 应用（聊天生成 SQL→人工校验→"Save as verified query"→上传 YAML）；Snowsight 还提供 **Verified Query Suggestion（基于用户行为推荐新 verified queries）**。
- 《Getting Started with Cortex Analyst》官方指南：https://www.snowflake.com/en/developers/guides/getting-started-with-cortex-analyst/ —— 「verified queries 作为 few-shot 示例显著提升准确率」；建议起步 3-5 张表、每表 10-20 列；「Cortex Analyst 使用 agentic AI setup + SOTA LLM 达成高 text-to-SQL 准确率」；RBAC 集成。
- 《Cortex Agents》官方文档：https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents —— 工作流四要素：**规划（结构化/非结构化任务编排）、探索选项（对模糊问题枚举多种解释以消歧）、拆分子任务、跨工具路由（Cortex Analyst / Cortex Search / 自定义存储过程与 UDF）+ 反射（每次工具调用后评估结果，决定澄清/迭代/最终回答）**；**Threads 对象持久化多轮上下文**（客户端不必自管）；显式反馈机制（正/负评分 + 文本）；**Cortex Agent evaluations（Goal-Plan-Action 框架：答案正确性、逻辑一致性；工具选择/执行指标 preview）**；运行时 Guardrails（提示注入/越狱检测，含工具调用间接注入）；「Snowflake 不保证 LLM 答案准确性，须人工复核后再面向用户」。
- Agent 编排官方指南页：https://www.snowflake.com/en/artificial-intelligence/agents/agent-orchestration/ —— 明确「原则上是**单 Agent 编排模型**：一个 Cortex Agent 管理任务并在已配置工具中选择；工具本身可以是复杂服务甚至其他 Agent」「Evaluate the path as well as the result（评估路径而不仅是结果）」。

**问数链路还原（官方确认）**：提问 → Cortex Agents 规划/消歧/拆任务 → 路由到 Cortex Analyst（语义模型 YAML：逻辑表、维度、度量、同义词、示例值）→ SQL 生成（命中 VQR 则复用 verified SQL）→ 执行（RBAC，调用方角色权限）→ 反射（评估工具结果，必要时澄清/迭代）→ 回答（含 SQL 与 confidence）→ 多轮（thread）→ 反馈（评分/文本）→ 评估迭代（evaluations + VQR suggestion 回流语义模型）。**可视化/看板**：非 Cortex 职责（REST API 输出，由 SiS/前端承载），标注**不适用/未找到证据**。

---

## 5. Microsoft Fabric Data Agent

**一句话定位**：Fabric 内可配置的问答型 Agent（原 AI skill），靠"指令 + 数据源说明 + 示例查询"三件套提升 NL2SQL 质量；2026 年处于向 Fabric IQ 迁移的过渡期。

**官方链接与日期：**
- 《Data agent configurations》官方文档：https://learn.microsoft.com/en-us/fabric/data-science/data-agent-configurations —— 配置体系：**Data agent instructions（Agent 级：目标、数据源优先级、术语、回答规范、常见主题处理）**；**Data source instructions（数据源级：表/列/关系/查询逻辑）**；**Data source description（帮助 Agent 路由选择数据源）**；**Example queries（few-shot：命中数据源后自动检索最相关的 top-3 示例注入生成过程）**；Schema object descriptions（preview 运行时）；**Topics（preview：大型主题化指令，按问题相关性只注入匹配段落）**。
- 最佳实践官方文档：https://learn.microsoft.com/fabric/data-science/data-agent-configuration-best-practices —— 「限制所选 schema（无关对象增加歧义）」「对复杂逻辑使用示例查询」「测试并细化上下文」。
- 概念页《Data agent concept》：https://learn.microsoft.com/en-us/fabric/data-science/concept-data-agent —— 「识别正确的数据源后，Fabric data agent 会**改写问题（rephrase）使其清晰结构化**，再调用对应工具生成结构化查询（SQL/DAX/KQL）」（官方确认的中间改写步骤）。
- Foundry 集成文档（重要状态变化，官方确认）：https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/tools/fabric —— **「Foundry 代理服务中的 Microsoft Fabric 数据代理工具计划于 2026-11-06 弃用，请改用 Fabric IQ 工具」**；身份传递（On-Behalf-Of）授权；数据源最低权限表（Power BI 语义模型 Read 且 RLS/CLS 继续生效、Lakehouse/Warehouse/KQL/镜像库/Ontology/Microsoft Graph）；**不支持服务主体认证**；NL2SQL 所用模型不受编排模型选择影响。
- Fabric 2026 年 6 月功能汇总（官方博客）：https://community.fabric.microsoft.com/（Fabric Updates Blog, June 2026 Feature Summary）—— **Data agents in Microsoft 365 Copilot 正式 GA**（长查询不超时）；**Creator Agent（preview：AI 辅助生成/迭代 agent 指令、数据源指令、示例查询配置）**；**Preview Runtime（预览运行时：新版 NL2SQL 工具集——更好利用示例查询、**意图模糊时主动追问澄清（asks clarifying questions）**、超出示例范围时智能探索数据、运行步骤/命中示例/结构化诊断可见）**；跨数据源路由改进（综合 schema、示例查询、数据源描述信号）；**Code Interpreter 工具（preview：Python 统计分析/预测/可视化）**。
- 状态边界说明（第三方梳理）：https://dataworkers.io/blog/microsoft-fabric-data-agents-vs-data-workers/ —— 「概念页（2026-09-29 更新）称已 GA，AI 发布状态表（2026-07-12 更新）仍列 preview；Copilot Studio 集成 2026-08 GA；服务主体支持与 Foundry 集成仍 preview」——**API/集成面状态碎片化，引用时须注明具体面**。（第三方推测，但与官方弃用公告互洽。）

**问数链路还原（官方确认）**：提问 → 数据源路由（描述/schema/示例查询信号）→ 问题改写（rephrase）→ 工具调用生成 SQL/DAX/KQL（few-shot top-3 示例注入；preview 运行时支持主动澄清追问）→ 以最终用户身份执行（OBO，RLS/CLS 生效）→ 只读查询返回 → 回答生成；多轮上下文官方支持（文档可推导）；**验证器/评估**：Creator Agent 提供"setup and test workflow（审查并接受 AI 生成的配置更新）"，未见独立的自动回归评估套件官方文档（部分支持）。**记忆**：未找到跨会话记忆官方描述（未找到证据）。

---

## 6. 开源方案补充

### Vanna（vanna-ai/vanna，MIT）
- GitHub：https://github.com/vanna-ai/vanna 。机制（官方 README/文档口径）：**RAG-to-SQL**——训练数据（DDL/文档/SQL 对）入向量库，提问时检索相关上下文生成 SQL；前端/LLM/向量库全解耦；生成 SQL 报错可自动反馈修正；支持 self-learning（成功执行的 SQL 可自动入训练集）。
- ⚠️ 第三方信息（https://www.hqwc.cn/a/760381.html ，2026 年文章）：GitHub API 快照显示 vanna-ai/vanna 已 **archived=true**（约 23.8k stars）——**官方仓库归档状态请以 GitHub 页面实时为准**（第三方推测）。

### WrenAI（Canner/WrenAI，AGPL-3.0）
- GitHub：https://github.com/Canner/WrenAI ；官网：https://wrenai.cn/ 。机制：**语义建模层（MDL）+ RAG**——先定义业务术语与表关系，LLM 基于语义层而非裸 schema 生成 SQL；问句-SQL 对积累实现持续学习；GenBI（问数→图表→仪表盘→API）。
- 第三方对比（https://sudiptapathak.com/blog/dissecting-open-source-nl2sql ）：Vanna≈22k stars（RAG+agent）、WrenAI≈14k stars（semantic model + RAG + transpiler）、DB-GPT≈17k stars（多 Agent）；WrenAI 语义层架构"面对复杂表结构准确率更值得借鉴"（第三方推测）。

---

## 7. 竞品对比表

单元格取值：**官方确认** ｜ **部分支持** ｜ **未找到证据** ｜ **不适用**

| 产品 | 官方证据/链接 | 数据语义/指标治理 | Golden/Verified SQL | 自动选数据源 | 歧义澄清 | 多轮上下文 | 多步骤/多Agent分析 | 记忆能力 | SQL/结果可追溯 | 自动验证/回归 | 可借鉴的机制 | 对本系统适配难度 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 腾讯云 DataBuddy | cloud.tencent.cn/document/product/1835/135576（2026-09-11）；发布稿 2026-06-05/2026-09-23 | 官方确认（Unity Semantics 本体/指标/维度；语义层下 NL2SQL 90%+） | 部分支持（插件自述"语义层/text2sql 双路路由与降级"；未见公开 Golden SQL 库文档） | 官方确认（分析空间绑定资源=显式空间选择；空间内需用户确认） | 官方确认（插件自述四大专用工具"前置澄清"契约、禁止模糊直传；面向用户 AskUserQuestion） | 官方确认（Agent 多轮，maxTurns=100；复杂任务先 Plan） | 官方确认（工程/治理/分析三 Agent + Plan 编排；归因/预测/异动/相关性专用工具） | 部分支持（官方媒体稿提"个人使用记忆"六层知识体系；无机制文档） | 官方确认（返回 Stmt(SQL)/Source/Metric/Fallback History；findings 含 caveats） | 部分支持（官方宣称准确率数字；未见公开评估工具） | 专用分析工具前置澄清契约；重试意图锁；分析空间=资源白名单 | 低-中（同云同体系，CLI 契约可直接对标） |
| 阿里云 Quick BI 智能小Q | help.aliyun.com/en/quick-bi/user-guide/smart-q-home-page（2026-04-05）；aipro-skill（2026-09-15） | 官方确认（数据集问数配置：学习数据集、字段质量评估、问数调优） | 部分支持（快捷提问/推荐问题；未见 Golden SQL 库） | 官方确认（未指定时自动从有权限数据集中智能选表） | 未找到证据（仅推荐问题引导，无主动反问澄清的官方描述） | 官方确认（追加提问自动补齐上轮维度度量；AIPro 会话管理） | 官方确认（Q-DataQuery/Insight/Report/Build/Search 五 Agent 意图路由；波动归因/趋势预测） | 未找到证据（跨会话记忆无官方描述） | 官方确认（展示解析过程+SQL 伪代码+查看底层查询语句） | 部分支持（问数调优指南、点赞点踩；无自动回归） | 意图路由超级框；问数配置前置（学习数据集+字段质量评估） | 低（BI 内嵌形态，机制透明） |
| Databricks Genie Agent | databricks.com/blog/aibi-genie-now-generally-available（2025-06 GA）；docs.databricks.com/aws/en/genie/conversation-api | 官方确认（Knowledge Store：列级同义词/采样值、join 关系、UC Metric Views、值字典） | 官方确认（trusted assets=参数化示例 SQL/UDF 命中即执行并标注；example_question_sqls） | 部分支持（space 即数据源边界，space 内多表自动选；跨 space 需路由层） | 部分支持（靠值字典/指令消歧；未见主动反问澄清官方描述） | 官方确认（Conversation API 多轮对话） | 官方确认（Deep Research preview：研究计划+多假设并行+引用；self-reflection 自纠） | 官方确认（knowledge extraction：对话中提炼语义片段，用户确认后入知识库） | 官方确认（每个回答附生成 SQL 与解释；trusted asset 标注；audit logs） | 官方确认（Benchmarks 标准 SQL 对拍 Correct/Needs Review + Evaluations 追踪 + Request Review 人工复核闭环） | Benchmarks+Request Review 闭环；trusted assets 分级信任；值字典 | 中（Benchmarks/Review 机制轻量可抄；Knowledge Store 全量照搬成本高） |
| ThoughtSpot Spotter | docs.thoughtspot.com/cloud/latest/semantic-layer；spotter-coaching-options（26.6.0.cl） | 官方确认（Spotter Semantics：人审定义、token 化众包、TML as-code、RLS/CLS 编译进每条查询） | 部分支持（Reference questions 供泛化推理；官方明确 coaching 不存答案不保证同响应） | 官方确认（Spotter 跨 Model/数据源；语义层统一定义） | 官方确认（coaching 目标即"resolve ambiguity""reduce repeated clarification"） | 官方确认（多轮追问；Memory 保持跨追问定义一致） | 官方确认（Spotter/Model/Viz/Code 四 Agent；Spotter 多步推理+自我校验） | 官方确认（Memory：从可信 Liveboards 与对话纠正自动生成的 AI 上下文层） | 官方确认（verifiable search tokens 而非自由 SQL；同问同答；对话监控） | 部分支持（TML CI/CD+自动化测试属工程实践；未见内置问数回归套件文档） | 确定性查询编译（LLM 不定 SQL）；Memory 自动上下文层；人审 token 化定义 | 高（确定性查询编译器是多年自研引擎，不宜照搬；Memory/coaching 分层可借鉴） |
| Snowflake Cortex Analyst/Agents | docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-analyst/verified-query-repository；cortex-agents | 官方确认（语义模型 YAML：逻辑表/维度/度量/同义词/示例值；semantic views） | 官方确认（VQR：verified_queries 段、命中复用、confidence 可见、Snowsight 基于用户行为推荐新增） | 官方确认（Agents 跨 Analyst/Search/自定义工具路由；Analyst 内按语义模型） | 官方确认（Agents"探索选项"枚举解释消歧 + 反射阶段可请求澄清） | 官方确认（Threads 对象持久化上下文） | 官方确认（规划→拆子任务→工具路由→反射；单 Agent 编排模型） | 部分支持（反馈评分+文本回流；无自动记忆层官方描述） | 官方确认（响应含 SQL 与 confidence；官方要求人工复核后上线） | 官方确认（Agent evaluations：Goal-Plan-Action 框架，答案正确性/逻辑一致性；VQR suggestion 闭环） | VQR（问题-SQL 对+验证人元数据+命中可见）；语义模型 YAML 单文件治理；Goal-Plan-Action 评估 | 低-中（VQR 与 YAML 语义模型是中小系统可直接照搬的范式） |
| Microsoft Fabric Data Agent | learn.microsoft.com/en-us/fabric/data-science/data-agent-configurations；foundry/tools/fabric（2026-11-06 弃用公告） | 部分支持（指令三件套+schema 描述；无独立指标语义层，依赖 Power BI 语义模型） | 官方确认（example queries few-shot，命中源后检索 top-3 注入；非"命中即执行"） | 官方确认（数据源描述+schema+示例综合信号路由；2026-06 路由改进） | 官方确认（preview 运行时 NL2SQL：意图模糊时主动追问澄清） | 官方确认（多轮对话；M365 Copilot 长查询支持） | 部分支持（单 Agent + Code Interpreter 工具；无多 Agent 编排官方描述） | 未找到证据 | 官方确认（运行步骤/命中示例/结构化诊断可见；问题改写中间态可见） | 部分支持（Creator Agent 引导式配置+测试 workflow；无自动回归套件文档） | 示例查询 top-3 检索注入；数据源级指令分层；⚠️ 产品面正向 Fabric IQ 迁移，API 状态碎片化 | 中（机制简单可抄；但产品本身处于迁移期，不宜深度对齐其 API） |
| WrenAI（开源） | github.com/Canner/WrenAI；wrenai.cn | 官方确认（MDL 语义建模层：术语与表关系先建模再生成） | 官方确认（问句-SQL 对积累=持续学习） | 部分支持 | 部分支持（Ask 流程含追问澄清，官方文档级证据有限） | 官方确认（多轮对话） | 部分支持（GenBI 问数→图表→看板流水线） | 部分支持（问句-SQL 对积累） | 官方确认（生成 SQL 可见） | 未找到证据 | 语义层优先于裸 schema 的架构；AGPL 注意商用合规 | 低（可直接部署/读源码） |
| Vanna（开源） | github.com/vanna-ai/vanna（第三方称已归档） | 部分支持（DDL/文档/SQL 对训练语料，无独立语义层） | 官方确认（SQL 对即训练数据；self-learning 成功 SQL 自动入库） | 部分支持 | 未找到证据 | 部分支持 | 不适用（单点 text2SQL 库） | 官方确认（self-learning） | 官方确认（SQL 可见） | 未找到证据 | RAG-to-SQL 最小闭环；仓库疑似归档，慎作长期依赖 | 低 |

---

## 8. 最值得借鉴的机制清单（按自研适配优先级排序）

**适合中小型自研系统（强烈推荐直接借鉴）：**

1. **Verified Query Repository（Snowflake VQR）**：语义模型内维护"问题→已验证 SQL"对，带 verified_by/verified_at 元数据；命中即复用并在响应中可见命中了哪条。实现成本低（一张表 + 向量召回 + 命中标注），收益直接（高频题零幻觉）。
2. **Benchmarks + Request Review 双闭环（Databricks）**：作者侧基准题+标准 SQL 自动对拍（Correct/Needs Review），用户侧一键请求专家复核、修正后回流指令库。中小系统可用"错题库 + 定时回归脚本 + 用户纠错入口"极简实现。
3. **分层指令体系（Fabric/Quick BI 共通）**：Agent 级指令（目标/术语/数据源优先级）+ 数据源级指令（表/关系/查询逻辑）+ 示例查询（few-shot 检索 top-N 注入）。纯配置工程，零算法门槛。
4. **专用分析工具的前置澄清契约（DataBuddy 插件实践）**：归因/预测/异动/相关性各自定义"合格问题"要素清单（目标指标、当期、基期、维度、粒度），"禁止模糊直传"，要素缺失先澄清再调用。本质是工具调用的参数校验前置到语义层，工程上就是结构化 intent schema + 必填项检查。
5. **分析空间=资源白名单（DataBuddy/Fabric 共通）**：用户或治理侧显式圈定可问数的表/语义模型集合，Agent 只在白名单内检索——同时解决"自动选数据源"和权限收窄问题。
6. **可信资产分级标注（Databricks trusted assets / Quick BI 查看 SQL）**：回答上明确区分"命中已验证 SQL"vs"即时生成"，给用户差异化的信任信号；前端仅是一个标签 + SQL 展示。

**成本过高、不宜照搬（仅作方向参考）：**

7. **确定性查询编译器（ThoughtSpot）**：不用 LLM 生成自由 SQL，而是语义 token → 专有查询编译器。保证"同问同答"与 RLS/CLS 强制，但这是多年自研引擎，中小团队不应重造；可用"SQL 模板化 + 方言校验 + 只读执行"近似替代。
8. **全量多 Agent 编排平台（DataBuddy 三 Agent / ThoughtSpot 四 Agent）**：角色拆分本身可借鉴（问数/归因/看板分工），但跨 Agent 编排、权限联邦、审计链路成本高；中小系统先用"单 Agent + 工具路由"（Snowflake 官方也建议单 Agent 优先）。
9. **知识挖掘/自动语义抽取（Databricks knowledge mining）**：从血缘与查询历史自动建议指令，依赖成熟的 UC 血缘与查询日志基础设施，数据基础不到位时 ROI 低。
10. **Deep Research 式多假设并行研究（Databricks preview / Spotter 3）**：产品化程度低、token 成本高，适合作为远期"深度分析模式"方向，不宜一期实现。

---

*附：本地旁证文件路径——`/Users/ltq/.workbuddy/plugins/marketplaces/experts/plugins/workbuddy-data-expert-team/`（README.md、agents/databuddy-analyst.md、agents/databuddy-governor.md）。*
