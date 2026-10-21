# C. 专家团蒸馏架构设计（普通=蒸馏四角色 / 高级=完整七专家+循环校验）

- 版本：v4（2026-10-21，按用户要求改名：不再使用 Agent 编号—— supervisor 统一称**主理人**，三位专家正式起名：**问津**（路由）/ **格物**（SQL 工程）/ **析微**（数据分析）；不通过打回三个专家每人重新校验）｜ 配套：主报告第 8-10 章
- 核心命题：**普通问数保持 4 个角色（1 主理人 + 3 专家：问津/格物/析微），功能对标现有四段执行体；高级专家团扩展到主理人 + 7 专家 + Skills + 多重循环校验**。两档共用同一套注册表与底座，档位开关裁剪。

---

## 1. 设计原则

1. **蒸馏版不动骨架，原审计段升任主理人**：现有四段执行体中 **路由中枢段/SQL 架构师段/业务分析官段转为三个专家（问津/格物/析微）**，**原合规审计段（fail-close 人设）升任主理人·综合复核专家**——复核三个专家的全部内容。改造只做三件事：任务状态（TaskState）读写、L0 确定性闸门、升级出口。
2. **完整版才上复杂度**：7 专家、任务 DAG、L0/L1/L2 三层校验、多重循环，全部只在高级档启用。
3. **确定性服务承载关键能力**：记忆、权限、SQL 执行、结果验证是服务不是 Prompt；LLM 只做语义判断与生成。
4. **复杂≠堆角色**：完整版的复杂体现在**循环校验**（修复回环/核验回环/对拍回环/澄清循环/降级链），不是把简单并行串行拉长。

---

## 2. 蒸馏版：四角色（普通问数）

| 角色 | 姓名 | 来源 | 职责 | LLM 调用 |
|------|------|------|------|---------|
| 路由专家 | **问津** | 原路由段演进 | 意图识别、数据集路由（规则打分+节点索引）、歧义消歧（确认卡）、TaskState 读写、指代消解与条件继承 | 0-1 次（低置信才调） |
| SQL 工程专家 | **格物** | 原生成段演进 | Golden 命中复用 / 规则构建 / LLM 生成；解释 Join 与聚合 | 0-1 次 |
| 数据分析专家 | **析微** | 原分析段演进 | 老板视角结论、图表、口径说明、管理建议 | 1 次 |
| **主理人·综合复核专家** | **主理人** | **原审计段演进** | 定档（普通/完整）、拆任务分派、**综合复核三个专家的全部内容**（路由依据/SQL/口径/结论一致性/证据充分性/交付契约）、不通过→打回三个专家每人重新校验、组织最终交付 | 1 次（必跑） |

> 命名释义：问津——探寻路径，找到对的数据集与口径；格物——格物致知，构建查询；析微——析毫剖芒，从数据出结论。对外演示与文档统一用名字称呼，不再出现编号。

**蒸馏版流程（12 步）**：
1. 入口：feature+权限+错字/方向守卫（现有 ask_chat.py，不动）；
2. 主理人读 TaskState，输出复杂度评分——低于阈值走本流程，高于阈值提示“可升级高级”（用户可忽略，上下文不丢）；
3. 路由专家做指代消解与条件继承（resolve_followup 演进为 TaskState 增量更新，未修改条件保留，每条条件带来源标注）；
4. 路由专家选择数据集：规则+节点索引+权限白名单；top2 分差<阈值→确认卡澄清 1 轮；否则带假设继续并在答案标注；
5. 装载资产（get_dataset_context 现有）+ Golden 语义召回（P1 加向量），命中标注“已验证模板”；
6. SQL 工程：Golden 命中→直接执行；否则规则构建器→LLM 生成；
7. **L0 闸门零 token 全跑**：sql_gate（AST/只读/单语句/白名单）→ executor（statement_timeout/行数上限/只读账号）→ result_validator（粒度/重复/时间边界/空值/分母）；
8. **L1 按需**：仅当路由低置信 / 执行失败 / result_validator 标记风险 → 审查 1 次，不过→打回 SQL 工程修复回环≤2；
9. 数据分析专家解读 + answer_contract 交付契约检查（口径/数据源/时间/筛选/SQL 入口必含）；
10. **主理人综合复核**：复核三个专家的全部内容——路由依据是否成立、SQL 与口径是否一致、结论是否被证据支撑、交付契约是否齐全；
11. **复核不通过→打回三个专家，每人针对问题清单重新校验一遍**（修正结论或附理由坚持）→重新返回→主理人再复核（轮次预算内）；
12. 复核通过→组织最终交付（结果+图表+口径+SQL 查看入口）+ TaskState 写回 + 记忆候选（待审核）；降级出口：复杂度超阈值→升级完整版接续执行（已执行产物复用，不重跑）。

**LLM 调用总数 2-4 次**（Golden 命中时 1-2 次）。这是“快、稳、省”的定位：不为简单问题启动重型链路。

