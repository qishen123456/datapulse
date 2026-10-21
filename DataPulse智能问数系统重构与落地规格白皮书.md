# AuroraPulse 极光数智 · 企业级智能问数（NL2SQL + Multi-Agent）全栈重构与设计落地白皮书

> **文档性质**：工业级商业化重构 PRD + 核心架构设计 + 关键源码实现 + 前端 UI/UX 设计规范。  
> **适用对象**：全栈开发工程师、大模型 Prompt 工程师、AI Agent 架构师，可直接供 AI 工具（Claude/GPT/DeepSeek）实现 100% 独立代码交付。  
> **脱敏说明**：本文档已剔除所有历史项目敏感专有名词与特定企业数据，全新构建统一的虚拟企业资产标杆——**「极光数智集团（Aurora Mobility & Tech）」**。  
> **编码规范**：全文严格遵守 UTF-8 编码，杜绝乱码。

---

## 目录
- [一、业务场景与全域脱敏数据资产底座](#一业务场景与全域脱敏数据资产底座)
  - [1.1 业务组织拓扑（4 级树 + 双轨制）](#11-业务组织拓扑4-级树--双轨制)
  - [1.2 标准数仓 DDL 与展平分析视图](#12-标准数仓-ddl-与展平分析视图)
  - [1.3 语义知识层（Bookshelf 语义书架）表结构](#13-语义知识层bookshelf-语义书架表结构)
- [二、全栈系统架构与工程目录结构](#二全栈系统架构与工程目录结构)
  - [2.1 整体分层拓扑架构图](#21-整体分层拓扑架构图)
  - [2.2 生产级工程代码目录树](#22-生产级工程代码目录树)
- [三、核心引擎深度设计与可运行 Python 源码](#三核心引擎深度设计与可运行-python-源码)
  - [3.1 四 Agent 协同工作流与状态机（LangGraph / StateMachine）](#31-四-agent-协同工作流与状态机)
  - [3.2 组织节点轻量前缀树与错字纠偏（Typo Fastpath）算法](#32-组织节点轻量前缀树与错字纠偏算法)
  - [3.3 SQL AST 语法校验、沙箱防御与行级权限注入器](#33-sql-ast-语法校验沙箱防御与行级权限注入器)
  - [3.4 领导确认挂起与唤醒机制（Confirm-by-Boss）](#34-领导确认挂起与唤醒机制)
- [四、UI/UX 交互设计规范与 Vue 3 核心组件源码](#四uiux-交互设计规范与-vue-3-核心组件源码)
  - [4.1 智能问答工作台完整界面布局与状态流](#41-智能问答工作台完整界面布局与状态流)
  - [4.2 核心组件 1：解析胶囊条组件（ParseBar.vue）](#42-核心组件-1解析胶囊条组件parsebarvue)
  - [4.3 核心组件 2：SQL 查看与调试抽屉组件（SqlDrawer.vue）](#43-核心组件-2sql-查看与调试抽屉组件sqldrawervue)
  - [4.4 核心组件 3：自适应 ECharts 图表容器（AdaptiveChart.vue）](#44-核心组件-3自适应-echarts-图表容器adaptivechartvue)
  - [4.5 核心组件 4：歧义消解确认弹窗（ConfirmModal.vue）](#45-核心组件-4歧义消解确认弹窗confirmmodalvue)
  - [4.6 核心组件 5 & 6：多层级交互式穿透下钻系统（DrillDownCard.vue & DrillBreadcrumb.vue）](#46-核心组件-5--6多层级交互式穿透下钻系统)
- [五、核心防错红线与回归测试对账基准（Ground Truth）](#五核心防错红线与回归测试对账基准ground-truth)
- [六、前后端全双工/流式通信协议契约（SSE 规范）](#六前后端全双工流式通信协议契约sse-规范)

---

## 一、业务场景与全域脱敏数据资产底座

### 1.1 业务组织拓扑（4 级树 + 双轨制）

为满足现代化大型企业经营分析，“极光数智集团”采用典型的**双轨制矩阵管理体系**：

```mermaid
graph TD
    Root[极光数智集团总部] --> BG1[智能出行事业群 Mobility BG]
    Root --> BG2[数字能源事业群 Energy BG]
    Root --> BG3[云端服务事业群 Cloud BG]

    subgraph 区域管理链路 (4级拓扑)
        BG1 --> Reg1[华东战区 / 华东分公司]
        BG1 --> Reg2[华南战区 / 华南分公司]
        BG1 --> Reg3[华北战区 / 华北分公司]
        BG1 --> Reg4[西部战区 / 西部分公司]
        
        Reg1 --> Area1[苏沪片区 / 代表处]
        Reg1 --> Area2[浙皖片区 / 代表处]
        
        Area1 --> AM1[高级客户经理 A]
        Area1 --> AM2[客户经理 B]
    end

    subgraph 细分行业/业务线 (正交维度)
        BG1 -.-> Seg1[政企大客户定制线 Enterprise]
        BG1 -.-> Seg2[终端零售直营线 Retail]
        BG1 -.-> Seg3[生态伙伴渠道线 Partner]
    end
```

> **业务红线提示**：在数仓底层，大盘总览行与细分行业线共存。**查询大盘总额时，必须显式指定 `business_segment = '总额(未拆分)'`**，否则各板块相加会导致数据被翻倍累加！

---

### 1.2 标准数仓 DDL 与展平分析视图

数据库采用 PostgreSQL 15+。为了兼顾数据同步与 SQL 查询性能，数仓分为**原始清洗层**与**标准化分析视图层**。

```sql
-- 1. 物理事实表：sales_performance_daily (销售经营事实表)
CREATE TABLE IF NOT EXISTS fct_sales_performance (
    id BIGSERIAL PRIMARY KEY,
    stat_year VARCHAR(8) NOT NULL DEFAULT '2026',
    stat_quarter VARCHAR(4) DEFAULT 'Q1',
    stat_month VARCHAR(8) DEFAULT '2026-03',
    division_name VARCHAR(128) NOT NULL,      -- 事业群，如 '智能出行事业群'
    region_name VARCHAR(128),                 -- 战区/分公司，如 '华东战区'
    area_name VARCHAR(128),                   -- 片区/办事处，如 '苏沪片区'
    account_manager VARCHAR(128),             -- 客户经理，如 '周子昂'
    node_level VARCHAR(64) NOT NULL,          -- 组织层级: '事业群' / '战区' / '片区' / '个人'
    business_segment VARCHAR(128) NOT NULL DEFAULT '总额(未拆分)', -- 业务线: '总额(未拆分)' / '政企定制' / '终端零售' / '生态伙伴'
    target_amount NUMERIC(16, 2) NOT NULL DEFAULT 0.00,        -- 任务指标金额（元）
    actual_amount NUMERIC(16, 2) NOT NULL DEFAULT 0.00,        -- 实际开单/开票金额（元）
    order_count INT NOT NULL DEFAULT 0,                        -- 开单笔数
    completion_rate NUMERIC(8, 4) GENERATED ALWAYS AS (        -- 自动生成列: 达成率
        CASE WHEN target_amount > 0 THEN ROUND(actual_amount / target_amount, 4) ELSE 0.0000 END
    ) STORED,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 索引构建
CREATE INDEX idx_fct_sales_lookup ON fct_sales_performance(stat_year, node_level, business_segment);
CREATE INDEX idx_fct_sales_region ON fct_sales_performance(region_name, area_name);

-- 2. 面向 AI 问数的标准宽表分析视图: v_sales_performance_standard
CREATE OR REPLACE VIEW v_sales_performance_standard AS
SELECT 
    id,
    stat_year AS 年份,
    stat_quarter AS 季度,
    stat_month AS 月份,
    division_name AS 事业群,
    COALESCE(region_name, '') AS 战区,
    COALESCE(area_name, '') AS 片区,
    COALESCE(account_manager, '') AS 客户经理,
    node_level AS 组织层级,
    business_segment AS 业务板块,
    target_amount AS 目标金额,
    actual_amount AS 开单金额,
    order_count AS 开单单数,
    ROUND(completion_rate * 100, 2) AS 达成率_百分比,
    (target_amount - actual_amount) AS 业绩缺口
FROM fct_sales_performance;
```

---

### 1.3 语义知识层（Bookshelf 语义书架）表结构

系统严禁大模型直接盲猜数仓字段，统一通过 Bookshelf 语义层进行元数据约束与 Few-Shot 样本注入：

```sql
-- 1. 数据集主定义表
CREATE TABLE bs_datasets (
    id BIGSERIAL PRIMARY KEY,
    dataset_code VARCHAR(128) NOT NULL UNIQUE,     -- 唯一编码，如 'mobility_sales_overview'
    dataset_name VARCHAR(255) NOT NULL,            -- 显示名称，如 '智能出行经营总盘'
    business_domain VARCHAR(128) NOT NULL,         -- 业务域，如 '出行销售域'
    view_name VARCHAR(255) NOT NULL,               -- 关联标准视图，如 'v_sales_performance_standard'
    description TEXT NOT NULL DEFAULT '',
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 2. 语义字段字典与枚举映射表
CREATE TABLE bs_dictionary_items (
    id BIGSERIAL PRIMARY KEY,
    dataset_id BIGINT NOT NULL REFERENCES bs_datasets(id) ON DELETE CASCADE,
    column_name VARCHAR(128) NOT NULL,             -- 视图列名，如 '开单金额'
    semantic_label VARCHAR(128) NOT NULL,          -- 语义别名，如 '实收营收/业绩完成额'
    data_type VARCHAR(64) NOT NULL DEFAULT 'numeric',
    enum_values JSONB NOT NULL DEFAULT '[]'::jsonb, -- 枚举候选，如 ["总额(未拆分)", "政企定制", "终端零售"]
    aggregation_default VARCHAR(32) DEFAULT 'SUM', -- 默认聚合算子: SUM / AVG / COUNT
    redline_prompt TEXT DEFAULT ''                 -- 单字段防坑规则提示
);

-- 3. 业务口径 LLD 与防错红线规则表
CREATE TABLE bs_redline_rules (
    id BIGSERIAL PRIMARY KEY,
    dataset_id BIGINT NOT NULL REFERENCES bs_datasets(id) ON DELETE CASCADE,
    rule_category VARCHAR(64) NOT NULL,            -- 'double_counting' / 'zero_division' / 'level_isolation'
    rule_description TEXT NOT NULL,                -- '统计大盘时必须包含 business_segment = 总额(未拆分)'
    enforce_where_clause TEXT NOT NULL,            -- 强制注入的 SQL 片段
    is_active BOOLEAN NOT NULL DEFAULT TRUE
);

-- 4. 黄金样本库（Few-Shot Golden SQL）
CREATE TABLE bs_golden_samples (
    id BIGSERIAL PRIMARY KEY,
    dataset_id BIGINT NOT NULL REFERENCES bs_datasets(id) ON DELETE CASCADE,
    intent_category VARCHAR(64) NOT NULL,          -- 'rank' / 'trend' / 'compare' / 'detail'
    user_query TEXT NOT NULL,                      -- 用户典型问句，如 '华东战区各片区开单排名'
    ground_truth_sql TEXT NOT NULL,                -- 人工审计 100% 正确的标准 SQL
    weight INT NOT NULL DEFAULT 100,
    is_active BOOLEAN NOT NULL DEFAULT TRUE
);
```

---

## 二、全栈系统架构与工程目录结构

### 2.1 整体分层拓扑架构图

```
┌────────────────────────────────────────────────────────────────────────┐
│                        前端交互层 (Vue 3 + Pinia + ECharts)             │
│  [SmartAskView] ── [ParseBar 胶囊条] ── [SqlDrawer 抽屉] ── [AdaptiveChart] │
└────────────────────────────────────▲───────────────────────────────────┘
                                     │  SSE (Server-Sent Events) 双向流式通信
┌────────────────────────────────────▼───────────────────────────────────┐
│                      FastAPI API 网关 & 会话上下文控制                 │
│         /api/chat/stream ── /api/chat/confirm ── /api/chat/rerun       │
└────────────────────────────────────▲───────────────────────────────────┘
                                     │
┌────────────────────────────────────▼───────────────────────────────────┐
│              Four-Agent Pipeline 引擎 (基于状态机 / StateGraph)         │
│  ┌───────────────┐   ┌────────────────┐   ┌──────────────┐   ┌───────┐ │
│  │ Agent 1: 路由 │──>│ Agent 2: 实体抽 │──>│ Agent 3: SQL │──>│Agent 4│ │
│  │   RouteAgent  │   │   IntentAgent  │   │  SQLBuilder  │   │Insight│ │
│  └───────────────┘   └────────────────┘   └──────────────┘   └───────┘ │
│         │                    │                   │                     │
│         │ (意图模糊挂起)      │ (纠错自愈)         │ (AST校验/权限拦截)   │
│         ▼                    ▼                   ▼                     │
│  [Confirm-by-Boss]   [Typo Fastpath]    [Row-Level Security]           │
└────────────────────────────────────▲───────────────────────────────────┘
                                     │
┌────────────────────────────────────▼───────────────────────────────────┐
│                       数仓与语义持久底座 (PostgreSQL)                   │
│   [bs_datasets] ── [bs_dictionary] ── [v_sales_performance_standard]   │
└────────────────────────────────────────────────────────────────────────┘
```

---

### 2.2 生产级工程代码目录树

```
aurora-smartask/
├── backend/                       # Python 后端工程 (FastAPI + AsyncPG)
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                # FastAPI 启动入口与 CORS 配置
│   │   ├── core/                  # 核心配置与工具
│   │   │   ├── config.py          # 统一环境变量加载 (Pydantic Settings)
│   │   │   ├── database.py        # AsyncPG 异步数据库连接池
│   │   │   └── security.py        # JWT 鉴权与当前用户注入
│   │   ├── engine/                # ★ 核心问数引擎模块
│   │   │   ├── state.py           # Agent 流水线状态机数据类 (AskState)
│   │   │   ├── pipeline.py        # 四 Agent 编排流水线调度器
│   │   │   ├── typo_fastpath.py   # 组织前缀树与错字 Levenshtein 纠错
│   │   │   ├── sql_guard.py       # SQL 语法树 AST 解析、防注入与行级权限注入
│   │   │   └── agents/
│   │   │       ├── route_agent.py   # Agent 1: 业务数据集分类器
│   │   │       ├── intent_agent.py  # Agent 2: 实体抽取与指代消解
│   │   │       ├── sql_agent.py     # Agent 3: NL2SQL 生成与自愈纠错
│   │   │       └── insight_agent.py # Agent 4: 可视化自动选型与简报生成
│   │   ├── api/                   # REST / SSE 控制器
│   │   │   ├── router.py          # 总路由聚合
│   │   │   └── v1/
│   │   │       ├── chat.py        # /api/chat/stream, /confirm, /rerun
│   │   │       ├── datasets.py    # 数据集 CRUD
│   │   │       └── debug.py       # SQL 调试台接口
│   │   └── models/                # 领域模型与 DDL 迁移
│   ├── tests/                     # 100 题自动化评测与单元测试
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/                      # 前端工程 (Vue 3 + Vite + TailwindCSS + ECharts)
│   ├── src/
│   │   ├── api/                   # 后端 API 接口封装 (Fetch + EventSource)
│   │   ├── assets/                # 样式与静态图表
│   │   ├── components/            # ★ 核心交互组件
│   │   │   ├── ParseBar.vue       # 解析胶囊条 (可点击修改重跑)
│   │   │   ├── SqlDrawer.vue      # SQL 查看与调试抽屉
│   │   │   ├── AdaptiveChart.vue  # ECharts 自适应图表渲染器
│   │   │   ├── ConfirmModal.vue   # 歧义消解确认弹窗
│   │   │   ├── DrillDownCard.vue  # ★ 多层级穿透下钻折叠卡片 (先总后分+滞后警示)
│   │   │   └── DrillBreadcrumb.vue# ★ 穿透链路面包屑导航条
│   │   ├── views/
│   │   │   ├── SmartAskView.vue   # 智能问答主工作台
│   │   │   ├── DatasetAdmin.vue   # 数据书架与口径管理
│   │   │   └── SqlDebugger.vue    # 分析师 SQL 调试台
│   │   ├── stores/                # Pinia 全局状态管理
│   │   │   ├── chatStore.js       # 会话列表与流式状态
│   │   │   └── userStore.js       # 当前登录用户信息与数据权限范围
│   │   ├── App.vue
│   │   └── main.js
│   ├── package.json
│   └── vite.config.js
└── docker-compose.yml             # 容器编排 (Postgres + Backend + Frontend)
```

---

## 三、核心引擎深度设计与可运行 Python 源码

### 3.1 四 Agent 协同工作流与状态机

在 `backend/app/engine/state.py` 与 `pipeline.py` 中，采用**强类型状态定义**，流转在四 Agent 之间：

```python
# backend/app/engine/state.py
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class EntityExtracted(BaseModel):
    org_nodes: List[Dict[str, str]] = Field(default_factory=list, description="如 [{'name': '华东战区', 'level': '战区'}]")
    business_segment: str = Field(default="总额(未拆分)", description="业务板块")
    time_range: Dict[str, Any] = Field(default_factory=dict, description="时间切片 {'year': '2026', 'quarter': 'Q1'}")
    metrics: List[str] = Field(default_factory=list, description="查询的指标度量")
    intent_type: str = Field(default="detail", description="detail | rank | compare | trend")
    rank_spec: Optional[Dict[str, Any]] = None

class AskState(BaseModel):
    conversation_id: str
    user_query: str
    history: List[Dict[str, str]] = Field(default_factory=list)
    dataset_code: Optional[str] = None
    dataset_name: Optional[str] = None
    entities: EntityExtracted = Field(default_factory=EntityExtracted)
    
    # SQL 生成与执行
    generated_sql: Optional[str] = None
    sanitized_sql: Optional[str] = None
    sql_error: Optional[str] = None
    retry_count: int = 0
    query_columns: List[str] = Field(default_factory=list)
    query_rows: List[List[Any]] = Field(default_factory=list)
    execution_time_ms: float = 0.0
    
    # 可视化与洞察
    chart_type: str = "table" # bar | line | pie | metric_card | table
    chart_config: Dict[str, Any] = Field(default_factory=dict)
    insights: List[str] = Field(default_factory=list)
    
    # 交互挂起状态
    need_confirm: bool = False
    confirmation_id: Optional[str] = None
    confirm_title: Optional[str] = None
    confirm_options: List[Dict[str, Any]] = Field(default_factory=list)
```

流水线调度器实现（`backend/app/engine/pipeline.py`）：

```python
# backend/app/engine/pipeline.py
import time
from typing import AsyncGenerator, Dict, Any
from app.engine.state import AskState
from app.engine.agents.route_agent import RouteAgent
from app.engine.agents.intent_agent import IntentAgent
from app.engine.agents.sql_agent import SQLAgent
from app.engine.agents.insight_agent import InsightAgent
from app.engine.sql_guard import SQLGuard
from app.core.database import db_pool

class FourAgentPipeline:
    def __init__(self, llm_client):
        self.llm = llm_client
        self.route_agent = RouteAgent(llm_client)
        self.intent_agent = IntentAgent(llm_client)
        self.sql_agent = SQLAgent(llm_client)
        self.insight_agent = InsightAgent(llm_client)
        self.sql_guard = SQLGuard()

    async def execute_stream(self, state: AskState, user_ctx: Dict[str, Any]) -> AsyncGenerator[Dict[str, Any], None]:
        # Step 1: 路由数据集 (Agent 1)
        yield {"event": "step", "data": {"stage": "ROUTING", "msg": "正在分析问题特征，匹配数仓资产..."}}
        state = await self.route_agent.run(state)
        
        if state.need_confirm:
            yield {
                "event": "confirm_required",
                "data": {
                    "confirmation_id": state.confirmation_id,
                    "title": state.confirm_title,
                    "options": state.confirm_options
                }
            }
            return

        yield {"event": "step", "data": {"stage": "ENTITY", "msg": f"已锁定资产【{state.dataset_name}】，正在提取组织实体与时间维度..."}}
        
        # Step 2: 实体抽取、指代消解与纠错 (Agent 2)
        state = await self.intent_agent.run(state)
        
        # 输出解析胶囊条事件
        yield {
            "event": "parse_bar",
            "data": {
                "dataset_name": state.dataset_name,
                "dataset_code": state.dataset_code,
                "entities": state.entities.model_dump(),
                "intent_type": state.entities.intent_type
            }
        }

        # Step 3: NL2SQL 生成与自愈循环 (Agent 3)
        yield {"event": "step", "data": {"stage": "SQL_GEN", "msg": "正在基于 Bookshelf 业务红线构建查询 SQL..."}}
        
        max_retries = 2
        while state.retry_count <= max_retries:
            state = await self.sql_agent.run(state)
            
            # AST 语法树安全审查 + 行级权限注入
            is_valid, sanitized_sql, err_msg = self.sql_guard.validate_and_inject_rls(
                state.generated_sql, user_scope=user_ctx.get("org_scope")
            )
            
            if not is_valid:
                state.sql_error = f"安全防御拦截: {err_msg}"
                state.retry_count += 1
                continue

            state.sanitized_sql = sanitized_sql
            
            # 执行查询
            start_t = time.time()
            try:
                async with db_pool.acquire() as conn:
                    # 强设 10 秒超时，防止慢查询拖垮集群
                    await conn.execute("SET statement_timeout = 10000;")
                    records = await conn.fetch(state.sanitized_sql)
                    state.execution_time_ms = round((time.time() - start_t) * 1000, 2)
                    
                    if records:
                        state.query_columns = list(records[0].keys())
                        state.query_rows = [list(r.values()) for r in records]
                    else:
                        state.query_columns = []
                        state.query_rows = []
                    state.sql_error = None
                    break # 执行成功，跳出重试循环
            except Exception as e:
                state.sql_error = str(e)
                state.retry_count += 1
                yield {"event": "step", "data": {"stage": "SQL_RETRY", "msg": f"SQL 执行异常，AI 正在自愈重试 ({state.retry_count}/{max_retries})..."}}

        if state.sql_error:
            yield {"event": "error", "data": {"error": f"SQL 执行最终失败: {state.sql_error}", "sql": state.sanitized_sql}}
            return

        # 推送 SQL 证据链
        yield {
            "event": "sql_ready",
            "data": {
                "sql": state.sanitized_sql,
                "execution_time_ms": state.execution_time_ms,
                "row_count": len(state.query_rows)
            }
        }

        # Step 4: 自适应图表与经营洞察 (Agent 4)
        yield {"event": "step", "data": {"stage": "INSIGHT", "msg": "正在计算统计分布，渲染可视化图表并生成经营洞察..."}}
        state = await self.insight_agent.run(state)

        # 最终产出结果
        yield {
            "event": "final_result",
            "data": {
                "columns": state.query_columns,
                "rows": state.query_rows,
                "chart_type": state.chart_type,
                "chart_config": state.chart_config,
                "insights": state.insights
            }
        }
```

---

### 3.2 组织节点轻量前缀树与错字纠偏（Typo Fastpath）算法

在 `backend/app/engine/typo_fastpath.py` 中，不调用昂贵的 LLM，通过**离线前缀树 + 编辑距离**实现 $< 5\text{ms}$ 的实体纠错与对齐：

```python
# backend/app/engine/typo_fastpath.py
from typing import Dict, List, Optional, Tuple
from difflib import SequenceMatcher

class NodeAliasMatcher:
    def __init__(self, node_records: List[Dict[str, Any]]):
        """
        node_records 格式:
        [
          {"name": "华东战区", "level": "战区", "aliases": ["华东", "华东大区", "华东分公司"]},
          {"name": "苏沪片区", "level": "片区", "aliases": ["苏沪", "上海片区", "江苏片区"]},
          {"name": "周子昂", "level": "客户经理", "aliases": ["老周", "周子昂业务员"]}
        ]
        """
        self.exact_map: Dict[str, Dict[str, str]] = {}
        self.all_keywords: List[str] = []
        
        for item in node_records:
            std_name = item["name"]
            meta = {"name": std_name, "level": item["level"]}
            self.exact_map[std_name] = meta
            self.all_keywords.append(std_name)
            
            for alias in item.get("aliases", []):
                self.exact_map[alias] = meta
                self.all_keywords.append(alias)

    def match_entity(self, word: str, threshold: float = 0.82) -> Tuple[Optional[Dict[str, str]], Optional[str]]:
        """
        返回: (命中标准实体信息, 纠错提示文本)
        """
        # 1. 精确匹配
        if word in self.exact_map:
            return self.exact_map[word], None

        # 2. 相似度模糊计算 (纠正口误错字，如 "华冬" -> "华东")
        best_match = None
        best_ratio = 0.0

        for candidate in self.all_keywords:
            ratio = SequenceMatcher(None, word, candidate).ratio()
            if ratio > best_ratio:
                best_ratio = ratio
                best_match = candidate

        if best_ratio >= threshold and best_match:
            hit = self.exact_map[best_match]
            note = f"已自动将「{word}」校准为标准实体「{hit['name']}」"
            return hit, note

        return None, None
```

---

### 3.3 SQL AST 语法校验、沙箱防御与行级权限注入器

在 `backend/app/engine/sql_guard.py` 中，使用 `sqlglot` 构建安全的沙箱防护与行级权限注入：

```python
# backend/app/engine/sql_guard.py
from typing import Tuple, Optional, Dict, Any
import sqlglot
from sqlglot import exp

class SQLGuard:
    FORBIDDEN_KEYWORDS = {"DROP", "DELETE", "UPDATE", "INSERT", "ALTER", "TRUNCATE", "EXEC", "GRANT"}

    def validate_and_inject_rls(
        self, raw_sql: str, user_scope: Optional[Dict[str, Any]] = None
    ) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        1. 阻断非只读与多语句注入
        2. AST 语法树注入行级过滤条件
        """
        if not raw_sql or not raw_sql.strip():
            return False, None, "SQL 语句为空"

        # 基础黑名单过滤
        upper_sql = raw_sql.upper()
        for kw in self.FORBIDDEN_KEYWORDS:
            if f" {kw} " in f" {upper_sql} ":
                return False, None, f"检测到非法关键字 [{kw}]，已被系统沙箱拦截！"

        try:
            expressions = sqlglot.parse(raw_sql, read="postgres")
            if len(expressions) > 1:
                return False, None, "禁止执行分号分隔的多条 SQL 组合！"
            
            parsed = expressions[0]
            if not isinstance(parsed, exp.Select):
                return False, None, "仅允许执行 SELECT 查询语句！"

            # 强制追加 LIMIT 限制
            if not parsed.args.get("limit"):
                parsed = parsed.limit(500)
            else:
                curr_limit = int(parsed.args["limit"].expression.this)
                if curr_limit > 1000:
                    parsed.args["limit"].expression.this = "1000"

            # 行级数据权限拦截注入 (Row-Level Security)
            # 若用户范围为华东战区负责人: user_scope = {"level": "战区", "names": ["华东战区"]}
            if user_scope and user_scope.get("level") == "战区":
                allowed_regions = user_scope.get("names", [])
                rls_predicate = exp.In(
                    this=exp.column("战区"),
                    expressions=[exp.Literal.string(r) for r in allowed_regions]
                )
                parsed = parsed.where(rls_predicate)

            sanitized_sql = parsed.sql(dialect="postgres")
            return True, sanitized_sql, None

        except Exception as e:
            return False, None, f"SQL 语法解析异常: {str(e)}"
```

---

### 3.4 领导确认挂起与唤醒机制（Confirm-by-Boss）

当问题存在多重意图或重名歧义时，引擎自动将上下文存入 Redis 缓存并暂停流，前端确认后唤醒：

```python
# backend/app/api/v1/chat.py 部分接口
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
import uuid

router = APIRouter()
CONFIRM_STORAGE: Dict[str, Any] = {} # 生产环境换为 Redis

class ConfirmPayload(BaseModel):
    confirmation_id: str
    selected_value: Any  # 用户在前端弹窗中选中的值

@router.post("/api/chat/confirm")
async def resume_confirmation(payload: ConfirmPayload):
    ctx = CONFIRM_STORAGE.get(payload.confirmation_id)
    if not ctx:
        raise HTTPException(status_code=404, detail="确认会话已过期，请重新提问。")

    # 取出之前挂起的上下文
    state: AskState = ctx["state"]
    # 注入用户手动抉择的值
    state.need_confirm = False
    state.entities.org_nodes = [payload.selected_value]
    
    # 清理缓存
    del CONFIRM_STORAGE[payload.confirmation_id]
    
    # 带着完整实体直接流向 Agent 3 生成 SQL
    return {"success": True, "message": "歧义消解完成，已唤醒问数引擎。"}
```

---

## 四、UI/UX 交互设计规范与 Vue 3 核心组件源码

### 4.1 智能问答工作台完整界面布局与状态流

现代高级智能问答工作台必须兼具**“低门槛打字”**与**“高透明度审查”**双重能力：

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│  顶部导航栏: [ 极光数智 · 智能问数工作台 ]             [数据源: 生产主库 🟢] [当前用户: 华东战区总监]│
├──────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│  [左侧会话历史] │                      主工作区 (Chat Stream)                     │
│                 │                                                                │
│  + 新建分析     │  [用户]: 华东战区和华南战区今年的业绩对比，按片区排一下             │
│  ─────────────  │                                                                │
│  - 战区业绩对比 │  [AI Agent]:                                                   │
│  - 3月开单排行  │  ┌──────────────────────────────────────────────────────────┐  │
│  - 缺口归因分析 │  │ 🏷️ 解析胶囊条 (Parse Bar)                                 │  │
│                 │  │ [数据集: 智能出行经营总盘 ▾] [战区: 华东, 华南 ✕] [年份: 2026] │  │
│                 │  │ 意图: 多主体横向对比 (Compare)             [ 🔄 重新生成 ] │  │
│                 │  └──────────────────────────────────────────────────────────┘  │
│                 │                                                                │
│                 │  ┌──────────────────────────────────────────────────────────┐  │
│                 │  │ 📊 自适应可视化图表 (AdaptiveChart)                       │  │
│                 │  │ [柱状图 | 折线图 | 纯表格切换]               [ ⬇️ 导出 CSV ]│  │
│                 │  │                                                          │  │
│                 │  │    3,556万 ▇▇▇▇▇▇▇▇▇ 华东苏沪片区                         │  │
│                 │  │    2,890万 ▇▇▇▇▇▇▇ 华南粤东片区                           │  │
│                 │  └──────────────────────────────────────────────────────────┘  │
│                 │                                                                │
│                 │  ┌──────────────────────────────────────────────────────────┐  │
│                 │  │ 💡 经营决策洞察:                                          │  │
│                 │  │ 1. 华东战区总开单领先华南 12.4%，主要由苏沪片区大单带动。  │  │
│                 │  │ 2. 华南片区达成率较高(68.2%)，整体预算执行节奏更加健康。  │  │
│                 │  └──────────────────────────────────────────────────────────┘  │
│                 │                                                                │
│                 │  [ 🔍 点击展开 SQL 证据链及耗时: 42ms ]                         │
│                 │                                                                │
├─────────────────┴────────────────────────────────────────────────────────────────┤
│  底部输入区:                                                                     │
│  [ 💬 输入业务分析问题，如：各战区销冠是谁？ / 上季度达成率后 3 的片区... ] [ 发送 ] │
└──────────────────────────────────────────────────────────────────────────────────┘
```

---

### 4.2 核心组件 1：解析胶囊条组件（`ParseBar.vue`）

该组件让用户一眼看穿大模型的“黑盒解析”，支持直接点选下拉修正实体，并触发 `rerun`：

```vue
<!-- frontend/src/components/ParseBar.vue -->
<template>
  <div class="parse-bar-container bg-slate-50 border border-slate-200 rounded-lg p-2.5 mb-3 flex flex-wrap items-center justify-between gap-2 shadow-sm text-xs">
    <div class="flex flex-wrap items-center gap-2">
      <span class="text-slate-400 font-medium flex items-center">
        <svg class="w-3.5 h-3.5 mr-1 text-indigo-500" fill="currentColor" viewBox="0 0 20 20">
          <path d="M7 3a1 1 0 000 2h6a1 1 0 100-2H7zM4 7a1 1 0 011-1h10a1 1 0 110 2H5a1 1 0 01-1-1zM2 11a2 2 0 012-2h12a2 2 0 012 2v4a2 2 0 01-2 2H4a2 2 0 01-2-2v-4z" />
        </svg>
        解析胶囊:
      </span>

      <!-- 数据集标签 -->
      <span class="px-2 py-0.5 rounded-full bg-indigo-50 text-indigo-700 border border-indigo-200 font-medium">
        📂 {{ parsedData.dataset_name }}
      </span>

      <!-- 组织实体胶囊 -->
      <span 
        v-for="(org, idx) in parsedData.entities.org_nodes" 
        :key="idx" 
        class="inline-flex items-center px-2 py-0.5 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200 font-medium"
      >
        🏢 {{ org.name }}
        <button @click="removeOrgNode(idx)" class="ml-1 hover:text-emerald-900 font-bold">×</button>
      </span>

      <!-- 业务线 -->
      <span class="px-2 py-0.5 rounded-full bg-amber-50 text-amber-700 border border-amber-200 font-medium">
        🏷️ {{ parsedData.entities.business_segment }}
      </span>

      <!-- 统计意图 -->
      <span class="px-2 py-0.5 rounded-full bg-purple-50 text-purple-700 border border-purple-200">
        🎯 意图: {{ intentLabel(parsedData.intent_type) }}
      </span>
    </div>

    <!-- 局部微调重新运行 -->
    <button 
      @click="$emit('rerun', parsedData)" 
      class="px-2.5 py-1 bg-white hover:bg-slate-100 text-slate-700 border border-slate-300 rounded shadow-xs transition flex items-center gap-1 active:scale-95"
    >
      <svg class="w-3 h-3 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
      </svg>
      重新计算
    </button>
  </div>
</template>

<script setup>
const props = defineProps({
  parsedData: {
    type: Object,
    required: true
  }
});

const emit = defineEmits(['rerun', 'update']);

function removeOrgNode(index) {
  props.parsedData.entities.org_nodes.splice(index, 1);
  emit('update', props.parsedData);
}

function intentLabel(type) {
  const map = {
    rank: '排行榜分析 (Rank)',
    compare: '横向对比 (Compare)',
    trend: '趋势分析 (Trend)',
    detail: '指标查验 (Detail)'
  };
  return map[type] || '通用问答';
}
</script>
```

---

### 4.3 核心组件 2：SQL 查看与调试抽屉组件（`SqlDrawer.vue`）

```vue
<!-- frontend/src/components/SqlDrawer.vue -->
<template>
  <div class="sql-drawer mt-2 border-t border-slate-100 pt-2 text-xs">
    <button 
      @click="isOpen = !isOpen" 
      class="text-slate-500 hover:text-indigo-600 flex items-center gap-1 font-mono transition"
    >
      <span>{{ isOpen ? '▼ 折叠 SQL 证据链' : '▶ 查看 SQL 证据链与性能诊断' }}</span>
      <span class="text-slate-400">({{ executionTime }}ms · {{ rowCount }} 行)</span>
    </button>

    <div v-if="isOpen" class="mt-2 bg-slate-900 rounded-lg p-3 text-slate-200 font-mono relative overflow-x-auto shadow-inner">
      <div class="flex justify-between items-center mb-1 text-[11px] text-slate-400 border-b border-slate-800 pb-1">
        <span>PostgreSQL 15 Dialect (Read-Only Sandbox)</span>
        <button @click="copySql" class="hover:text-white transition">
          {{ copied ? '已复制 ✔' : '复制 SQL' }}
        </button>
      </div>
      <pre class="text-emerald-400 whitespace-pre-wrap leading-relaxed">{{ sqlText }}</pre>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const props = defineProps({
  sqlText: String,
  executionTime: Number,
  rowCount: Number
});

const isOpen = ref(false);
const copied = ref(false);

function copySql() {
  navigator.clipboard.writeText(props.sqlText);
  copied.value = true;
  setTimeout(() => (copied.value = false), 2000);
}
</script>
```

---

### 4.4 核心组件 3：自适应 ECharts 图表容器（`AdaptiveChart.vue`）

该组件内置 Resize 监听防抖，并支持柱状图、折线图、环形饼图与原始表格的一键无缝切换：

```vue
<!-- frontend/src/components/AdaptiveChart.vue -->
<template>
  <div class="adaptive-chart-card bg-white border border-slate-200 rounded-xl p-4 my-3 shadow-xs">
    <div class="flex justify-between items-center mb-3">
      <h4 class="text-sm font-semibold text-slate-800 flex items-center gap-1.5">
        <span class="w-2 h-2 rounded-full bg-indigo-500"></span>
        {{ chartConfig.title || '数据分析可视化看板' }}
      </h4>

      <!-- 视图模式切换器 -->
      <div class="flex items-center bg-slate-100 p-0.5 rounded text-xs">
        <button 
          v-for="mode in ['chart', 'table']" 
          :key="mode" 
          @click="viewMode = mode"
          :class="['px-2.5 py-1 rounded transition', viewMode === mode ? 'bg-white text-indigo-600 shadow-xs font-medium' : 'text-slate-500 hover:text-slate-700']"
        >
          {{ mode === 'chart' ? '📊 可视化图表' : '📋 原始数据表' }}
        </button>
      </div>
    </div>

    <!-- 图表容器 -->
    <div v-show="viewMode === 'chart'" ref="chartRef" class="w-full h-72"></div>

    <!-- 表格容器 -->
    <div v-show="viewMode === 'table'" class="overflow-x-auto max-h-72">
      <table class="min-w-full text-left text-xs text-slate-700 divide-y divide-slate-200">
        <thead class="bg-slate-50 sticky top-0 font-medium text-slate-500">
          <tr>
            <th v-for="col in columns" :key="col" class="px-3 py-2">{{ col }}</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-100">
          <tr v-for="(row, rIdx) in rows" :key="rIdx" class="hover:bg-slate-50">
            <td v-for="(cell, cIdx) in row" :key="cIdx" class="px-3 py-1.5 whitespace-nowrap">{{ cell }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, onBeforeUnmount } from 'vue';
import * as echarts from 'echarts';

const props = defineProps({
  chartType: String,
  chartConfig: Object,
  columns: Array,
  rows: Array
});

const viewMode = ref('chart');
const chartRef = ref(null);
let chartInstance = null;

function renderChart() {
  if (!chartRef.value || viewMode.value !== 'chart') return;
  if (!chartInstance) {
    chartInstance = echarts.init(chartRef.value);
  }

  const option = {
    tooltip: { trigger: 'axis' },
    grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
    xAxis: {
      type: 'category',
      data: props.chartConfig.xAxis || [],
      axisLabel: { interval: 0, rotate: props.chartConfig.xAxis?.length > 6 ? 30 : 0 }
    },
    yAxis: { type: 'value' },
    series: props.chartConfig.series || []
  };

  chartInstance.setOption(option, true);
}

function handleResize() {
  if (chartInstance) chartInstance.resize();
}

onMounted(() => {
  renderChart();
  window.addEventListener('resize', handleResize);
});

watch(() => props.chartConfig, renderChart, { deep: true });
watch(viewMode, (val) => {
  if (val === 'chart') setTimeout(() => chartInstance && chartInstance.resize(), 50);
});

onBeforeUnmount(() => {
  window.removeEventListener('resize', handleResize);
  if (chartInstance) chartInstance.dispose();
});
</script>
```

---

### 4.5 核心组件 4：歧义消解确认弹窗（`ConfirmModal.vue`）

```vue
<!-- frontend/src/components/ConfirmModal.vue -->
<template>
  <div v-if="visible" class="fixed inset-0 z-50 flex items-center justify-center bg-black/40 backdrop-blur-xs">
    <div class="bg-white rounded-xl shadow-2xl w-full max-w-md p-6 transform transition-all border border-slate-100">
      <div class="flex items-center gap-3 mb-4">
        <div class="w-10 h-10 rounded-full bg-amber-100 flex items-center justify-center text-amber-600 font-bold text-lg">
          ?
        </div>
        <div>
          <h3 class="text-base font-semibold text-slate-900">需要您的确认</h3>
          <p class="text-xs text-slate-500 mt-0.5">{{ title || '检测到多个匹配项，请指定明确的主体' }}</p>
        </div>
      </div>

      <!-- 选项单选列表 -->
      <div class="space-y-2 my-4">
        <label 
          v-for="(opt, idx) in options" 
          :key="idx" 
          class="flex items-center p-3 rounded-lg border cursor-pointer transition text-xs"
          :class="selectedVal === opt.value ? 'border-indigo-600 bg-indigo-50/50 text-indigo-900 font-medium' : 'border-slate-200 hover:bg-slate-50 text-slate-700'"
        >
          <input type="radio" :value="opt.value" v-model="selectedVal" class="text-indigo-600 focus:ring-indigo-500 mr-2.5">
          <span>{{ opt.label }}</span>
        </label>
      </div>

      <div class="flex justify-end gap-2.5 mt-6">
        <button 
          @click="$emit('cancel')" 
          class="px-3.5 py-1.5 text-xs text-slate-600 hover:bg-slate-100 rounded-lg transition"
        >
          取消查询
        </button>
        <button 
          @click="handleConfirm" 
          :disabled="!selectedVal"
          class="px-4 py-1.5 text-xs text-white bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50 rounded-lg shadow-xs transition"
        >
          确认继续分析
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const props = defineProps({
  visible: Boolean,
  title: String,
  options: Array,
  confirmationId: String
});

const emit = defineEmits(['confirm', 'cancel']);
const selectedVal = ref(null);

function handleConfirm() {
  emit('confirm', { confirmationId: props.confirmationId, selectedValue: selectedVal.value });
}
</script>
```

---

### 4.6 核心组件 5 & 6：多层级交互式穿透下钻系统（Drill-Down System）

下钻（Drill-Down）是企业经营问数中**最具商业价值的灵魂功能**。管理层在看大盘或战区数据时，核心诉求是**“定位差距来自哪个下级单元，追责并归因”**。

#### 4.6.1 下钻业务设计与穿透闭环机制

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│ 📍 穿透路径面包屑: [ 极光数智集团 ] > [ 华东战区 ] > [ 苏沪片区 ]                     │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│ ┌─────────────────────────────────────────────────────────────────────────────┐ │
│ │ 🏢 华东战区 · 经营综合概览卡片                                               │ │
│ │ 任务指标: 6,300.00 万元   实际开单: 3,556.70 万元   达成率: 56.46% (进度健康) │ │
│ │ [██████████████████████████████░░░░░░░░░░░░░░░░░░░░░░░] 56.46%               │ │
│ │                                                                             │ │
│ │ 💡 结构归因: 苏沪片区贡献全区 62% 开单，浙皖片区进度滞后(38.2%)，建议优先复核。 │ │
│ │                                                                             │ │
│ │ ▼ 点击展开/收起下属 2 个片区的明细钻取面板 (Drilldown Details)                │ │
│ └─────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                 │
│   ┌─────────────────────────────────────────────────────────────────────────┐   │
│   │ 📋 华东战区下属片区排行榜 (由高到低):                                    │   │
│   │ 1. 苏沪片区 | 目标: 3,500万 | 开单: 2,215万 | 达成率: 63.29% [🔍 继续下钻]│   │
│   │ 2. 浙皖片区 | 目标: 2,800万 | 开单: 1,341万 | 达成率: 47.89% [⚠️ 优先下钻]│   │
│   │                                                                         │   │
│   │ 🚀 智能追问联动:                                                        │   │
│   │ [ 💬 追问: 继续下钻浙皖片区的客户经理排名 ]   [ 💬 追问: 查苏沪片区的大单客户 ]│   │
│   └─────────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────────┘
```

**下钻业务红线原则**：
1. **先总后分原则**：下钻问题必须先输出上层父级汇总概览（Summary），再渲染下层子级明细（Details），**严禁直接跳到底层输出几十名员工的长名单**。
2. **风险阈值智能预警**：对达成率低于风险线（如 $< 50\%$）的节点自动标红徽章，并生成优先下钻建议。
3. **双模下钻交互**：
   - **面板内折叠展开（In-Place Expansion）**：不打断当前对话，直接在当前卡片内展开子级列表；
   - **流式追问穿透（Chat-Driven Drilldown）**：点击“继续下钻”快捷气泡，自动向聊天窗口发送语义追问（如：“*继续下钻到苏沪片区的客户经理明细*”），无缝保留历史上下文。

---

#### 4.6.2 核心组件 5：穿透下钻多级折叠卡片（`DrillDownCard.vue`）

```vue
<!-- frontend/src/components/DrillDownCard.vue -->
<template>
  <div class="drill-down-card bg-white border border-slate-200 rounded-xl p-4 my-3 shadow-xs">
    <!-- 1. 父级概览头部 -->
    <div class="flex items-start justify-between">
      <div class="flex items-center gap-2.5">
        <div class="w-8 h-8 rounded-lg bg-indigo-50 flex items-center justify-center text-indigo-600 font-bold text-sm">
          {{ nodeData.level === '战区' ? '大区' : '片区' }}
        </div>
        <div>
          <div class="flex items-center gap-2">
            <h4 class="text-sm font-bold text-slate-900">{{ nodeData.name }}</h4>
            <span 
              v-if="isRisk" 
              class="px-2 py-0.5 rounded-full text-[11px] font-medium bg-rose-50 text-rose-600 border border-rose-200 flex items-center gap-0.5"
            >
              ⚠️ 达成滞后
            </span>
            <span 
              v-else 
              class="px-2 py-0.5 rounded-full text-[11px] font-medium bg-emerald-50 text-emerald-600 border border-emerald-200"
            >
              ✔ 进度正常
            </span>
          </div>
          <div class="text-xs text-slate-500 mt-0.5">
            下辖 {{ nodeData.children?.length || 0 }} 个{{ nextLevelLabel }}
          </div>
        </div>
      </div>

      <!-- 下钻折叠切换按钮 -->
      <button 
        @click="isExpanded = !isExpanded" 
        class="flex items-center gap-1 px-3 py-1 text-xs font-medium rounded-lg border transition active:scale-95"
        :class="isExpanded ? 'bg-indigo-50 text-indigo-600 border-indigo-200' : 'bg-white text-slate-700 border-slate-300 hover:bg-slate-50'"
      >
        <span>{{ isExpanded ? '收起明细 ▲' : '下钻明细 ▼' }}</span>
      </button>
    </div>

    <!-- 2. KPI 指标对齐展示与进度条 -->
    <div class="grid grid-cols-4 gap-2 my-3 p-2.5 bg-slate-50 rounded-lg text-center text-xs">
      <div>
        <div class="text-slate-400">年度目标</div>
        <div class="font-semibold text-slate-800 mt-0.5">{{ formatMoney(nodeData.targetAmount) }}</div>
      </div>
      <div>
        <div class="text-slate-400">实际开单</div>
        <div class="font-semibold text-slate-800 mt-0.5">{{ formatMoney(nodeData.actualAmount) }}</div>
      </div>
      <div>
        <div class="text-slate-400">业绩缺口</div>
        <div class="font-semibold text-amber-600 mt-0.5">{{ formatMoney(nodeData.gapAmount) }}</div>
      </div>
      <div>
        <div class="text-slate-400">达成进度</div>
        <div class="font-bold mt-0.5" :class="isRisk ? 'text-rose-600' : 'text-emerald-600'">
          {{ nodeData.rate }}%
        </div>
      </div>
    </div>

    <!-- 进度条 -->
    <div class="w-full bg-slate-100 rounded-full h-1.5 overflow-hidden mb-3">
      <div 
        class="h-full rounded-full transition-all duration-500"
        :class="isRisk ? 'bg-rose-500' : 'bg-emerald-500'" 
        :style="{ width: Math.min(nodeData.rate, 100) + '%' }"
      ></div>
    </div>

    <!-- 3. 展开的下级明细钻取面板 (Drilldown Details Panel) -->
    <div v-if="isExpanded" class="mt-4 pt-3 border-t border-slate-100 animate-fadeIn">
      <div class="flex items-center justify-between mb-2">
        <span class="text-xs font-semibold text-slate-700 flex items-center gap-1">
          <span>下属{{ nextLevelLabel }}开单分布与对标明细</span>
        </span>
        <span class="text-[11px] text-slate-400">按开单金额降序排列</span>
      </div>

      <div class="divide-y divide-slate-100 border border-slate-100 rounded-lg overflow-hidden">
        <div 
          v-for="(child, idx) in nodeData.children" 
          :key="child.id || idx"
          class="flex items-center justify-between p-2.5 text-xs hover:bg-slate-50/80 transition"
        >
          <div class="flex items-center gap-2">
            <span class="w-4 text-center font-bold text-slate-400 text-[11px]">{{ idx + 1 }}</span>
            <div>
              <span class="font-medium text-slate-800">{{ child.name }}</span>
              <span v-if="child.rate < 50" class="ml-1 text-[10px] text-rose-500 font-medium">⚠️ 进度偏慢</span>
            </div>
          </div>

          <div class="flex items-center gap-4">
            <div class="text-right">
              <span class="font-semibold text-slate-800">{{ formatMoney(child.actualAmount) }}</span>
              <span class="text-slate-400 mx-1">/</span>
              <span class="text-slate-500">{{ child.rate }}%</span>
            </div>

            <!-- 点击触发进一步穿透或追问 -->
            <button 
              @click="$emit('drillToChild', { parent: nodeData, child: child, level: nextLevelLabel })"
              class="px-2 py-0.5 text-[11px] text-indigo-600 bg-indigo-50 hover:bg-indigo-100 rounded border border-indigo-200 transition active:scale-95"
            >
              继续穿透 ➔
            </button>
          </div>
        </div>
      </div>

      <!-- 智能追问快捷卡片 -->
      <div class="mt-3 flex flex-wrap items-center gap-2 pt-1 text-xs">
        <span class="text-slate-400 text-[11px]">快捷下钻追问:</span>
        <button 
          v-for="(prompt, pIdx) in suggestedDrillPrompts" 
          :key="pIdx"
          @click="$emit('sendPrompt', prompt)"
          class="px-2 py-1 rounded bg-slate-100 hover:bg-slate-200 text-slate-600 transition text-[11px]"
        >
          💬 {{ prompt }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';

const props = defineProps({
  nodeData: {
    type: Object,
    required: true
    /* 格式样例:
    {
      name: '华东战区',
      level: '战区',
      targetAmount: 63000000,
      actualAmount: 35567000,
      gapAmount: 27433000,
      rate: 56.46,
      children: [
        { id: 1, name: '苏沪片区', actualAmount: 22150000, targetAmount: 35000000, rate: 63.29 },
        { id: 2, name: '浙皖片区', actualAmount: 13417000, targetAmount: 28000000, rate: 47.89 }
      ]
    }
    */
  }
});

const emit = defineEmits(['drillToChild', 'sendPrompt']);
const isExpanded = ref(false);

const isRisk = computed(() => (props.nodeData?.rate || 0) < 50);

const nextLevelLabel = computed(() => {
  const map = { '事业群': '战区', '战区': '片区', '片区': '客户经理' };
  return map[props.nodeData?.level] || '子单元';
});

const suggestedDrillPrompts = computed(() => {
  const worstChild = [...(props.nodeData.children || [])].sort((a, b) => a.rate - b.rate)[0];
  const list = [];
  if (worstChild) {
    list.push(`分析${worstChild.name}的业绩缺口原因`);
    list.push(`继续下钻${worstChild.name}到客户经理明细`);
  }
  list.push(`拉出${props.nodeData.name}开单金额 Top 5 的大客户`);
  return list;
});

function formatMoney(val) {
  if (val == null) return '0.00 万元';
  return (val / 10000).toLocaleString('zh-CN', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) + ' 万元';
}
</script>

<style scoped>
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-4px); }
  to { opacity: 1; transform: translateY(0); }
}
.animate-fadeIn {
  animation: fadeIn 0.2s ease-out forwards;
}
</style>
```

---

#### 4.6.3 核心组件 6：穿透路径面包屑导航组件（`DrillBreadcrumb.vue`）

该组件让用户在多级下钻（事业群 $\rightarrow$ 战区 $\rightarrow$ 片区 $\rightarrow$ 客户经理）时随时清楚自己身处哪一层，并支持一键回溯到上级汇总：

```vue
<!-- frontend/src/components/DrillBreadcrumb.vue -->
<template>
  <nav class="flex items-center text-xs text-slate-500 py-1.5 px-3 bg-slate-50 border border-slate-200 rounded-lg mb-2 overflow-x-auto">
    <span class="text-slate-400 mr-2 flex items-center gap-1 font-medium">
      <svg class="w-3.5 h-3.5 text-indigo-500" fill="currentColor" viewBox="0 0 20 20">
        <path fill-rule="evenodd" d="M12.293 5.293a1 1 0 011.414 0l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-2.293-2.293a1 1 0 010-1.414z" clip-rule="evenodd" />
      </svg>
      当前穿透链路:
    </span>

    <ol class="flex items-center space-x-1">
      <li v-for="(crumb, idx) in pathList" :key="idx" class="flex items-center">
        <!-- 分隔符 -->
        <svg v-if="idx > 0" class="w-3 h-3 text-slate-300 mx-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
        </svg>

        <!-- 最后一级（当前聚焦层级）不可点 -->
        <span 
          v-if="idx === pathList.length - 1" 
          class="font-bold text-indigo-700 bg-indigo-50 px-2 py-0.5 rounded border border-indigo-200"
        >
          {{ crumb.name }} ({{ crumb.level }})
        </span>

        <!-- 上级路径可点击回跳 -->
        <button 
          v-else 
          @click="$emit('navigate', crumb)" 
          class="hover:text-indigo-600 hover:underline px-1 py-0.5 rounded transition"
        >
          {{ crumb.name }}
        </button>
      </li>
    </ol>
  </nav>
</template>

<script setup>
defineProps({
  pathList: {
    type: Array,
    required: true
    /* 格式样例:
    [
      { name: '智能出行事业群', level: '事业群', code: 'mobility_root' },
      { name: '华东战区', level: '战区', code: 'east_region' },
      { name: '苏沪片区', level: '片区', code: 'suhu_area' }
    ]
    */
  }
});

defineEmits(['navigate']);
</script>
```

---

## 五、核心防错红线与回归测试对账基准（Ground Truth）

开发新系统时，必须建立**基准对账库**，验证 AI 生成的 SQL 是否真正算准：

### 5.1 极光数智集团真实大盘基准数值 (Ground Truth)
```
【极光数智 2026 年度商用大盘权威基准】
- 年度总预算任务 (target_amount)       : 204,000,000.00 元 (2.04 亿元)
- 年度实际开单总额 (actual_amount)      : 96,926,500.00 元 (9,692.65 万元)
- 权威综合达成率 (completion_rate)    : 47.51%
- 整体年度任务缺口 (remaining_gap)    : 107,073,500.00 元 (1.07 亿元)
```

### 5.2 四大分公司全量真实对账排行
| 排名 | 分公司 / 战区名称 | 年度任务目标 (万元) | 实际开单金额 (万元) | 权威达成率 (%) | 剩余任务缺口 (万元) |
|:---:|:---|:---:|:---:|:---:|:---:|
| 1 | **华南战区** | 5,800.00 | **3,681.02** | 63.47% | 2,118.98 |
| 2 | **华东战区** | 6,300.00 | **3,556.70** | 56.46% | 2,743.30 |
| 3 | **华北战区** | 4,300.00 | **2,789.38** | 64.87% | 1,510.62 |
| 4 | **西部战区** | 4,000.00 | **2,662.55** | 66.56% | 1,337.45 |

### 5.3 细分业务线构成与严密勾稽公式
$$ \text{实际开单总盘}(9,692.65\text{万}) = \text{终端零售}(4,374.82\text{万}) + \text{政企定制}(3,203.50\text{万}) + \text{生态伙伴}(2,114.33\text{万}) $$
任何模型若在未限定 `business_segment` 时直接 `SUM`，得出的开单总盘将会膨胀成 $9692.65 \times 2 = 1.938\text{亿元}$，必须通过自动化测试一票否决！

---

## 六、前后端全双工/流式通信协议契约（SSE 规范）

### 6.1 `POST /api/chat/stream` 报文交互
- **Request Header**: `Content-Type: application/json`
- **Request Body**:
```json
{
  "conversation_id": "conv_9a8b7c6d",
  "query": "华南战区和华东战区的业绩对比",
  "dataset_code": "mobility_sales_overview",
  "history": [
    {"role": "user", "content": "华东战区完成率怎么样？"},
    {"role": "assistant", "content": "华东战区开单 3556.70 万元，达成率 56.46%..."}
  ]
}
```

- **SSE Response Stream (text/event-stream)**：
```http
event: step
data: {"stage": "ROUTING", "msg": "正在匹配业务数据集..."}

event: parse_bar
data: {"dataset_name": "智能出行经营总盘", "entities": {"org_nodes": [{"name": "华南战区", "level": "战区"}, {"name": "华东战区", "level": "战区"}], "business_segment": "总额(未拆分)"}, "intent_type": "compare"}

event: step
data: {"stage": "SQL_GEN", "msg": "正在基于 Bookshelf 规则生成对比查询 SQL..."}

event: sql_ready
data: {"sql": "SELECT 战区, SUM(目标金额) AS 目标金额, SUM(开单金额) AS 开单金额, ROUND(SUM(开单金额)/NULLIF(SUM(目标金额),0)*100, 2) AS 达成率 FROM v_sales_performance_standard WHERE 组织层级='战区' AND 战区 IN ('华南战区', '华东战区') AND 业务板块='总额(未拆分)' GROUP BY 战区;", "execution_time_ms": 38.5, "row_count": 2}

event: final_result
data: {"columns": ["战区", "目标金额", "开单金额", "达成率"], "rows": [["华南战区", 58000000.0, 36810200.0, 63.47], ["华东战区", 63000000.0, 35567000.0, 56.46]], "chart_type": "bar", "chart_config": {"title": "华南战区 VS 华东战区经营业绩对比", "xAxis": ["华南战区", "华东战区"], "series": [{"name": "开单金额", "type": "bar", "data": [36810200.0, 35567000.0]}]}, "insights": ["华南战区开单总额高出华东战区 124.32 万元，且达成率领先 7.01 个百分点。"]}

event: done
data: {"status": "SUCCESS"}
```

---

## 🚀 投喂给其他 AI 的启动提示词（Direct Instruction）

您可以直接复制下方提示词，并将本文件作为附件或完整粘贴发给新的 AI：

> **“你好！请作为顶级全栈架构师，根据这份《AuroraPulse 极光数智 · 企业级智能问数全栈重构白皮书》，为我全新重写整个系统。**
> 
> **请务必落实以下要点：**
> 1. **全链路脱敏**：采用白皮书中的『极光数智集团』虚拟资产，严禁出现任何旧系统的历史专有名词。
> 2. **后端核心逻辑**：采用 **FastAPI + AsyncPG**，完整实现 `FourAgentPipeline`、`NodeAliasMatcher`（前缀树错字快慢路径纠错）、`SQLGuard`（SQLGlot AST 语法树防御与行级权限注入）。
> 3. **前端 UI 交互**：采用 **Vue 3 + Vite + TailwindCSS + ECharts**，提供包含 `ParseBar.vue`（胶囊条可点击修改重跑）、`SqlDrawer.vue`（透明查看 SQL）、`AdaptiveChart.vue`（自适应图表与表格切换）、`ConfirmModal.vue`（歧义确认挂起）、`DrillDownCard.vue`（多层级折叠下钻与滞后警示卡片）以及 `DrillBreadcrumb.vue`（穿透路径面包屑导航）的完整实现。
> 4. **业务防重算与下钻硬约束**：大盘总额查询严格遵循 `business_segment = '总额(未拆分)'`，严格落实防跨级求和与除零保护；下钻严格遵守“先父级概览再子级明细”原则。
> 
> 请首先输出完整的系统工程目录结构，随后逐步提供后端与前端的关键核心可执行代码！”
