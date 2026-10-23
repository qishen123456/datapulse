# 治理工作台视觉重构 · 2026-10-23

## 设计 Token

实现文件：`datapivot-demo/frontend/src/styles/precision-theme.css`。

| 用途 | 值 |
| --- | --- |
| 主文字 | #0F172A |
| 正文 / 次要说明 | #334155 / #475569 |
| 辅助文字 | #64748B |
| 页面 / 面板 | #F8FAFC / #FFFFFF |
| 主操作 / 选中背景 | #2563EB / #EFF6FF |
| 成功文字 / 背景 | #047857 / #ECFDF5 |
| 危险文字 / 背景 | #BE123C / #FFF1F2 |
| 容器 / 控件圆角 | 12px / 8px |
| 阴影 | 0 2px 8px #0F172A06 |
| 交互过渡 | 150ms，尊重减少动态效果设置 |

数字采用 tabular-nums；组织编码与指令使用系统等宽字体。亮绿色不用于小字号正文。

## 按任务组织布局

- 控制台：分色指标区、大数字、56px 权限行与吸顶表头；保留原全选及保存逻辑，不虚构趋势。
- 专家协作：角色目录 + 指令文档工作台。新增行数、Token 估算、全屏、Esc 退出、追加结构草稿、本地非空检查。检查不是模型测试，估算不是计费 Token；保存后指令才生效。
- 组织树：树形引导线、等宽编码胶囊、属性检查器与编码复制。
- 账号：紧凑筛选组、匹配与选中数量、编辑与更多操作菜单；删除继续走已有二次确认。
- 迁移：JSON 拖入复用原读取与预检流程，遵循文件选择权限；读取新包时清空旧包与旧预检结果。
- 报告模板：顶部数据集选择带取代第二侧栏，首次进入自动读取首个数据集，不自动保存。
- 空状态：新增原创内联 SVG 组件 `components/GovernanceEmpty.vue`，不依赖外部插画。

核心页面代码：`datapivot-demo/frontend/src/views/AgentManagement.vue`、`OrganizationTrees.vue`、`EmployeePermissions.vue`、`RuntimeMigration.vue`、`DatasetReportConfig.vue`。

## 问数边界

根据用户后续授权，问数页面可以更改样式。本轮仅调整 `styles/analysisStudio.css` 颜色及共享视觉变量，没有修改问数状态机、权限、模型调用、双路径流程、报告逻辑或输入队列。

## 验收

- 生产构建通过；原有大 bundle 警告仍存在。
- 27 项问数流程、公共事实、结果呈现和队列测试通过。
- 13 模块浏览器渲染、页签操作、账号键盘操作、侧栏折叠与响应式检查通过。
- 隔离数据问数浏览器回归通过：计划选择、显式确认、证据报告、详情栏与响应式；未调用外部模型。
- 新增 `scripts/test-governance-precision.mjs` 验证全屏草稿、组织属性、账号菜单、JSON 拖入、报告顶部布局，以及六个治理页 1440/390 宽度。测试不保存配置、不删除账号、不正式导入数据。
- 本轮仅更新前端容器；后端与数据库未重建。

开发验收截图：`/private/tmp/datapulse-precision/`。
部署验收截图：`/private/tmp/datapulse-precision-deployed/`。

## 第二轮：按任务区分工作面

用户否定第一轮视觉后，重做信息层级，而非继续统一卡片装饰：
- 专家角色改为横向选择，主要工作区改为指令文档 + 执行边界侧注；保留所有指令、知识、资料与配置操作。
- 控制台改为局部纵向导航 + 权限台账，移除指标彩色卡片底色，减少表格嵌套边框。
- 组织树突出主画布与属性检查器，指标收为轻量计数行。
- 问数首页改为编辑式排版：业务问题标题、方法侧注、编号问题目录。问题来源、刷新、点击带入与授权范围仍保留。
- 导航使用低饱和灰底，主操作使用石墨色，蓝色保留给选中与焦点。修正输入框遗留绿色焦点与环绕动效颜色；动效与执行逻辑保留。
- 参考原则：Linear 的内容优先和稳定操作位置（https://linear.app/now/behind-the-latest-design-refresh）；Supabase Studio 的编辑上下文和检查面板（https://supabase.com/blog/tabs-dashboard-updates）。没有复制其品牌资产。

第二轮验证：生产构建、13 模块浏览器检查、六个治理页面 1440/390 宽度、新增治理交互、问数隔离数据回归均通过。截图位于 `/private/tmp/datapulse-editorial/` 与 `/private/tmp/datapulse-editorial-all/`。此次无后端改动。