---

## 3. 完整版：主理人 + 7 专家 + Skills + 多重循环（高级专家团）

### 3.1 七专家（按需启用）

| # | 专家 | 职责边界 | 启用时机 |
|---|------|---------|---------|
| E0 | **主理人·综合复核** | 定档、拆任务分派、**综合复核全部专家产出**、打回全员重新校验、裁决/停止/降级、组织最终交付 | 每次 |
| E1 | 上下文管家 | 指代消解、工作区恢复、记忆检索、冲突识别，产出 Context Packet | 每次入口 |
| E2 | 资产路由专家（问津扩展） | 数据集/表/字段选择、权限、时效、跨源可用性；输出候选+置信度 | 路由不确定或跨域时 |
| E3 | 业务语义专家 | 指标定义、术语、时间口径、过滤条件、维度粒度 | 口径存疑时 |
| E4 | 查询规划专家 | 业务问题→可验证子问题→DAG（节点/依赖/验收/重试） | 每次（规划阶段） |
| E5 | SQL 工程专家（格物扩展） | Golden 复用/生成/优化；解释 Join 聚合 | 每个查询节点 |
| E6 | 独立审查专家 | SQL 级 L1 审查：语义一致性/权限/粒度/重复计数/时间边界/安全；**非生成者自审**；是主理人综合复核之下的第二层 | 每个查询节点 |
| E7 | 数据分析专家（析微扩展） | 贡献度/异常定位/分层比较/假设检查/敏感性验证；含可视化表达 | 结果需解读时 |

### 3.2 三层校验 Skills

| 层 | Skills | 说明 | 档位 |
|----|--------|------|------|
| L0 确定性（零 token） | sql_gate / executor / result_validator / answer_contract | 失败即阻断或触发修复，程序判定不靠模型 | 两档全跑 |
| L1 LLM 审查 | reviewer（独立审查，fail-close）/ self_check（结论自检）/ semantic_consistency（口径一致性） | 蒸馏版按需 1 次；完整版每查询节点必跑 self_check 与 semantic_consistency | 按需 / 每节点 |
| L2 交叉验证 | evidence_vote（多 SQL 路径对拍）/ sensitivity_check（换时间窗/粒度复算） | 仅完整版关键指标；对拍不一致→回口径核验，不投票 | 仅完整版 |

### 3.3 多重循环校验（完整版的“复杂”所在）

| 循环 | 触发 | 动作 | 上限 |
|------|------|------|------|
| 澄清循环 | 硬歧义（影响结论） | 主理人提出最少必要问题，给选项+差异说明 | ≤2 轮 |
| 修复回环 | L0 闸门/L1 审查/L2 对拍任一不过 | 错误分类→SQL 工程修复→重过全链路 | ≤2 次/节点 |
| 全员复核循环 | 主理人综合复核**不通过**：证据不足/专家矛盾/对拍不一致/口径冲突 | 主理人将问题清单（矛盾点/缺口/疑问）**打回三个专家，每人重新校验一遍**→专家复核：修正结论或附理由坚持→重新返回主理人再复核（禁止多数投票；仍矛盾→主理人指定口径核验） | 轮次/token/耗时预算内 |
| 假设检查循环 | E7 提出原因假设 | 设计验证查询→执行→确认/推翻，输出“已验证/未验证”标注 | 预算内 |
| 降级链 | 问题坍缩为简单题 / 连续两次节点失败 / 预算将尽 | 自动走蒸馏路径完成 / 降级重试一次 / 带缺口停止并交付已得证据 | — |

### 3.4 完整版流程：主理人分派-等待-综合评估（扇出/扇入循环）

**一个循环单元 = 分派 → 并行执行各自返回 → 综合评估 → 分支**：

1. **主理人结构化解析**：恢复工作区+Context Packet，输出 {已知条件， 未决问题， 成功标准， 风险等级}；
2. **澄清循环**（≤2 轮，仅硬歧义）；
3. **主理人拆任务并分派**：从 7 专家池按需选出本轮专家（典型一轮 3 名：路由/SQL 工程/数据分析，与蒸馏版同构；上下文管家/业务语义/查询规划/独立审查按需进入分派名单），每个任务带输入、预期输出、验收条件；
4. **专家并行执行，各自返回结构化结果**（交接协议 JSON：findings/artifact_refs/evidence_refs/assumptions/unresolved_questions/risk_flags/recommended_next_actions），**专家之间不直连、不共享中间态，只对主理人负责**；
5. **主理人等待收齐后综合评估**：证据是否支撑结论？专家间是否矛盾？口径是否一致？假设是否已验证？；
6. **分支**：
   - 通过 → 进入交付；
   - **不通过 → 全员复核循环**：主理人附问题清单打回三个专家，每人重新校验一遍（修正或附理由坚持），重新返回后主理人再复核；
   - 预算将尽 → 带缺口停止，交付已得证据；
   - 判定问题变简单 → 降级蒸馏版路径完成剩余部分；
