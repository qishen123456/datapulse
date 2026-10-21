# 外部问数机制调研与架构决策记录

核对日期：2026-10-21。本轮依据为下列公开产品文档/论文，以及当前后端实际实现；旧项目规划文件不作为新机制的证据。每项区分“公开确认”与“本项目拟实现”。产品文档未列更新时间时不推测发布时间。

| 来源编号 | 本轮核对的一手资料 | 公开确认的机制（简述） | 本项目采纳与不照搬的部分 |
|---|---|---|---|
| S1 | [WrenAI Context](https://docs.getwren.ai/oss/concepts/what_is_context)、[MDL 模型](https://wrenai.readme.io/reference/get_models)、[Relationships](https://docs.getwren.ai/oss/guide/modeling/relationships) | MDL 组织模型、计算字段和关系；Context 比表结构更广。Context 文档区分不同能力的交付阶段 | 采纳“可审查语义契约”；权限执行、语义发布与证明回执自行设计，不能声称 Wren 当前所有上下文治理都已完备。与 Wren 集成先做少量模型适配 PoC，再决定使用其引擎还是保留自有编译层 |
| S2 | [CHESS v3 全文，2024-11-25](https://arxiv.org/html/2405.16755v3)，重点 §3.1、§3.2、§3.3、Appendix A | 分层实体/描述检索、Schema 选择、候选 SQL 和自然语言测试评分；按计算预算组合这些能力 | 采纳“检索→候选→验证”分工，业务断言/AST/权限为自建硬规则。自然语言评分不构成确定性证明；Schema 不能盲目越小越好；不复制论文高计算配置的采样规模 |
| S3 | [MAC-SQL v6 全文，2025-03-18](https://arxiv.org/html/2312.11242v6)，重点 §3.2–3.4 | Selector 缩小数据范围；Decomposer 分解查询；Refiner 使用外部执行反馈修正错误 | 工具反馈编成类型化错误/失效产物/定向重跑工单；空结果先判断是否业务合法，不把“有非空结果”当修复成功；共享两次额度是项目约束 |
| S4 | [ThoughtSpot Semantic Layer / Spotter Semantics](https://docs.thoughtspot.com/cloud/26.9.0.cl/semantic-layer/)；[Sage 公开说明](https://www.thoughtspot.com/blog/enhanced-ai-powered-analytics-with-gpt) | 官方描述业务定义、语义模型、安全与确定性查询生成的结合 | 采纳“模型理解意图，语义/查询层执行受治理逻辑”。其私有查询生成器不能直接复刻；项目通过 SemanticPlan IR、编译器与运行闸门近似实现这些原则，不宣称等同其产品保证 |
| S5 | [DataWind / Data Agent 深度研究](https://docs.volcengine.com/docs/Dataagent/DepthResearchAgent?lang=zh)、[私有化深度研究说明](https://docs.volcengine.com/docs/DataAgentPrivate/DepthResearchAgent-1?lang=zh)、[智能问数](https://docs.volcengine.com/docs/Dataagent/IntelligentQueryAgent?lang=zh) | 公开说明分析大纲、SQL/Python 分析、研究报告，以及业务知识/分析模板/报告要求的沉淀 | 采纳“业务知识 + 分析手册 + 报告契约”；Python 不是在 Flask 中任意执行字符串，而是登记算子/受限沙箱。本文没有接外网或 MCP 去传输本项目数据 |
| S6 | 本项目设计推导，非厂商能力断言 | 两模式独立、持久控制面、证据账本、全任务共享两次返工、声明级准入与发布验收 | 上述组合需要按规格实现/压测/回归；HTML 演示不代表后端已有能力 |

检索补充：[BIRD 官方榜单](https://bird-bench.github.io/)。本轮以论文机制为对标，CHESS/MAC-SQL 的历史成绩和不同模型/赛道不等于 2026-10-21 的统一“当前榜首”，也不外推项目正确率。

## 对上一版的实质变更

1. `Schema Linking` 不再只是向量标签：分开目录检索、实体值对齐、合法 Join 图和语义 IR，检索与生成有明确数据结构。
2. 高级不是三个专家各返回一段意见：每路有取证计划、候选查询、独立验证和执行回执，之后才汇合。
3. “可信度总分”改为硬规则状态 + 证据矩阵 + 反证；安全/单位/基数失败不能被其他检查加分抵消。
4. 分析手册含适用条件、输入、算子、反证和停止规则；历史分析报告只作参考，不是现行指标定义。
5. 统计计算与自然语言表达分开；分析算子登记版本，数值来自已核验证据，叙述声明逐条回链。
6. 42 个节点包括数据服务/运行时/条件节点，主理人仍是唯一对外负责角色；不要求建立42个人格或调用42次模型。

## 项目差距的新代码证据

- `backend/datapulse_advanced/skills/planner.py:7`：`infer` 正则提取 intent/topN/targetLevel 等；没有生成包含 `depends_on/acceptance/required/budget` 的执行 DAG。
- `backend/datapulse_advanced/skills/evidence_vote.py:9`：汇总多个规则的 weights 后得到 score，基于告警与阈值作建议；没有针对每条业务声明执行独立事实核对。
- `backend/datapulse_advanced/skills/sql_quality.py`：主要通过字符串规则、字段/表匹配和打分检查 SQL；不能视为 AST/方言语义分析的替代品。
- `backend/datapulse_advanced/skills/pandas_analyze.py:22`：已有行数据加工、指标与排序，可复用基础能力；不能由此认定已实现可控代码沙箱、假设检验或预测回测。
- `backend/ask_flow/controller.py:163/171`：高级错误可以回退 basic。新架构必须显式禁用跨模式回退，返回本高级任务的终态。
- `backend/datasource_router.py:192`：执行层直接读取完整结果，需增加超时、行/字节预算、取消与只读适配。实际数据库账号权限仍须部署审计。

代码路径相对项目 `datapivot-demo/`。以上是静态核查，不冒充生产运行日志或实测效果。

## 组织权限复用修正（两模式均必经）

系统已有组织树和数据集/组织范围权限，不将其列为缺失能力。普通L0和高级H02都调用现有 `allowed_dataset_ids_for_user` / `user_org_scope_for_rule`，组织提及复用 `org_mention_permission_check`，SQL执行及修复后复用 `apply_row_level_filter`。高级拆分DAG后需要保证这些既有行为在每条新执行路径上继续生效，而不是新增第二套授权。当前已核查的数据集/组织隔离不等于已确认列级策略或数据库原生RLS。