7. **统一交付**：结论+图表+证据链+口径+SQL/执行轨迹入口+不确定性说明；
8. **检查点**：每轮分派任务/专家返回/评估结论全量落库（`advanced_task_graph` + `advanced_task_round`），断点恢复+重放；
9. **记忆候选**：提交审核，通过后才进长期记忆/正式配置。

**Skills 挂接规则**：L0 闸门挂在格物的执行动作上（必经）；L1 审查由独立审查专家承载（每轮必跑）；L2 对拍挂在析微的关键指标动作上（仅关键指标）。Skills 是专家可调用的确定性工具，不是独立角色。

---

## 4. 关键数据结构

```json
// 专家注册表（现有 4 角色 → 扩展为 8 角色）
{"expert_id": "supervisor_reviewer", "tier": "both", "source": "agent3",
 "role_prompt": "...", "duties": ["tier_decide", "dispatch", "comprehensive_review", "reject_all", "finalize"]}
{"expert_id": "sql_engineer", "tier": "both", "source": "agent2",
 "role_prompt": "...", "deterministic_deps": ["sql_gate", "executor"]}

// 档位配置（ask_flow.json 扩展）
{"defaultFlow": "basic", "advancedEnabled": false,
 "distilledExperts": ["router", "sql_engineer", "analyst", "supervisor_reviewer"],
 "fullExperts": ["context_steward", "router", "semantic", "planner",
                 "sql_engineer", "reviewer", "analyst"],
 "budgets": {"clarifyRounds": 2, "sqlRepairPerNode": 2,
             "maxTokens": 200000, "maxSeconds": 300}}

// 交接协议（ask_flow/contracts.py，所有专家统一）
{"task_id": "task_xxx", "node_id": "n3", "agent_role": "sql_engineer",
 "status": "completed|needs_clarification|blocked|failed",
 "findings": [], "artifact_refs": [], "evidence_refs": [],
 "assumptions": [], "unresolved_questions": [], "risk_flags": [],
 "recommended_next_actions": []}

// 任务图（新表 advanced_task_graph）
{task_id, node_id, node_type, inputs_ref, expected_output, acceptance,
 depends_on[], retry_policy, status, checkpoint_ref, config_version, loop_count}
```

---

## 5. 代码改造触点

| 现有模块 | 改造为 | 档位 |
|---------|--------|------|
| four_agent_ask.py 路由段（route_with_agent1:4005 / _agent1_route_with_llm:3905 / _detect_ambiguity:3770） | **问津**·路由专家（蒸馏版三专家之一；完整版扩展出资产路由/上下文管家/业务语义） | both |
| four_agent_ask.py 生成段（_agent2_generate_sql:7705 / _build_rule_based_sql:5020） | **格物**·SQL 工程专家 | both |
| four_agent_ask.py 审计段（_agent3_review:8551 fail-close） | **主理人**·综合复核专家（fail-close 人设升级为综合复核；完整版另设 SQL 级独立审查 E6 作第二层） | both |
| four_agent_ask.py 分析段（_agent4_analysis:8914） | **析微**·数据分析专家 | both |
| datapulse_advanced/skills/planner.py | E4 查询规划专家（升级为 DAG 产出） | full |
| datapulse_advanced/skills/dataset_route.py+route_guard.py | E2 资产路由专家 | full |
| datapulse_advanced/skills/golden_sql.py | Golden 召回+命中标注（蒸馏版也用） | both |
| datapulse_advanced/skills/evidence_vote.py | L2 对拍 | full |
| datapulse_advanced/skills/self_check.py/sql_quality.py | L1 reviewer/self_check | both（按需/每节点） |
| datapulse_advanced/skills/answer_contract.py | answer_contract L0 | both |
| memory/short_term_memory.py | 上下文管家+TaskState 服务 | both |
| datasource_router.py:192 | executor 包装（超时/行限/只读账号） | both |
| ask_flow/controller.py | 档位决策+复杂度评分+降级链 | both |
| 新：safety/sql_gate.py、result_validator.py | L0 skills | both |

---

## 6. 验收

1. **蒸馏版不劣化**：同一基准题集，蒸馏版 vs 现状四段执行体——SQL 正确率不降、LLM 调用次数≤4、P95 时延≤15s；
2. **完整版增量价值**：复杂题集上完整版 vs 蒸馏版——无证据结论率=0、任务完成率≥80%；做消融（无 L2 / 无核验回环 / 无假设检查）证明每层循环的边际价值，价值为负的循环降级为可选；
3. **循环上限有效**：构造必然失败题，验证修复≤2、澄清≤2、预算尽停止全部生效且不死循环；
4. **档位切换无损**：蒸馏→完整切换时 TaskState 与已执行产物复用，不重复查询；
5. **降级链**：简单题误入高级 / 连续节点失败 / 预算将尽三类场景分别走向“蒸馏路径 / 降级重试一次 / 带缺口停止”。
