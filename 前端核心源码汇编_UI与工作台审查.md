# DataPulse 前端核心架构与 UI 源码汇编

> 本文档汇总了前端关键样式系统、外层框架（Header / Sidebar / Layout）、技能与智能体管理、数据集管理以及问数工作台的完整源码，供前端架构与 UI/UX 专家进行全面审查。

## 目录结构索引

- [全局样式与基础规范 (src/style.css)](#全局样式与基础规范-srcstyle.css)
- [模块内部新版设计样式 (src/styles/module-interiors.css)](#模块内部新版设计样式-srcstylesmodule-interiors.css)
- [设计系统色彩与微交互 (src/styles/precision-theme.css)](#设计系统色彩与微交互-srcstylesprecision-theme.css)
- [外层框架与全局导航 (src/App.vue)](#外层框架与全局导航-srcApp.vue)
- [智能体管线与技能管理 (src/views/AgentManagement.vue)](#智能体管线与技能管理-srcviewsAgentManagement.vue)
- [专家分析与技能呈现卡片 (src/components/askdesk/AnalysisBrief.vue)](#专家分析与技能呈现卡片-srccomponentsaskdeskAnalysisBrief.vue)
- [数据集资产管理页面 (src/views/DatasetManagement.vue)](#数据集资产管理页面-srcviewsDatasetManagement.vue)
- [问数工作台核心页面 (src/views/AskDesk.vue)](#问数工作台核心页面-srcviewsAskDesk.vue)

---

## 全局样式与基础规范 (src/style.css)

**文件路径**: `datapivot-demo/frontend/src/style.css`

```css
/* ===== 全局基础重置 ===== */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body {
  width: 100%;
  height: 100%;
  overflow: hidden;
}

body {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-rendering: optimizeLegibility;
  background: var(--bg-page, #F2F5F4);
  color: var(--text-title, #0F172A);
}

#app {
  width: 100%;
  height: 100%;
}

a {
  color: inherit;
  text-decoration: none;
}

button {
  border: none;
  background: none;
  cursor: pointer;
  font-family: inherit;
}

input, textarea, select {
  font-family: inherit;
}

ul, ol {
  list-style: none;
}

img {
  max-width: 100%;
  display: block;
}

/* 滚动条美化 */
::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}

::-webkit-scrollbar-track {
  background: transparent;
}

::-webkit-scrollbar-thumb {
  background: var(--border, #E5E7EB);
  border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
  background: var(--border-hover, #D1D5DB);
}

```

---

## 模块内部新版设计样式 (src/styles/module-interiors.css)

**文件路径**: `datapivot-demo/frontend/src/styles/module-interiors.css`

```css
/* Module interiors only. Every selector requires a module root; no shell or ask selectors. */
.workspace-shell .page-wrap .module-layout-v4 {
  --module-line: #e5eaf1;
  --module-muted: #526174
}

/* Connections: inspect the selected endpoint above an edge-to-edge inventory. */
.workspace-shell .page-wrap .module-layout-v4.db-page .db-workbench {
  display: flex;
  flex-direction: column;
  gap: 22px;
  background: transparent;
  border: 0 !important;
  box-shadow: none !important
}

.workspace-shell .page-wrap .module-layout-v4.db-page .db-detail {
  display: grid;
  grid-template-columns: 38px minmax(150px, .8fr) auto;
  gap: 8px 18px;
  align-items: center;
  width: auto;
  background: #f4f6fa !important;
  border: 0;
  border-radius: 10px;
  padding: 24px;
  position: static;
  min-width: 0
}

.workspace-shell .page-wrap .module-layout-v4.db-page .db-detail-mark {
  grid-column: 1;
  grid-row: 1/3;
  width: 36px;
  height: 36px;
  margin: 0;
  background: #e4eaf3;
  color: #334155;
  border-radius: 8px
}

.workspace-shell .page-wrap .module-layout-v4.db-page .db-detail-eyebrow {
  grid-column: 2;
  grid-row: 1;
  margin: 0;
  font-size: 10px
}

.workspace-shell .page-wrap .module-layout-v4.db-page .db-detail h3 {
  grid-column: 2;
  grid-row: 2;
  font-size: 18px;
  margin: 0
}

.workspace-shell .page-wrap .module-layout-v4.db-page .db-engine {
  grid-column: 3;
  grid-row: 1/3;
  justify-self: end;
  margin: 0
}

.workspace-shell .page-wrap .module-layout-v4.db-page .db-detail dl {
  grid-column: 1/-1;
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1.2fr;
  gap: 20px;
  border-top: 1px solid #e1e6ee;
  margin: 14px 0 0;
  padding-top: 20px
}

.workspace-shell .page-wrap .module-layout-v4.db-page .db-detail dl>div {
  padding: 0;
  border: 0;
  min-width: 0
}

.workspace-shell .page-wrap .module-layout-v4.db-page .db-detail dd {
  overflow-wrap: anywhere;
  margin: 8px 0 0;
  font-size: 13px
}

.workspace-shell .page-wrap .module-layout-v4.db-page .db-detail-actions {
  grid-column: 1/-1;
  display: flex;
  gap: 8px;
  margin-top: 10px;
  padding: 0;
  border: 0
}

.workspace-shell .page-wrap .module-layout-v4.db-page .db-inventory {
  width: 100%;
  min-width: 0
}

.workspace-shell .page-wrap .module-layout-v4.db-page .admin-table-card {
  border: 0 !important;
  border-radius: 0 !important;
  box-shadow: none !important
}

.workspace-shell .page-wrap .module-layout-v4.db-page .admin-table-card>.el-card__body {
  padding: 0
}

.workspace-shell .page-wrap .module-layout-v4.db-page .admin-table-card>.el-card__header {
  padding: 12px 0
}

/* Model services: providers are a horizontal catalog, settings are the main document. */
.workspace-shell .page-wrap .module-layout-v4.cs-page .cs-layout {
  display: flex;
  flex-direction: column;
  gap: 24px;
  border: 0;
  overflow: visible
}

.workspace-shell .page-wrap .module-layout-v4.cs-page .cs-sidebar {
  width: 100%;
  min-width: 0;
  display: grid;
  grid-template-columns: 150px minmax(0, 1fr) auto;
  align-items: center;
  gap: 18px;
  padding: 16px;
  background: #f4f6fa;
  border: 0;
  border-radius: 10px;
  box-sizing: border-box
}

.workspace-shell .page-wrap .module-layout-v4.cs-page .cs-sidebar-head {
  padding: 0;
  border: 0
}

.workspace-shell .page-wrap .module-layout-v4.cs-page .cs-sidebar-scroll {
  display: flex;
  gap: 8px;
  min-width: 0;
  overflow-x: auto;
  padding: 4px;
  flex: none
}

.workspace-shell .page-wrap .module-layout-v4.cs-page .cs-ch-item {
  flex: 0 0 190px;
  margin: 0;
  padding: 12px;
  min-height: 70px;
  border-radius: 8px;
  background: #fff;
  border: 1px solid transparent;
  box-shadow: none
}

.workspace-shell .page-wrap .module-layout-v4.cs-page .cs-ch-item.is-active {
  border-color: #9cb4d8;
  background: #fff;
  box-shadow: 0 2px 6px #17212f07
}

.workspace-shell .page-wrap .module-layout-v4.cs-page .cs-ch-icon {
  width: 28px;
  height: 28px;
  background: #edf1f7;
  box-shadow: none;
  border-radius: 7px;
  color: #334155
}

.workspace-shell .page-wrap .module-layout-v4.cs-page .cs-sidebar-footer {
  padding: 0;
  border: 0
}

.workspace-shell .page-wrap .module-layout-v4.cs-page .cs-main {
  padding: 0;
  overflow: visible;
  border: 0 !important;
  background: white
}

.workspace-shell .page-wrap .module-layout-v4.cs-page .cs-hero {
  background: white;
  border: 0;
  border-bottom: 1px solid var(--module-line);
  border-radius: 0;
  padding: 0 0 22px
}

.workspace-shell .page-wrap .module-layout-v4.cs-page .cs-config-grid {
  grid-template-columns: minmax(0, 1fr);
  max-width: 900px;
  gap: 0
}

.workspace-shell .page-wrap .module-layout-v4.cs-page .cs-config-card {
  border: 0;
  border-bottom: 1px solid var(--module-line);
  border-radius: 0;
  padding: 24px 0;
  display: grid;
  grid-template-columns: 220px minmax(0, 1fr);
  gap: 24px;
  background: #fff;
  box-shadow: none
}

.workspace-shell .page-wrap .module-layout-v4.cs-page .cs-section-head {
  margin: 0;
  align-items: flex-start
}

.workspace-shell .page-wrap .module-layout-v4.cs-page .cs-provider-icon {
  width: 40px;
  height: 40px;
  box-shadow: none;
  background: #e7edf6;
  color: #334155;
  border-radius: 8px
}

/* Dataset knowledge: asset switcher across the top, knowledge workspace underneath. */
.workspace-shell .page-wrap .module-layout-v4.dataset-page .dataset-workspace {
  display: flex;
  flex-direction: column;
  border: 0 !important;
  overflow: visible
}

.workspace-shell .page-wrap .module-layout-v4.dataset-page .dataset-catalog {
  width: 100%;
  min-width: 0;
  padding: 16px;
  background: #f4f6fa !important;
  border: 0;
  border-radius: 10px;
  display: grid;
  grid-template-columns: 210px minmax(0, 1fr);
  gap: 12px 20px;
  box-sizing: border-box
}

.workspace-shell .page-wrap .module-layout-v4.dataset-page .catalog-heading {
  grid-column: 1;
  margin: 0;
  padding: 0;
  align-self: start
}

.workspace-shell .page-wrap .module-layout-v4.dataset-page .toolbar-col {
  grid-column: 1;
  grid-row: 2;
  gap: 8px
}

.workspace-shell .page-wrap .module-layout-v4.dataset-page .dataset-catalog-list {
  grid-column: 2;
  grid-row: 1/3;
  display: flex;
  overflow: auto;
  gap: 10px;
  padding: 3px;
  min-height: 0;
  max-height: none
}

.workspace-shell .page-wrap .module-layout-v4.dataset-page .dataset-tile {
  flex: 0 0 245px;
  margin: 0;
  padding: 16px;
  align-self: stretch;
  background: #fff;
  border: 1px solid transparent;
  min-height: 115px;
  box-shadow: none
}

.workspace-shell .page-wrap .module-layout-v4.dataset-page .dataset-tile.active {
  border-color: #9cb4d8;
  background: #fff;
  box-shadow: 0 2px 6px #17212f07
}

.workspace-shell .page-wrap .module-layout-v4.dataset-page .catalog-footnote {
  grid-column: 1/-1;
  padding: 0;
  border: 0;
  margin: 0
}

.workspace-shell .page-wrap .module-layout-v4.dataset-page .dataset-editor {
  border: 0;
  min-width: 0
}

.workspace-shell .page-wrap .module-layout-v4.dataset-page .dataset-identity {
  padding: 28px 0 22px
}

.workspace-shell .page-wrap .module-layout-v4.dataset-page .dataset-editor-body {
  padding: 0
}

.workspace-shell .page-wrap .module-layout-v4.dataset-page .dataset-properties {
  margin-top: 0
}

/* Organization: types are top-level tabs; tree and property inspector share the canvas. */
.workspace-shell .page-wrap .module-layout-v4.org-page .workspace {
  display: flex;
  flex-direction: column;
  gap: 22px
}

.workspace-shell .page-wrap .module-layout-v4.org-page .type-panel {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 10px;
  width: 100%;
  padding: 12px;
  background: #f4f6fa;
  border: 0;
  border-radius: 10px;
  box-sizing: border-box
}

.workspace-shell .page-wrap .module-layout-v4.org-page .type-panel .panel-head {
  margin: 0;
  padding: 0 14px 0 0;
  border: 0;
  min-width: 120px
}

.workspace-shell .page-wrap .module-layout-v4.org-page .type-panel .panel-head h2 {
  font-size: 13px
}

.workspace-shell .page-wrap .module-layout-v4.org-page .type-panel .panel-head p {
  font-size: 11px
}

.workspace-shell .page-wrap .module-layout-v4.org-page .type-item {
  width: auto;
  min-width: 210px;
  margin: 0;
  padding: 14px 18px;
  border: 1px solid transparent;
  background: white
}

.workspace-shell .page-wrap .module-layout-v4.org-page .type-item.active {
  background: #fff;
  border-color: #9cb4d8
}

.workspace-shell .page-wrap .module-layout-v4.org-page .detail-panel {
  padding: 0;
  border: 0;
  box-shadow: none
}

.workspace-shell .page-wrap .module-layout-v4.org-page .tree-layout {
  grid-template-columns: minmax(0, 1fr) 300px;
  gap: 24px
}

.workspace-shell .page-wrap .module-layout-v4.org-page .tree-box {
  padding: 16px;
  background: #fff;
  border: 1px solid #e5eaf1;
  border-radius: 10px;
  max-height: 650px;
  overflow: auto
}

.workspace-shell .page-wrap .module-layout-v4.org-page .node-panel {
  position: sticky;
  top: 0;
  align-self: start;
  min-height: 360px
}

/* Sync: tasks own the left canvas, counts become a compact operational side strip. */
.workspace-shell .page-wrap .module-layout-v4.fs-page {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 190px;
  gap: 0 24px;
  align-items: start
}

.workspace-shell .page-wrap .module-layout-v4.fs-page>.fs-hero {
  grid-column: 1/-1
}

.workspace-shell .page-wrap .module-layout-v4.fs-page>.fs-stat-grid {
  grid-column: 2;
  grid-row: 2;
  display: flex;
  flex-direction: column;
  gap: 0;
  border: 0;
  background: #f4f6fa;
  border-radius: 10px;
  padding: 8px 18px;
  margin: 0
}

.workspace-shell .page-wrap .module-layout-v4.fs-page .fs-stat-card {
  padding: 18px 0;
  border: 0;
  border-bottom: 1px solid #e1e6ee;
  border-radius: 0;
  background: transparent;
  box-shadow: none;
  min-height: 0
}

.workspace-shell .page-wrap .module-layout-v4.fs-page .fs-stat-card:last-child {
  border-bottom: 0
}

.workspace-shell .page-wrap .module-layout-v4.fs-page .fs-stat-copy {
  display: flex;
  flex-direction: column;
  gap: 6px
}

.workspace-shell .page-wrap .module-layout-v4.fs-page .fs-stat-copy strong {
  font-size: 28px;
  line-height: 1.4;
  font-weight: 500
}

.workspace-shell .page-wrap .module-layout-v4.fs-page>.fs-ops-board {
  grid-column: 1;
  grid-row: 2;
  min-width: 0;
  padding: 0;
  border: 0 !important;
  box-shadow: none !important
}

.workspace-shell .page-wrap .module-layout-v4.fs-page .fs-ops-panel {
  padding-inline: 0
}

/* Release: import and impact preview come first, resources are an optional audit appendix. */
.workspace-shell .page-wrap .module-layout-v4.migration-page .workbench {
  padding-top: 0;
  border-top: 0;
  grid-template-columns: minmax(300px, .8fr) minmax(0, 1.2fr);
  gap: 28px
}

.release-resource-drawer {
  margin-top: 24px;
  border: 1px solid #e5eaf1;
  border-radius: 10px;
  padding: 18px
}

.release-resource-drawer>summary {
  font-size: 13px;
  font-weight: 550;
  color: #334155;
  cursor: pointer
}

.release-resource-drawer[open]>summary {
  margin-bottom: 20px
}

.workspace-shell .page-wrap .module-layout-v4.migration-page .metric-grid {
  grid-template-columns: repeat(3, minmax(0, 1fr));
  border: 0;
  gap: 12px
}

.workspace-shell .page-wrap .module-layout-v4.migration-page .metric-card {
  background: #f4f6fa !important;
  border: 0 !important;
  border-radius: 8px !important
}

/* Accounts: selection actions share the list toolbar, descriptive fields keep more room. */
.workspace-shell .page-wrap .module-layout-v4.permission-page .toolbar {
  display: grid;
  grid-template-columns: minmax(240px, 1fr) 160px 150px auto;
  gap: 12px
}

.workspace-shell .page-wrap .module-layout-v4.permission-page .user-table-card {
  border: 1px solid #e5eaf1;
  border-radius: 10px;
  overflow: hidden;
  padding: 0
}

.workspace-shell .page-wrap .module-layout-v4.permission-page .el-table td {
  height: 64px
}

/* Skill workspace: separate section index and editable capability surface. */
.workspace-shell .page-wrap .module-layout-v4.advanced-page .advanced-workbench {
  padding: 0;
  border: 0
}

.workspace-shell .page-wrap .module-layout-v4.advanced-page .advanced-tabs>.el-tabs__header {
  width: 155px;
  padding: 12px;
  background: #f4f6fa;
  border-radius: 10px;
  margin-right: 26px
}

.workspace-shell .page-wrap .module-layout-v4.advanced-page .advanced-tabs>.el-tabs__content {
  padding: 0;
  min-width: 0
}

.workspace-shell .page-wrap .module-layout-v4.advanced-page .advanced-tabs .el-tabs__item {
  justify-content: flex-start;
  text-align: left;
  height: 44px
}

.workspace-shell .page-wrap .module-layout-v4.advanced-page .plain-panel {
  padding: 0;
  border: 0;
  box-shadow: none
}

@media(max-width:1100px) {
  .workspace-shell .page-wrap .module-layout-v4.fs-page {
    grid-template-columns: minmax(0, 1fr)
  }

  .workspace-shell .page-wrap .module-layout-v4.fs-page>.fs-stat-grid {
    grid-column: 1;
    grid-row: 2;
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 16px;
    margin-bottom: 20px
  }

  .workspace-shell .page-wrap .module-layout-v4.fs-page>.fs-ops-board {
    grid-row: 3
  }

  .workspace-shell .page-wrap .module-layout-v4.cs-page .cs-sidebar {
    grid-template-columns: 1fr
  }

  .workspace-shell .page-wrap .module-layout-v4.cs-page .cs-sidebar-scroll {
    width: 100%
  }

  .workspace-shell .page-wrap .module-layout-v4.cs-page .cs-config-card {
    grid-template-columns: 180px minmax(0, 1fr)
  }

  .workspace-shell .page-wrap .module-layout-v4.org-page .tree-layout {
    grid-template-columns: minmax(0, 1fr) 260px
  }
}

@media(max-width:720px) {
  .workspace-shell .page-wrap .module-layout-v4.db-page .db-detail {
    padding: 16px;
    grid-template-columns: 32px minmax(0, 1fr)
  }

  .workspace-shell .page-wrap .module-layout-v4.db-page .db-engine {
    grid-column: 2;
    grid-row: 3;
    justify-self: start
  }

  .workspace-shell .page-wrap .module-layout-v4.db-page .db-detail dl {
    grid-template-columns: 1fr 1fr;
    gap: 20px 12px
  }

  .workspace-shell .page-wrap .module-layout-v4.cs-page .cs-config-card {
    grid-template-columns: 1fr;
    gap: 16px
  }

  .workspace-shell .page-wrap .module-layout-v4.dataset-page .dataset-catalog {
    grid-template-columns: 1fr
  }

  .workspace-shell .page-wrap .module-layout-v4.dataset-page .dataset-catalog-list {
    grid-column: 1;
    grid-row: 3
  }

  .workspace-shell .page-wrap .module-layout-v4.dataset-page .catalog-footnote {
    grid-row: 4
  }

  .workspace-shell .page-wrap .module-layout-v4.org-page .tree-layout {
    grid-template-columns: 1fr
  }

  .workspace-shell .page-wrap .module-layout-v4.org-page .node-panel {
    position: static
  }

  .workspace-shell .page-wrap .module-layout-v4.migration-page .workbench {
    grid-template-columns: 1fr
  }

  .workspace-shell .page-wrap .module-layout-v4.migration-page .metric-grid {
    grid-template-columns: 1fr 1fr
  }

  .workspace-shell .page-wrap .module-layout-v4.permission-page .toolbar {
    grid-template-columns: 1fr
  }

  .workspace-shell .page-wrap .module-layout-v4.fs-page>.fs-stat-grid {
    grid-template-columns: 1fr 1fr
  }

  .workspace-shell .page-wrap .module-layout-v4.advanced-page .advanced-tabs>.el-tabs__header {
    width: 120px;
    margin-right: 14px;
    padding: 6px
  }

  .workspace-shell .page-wrap .module-layout-v4.advanced-page .advanced-tabs .el-tabs__item {
    font-size: 12px !important
  }
}

.workspace-shell .page-wrap .module-layout-v4.permission-page .account-bulk-actions {
  grid-column: 1/-1;
  display: flex;
  align-items: center;
  gap: 10px;
  border-top: 1px solid #e1e6ee;
  padding-top: 12px
}

.workspace-shell .page-wrap .module-layout-v4.permission-page .account-bulk-actions>span {
  margin-right: auto;
  font-size: 12px;
  color: #475569
}

.workspace-shell .page-wrap .module-layout-v4.fs-page {
  align-content: start;
  grid-template-rows: auto auto;
  min-height: 0
}

.workspace-shell .page-wrap .module-layout-v4.cs-page .cs-sidebar-scroll {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  overflow: visible
}

.workspace-shell .page-wrap .module-layout-v4.cs-page .cs-ch-item {
  min-width: 0;
  width: 100%;
  box-sizing: border-box
}

@media(max-width:720px) {
  .workspace-shell .page-wrap .module-layout-v4.cs-page .cs-sidebar-scroll {
    grid-template-columns: repeat(2, minmax(0, 1fr))
  }

  .workspace-shell .page-wrap .module-layout-v4.cs-page .cs-ch-item {
    padding: 10px 8px;
    gap: 8px
  }

  .workspace-shell .page-wrap .module-layout-v4.cs-page .cs-ch-icon {
    display: none
  }
}
```

---

## 设计系统色彩与微交互 (src/styles/precision-theme.css)

**文件路径**: `datapivot-demo/frontend/src/styles/precision-theme.css`

```css
/* Precision workspace tokens. Presentation only; no workflow or permission overrides. */
:root {
 --studio-bg:#f8fafc;--studio-surface:#fff;--studio-ink:#0f172a;--studio-muted:#475569;--studio-accent:#2563eb;--studio-line:#e2e8f0;--studio-soft:#eff6ff;--studio-action:#2563eb;
 --brand-primary:#2563eb;--brand-primary-hover:#1d4ed8;--brand-primary-active:#1e40af;--brand-primary-soft:#eff6ff;--brand-primary-soft-2:#f8fafc;--brand-primary-focus:#2563eb14;--brand-primary-focus-strong:#2563eb26;--brand-action:#2563eb;--brand-accent:#2563eb;
 --color-primary:#2563eb;--bg-page:#f8fafc;--bg-soft:#f1f5f9;--bg-hover:#eff6ff;--border:#dbe3ed;--border-light:#edf2f7;--border-hover:#94a3b8;
 --text-title:#0f172a;--text-body:#334155;--text-secondary:#475569;--text-muted:#64748b;--text-placeholder:#64748b;
 --el-color-primary:#2563eb;--el-color-primary-dark-2:#1d4ed8;--el-color-primary-light-3:#60a5fa;--el-color-primary-light-5:#93c5fd;--el-color-primary-light-7:#bfdbfe;--el-color-primary-light-8:#dbeafe;--el-color-primary-light-9:#eff6ff;
 --el-text-color-primary:#0f172a;--el-text-color-regular:#334155;--el-text-color-secondary:#475569;--el-text-color-placeholder:#64748b;--el-fill-color-light:#f8fafc;--el-border-color:#dbe3ed;--el-border-color-light:#e2e8f0;
 --radius-card:12px;--radius-md:8px;--shadow-xs:0 1px 2px #0f172a05;--shadow-sm:0 2px 8px #0f172a06;
}
.workspace-shell.app-shell{background:#f8fafc}
.workspace-shell .workspace-nav{background:rgba(248,250,252,.94);backdrop-filter:blur(16px);border-right:1px solid #e2e8f0}
.workspace-shell .workspace-nav-link{color:#475569;position:relative;transition:background 150ms,color 150ms}
.workspace-shell .workspace-nav-link[aria-current=page]{color:#1d4ed8;background:#2563eb0d}
.workspace-shell .workspace-nav-link[aria-current=page]:before{background:#2563eb;width:3px}
.workspace-shell .workspace-nav-group h2{color:#64748b;font-size:11px;letter-spacing:.06em}
.workspace-shell .workspace-bar{background:#ffffffeb;border-bottom:1px solid #edf2f7}
.workspace-shell .workspace-nav .topnav-user-chip{background:#fff!important;border:1px solid #e2e8f0!important;border-radius:12px!important;box-shadow:var(--shadow-xs)}
.workspace-shell .workspace-nav .topnav-user-dropdown{border-radius:14px;box-shadow:0 12px 40px #0f172a18}
.workspace-shell .workspace-nav .topnav-user-dropdown button:hover{background:#f1f5f9}
.workspace-shell .el-button:not(.is-link):not(.is-text){border-radius:8px!important}
.workspace-shell .el-button--danger.is-link{background:#fff1f2!important;color:#be123c!important;border:1px solid #fecdd3!important;padding:5px 10px}
.workspace-shell .el-tag{border-radius:100px!important}.workspace-shell .el-tag--success{color:#047857;background:#ecfdf5}
.workspace-shell .el-table{--el-table-text-color:#334155;--el-table-row-hover-bg-color:#f8fafc}
.workspace-shell .el-table th.el-table__cell{background:#f8fafc!important;color:#475569!important}
.workspace-shell .el-table__body tr:hover>td.el-table__cell{background:#f8fafc!important}
.workspace-shell .el-switch{--el-switch-on-color:#2563eb;--el-switch-off-color:#cbd5e1}
/* Console: compact control navigation and a readable permission ledger. */
.workspace-shell .page-wrap .console-page .summary-strip{border:0;background:transparent;gap:12px;overflow:visible}
.workspace-shell .page-wrap .console-page .summary-strip>div{border:0;border-radius:12px;background:#eff6ff;padding:20px 24px;display:flex;align-items:baseline;gap:12px;box-shadow:var(--shadow-xs)}
.workspace-shell .page-wrap .console-page .summary-strip>div:nth-child(2){background:#f1f5f9}
.workspace-shell .page-wrap .console-page .summary-strip>div:nth-child(3){background:#ecfdf5}
.workspace-shell .page-wrap .console-page .summary-strip>div:nth-child(4){background:#fff7ed}
.workspace-shell .page-wrap .console-page .summary-strip strong{font-size:30px;font-variant-numeric:tabular-nums;letter-spacing:-1px;color:#0f172a}
.workspace-shell .page-wrap .console-tabs{border:0;border-bottom:1px solid #e2e8f0;background:transparent;border-radius:0;padding:0 0 10px;gap:8px}
.workspace-shell .page-wrap .console-page .matrix-row{min-height:56px;transition:background 150ms}
.workspace-shell .page-wrap .console-page .matrix-row:not(.matrix-head):hover{background:#f8fafc}
.workspace-shell .page-wrap .console-page .matrix-head{position:sticky;top:0;z-index:3;background:#f1f5f9;color:#475569;box-shadow:0 1px 0 #e2e8f0}
.workspace-shell .page-wrap .console-page .feature-col :is(p,small){color:#475569}
/* Expert studio: instruction document with its own editing tools. */
.workspace-shell .page-wrap .agent-workbench{border:0!important;box-shadow:0 2px 16px #0f172a08;grid-template-columns:260px minmax(0,1fr)}
.workspace-shell .page-wrap .agent-rail{background:#f1f5f9!important;border-right:0!important}
.workspace-shell .page-wrap .agent-card.active{background:#fff!important;border-color:transparent!important;box-shadow:0 3px 12px #0f172a0d!important;transform:translateX(3px)}
.workspace-shell .page-wrap .agent-card-copy strong{color:#0f172a}.workspace-shell .page-wrap .agent-card-copy small{color:#475569}
.workspace-shell .page-wrap .agent-editor .editor-content{background:#fff;padding-top:16px}
.instruction-toolbar{display:flex;align-items:center;gap:16px;flex-wrap:wrap;background:#f1f5f9;padding:12px 14px;border-radius:10px 10px 0 0;font:12px ui-monospace,SFMono-Regular,monospace;color:#475569}
.instruction-toolbar>div{margin-left:auto;display:flex;gap:6px}.instruction-toolbar .el-button+.el-button{margin-left:0}
.workspace-shell .page-wrap .agent-editor .prompt-input textarea{border-radius:0 0 10px 10px!important;box-shadow:none!important;background:#f8fafc!important;color:#0f172a!important;font:13px/2 ui-monospace,SFMono-Regular,'PingFang SC',monospace!important;min-height:360px;padding:24px!important}
.workspace-shell .page-wrap .instruction-section.editor-expanded{position:fixed;inset:20px;z-index:2100;background:white;padding:28px;box-shadow:0 0 0 100vmax #0f172a80;border-radius:12px;overflow:auto}
.workspace-shell .page-wrap .instruction-section.editor-expanded textarea{height:calc(100dvh - 260px)}
/* Organization: a directory rail, branching canvas and a property inspector. */
.workspace-shell .page-wrap .org-page .stat-grid{background:transparent;border:0;gap:20px;margin-bottom:24px}
.workspace-shell .page-wrap .org-page .stat-item{background:transparent;border:0;border-left:2px solid #dbeafe;border-radius:0;padding:4px 18px}
.workspace-shell .page-wrap .org-page .workspace{gap:20px;grid-template-columns:220px minmax(0,1fr)}
.workspace-shell .page-wrap .org-page .type-panel{background:transparent;border:0;padding:12px 0}
.workspace-shell .page-wrap .org-page .type-item{background:transparent;border:0;border-radius:8px}
.workspace-shell .page-wrap .org-page .type-item.active{background:#eff6ff;border-color:transparent;color:#1d4ed8}
.workspace-shell .page-wrap .org-page .detail-panel{border:0;box-shadow:var(--shadow-sm);padding:24px}
.workspace-shell .page-wrap .org-page .tree-box{border:0;background:#fff}
.workspace-shell .page-wrap .org-page .node-panel{background:#f8fafc;border:0;box-shadow:none;border-radius:12px}
.workspace-shell .page-wrap .org-page .el-tree-node__children{margin-left:8px;border-left:1px dashed #cbd5e1}
.workspace-shell .page-wrap .org-page .el-tree-node__content{min-height:56px}
.node-code,.copy-code{font:11px/1.6 ui-monospace,SFMono-Regular,monospace;background:#f1f5f9;color:#475569;padding:2px 6px;border-radius:5px;width:fit-content}
.copy-code{display:inline-flex;align-items:center;gap:8px;max-width:100%;overflow-wrap:anywhere;cursor:pointer}
/* Account directory: unified toolbar, list caption, inline action group. */
.workspace-shell .page-wrap .permission-page .toolbar{justify-content:flex-start;grid-template-columns:minmax(220px,420px) 160px 160px;border:0;border-radius:12px 12px 0 0;padding:16px 20px;margin-bottom:0;background:#fff}
.workspace-shell .page-wrap .permission-page .user-table-card{border:0;border-radius:0 0 12px 12px;padding:0 20px 12px;box-shadow:var(--shadow-sm)}
.account-list-caption{display:flex;justify-content:space-between;align-items:center;padding:18px 0;font-size:13px;color:#475569}.account-list-caption strong{color:#0f172a}
.workspace-shell .page-wrap .permission-page .el-table td{height:56px;font-variant-numeric:tabular-nums}
.workspace-shell .page-wrap .permission-page .status-switch{min-width:36px}.workspace-shell .page-wrap .permission-page .status-switch .el-switch__core{min-width:36px!important;width:36px;height:20px}
/* Migration is a staged release surface; only the upload area accepts drops. */
.workspace-shell .page-wrap .migration-page .upload-zone{border:1px dashed #94a3b8;border-radius:12px;background:#f8fafc;padding:28px;min-height:150px;transition:background 150ms,border-color 150ms}
.workspace-shell .page-wrap .migration-page .upload-zone.is-dragging{background:#eff6ff;border-color:#2563eb;box-shadow:0 0 0 4px #2563eb12}
.workspace-shell .page-wrap .migration-page .file-picker{background:#2563eb;color:#fff;border-radius:8px}
.workspace-shell .page-wrap .migration-page .workbench{grid-template-columns:minmax(300px,.8fr) minmax(400px,1.2fr);gap:20px}
.workspace-shell .page-wrap .migration-page .panel-card{border:0!important;box-shadow:var(--shadow-sm)!important}
/* Report configuration: dataset shelf above the document, no second left navigation. */
.workspace-shell .page-wrap .rc-layout{display:flex;flex-direction:column;border:0!important;box-shadow:var(--shadow-sm)}
.workspace-shell .page-wrap .rc-sidebar{width:100%;flex:none;border-right:0!important;border-bottom:1px solid #e2e8f0;background:#f8fafc;padding:14px 20px;display:flex;align-items:center;gap:18px;overflow:auto}
.workspace-shell .page-wrap .rc-sidebar-title{white-space:nowrap;padding:0}.workspace-shell .page-wrap .rc-search{width:200px;min-width:160px;padding:0}
.workspace-shell .page-wrap .rc-sidebar-scroll{display:flex;gap:8px;overflow:auto;padding:0}
.workspace-shell .page-wrap .rc-ds-item{min-width:200px;max-width:260px;margin:0;padding:12px;border:1px solid transparent;border-radius:8px}
.workspace-shell .page-wrap .rc-ds-item.is-active{background:#fff;border-color:#bfdbfe;box-shadow:var(--shadow-xs)}
.workspace-shell .page-wrap .rc-main{width:100%;min-width:0;flex:1}.workspace-shell .page-wrap .rc-main-header{padding:20px 24px}
@media(max-width:1000px){.workspace-shell .page-wrap .org-page .workspace{grid-template-columns:180px minmax(0,1fr)}.workspace-shell .page-wrap .migration-page .workbench{grid-template-columns:1fr}.workspace-shell .page-wrap .rc-sidebar{flex-wrap:wrap}.workspace-shell .page-wrap .rc-sidebar-scroll{width:100%}}
@media(max-width:720px){.workspace-shell .page-wrap .agent-workbench,.workspace-shell .page-wrap .org-page .workspace{grid-template-columns:1fr}.workspace-shell .page-wrap .permission-page .toolbar{grid-template-columns:1fr}.instruction-toolbar>div{margin-left:0}.workspace-shell .page-wrap .org-page .detail-panel{padding:14px}.workspace-shell .page-wrap .instruction-section.editor-expanded{inset:6px;padding:14px}.account-list-caption{flex-wrap:wrap;gap:10px}}
@media(prefers-reduced-motion:reduce){.workspace-shell *{transition:none!important}}

.workspace-shell .page-wrap .rc-sidebar{flex-direction:row;min-width:0;width:100%;box-sizing:border-box;background:#f8fafc!important}
.workspace-shell .page-wrap .rc-sidebar-scroll{flex:1;min-width:0;max-height:none;overflow-x:auto;overflow-y:hidden}
.workspace-shell .page-wrap .rc-ds-item{flex-shrink:0}
.workspace-shell .page-wrap .org-page .stat-item{background:transparent!important;border:0!important;border-left:2px solid #dbeafe!important;padding:4px 18px!important}
.workspace-shell .workspace-nav :is(.topnav-user-avatar,.account-menu-avatar){background:#eff6ff!important;color:#1d4ed8!important;border-color:#dbeafe!important}
.workspace-shell .workspace-nav-link .el-icon{color:inherit}
.workspace-shell .page-wrap .console-page .el-button--warning.is-plain{background:white!important;border-color:#dbe3ed!important;color:#475569!important}
.workspace-shell .page-wrap .migration-page .upload-zone p{color:#475569}
.workspace-shell .page-wrap .rc-card{background:#fff;border-color:#edf2f7;box-shadow:none}
.workspace-shell .page-wrap .rc-ds-badge{color:#047857;background:#ecfdf5}
/* Work surfaces, not a collection of dashboard cards. */
.editorial-shell{--studio-bg:#f4f5f7;--studio-ink:#17212f;--studio-action:#202c3d;--brand-primary:#202c3d;--brand-primary-hover:#101b2a;--brand-primary-active:#101b2a;--studio-soft:#eaf0fa}
.editorial-shell .workspace-nav{background:#eef0f4;backdrop-filter:none;border-right:0;padding-top:8px}
.editorial-shell .workspace-brand-row{padding-top:15px;padding-bottom:20px}
.editorial-shell .studio-brandmark{background:#202c3d!important;border-radius:8px!important}
.editorial-shell .workspace-search{background:#ffffff80;border:0;box-shadow:0 1px 2px #17212f09;border-radius:8px}
.editorial-shell .workspace-nav-group{margin-bottom:22px}
.editorial-shell .workspace-nav-group h2{font-size:10px;letter-spacing:.07em;color:#64748b;margin-bottom:6px}
.editorial-shell .workspace-nav-link{min-height:36px;border-radius:6px;font-size:12px}
.editorial-shell .workspace-nav-link[aria-current=page]{background:#fff;color:#17212f;box-shadow:0 1px 4px #17212f0a}
.editorial-shell .workspace-nav-link[aria-current=page]:before{background:#2563eb;left:0;height:16px;width:2px}
.editorial-shell .workspace-nav .topnav-user-chip{background:transparent!important;border:0!important;box-shadow:none;border-radius:8px!important}
.editorial-shell .workspace-nav .topnav-user-avatar{background:#dce3ed!important;color:#28364b!important;border:0!important}
.editorial-shell .workspace-bar{height:52px;min-height:52px;background:#fff;border-bottom:1px solid #e8ebf0}
.editorial-shell .page-wrap{background:#fff;padding:28px 32px}
.editorial-shell .page-wrap :is(.expert-page-head,.org-hero,.permission-page>.page-head,.report-settings-heading,.console-hero,.migration-page>.hero-card,.admin-page-head,.cs-page-heading,.dataset-page-heading,.fs-hero){padding:0 0 24px!important;border-bottom:1px solid #e8ebf0!important;margin-bottom:24px!important}
.editorial-shell .page-wrap :is(.expert-page-head,.org-hero,.permission-page>.page-head,.report-settings-heading,.console-hero,.migration-page>.hero-card,.admin-page-head,.cs-page-heading,.dataset-page-heading,.fs-hero) :is(h1,h2){font-size:27px;font-weight:600;letter-spacing:-.8px}
.editorial-shell .page-wrap :is(.page-overline,.hero-kicker,.kicker,.admin-kicker,.report-settings-heading>div>span){font-size:10px!important;letter-spacing:.1em!important}
/* Expert workspace: roles above, document and guidance side-by-side. */
.editorial-shell .page-wrap .document-workbench{display:flex;flex-direction:column;border:0!important;box-shadow:none!important;border-radius:0;overflow:visible}
.editorial-shell .page-wrap .document-workbench .agent-rail{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;padding:0 0 24px;background:transparent!important;border:0!important}
.editorial-shell .page-wrap .document-workbench .agent-rail-head{grid-column:1/-1;padding:0 0 4px;font-size:11px}
.editorial-shell .page-wrap .document-workbench .role-rail-note{grid-column:1/-1;border:0;margin:0;padding:0;display:flex;gap:20px;align-items:center}
.editorial-shell .page-wrap .document-workbench .role-rail-note>p{margin:0;font-size:11px}.editorial-shell .page-wrap .document-workbench .role-rail-note br{display:none}.editorial-shell .page-wrap .document-workbench .rail-note-label{display:none}
.editorial-shell .page-wrap .document-workbench .agent-card{margin:0;padding:16px 12px;border:1px solid #e8ebf0;border-radius:8px;background:#fff;align-items:flex-start;min-height:94px;transition:border-color 150ms}
.editorial-shell .page-wrap .document-workbench .agent-card.active{transform:none;background:#f2f5fb!important;border:1px solid #aebfd8!important;box-shadow:none!important}
.editorial-shell .page-wrap .document-workbench .agent-card-no{border:0;background:transparent;color:#64748b;font:11px/1.8 ui-monospace,monospace;width:auto}
.editorial-shell .page-wrap .document-workbench .agent-card-copy strong{font-size:13px}.editorial-shell .page-wrap .document-workbench .role-selected-dot{margin-top:6px}
.editorial-shell .page-wrap .document-workbench .agent-editor{border-top:1px solid #e2e8f0}
.editorial-shell .page-wrap .document-workbench .agent-editor-head{padding:24px 0 12px}.editorial-shell .page-wrap .document-workbench .role-execution-note{padding:0 0 20px}.editorial-shell .page-wrap .document-workbench .editor-overline{display:none}
.editorial-shell .page-wrap .document-workbench .editor-section-tabs{padding:0;gap:30px}
.editorial-shell .page-wrap .document-workbench .editor-content{display:grid;grid-template-columns:minmax(0,1fr) 230px;gap:32px;padding:24px 0}
.editorial-shell .page-wrap .document-workbench .instruction-section{grid-column:1;grid-row:1;min-width:0}.instruction-context{grid-column:2;grid-row:1;border-left:1px solid #e8ebf0;padding-left:24px}.instruction-context>span{font:10px ui-monospace,monospace;color:#64748b}.instruction-context h3{font-size:14px;margin:12px 0 24px}.instruction-context dl>div{margin:0 0 24px}.instruction-context dt{font-size:11px;color:#64748b}.instruction-context dd{font-size:12px;line-height:1.9;margin:7px 0 0;color:#334155}
.editorial-shell .page-wrap .document-workbench :is(.profile-section,.knowledge-section){grid-column:1/-1}
.editorial-shell .page-wrap .document-workbench .instruction-toolbar{background:#edf0f5;border-radius:8px 8px 0 0;gap:12px}
.editorial-shell .page-wrap .document-workbench .prompt-input textarea{background:#f8f9fc!important;min-height:350px;line-height:2!important}
.editorial-shell .page-wrap .document-workbench .instruction-section.editor-expanded{display:block;z-index:2100}
/* Console: section navigation remains visible beside the permission ledger. */
.editorial-shell .page-wrap .console-page{display:grid;grid-template-columns:170px minmax(0,1fr);column-gap:28px;align-items:start}
.editorial-shell .page-wrap .console-page>.console-hero{grid-column:1/-1}
.editorial-shell .page-wrap .console-page>.console-tabs{grid-column:1;position:sticky;top:0;display:flex;flex-direction:column;align-items:stretch;border:0;background:#f6f7f9;padding:8px;border-radius:8px;gap:3px}
.editorial-shell .page-wrap .console-page>.console-tabs button{text-align:left;padding:0 12px;font-size:12px;white-space:normal}
.editorial-shell .page-wrap .console-page>.console-tabs button.active{background:#fff;color:#17212f;box-shadow:0 1px 4px #17212f0a}
.editorial-shell .page-wrap .console-command-layout{grid-column:2;min-width:0;margin:0}
.editorial-shell .page-wrap .console-page .summary-strip{gap:0;border-radius:0;border-bottom:1px solid #e2e8f0;padding:0 0 22px;margin-bottom:24px}
.editorial-shell .page-wrap .console-page .summary-strip>div{background:transparent!important;box-shadow:none;border-right:1px solid #e8ebf0;border-radius:0;padding:4px 18px;display:flex;flex-direction:column;gap:4px}
.editorial-shell .page-wrap .console-page .summary-strip>div:first-child{padding-left:0}.editorial-shell .page-wrap .console-page .summary-strip>div:last-child{border:0}.editorial-shell .page-wrap .console-page .summary-strip strong{font-size:32px;font-weight:500}
.editorial-shell .page-wrap .console-page :is(.permission-card,.module-card){border:0;box-shadow:none;border-radius:0}.editorial-shell .page-wrap .console-page .card-head{padding:16px 0;background:transparent}.editorial-shell .page-wrap .console-page .matrix-table{padding:0;border:0}.editorial-shell .page-wrap .console-page .card-head h2{font-size:18px}.editorial-shell .page-wrap .console-page .matrix-head{border-radius:6px}
/* Tree is the primary canvas; metadata is a quiet inspector. */
.editorial-shell .page-wrap .org-page .stat-grid{display:flex;justify-content:flex-start;gap:30px;padding:0 0 20px;border-bottom:1px solid #e8ebf0;border-radius:0}
.editorial-shell .page-wrap .org-page .stat-item{display:flex;gap:10px;align-items:baseline;border:0!important;padding:0!important}.editorial-shell .page-wrap .org-page .stat-item strong{font:18px ui-monospace,monospace}
.editorial-shell .page-wrap .org-page .workspace{border:0;background:transparent;grid-template-columns:180px minmax(0,1fr)}
.editorial-shell .page-wrap .org-page .detail-panel{padding:0 0 0 24px;box-shadow:none;border-left:1px solid #e8ebf0;border-radius:0}
.editorial-shell .page-wrap .org-page .type-panel h2{font-size:12px}.editorial-shell .page-wrap .org-page .tree-layout{gap:20px;grid-template-columns:minmax(0,1fr) 260px}
.editorial-shell .page-wrap .org-page .tree-box{padding:16px 0}.editorial-shell .page-wrap .org-page .node-panel{border-radius:8px;background:#f6f7f9;min-height:340px}
/* Connections and model settings use edge-to-edge work surfaces. */
.editorial-shell .page-wrap :is(.db-workbench,.dataset-workspace,.cs-main,.fs-ops-board){box-shadow:none!important;border-radius:0!important;border:0!important}
.editorial-shell .page-wrap :is(.db-detail,.dataset-catalog,.cs-channel-list){background:#f6f7f9!important;border-radius:8px}
.editorial-shell .page-wrap .permission-page .toolbar{background:#f6f7f9;border-radius:8px;padding:12px 16px;margin-bottom:16px}
.editorial-shell .page-wrap .permission-page .user-table-card{padding:0;border-radius:0;box-shadow:none}
.editorial-shell .page-wrap .migration-page .workbench{border-top:1px solid #e8ebf0;padding-top:24px}
.editorial-shell .page-wrap .migration-page .panel-card{box-shadow:none!important;border-radius:0!important}.editorial-shell .page-wrap .migration-page .panel-card .el-card__header{padding:0 0 18px}.editorial-shell .page-wrap .migration-page .panel-card .el-card__body{padding:20px 0}.editorial-shell .page-wrap .migration-page .upload-zone{background:#f6f8fc;border:1px dashed #b4c1d2}
.editorial-shell .page-wrap-smart{padding:0;background:#fff}
.editorial-shell .ax-page,.editorial-shell .ax-workspace,.editorial-shell .ax-chat-panel,.editorial-shell .ax-chat-body,.editorial-shell .ax-composer-track{background:#fff!important}
.editorial-shell .ax-detail-panel-container{border-left:1px solid #e8ebf0;box-shadow:none}
.editorial-shell .ax-composer-track .cmp-dock{border:1px solid #d6deea;border-radius:16px;box-shadow:0 6px 28px #23304a09}
@media(max-width:1100px){.editorial-shell .page-wrap .document-workbench .editor-content{grid-template-columns:1fr}.instruction-context{grid-column:1;grid-row:2;display:block;border-left:0;border-top:1px solid #e8ebf0;padding:20px 0}.instruction-context dl{display:grid;grid-template-columns:1fr 1fr;gap:16px}.editorial-shell .page-wrap .org-page .tree-layout{grid-template-columns:1fr}.editorial-shell .page-wrap .document-workbench .agent-rail{grid-template-columns:1fr 1fr}}
@media(max-width:720px){.editorial-shell .page-wrap{padding:20px 16px}.editorial-shell .page-wrap-smart{padding:0}.editorial-shell .page-wrap .console-page{display:block}.editorial-shell .page-wrap .console-page>.console-tabs{position:static;flex-direction:row;flex-wrap:wrap;margin-bottom:20px}.editorial-shell .page-wrap .console-page .summary-strip strong{font-size:24px}.editorial-shell .page-wrap .org-page .workspace{grid-template-columns:1fr}.editorial-shell .page-wrap .org-page .detail-panel{padding:0;border:0}.editorial-shell .page-wrap .org-page .stat-grid{flex-wrap:wrap;gap:16px}.editorial-shell .page-wrap .document-workbench .role-rail-note{flex-wrap:wrap}.editorial-shell .page-wrap .document-workbench .agent-card{min-height:90px}.editorial-shell .page-wrap .document-workbench .editor-content{padding-top:20px}.instruction-context dl{grid-template-columns:1fr}}

.workspace-shell.editorial-shell .page-wrap{background:#fff!important}
.workspace-shell.editorial-shell .page-wrap .console-page :is(.permission-card,.module-card){border:0!important;border-radius:0!important;box-shadow:none!important}
.workspace-shell.editorial-shell .ax-page .ax-composer-track .cmp-dock:focus-within{border-color:#93b4ec!important;box-shadow:0 0 0 3px #2563eb0a,0 6px 28px #23304a09!important}
.workspace-shell.editorial-shell .ax-page .ax-composer-track .cmp-textarea::placeholder{color:#64748b}

```

---

## 外层框架与全局导航 (src/App.vue)

**文件路径**: `datapivot-demo/frontend/src/App.vue`

```vue
<template>
  <router-view v-if="isAuthCallbackRoute" />
  <div v-else-if="!authReady" class="auth-loading-screen">
    <div class="auth-loading-card">
      <div class="auth-loading-mark"></div>
      <strong>正在校验登录状态</strong>
      <span>请稍候...</span>
    </div>
  </div>
  <AuthLogin v-else-if="!authUser" @authenticated="handleAuthenticated" />
  <el-container v-else class="app-shell workspace-shell editorial-shell" :class="{ 'is-nav-collapsed': navCollapsed }">
    <button v-if="shellNavOpen" class="shell-nav-backdrop" type="button" aria-label="关闭导航" @click="shellNavOpen = false"></button>
    <aside class="workspace-nav" :class="{ 'is-open': shellNavOpen }" aria-label="工作空间导航">
      <div class="workspace-brand-row"><button class="topnav-brand" type="button" @click="router.push('/ask')">
        <span class="studio-brandmark" aria-label="DataPulse"><svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M5 16V10M12 19V5M19 15V9" stroke="currentColor" stroke-width="3" stroke-linecap="round"/></svg></span>
        <span class="topnav-brand-name">DataPulse</span>
        <span class="topnav-brand-env">脉策智能</span>
      </button><button class="nav-collapse-toggle" type="button" :aria-label="navCollapsed ? '展开侧栏' : '收起侧栏'" :title="navCollapsed ? '展开侧栏' : '收起侧栏'" @click="toggleNavCollapsed"><svg viewBox="0 0 20 20" fill="none" aria-hidden="true"><rect x="3" y="4" width="14" height="12" rx="2"/><path d="M8 4v12"/></svg></button></div>

      <button class="workspace-search" type="button" @click="openCommandPalette"><el-icon><Search /></el-icon><span>搜索功能</span><kbd>⌘ K</kbd></button>
      <nav class="workspace-nav-scroll" aria-label="系统模块">
        <section v-for="group in navigationGroups" :key="group.label" class="workspace-nav-group">
          <h2>{{ group.label }}</h2>
          <button v-for="item in group.items" :key="item.path" class="workspace-nav-link" type="button" :title="navCollapsed ? item.label : undefined" :aria-label="item.label" :aria-current="activeMenu === item.path ? 'page' : undefined" @click="handleMenuSelect(item.path)"><el-icon><component :is="item.icon" /></el-icon><span>{{ item.label }}</span></button>
        </section>
      </nav>
      <div class="topnav-actions">
        <div class="topnav-user">
          <button ref="accountTrigger" class="topnav-user-chip" type="button" aria-label="账号菜单" aria-haspopup="menu" :aria-expanded="userMenuVisible" aria-controls="workspace-account-menu" @click.stop="toggleUserMenu" @keydown.down.prevent="openAccountMenu">
            <span class="topnav-user-avatar">{{ authUserInitial }}</span>
            <span class="topnav-user-status" :class="{ 'is-online': backendOk }" aria-hidden="true"></span>
            <span class="topnav-user-meta">
              <span class="topnav-user-name">{{ authUserName }}</span>
              <span class="topnav-user-role">{{ authRoleLabel }}</span>
            </span>
            <svg class="account-menu-indicator" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true"><circle cx="4" cy="10" r="1.3"/><circle cx="10" cy="10" r="1.3"/><circle cx="16" cy="10" r="1.3"/></svg>
          </button>
          <transition name="user-menu-rise">
            <div v-if="userMenuVisible" id="workspace-account-menu" ref="accountMenu" class="topnav-user-dropdown" role="menu" aria-label="账号设置" @click.stop @keydown="handleAccountMenuKey">
              <div class="account-menu-identity"><span class="account-menu-avatar">{{ authUserInitial }}</span><div><strong>{{ authUserName }}</strong><span>{{ authRoleLabel }}</span></div></div>
              <button v-if="authRole === 'super_admin' && appFeatureAccess.admin_console" type="button" role="menuitem" @click="openAdminConsole"><el-icon><Setting /></el-icon><span>系统控制台</span><kbd>管理</kbd></button>
              <button v-if="appFeatureAccess.app_password_change" type="button" role="menuitem" @click="openPasswordDialog"><el-icon><Lock /></el-icon><span>修改密码</span></button>
              <div class="account-menu-separator"></div>
              <button class="danger" type="button" role="menuitem" @click="handleLogout"><svg viewBox="0 0 20 20" fill="none" aria-hidden="true"><path d="M8 3H4v14h4M8 10h9m-3-3 3 3-3 3" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/></svg><span>退出登录</span></button>
            </div>
          </transition>
        </div>
      </div>
    </aside>

    <el-container class="app-body">
      <header class="workspace-bar"><div><button class="shell-menu-toggle" type="button" aria-label="展开导航" @click="shellNavOpen = !shellNavOpen"><el-icon><Expand /></el-icon></button><span class="workspace-location">{{ currentGroupLabel }}</span><span class="workspace-separator">/</span><strong>{{ currentTitle }}</strong></div><span class="workspace-connection"><i :class="{ online: backendOk }"></i>{{ backendOk ? '服务已连接' : '服务连接异常' }}</span></header>
      <button v-if="showBackToConsole" class="workspace-back" type="button" @click="backToConsole">← 返回控制台</button>

      <el-main class="page-wrap" :class="{ 'page-wrap-smart': isDataPulseRoute }">
        <router-view v-slot="{ Component }">
          <keep-alive :include="cachedPageNames">
            <component :is="Component" />
          </keep-alive>
        </router-view>
      </el-main>
    </el-container>

    <el-drawer
      v-model="historyDrawerVisible"
      title="全部任务"
      size="420px"
      custom-class="history-drawer"
    >
      <div class="history-drawer-head">
        <div>
          <div class="history-drawer-title">{{ historySessions.length }} 个任务</div>
          <div class="history-drawer-desc">选择任意任务可恢复到分析工作台。</div>
        </div>
        <button
          v-if="historySessions.length && appFeatureAccess.app_history_clear"
          class="history-drawer-clear"
          type="button"
          :disabled="isClearingHistory"
          @click="clearHistoryList"
        >
          {{ isClearingHistory ? '清空中...' : '清空全部' }}
        </button>
      </div>
      <div v-if="historySessions.length || currentRunningTask" class="history-drawer-list">
        <!-- 抽屉里的虚拟"当前执行任务"行 -->
        <article
          v-if="currentRunningTask"
          class="history-item history-drawer-item history-item-running"
          :key="currentRunningTask.id"
          :aria-label="'当前任务：' + currentRunningTask.title"
          @click="handleRunningTaskClick; historyDrawerVisible = false"
        >
          <div class="history-drawer-index">{{ currentRunningTask.status === 'pending_confirmation' ? '待确认' : '执行' }}</div>
          <div class="history-item-main">
            <div class="history-item-top">
              <div class="history-item-title">{{ currentRunningTask.title }}</div>
              <div class="history-item-status">
                <TaskStatusIndicator
                  :variant="currentRunningTask.status"
                  :show-text-label="true"
                />
              </div>
            </div>
            <div class="history-drawer-meta-row">
              <span class="history-drawer-dataset">{{ currentRunningTask.datasetName }}</span>
              <span class="history-drawer-time">刚刚发起</span>
            </div>
          </div>
        </article>

        <article
          v-for="(item, index) in historySessions"
          :key="item.id"
          class="history-item history-drawer-item"
          :class="{ 'history-item-active': item.id === activeHistoryId }"
          @click="openHistorySession(item); historyDrawerVisible = false"
        >
          <div class="history-drawer-index">{{ String(index + 1).padStart(2, '0') }}</div>
          <div class="history-item-main">
            <div class="history-item-top">
              <div class="history-item-title">{{ item.title }}</div>
              <div class="history-item-status">
                <TaskStatusIndicator
                  :variant="inferTaskVariant(item)"
                  :show-text-label="true"
                />
                <span v-if="item.id === activeHistoryId" class="history-item-badge">当前</span>
              </div>
            </div>
            <div class="history-drawer-meta-row">
              <span class="history-drawer-dataset">{{ item.datasetName || '自动路由数据集' }}</span>
              <span class="history-drawer-time">{{ item.updatedAt }}</span>
            </div>
          </div>
          <button
            v-if="appFeatureAccess.app_history_delete"
            class="history-item-delete"
            type="button"
            aria-label="删除任务"
            @click.stop="removeHistoryItem(item.id)"
          >
            <span class="history-item-delete-icon" aria-hidden="true"></span>
          </button>
        </article>
      </div>
      <div v-else class="history-empty history-drawer-empty">
        <div class="history-empty-title">暂无任务</div>
        <div class="history-empty-desc">发起分析后，这里会显示你的任务记录。</div>
      </div>
    </el-drawer>

    <el-dialog
      v-model="passwordDialogVisible"
      title="修改密码"
      width="420px"
      custom-class="password-dialog"
      :close-on-click-modal="false"
    >
      <div class="password-panel">
        <span class="password-panel-icon">锁</span>
        <div>
          <h3>更新登录密码</h3>
          <p>建议使用至少 8 位，并包含数字和字母的密码。</p>
        </div>
      </div>
      <div class="password-form">
        <label>
          <span>原密码</span>
          <div class="dialog-password-control">
            <input
              v-model="passwordForm.old_password"
              :type="passwordVisible.old ? 'text' : 'password'"
              autocomplete="current-password"
              placeholder="请输入当前密码"
              @keydown.enter="submitPasswordChange"
            />
            <button
              class="dialog-password-eye"
              type="button"
              :aria-label="passwordVisible.old ? '隐藏原密码' : '显示原密码'"
              @click="passwordVisible.old = !passwordVisible.old"
            >
              <el-icon><component :is="passwordVisible.old ? Hide : View" /></el-icon>
            </button>
          </div>
        </label>
        <label>
          <span>新密码</span>
          <div class="dialog-password-control">
            <input
              v-model="passwordForm.new_password"
              :type="passwordVisible.next ? 'text' : 'password'"
              autocomplete="new-password"
              placeholder="至少 8 位"
              @keydown.enter="submitPasswordChange"
            />
            <button
              class="dialog-password-eye"
              type="button"
              :aria-label="passwordVisible.next ? '隐藏新密码' : '显示新密码'"
              @click="passwordVisible.next = !passwordVisible.next"
            >
              <el-icon><component :is="passwordVisible.next ? Hide : View" /></el-icon>
            </button>
          </div>
        </label>
        <label>
          <span>确认新密码</span>
          <div class="dialog-password-control">
            <input
              v-model="passwordForm.confirm_password"
              :type="passwordVisible.confirm ? 'text' : 'password'"
              autocomplete="new-password"
              @keydown.enter="submitPasswordChange"
            />
            <button
              class="dialog-password-eye"
              type="button"
              :aria-label="passwordVisible.confirm ? '隐藏确认密码' : '显示确认密码'"
              @click="passwordVisible.confirm = !passwordVisible.confirm"
            >
              <el-icon><component :is="passwordVisible.confirm ? Hide : View" /></el-icon>
            </button>
          </div>
        </label>
      </div>
      <template #footer>
        <button class="dialog-ghost-button" type="button" @click="passwordDialogVisible = false">取消</button>
        <button class="dialog-primary-button" type="button" :disabled="passwordSaving" @click="submitPasswordChange">
          {{ passwordSaving ? '保存中...' : '确认修改' }}
        </button>
      </template>
    </el-dialog>

    <div
      v-if="showAdminConsoleFloat"
      class="admin-console-float"
      :style="adminConsoleFloatStyle"
      @pointerdown="startAdminConsoleFloatDrag"
    >
      <button
        class="admin-console-float-main"
        :class="{ dragging: adminConsoleFloatDragging }"
        type="button"
        @click.stop="handleAdminConsoleFloatOpen"
      >
        <el-icon><Setting /></el-icon>
        <span>控制台</span>
      </button>
      <button
        class="admin-console-float-close"
        type="button"
        aria-label="关闭控制台悬浮入口"
        @pointerdown.stop
        @click.stop="dismissAdminConsoleFloat"
      >
        x
      </button>
    </div>
    <SqlDebugFloat />
  </el-container>

  <!-- 全局命令面板（⌘K / Ctrl+K） -->
  <transition name="palette-fade">
    <div v-if="commandPaletteVisible" class="command-palette-mask" @click.self="closeCommandPalette">
      <div class="command-palette" role="dialog" aria-label="命令面板">
        <div class="command-palette-search">
          <span class="command-palette-search-icon" aria-hidden="true"></span>
          <input
            ref="commandInputRef"
            v-model="commandQuery"
            class="command-palette-input"
            type="text"
            placeholder="输入模块名称或关键词…"
            autocomplete="off"
            @keydown.esc="closeCommandPalette"
            @keydown.enter.prevent="runActiveCommand"
            @keydown.up.prevent="moveCommandCursor(-1)"
            @keydown.down.prevent="moveCommandCursor(1)"
          />
          <span class="command-palette-hint">ESC 关闭</span>
        </div>
        <div class="command-palette-list">
          <button
            v-for="(cmd, idx) in filteredCommands"
            :key="cmd.path"
            class="command-palette-item"
            :class="{ 'is-active': idx === commandCursor }"
            type="button"
            @mouseenter="commandCursor = idx"
            @click="runCommand(cmd)"
          >
            <el-icon class="command-palette-item-icon"><component :is="cmd.icon" /></el-icon>
            <span class="command-palette-item-body">
              <span class="command-palette-item-label">{{ cmd.label }}</span>
              <span class="command-palette-item-path">{{ cmd.path }}</span>
            </span>
          </button>
          <div v-if="!filteredCommands.length" class="command-palette-empty">没有匹配的模块</div>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup>
import { computed, nextTick, onMounted, onUnmounted, ref, watch } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useRoute, useRouter } from 'vue-router'
import { ChatLineRound, Coin, Collection, Connection, Cpu, Document, Hide, Lock, MagicStick, Monitor, Operation, Setting, Share, UploadFilled, View, Search, Expand } from '@element-plus/icons-vue'
import AuthLogin from './auth/AuthLogin.vue'
import SqlDebugFloat from './components/SqlDebugFloat.vue'
import TaskStatusIndicator from './components/TaskStatusIndicator.vue'
import { preloadRouteComponents } from './router'
import { changePassword, clearAuthToken, getCurrentUser, healthCheck, logout } from './api/index.js'
import { useDataPulseSession } from './state/askDeskSession.js'
import { useDataPulseHistory } from './state/askDeskHistory.js'
import { useDataPulseTaskView } from './state/askDeskTaskView.js'
import { useFeatureFlags } from './state/featureFlags.js'

const route = useRoute()
const router = useRouter()
const session = useDataPulseSession()
const {
  historySessions,
  activeHistoryId,
  buildHistoryScope,
  setHistoryScope,
  loadHistory,
  syncHistory,
  removeHistory,
  clearHistory,
  requestRestore,
  setActiveHistory,
} = useDataPulseHistory()
const {
  runningSessionId,
  runningTaskStatus,
  completedTaskId,
  viewingTaskId,
  isViewingReadonly,
  setRunningSessionId,
  setViewingTask,
  switchViewToDefault,
  clearRunningSessionId,
  switchViewToRunning,
} = useDataPulseTaskView()
const {
  features: featureFlags,
  ready: featureFlagsReady,
  loadFeatureFlags,
  clearFeatureFlags,
} = useFeatureFlags()
const appFeatureKeys = [
  'app_history_clear',
  'app_history_delete',
  'admin_console',
  'app_password_change',
]
const appFeatureAccess = computed(() => appFeatureKeys.reduce((map, key) => {
  map[key] = isFeatureEnabled(key)
  return map
}, {}))
const backendOk = ref(false)
const authUser = ref(null)
const authReady = ref(false)
const passwordDialogVisible = ref(false)
const passwordSaving = ref(false)
const passwordForm = ref({
  old_password: '',
  new_password: '',
  confirm_password: ''
})
const passwordVisible = ref({
  old: false,
  next: false,
  confirm: false,
})
const shellNavOpen = ref(false)
const currentTime = ref('')
const historyDrawerVisible = ref(false)
const isClearingHistory = ref(false)
const userMenuVisible = ref(false)
const accountMenu = ref(null), accountTrigger = ref(null)
const navCollapsed = ref(localStorage.getItem('datapulse_nav_collapsed') === '1')
const toggleNavCollapsed = () => {
  navCollapsed.value = !navCollapsed.value
  localStorage.setItem('datapulse_nav_collapsed',navCollapsed.value ? '1' : '0')
  closeUserMenu()
}
const openAccountMenu = async () => {
  userMenuVisible.value = true
  await nextTick()
  accountMenu.value?.querySelector('[role=menuitem]')?.focus()
}
const handleAccountMenuKey = event => {
  const items = [...(accountMenu.value?.querySelectorAll('[role=menuitem]') || [])]
  const index = items.indexOf(document.activeElement)
  if (['ArrowDown','ArrowUp','Home','End'].includes(event.key)) {
    event.preventDefault()
    const next=event.key==='Home'?0:event.key==='End'?items.length-1:(index+(event.key==='ArrowDown'?1:-1)+items.length)%items.length
    items[next]?.focus()
  } else if(event.key==='Escape') { event.preventDefault();closeUserMenu();accountTrigger.value?.focus() }
  else if(event.key==='Tab')closeUserMenu()
}

/* ── 全局命令面板（⌘K / Ctrl+K）── */
const commandPaletteVisible = ref(false)
const commandQuery = ref('')
const commandCursor = ref(0)
const commandInputRef = ref(null)

const roleRank = {
  super_admin: 4,
  admin: 3,
  business_admin: 2,
  user: 1
}

// 全部为顶部一级菜单（含模型服务及原「系统管理」各子项）；按角色+功能位过滤可见性，
// 横向空间不足时 Element Plus 自动收进「...」溢出菜单
const menuItems = [
  { path: '/ask', label: '问数助手', icon: ChatLineRound, minRole: 'user', featureKey: 'ask_ask_workspace' },
  { path: '/sql-debug', label: '查询控制台', icon: Monitor, minRole: 'user', featureKey: 'dataset_sql_preview_run' },
  { path: '/agents', label: '专家协作', icon: Cpu, minRole: 'admin', featureKey: 'agent_management' },
  { path: '/datasets', label: '数据集管理', icon: Collection, minRole: 'admin', featureKey: 'dataset_management' },
  { path: '/databases', label: '数据源管理', icon: Coin, minRole: 'admin', featureKey: 'database_management' },
  { path: '/ai-models', label: '模型服务', icon: MagicStick, minRole: 'admin', featureKey: 'ai_model_config' },
  { path: '/report-config', label: '报告模板', icon: Document, minRole: 'admin', featureKey: 'report_config' },
  { path: '/advanced-capabilities', label: '技能与工具', icon: Operation, minRole: 'admin', featureKey: 'advanced_capabilities' },
  { path: '/feishu-sync', label: '飞书同步', icon: Connection, minRole: 'admin', featureKey: 'feishu_sync' },
  { path: '/runtime-migration', label: '迁移发布', icon: UploadFilled, minRole: 'super_admin', featureKey: 'runtime_migration' },
  { path: '/organization-trees', label: '组织树', icon: Share, minRole: 'super_admin', featureKey: 'organization_tree_management' },
  { path: '/employee-permissions', label: '账号与权限', icon: Lock, minRole: 'super_admin', featureKey: 'employee_permissions' },
  { path: '/admin-console', label: '系统控制台', icon: Setting, minRole: 'super_admin', featureKey: 'admin_console' }
]

const routeComponentNamesByPath = {
  '/ask': 'DataPulse',
  '/sql-debug': 'SqlDebug',
  '/agents': 'AgentManagement',
  '/datasets': 'DatasetManagement',
  '/bookshelves': 'Bookshelves',
  '/databases': 'Databases',
  '/ai-models': 'AIModels',
  '/report-config': 'DatasetReportConfig',
  '/advanced-capabilities': 'AdvancedCapabilities',
  '/feishu-sync': 'FeishuSync',
  '/runtime-migration': 'RuntimeMigration',
  '/organization-trees': 'OrganizationTrees',
  '/employee-permissions': 'EmployeePermissions',
  '/admin-console': 'AdminConsole',
}

const subtitleMap = {
  '/ask': '',
  '/sql-debug': '快速生成、执行与核对问数 SQL',
  '/agents': '配置主理人与领域专家的职责、提示词和协作约束',
  '/datasets': '治理数据集元数据、书架与Golden SQL',
  '/databases': '管理 PostgreSQL 与其他业务数据连接',
  '/ai-models': '配置默认模型、通道与调用参数',
  '/report-config': '维护数据集对应的报告模板与展示规范',
  '/advanced-capabilities': '管理两条问数路径的技能、执行边界与外部工具',
  '/feishu-sync': '管理飞书多维表格同步、日志与任务控制',
  '/runtime-migration': '导出导入运行态配置，发布前自动备份可回滚',
  '/organization-trees': '维护多套独立组织树类型与树形节点',
  '/employee-permissions': '维护员工身份映射、角色与可访问范围'
}

const activeMenu = computed(() => route.path)
const isAuthCallbackRoute = computed(() => route.path === '/auth/callback')
const isDataPulseRoute = computed(() => route.path === '/ask')
const showBackToConsole = computed(() => route.query?.from === 'admin-console' && route.path !== '/admin-console')
const authRole = computed(() => authUser.value?.role || 'user')
const authRoleLabel = computed(() => ({ super_admin: '超级管理员', admin: '管理员', business_admin: '业务管理员', user: '普通用户' }[authRole.value] || '普通用户'))
const canAccessRole = (minRole) => (roleRank[authRole.value] || 0) >= (roleRank[minRole] || 0)
const isFeatureEnabled = (key) => {
  if (!key) return true
  const feature = featureFlags.value?.[key]
  if (!featureFlagsReady.value || !feature) return true
  if (typeof feature.available === 'boolean') return feature.available
  return Boolean(feature.enabled)
}
const hasLoadedFeatureDecision = (key) => Boolean(key && featureFlagsReady.value && featureFlags.value?.[key])
const canAccessMenuItem = (item) => {
  if (!item) return true
  // 角色是硬门槛：普通用户无论功能开关如何，都看不到 minRole 更高的管理入口
  // （功能开关只做"同角色内的灰度/回收"，不能反向为低角色越权开放）
  if (!canAccessRole(item.minRole)) return false
  if (hasLoadedFeatureDecision(item.featureKey)) {
    return isFeatureEnabled(item.featureKey)
  }
  return true
}
const availableMenuItems = computed(() => menuItems.filter((item) => !item.hidden && canAccessMenuItem(item)))
const navigationGroups = computed(() => [
  {label:'分析工作区',paths:['/ask','/sql-debug']},
  {label:'数据资产',paths:['/datasets','/databases','/feishu-sync']},
  {label:'问数编排',paths:['/agents','/advanced-capabilities','/ai-models','/report-config']},
  {label:'组织治理',paths:['/organization-trees','/employee-permissions']},
  {label:'系统运维',paths:['/admin-console','/runtime-migration']},
].map(group=>({...group,items:group.paths.map(path=>availableMenuItems.value.find(item=>item.path===path)).filter(Boolean)})).filter(group=>group.items.length))
const currentGroupLabel = computed(()=>navigationGroups.value.find(group=>group.items.some(item=>item.path===route.path))?.label || '工作空间')

/* 命令面板：按关键词过滤当前账号可访问的模块 */
const filteredCommands = computed(() => {
  const q = commandQuery.value.trim().toLowerCase()
  const list = availableMenuItems.value || []
  if (!q) return list
  return list.filter((item) => (
    String(item.label || '').toLowerCase().includes(q)
    || String(item.path || '').toLowerCase().includes(q)
  ))
})

const cachedPageNames = computed(() => (
  Array.from(new Set(availableMenuItems.value.map((item) => routeComponentNamesByPath[item.path]).filter(Boolean)))
))
const currentTitle = computed(() => menuItems.find((item) => item.path === route.path)?.label || '问数助手')
const currentSubtitle = computed(() => subtitleMap[route.path] || '自然语言自助问数')
const activeDatasetIds = computed(() => session.activeDatasetIds.value || [])
// 虚拟"当前执行/待确认任务"：session 在跑或待确认时显示在历史列表顶部，不持久化
const currentRunningTask = computed(() => {
  const status = session.state?.status
  if (status !== 'running' && status !== 'waiting_confirmation') return null
  const question = String(session.state?.question || '').trim()
  if (!question) return null
  return {
    id: '__current_running__',
    title: question.slice(0, 24),
    datasetName: status === 'waiting_confirmation' ? '待确认' : '正在分析中',
    status: status === 'waiting_confirmation' ? 'pending_confirmation' : 'running',
    isVirtual: true,
  }
})
const cleanDisplayName = (value) => {
  const text = String(value || '').trim()
  if (!text || /^[?\s]+$/.test(text)) return ''
  return text.replace(/^\?+\s*/, '')
}
const authUserName = computed(() => (
  cleanDisplayName(authUser.value?.name)
  || cleanDisplayName(authUser.value?.permission_name)
  || cleanDisplayName(authUser.value?.username)
  || cleanDisplayName(authUser.value?.zh_name)
  || cleanDisplayName(authUser.value?.union_id)
  || '已登录'
))
const authUserInitial = computed(() => String(authUserName.value || '登').slice(0, 1).toUpperCase())

const refreshClock = () => {
  currentTime.value = new Date().toLocaleString('zh-CN', { hour12: false })
}

const pingBackend = async () => {
  try {
    await healthCheck()
    backendOk.value = true
  } catch {
    backendOk.value = false
  }
}

const refreshAuthUser = async () => {
  try {
    const data = await getCurrentUser()
    authUser.value = data?.authenticated ? (data.user || {}) : null
    syncHistoryScope()
    if (authUser.value) {
      loadFeatureFlags(true)
        .then(() => enforceRouteAccess())
        .catch(() => {})
      syncHistory().catch(() => {})
      scheduleRoutePreload()
    } else clearFeatureFlags()
  } catch {
    authUser.value = null
    clearFeatureFlags()
    syncHistoryScope()
  } finally {
    authReady.value = true
  }
}

const syncHistoryScope = () => {
  if (!authUser.value) {
    setHistoryScope('anonymous')
    return
  }
  setHistoryScope(buildHistoryScope(authUser.value))
}

const handleAuthenticated = async (user) => {
  authUser.value = user || null
  syncHistoryScope()
  if (authUser.value) {
    loadFeatureFlags(true)
      .then(() => enforceRouteAccess())
      .catch(() => {})
    syncHistory().catch(() => {})
    scheduleRoutePreload()
  } else clearFeatureFlags()
  authReady.value = true
  enforceRouteAccess()
}

const submitPasswordChange = async () => {
  if (passwordSaving.value) return
  if (authRole.value === 'super_admin') {
    ElMessage.warning('超级管理员密码由 .env 管理，请修改 DATAPULSE_ADMIN_PASSWORD')
    return
  }
  if (!passwordForm.value.old_password || !passwordForm.value.new_password) {
    ElMessage.warning('请填写原密码和新密码')
    return
  }
  if (passwordForm.value.new_password !== passwordForm.value.confirm_password) {
    ElMessage.warning('两次输入的新密码不一致')
    return
  }
  if (passwordForm.value.new_password.length < 8) {
    ElMessage.warning('新密码至少需要 8 位')
    return
  }
  passwordSaving.value = true
  try {
    await changePassword({
      old_password: passwordForm.value.old_password,
      new_password: passwordForm.value.new_password
    })
    passwordDialogVisible.value = false
    passwordForm.value = { old_password: '', new_password: '', confirm_password: '' }
    passwordVisible.value = { old: false, next: false, confirm: false }
    ElMessage({
      message: '密码已修改，请重新登录',
      type: 'success',
      duration: 2200,
      customClass: 'app-toast-modern',
    })
    clearAuthToken()
    authUser.value = null
    clearFeatureFlags()
    syncHistoryScope()
  } finally {
    passwordSaving.value = false
  }
}

const toggleUserMenu = () => {
  userMenuVisible.value = !userMenuVisible.value
}

const closeUserMenu = () => {
  userMenuVisible.value = false
}

/* ── 命令面板行为 ── */
const openCommandPalette = () => {
  commandPaletteVisible.value = true
  commandQuery.value = ''
  commandCursor.value = 0
  userMenuVisible.value = false
  nextTick(() => {
    commandInputRef.value?.focus()
  })
}

const closeCommandPalette = () => {
  commandPaletteVisible.value = false
  commandQuery.value = ''
  commandCursor.value = 0
}

const moveCommandCursor = (delta) => {
  const total = filteredCommands.value.length
  if (!total) return
  commandCursor.value = (commandCursor.value + delta + total) % total
}

const runCommand = (cmd) => {
  if (!cmd) return
  closeCommandPalette()
  if (route.path !== cmd.path) router.push(cmd.path)
}

const runActiveCommand = () => {
  runCommand(filteredCommands.value[commandCursor.value])
}

const handleCommandHotkey = (event) => {
  if(event.key==='Escape' && userMenuVisible.value){closeUserMenu();accountTrigger.value?.focus()}
  if ((event.metaKey || event.ctrlKey) && String(event.key).toLowerCase() === 'k') {
    event.preventDefault()
    if (commandPaletteVisible.value) closeCommandPalette()
    else openCommandPalette()
  }
}

const openPasswordDialog = () => {
  closeUserMenu()
  passwordDialogVisible.value = true
}

const ADMIN_CONSOLE_LAST_ROUTE_KEY = 'datapulse_admin_console_last_route'

const getAdminConsoleTarget = () => {
  const fallback = '/admin-console'
  const saved = localStorage.getItem(ADMIN_CONSOLE_LAST_ROUTE_KEY) || sessionStorage.getItem(ADMIN_CONSOLE_LAST_ROUTE_KEY) || ''
  return saved.startsWith('/admin-console') ? saved : fallback
}

const openAdminConsole = () => {
  closeUserMenu()
  router.push(getAdminConsoleTarget())
}

const backToConsole = () => {
  router.push(getAdminConsoleTarget())
}

const ADMIN_CONSOLE_FLOAT_POSITION_KEY = 'datapulse_admin_console_float_position'
const ADMIN_CONSOLE_FLOAT_HIDDEN_KEY = 'datapulse_admin_console_float_hidden'
const ADMIN_CONSOLE_FLOAT_TOGGLE_EVENT = 'datapulse-admin-console-float-toggle'
const adminConsoleFloatVisible = ref(false)
const adminConsoleFloatDragging = ref(false)
const adminConsoleFloatPosition = ref({ x: 0, y: 0 })
let adminConsoleFloatMoved = false
let adminConsoleFloatOffset = { x: 0, y: 0 }

const getDefaultAdminConsoleFloatPosition = () => ({
  x: Math.max(16, window.innerWidth - 164),
  y: Math.max(88, window.innerHeight - 118),
})

const clampAdminConsoleFloatPosition = (position) => {
  const width = 154
  const height = 56
  return {
    x: Math.min(Math.max(12, Number(position?.x) || 0), Math.max(12, window.innerWidth - width)),
    y: Math.min(Math.max(76, Number(position?.y) || 0), Math.max(76, window.innerHeight - height)),
  }
}

const persistAdminConsoleFloatState = () => {
  sessionStorage.setItem(ADMIN_CONSOLE_FLOAT_POSITION_KEY, JSON.stringify(adminConsoleFloatPosition.value))
  sessionStorage.setItem(ADMIN_CONSOLE_FLOAT_HIDDEN_KEY, adminConsoleFloatVisible.value ? '0' : '1')
}

const restoreAdminConsoleFloatState = () => {
  const hidden = sessionStorage.getItem(ADMIN_CONSOLE_FLOAT_HIDDEN_KEY) !== '0'
  adminConsoleFloatVisible.value = !hidden
  try {
    const saved = JSON.parse(sessionStorage.getItem(ADMIN_CONSOLE_FLOAT_POSITION_KEY) || 'null')
    adminConsoleFloatPosition.value = clampAdminConsoleFloatPosition(saved || getDefaultAdminConsoleFloatPosition())
  } catch {
    adminConsoleFloatPosition.value = getDefaultAdminConsoleFloatPosition()
  }
}

const adminConsoleFloatStyle = computed(() => ({
  left: `${adminConsoleFloatPosition.value.x}px`,
  top: `${adminConsoleFloatPosition.value.y}px`,
}))

const showAdminConsoleFloat = computed(() => (
  authRole.value === 'super_admin'
  && appFeatureAccess.value.admin_console
  && adminConsoleFloatVisible.value
))

const stopAdminConsoleFloatDrag = () => {
  if (!adminConsoleFloatDragging.value) return
  adminConsoleFloatDragging.value = false
  persistAdminConsoleFloatState()
  window.removeEventListener('pointermove', handleAdminConsoleFloatDrag)
  window.removeEventListener('pointerup', stopAdminConsoleFloatDrag)
}

const handleAdminConsoleFloatDrag = (event) => {
  if (!adminConsoleFloatDragging.value) return
  adminConsoleFloatPosition.value = clampAdminConsoleFloatPosition({
    x: event.clientX - adminConsoleFloatOffset.x,
    y: event.clientY - adminConsoleFloatOffset.y,
  })
  adminConsoleFloatMoved = true
}

const startAdminConsoleFloatDrag = (event) => {
  if (event.button !== 0) return
  adminConsoleFloatDragging.value = true
  adminConsoleFloatMoved = false
  adminConsoleFloatOffset = {
    x: event.clientX - adminConsoleFloatPosition.value.x,
    y: event.clientY - adminConsoleFloatPosition.value.y,
  }
  window.addEventListener('pointermove', handleAdminConsoleFloatDrag)
  window.addEventListener('pointerup', stopAdminConsoleFloatDrag)
}

const handleAdminConsoleFloatOpen = () => {
  if (adminConsoleFloatMoved) {
    adminConsoleFloatMoved = false
    return
  }
  openAdminConsole()
}

const dismissAdminConsoleFloat = () => {
  adminConsoleFloatVisible.value = false
  persistAdminConsoleFloatState()
}

const handleAdminConsoleFloatResize = () => {
  adminConsoleFloatPosition.value = clampAdminConsoleFloatPosition(adminConsoleFloatPosition.value)
  persistAdminConsoleFloatState()
}

const handleAdminConsoleFloatToggle = (event) => {
  const visible = Boolean(event?.detail?.visible)
  adminConsoleFloatVisible.value = visible
  if (visible && (!adminConsoleFloatPosition.value.x || !adminConsoleFloatPosition.value.y)) {
    adminConsoleFloatPosition.value = getDefaultAdminConsoleFloatPosition()
  }
  persistAdminConsoleFloatState()
}

const handleLogout = async () => {
  try {
    await logout()
    clearAuthToken()
    authUser.value = null
    clearFeatureFlags()
    syncHistoryScope()
    ElMessage({
      message: '已退出登录',
      type: 'success',
      duration: 1800,
      customClass: 'app-toast-modern',
    })
  } catch {
    clearAuthToken()
    authUser.value = null
    clearFeatureFlags()
    syncHistoryScope()
  }
  if (route.path !== '/ask') {
    router.replace('/ask')
  }
}

const refreshCurrentPage = () => {
  window.location.reload()
}

const handleMenuSelect = (index) => {
  shellNavOpen.value = false
  if (!index || index === route.path) return
  const target = menuItems.find((item) => item.path === index)
  if (target && !canAccessMenuItem(target)) {
    ElMessage.warning('该功能暂未开放')
    return
  }
  router.push(index)
}

const fallbackRoute = () => availableMenuItems.value[0]?.path || '/ask'

const enforceRouteAccess = () => {
  if (!authUser.value || isAuthCallbackRoute.value) return
  const target = menuItems.find((item) => item.path === route.path)
  if (target && !canAccessMenuItem(target)) {
    const nextPath = fallbackRoute()
    if (route.path !== nextPath) router.replace(nextPath)
  }
}

// 新版外壳：任务历史以右侧抽屉呈现。切换/新建任务后自动收起抽屉。
const pulseHistoryPanel = () => {
  historyDrawerVisible.value = false
}

const openHistorySession = async (item) => {
  if (!item?.id) return
  setActiveHistory(item.id)
  // 如果点击的就是当前运行中/待确认/刚完成的任务，直接切回对应视图
  if (runningSessionId.value === item.id || completedTaskId.value === item.id) {
    switchViewToRunning()
    await router.push('/ask')
    pulseHistoryPanel()
  } else if (runningSessionId.value) {
    // 只要有后台运行中/待确认任务，都以只读模式打开历史，不打断当前任务
    setViewingTask(item.id)
    await requestRestore(item.id, { readonly: true })
    await router.push('/ask')
    pulseHistoryPanel()
  } else {
    // 没有活动任务时才恢复历史并重置当前会话
    switchViewToDefault()
    requestRestore(item.id)
    await router.push('/ask')
    pulseHistoryPanel()
  }
}

const removeHistoryItem = (id) => {
  removeHistory(id)
}

// 根据 history item 推断 TaskStatusIndicator 的 variant（仅历史项）
// 注意：执行中状态由 currentRunningTask 虚拟行单独处理
const inferTaskVariant = (item) => {
  if (item?.status === 'running' || (runningSessionId.value === item?.id && runningTaskStatus.value === 'running')) return 'running'
  const result = item?.reportSnapshot?.result || {}
  if (result.requires_confirmation) return 'pending_confirmation'
  if (result.error) return 'failed'
  return 'completed'
}

const createFreshChat = async () => {
  setActiveHistory('')
  switchViewToDefault()
  await router.push('/ask')
  window.dispatchEvent(new CustomEvent('datapulse-create-fresh-chat'))
  pulseHistoryPanel()
}

// 点击左侧执行中虚拟任务行：直接切回实时执行视图
const handleRunningTaskClick = async () => {
  switchViewToRunning()
  setActiveHistory(runningSessionId.value || '')
  await router.push('/ask')
  pulseHistoryPanel()
}

const clearHistoryList = async () => {
  try {
    await ElMessageBox.confirm(
      '清空后将删除当前保存的全部任务记录。',
      '清空任务',
      {
        type: 'info',
        confirmButtonText: '确认清空',
        cancelButtonText: '取消',
        customClass: 'ax-message-box',
      }
    )
  } catch {
    // user cancelled
    return
  }

  isClearingHistory.value = true
  try {
    await clearHistory()
    ElMessage.success('任务已清空')
  } catch (error) {
    ElMessage.error('清空失败，任务记录已恢复，请稍后重试')
  } finally {
    isClearingHistory.value = false
  }
}

let clockTimer = null
let healthTimer = null
let historyFocusTimer = null
let routePreloadScheduled = false

const scheduleRoutePreload = () => {
  if (routePreloadScheduled) return
  routePreloadScheduled = true
  const preload = () => {
    preloadRouteComponents(cachedPageNames.value).catch(() => {})
  }
  if (typeof window.requestIdleCallback === 'function') {
    window.requestIdleCallback(preload, { timeout: 2000 })
  } else {
    window.setTimeout(preload, 800)
  }
}

// 工作台头部「任务」入口 → 打开右侧任务抽屉
const handleHistoryFocus = () => {
  if (route.path !== '/ask') {
    router.push('/ask')
  }
  if (historyFocusTimer) {
    clearTimeout(historyFocusTimer)
  }
  historyFocusTimer = window.setTimeout(() => {
    historyDrawerVisible.value = true
  }, 60)
}

const handleGlobalClick = () => {
  closeUserMenu()
}

const handleFeatureFlagsUpdated = async () => {
  if (authUser.value) {
    await loadFeatureFlags(true)
  } else {
    clearFeatureFlags()
  }
  enforceRouteAccess()
}

const handleUnauthorized = () => {
  // 登录态失效（接口 401）：清空当前用户 → 模板回落到登录页
  if (authUser.value) {
    authUser.value = null
    clearFeatureFlags()
    syncHistoryScope()
  }
}

onMounted(() => {
  refreshClock()
  pingBackend()
  refreshAuthUser()
  clockTimer = setInterval(refreshClock, 1000)
  healthTimer = setInterval(pingBackend, 10000)
  window.addEventListener('datapulse-history-focus', handleHistoryFocus)
  window.addEventListener('click', handleGlobalClick)
  window.addEventListener('datapulse-feature-flags-updated', handleFeatureFlagsUpdated)
  window.addEventListener('datapulse:unauthorized', handleUnauthorized)
  window.addEventListener('keydown', handleCommandHotkey)
})

onUnmounted(() => {
  clearInterval(clockTimer)
  clearInterval(healthTimer)
  if (historyFocusTimer) {
    clearTimeout(historyFocusTimer)
  }
  window.removeEventListener('datapulse-history-focus', handleHistoryFocus)
  window.removeEventListener('click', handleGlobalClick)
  window.removeEventListener('datapulse-feature-flags-updated', handleFeatureFlagsUpdated)
  window.removeEventListener('datapulse:unauthorized', handleUnauthorized)
  window.removeEventListener('keydown', handleCommandHotkey)
})

watch(() => route.path, (path) => {
  enforceRouteAccess()
  if (path === '/ask') {
    loadHistory()
    syncHistory()
  }
})

watch(authUser, () => {
  syncHistoryScope()
  if (authUser.value) syncHistory()
  enforceRouteAccess()
})
onMounted(() => {
  restoreAdminConsoleFloatState()
  window.addEventListener('resize', handleAdminConsoleFloatResize)
  window.addEventListener(ADMIN_CONSOLE_FLOAT_TOGGLE_EVENT, handleAdminConsoleFloatToggle)
})

onUnmounted(() => {
  stopAdminConsoleFloatDrag()
  window.removeEventListener('resize', handleAdminConsoleFloatResize)
  window.removeEventListener(ADMIN_CONSOLE_FLOAT_TOGGLE_EVENT, handleAdminConsoleFloatToggle)
})
</script>

<style>
:root {
  --shell-bg: var(--bg-page, #F2F5F4);
  --panel-bg: var(--bg-card, #FFFFFF);
  --panel-border: var(--border, #E5E7EB);
  --ink-strong: var(--text-title, #111827);
  --ink-soft: var(--text-muted, #9CA3AF);
  --brand: #1d4ed8;
  --brand-soft: #eff6ff;
}

* {
  box-sizing: border-box;
}

html,
body,
#app {
  margin: 0;
  height: 100%;
  background: var(--bg-page);
  font-family: var(--font-sans, 'Microsoft YaHei UI', 'Microsoft YaHei', 'PingFang SC', sans-serif);
  color: var(--text-title, #111827);
}

.app-shell {
  height: 100%;
}

.auth-loading-screen {
  min-height: 100vh;
  display: grid;
  place-items: center;
  background: var(--bg-page, #F2F5F4);
}

.auth-loading-card {
  width: 260px;
  padding: 26px;
  border-radius: var(--radius-lg, 6px);
  display: grid;
  justify-items: center;
  gap: 9px;
  background: var(--bg-card, #FFFFFF);
  border: 1px solid var(--border, #E5E7EB);
  box-shadow: var(--shadow-lg, 0 4px 8px rgba(0,0,0,0.03), 0 16px 40px rgba(0,0,0,0.07));
  color: var(--text-title, #111827);
}

.auth-loading-card span {
  color: var(--text-secondary, #6B7280);
  font-size: 12px;
}

.auth-loading-mark {
  width: 38px;
  height: 38px;
  border-radius: 10px;
  background: rgba(8, 17, 16, 0.88);
  animation: auth-loading-pulse 1.2s ease-in-out infinite alternate;
}

@keyframes auth-loading-pulse {
  from { transform: scale(0.92); opacity: 0.72; }
  to { transform: scale(1); opacity: 1; }
}

/* ==========================================================================
   外壳：顶部横向导航（新版布局 · 无左侧栏）
   ========================================================================== */

.app-shell {
  display: flex;
  flex-direction: column;
  height: 100%;
}

/* ── 顶栏容器：清雅浅底 + 绿色呼吸节奏 ── */
.app-topnav {
  display: flex;
  align-items: center;
  gap: 16px;
  flex: 0 0 auto;
  height: 56px !important;
  padding: 0 20px;
  background: linear-gradient(180deg, #ffffff 0%, #f6faf9 100%);
  border-bottom: 1.5px solid #e1efe9 !important;
  box-shadow: 0 2px 8px rgba(29, 78, 216, 0.04);
  z-index: 40;
}

/* ── 品牌区 ── */
.topnav-brand {
  display: inline-flex;
  align-items: center;
  gap: 9px;
  flex: 0 0 auto;
  padding: 5px 10px 5px 6px;
  border: 0;
  border-radius: 6px;
  background: transparent;
  cursor: pointer;
  transition: background var(--duration-fast, 150ms) var(--ease-out, ease);
}

.topnav-brand:hover {
  background: rgba(29, 78, 216, 0.07);
}

.topnav-logo {
  height: 28px;
  width: auto;
  object-fit: contain;
  flex-shrink: 0;
}

.topnav-brand-name {
  font-size: 17px;
  font-weight: 800;
  letter-spacing: -0.02em;
  color: #0f172a;
  white-space: nowrap;
}

/* 脉策智能绿色实体块 */
.topnav-brand-env {
  padding: 2.5px 8px;
  border-radius: 5px;
  background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%);
  color: #ffffff;
  font-size: 10.5px;
  font-weight: 700;
  letter-spacing: 0.04em;
  white-space: nowrap;
  box-shadow: 0 1px 3px rgba(29, 78, 216, 0.25);
}

/* ── 横向主导航：激活项为高辨识度实心绿色块 ── */
.topnav-menu.el-menu {
  flex: 1 1 auto;
  min-width: 0;
  height: 56px;
  border-bottom: 0 !important;
  background: transparent;
}

.topnav-menu.el-menu--horizontal > .el-menu-item,
.topnav-menu.el-menu--horizontal > .el-sub-menu > .el-sub-menu__title {
  position: relative;
  display: inline-flex;
  align-items: center;
  height: 36px !important;
  line-height: 36px !important;
  margin: 10px 4px;
  padding: 0 16px !important;
  border-bottom: 0 !important;
  border-radius: 7px;
  background: transparent !important;
  color: #475569 !important;
  font-size: 13.5px;
  font-weight: 600;
  transition: all 0.18s ease;
}

.topnav-menu .el-menu-item .el-icon,
.topnav-menu .el-sub-menu__title .el-icon {
  width: 17px;
  height: 17px;
  margin-right: 6px;
  font-size: 16px;
  color: inherit;
}

.topnav-menu.el-menu--horizontal > .el-menu-item:hover,
.topnav-menu.el-menu--horizontal > .el-sub-menu > .el-sub-menu__title:hover {
  color: #1d4ed8 !important;
  background: rgba(29, 78, 216, 0.08) !important;
}

/* 主导航与溢出菜单使用相同的浅蓝激活态。 */
.topnav-menu.el-menu--horizontal > .el-menu-item.is-active,
.topnav-menu.el-menu--horizontal > .el-sub-menu.is-active > .el-sub-menu__title {
  color: #1d4ed8 !important;
  background: #eff6ff !important;
  border-bottom: 0 !important;
  font-weight: 700;
  box-shadow: none;
}

.topnav-menu.el-menu--horizontal > .el-menu-item.is-active .el-icon,
.topnav-menu.el-menu--horizontal > .el-sub-menu.is-active > .el-sub-menu__title .el-icon {
  color: #1d4ed8 !important;
}

.topnav-menu.el-menu--horizontal > .el-menu-item.is-active::after,
.topnav-menu.el-menu--horizontal > .el-sub-menu.is-active > .el-sub-menu__title::after {
  content: none;
}

/* ── 系统管理下拉指示箭头微调（ellipsis 溢出菜单同样复用） ── */
.topnav-menu .el-sub-menu .el-sub-menu__icon-arrow {
  position: static !important;
  margin-top: 0 !important;
  margin-left: 6px !important;
  font-size: 11px !important;
  color: #94a3b8 !important;
  transition: transform 0.25s cubic-bezier(0.16, 1, 0.3, 1), color 0.2s ease !important;
}

.topnav-menu .el-sub-menu:hover .el-sub-menu__icon-arrow {
  color: #1d4ed8 !important;
}

.topnav-menu .el-sub-menu.is-active .el-sub-menu__icon-arrow {
  color: #ffffff !important;
}

.topnav-menu .el-sub-menu.is-opened .el-sub-menu__icon-arrow {
  transform: rotate(180deg) !important;
}

/* ── 管理配置下拉浮层：浅绿精致卡片 ── */
.el-menu--popup {
  min-width: 190px !important;
  padding: 6px !important;
  border-radius: 8px !important;
  background: #ffffff !important;
  border: 1px solid #d1fae5 !important;
  box-shadow: 0 12px 32px rgba(29, 78, 216, 0.12) !important;
}

.el-menu--popup .el-menu-item {
  height: 36px !important;
  line-height: 36px !important;
  margin: 2px 0 !important;
  padding: 0 12px !important;
  border-radius: 6px !important;
  font-size: 13px !important;
  font-weight: 500 !important;
  color: #334155 !important;
  background: transparent !important;
  transition: background-color 0.15s ease, color 0.15s ease !important;
}

.el-menu--popup .el-menu-item .el-icon {
  width: 16px !important;
  height: 16px !important;
  font-size: 15px !important;
  margin-right: 8px !important;
  color: #1d4ed8 !important;
}

.el-menu--popup .el-menu-item:hover {
  background: #f0fdf4 !important;
  color: #1d4ed8 !important;
}

.el-menu--popup .el-menu-item.is-active {
  background: #1d4ed8 !important;
  color: #ffffff !important;
  font-weight: 600 !important;
}

.el-menu--popup .el-menu-item.is-active .el-icon {
  color: #ffffff !important;
}

/* ── 顶栏右侧动作区 ── */
.topnav-actions {
  display: flex;
  align-items: center;
  gap: 10px;
  flex: 0 0 auto;
}

.history-item {
  position: relative;
  display: flex;
  align-items: flex-start;
  /* bug 2026-08-25 全角色方案：卡片死硬固定 100px（!important 防内部样式覆盖），
     4 个大小永远一致；内容溢出被 overflow hidden 截断 */
  flex: none !important;
  height: 100px !important;
  min-height: 100px !important;
  max-height: 100px !important;
  box-sizing: border-box;
  gap: 10px;
  width: 100%;
  padding: 12px 14px;
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.03);
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  animation: history-item-enter 0.24s cubic-bezier(0.4, 0, 0.2, 1);
  overflow: hidden;
}

.history-item::before {
  content: '';
  position: absolute;
  left: 0;
  top: 12px;
  bottom: 12px;
  width: 3px;
  border-radius: 999px;
  background: transparent;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.history-item:hover {
  border-color: rgba(255, 255, 255, 0.12);
  background: rgba(255, 255, 255, 0.07);
  box-shadow: 0 4px 12px rgba(0,0,0,0.12);
  transform: translateY(-1px);
}

.history-item-active {
  border-color: rgba(29, 78, 216, 0.25);
  background: rgba(29, 78, 216, 0.1);
  box-shadow: 0 2px 8px rgba(29, 78, 216, 0.08);
}

.history-item-active::before {
  background: var(--brand-primary, #1d4ed8);
}

.history-item-active .history-item-title {
  color: #ffffff;
  font-weight: 600;
}

.history-item-main {
  min-width: 0;
  flex: 1;
  /* 卡片内容垂直居中：标题在上，底行(时间+状态)在下 */
  display: flex;
  flex-direction: column;
  justify-content: center;
  height: 100%;
  gap: 6px;
}

/* 卡片底行：时间靠左，状态靠右 */
.history-item-bottom {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 6px;
  min-width: 0;
}

.history-item-top {
  display: flex;
  align-items: flex-start;
  gap: 6px;
  padding-right: 2px;
  min-width: 0;
  flex: 1;
}

.history-item-title {
  font-size: 12px;
  line-height: 1.52;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.85);
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  min-width: 0;
  /* 标题只占自然高度，不拉伸，由 main 垂直居中 */
  flex: 0 0 auto;
  /* 避免两行标题贴到右侧删除按钮 */
  padding-right: 4px;
}

.history-item-badge {
  flex-shrink: 0;
  height: 17px;
  padding: 0 6px;
  border-radius: 999px;
  background: var(--brand-primary, #1d4ed8);
  color: #ffffff;
  font-size: 10px;
  font-weight: 700;
  display: inline-flex;
  align-items: center;
}

/* 状态指示容器：标题 + 状态指示器 + 当前 badge 同行排列 */
.history-item-status {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  flex-shrink: 0;
  margin-left: auto;
}

/* 虚拟"当前执行任务"行：与历史项区分，左红竖条 + 微红底 */
.history-item-running {
  position: relative;
  background: linear-gradient(135deg, rgba(29, 78, 216, 0.1) 0%, rgba(29, 78, 216, 0.06) 100%);
  border: 1px solid rgba(29, 78, 216, 0.2);
  border-radius: 12px;
  margin-bottom: 10px;
  padding-right: 14px;
}

.history-item-running::before {
  content: '';
  position: absolute;
  left: 0;
  top: 10px;
  bottom: 10px;
  width: 3px;
  border-radius: 2px;
  background: var(--brand-primary, #1d4ed8);
  opacity: 0.9;
}

.history-item-running .history-item-title {
  font-weight: 600;
}

.history-item-meta,
.history-item-time {
  margin-top: 6px;
  font-size: 11px;
  line-height: 1.4;
  color: rgba(255, 255, 255, 0.55);
}

.history-item-delete {
  width: 22px;
  height: 22px;
  border: 1px solid transparent;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.08);
  color: rgba(255, 255, 255, 0.6);
  cursor: pointer;
  font-size: 13px;
  line-height: 1;
  flex-shrink: 0;
  margin-top: 1px;
  transition: all 0.18s ease;
}

.history-item-delete-icon {
  position: relative;
  width: 10px;
  height: 10px;
  display: inline-flex;
}

.history-item-delete-icon::before,
.history-item-delete-icon::after {
  content: '';
  position: absolute;
  left: 4px;
  top: 0;
  width: 1.5px;
  height: 10px;
  border-radius: 999px;
  background: currentColor;
}

.history-item-delete-icon::before {
  transform: rotate(45deg);
}

.history-item-delete-icon::after {
  transform: rotate(-45deg);
}

.history-item-delete:hover {
  border-color: var(--border, #E5E7EB);
  background: var(--bg-card, #FFFFFF);
  color: var(--text-secondary, #6B7280);
  box-shadow: var(--shadow-xs, 0 1px 2px rgba(0,0,0,0.04));
}

@keyframes history-item-enter {
  from {
    opacity: 0;
    transform: translateX(-5px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.history-empty {
  min-height: 176px;
  border: 1px dashed var(--border-hover, #D1D5DB);
  border-radius: var(--radius-md, 12px);
  background: var(--bg-soft, #F3F4F6);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 18px;
}

.history-empty-title {
  font-size: 12px;
  font-weight: 600;
  color: var(--text-title, #111827);
}

.history-empty-desc {
  margin-top: 6px;
  font-size: 10px;
  line-height: 1.6;
  color: var(--text-secondary, #6B7280);
}

.history-drawer {
  border-radius: 8px 0 0 8px;
  overflow: hidden;
  border-left: 1px solid rgba(17, 24, 39, 0.08);
  box-shadow: 0 24px 56px rgba(15, 23, 42, 0.12);
}

.history-drawer .el-drawer__header {
  margin-bottom: 0;
  padding: 24px 26px 16px;
  border-bottom: 1px solid var(--border, #E5E7EB);
  background: var(--bg-card, #FFFFFF);
}

.history-drawer .el-drawer__title {
  color: var(--text-title, #111827);
  font-size: 20px;
  font-weight: 900;
  letter-spacing: -0.02em;
}

.history-drawer .el-drawer__body {
  padding: 18px 18px 22px;
  display: flex;
  flex-direction: column;
  min-height: 0;
  background: #F8F8F7;
}

.history-drawer-head {
  position: relative;
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 14px;
  padding: 16px;
  border: 1px solid rgba(17, 24, 39, 0.08);
  border-radius: 6px;
  background: #FFFFFF;
  box-shadow: 0 10px 22px rgba(15, 23, 42, 0.045);
}

.history-drawer-title {
  color: var(--text-title, #111827);
  font-size: 16px;
  font-weight: 900;
}

.history-drawer-desc {
  margin-top: 4px;
  color: var(--text-secondary, #6B7280);
  font-size: 12px;
}

.history-drawer-clear {
  height: 30px;
  padding: 0 12px;
  border: 1px solid var(--error-soft, #eff6ff);
  border-radius: 999px;
  background: var(--error-soft, #eff6ff);
  color: var(--error, #1d4ed8);
  font-size: 11px;
  font-weight: 800;
  cursor: pointer;
}

.history-drawer-list {
  flex: 1;
  min-height: 0;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 14px;
  padding-right: 4px;
}

.history-drawer-item {
  position: relative;
  margin: 0;
  align-items: center;
  /* 抽屉内卡片保持自然高度，不参与侧栏卡片的均分拉伸 */
  flex: 0 0 auto;
  gap: 14px;
  min-height: 94px;
  padding: 18px 46px 18px 18px;
  border-radius: 6px;
  border-color: rgba(17, 24, 39, 0.07);
  background: #FFFFFF;
  box-shadow: 0 8px 20px rgba(15, 23, 42, 0.035);
}

.history-drawer-item:hover {
  border-color: rgba(17, 24, 39, 0.12);
  box-shadow: 0 12px 26px rgba(15, 23, 42, 0.055);
  background: #FFFFFF;
}

.history-drawer-item.history-item-active {
  border-color: rgba(29, 78, 216, 0.18);
  background: #F5F6F8;
  box-shadow:
    0 10px 24px rgba(15, 23, 42, 0.045),
    inset 4px 0 0 #1d4ed8;
}

.history-drawer-item.history-item-active::before {
  background: transparent;
}

.history-drawer-index {
  width: 42px;
  height: 42px;
  border-radius: 10px;
  flex-shrink: 0;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  color: #6B7280;
  font-size: 13px;
  font-weight: 900;
  background: #F1F0EE;
  border: 1px solid rgba(17, 24, 39, 0.08);
}

.history-drawer-item .history-item-title {
  color: #111827;
  font-size: 15px;
  font-weight: 800;
  line-height: 1.45;
  text-shadow: none;
  -webkit-line-clamp: 2;
}

.history-drawer-item.history-item-active .history-item-title {
  color: #111827;
  font-weight: 900;
}

.history-drawer-meta-row {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 10px;
}

/* 抽屉内 main 恢复默认块布局，不继承侧栏卡片的垂直居中 */
.history-drawer-item .history-item-main {
  display: block;
  height: auto;
  justify-content: normal;
  gap: 0;
}

.history-drawer-dataset {
  max-width: 210px;
  height: 24px;
  padding: 0 10px;
  border-radius: 999px;
  display: inline-flex;
  align-items: center;
  color: #6B7280;
  font-size: 12px;
  font-weight: 800;
  background: #F1F0EE;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.history-drawer-time {
  color: #9CA3AF;
  font-size: 12px;
  font-variant-numeric: tabular-nums;
}

.history-drawer-item .history-item-delete {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  opacity: 0;
}

.history-drawer-item:hover .history-item-delete {
  opacity: 1;
}

.history-drawer-empty {
  flex: 1;
}

.ax-message-box {
  border-radius: var(--radius-xl, 8px) !important;
  border: 1px solid var(--border, #E5E7EB) !important;
  box-shadow: var(--shadow-lg, 0 4px 8px rgba(0,0,0,0.03), 0 16px 40px rgba(0,0,0,0.07)) !important;
  padding: 18px 18px 16px !important;
}

.ax-message-box .el-message-box__header {
  padding-bottom: 6px;
}

.ax-message-box .el-message-box__title {
  font-size: 20px;
  font-weight: 700;
  color: var(--text-title, #111827);
}

.ax-message-box .el-message-box__headerbtn {
  top: 16px;
  right: 16px;
}

.ax-message-box .el-message-box__status {
  width: 22px;
  height: 22px;
  margin-right: 10px;
  border-radius: 999px;
  background: var(--bg-soft, #F3F4F6);
  color: var(--text-secondary, #6B7280) !important;
}

.ax-message-box .el-message-box__content {
  padding-top: 4px;
  padding-bottom: 8px;
}

.ax-message-box .el-message-box__message {
  font-size: 14px;
  line-height: 1.7;
  color: var(--text-body, #374151);
}

.ax-message-box .el-message-box__btns {
  padding-top: 8px;
}

.ax-message-box .el-button {
  min-width: 96px;
  height: 36px;
  border-radius: 999px;
}

/* ===== 顶栏右上：用户菜单 ===== */
.topnav-user {
  position: relative;
}

.topnav-user-chip {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  height: 33px;
  padding: 0 9px 0 4px;
  border: 1px solid rgba(29, 78, 216, 0.22);
  border-radius: 6px;
  background: #eff6ff;
  cursor: pointer;
  text-align: left;
  transition: all var(--duration-fast, 150ms) var(--ease-out, ease);
}

.topnav-user-chip:hover {
  border-color: #1d4ed8;
  background: #ffffff;
  box-shadow: 0 2px 6px rgba(29, 78, 216, 0.12);
}

.topnav-user-avatar {
  flex: 0 0 auto;
  width: 26px;
  height: 26px;
  border-radius: 50%;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0;
  color: #ffffff;
  background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%);
  box-shadow: 0 2px 6px rgba(15, 118, 110, 0.28);
}

.topnav-user-status {
  flex: 0 0 auto;
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #cbd5e1;
}

.topnav-user-status.is-online {
  background: #10b981;
  box-shadow: 0 0 0 2px rgba(16, 185, 129, 0.16);
}

.topnav-user-meta {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 0;
  min-width: 0;
}

.topnav-user-name {
  max-width: 100px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-size: 12px;
  font-weight: 700;
  color: #1e293b;
  line-height: 1.2;
}

.topnav-user-role {
  font-size: 10px;
  color: #64748b;
  line-height: 1.2;
}

.topnav-user-arrow {
  flex: 0 0 auto;
  width: 0;
  height: 0;
  border-left: 4px solid transparent;
  border-right: 4px solid transparent;
  border-top: 5px solid #94a3b8;
}

.topnav-user-dropdown {
  position: absolute;
  right: 0;
  top: calc(100% + 8px);
  z-index: 60;
  width: 224px;
  padding: 6px;
  border-radius: var(--radius-md, 6px);
  background: #ffffff;
  border: 1px solid var(--border, #D6DEDB);
  box-shadow: 0 16px 40px rgba(11, 22, 21, 0.22);
}

.topnav-user-dropdown button {
  display: flex;
  flex-direction: column;
  gap: 2px;
  width: 100%;
  padding: 9px 10px;
  border: 0;
  border-radius: 10px;
  background: transparent;
  text-align: left;
  cursor: pointer;
  transition: background var(--duration-fast, 150ms) var(--ease-out, ease);
}

.topnav-user-dropdown button:hover {
  background: var(--brand-primary-soft, #eff6ff);
}

.topnav-user-dropdown button strong {
  font-size: 13px;
  font-weight: 600;
  color: var(--text-title, #0F172A);
}

.topnav-user-dropdown button span {
  font-size: 11px;
  color: var(--text-secondary, #64748B);
}

.topnav-user-dropdown button.danger strong {
  color: var(--error, #DC2626);
}

/* 主体容器：顶栏之下的全宽区域 */
.app-body {
  flex: 1 1 auto;
  min-width: 0;
  min-height: 0;
}

/* ===== 二级上下文条（非工作台页面显示） ===== */
.context-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  flex: 0 0 auto;
  height: 46px !important;
  padding: 0 24px;
  background: #ffffff;
  border-bottom: 1px solid var(--border, #D6DEDB) !important;
}

.context-left {
  display: flex;
  align-items: center;
  gap: 10px;
  min-width: 0;
}

.context-title {
  position: relative;
  font-size: 15px;
  font-weight: 700;
  color: var(--text-title, #111827);
  white-space: nowrap;
  padding-left: 10px;
}

/* 标题左侧青色竖条：新版识别标记 */
.context-title::before {
  content: '';
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 3px;
  height: 14px;
  background: #1d4ed8;
  border-radius: 1px;
}

.context-subtitle {
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-size: 12px;
  color: var(--text-muted, #94A3B8);
}

.context-back {
  flex: 0 0 auto;
  height: 26px;
  padding: 0 11px;
  border: 1px solid var(--border, #D6DEDB);
  border-radius: 4px;
  background: #ffffff;
  color: var(--text-secondary, #475569);
  font-size: 12px;
  font-weight: 650;
  cursor: pointer;
  white-space: nowrap;
  transition: all 0.2s ease;
}

.context-back:hover {
  border-color: var(--brand-primary, #1d4ed8);
  background: var(--brand-primary-soft, #eff6ff);
  color: var(--brand-primary, #1d4ed8);
}

.context-right {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-shrink: 0;
}

.admin-login-button,
.feishu-login-button {
  height: 30px;
  padding: 0 14px;
  border: 1px solid var(--border, #E5E7EB);
  border-radius: 999px;
  background: var(--bg-card, #FFFFFF);
  color: var(--text-body, #374151);
  font-size: 12px;
  font-weight: 800;
  cursor: pointer;
  box-shadow: var(--shadow-xs, 0 1px 2px rgba(0,0,0,0.04));
  transition: all 0.2s ease;
}

.admin-login-button {
  border-color: var(--border, #E5E7EB);
  background: var(--bg-card, #FFFFFF);
  color: var(--text-body, #374151);
  box-shadow: var(--shadow-xs, 0 1px 2px rgba(0,0,0,0.04));
}

.admin-login-button:hover,
.feishu-login-button:hover:not(:disabled) {
  transform: translateY(-1px);
}

.feishu-login-button:hover:not(:disabled) {
  border-color: var(--border-hover, #D1D5DB);
  background: var(--bg-soft, #F3F4F6);
}

.admin-login-button:hover {
  border-color: var(--border-hover, #D1D5DB);
  background: var(--bg-soft, #F3F4F6);
}

.feishu-login-button:disabled {
  cursor: not-allowed;
  opacity: 0.7;
}


.admin-console-float {
  position: fixed;
  z-index: 1200;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  touch-action: none;
}

.admin-console-float-main,
.admin-console-float-close {
  border: 1px solid var(--border, #E5E7EB);
  color: var(--text-title, #111827);
  background: var(--bg-card, #FFFFFF);
  box-shadow: var(--shadow-lg, 0 4px 8px rgba(0,0,0,0.03), 0 16px 40px rgba(0,0,0,0.07));
}

.admin-console-float-main {
  height: 44px;
  padding: 0 16px;
  border-radius: 999px;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  font-weight: 700;
  cursor: grab;
}

.admin-console-float-main.dragging {
  cursor: grabbing;
}

.admin-console-float-main .el-icon {
  width: 20px;
  height: 20px;
  border-radius: 999px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  color: #ffffff;
  background: var(--brand-black, #1A1A1A);
}

.admin-console-float-close {
  width: 34px;
  height: 34px;
  border-radius: 999px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  font-weight: 700;
  cursor: pointer;
}

.admin-console-float-main:hover,
.admin-console-float-close:hover {
  transform: translateY(-1px);
}

.admin-login-dialog {
  border-radius: 6px !important;
}

.admin-login-form {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.admin-login-field {
  display: flex;
  flex-direction: column;
  gap: 7px;
  color: var(--text-body, #374151);
  font-size: 13px;
  font-weight: 700;
}

.admin-login-field input {
  height: 38px;
  padding: 0 12px;
  border: 1px solid var(--border, #E5E7EB);
  border-radius: var(--radius-sm, 8px);
  outline: none;
  color: var(--text-title, #111827);
  font-size: 14px;
  transition: all 0.18s ease;
}

.admin-login-field input:focus {
  border-color: var(--brand-primary, #1d4ed8);
  box-shadow: 0 0 0 3px var(--brand-primary-focus, rgba(29, 78, 216, 0.16));
}

.auth-password-button {
  height: 22px;
  padding: 0 8px;
  border: 0;
  border-radius: 999px;
  background: var(--bg-soft, #F3F4F6);
  color: var(--text-secondary, #6B7280);
  font-size: 11px;
  font-weight: 750;
  cursor: pointer;
}

.auth-password-button:hover {
  background: var(--border-light, #F3F4F6);
}

.password-dialog {
  border-radius: var(--radius-lg, 6px) !important;
  overflow: hidden;
  box-shadow: var(--shadow-xl, 0 8px 16px rgba(0,0,0,0.04), 0 24px 56px rgba(0,0,0,0.08)) !important;
}

.password-dialog .el-dialog__header {
  padding: 22px 28px 14px;
  margin: 0;
  border-bottom: 0;
}

.password-dialog .el-dialog__title {
  font-size: 18px;
  font-weight: 900;
  color: var(--text-title, #111827);
}

.password-dialog .el-dialog__body {
  padding: 8px 28px 24px;
}

.password-dialog .el-dialog__footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  padding: 18px 28px 24px;
  border-top: 1px solid var(--border-light, #F3F4F6);
  background: var(--bg-card, #FFFFFF);
}

.password-panel {
  margin-bottom: 18px;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px;
  border: 1px solid var(--brand-primary-soft, #eff6ff);
  border-radius: var(--radius-md, 12px);
  background: var(--brand-primary-soft, #eff6ff);
}

.password-panel-icon {
  width: 38px;
  height: 38px;
  border-radius: var(--radius-sm, 8px);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  background: var(--brand-black, #1A1A1A);
  color: #fff;
  font-size: 13px;
  font-weight: 900;
  box-shadow: var(--shadow-sm, 0 1px 3px rgba(0,0,0,0.04));
}

.password-panel h3 {
  margin: 0;
  color: var(--text-title, #111827);
  font-size: 14px;
  font-weight: 900;
}

.password-panel p {
  margin: 6px 0 0;
  color: var(--text-secondary, #6B7280);
  font-size: 12px;
  line-height: 1.5;
}

.password-form {
  display: flex;
  flex-direction: column;
  gap: 13px;
}

.password-form label {
  display: flex;
  flex-direction: column;
  gap: 7px;
  color: var(--text-body, #374151);
  font-size: 13px;
  font-weight: 800;
}

.password-form input {
  width: 100%;
  height: 40px;
  box-sizing: border-box;
  padding: 0 13px;
  border: 1px solid var(--border, #E5E7EB);
  border-radius: var(--radius-sm, 8px);
  outline: none;
  color: var(--text-title, #111827);
  font-size: 14px;
  background: var(--bg-card, #FFFFFF);
  transition: all 0.18s ease;
}

.dialog-password-control {
  position: relative;
}

.dialog-password-control input {
  padding-right: 44px;
}

.dialog-password-control input[type="password"] {
  font-size: 20px;
}

.dialog-password-control input::placeholder {
  font-size: 13px;
}

.dialog-password-eye {
  position: absolute;
  right: 6px;
  top: 50%;
  width: 30px;
  height: 30px;
  padding: 0;
  border: 0;
  border-radius: var(--radius-xs, 6px);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  color: var(--text-muted, #9CA3AF);
  background: transparent;
  cursor: pointer;
  transition: all 0.18s ease;
  transform: translateY(-50%);
}

.dialog-password-eye:hover {
  color: var(--text-secondary, #6B7280);
  background: var(--bg-soft, #F3F4F6);
}

.dialog-password-eye .el-icon {
  font-size: 16px;
}

.password-form input:focus {
  border-color: var(--brand-primary, #1d4ed8);
  box-shadow: 0 0 0 3px var(--brand-primary-focus, rgba(29, 78, 216, 0.16));
}

.dialog-ghost-button,
.dialog-primary-button {
  min-width: 82px;
  height: 38px;
  padding: 0 18px;
  border-radius: 11px;
  font-size: 13px;
  font-weight: 800;
  cursor: pointer;
  transition: all 0.18s ease;
}

.dialog-ghost-button {
  border: 1px solid var(--border, #E5E7EB);
  background: var(--bg-card, #FFFFFF);
  color: var(--text-body, #374151);
}

.dialog-primary-button {
  border: 1px solid var(--brand-primary, #1d4ed8);
  background: var(--brand-primary, #1d4ed8);
  color: #fff;
  box-shadow: var(--shadow-sm, 0 1px 3px rgba(0,0,0,0.04));
}

.dialog-ghost-button:hover {
  border-color: var(--border-hover, #D1D5DB);
  background: var(--bg-soft, #F3F4F6);
}

.dialog-primary-button:hover {
  background: var(--brand-primary-hover, #1e40af);
  border-color: var(--brand-primary-hover, #1e40af);
}

.dialog-primary-button:disabled {
  cursor: not-allowed;
  opacity: 0.7;
}

.app-toast-modern.el-message {
  min-width: 0;
  width: auto;
  max-width: min(360px, calc(100vw - 32px));
  padding: 9px 13px;
  border: 1px solid var(--border, #E5E7EB);
  border-radius: var(--radius-sm, 8px);
  background: var(--bg-card, #FFFFFF);
  box-shadow: var(--shadow-md, 0 2px 4px rgba(0,0,0,0.03), 0 8px 24px rgba(0,0,0,0.05));
  backdrop-filter: blur(10px);
}

.app-toast-modern .el-message__content {
  color: var(--text-title, #111827);
  font-size: 12px;
  font-weight: 760;
  line-height: 1.35;
}

.app-toast-modern .el-message__icon {
  margin-right: 8px;
  color: var(--brand-black, #1A1A1A);
  font-size: 14px;
}

.backend-status-chip {
  height: 26px;
  padding: 0 10px;
  border-radius: 4px;
  display: inline-flex;
  align-items: center;
  gap: 7px;
  font-size: 12px;
  font-weight: 750;
  letter-spacing: 0.01em;
  border: 1px solid var(--border, #D6DEDB);
  background: var(--bg-card, #FFFFFF);
  color: var(--text-secondary, #6B7280);
  box-shadow: none;
}

.backend-status-chip.is-online {
  border-color: rgba(16, 185, 129, 0.32);
  background: var(--success-soft, #ECFDF5);
  color: var(--success, #059669);
}

.backend-status-chip.is-offline {
  border-color: rgba(220, 38, 38, 0.28);
  background: var(--error-soft, #FEF2F2);
  color: var(--error, #DC2626);
}

.backend-status-dot {
  width: 7px;
  height: 7px;
  border-radius: 2px;
  background: currentColor;
  box-shadow: 0 0 0 3px color-mix(in srgb, currentColor 14%, transparent);
}

.clock {
  font-variant-numeric: tabular-nums;
  color: var(--text-muted, #9CA3AF);
  font-size: 12px;
}

.page-wrap {
  padding: 0 24px 24px;
  overflow: auto;
  background: var(--bg-page, #F2F5F4);
}

.page-wrap-smart {
  /* 工作台全出血：内容区自行管padding，外壳不再留边 */
  padding: 0;
  overflow: hidden;
  display: flex;
  min-height: 0;
}

.page-wrap-smart > * {
  flex: 1;
  min-height: 0;
}

.page-wrap > * {
  animation: page-enter 0.28s ease;
}

.history-panel-enter-active,
.history-panel-leave-active {
  transition: all 0.2s ease;
}

.history-panel-enter-from,
.history-panel-leave-to {
  opacity: 0;
  transform: translateY(6px);
}

@keyframes page-enter {
  from { opacity: 0; transform: translateY(8px); }
  to { opacity: 1; transform: translateY(0); }
}

/* ===== 全局命令面板（⌘K） ===== */
.command-palette-mask {
  position: fixed;
  inset: 0;
  z-index: 3000;
  display: flex;
  align-items: flex-start;
  justify-content: center;
  padding: 12vh 20px 20px;
  background: rgba(15, 23, 42, 0.42);
  backdrop-filter: saturate(140%) blur(6px);
  -webkit-backdrop-filter: saturate(140%) blur(6px);
}

.command-palette {
  width: 100%;
  max-width: 560px;
  max-height: 60vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  border: 1px solid var(--border, #E2E8F0);
  border-radius: var(--radius-xl, 8px);
  background: var(--bg-card, #FFFFFF);
  box-shadow: 0 32px 80px rgba(11, 22, 21, 0.35);
}

.command-palette-search {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 14px 16px;
  border-bottom: 1px solid var(--border-light, #eff6ff);
  background: var(--brand-gradient-soft, linear-gradient(135deg, #eff6ff 0%, #eff6ff 100%));
}

.command-palette-search-icon {
  flex: 0 0 auto;
  width: 15px;
  height: 15px;
  border-radius: 50%;
  border: 1.8px solid var(--brand-primary, #1d4ed8);
  position: relative;
}

.command-palette-search-icon::after {
  content: '';
  position: absolute;
  left: 12px;
  top: 12px;
  width: 7px;
  height: 2px;
  border-radius: 2px;
  background: var(--brand-primary, #1d4ed8);
  transform: rotate(45deg);
  transform-origin: left center;
}

.command-palette-input {
  flex: 1 1 auto;
  min-width: 0;
  border: 0;
  outline: none;
  background: transparent;
  color: var(--text-title, #0F172A);
  font-size: 15px;
}

.command-palette-input::placeholder {
  color: var(--text-placeholder, #CBD5E1);
}

.command-palette-hint {
  flex: 0 0 auto;
  padding: 2px 8px;
  border: 1px solid var(--border, #E2E8F0);
  border-radius: 6px;
  background: rgba(255, 255, 255, 0.7);
  color: var(--text-muted, #94A3B8);
  font-size: 11px;
  letter-spacing: 0.02em;
}

.command-palette-list {
  flex: 1 1 auto;
  min-height: 0;
  overflow-y: auto;
  padding: 8px;
}

.command-palette-item {
  display: flex;
  align-items: center;
  gap: 12px;
  width: 100%;
  padding: 10px 12px;
  border: 0;
  border-radius: var(--radius-md, 12px);
  background: transparent;
  text-align: left;
  cursor: pointer;
  transition: background var(--duration-fast, 150ms) var(--ease-out, ease);
}

.command-palette-item.is-active {
  background: var(--brand-primary-soft, #eff6ff);
}

.command-palette-item-icon {
  flex: 0 0 auto;
  width: 32px;
  height: 32px;
  border-radius: 10px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: var(--brand-gradient-soft, linear-gradient(135deg, #eff6ff 0%, #eff6ff 100%));
  color: var(--brand-primary, #1d4ed8);
  font-size: 16px;
}

.command-palette-item.is-active .command-palette-item-icon {
  background: var(--brand-gradient, linear-gradient(135deg, #1d4ed8 0%, #2563eb 100%));
  color: #ffffff;
}

.command-palette-item-body {
  display: flex;
  flex-direction: column;
  gap: 1px;
  min-width: 0;
}

.command-palette-item-label {
  font-size: 13px;
  font-weight: 600;
  color: var(--text-title, #0F172A);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.command-palette-item-path {
  font-family: var(--font-mono, monospace);
  font-size: 11px;
  color: var(--text-muted, #94A3B8);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.command-palette-empty {
  padding: 26px 12px;
  text-align: center;
  color: var(--text-muted, #94A3B8);
  font-size: 13px;
}

/* 面板/菜单过渡动画 */
.palette-fade-enter-active,
.palette-fade-leave-active {
  transition: opacity 0.2s ease;
}

.palette-fade-enter-active .command-palette,
.palette-fade-leave-active .command-palette {
  transition: transform 0.22s var(--ease-out, cubic-bezier(0.16, 1, 0.3, 1));
}

.palette-fade-enter-from,
.palette-fade-leave-to {
  opacity: 0;
}

.palette-fade-enter-from .command-palette,
.palette-fade-leave-to .command-palette {
  transform: translateY(-12px) scale(0.98);
}

.user-menu-rise-enter-active,
.user-menu-rise-leave-active {
  transition: opacity 0.18s ease, transform 0.18s var(--ease-out, cubic-bezier(0.16, 1, 0.3, 1));
}

.user-menu-rise-enter-from,
.user-menu-rise-leave-to {
  opacity: 0;
  transform: translateY(8px);
}

@media (max-width: 1180px) {
  .topnav-brand-env {
    display: none;
  }

  .topnav-user-meta {
    display: none;
  }

  .topnav-user-chip {
    padding: 0 10px 0 4px;
  }
}

@media (max-width: 900px) {
  .app-topnav {
    gap: 10px;
    padding: 0 12px;
  }

  .topnav-brand-name {
    display: none;
  }

  .topnav-menu .el-menu-item span,
  .topnav-menu .el-sub-menu__title span {
    display: none;
  }

  .topnav-menu.el-menu--horizontal > .el-menu-item,
  .topnav-menu.el-menu--horizontal > .el-sub-menu > .el-sub-menu__title {
    padding: 0 10px !important;
  }

  .topnav-menu .el-menu-item .el-icon,
  .topnav-menu .el-sub-menu__title .el-icon {
    margin-right: 0;
  }
}
</style>


<style scoped>
.studio-brandmark{display:grid;place-items:center;width:28px;height:28px;color:#fff;background:var(--brand-primary);border-radius:7px}.studio-brandmark svg{width:20px;height:20px}
</style>

<style>
.workspace-shell.app-shell{display:grid!important;grid-template-columns:222px minmax(0,1fr);height:100dvh;overflow:hidden;background:var(--studio-surface);transition:grid-template-columns .18s ease}
.workspace-nav{background:#f2f4ef;border-right:1px solid var(--studio-line);display:flex;flex-direction:column;padding:16px 11px 11px;min-height:0;min-width:0;z-index:45}
.workspace-brand-row{display:flex;align-items:center;min-height:40px;margin:0 4px 16px;gap:4px}
.workspace-nav .topnav-brand{justify-content:flex-start;padding:0 4px;gap:9px;min-width:0;flex:1}
.workspace-nav .topnav-brand-name{font-size:16px;font-weight:650;letter-spacing:-.6px;color:var(--studio-ink)}
.workspace-nav .topnav-brand-env{display:none}
.workspace-nav .studio-brandmark{width:27px;height:27px;background:var(--studio-action);border-radius:8px}
.nav-collapse-toggle{display:grid;place-items:center;width:27px;height:29px;border-radius:6px;color:var(--studio-muted);flex-shrink:0}
.nav-collapse-toggle:hover{background:#e6ebe2;color:var(--studio-ink)}
.nav-collapse-toggle svg{width:17px;height:17px;stroke:currentColor;stroke-width:1.4}
.workspace-search{display:flex;align-items:center;gap:9px;border:1px solid #dce2d7;background:#ffffffb3;color:#59665c;border-radius:8px;padding:9px 10px;font-size:13px;cursor:pointer;margin:0 3px 20px;text-align:left;box-shadow:none}
.workspace-search:hover{background:#fff;border-color:#b8c5b7}
.workspace-search kbd{margin-left:auto;color:#73806f;font:12px system-ui}
.workspace-nav-scroll{overflow:auto;min-height:0;flex:1;scrollbar-width:thin;scrollbar-color:transparent transparent}
.workspace-nav-scroll:hover{scrollbar-color:#cad3c6 transparent}
.workspace-nav-group{margin-bottom:20px}
.workspace-nav-group h2{font-size:12px;font-weight:500;color:#697566;margin:0;padding:3px 12px 7px;letter-spacing:.02em}
.workspace-nav-link{position:relative;display:flex;align-items:center;gap:10px;width:100%;text-align:left;background:none;border:0;padding:9px 12px;font-size:13px;color:#4c584f;cursor:pointer;border-radius:7px;min-height:37px;margin:2px 0;transition:background .15s,color .15s}
.workspace-nav-link:hover{background:#e9eee5;color:var(--studio-ink)}
.workspace-nav-link[aria-current=page]{background:#e5ede3;color:#244b37;font-weight:600;box-shadow:none}
.workspace-nav-link[aria-current=page]::before{content:'';position:absolute;left:0;top:11px;bottom:11px;width:3px;border-radius:3px;background:var(--studio-accent)}
.workspace-nav-link .el-icon{font-size:16px;color:#687665}
.workspace-nav-link[aria-current=page] .el-icon{color:var(--studio-accent)}
.workspace-nav .topnav-actions{margin:5px 0 0;padding-top:9px;border-top:1px solid #dce2d7;display:block}
.workspace-nav .topnav-user{width:100%}
.workspace-nav .topnav-user-chip{display:flex;gap:10px;width:100%;border:0!important;background:transparent!important;box-shadow:none!important;padding:9px!important;min-height:53px;border-radius:8px;justify-content:flex-start}
.workspace-nav .topnav-user-chip:hover,.workspace-nav .topnav-user-chip[aria-expanded=true]{background:#e5ebe0!important}
.workspace-nav .topnav-user-meta{flex:1;text-align:left;min-width:0;gap:4px}
.workspace-nav .topnav-user-avatar{width:31px;height:31px;background:#e1e8db;color:#3e5543;border:1px solid #ccd7c7;font-size:13px;border-radius:10px;box-shadow:none}
.workspace-nav .topnav-user-status{display:none}
.workspace-nav .topnav-user-name{font-size:13px;font-weight:550;color:var(--studio-ink)}
.workspace-nav .topnav-user-role{font-size:12px;color:#667160}
.account-menu-indicator{width:17px;height:17px;color:#63705f;flex:none}
.workspace-nav .topnav-user-chip[aria-expanded=true] .account-menu-indicator{color:var(--studio-accent)}
.workspace-nav .topnav-user-dropdown{top:auto!important;bottom:calc(100% + 10px);left:0;right:auto;width:248px;max-width:calc(100vw - 28px);background:#fff;border:1px solid var(--studio-line);box-shadow:0 14px 42px #24292e16,0 2px 7px #24292e07;border-radius:13px;padding:7px;z-index:70}
.account-menu-identity{display:flex;gap:11px;align-items:center;padding:12px 10px 15px;margin-bottom:6px;border-bottom:1px solid var(--border-light)}
.account-menu-identity>div{display:flex;flex-direction:column;gap:5px}
.workspace-nav .account-menu-identity strong{font-size:14px;font-weight:600;color:var(--studio-ink)}
.workspace-nav .account-menu-identity span{font-size:12px;color:var(--studio-muted)}
.workspace-nav .account-menu-identity .account-menu-avatar{display:grid;place-items:center;width:36px;height:36px;background:var(--studio-soft);border:1px solid #d8e2d5;border-radius:11px;color:var(--studio-accent);font-size:14px}
.workspace-nav .topnav-user-dropdown button{display:flex;flex-direction:row;align-items:center;gap:11px;border-radius:7px;padding:11px;min-height:40px;color:var(--text-body)}
.workspace-nav .topnav-user-dropdown button span{font-size:13px;color:inherit}
.workspace-nav .topnav-user-dropdown button .el-icon,.workspace-nav .topnav-user-dropdown button>svg{width:17px;height:17px;font-size:16px;color:var(--studio-muted)}
.workspace-nav .topnav-user-dropdown button:hover{background:#f0f4ed}
.workspace-nav .topnav-user-dropdown kbd{font:12px system-ui;color:#73806e;margin-left:auto}
.account-menu-separator{height:1px;background:var(--border-light);margin:6px}
.workspace-nav .topnav-user-dropdown button.danger{color:#a14743}
.workspace-nav .topnav-user-dropdown button.danger>svg{color:inherit}
.workspace-nav .topnav-user-dropdown button.danger:hover{background:#fcf1ef}
.workspace-shell .app-body{display:flex;flex-direction:column;min-height:0;min-width:0;overflow:hidden}
.workspace-bar{height:50px;min-height:50px;display:flex;align-items:center;justify-content:space-between;padding:0 30px;border-bottom:1px solid var(--studio-line);background:#fff;gap:12px}
.workspace-bar>div{display:flex;align-items:center;gap:12px;min-width:0}
.workspace-location{color:var(--studio-muted);font-size:12px}
.workspace-separator{color:#a4afa0;font-size:12px}
.workspace-bar strong{font-size:13px;font-weight:500;color:var(--studio-ink)}
.workspace-connection{display:flex;align-items:center;gap:7px;color:var(--studio-muted);font-size:12px;white-space:nowrap}
.workspace-connection i{width:6px;height:6px;border-radius:50%;background:#a4793f}
.workspace-connection i.online{background:var(--studio-accent)}
.workspace-shell .page-wrap{min-height:0;flex:1;padding:28px 32px;background:var(--studio-bg)}
.workspace-shell .page-wrap-smart{padding:0}
.workspace-shell .ax-page{height:100%;min-height:0}
.workspace-back{border:0;background:#fff;color:var(--studio-accent);text-align:left;font-size:13px;padding:11px 30px;cursor:pointer}
.shell-menu-toggle{display:none;border:0;background:none;color:var(--text-body);padding:7px}
.shell-nav-backdrop{display:none}
@media(min-width:901px){
  .workspace-shell.is-nav-collapsed{grid-template-columns:66px minmax(0,1fr)}
  .is-nav-collapsed .workspace-brand-row{flex-direction:column;gap:9px;margin-bottom:12px}
  .is-nav-collapsed .topnav-brand-name,.is-nav-collapsed .workspace-search span,.is-nav-collapsed .workspace-search kbd,.is-nav-collapsed .workspace-nav-link>span,.is-nav-collapsed .workspace-nav-group h2,.is-nav-collapsed .topnav-user-meta,.is-nav-collapsed .account-menu-indicator{display:none}
  .is-nav-collapsed .workspace-search{padding:9px;justify-content:center;margin:0 3px 15px}
  .is-nav-collapsed .workspace-nav-link{justify-content:center;padding:10px 0}
  .is-nav-collapsed .workspace-nav-group{margin-bottom:16px}
  .is-nav-collapsed .workspace-nav .topnav-user-chip{padding:7px 5px!important}
  .is-nav-collapsed .workspace-nav .topnav-user-dropdown{left:0}
}
@media(max-width:900px){
  .workspace-shell.app-shell{grid-template-columns:minmax(0,1fr)}
  .workspace-nav{display:none}
  .workspace-nav.is-open{display:flex;position:fixed;inset:0 auto 0 0;width:240px;box-shadow:20px 0 60px #24292e26}
  .nav-collapse-toggle{display:none}
  .shell-menu-toggle{display:inline-flex}
  .shell-nav-backdrop{display:block;position:fixed;inset:0;border:0;background:#24292e40;z-index:44}
  .workspace-bar{padding:0 16px}
  .workspace-shell .page-wrap{padding:22px 16px}
  .workspace-shell .page-wrap-smart{padding:0}
  .workspace-location,.workspace-separator{display:none}
}
@media(prefers-reduced-motion:reduce){.workspace-shell *{scroll-behavior:auto}.workspace-shell.app-shell,.workspace-nav-link{transition:none}}
</style>

```

---

## 智能体管线与技能管理 (src/views/AgentManagement.vue)

**文件路径**: `datapivot-demo/frontend/src/views/AgentManagement.vue`

```vue
<template>
  <div class="agent-page">
    <header class="expert-page-head"><div><span class="page-overline">协作配置</span><h1>专家协作</h1><p>定义每个角色的职责、执行指令与业务知识。</p></div><div class="expert-head-actions"><el-button @click="router.push('/advanced-capabilities?tab=skills')">技能与工具</el-button><el-button @click="router.push('/admin-console?tab=ask-flow')">流程策略</el-button></div></header>
    <div class="agent-workbench document-workbench">
      <aside class="agent-rail" aria-label="协作角色">
        <div class="agent-rail-head"><span>协作角色</span><small>{{ agents.length }}</small></div>
        <button v-for="item in agents" :key="item.agent_no" class="agent-card" :class="{active:selectedAgentNo===item.agent_no}" :aria-pressed="selectedAgentNo===item.agent_no" @click="selectAgent(item)">
          <span class="agent-card-no">{{ String(item.agent_no).padStart(2,'0') }}</span><span class="agent-card-copy"><strong>{{ roleNames[item.agent_no] || item.name }}</strong><small>{{ roleShort[item.agent_no] }}</small></span><span v-if="selectedAgentNo===item.agent_no" class="role-selected-dot"></span>
        </button>
        <div class="role-rail-note"><span class="rail-note-label">协作方式</span><p>主理人统筹任务<br>专家完成查询、核验与解读</p><details class="collaboration-map"><summary>查看两条执行路径</summary><div><span>普通问数</span><ol><li>识别范围与口径</li><li>生成查询并核验</li><li>解读结果与交付</li></ol></div><div><span>高阶研究</span><ol><li>规划取证方向</li><li>多分支并行验证</li><li>汇合证据与签收</li></ol></div></details></div>
      </aside>
      <section class="agent-editor">
        <header class="agent-editor-head"><div><span class="editor-overline">角色工作区</span><h2>{{ roleNames[selectedAgentNo] || '角色详情' }}</h2></div><el-button v-if="isFeatureEnabled('agent_config_edit')" type="primary" @click="saveAgent">保存配置</el-button></header>
        <GovernanceEmpty v-if="!selectedAgentNo" description="请选择一个协作角色" />
        <template v-else>
          <div class="role-execution-note"><span class="execution-indicator"></span><p>{{ roleBindings[selectedAgentNo] }}</p></div>
          <nav class="editor-section-tabs" aria-label="角色配置分区"><button v-for="item in editorSections" :key="item.key" :aria-pressed="editorTab===item.key" @click="editorTab=item.key">{{ item.label }}<span v-if="item.key==='knowledge'">{{ form.knowledge_base.length }}</span></button></nav>
          <div class="editor-content"><aside class="instruction-context" v-if="editorTab==='instructions'"><span>执行边界</span><h3>配置如何生效</h3><dl><div><dt>调用角色</dt><dd>{{ roleNames[selectedAgentNo] }}</dd></div><div><dt>应用范围</dt><dd>保存后用于后续新任务</dd></div><div><dt>安全约束</dt><dd>组织权限与查询安全由固定护栏校验，不能被指令覆盖。</dd></div><div><dt>检查方式</dt><dd>本地检查确认指令非空；不执行 SQL，也不调用模型。</dd></div></dl></aside>
            <section v-if="editorTab==='instructions'" class="instruction-section" :class="{ 'editor-expanded': editorExpanded }" @keydown.esc="editorExpanded = false"><div class="section-heading"><div><h3>执行指令</h3><p>此指令随该角色的模型调用读取，保存后用于后续新任务。</p></div><span class="text-count">{{ form.system_prompt.length.toLocaleString() }} 字符</span></div><div class="instruction-toolbar"><span>instruction.md</span><span>{{ promptLines }} 行 · ≈ {{ estimatedTokens }} tokens（估算）</span><div><el-button size="small" :disabled="!isFeatureEnabled('agent_config_edit')" @click="insertOutline">插入结构</el-button><el-button size="small" @click="validateInstruction">检查指令</el-button><el-button size="small" @click="editorExpanded = !editorExpanded">{{ editorExpanded ? '退出全屏' : '全屏编辑' }}</el-button></div></div><el-input :disabled="!isFeatureEnabled('agent_config_edit')" v-model="form.system_prompt" type="textarea" :rows="17" class="prompt-input" aria-label="系统提示词" /><div class="editor-footnote"><span>指令负责业务行为与输出要求。</span><span>权限与查询安全由固定护栏执行</span></div></section>
            <section v-else-if="editorTab==='knowledge'" class="knowledge-section"><div class="section-heading"><div><h3>业务知识</h3><p>补充该角色需要遵循的术语、口径和业务约束。</p></div><el-button v-if="isFeatureEnabled('agent_config_edit')" size="small" @click="addKnowledge">新增知识片段</el-button></div><div v-for="(item,index) in form.knowledge_base" :key="index" class="knowledge-item"><span class="knowledge-index">{{ String(index+1).padStart(2,'0') }}</span><el-input :disabled="!isFeatureEnabled('agent_config_edit')" v-model="form.knowledge_base[index]" type="textarea" :rows="3" :aria-label="`知识片段 ${index+1}`" /><el-button v-if="isFeatureEnabled('agent_config_edit')" link type="danger" @click="form.knowledge_base.splice(index,1)">删除</el-button></div><GovernanceEmpty v-if="!form.knowledge_base.length" description="暂无知识片段" :image-size="72" /></section>
            <section v-else class="profile-section"><div class="section-heading"><div><h3>角色资料</h3><p>维护展示名称与职责说明，角色的执行绑定保持一致。</p></div></div><label class="agent-field"><span>显示名称</span><el-input :disabled="!isFeatureEnabled('agent_config_edit')" v-model="form.name" /></label><label class="agent-field"><span>职责说明</span><el-input :disabled="!isFeatureEnabled('agent_config_edit')" v-model="form.role_summary" type="textarea" :rows="5" /></label></section>
          </div>
        </template>
      </section>
    </div>
  </div>
</template>

<script setup>
import GovernanceEmpty from "../components/GovernanceEmpty.vue"
import { computed, onMounted, reactive, ref, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { useRouter, useRoute } from 'vue-router'
import { getAgents, updateAgent } from '../api/index.js'
import { useFeatureFlags } from '../state/featureFlags.js'

const router = useRouter()
const pageRoute = useRoute()
const roleNames = {1:'主理人 · 路由与研究规划',2:'查询专家',3:'核验专家',4:'分析与报告专家'}
const roleBindings = {1:'普通：识别范围、路由与口径确认；高阶：形成研究计划并拆分取证方向。',2:'两条路径：依据字段、关联与金标样例生成查询，参与有界修复。',3:'两条路径：复核查询、字段与业务口径；执行前仍经过固定安全护栏。',4:'普通：解读核验结果；高阶：根据分支证据形成研究报告并接受复核。'}
const agents = ref([])
const selectedAgentNo = ref(null)
const editorTab = ref('instructions')
const editorSections = [{key:'instructions',label:'执行指令'},{key:'knowledge',label:'业务知识'},{key:'profile',label:'角色资料'}]
const roleShort = {1:'路由 · 规划 · 签收',2:'字段映射 · 查询生成',3:'口径复核 · 结果核验',4:'证据解读 · 报告交付'}
const { isFeatureEnabled, loadFeatureFlags } = useFeatureFlags()
const form = reactive({
  name: '',
  role_summary: '',
  system_prompt: '',
  knowledge_base: []
})

const editorExpanded = ref(false)
const promptLines = computed(() => form.system_prompt.split('\n').length)
const estimatedTokens = computed(() => Math.ceil([...form.system_prompt].reduce((n,c) => n + (/[^\x00-\x7F]/.test(c) ? 1 : 0.25), 0)))
const insertOutline = () => {
  form.system_prompt += '\n\n## 任务目标\n\n## 业务约束\n\n## 输出格式\n'
  ElMessage.info('已追加结构草稿，保存后才生效')
}
const validateInstruction = () => {
  if (!form.system_prompt.trim()) return ElMessage.warning('指令不能为空')
  ElMessage.success('本地检查通过：指令非空。此检查不会调用模型或执行查询。')
}
const applyAgent = (agent) => {
  selectedAgentNo.value = agent.agent_no
  form.name = /^Agent[1-4]\b/.test(agent.name || '') ? roleNames[agent.agent_no] : agent.name || roleNames[agent.agent_no] || ''
  form.role_summary = agent.role_summary || ''
  form.system_prompt = agent.system_prompt || ''
  form.knowledge_base = Array.isArray(agent.knowledge_base) ? [...agent.knowledge_base] : []
}

const loadAgents = async () => {
  const result = await getAgents()
  agents.value = result.agents || []
  if (!selectedAgentNo.value && agents.value.length > 0) {
    applyAgent(agents.value.find(item=>item.agent_no===Number(pageRoute.query.role)) || agents.value[0])
  }
}

const selectAgent = (agent) => {
  applyAgent(agent)
}

const addKnowledge = () => {
  form.knowledge_base.push('')
}

const saveAgent = async () => {
  if (!selectedAgentNo.value) return
  await updateAgent(selectedAgentNo.value, {
    name: form.name,
    role_summary: form.role_summary,
    system_prompt: form.system_prompt,
    knowledge_base: form.knowledge_base
  })
  ElMessage.success('角色配置已保存，对后续新任务生效')
  await loadAgents()
}

watch(()=>pageRoute.query.role, value=>{const role=agents.value.find(item=>item.agent_no===Number(value));if(role)applyAgent(role)})

onMounted(() => {
  loadFeatureFlags()
  loadAgents()
})
</script>
<style scoped>
.agent-page{color:#18222f;max-width:1600px;margin:0 auto;padding:4px 0 28px}.expert-page-head{display:flex;justify-content:space-between;align-items:center;gap:20px;padding:8px 0 26px}.page-overline,.editor-overline{display:block;color:#637184;font-size:11px;letter-spacing:.06em;margin-bottom:7px}.expert-page-head h1{font-size:25px;font-weight:600;letter-spacing:-.6px;margin:0}.expert-page-head p{font-size:13px;color:#687586;margin:8px 0 0}.expert-head-actions{display:flex;gap:8px}.expert-head-actions :deep(.el-button+.el-button){margin-left:0}.agent-workbench{display:grid;grid-template-columns:264px minmax(0,1fr);border:1px solid #e2e6eb;border-radius:12px;background:#fff;min-height:650px;overflow:hidden}.agent-rail{padding:22px 14px;background:#f9fafb;border-right:1px solid #e8ebef}.agent-rail-head{display:flex;justify-content:space-between;align-items:center;padding:0 12px 18px;color:#778292;font-size:12px}.agent-rail-head small{font-size:11px;border:1px solid #e2e6eb;border-radius:5px;padding:1px 6px}.agent-card{display:flex;gap:11px;align-items:center;width:100%;text-align:left;padding:15px 12px;border:1px solid #edf0f5;border-radius:10px;margin-bottom:14px;color:#465365;background:#ffffff;position:relative;transition:all .18s cubic-bezier(0.4, 0, 0.2, 1);box-shadow:0 1px 3px rgba(15,23,42,0.03)}.agent-card:hover{background:#fafbfd;border-color:#cbd5e1;transform:translateY(-1px)}.agent-card.active{background:#ffffff;border-color:#3b82f6;box-shadow:0 4px 14px rgba(37,99,235,0.09);outline:1px solid #3b82f6}.agent-card:not(:last-of-type)::after{content:'→';position:absolute;top:50%;right:-10px;transform:translateY(-50%);font-size:11px;color:#64748b;font-weight:700;line-height:1;pointer-events:none;z-index:5;background:#ffffff;border:1px solid #cbd5e1;border-radius:50%;width:18px;height:18px;display:flex;align-items:center;justify-content:center;box-shadow:0 1px 3px rgba(15,23,42,0.06)}.agent-card-no{font-size:11px;line-height:28px;text-align:center;border-radius:8px;width:30px;height:30px;flex-shrink:0;font-weight:700;font-variant-numeric:tabular-nums;transition:all .18s}.agent-card:nth-of-type(1) .agent-card-no{color:#2563eb;background:#eff6ff;border:1px solid #dbeafe}.agent-card:nth-of-type(2) .agent-card-no{color:#7c3aed;background:#f5f3ff;border:1px solid #ede9fe}.agent-card:nth-of-type(3) .agent-card-no{color:#d97706;background:#fffbeb;border:1px solid #fef3c7}.agent-card:nth-of-type(4) .agent-card-no{color:#059669;background:#ecfdf5;border:1px solid #d1fae5}.active .agent-card-no{box-shadow:0 2px 6px rgba(0,0,0,0.08)}.agent-card-copy{display:flex;min-width:0;flex:1;flex-direction:column;gap:5px}.agent-card-copy strong{font-size:13px;font-weight:600;color:#1e293b;line-height:1.4}.agent-card-copy small{font-size:11px;color:#64748b}.role-selected-dot{width:6px;height:6px;border-radius:50%;background:#2563eb;box-shadow:0 0 6px rgba(37,99,235,0.5)}.role-rail-note{margin:28px 8px 0;padding-top:18px;border-top:1px solid #e2e8f0}.rail-note-label{font-size:11px;font-weight:600;color:#64748b;letter-spacing:0.04em;text-transform:uppercase}.role-rail-note>p{font-size:12px;line-height:1.8;color:#475569;margin:8px 0 16px}.collaboration-map summary{font-size:12px;color:#2563eb;cursor:pointer;font-weight:500}.collaboration-map>div{padding-top:14px}.collaboration-map>div>span{font-size:11px;font-weight:600;color:#475569}.collaboration-map ol{margin:8px 0 0;padding-left:14px;list-style:decimal;font-size:11px;line-height:1.8;color:#64748b}.agent-editor{min-width:0}.agent-editor-head{display:flex;justify-content:space-between;align-items:center;gap:16px;padding:25px 30px 18px}.agent-editor-head h2{font-size:19px;font-weight:550;margin:0;letter-spacing:-.3px}.role-execution-note{display:flex;align-items:flex-start;gap:8px;padding:0 30px 23px}.execution-indicator{width:5px;height:5px;background:#8aa493;flex-shrink:0;border-radius:50%;margin-top:7px}.role-execution-note p{font-size:12px;line-height:1.8;color:#637184;margin:0}.editor-section-tabs{display:flex;gap:26px;padding:0 30px;border-bottom:1px solid #e7ebf0}.editor-section-tabs button{display:flex;align-items:center;gap:7px;color:#6b798b;font-size:12px;padding:0 0 13px;border-bottom:2px solid transparent}.editor-section-tabs button[aria-pressed=true]{color:#2e5079;border-color:#365f91}.editor-section-tabs span{padding:1px 5px;border-radius:4px;background:#f0f3f6;font-size:10px}.editor-content{padding:27px 30px 30px}.section-heading{display:flex;align-items:flex-start;justify-content:space-between;gap:16px;margin-bottom:20px}.section-heading h3{font-size:14px;font-weight:550;margin:0 0 7px}.section-heading p{color:#637184;font-size:12px;line-height:1.8;margin:0}.text-count{font-size:11px;color:#9aa3af;white-space:nowrap}.prompt-input :deep(textarea){background:#fbfcfd;font-family:'SFMono-Regular',Consolas,'PingFang SC',monospace;font-size:13px;line-height:1.9;padding:20px;box-shadow:0 0 0 1px #e5e9ee inset;color:#425169;border-radius:8px;resize:vertical}.editor-footnote{display:flex;justify-content:space-between;gap:12px;margin-top:12px;color:#8b96a4;font-size:11px;line-height:1.7}.knowledge-item{display:flex;gap:14px;align-items:flex-start;padding:18px 0;border-bottom:1px solid #edf0f3}.knowledge-index{font-size:11px;color:#96a0ac;padding-top:9px}.knowledge-item :deep(textarea){padding:12px;line-height:1.8}.agent-field{display:flex;flex-direction:column;gap:10px;font-size:12px;color:#566578;margin-bottom:24px;max-width:760px}.profile-section{min-height:420px}@media(max-width:1000px){.agent-workbench{grid-template-columns:220px minmax(0,1fr)}.expert-page-head{align-items:flex-start}.expert-head-actions{flex-wrap:wrap;justify-content:flex-end}.agent-editor-head,.editor-content{padding-left:22px;padding-right:22px}.role-execution-note,.editor-section-tabs{padding-left:22px;padding-right:22px}}@media(max-width:720px){.expert-page-head{flex-direction:column}.agent-workbench{grid-template-columns:1fr}.agent-rail{border-right:0;border-bottom:1px solid #e8ebef;display:grid;grid-template-columns:1fr 1fr;gap:4px;padding:12px}.agent-rail-head,.role-rail-note{display:none}.agent-card{margin:0}.agent-card-no{display:none}.agent-card-copy strong{font-size:11px}.agent-card-copy small{font-size:10px}.agent-editor-head h2{font-size:17px}.editor-footnote{flex-direction:column}.text-count{display:none}}
</style>

```

---

## 专家分析与技能呈现卡片 (src/components/askdesk/AnalysisBrief.vue)

**文件路径**: `datapivot-demo/frontend/src/components/askdesk/AnalysisBrief.vue`

```vue
<template>
  <section class="analysis-brief" :class="{compact}" aria-label="分析思路与依据">
    <header>
      <div>
        <span class="brief-eyebrow">本次执行</span>
        <h3>{{ compact ? '查询参数与依据' : '从问题到结果，有据可查' }}</h3>
      </div>
      <span class="brief-update">
        <i :class="{live:busy}"></i>{{ busy ? '流水线实时执行中' : '执行记录' }}
      </span>
    </header>
    <div class="brief-facts" aria-label="查询事实摘要">
      <article v-for="(fact,index) in facts" :key="fact.id" class="brief-fact" :class="[fact.status, `fact-${fact.id}`]" :data-fact="fact.id">
        <div class="fact-label">
          <span class="fact-idx">{{ String(index+1).padStart(2,'0') }}</span>
          <h4>{{ fact.label }}</h4>
          <small v-if="fact.status==='pending'" class="status-tag pending">
            <span v-if="busy" class="tag-pulse"></span>{{ busy ? stageLabel(fact.id) : '未记录' }}
          </small>
          <small v-else-if="fact.status==='warning'" class="status-tag warning">需关注</small>
          <small v-else class="status-tag confirmed">已就绪</small>
        </div>

        <p class="fact-value" :class="{'is-pending': fact.status === 'pending'}">
          {{ fact.status === 'pending' && busy ? stagePendingDesc(fact.id) : fact.value }}
        </p>

        <!-- 针对数据来源等结构化指标，提炼为精致胶囊 Chips，避免同名文字重复堆叠 -->
        <div v-if="chipsForFact(fact).length" class="fact-chips">
          <span v-for="(chip, i) in chipsForFact(fact)" :key="i" class="fact-chip">{{ chip }}</span>
        </div>

        <!-- 普通指标行（过滤掉与大字完全相同的多余重复标签） -->
        <dl v-else-if="cleanPreviewLines(fact).length" class="fact-preview">
          <div v-for="(line,i) in cleanPreviewLines(fact).slice(0,2)" :key="i">
            <dt v-if="shouldShowDt(line, fact)">{{ cleanLabel(line.label) }}</dt>
            <dd>{{ line.value }}</dd>
          </div>
        </dl>

        <details v-if="cleanPreviewLines(fact).length > 2" class="fact-detail">
          <summary>
            查看{{ fact.id==='results'?'字段与规模':fact.id==='sources'?'数据依据':'具体说明' }}
            <svg viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="m6 3 5 5-5 5" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"/></svg>
          </summary>
          <dl>
            <div v-for="(line,i) in cleanPreviewLines(fact).slice(2)" :key="i">
              <dt v-if="shouldShowDt(line, fact)">{{ cleanLabel(line.label) }}</dt>
              <dd>{{ line.value }}</dd>
            </div>
          </dl>
        </details>
      </article>
    </div>

    <details v-if="entries.length" class="brief-records">
      <summary>
        <span>执行记录与依据</span>
        <small>{{ entries.length }} 项记录</small>
        <svg viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="m6 3 5 5-5 5" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"/></svg>
      </summary>
      <ol>
        <li v-for="entry in entries" :key="entry.id">
          <span class="brief-marker" :class="entry.status"></span>
          <div>
            <strong>{{ entry.heading }}</strong>
            <dl>
              <div v-for="(line,index) in entry.lines" :key="index">
                <dt>{{ line.label }}</dt>
                <dd>{{ line.value }}</dd>
              </div>
            </dl>
          </div>
        </li>
      </ol>
    </details>
    <div v-if="busy && latest" class="brief-current" role="status">
      <span aria-hidden="true" class="pulse-beacon"></span>
      <p>{{ latest }}</p>
    </div>
  </section>
</template>

<script setup>
import { computed } from 'vue'
import { analysisActivity, analysisFacts, latestAnalysisSummary } from '../../utils/analysisActivity'

const props = defineProps({
  workflow: { type: Object, default: () => ({}) },
  result: Object,
  busy: Boolean,
  compact: Boolean
})

const entries = computed(() => analysisActivity(props.workflow, props.result))
const facts = computed(() => analysisFacts(props.workflow, props.result))
const latest = computed(() => latestAnalysisSummary(props.workflow))

// 阶段性状态标签，杜绝全部卡片机械重复“待返回”
const stageLabel = (id) => {
  const map = {
    plan: '待规划',
    aggregation: '待聚合',
    review: '待审核',
    results: '待执行'
  }
  return map[id] || '进行中'
}

// 处于待返回状态时提供明确的阶段感知提示，消除干瘪的“等待返回”
const stagePendingDesc = (id) => {
  const map = {
    plan: '正在由 Agent2 解析业务口径与查询方案...',
    aggregation: '等待查询逻辑生成后解析聚合度量...',
    review: '等待 Agent3 语法、安全与数据权限核验...',
    results: '等待底层数据库引擎执行返回结果集...'
  }
  return map[id] || '等待流水线流转返回...'
}

// 智能清洗 previewLines，彻底消除大字与小字完全一模一样的“套娃重复”
const cleanPreviewLines = (fact) => {
  return (fact.details || []).filter(line => {
    // 如果 line 的值本身就是 fact.value（大字），过滤掉
    if (line.value === fact.value) return false
    return true
  })
}

// 将“64 个字段定义 · 4 条表关联 · 5 个 SQL 参考样例”提炼为高科技现代 Chips
const chipsForFact = (fact) => {
  if (fact.id === 'sources' && fact.details?.length) {
    const countsLine = fact.details.find(d => d.value && d.value.includes('字段定义'))
    if (countsLine) {
      return countsLine.value.split('·').map(s => s.trim()).filter(Boolean)
    }
  }
  if (fact.id === 'scope' && fact.details?.length) {
    const timeLine = fact.details.find(d => d.label && d.label.includes('时间'))
    if (timeLine) {
      return [`时间范围: ${timeLine.value}`]
    }
  }
  return []
}

// 是否展示小标签 dt：如果 label 与上层大字或者卡片主题完全相同，则隐藏 dt
const shouldShowDt = (line, fact) => {
  if (!line.label) return false
  if (line.label === fact.value) return false
  if (line.label.includes(fact.value)) return false
  return true
}

// 移除“江城燃气·安全与管网治理 · 时间”这种冗长连缀，只保留纯粹的说明
const cleanLabel = (label) => {
  if (!label) return ''
  const parts = label.split('·').map(s => s.trim())
  return parts.length > 1 ? parts[parts.length - 1] : label
}
</script>

<style scoped>
.analysis-brief {
  --fact-ink: #0f172a;
  --fact-muted: #64748b;
  --fact-line: #e2e8f0;
  color: var(--fact-ink);
  padding: 22px 0 0;
  border-top: 1px solid var(--fact-line);
}
.analysis-brief > header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 20px;
}
.brief-eyebrow {
  display: inline-block;
  font: 600 10px/1 ui-monospace, SFMono-Regular, Menlo, monospace;
  letter-spacing: 0.08em;
  color: #2563eb;
  background: #eff6ff;
  border: 1px solid #dbeafe;
  padding: 2px 7px;
  border-radius: 4px;
  margin-bottom: 6px;
}
.analysis-brief h3 {
  font-size: 16px;
  letter-spacing: -0.3px;
  font-weight: 700;
  margin: 0;
  color: var(--fact-ink);
}
.brief-update {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  color: var(--fact-muted);
  white-space: nowrap;
}
.brief-update i {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #94a3b8;
}
.brief-update i.live {
  background: #10b981;
  box-shadow: 0 0 0 4px rgba(16, 185, 129, 0.15);
  animation: pulse-ring 2s infinite ease-in-out;
}

@keyframes pulse-ring {
  0%, 100% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.15); opacity: 0.8; }
}

.brief-facts {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  border: 1px solid var(--fact-line);
  border-radius: 12px;
  overflow: hidden;
  background: #ffffff;
  box-shadow: 0 1px 3px rgba(15, 23, 42, 0.03);
}
.brief-fact {
  min-width: 0;
  padding: 18px 20px;
  border-bottom: 1px solid var(--fact-line);
  background: #ffffff;
  transition: background-color 0.15s ease;
}
.brief-fact:hover {
  background: #fbfcfe;
}
.brief-fact:nth-child(odd) {
  border-right: 1px solid var(--fact-line);
}
.brief-fact:nth-last-child(-n+2) {
  border-bottom: 0;
}

.fact-label {
  display: flex;
  align-items: center;
  gap: 8px;
}
.fact-idx {
  font: 600 11px ui-monospace, SFMono-Regular, monospace;
  color: #3b82f6;
  background: #eff6ff;
  padding: 1px 6px;
  border-radius: 4px;
}
.fact-label h4 {
  font-size: 13px;
  font-weight: 600;
  color: #334155;
  margin: 0;
}

/* 状态 Badge */
.status-tag {
  margin-left: auto;
  font-size: 11px;
  font-weight: 500;
  padding: 2px 8px;
  border-radius: 12px;
  display: inline-flex;
  align-items: center;
  gap: 5px;
}
.status-tag.pending {
  color: #64748b;
  background: #f1f5f9;
}
.status-tag.confirmed {
  color: #065f46;
  background: #ecfdf5;
}
.status-tag.warning {
  color: #b45309;
  background: #fef3c7;
}
.tag-pulse {
  display: inline-block;
  width: 5px;
  height: 5px;
  border-radius: 50%;
  background: #3b82f6;
  animation: pulse-ring 1.5s infinite;
}

.fact-value {
  margin: 10px 0 0;
  font-size: 13px !important;
  line-height: 1.7;
  font-weight: 600;
  color: var(--fact-ink);
  overflow-wrap: anywhere;
  white-space: pre-line;
}
.fact-value.is-pending {
  color: #64748b;
  font-weight: 400;
  font-size: 12px !important;
  font-style: italic;
}

/* 现代高科技 Chips 胶囊 */
.fact-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-top: 10px;
}
.fact-chip {
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
  font-size: 11px;
  font-weight: 500;
  color: #1e40af;
  background: #eff6ff;
  border: 1px solid #dbeafe;
  padding: 2px 8px;
  border-radius: 6px;
}

.fact-preview {
  margin-top: 8px;
}
.fact-preview dt {
  font-size: 11px;
  color: var(--fact-muted);
}
.fact-preview dd {
  margin: 2px 0 0;
  font-size: 12px;
  color: #334155;
  overflow-wrap: anywhere;
}

.fact-detail {
  margin-top: 10px;
}
.fact-detail summary {
  display: flex;
  align-items: center;
  gap: 5px;
  cursor: pointer;
  list-style: none;
  font-size: 11px;
  color: #2563eb;
}
.fact-detail svg, .brief-records svg {
  width: 12px;
  height: 12px;
  transition: transform 0.15s;
}
.fact-detail[open] summary svg, .brief-records[open] > summary svg {
  transform: rotate(90deg);
}

.brief-records {
  margin-top: 16px;
}
.brief-records > summary {
  display: flex;
  align-items: center;
  gap: 10px;
  list-style: none;
  cursor: pointer;
  font-size: 12px;
  color: #475569;
  padding: 6px 0;
}
.brief-records summary small {
  font-size: 11px;
  color: #64748b;
  background: #f1f5f9;
  padding: 1px 7px;
  border-radius: 10px;
}

.analysis-brief ol {
  list-style: none;
  padding: 14px 0 4px;
  margin: 0;
  display: grid;
  gap: 16px;
}
.analysis-brief li {
  display: flex;
  gap: 12px;
  align-items: flex-start;
  min-width: 0;
}
.brief-marker {
  width: 7px;
  height: 7px;
  flex-shrink: 0;
  margin-top: 8px;
  border-radius: 50%;
  background: #94a3b8;
}
.brief-marker.completed {
  background: #10b981;
}
.brief-marker.warning, .brief-marker.failed {
  background: #f59e0b;
}

.brief-current {
  display: flex;
  gap: 10px;
  align-items: center;
  margin-top: 16px;
  padding: 10px 14px;
  border-radius: 8px;
  background: linear-gradient(135deg, #f0fdf4 0%, #eff6ff 100%);
  border: 1px solid #dbeafe;
}
.pulse-beacon {
  width: 6px;
  height: 6px;
  background: #2563eb;
  border-radius: 50%;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.2);
  animation: pulse-ring 2s infinite;
}
.brief-current p {
  font-size: 12px;
  color: #1e293b;
  margin: 0;
}

/* 抽屉紧凑模式 */
.compact {
  border-top: 0;
  padding-top: 0;
}
.compact > header {
  margin-bottom: 16px;
}
.compact h3 {
  font-size: 14px;
}
.compact .brief-eyebrow {
  display: none;
}
.compact .brief-facts {
  display: block;
  border: 0;
  border-radius: 0;
  box-shadow: none;
}
.compact .brief-fact {
  padding: 14px 0;
  border: 0;
  border-bottom: 1px solid var(--fact-line);
}
.compact .brief-fact:first-child {
  padding-top: 0;
}
.compact .brief-fact:last-child {
  border-bottom: 0;
}
</style>

```

---

## 数据集资产管理页面 (src/views/DatasetManagement.vue)

**文件路径**: `datapivot-demo/frontend/src/views/DatasetManagement.vue`

```vue
<template>
  <div class="module-layout-v4 dataset-page">
    <header class="dataset-page-heading">
      <div><span class="dataset-eyebrow">数据资产 / DATASETS</span><h1>数据集</h1><p>连接业务口径、数据模型与问数知识。</p></div>
      <div class="header-actions">
        <el-button v-if="isFeatureEnabled('dataset_prompt_generate')" plain @click="openPromptDatasetDialog">从业务描述生成</el-button>
        <el-button v-if="isFeatureEnabled('dataset_create')" type="primary" @click="createDataset">新建数据集</el-button>
      </div>
    </header>
    <div class="dataset-workspace">
      <aside class="dataset-catalog" aria-label="数据集目录">
        <div class="catalog-heading"><strong>资产目录</strong><span>{{ datasetStatusCounts.all }}</span></div>
        <div class="toolbar-col">
          <el-input v-model="searchKeyword" clearable placeholder="搜索名称或编码" aria-label="搜索数据集" />
          <div class="dataset-status-filter" role="group" aria-label="数据集状态筛选">
            <button v-for="filter in [{key:'all',label:'全部'},{key:'active',label:'启用'},{key:'inactive',label:'停用'}]" :key="filter.key" type="button" :aria-pressed="listStatusFilter === filter.key" @click="listStatusFilter=filter.key">{{ filter.label }}<span>{{ datasetStatusCounts[filter.key] }}</span></button>
          </div>
          <el-select v-model="listFilterSourceId" clearable placeholder="所有数据来源" size="small" aria-label="按数据来源筛选">
            <el-option label="全部来源" value="" />
            <el-option v-for="source in dataSources" :key="source.id" :label="source.name" :value="source.id" />
          </el-select>
        </div>
        <div class="dataset-catalog-list" v-loading="datasetsLoading">
          <button v-for="item in filteredDatasets" :key="item.id" type="button" class="dataset-tile" :class="{active:selectedDatasetId===item.id,inactive:item.is_active===false}" :aria-pressed="selectedDatasetId===item.id" @click="onSelectDataset(item)">
            <span class="dataset-tile-head"><span class="dataset-asset-icon" aria-hidden="true"><svg viewBox="0 0 20 20" fill="none"><rect x="3" y="3" width="14" height="14" rx="3" stroke="currentColor"/><path d="M3 8h14M8 8v9" stroke="currentColor"/></svg></span><span class="dataset-tile-title">{{ item.dataset_name || '未命名数据集' }}</span></span>
            <span class="dataset-tile-meta">{{ item.dataset_code }}</span>
            <span class="dataset-tile-sub"><span class="asset-state" :class="{inactive:item.is_active===false}">{{ item.is_active===false?'已停用':'已启用' }}</span><span>{{ item.dataset_readonly?'只读':item.can_edit?'可维护':'' }}</span><span>{{ item.golden_sql_count || 0 }} 个 SQL 样例</span></span>
          </button>
          <el-empty v-if="!datasetsLoading && filteredDatasets.length===0" description="没有匹配的数据集" :image-size="60" />
        </div>
        <div class="catalog-footnote">数据范围与维护权限由组织策略控制</div>
      </aside>
      <main class="dataset-editor">
        <header class="dataset-identity">
          <div class="dataset-identity-copy"><div class="dataset-identity-line"><span class="dataset-eyebrow">{{ datasetForm.dataset_code || 'ASSET WORKSPACE' }}</span><span v-if="selectedDatasetId" class="asset-state" :class="{inactive:datasetForm.is_active===false}">{{ datasetForm.is_active===false?'已停用':'已启用' }}</span><span v-if="isDirty" class="dirty-indicator">未保存</span></div><h2>{{ datasetForm.dataset_name || '选择一个数据集' }}</h2><div v-if="selectedDatasetId" class="dataset-identity-meta"><span>{{ datasetForm.business_domain || '未设置业务域' }}</span><i></i><span>{{ sourceNameById(datasetForm.source_id) }}</span><i></i><span>{{ full.schema_definition.length }} 张表 · {{ full.data_dictionary.length }} 个字段</span></div></div>
          <div class="header-actions">
            <el-button v-if="isFeatureEnabled('dataset_autofill')" plain :disabled="!selectedDatasetId || !selectedCanEdit" @click="autofillSelectedDataset">智能补齐</el-button>
            <el-button v-if="canSaveShelfContent" type="primary" :disabled="!isDirty || !canSaveShelfContent" @click="saveFull">保存修改</el-button>
          </div>
        </header>
        <div class="dataset-editor-body">
          <el-empty v-if="!selectedDatasetId" description="请选择一个数据集后开始维护。" />
          <template v-else>
            <el-alert
              v-if="selectedDatasetReadonly"
              :title="readonlyAlertTitle"
              type="warning"
              :closable="false"
              show-icon
              class="readonly-alert"
            />
            <details :key="selectedDatasetId" class="dataset-properties">
              <summary><span>基础属性</span><span class="properties-summary">名称、来源与启用状态</span><svg viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="m6 3 5 5-5 5" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"/></svg></summary>
              <div class="dataset-properties-body">
                <el-form label-position="top" class="base-form" :disabled="!selectedCanEdit">
                  <el-form-item label="数据集编码"><el-input v-model="datasetForm.dataset_code" @input="markDirty" /></el-form-item>
                  <el-form-item label="数据集名称"><el-input v-model="datasetForm.dataset_name" @input="markDirty" /></el-form-item>
                  <el-form-item label="业务域"><el-input v-model="datasetForm.business_domain" @input="markDirty" /></el-form-item>
                  <el-form-item label="默认数据来源"><el-select v-model="datasetForm.source_id" clearable style="width:100%" @change="markDirty"><el-option v-for="source in dataSources" :key="source.id" :label="source.name" :value="source.id" /></el-select></el-form-item>
                  <el-form-item label="描述" class="property-description"><el-input v-model="datasetForm.description" @input="markDirty" /></el-form-item>
                  <el-form-item label="参与问数"><el-switch v-model="datasetForm.is_active" @change="markDirty" /><span class="property-switch-note">{{ datasetForm.is_active?'启用':'停用' }}</span></el-form-item>
                </el-form>
                <div class="property-danger"><span>删除后，关联的知识配置将一并移除。</span><el-button v-if="isFeatureEnabled('dataset_delete')" type="danger" link @click="removeDataset" :disabled="!selectedCanDelete">删除数据集</el-button></div>
              </div>
            </details>
            <details v-if="qualitySummary && canViewDatasetShelfDetails" class="quality-disclosure">
              <summary><span class="quality-score">{{ qualitySummary.score }}<small>/100</small></span><div class="quality-summary-copy"><strong>知识完整性<span>{{ qualitySummary.label }}</span></strong><span>{{ qualitySummary.gaps?.length?`${qualitySummary.gaps.length} 项内容待完善`:'当前配置已覆盖主要问数知识' }}</span></div><div class="quality-track" aria-hidden="true"><i :style="{width:`${qualitySummary.score}%`}"></i></div><span class="quality-detail-label">查看检查项</span><svg viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="m6 3 5 5-5 5" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"/></svg></summary>
              <div class="quality-overview"><div class="quality-checks"><span v-for="item in qualitySummary.checks" :key="item.key" class="quality-check"><span>{{ item.label }}</span><strong>{{ item.score }}<small>/{{ item.max_score }}</small></strong></span></div><div v-if="qualitySummary.gaps?.length" class="quality-gaps"><div v-for="(gap,index) in qualitySummary.gaps" :key="index">{{ gap }}</div></div></div>
            </details>

            <div v-if="!canViewDatasetShelfDetails" class="readonly-summary-card">
              <div class="readonly-summary-title">当前账号仅开放数据集基础信息</div>
              <div class="readonly-summary-desc">
                书架维护内容、训练样例、DDL 和 专家提示词仅对有维护权限的账号展示；SQL 调试请到智能问数首页使用调试台。
              </div>
              <div class="readonly-summary-grid">
                <div>
                  <span>数据集</span>
                  <strong>{{ datasetForm.dataset_name || '-' }}</strong>
                </div>
                <div>
                  <span>编码</span>
                  <strong>{{ datasetForm.dataset_code || '-' }}</strong>
                </div>
                <div>
                  <span>业务域</span>
                  <strong>{{ datasetForm.business_domain || '-' }}</strong>
                </div>
                <div>
                  <span>状态</span>
                  <strong>{{ datasetForm.is_active === false ? '停用' : '启用' }}</strong>
                </div>
              </div>
            </div>

            <section v-else class="knowledge-workspace">
              <div class="knowledge-category-nav" role="group" aria-label="知识资产分类"><button v-for="group in assetGroups" :key="group.id" type="button" :aria-pressed="activeAssetGroup.id===group.id" @click="activeTab=group.items[0].key">{{ group.label }}<span>{{ group.items.length }}</span></button></div>
              <nav class="knowledge-section-nav" aria-label="知识配置分区"><button v-for="item in activeAssetGroup.items" :key="item.key" type="button" :aria-current="activeTab===item.key?'page':undefined" @click="activeTab=item.key">{{ item.label }}<span>{{ assetCount(item.key) }}</span></button></nav>
              <div class="knowledge-section-intro"><div><h3>{{ activeAssetSection.label }}</h3><p>{{ activeAssetSection.description }}</p></div><span>{{ assetCount(activeTab) }} 项配置</span></div>
              <el-tabs v-model="activeTab" class="knowledge-content-tabs">
              <!-- 常见问题 -->
              <el-tab-pane label="常见问题" name="common_questions">
                <div v-if="canUseDatasetAction('question', 'create')" class="toolbar"><el-button size="small" @click="openItemEditor('question', -1)">新增常见问题</el-button></div>
                <el-table :data="full.common_questions" border size="small">
                  <el-table-column label="问题" min-width="300"><template #default="{ row }">{{ row.question_text || '(空)' }}</template></el-table-column>
                  <el-table-column label="排序" width="80"><template #default="{ row }">{{ row.sort_order }}</template></el-table-column>
                  <el-table-column label="操作" width="130">
                    <template #default="{ $index }">
                      <el-button v-if="canUseDatasetAction('question', 'update')" link type="primary" @click="openItemEditor('question', $index)">编辑</el-button>
                      <el-button v-if="canUseDatasetAction('question', 'delete')" link type="danger" @click="deleteCollectionItem('question', $index)">删除</el-button>
                    </template>
                  </el-table-column>
                </el-table>
              </el-tab-pane>

              <el-tab-pane label="标准题集" name="regression_cases">
                <div v-if="canUseDatasetAction('regression', 'create')" class="toolbar"><el-button size="small" @click="openItemEditor('regression', -1)">新增回归题</el-button></div>
                <el-table :data="full.regression_cases" border size="small">
                  <el-table-column label="类型" width="110"><template #default="{ row }">{{ row.case_type }}</template></el-table-column>
                  <el-table-column label="问题" min-width="260"><template #default="{ row }">{{ row.question_text || '(空)' }}</template></el-table-column>
                  <el-table-column label="预期焦点" min-width="260"><template #default="{ row }">{{ row.expected_focus || '-' }}</template></el-table-column>
                  <el-table-column label="执行预期" width="120"><template #default="{ row }">{{ row.expected_intent || '-' }}</template></el-table-column>
                  <el-table-column label="操作" width="130">
                    <template #default="{ $index }">
                      <el-button v-if="canUseDatasetAction('regression', 'update')" link type="primary" @click="openItemEditor('regression', $index)">编辑</el-button>
                      <el-button v-if="canUseDatasetAction('regression', 'delete')" link type="danger" @click="deleteCollectionItem('regression', $index)">删除</el-button>
                    </template>
                  </el-table-column>
                </el-table>
              </el-tab-pane>

              <!-- 路由词/别名 -->
              <el-tab-pane label="路由词/别名" name="synonyms">
                <div v-if="canUseDatasetAction('synonym', 'create')" class="toolbar"><el-button size="small" @click="openItemEditor('synonym', -1)">新增路由词</el-button></div>
                <el-table :data="full.synonyms" border size="small">
                  <el-table-column label="同义词" min-width="180"><template #default="{ row }">{{ row.synonym }}</template></el-table-column>
                  <el-table-column label="归一词" min-width="180"><template #default="{ row }">{{ row.normalized_synonym }}</template></el-table-column>
                  <el-table-column label="权重" width="80"><template #default="{ row }">{{ row.weight }}</template></el-table-column>
                  <el-table-column label="操作" width="130">
                    <template #default="{ $index }">
                      <el-button v-if="canUseDatasetAction('synonym', 'update')" link type="primary" @click="openItemEditor('synonym', $index)">编辑</el-button>
                      <el-button v-if="canUseDatasetAction('synonym', 'delete')" link type="danger" @click="deleteCollectionItem('synonym', $index)">删除</el-button>
                    </template>
                  </el-table-column>
                </el-table>
              </el-tab-pane>

              <!-- LLD 文档 -->
              <el-tab-pane label="LLD 文档" name="lld">
                <div v-if="canUseDatasetAction('lld', 'create')" class="toolbar"><el-button size="small" @click="openItemEditor('lld', -1)">新增 LLD</el-button></div>
                <el-table :data="full.lld_documents" border size="small">
                  <el-table-column label="版本" width="80"><template #default="{ row }">v{{ row.version }}</template></el-table-column>
                  <el-table-column label="标题" min-width="200"><template #default="{ row }">{{ row.title || '(未命名)' }}</template></el-table-column>
                  <el-table-column label="内容预览" min-width="300"><template #default="{ row }"><div class="text-preview">{{ (row.content || '').slice(0, 80) || '(空)' }}</div></template></el-table-column>
                  <el-table-column label="操作" width="130">
                    <template #default="{ $index }">
                      <el-button v-if="canUseDatasetAction('lld', 'update')" link type="primary" @click="openItemEditor('lld', $index)">编辑</el-button>
                      <el-button v-if="canUseDatasetAction('lld', 'delete')" link type="danger" @click="deleteCollectionItem('lld', $index)">删除</el-button>
                    </template>
                  </el-table-column>
                </el-table>
              </el-tab-pane>

              <!-- 数据字典 -->
              <el-tab-pane label="数据字典" name="dictionary">
                <div class="toolbar">
                  <el-button v-if="canUseDatasetAction('dict', 'create')" size="small" @click="openItemEditor('dict', -1)">新增字段</el-button>
                  <el-button v-if="canUseDatasetFeature('dataset_dict_extract')" size="small" type="success" @click="extractDictFromDDL">从 DDL 提取字段</el-button>
                  <el-button v-if="canUseDatasetFeature('dataset_dict_extract')" size="small" type="primary" :loading="pgDictLoading" @click="extractDictFromPg">从 PG 提取 fields</el-button>
                  <el-button v-if="canUseDatasetAction('dict', 'delete')" size="small" type="danger" plain @click="clearDictionary">清空字段</el-button>
                </div>
                <el-table :data="full.data_dictionary" border size="small">
                  <el-table-column label="表名" min-width="160"><template #default="{ row }">{{ row.table_name }}</template></el-table-column>
                  <el-table-column label="字段" min-width="140"><template #default="{ row }">{{ row.column_name }}</template></el-table-column>
                  <el-table-column label="JSONB Key" min-width="120"><template #default="{ row }">{{ row.jsonb_key || '-' }}</template></el-table-column>
                  <el-table-column label="语义名" min-width="140"><template #default="{ row }">{{ row.semantic_name || '-' }}</template></el-table-column>
                  <el-table-column label="操作" width="130">
                    <template #default="{ $index }">
                      <el-button v-if="canUseDatasetAction('dict', 'update')" link type="primary" @click="openItemEditor('dict', $index)">编辑</el-button>
                      <el-button v-if="canUseDatasetAction('dict', 'delete')" link type="danger" @click="deleteCollectionItem('dict', $index)">删除</el-button>
                    </template>
                  </el-table-column>
                </el-table>
              </el-tab-pane>

              <!-- DDL + 表关联 (保留原始交互方式，已有 Drawer) -->
              <el-tab-pane label="DDL + 表关联" name="schema">
                <div class="toolbar">
                  <el-button v-if="canUseDatasetFeature('dataset_source_table')" size="small" @click="openSourceTableDialog">从数据源拉表</el-button>
                  <el-button v-if="canUseDatasetFeature('dataset_schema_create')" size="small" @click="addSchema">新增DDL</el-button>
                  <el-button v-if="canUseDatasetAction('relation', 'create')" size="small" @click="openItemEditor('relation', -1)">新增关联</el-button>
                </div>
                <div class="section-title">表清单和 DDL</div>
                <el-table :data="full.schema_definition" border size="small">
                  <el-table-column label="来源" width="140"><template #default="{ row }"><el-tag effect="plain" size="small">{{ sourceNameById(row.source_id) }}</el-tag></template></el-table-column>
                  <el-table-column label="表名" width="200"><template #default="{ row }"><span class="schema-name-cell">{{ row.table_name || '未命名表' }}</span></template></el-table-column>
                  <el-table-column label="DDL 预览" min-width="300"><template #default="{ row }"><div class="ddl-preview-line">{{ ddlPreview(row.ddl_sql) }}</div></template></el-table-column>
                  <el-table-column label="操作" width="130">
                    <template #default="{ row, $index }">
                      <el-button v-if="canUseDatasetFeature('dataset_schema_update')" link type="primary" @click="openSchemaEditor(row, $index)">编辑</el-button>
                      <el-button v-if="canUseDatasetFeature('dataset_schema_delete')" link type="danger" @click="removeSchema($index)">删除</el-button>
                    </template>
                  </el-table-column>
                </el-table>
                <div class="section-title">表关联</div>
                <el-table :data="full.table_relations" border size="small">
                  <el-table-column label="左表"><template #default="{ row }">{{ row.left_table }}</template></el-table-column>
                  <el-table-column label="左键"><template #default="{ row }">{{ row.left_key }}</template></el-table-column>
                  <el-table-column label="右表"><template #default="{ row }">{{ row.right_table }}</template></el-table-column>
                  <el-table-column label="右键"><template #default="{ row }">{{ row.right_key }}</template></el-table-column>
                  <el-table-column label="类型" width="100"><template #default="{ row }">{{ row.relation_type }}</template></el-table-column>
                  <el-table-column label="操作" width="130">
                    <template #default="{ $index }">
                      <el-button v-if="canUseDatasetAction('relation', 'update')" link type="primary" @click="openItemEditor('relation', $index)">编辑</el-button>
                      <el-button v-if="canUseDatasetAction('relation', 'delete')" link type="danger" @click="deleteCollectionItem('relation', $index)">删除</el-button>
                    </template>
                  </el-table-column>
                </el-table>
              </el-tab-pane>

              <!-- Golden SQL -->
              <el-tab-pane label="Golden SQL" name="golden">
                <div v-if="canUseDatasetAction('golden', 'create')" class="toolbar"><el-button size="small" @click="openItemEditor('golden', -1)">新增训练实例</el-button></div>
                <el-table :data="full.golden_sql_samples" border size="small">
                  <el-table-column label="Intent" width="100"><template #default="{ row }">{{ row.intent_type }}</template></el-table-column>
                  <el-table-column label="问题" min-width="260"><template #default="{ row }">{{ row.question || '(空)' }}</template></el-table-column>
                  <el-table-column label="SQL 预览" min-width="280"><template #default="{ row }"><div class="ddl-preview-line">{{ (row.sql_text || '').slice(0, 100) || '(空)' }}</div></template></el-table-column>
                  <el-table-column label="分数" width="70"><template #default="{ row }">{{ row.quality_score }}</template></el-table-column>
                  <el-table-column label="操作" width="130">
                    <template #default="{ $index }">
                      <el-button v-if="canUseDatasetAction('golden', 'update')" link type="primary" @click="openItemEditor('golden', $index)">编辑</el-button>
                      <el-button v-if="canUseDatasetAction('golden', 'delete')" link type="danger" @click="deleteCollectionItem('golden', $index)">删除</el-button>
                    </template>
                  </el-table-column>
                </el-table>
              </el-tab-pane>

              <!-- 专家提示片段 -->
              <el-tab-pane label="专家提示片段" name="prompts">
                <div v-if="canUseDatasetAction('prompt', 'create')" class="toolbar"><el-button size="small" @click="openItemEditor('prompt', -1)">新增片段</el-button></div>
                <el-table :data="full.agent_prompts" border size="small">
                  <el-table-column label="协作角色" width="140"><template #default="{ row }">{{ {1:'主理人',2:'查询专家',3:'核验专家',4:'分析与报告专家'}[row.agent_no] || `角色 ${row.agent_no}` }}</template></el-table-column>
                  <el-table-column label="Key" width="150"><template #default="{ row }">{{ row.prompt_key }}</template></el-table-column>
                  <el-table-column label="内容预览" min-width="300"><template #default="{ row }"><div class="text-preview">{{ (row.prompt_content || '').slice(0, 120) || '(空)' }}</div></template></el-table-column>
                  <el-table-column label="操作" width="130">
                    <template #default="{ $index }">
                      <el-button v-if="canUseDatasetAction('prompt', 'update')" link type="primary" @click="openItemEditor('prompt', $index)">编辑</el-button>
                      <el-button v-if="canUseDatasetAction('prompt', 'delete')" link type="danger" @click="deleteCollectionItem('prompt', $index)">删除</el-button>
                    </template>
                  </el-table-column>
                </el-table>
              </el-tab-pane>

              <!-- 外部配置 -->
              <el-tab-pane label="飞书/外部配置" name="external">
                <div v-if="canUseDatasetAction('extcfg', 'create')" class="toolbar"><el-button size="small" @click="openItemEditor('extcfg', -1)">新增配置</el-button></div>
                <el-table :data="full.external_configs" border size="small">
                  <el-table-column label="类型" width="140"><template #default="{ row }">{{ row.config_type }}</template></el-table-column>
                  <el-table-column label="Key" width="200"><template #default="{ row }">{{ row.config_key }}</template></el-table-column>
                  <el-table-column label="配置预览" min-width="300"><template #default="{ row }"><div class="text-preview">{{ jsonString(row.config_value).slice(0, 100) }}</div></template></el-table-column>
                  <el-table-column label="操作" width="130">
                    <template #default="{ $index }">
                      <el-button v-if="canUseDatasetAction('extcfg', 'update')" link type="primary" @click="openItemEditor('extcfg', $index)">编辑</el-button>
                      <el-button v-if="canUseDatasetAction('extcfg', 'delete')" link type="danger" @click="deleteCollectionItem('extcfg', $index)">删除</el-button>
                    </template>
                  </el-table-column>
                </el-table>
              </el-tab-pane>

              <!-- 数据转换 -->
              <el-tab-pane label="数据转换" name="transforms">
                <div class="toolbar">
                  <el-button
                    v-if="isFeatureEnabled('dataset_transform_edit') && selectedCanEdit"
                    size="small"
                    type="primary"
                    @click="openTransformEditor()"
                  >新增转换任务</el-button>
                  <el-button size="small" @click="loadTransforms" :loading="transformLoading">刷新</el-button>
                </div>
                <el-table :data="transforms" border size="small" v-loading="transformLoading">
                  <el-table-column label="任务名称" min-width="160">
                    <template #default="{ row }">{{ row.name }}</template>
                  </el-table-column>
                  <el-table-column label="源表 → 目标" min-width="220">
                    <template #default="{ row }">
                      <div>{{ row.source_table }} →</div>
                      <div><el-tag size="small" effect="plain">{{ row.target_type }}</el-tag> {{ row.target_name }}</div>
                    </template>
                  </el-table-column>
                  <el-table-column label="自动执行" width="90">
                    <template #default="{ row }">{{ row.auto_run_on_sync ? '是' : '否' }}</template>
                  </el-table-column>
                  <el-table-column label="状态" width="140">
                    <template #default="{ row }">
                      <div v-if="row.last_run_status">
                        <el-tag :type="row.last_run_status === 'success' ? 'success' : 'danger'" size="small" effect="light">{{ row.last_run_status }}</el-tag>
                        <div class="text-muted" style="font-size: 11px;">{{ formatTime(row.last_run_at) }}</div>
                      </div>
                      <span v-else class="text-muted">尚未执行</span>
                    </template>
                  </el-table-column>
                  <el-table-column label="操作" width="180" fixed="right">
                    <template #default="{ row }">
                      <el-button link type="primary" size="small" :loading="transformRunLoading[row.id]" @click="handleRunTransform(row)">执行</el-button>
                      <el-button v-if="isFeatureEnabled('dataset_transform_edit') && selectedCanEdit" link type="primary" size="small" @click="openTransformEditor(row)">编辑</el-button>
                      <el-button v-if="isFeatureEnabled('dataset_transform_edit') && selectedCanEdit" link type="danger" size="small" @click="handleDeleteTransform(row)">删除</el-button>
                    </template>
                  </el-table-column>
                </el-table>
              </el-tab-pane>
              </el-tabs>
            </section>
          </template>
        </div>
      </main>
    </div>

    <!-- ========== 通用编辑弹窗 ========== -->
    <el-dialog v-model="itemEditorVisible" :title="itemEditorTitle" width="680px" destroy-on-close top="6vh">
      <!-- 常见问题编辑 -->
      <el-form v-if="itemEditorType === 'question'" label-width="80px">
        <el-form-item label="问题"><el-input v-model="itemDraft.question_text" placeholder="输入常见问题文本" /></el-form-item>
        <el-form-item label="排序"><el-input-number v-model="itemDraft.sort_order" :min="1" :max="9999" /></el-form-item>
      </el-form>

      <el-form v-if="itemEditorType === 'regression'" label-width="90px">
        <el-row :gutter="12">
          <el-col :span="12">
            <el-form-item label="题型">
              <el-select v-model="itemDraft.case_type" style="width:100%">
                <el-option value="detail" label="明细题" />
                <el-option value="summary" label="汇总题" />
                <el-option value="trend" label="趋势题" />
                <el-option value="confirmation" label="口径确认题" />
                <el-option value="cross_dataset" label="跨数据集题" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12"><el-form-item label="排序"><el-input-number v-model="itemDraft.sort_order" :min="1" :max="9999" style="width:100%" /></el-form-item></el-col>
        </el-row>
        <el-form-item label="问题"><el-input v-model="itemDraft.question_text" placeholder="输入标准回归题" /></el-form-item>
        <el-form-item label="预期焦点">
          <el-input v-model="itemDraft.expected_focus" type="textarea" :rows="4" resize="vertical" placeholder="例如：应命中磐石事业群数据集；应先触发组织口径确认；结果应包含月度趋势。" />
        </el-form-item>
        <el-form-item label="执行预期">
          <el-select v-model="itemDraft.expected_intent" style="width:100%">
            <el-option value="direct_execute" label="直接执行" />
            <el-option value="generate_sql" label="生成 SQL" />
            <el-option value="requires_confirmation" label="需要确认" />
          </el-select>
        </el-form-item>
      </el-form>

      <!-- 同义词编辑 -->
      <el-form v-if="itemEditorType === 'synonym'" label-width="80px">
        <el-form-item label="同义词"><el-input v-model="itemDraft.synonym" /></el-form-item>
        <el-form-item label="归一词"><el-input v-model="itemDraft.normalized_synonym" /></el-form-item>
        <el-form-item label="权重"><el-input-number v-model="itemDraft.weight" :min="1" :max="10" /></el-form-item>
      </el-form>

      <!-- LLD 编辑 -->
      <el-form v-if="itemEditorType === 'lld'" label-width="80px">
        <el-row :gutter="12">
          <el-col :span="8"><el-form-item label="版本"><el-input-number v-model="itemDraft.version" :min="1" style="width:100%" /></el-form-item></el-col>
          <el-col :span="16"><el-form-item label="标题"><el-input v-model="itemDraft.title" /></el-form-item></el-col>
        </el-row>
        <el-form-item label="内容">
          <el-input v-model="itemDraft.content" type="textarea" :rows="18" resize="vertical" placeholder="业务逻辑、红线、隔离规则..." class="mono-textarea" />
        </el-form-item>
      </el-form>

      <!-- 数据字典编辑 -->
      <el-form v-if="itemEditorType === 'dict'" label-width="90px">
        <el-row :gutter="12">
          <el-col :span="12"><el-form-item label="表名"><el-input v-model="itemDraft.table_name" /></el-form-item></el-col>
          <el-col :span="12"><el-form-item label="字段名"><el-input v-model="itemDraft.column_name" /></el-form-item></el-col>
        </el-row>
        <el-row :gutter="12">
          <el-col :span="12"><el-form-item label="JSONB Key"><el-input v-model="itemDraft.jsonb_key" /></el-form-item></el-col>
          <el-col :span="12"><el-form-item label="语义名"><el-input v-model="itemDraft.semantic_name" /></el-form-item></el-col>
        </el-row>
      </el-form>

      <!-- 表关联编辑 -->
      <el-form v-if="itemEditorType === 'relation'" label-width="80px">
        <el-row :gutter="12">
          <el-col :span="12"><el-form-item label="左表"><el-input v-model="itemDraft.left_table" /></el-form-item></el-col>
          <el-col :span="12"><el-form-item label="左键"><el-input v-model="itemDraft.left_key" /></el-form-item></el-col>
        </el-row>
        <el-row :gutter="12">
          <el-col :span="12"><el-form-item label="右表"><el-input v-model="itemDraft.right_table" /></el-form-item></el-col>
          <el-col :span="12"><el-form-item label="右键"><el-input v-model="itemDraft.right_key" /></el-form-item></el-col>
        </el-row>
        <el-form-item label="关联类型"><el-input v-model="itemDraft.relation_type" placeholder="inner / left / right" /></el-form-item>
      </el-form>

      <!-- Golden SQL 编辑 -->
      <el-form v-if="itemEditorType === 'golden'" label-width="90px">
        <el-row :gutter="12">
          <el-col :span="12"><el-form-item label="Intent"><el-input v-model="itemDraft.intent_type" placeholder="detail / summary" /></el-form-item></el-col>
          <el-col :span="12"><el-form-item label="质量分"><el-input-number v-model="itemDraft.quality_score" :min="0" :max="100" style="width:100%" /></el-form-item></el-col>
        </el-row>
        <el-form-item label="自然语言问题"><el-input v-model="itemDraft.question" /></el-form-item>
        <el-form-item label="标准 SQL">
          <el-input v-model="itemDraft.sql_text" type="textarea" :rows="14" resize="vertical" placeholder="标准 PostgreSQL SQL" class="mono-textarea" />
        </el-form-item>
      </el-form>

      <!-- 专家提示词编辑 -->
      <el-form v-if="itemEditorType === 'prompt'" label-width="90px">
        <el-row :gutter="12">
          <el-col :span="8">
            <el-form-item label="Agent">
              <el-select v-model="itemDraft.agent_no" style="width:100%">
                <el-option :value="1" label="Agent1" /><el-option :value="2" label="Agent2" />
                <el-option :value="3" label="Agent3" /><el-option :value="4" label="Agent4" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="16"><el-form-item label="Key"><el-input v-model="itemDraft.prompt_key" /></el-form-item></el-col>
        </el-row>
        <el-form-item label="Prompt 内容">
          <el-input v-model="itemDraft.prompt_content" type="textarea" :rows="16" resize="vertical" placeholder="在这里编辑完整的提示词内容..." class="mono-textarea" />
        </el-form-item>
      </el-form>

      <!-- 外部配置编辑 -->
      <el-form v-if="itemEditorType === 'extcfg'" label-width="90px">
        <el-row :gutter="12">
          <el-col :span="10"><el-form-item label="类型"><el-input v-model="itemDraft.config_type" /></el-form-item></el-col>
          <el-col :span="14"><el-form-item label="Key"><el-input v-model="itemDraft.config_key" /></el-form-item></el-col>
        </el-row>
        <el-form-item label="配置 JSON">
          <el-input v-model="itemDraftJson" type="textarea" :rows="14" resize="vertical" class="mono-textarea" placeholder='{"key": "value"}' />
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="itemEditorVisible = false">取消</el-button>
        <el-button v-if="canSaveItemEditor" type="primary" @click="saveItemEditor">确认保存</el-button>
      </template>
    </el-dialog>

    <!-- 大段提示词生成数据集 -->
    <el-dialog
      v-model="promptDatasetVisible"
      title="根据提示词生成新数据集"
      width="1120px"
      class="prompt-dataset-dialog"
      destroy-on-close
      top="3vh"
      :close-on-click-modal="!promptDatasetLoading"
    >
      <div class="prompt-generate-shell">
        <el-alert
          type="info"
          :closable="false"
          show-icon
          title="把 DDL、fields 字段字典、LLD、查询与报告专家 提示词、示例 SQL 粘贴进来，系统会生成一套新的数据集书架内容。"
        />
        <div v-if="promptDatasetLoading || promptDatasetStatus" class="prompt-progress-panel">
          <div class="prompt-progress-head">
            <div>
              <strong>{{ promptDatasetStageTitle }}</strong>
              <span>{{ promptDatasetStatus }}</span>
            </div>
            <em>{{ promptDatasetElapsedText }}</em>
          </div>
          <el-progress :percentage="promptDatasetProgress" :status="promptDatasetProgress === 100 ? 'success' : undefined" />
          <div class="prompt-stage-strip">
            <div
              v-for="(step, index) in PROMPT_DATASET_STEPS"
              :key="step"
              class="prompt-stage"
              :class="{ active: index === promptDatasetStepIndex, done: index < promptDatasetStepIndex }"
            >
              <span>{{ index + 1 }}</span>
              <strong>{{ step }}</strong>
            </div>
          </div>
          <div class="prompt-progress-note">
            AI 正在阅读大段文档并生成 DDL、字段字典、Golden SQL 和 专家提示词，复杂提示词通常需要 1-5 分钟。页面有耗时和阶段反馈，失败后会给出具体原因和建议。
          </div>
        </div>
        <el-form label-width="112px" class="prompt-generate-form">
          <el-row :gutter="12">
            <el-col :span="12">
              <el-form-item label="绑定数据源">
                <el-select v-model="promptDatasetForm.source_id" clearable style="width:100%">
                  <el-option v-for="source in dataSources" :key="source.id" :label="source.name" :value="source.id" />
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="参考样式">
                <el-select v-model="promptDatasetForm.style_dataset_id" clearable placeholder="可选：参考当前某个数据集的书架风格" style="width:100%">
                  <el-option v-for="item in datasets" :key="item.id" :label="item.dataset_name" :value="item.id" />
                </el-select>
              </el-form-item>
            </el-col>
          </el-row>
          <el-row :gutter="12">
            <el-col :span="8"><el-form-item label="名称覆盖"><el-input v-model="promptDatasetForm.dataset_name" placeholder="可空，AI 自动推断" /></el-form-item></el-col>
            <el-col :span="8"><el-form-item label="编码覆盖"><el-input v-model="promptDatasetForm.dataset_code" placeholder="可空，AI 自动推断" /></el-form-item></el-col>
            <el-col :span="8"><el-form-item label="业务域覆盖"><el-input v-model="promptDatasetForm.business_domain" placeholder="可空，AI 自动推断" /></el-form-item></el-col>
          </el-row>
          <el-form-item label="大段提示词">
            <el-input
              v-model="promptDatasetForm.doc_text"
              type="textarea"
              :rows="16"
              resize="vertical"
              class="mono-textarea"
              placeholder="粘贴 DDL、字段字典、业务口径、报告要求、专家提示词、示例 SQL 等内容..."
            />
          </el-form-item>
        </el-form>
      </div>
      <template #footer>
        <el-button v-if="!promptDatasetLoading" @click="promptDatasetVisible = false">取消</el-button>
        <el-button v-else plain type="warning" @click="cancelPromptDatasetGeneration">停止生成</el-button>
        <el-button type="primary" :loading="promptDatasetLoading" @click="generateDatasetFromPrompt">
          生成并保存新数据集
        </el-button>
      </template>
    </el-dialog>

    <!-- 从数据源拉表 dialog -->
    <el-dialog v-model="sourceDialogVisible" title="从数据源拉表进数据集" width="72%">
      <div class="toolbar-col" style="margin-bottom:10px">
        <el-select v-model="sourceDialogSourceId" placeholder="选择数据源" style="width:320px">
          <el-option v-for="source in dataSources" :key="source.id" :label="source.name" :value="source.id" />
        </el-select>
        <el-button v-if="canUseDatasetFeature('dataset_source_table')" type="primary" @click="loadSourceTables">加载表清单</el-button>
      </div>
      <el-table :data="sourceTables" border @selection-change="onSourceTableSelection">
        <el-table-column type="selection" width="55" />
        <el-table-column prop="full_table_name" label="表名" min-width="260" />
        <el-table-column prop="column_count" label="字段数" width="100" />
        <el-table-column label="DDL预览" min-width="280">
          <template #default="{ row }"><el-input :model-value="row.ddl_sql" type="textarea" :rows="2" readonly /></template>
        </el-table-column>
      </el-table>
      <template #footer>
        <el-button @click="sourceDialogVisible = false">取消</el-button>
        <el-button v-if="canUseDatasetFeature('dataset_source_table')" type="primary" @click="appendSelectedSourceTables">
          加入当前数据集{{ selectedSourceTables.length > 0 ? ` (${selectedSourceTables.length} 张表)` : '' }}
        </el-button>
      </template>
    </el-dialog>

    <!-- DDL 编辑 drawer -->
    <el-drawer v-model="schemaEditorVisible" size="72%" destroy-on-close :with-header="false">
      <div class="schema-editor-shell">
        <div class="schema-editor-header">
          <div>
            <div class="panel-title">{{ schemaEditorIndex === -1 ? '新增 DDL' : '编辑 DDL' }}</div>
            <div class="schema-editor-subtitle">独立维护表定义，宽敞编辑不拥挤</div>
          </div>
          <div class="header-actions">
            <el-button @click="schemaEditorVisible = false">关闭</el-button>
            <el-button v-if="canUseDatasetFeature('dataset_schema_update')" type="primary" @click="saveSchemaEditor">保存 DDL</el-button>
          </div>
        </div>
        <el-form label-width="110px" class="schema-editor-form">
          <el-row :gutter="14">
            <el-col :span="8">
              <el-form-item label="来源">
                <el-select v-model="schemaEditor.source_id" clearable placeholder="请选择来源">
                  <el-option v-for="source in dataSources" :key="source.id" :label="source.name" :value="source.id" />
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="8"><el-form-item label="表名"><el-input v-model="schemaEditor.table_name" placeholder="例如 datapivot_core_data" /></el-form-item></el-col>
            <el-col :span="8"><el-form-item label="描述"><el-input v-model="schemaEditor.description" placeholder="说明这张表的用途" /></el-form-item></el-col>
          </el-row>
          <el-form-item label="DDL 正文">
            <el-input v-model="schemaEditor.ddl_sql" type="textarea" :rows="24" resize="vertical" class="mono-textarea" placeholder="在这里编辑完整 DDL，支持大段文本" />
          </el-form-item>
        </el-form>
      </div>
    </el-drawer>

    <!-- 数据转换编辑弹窗 -->
    <el-dialog v-model="transformDialogVisible" :title="isTransformEdit ? '编辑转换任务' : '新增转换任务'" width="780px" destroy-on-close top="5vh">
      <el-form label-width="110px" :disabled="!selectedCanEdit">
        <el-row :gutter="14">
          <el-col :span="12">
            <el-form-item label="任务名称" required>
              <el-input v-model="transformForm.name" placeholder="例如：线上业务视图" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="源表" required>
              <el-input v-model="transformForm.source_table" placeholder="例如：feishu_tbl_beta" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="14">
          <el-col :span="12">
            <el-form-item label="目标类型">
              <el-select v-model="transformForm.target_type" style="width: 100%">
                <el-option label="视图 VIEW" value="view" />
                <el-option label="表 TABLE" value="table" />
                <el-option label="物化视图 MATERIALIZED VIEW" value="materialized_view" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="目标名称" required>
              <el-input v-model="transformForm.target_name" placeholder="例如：v_feishu_tbl_beta" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="转换 SQL" required>
          <div style="margin-bottom: 6px;">
            <el-button size="small" @click="applyOnlineTemplate">套用线上业务模板</el-button>
            <el-button size="small" :loading="transformTestLoading" @click="handleTestTransformSql">测试 SQL</el-button>
            <span class="muted-text" style="margin-left: 8px;">只允许单条 SELECT 或 WITH 语句，可用 <code v-pre>{{source_table}}</code> 占位符</span>
          </div>
          <el-input v-model="transformForm.transform_sql" type="textarea" :rows="14" resize="vertical" placeholder="输入 SELECT 语句..." />
        </el-form-item>
        <el-row :gutter="14">
          <el-col :span="8">
            <el-form-item label="自动执行">
              <el-switch v-model="transformForm.auto_run_on_sync" active-text="源表同步后自动执行" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="启用状态">
              <el-switch v-model="transformForm.is_active" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="绑定同步任务">
              <el-input v-model="transformForm.sync_dependency" placeholder="可选：飞书同步配置名称/ID" />
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
      <template #footer>
        <el-button @click="closeTransformEditor">取消</el-button>
        <el-button type="primary" :loading="transformLoading" @click="saveTransform">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import "../styles/module-interiors.css"
import { computed, onMounted, onUnmounted, reactive, ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  createBookshelfDataset, deleteBookshelfDataset, getBookshelfDatasetFull,
  extractBookshelfDictionaryFromPg, generateBookshelfDatasetFromPrompt, getBookshelfDatasets, getDataSources, getSourceTables,
  saveBookshelfDatasetFull, updateBookshelfDataset,
  getDatasetTransforms, createDatasetTransform, updateDatasetTransform, deleteDatasetTransform,
  runDatasetTransform, testDatasetTransformSql
} from '../api/index.js'
import { useFeatureFlags } from '../state/featureFlags.js'
import {
  dedupeGoldenSqlSamples,
  extractSqlSamplesFromPrompts,
  mergeAutofillCollection,
} from '../utils/datasetAutofillPromptMining.js'

const assetGroups = [
  {id:'business',label:'业务知识',items:[
    {key:'common_questions',label:'常见问题',description:'让用户从熟悉的业务问题开始，提供可直接发起的提问入口。',collection:'common_questions'},
    {key:'synonyms',label:'术语与别名',description:'对齐业务习惯用语与标准名称，帮助主理人识别数据范围。',collection:'synonyms'},
    {key:'lld',label:'业务口径',description:'记录业务定义、统计边界和数据使用约束。',collection:'lld_documents'},
    {key:'prompts',label:'专家知识',description:'为协作角色补充当前数据集的领域知识与处理要求。',collection:'agent_prompts'}]},
  {id:'model',label:'数据模型',items:[
    {key:'dictionary',label:'字段字典',description:'建立物理字段与业务含义的对应关系，为查询生成提供依据。',collection:'data_dictionary'},
    {key:'schema',label:'表与关联',description:'维护可查询的表结构与连接关系。',collection:'schema_definition'},
    {key:'transforms',label:'数据转换',description:'维护原始数据到分析表或视图的转换任务。'}]},
  {id:'quality',label:'质量与接入',items:[
    {key:'golden',label:'SQL 样例',description:'保存经过核对的查询样例，供查询专家参考。',collection:'golden_sql_samples'},
    {key:'regression_cases',label:'标准题集',description:'定义代表性业务问题及预期结果，用于验证问数质量。',collection:'regression_cases'},
    {key:'external',label:'外部配置',description:'维护飞书与其他外部系统在当前数据集上的接入配置。',collection:'external_configs'}]}
]
const activeAssetGroup = computed(()=>assetGroups.find(group=>group.items.some(item=>item.key===activeTab.value)) || assetGroups[0])
const activeAssetSection = computed(()=>activeAssetGroup.value.items.find(item=>item.key===activeTab.value) || activeAssetGroup.value.items[0])
const assetCount = key => key==='transforms'?transforms.value.length:(full[assetGroups.flatMap(group=>group.items).find(item=>item.key===key)?.collection] || []).length

// ========== 基础状态 ==========
const datasets = ref([])
const datasetsLoading = ref(true)
const dataSources = ref([])
const listFilterSourceId = ref('')
const listStatusFilter = ref('active')
const searchKeyword = ref('')
const selectedDatasetId = ref(null)
const activeTab = ref('common_questions')
const isDirty = ref(false)
const newDatasetSourceId = ref(null)
const qualitySummary = ref(null)
const pgDictLoading = ref(false)
const promptDatasetVisible = ref(false)
const promptDatasetLoading = ref(false)
const promptDatasetStatus = ref('')
const promptDatasetStepIndex = ref(-1)
const promptDatasetProgress = ref(0)
const promptDatasetElapsed = ref(0)
let promptDatasetTimer = null
let promptDatasetAbortController = null
const { isFeatureEnabled, loadFeatureFlags } = useFeatureFlags()

const PROMPT_DATASET_STEPS = ['准备输入', 'AI 生成', '校验质量', '创建数据集', '保存书架']
const promptDatasetStageTitle = computed(() => {
  if (promptDatasetStepIndex.value < 0) return '等待开始'
  return PROMPT_DATASET_STEPS[promptDatasetStepIndex.value] || '处理中'
})
const promptDatasetElapsedText = computed(() => {
  if (!promptDatasetElapsed.value) return '尚未开始'
  const minutes = Math.floor(promptDatasetElapsed.value / 60)
  const seconds = promptDatasetElapsed.value % 60
  return `已用时 ${minutes}:${String(seconds).padStart(2, '0')}`
})

const datasetForm = reactive({ dataset_code: '', dataset_name: '', business_domain: '', source_id: null, description: '', is_active: true })
const promptDatasetForm = reactive({
  source_id: null,
  style_dataset_id: null,
  dataset_name: '',
  dataset_code: '',
  business_domain: '',
  doc_text: '',
})
const full = reactive({
  common_questions: [], regression_cases: [], synonyms: [], lld_documents: [], data_dictionary: [],
  schema_definition: [], table_relations: [], golden_sql_samples: [],
  agent_prompts: [], external_configs: []
})

const transforms = ref([])
const transformDialogVisible = ref(false)
const transformEditId = ref(null)
const transformLoading = ref(false)
const transformRunLoading = ref({})
const transformTestLoading = ref(false)
const transformForm = reactive({
  name: '',
  source_table: '',
  target_type: 'view',
  target_name: '',
  transform_sql: '',
  is_active: true,
  auto_run_on_sync: false,
  sync_dependency: ''
})
const isTransformEdit = computed(() => Boolean(transformEditId.value))

const selectedDataset = computed(() => datasets.value.find(item => Number(item.id) === Number(selectedDatasetId.value)) || null)
const selectedCanEdit = computed(() => Boolean(selectedDataset.value?.can_edit))
const selectedCanDelete = computed(() => Boolean(selectedDataset.value?.can_delete))
const selectedDatasetScopeHit = computed(() => Boolean(selectedDataset.value?.dataset_scope_hit || selectedCanEdit.value))
const selectedDatasetReadonly = computed(() => Boolean(selectedDataset.value?.dataset_readonly || (selectedDatasetId.value && !selectedCanEdit.value)))
const datasetItemActionFeatureKeys = [
  'dataset_question_create', 'dataset_question_update', 'dataset_question_delete',
  'dataset_regression_create', 'dataset_regression_update', 'dataset_regression_delete',
  'dataset_synonym_create', 'dataset_synonym_update', 'dataset_synonym_delete',
  'dataset_lld_create', 'dataset_lld_update', 'dataset_lld_delete',
  'dataset_dict_create', 'dataset_dict_update', 'dataset_dict_delete',
  'dataset_schema_create', 'dataset_schema_update', 'dataset_schema_delete',
  'dataset_relation_create', 'dataset_relation_update', 'dataset_relation_delete',
  'dataset_golden_create', 'dataset_golden_update', 'dataset_golden_delete',
  'dataset_prompt_create', 'dataset_prompt_update', 'dataset_prompt_delete',
  'dataset_extcfg_create', 'dataset_extcfg_update', 'dataset_extcfg_delete',
]
const datasetShelfFeatureKeys = [
  'dataset_save',
  'dataset_prompt_generate',
  'dataset_autofill',
  'dataset_dict_extract',
  'dataset_source_table',
  ...datasetItemActionFeatureKeys,
]
const canViewDatasetShelfDetails = computed(() => Boolean(
  selectedCanEdit.value || datasetShelfFeatureKeys.some(key => isFeatureEnabled(key))
))
const readonlyAlertTitle = computed(() => (
  canViewDatasetShelfDetails.value
    ? '当前数据集为只读状态，仅可查看，不能编辑。'
    : '当前账号仅可查看数据集基础信息，书架维护内容已隐藏。'
))
const canUseDatasetFeature = (key) => Boolean(selectedCanEdit.value && isFeatureEnabled(key))
const datasetItemActionFeatureMap = {
  question: { create: 'dataset_question_create', update: 'dataset_question_update', delete: 'dataset_question_delete' },
  regression: { create: 'dataset_regression_create', update: 'dataset_regression_update', delete: 'dataset_regression_delete' },
  synonym: { create: 'dataset_synonym_create', update: 'dataset_synonym_update', delete: 'dataset_synonym_delete' },
  lld: { create: 'dataset_lld_create', update: 'dataset_lld_update', delete: 'dataset_lld_delete' },
  dict: { create: 'dataset_dict_create', update: 'dataset_dict_update', delete: 'dataset_dict_delete' },
  relation: { create: 'dataset_relation_create', update: 'dataset_relation_update', delete: 'dataset_relation_delete' },
  golden: { create: 'dataset_golden_create', update: 'dataset_golden_update', delete: 'dataset_golden_delete' },
  prompt: { create: 'dataset_prompt_create', update: 'dataset_prompt_update', delete: 'dataset_prompt_delete' },
  extcfg: { create: 'dataset_extcfg_create', update: 'dataset_extcfg_update', delete: 'dataset_extcfg_delete' },
}
const datasetActionFeatureKey = (type, action) => datasetItemActionFeatureMap[type]?.[action] || ''
const canUseDatasetAction = (type, action) => {
  const key = datasetActionFeatureKey(type, action)
  if (type === 'question') {
    return Boolean(selectedDatasetScopeHit.value && isFeatureEnabled(key))
  }
  return canUseDatasetFeature(key)
}
const canModifyCommonQuestions = computed(() => selectedDatasetScopeHit.value && (
  isFeatureEnabled('dataset_question_create')
  || isFeatureEnabled('dataset_question_update')
  || isFeatureEnabled('dataset_question_delete')
))
const canSaveShelfContent = computed(() => selectedDatasetScopeHit.value && (
  isFeatureEnabled('dataset_save') || canModifyCommonQuestions.value
))
const warnReadonly = () => {
  ElMessage.warning(selectedDatasetReadonly.value ? '当前数据集未命中你的员工组织范围，仅可查看。' : '当前账号没有该数据集的编辑权限。')
}
const ensureSelectedCanEdit = () => {
  if (selectedCanEdit.value) return true
  warnReadonly()
  return false
}
const markDirty = () => {
  if (!canSaveShelfContent.value) return
  isDirty.value = true
}
const deleteCollectionItem = async (type, index) => {
  const key = COLLECTIONS[type]
  if (!key || !Array.isArray(full[key])) return
  const removed = full[key].splice(index, 1)
  markDirty()
  // 常见问题支持部分保存；其他类型需具备完整 dataset_save 权限才可自动保存
  const canAutoSave = canUseDatasetFeature('dataset_save') || type === 'question'
  if (!canAutoSave) {
    ElMessage.info('已删除，请记得点击「保存书架内容」后生效')
    return
  }
  const ok = await saveFull()
  if (!ok) {
    full[key].splice(index, 0, ...removed)
  }
}
const qualityAlertType = computed(() => {
  if (!qualitySummary.value) return 'info'
  return qualitySummary.value.level === 'healthy' ? 'success' : qualitySummary.value.level === 'warning' ? 'warning' : 'error'
})
const qualityCheckTagType = (status) => (status === 'healthy' ? 'success' : status === 'warning' ? 'warning' : 'danger')
const isSyybDataset = computed(() => {
  const text = [datasetForm.dataset_name, datasetForm.dataset_code, datasetForm.business_domain].filter(Boolean).join(' ')
  return /磐石事业群|磐石|panshi_deal_flow/i.test(text)
})
const selectedDatasetName = computed(() => datasetForm.dataset_name || selectedDataset.value?.dataset_name || '当前数据集')

const SYYB_DEFAULT_DDL = `CREATE TABLE datapivot_core_data (
  id BIGINT,
  fields JSONB
);`

const createSyybTemplate = (sourceId) => ({
  common_questions: [
    { question_text: '磐石事业群当前年整体达成率是多少？', sort_order: 10, is_active: true },
    { question_text: '澔原战区当前年达成率和剩余任务是多少？', sort_order: 20, is_active: true },
    { question_text: '哪些片区达成率最低？', sort_order: 30, is_active: true },
    { question_text: '各行业部当前年开单金额排名如何？', sort_order: 40, is_active: true },
  ],
  regression_cases: [
    {
      case_type: 'summary',
      question_text: '磐石事业群当前年整体达成率是多少？',
      expected_focus: '应命中磐石事业群数据集，并输出事业群层级汇总达成率。',
      expected_intent: 'generate_sql',
      sort_order: 10,
      is_active: true,
    },
    {
      case_type: 'trend',
      question_text: '澔原战区今年任务和开单差距大吗？',
      expected_focus: '应保留澔原战区过滤意图，并给出剩余任务金额判断。',
      expected_intent: 'generate_sql',
      sort_order: 20,
      is_active: true,
    },
    {
      case_type: 'confirmation',
      question_text: '战区和片区分别怎么看业绩？',
      expected_focus: '应触发层级口径确认，避免把下级明细汇总进上级。',
      expected_intent: 'requires_confirmation',
      sort_order: 30,
      is_active: true,
    },
  ],
  synonyms: [
    { synonym: '磐石事业群', normalized_synonym: '磐石事业群', weight: 10 },
    { synonym: '星澜商用', normalized_synonym: '磐石事业群', weight: 9 },
    { synonym: '澔原战区', normalized_synonym: '澔原战区', weight: 8 },
    { synonym: '销售业绩', normalized_synonym: '销售业绩', weight: 7 },
  ],
  lld_documents: [
    {
      version: 1,
      title: '磐石事业群飞书销售表问数规则',
      content: '核心约束：数据来自 datapivot_core_data，业务字段位于 fields(JSONB)，年份口径固定为 2026。统计战区、片区、行业部等上级层级时，必须排除下级明细行，避免重复累计。金额字段统一先清洗非数字字符后再转 NUMERIC。',
      redline_rules: ['仅允许只读SQL', '必须按2026过滤', '必须执行层级隔离', '默认LIMIT 100'],
      is_active: true,
    },
  ],
  data_dictionary: [
    {
      table_name: 'datapivot_core_data',
      column_name: 'fields',
      jsonb_key: '事业群',
      semantic_name: '事业群',
      data_type: 'text',
      enum_mapping: {},
      extraction_rule: "CASE WHEN jsonb_typeof(fields->'事业群')='array' THEN fields->'事业群'->0->>'text' ELSE fields->>'事业群' END",
      is_active: true,
    },
    {
      table_name: 'datapivot_core_data',
      column_name: 'fields',
      jsonb_key: '战区',
      semantic_name: '战区',
      data_type: 'text',
      enum_mapping: {},
      extraction_rule: "CASE WHEN jsonb_typeof(fields->'战区')='array' THEN fields->'战区'->0->>'text' ELSE fields->>'战区' END",
      is_active: true,
    },
    {
      table_name: 'datapivot_core_data',
      column_name: 'fields',
      jsonb_key: '片区',
      semantic_name: '片区',
      data_type: 'text',
      enum_mapping: {},
      extraction_rule: "CASE WHEN jsonb_typeof(fields->'片区')='array' THEN fields->'片区'->0->>'text' ELSE fields->>'片区' END",
      is_active: true,
    },
    {
      table_name: 'datapivot_core_data',
      column_name: 'fields',
      jsonb_key: '客户经理',
      semantic_name: '客户经理',
      data_type: 'text',
      enum_mapping: {},
      extraction_rule: "CASE WHEN jsonb_typeof(fields->'客户经理')='array' THEN fields->'客户经理'->0->>'text' ELSE fields->>'客户经理' END",
      is_active: true,
    },
    {
      table_name: 'datapivot_core_data',
      column_name: 'fields',
      jsonb_key: '当前年',
      semantic_name: '当前年',
      data_type: 'text',
      enum_mapping: {},
      extraction_rule: "CASE WHEN jsonb_typeof(fields->'当前年')='array' THEN fields->'当前年'->0->>'text' ELSE fields->>'当前年' END",
      is_active: true,
    },
    {
      table_name: 'datapivot_core_data',
      column_name: 'fields',
      jsonb_key: '总任务（金额）',
      semantic_name: '总任务金额',
      data_type: 'numeric',
      enum_mapping: {},
      extraction_rule: "COALESCE(NULLIF(regexp_replace(CASE WHEN jsonb_typeof(fields->'总任务（金额）')='array' THEN fields->'总任务（金额）'->0->>'text' ELSE fields->>'总任务（金额）' END,'[^0-9.-]','','g'),''),'0')::NUMERIC",
      is_active: true,
    },
    {
      table_name: 'datapivot_core_data',
      column_name: 'fields',
      jsonb_key: '年度开单金额',
      semantic_name: '年度开单金额',
      data_type: 'numeric',
      enum_mapping: {},
      extraction_rule: "COALESCE(NULLIF(regexp_replace(CASE WHEN jsonb_typeof(fields->'年度开单金额')='array' THEN fields->'年度开单金额'->0->>'text' ELSE fields->>'年度开单金额' END,'[^0-9.-]','','g'),''),'0')::NUMERIC",
      is_active: true,
    },
  ],
  schema_definition: [
    {
      table_name: 'datapivot_core_data',
      ddl_sql: SYYB_DEFAULT_DDL,
      description: '飞书多维表格落库主表，业务字段位于 fields(JSONB)。',
      source_id: sourceId,
      is_active: true,
    },
  ],
  table_relations: [],
  golden_sql_samples: [
    {
      intent_type: 'summary',
      question: '磐石事业群当前年整体达成率是多少？',
      sql_text: `WITH 字段提取 AS (
  SELECT
    CASE WHEN jsonb_typeof(fields->'当前年')='array' THEN fields->'当前年'->0->>'text' ELSE fields->>'当前年' END AS 当前年,
    CASE WHEN jsonb_typeof(fields->'战区')='array' THEN fields->'战区'->0->>'text' ELSE fields->>'战区' END AS 战区,
    CASE WHEN jsonb_typeof(fields->'片区')='array' THEN fields->'片区'->0->>'text' ELSE fields->>'片区' END AS 片区,
    CASE WHEN jsonb_typeof(fields->'客户经理')='array' THEN fields->'客户经理'->0->>'text' ELSE fields->>'客户经理' END AS 客户经理,
    COALESCE(NULLIF(regexp_replace(CASE WHEN jsonb_typeof(fields->'总任务（金额）')='array' THEN fields->'总任务（金额）'->0->>'text' ELSE fields->>'总任务（金额）' END,'[^0-9.-]','','g'),''),'0')::NUMERIC AS 任务金额,
    COALESCE(NULLIF(regexp_replace(CASE WHEN jsonb_typeof(fields->'年度开单金额')='array' THEN fields->'年度开单金额'->0->>'text' ELSE fields->>'年度开单金额' END,'[^0-9.-]','','g'),''),'0')::NUMERIC AS 开单金额
  FROM datapivot_core_data
), 事业群汇总 AS (
  SELECT 任务金额, 开单金额
  FROM 字段提取
  WHERE 当前年='2026'
    AND 战区 IS NOT NULL AND 战区<>''
    AND (片区 IS NULL OR 片区='')
    AND (客户经理 IS NULL OR 客户经理='')
)
SELECT
  SUM(任务金额) AS 总任务金额,
  SUM(开单金额) AS 年度开单金额,
  CASE WHEN SUM(任务金额)>0 THEN ROUND(SUM(开单金额)/SUM(任务金额)*100,2) ELSE 0 END AS 达成率,
  ROUND(SUM(任务金额)-SUM(开单金额),2) AS 剩余任务金额
FROM 事业群汇总
LIMIT 100`,
      tags: ['磐石事业群', '达成率', '汇总'],
      quality_score: 95,
      is_active: true,
    },
    {
      intent_type: 'detail',
      question: '澔原战区当前年达成率和剩余任务是多少？',
      sql_text: `WITH 字段提取 AS (
  SELECT
    CASE WHEN jsonb_typeof(fields->'当前年')='array' THEN fields->'当前年'->0->>'text' ELSE fields->>'当前年' END AS 当前年,
    CASE WHEN jsonb_typeof(fields->'战区')='array' THEN fields->'战区'->0->>'text' ELSE fields->>'战区' END AS 战区,
    CASE WHEN jsonb_typeof(fields->'片区')='array' THEN fields->'片区'->0->>'text' ELSE fields->>'片区' END AS 片区,
    CASE WHEN jsonb_typeof(fields->'客户经理')='array' THEN fields->'客户经理'->0->>'text' ELSE fields->>'客户经理' END AS 客户经理,
    COALESCE(NULLIF(regexp_replace(CASE WHEN jsonb_typeof(fields->'总任务（金额）')='array' THEN fields->'总任务（金额）'->0->>'text' ELSE fields->>'总任务（金额）' END,'[^0-9.-]','','g'),''),'0')::NUMERIC AS 任务金额,
    COALESCE(NULLIF(regexp_replace(CASE WHEN jsonb_typeof(fields->'年度开单金额')='array' THEN fields->'年度开单金额'->0->>'text' ELSE fields->>'年度开单金额' END,'[^0-9.-]','','g'),''),'0')::NUMERIC AS 开单金额
  FROM datapivot_core_data
)
SELECT
  '澔原战区' AS 节点名称,
  SUM(任务金额) AS 总任务金额,
  SUM(开单金额) AS 年度开单金额,
  CASE WHEN SUM(任务金额)>0 THEN ROUND(SUM(开单金额)/SUM(任务金额)*100,2) ELSE 0 END AS 达成率,
  ROUND(SUM(任务金额)-SUM(开单金额),2) AS 剩余任务金额
FROM 字段提取
WHERE 当前年='2026'
  AND 战区='澔原战区'
  AND (片区 IS NULL OR 片区='')
  AND (客户经理 IS NULL OR 客户经理='')
LIMIT 100`,
      tags: ['澔原战区', '战区', '达成率'],
      quality_score: 92,
      is_active: true,
    },
    {
      intent_type: 'ranking',
      question: '哪些片区达成率最低？',
      sql_text: `WITH 字段提取 AS (
  SELECT
    CASE WHEN jsonb_typeof(fields->'当前年')='array' THEN fields->'当前年'->0->>'text' ELSE fields->>'当前年' END AS 当前年,
    CASE WHEN jsonb_typeof(fields->'战区')='array' THEN fields->'战区'->0->>'text' ELSE fields->>'战区' END AS 战区,
    CASE WHEN jsonb_typeof(fields->'片区')='array' THEN fields->'片区'->0->>'text' ELSE fields->>'片区' END AS 片区,
    CASE WHEN jsonb_typeof(fields->'客户经理')='array' THEN fields->'客户经理'->0->>'text' ELSE fields->>'客户经理' END AS 客户经理,
    COALESCE(NULLIF(regexp_replace(CASE WHEN jsonb_typeof(fields->'总任务（金额）')='array' THEN fields->'总任务（金额）'->0->>'text' ELSE fields->>'总任务（金额）' END,'[^0-9.-]','','g'),''),'0')::NUMERIC AS 任务金额,
    COALESCE(NULLIF(regexp_replace(CASE WHEN jsonb_typeof(fields->'年度开单金额')='array' THEN fields->'年度开单金额'->0->>'text' ELSE fields->>'年度开单金额' END,'[^0-9.-]','','g'),''),'0')::NUMERIC AS 开单金额
  FROM datapivot_core_data
), 片区汇总 AS (
  SELECT 战区, 片区, SUM(任务金额) AS 总任务金额, SUM(开单金额) AS 年度开单金额
  FROM 字段提取
  WHERE 当前年='2026'
    AND 片区 IS NOT NULL AND 片区<>''
    AND (客户经理 IS NULL OR 客户经理='')
  GROUP BY 战区, 片区
)
SELECT
  战区,
  片区,
  总任务金额,
  年度开单金额,
  CASE WHEN 总任务金额>0 THEN ROUND(年度开单金额/总任务金额*100,2) ELSE 0 END AS 达成率
FROM 片区汇总
ORDER BY 达成率 ASC, 总任务金额 DESC
LIMIT 100`,
      tags: ['片区', '排行', '低达成率'],
      quality_score: 90,
      is_active: true,
    },
  ],
  agent_prompts: [
    {
      agent_no: 1,
      prompt_key: 'default',
      prompt_content: '你是 Agent1（语义路由与口径守卫）。识别磐石事业群问题对应的数据集与统计口径；涉及战区、片区、行业部、客户经理等层级时，优先检查是否存在统计歧义，必要时先确认口径。所有当前年相关问题统一按 2026 处理。',
      is_active: true,
    },
    {
      agent_no: 2,
      prompt_key: 'default',
      prompt_content: '你是 Agent2（SQL 生成专家），仅允许输出 PostgreSQL 只读 SQL。表为 datapivot_core_data，业务字段位于 fields(JSONB)。金额字段必须清洗为 NUMERIC，年份固定过滤 2026，统计上级层级时必须排除下级明细行。',
      is_active: true,
    },
    {
      agent_no: 3,
      prompt_key: 'default',
      prompt_content: '你是 Agent3（SQL 复核官）。复核 SQL 是否只读、安全、可执行，是否正确使用 JSONB 提取、金额清洗、2026 年过滤、层级隔离和 LIMIT 100；若不满足，直接修正并返回 final_sql。',
      is_active: true,
    },
    {
      agent_no: 4,
      prompt_key: 'default',
      prompt_content: '你是 Agent4（业务解读官），面向磐石事业群管理层输出结论。先给出整体达成、风险和动作建议，再按事业群、线、战区或片区分层展开，避免空话。',
      is_active: true,
    },
  ],
  external_configs: [
    {
      config_type: 'dataset_meta',
      config_key: 'sql_generation_profile',
      config_value: {
        year_fixed: '2026',
        main_table: 'datapivot_core_data',
        db_type: 'postgresql',
        jsonb_column: 'fields',
        readonly: true,
      },
      is_active: true,
    },
  ],
})

const mergeCollection = (collectionName, items, keyFn, options = {}) => {
  mergeAutofillCollection(full[collectionName], items, keyFn, options)
}

const quoteIdent = (name) => `"${String(name || '').replace(/"/g, '""')}"`
const quoteTable = (name) => String(name || '').split('.').filter(Boolean).map(quoteIdent).join('.')
const compactName = (value, fallback = '当前数据集') => String(value || fallback).trim() || fallback
const semanticNameOf = (columnName) => {
  const raw = String(columnName || '').trim()
  const lower = raw.toLowerCase()
  const compound = [
    [/(order|deal|sale).*(no|code|number)$/, '订单编号'],
    [/(order|deal|sale).*(amount|money|amt|price)$/, '订单金额'],
    [/(order|deal|sale).*(count|qty|quantity)$/, '订单数量'],
    [/(order|deal|sale).*(status|state)$/, '订单状态'],
    [/(order|deal|sale).*(date|day)$/, '订单日期'],
    [/(region|area|province|city).*name$/, '区域名称'],
    [/(dept|department).*name$/, '部门名称'],
    [/(customer|client).*name$/, '客户名称'],
    [/(product|sku).*name$/, '产品名称'],
    [/(employee|staff|sales).*name$/, '员工名称'],
    [/(company|org|organization).*name$/, '组织名称'],
  ].find(([pattern]) => pattern.test(lower))
  if (compound) return compound[1]
  const mapped = [
    [/^(id|.*_id)$/, '编号'],
    [/(name|title|label|名称|姓名)$/, '名称'],
    [/(code|编码|编号)$/, '编码'],
    [/(date|day|日期)$/, '日期'],
    [/(time|created_at|updated_at|时间)$/, '时间'],
    [/(amount|money|amt|price|金额|价格|费用)$/, '金额'],
    [/(count|qty|quantity|数量)$/, '数量'],
    [/(rate|ratio|percent|比例|率)$/, '比例'],
    [/(status|state|状态)$/, '状态'],
    [/(type|category|分类|类型)$/, '类型'],
    [/(dept|department|部门)$/, '部门'],
    [/(org|organization|company|公司|组织)$/, '组织'],
    [/(region|area|province|city|区域|省|市)$/, '区域'],
  ].find(([pattern]) => pattern.test(lower) || pattern.test(raw))
  if (mapped) return mapped[1]
  return raw
    .replace(/^fields[._-]?/i, '')
    .replace(/[_-]+/g, ' ')
    .replace(/\s+/g, ' ')
    .trim() || raw || '字段'
}
const parseDdlColumns = (schema) => {
  const ddl = String(schema?.ddl_sql || '')
  const tableName = compactName(schema?.table_name, 'unknown_table')
  const columns = []
  const colRegex = /^\s*["`']?([\w\u4e00-\u9fa5]+)["`']?\s+([a-zA-Z][\w]*(?:\s*\([^)]*\))?)/gm
  let match
  while ((match = colRegex.exec(ddl)) !== null) {
    const colName = match[1]
    const lower = colName.toLowerCase()
    if (['constraint', 'primary', 'unique', 'index', 'check', 'foreign', 'create', 'alter', 'table', 'key'].includes(lower)) continue
    columns.push({
      table_name: tableName,
      column_name: colName,
      jsonb_key: '',
      semantic_name: semanticNameOf(colName),
      data_type: match[2] || 'text',
      enum_mapping: {},
      extraction_rule: '',
      is_active: true,
    })
  }
  return columns
}
const isNumericType = (type) => /int|numeric|decimal|double|float|real|money|number/i.test(String(type || ''))
const isTextLikeType = (type) => /char|text|varchar|uuid|jsonb?|enum/i.test(String(type || ''))
const buildSelectList = (columns) => {
  const selected = (columns || []).slice(0, 8)
  if (selected.length === 0) return '*'
  return selected.map(col => `${quoteIdent(col.column_name)} AS ${quoteIdent(col.semantic_name || col.column_name)}`).join(',\n  ')
}
const truncateText = (value, max = 3600) => {
  const text = String(value || '').trim()
  return text.length > max ? `${text.slice(0, max)}\n...已截断，完整 DDL 以数据集书架为准。` : text
}
const buildPromptDdlContext = (schemas) => schemas
  .map(item => `表：${item.table_name}\n${truncateText(item.ddl_sql, 2200)}`)
  .join('\n\n')
const buildPromptDictionaryContext = (items) => (items || [])
  .slice(0, 80)
  .map(item => `- ${item.table_name}.${item.column_name}：${item.semantic_name || item.column_name}，类型=${item.data_type || 'unknown'}${item.jsonb_key ? `，JSON key=${item.jsonb_key}` : ''}`)
  .join('\n')
const buildAgent1Prompt = ({ datasetName, domain, promptTableNames }) => `你是 Agent1（语义路由与口径守卫）。
当前数据集：「${datasetName}」
业务域：「${domain}」
可用表：${promptTableNames}

职责：
1. 判断用户问题是否应命中当前数据集。
2. 从问题中提取统计对象、指标、时间范围、筛选条件、排序/TopN/对比意图。
3. 用户说“这个、那个、继续下钻、换成上月”等省略表达时，优先沿用上一轮数据集和口径。
4. 如果实体、指标、时间或字段口径不清，先追问；不要让 Agent2 猜字段或猜业务规则。
5. 不得虚构 DDL、数据字典、LLD 中不存在的字段。`
const buildAgent2Prompt = ({ datasetName, domain, schemas, dictionaryForBuild, promptTableNames }) => `你是 Agent2（SQL 生成专家），你的输出质量直接决定问数是否可信。
当前数据集：「${datasetName}」
业务域：「${domain}」
可用表：${promptTableNames}

硬性规则：
1. 只生成 PostgreSQL 只读 SQL，禁止 INSERT、UPDATE、DELETE、TRUNCATE、DROP、ALTER、CREATE。
2. 只能使用下方 DDL 和数据字典中出现的表、字段、JSON key；字段不存在时不要猜，必须要求补充口径。
3. SQL 必须能独立执行；表名、字段名需要正确引用；聚合查询必须保证 GROUP BY 合法。
4. 明细查询默认 LIMIT 100；Top/排名查询默认 LIMIT 20；除非用户明确要求更多。
5. 输出列使用中文别名，让 Agent4 可以直接写报告。
6. 金额、数量、比例等指标必须按字段类型谨慎处理：数值字段可直接聚合；文本金额必须先清洗再转 numeric；无法确认类型时先给保守 SQL 或追问。
7. 用户要求对比时，要同时返回所有对比对象，不得只返回其中一个。
8. 用户要求下钻时，要先返回上一级摘要，再返回下一层明细；不能用明细直接替代管理层级结论。
9. 如果涉及时间但数据集中没有明确时间字段，必须说明无法按时间过滤或要求用户补充时间字段。
10. 如果查询意图与当前 DDL 不匹配，返回需要澄清的原因，不要硬造 SQL。

DDL 上下文：
${buildPromptDdlContext(schemas)}

字段语义：
${buildPromptDictionaryContext(dictionaryForBuild) || '暂无字段字典，请优先依据 DDL 字段名谨慎推断。'}`
const buildAgent3Prompt = ({ datasetName }) => `你是 Agent3（SQL 复核官）。
当前数据集：「${datasetName}」

复核重点：
1. SQL 是否只读、安全。
2. 表名、字段名、JSON key 是否来自当前数据集 DDL/字典。
3. 聚合、GROUP BY、ORDER BY、SELECT DISTINCT 是否符合 PostgreSQL 语法。
4. 明细查询是否有限制返回行数。
5. 对比场景是否遗漏用户要求的任一对象。
6. 下钻场景是否保留管理层级，不直接跳到过细明细。

发现问题时，优先修正 SQL；无法修正时明确指出缺少哪个字段或口径。`
const buildAgent4Prompt = ({ datasetName, domain }) => `你是 Agent4（报告生成与业务解读官）。
当前数据集：「${datasetName}」
业务域：「${domain}」

报告规则：
1. 必须基于 SQL 结果说话，不得编造查询结果之外的数字、排名、原因或建议。
2. 开头先回答用户问题，用 1-3 句话给出核心结论；不要把字段逐项堆成流水账。
3. 对比问题必须同时呈现各对象核心指标，并明确差异、领先/落后、风险点。
4. 下钻问题必须先说上层概览，再说下层贡献或拖累，不要只给长名单。
5. 输出结构优先采用：核心结论、关键指标对比、风险/异常、建议动作。
6. 如果结果为空，要说明可能原因：筛选条件未命中、字段口径缺失、时间范围不匹配或数据未同步。
7. 当查询结果字段不足以支撑判断时，明确说“当前结果不足以判断”，并建议补充字段或追问。`
const buildGenericAutofillTemplate = () => {
  const datasetName = compactName(datasetForm.dataset_name)
  const domain = compactName(datasetForm.business_domain, '未分类业务域')
  const schemas = full.schema_definition.filter(item => String(item.table_name || '').trim() && String(item.ddl_sql || '').trim())
  const dictionary = schemas.flatMap(parseDdlColumns)
  const dictionaryForBuild = [...full.data_dictionary, ...dictionary]
  const promptSqlSamples = extractSqlSamplesFromPrompts(full.agent_prompts, datasetName)
  const firstSchema = schemas[0]
  const firstTable = quoteTable(firstSchema?.table_name)
  const firstColumns = dictionaryForBuild.filter(item => item.table_name === firstSchema?.table_name)
  const numericCol = firstColumns.find(item => isNumericType(item.data_type))
  const dimensionCol = firstColumns.find(item => isTextLikeType(item.data_type) && !/id|编号|编码/i.test(`${item.column_name}${item.semantic_name}`))
  const hasJsonbFields = firstColumns.some(item => item.column_name === 'fields' && /jsonb?/i.test(item.data_type))
  const goldenSql = [...promptSqlSamples]
  if (firstTable) {
    goldenSql.push({
      intent_type: 'summary',
      question: `${datasetName}一共有多少条记录？`,
      sql_text: `SELECT COUNT(*) AS "记录数"\nFROM ${firstTable};`,
      tags: [datasetName, '汇总'],
      quality_score: 82,
    })
    goldenSql.push({
      intent_type: 'detail',
      question: `${datasetName}最近有哪些明细数据？`,
      sql_text: `SELECT\n  ${buildSelectList(firstColumns)}\nFROM ${firstTable}\nLIMIT 20;`,
      tags: [datasetName, '明细'],
      quality_score: 80,
    })
    if (dimensionCol) {
      goldenSql.push({
        intent_type: 'aggregation',
        question: `${datasetName}按${dimensionCol.semantic_name}分布如何？`,
        sql_text: `SELECT\n  ${quoteIdent(dimensionCol.column_name)} AS ${quoteIdent(dimensionCol.semantic_name)},\n  COUNT(*) AS "记录数"\nFROM ${firstTable}\nGROUP BY ${quoteIdent(dimensionCol.column_name)}\nORDER BY "记录数" DESC\nLIMIT 20;`,
        tags: [datasetName, dimensionCol.semantic_name],
        quality_score: 82,
      })
    }
    if (numericCol) {
      goldenSql.push({
        intent_type: 'metric_summary',
        question: `${datasetName}${numericCol.semantic_name}合计是多少？`,
        sql_text: `SELECT SUM(${quoteIdent(numericCol.column_name)}) AS ${quoteIdent(`${numericCol.semantic_name}合计`)}\nFROM ${firstTable};`,
        tags: [datasetName, numericCol.semantic_name],
        quality_score: 82,
      })
    }
    if (dimensionCol && numericCol) {
      goldenSql.push({
        intent_type: 'topn',
        question: `${datasetName}按${dimensionCol.semantic_name}看${numericCol.semantic_name}排名如何？`,
        sql_text: `SELECT\n  ${quoteIdent(dimensionCol.column_name)} AS ${quoteIdent(dimensionCol.semantic_name)},\n  SUM(${quoteIdent(numericCol.column_name)}) AS ${quoteIdent(`${numericCol.semantic_name}合计`)}\nFROM ${firstTable}\nGROUP BY ${quoteIdent(dimensionCol.column_name)}\nORDER BY ${quoteIdent(`${numericCol.semantic_name}合计`)} DESC\nLIMIT 20;`,
        tags: [datasetName, dimensionCol.semantic_name, numericCol.semantic_name],
        quality_score: 84,
      })
    }
    if (hasJsonbFields) {
      goldenSql.push({
        intent_type: 'schema_probe',
        question: `${datasetName}JSON 字段里有哪些 key？`,
        sql_text: `SELECT key AS "字段名", COUNT(*) AS "出现次数"\nFROM ${firstTable}, LATERAL jsonb_object_keys(fields) AS key\nGROUP BY key\nORDER BY "出现次数" DESC\nLIMIT 50;`,
        tags: [datasetName, 'JSONB'],
        quality_score: 80,
      })
    }
    while (goldenSql.length < 3) {
      goldenSql.push({
        intent_type: 'detail',
        question: `${datasetName}样例数据${goldenSql.length + 1}怎么看？`,
        sql_text: `SELECT\n  ${buildSelectList(firstColumns)}\nFROM ${firstTable}\nLIMIT 20 OFFSET ${(goldenSql.length - 1) * 20};`,
        tags: [datasetName, '样例'],
        quality_score: 78,
      })
    }
  }
  const promptQuestions = promptSqlSamples
    .filter(item => !/^.+样例 SQL \d+$/.test(item.question || ''))
    .slice(0, 3)
  const promptTableNames = schemas.map(item => item.table_name).join('、') || '已维护 DDL 的表'
  return {
    __meta: {
      prompt_sql_count: promptSqlSamples.length,
    },
    common_questions: [
      { question_text: `${datasetName}一共有多少条记录？`, sort_order: 10, is_active: true },
      { question_text: `${datasetName}最近有哪些明细数据？`, sort_order: 20, is_active: true },
      ...(dimensionCol ? [{ question_text: `${datasetName}按${dimensionCol.semantic_name}分布如何？`, sort_order: 30, is_active: true }] : []),
      ...(numericCol ? [{ question_text: `${datasetName}${numericCol.semantic_name}合计是多少？`, sort_order: 40, is_active: true }] : []),
      ...(dimensionCol && numericCol ? [{ question_text: `${datasetName}按${dimensionCol.semantic_name}看${numericCol.semantic_name}排名如何？`, sort_order: 50, is_active: true }] : []),
      ...promptQuestions.map((item, index) => ({ question_text: item.question, sort_order: 60 + index * 10, is_active: true })),
    ],
    regression_cases: [
      { case_type: 'summary', question_text: `${datasetName}一共有多少条记录？`, expected_focus: '应命中当前数据集，并返回总记录数。', expected_intent: 'generate_sql', sort_order: 10, is_active: true },
      { case_type: 'detail', question_text: `${datasetName}最近有哪些明细数据？`, expected_focus: '应基于当前 DDL 返回明细列表，并限制返回行数。', expected_intent: 'generate_sql', sort_order: 20, is_active: true },
      ...(dimensionCol ? [{ case_type: 'aggregation', question_text: `${datasetName}按${dimensionCol.semantic_name}分布如何？`, expected_focus: `应按${dimensionCol.semantic_name}聚合统计。`, expected_intent: 'generate_sql', sort_order: 30, is_active: true }] : []),
      ...promptQuestions.map((item, index) => ({
        case_type: 'prompt_example',
        question_text: item.question,
        expected_focus: '应优先参考已维护 查询与报告专家 中的样例 SQL 和业务逻辑。',
        expected_intent: 'generate_sql',
        sort_order: 40 + index * 10,
        is_active: true,
      })),
    ],
    synonyms: [
      { synonym: datasetName, normalized_synonym: datasetName, weight: 10 },
      ...(datasetForm.dataset_code ? [{ synonym: datasetForm.dataset_code, normalized_synonym: datasetName, weight: 8 }] : []),
      ...(datasetForm.business_domain ? [{ synonym: datasetForm.business_domain, normalized_synonym: datasetName, weight: 6 }] : []),
    ],
    lld_documents: [{
      version: full.lld_documents.length + 1,
      title: `${datasetName}智能问数基础口径`,
      content: `# ${datasetName}智能问数基础口径\n\n## 业务域\n${domain}\n\n## 数据范围\n当前数据集基于已维护 DDL 自动生成基础问数配置，涉及表：${promptTableNames}。\n\n## 字段口径\n字段语义优先使用数据字典；字典缺失时只能依据 DDL 字段名进行谨慎推断，不得编造未出现在 DDL 或业务描述中的字段。\n\n## SQL 红线\n只允许生成只读 SQL；必须使用当前数据集维护的表结构和字段；聚合、排序、筛选条件需要与用户问题一致；无法判断业务口径时先追问。`,
      redline_rules: ['只读 SQL', '不得编造字段', '口径不清先追问', '结果必须限制返回行数'],
      is_active: true,
    }],
    data_dictionary: dictionary,
    golden_sql_samples: dedupeGoldenSqlSamples(goldenSql).slice(0, 12),
    agent_prompts: [
      { agent_no: 1, prompt_key: 'default', prompt_content: buildAgent1Prompt({ datasetName, domain, promptTableNames }), is_active: true },
      { agent_no: 2, prompt_key: 'default', prompt_content: buildAgent2Prompt({ datasetName, domain, schemas, dictionaryForBuild, promptTableNames }), is_active: true },
      { agent_no: 3, prompt_key: 'default', prompt_content: buildAgent3Prompt({ datasetName }), is_active: true },
      { agent_no: 4, prompt_key: 'default', prompt_content: buildAgent4Prompt({ datasetName, domain }), is_active: true },
    ],
    external_configs: [{
      config_type: 'dataset_meta',
      config_key: 'sql_generation_profile',
      config_value: { db_type: 'postgresql', readonly: true, tables: schemas.map(item => item.table_name) },
      is_active: true,
    }],
  }
}

const autofillSelectedDataset = async () => {
  if (!selectedDatasetId.value) return
  if (!selectedCanEdit.value) { warnReadonly(); return }
  const hasUsableDdl = full.schema_definition.some(item => String(item.table_name || '').trim() && String(item.ddl_sql || '').trim())
  const sourceId = datasetForm.source_id || newDatasetSourceId.value || dataSources.value[0]?.id || null
  if (!isSyybDataset.value && !hasUsableDdl) {
    ElMessage.warning(`请先为「${selectedDatasetName.value}」维护至少一张表的 DDL，再执行智能补齐。`)
    return
  }
  if (isSyybDataset.value && !sourceId) {
    ElMessage.warning('请先为当前数据集选择一个数据源。')
    return
  }
  try {
    await ElMessageBox.confirm(`将根据「${selectedDatasetName.value}」当前已维护的 DDL 和基础信息，重点补齐字段字典与 4 个 专家提示词（尤其 查询专家 SQL 生成、Agent4 报告解读），并补充少量常见问题和 Golden SQL 样例。确认继续？`, '智能补齐数据集', {
      type: 'info',
      confirmButtonText: '开始补齐',
      cancelButtonText: '取消',
    })
  } catch {
    return
  }

  const template = isSyybDataset.value ? createSyybTemplate(sourceId) : buildGenericAutofillTemplate()
  if (!isSyybDataset.value && template.data_dictionary.length === 0 && full.data_dictionary.length === 0) {
    ElMessage.warning('当前 DDL 暂未解析出字段，请检查 DDL 是否包含标准列定义。')
    return
  }
  if (isSyybDataset.value) {
    if (!datasetForm.dataset_name) datasetForm.dataset_name = '磐石成交流水'
    if (!datasetForm.dataset_code) datasetForm.dataset_code = 'panshi_deal_flow_2026'
    if (!datasetForm.business_domain) datasetForm.business_domain = '磐石业务域销售业绩分析'
    if (!datasetForm.description) datasetForm.description = '磐石业务域（在线表格）四 Agent 模板'
    if (!datasetForm.source_id) datasetForm.source_id = sourceId
  } else if (!datasetForm.description) {
    datasetForm.description = `${selectedDatasetName.value}智能问数数据集`
  }

  mergeCollection('common_questions', template.common_questions, item => item.question_text)
  mergeCollection('regression_cases', template.regression_cases, item => `${item.case_type}|${item.question_text}`)
  mergeCollection('synonyms', template.synonyms, item => item.synonym)
  mergeCollection('lld_documents', template.lld_documents, item => `${item.version}|${item.title}`)
  mergeCollection('data_dictionary', template.data_dictionary, item => `${item.table_name}|${item.column_name}|${item.jsonb_key}`, { preserveExisting: true })
  mergeCollection('schema_definition', template.schema_definition, item => item.table_name)
  mergeCollection('golden_sql_samples', template.golden_sql_samples, item => item.question, { preserveExisting: true })
  mergeCollection('agent_prompts', template.agent_prompts, item => `${item.agent_no}|${item.prompt_key}`, { preservePromptContent: true })
  mergeCollection('external_configs', template.external_configs, item => `${item.config_type}|${item.config_key}`)

  activeTab.value = 'prompts'
  markDirty()
  if (!isSyybDataset.value && template.__meta?.prompt_sql_count) {
    ElMessage.success(`已从 查询与报告专家 提取 ${template.__meta.prompt_sql_count} 条样例 SQL，并保留原有 Prompt 内容。`)
  }
  await saveFull()
}

// ========== 左侧:搜索+筛选 ==========
const datasetStatusCounts = computed(() => {
  const active = datasets.value.filter(item => item.is_active !== false).length
  const inactive = datasets.value.filter(item => item.is_active === false).length
  return { all: datasets.value.length, active, inactive }
})

const filteredDatasets = computed(() => {
  let list = datasets.value
  if (listStatusFilter.value === 'active') list = list.filter(i => i.is_active !== false)
  if (listStatusFilter.value === 'inactive') list = list.filter(i => i.is_active === false)
  if (listFilterSourceId.value) list = list.filter(i => Number(i.source_id) === Number(listFilterSourceId.value))
  if (searchKeyword.value.trim()) {
    const kw = searchKeyword.value.trim().toLowerCase()
    list = list.filter(i => (i.dataset_name || '').toLowerCase().includes(kw) || (i.dataset_code || '').toLowerCase().includes(kw))
  }
  return list
})

const sourceNameById = (id) => dataSources.value.find(x => Number(x.id) === Number(id))?.name || '未设置'

// ========== 通用弹窗编辑器 ==========
const itemEditorVisible = ref(false)
const itemEditorType = ref('')
const itemEditorIndex = ref(-1)
const itemDraft = reactive({})
const itemDraftJson = ref('{}')

const EDITOR_TITLES = {
  question: '编辑常见问题', regression: '编辑标准题集', synonym: '编辑路由词/别名', lld: '编辑 LLD 文档',
  dict: '编辑数据字典', relation: '编辑表关联', golden: '编辑 Golden SQL',
  prompt: '编辑 专家提示片段', extcfg: '编辑外部配置'
}
const COLLECTIONS = {
  question: 'common_questions', regression: 'regression_cases', synonym: 'synonyms', lld: 'lld_documents',
  dict: 'data_dictionary', relation: 'table_relations', golden: 'golden_sql_samples',
  prompt: 'agent_prompts', extcfg: 'external_configs'
}
const FULL_COLLECTION_KEYS = [
  'common_questions',
  'regression_cases',
  'synonyms',
  'lld_documents',
  'data_dictionary',
  'schema_definition',
  'table_relations',
  'golden_sql_samples',
  'agent_prompts',
  'external_configs',
]
const DEFAULTS = {
  question: () => ({ question_text: '', sort_order: (full.common_questions.length + 1) * 10, is_active: true }),
  regression: () => ({
    case_type: 'summary',
    question_text: '',
    expected_focus: '',
    expected_intent: 'generate_sql',
    sort_order: (full.regression_cases.length + 1) * 10,
    is_active: true,
  }),
  synonym: () => ({ synonym: '', normalized_synonym: '', weight: 1 }),
  lld: () => ({ version: full.lld_documents.length + 1, title: '', content: '' }),
  dict: () => ({ table_name: '', column_name: '', jsonb_key: '', semantic_name: '', data_type: 'text' }),
  relation: () => ({ left_table: '', left_key: '', right_table: '', right_key: '', relation_type: 'inner' }),
  golden: () => ({ intent_type: 'detail', question: '', sql_text: '', quality_score: 80 }),
  prompt: () => ({ agent_no: 1, prompt_key: 'default', prompt_content: '' }),
  extcfg: () => ({ config_type: 'feishu_sync', config_key: `config_${Date.now()}`, config_value: {} })
}

const itemEditorTitle = computed(() => {
  const prefix = itemEditorIndex.value === -1 ? '新增' : '编辑'
  return (EDITOR_TITLES[itemEditorType.value] || '编辑').replace('编辑', prefix)
})
const canSaveItemEditor = computed(() => canUseDatasetAction(
  itemEditorType.value,
  itemEditorIndex.value === -1 ? 'create' : 'update'
))

const openItemEditor = (type, index) => {
  if (!canUseDatasetAction(type, index === -1 ? 'create' : 'update')) {
    warnReadonly()
    return
  }
  itemEditorType.value = type
  itemEditorIndex.value = index
  const col = full[COLLECTIONS[type]]
  const source = index >= 0 ? col[index] : DEFAULTS[type]()
  Object.keys(itemDraft).forEach(k => delete itemDraft[k])
  Object.assign(itemDraft, JSON.parse(JSON.stringify(source)))
  if (type === 'extcfg') itemDraftJson.value = jsonString(itemDraft.config_value)
  itemEditorVisible.value = true
}

const saveItemEditor = () => {
  if (!canSaveItemEditor.value) {
    warnReadonly()
    return
  }
  const type = itemEditorType.value
  const col = full[COLLECTIONS[type]]
  if (type === 'extcfg') {
    try { itemDraft.config_value = JSON.parse(itemDraftJson.value || '{}') } catch { ElMessage.warning('JSON 格式错误'); return }
  }
  const copy = JSON.parse(JSON.stringify(itemDraft))
  if (itemEditorIndex.value >= 0) col[itemEditorIndex.value] = copy
  else col.push(copy)
  itemEditorVisible.value = false
  markDirty()
}

// ========== 从 DDL 提取数据字典 ==========
const extractDictFromDDL = () => {
  if (!canUseDatasetFeature('dataset_dict_extract')) { warnReadonly(); return }
  if (full.schema_definition.length === 0) { ElMessage.warning('请先在 DDL 标签页中添加表定义'); return }
  let added = 0
  full.schema_definition.forEach(schema => {
    const ddl = schema.ddl_sql || ''
    const colRegex = /^\s+["']?(\w+)["']?\s+([\w()]+)/gm
    let match
    while ((match = colRegex.exec(ddl)) !== null) {
      const colName = match[1].toLowerCase()
      if (['constraint', 'primary', 'unique', 'index', 'check', 'foreign', 'create', 'alter', 'table'].includes(colName)) continue
      const exists = full.data_dictionary.some(d => d.table_name === schema.table_name && d.column_name === colName)
      if (!exists) {
        full.data_dictionary.push({ table_name: schema.table_name, column_name: colName, jsonb_key: '', semantic_name: '', data_type: match[2] || 'text' })
        added++
      }
    }
  })
  if (added > 0) { ElMessage.success(`已从 DDL 提取 ${added} 个新字段`); markDirty() }
  else ElMessage.info('DDL 中没有发现新的字段可提取，或字段已存在')
}

const mergeDictionaryItems = (items = []) => {
  let added = 0
  let updated = 0
  items.forEach(item => {
    const tableName = String(item.table_name || '').trim()
    const columnName = String(item.column_name || '').trim()
    const jsonbKey = String(item.jsonb_key || '').trim()
    if (!tableName || !columnName) return
    const key = `${tableName}|${columnName}|${jsonbKey}`
    const index = full.data_dictionary.findIndex(d => `${d.table_name || ''}|${d.column_name || ''}|${d.jsonb_key || ''}` === key)
    const next = {
      table_name: tableName,
      column_name: columnName,
      jsonb_key: jsonbKey,
      semantic_name: item.semantic_name || jsonbKey || columnName,
      data_type: item.data_type || '字符串',
      enum_mapping: item.enum_mapping || {},
      extraction_rule: item.extraction_rule || '',
      is_active: item.is_active !== false,
    }
    if (index >= 0) {
      full.data_dictionary[index] = { ...full.data_dictionary[index], ...next }
      updated++
    } else {
      full.data_dictionary.push(next)
      added++
    }
  })
  return { added, updated }
}

const extractDictFromPg = async () => {
  if (!canUseDatasetFeature('dataset_dict_extract')) { warnReadonly(); return }
  if (!selectedDatasetId.value) { ElMessage.warning('请先选择数据集'); return }
  const schema = full.schema_definition.find(item => String(item.table_name || '').trim()) || {}
  const tableName = String(schema.table_name || '').trim()
  if (!tableName) { ElMessage.warning('请先在 DDL + 表关联中维护来源表，或先从数据源拉表'); return }
  pgDictLoading.value = true
  try {
    const res = await extractBookshelfDictionaryFromPg(selectedDatasetId.value, {
      source_id: datasetForm.source_id,
      table_name: tableName,
      jsonb_column: 'fields',
      sample_limit: 5000,
    })
    const { added, updated } = mergeDictionaryItems(res.items || [])
    if (added || updated) {
      markDirty()
      ElMessage.success(`已从 PostgreSQL 提取字段：新增 ${added} 条，更新 ${updated} 条，JSONB Key ${res.jsonb_key_count || 0} 个`)
    } else {
      ElMessage.info('PostgreSQL 未发现新的字段，或字段已是最新')
    }
  } finally {
    pgDictLoading.value = false
  }
}

const clearDictionary = async () => {
  if (!canUseDatasetAction('dict', 'delete')) { warnReadonly(); return }
  if (!full.data_dictionary.length) { ElMessage.info('当前数据字典已经是空的'); return }
  await ElMessageBox.confirm('确认清空当前数据字典？清空后需要点击“保存书架内容”才会写入后端。', '清空数据字典', { type: 'warning' })
  full.data_dictionary = []
  markDirty()
  ElMessage.success('已清空当前数据字典，请保存书架内容')
}

// ========== 数据加载/保存 ==========
const applyDataset = (d) => {
  datasetForm.dataset_code = d?.dataset_code || ''; datasetForm.dataset_name = d?.dataset_name || ''
  datasetForm.business_domain = d?.business_domain || ''; datasetForm.source_id = d?.source_id || null
  datasetForm.description = d?.description || ''; datasetForm.is_active = d?.is_active !== false
}
const resetFull = () => { FULL_COLLECTION_KEYS.forEach(key => { full[key] = [] }); qualitySummary.value = null }

const loadDatasets = async () => {
  datasetsLoading.value = true
  try { datasets.value = (await getBookshelfDatasets({ include_inactive: 1 })).datasets || [] }
  finally { datasetsLoading.value = false }
}
const loadDataSources = async () => {
  dataSources.value = (await getDataSources()).databases || []
  if (!newDatasetSourceId.value && dataSources.value.length > 0) newDatasetSourceId.value = dataSources.value[0].id
}

const selectDataset = async (dataset) => {
  selectedDatasetId.value = dataset.id
  applyDataset(dataset)
  const r = await getBookshelfDatasetFull(dataset.id)
  if (r.dataset) {
    const idx = datasets.value.findIndex(item => Number(item.id) === Number(dataset.id))
    if (idx >= 0) datasets.value[idx] = { ...datasets.value[idx], ...r.dataset }
    applyDataset(r.dataset)
  }
  FULL_COLLECTION_KEYS.forEach(key => { full[key] = r[key] || [] })
  qualitySummary.value = r.quality_summary || null
  isDirty.value = false
  await loadTransforms()
}

const onSelectDataset = async (item) => {
  if (isDirty.value) {
    try { await ElMessageBox.confirm('当前有未保存的修改，切换后将丢失。确认切换？', '提示', { type: 'warning' }) }
    catch { return }
  }
  await selectDataset(item)
}

const createDataset = async () => {
  const r = await createBookshelfDataset({ dataset_code: `dataset_${Date.now()}`, dataset_name: '新数据集', business_domain: '未分类', source_id: newDatasetSourceId.value || undefined, description: '' })
  await loadDatasets()
  const t = datasets.value.find(i => i.id === r.dataset?.id)
  if (t) await selectDataset(t)
}

const removeDataset = async () => {
  if (!selectedDatasetId.value) return
  if (!selectedCanDelete.value) { warnReadonly(); return }
  await ElMessageBox.confirm('确认删除当前数据集吗？', '删除确认', { type: 'warning' })
  await deleteBookshelfDataset(selectedDatasetId.value)
  ElMessage.success('数据集已删除'); selectedDatasetId.value = null; resetFull(); isDirty.value = false; await loadDatasets()
}

const saveFull = async () => {
  if (!selectedDatasetId.value) return
  if (!canSaveShelfContent.value) { warnReadonly(); return false }
  const hasFullSave = canUseDatasetFeature('dataset_save')
  const payload = hasFullSave
    ? {}
    : { __partial: true, common_questions: full.common_questions }
  if (hasFullSave) {
    FULL_COLLECTION_KEYS.forEach(key => { payload[key] = full[key] })
  }
  try {
    if (hasFullSave) {
      await updateBookshelfDataset(selectedDatasetId.value, { ...datasetForm })
    }
    await saveBookshelfDatasetFull(selectedDatasetId.value, payload)
    ElMessage.success('书架内容已保存'); isDirty.value = false
    await loadDatasets()
    const currentDataset = datasets.value.find(item => Number(item.id) === Number(selectedDatasetId.value))
    if (currentDataset) {
      if ((listStatusFilter.value === 'active' && currentDataset.is_active === false)
        || (listStatusFilter.value === 'inactive' && currentDataset.is_active !== false)) {
        listStatusFilter.value = 'active'
      }
      await selectDataset(currentDataset)
    }
    return true
  } catch (err) {
    const details = err?.response?.data?.details
    if (Array.isArray(details) && details.length) {
      ElMessageBox.alert(details.join('<br/>'), '保存前校验未通过', {
        confirmButtonText: '知道了',
        dangerouslyUseHTMLString: true,
        type: 'warning',
      })
      return false
    }
    ElMessage.error(err?.response?.data?.error || err?.message || '保存失败')
    return false
  }
}

// ========== 大段提示词生成新数据集 ==========
const resetPromptDatasetForm = () => {
  promptDatasetForm.source_id = datasetForm.source_id || newDatasetSourceId.value || dataSources.value[0]?.id || null
  promptDatasetForm.style_dataset_id = selectedDatasetId.value || null
  promptDatasetForm.dataset_name = ''
  promptDatasetForm.dataset_code = ''
  promptDatasetForm.business_domain = ''
  promptDatasetForm.doc_text = ''
  resetPromptDatasetProgress()
}

const openPromptDatasetDialog = () => {
  if (!isFeatureEnabled('dataset_prompt_generate')) return
  resetPromptDatasetForm()
  promptDatasetVisible.value = true
}

const resetPromptDatasetProgress = () => {
  if (promptDatasetTimer) window.clearInterval(promptDatasetTimer)
  promptDatasetTimer = null
  promptDatasetStatus.value = ''
  promptDatasetStepIndex.value = -1
  promptDatasetProgress.value = 0
  promptDatasetElapsed.value = 0
}

const startPromptDatasetTimer = () => {
  if (promptDatasetTimer) window.clearInterval(promptDatasetTimer)
  const startedAt = Date.now()
  promptDatasetElapsed.value = 1
  promptDatasetTimer = window.setInterval(() => {
    promptDatasetElapsed.value = Math.max(1, Math.floor((Date.now() - startedAt) / 1000))
    if (promptDatasetLoading.value && promptDatasetProgress.value < 88) {
      promptDatasetProgress.value = Math.min(88, promptDatasetProgress.value + (promptDatasetElapsed.value > 90 ? 1 : 2))
    }
  }, 1000)
}

const setPromptDatasetStage = (index, status, progress = null) => {
  promptDatasetStepIndex.value = index
  promptDatasetStatus.value = status
  if (progress !== null) promptDatasetProgress.value = Math.max(promptDatasetProgress.value, progress)
}

const cancelPromptDatasetGeneration = () => {
  if (promptDatasetAbortController) {
    promptDatasetAbortController.abort()
    setPromptDatasetStage(promptDatasetStepIndex.value, '已停止本次生成请求，可以修改提示词后重新生成。', promptDatasetProgress.value)
  }
}

const escapeHtml = (value) => String(value ?? '')
  .replace(/&/g, '&amp;')
  .replace(/</g, '&lt;')
  .replace(/>/g, '&gt;')
  .replace(/"/g, '&quot;')
  .replace(/'/g, '&#39;')

const promptDatasetFailureLines = (err, createdDatasetId) => {
  const status = err?.response?.status
  const data = err?.response?.data || {}
  const url = err?.config?.url || '/api/bookshelves/datasets/generate-from-prompt'
  const message = data.error || err?.message || '未知错误'
  if (err?.code === 'ERR_CANCELED' || message === 'canceled') {
    return [
      '失败位置：前端主动取消请求',
      '详细报错：本次生成已停止，后端请求不再等待前端响应。',
      '建议：缩短提示词、补充关键 DDL/字段字典后重新生成；如果后端仍在跑旧请求，稍等一会儿再试。',
      '建议改代码位置：frontend/src/views/DatasetManagement.vue 的 cancelPromptDatasetGeneration；后端入口 backend/controllers/bookshelf.py。',
    ]
  }
  const lines = [
    `失败位置：${url}${status ? `（HTTP ${status}）` : ''}`,
    `详细报错：${message}`,
  ]
  if (Array.isArray(data.details) && data.details.length) {
    lines.push(`校验未通过：${data.details.join('；')}`)
  }
  if (createdDatasetId) {
    lines.push(`当前状态：数据集基础信息已创建，ID=${createdDatasetId}，书架内容保存失败；页面会切到这个数据集，方便你继续补齐。`)
  }
  if (status === 404 && url.includes('generate-from-prompt')) {
    lines.push('建议：后端没有加载“提示词生成数据集”接口，重启 backend/app.py 后再试。')
    lines.push('代码位置：backend/controllers/bookshelf.py 的 generate-from-prompt 路由、backend/app.py 蓝图注册。')
  } else if (status === 404 && url.includes('/bookshelves/datasets')) {
    lines.push('建议：这是“创建数据集”接口 404。请强刷页面，确认浏览器请求的是 /api/bookshelves/datasets；前端已自动用显式 /api 路径重试一次。')
    lines.push('代码位置：frontend/src/api/index.js 的 createBookshelfDataset；backend/controllers/bookshelf.py 的 POST /api/bookshelves/datasets。')
  } else if (status === 400) {
    lines.push('建议：补充更完整的 DDL、字段字典、LLD、示例 SQL，或先选择一个绑定数据源。')
    lines.push('代码位置：backend/controllers/bookshelf.py 的参数校验和 _validate_full_payload。')
  } else if (status >= 500) {
    lines.push('建议：优先检查默认 AI 模型/API Key、模型超时、返回 JSON 是否完整，以及 /full 保存时的字段格式。')
    lines.push('代码位置：backend/dataset_copilot/payload_generator.py、backend/controllers/bookshelf.py。')
  } else {
    lines.push('建议：打开“系统控制台 -> 日志管理”，筛选“报错”或搜索 generate-from-prompt 查看后端记录。')
  }
  return lines
}

const uniqueDatasetCode = (code) => {
  const base = String(code || `dataset_${Date.now()}`)
    .trim()
    .replace(/[^A-Za-z0-9_]+/g, '_')
    .replace(/^_+|_+$/g, '')
    .slice(0, 80) || `dataset_${Date.now()}`
  const exists = datasets.value.some(item => String(item.dataset_code || '').toLowerCase() === base.toLowerCase())
  return exists ? `${base}_${Date.now().toString().slice(-6)}` : base
}

const buildGeneratedFullPayload = (generatedPayload, sourceId = null) => {
  const payload = {}
  FULL_COLLECTION_KEYS.forEach(key => { payload[key] = Array.isArray(generatedPayload?.[key]) ? generatedPayload[key] : [] })
  if (sourceId) {
    payload.schema_definition = payload.schema_definition.map(item => ({ ...item, source_id: sourceId }))
  }
  if (generatedPayload?.report_config && typeof generatedPayload.report_config === 'object') {
    payload.report_config = generatedPayload.report_config
  }
  return payload
}

const generateDatasetFromPrompt = async () => {
  if (!isFeatureEnabled('dataset_prompt_generate')) return
  const docText = String(promptDatasetForm.doc_text || '').trim()
  if (docText.length < 80) {
    ElMessage.warning('请粘贴更完整的提示词、DDL、字段字典或业务口径，至少 80 字。')
    return
  }
  const sourceId = promptDatasetForm.source_id || newDatasetSourceId.value || dataSources.value[0]?.id || null
  if (!sourceId) {
    ElMessage.warning('请先选择或配置一个数据源。')
    return
  }

  promptDatasetLoading.value = true
  startPromptDatasetTimer()
  setPromptDatasetStage(0, '正在检查输入、数据源和参考样式...', 8)
  let createdDatasetId = null
  try {
    promptDatasetAbortController = new AbortController()
    setPromptDatasetStage(1, '正在请求后端 AI 生成接口。大段提示词会比较慢，请稍等...', 18)
    const generated = await generateBookshelfDatasetFromPrompt({
      doc_text: docText,
      source_id: sourceId,
      style_dataset_id: promptDatasetForm.style_dataset_id || undefined,
      dataset_name: promptDatasetForm.dataset_name || undefined,
      dataset_code: promptDatasetForm.dataset_code || undefined,
      business_domain: promptDatasetForm.business_domain || undefined,
    }, {
      signal: promptDatasetAbortController.signal,
    })
    setPromptDatasetStage(2, 'AI 已返回，正在检查 LLD、DDL、字段字典、Golden SQL 和 专家提示词 是否完整...', 76)
    const validationErrors = generated.validation_errors || []
    if (validationErrors.length) {
      setPromptDatasetStage(2, '生成结果未达到保存标准，请按弹窗提示补充底稿后重试。', 76)
      await ElMessageBox.alert(validationErrors.join('<br/>'), '生成结果还不完整', {
        confirmButtonText: '知道了',
        dangerouslyUseHTMLString: true,
        type: 'warning',
      })
      return
    }

    const meta = generated.dataset_meta || {}
    const createPayload = {
      dataset_code: uniqueDatasetCode(meta.dataset_code || promptDatasetForm.dataset_code),
      dataset_name: meta.dataset_name || promptDatasetForm.dataset_name || 'AI生成数据集',
      business_domain: meta.business_domain || promptDatasetForm.business_domain || meta.dataset_name || 'AI生成数据集',
      source_id: sourceId,
      description: meta.description || `由大段提示词自动生成：${meta.dataset_name || promptDatasetForm.dataset_name || 'AI生成数据集'}`,
    }
    setPromptDatasetStage(3, `正在创建数据集：${createPayload.dataset_name}`, 84)
    const created = await createBookshelfDataset(createPayload)
    createdDatasetId = created.dataset?.id
    if (!createdDatasetId) throw new Error('数据集创建成功但未返回 ID')

    setPromptDatasetStage(4, '正在保存书架内容：LLD、DDL、字段字典、Golden SQL、专家提示词...', 92)
    await saveBookshelfDatasetFull(createdDatasetId, buildGeneratedFullPayload(generated.payload || {}, sourceId))
    setPromptDatasetStage(4, '保存完成，正在刷新数据集列表...', 100)
    promptDatasetVisible.value = false
    ElMessage.success(`已生成并保存「${createPayload.dataset_name}」`)
    await loadDatasets()
    const target = datasets.value.find(item => Number(item.id) === Number(createdDatasetId))
    if (target) await selectDataset(target)
  } catch (err) {
    const details = err?.response?.data?.details
    if (Array.isArray(details) && details.length) {
      const isGenerateError = String(err?.config?.url || '').includes('generate-from-prompt')
      setPromptDatasetStage(Math.max(promptDatasetStepIndex.value, 0), isGenerateError ? 'AI 生成失败，已整理原因和建议。' : '保存前校验未通过，已整理原因和建议。', promptDatasetProgress.value)
      await ElMessageBox.alert(details.map(line => `<p>${escapeHtml(line)}</p>`).join(''), isGenerateError ? 'AI 生成失败' : '保存前校验未通过', {
        confirmButtonText: '知道了',
        dangerouslyUseHTMLString: true,
        type: isGenerateError ? 'error' : 'warning',
      })
    } else if (err?.response?.status === 404 && err?.response?.data?.error === 'API not found') {
      setPromptDatasetStage(Math.max(promptDatasetStepIndex.value, 0), '接口 404，已整理原因和建议。', promptDatasetProgress.value)
      await ElMessageBox.alert(
        promptDatasetFailureLines(err, createdDatasetId).map(line => `<p>${escapeHtml(line)}</p>`).join(''),
        '接口未找到',
        { confirmButtonText: '知道了', dangerouslyUseHTMLString: true, type: 'error' },
      )
    } else {
      setPromptDatasetStage(Math.max(promptDatasetStepIndex.value, 0), '处理失败，已整理原因和建议。', promptDatasetProgress.value)
      await ElMessageBox.alert(
        promptDatasetFailureLines(err, createdDatasetId).map(line => `<p>${escapeHtml(line)}</p>`).join(''),
        '生成数据集失败',
        { confirmButtonText: '知道了', dangerouslyUseHTMLString: true, type: 'error' },
      )
    }
    if (createdDatasetId) {
      await loadDatasets()
      const target = datasets.value.find(item => Number(item.id) === Number(createdDatasetId))
      if (target) await selectDataset(target)
    }
  } finally {
    promptDatasetLoading.value = false
    promptDatasetAbortController = null
    if (promptDatasetTimer) window.clearInterval(promptDatasetTimer)
    promptDatasetTimer = null
  }
}

// ========== 从数据源拉表 ==========
const sourceDialogVisible = ref(false); const sourceDialogSourceId = ref(null)
const sourceTables = ref([]); const selectedSourceTables = ref([])

const openSourceTableDialog = () => {
  if (!canUseDatasetFeature('dataset_source_table')) { warnReadonly(); return }
  sourceDialogVisible.value = true; sourceDialogSourceId.value = datasetForm.source_id || dataSources.value[0]?.id || null; sourceTables.value = []; selectedSourceTables.value = []
}
const loadSourceTables = async () => { if (!sourceDialogSourceId.value) { ElMessage.warning('请先选择数据源'); return }; sourceTables.value = (await getSourceTables(sourceDialogSourceId.value)).tables || [] }
const onSourceTableSelection = (rows) => { selectedSourceTables.value = rows || [] }
const appendSelectedSourceTables = () => {
  if (!canUseDatasetFeature('dataset_source_table')) { warnReadonly(); return }
  if (selectedSourceTables.value.length === 0) { ElMessage.warning('请先勾选表'); return }
  let added = 0
  selectedSourceTables.value.forEach(t => {
    if (full.schema_definition.some(x => x.table_name === t.full_table_name)) return
    full.schema_definition.push({ table_name: t.full_table_name, ddl_sql: t.ddl_sql || '', description: '', source_id: sourceDialogSourceId.value }); added++
  })
  sourceDialogVisible.value = false; ElMessage.success(`已加入 ${added} 张表`); if (added > 0) markDirty()
}

// ========== DDL Drawer ==========
const schemaEditorVisible = ref(false); const schemaEditorIndex = ref(-1)
const schemaEditor = reactive({ table_name: '', ddl_sql: '', description: '', source_id: null })
const resetSchemaEditor = () => { schemaEditor.table_name = ''; schemaEditor.ddl_sql = ''; schemaEditor.description = ''; schemaEditor.source_id = null }
const openSchemaEditor = (row = null, index = -1) => {
  if (!canUseDatasetFeature(index === -1 ? 'dataset_schema_create' : 'dataset_schema_update')) { warnReadonly(); return }
  schemaEditorIndex.value = index
  if (row) { schemaEditor.table_name = row.table_name || ''; schemaEditor.ddl_sql = row.ddl_sql || ''; schemaEditor.description = row.description || ''; schemaEditor.source_id = row.source_id || null }
  else resetSchemaEditor()
  schemaEditorVisible.value = true
}
const saveSchemaEditor = () => {
  if (!canUseDatasetFeature(schemaEditorIndex.value === -1 ? 'dataset_schema_create' : 'dataset_schema_update')) { warnReadonly(); return }
  if (!schemaEditor.table_name.trim()) { ElMessage.warning('请填写表名'); return }
  const item = { table_name: schemaEditor.table_name.trim(), ddl_sql: schemaEditor.ddl_sql || '', description: schemaEditor.description || '', source_id: schemaEditor.source_id || null }
  if (schemaEditorIndex.value >= 0) full.schema_definition[schemaEditorIndex.value] = item
  else full.schema_definition.push(item)
  schemaEditorVisible.value = false; resetSchemaEditor(); markDirty()
}
const removeSchema = (i) => {
  if (!canUseDatasetFeature('dataset_schema_delete')) { warnReadonly(); return }
  full.schema_definition.splice(i, 1); markDirty()
}
const addSchema = () => openSchemaEditor()

// ========== 数据转换 ==========
const loadTransforms = async () => {
  if (!selectedDatasetId.value) {
    transforms.value = []
    return
  }
  transformLoading.value = true
  try {
    const r = await getDatasetTransforms(selectedDatasetId.value)
    transforms.value = r.transforms || []
  } catch (error) {
    transforms.value = []
  } finally {
    transformLoading.value = false
  }
}
const resetTransformForm = () => {
  Object.assign(transformForm, {
    name: '',
    source_table: '',
    target_type: 'view',
    target_name: '',
    transform_sql: '',
    is_active: true,
    auto_run_on_sync: false,
    sync_dependency: ''
  })
}
const openTransformEditor = (row = null) => {
  if (!ensureSelectedCanEdit()) return
  transformEditId.value = row ? row.id : null
  resetTransformForm()
  if (row) {
    Object.assign(transformForm, {
      name: row.name || '',
      source_table: row.source_table || '',
      target_type: row.target_type || 'view',
      target_name: row.target_name || '',
      transform_sql: row.transform_sql || '',
      is_active: row.is_active !== false,
      auto_run_on_sync: row.auto_run_on_sync === true,
      sync_dependency: row.sync_dependency || ''
    })
  }
  transformDialogVisible.value = true
}
const closeTransformEditor = () => {
  transformDialogVisible.value = false
  transformEditId.value = null
  resetTransformForm()
}
const saveTransform = async () => {
  if (!ensureSelectedCanEdit()) return
  if (!transformForm.name.trim()) { ElMessage.warning('请输入任务名称'); return }
  if (!transformForm.source_table.trim()) { ElMessage.warning('请输入源表名'); return }
  if (!transformForm.target_name.trim()) { ElMessage.warning('请输入目标名称'); return }
  if (!transformForm.transform_sql.trim()) { ElMessage.warning('请输入转换 SQL'); return }
  transformLoading.value = true
  try {
    const payload = {
      name: transformForm.name.trim(),
      source_table: transformForm.source_table.trim(),
      target_type: transformForm.target_type,
      target_name: transformForm.target_name.trim(),
      transform_sql: transformForm.transform_sql.trim(),
      is_active: transformForm.is_active,
      auto_run_on_sync: transformForm.auto_run_on_sync,
      sync_dependency: transformForm.sync_dependency.trim()
    }
    if (transformEditId.value) {
      await updateDatasetTransform(transformEditId.value, payload)
      ElMessage.success('转换任务更新成功')
    } else {
      await createDatasetTransform(selectedDatasetId.value, payload)
      ElMessage.success('转换任务创建成功')
    }
    closeTransformEditor()
    await loadTransforms()
  } finally {
    transformLoading.value = false
  }
}
const handleDeleteTransform = async (row) => {
  if (!ensureSelectedCanEdit()) return
  try {
    await ElMessageBox.confirm(`确认删除转换任务 "${row.name}" 吗？`, '删除确认', { type: 'warning' })
    await deleteDatasetTransform(row.id)
    ElMessage.success('转换任务已删除')
    await loadTransforms()
  } catch (error) {
    if (error !== 'cancel') {
      // ElMessage.error 已由 api 拦截器处理
    }
  }
}
const handleRunTransform = async (row) => {
  transformRunLoading.value = { ...transformRunLoading.value, [row.id]: true }
  try {
    const r = await runDatasetTransform(row.id)
    ElMessage.success(r.message || '执行成功')
    await loadTransforms()
  } finally {
    transformRunLoading.value = { ...transformRunLoading.value, [row.id]: false }
  }
}
const handleTestTransformSql = async () => {
  if (!transformForm.transform_sql.trim()) { ElMessage.warning('请输入转换 SQL'); return }
  transformTestLoading.value = true
  try {
    const r = await testDatasetTransformSql({
      target_type: transformForm.target_type,
      target_name: transformForm.target_name || 'test_target',
      source_table: transformForm.source_table,
      transform_sql: transformForm.transform_sql.trim()
    })
    if (r.success) ElMessage.success(r.message || '测试成功')
    else ElMessage.error(r.error || '测试失败')
  } finally {
    transformTestLoading.value = false
  }
}
const applyOnlineTemplate = () => {
  transformForm.source_table = 'feishu_tbl_beta'
  transformForm.target_name = 'v_feishu_tbl_beta'
  transformForm.target_type = 'view'
  transformForm.transform_sql = `SELECT
  id,
  record_id,
  fields->>'状态' AS 审批状态,
  fields->>'编号' AS 编号,
  fields->>'经营主体' AS 集团,
  fields->>'事业群' AS 事业群,
  NULLIF(fields->>'行业部','') AS 行业部,
  NULLIF(fields->>'业务承接角色','') AS 细分业务,
  fields->>'层级级别' AS 层级级别,
  fields->>'任务承接人' AS 负责人,
  fields->>'任务维护人' AS 上级负责人,
  NULLIF(trim(fields->>'总任务（金额）'),'')::numeric AS 年度目标营收,
  NULLIF(trim(fields->>'年度开单金额'),'')::numeric AS 年度开单金额,
  NULLIF(trim(fields->>'总任务达成率'),'')::numeric AS 总任务达成率,
  NULLIF(trim(fields->>'当前月份任务达成率'),'')::numeric AS 当前月份任务达成率,
  NULLIF(trim(fields->>'截止当前目标阈值达成率'),'')::numeric AS 截止当前目标阈值达成率,
  NULLIF(trim(fields->>'本月开单金额'),'')::numeric AS 本月开单金额,
  NULLIF(trim(fields->>'本月当前目标阈值'),'')::numeric AS 本月当前目标阈值,
  NULLIF(trim(fields->>'年度阈值/开单差额（万）'),'')::numeric AS 年度阈值开单差额万,
  NULLIF(trim(fields->>'月度阈值/开单差额（万）'),'')::numeric AS 月度阈值开单差额万,
  NULLIF(trim(fields->>'总金额转换（以万为单位）'),'')::numeric AS 总金额转换万,
  NULLIF(trim(fields->>'年度开单金额转换（以万为单位）'),'')::numeric AS 年度开单金额转换万,
  fields->>'链接字段(勿删)' AS 组织路径,
  fields->>'当前年' AS 当前年,
  fields->>'当前月' AS 当前月,
  NULLIF(trim(fields->>'2601'),'')::numeric AS q1目标,
  NULLIF(trim(fields->>'2602'),'')::numeric AS q2目标,
  NULLIF(trim(fields->>'2603'),'')::numeric AS q3目标,
  NULLIF(trim(fields->>'2604'),'')::numeric AS q4目标
FROM {{source_table}}
WHERE fields IS NOT NULL AND fields <> '{}'::jsonb
  AND NULLIF(fields->>'编号','') IS NOT NULL`
}
const formatTime = (value) => {
  if (!value) return '-'
  const d = new Date(value)
  if (Number.isNaN(d.getTime())) return value
  return d.toLocaleString('zh-CN', { hour12: false })
}

// ========== 工具函数 ==========
const ddlPreview = (t) => { const n = String(t || '').replace(/\s+/g, ' ').trim(); return n ? (n.length > 120 ? n.slice(0, 120) + '...' : n) : '暂无 DDL' }
const jsonString = (v) => { try { return JSON.stringify(v || {}, null, 2) } catch { return '{}' } }

onMounted(async () => {
  await loadFeatureFlags()
  await Promise.all([loadDatasets(), loadDataSources()])
  if (datasets.value.length > 0) await selectDataset(datasets.value[0])
  else resetFull()
})

onUnmounted(() => {
  if (promptDatasetAbortController) promptDatasetAbortController.abort()
  if (promptDatasetTimer) window.clearInterval(promptDatasetTimer)
})
</script>

<style scoped>
.dataset-page { min-width:0; color:#18222f; }
.dataset-page-heading {display:flex;justify-content:space-between;align-items:center;gap:20px;margin-bottom:24px;}
.dataset-eyebrow{font-size:10px;letter-spacing:1.3px;color:#76818f;font-weight:600;}
.dataset-page-heading h1{font-size:25px;font-weight:600;letter-spacing:-.6px;margin:7px 0 6px;}
.dataset-page-heading p{font-size:13px;color:#74808d;}
.dataset-workspace{display:grid;grid-template-columns:270px minmax(0,1fr);border:1px solid #e1e5ea;border-radius:12px;background:#fff;overflow:hidden;min-height:650px;}
.dataset-catalog{display:flex;flex-direction:column;min-width:0;background:#fafbfc;border-right:1px solid #e5e8ed;}
.catalog-heading{display:flex;align-items:center;justify-content:space-between;padding:22px 18px 14px;}
.catalog-heading strong{font-size:13px;font-weight:600;}.catalog-heading>span{font-size:11px;color:#738192;padding:2px 7px;border-radius:5px;background:#edf0f4;}
.toolbar-col{display:flex;flex-direction:column;gap:12px;padding:0 14px 16px;border-bottom:1px solid #e9ecf0;}
.dataset-status-filter{display:flex;gap:3px;background:#eef1f4;border-radius:6px;padding:3px;}
.dataset-status-filter button{display:flex;justify-content:center;gap:7px;flex:1;align-items:center;color:#7a8592;font-size:11px;min-height:27px;border-radius:4px;}
.dataset-status-filter button[aria-pressed=true]{background:#fff;color:#26364b;box-shadow:0 1px 3px #14273d0d;}.dataset-status-filter button>span{font-size:10px;opacity:.75;}
.dataset-catalog-list{flex:1;padding:10px 8px;overflow:auto;max-height:calc(100dvh - 375px);min-height:280px;}
.dataset-tile{display:block;width:100%;text-align:left;padding:14px 12px;border:1px solid transparent;border-radius:7px;margin:2px 0 6px;background:transparent;transition:background .15s,border-color .15s;}
.dataset-tile:hover{background:#f0f3f6;}.dataset-tile.active{background:#fff;border-color:#d5dfe9;box-shadow:0 2px 5px #1a2d4306;}
.dataset-tile-head{display:flex;align-items:flex-start;gap:10px;}.dataset-asset-icon{width:23px;height:23px;flex:none;color:#6d839b;}.dataset-asset-icon svg{width:20px;height:20px;}.dataset-tile.active .dataset-asset-icon{color:#365f91;}
.dataset-tile-title{font-size:13px;font-weight:600;line-height:1.65;color:#354154;overflow-wrap:anywhere;}.dataset-tile-meta{display:block;margin:5px 0 9px 33px;font-size:10px;letter-spacing:.5px;color:#7b8795;}.dataset-tile-sub{display:flex;flex-wrap:wrap;gap:9px;font-size:10px;color:#89929d;margin-left:33px;}.asset-state{display:inline-flex;align-items:center;gap:5px;font-size:10px;font-weight:500;color:#51836f;white-space:nowrap;}.asset-state:before{content:'';width:5px;height:5px;border-radius:50%;background:#519577;}.asset-state.inactive{color:#8e96a0;}.asset-state.inactive:before{background:#a1a8b0;}.dataset-tile.inactive .dataset-tile-title{color:#8a939f;}
.catalog-footnote{margin-top:auto;padding:16px 18px;border-top:1px solid #e8ebef;font-size:10px;line-height:1.6;color:#8c96a2;}
.dataset-editor{min-width:0;background:#fff;}.dataset-identity{display:flex;justify-content:space-between;align-items:center;gap:18px;padding:24px 26px;border-bottom:1px solid #e9edf1;}.dataset-identity-copy{min-width:0;}.dataset-identity-line{display:flex;align-items:center;gap:12px;flex-wrap:wrap;}.dataset-identity h2{font-size:20px;font-weight:600;line-height:1.6;margin:8px 0 6px;letter-spacing:-.4px;}.dataset-identity-meta{display:flex;align-items:center;gap:10px;flex-wrap:wrap;color:#798592;font-size:11px;}.dataset-identity-meta i{width:3px;height:3px;border-radius:50%;background:#c4cbd3;}.dirty-indicator{color:#a47c35;font-size:10px;background:#fcf6e9;padding:2px 7px;border-radius:4px;}
.header-actions{display:flex;gap:8px;flex-wrap:wrap;justify-content:flex-end;}.header-actions :deep(.el-button+.el-button){margin-left:0;}.dataset-editor-body{padding:0 26px 26px;}
.dataset-properties{border-bottom:1px solid #eceff3;}.dataset-properties summary{display:flex;align-items:center;gap:14px;list-style:none;padding:16px 0;font-size:12px;color:#435164;cursor:pointer;}.dataset-properties summary::-webkit-details-marker,.quality-disclosure summary::-webkit-details-marker{display:none;}.properties-summary{font-size:11px;color:#8b95a2;}.dataset-properties summary svg,.quality-disclosure summary svg{width:12px;height:12px;margin-left:auto;color:#8593a3;transition:transform .15s;}.dataset-properties[open] summary svg,.quality-disclosure[open] summary svg{transform:rotate(90deg);}.dataset-properties-body{padding:4px 0 20px;}.base-form{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:4px 18px;}.base-form :deep(.el-form-item__label){font-size:11px!important;color:#6f7b8c;line-height:1.6!important;margin-bottom:7px;}.property-description{grid-column:span 2;}.property-switch-note{font-size:11px;color:#6e7d8d;margin-left:10px;}.property-danger{display:flex;align-items:center;justify-content:space-between;gap:12px;padding-top:8px;font-size:11px;color:#9099a5;}
.quality-disclosure{margin:16px 0;border:1px solid #e6ebee;border-radius:7px;}.quality-disclosure>summary{display:flex;align-items:center;gap:16px;padding:13px 16px;cursor:pointer;list-style:none;}.quality-score{font-size:23px;letter-spacing:-.6px;color:#3d6b5c;font-variant-numeric:tabular-nums;}.quality-score small{font-size:10px;color:#90a196;margin-left:3px;}.quality-summary-copy{display:flex;flex-direction:column;gap:4px;font-size:11px;color:#89948f;}.quality-summary-copy strong{font-size:12px;font-weight:500;color:#45584e;}.quality-summary-copy strong span{font-size:10px;color:#7a9585;margin-left:12px;}.quality-track{height:4px;background:#edf1ef;border-radius:4px;max-width:160px;flex:1;margin-left:auto;overflow:hidden;}.quality-track i{display:block;height:100%;background:#6d9b84;border-radius:4px;}.quality-detail-label{font-size:10px;color:#7c8b85;}.quality-disclosure summary svg{margin-left:0;}.quality-overview{padding:0 16px 16px;}.quality-checks{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px;}.quality-check{display:flex;justify-content:space-between;gap:8px;font-size:10px;color:#7a8790;padding:9px 0;border-top:1px solid #edf0f2;}.quality-check strong{font-weight:500;color:#4f6f60;white-space:nowrap;}.quality-check small{font-size:10px;color:#a0a9af;}.quality-gaps{font-size:11px;line-height:1.7;color:#957a46;margin-top:10px;}
.knowledge-workspace{margin-top:23px;min-width:0;}.knowledge-category-nav{display:flex;align-items:center;gap:24px;border-bottom:1px solid #e9edf1;}.knowledge-category-nav button{font-size:13px;font-weight:500;color:#8a94a1;padding:0 0 12px;border-bottom:2px solid transparent;display:flex;align-items:center;gap:7px;}.knowledge-category-nav button[aria-pressed=true]{color:#365f91;border-color:#365f91;}.knowledge-category-nav button span{font-size:10px;background:#f0f3f7;color:#8c99a8;min-width:18px;text-align:center;line-height:17px;border-radius:4px;}.knowledge-section-nav{display:flex;gap:6px;flex-wrap:wrap;margin:16px 0 22px;}.knowledge-section-nav button{font-size:11px;color:#7c8897;padding:7px 11px;border:1px solid transparent;border-radius:5px;}.knowledge-section-nav button span{font-size:10px;color:#9aa6b4;margin-left:7px;}.knowledge-section-nav button[aria-current=page]{color:#385b85;background:#f1f5f9;border-color:#e2e9f1;}.knowledge-section-intro{display:flex;justify-content:space-between;gap:16px;margin-bottom:20px;align-items:flex-start;}.knowledge-section-intro h3{font-size:15px;font-weight:600;color:#283647;margin-bottom:6px;}.knowledge-section-intro p{font-size:11px;line-height:1.7;color:#82909d;}.knowledge-section-intro>span{font-size:10px;color:#96a0ac;white-space:nowrap;padding-top:2px;}.knowledge-content-tabs :deep(>.el-tabs__header){display:none;}.knowledge-content-tabs :deep(.el-tabs__content){min-width:0;overflow:hidden;}.knowledge-content-tabs :deep(.el-table){--el-table-border-color:#e9edf2;--el-table-header-bg-color:#f8fafb;font-size:12px;}.knowledge-content-tabs :deep(.el-table th.el-table__cell){font-weight:500;font-size:11px;color:#7b8795;}.knowledge-content-tabs :deep(.el-table .el-table__cell){padding:11px 0;}.knowledge-content-tabs :deep(.el-table--border .el-table__cell){border-right:none;}.knowledge-content-tabs :deep(.el-table--border::after){display:none;}.toolbar{display:flex;gap:8px;flex-wrap:wrap;justify-content:flex-end;margin-bottom:12px;}.toolbar :deep(.el-button+.el-button){margin-left:0;}
.readonly-alert{margin:16px 0;}.readonly-summary-card{padding:22px;border:1px solid #e7ebf0;border-radius:8px;background:#fafbfc;margin-top:20px;}.readonly-summary-title{font-size:14px;font-weight:600;}.readonly-summary-desc{font-size:12px;color:#83909d;line-height:1.8;margin:9px 0 20px;}.readonly-summary-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px;}.readonly-summary-grid span{display:block;font-size:10px;color:#8794a3;margin-bottom:6px;}.readonly-summary-grid strong{font-size:12px;color:#536276;}
.dataset-page button:focus-visible,.dataset-page summary:focus-visible{outline:2px solid #6c8cad;outline-offset:3px;}
@media(max-width:1300px){.dataset-workspace{grid-template-columns:230px minmax(0,1fr);}.dataset-identity{align-items:flex-start;flex-direction:column;}.dataset-identity .header-actions{width:100%;justify-content:flex-start;}.quality-track{max-width:90px;}.quality-checks{grid-template-columns:repeat(2,minmax(0,1fr));}.base-form{grid-template-columns:repeat(2,minmax(0,1fr));}.property-description{grid-column:span 1;}}
@media(max-width:900px){.dataset-workspace{grid-template-columns:1fr;}.dataset-catalog{border-right:0;border-bottom:1px solid #e5e8ed;}.catalog-heading{padding:16px 18px 10px;}.toolbar-col{display:grid;grid-template-columns:minmax(150px,1fr) minmax(180px,1fr);}.toolbar-col>.el-select{display:flex;grid-column:1/-1;}.dataset-catalog-list{display:flex;gap:8px;min-height:0;max-height:220px;overflow:auto;padding:10px 14px;}.dataset-tile{min-width:230px;max-width:270px;}.catalog-footnote{display:none;}.dataset-page-heading{align-items:flex-start;}.dataset-page-heading .header-actions{max-width:50%;}}
@media(max-width:600px){.dataset-page-heading{flex-direction:column;gap:15px;}.dataset-page-heading .header-actions{max-width:none;}.dataset-identity{padding:20px;}.dataset-editor-body{padding:0 16px 20px;}.dataset-identity h2{font-size:18px;}.quality-track,.quality-detail-label{display:none;}.quality-disclosure>summary{gap:12px;}.quality-disclosure summary svg{margin-left:auto;}.knowledge-category-nav{gap:18px;}.knowledge-category-nav button{font-size:12px;}.base-form{grid-template-columns:1fr;}.toolbar-col{display:flex;}.dataset-catalog-list{max-height:165px;}.properties-summary{font-size:10px;}.quality-checks{grid-template-columns:1fr;}.knowledge-section-intro>span{display:none;}.readonly-summary-grid{grid-template-columns:1fr;}}
.section-title { margin: 18px 0 10px; font-weight: 700; font-size: 14px; color: var(--text-title, #111827); }
.muted-text { color: var(--text-muted, #9CA3AF); font-size: 12px; line-height: 1.5; }
.text-preview { font-size: 12px; color: var(--text-body, #6B7280); line-height: 1.5; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; max-width: 400px; }
.schema-name-cell { font-weight: 600; color: var(--text-title, #111827); }
.ddl-preview-line { font-family: 'JetBrains Mono', Consolas, Monaco, monospace; font-size: 12px; line-height: 1.4; color: var(--text-body, #6B7280); word-break: break-word; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; max-width: 500px; }
.schema-editor-shell { display: flex; flex-direction: column; gap: 18px; height: 100%; }
.schema-editor-header { display: flex; align-items: center; justify-content: space-between; gap: 16px; }
.schema-editor-subtitle { margin-top: 6px; color: var(--text-muted, #9CA3AF); font-size: 13px; }
.schema-editor-form { flex: 1; }
:global(.prompt-dataset-dialog) {
  max-width: calc(100vw - 48px);
}
:global(.prompt-dataset-dialog .el-dialog__body) {
  max-height: calc(100vh - 170px);
  overflow: auto;
  padding-top: 18px;
}
.prompt-generate-shell { display: flex; flex-direction: column; gap: 14px; }
.prompt-generate-form {
  margin-top: 2px;
  padding: 16px 16px 2px;
  border: 1px solid #F2F5F4;
  border-radius: 4px;
  background: #F2F5F4;
}
.prompt-progress-panel {
  border: 1px solid #eff6ff;
  background: linear-gradient(180deg, #F2F5F4 0%, #eff6ff 100%);
  border-radius: 4px;
  padding: 14px 16px;
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.75);
}
.prompt-progress-head {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 10px;
}
.prompt-progress-head strong {
  display: block;
  color: #111827;
  font-size: 14px;
}
.prompt-progress-head span {
  display: block;
  margin-top: 4px;
  color: #6B7280;
  font-size: 13px;
  line-height: 1.5;
}
.prompt-progress-head em {
  flex: 0 0 auto;
  color: #1d4ed8;
  font-style: normal;
  font-weight: 600;
}
.prompt-stage-strip {
  display: grid;
  grid-template-columns: repeat(5, minmax(0, 1fr));
  gap: 8px;
  margin-top: 12px;
}
.prompt-stage {
  display: flex;
  align-items: center;
  gap: 8px;
  min-height: 38px;
  padding: 7px 9px;
  border: 1px solid #F3F4F6;
  border-radius: 4px;
  color: #6B7280;
  background: rgba(255, 255, 255, 0.72);
}
.prompt-stage span {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 22px;
  height: 22px;
  border-radius: 999px;
  color: #6B7280;
  background: #F3F4F6;
  font-size: 12px;
  font-weight: 800;
  flex-shrink: 0;
}
.prompt-stage strong {
  min-width: 0;
  font-size: 13px;
  line-height: 1.25;
}
.prompt-stage.done,
.prompt-stage.active {
  border-color: #eff6ff;
  color: #1d4ed8;
  background: #ECFDF5;
}
.prompt-stage.done span,
.prompt-stage.active span {
  color: #fff;
  background: #1d4ed8;
}
.prompt-stage.active {
  box-shadow: 0 8px 18px rgba(0, 0, 0, 0.12);
}
.prompt-progress-note {
  margin-top: 10px;
  color: #6B7280;
  font-size: 12px;
  line-height: 1.6;
}
.mono-textarea :deep(textarea) { font-family: 'JetBrains Mono', Consolas, Monaco, monospace; font-size: 13px; line-height: 1.6; }
@media (max-width: 900px) {
  .prompt-stage-strip { grid-template-columns: repeat(2, minmax(0, 1fr)); }
}
</style>

```

---

## 问数工作台核心页面 (src/views/AskDesk.vue)

**文件路径**: `datapivot-demo/frontend/src/views/AskDesk.vue`

```vue
<template>
  <div class="ax-page">
    <div class="ax-shell">
      <section class="ax-workspace" :class="{ 'is-detail-hidden': !detailPanelVisible }">
        <!-- 历史按需打开，不占用分析画布 -->
        <SessionSidebar
          ref="historyPanelRef"
          :busy="isRunning"
          :allow-new-chat="featureAccess.ask_new_chat"
          :sessions="historySessions"
          :active-session-id="activeHistoryId"
          :allow-clear="canUseFeature('app_history_clear')"
          :allow-delete="canUseFeature('app_history_delete')"
          @new-chat="handleNewChat"
          @select-session="handleSelectHistorySession"
          @delete-session="handleDeleteHistorySession"
          @clear-all="handleClearAllSessions"
        />

        <!-- 📌 左侧/中间 对话区-->
        <div class="ax-chat-panel" :class="{ 'is-detail-hidden': !detailPanelVisible }">
          <!-- 头部组件-->
          <div class="ax-content-track ax-header-track">
            <ChatHeader
              :flow="requestedFlow"
              :show-panel="detailPanelVisible"
              :allow-toggle-panel="featureAccess.debug_execution_trace && featureAccess.ask_field_execution_trace"
              :allow-new-chat="featureAccess.ask_new_chat"
              @toggle-panel="togglePanel"
              @new-chat="handleNewChat"
              @show-history="focusSidebarHistory"
            />
          </div>

          <!-- 只读视图提示：正在查看历史，后台有任务执行中/待确认/已完成/失败 -->
          <div v-if="isViewingReadonly && runningTaskStatus !== 'idle'" class="ax-readonly-banner" :class="`banner-${runningTaskStatus}`" @click="handleReturnToRunning">
            <span v-if="runningTaskStatus === 'running'" class="ax-readonly-banner-icon ax-spin-ring-small">
              <span class="ax-spin-ring-track-small"></span>
              <span class="ax-spin-ring-bar-small"></span>
            </span>
            <span v-else-if="runningTaskStatus === 'pending_confirmation'" class="ax-readonly-banner-icon">⚠️</span>
            <span v-else-if="runningTaskStatus === 'completed'" class="ax-readonly-banner-icon">✅</span>
            <span v-else class="ax-readonly-banner-icon">❌</span>
            <span class="ax-readonly-banner-text">
              <template v-if="runningTaskStatus === 'running'">正在查看历史任务，后台有任务正在执行中，点击此处跳回执行中的任务</template>
              <template v-else-if="runningTaskStatus === 'pending_confirmation'">后台任务需要确认口径，点击此处返回确认</template>
              <template v-else-if="runningTaskStatus === 'completed'">后台任务已执行完成，点击此处查看结果</template><template v-else-if="runningTaskStatus === 'partial'">后台任务仅形成部分结果，点击此处查看待完成项</template>
              <template v-else>后台任务执行失败，点击此处查看详情</template>
            </span>
            <!-- i18n: datapulse.task.readonlyBanner -->
          </div>

          <!-- 会话滚动区-->
          <div class="ax-chat-body" ref="chatBodyRef">
            <div class="ax-content-track ax-chat-content">
            <!-- 欢迎首屏 -->
            <WelcomeScreen
              v-if="messages.length === 0"
              :flow="requestedFlow"
              :welcome-text="requestedFlow === 'advanced' ? '从一个业务疑问开始，先制定计划，再用证据逐步验证。' : '把业务问题交给我，获取口径清晰、可以核对的答案。'"
              :common-questions="commonQuestions"
              :common-questions-loading="commonQuestionsLoading"
              :allow-quick-ask="featureAccess.ask_quick_ask"
              :allow-refresh-questions="featureAccess.ask_quick_refresh"
              @quick-ask="quickAsk"
              @refresh-questions="refreshCommonQuestions"
            />

            <!-- 消息列表 -->
            <div class="ax-msg-list">
              <div v-for="msg in displayMessages" :key="msg.id" class="ax-msg-wrap">
                <!-- 用户气泡 -->
                <UserBubble
                  v-if="msg.role === 'user'"
                  :content="msg.content"
                  :disabled="isRunning"
                  :allow-copy="featureAccess.ask_question_copy"
                  :allow-edit="featureAccess.ask_question_edit"
                  :allow-rerun="featureAccess.ask_question_rerun"
                  @copy="copyQuestion(msg)"
                  @edit="editQuestion(msg)"
                  @rerun="rerunQuestion(msg)"
                />

                <!-- AI 回复 -->
                <div v-else class="ax-ai-wrap">
                  <div class="ax-ai-meta">
                    <div class="ax-ai-avatar" aria-label="脉策经营分析助手头像">
                      <svg class="ax-ai-avatar-svg" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" focusable="false">
                        <defs>
                          <linearGradient id="aiRingChat" x1="0%" y1="0%" x2="100%" y2="100%">
                            <stop offset="0%" stop-color="#14B8A6" />
                            <stop offset="100%" stop-color="#0E7490" />
                          </linearGradient>
                          <linearGradient id="aiDiscChat" x1="0%" y1="0%" x2="0%" y2="100%">
                            <stop offset="0%" stop-color="#FFFFFF" />
                            <stop offset="100%" stop-color="#F0FDFA" />
                          </linearGradient>
                        </defs>
                        <circle cx="50" cy="50" r="48" fill="url(#aiDiscChat)" />
                        <circle cx="50" cy="50" r="46" fill="none" stroke="url(#aiRingChat)" stroke-width="3.5" />
                        <path d="M28 62 L42 40 L52 52 L62 36 L72 44" fill="none" stroke="#0D9488" stroke-width="5" stroke-linecap="round" stroke-linejoin="round" />
                        <circle cx="72" cy="44" r="4.5" fill="#0D9488" />
                      </svg>
                    </div>
                    <span class="ax-ai-name">DataPulse AI 经营分析顾问</span>
                  </div>
                  <div class="ax-ai-cards">
                    <!-- 加载中-->
                    <div v-if="msg.loading && !displayLogs.length" class="ax-thinking-loading">
                      <div class="ax-dots">
                        <span></span><span></span><span></span>
                      </div>
                      <span class="ax-thinking-text">正在分析问题意图并规划路径...</span>
                    </div>

                    <!-- 结构化解析条（响应层聚合，后端开关+角色门控；确认卡/纠正卡消息不出条）。置顶：先看到"系统怎么理解"，再看执行过程。运行中显示实时条（理解完成即推），终态以 result.parse_bar 为准 -->
                    <ParseBar
                      v-if="parseBarFor(msg)"
                      :bar="parseBarFor(msg)"
                      :dataset-id="getParseBarDatasetId(msg)"
                      :editable="!isRunning && !isViewingReadonly"
                      @ask="handleParseBarAsk(msg, $event)"
                    />

                    <AskProcessView
                      v-if="workflowFor(msg)?.run_id"
                      :workflow="workflowFor(msg)"
                      :result="msg.data"
                      :status="msg.loading ? 'running' : msg.data?.aborted ? 'canceled' : msg.data?.error ? 'error' : 'completed'"
                      :readonly="isViewingReadonly"
                      :allow-inspector="featureAccess.debug_execution_trace && featureAccess.ask_field_execution_trace"
                      :allow-retry="featureAccess.ask_quick_ask && featureAccess.ask_send_question && !isViewingReadonly && !isRunning"
                      @inspect="openActivityInspector(msg,$event)"
                      @retry="draftAnswerFollowUp(msg.data?.question || '')"
                      :busy="Boolean(msg.loading || confirmationSubmitting[msg.id])"
                      :allow-technical="featureAccess.debug_execution_trace && featureAccess.ask_field_generated_sql"
                      :render-chart="renderChartSpec"
                      :allow-auto-chart="featureAccess.ask_chart_auto_infer"
                      :allow-download="featureAccess.ask_report_download"
                      @download-report="downloadResearchReport(msg)"
                      @start-plan="doConfirm({ label: '确认研究计划', plan_branch_ids: $event }, msg)"
                    />
                    <PlanCard v-else :route="msg.data?.route" />

                    <!-- 错字短路纠正卡（第 0 层快检命中：只出此卡，不进流水线） -->
                    <div v-if="msg.data?.early_clarify" class="ax-early-clarify">
                      <div class="ax-early-clarify-head">
                        <span class="ax-clarify-icon">?</span>
                        <span class="ax-early-clarify-title">
                          {{ msg.data.clarify_suggestion?.reason || '这个问题里可能有错字' }}
                        </span>
                      </div>
                      <div class="ax-early-clarify-body">
                        <span class="ax-early-clarify-label">你是不是想问：</span>
                        <button
                          v-for="(cand, ci) in (msg.data.clarify_suggestion?.candidates || [])"
                          :key="ci"
                          class="ax-clarify-chip ax-early-clarify-chip"
                          :disabled="isRunning"
                          @click.stop.prevent="applyClarifySuggestion(cand)"
                        >{{ cand }}</button>
                      </div>
                      <button
                        class="ax-early-clarify-continue"
                        :disabled="isRunning"
                        @click.stop.prevent="resendOriginalQuestion(msg)"
                      >没问题，按原问题继续查</button>
                      <div class="ax-clarify-freeform">
                        <input
                          v-model="clarifyDrafts[msg.id]"
                          class="ax-clarify-input"
                          :disabled="isRunning"
                          placeholder="都不是？输入你想问的"
                          @keydown.enter.exact.prevent="handleClarifyDraftEnter($event, msg)"
                          @click.stop
                        />
                        <button
                          class="ax-clarify-send"
                          :disabled="isRunning || !String(clarifyDrafts[msg.id] || '').trim()"
                          @click.stop.prevent="submitClarifyDraft(msg)"
                        >发送</button>
                      </div>
                    </div>

                    <!-- 纠正条（守门员预览，后端按角色门控，默认仅超管可见） -->
                    <div v-if="msg.data?.clarify_suggestion && !msg.data?.early_clarify" class="ax-clarify-strip">
                      <span class="ax-clarify-icon">?</span>
                      <span class="ax-clarify-text">
                        已按「{{ msg.data.clarify_suggestion.interpretation }}」理解
                        <span v-if="msg.data.clarify_suggestion.reason" class="ax-clarify-reason">
                          {{ msg.data.clarify_suggestion.reason }}
                        </span>
                      </span>
                      <span class="ax-clarify-chips">
                        <button
                          v-for="(cand, ci) in msg.data.clarify_suggestion.candidates"
                          :key="ci"
                          class="ax-clarify-chip"
                          :disabled="isRunning"
                          @click.stop.prevent="applyClarifySuggestion(cand)"
                        >{{ cand }}</button>
                      </span>
                      <span class="ax-clarify-freeform ax-clarify-freeform-inline">
                        <input
                          v-model="clarifyDrafts[msg.id]"
                          class="ax-clarify-input"
                          :disabled="isRunning"
                          placeholder="都不是？输入你想问的"
                          @keydown.enter.exact.prevent="handleClarifyDraftEnter($event, msg)"
                          @click.stop
                        />
                        <button
                          class="ax-clarify-send"
                          :disabled="isRunning || !String(clarifyDrafts[msg.id] || '').trim()"
                          @click.stop.prevent="submitClarifyDraft(msg)"
                        >发送</button>
                      </span>
                    </div>

                    <!-- 思考过程卡（可折叠）-->
                    <ThinkingCard
                      v-if="shouldShowThinkingCard(msg)"
                      :steps="getThinkingSteps(msg)"
                      :loading="msg.loading"
                      :is-open="thinkingOpen[msg.id]"
                      @toggle="toggleThinking(msg.id)"
                    />

                    <!-- 确认口径卡-->
                    <div v-if="!msg.data?.workflow && shouldShowResultHandoff(msg)" class="ax-flow-handoff">
                      <div class="ax-flow-handoff-top">
                        <div class="ax-flow-handoff-kicker">执行已完成</div>
                        <span v-if="getAskFlowLabel(msg)" class="ax-flow-badge" :class="getAskFlowClass(msg)">
                          {{ getAskFlowLabel(msg) }}
                        </span>
                      </div>
                      <div class="ax-flow-handoff-title">正在整理结果摘要与报告内容</div>
                      <div class="ax-flow-handoff-desc">
                        执行轨迹已经沉淀完成，下面将继续承接结果摘要、报告内容和附件产物。                      </div>
                    </div>

                    <div v-if="shouldShowConfirmationCard(msg)" class="ax-card ax-confirm-card">
                      <div class="ax-confirm-header">
                        <span class="ax-confirm-badge">需要确认</span>
                        <span class="ax-confirm-q">{{ msg.data.confirmation_question }}</span>
                      </div>
                      <div class="ax-confirm-opts">
                        <div class="ax-confirm-list">
                          <button
                            v-for="(opt, idx) in visibleConfirmationOptions(msg)"
                            :key="getConfirmOptionKey(opt)"
                            class="ax-confirm-row"
                            :class="{ 'ax-confirm-row-top': idx === 0 }"
                            :disabled="isRunning || confirmationSubmitting[msg.id]"
                            @click.stop.prevent="doConfirm(opt, msg)"
                          >
                            <span class="ax-confirm-rank">{{ idx + 1 }}</span>
                            <span class="ax-confirm-info">
                              <span class="ax-confirm-row-label">
                                {{ getConfirmOptionLabel(opt) }}
                                <span v-if="opt.recommended" class="ax-confirm-recommended">推荐</span>
                              </span>
                              <span v-if="getConfirmOptionDescription(opt)" class="ax-confirm-row-desc">
                                {{ getConfirmOptionDescription(opt) }}
                              </span>
                            </span>
                            <span class="ax-confirm-spacer"></span>
                            <span v-if="shouldShowConfirmOptionScore(msg, opt)" class="ax-confirm-score">
                              {{ getConfirmOptionScore(opt) }}分
                            </span>
                          </button>
                        </div>
                        <button
                          v-if="(msg.data.confirmation_options || []).length > 4"
                          class="ax-confirm-toggle"
                          :disabled="isRunning || confirmationSubmitting[msg.id]"
                          @click.stop.prevent="toggleConfirmOptions(msg.id)"
                        >
                          {{ confirmExpanded[msg.id] ? '收起' : `展开更多 (${msg.data.confirmation_options.length - 4})` }}
                        </button>
                      </div>
                      <div class="ax-confirm-freeform">
                        <textarea
                          v-model="confirmationDrafts[msg.id]"
                          class="ax-confirm-textarea"
                          :disabled="isRunning || confirmationSubmitting[msg.id]"
                          placeholder="都不合适？补充说明继续分析，例如：按华东区域战区口径。"
                          @keydown.enter.exact.prevent="handleConfirmationDraftEnter($event, msg)"
                          @click.stop
                        ></textarea>
                        <button
                          class="ax-confirm-send"
                          :disabled="isRunning || confirmationSubmitting[msg.id] || !String(confirmationDrafts[msg.id] || '').trim()"
                          @click.stop.prevent="submitConfirmationDraft(msg)"
                        >
                          发送补充说明
                        </button>
                      </div>
                    </div>

                    <div v-else-if="shouldShowConfirmationSubmitted(msg)" class="ax-card ax-confirm-submitted">
                      <div class="ax-confirm-submitted-head">
                        <span class="ax-confirm-submitted-dot"></span>
                        <span class="ax-confirm-submitted-title">已提交确认，正在继续执行</span>
                      </div>
                      <div class="ax-confirm-submitted-desc">
                        系统已收到老板确认口径，正在继续生成 SQL 与后续分析结果。                      </div>
                    </div>

                    <div
                      v-if="!msg.data?.research && shouldShowResultChain(msg)"
                      class="ax-result-chain"
                      :ref="el => setResultChainRef(msg.id, el)"
                    >
                    <ResultDigestCard
                      v-if="!(msg.data?.research || msg.data?.research_plan) && (getReport(msg) || getPrimaryDataset(msg))"
                      :title="getResultTitle(msg)"
                      :display-title="msg.data?.display_title || ''"
                      :question="msg.data?.question || session.state.question"
                      :report="getReport(msg)"
                      :dataset="getPrimaryDataset(msg)"
                      :datasets="getDatasets(msg)"
                      :route="msg.data?.route || null"
                      :flow-label="getAskFlowLabel(msg)"
                      :flow-class="getAskFlowClass(msg)"
                      :flow-hint="getAskFlowHint(msg)"
                      :show-details-button="featureAccess.ask_report_details"
                      :allow-download="featureAccess.ask_report_download"
                      :allow-technical="featureAccess.debug_execution_trace && featureAccess.ask_field_generated_sql"
                      :allow-auto-chart="featureAccess.ask_chart_auto_infer"
                      :render-chart="renderChartSpec"
                      :allow-follow-up="featureAccess.ask_quick_ask && featureAccess.ask_send_question && !isRunning && !isViewingReadonly"
                      @follow-up="draftAnswerFollowUp"
                      @view-details="openDetailPanel(msg)"
                      @view-report="openMessageReport(msg.data)"
                    />

                    <div
                      v-else-if="shouldShowResultChain(msg)"
                      class="ax-result-empty"
                    >
                      <div class="ax-result-empty-icon">📭</div>
                      <div class="ax-result-empty-title">未查询到可用数据</div>
                      <div class="ax-result-empty-desc">
                        执行链路已完成，但当前结果中没有可展示的数据。可能原因：当前账号权限范围未覆盖该对象、问题条件未命中任何记录，或数据集配置已变更。可尝试切换账号、调整问题范围，或联系管理员检查数据权限。
                      </div>
                    </div>

                    <!-- 状态提示卡-->
                    </div>
                    <div v-if="msg.data?.aborted" class="ax-card ax-cancel-card">
                      <span class="ax-cancel-icon" aria-hidden="true">
                        <span class="ax-cancel-icon-core"></span>
                      </span>
                      <div class="ax-cancel-copy">
                        <div class="ax-cancel-kicker">FLOW INTERRUPTED</div>
                        <div class="ax-cancel-title">本轮问数已取消</div>
                        <div class="ax-cancel-desc">已请求停止。正在执行的操作将在返回或超时后退出，后续步骤不再启动。</div>
                      </div>
                    </div>
                    <div v-if="msg.data?.error" class="ax-card ax-error-card" role="alert">
                      <span>❌</span>
                      <span>{{ msg.data.error }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            </div>
          </div>

          <!-- 底部输入区-->
          <div class="ax-content-track ax-composer-track">
            <QuestionQueue :items="questionQueue" :paused="queuePaused" :reason="queueReason" :busy="isRunning" :disabled="isViewingReadonly || !featureAccess.ask_send_question" @resume="resumeQuestionQueue" @pause="pauseQuestionQueue('已手动暂停，当前问题继续执行')" @remove="removeQueuedQuestion" @edit="editQueuedQuestion" @move-up="questionQueue=moveQuestionUp(questionQueue,$event)" @clear="clearQuestionQueue" />
            <div v-if="queueDraftFlow" class="queue-draft-context">正在编辑队列问题 · {{ queueDraftFlow==='advanced'?'高阶研究':'普通问数' }}<button @click="queueDraftFlow=''">改用当前模式</button></div>
            <ComposerArea
              :queue-mode="isRunning || questionQueue.length>0 || session.state.status==='waiting_confirmation'"
              :flow="queueDraftFlow || requestedFlow"
              :class="{ 'ax-composer-narrow': !detailPanelVisible }"
              v-model:query="query"
              v-model:dataset-id="datasetId"
              v-model:model-id="modelId"
              :datasets="datasets"
              :ai-models="aiModels"
              :is-running="isRunning"
              :disabled="isViewingReadonly"
              :allow-send="featureAccess.ask_send_question"
              :allow-stop="featureAccess.ask_stop_run"
              :allow-dataset-select="featureAccess.ask_dataset_select"
              :allow-model-select="featureAccess.ask_model_select"
              :status-text="isRunning || session.state.status === 'completed' ? statusBarText : ''"
              :status-elapsed="isRunning ? `${elapsed}s` : ''"
              :status-tone="taskOutcome(session.state.result,{status:session.state.status,busy:isRunning,workflow:session.state.workflow}).status"
              :status-flow-label="activeAskFlowLabel"
              :status-flow-class="activeAskFlowClass"
              :status-flow-hint="activeAskFlowLabel ? activeAskFlowHint : ''"
              @send="handleSend"
              @stop="handleStop"
              @dataset-change="handleDatasetChange"
            />
          </div>
        </div>

        <!-- ██ 右侧 决策推导透视面板（全新设计） -->
        <transition name="ax-panel-slide">
          <div v-if="detailPanelVisible" class="ax-detail-panel-container">
            <ReasoningPanel
              :logs="inspectionBusy || inspectionResult === session.state.result ? displayLogs : []"
              :status="inspectionBusy ? 'running' : ''"
              :workflow="inspectionWorkflow"
              :result="inspectionResult"
              :busy="inspectionBusy"
              :allow-technical="featureAccess.ask_field_generated_sql"
              :allow-retry="featureAccess.ask_quick_ask && featureAccess.ask_send_question && !isViewingReadonly && !isRunning"
              :focus-phase="inspectorFocusPhase"
              :allow-report="featureAccess.ask_report_details"
              @view-report="openMessageReport(inspectionResult)"
              @retry="draftAnswerFollowUp(inspectionResult?.question || session.state.question)"
              @close="togglePanel"
            >
              <template #content="{ log, index }">
                <div v-if="log.sql && featureAccess.ask_field_generated_sql" class="ax-log-section">
                  <div class="ax-log-section-title">{{ log.sqlTitle || '生成 SQL' }}</div>
                  <SqlBlock :sql="log.sql" :allow-copy="featureAccess.ask_sql_copy" />
                </div>

                <div v-if="log.chartData" class="ax-log-section">
                  <div class="ax-log-section-title">{{ log.chartTitle || '图表预览' }}</div>
                  <button v-if="featureAccess.chart_viewer" class="ax-ghost-btn ax-log-inline-action" @click="openChartViewer(log.chartData, log.chartTitle || '图表预览')">放大查看</button>
                  <div class="ax-chart-embed" :ref="el => initLogChart(el, log.chartData, index)"></div>
                </div>

                <div v-if="log.tableRows?.length" class="ax-log-section">
                  <div class="ax-log-section-title">{{ log.tableTitle || '结果预览' }}</div>
                  <div class="ax-mini-table-wrap">
                    <el-table :data="log.tableRows.slice(0, 5)" size="small" border class="ax-mini-table">
                      <el-table-column v-for="c in log.tableColumns" :key="c" :prop="c" :label="c" min-width="100" show-overflow-tooltip />
                    </el-table>
                    <div v-if="log.tableRows.length > 5" class="ax-table-more">共 {{ log.tableRows.length }} 行</div>
                  </div>
                </div>

              </template>
            </ReasoningPanel>

            </div>
          </transition>
      </section>
    </div>

    <el-dialog
      v-model="reportViewerVisible"
      title=""
      :fullscreen="reportDialogFullscreen"
      :width="reportDialogFullscreen ? undefined : 'min(1280px, 94vw)'"
      top="4vh"
      class="ax-report-dialog"
      destroy-on-close
    >
      <div class="ax-report-dialog-body">
        <div class="ax-report-dialog-head">
              <div class="ax-report-dialog-title-block">
            <h3 class="ax-report-dialog-title">数据分析报告</h3>
            <p v-if="reportViewerTitle" class="ax-report-dialog-subtitle">{{ reportViewerTitle }}</p>
          </div>
          <div class="ax-report-dialog-actions">
            <button class="ax-secondary-btn" @click="reportDialogFullscreen = !reportDialogFullscreen">
              <span class="ax-btn-label">{{ reportDialogFullscreen ? '退出全屏' : '全屏查看' }}</span>
            </button>
            <button class="ax-secondary-btn" @click="reportViewerVisible = false">
              <span class="ax-btn-label">关闭</span>
            </button>
          </div>
        </div>
        <iframe class="html-report-reader" title="完整 HTML 分析报告" sandbox="" :srcdoc="reportViewerResearch ? buildResearchReportHtml(reportViewerResearch,{allowAutoChart:featureAccess.ask_chart_auto_infer}) : answerHtml(reportViewerTitle,reportViewerDatasets,reportViewerReport)"></iframe>
      </div>
    </el-dialog>

    <el-dialog
      v-model="chartViewerVisible"
      :title="chartViewerTitle"
      width="min(980px, 92vw)"
      top="8vh"
      class="ax-chart-dialog"
      destroy-on-close
    >
      <div class="ax-chart-dialog-body">
        <div v-if="chartViewerHasTable" class="ax-chart-dialog-head">
          <div class="ax-chart-dialog-kicker">DETAIL VIEW</div>
          <div class="ax-chart-dialog-switch">
            <button
              type="button"
              class="ax-chart-switch-btn"
              :class="{ 'is-active': chartViewerMode === 'chart' }"
              @click="chartViewerMode = 'chart'"
            >
              图表
            </button>
            <button
              type="button"
              class="ax-chart-switch-btn"
              :class="{ 'is-active': chartViewerMode === 'table' }"
              @click="chartViewerMode = 'table'"
            >
              数据表
            </button>
          </div>
        </div>
        <div v-if="chartViewerMode === 'chart' && chartViewerSpec?.chartType === 'metric'" class="ax-insight-metric ax-insight-metric-large">
          <div class="ax-insight-metric-value">{{ chartViewerSpec.value }}</div>
          <div class="ax-insight-metric-label">{{ chartViewerSpec.label }}</div>
        </div>
        <div v-else-if="chartViewerMode === 'chart'" ref="chartDialogRef" class="ax-chart-dialog-canvas"></div>
        <div v-else class="ax-chart-dialog-table">
          <div class="ax-chart-dialog-table-meta">
            <span>{{ chartViewerTableColumns.length }} 列</span>
            <span>{{ chartViewerTableRows.length }} 行</span>
          </div>
          <el-table :data="chartViewerTableRows" size="small" border height="68vh" style="width: 100%">
            <el-table-column
              v-for="column in chartViewerTableColumns"
              :key="column"
              :prop="column"
              :label="column"
              min-width="140"
              show-overflow-tooltip
            />
          </el-table>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { computed, nextTick, onActivated, onDeactivated, onMounted, onUnmounted, reactive, ref, watch } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { marked } from 'marked'
import { buildResearchReportHtml } from '../utils/researchReport'
import * as echarts from 'echarts'
import { getBookshelfDatasets, getCommonQuestions, getActiveAIModels, recordParseBarFeedback, getAskCapabilities } from '../api/index'
import { useDataPulseSession } from '../state/askDeskSession'
import { getSessionCache, setSessionCache } from '../state/sessionCache'
import { useFeatureFlags } from '../state/featureFlags'

import SessionSidebar from '../components/askdesk/SessionSidebar.vue'
import ChatHeader from '../components/askdesk/ChatHeader.vue'
import WelcomeScreen from '../components/askdesk/ExploreWelcome.vue'
import UserBubble from '../components/askdesk/UserBubble.vue'
import PlanCard from '../components/askdesk/PlanCard.vue'
import ParseBar from '../components/askdesk/ParseBar.vue'
import ThinkingCard from '../components/askdesk/ThinkingCard.vue'
import {taskOutcome} from '../state/askWorkflow'
import QuestionQueue from '../components/askdesk/QuestionQueue.vue'
import {queuedQuestion,appendQuestion,moveQuestionUp,queuePauseReason} from '../state/questionQueue'
import AskProcessView from '../components/askdesk/AskProcessView.vue'
import ResultDigestCard from '../components/askdesk/AnswerCanvas.vue'
import ComposerArea from '../components/askdesk/ComposerArea.vue'
import {answerHtml} from '../utils/answerPresentation'
import ReasoningPanel from '../components/askdesk/ReasoningPanel.vue'
import SqlBlock from '../components/askdesk/SqlBlock.vue'

defineOptions({ name: 'DataPulse' })
import { useDataPulseHistory } from '../state/askDeskHistory'
import { useDataPulseTaskView } from '../state/askDeskTaskView'
import { useDataPulseReportHistory } from '../composables/useAskDeskReportHistory'
import { buildOrgTree, getDefaultConfig as getDefaultReportTreeConfig } from '../composables/useOrgTree'

const session = useDataPulseSession()
const { isFeatureEnabled, loadFeatureFlags } = useFeatureFlags()
const smartFeatureKeys = [
  'debug_execution_trace',
  'ask_field_execution_trace',
  'ask_field_generated_sql',
  'ask_field_dataset_hit',
  'ask_field_error_detail',
  'ask_field_confidence',
  'ask_field_token_usage',
  'ask_new_chat',
  'ask_quick_ask',
  'ask_quick_refresh',
  'ask_question_copy',
  'ask_question_edit',
  'ask_question_rerun',
  'ask_confirm_scope',
  'ask_submit_note',
  'chart_viewer',
  'ask_report_details',
  'ask_send_question',
  'ask_stop_run',
  'ask_dataset_select',
  'ask_model_select',
  'ask_sql_copy',
  'report_fullscreen',
  'ask_report_download',
  'ask_chart_auto_infer',
]
const featureAccess = computed(() => smartFeatureKeys.reduce((map, key) => {
  map[key] = isFeatureEnabled(key)
  return map
}, {}))
const canUseFeature = (key) => Boolean(featureAccess.value[key])
const {
  historySessions,
  activeHistoryId,
  pendingRestoreId,
  loadHistory,
  upsertHistory,
  removeHistory,
  clearHistory,
  findHistoryById,
  clearRestoreRequest,
  setActiveHistory,
  takePendingRestoreOptions,
} = useDataPulseHistory()
const {
  runningSessionId,
  viewingTaskId,
  isViewingReadonly,
  readonlySnapshot,
  runningTaskStatus,
  completedTaskId,
  pendingTaskId,
  setRunningSessionId,
  clearRunningSessionId,
  markRunningTaskPending,
  markRunningTaskCompleted,
  markRunningTaskFailed,
  switchViewToRunning,
  switchViewToDefault,
} = useDataPulseTaskView()
const askCapabilities = ref({ advancedAvailable: false })
const requestedFlow = ref('basic')
let capabilityRequest = 0
const refreshAskCapabilities = async () => {
  const seq = ++capabilityRequest
  try {
    const response = await getAskCapabilities(datasetId.value)
    if (seq !== capabilityRequest) return
    askCapabilities.value = response.data || {}
    showAskFlowBadge.value = false
    requestedFlow.value = askCapabilities.value.defaultFlow || 'basic'
  } catch { askCapabilities.value = { advancedAvailable: false } }
}
const downloadResearchReport = async msg => {
  if (!canUseFeature('ask_report_download')) return
  try {
    const { data } = await getAskCapabilities()
    if (!data?.reportDownloadAvailable || data.authorizationScope !== msg.data?.authorization_scope) {
      ElMessage.warning('当前权限已变化，请重新查询后再下载研究报告。')
      return
    }
    const url = URL.createObjectURL(new Blob([buildResearchReportHtml(msg.data, { allowAutoChart: featureAccess.value.ask_chart_auto_infer })], { type:'text/html;charset=utf-8' }))
    const anchor = document.createElement('a')
    anchor.href = url
    anchor.download = `DataPulse研究报告-${new Date().toISOString().slice(0,10)}.html`
    anchor.click()
    setTimeout(() => URL.revokeObjectURL(url),1000)
  } catch { ElMessage.error('未能验证当前下载权限，请稍后再试。') }
}
const workflowFor = msg => msg.loading || (isCurrentSessionMessage(msg) && session.state.status === 'running') ? session.state.workflow : msg.data?.workflow
const query = ref('')
const datasetId = ref(null)
const modelId = ref(null)
const datasets = ref([])
const aiModels = ref([])
// 数据集就绪信号：登录后 getBookshelfDatasets 为异步，历史恢复的权限过滤必须等它就绪，
// 否则 datasets.value 仍为空会被 isDatasetVisible 全部误判为无权限（首次点历史误报）。
const datasetsLoaded = ref(false)
let datasetsLoadedResolve = null
const ensureDatasetsReady = () => {
  if (datasetsLoaded.value) return Promise.resolve()
  return new Promise((resolve) => {
    datasetsLoadedResolve = resolve
    // 兜底超时放行：后端 GET 已做权限过滤，前端仅为二次校验，超时不再阻塞恢复。
    setTimeout(() => {
      if (datasetsLoadedResolve) { datasetsLoadedResolve(); datasetsLoadedResolve = null }
    }, 2500)
  })
}
const markDatasetsLoaded = () => {
  datasetsLoaded.value = true
  if (datasetsLoadedResolve) { datasetsLoadedResolve(); datasetsLoadedResolve = null }
}
const commonQuestions = ref([])
const commonQuestionsLoading = ref(false)
const messages = reactive([])
const confirmationDrafts = reactive({})
const clarifyDrafts = reactive({})
const confirmationSubmitting = reactive({})
const confirmExpanded = reactive({})

// keep-alive 切回 / 刷新都会调：先看是否有残留 stale，再清掉 session.result + 全部 UI 卡片状态
// hasActiveAsk 守卫：本页正在执行的问数不清（误杀会导致 result 帧被忽略、显示已取消）
const clearStaleSessionState = () => {
  const hasStaleRecovered = session.state.result || session.state.question || session.state.logs?.length
  if (!hasStaleRecovered || session.hasActiveAsk?.()) return
  session.clearRecoveredSessionResult()
  clearChatUiState()
}
const showPanel = ref(false)
const chatBodyRef = ref(null)
const panelRef = ref(null)
const sideReportRef = ref(null)
const sideReportHeadRef = ref(null)
const chartDialogRef = ref(null)
const resultChainRefs = new Map()
const thinkingOpen = reactive({})
const logOpen = reactive({})
const timelineVersion = ref(0)
const reportViewerVisible = ref(false)
const reportViewerResearch = ref(null)
const reportViewerTitle = ref('')
const reportViewerReport = ref('')
const reportViewerDatasets = ref([])
const reportDialogFullscreen = ref(false)
const chartViewerVisible = ref(false)
const chartViewerTitle = ref('图表预览')
const chartViewerSpec = ref(null)
const chartViewerMode = ref('chart')
const detailReportResult = ref(null)
const officeDrillOpen = reactive({})
const messageDerivedCache = new WeakMap()
const datasetChartSpecCache = new WeakMap()
const chartElementCache = new WeakMap()
let activePrintFrame = null
let msgCounter = 0
let elapsed = ref(0)
let timerInst = null
let chatScrollTimer = null
let panelScrollTimer = null
let reportTopScrollTimers = []
const activeRequestAiMessageId = ref(null)
const pendingQuickDataset = ref(null)
const isDatasetManuallySelected = ref(false)

const isRunning = computed(() => session.state.status === 'running')

const displayMessages = computed(() => {
  if (isViewingReadonly.value && readonlySnapshot.value?.messages) {
    return readonlySnapshot.value.messages
  }
  return messages
})

const displayLogs = computed(() => {
  if (isViewingReadonly.value && readonlySnapshot.value?.logs) {
    return readonlySnapshot.value.logs
  }
  return session.state.logs
})

// 解析条编辑（重设计）：点候选 = 本地暂存（可连改多个槽位），确认后把修正问句
// 作为一条新提问发进当前会话（新用户气泡 + 新 AI 回复），替代旧的"点选即就地重跑"
const getParseBarDatasetId = (msg) => {
  const dsr = msg?.data?.dataset_results
  const first = Array.isArray(dsr) && dsr.length ? dsr[0] : null
  const id = first?.dataset_id ?? msg?.data?.route?.dataset_ids?.[0]
  const n = Number(id)
  return Number.isFinite(n) && n > 0 ? n : null
}

// 按 span offset 倒序替换，把暂存修改编译成新问句（dataset 槽无 span，走显式锚定）
const compileParseBarQuestion = (question, overrides) => {
  const repls = (overrides || [])
    .filter(o => (o.slot === 'node' || o.slot === 'metric') && Number.isInteger(o.start) && Number.isInteger(o.end))
    .map(o => ({ start: o.start, end: o.end, text: String(o.new_label || o.new_value || '') }))
    .filter(r => r.text)
    .sort((a, b) => b.start - a.start)
  let q = String(question || '')
  for (const r of repls) q = q.slice(0, r.start) + r.text + q.slice(r.end)
  return q.trim()
}

// 运行中实时解析条（理解阶段完成即出条）：终态优先用 result.parse_bar；
// 实时条只挂在当前正在执行的那条 AI 消息上（loading 结束即收回，确认卡不残留）
const liveParseBar = computed(() => session.state.liveParseBar)
const parseBarFor = (msg) => msg.data?.parse_bar
  || (msg.loading && msg.id === activeRequestAiMessageId.value ? liveParseBar.value : null)

const handleParseBarAsk = async (msg, payload) => {
  const bar = msg?.data?.parse_bar
  const overrides = Array.isArray(payload?.overrides) ? payload.overrides : []
  if (!bar || !overrides.length) return
  if (isRunning.value) {
    ElMessage.info('正在查询中，请稍后再试')
    return
  }
  const list = displayMessages.value || []
  const idx = list.findIndex(m => m.id === msg.id)
  const userMsg = idx > 0 ? list[idx - 1] : null
  const question = String(userMsg && userMsg.role === 'user' ? userMsg.content : '').trim()
  if (!question) return
  const compiled = compileParseBarQuestion(question, overrides)
  const dsOverride = overrides.find(o => o.slot === 'dataset')
  const dsId = Number(dsOverride?.dataset_id ?? payload?.dataset_id)
  const pinnedDatasetId = Number.isFinite(dsId) && dsId > 0 ? dsId : null
  // 仅改数据集（问句无字面变化）时沿用原问句 + 显式锚定新数据集
  const finalQuestion = compiled && compiled !== question ? compiled : question
  if (finalQuestion === question && !pinnedDatasetId) {
    ElMessage.info('未改动解析内容')
    return
  }
  // 修正学习落库 fail-open：不等待、不阻塞提问链路
  recordParseBarFeedback({
    question,
    parse_bar: bar,
    overrides,
    dataset_id: pinnedDatasetId,
    session_id: session.state.conversationSessionId || ''
  }).catch(() => {})
  // 复用主发送链路（同 applyClarifySuggestion 范式）；改数据集时显式锚定，
  // 绕过 datasetInput 的自动释放启发式（用户已明确指定口径）
  query.value = finalQuestion
  await handleSend(pinnedDatasetId ? { datasetId: pinnedDatasetId } : undefined)
}

const displayResult = computed(() => {
  if (isViewingReadonly.value && readonlySnapshot.value?.result) {
    return readonlySnapshot.value.result
  }
  return session.state.result
})

const timelineKey = computed(() => `${session.state.conversationSessionId || 'fresh'}-${timelineVersion.value}`)
const detailPanelVisible = computed(() => showPanel.value && canUseFeature('debug_execution_trace') && canUseFeature('ask_field_execution_trace'))
const canViewCharts = computed(() => canUseFeature('chart_viewer'))
const canViewFullscreenReport = computed(() => canUseFeature('report_fullscreen'))

const statusBarText = computed(() => {
  if(session.state.status==='idle')return ''
  return taskOutcome(session.state.result,{status:session.state.status,busy:isRunning.value,workflow:session.state.workflow}).label
})

const activeReportResult = computed(() => {
  if (isViewingReadonly.value && displayResult.value) {
    return displayResult.value
  }
  return detailReportResult.value || session.state.result || null
})
const inspectorFocusPhase=ref(-1)
const inspectionBusy=computed(()=>isRunning.value && !isViewingReadonly.value)
const inspectionResult=computed(()=>inspectionBusy.value?null:activeReportResult.value)
const inspectionWorkflow=computed(()=>inspectionBusy.value?session.state.workflow:inspectionResult.value?.workflow || {})
const openActivityInspector=async(msg,phase=0)=>{
  if(!canUseFeature('debug_execution_trace') || !canUseFeature('ask_field_execution_trace'))return
  detailReportResult.value=msg?.loading?null:msg?.data || null
  inspectorFocusPhase.value=-1
  showPanel.value=true
  await nextTick()
  inspectorFocusPhase.value=phase
  resizeRenderedCharts()
}
const latestSessionError = computed(() => {
  const msg = activeRequestAiMessage.value || currentSessionAiMessage.value
  return String(msg?.data?.error || session.state.result?.error || '').trim()
})
const showAskFlowBadge = ref(false)

const activeAskFlowMeta = computed(() => {
  if (!showAskFlowBadge.value) return null
  const meta = activeReportResult.value?.ask_flow || activeReportResult.value?.diagnostics?.ask_flow || null
  return meta && typeof meta === 'object' ? meta : null
})

const activeAskFlowLabel = computed(() => {
  const flow = String(activeAskFlowMeta.value?.flow || '').toLowerCase()
  if (flow === 'advanced') return '进阶流程'
  if (flow === 'basic') return '基础流程'
  return ''
})

const activeAskFlowClass = computed(() => String(activeAskFlowMeta.value?.flow || '').toLowerCase() === 'advanced' ? 'is-advanced' : 'is-basic')

const activeAskFlowHint = computed(() => {
  const reason = String(activeAskFlowMeta.value?.reason || '')
  const map = {
    basic_selected: '当前问数由基础流程执行',
    advanced_selected: '当前问数由进阶流程执行',
    advanced_disabled: '进阶未启用，已回落基础流程',
    advanced_role_denied: '当前角色未进入进阶灰度',
    advanced_error_fallback: '进阶异常，已回退基础流程',
  }
  return map[reason] || '当前问数流程'
})

const latestDatasets = computed(() => (
  Array.isArray(activeReportResult.value?.dataset_results) ? activeReportResult.value.dataset_results : []
))

const mergeDatasetReports = (datasetResults) => (
  (datasetResults || [])
    .map((dataset, index) => {
      const analysis = String(dataset?.analysis || '').trim()
      if (!analysis) return ''
      const datasetName = dataset?.dataset_name || `数据集 ${dataset?.dataset_id || index + 1}`
      return datasetResults.length > 1 ? `## ${datasetName}\n\n${analysis}` : analysis
    })
    .filter(Boolean)
    .join('\n\n---\n\n')
)

const parseMetricNumber = (value) => {
  if (value === null || value === undefined || value === '') return null
  if (typeof value === 'number') return Number.isFinite(value) ? value : null
  const text = String(value || '').trim()
  const numeric = Number(text.replace(/[^0-9.-]/g, ''))
  if (!Number.isFinite(numeric)) return null
  if (text.includes('亿')) return numeric * 100000000
  if (text.includes('万')) return numeric * 10000
  return numeric
}

const findDatasetKpiNumber = (dataset, matcher) => {
  const kpis = Array.isArray(dataset?.report_spec?.kpis) ? dataset.report_spec.kpis : []
  const item = kpis.find(kpi => matcher.test(`${kpi?.key || ''}${kpi?.label || ''}`))
  if (!item) return null
  return parseMetricNumber(item.value ?? item.displayValue)
}

const findDatasetRowNumber = (dataset, matcher) => {
  const rows = Array.isArray(dataset?.rows) ? dataset.rows : []
  const row = rows.find(item => item && typeof item === 'object') || {}
  const key = Object.keys(row).find(name => matcher.test(name))
  return key ? parseMetricNumber(row[key]) : null
}

const inferSubjectLevel = (name) => {
  const text = String(name || '')
  if (text.includes('事业群')) return '事业群'
  if (text.includes('战区')) return '战区'
  if (text.includes('行业部')) return '行业部'
  if (text.includes('片区')) return '片区'
  return '对象'
}

const buildDatasetComparisonRow = (dataset) => {
  const subjectName = dataset?.comparison_subject_name || dataset?.dataset_name || `数据集 ${dataset?.dataset_id || ''}`.trim()
  const overview = dataset?.cross_dataset_subject_overview || {}
  const task = parseMetricNumber(overview?.task)
    ?? findDatasetKpiNumber(dataset, /总任务|任务金额|目标|task/i)
    ?? findDatasetRowNumber(dataset, /总任务|任务金额|目标/i)
  const actual = parseMetricNumber(overview?.actual)
    ?? findDatasetKpiNumber(dataset, /年度开单|开单金额|开单|完成|实际|actual/i)
    ?? findDatasetRowNumber(dataset, /年度开单|开单金额|开单|完成|实际/i)
  const rate = parseMetricNumber(overview?.rate)
    ?? findDatasetKpiNumber(dataset, /达成率|完成率|rate|percent/i)
    ?? findDatasetRowNumber(dataset, /达成率|完成率/i)
    ?? (task ? (Number(actual || 0) / task) * 100 : null)
  const remain = parseMetricNumber(overview?.remain)
    ?? findDatasetKpiNumber(dataset, /剩余|缺口|差额|remain|gap/i)
    ?? findDatasetRowNumber(dataset, /剩余|缺口|差额/i)
    ?? (task !== null && actual !== null ? task - actual : null)
  return {
    节点名称: subjectName,
    层级: overview?.level || dataset?.comparison_subject_level || inferSubjectLevel(subjectName),
    总任务金额: task,
    年度开单金额: actual,
    达成率: rate,
    剩余任务金额: remain,
  }
}

const collectResolvedNamesFromDatasets = (datasetResults) => {
  const names = []
  const add = (value) => {
    const text = String(value || '').trim()
    if (text && !names.includes(text)) names.push(text)
  }
  ;(datasetResults || []).forEach((dataset) => {
    const resolved = dataset?.resolved_entities || {}
    ;(resolved.all_members || []).forEach(add)
    ;(resolved.entities || []).forEach((entity) => {
      ;(entity?.members || []).forEach(add)
    })
  })
  return names
}

const datasetRowsContainAnyName = (dataset, names = []) => {
  if (!names.length) return false
  return (dataset?.rows || []).some((row) => {
    const text = Object.values(row || {}).map(value => String(value ?? '')).join(' ')
    return names.some(name => text.includes(name))
  })
}

const buildAggregateDataset = (datasetResults) => {
  if (!Array.isArray(datasetResults) || datasetResults.length === 0) return null
  if (datasetResults.length === 1) return datasetResults[0]

  const resolvedNames = collectResolvedNamesFromDatasets(datasetResults)
  if (resolvedNames.length === 1) {
    const matching = datasetResults.filter(dataset => datasetRowsContainAnyName(dataset, resolvedNames))
    if (matching.length === 1) return matching[0]
  }

  const totalRows = datasetResults.reduce((sum, item) => sum + Number(item?.row_count || item?.rows?.length || 0), 0)
  const allColumns = Array.from(new Set(datasetResults.flatMap(item => item?.columns || [])))
  const comparisonRows = datasetResults.map(buildDatasetComparisonRow).filter(item => item.节点名称)

  return {
    dataset_name: `共 ${datasetResults.length} 个数据集`,
    dataset_id: 'multi',
    row_count: totalRows,
    rows: comparisonRows,
    columns: Array.from(new Set([...allColumns, '节点名称', '层级', '总任务金额', '年度开单金额', '达成率', '剩余任务金额'])),
  }
}

const latestDataset = computed(() => buildAggregateDataset(latestDatasets.value))

const latestReport = computed(() => mergeDatasetReports(latestDatasets.value))

const isDatasetVisible = (id) => {
  const value = Number(id)
  if (!Number.isFinite(value)) return false
  return datasets.value.some(item => Number(item?.id) === value)
}

const sanitizeDatasetSelection = () => {
  if (datasetId.value && !isDatasetVisible(datasetId.value)) {
    datasetId.value = null
    isDatasetManuallySelected.value = false
  }
  if (session.state.selectedDatasetId && !isDatasetVisible(session.state.selectedDatasetId)) {
    session.state.selectedDatasetId = null
  }
  if (pendingQuickDataset.value?.datasetId && !isDatasetVisible(pendingQuickDataset.value.datasetId)) {
    pendingQuickDataset.value = null
  }
}

const datasetResults = computed(() => latestDatasets.value)
const hasSideReport = computed(() => {
  if (activeReportResult.value?.research) return false
  if (latestSessionError.value) return false
  return resultPreviews.value.length > 0 || !!latestReport.value
})
const sideReportHeading = computed(() => '业绩分析报告')

const reportSceneTemplate = computed(() => {
  const sourceDatasets = reportViewerVisible.value ? reportViewerDatasets.value : latestDatasets.value
  const specTemplate = sourceDatasets.find(item => item?.report_spec?.layoutTemplate)?.report_spec?.layoutTemplate
  if (specTemplate) return specTemplate
  const answerMode = String(sourceDatasets.find(item => item?.report_spec?.answerMode)?.report_spec?.answerMode || '').trim()
  if (answerMode === 'comparison') return 'comparison'
  if (answerMode === 'ranking') return 'ranking'
  if (answerMode === 'drilldown' || answerMode === 'filter') return 'detail'
  const questionText = String(activeReportResult.value?.question || session.state.question || query.value || '')
  if (/对比|比较|哪个|谁更|差异|和.+比|跟.+比|与.+比|\bvs\b/i.test(questionText)) return 'comparison'
  if (/排名|排行|前\s*(?:\d+|[一二两三四五六七八九十]+)|Top\s*\d+|TOP\s*\d+|最好|最差|最高|最低/.test(questionText)) return 'ranking'
  return 'detail'
})

const reportSceneTemplateLabel = computed(() => ({
  comparison: '对比模板',
  ranking: '排名模板',
  detail: '详情模板',
}[reportSceneTemplate.value] || '详情模板'))

const normalizeConfidenceScore = (value, fallback = 0) => {
  const numeric = Number(value)
  if (!Number.isFinite(numeric)) return fallback
  return Math.max(0, Math.min(100, Math.round(numeric)))
}

const buildRouteConfidenceMeta = (route = {}) => {
  const candidateCount = Array.isArray(route?.candidate_dataset_ids)
    ? route.candidate_dataset_ids.length
    : Array.isArray(route?.dataset_ids)
      ? route.dataset_ids.length
      : 0

  let score = normalizeConfidenceScore(route?.match_score, candidateCount <= 1 ? 78 : 64)
  if (candidateCount > 1) score -= Math.min(12, (candidateCount - 1) * 6)
  if (route?.requires_confirmation) score = Math.min(score, 60)
  if (route?.preferred_dataset_override) score = Math.max(score, 72)

  return {
    score,
    tone: score >= 82 ? 'success' : score >= 65 ? 'info' : 'warning',
    label: score >= 82 ? '路由把握' : score >= 65 ? '路由可用' : '路由待确认',
    value: `${score}`,
    candidateCount,
  }
}

const buildResultConfidenceMeta = (route = {}, datasets = []) => {
  const reviews = (datasets || []).map(item => item?.agent3_review).filter(Boolean)
  const approvedCount = reviews.filter(item => item?.approved !== false).length
  const riskCount = reviews.reduce((sum, item) => sum + (Array.isArray(item?.risks) ? item.risks.length : 0), 0)
  const datasetTotal = (datasets || []).length
  const rowsReady = (datasets || []).filter(item => Array.isArray(item?.rows) && item.rows.length > 0).length
  const analysesReady = (datasets || []).filter(item => String(item?.analysis || '').trim()).length

  let score = 55
  if (datasetTotal > 0) score += 8
  if (rowsReady === datasetTotal && datasetTotal > 0) score += 16
  else if (rowsReady > 0) score += 8
  if (reviews.length === datasetTotal && approvedCount === datasetTotal && datasetTotal > 0) score += 12
  else if (approvedCount > 0) score += 6
  if (analysesReady === datasetTotal && datasetTotal > 0) score += 8
  score -= Math.min(18, riskCount * 4)
  if (buildRouteConfidenceMeta(route).candidateCount > 1) score -= 5
  score = normalizeConfidenceScore(score, 60)

  return {
    score,
    tone: score >= 80 ? 'success' : score >= 62 ? 'info' : 'warning',
    label: score >= 80 ? '结果稳定' : score >= 62 ? '结果可用' : '结果谨慎',
    value: riskCount > 0 ? `${score} / ${riskCount} 风险` : `${score}`,
  }
}

const sideConfidenceBadges = computed(() => {
  if (activeReportResult.value?.workflow) return []
  const advanced = activeReportResult.value?.diagnostics?.advanced || {}
  const evidenceVote = advanced?.evidence_vote || {}
  const templatePolicy = advanced?.template_policy || {}
  const routeGuard = advanced?.route_guard || {}
  const backendConfidence = activeReportResult.value?.confidence || {}
  const routeMeta = backendConfidence?.route
    ? {
        score: Number(backendConfidence.route.score || 0),
        tone: backendConfidence.route.level === 'high' ? 'success' : backendConfidence.route.level === 'medium' ? 'info' : 'warning',
        label: '路由把握',
        value: `${backendConfidence.route.label || ''} ${backendConfidence.route.score || 0}`.trim(),
      }
    : buildRouteConfidenceMeta(activeReportResult.value?.route || {})
  const resultMeta = backendConfidence?.result
    ? {
        score: Number(backendConfidence.result.score || 0),
        tone: backendConfidence.result.level === 'high' ? 'success' : backendConfidence.result.level === 'medium' ? 'info' : 'warning',
        label: '结果可信',
        value: `${backendConfidence.result.label || ''} ${backendConfidence.result.score || 0}`.trim(),
      }
    : buildResultConfidenceMeta(activeReportResult.value?.route || {}, latestDatasets.value)
  const advancedVoteMeta = evidenceVote?.decision
    ? {
        score: Number(evidenceVote.confidence_score || 0),
        tone: evidenceVote.decision === 'accept' ? 'success' : evidenceVote.decision === 'accept_with_caution' ? 'info' : 'warning',
        label: '进阶择优',
        value: `${({
          accept: '可采信',
          accept_with_caution: '谨慎采信',
          review_required: '需复核',
        }[evidenceVote.decision] || evidenceVote.decision)} ${evidenceVote.confidence_score || 0}`.trim(),
      }
    : null
  const templateMeta = templatePolicy?.expected_top_n
    ? {
        score: Number(templatePolicy.expected_top_n || 0),
        tone: Number(templatePolicy.warning_count || 0) > 0 ? 'warning' : 'success',
        label: '模板策略',
        value: `Top${templatePolicy.expected_top_n}`,
      }
    : null
  const routeGuardLabel = {
    auto_lock: '自动锁定',
    cross_dataset_compare: '跨集对比',
    manual_respected: '手动优先',
    manual_mismatch: '手动错配',
    needs_confirmation: '待确认',
    no_candidate: '无候选',
    observe: '观察',
  }[routeGuard.action] || routeGuard.action
  const guardMeta = routeGuard?.action
    ? {
        score: Number(routeGuard.confidence || 0),
        tone: routeGuard.action === 'auto_lock' || routeGuard.action === 'manual_respected' ? 'success' : 'warning',
        label: '路由守门',
        value: routeGuardLabel,
      }
    : null
  return [routeMeta, resultMeta, advancedVoteMeta, templateMeta, guardMeta].filter(item => item?.score > 0)
})

const routeDecisionDetail = computed(() => {
  const result = activeReportResult.value || {}
  const advanced = result?.diagnostics?.advanced || {}
  const route = result.route || {}
  const summary = String(result.confidence?.route?.summary || '').trim()
  const reason = String(result.confidence?.route?.reason || route.arbiter_reason || '').trim()
  const reasonLabel = {
    profile_scope_resolved: '组织画像命中',
    explicit_dataset_alias: '同义词命中',
    organization_tree_name_resolved: '组织树命中',
    top_candidate_score_clear: '候选分数领先',
    high_confidence: '高置信语义匹配',
    low_similarity_requires_boss_confirm: '相似命中待确认',
  }[reason] || ''
  const ids = Array.isArray(route.dataset_ids) ? route.dataset_ids : []
  const names = ids.map(id => datasetNameMap.value.get(Number(id)) || `数据集 ${id}`).filter(Boolean)
  const routeGuard = advanced?.route_guard || {}
  const evidenceVote = advanced?.evidence_vote || {}
  const advancedLines = [
    routeGuard?.reason ? `进阶守门：${routeGuard.reason}` : '',
    evidenceVote?.recommended_action ? `采信建议：${evidenceVote.recommended_action}` : '',
  ].filter(Boolean)
  if (!summary && !reasonLabel && !names.length && !advancedLines.length) return ''
  return [
    names.length ? `自动路由：${names.join('、')}` : '',
    reasonLabel ? `依据：${reasonLabel}` : '',
    summary,
    ...advancedLines,
  ].filter(Boolean).join('；')
})

const detailPanelState = computed(() => {
  const m = {
    idle: '待命',
    running: '执行中',
    completed: '已完成',
    canceled: '已取消',
    error: '异常',
    waiting_confirmation: '待确认',
  }
  return m[session.state.status] || '待命'
})

const detailPanelDesc = computed(() => {
  if (session.state.status === 'running') {
    return session.latestLog?.value?.summary || session.latestLog?.value?.title || session.state.logs.slice(-1)[0]?.detail || '正在持续更新本轮问数任务的执行进度。'
  }
  if (session.state.status === 'completed') {
    return '本轮问数已经完成，可以继续查看执行细节、结果数据和完整报告。'
  }
  if (session.state.status === 'canceled') {
    return '你已手动取消本轮问数，执行链路已停止。'
  }
  if (session.state.status === 'waiting_confirmation') {
    return '当前任务等待确认统计口径，确认后会继续后续执行步骤。'
  }
  if (session.state.status === 'error') {
    return session.state.error || '当前任务执行异常，请查看节点详情后重新发起问数。'
  }
  return '发起问题后，这里会持续展示本轮任务的完整执行轨迹。'
})

const amountColumnPattern = /金额|开单|任务|销售|收入|成本|利润|缺口|剩余|回款|费用|价格|单价|amount|sales|revenue|cost|profit|remain/i
const rateColumnPattern = /率|percent|rate/i

const formatAmount = (value, metric = {}) => {
  const numeric = typeof value === 'number'
    ? value
    : Number(String(value ?? '').replace(/[^0-9.-]/g, ''))
  if (!Number.isFinite(numeric)) return '-'

  const unit = String(metric.unit || '').trim()
  const scale = Number(metric.scale) || 1
  const display = numeric / scale
  const absDisplay = Math.abs(display)

  const fmt = (num, digits = 2) => {
    if (Number.isInteger(num)) return String(num)
    return Number(num).toFixed(digits).replace(/\.?0+$/, '')
  }

  if (unit === '万元') {
    if (absDisplay < 10000) return `${fmt(display)}万`
    return `${fmt(display / 10000)}亿`
  }

  // 默认按 "元" 口径展示
  if (absDisplay < 10000) return fmt(display)
  if (absDisplay < 1000000) return `${(display / 10000).toFixed(1).replace(/\.?0+$/, '')}万`
  if (absDisplay < 100000000) return `${Math.round(display / 10000)}万`
  return `${(display / 100000000).toFixed(2).replace(/\.?0+$/, '')}亿`
}

const resolveAmountMetric = (metric = {}, dataset = null, column = '') => {
  const nextMetric = { ...(metric || {}) }
  if (String(nextMetric.unit || '').trim()) return nextMetric

  const reportSpec = dataset?.report_spec || {}
  const reportUnit = String(reportSpec.amountUnit || '').trim()
  const metricColumn = String(nextMetric.column || column || '').trim()

  if (reportUnit && isAmountColumn(metricColumn || nextMetric.label || nextMetric.key || '')) {
    nextMetric.unit = reportUnit
    nextMetric.scale = Number(nextMetric.scale) || 1
    return nextMetric
  }

  return nextMetric
}

const formatChartAmount = (value, dataset = null, column = '') => (
  formatAmount(value, resolveAmountMetric({ format: 'amount', column }, dataset, column))
)

const isAmountColumn = (column = '') => amountColumnPattern.test(String(column || ''))
const isRateColumn = (column = '') => rateColumnPattern.test(String(column || ''))

const formatDisplayValue = (value) => {
  if (typeof value === 'number') {
    if (Number.isInteger(value)) return value.toLocaleString()
    return value.toLocaleString('zh-CN', { maximumFractionDigits: 2 })
  }
  return String(value ?? '-')
}

const formatValueByColumn = (value, column = '', dataset = null) => {
  if (isAmountColumn(column)) {
    const metric = resolveAmountMetric({}, dataset, column)
    const col = String(column || '')
    if (/_万元$/.test(col) || /万元$/.test(col)) {
      metric.unit = '万元'
      metric.scale = 1
    }
    return formatAmount(value, metric)
  }
  return formatDisplayValue(value)
}

const formatBusinessValueByColumn = (value, column = '', dataset = null) => {
  const rawText = String(value ?? '').trim()
  if (rawText && /[万亿%]/.test(rawText)) return rawText
  return formatValueByColumn(value, column, dataset)
}

const getLabelColumn = (dataset) => {
  const columns = dataset?.columns || []
  const firstRow = dataset?.rows?.[0] || {}
  return (
    columns.find(col => /组织路径|归属组织|组织归属|管理链路|路径/i.test(col)) ||
    columns.find(col => /日期|时间|城市|战区|片区|行业部|名称|水平|类型|标识/i.test(col)) ||
    columns.find(col => typeof firstRow[col] === 'string') ||
    columns[0]
  )
}

const getNumericColumns = (dataset) => {
  const columns = dataset?.columns || []
  const firstRow = dataset?.rows?.[0] || {}
  return columns.filter(col => typeof firstRow[col] === 'number')
}

const getMetricCards = (dataset) => {
  const rows = dataset?.rows || []
  if (!rows.length) return []

  const businessCards = getBusinessMetricCards(dataset)
  if (businessCards.length) return businessCards

  const firstRow = rows[0]
  const numericColumns = getNumericColumns(dataset)
  const cards = []

  numericColumns.slice(0, 3).forEach((column) => {
    const values = rows.map(row => row[column]).filter(value => typeof value === 'number')
    if (!values.length) return
    const displayValue = rows.length === 1 ? firstRow[column] : Math.max(...values)
    cards.push({ label: rows.length === 1 ? column : `最高${column}`, value: formatValueByColumn(displayValue, column, dataset) })
  })

  if (rows.length === 1 && cards.length === 0) {
    const labelColumn = getLabelColumn(dataset)
    if (labelColumn) cards.push({ label: labelColumn, value: formatDisplayValue(firstRow[labelColumn]) })
  }

  if (rows.length > 1) cards.push({ label: '数据行数', value: formatDisplayValue(rows.length) })
  return cards.slice(0, 3)
}

const toNumber = (value) => {
  if (typeof value === 'number') return Number.isFinite(value) ? value : null
  const cleaned = String(value ?? '').replace(/[^0-9.-]/g, '')
  if (!cleaned) return null
  const numeric = Number(cleaned)
  return Number.isFinite(numeric) ? numeric : null
}

const pickColumn = (dataset, names) => {
  const columns = dataset?.columns || []
  return names.find(name => columns.includes(name)) || ''
}

const getDatasetReportConfig = (dataset) => (
  dataset?.report_config
  || activeReportResult.value?.report_configs?.[String(dataset?.dataset_id)]
  || activeReportResult.value?.report_config
  || getDefaultReportTreeConfig()
)

const getDatasetTreeModel = (dataset) => {
  const rows = Array.isArray(dataset?.rows) ? dataset.rows : []
  if (!rows.length) return null
  return buildOrgTree(rows, getDatasetReportConfig(dataset))
}

const sumBusinessColumn = (rows, column) => {
  if (!column) return null
  const values = rows.map(row => toNumber(row?.[column])).filter(value => value !== null)
  if (!values.length) return null
  return values.reduce((sum, value) => sum + value, 0)
}

const calcBusinessRate = (rows, taskCol, actualCol, rateCol) => {
  const task = sumBusinessColumn(rows, taskCol)
  const actual = sumBusinessColumn(rows, actualCol)
  if (task && actual !== null && task > 0) return Number((actual / task * 100).toFixed(2))
  const rates = rows.map(row => toNumber(row?.[rateCol])).filter(value => value !== null)
  if (!rates.length) return null
  return Number((rates.reduce((sum, value) => sum + value, 0) / rates.length).toFixed(2))
}

const formatBusinessAmount = (value) => {
  if (value === null || value === undefined) return '-'
  return formatAmount(value)
}

const formatMetricByDefinition = (value, metric = {}, dataset = null) => {
  if (value === null || value === undefined) return '-'
  if (metric.format === 'percent') return `${Number(value).toLocaleString('zh-CN', { maximumFractionDigits: 2 })}%`
  if (metric.format === 'amount' || metric.format === 'currency') return formatAmount(value, resolveAmountMetric(metric, dataset))
  return formatDisplayValue(value)
}

const getMetricDefinition = (config, key, matcher) => {
  const metrics = config?.metrics || []
  return metrics.find(item => item.key === key)
    || metrics.find(item => matcher?.(item))
    || null
}

const getNodeMetricValue = (node, metric) => {
  if (!node || !metric) return null
  const direct = toNumber(node.metrics?.[metric.key])
  if (direct !== null) return direct
  return toNumber(node.raw?.[metric.column])
}

const getRateTone = (rate, benchmark = 15, risk = 10) => {
  const value = toNumber(rate)
  if (value === null) return 'neutral'
  if (value >= benchmark) return 'good'
  if (value >= risk) return 'warn'
  return 'danger'
}

const getToneLabel = (tone) => ({ good: '区域标杆', warn: '中等达成', danger: '低达成风险' }[tone] || '待观察')

const getRateTag = (rate, benchmark = 15, risk = 10, goodLabel = '标杆') => {
  const tone = getRateTone(rate, benchmark, risk)
  if (tone === 'good') return `✅ ${goodLabel}`
  if (tone === 'warn') return '🟡 中等'
  if (tone === 'danger') return '⚠️ 风险'
  return '未分级'
}

const getOfficeThresholds = (config = {}) => {
  const risk = toNumber(config?.officeRiskThreshold ?? config?.riskThreshold) ?? 10
  const configuredBenchmark = toNumber(config?.officeBenchmarkThreshold ?? config?.benchmarkThreshold)
  return {
    risk,
    benchmark: configuredBenchmark ?? 15,
  }
}

const getOfficeRateTone = (rate, config = {}) => {
  const { benchmark, risk } = getOfficeThresholds(config)
  return getRateTone(rate, benchmark, risk)
}

const getOfficeToneLabel = (tone) => ({ good: '区域标杆', warn: '需推进', danger: '低达成风险' }[tone] || '待观察')

const getOfficeRateTag = (rate, config = {}, goodLabel = '区域标杆') => {
  const tone = getOfficeRateTone(rate, config)
  if (tone === 'good') return `✅ ${goodLabel}`
  if (tone === 'warn') return '🟠 需推进'
  if (tone === 'danger') return '⚠️ 风险'
  return '未分级'
}

const getToneFromDisplayTag = (label = '', fallback = 'neutral') => {
  const text = String(label || '')
  if (/风险|重点风险/.test(text)) return 'danger'
  if (/承压|第三梯队/.test(text)) return 'danger'
  if (/推进|第二梯队|稳定|中位/.test(text)) return 'warn'
  if (/标杆|领先|第一梯队/.test(text)) return 'good'
  return fallback
}

const requestedLevelTokens = ['城市战区', '城市站', '事业群', '行业部', '战区', '片区', '客户经理', '业务员', '部门', '线']

const canonicalRequestedLevel = (value) => {
  const text = String(value || '').trim()
  if (text === '城市战区') return '城市站'
  return text
}

const getQuestionText = () => String(session.state.question || query.value || '').trim()

const getRequestedLevelValues = (questionText = getQuestionText(), config = {}) => {
  const values = []
  const configuredValues = (config?.levels || [])
    .flatMap(level => level?.values || [])
    .map(value => String(value || '').trim())
    .filter(Boolean)
  ;[...configuredValues, ...requestedLevelTokens].forEach((value) => {
    const canonical = canonicalRequestedLevel(value)
    if (value && questionText.includes(value) && !values.includes(canonical)) values.push(canonical)
  })
  return values
}

const isNegativeRankingQuestion = (questionText = getQuestionText()) => (
  /完成.*不好|不好|差|最差|最低|落后|承压|风险|低于|倒数|垫底|未完成|缺口/.test(questionText || '')
)

const isRateRankingQuestion = (questionText = getQuestionText()) => (
  /达成率|完成率|完成|进度|不好|最低|最差|排名|排行|承压|风险/.test(questionText || '')
)

const isAmountRankingQuestion = (questionText = getQuestionText()) => (
  /排名|排行|Top\s*\d+|TOP\s*\d+|前\s*(?:\d+|[一二两三四五六七八九十]+)|最高|最低|最好|最差/.test(questionText || '')
  && /年度开单|开单金额|开单|实际|销售/.test(questionText || '')
)

const getQuestionRankingMetricLabel = (questionText = getQuestionText()) => {
  const text = String(questionText || '')
  if (!/排名|排行|Top\s*\d+|TOP\s*\d+|前\s*(?:\d+|[一二两三四五六七八九十]+)|最高|最低|最好|最差/.test(text)) return ''
  if (/年度开单|开单金额|开单|实际|销售/.test(text)) return '年度开单金额'
  if (/总任务|任务金额|目标/.test(text)) return '总任务金额'
  if (/剩余|缺口|差额|待完成/.test(text)) return '剩余任务金额'
  if (/达成率|完成率|进度|完成/.test(text)) return '达成率'
  return ''
}

const getRankingPolicy = (config = {}) => (
  config?.intentPolicies?.ranking && typeof config.intentPolicies.ranking === 'object'
    ? config.intentPolicies.ranking
    : {}
)

const getConfiguredTopN = (report = null) => {
  const config = report?.dataset ? getDatasetReportConfig(report.dataset) : getDefaultReportTreeConfig()
  const intentTopN = toNumber(report?.dataset?.report_spec?.debug?.query_intent?.top_n)
  const policy = getRankingPolicy(config)
  const defaultTopN = toNumber(policy.defaultTopN) ?? 3
  const maxTopN = toNumber(policy.maxTopN) ?? 20
  if (report?.answerMode === 'ranking' && intentTopN === null) {
    return Math.max(1, Array.isArray(report?.offices) && report.offices.length ? report.offices.length : defaultTopN)
  }
  const value = intentTopN ?? defaultTopN
  return Math.max(1, Math.min(maxTopN, value))
}

const sortNodesForQuestion = (nodes = [], rateMetric = null) => {
  const lowFirst = isNegativeRankingQuestion()
  return [...nodes].sort((left, right) => {
    const leftValue = getNodeMetricValue(left, rateMetric) || 0
    const rightValue = getNodeMetricValue(right, rateMetric) || 0
    return lowFirst ? leftValue - rightValue : rightValue - leftValue
  })
}

const normalizeOfficeCompareSpec = (chartSpec = {}, config = {}) => {
  if (!chartSpec || typeof chartSpec !== 'object') return chartSpec
  const rows = Array.isArray(chartSpec.rows) ? chartSpec.rows : []
  const columns = Array.isArray(chartSpec.columns) && chartSpec.columns.length
    ? [...chartSpec.columns]
    : Object.keys(rows[0] || {})
  const rateColumn = findColumn(columns, column => isRateColumn(column)) || '达成率'
  const nextColumns = columns.includes('标签') ? columns : [...columns, '标签']
  return {
    ...chartSpec,
    columns: nextColumns,
    sortColumn: chartSpec.sortColumn || '',
    rows: rows.map(row => ({
      ...row,
      标签: row?.标签 || getOfficeRateTag(row?.[rateColumn], config),
    })),
  }
}

const subjectAccentPalette = [
  { accent: '#1A1A1A', soft: 'rgba(26, 26, 26, 0.06)', border: 'rgba(26, 26, 26, 0.18)' },
  { accent: '#10B981', soft: 'rgba(16, 185, 129, 0.08)', border: 'rgba(16, 185, 129, 0.22)' },
  { accent: '#F59E0B', soft: 'rgba(245, 158, 11, 0.09)', border: 'rgba(245, 158, 11, 0.24)' },
  { accent: '#6B7280', soft: 'rgba(107, 114, 128, 0.08)', border: 'rgba(107, 114, 128, 0.22)' },
]

const getSubjectAccent = (index = 0) => subjectAccentPalette[Math.abs(index) % subjectAccentPalette.length]

const getOfficeAccentStyle = (_office, index = 0) => {
  const color = getSubjectAccent(index)
  return {
    '--office-accent': color.accent,
    '--office-accent-soft': color.soft,
    '--office-accent-border': color.border,
  }
}

const decorateMetricCards = (kpis = [], offices = []) => (
  (kpis || []).map((item) => {
    const label = item.label || item.key || ''
    const officeIndex = offices.findIndex(office => label.startsWith(office.name))
    if (officeIndex < 0) {
      return {
        label,
        value: item.value ?? item.displayValue ?? formatDisplayValue(item.value),
      }
    }
    const office = offices[officeIndex]
    const color = getSubjectAccent(officeIndex)
    return {
      label: label.replace(office.name, ''),
      value: item.value ?? item.displayValue ?? formatDisplayValue(item.value),
      subject: office.name,
      accentStyle: {
        '--metric-accent': color.accent,
        '--metric-accent-soft': color.soft,
        '--metric-accent-border': color.border,
      },
    }
  }).filter(item => item.label)
)

const getOfficeKpiLabel = (office, type) => {
  const matchers = {
    task: /总任务|任务金额|目标/i,
    actual: /年度开单|开单|完成|实际|销售/i,
    remain: /剩余|缺口|差额|remain/i,
    rate: /达成率|percent|rate/i,
  }
  const matcher = matchers[type]
  const item = (office?.kpis || []).find(kpi => matcher?.test(kpi.label || ''))
  return item?.value || '-'
}

const getReportKpi = (report, type) => {
  const matchers = {
    task: /总任务|任务金额|目标/i,
    actual: /年度开单|开单|完成|实际|销售/i,
    remain: /剩余|缺口|差额|remain/i,
    rate: /达成率|percent|rate/i,
  }
  const matcher = matchers[type]
  return (report?.kpis || []).find(kpi => matcher?.test(kpi.label || '')) || null
}

const getReportKpiText = (report, type) => getReportKpi(report, type)?.value || '-'

const getSingleOrgCounts = (report) => {
  const offices = report?.offices || []
  const directCount = offices.length
  const detailCount = offices.reduce((sum, office) => (
    sum + Number(office.childCount || office.detailRows?.length || 0)
  ), 0)
  return {
    directCount,
    detailCount,
    directLabel: report?.compareLevelLabel || '下级节点',
    detailLabel: report?.detailLevelLabel || '明细节点',
  }
}

const getKnownChildLevelLabel = (levelLabel = '') => {
  const text = String(levelLabel || '').trim()
  if (/战区/.test(text) && !/城市/.test(text)) return '城市站'
  if (/片区|行业部/.test(text)) return '客户经理'
  return ''
}

const getOfficeSubtitle = (office, report) => {
  if (office?.isLeafLevel) {
    return `${office.leafLabel || '当前最细层'} · ${office.parentName || '当前口径'}`
  }
  return `${office?.childCount || 0} 个${report?.detailLevelLabel || office?.detailLevelLabel || '明细层级'} · ${office?.parentName || '当前口径'}`
}

const getOfficeToggleTitle = (office, report) => (
  office?.isLeafLevel
    ? `查看${office.name || '当前对象'}当前层指标`
    : `展开查看${office?.childCount || 0}个${report?.detailLevelLabel || office?.detailLevelLabel || '明细层级'}`
)

const getOfficeEmptyDrillText = (office, report) => (
  office?.isLeafLevel
    ? `${office.name || '当前对象'}已到当前最细层，暂无可继续下钻的下级明细。`
    : `当前 SQL 结果未返回 ${report?.detailLevelLabel || office?.detailLevelLabel || '明细层级'} 明细。请重新问“${office?.name || '当前对象'}下${report?.detailLevelLabel || office?.detailLevelLabel || '明细层级'}业绩明细”或检查 SQL 是否包含下级层级。`
)

const reportHasDrillableOffices = (report) => (
  Array.isArray(report?.offices) && report.offices.some(office => !office?.isLeafLevel)
)

const isLeafOnlyReport = (report) => (
  Array.isArray(report?.offices) && report.offices.length > 0 && report.offices.every(office => office?.isLeafLevel)
)

const canToggleOffice = (office) => !office?.isLeafLevel

const getReportRiskCount = (report) => {
  const offices = Array.isArray(report?.offices) ? report.offices : []
  if (!offices.length) return 0
  const threshold = report?.answerMode === 'ranking' || report?.answerMode === 'filter' ? 10 : 15
  return offices.filter(item => {
    const rate = toNumber(item?.rate)
    return rate !== null && rate < threshold
  }).length
}

const getMetricValueFromOffice = (office, label = '') => {
  const metricText = String(label || '')
  const kpis = Array.isArray(office?.kpis) ? office.kpis : []
  const direct = kpis.find(item => {
    const itemLabel = String(item?.label || '')
    return itemLabel && (itemLabel.includes(metricText) || metricText.includes(itemLabel))
  })
  const directValue = toNumber(direct?.value)
  if (directValue !== null) return directValue
  if (isRateMetricLabel(metricText)) return toNumber(office?.rate)
  if (/开单|完成|实际|销售/i.test(metricText)) return toNumber(getOfficeKpiLabel(office, 'actual'))
  if (/任务|目标/i.test(metricText)) return toNumber(getOfficeKpiLabel(office, 'task'))
  if (/剩余|缺口|差额|remain/i.test(metricText)) return toNumber(getOfficeKpiLabel(office, 'remain'))
  return toNumber(office?.rate)
}

const getReportSortSpec = (report = null) => {
  const datasetSortSpec = report?.dataset?.report_spec?.sortSpec
  const directSortSpec = report?.sortSpec
  const source = (datasetSortSpec && typeof datasetSortSpec === 'object' ? datasetSortSpec : directSortSpec) || {}
  const explicitMetricLabel = getQuestionRankingMetricLabel()
  if (!explicitMetricLabel || report?.answerMode !== 'ranking') return source
  return {
    ...source,
    metricLabel: explicitMetricLabel,
    direction: source.direction || (isNegativeRankingQuestion() ? 'asc' : 'desc'),
  }
}

const getSortMetricLabel = (report = null, fallback = '达成率') => (
  (report?.answerMode === 'ranking' ? getQuestionRankingMetricLabel() : '')
  || getReportSortSpec(report).metricLabel
  || report?.primaryAnswer?.metricLabel
  || report?.filterAnswer?.metricLabel
  || fallback
)

const normalizeRankingPrimaryAnswer = (report, offices = []) => {
  const answer = report?.primaryAnswer || {}
  if (report?.answerMode !== 'ranking') return answer
  const metricLabel = getQuestionRankingMetricLabel() || getReportSortSpec(report).metricLabel || answer?.metricLabel || '达成率'
  const levelLabel = report?.compareLevelLabel || answer?.targetLevel || '对象'
  const count = offices.length || Number(answer?.count || answer?.total || 0) || 0
  return {
    ...answer,
    title: answer?.title || '排名结果',
    text: `已按${metricLabel}输出${count ? ` ${count} 个` : ''}${levelLabel}的排序结果`,
    metricLabel,
    targetLevel: levelLabel,
    direction: getReportSortSpec(report).direction || answer?.direction || (isNegativeRankingQuestion() ? 'asc' : 'desc'),
  }
}

const sortOfficesByAnswerMetric = (offices = [], report = null) => {
  if (!Array.isArray(offices) || !offices.length) return []
  const sortSpec = getReportSortSpec(report)
  const metricLabel = getSortMetricLabel(report, '')
  if (!metricLabel) return [...offices]
  const lowFirst = (sortSpec.direction || report?.primaryAnswer?.direction || '').toLowerCase() === 'asc'
  return [...offices].sort((left, right) => {
    const leftValue = getMetricValueFromOffice(left, metricLabel)
    const rightValue = getMetricValueFromOffice(right, metricLabel)
    if (leftValue === null && rightValue === null) return 0
    if (leftValue === null) return 1
    if (rightValue === null) return -1
    return lowFirst ? leftValue - rightValue : rightValue - leftValue
  })
}

const getSingleOrgRateTone = (report) => {
  const rate = toNumber(getReportKpiText(report, 'rate'))
  if (rate === null) return 'neutral'
  return rate < 10 ? 'danger' : rate < 15 ? 'warn' : 'good'
}

const getSingleOrgConclusion = (report) => {
  if (!report) return ''
  const focusName = report.focusName || '当前组织'
  const task = getReportKpiText(report, 'task')
  const actual = getReportKpiText(report, 'actual')
  const rate = getReportKpiText(report, 'rate')
  const remain = getReportKpiText(report, 'remain')
  const remainText = remain && remain !== '-' ? `，剩余缺口 ${remain}` : ''
  const toneLabel = {
    good: '整体进度相对领先',
    warn: '整体进度偏滞后',
    danger: '整体进度明显滞后',
    neutral: '整体进度已形成初步判断',
  }[getSingleOrgRateTone(report)]
  return `${focusName}${toneLabel}，年度总任务 ${task}，当前开单 ${actual}，整体达成率 ${rate}${remainText}。`
}

const getSingleOrgRankContext = (report) => {
  const offices = report?.offices || []
  const ranked = [...offices].filter(item => item.rate !== null).sort((a, b) => (b.rate || 0) - (a.rate || 0))
  const best = ranked[0]
  const worst = ranked[ranked.length - 1]
  const diff = best && worst && best.rate !== null && worst.rate !== null
    ? Math.abs((best.rate || 0) - (worst.rate || 0)).toFixed(2).replace(/\.?0+$/, '')
    : ''
  return { best, worst, diff }
}

const getReportMetricContext = (report) => {
  const metricLabel = getSortMetricLabel(report, '达成率')
  const sortSpec = getReportSortSpec(report)
  const lowFirst = String(sortSpec.direction || report?.primaryAnswer?.direction || '').toLowerCase() === 'asc'
  const ranked = sortOfficesByAnswerMetric(
    (report?.offices || []).filter(item => getMetricValueFromOffice(item, metricLabel) !== null),
    report,
  )
  const best = ranked[0] || null
  const worst = ranked[ranked.length - 1] || null
  const bestValue = best ? getMetricValueFromOffice(best, metricLabel) : null
  const worstValue = worst ? getMetricValueFromOffice(worst, metricLabel) : null
  const diff = bestValue !== null && worstValue !== null && best?.name !== worst?.name
    ? (isRateMetricLabel(metricLabel)
      ? `${Math.abs(bestValue - worstValue).toFixed(2).replace(/\.?0+$/, '')}个百分点`
      : formatAmount(Math.abs(bestValue - worstValue)))
    : ''
  return { metricLabel, lowFirst, ranked, best, worst, diff }
}

const isCollectionAnswerMode = (report) => ['filter', 'ranking', 'drilldown'].includes(report?.answerMode || '')
const isRateMetricLabel = (label = '') => /达成率|完成率|rate|percent/i.test(String(label || ''))
const isAmountMetricLabel = (label = '') => /开单|金额|任务|销售|完成|实际/i.test(String(label || ''))
const findOfficeMetricValueByLabel = (office, label = '') => {
  const kpis = Array.isArray(office?.kpis) ? office.kpis : []
  const text = String(label || '')
  if (!text) return ''
  const direct = kpis.find(item => {
    const itemLabel = String(item?.label || '')
    return itemLabel && (itemLabel.includes(text) || text.includes(itemLabel))
  })
  if (direct?.value) return direct.value
  if (isRateMetricLabel(text)) return office?.rateLabel || ''
  if (/开单|完成|实际|销售/i.test(text)) return getOfficeKpiLabel(office, 'actual')
  if (/任务|目标/i.test(text)) return getOfficeKpiLabel(office, 'task')
  if (/剩余|缺口|差额|remain/i.test(text)) return getOfficeKpiLabel(office, 'remain')
  return ''
}

const buildCollectionMetricCards = (report) => {
  const offices = sortOfficesByAnswerMetric(report?.offices, report)
  if (!offices.length) return []
  const leader = offices[0] || null
  const tail = offices[offices.length - 1] || null
  const metricLabel = getSortMetricLabel(report, '指标')
  const metricValue = (office) => (
    findOfficeMetricValueByLabel(office, metricLabel)
    || (isAmountMetricLabel(metricLabel) ? getOfficeKpiLabel(office, 'actual') : '')
    || office?.rateLabel
    || '-'
  )
  const riskCount = getReportRiskCount(report)
  return [
    {
      label: report?.answerMode === 'filter' ? '命中数量' : '结果数量',
      value: `${offices.length} 个`,
      hint: `${report?.compareLevelLabel || '对象'}结果集合`,
      tone: 'neutral',
    },
    leader ? {
      label: report?.answerMode === 'ranking' ? '榜首结果' : '最高结果',
      value: leader.name,
      hint: `${metricLabel} ${metricValue(leader)}`,
      tone: 'good',
    } : null,
    tail ? {
      label: report?.answerMode === 'ranking' ? '末位结果' : '边界结果',
      value: tail.name,
      hint: `${metricLabel} ${metricValue(tail)}`,
      tone: report?.answerMode === 'ranking' ? 'warn' : 'neutral',
    } : null,
    {
      label: '风险节点',
      value: `${riskCount} 个`,
      hint: riskCount ? '存在明显滞后对象，建议继续下钻' : '当前结果内暂无明显风险节点',
      tone: riskCount ? 'danger' : 'good',
    },
  ].filter(Boolean)
}

const enrichSingleOrgMetricCards = (cards = [], report) => (
  (cards || []).map((card) => {
    const label = card.label || ''
    let hint = ''
    let tone = ''
    if (/总任务|任务金额|目标/i.test(label)) {
      hint = `${report?.focusName || '当前组织'}年度目标总量`
    } else if (/年度开单|开单|完成|实际|销售/i.test(label)) {
      hint = '当前已完成金额'
    } else if (/达成率|percent|rate/i.test(label)) {
      tone = getSingleOrgRateTone(report)
      hint = tone === 'good' ? '高于标杆线，保持节奏' : tone === 'danger' ? '低于风险线，需重点干预' : '低于预期进度，需持续跟进'
    } else if (/剩余|缺口|差额|remain/i.test(label)) {
      tone = 'warn'
      hint = '后续需推进缺口金额'
    }
    return { ...card, hint, tone }
  })
)

const getDrillBestText = (office) => {
  const rows = Array.isArray(office?.detailRows) ? office.detailRows : []
  const best = rows.filter(item => item.rate !== null && item.rate !== undefined)
    .sort((left, right) => (right.rate || 0) - (left.rate || 0))[0]
  if (!best) return office?.highlight || '暂无下级明细'
  return `${best.name} ${best.rateLabel || '-'}`
}

const getDrillWorstText = (office) => {
  const rows = Array.isArray(office?.detailRows) ? office.detailRows : []
  const worst = rows.filter(item => item.rate !== null && item.rate !== undefined)
    .sort((left, right) => (left.rate || 0) - (right.rate || 0))[0]
  if (!worst) return office?.riskSummary || '暂无风险明细'
  return `${worst.name} ${worst.rateLabel || '-'}`
}

const findColumn = (columns = [], matcher) => columns.find(column => matcher(String(column || ''))) || ''

const buildOfficeDetailRows = (chartSpec = {}, config = {}) => {
  const rows = Array.isArray(chartSpec.rows) ? chartSpec.rows : []
  const columns = Array.isArray(chartSpec.columns) && chartSpec.columns.length
    ? chartSpec.columns
    : Object.keys(rows[0] || {})
  const dataset = chartSpec?.dataset || null
  const nameColumn = columns[0] || '名称'
  const rateColumn = findColumn(columns, column => isRateColumn(column)) || '达成率'
  const taskColumn = findColumn(columns, column => /任务|目标/i.test(column) && !/剩余|缺口/i.test(column))
  const actualColumn = findColumn(columns, column => /开单|完成|实际|销售/i.test(column))
  const remainColumn = findColumn(columns, column => /剩余|缺口|差额|remain/i.test(column))

  return rows.map((row) => {
    const rate = toNumber(row?.[rateColumn]) || 0
    const remain = toNumber(row?.[remainColumn]) || 0
    const task = toNumber(row?.[taskColumn]) || 0
    const actual = toNumber(row?.[actualColumn]) || 0
    const label = row?.标签 || getOfficeRateTag(rate, config, '标杆')
    return {
      name: row?.[nameColumn] || row?.名称 || '-',
      rate,
      rateLabel: isRateColumn(rateColumn) ? `${rate.toLocaleString('zh-CN', { maximumFractionDigits: 2 })}%` : formatDisplayValue(rate),
      task,
      taskLabel: taskColumn ? formatAmount(task, resolveAmountMetric({ format: 'amount', column: taskColumn }, dataset, taskColumn)) : '-',
      actual,
      actualLabel: actualColumn ? formatAmount(actual, resolveAmountMetric({ format: 'amount', column: actualColumn }, dataset, actualColumn)) : '-',
      remain,
      remainLabel: remainColumn ? formatAmount(remain, resolveAmountMetric({ format: 'amount', column: remainColumn }, dataset, remainColumn)) : '-',
      label,
      tone: getToneFromDisplayTag(label, getOfficeRateTone(rate, config)),
      progress: Math.max(0, Math.min(100, rate)),
      gapProgress: 0,
    }
  }).map((row, _index, list) => {
    const maxRemain = Math.max(...list.map(item => item.remain || 0), 1)
    return {
      ...row,
      gapProgress: Math.max(0, Math.min(100, ((row.remain || 0) / maxRemain) * 100)),
    }
  })
}

const getDescendantNodes = (node) => {
  const output = []
  const walk = (current) => {
    ;(current?.children || []).forEach((child) => {
      output.push(child)
      walk(child)
    })
  }
  walk(node)
  return output
}

const isLeafNode = (node) => !Array.isArray(node?.children) || node.children.length === 0

const getLevelLabelFromNodes = (nodes = [], fallback = '层级') => {
  const values = Array.from(new Set(nodes.map(node => node?.levelValue || node?.levelName).filter(Boolean)))
  if (values.length === 1) return values[0]
  if (values.length > 1) return values.join(' / ')
  return fallback
}

const findQuestionFocusNode = (nodes = []) => {
  const questionText = String(session.state.question || query.value || '').trim()
  if (!questionText) return null
  return [...nodes]
    .filter(node => node?.name && questionText.includes(node.name) && Array.isArray(node.children) && node.children.length > 0)
    .sort((a, b) => String(b.name).length - String(a.name).length)[0] || null
}

const getComparisonNodes = (model) => {
  const focusNode = findQuestionFocusNode(model.flatNodes || [])
  const requestedLevels = getRequestedLevelValues(getQuestionText(), model.config || {})
  if (requestedLevels.length) {
    const scopedNodes = focusNode ? getDescendantNodes(focusNode) : (model.flatNodes || [])
    const levelNodes = scopedNodes.filter(node => (
      node?.name
      && (
        requestedLevels.includes(canonicalRequestedLevel(node.levelValue))
        || requestedLevels.includes(canonicalRequestedLevel(node.levelName))
        || requestedLevels.some(value => value && String(node.name || '').includes(value))
      )
    ))
    if (levelNodes.length) return levelNodes
  }
  if (focusNode?.children?.length) return focusNode.children
  const singleRoot = model.tree?.length === 1 ? model.tree[0] : null
  if (singleRoot?.children?.length) return singleRoot.children
  const parentNodes = (model.flatNodes || []).filter(node => Array.isArray(node.children) && node.children.length > 0)
  const maxParentDepth = Math.max(...parentNodes.map(node => Number(node.depth) || 0), 0)
  return parentNodes.filter(node => Number(node.depth) === maxParentDepth)
}

const getDetailNodes = (node) => {
  const directChildren = (node?.children || []).filter(item => item?.name)
  if (directChildren.length) return directChildren
  return getDescendantNodes(node).filter(item => item?.name)
}

const hasBusinessDrillDataset = (datasets) => (
  (datasets || []).some(dataset => Boolean(buildBusinessDrillReport(dataset)))
)

const buildBusinessDrillReportFromSpec = (dataset) => {
  const spec = dataset?.report_spec
  if (!spec || spec.version !== '2.0') return null
  const overviewChart = Array.isArray(spec.charts) ? spec.charts[0] : null
  const rawAccordions = Array.isArray(spec.accordions) ? spec.accordions : []
  const overviewRows = Array.isArray(overviewChart?.rows) ? overviewChart.rows : []
  if (!overviewChart && !rawAccordions.length) return null

  const config = getDatasetReportConfig(dataset)
  const requestedLevels = getRequestedLevelValues(getQuestionText(), config)
  const compareLevelLabel = requestedLevels[0] || spec.scope?.compareLevelLabel || '下一层级'
  const detailLevelLabel = spec.scope?.detailLevelLabel || '明细层级'
  const inferredDetailLevelLabel = getKnownChildLevelLabel(compareLevelLabel) || detailLevelLabel
  const accordions = rawAccordions.length
    ? rawAccordions
    : overviewRows.map((row, index) => {
        const name = row?.名称 || row?.name || row?.[overviewChart?.columns?.[0]] || `当前层对象 ${index + 1}`
        return {
          id: `overview-${index}-${name}`,
          title: name,
          parentName: spec.scope?.focusNode || '',
          levelLabel: compareLevelLabel,
          detailLevelLabel: inferredDetailLevelLabel,
          isLeafLevel: !getKnownChildLevelLabel(compareLevelLabel),
          leafLabel: getKnownChildLevelLabel(compareLevelLabel) ? '' : '当前最细层',
          childCount: 0,
          tag: row?.标签 || '',
          kpis: Object.entries(row || {})
            .filter(([key]) => !['名称', 'name', '标签'].includes(key))
            .map(([key, value]) => ({ label: key, value })),
          narrative: `${name}已是当前结果的最细层级。`,
          detailNarrative: `${name}已是当前结果的最细层级，右侧展示该节点当前指标。`,
          chart: {
            chartType: overviewChart?.chartType || 'horizontalDrill',
            title: `${name}当前层指标`,
            columns: overviewChart?.columns || Object.keys(row || {}),
            rows: [row],
            dataset,
          },
          drillGroups: [],
        }
      })
  const matchedAccordions = requestedLevels.length
    ? accordions.filter(item => (
        requestedLevels.includes(item?.levelLabel)
        || requestedLevels.some(value => value && String(item?.title || '').includes(value))
      ))
    : []
  const sourceAccordions = requestedLevels.length && matchedAccordions.length ? matchedAccordions : accordions
  const mappedOffices = sourceAccordions.map((item) => {
    const itemLevelLabel = item.levelLabel || compareLevelLabel
    const knownChildLevelLabel = getKnownChildLevelLabel(itemLevelLabel)
    const itemDetailLevelLabel = item.detailLevelLabel || knownChildLevelLabel || detailLevelLabel
    const rateKpi = (item.kpis || []).find(kpi => /率|percent|rate/i.test(kpi.label || ''))
    const rateValue = toNumber(rateKpi?.value)
    const chartRows = Array.isArray(item.chart?.rows) ? item.chart.rows : []
    const narrative = String(item.narrative || '').trim()
    const detailRows = buildOfficeDetailRows({ ...(item.chart || {}), dataset }, config)
    const drillGroups = (Array.isArray(item.drillGroups) ? item.drillGroups : [])
      .map((group) => {
        const groupRateKpi = (group.kpis || []).find(kpi => /率|percent|rate/i.test(kpi.label || ''))
        const groupRateValue = toNumber(groupRateKpi?.value)
        const groupRows = buildOfficeDetailRows({ ...(group.chart || {}), dataset }, config)
        const groupTag = group.tag || getOfficeRateTag(groupRateValue, config, '片区标杆')
        return {
          id: group.id || `${item.id || item.title}-${group.title}`,
          name: group.title || '未命名下级节点',
          parentName: group.parentName || item.title || '',
          tone: getToneFromDisplayTag(groupTag, getOfficeRateTone(groupRateValue, config)),
          tag: groupTag,
          rate: groupRateValue,
          rateLabel: groupRateKpi?.value || '-',
          progress: Math.max(0, Math.min(100, groupRateValue || 0)),
          childCount: groupRows.length,
          kpis: group.kpis || [],
          summary: String(group.narrative || '').trim(),
          chartText: group.detailNarrative || (groupRows.length ? `${group.title || '当前节点'}继续下钻到${group.detailLevelLabel || '业务员'}。` : ''),
          detailLevelLabel: group.detailLevelLabel || '业务员',
          detailRows: groupRows,
        }
      })
      .filter(group => group.detailRows.length > 0)
    const summaryText = narrative
      .split('\n')
      .map(line => line.trim())
      .filter(Boolean)
      .slice(0, 3)
      .join('；') || narrative
    const itemTag = item.tag || getOfficeRateTag(rateValue, config, '区域标杆')
    return {
      id: item.id || item.title,
      name: item.title || '未命名节点',
      parentName: item.parentName || item.levelLabel || '',
      tone: getToneFromDisplayTag(itemTag, getOfficeRateTone(rateValue, config)),
      tag: itemTag,
      highlight: item.highlight || '',
      rankLabel: item.rankLabel || '',
      rate: rateValue,
      rateLabel: rateKpi?.value || '-',
      progress: Math.max(0, Math.min(100, rateValue || 0)),
      childCount: Number.isFinite(Number(item.childCount)) ? Number(item.childCount) : chartRows.length,
      isLeafLevel: knownChildLevelLabel ? false : Boolean(item.isLeafLevel),
      leafLabel: knownChildLevelLabel ? '' : (item.leafLabel || ''),
      kpis: item.kpis || [],
      summary: summaryText,
      chartText: item.detailNarrative || '',
      chartSpec: item.chart,
      detailRows,
      drillGroups,
      detailLevelLabel: itemDetailLevelLabel,
    }
  })
  const answerMode = spec.answerMode || spec.analysisMode || 'detail'
  const answerSummary = spec.answerSummary || {}
  const reportContext = {
    dataset,
    sortSpec: spec.sortSpec || {},
    answerMode,
    primaryAnswer: ['ranking', 'drilldown'].includes(answerMode) ? answerSummary : null,
    filterAnswer: answerMode === 'filter' ? answerSummary : null,
  }
  const offices = sortOfficesByAnswerMetric(mappedOffices, reportContext).map((office, index) => {
    if (answerMode !== 'ranking') return office
    const childLevelLabel = getKnownChildLevelLabel(compareLevelLabel)
    const summary = childLevelLabel
      ? `${office.name}${office.tag ? ` ${office.tag}` : ''}；总任务金额 ${getOfficeKpiLabel(office, 'task')}，年度开单金额 ${getOfficeKpiLabel(office, 'actual')}，达成率 ${getOfficeKpiLabel(office, 'rate')}，剩余任务金额 ${getOfficeKpiLabel(office, 'remain')}。可继续下钻查看${childLevelLabel}明细。`
      : String(office.summary || '').replace(/（排序第\d+）/g, '')
    return {
      ...office,
      rankLabel: `排序第${index + 1}`,
      summary,
    }
  })
  const riskCount = getReportRiskCount({ ...reportContext, offices })
  const officeNames = new Set(offices.map(item => item.name))
  const filteredOverviewChart = overviewChart && officeNames.size
    ? {
        ...overviewChart,
        rows: (overviewChart.rows || []).filter(row => officeNames.has(row?.名称 || row?.name || row?.[overviewChart.columns?.[0]])),
      }
    : overviewChart
  const summary = Array.isArray(spec.narrative) && spec.narrative.length
    ? spec.narrative.join('；')
    : spec.sections?.find(section => section.key === 'overview')?.narrative || `本次结果覆盖 ${offices.length} 个${compareLevelLabel}。`
  const matchedNodes = Array.isArray(spec.matchedNodes) ? spec.matchedNodes : []
  const filterAnswer = spec.answerMode === 'filter'
    ? {
        ...spec.answerSummary,
        nodes: matchedNodes.map((node) => {
          const office = offices.find(item => item.name === node.name)
          const metric = node.metric || {}
          return {
            id: office?.id || node.id || node.name,
            name: node.name || '未命名对象',
            levelLabel: node.levelLabel || compareLevelLabel,
            tag: node.tag || office?.tag || '',
            tone: office?.tone || getOfficeRateTone(toNumber(metric.rawValue), config),
            metricLabel: metric.label || spec.answerSummary?.metricLabel || '指标',
            metricValue: metric.value ?? formatDisplayValue(metric.rawValue),
            kpis: Array.isArray(node.kpis) ? node.kpis : [],
          }
        }),
      }
    : null
  let primaryAnswer = ['ranking', 'drilldown'].includes(spec.answerMode)
    ? {
        ...spec.answerSummary,
      }
    : null

  const sortMetricLabel = getSortMetricLabel({ ...reportContext, primaryAnswer, filterAnswer }, '达成率')
  primaryAnswer = normalizeRankingPrimaryAnswer({ ...reportContext, primaryAnswer, filterAnswer, compareLevelLabel }, offices)

  return {
    dataset,
    sortSpec: spec.sortSpec || {},
    analysisMode: spec.analysisMode || 'detail',
    answerMode,
    primaryAnswer,
    filterAnswer,
    focusName: spec.scope?.focusNode || '',
    isSingleFocus: Boolean(spec.scope?.focusNode && spec.analysisMode !== 'comparative'),
    kpis: (spec.kpis || []).map(item => ({
      label: item.label || item.key,
      value: item.displayValue ?? formatDisplayValue(item.value),
    })).filter(item => item.label),
    offices,
    compareLevelLabel,
    detailLevelLabel: inferredDetailLevelLabel,
    officeCompareSpec: normalizeOfficeCompareSpec(filteredOverviewChart, config),
    officeCompareText: getKnownChildLevelLabel(compareLevelLabel)
      ? `当前结果按${compareLevelLabel}展示；${compareLevelLabel}下级为${inferredDetailLevelLabel}，可继续下钻查看${inferredDetailLevelLabel}明细。`
      : spec.sections?.find(section => section.key === 'drill')?.narrative || `一行一个同层级对象，按${sortMetricLabel}排序；对齐展示任务、开单、缺口、达成率和进度条，必要时继续下钻。`,
    summary,
    riskTone: riskCount ? 'danger' : 'good',
    riskLabel: riskCount ? `风险 ${riskCount} 个` : '整体可控',
  }
}

const buildBusinessDrillReport = (dataset) => {
  const specReport = buildBusinessDrillReportFromSpec(dataset)
  if (specReport) return specReport

  const model = getDatasetTreeModel(dataset)
  if (!model?.flatNodes?.length) return null
  const config = model.config || getDatasetReportConfig(dataset)
  const taskMetric = getMetricDefinition(config, 'task', item => /任务|目标/i.test(item.label || item.column || ''))
  const actualMetric = getMetricDefinition(config, 'actual', item => /开单|完成|实际/i.test(item.label || item.column || ''))
  const rateMetric = getMetricDefinition(config, 'rate', item => item.format === 'percent' || /率|rate/i.test(item.label || item.column || ''))
  const remainMetric = getMetricDefinition(config, 'remain', item => /剩余|缺口|差额/i.test(item.label || item.column || ''))
  if (!rateMetric) return null
  const rankingMetric = isAmountRankingQuestion() ? (actualMetric || rateMetric) : rateMetric
  const rankingMetricLabel = rankingMetric?.label || rankingMetric?.column || '达成率'
  const rankingChartType = isAmountRankingQuestion() ? 'bar' : 'horizontalRateBar'

  const focusNode = findQuestionFocusNode(model.flatNodes || [])
  const isSingleFocus = Boolean(focusNode && !/对比|比较|哪个|谁更|差异|分别|各自|和.+比|跟.+比|与.+比|\bvs\b/i.test(session.state.question || query.value || ''))
  const officeNodes = getComparisonNodes(model)
    .filter(node => node?.name)

  if (!officeNodes.length) return null
  const compareLevelLabel = getLevelLabelFromNodes(officeNodes, '下一层级')
  const detailLevelLabel = getLevelLabelFromNodes(officeNodes.flatMap(getDetailNodes), '明细层级')

  const offices = officeNodes.map((office) => {
    const people = getDetailNodes(office)
    const directChildren = people.length ? people : office.children || []
    const sortedPeople = [...directChildren]
      .filter(item => item?.name)
      .sort((a, b) => (getNodeMetricValue(a, rankingMetric) || 0) - (getNodeMetricValue(b, rankingMetric) || 0))
    const sortedPeopleDesc = [...sortedPeople].sort((a, b) => (getNodeMetricValue(b, rateMetric) || 0) - (getNodeMetricValue(a, rateMetric) || 0))
    const rate = getNodeMetricValue(office, rateMetric)
    const tone = getOfficeRateTone(rate, config)
    const riskPeople = sortedPeople.filter(item => getRateTone(getNodeMetricValue(item, rateMetric), 20, 10) === 'danger')
    const bestPerson = sortedPeopleDesc[0]
    const worstPerson = sortedPeople[0]
    const formatPersonMetric = (person, metric) => (
      metric ? formatMetricByDefinition(getNodeMetricValue(person, metric), metric, dataset) : '-'
    )
    const describePerson = (person) => {
      if (!person) return ''
      const actualText = formatPersonMetric(person, actualMetric)
      const taskText = formatPersonMetric(person, taskMetric)
      const remainText = formatPersonMetric(person, remainMetric)
      const rateText = formatPersonMetric(person, rateMetric)
      return `${person.name}开单${actualText} / 任务${taskText}，达成率${rateText}${remainMetric ? `，剩余缺口${remainText}` : ''}`
    }
    const chartPeople = isNegativeRankingQuestion() ? sortedPeople : [...directChildren]
      .filter(item => item?.name)
      .sort((a, b) => (getNodeMetricValue(b, rankingMetric) || 0) - (getNodeMetricValue(a, rankingMetric) || 0))
    const chartRows = chartPeople.map(person => {
      const personRate = getNodeMetricValue(person, rateMetric) || 0
      return {
      名称: person.name,
      [rateMetric.label || rateMetric.column || '达成率']: personRate,
      [actualMetric?.label || actualMetric?.column || '完成']: getNodeMetricValue(person, actualMetric) || 0,
      [taskMetric?.label || taskMetric?.column || '任务']: getNodeMetricValue(person, taskMetric) || 0,
      ...(remainMetric ? { [remainMetric.label || remainMetric.column || '剩余']: getNodeMetricValue(person, remainMetric) || 0 } : {}),
      标签: getOfficeRateTag(personRate, config, '标杆'),
    }
    })
    const officeKpis = [
      taskMetric ? { label: taskMetric.label || taskMetric.column, value: formatMetricByDefinition(getNodeMetricValue(office, taskMetric), taskMetric, dataset) } : null,
      actualMetric ? { label: actualMetric.label || actualMetric.column, value: formatMetricByDefinition(getNodeMetricValue(office, actualMetric), actualMetric, dataset) } : null,
      { label: rateMetric.label || rateMetric.column || '达成率', value: formatMetricByDefinition(rate, rateMetric, dataset) },
      remainMetric ? { label: remainMetric.label || remainMetric.column, value: formatMetricByDefinition(getNodeMetricValue(office, remainMetric), remainMetric, dataset) } : null,
    ].filter(Boolean)

    return {
      id: office.id || office.name,
      name: office.name,
      parentName: office.parentName,
      tone,
      rate,
      rateLabel: formatMetricByDefinition(rate, rateMetric, dataset),
      progress: Math.max(0, Math.min(100, rate || 0)),
      childCount: sortedPeople.length,
      isLeafLevel: sortedPeople.length === 0,
      leafLabel: sortedPeople.length === 0 ? '当前最细层' : '',
      kpis: officeKpis,
      tag: getOfficeRateTag(rate, config, '区域标杆'),
      highlight: bestPerson ? `亮点：${bestPerson.name}达成率${formatPersonMetric(bestPerson, rateMetric)}` : '',
      rankLabel: '',
      summary: `${office.name}达成率${formatMetricByDefinition(rate, rateMetric, dataset)}，${getOfficeToneLabel(tone)}；任务${taskMetric ? formatMetricByDefinition(getNodeMetricValue(office, taskMetric), taskMetric, dataset) : '-'} / 已完成${actualMetric ? formatMetricByDefinition(getNodeMetricValue(office, actualMetric), actualMetric, dataset) : '-'}${remainMetric ? ` / 缺口${formatMetricByDefinition(getNodeMetricValue(office, remainMetric), remainMetric, dataset)}` : ''}。${bestPerson ? `亮点：${bestPerson.name}达成率${formatPersonMetric(bestPerson, rateMetric)}` : `暂无${detailLevelLabel}明细`}；${riskPeople.length ? `${riskPeople.length} 个${detailLevelLabel}低于10%风险线` : `暂无低于10%的风险${detailLevelLabel}`}。`,
      chartText: `${office.name}下钻到${detailLevelLabel}层：${bestPerson ? `最高为${describePerson(bestPerson)}` : `暂无${detailLevelLabel}明细`}；${worstPerson ? `最低为${describePerson(worstPerson)}。` : ''}`,
      chartSpec: {
        chartType: 'horizontalDrill',
        title: `${office.name}${detailLevelLabel}达成率与缺口`,
        columns: ['名称', actualMetric?.label || actualMetric?.column || '完成', taskMetric?.label || taskMetric?.column || '任务', remainMetric?.label || remainMetric?.column || '剩余', rateMetric.label || rateMetric.column || '达成率'].filter(Boolean),
        rows: chartRows,
        dataset,
      },
      detailRows: buildOfficeDetailRows({
        columns: ['名称', actualMetric?.label || actualMetric?.column || '完成', taskMetric?.label || taskMetric?.column || '任务', remainMetric?.label || remainMetric?.column || '剩余', rateMetric.label || rateMetric.column || '达成率'].filter(Boolean),
        rows: chartRows,
      }, config),
    }
  }).sort((a, b) => {
    const left = getMetricValueFromOffice(a, rankingMetricLabel) || 0
    const right = getMetricValueFromOffice(b, rankingMetricLabel) || 0
    return isNegativeRankingQuestion() ? left - right : right - left
  })

  const kpis = (config.metrics || []).map(metric => ({
    label: metric.label || metric.column || metric.key,
    value: formatMetricByDefinition(model.rootMetrics?.[metric.key], metric, dataset),
  })).filter(item => item.value !== '-')
  const bestOffice = offices[0]
  const worstOffice = offices[offices.length - 1]
  const riskCount = offices.filter(item => item.tone === 'danger').length
  const officeCompareRows = offices.map(office => ({
    名称: office.name,
    [actualMetric?.label || actualMetric?.column || '完成']: getNodeMetricValue(officeNodes.find(node => node.name === office.name), actualMetric) || 0,
    [taskMetric?.label || taskMetric?.column || '任务']: getNodeMetricValue(officeNodes.find(node => node.name === office.name), taskMetric) || 0,
    ...(remainMetric ? { [remainMetric.label || remainMetric.column || '剩余']: getNodeMetricValue(officeNodes.find(node => node.name === office.name), remainMetric) || 0 } : {}),
    [rateMetric.label || rateMetric.column || '达成率']: office.rate || 0,
    标签: office.tag,
  })).sort((a, b) => {
    const key = rankingMetric.label || rankingMetric.column || '达成率'
    return isNegativeRankingQuestion()
      ? (a[key] || 0) - (b[key] || 0)
      : (b[key] || 0) - (a[key] || 0)
  })
  const officeCompareSpec = {
    chartType: rankingChartType,
    title: `各${compareLevelLabel}${rankingMetricLabel}排序`,
    columns: ['名称', actualMetric?.label || actualMetric?.column || '完成', taskMetric?.label || taskMetric?.column || '任务', remainMetric?.label || remainMetric?.column || '剩余', rateMetric.label || rateMetric.column || '达成率', '标签'].filter(Boolean),
    rows: officeCompareRows,
    sortColumn: rankingMetricLabel,
    lowFirst: isNegativeRankingQuestion(),
  }
  return {
    dataset,
    analysisMode: isSingleFocus ? 'detail' : 'comparative',
    focusName: focusNode?.name || '',
    isSingleFocus,
    kpis: kpis.slice(0, 6),
    offices,
    compareLevelLabel,
    detailLevelLabel,
    officeCompareSpec,
    officeCompareText: isNegativeRankingQuestion()
      ? `${worstOffice ? `${worstOffice.name}达成率最低，为${worstOffice.rateLabel}` : ''}${bestOffice ? `；最高为${bestOffice.name}，${bestOffice.rateLabel}` : ''}。按低达成率优先展示，便于定位承压节点。`
      : `${bestOffice ? `${bestOffice.name}${rankingMetricLabel}最高，为${findOfficeMetricValueByLabel(bestOffice, rankingMetricLabel) || '-'}` : ''}${worstOffice ? `；${worstOffice.name}${rankingMetricLabel}最低，为${findOfficeMetricValueByLabel(worstOffice, rankingMetricLabel) || '-'}` : ''}。一行一个同层级对象，对齐展示金额和进度条。`,
    summary: isNegativeRankingQuestion()
      ? `本次结果覆盖 ${offices.length} 个${compareLevelLabel}，已按低达成率优先排序。${worstOffice ? `${worstOffice.name}当前完成最弱，达成率${worstOffice.rateLabel}` : ''}${bestOffice ? `；最高为${bestOffice.name}，达成率${bestOffice.rateLabel}` : ''}。`
      : `本次结果覆盖 ${offices.length} 个${compareLevelLabel}。${bestOffice ? `${bestOffice.name}${rankingMetricLabel}最高，为${findOfficeMetricValueByLabel(bestOffice, rankingMetricLabel) || '-'}` : ''}${worstOffice ? `；${worstOffice.name}${rankingMetricLabel}最低，为${findOfficeMetricValueByLabel(worstOffice, rankingMetricLabel) || '-'}` : ''}。`,
    riskTone: riskCount ? 'danger' : 'good',
    riskLabel: riskCount ? `风险 ${riskCount} 个` : '整体可控',
  }
}

const getBusinessMetricCards = (dataset) => {
  const model = getDatasetTreeModel(dataset)
  if (!model?.levelSections?.length) return []
  const config = model.config || getDatasetReportConfig(dataset)
  const cards = []
  ;(config.metrics || []).forEach((metric) => {
    const value = model.rootMetrics?.[metric.key]
    if (value !== null && value !== undefined) {
      cards.push({ label: metric.label || metric.column || metric.key, value: formatMetricByDefinition(value, metric, dataset) })
    }
  })
  model.levelSections.slice(0, 2).forEach((section) => {
    cards.push({ label: `${section.levelName}数量`, value: formatDisplayValue(section.nodes.length) })
  })
  return cards.slice(0, 6)
}

const buildLayeredBusinessCharts = (dataset) => {
  const model = getDatasetTreeModel(dataset)
  if (!model?.levelSections?.length) return []
  const config = model.config || getDatasetReportConfig(dataset)
  const taskMetric = config.metrics?.find(item => item.key === 'task')
  const actualMetric = config.metrics?.find(item => item.key === 'actual')
  const rateMetric = config.metrics?.find(item => item.key === 'rate') || config.metrics?.find(item => item.format === 'percent')
  if (!rateMetric) return []
  const requestedLevels = getRequestedLevelValues(getQuestionText(), config)

  return model.levelSections
    .filter(section => (
      !requestedLevels.length
      || requestedLevels.some(value => section.levelValues?.includes(value) || section.levelName?.includes(value))
    ))
    .map((section) => {
      const rows = section.nodes
        .map(node => ({
          名称: node.name,
          [taskMetric?.label || taskMetric?.column || '目标']: toNumber(node.raw?.[taskMetric?.column]) ?? 0,
          [actualMetric?.label || actualMetric?.column || '完成']: toNumber(node.raw?.[actualMetric?.column]) ?? 0,
          [rateMetric?.label || rateMetric?.column || '达成率']: toNumber(node.raw?.[rateMetric?.column]) ?? 0,
          signalTone: section.riskNodes.some(item => item.id === node.id) ? 'danger' : section.topNodes.some(item => item.id === node.id) ? 'good' : 'neutral',
        }))
        .filter(row => row.名称)
        .sort((a, b) => {
          const key = rateMetric.label || rateMetric.column || '达成率'
          return isNegativeRankingQuestion()
            ? (a[key] || 0) - (b[key] || 0)
            : (b[key] || 0) - (a[key] || 0)
        })
        .slice(0, 12)
      if (!rows.length) return null
      const titlePrefix = section.trackNames.length ? `${section.trackNames.join(' / ')}：` : ''
      const rateFocused = requestedLevels.length || isRateRankingQuestion()
      const columns = rateFocused
        ? ['名称', rateMetric?.label || rateMetric?.column].filter(Boolean)
        : [
            '名称',
            taskMetric?.label || taskMetric?.column,
            actualMetric?.label || actualMetric?.column,
            rateMetric?.label || rateMetric?.column,
          ].filter(Boolean)
      return {
        chartType: rateFocused ? 'horizontalRateBar' : taskMetric && actualMetric ? 'combo' : 'bar',
        title: `${titlePrefix}${section.levelName}完成情况`,
        columns,
        rows,
        dataset,
        lowFirst: isNegativeRankingQuestion(),
      }
    })
    .filter(Boolean)
}

const inferChartSpec = (dataset) => {
  const rows = dataset?.rows || []
  if (!rows.length) return null

  const layeredCharts = buildLayeredBusinessCharts(dataset)
  if (layeredCharts.length) return layeredCharts[0]

  const labelColumn = getLabelColumn(dataset)
  const numericColumns = getNumericColumns(dataset)
  if (!labelColumn && !numericColumns.length) return null

  const firstRow = rows[0] || {}
  const nameText = `${dataset?.dataset_name || ''} ${(dataset?.analysis || '').slice(0, 80)}`

  if (rows.length === 1) {
    if (numericColumns.length > 0) {
      return {
        chartType: 'metric',
        title: dataset?.dataset_name || '关键指标',
        value: formatValueByColumn(firstRow[numericColumns[0]], numericColumns[0]),
        label: numericColumns[0],
      }
    }
    if (labelColumn) {
      return {
        chartType: 'metric',
        title: dataset?.dataset_name || '关键指标',
        value: formatDisplayValue(firstRow[labelColumn]),
        label: labelColumn,
      }
    }
  }

  if (/日期|时间/.test(labelColumn || '') && numericColumns.length > 0) {
    return {
      chartType: 'trend',
      title: '趋势组合图',
      columns: [labelColumn, ...numericColumns.slice(0, 2)],
      rows,
    }
  }

  if (/Top|TOP|股票|排名/i.test(nameText) || rows.length > 6) {
    return {
      chartType: 'bar',
      title: 'Top 结果分布',
      columns: [labelColumn, numericColumns[0]].filter(Boolean),
      rows,
    }
  }

  if (numericColumns.length > 0) {
    return {
      chartType: /城市|佣金|分布|占比/i.test(nameText) ? 'pie' : 'bar',
      title: /城市|佣金|分布|占比/i.test(nameText) ? '分类占比' : '分类对比',
      columns: [labelColumn, numericColumns[0]].filter(Boolean),
      rows,
    }
  }

  return null
}

const buildSingleRowMetricCharts = (dataset) => {
  const rows = dataset?.rows || []
  if (rows.length !== 1) return []

  const numericColumns = getNumericColumns(dataset)
  const firstRow = rows[0] || {}
  const datasetName = dataset?.dataset_name || '结果图表'
  const charts = []

  if (numericColumns.length >= 2) {
    charts.push({
      chartType: 'bar',
      title: '关键指标对比',
      columns: ['指标', '数值'],
      rows: numericColumns.slice(0, 6).map(column => ({
        指标: column,
        数值: Number(firstRow[column]) || 0,
      })),
    })
  }

  const completedKey = numericColumns.find(column => /开单|完成|达成|实际|已完成/i.test(column))
  const remainKey = numericColumns.find(column => /剩余|未完成|差额|缺口/i.test(column))
  if (completedKey && remainKey) {
    charts.push({
      chartType: 'pie',
      title: '完成与剩余结构',
      columns: ['分类', '数值'],
      rows: [
        { 分类: completedKey, 数值: Math.max(0, Number(firstRow[completedKey]) || 0) },
        { 分类: remainKey, 数值: Math.max(0, Number(firstRow[remainKey]) || 0) },
      ],
    })
  }

  return charts.map((chart, index) => ({
    key: `${dataset?.dataset_id || datasetName}-single-${index}`,
    caption: index === 0 ? '核心图表' : `衍生图表 ${index}`,
    dataset,
    metricCards: getMetricCards(dataset),
    chartSpec: chart,
  }))
}

const hasChartRows = (chartSpec) => Array.isArray(chartSpec?.rows) && chartSpec.rows.length > 0

const getReportSpecCharts = (dataset) => (
  Array.isArray(dataset?.report_spec?.charts)
    ? dataset.report_spec.charts.filter(Boolean)
    : []
)

const dedupeChartSpecs = (charts = []) => {
  const seen = new Set()
  const result = []
  charts.filter(Boolean).forEach((chart) => {
    const columns = Array.isArray(chart.columns) ? chart.columns.join('|') : ''
    const key = `${chart.chartType || ''}-${chart.title || ''}-${columns}`
    if (seen.has(key)) return
    seen.add(key)
    result.push(chart)
  })
  return result
}

const getDatasetChartSpecs = (dataset, { includeFallback = true } = {}) => {
  if (!dataset || typeof dataset !== 'object') return []
  if (dataset?.report_spec?.scope?.focusNodeIsLeaf) {
    const value = []
    datasetChartSpecCache.set(dataset, { key: [getQuestionText(), includeFallback ? 'fallback' : 'strict', 'leaf-focus-none'].join('|'), value })
    return value
  }
  const cacheKey = [
    getQuestionText(),
    includeFallback ? 'fallback' : 'strict',
    canUseFeature('ask_chart_auto_infer') ? 'infer-on' : 'infer-off',
  ].join('|')
  const cached = datasetChartSpecCache.get(dataset)
  if (cached?.key === cacheKey) return cached.value
  const specCharts = getReportSpecCharts(dataset)
  const value = specCharts.length
    ? dedupeChartSpecs(specCharts)
    : (!includeFallback || !canUseFeature('ask_chart_auto_infer')) ? []
    : dedupeChartSpecs([
    ...buildLayeredBusinessCharts(dataset),
    inferChartSpec(dataset),
    ...buildSingleRowMetricCharts(dataset).map(item => item.chartSpec),
  ])
  datasetChartSpecCache.set(dataset, { key: cacheKey, value })
  return value
}

const buildReportTableBlocks = (datasets = []) => {
  return (datasets || [])
    .filter(dataset => Array.isArray(dataset?.rows) && dataset.rows.length > 0 && Array.isArray(dataset?.columns) && dataset.columns.length > 0)
    .slice(0, 3)
    .map((dataset, index) => {
      const labelColumn = getLabelColumn(dataset)
      const numericColumns = getNumericColumns(dataset)
      const pathColumns = (dataset.columns || []).filter(column => /组织路径|归属组织|组织归属|管理链路|路径|上级名称|战区|片区|行业部/.test(column))
      const prioritizedColumns = [
        labelColumn,
        ...pathColumns,
        ...numericColumns,
        ...(dataset.columns || []),
      ].filter(Boolean)
      const columns = Array.from(new Set(prioritizedColumns)).slice(0, 6)
      const title = dataset.rows.length > 6
        ? `${dataset.dataset_name} 结果明细表`
        : `${dataset.dataset_name} 关键结果表`
      const description = dataset.rows.length > 6
        ? '补充展示图表对应的原始数据明细，方便继续核对与下钻。'
        : '提炼当前报告里的关键字段与结果值，便于快速核对。'

      return {
        key: `${dataset.dataset_id || index}-${dataset.dataset_name || 'table'}`,
        dataset,
        title,
        description,
        columns,
        rows: dataset.rows,
      }
    })
}

const resultPreviews = computed(() => (
  datasetResults.value.slice(0, 4).map((dataset, index) => {
    const chartSpecs = getDatasetChartSpecs(dataset)

    return {
      key: `${dataset.dataset_id || index}-${dataset.dataset_name || 'dataset'}`,
      caption: index === 0 ? '主结果视图' : '结果视图',
      dataset,
      metricCards: getMetricCards(dataset),
      chartSpec: chartSpecs[0] || null,
      extraCharts: chartSpecs.slice(1),
    }
  })
))

const sideReportCharts = computed(() => (
  latestDatasets.value
    .slice(0, 3)
    .flatMap((dataset, datasetIndex) => {
      const chartSpecs = getDatasetChartSpecs(dataset)
      return chartSpecs.slice(0, 3).map((chartSpec, chartIndex) => ({
        key: `side-report-chart-${dataset.dataset_id || datasetIndex}-${chartIndex}`,
        caption: chartSpec.title || `图表 ${chartIndex + 1}`,
        dataset,
        chartSpec,
      }))
    })
))

const reportDialogCharts = computed(() => {
  const sourceItems = reportViewerVisible.value
    ? reportViewerDatasets.value.slice(0, 4).flatMap((dataset, index) => {
        const chartSpecs = getDatasetChartSpecs(dataset)
        return chartSpecs.map((chartSpec, chartIndex) => ({
          key: `${dataset.dataset_id || index}-${dataset.dataset_name || 'dataset'}-${chartIndex}`,
          caption: chartSpec.title || (chartIndex === 0 ? '主结果视图' : `图表 ${chartIndex + 1}`),
          dataset,
          metricCards: getMetricCards(dataset),
          chartSpec,
        }))
      })
    : resultPreviews.value.flatMap(item => (
        item?.dataset ? [item, ...buildSingleRowMetricCharts(item.dataset)] : [item]
      ))

  const deduped = []
  const seen = new Set()
  sourceItems.forEach((item) => {
    if (!item?.chartSpec) return
    const key = `${item.key}-${item.chartSpec.chartType}-${item.chartSpec.title || ''}`
    if (seen.has(key)) return
    seen.add(key)
    deduped.push(item)
  })
  return deduped
})

const reportDialogMetricCards = computed(() => {
  const source = reportSourceDatasets.value
  const drillReport = activeBusinessDrillReport.value
  if (drillReport && isCollectionAnswerMode(drillReport)) {
    return buildCollectionMetricCards(drillReport)
  }
  if (drillReport?.kpis?.length) {
    const cards = drillReport.isSingleFocus
      ? drillReport.kpis.slice(0, 4).map(item => ({
          label: item.label || item.key || '',
          value: item.value ?? item.displayValue ?? formatDisplayValue(item.value),
        }))
      : decorateMetricCards(drillReport.kpis, drillReport.offices).slice(0, 8)
    return drillReport.isSingleFocus ? enrichSingleOrgMetricCards(cards, drillReport) : cards
  }
  return (
    (reportViewerVisible.value
      ? (reportViewerDatasets.value[0] ? getMetricCards(reportViewerDatasets.value[0]) : [])
      : resultPreviews.value[0]?.metricCards
    ) || []
  )
})

const reportTableBlocks = computed(() => (
  buildReportTableBlocks(reportSourceDatasets.value)
))

const reportSourceDatasets = computed(() => (
  reportViewerVisible.value ? reportViewerDatasets.value : latestDatasets.value
))

const findBusinessDrillReport = (datasets = []) => {
  const reports = (datasets || [])
    .map(buildBusinessDrillReport)
    .filter(Boolean)
  if (!reports.length) return null
  // 修 4（渲染侧优先级）：优先使用有明确 answerMode 的报告。
  // 用户问 ranking/TopN 问题时，ranking 报告的 offices 是客户经理层级；
  // 若无优先级，dataset_results[0] 若为 Overview 报告（行业部层级）会被误取，
  // 导致 offices 全是行业部/片区节点而不是客户经理。
  const INTENT_MODES = ['ranking', 'filter', 'drilldown', 'comparison']
  const intentful = reports.find(r => INTENT_MODES.includes(String(r.answerMode || '').trim()))
  if (intentful) return intentful
  const withOffices = reports.find(r => Array.isArray(r.offices) && r.offices.length > 0)
  if (withOffices) return withOffices
  return reports[0]
}

const businessDrillReport = computed(() => (
  findBusinessDrillReport(latestDatasets.value)
))

const activeBusinessDrillReport = computed(() => (
  reportViewerVisible.value
    ? findBusinessDrillReport(reportViewerDatasets.value)
    : businessDrillReport.value
))

const sideBusinessSummaryText = computed(() => (
  businessDrillReport.value?.primaryAnswer?.text
  || businessDrillReport.value?.filterAnswer?.text
  || businessDrillReport.value?.summary
  || ''
))

const sideBusinessMetricCards = computed(() => (
  businessDrillReport.value
    ? (
        isCollectionAnswerMode(businessDrillReport.value)
          ? buildCollectionMetricCards(businessDrillReport.value)
          : businessDrillReport.value.isSingleFocus
          ? enrichSingleOrgMetricCards(
              businessDrillReport.value.kpis.slice(0, 4).map(item => ({
                label: item.label || item.key || '',
                value: item.value ?? item.displayValue ?? formatDisplayValue(item.value),
              })),
              businessDrillReport.value,
            )
          : decorateMetricCards(businessDrillReport.value.kpis, businessDrillReport.value.offices).slice(0, 8)
      )
    : []
))

const dialogBusinessDrillReport = computed(() => activeBusinessDrillReport.value)

const dialogCoreConclusion = computed(() => {
  const report = dialogBusinessDrillReport.value
  if (report?.answerMode === 'ranking') {
    const metricContext = getReportMetricContext(report)
    const leader = metricContext.best
    const follower = metricContext.ranked[1] || null
    if (leader) {
      const leaderText = findOfficeMetricValueByLabel(leader, metricContext.metricLabel) || '-'
      const followerText = follower ? (findOfficeMetricValueByLabel(follower, metricContext.metricLabel) || '-') : ''
      const diffText = metricContext.diff ? `，较${follower?.name}${metricContext.lowFirst ? '更低' : '更高'}${metricContext.diff}` : ''
      return `${leader.name}当前位于首位，${metricContext.metricLabel}${leaderText}${follower ? `${diffText}` : ''}；建议继续下钻定位差距来自哪些下级单元。`
    }
  }
  if (report?.primaryAnswer?.text) return report.primaryAnswer.text
  if (report?.filterAnswer?.text) return report.filterAnswer.text
  const offices = report?.offices || []
  if (offices.length >= 2) {
    const metricLabel = getSortMetricLabel(report, '达成率')
    const lowFirst = (getReportSortSpec(report).direction || '').toLowerCase() === 'asc'
    const ranked = sortOfficesByAnswerMetric(
      offices.filter(item => getMetricValueFromOffice(item, metricLabel) !== null),
      report,
    )
    const leader = ranked[0]
    const follower = ranked[1]
    if (leader && follower) {
      const leaderValue = getMetricValueFromOffice(leader, metricLabel)
      const followerValue = getMetricValueFromOffice(follower, metricLabel)
      const diff = leaderValue !== null && followerValue !== null
        ? Math.abs(leaderValue - followerValue)
        : null
      const diffText = diff === null
        ? ''
        : isRateMetricLabel(metricLabel)
        ? `${diff.toFixed(2).replace(/\.?0+$/, '')} 个百分点`
        : formatAmount(diff)
      const relationText = lowFirst ? '更低' : '更高'
      return `${leader.name}当前位于首位，较${follower.name}${metricLabel}${relationText}${diffText ? ` ${diffText}` : ''}；建议继续下钻定位差距来自哪些下级单元。`
    }
  }
  const reportText = String(reportViewerReport.value || latestReport.value || '').trim()
  const match = reportText.match(/(?:核心结论|结论)[:：]?\s*([^。\n]{12,120}。?)/)
  if (match?.[1]) return match[1].trim()
  return report?.summary || ''
})

const dialogReportStageTitle = computed(() => {
  const report = dialogBusinessDrillReport.value
  if (!report) return '下钻分析'
  if (report.answerMode === 'ranking') return isLeafOnlyReport(report) ? `${report.compareLevelLabel}排名列表` : `${report.compareLevelLabel}排名结果`
  if (report.answerMode === 'filter') return isLeafOnlyReport(report) ? `${report.compareLevelLabel}命中列表` : `${report.compareLevelLabel}命中结果`
  if (report.answerMode === 'drilldown') return `${report.compareLevelLabel}下钻分析`
  return isLeafOnlyReport(report) ? `${report.compareLevelLabel}结果列表` : `${report.compareLevelLabel}下钻分析`
})

const getOfficeMetricText = (office, type) => getOfficeKpiLabel(office, type) || '-'

const buildComparisonMetricTable = (offices = []) => {
  if (!offices.length) return ''
  const displayOffices = offices.length <= 4
    ? offices
    : [offices[0], offices[1], offices[offices.length - 2], offices[offices.length - 1]]
        .filter((item, index, list) => item && list.findIndex(row => row.name === item.name) === index)
  const header = ['指标', ...displayOffices.map(item => item.name)]
  const rows = [
    ['总任务金额', ...displayOffices.map(item => getOfficeMetricText(item, 'task'))],
    ['已完成金额', ...displayOffices.map(item => getOfficeMetricText(item, 'actual'))],
    ['整体达成率', ...displayOffices.map(item => getOfficeMetricText(item, 'rate'))],
    ['剩余缺口金额', ...displayOffices.map(item => getOfficeMetricText(item, 'remain'))],
  ]
  const table = [
    `| ${header.join(' | ')} |`,
    `| ${header.map(() => '---').join(' | ')} |`,
    ...rows.map(row => `| ${row.join(' | ')} |`),
  ].join('\n')
  const levelLabel = dialogBusinessDrillReport.value?.compareLevelLabel || businessDrillReport.value?.compareLevelLabel || '对象'
  const note = offices.length > 4 ? `\n\n本次对象较多，表内展示最高/次高/次低/最低摘要，完整 ${offices.length} 个${levelLabel}见下方对比分析表。` : ''
  return `${table}${note}`
}

const buildRankMetricTable = (items = [], title = '对象') => {
  if (!items.length) return ''
  return [
    `| ${title} | 任务 | 完成 | 达成率 | 缺口 |`,
    '| --- | ---: | ---: | ---: | ---: |',
    ...items.map(item => (
      `| ${item.name} | ${getOfficeMetricText(item, 'task')} | ${getOfficeMetricText(item, 'actual')} | ${getOfficeMetricText(item, 'rate')} | ${getOfficeMetricText(item, 'remain')} |`
    )),
  ].join('\n')
}

const getQuestionTargetLevel = (questionText = getQuestionText()) => {
  const hit = requestedLevelTokens.find(token => token && questionText.includes(token))
  return hit || ''
}

const getDirectAnswerFromRows = (report) => {
  const dataset = report?.dataset
  const rows = Array.isArray(dataset?.rows) ? dataset.rows : []
  if (!rows.length) return null
  const questionText = getQuestionText()
  const targetLevel = getQuestionTargetLevel(questionText)
  if (!targetLevel) return null
  const columns = dataset?.columns || Object.keys(rows[0] || {})
  const levelColumn = findColumn(columns, column => /层级|级别|level/i.test(column))
  const nameColumn = findColumn(columns, column => /节点名称|名称|战区|城市站|组织/i.test(column)) || columns[0]
  const rateColumn = findColumn(columns, column => isRateColumn(column)) || '达成率'
  const taskColumn = findColumn(columns, column => /总任务|任务金额|目标/i.test(column) && !/剩余|缺口|差额/i.test(column))
  const actualColumn = findColumn(columns, column => /年度开单|开单|完成|实际|销售/i.test(column))
  const remainColumn = findColumn(columns, column => /剩余|缺口|差额|remain/i.test(column))
  const candidates = rows
    .filter(row => {
      const levelText = String(row?.[levelColumn] || '')
      const nameText = String(row?.[nameColumn] || '')
      return levelText.includes(targetLevel) || nameText.includes(targetLevel)
    })
    .map(row => ({
      name: row?.[nameColumn] || row?.节点名称 || row?.名称 || '-',
      level: targetLevel,
      rate: toNumber(row?.[rateColumn]),
      rateLabel: rateColumn ? formatBusinessValueByColumn(row?.[rateColumn], rateColumn, dataset) : '-',
      task: toNumber(row?.[taskColumn]),
      taskLabel: taskColumn ? formatBusinessValueByColumn(row?.[taskColumn], taskColumn, dataset) : '-',
      actual: toNumber(row?.[actualColumn]),
      actualLabel: actualColumn ? formatBusinessValueByColumn(row?.[actualColumn], actualColumn, dataset) : '-',
      remain: toNumber(row?.[remainColumn]),
      remainLabel: remainColumn ? formatBusinessValueByColumn(row?.[remainColumn], remainColumn, dataset) : '-',
    }))
    .filter(item => item.name && item.rate !== null)
  if (!candidates.length) return null
  const lowFirst = isNegativeRankingQuestion(questionText)
  const winner = [...candidates].sort((left, right) => (
    lowFirst ? (left.rate || 0) - (right.rate || 0) : (right.rate || 0) - (left.rate || 0)
  ))[0]
  const metricText = /线下/.test(questionText) ? '线下业务' : '当前口径'
  const directionText = lowFirst ? '完成最弱' : '完成最好'
  const riskText = winner.rate !== null && winner.rate < 60
    ? `但达成率低于60%红线，仍需关注任务缺口和后续转化。`
    : '当前未触发60%红线。'
  return {
    ...winner,
    targetLevel,
    sentence: `${metricText}${directionText}的${targetLevel}是${winner.name}，达成率${winner.rateLabel}，总任务${winner.taskLabel}，实际开单${winner.actualLabel}，任务缺口${winner.remainLabel}；${riskText}`,
  }
}

const getRateDistribution = (items = []) => {
  const source = items.filter(item => item?.rate !== null && item?.rate !== undefined)
  const total = source.length || 0
  const buckets = [
    { label: '20%以下', count: 0, matcher: rate => rate < 20 },
    { label: '20%-40%', count: 0, matcher: rate => rate >= 20 && rate < 40 },
    { label: '40%以上', count: 0, matcher: rate => rate >= 40 },
  ]
  source.forEach((item) => {
    const bucket = buckets.find(part => part.matcher(Number(item.rate)))
    if (bucket) bucket.count += 1
  })
  return buckets.map(item => ({
    ...item,
    pct: total ? `${Math.round(item.count / total * 100)}%` : '0%',
  }))
}

const buildRateDistributionText = (items = []) => (
  getRateDistribution(items).map(item => `${item.label}：${item.count}个（${item.pct}）`).join('；')
)

const getTrendProgressText = (report) => {
  const kpis = Array.isArray(report?.kpis) ? report.kpis : []
  const trendItems = kpis
    .filter(item => /同比|环比|较上期|较同期|增长|变化/i.test(`${item?.label || ''}${item?.key || ''}`))
    .map(item => `${item.label || item.key}：${item.value ?? item.displayValue ?? '-'}`)
  if (trendItems.length) return trendItems.join('；')
  return '本次 SQL 结果未返回同比/环比字段，当前以达成率、缺口和分布判断进度；建议后续在数据集中补充同期/上期指标列。'
}

const getPressureDiagnosis = (item, detailLabel = '下级节点') => {
  if (!item) return ''
  const task = toNumber(getOfficeMetricText(item, 'task'))
  const actual = toNumber(getOfficeMetricText(item, 'actual'))
  const remain = toNumber(getOfficeMetricText(item, 'remain'))
  const rate = toNumber(getOfficeMetricText(item, 'rate'))
  const detailCount = Number(item.childCount || item.detailRows?.length || 0)
  const signals = []
  if (task !== null && remain !== null && task > 0 && remain / task >= 0.5) {
    signals.push('任务体量或缺口压力偏大')
  }
  if (rate !== null && rate < 20) {
    signals.push('整体转化进度偏慢')
  }
  if (actual !== null && task !== null && task > 0 && actual / task < 0.25) {
    signals.push('客户转化或项目落单不足')
  }
  if (detailCount > 0) {
    signals.push(`需继续下钻${detailCount}个${detailLabel}确认项目阶段`)
  }
  return signals.length
    ? `${item.name}可能由${signals.join('、')}共同造成，优先用下级明细验证。`
    : `${item.name}需要补充项目阶段、客户转化和资源投入字段后再做归因。`
}

const buildBusinessNarrativeSections = (report) => {
  const offices = report?.offices || []
  if (!report || !offices.length) return []
  if (report.answerMode === 'ranking') {
    const metricContext = getReportMetricContext(report)
    const configuredTopN = getConfiguredTopN(report)
    const ranked = metricContext.ranked.length ? metricContext.ranked : offices
    const topItems = ranked.slice(0, configuredTopN)
    const bottomItems = [...ranked].reverse().slice(0, configuredTopN)
    const riskCount = offices.filter(item => item.tone === 'danger').length
    const metricTable = buildComparisonMetricTable(ranked)
    return [
      {
        title: '一、核心结论',
        body: [
          report.primaryAnswer?.text || report.summary,
          metricContext.best && metricContext.worst && metricContext.best.name !== metricContext.worst.name
            ? `${metricContext.best.name}${metricContext.metricLabel}${findOfficeMetricValueByLabel(metricContext.best, metricContext.metricLabel) || '-'}位于榜首；${metricContext.worst.name}${metricContext.metricLabel}${findOfficeMetricValueByLabel(metricContext.worst, metricContext.metricLabel) || '-'}位于末位${metricContext.diff ? `，首尾相差${metricContext.diff}` : ''}。`
            : '',
          riskCount
            ? `风险信号：当前结果中有${riskCount}个对象处于低达成风险，排名领先不代表进度无风险。`
            : '风险信号：当前结果内暂无明显低达成风险对象。',
        ].filter(Boolean).join('\n'),
      },
      {
        title: '二、关键指标与排序结果',
        body: [
          metricTable,
          `当前按${metricContext.metricLabel}${metricContext.lowFirst ? '由低到高' : '由高到低'}排序；右侧列表、图表与摘要已统一使用这一指标。`,
        ].filter(Boolean).join('\n\n'),
      },
      {
        title: `三、${report.compareLevelLabel}Top${configuredTopN}/末${configuredTopN}`,
        body: [
          `Top${configuredTopN}：`,
          buildRankMetricTable(topItems, report.compareLevelLabel || '对象'),
          '',
          `末${configuredTopN}：`,
          buildRankMetricTable(bottomItems, report.compareLevelLabel || '对象'),
        ].filter(Boolean).join('\n\n'),
      },
      {
        title: '四、后续动作',
        body: [
          metricContext.best ? `榜首复盘：优先复盘${metricContext.best.name}在${metricContext.metricLabel}上的领先做法，并核对其达成率与缺口是否同步健康。` : '',
          metricContext.worst ? `末位下钻：围绕${metricContext.worst.name}继续下钻${report.detailLevelLabel}，确认是任务体量、项目阶段还是客户转化拖累。` : '',
          '统一口径：排名按问题中的指标排序，风险继续看达成率与缺口，避免把“排位”和“健康度”混为一谈。',
        ].filter(Boolean).join('\n'),
      },
    ]
  }
  const ranked = [...offices].filter(item => item.rate !== null).sort((a, b) => (b.rate || 0) - (a.rate || 0))
  const best = ranked[0] || offices[0]
  const worst = ranked[ranked.length - 1] || offices[offices.length - 1]
  const configuredTopN = getConfiguredTopN(report)
  const topItems = ranked.slice(0, configuredTopN)
  const bottomItems = [...ranked].reverse().slice(0, configuredTopN)
  const directAnswer = getDirectAnswerFromRows(report)
  const diff = best?.rate !== null && worst?.rate !== null
    ? Math.abs((best.rate || 0) - (worst.rate || 0)).toFixed(2).replace(/\.?0+$/, '')
    : ''
  const visibleNames = offices.length <= 4
    ? offices.map(item => item.name).join('、')
    : `${offices.length} 个${report.compareLevelLabel}`
  const riskOffices = offices.filter(item => item.tone === 'danger')
  const riskText = riskOffices.length
    ? `${riskOffices.slice(0, 3).map(item => item.name).join('、')}处于低达成风险${riskOffices.length > 3 ? `等 ${riskOffices.length} 个对象` : ''}`
    : '当前同层级对象暂无低达成风险'
  const distributionText = buildRateDistributionText(offices)
  const trendText = getTrendProgressText(report)
  const topBottomTable = [
    `Top${configuredTopN}：`,
    buildRankMetricTable(topItems, report.compareLevelLabel || '对象'),
    '',
    `末${configuredTopN}：`,
    buildRankMetricTable(bottomItems, report.compareLevelLabel || '对象'),
  ].filter(Boolean).join('\n\n')

  if (report.isSingleFocus) {
    const focusName = report.focusName || '当前组织'
    const counts = getSingleOrgCounts(report)
    const rankContext = getSingleOrgRankContext(report)
    const overallRate = getReportKpiText(report, 'rate')
    const tableRows = offices.length <= 6
      ? offices
      : [
          ...ranked.slice(0, configuredTopN),
          ...ranked.slice(-Math.min(2, configuredTopN)),
        ].filter((item, index, list) => item && list.findIndex(row => row.name === item.name) === index)
    const comparisonRows = tableRows.map((office) => {
      const diffValue = office.rate !== null && toNumber(overallRate) !== null ? (office.rate - toNumber(overallRate)) : null
      const diffText = diffValue === null
        ? '-'
        : `${diffValue >= 0 ? '高于大盘' : '低于大盘'} ${Math.abs(diffValue).toFixed(2).replace(/\.?0+$/, '')}pct`
      return `| ${office.name} | ${office.rateLabel} | ${diffText} | ${office.tag || '-'} |`
    })
    const comparisonTable = [
      `数据为${focusName}下${counts.directCount}个${counts.directLabel}摘要，完整明细见下方附表。`,
      '',
      '| 对象 | 达成率 | 与大盘对比 | 标签 |',
      '| --- | --- | --- | --- |',
      ...comparisonRows,
    ].join('\n')
    return [
      {
        title: `一、${focusName}核心结论`,
        body: [
          directAnswer
            ? `1. ${directAnswer.sentence}`
            : `1. 当前进度：${getSingleOrgConclusion(report)}`,
          rankContext.diff
            ? `2. 头尾差异：${rankContext.best.name}达成率${rankContext.best.rateLabel}领跑，${rankContext.worst.name}达成率${rankContext.worst.rateLabel}承压，首尾差距${rankContext.diff}个百分点。`
            : report.summary,
          `3. 风险信号：${riskText}；${distributionText}。`,
        ].filter(Boolean).slice(0, 3).join('\n'),
      },
      {
        title: `二、${focusName}关键指标与二级拆解`,
        body: [
          `事业群/主体大盘：总任务金额 ${getReportKpiText(report, 'task')}，年度开单金额 ${getReportKpiText(report, 'actual')}，整体达成率 ${overallRate}，剩余任务金额 ${getReportKpiText(report, 'remain')}。`,
          `同比/环比进度：${trendText}`,
          `达成率分布：${distributionText}`,
          comparisonTable,
        ].filter(Boolean).join('\n\n'),
      },
      {
        title: `三、${counts.directLabel}Top${configuredTopN}/末${configuredTopN}对比`,
        body: topBottomTable,
      },
      {
        title: '四、结构看板与问题溯源',
        body: [
          `标杆分析：${rankContext.best ? `${rankContext.best.name}是当前标杆，任务 ${getOfficeMetricText(rankContext.best, 'task')}，完成 ${getOfficeMetricText(rankContext.best, 'actual')}，达成率 ${rankContext.best.rateLabel}；建议复盘其目标拆解、客户推进和项目转化节奏。` : '当前未识别稳定标杆。'}`,
          `压力节点：${rankContext.worst ? getPressureDiagnosis(rankContext.worst, counts.detailLabel) : '当前未识别明显压力节点。'}`,
          `分层归因：事业群层面关注头部贡献与尾部拖累是否过度分化；${counts.directLabel}层面重点比较标杆和末位在任务体量、项目阶段、客户转化和资源投入上的差异。`,
        ].join('\n\n'),
      },
      {
        title: '五、动作落地',
        body: [
          rankContext.best ? `标杆经验推广：由${rankContext.best.name}输出可复制动作清单，两周内同步给达成率低于20%的${counts.directLabel}。` : '',
          rankContext.worst ? `压力节点帮扶：围绕${rankContext.worst.name}建立下钻清单，责任方为业务负责人+经营分析；输出项目阶段、客户转化、缺口金额三张明细表。` : '',
          `整体优化：按${counts.directLabel}建立红黄绿看板，低于20%周度复盘，20%-40%专项推进，高于40%沉淀打法并横向复制。`,
        ].filter(Boolean).join('\n'),
      },
    ]
  }
  return [
    {
      title: '一、核心结论',
      body: [
        directAnswer
          ? `1. ${directAnswer.sentence}`
          : diff
          ? `1. 当前对比覆盖${visibleNames}，${best.name}达成率${best.rateLabel}领先，${worst.name}达成率${worst.rateLabel}承压，首尾差${diff}个百分点。`
          : `1. ${report.summary}`,
        `2. 头部/尾部差异：Top${configuredTopN}为${topItems.map(item => `${item.name}(${item.rateLabel})`).join('、') || '暂无'}；末${configuredTopN}为${bottomItems.map(item => `${item.name}(${item.rateLabel})`).join('、') || '暂无'}。`,
        `3. 核心风险信号：${riskText}；${distributionText}。`,
      ].join('\n'),
    },
    {
      title: '二、关键指标与分层拆解',
      body: [
        buildComparisonMetricTable(offices),
        `同比/环比进度：${trendText}`,
        `分布看板：${distributionText}`,
      ].join('\n\n'),
    },
    {
      title: `三、${report.compareLevelLabel}Top${configuredTopN}/末${configuredTopN}对比`,
      body: topBottomTable,
    },
    {
      title: '四、结构看板与问题溯源',
      body: [
        `标杆分析：${best.name}任务 ${getOfficeMetricText(best, 'task')}，完成 ${getOfficeMetricText(best, 'actual')}，达成率 ${best.rateLabel}；优先复盘其目标拆解、客户推进和项目转化动作。`,
        `压力节点：${getPressureDiagnosis(worst, report.detailLevelLabel)}`,
        `分层归因：事业群层面看头部贡献、尾部拖累和任务分配合理性；${report.compareLevelLabel}层面看任务体量、项目阶段、客户转化和资源投入差异。`,
      ].join('\n\n'),
    },
    {
      title: '五、动作落地',
      body: [
        `标杆经验推广：由${directAnswer?.name || best.name}沉淀关键动作，覆盖${bottomItems.map(item => item.name).join('、') || '低达成节点'}，两周内完成打法复盘和任务拆解。`,
        `压力节点帮扶：围绕${worst.name}下钻${report.detailLevelLabel}，责任方为业务负责人+经营分析；输出项目阶段、客户转化、缺口金额三类问题清单。`,
        `整体优化：按达成率分布配置资源，低于20%节点进入周度专项，20%-40%节点做过程纠偏，高于40%节点提炼可复制打法。`,
      ].join('\n'),
    },
  ]
}

const reportOverviewTitle = computed(() => {
  const drillReport = activeBusinessDrillReport.value
  return drillReport?.isSingleFocus
    ? `${drillReport.focusName || '当前组织'}业绩核心结论`
    : '分析摘要'
})

const reportSummaryBullets = computed(() => {
  const bullets = []
  const sourceDatasets = reportSourceDatasets.value
  const primary = sourceDatasets[0]
  const drillReport = activeBusinessDrillReport.value
  const names = sourceDatasets.map(item => item.dataset_name).filter(Boolean)
  if (drillReport?.isSingleFocus) {
    const counts = getSingleOrgCounts(drillReport)
    const rankContext = getSingleOrgRankContext(drillReport)
    bullets.push(getSingleOrgConclusion(drillReport))
    bullets.push(`覆盖范围：${counts.directCount}个${counts.directLabel}${counts.detailCount ? `，${counts.detailCount}个${counts.detailLabel}` : ''}。`)
    if (rankContext.best && rankContext.worst && rankContext.diff) {
      bullets.push(`${rankContext.best.name}达成率最高，为${rankContext.best.rateLabel}；${rankContext.worst.name}压力最大，为${rankContext.worst.rateLabel}，首尾差距${rankContext.diff}个百分点。`)
    }
    if (names.length) bullets.push(`命中数据集：${names.join('、')}`)
    return bullets.filter(Boolean)
  }
  if (drillReport?.offices?.length) {
    const metricContext = getReportMetricContext(drillReport)
    const best = metricContext.best || drillReport.offices[0]
    const worst = metricContext.worst || drillReport.offices[drillReport.offices.length - 1]
    const riskCount = drillReport.offices.filter(item => item.tone === 'danger').length
    bullets.push(`当前覆盖 ${drillReport.offices.length} 个${drillReport.compareLevelLabel}，先横向比较再下钻${drillReport.detailLevelLabel}。`)
    if (best && worst) {
      bullets.push(metricContext.diff
        ? `${best.name}${metricContext.metricLabel}${findOfficeMetricValueByLabel(best, metricContext.metricLabel) || '-'}领先，${worst.name}${metricContext.metricLabel}${findOfficeMetricValueByLabel(worst, metricContext.metricLabel) || '-'}位于末位，首尾差${metricContext.diff}。`
        : `${best.name}表现靠前，${worst.name}需要优先下钻复核。`)
    }
    bullets.push(riskCount
      ? `风险信号：${riskCount}个${drillReport.compareLevelLabel}处于低达成风险，需按缺口和项目阶段拆解责任。`
      : `风险信号：暂无明显低达成${drillReport.compareLevelLabel}，继续保持周度过程跟踪。`)
    return bullets.filter(Boolean).slice(0, 3)
  }
  if (session.state.question) bullets.push(`原始问题：${session.state.question}`)
  bullets.push(`报告模板：${reportSceneTemplateLabel.value}`)
  if (drillReport) {
    const nextLevelText = drillReport.offices?.some(item => item.drillGroups?.length)
      ? `，再从${drillReport.detailLevelLabel}继续下钻到业务员`
      : ''
    bullets.push(`分析口径：先横向比较 ${drillReport.offices.length} 个${drillReport.compareLevelLabel}，再纵向展开${drillReport.detailLevelLabel}${nextLevelText}。`)
  }
  if (names.length) bullets.push(`命中数据集：${names.join('、')}`)
  if (sourceDatasets.length) {
    const totalRows = sourceDatasets.reduce((sum, item) => sum + Number(item?.row_count || item?.rows?.length || 0), 0)
    bullets.push(`数据结果：共返回 ${sourceDatasets.length} 份结果，累计 ${totalRows} 行数据。`)
  }
  const reviewSummary = primary?.agent3_review?.review_summary
  if (reviewSummary) bullets.push(`SQL 复核结论：${reviewSummary}`)
  const sample = primary?.rows?.[0]
  const columns = primary?.columns || []
  if (!drillReport && sample && columns.length) {
    const snippet = columns.slice(0, 3).map(column => `${column}=${sample[column]}`).join('；')
    if (snippet) bullets.push(`样例结果：${snippet}`)
  }
  if (!bullets.length && (reportViewerReport.value || latestReport.value)) {
    bullets.push('本轮报告已生成，可继续查看下方图表分析与完整解读。')
  }
  return bullets
})

const reportNarrativeSections = computed(() => {
  const raw = String((reportViewerVisible.value ? reportViewerReport.value : latestReport.value) || '').trim()
  if (!raw) return []

  const sections = splitReportSections(raw)

  if (!sections.length) {
    return [{
      title: reportViewerTitle.value || sideReportHeading.value,
      body: normalizeReportMarkdown(raw),
    }]
  }

  return sections
})

const businessNarrativeSections = computed(() => {
  const generated = buildBusinessNarrativeSections(dialogBusinessDrillReport.value || businessDrillReport.value)
  if (generated.length) return generated
  return reportNarrativeSections.value
    .filter(section => !/^业绩分析报告$/.test(section.title))
    .slice(0, 4)
})

// 方法
const renderMd = (text) => marked.parse(text || '')
const renderReportMd = (text) => marked.parse(normalizeReportMarkdown(text))

const normalizeReportMarkdown = (text) => (
  String(text || '')
    .replace(/\r\n/g, '\n')
    .replace(/^#\s+/gm, '## ')
    .replace(/\n---\n/g, '\n\n')
    .replace(/[ \t]+•[ \t]*/g, '\n- ')
    .replace(/^•[ \t]*/gm, '- ')
    .replace(/([。！？；;])\s*(?=##|###)/g, '$1\n\n')
    .replace(/\n{3,}/g, '\n\n')
    .trim()
)

const splitReportSections = (text) => {
  const normalized = normalizeReportMarkdown(text).replace(/^##\s*业绩分析报告\s*/i, '').trim()
  if (!normalized) return []

  const headingPattern = /^#{2,3}\s+(.+)$/gm
  const matches = Array.from(normalized.matchAll(headingPattern))
  if (!matches.length) {
    return [{ title: '核心结论', body: normalized }]
  }

  const sections = []
  const leading = normalized.slice(0, matches[0].index).trim()
  if (leading) sections.push({ title: '核心结论', body: leading })

  matches.forEach((match, index) => {
    const title = String(match[1] || '').trim()
    const start = Number(match.index || 0) + match[0].length
    const end = index + 1 < matches.length ? Number(matches[index + 1].index || normalized.length) : normalized.length
    const body = normalized.slice(start, end).trim()
    if (!title || /^业绩分析报告$/.test(title)) return
    if (body) sections.push({ title, body })
  })

  return sections
}

const togglePanel = () => {
  showPanel.value = !showPanel.value
  nextTick(resizeRenderedCharts)
}
const toggleThinking = (id) => { thinkingOpen[id] = !thinkingOpen[id] }
const toggleLog = (i) => { logOpen[i] = !logOpen[i] }
const setResultChainRef = (id, el) => {
  if (!id) return
  if (el) resultChainRefs.set(id, el)
  else resultChainRefs.delete(id)
}
const openDetailPanel = (msg = null) => {
  if (msg?.data && !msg.data.error && !msg.data.requires_confirmation) {
    detailReportResult.value = JSON.parse(JSON.stringify(msg.data))
  } else {
    detailReportResult.value = null
  }
  showPanel.value = true
  nextTick(resizeRenderedCharts)
  scrollPanelToReportTop()
}

const scrollPanelToReportTop = () => nextTick(() => {
  const panel = panelRef.value
  const report = sideReportRef.value
  const reportHead = sideReportHeadRef.value
  if (!panel) return
  if (!report) {
    panel.scrollTo({ top: 0, behavior: 'auto' })
    return
  }
  const target = reportHead || report
  const panelRect = panel.getBoundingClientRect()
  const targetRect = target.getBoundingClientRect()
  const top = panel.scrollTop + targetRect.top - panelRect.top - 12
  panel.scrollTo({ top: Math.max(0, top), behavior: 'auto' })
})

const clearExecutionPanelState = () => {
  detailReportResult.value = null
  Object.keys(logOpen).forEach(k => delete logOpen[k])
  // S1 信号重置：开始新一轮执行即脱离"历史快照恢复"状态
  if (session?.state) session.state.isHistoricalSnapshot = false
  timelineVersion.value += 1
  nextTick(() => {
    if (panelRef.value) panelRef.value.scrollTop = 0
  })
}

const clearChatUiState = () => {
  Object.keys(thinkingOpen).forEach(k => delete thinkingOpen[k])
  Object.keys(confirmationDrafts).forEach(k => delete confirmationDrafts[k])
  Object.keys(clarifyDrafts).forEach(k => delete clarifyDrafts[k])
  Object.keys(confirmationSubmitting).forEach(k => delete confirmationSubmitting[k])
  Object.keys(confirmExpanded).forEach(k => delete confirmExpanded[k])
  Object.keys(officeDrillOpen).forEach(k => delete officeDrillOpen[k])
  reportViewerVisible.value = false
  chartViewerVisible.value = false
  elapsed.value = 0
  stopTimer()
  clearExecutionPanelState()
}

const isUiEventLike = (value) => Boolean(
  value
  && typeof value === 'object'
  && (
    typeof value.preventDefault === 'function'
    || typeof value.stopPropagation === 'function'
    || value.type
  )
)

const openReportViewer = (report = latestReport.value, title = sideReportHeading.value, datasetsForReport = latestDatasets.value) => {
  if (isUiEventLike(report)) {
    report = latestReport.value
    title = sideReportHeading.value
    datasetsForReport = latestDatasets.value
  }
  if (!report && !datasetsForReport?.length) {
    ElMessage.warning('当前还没有可查看的完整报告')
    return
  }
  reportViewerResearch.value = null
  reportViewerReport.value = report
  reportViewerTitle.value = normalizeReportTitle(title)
  reportViewerDatasets.value = Array.isArray(datasetsForReport) ? datasetsForReport : []
  reportDialogFullscreen.value = false
  reportViewerVisible.value = true
}
const openMessageReport = result => {
  if(!canUseFeature('ask_report_details') || !result)return
  const datasets=result.research?(result.research.evidence || []).flatMap(e=>e.dataset_results || []):result.dataset_results || []
  const report=String(result.report || result.analysis || datasets.map(ds=>ds.analysis || '').join('\n\n'))
  openReportViewer(report,result.question || '数据分析报告',datasets)
  reportViewerResearch.value = result.research ? result : null
}
const openFullScreenReport = () => {
  openReportViewer(latestReport.value, sideReportHeading.value, latestDatasets.value)
  reportDialogFullscreen.value = true
}
const openChartViewer = (spec, title = '图表预览') => {
  if (!spec) return
  chartViewerSpec.value = spec
  chartViewerTitle.value = title
  chartViewerMode.value = 'chart'
  chartViewerVisible.value = true
}

const isOfficeExpanded = (id) => officeDrillOpen[String(id)] === true
const toggleOfficeDrill = (id) => {
  const key = String(id)
  officeDrillOpen[key] = !isOfficeExpanded(key)
  nextTick(resizeRenderedCharts)
}

const chartViewerTableRows = computed(() => (
  Array.isArray(chartViewerSpec.value?.rows) ? chartViewerSpec.value.rows : []
))

const chartViewerTableColumns = computed(() => (
  Array.isArray(chartViewerSpec.value?.columns) ? chartViewerSpec.value.columns : []
))

const chartViewerHasTable = computed(() => (
  chartViewerTableRows.value.length > 0 && chartViewerTableColumns.value.length > 0
))

const getPlanSteps = (msg) => {
  const route = msg.data?.route
  if (!route) return []
  const text = typeof route === 'string' ? route : (route.route_desc || JSON.stringify(route))
  return text.split('\n').filter(l => l.trim().match(/^步骤\d|^\d+[\.、]/)).map(s => s.replace(/^(步骤\d+[:：]?|\d+[\.、\s]*)/i, '').trim()).filter(Boolean)
}

const getThinkingSteps = (msg) => {
  const mapStatus = (status) => ({
    success: 'completed',
    completed: 'completed',
    running: 'running',
    pending: 'pending',
    warning: 'warning',
    error: 'error',
  }[status] || 'completed')

  const toStep = (step) => ({
    text: step?.text || step?.title || step?.detail || '执行步骤',
    detail: step?.detail && step?.detail !== step?.title ? step.detail : '',
    status: mapStatus(step?.status),
  })

  if (msg.loading) return session.state.logs.map(toStep)
  if (!msg.data) return []

  const isCurrentResult =
    msg.data?.question &&
    session.state.question &&
    msg.data.question === session.state.question &&
    session.state.logs.length > 0

  if (isCurrentResult) {
    return session.state.logs.map((step) => ({
      text: step?.title || step?.summary || '执行步骤',
      detail: step?.summary || step?.detailLines?.[0] || '',
      status: mapStatus(step?.status),
      statusText: step?.status === 'warning' ? '待确认' : undefined,
    }))
  }

  const steps = []
  if (msg.data.route) {
    steps.push({
      text: '已完成问题理解与执行规划',
      detail: '系统已经确定查询路径与分析重点。',
      status: 'completed',
    })
  }
  ;(msg.data.dataset_results || []).forEach((r) => {
    steps.push({
      text: `已完成数据检索 ${r.dataset_name || '目标数据集'}`,
      detail: r.rows?.length ? `已返回 ${r.rows.length} 行结果数据。` : '已拿到可分析的数据结果。',
      status: 'completed',
    })
  })
  if (msg.data.dataset_results?.[0]?.analysis) {
    steps.push({
      text: '已生成经营分析报告',
      detail: '报告摘要已经同步写入左侧回复区与右侧结果区。',
      status: 'completed',
    })
  }
  if (msg.data.requires_confirmation) {
    steps.push({
      text: '等待确认统计口径',
      detail: msg.data.confirmation_question || '需要先确认业务口径再继续执行。',
      status: 'warning',
    })
  }
  if (msg.data.error) {
    steps.push({
      text: '执行过程中发生异常',
      detail: msg.data.error,
      status: 'error',
    })
  }
  return steps
}

const isCurrentSessionMessage = (msg) => {
  return Boolean(
    !session.state.isHistoricalSnapshot &&
    msg?.data?.question &&
    session.state.question &&
    msg.data.question === session.state.question &&
    session.state.logs.length > 0
  )
}

const latestAiMessage = computed(() => (
  [...messages].reverse().find(item => item?.role === 'ai') || null
))

const isLatestAiMessage = (msg) => latestAiMessage.value?.id === msg?.id

const currentSessionAiMessage = computed(() => (
  [...messages].reverse().find(item => item?.role === 'ai' && isCurrentSessionMessage(item)) || latestAiMessage.value || null
))

const activeRequestAiMessage = computed(() => (
  messages.find(item => item?.id === activeRequestAiMessageId.value) || null
))

const syncPendingConfirmationMessage = () => {
  const result = session.state.result
  if (session.state.status !== 'waiting_confirmation' || !result?.requires_confirmation) return

  const msg = activeRequestAiMessage.value || currentSessionAiMessage.value
  if (!msg || msg.role !== 'ai') return
  if (msg.data?.requires_confirmation) return

  msg.loading = false
  msg.data = JSON.parse(JSON.stringify(result))
  thinkingOpen[msg.id] = false
  if (!(msg.id in confirmationDrafts)) confirmationDrafts[msg.id] = ''
  stopTimer()
  scheduleChatScroll(36, 'smooth')
}

const syncCompletedResultMessage = () => {
  const result = session.state.result
  if (session.state.status !== 'completed' || !result || result?.requires_confirmation || result?.error) return

  const msg = activeRequestAiMessage.value || currentSessionAiMessage.value
  if (!msg || msg.role !== 'ai') return

  const sameQuestion = !result.question || !session.state.question || result.question === session.state.question
  if (!sameQuestion) return

  const needsSync = msg.loading || !msg.data || !Array.isArray(msg.data?.dataset_results)
  if (!needsSync) return

  msg.loading = false
  msg.data = JSON.parse(JSON.stringify(result))
  thinkingOpen[msg.id] = false
  stopTimer()
  scheduleChatReportTop(48, 'smooth')
}

const shouldShowLiveFeed = (msg) => {
  if (msg?.loading) return true
  if (msg?.data?.early_clarify) return false
  if (!session.state.logs.length) return false
  if (msg?.data?.requires_confirmation) return false
  if (msg?.data?.aborted) return isLatestAiMessage(msg) || isCurrentSessionMessage(msg)
  return Boolean(
    isCurrentSessionMessage(msg) ||
    (isLatestAiMessage(msg) && ['completed', 'canceled', 'error'].includes(session.state.status))
  )
}

const getLiveFeedMode = (msg) => {
  if (msg?.data?.aborted || session.state.status === 'canceled') return 'canceled'
  if (!msg?.data?.aborted && session.state.status === 'completed' && (isCurrentSessionMessage(msg) || isLatestAiMessage(msg))) {
    return 'completed'
  }
  if (msg?.loading) return 'live'
  return 'completed'
}

const shouldShowThinkingCard = (msg) => {
  if (msg?.loading) return !session.state.logs.length
  return false
}

const shouldShowConfirmationCard = (msg) => Boolean(
  !isViewingReadonly.value && msg?.data?.confirmation_type !== 'research_plan' && msg?.data?.requires_confirmation && !confirmationSubmitting[msg.id] && !msg?.loading
)

const shouldShowConfirmationSubmitted = (msg) => Boolean(
  !isViewingReadonly.value && msg?.data?.confirmation_type !== 'research_plan' && msg?.data?.requires_confirmation && confirmationSubmitting[msg.id]
)

const isMessageExecutionComplete = (msg) => {
  if (!msg?.data || msg?.loading || msg?.data?.error || msg?.data?.requires_confirmation) return false
  if (isViewingReadonly.value) return true
  if (!isCurrentSessionMessage(msg)) return true
  return session.state.status === 'completed'
}

const shouldShowResultHandoff = (msg) => {
  return Boolean(
    isMessageExecutionComplete(msg) &&
    isCurrentSessionMessage(msg) &&
    (getReport(msg) || getPrimaryDataset(msg))
  )
}

const shouldShowResultChain = (msg) => Boolean(
  !msg?.data?.early_clarify &&
  isMessageExecutionComplete(msg) &&
  (getReport(msg) || getPrimaryDataset(msg) || (msg.data && !msg.data.error))
)

const getMessageDerived = (msg) => {
  if (!msg || typeof msg !== 'object') return null
  const data = msg.data || null
  const datasetResults = data?.dataset_results || null
  const questionKey = getQuestionText()
  const cached = messageDerivedCache.get(msg)
  if (cached?.data === data && cached?.datasetResults === datasetResults && cached?.questionKey === questionKey) {
    return cached
  }
  const entry = {
    data,
    datasetResults,
    questionKey,
    datasets: null,
    report: undefined,
    primaryDataset: undefined,
    visualPreviews: undefined,
  }
  messageDerivedCache.set(msg, entry)
  return entry
}

const getDatasets = (msg) => {
  const cache = getMessageDerived(msg)
  if (cache?.datasets) return cache.datasets
  const raw = Array.isArray(msg?.data?.dataset_results) ? msg.data.dataset_results : []
  if (!raw.length) {
    if (cache) cache.datasets = []
    return []
  }
  const subjectByDatasetId = new Map()
  const orgRoute = msg?.data?.diagnostics?.advanced?.route_guard?.organization_route || {}
  ;(orgRoute.organization_mentions || []).forEach((item) => {
    const subjectName = String(item?.node_name || '').trim()
    if (!subjectName) return
    ;(item?.dataset_ids || []).forEach((id) => {
      const numericId = Number(id)
      if (Number.isFinite(numericId)) {
        subjectByDatasetId.set(numericId, subjectName)
      }
    })
  })
  const enriched = raw.map((dataset) => {
    const subjectName = subjectByDatasetId.get(Number(dataset?.dataset_id))
    return subjectName
      ? { ...dataset, comparison_subject_name: subjectName, comparison_subject_level: inferSubjectLevel(subjectName) }
      : dataset
  })
  const visible = enriched.filter(dataset => isDatasetVisible(dataset?.dataset_id))
  const datasetsForMessage = visible.length ? visible : enriched
  if (cache) cache.datasets = datasetsForMessage
  return datasetsForMessage
}
const getReport = (msg) => {
  const cache = getMessageDerived(msg)
  if (cache && cache.report !== undefined) return cache.report
  const report = mergeDatasetReports(getDatasets(msg))
  if (cache) cache.report = report
  return report
}
const getPrimaryDataset = (msg) => {
  const cache = getMessageDerived(msg)
  if (cache && cache.primaryDataset !== undefined) return cache.primaryDataset
  const dataset = buildAggregateDataset(getDatasets(msg))
  if (cache) cache.primaryDataset = dataset
  return dataset
}
const getResultTitle = (msg) => {
  if (msg.data?.display_title) {
    return msg.data.display_title.length > 20 ? `${msg.data.display_title.slice(0, 20)}...` : msg.data.display_title
  }
  const raw = msg.data?.question || session.state.question || '本月公司经营表现分析'
  const normalized = normalizeReportTitle(raw)
  return normalized.length > 20 ? `${normalized.slice(0, 20)}...` : normalized
}

const formatElapsedLabel = (seconds) => {
  const totalSeconds = Math.max(0, Math.round(Number(seconds) || 0))
  const minutes = Math.floor(totalSeconds / 60)
  const remain = totalSeconds % 60
  if (minutes <= 0) return `${remain}s`
  return `${minutes}m ${remain}s`
}

const isAbortLikeInteractionError = (error) => {
  const text = `${error?.name || ''} ${error?.code || ''} ${error?.message || ''}`
  return Boolean(
    error?.isUserAbort ||
    /AbortError|CanceledError|ERR_CANCELED|aborted|cancelled|canceled|BodyStreamBuffer/i.test(text)
  )
}

const getMessageElapsedLabel = (msg) => {
  if (msg?.loading && isCurrentSessionMessage(msg)) {
    return formatElapsedLabel(elapsed.value)
  }
  return ''
}

const getAskFlowMeta = (msg) => {
  if (!showAskFlowBadge.value) return null
  const meta = msg?.data?.ask_flow || msg?.data?.diagnostics?.ask_flow || null
  return meta && typeof meta === 'object' ? meta : null
}

const getAskFlowLabel = (msg) => {
  const flow = String(getAskFlowMeta(msg)?.flow || '').toLowerCase()
  if (flow === 'advanced') return '进阶流程'
  if (flow === 'basic') return '基础流程'
  return ''
}

const getAskFlowClass = (msg) => {
  const flow = String(getAskFlowMeta(msg)?.flow || '').toLowerCase()
  return flow === 'advanced' ? 'is-advanced' : 'is-basic'
}

const getAskFlowHint = (msg) => {
  const reason = String(getAskFlowMeta(msg)?.reason || '')
  const map = {
    basic_selected: '由基础流程执行',
    advanced_selected: '由进阶流程执行',
    advanced_disabled: '进阶未启用，已回落基础流程',
    advanced_role_denied: '当前角色未进入进阶灰度',
    advanced_error_fallback: '进阶异常，已回退基础流程',
  }
  return map[reason] || ''
}

const getVisualPreviews = (msg) => {
  const cache = getMessageDerived(msg)
  if (cache && cache.visualPreviews !== undefined) return cache.visualPreviews
  const sourceDatasets = getDatasets(msg)
  const previews = hasBusinessDrillDataset(sourceDatasets) ? [] : sourceDatasets
    .slice(0, 2)
    .map((dataset, index) => ({
      key: `${dataset.dataset_id || index}-${dataset.dataset_name || 'dataset'}`,
      dataset,
      chartSpec: getDatasetChartSpecs(dataset)[0] || null,
    }))
    .filter(item => item.chartSpec && (item.chartSpec.chartType === 'metric' || hasChartRows(item.chartSpec)))
  if (cache) cache.visualPreviews = previews
  return previews
}

const focusComposer = (selectAll = false) => nextTick(() => {
  const textarea = document.querySelector('.cmp-textarea')
  if (!(textarea instanceof HTMLTextAreaElement)) return
  textarea.focus()
  const end = textarea.value.length
  textarea.setSelectionRange(selectAll ? 0 : end, end)
})

const writeClipboard = async (text) => {
  if (navigator.clipboard?.writeText) {
    await navigator.clipboard.writeText(text)
    return
  }
  const textarea = document.createElement('textarea')
  textarea.value = text
  textarea.setAttribute('readonly', 'readonly')
  textarea.style.position = 'fixed'
  textarea.style.left = '-9999px'
  document.body.appendChild(textarea)
  textarea.select()
  document.execCommand('copy')
  document.body.removeChild(textarea)
}

const copyQuestion = async (msg) => {
  if (!canUseFeature('ask_question_copy')) return
  const text = String(msg?.content || '').trim()
  if (!text) return
  try {
    await writeClipboard(text)
    ElMessage.success('问题已复制')
  } catch {
    ElMessage.warning('复制失败，请手动复制')
  }
}

const editQuestion = (msg) => {
  if (!canUseFeature('ask_question_edit')) return
  const text = String(msg?.content || '').trim()
  if (!text) return
  if (isRunning.value) {
    ElMessage.warning('当前正在执行，停止后再修改问题')
    return
  }
  query.value = text
  focusComposer(true)
  ElMessage.success('已放入输入框，修改后按 Enter 发送')
}

const clearMessageRuntimeState = (items = []) => {
  items.forEach((item) => {
    if (!item?.id) return
    delete thinkingOpen[item.id]
    delete confirmationDrafts[item.id]
    delete clarifyDrafts[item.id]
    delete confirmationSubmitting[item.id]
    delete confirmExpanded[item.id]
  })
}

const rerunQuestion = async (msg) => {
  if (!canUseFeature('ask_question_rerun')) return
  const text = String(msg?.content || '').trim()
  if (!text || isRunning.value) return

  // 重问创建新的任务条目
  const createShellId = () => {
    if (typeof window !== 'undefined' && window.crypto?.randomUUID) {
      return `history-report-${window.crypto.randomUUID()}`
    }
    return `history-report-${Date.now()}-${Math.random().toString(16).slice(2)}`
  }
  const shellId = createShellId()

  const runningShell = {
    id: shellId,
    title: String(text).slice(0, 24),
    question: text,
    datasetId: datasetId.value || null,
    datasetName: datasets.value.find(d => d.id === datasetId.value)?.name || '',
    updatedAt: new Date().toISOString(),
    status: 'running',
    reportSnapshot: null,
  }
  upsertHistory(runningShell)
  setActiveHistory(shellId)
  setRunningSessionId(shellId)
  switchViewToDefault()

  session.resetSession()
  clearChatUiState()
  messages.splice(0, messages.length)
  const uid = ++msgCounter
  messages.push({ id: uid, role: 'user', content: text })
  const aid = ++msgCounter
  const aiMsg = { id: aid, role: 'ai', loading: true, data: null }
  messages.push(aiMsg)
  activeRequestAiMessageId.value = aid
  thinkingOpen[aid] = true

  query.value = ''
  clearExecutionPanelState()
  scheduleChatScroll(24, 'smooth')
  startTimer()

  try {
    const datasetInput = getDatasetInputForQuestion(text)
    const res = await session.startAsk(text, datasetInput, getModelInputForQuestion(), {})
    clearPendingQuickDataset()
    if (res) {
      aiMsg.loading = false
      aiMsg.data = res
      if (res?.requires_confirmation) {
        markRunningTaskPending(shellId)
        upsertHistory({ ...runningShell, status: 'pending_confirmation' })
      } else if (!res?.error) {
        saveCurrentToHistory(res, { preferId: shellId })
        markRunningTaskCompleted(shellId, taskOutcome(res || aiMsg.data).status)
      } else {
        markRunningTaskFailed(shellId)
      }
    } else if (!aiMsg.data) {
      aiMsg.loading = false
      aiMsg.data = { aborted: true }
      markRunningTaskFailed(shellId)
    } else {
      aiMsg.loading = false
      markRunningTaskFailed(shellId)
    }
    thinkingOpen[aid] = false
    if (res && !res?.requires_confirmation && !res?.error) scheduleChatReportTop(48, 'smooth')
    else scheduleChatScroll(48, 'smooth')
  } catch (err) {
    if (isAbortLikeInteractionError(err)) {
      aiMsg.loading = false
      aiMsg.data = { aborted: true, question: text }
      thinkingOpen[aid] = false
      scheduleChatScroll(36, 'smooth')
      markRunningTaskFailed(shellId)
      return
    }
    if (aiMsg.data?.requires_confirmation && session.state.status === 'waiting_confirmation') {
      aiMsg.loading = false
      thinkingOpen[aid] = false
      scheduleChatScroll(36, 'smooth')
      return
    }
    aiMsg.loading = false
    aiMsg.data = { error: err.response?.data?.error || err.message || '系统繁忙' }
    query.value = text
    scheduleChatScroll(36, 'smooth')
  } finally {
    stopTimer()
    finishQuestionQueue(aiMsg.data)
  }
}

// 纠正条 chip 点击：把候选理解直接作为新问题发送（复用主发送链路）
const applyClarifySuggestion = (text) => {
  const t = String(text || '').trim()
  if (!t || isRunning.value) return
  query.value = t
  handleSend()
}

// 纠正条/错字卡自由输入：推荐候选都不是时，用户直接输入新问句走主链路
const submitClarifyDraft = (msg) => {
  const text = String(clarifyDrafts[msg?.id] || '').trim()
  if (!text || isRunning.value) return
  clarifyDrafts[msg.id] = ''
  applyClarifySuggestion(text)
}

const handleClarifyDraftEnter = (event, msg) => {
  if (event?.isComposing) return
  submitClarifyDraft(msg)
}

// 错字短路纠正卡：用户确认原问题没错字，带 skipTypoCheck 跳过第 0 层快检重新发送
const resendOriginalQuestion = (msg) => {
  const t = String(msg?.data?.question || msg?.question || '').trim()
  if (!t || isRunning.value) return
  query.value = t
  handleSend({ skipTypoCheck: true })
}

const questionQueue=ref([])
const queuePaused=ref(false)
const queueDraftFlow=ref('')
const queueReason=ref('')
const sendInFlight=ref(false)
let queueGeneration=0
const pauseQuestionQueue=reason=>{queuePaused.value=true;queueReason.value=reason}
const clearQuestionQueue=()=>{questionQueue.value=[];queuePaused.value=false;queueReason.value=''}
const removeQueuedQuestion=id=>{questionQueue.value=questionQueue.value.filter(item=>item.id!==id)}
const editQueuedQuestion=id=>{
  const item=questionQueue.value.find(item=>item.id===id)
  if(!item || isViewingReadonly.value)return
  if(query.value.trim()){ElMessage.info('先发送或整理当前草稿，再编辑队列问题');return}
  query.value=item.question;datasetId.value=item.datasetId;modelId.value=item.modelId;queueDraftFlow.value=item.flow
  isDatasetManuallySelected.value=Boolean(item.datasetId)
  removeQueuedQuestion(id);focusComposer()
}
const drainQuestionQueue=()=>{
  if(sendInFlight.value || isRunning.value || isViewingReadonly.value || queuePaused.value || !questionQueue.value.length)return
  if(!canUseFeature('ask_send_question')){pauseQuestionQueue('发送权限已变更，请确认后继续');return}
  if(session.state.status==='waiting_confirmation'){pauseQuestionQueue(queuePauseReason('waiting'));return}
  const upcoming=questionQueue.value[0]
  if(upcoming.datasetId && (!canUseFeature('ask_dataset_select') || !datasets.value.some(d=>Number(d.id)===Number(upcoming.datasetId)))){pauseQuestionQueue('排队问题的数据集或选择权限已变更，请检查后继续');return}
  if(upcoming.modelId && (!canUseFeature('ask_model_select') || !aiModels.value.some(m=>Number(m.id)===Number(upcoming.modelId)))){pauseQuestionQueue('排队问题的模型或选择权限已变更，请检查后继续');return}
  const [item,...rest]=questionQueue.value
  questionQueue.value=rest
  void handleSend({_queueItem:item})
}
const resumeQuestionQueue=()=>{
  if(session.state.status==='waiting_confirmation'){ElMessage.info('请先确认当前问题或研究计划');return}
  queuePaused.value=false;queueReason.value='';drainQuestionQueue()
}
const finishQuestionQueue=result=>{
  const reason=queuePauseReason(taskOutcome(result).status)
  if(reason){if(questionQueue.value.length)pauseQuestionQueue(reason);return}
  if(queueReason.value===queuePauseReason('waiting')){queuePaused.value=false;queueReason.value=''}
  window.setTimeout(drainQuestionQueue,0)
}
const handleSend = async (sendOptions) => {
  const opts = (sendOptions && typeof sendOptions === 'object' && !Array.isArray(sendOptions)) ? sendOptions : undefined
  if (!canUseFeature('ask_send_question')) return
  const queued=opts?._queueItem
  const text = String(queued?.question || query.value).trim()
  if (!text || isViewingReadonly.value) return
  const submitted=queued || queuedQuestion(text,{datasetId:opts?.datasetId || getDatasetInputForQuestion(text),datasetName:datasets.value.find(d=>Number(d.id)===Number(opts?.datasetId || getDatasetInputForQuestion(text)))?.dataset_name,modelId:getModelInputForQuestion(),flow:queueDraftFlow.value || requestedFlow.value})
  if(!queued && (isRunning.value || sendInFlight.value || questionQueue.value.length || session.state.status==='waiting_confirmation')){
    try{questionQueue.value=appendQuestion(questionQueue.value,submitted)}catch(error){ElMessage.info(error.message);return}
    query.value='';queueDraftFlow.value='';clearPendingQuickDataset()
    if(session.state.status==='waiting_confirmation')pauseQuestionQueue(queuePauseReason('waiting'))
    drainQuestionQueue();focusComposer();return
  }
  const dispatchToken=++queueGeneration
  sendInFlight.value=true
  requestedFlow.value=submitted.flow
  if(!queued){query.value='';queueDraftFlow.value='';queuePaused.value=false;queueReason.value=''}
  const createShellId = () => {
    if (typeof window !== 'undefined' && window.crypto?.randomUUID) {
      return `history-report-${window.crypto.randomUUID()}`
    }
    return `history-report-${Date.now()}-${Math.random().toString(16).slice(2)}`
  }
  const shellId = createShellId()

  const runningShell = {
    id: shellId,
    title: String(text).slice(0, 24),
    question: text,
    datasetId: submitted.datasetId,
    datasetName: submitted.datasetName,
    updatedAt: new Date().toISOString(),
    status: 'running',
    reportSnapshot: null,
  }
  upsertHistory(runningShell)
  setActiveHistory(shellId)
  setRunningSessionId(shellId)
  switchViewToDefault()

  const uid = ++msgCounter
  messages.push({ id: uid, role: 'user', content: text })
  const aid = ++msgCounter
  const aiMsg = { id: aid, role: 'ai', loading: true, data: null }
  messages.push(aiMsg)
  activeRequestAiMessageId.value = aid
  thinkingOpen[aid] = true

  clearExecutionPanelState()
  scheduleChatScroll(24, 'smooth')
  startTimer()

  try {
    // 解析条确认链路可显式锚定数据集（opts.datasetId）：用户已明确指定口径，
    // 跳过 datasetInput 的自动释放启发式
    const res = await session.startAsk(text, submitted.datasetId, submitted.modelId, { ...opts, _queueItem:undefined, askFlow:undefined })
    clearPendingQuickDataset()
    if (res) {
      aiMsg.loading = false
      aiMsg.data = res
      if (res?.requires_confirmation) {
        markRunningTaskPending(shellId)
        upsertHistory({ ...runningShell, status: 'pending_confirmation' })
      } else if (!res?.error) {
        saveCurrentToHistory(res, { preferId: shellId })
        markRunningTaskCompleted(shellId, taskOutcome(res || aiMsg.data).status)
      } else {
        markRunningTaskFailed(shellId)
      }
    } else if (!aiMsg.data) {
      aiMsg.loading = false
      aiMsg.data = { aborted: true }
      markRunningTaskFailed(shellId)
    } else {
      aiMsg.loading = false
      markRunningTaskCompleted(shellId, taskOutcome(res || aiMsg.data).status)
    }
    thinkingOpen[aid] = false
    if (res && !res?.requires_confirmation && !res?.error) scheduleChatReportTop(48, 'smooth')
    else scheduleChatScroll(48, 'smooth')
  } catch (err) {
    if (isAbortLikeInteractionError(err)) {
      aiMsg.loading = false
      aiMsg.data = { aborted: true, question: text }
      thinkingOpen[aid] = false
      scheduleChatScroll(36, 'smooth')
      markRunningTaskFailed(shellId)
      return
    }
    if (aiMsg.data?.requires_confirmation && session.state.status === 'waiting_confirmation') {
      aiMsg.loading = false
      thinkingOpen[aid] = false
      scheduleChatScroll(36, 'smooth')
      return
    }
    aiMsg.loading = false
    aiMsg.data = { error: err.response?.data?.error || err.message || '系统繁忙' }
    if(!query.value.trim() && !queued)query.value = text
    scheduleChatScroll(36, 'smooth')
    markRunningTaskFailed(shellId)
  } finally {
    if(dispatchToken===queueGeneration){stopTimer();sendInFlight.value=false;finishQuestionQueue(aiMsg.data)}
  }
}

const handleStop = () => {
  if (!canUseFeature('ask_stop_run')) return
  if(questionQueue.value.length)pauseQuestionQueue(queuePauseReason('canceled'))
  session.stopAsk()
  const msg = latestAiMessage.value
  if (msg?.role === 'ai' && msg.loading) {
    msg.loading = false
    msg.data = {
      ...(msg.data || {}),
      aborted: true,
      requires_confirmation: false,
      workflow: { ...session.state.workflow, status: "canceled" },
      question: session.state.question || query.value.trim(),
    }
    thinkingOpen[msg.id] = false
  }
  stopTimer()
  if (runningSessionId.value) {
    markRunningTaskFailed(runningSessionId.value)
  }
  ElMessage({
    message: '已停止执行',
    type: 'warning',
    duration: 1500,
    showClose: false,
    customClass: 'ax-toast-modern ax-toast-stop',
  })
}

const resetForNewChat = () => {
  queueGeneration++;sendInFlight.value=false
  questionQueue.value=[];queuePaused.value=false;queueReason.value='';queueDraftFlow.value=''
  // 修 1（reset 保存 guard）：只有完整、正确的结果才保存，避免把 requires_confirmation 中间态
  // （行业部 Overview 层级）当成正式历史保存；也避免旧会话残留的脏 result 被保存。
  const cur = session.state.result || null
  const isCompleteResult = Boolean(
    cur &&
    typeof cur === 'object' &&
    !cur.requires_confirmation &&
    !cur.error &&
    Array.isArray(cur.dataset_results) &&
    cur.dataset_results.length > 0
  )
  if (isCompleteResult) saveCurrentToHistory(cur)
  messages.splice(0, messages.length)
  activeRequestAiMessageId.value = null
  query.value = ''
  clearRestoreRequest()
  setActiveHistory('')
  clearChatUiState()
  session.resetSession()
  showPanel.value = false
  nextTick(() => {
    scheduleChatScroll(20, 'auto')
    schedulePanelScroll(20, 'auto', true)
    focusComposer()
  })
}

const handleNewChat = async () => {
  if (messages.length === 0) {
    resetForNewChat()
    return
  }

  try {
    await ElMessageBox.confirm(
      questionQueue.value.length ? '开始新会话后，将清空待问队列与未发送草稿；当前记录归档到历史对话。' : '开始新会话后，当前执行记录会被清空，并自动归档到历史对话中。',
      '开始新会话',
      {
        type: 'info',
        confirmButtonText: '开始新会话',
        cancelButtonText: '暂不切换',
        distinguishCancelAndClose: true,
        customClass: 'ax-message-box',
      }
    )
    resetForNewChat()
  } catch {
    // user cancelled
  }
}

const historyPanelRef = ref(null)
const focusSidebarHistory = () => {
  historyPanelRef.value?.open()
}

const handleSelectHistorySession = async (item) => {
  if (isRunning.value) {
    ElMessage.warning('当前有任务正在执行，请稍候再切换')
    return
  }
  if (!item || item.id === activeHistoryId.value) return
  if(questionQueue.value.length)pauseQuestionQueue('正在查看历史会话，返回后可继续队列')
  await restoreHistory(item)
}

const handleDeleteHistorySession = async (item, event) => {
  event?.stopPropagation()
  if (!item?.id) return
  try {
    await removeHistory(item.id)
    ElMessage.success('已删除该会话记录')
    if (activeHistoryId.value === item.id) {
      resetForNewChat()
    }
  } catch (e) {
    ElMessage.error('删除会话失败')
  }
}

const handleClearAllSessions = async () => {
  try {
    await ElMessageBox.confirm('确定要清空全部历史会话记录吗？', '提示', {
      confirmButtonText: '确定清空',
      cancelButtonText: '取消',
      type: 'warning',
      customClass: 'ax-message-box',
    })
    await clearHistory()
    resetForNewChat()
    ElMessage.success('已清空全部会话')
  } catch (e) {
    // cancelled
  }
}

const datasetNameMap = computed(() => new Map(
  (datasets.value || []).map(item => [Number(item.id), item.dataset_name])
))

const normalizeReportTitle = (text) => {
  let s = String(text ?? '').trim()
  if (!s) return '业绩分析报告'
  s = s.replace(
    /^(?:我说的是|我说的是|我说|我的问题是|我想问|我想知道|请问|问一下|看一下|查一下|看下|查下|请|麻烦|帮我|给我|告诉我|咨询一下|了解一下|看看)(?:[，,：:\s]+)?/,
    ''
  )
  s = s.replace(/[？?！!。]+$/g, '').trim()
  if (s.endsWith('的')) {
    s = s.slice(0, -1).trim()
  }
  return s || '业绩分析报告'
}

const buildDownloadFilename = (title) => {
  const base = String(normalizeReportTitle(title))
    .replace(/[\\/:*?"<>|]+/g, '-')
    .replace(/\s+/g, ' ')
    .trim()
  return `${base || '业绩分析报告'}.pdf`
}

const buildReportHtml = (title, report) => `<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>${normalizeReportTitle(title)}</title>
  <style>
    @page { size: A4; margin: 16mm 14mm; }
    :root { --primary: #1A1A1A; --page-bg: #F2F5F4; --card-bg: #ffffff; --text: #111827; }
    body { margin: 0; font-family: var(--font-sans, "Microsoft YaHei UI", "Microsoft YaHei", "PingFang SC", sans-serif); background: var(--page-bg); color: var(--text); }
    .page { max-width: 960px; margin: 0 auto; padding: 40px 24px 72px; }
    .card { background: var(--card-bg); border-radius: 4px; padding: 28px 32px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
    .eyebrow { font-size: 12px; color: var(--primary); font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; }
    h1 { margin: 12px 0 8px; font-size: 28px; line-height: 1.25; }
    h2 { margin: 28px 0 12px; font-size: 20px; }
    h3 { margin: 20px 0 10px; font-size: 16px; }
    p, li { font-size: 14px; line-height: 1.8; color: #6B7280; }
    hr { border: none; border-top: 1px solid #E5E7EB; margin: 24px 0; }
    code { background: #F3F4F6; padding: 2px 6px; border-radius: 6px; }
    table { width: 100%; border-collapse: collapse; margin: 16px 0; }
    th, td { border: 1px solid #E5E7EB; padding: 10px 12px; text-align: left; font-size: 13px; }
    th { background: #F2F5F4; color: #111827; }
    .print-tip { margin-top: 20px; font-size: 12px; color: #9CA3AF; }
    @media print {
      body { background: #ffffff; }
      .page { max-width: none; padding: 0; }
      .card { border: none; border-radius: 0; padding: 0; box-shadow: none; }
      .print-tip { display: none; }
    }
  </style>
</head>
<body>
  <main class="page">
    <section class="card">
      <div class="eyebrow">Data Agent Report</div>
      <h1>${normalizeReportTitle(title)}</h1>
      <article>${renderMd(report)}</article>
      <div class="print-tip">请在打印对话框中选择“另存为 PDF”</div>
    </section>
  </main>
</body>
</html>`

const downloadLatestReport = (report = latestReport.value, title = sideReportHeading.value) => {
  if (!report) {
    ElMessage.warning('当前还没有可导出的报告内容')
    return
  }

  const exportTitle = normalizeReportTitle(title)
  if (activePrintFrame?.parentNode) {
    activePrintFrame.parentNode.removeChild(activePrintFrame)
    activePrintFrame = null
  }

  const frame = document.createElement('iframe')
  frame.style.position = 'fixed'
  frame.style.right = '0'
  frame.style.bottom = '0'
  frame.style.width = '0'
  frame.style.height = '0'
  frame.style.border = '0'
  frame.style.opacity = '0'
  frame.setAttribute('aria-hidden', 'true')
  document.body.appendChild(frame)
  activePrintFrame = frame

  const html = buildReportHtml(exportTitle, report)
  let printed = false
  const triggerPrint = () => {
    if (printed) return
    printed = true
    const frameWindow = frame.contentWindow
    if (!frameWindow) {
      ElMessage.warning('当前无法打开打印窗口，请稍后重试')
      return
    }

    try {
      frameWindow.document.open()
      frameWindow.document.write(html)
      frameWindow.document.close()
      frameWindow.document.title = buildDownloadFilename(exportTitle)
      frameWindow.focus()
      window.setTimeout(() => {
        frameWindow.print()
      }, 260)
      ElMessage.success('已准备好报告，请在打印对话框中选择“另存为 PDF”')
    } catch (error) {
      ElMessage.warning('当前无法导出 PDF，请稍后重试')
    }
  }

  frame.onload = triggerPrint
  window.setTimeout(triggerPrint, 40)
}
const draftAnswerFollowUp = (item) => {
  if (isRunning.value || isViewingReadonly.value || !canUseFeature('ask_send_question') || !canUseFeature('ask_quick_ask')) return
  // The same controlled dataset router rechecks scope when the user submits.
  quickAsk(item)
}
const quickAsk = (item) => {
  if (!canUseFeature('ask_quick_ask')) return
  const text = typeof item === 'string' ? item : String(item?.question_text || '').trim()
  if (!text) return
  const nextDatasetId = typeof item === 'string' ? null : Number(item?.dataset_id || 0)
  datasetId.value = null
  isDatasetManuallySelected.value = false
  pendingQuickDataset.value = nextDatasetId ? { datasetId: nextDatasetId, question: text } : null
  query.value = text
  nextTick(() => {
    const textarea = document.querySelector('.cmp-textarea')
    if (textarea instanceof HTMLTextAreaElement) {
      textarea.focus()
      textarea.setSelectionRange(textarea.value.length, textarea.value.length)
    }
  })
  const datasetName = typeof item === 'string' ? '' : String(item?.dataset_name || item?.dataset_tag || '').trim()
  ElMessage({
    message: datasetName ? `问题已填入 · ${datasetName}` : '问题已填入',
    type: 'success',
    duration: 1500,
    showClose: false,
    customClass: 'ax-toast-modern'
  })
}

const handleExternalFreshChat = () => {
  resetForNewChat()
}

const getConfirmOptionKey = (opt) => (typeof opt === 'string' ? opt : (opt?.id || opt?.label || JSON.stringify(opt)))
const getConfirmOptionLabel = (opt) => (typeof opt === 'string' ? opt : (opt?.label || opt?.name || '确认选项'))

const getConfirmOptionDescription = (opt) => (typeof opt === 'string' ? '' : String(opt?.description || '').trim())
const getConfirmOptionScore = (opt) => {
  if (typeof opt === 'string') return null
  const raw = opt?.score
  if (raw === null || raw === undefined || raw === '') return null
  const n = Number(raw)
  return Number.isFinite(n) ? Math.round(n) : null
}
const shouldShowConfirmOptionScore = () => false
const getConfirmOptionScorePct = (opt) => {
  const score = getConfirmOptionScore(opt)
  return score == null ? 0 : Math.min(100, Math.max(0, score))
}
const sortedConfirmationOptions = (msg) => {
  const opts = msg?.data?.confirmation_options || []
  const copy = opts.map((opt, idx) => ({ opt, idx }))
  copy.sort((a, b) => {
    const sa = getConfirmOptionScore(a.opt)
    const sb = getConfirmOptionScore(b.opt)
    if (sa != null && sb != null) return sb - sa
    if (sa != null) return -1
    if (sb != null) return 1
    return a.idx - b.idx
  })
  return copy.map(item => item.opt)
}
const visibleConfirmationOptions = (msg) => {
  const opts = sortedConfirmationOptions(msg)
  if (confirmExpanded[msg?.id]) return opts
  return opts.slice(0, 4)
}
const toggleConfirmOptions = (msgId) => {
  confirmExpanded[msgId] = !confirmExpanded[msgId]
}
const getConfirmOptionDatasetNames = (opt) => {
  if (typeof opt === 'string') return []
  const ids = Array.isArray(opt?.dataset_ids) ? opt.dataset_ids : []
  return ids.map(id => datasetNameMap.value.get(Number(id)) || `数据集 ${id}`)
}
const getConfirmOptionMemberNames = (opt) => {
  if (typeof opt === 'string') return []
  return (Array.isArray(opt?.resolved_members) ? opt.resolved_members : [])
    .map(item => String(item || '').trim())
    .filter(Boolean)
}
const getConfirmOptionImpact = (opt) => {
  if (typeof opt === 'string') return '确认后将继续执行当前问数任务。'
  const optionType = String(opt?.option_type || '')
  if (optionType === 'cross_dataset') return '确认后将以多数据集汇总方式继续生成结果和报告。'
  if (optionType === 'dataset_scope') return '确认后将采用该数据集口径，并继续生成 SQL 与分析报告。'
  if (optionType === 'dataset_disambiguation') return '确认后将采用具体数据集口径，并继续生成后续分析结果。'
  if (optionType === 'member_set_confirmation') {
    return String(opt?.scope_mode || '') === 'compare'
      ? '确认后将按成员逐个对比，再输出结论和报告。'
      : '确认后将先按该成员集合汇总，再继续生成分析结果。'
  }
  return '确认后将按照当前选定口径继续执行。'
}
const getConfirmationCandidateNames = (msg) => {
  const ids = msg?.data?.route?.candidate_dataset_ids || []
  return ids.map(id => datasetNameMap.value.get(Number(id)) || `数据集 ${id}`)
}
const getConfirmationScopeSummary = (msg) => {
  const route = msg?.data?.route || {}
  const confirmationType = String(route?.confirmation_type || '')
  const candidateCount = Array.isArray(route?.candidate_dataset_ids) ? route.candidate_dataset_ids.length : 0
  if (confirmationType === 'member_set_confirmation') {
    const memberCount = Array.isArray(route?.resolved_entities_preview) ? route.resolved_entities_preview.length : 0
    return memberCount > 0
      ? `当前需要确认集合口径，涉及 ${memberCount} 个成员，确认后会继续执行分析。`
      : '当前需要确认集合口径，确认后会继续执行分析。'
  }
  if (confirmationType === 'dataset_disambiguation') {
    return '当前命中了多个可能的数据集口径，确认后会采用对应执行范围。'
  }
  if (candidateCount > 1) return `当前存在 ${candidateCount} 个候选口径，确认后会采用对应执行范围。`
  return '当前需要先确认业务口径，确认后才会继续执行查询与报告生成。'
}

const doConfirm = async (opt, msg) => {
  // 第一时间设置提交状态，立即禁用按钮，防止重复点击或事件冒泡干扰
  if (msg?.id) confirmationSubmitting[msg.id] = true
  // 用户确认后，全局状态从待确认变回执行中，同步顶部banner和左侧任务状态
  if (runningTaskStatus.value === 'pending_confirmation' && runningSessionId.value) {
    runningTaskStatus.value = 'running'
    pendingTaskId.value = null
    const currentShell = historySessions.value.find(h => h.id === runningSessionId.value)
    if (currentShell) {
      upsertHistory({ ...currentShell, status: 'running' })
    }
  }
  startTimer()
  detailReportResult.value = null
  const originalData = msg?.data ? JSON.parse(JSON.stringify(msg.data)) : null
  // 预选联动：点确认选项立即把解析条更新为选中的数据集/节点（执行中也显示所选，不等执行完）。
  // 解决"我选了商用，但上面解析条没变"——ParseBar 用 slots 渲染，更新 slots 即联动（2026-09-01 用户实测反馈）。
  if (msg?.data?.parse_bar && opt && typeof opt === 'object') {
    const pb = msg.data.parse_bar
    const selNode = String(opt.resolved_subject_name || '').trim()
    const selDs = String(opt.dataset_name || '').trim()
    if (Array.isArray(pb.slots)) {
      pb.slots = pb.slots.map((s) => {
        if (s && s.slot === 'node' && selNode) return { ...s, resolved_value: selNode }
        if (s && s.slot === 'dataset' && selDs) return { ...s, resolved_value: selDs }
        return s
      })
    }
  }
  if (msg) {
    msg.loading = true
  }
  try {
    const res = await session.submitBossConfirmation(opt, {
      candidateDatasetIds: msg?.data?.route?.candidate_dataset_ids || msg?.data?.route?.dataset_ids || [],
      originalQuestion: msg?.data?.question || session.state.question,
      sessionId: msg?.data?.session_id,
    })
    const last = [...messages].reverse().find(m => m.role === 'ai')
    if (!res) {
      if (last) {
        last.loading = false
        last.data = { aborted: true, question: session.state.question }
      }
      if (msg?.id) confirmationSubmitting[msg.id] = false
      if (runningSessionId.value) markRunningTaskFailed(runningSessionId.value)
      scheduleChatScroll(36, 'smooth')
      return
    }
    if (last) {
      last.loading = false
      last.data = res
      activeRequestAiMessageId.value = last.id
    }
    if (!res?.requires_confirmation && !res?.error) {
      saveCurrentToHistory(res, { preferId: runningSessionId.value })
      markRunningTaskCompleted(runningSessionId.value,taskOutcome(res).status)
    } else if (res?.requires_confirmation) {
      markRunningTaskPending(runningSessionId.value)
      const currentShell = historySessions.value.find(h => h.id === runningSessionId.value)
      if (currentShell) {
        upsertHistory({ ...currentShell, status: 'pending_confirmation' })
      }
    } else {
      markRunningTaskFailed(runningSessionId.value)
    }
    if (msg?.id && typeof opt === 'string') confirmationDrafts[msg.id] = ''
    if (!res?.requires_confirmation && !res?.error) scheduleChatReportTop(36, 'smooth')
    else scheduleChatScroll(36, 'smooth')
  } catch (error) {
    if (isAbortLikeInteractionError(error)) {
      if (msg) {
        msg.loading = false
        msg.data = { aborted: true, question: session.state.question }
      }
      if (msg?.id) confirmationSubmitting[msg.id] = false
      scheduleChatScroll(36, 'smooth')
      return
    }
    if (msg) {
      msg.loading = false
      if (originalData?.requires_confirmation) {
        msg.data = {
          ...originalData,
          requires_confirmation: true,
          error: '',
        }
      }
    }
    if (msg?.id) confirmationSubmitting[msg.id] = false
    ElMessage.error(error?.response?.data?.error || error?.message || '提交失败')
    scheduleChatScroll(36, 'smooth')
  }
  finally { if (msg?.id) confirmationSubmitting[msg.id] = false; stopTimer(); finishQuestionQueue(msg?.data) }
}

const scrollChat = (behavior = 'smooth') => nextTick(() => {
  if (chatBodyRef.value) {
    chatBodyRef.value.scrollTo({ top: chatBodyRef.value.scrollHeight, behavior })
  }
})

const scrollChatToReportTop = (behavior = 'auto') => nextTick(() => {
  const container = chatBodyRef.value
  if (!container) return
  const latestId = latestAiMessage.value?.id
  const researchDesks = container.querySelectorAll('.research-desk.is-research')
  const researchDesk = researchDesks[researchDesks.length - 1]
  const researchTarget = researchDesk?.querySelector('.research-report') || researchDesk
  const allResultChains = Array.from(container.querySelectorAll('.ax-result-chain'))
  const target = researchTarget || (latestId && resultChainRefs.get(latestId))
    || allResultChains[allResultChains.length - 1]
  if (!target) {
    scrollChat(behavior)
    return
  }
  const containerRect = container.getBoundingClientRect()
  const targetRect = target.getBoundingClientRect()
  const top = container.scrollTop + targetRect.top - containerRect.top - 12
  container.scrollTo({ top: Math.max(0, top), behavior })
})

const isPanelNearBottom = () => {
  const el = panelRef.value
  if (!el) return true
  return el.scrollHeight - el.scrollTop - el.clientHeight < 120
}

const shouldFollowPanelBottom = () => ['running', 'waiting_confirmation'].includes(session.state.status)

const scrollPanel = (behavior = 'auto', force = false) => nextTick(() => {
  if (panelRef.value && (force || shouldFollowPanelBottom() || isPanelNearBottom())) {
    panelRef.value.scrollTo({ top: panelRef.value.scrollHeight, behavior })
  }
})

const {
  saveCurrentToHistory,
  restoreHistory,
} = useDataPulseReportHistory({
  session,
  messages,
  datasetId,
  datasets,
  isRunning,
  isDatasetVisible,
  ensureDatasetsReady,
  loadHistory,
  upsertHistory,
  setActiveHistory,
  detailReportResult,
  showPanel,
  thinkingOpen,
  logOpen,
  timelineVersion,
  scrollChat,
  scrollPanel,
  createMessageId: () => ++msgCounter,
})

const scheduleChatScroll = (delay = 40, behavior = 'smooth') => {
  if (isViewingReadonly.value) return
  if (chatScrollTimer) clearTimeout(chatScrollTimer)
  chatScrollTimer = window.setTimeout(() => {
    if (latestAiMessage.value?.data?.research_plan) scrollChatToReportTop(behavior)
    else scrollChat(behavior)
  }, delay)
}

const clearReportTopScrollTimers = () => {
  reportTopScrollTimers.forEach(timer => clearTimeout(timer))
  reportTopScrollTimers = []
}

const scheduleChatReportTop = (delay = 40, behavior = 'auto') => {
  if (isViewingReadonly.value) return
  if (chatScrollTimer) clearTimeout(chatScrollTimer)
  clearReportTopScrollTimers()
  ;[delay, delay + 90, delay + 240].forEach((timeout) => {
    reportTopScrollTimers.push(window.setTimeout(() => {
      scrollChatToReportTop(behavior)
    }, timeout))
  })
}

const schedulePanelScroll = (delay = 150, behavior = 'auto', force = false) => {
  if (panelScrollTimer) clearTimeout(panelScrollTimer)
  panelScrollTimer = window.setTimeout(() => {
    scrollPanel(behavior, force)
  }, delay)
}

const startTimer = () => {
  elapsed.value = 0
  clearInterval(timerInst)
  timerInst = setInterval(() => elapsed.value++, 1000)
}

const compactQuestionText = (value) => String(value || '').replace(/\s+/g, '').toLowerCase()

const isConsumerDatasetMeta = (dataset = {}) => {
  const text = compactQuestionText(`${dataset.dataset_code || ''}${dataset.dataset_name || ''}${dataset.business_domain || ''}${dataset.description || ''}`)
  return text.includes('consumer') || text.includes('消费者') || text.includes('消费事业群')
}

const datasetAliasScore = (text, dataset) => {
  const question = compactQuestionText(text)
  if (!question || !dataset) return 0
  const aliases = [
    dataset.dataset_name,
    dataset.business_domain,
    ...(Array.isArray(dataset.synonyms) ? dataset.synonyms : []),
  ].map(compactQuestionText).filter(Boolean)
  let score = 0
  const suffixes = ['事业群', '战区', '行业部', '片区', '数据集', '销售业绩分析', '业绩分析']
  aliases.forEach((alias) => {
    if (alias.length < 2 || ['业绩', '分析', '数据', '指标', '结果'].includes(alias)) return
    if (question.includes(alias)) score = Math.max(score, 95)
    suffixes.forEach((suffix) => {
      if (!alias.includes(suffix)) return
      const prefix = alias.split(suffix, 1)[0]
      if (prefix.length >= 2 && question.includes(prefix)) score = Math.max(score, 90)
    })
  })
  if (isConsumerDatasetMeta(dataset)) {
    const consumerBranchAliases = ['沧岩战区', '沧岩', '澔岳战区']
    if (consumerBranchAliases.some(alias => question.includes(compactQuestionText(alias)))) {
      score = Math.max(score, 94)
    }
  }
  return score
}

const shouldReleaseSelectedDatasetForQuestion = (text, selectedId) => {
  if (!selectedId) return false
  const selected = datasets.value.find(item => Number(item.id) === Number(selectedId))
  if (!selected) return false
  const selectedScore = datasetAliasScore(text, selected)
  const bestOther = datasets.value
    .filter(item => Number(item.id) !== Number(selectedId))
    .map(item => ({ dataset: item, score: datasetAliasScore(text, item) }))
    .sort((left, right) => right.score - left.score)[0]
  return Boolean(bestOther && bestOther.score >= 90 && bestOther.score >= selectedScore + 12)
}

const getDatasetInputForQuestion = (text) => {
  if (!canUseFeature('ask_dataset_select')) return null
  const pending = pendingQuickDataset.value
  if (pending?.datasetId && String(pending.question || '').trim() === String(text || '').trim()) {
    if (shouldReleaseSelectedDatasetForQuestion(text, pending.datasetId)) return null
    return pending.datasetId
  }
  if (datasetId.value && isDatasetManuallySelected.value) {
    return datasetId.value
  }
  return null
}

const getModelInputForQuestion = () => (
  canUseFeature('ask_model_select') ? modelId.value : null
)

const clearPendingQuickDataset = () => {
  pendingQuickDataset.value = null
}

const submitConfirmationDraft = (msg) => {
  if (!canUseFeature('ask_submit_note')) return
  const text = String(confirmationDrafts[msg?.id] || '').trim()
  if (!text || isRunning.value) return
  doConfirm(text, msg)
}

const handleConfirmationDraftEnter = (event, msg) => {
  if (event?.isComposing) return
  submitConfirmationDraft(msg)
}
const stopTimer = () => clearInterval(timerInst)

const loadQuestions = async () => {
  commonQuestionsLoading.value = true
  try {
    const res = await getCommonQuestions(null, { random: 1, limit: 4, t: Date.now() })
    commonQuestions.value = (res.questions || res.common_questions || []).slice(0, 4)
  } catch {
    commonQuestions.value = []
  } finally {
    commonQuestionsLoading.value = false
  }
}

const handleDatasetChange = async () => {
  if (!canUseFeature('ask_dataset_select')) {
    datasetId.value = null
    isDatasetManuallySelected.value = false
    clearPendingQuickDataset()
    return
  }
  isDatasetManuallySelected.value = Boolean(datasetId.value)
  clearPendingQuickDataset()
  await loadQuestions()
}

const refreshCommonQuestions = async () => {
  if (!canUseFeature('ask_quick_refresh')) return
  if (commonQuestionsLoading.value) return
  await loadQuestions()
}

const getStatusColor = (rate) => {
  const value = toNumber(rate)
  if (value === null) return '#0D9488'
  if (value >= 15) return '#10B981'
  if (value >= 10) return '#F59E0B'
  return '#0D9488'
}

const getMetricColor = (column) => {
  const text = String(column || '')
  if (/任务|目标/i.test(text)) return '#0D9488'
  if (/开单|完成|实际|销售/i.test(text)) return '#10B981'
  if (/剩余|缺口|差额/i.test(text)) return '#F59E0B'
  if (/率|percent|rate/i.test(text)) return '#f59e0b'
  return '#6B7280'
}

const sortRowsForChart = (rows = [], columns = [], lowFirst = false, preferredColumn = '') => {
  const targetColumn = preferredColumn
    || columns.find(column => isRateColumn(column))
    || Object.keys(rows[0] || {}).find(column => isRateColumn(column))
  if (!targetColumn) return rows
  return [...rows].sort((a, b) => {
    const left = toNumber(a?.[targetColumn]) || 0
    const right = toNumber(b?.[targetColumn]) || 0
    return lowFirst ? left - right : right - left
  })
}

const renderChartSpec = (chart, data) => {
  const labelColumn = data.columns?.[0]
  const numericColumns = data.columns?.slice(1) || []
  const dataset = data?.dataset || null
  const preferredSortColumn = data.sortColumn || ''
  const sortedRows = sortRowsForChart(data.rows || [], data.columns || [], Boolean(data.lowFirst), preferredSortColumn)
  const colorPalette = ['#1A1A1A', '#10B981', '#F59E0B', '#0D9488', '#9CA3AF', '#6B7280']
  const shortSeriesName = (name) => String(name || '')
    .replace(/^年度/, '')
    .replace(/^总/, '')
    .replace('任务金额', '任务')
    .replace('开单金额', '开单')
    .replace('剩余任务金额', '剩余缺口')

  if (data.chartType === 'trend') {
    chart.setOption({
      backgroundColor: 'transparent',
      color: colorPalette,
      tooltip: { trigger: 'axis' },
      legend: { top: 0, textStyle: { color: '#6B7280', fontSize: 11 } },
      grid: { left: 34, right: 18, top: 34, bottom: 28, containLabel: true },
      xAxis: {
        type: 'category',
        data: sortedRows.map(row => row[labelColumn]),
        axisLabel: { color: '#9CA3AF', fontSize: 11, hideOverlap: true },
        axisLine: { lineStyle: { color: '#E5E7EB' } },
      },
      yAxis: {
        type: 'value',
        axisLabel: { color: '#9CA3AF', fontSize: 11 },
        splitLine: { lineStyle: { color: '#F3F4F6', type: 'dashed' } },
      },
      series: numericColumns.map((column, columnIndex) => ({
        name: column,
        type: columnIndex === 0 ? 'bar' : 'line',
        smooth: true,
        barMaxWidth: 18,
        symbolSize: columnIndex === 0 ? 0 : 6,
        itemStyle: { borderRadius: columnIndex === 0 ? [4, 4, 0, 0] : 0 },
        data: sortedRows.map(row => row[column]),
      })),
    })
    return
  }

  if (data.chartType === 'combo') {
    const categoryRows = sortedRows.slice(0, 12)
    const rateColumn = numericColumns.find(column => /率|percent|rate/i.test(column)) || numericColumns[numericColumns.length - 1]
    const barColumns = numericColumns
      .filter(column => column !== rateColumn && !/剩余|缺口|remain/i.test(column))
      .slice(0, 2)
    chart.setOption({
      backgroundColor: 'transparent',
      color: colorPalette,
      tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
      legend: {
        type: 'scroll',
        top: 2,
        left: 8,
        right: 8,
        itemWidth: 10,
        itemHeight: 8,
        icon: 'roundRect',
        formatter: shortSeriesName,
        textStyle: { color: '#6B7280', fontSize: 10 },
      },
      grid: { left: 42, right: 38, top: 68, bottom: 44, containLabel: true },
      xAxis: {
        type: 'category',
        data: categoryRows.map(row => row[labelColumn]),
        axisLabel: { color: '#9CA3AF', fontSize: 11, interval: 0, rotate: categoryRows.length > 4 ? 24 : 0, hideOverlap: true, margin: 12 },
        axisLine: { lineStyle: { color: '#E5E7EB' } },
      },
      yAxis: [
        {
          type: 'value',
          axisLabel: {
            color: '#9CA3AF',
            fontSize: 11,
            formatter: value => {
              const axisColumn = barColumns.find(column => isAmountColumn(column)) || barColumns[0] || ''
              return formatChartAmount(value, dataset, axisColumn)
            },
          },
          splitLine: { lineStyle: { color: '#F3F4F6', type: 'dashed' } },
        },
        {
          type: 'value',
          axisLabel: { color: '#9CA3AF', fontSize: 11, formatter: '{value}%' },
          splitLine: { show: false },
        },
      ],
      series: [
        ...barColumns.map((column) => ({
          name: column,
          type: 'bar',
          barMaxWidth: 18,
          itemStyle: { borderRadius: [4, 4, 0, 0], color: getMetricColor(column) },
          label: isAmountColumn(column) ? {
            show: true,
            position: 'top',
            color: '#6B7280',
            fontSize: 10,
            formatter: ({ value }) => formatChartAmount(value, dataset, column),
          } : undefined,
          data: categoryRows.map(row => ({
            value: row[column],
          })),
        })),
        {
          name: rateColumn,
          type: 'line',
          yAxisIndex: 1,
          smooth: true,
          symbolSize: 6,
          lineStyle: { width: 2.5, color: getMetricColor(rateColumn) },
          label: {
            show: true,
            position: 'top',
            color: '#6B7280',
            fontSize: 10,
            distance: 6,
            formatter: ({ value }) => `${formatDisplayValue(value)}%`,
          },
          data: categoryRows.map(row => ({
            value: row[rateColumn],
            itemStyle: { color: getStatusColor(row[rateColumn]) },
          })),
        },
      ],
    })
    return
  }

  if (data.chartType === 'horizontalRateBar' || data.chartType === 'horizontalDrill') {
    const categoryRows = sortedRows.slice(0, 12).reverse()
    const rateColumn = numericColumns.find(column => isRateColumn(column)) || numericColumns[numericColumns.length - 1]
    const remainColumn = numericColumns.find(column => /剩余|缺口|remain/i.test(column))
    const series = [
      {
        name: rateColumn,
        type: 'bar',
        barMaxWidth: 14,
        itemStyle: { borderRadius: [0, 5, 5, 0] },
        label: {
          show: true,
          position: 'right',
          color: '#6B7280',
          fontSize: 10,
          formatter: ({ value }) => `${formatDisplayValue(value)}%`,
        },
        data: categoryRows.map(row => ({
          value: row[rateColumn],
          itemStyle: { color: getStatusColor(row[rateColumn]) },
        })),
      },
    ]
    if (data.chartType === 'horizontalDrill' && remainColumn) {
      series.push({
        name: remainColumn,
        type: 'bar',
        barMaxWidth: 10,
        itemStyle: { borderRadius: [0, 4, 4, 0], color: '#F59E0B' },
        label: {
          show: true,
          position: 'right',
          color: '#9CA3AF',
          fontSize: 10,
          formatter: ({ value }) => formatChartAmount(value, dataset, remainColumn),
        },
        data: categoryRows.map(row => row[remainColumn]),
      })
    }
    chart.setOption({
      backgroundColor: 'transparent',
      color: colorPalette,
      tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
      legend: {
        show: series.length > 1,
        top: 2,
        right: 8,
        itemWidth: 10,
        itemHeight: 8,
        textStyle: { color: '#6B7280', fontSize: 10 },
      },
      grid: { left: 78, right: 58, top: series.length > 1 ? 34 : 14, bottom: 18, containLabel: true },
      xAxis: {
        type: 'value',
        axisLabel: { color: '#9CA3AF', fontSize: 11, formatter: value => `${value}%` },
        splitLine: { lineStyle: { color: '#F3F4F6', type: 'dashed' } },
      },
      yAxis: {
        type: 'category',
        data: categoryRows.map(row => row[labelColumn]),
        axisLabel: { color: '#6B7280', fontSize: 11 },
        axisLine: { show: false },
        axisTick: { show: false },
      },
      series,
    })
    return
  }

  if (data.chartType === 'bar') {
    const valueColumn = numericColumns[0]
    chart.setOption({
      backgroundColor: 'transparent',
      color: [colorPalette[0]],
      tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
      grid: { left: 34, right: 18, top: 18, bottom: 48, containLabel: true },
      xAxis: {
        type: 'category',
        data: sortedRows.slice(0, 8).map(row => row[labelColumn]),
        axisLabel: { color: '#9CA3AF', fontSize: 11, interval: 0, rotate: sortedRows.length > 5 ? 18 : 0 },
        axisLine: { lineStyle: { color: '#E5E7EB' } },
      },
      yAxis: {
        type: 'value',
        axisLabel: {
          color: '#9CA3AF',
          fontSize: 11,
          formatter: value => isAmountColumn(valueColumn) ? formatChartAmount(value, dataset, valueColumn) : value,
        },
        splitLine: { lineStyle: { color: '#F3F4F6', type: 'dashed' } },
      },
      series: [{
        type: 'bar',
        barMaxWidth: 22,
        itemStyle: { borderRadius: [5, 5, 0, 0] },
        label: {
          show: true,
          position: 'top',
          color: '#6B7280',
          fontSize: 11,
          fontWeight: 600,
          formatter: ({ value }) => (isAmountColumn(valueColumn) ? formatChartAmount(value, dataset, valueColumn) : formatDisplayValue(value)),
        },
        data: sortedRows.slice(0, 8).map(row => ({
          value: row[valueColumn],
          itemStyle: { color: isRateColumn(valueColumn) ? getStatusColor(row[valueColumn]) : colorPalette[0] },
        })),
      }],
    })
    return
  }

  const valueColumn = numericColumns[0]
  chart.setOption({
    color: colorPalette,
    tooltip: { trigger: 'item' },
    series: [{
      type: 'pie',
      radius: ['48%', '74%'],
      center: ['50%', '52%'],
      avoidLabelOverlap: true,
      label: {
        show: true,
        color: '#6B7280',
        fontSize: 11,
        lineHeight: 16,
        formatter: ({ name, percent, value }) => `${name}\n${formatDisplayValue(value)} · ${percent}%`,
      },
      labelLine: {
        show: true,
        length: 10,
        length2: 8,
        lineStyle: {
          color: 'rgba(0, 0, 0, 0.7)',
        },
      },
      data: sortedRows.slice(0, 6).map(row => ({ name: row[labelColumn], value: row[valueColumn] })),
    }],
  })
}

const chartRenderSignature = (data, key = '') => [
  key,
  data?.chartType || '',
  data?.title || '',
  Array.isArray(data?.columns) ? data.columns.join('|') : '',
  Array.isArray(data?.rows) ? data.rows.length : 0,
  data?.lowFirst ? 'low' : 'high',
].join('::')

const scheduleChartResize = (chart) => {
  if (!chart) return
  requestAnimationFrame(() => chart.resize())
}

const resizeRenderedCharts = () => {
  requestAnimationFrame(() => {
    document
      .querySelectorAll('.ax-inline-visual-chart, .ax-main-chart, .ax-side-extra-chart-canvas, .ax-report-chart-canvas, .ax-office-chart')
      .forEach((el) => {
        const chart = echarts.getInstanceByDom(el)
        if (chart) chart.resize()
      })
    if (chartDialogRef.value) {
      const dialogChart = echarts.getInstanceByDom(chartDialogRef.value)
      if (dialogChart) dialogChart.resize()
    }
  })
}

const initPreviewChart = (el, data, key) => {
  if (!el || !data?.rows?.length || !data?.columns?.length) return
  const signature = chartRenderSignature(data, key)
  nextTick(() => {
    const chart = echarts.getInstanceByDom(el) || echarts.init(el)
    const cached = chartElementCache.get(el)
    if (cached?.signature === signature && cached?.data === data) {
      return
    }
    renderChartSpec(chart, data)
    chartElementCache.set(el, { signature, data })
    scheduleChartResize(chart)
  })
}

const initLogChart = (el, data, key) => {
  if (!el || !data?.rows?.length || !data?.columns?.length) return
  const signature = chartRenderSignature(data, key)
  nextTick(() => {
    const chart = echarts.getInstanceByDom(el) || echarts.init(el)
    const cached = chartElementCache.get(el)
    if (cached?.signature === signature && cached?.data === data) {
      return
    }
    renderChartSpec(chart, data)
    chartElementCache.set(el, { signature, data })
    scheduleChartResize(chart)
  })
}

const renderDialogChart = () => {
  if (!chartViewerVisible.value || chartViewerMode.value !== 'chart' || !chartDialogRef.value || !chartViewerSpec.value) return
  if (chartViewerSpec.value.chartType === 'metric') return
  nextTick(() => {
    const chart = echarts.getInstanceByDom(chartDialogRef.value) || echarts.init(chartDialogRef.value)
    renderChartSpec(chart, chartViewerSpec.value)
    chart.resize()
  })
}

// 监听日志更新，自动展开最新节点
watch(() => session.state.logs.length, (len) => {
  if (len > 0) {
    logOpen[len - 1] = true
    if (!session.state.workflow.run_id) scheduleChatScroll(26, 'smooth')
    schedulePanelScroll(60, 'auto', shouldFollowPanelBottom())
  }
}, { flush: 'post' })

watch(() => session.state.logs.map(log => log.pulseText || '').join('|'), (signature) => {
  if (!signature) return
  if (!session.state.workflow.run_id) scheduleChatScroll(26, 'smooth')
  schedulePanelScroll(60, 'auto', shouldFollowPanelBottom())
}, { flush: 'post' })

watch(() => session.state.status, (s) => {
  syncPendingConfirmationMessage()
  syncCompletedResultMessage()
  if (s === 'completed') {
    nextTick(() => {
      scheduleChatReportTop(0, 'auto')
      if (hasSideReport.value) scrollPanelToReportTop()
    })
  }
  if (s === 'waiting_confirmation') {
    if (!session.state.workflow.run_id) scheduleChatScroll(26, 'smooth')
    schedulePanelScroll(60, 'auto', true)
  }
})

watch(() => session.state.result, () => {
  syncPendingConfirmationMessage()
  syncCompletedResultMessage()
}, { flush: 'post' })

watch(() => hasSideReport.value, (ready) => {
  if (ready && session.state.status === 'completed') {
    scrollPanelToReportTop()
    scheduleChatReportTop(0, 'auto')
  }
}, { flush: 'post' })

watch(() => [chartViewerVisible.value, chartViewerSpec.value, chartViewerMode.value], ([visible]) => {
  if (visible) {
    renderDialogChart()
    return
  }

  if (chartDialogRef.value) {
    const chart = echarts.getInstanceByDom(chartDialogRef.value)
    if (chart) chart.dispose()
  }

  chartViewerMode.value = 'chart'
}, { flush: 'post' })

watch(() => chartViewerMode.value, (mode) => {
  if (mode === 'chart') {
    renderDialogChart()
    return
  }

  if (chartDialogRef.value) {
    const chart = echarts.getInstanceByDom(chartDialogRef.value)
    if (chart) chart.dispose()
  }
})

watch(() => messages.length, () => {
  scheduleChatScroll(24, 'smooth')
}, { flush: 'post' })

const handleReturnToRunning = () => {
  switchViewToRunning()
  const targetId = runningSessionId.value || completedTaskId.value
  if (targetId) {
    setActiveHistory(targetId)
  } else {
    setActiveHistory(null)
  }
}

watch(() => pendingRestoreId.value, async (historyId) => {
  if (!historyId) return
  const item = findHistoryById(historyId)
  if (!item) {
    ElMessage.warning('未找到对应的历史对话记录')
    clearRestoreRequest()
    return
  }
  const options = takePendingRestoreOptions()
  await restoreHistory(item, options)
  if (!options?.readonly) {
    datasetId.value = null
    isDatasetManuallySelected.value = false
  }
  clearRestoreRequest()
}, { flush: 'post', immediate: true })

watch(canViewCharts, (allowed) => {
  if (!allowed) {
    chartViewerVisible.value = false
  }
})

watch(canViewFullscreenReport, (allowed) => {
  if (!allowed) {
    reportViewerVisible.value = false
  }
})

// 已选模型被后端过滤（未测通/同名去重/权限不足）时回退 Auto，避免 el-select 显示裸 id（bug 2026-08-26）
const sanitizeModelSelection = () => {
  if (modelId.value != null && !aiModels.value.some(m => Number(m.id) === Number(modelId.value))) {
    modelId.value = null
  }
}

onMounted(async () => {
  window.addEventListener('datapulse-create-fresh-chat', handleExternalFreshChat)
  loadFeatureFlags()
  refreshAskCapabilities()
  loadHistory()

  // 从 sessionStorage 还原输入状态
  const cached = getSessionCache()
  if (cached.query) query.value = cached.query
  if (cached.modelId !== undefined) modelId.value = cached.modelId

  try {
    const res = await getBookshelfDatasets()
    datasets.value = res.datasets || []
    markDatasetsLoaded()
    sanitizeDatasetSelection()
    await loadQuestions()
  } catch {}

  try {
    const modelRes = await getActiveAIModels()
    aiModels.value = modelRes.models || []
    sanitizeModelSelection()
  } catch {}

  if (session.state.selectedDatasetId && !isDatasetVisible(session.state.selectedDatasetId)) {
    session.state.selectedDatasetId = null
  }

  // 页面重新打开时不自动回灌旧结果；历史恢复仍通过显式操作触发。
  // 守卫细节见 clearStaleSessionState 定义处（L1346 区域）。
  clearStaleSessionState()
})

// keep-alive 重新激活时刷新引用数据（数据集、模型可能在其他页面被修改）
onActivated(async () => {
  refreshAskCapabilities()
  try {
    const res = await getBookshelfDatasets()
    datasets.value = res.datasets || []
    markDatasetsLoaded()
    sanitizeDatasetSelection()
  } catch {}
  try {
    const modelRes = await getActiveAIModels()
    aiModels.value = modelRes.models || []
    sanitizeModelSelection()
  } catch {}
  loadHistory()
  // keep-alive 切回也会复用旧实例上的 reactive 状态；同样需要清掉刷新/上一次卡死时的残留
  clearStaleSessionState()
})

watch(datasetId, refreshAskCapabilities)
// 将关键输入状态持久化到 sessionStorage，页面跳转后还原
watch([query, datasetId, modelId, isDatasetManuallySelected], ([q, d, m, manual]) => {
  setSessionCache({ query: q, datasetId: manual ? d : null, modelId: m })
}, { flush: 'post' })

onDeactivated(() => {
  if(questionQueue.value.length)pauseQuestionQueue('已离开问数页，返回后可继续队列')
  // keep-alive 停用时的轻量清理（不销毁组件状态）
  if (chatScrollTimer) clearTimeout(chatScrollTimer)
  if (panelScrollTimer) clearTimeout(panelScrollTimer)
  clearReportTopScrollTimers()
})

onUnmounted(() => {
  window.removeEventListener('datapulse-create-fresh-chat', handleExternalFreshChat)
  stopTimer()
  if (chatScrollTimer) clearTimeout(chatScrollTimer)
  if (panelScrollTimer) clearTimeout(panelScrollTimer)
  clearReportTopScrollTimers()
  if (activePrintFrame?.parentNode) {
    activePrintFrame.parentNode.removeChild(activePrintFrame)
    activePrintFrame = null
  }
  if (chartDialogRef.value) {
    const chart = echarts.getInstanceByDom(chartDialogRef.value)
    if (chart) chart.dispose()
  }
})
</script>

<style scoped>
/* ===== 页面布局 ===== */
/* 新版外壳：工作台改为全宽画布（去掉悬浮卡片外壳），内容仍在居中轨道内 */
.ax-page {
  height: 100%;
  background: var(--bg-page, #F5F7FB);
  overflow: hidden;
  font-family: var(--font-sans, 'Microsoft YaHei UI', 'Microsoft YaHei', 'PingFang SC', sans-serif);
  font-size: 14px;
  color: var(--text-title);
  padding: 0;
  box-sizing: border-box;
  --ax-content-width: 960px;
  --ax-content-gutter: 24px;
}

.ax-page :is(button, div, span) {
  transition:
    color 0.2s cubic-bezier(0.4, 0, 0.2, 1),
    background-color 0.2s cubic-bezier(0.4, 0, 0.2, 1),
    border-color 0.2s cubic-bezier(0.4, 0, 0.2, 1),
    opacity 0.2s cubic-bezier(0.4, 0, 0.2, 1),
    box-shadow 0.2s cubic-bezier(0.4, 0, 0.2, 1),
    transform 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.ax-shell {
  height: 100%;
  min-height: 0;
  display: flex;
  flex-direction: column;
}

.ax-workspace {
  flex: 1;
  min-height: 0;
  display: flex;
  overflow: hidden;
  gap: 0;
  border: 0;
  border-radius: 0;
  background: #FFFFFF;
  box-shadow: none;
  backdrop-filter: none;
}

.ax-workspace.is-detail-hidden {
  max-width: none;
  width: 100%;
  margin: 0 auto;
}

/* ===== 对话区 ===== */
.ax-chat-panel {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  background: #FFFFFF;
  border-radius: 0;
}

.ax-chat-panel.is-detail-hidden {
  max-width: none;
  width: 100%;
  margin: 0 auto;
  border-radius: 0;
}

.ax-content-track {
  width: min(100% - calc(var(--ax-content-gutter) * 2), var(--ax-content-width));
  max-width: var(--ax-content-width);
  margin-left: auto;
  margin-right: auto;
  box-sizing: border-box;
}

.ax-header-track {
  flex: 0 0 auto;
}

.ax-header-track :deep(.ax-header) {
  width: 100%;
  padding-left: 0;
  padding-right: 0;
}

.ax-chat-content {
  flex: 1 0 auto;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.ax-composer-track {
  flex: 0 0 auto;
  /* 贴底通栏：突破 960px 居中轨道，dock 背景/分隔线全宽，内容内部限宽 */
  width: calc(100% - 80px);
  max-width: 1120px;
  padding: 0;
}

/* 只读视图提示条 */
.ax-readonly-banner {
  flex: 0 0 auto;
  padding: 12px 20px;
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 13.5px;
  line-height: 1.5;
  cursor: pointer;
  margin: 0 20px 12px;
  border-radius: 4px;
  transition: all 0.2s ease;
}

.ax-readonly-banner:hover {
  transform: translateY(-1px);
}

.ax-readonly-banner.banner-running {
  background: linear-gradient(90deg, rgba(29, 78, 216, 0.06) 0%, rgba(29, 78, 216, 0.02) 100%);
  border-left: 4px solid #1d4ed8;
  color: #C41E24;
  box-shadow: 0 3px 10px rgba(29, 78, 216, 0.08);
}

.ax-readonly-banner.banner-running:hover {
  background: linear-gradient(90deg, rgba(29, 78, 216, 0.1) 0%, rgba(29, 78, 216, 0.04) 100%);
  box-shadow: 0 4px 14px rgba(29, 78, 216, 0.14);
}

.ax-readonly-banner.banner-completed {
  background: linear-gradient(90deg, rgba(82, 196, 26, 0.06) 0%, rgba(82, 196, 26, 0.02) 100%);
  border-left: 4px solid #52c41a;
  color: #389e0d;
  box-shadow: 0 3px 10px rgba(82, 196, 26, 0.08);
}

.ax-readonly-banner.banner-completed:hover {
  background: linear-gradient(90deg, rgba(82, 196, 26, 0.1) 0%, rgba(82, 196, 26, 0.04) 100%);
  box-shadow: 0 4px 14px rgba(82, 196, 26, 0.14);
}

.ax-readonly-banner.banner-pending_confirmation {
  background: linear-gradient(90deg, rgba(250, 173, 20, 0.06) 0%, rgba(250, 173, 20, 0.02) 100%);
  border-left: 4px solid #faad14;
  color: #d48806;
  box-shadow: 0 3px 10px rgba(250, 173, 20, 0.08);
}

.ax-readonly-banner.banner-pending_confirmation:hover {
  background: linear-gradient(90deg, rgba(250, 173, 20, 0.1) 0%, rgba(250, 173, 20, 0.04) 100%);
  box-shadow: 0 4px 14px rgba(250, 173, 20, 0.14);
}

.ax-readonly-banner.banner-failed {
  background: linear-gradient(90deg, rgba(255, 77, 79, 0.06) 0%, rgba(255, 77, 79, 0.02) 100%);
  border-left: 4px solid #ff4d4f;
  color: #cf1322;
  box-shadow: 0 3px 10px rgba(255, 77, 79, 0.08);
}

.ax-readonly-banner.banner-failed:hover {
  background: linear-gradient(90deg, rgba(255, 77, 79, 0.1) 0%, rgba(255, 77, 79, 0.04) 100%);
  box-shadow: 0 4px 14px rgba(255, 77, 79, 0.14);
}

.ax-spin-ring-small {
  position: relative;
  width: 16px;
  height: 16px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.ax-spin-ring-track-small {
  position: absolute;
  inset: 0;
  border-radius: 50%;
  border: 2px solid currentColor;
  opacity: 0.25;
}
.ax-spin-ring-bar-small {
  position: absolute;
  inset: 0;
  border-radius: 50%;
  border: 2px solid transparent;
  border-top-color: currentColor;
  animation: ax-ring-spin-small 0.8s linear infinite;
}
@keyframes ax-ring-spin-small {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.ax-readonly-banner-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  flex-shrink: 0;
}

.ax-readonly-banner-text {
  flex: 1;
  line-height: 1.4;
}

/* 聊天区 */
.ax-chat-body {
  flex: 1;
  overflow-y: auto;
  padding: 0 0 10px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  background: #FFFFFF;
}

.ax-chat-panel.is-detail-hidden .ax-chat-body {
  padding-left: 0;
  padding-right: 0;
}

/* 消息 */
.ax-msg-list {
  display: flex;
  flex-direction: column;
  gap: 0;
  width: 100%;
}
.ax-msg-wrap {
  animation: ax-fadein 0.3s ease-out;
  width: 100%;
  max-width: var(--ax-content-width);
}

.ax-chat-panel.is-detail-hidden .ax-msg-list {
  width: 100%;
  align-items: stretch;
}

.ax-chat-panel.is-detail-hidden .ax-msg-wrap {
  width: 100%;
  max-width: var(--ax-content-width);
}

.ax-chat-panel :deep(.cmp) {
  width: 100%;
  max-width: none;
  margin: 0;
}

/* dock 通栏，内容与消息阅读区对齐（960px 居中） */
.ax-chat-panel :deep(.cmp-dock) {
  padding-left: max(20px, calc((100% - var(--ax-content-width, 960px)) / 2));
  padding-right: max(20px, calc((100% - var(--ax-content-width, 960px)) / 2));
}
@keyframes ax-fadein {
  from { opacity: 0; transform: translateY(16px); }
  to { opacity: 1; transform: translateY(0); }
}

/* AI回复包装 */
.ax-ai-wrap {
  display: flex;
  flex-direction: column;
  gap: 14px;
  margin: 10px 0;
}
.ax-ai-meta {
  display: flex;
  align-items: center;
  gap: 12px;
}
.ax-ai-avatar {
  width: 40px;
  height: 40px;
  position: relative;
  overflow: visible;
  background: transparent;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  border: 0;
  box-shadow: 0 4px 12px rgba(29, 78, 216, 0.18);
  padding: 0;
}

.ax-ai-avatar::before {
  content: none;
}

.ax-ai-avatar::after {
  content: '';
  position: absolute;
  right: 1px;
  bottom: 1px;
  width: 9px;
  height: 9px;
  border-radius: 50%;
  background: #10B981;
  box-shadow:
    0 0 0 3px #FFFFFF,
    0 4px 9px rgba(16, 185, 129, 0.18);
}

.ax-ai-avatar-img {
  display: none;
}

.ax-ai-avatar-svg {
  width: 40px;
  height: 40px;
  display: block;
}
.ax-ai-name {
  font-size: 14.5px;
  font-weight: 700;
  color: #1E293B;
  letter-spacing: 0.2px;
}
.ax-ai-cards {
  display: flex;
  flex-direction: column;
  gap: 14px;
  padding-left: 52px;
  max-width: 900px;
}

.ax-chat-panel.is-detail-hidden .ax-ai-cards {
  max-width: 880px;
}

/* 通用卡片样式优化 */
.ax-card {
  background: #ffffff;
  border-radius: 6px;
  border: 1px solid rgba(226, 232, 240, 0.8);
  box-shadow: 
    0 1px 3px rgba(15, 23, 42, 0.04),
    0 4px 12px rgba(15, 23, 42, 0.03);
  transition: box-shadow 0.2s ease, transform 0.2s ease;
}

.ax-card:hover {
  box-shadow: 
    0 2px 6px rgba(15, 23, 42, 0.05),
    0 8px 20px rgba(15, 23, 42, 0.06);
}

.ax-result-chain {
  display: flex;
  flex-direction: column;
  gap: 10px;
  width: 100%;
  padding-top: 14px;
  margin-top: 1px;
  border-top: 1px dashed rgba(17, 24, 39, 0.1);
  animation: ax-curtain-open 0.32s cubic-bezier(0.4, 0, 0.2, 1);
  transform-origin: top center;
}

.ax-result-chain > * {
  width: 100%;
}

.ax-result-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 10px;
  width: 100%;
  max-width: 720px;
  padding: 30px 24px;
  border-radius: 4px;
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.92) 0%, rgba(248, 249, 250, 0.88) 100%);
  border: 1px dashed rgba(17, 24, 39, 0.1);
  box-shadow: 0 16px 28px rgba(15, 23, 42, 0.04);
  text-align: center;
}

.ax-result-empty-icon {
  font-size: 32px;
  line-height: 1;
  opacity: 0.85;
}

.ax-result-empty-title {
  font-size: 16px;
  font-weight: 700;
  color: var(--text-title, #111827);
}

.ax-result-empty-desc {
  font-size: 13px;
  line-height: 1.75;
  color: var(--text-secondary, #6B7280);
  max-width: 520px;
}

.ax-chat-panel.is-detail-hidden .ax-result-chain,
.ax-chat-panel.is-detail-hidden .ax-inline-visuals,
.ax-chat-panel.is-detail-hidden .ax-flow-handoff,
.ax-chat-panel.is-detail-hidden .ax-confirm-card {
  max-width: 880px;
}

.ax-inline-visuals {
  display: flex;
  flex-direction: column;
  gap: 12px;
  width: 100%;
  max-width: 980px;
  padding: 14px;
  border-radius: 6px;
  border: 1px solid rgba(29, 78, 216, 0.1);
  background: linear-gradient(180deg, #eff6ff 0%, #ffffff 100%);
  box-shadow: 0 8px 18px rgba(0, 0, 0, 0.035);
}

.ax-inline-visuals.is-single {
  width: min(100%, 980px);
}

.ax-inline-visuals-head {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 8px;
}

.ax-inline-visuals-kicker {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.08em;
  color: #1d4ed8;
}

.ax-inline-visuals-title {
  margin-top: 5px;
  font-size: 16px;
  font-weight: 600;
  color: #111827;
}

.ax-inline-visuals-caption {
  margin-top: 4px;
  font-size: 11px;
  line-height: 1.65;
  color: #9CA3AF;
}

.ax-inline-visuals-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
}

.ax-inline-visuals-grid.is-single {
  grid-template-columns: minmax(0, 1fr);
  justify-content: start;
}

.ax-inline-visual-card {
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 12px;
  border-radius: 5px;
  border: 1px solid rgba(0, 0, 0, 0.08);
  background: #ffffff;
}

.ax-inline-visual-card-head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 10px;
}

.ax-inline-visual-card-title {
  font-size: 13px;
  font-weight: 600;
  color: #111827;
  line-height: 1.5;
}

.ax-inline-visual-card-subtitle {
  margin-top: 3px;
  font-size: 11px;
  color: #9CA3AF;
}

.ax-inline-visual-chart {
  height: 320px;
  border-radius: 5px;
  overflow: hidden;
  background: #fff;
  border: 1px solid rgba(0, 0, 0, 0.06);
}

.ax-inline-visuals-grid.is-single .ax-inline-visual-chart {
  height: 360px;
}

/* 加载动画 */
.ax-thinking-loading {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 14px 16px;
  background: #FFFFFF;
  border: 1px solid rgba(0, 0, 0, 0.08);
  border-radius: 6px;
  width: fit-content;
  min-width: 320px;
  box-shadow: 0 10px 24px rgba(0, 0, 0, 0.04);
}
.ax-dots {
  display: flex;
  gap: 4px;
}
.ax-dots span {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #1A1A1A;
  animation: dot-pulse 1.2s ease-in-out infinite;
}
.ax-dots span:nth-child(2) { animation-delay: 0.2s; }
.ax-dots span:nth-child(3) { animation-delay: 0.4s; }
@keyframes dot-pulse {
  0%, 80%, 100% { opacity: 0.3; transform: scale(0.8); }
  40% { opacity: 1; transform: scale(1); }
}
.ax-thinking-text {
  font-size: 13px;
  color: #6B7280;
}

/* 确认区 */
.ax-flow-handoff {
  width: 100%;
  padding: 12px 14px;
  border-radius: 6px;
  border: 1px solid rgba(0, 0, 0, 0.08);
  background: linear-gradient(180deg, #F2F5F4 0%, #ffffff 100%);
  box-shadow: 0 8px 18px rgba(0, 0, 0, 0.035);
}

.ax-flow-handoff-kicker {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #1A1A1A;
}

.ax-flow-handoff-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
}

.ax-flow-badge {
  flex: none;
  padding: 3px 8px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 700;
  border: 1px solid rgba(26, 26, 26, 0.12);
  background: #F3F4F6;
  color: #1A1A1A;
}

.ax-flow-badge.is-advanced {
  border-color: rgba(16, 185, 129, 0.22);
  background: #ecfdf5;
  color: #10B981;
}

.ax-flow-handoff-title {
  margin-top: 5px;
  font-size: 14px;
  font-weight: 600;
  line-height: 1.55;
  color: #111827;
}

.ax-flow-handoff-desc {
  margin-top: 5px;
  font-size: 12px;
  line-height: 1.65;
  color: #6B7280;
}

.ax-clarify-strip {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
  width: 100%;
  padding: 8px 12px;
  margin-bottom: 8px;
  border: 1px solid rgba(29, 78, 216, 0.18);
  border-radius: 4px;
  background: rgba(29, 78, 216, 0.04);
  font-size: 13px;
  line-height: 1.5;
}
.ax-clarify-icon {
  flex: none;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: rgba(29, 78, 216, 0.12);
  color: #1d4ed8;
  font-size: 12px;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}
.ax-clarify-text {
  color: #334155;
}
.ax-clarify-reason {
  display: block;
  color: #94a3b8;
  font-size: 12px;
}
.ax-clarify-chips {
  display: inline-flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-left: auto;
}
.ax-clarify-chip {
  border: 1px solid rgba(29, 78, 216, 0.35);
  background: #fff;
  color: #1d4ed8;
  border-radius: 999px;
  padding: 3px 12px;
  font-size: 12px;
  cursor: pointer;
  transition: background 0.15s ease, color 0.15s ease;
}
.ax-clarify-chip:hover:not(:disabled) {
  background: #1d4ed8;
  color: #fff;
}
.ax-clarify-chip:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
/* 纠正条/错字卡自由输入：推荐候选都不是时直接输入新问句 */
.ax-clarify-freeform {
  display: flex;
  align-items: center;
  gap: 8px;
  width: 100%;
}
.ax-clarify-freeform-inline {
  flex: 1;
  min-width: 220px;
  max-width: 360px;
  width: auto;
}
.ax-clarify-input {
  flex: 1;
  min-width: 0;
  height: 30px;
  padding: 0 10px;
  border: 1px solid #f3c2c2;
  border-radius: 6px;
  font-size: 13px;
  color: #333;
  background: #fff;
  outline: none;
}
.ax-clarify-input:focus {
  border-color: #d33030;
}
.ax-clarify-input:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
.ax-clarify-send {
  flex-shrink: 0;
  height: 30px;
  padding: 0 14px;
  border: none;
  border-radius: 6px;
  font-size: 13px;
  color: #fff;
  background: #d33030;
  cursor: pointer;
}
.ax-clarify-send:hover:not(:disabled) {
  background: #b92828;
}
.ax-clarify-send:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
/* 错字短路纠正卡（第 0 层快检）：细条的醒目放大版，只出此卡 */
.ax-early-clarify {
  display: flex;
  flex-direction: column;
  gap: 10px;
  width: 100%;
  padding: 14px 16px;
  margin-bottom: 8px;
  border: 1px solid rgba(29, 78, 216, 0.3);
  border-radius: 5px;
  background: rgba(29, 78, 216, 0.05);
}
.ax-early-clarify-head {
  display: flex;
  align-items: center;
  gap: 8px;
}
.ax-early-clarify-title {
  color: #334155;
  font-size: 14px;
  font-weight: 600;
  line-height: 1.5;
}
.ax-early-clarify-body {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
}
.ax-early-clarify-label {
  color: #64748b;
  font-size: 13px;
}
.ax-early-clarify-chip {
  padding: 5px 14px;
  font-size: 13px;
  font-weight: 600;
}
.ax-early-clarify-continue {
  align-self: flex-start;
  border: none;
  background: transparent;
  color: #94a3b8;
  font-size: 12px;
  padding: 2px 0;
  cursor: pointer;
  text-decoration: underline;
  text-underline-offset: 3px;
}
.ax-early-clarify-continue:hover:not(:disabled) {
  color: #1d4ed8;
}
.ax-early-clarify-continue:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
.ax-confirm-card {
  border: 1px solid rgba(0, 0, 0, 0.08);
  border-radius: 5px;
  background: #fff;
  width: 100%;
  padding: 12px;
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.04);
}
.ax-confirm-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 10px;
  flex-wrap: wrap;
}
.ax-confirm-badge {
  flex: 0 0 auto;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 11px;
  font-weight: 700;
  background: #FFFBEB;
  color: #F59E0B;
}
.ax-confirm-q {
  flex: 1 1 auto;
  font-size: 13px;
  color: var(--text-title);
  line-height: 1.5;
}
.ax-confirm-opts {
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.ax-confirm-list {
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.ax-confirm-row {
  display: flex;
  align-items: center;
  gap: 10px;
  width: 100%;
  min-height: 48px;
  text-align: left;
  padding: 7px 10px;
  border-radius: 4px;
  border: 1px solid rgba(0, 0, 0, 0.08);
  color: #111827;
  background: #fff;
  cursor: pointer;
  font-size: 13px;
  transition: all 0.12s;
}
.ax-confirm-row:hover {
  background: #F3F4F6;
  border-color: rgba(26, 26, 26, 0.2);
}
.ax-confirm-row-top {
  border-color: rgba(26, 26, 26, 0.24);
  background: #F3F4F6;
  font-weight: 600;
}
.ax-confirm-row-top .ax-confirm-rank {
  background: #1A1A1A;
  color: #fff;
}
.ax-confirm-row-top .ax-confirm-score {
  background: rgba(26, 26, 26, 0.1);
  color: #1A1A1A;
  font-weight: 700;
}
.ax-confirm-rank {
  flex: 0 0 auto;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 18px;
  height: 18px;
  border-radius: 5px;
  background: rgba(26, 26, 26, 0.06);
  color: #1A1A1A;
  font-size: 10px;
  font-weight: 700;
}
.ax-confirm-info {
  flex: 0 1 auto;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 2px;
}
.ax-confirm-row-label {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-size: 13px;
  font-weight: 600;
  color: #111827;
}
.ax-confirm-row-desc {
  font-size: 11px;
  line-height: 1.4;
  color: #9CA3AF;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.ax-confirm-recommended {
  flex: 0 0 auto;
  padding: 1px 5px;
  border-radius: 4px;
  background: #1d4ed8;
  color: #fff;
  font-size: 10px;
  font-weight: 600;
}
.ax-confirm-spacer {
  flex: 1 0 auto;
}
.ax-confirm-score {
  flex: 0 0 auto;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 48px;
  height: 20px;
  padding: 0 7px;
  border-radius: 999px;
  background: rgba(26, 26, 26, 0.06);
  color: #1A1A1A;
  font-size: 11px;
  font-weight: 600;
}
.ax-confirm-toggle {
  margin-top: 4px;
  width: 100%;
  height: 32px;
  border-radius: 4px;
  border: 1px dashed rgba(26, 26, 26, 0.2);
  background: #fff;
  color: #1A1A1A;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.15s;
}
.ax-confirm-toggle:hover {
  background: #F3F4F6;
}

.ax-confirm-freeform {
  margin-top: 10px;
  display: flex;
  align-items: flex-start;
  gap: 8px;
}

.ax-confirm-textarea {
  flex: 1 1 auto;
  min-width: 0;
  min-height: 36px;
  height: 36px;
  resize: none;
  padding: 8px 10px;
  border-radius: 4px;
  border: 1px solid rgba(0, 0, 0, 0.1);
  background: #fff;
  font-size: 12px;
  line-height: 1.5;
  color: #111827;
  outline: none;
  box-sizing: border-box;
}

.ax-confirm-textarea:focus {
  border-color: rgba(26, 26, 26, 0.35);
  box-shadow: 0 0 0 2px rgba(26, 26, 26, 0.06);
}

.ax-confirm-textarea::placeholder {
  color: #9CA3AF;
}

.ax-confirm-send {
  flex: 0 0 auto;
  height: 36px;
  padding: 0 14px;
  border-radius: 4px;
  border: none;
  background: #1d4ed8;
  color: #fff;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
}

.ax-confirm-send:disabled,
.ax-confirm-row:disabled,
.ax-confirm-toggle:disabled {
  opacity: 0.55;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.ax-confirm-submitted {
  max-width: 760px;
  padding: 14px 16px;
  border-radius: 6px;
  border: 1px solid rgba(0, 0, 0, 0.08);
  background: linear-gradient(180deg, #F2F5F4 0%, #ffffff 100%);
  box-shadow: 0 10px 24px rgba(0, 0, 0, 0.035);
}

.ax-confirm-submitted-head {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 6px;
}

.ax-confirm-submitted-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #1d4ed8;
  box-shadow: 0 0 0 5px rgba(29, 78, 216, 0.08);
}

.ax-confirm-submitted-title {
  font-size: 13px;
  font-weight: 700;
  color: #1d4ed8;
}

.ax-confirm-submitted-desc {
  font-size: 12px;
  line-height: 1.65;
  color: #6B7280;
}

/* 状态提示区 */
.ax-error-card,
.ax-cancel-card {
  display: flex;
  gap: 8px;
  align-items: center;
  padding: 12px 16px;
  border-radius: 6px;
  max-width: 760px;
}

.ax-error-card {
  background: #eff6ff;
  border: 1px solid #eff6ff;
  color: var(--error);
}

.ax-cancel-card {
  align-items: flex-start;
  position: relative;
  overflow: hidden;
  gap: 12px;
  padding: 14px 16px;
  background:
    linear-gradient(90deg, rgba(0, 0, 0, 0.035) 1px, transparent 1px),
    linear-gradient(180deg, rgba(0, 0, 0, 0.035) 1px, transparent 1px),
    radial-gradient(circle at 12% 18%, rgba(29, 78, 216, 0.16), transparent 30%),
    linear-gradient(135deg, #F2F5F4 0%, #eff6ff 54%, #eff6ff 100%);
  background-size: 18px 18px, 18px 18px, auto, auto;
  border: 1px solid rgba(29, 78, 216, 0.22);
  color: #111827;
  box-shadow:
    0 12px 28px rgba(29, 78, 216, 0.08),
    inset 0 1px 0 rgba(255, 255, 255, 0.84);
}

.ax-cancel-card::before {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: inherit;
  border-left: 3px solid #1d4ed8;
  pointer-events: none;
}

.ax-cancel-card::after {
  content: '';
  position: absolute;
  right: 14px;
  top: 13px;
  width: 58px;
  height: 16px;
  border-top: 1px solid rgba(29, 78, 216, 0.2);
  border-right: 1px solid rgba(29, 78, 216, 0.42);
  transform: skewX(-24deg);
  pointer-events: none;
}

.ax-cancel-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 30px;
  height: 30px;
  position: relative;
  margin-top: 2px;
  border-radius: 50%;
  background:
    radial-gradient(circle, rgba(255, 255, 255, 0.96) 0 30%, transparent 31%),
    conic-gradient(from 210deg, rgba(29, 78, 216, 0.18), rgba(29, 78, 216, 0.85), rgba(29, 78, 216, 0.18));
  box-shadow:
    0 0 0 4px rgba(29, 78, 216, 0.06),
    0 0 18px rgba(29, 78, 216, 0.28);
  flex: 0 0 auto;
}

.ax-cancel-icon::before,
.ax-cancel-icon::after {
  content: '';
  position: absolute;
  background: #1d4ed8;
  border-radius: 999px;
}

.ax-cancel-icon::before {
  width: 14px;
  height: 2px;
  transform: rotate(45deg);
}

.ax-cancel-icon::after {
  width: 14px;
  height: 2px;
  transform: rotate(-45deg);
}

.ax-cancel-icon-core {
  position: absolute;
  inset: 7px;
  border-radius: 50%;
  border: 1px solid rgba(29, 78, 216, 0.28);
}

.ax-cancel-copy {
  position: relative;
  z-index: 1;
  min-width: 0;
}

.ax-cancel-kicker {
  margin-bottom: 3px;
  color: #1d4ed8;
  font-size: 10px;
  font-weight: 800;
  letter-spacing: 0.08em;
}

.ax-cancel-title {
  font-size: 14px;
  font-weight: 780;
  color: #111827;
}

.ax-cancel-desc {
  margin-top: 3px;
  font-size: 12px;
  line-height: 1.6;
  color: #6B7280;
}

.ax-link-btn {
  background: none;
  border: none;
  color: #1A1A1A;
  cursor: pointer;
  font-size: 12px;
  padding: 4px 5px;
}

.ax-link-btn:hover {
  text-decoration: underline;
}

.ax-link-btn.danger {
  color: #1d4ed8;
}

/* ===== 右侧面板 ===== */
.ax-detail-panel {
  width: clamp(360px, 34vw, 440px);
  max-width: 42vw;
  height: 100%;
  max-height: 100%;
  min-height: 0;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  border-left: 1px solid rgba(17, 24, 39, 0.07);
  background: #FFFFFF;
  box-shadow: none;
  flex-shrink: 0;
}
/* 新版右侧容器：ReasoningPanel（弹性占满）+ 侧栏报告（固定底部）纵向排列 */
.ax-detail-panel-container {
  width: clamp(360px, 34vw, 440px);
  max-width: 42vw;
  height: 100%;
  max-height: 100%;
  min-height: 0;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  background: #FFFFFF;
  flex-shrink: 0;
}
/* 推理面板优先占满剩余空间，保留最小可用高度；内容在其内部滚动 */
.ax-detail-panel-container > .reasoning-panel {
  flex: 1 1 auto;
  min-height: 260px;
}
/* 侧栏报告封顶 45% 高度并内部滚动，避免长报告把推理面板挤成 0 */
.ax-detail-panel-container > .ax-side-report {
  flex: 0 1 auto;
  min-height: 0;
  max-height: 45%;
  overflow-y: auto;
  overscroll-behavior: contain;
}
.ax-panel-header {
  padding: 28px 28px 24px;
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
  border-bottom: 1px solid rgba(17, 24, 39, 0.07);
  background: #FFFFFF;
  flex-shrink: 0;
}
.ax-panel-heading {
  display: flex;
  flex-direction: column;
  gap: 12px;
  min-width: 0;
}
.ax-panel-eyebrow {
  font-size: 18px;
  font-weight: 800;
  letter-spacing: 0;
  text-transform: none;
  color: #1d4ed8;
}
.ax-panel-title-row {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}
.ax-panel-title {
  font-size: 21px;
  font-weight: 800;
  color: #111827;
}
.ax-panel-state {
  display: inline-flex;
  align-items: center;
  height: 28px;
  padding: 0 12px;
  border-radius: 999px;
  font-size: 11px;
  font-weight: 700;
  background: rgba(17, 24, 39, 0.06);
  color: #6B7280;
  box-shadow: inset 0 0 0 1px rgba(17, 24, 39, 0.05);
}
.ax-panel-state.running {
  background: rgba(17, 24, 39, 0.88);
  color: rgba(255, 255, 255, 0.96);
}
.ax-panel-state.completed {
  background: rgba(16, 185, 129, 0.12);
  color: #059669;
}
.ax-panel-state.canceled {
  background: rgba(245, 158, 11, 0.12);
  color: #B45309;
}
.ax-panel-state.error {
  background: rgba(29, 78, 216, 0.1);
  color: #1d4ed8;
}
.ax-panel-state.waiting_confirmation {
  background: rgba(245, 158, 11, 0.12);
  color: #F59E0B;
}
.ax-panel-desc {
  margin: 0;
  font-size: 14px;
  line-height: 1.65;
  color: #7B8491;
  max-width: 360px;
}
.ax-panel-close {
  width: 38px;
  height: 38px;
  border-radius: 6px;
  border: 1px solid rgba(17, 24, 39, 0.06);
  background: rgba(255, 255, 255, 0.92);
  cursor: pointer;
  color: var(--text-muted);
  font-size: 20px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  box-shadow: none;
}

.ax-panel-close:hover {
  color: #1A1A1A;
  border-color: rgba(29, 78, 216, 0.14);
  background: rgba(255, 255, 255, 1);
}
.ax-panel-content {
  flex: 1;
  min-height: 0;
  overflow-y: auto;
  padding: 6px 0 14px;
  overscroll-behavior: contain;
}

/* 数据预览 */
.ax-preview {
  gap: 14px;
}

/* 汇总报告 */
.ax-report-view {
  padding: 0;
}
.ax-report-full {
  display: flex;
  flex-direction: column;
  gap: 14px;
}
.ax-kpi-shelf {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}
.ax-side-section-head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 10px;
}
.ax-side-dataset-name {
  margin-top: 4px;
  font-size: 14px;
  font-weight: 600;
  color: #111827;
}
.ax-side-meta {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
  justify-content: flex-end;
}
.ax-side-meta-chip {
  display: inline-flex;
  align-items: center;
  height: 22px;
  padding: 0 9px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.88);
  color: #6B7280;
  font-size: 10px;
  font-weight: 600;
  box-shadow: inset 0 0 0 1px rgba(17, 24, 39, 0.06);
}
.ax-kpi-card {
  flex: 1;
  min-width: 120px;
  border: 1px solid rgba(17, 24, 39, 0.08);
  border-radius: 6px;
  padding: 14px;
  text-align: center;
  background: linear-gradient(180deg, rgba(255, 255, 255, 1) 0%, rgba(251, 252, 253, 0.96) 100%);
  box-shadow:
    0 14px 24px rgba(15, 23, 42, 0.035),
    inset 0 1px 0 rgba(255, 255, 255, 0.92);
}

.ax-kpi-card.is-explained {
  min-height: 92px;
  padding: 14px 16px;
  text-align: left;
}

.ax-kpi-card.is-subject-metric {
  position: relative;
  overflow: hidden;
  border-color: var(--metric-accent-border);
  background: linear-gradient(180deg, var(--metric-accent-soft) 0%, #ffffff 72%);
}

.ax-kpi-card.is-subject-metric::before {
  content: '';
  position: absolute;
  inset: 0 auto 0 0;
  width: 4px;
  background: var(--metric-accent);
}

.ax-kpi-subject {
  margin-bottom: 4px;
  color: var(--metric-accent);
  font-size: 11px;
  font-weight: 800;
  line-height: 1.2;
}

.ax-kpi-card.is-subject-metric .ax-kpi-value {
  color: var(--metric-accent);
}

.ax-kpi-card.is-tone-good .ax-kpi-value {
  color: #10B981;
}

.ax-kpi-card.is-tone-warn .ax-kpi-value {
  color: #F59E0B;
}

.ax-kpi-card.is-tone-danger .ax-kpi-value {
  color: #1d4ed8;
}

.ax-kpi-value {
  font-size: 22px;
  font-weight: 800;
  color: rgba(17, 24, 39, 0.92);
  line-height: 1.2;
}
.ax-kpi-label {
  font-size: 12px;
  color: var(--text-muted);
  margin-top: 6px;
}

.ax-kpi-hint {
  margin-top: 8px;
  color: #6B7280;
  font-size: 11px;
  line-height: 1.55;
}
.ax-main-chart {
  height: 208px;
  border-radius: 6px;
  overflow: hidden;
  background: #fff;
  border: 1px solid rgba(17, 24, 39, 0.08);
}
.ax-insight-metric {
  min-height: 164px;
  border-radius: 6px;
  border: 1px solid rgba(17, 24, 39, 0.08);
  background: linear-gradient(180deg, #FFFFFF 0%, #F2F5F4 100%);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 18px;
}
.ax-insight-metric-value {
  font-size: 25px;
  line-height: 1.2;
  font-weight: 800;
  color: rgba(17, 24, 39, 0.92);
}
.ax-insight-metric-label {
  margin-top: 7px;
  font-size: 12px;
  color: #6B7280;
}
.ax-preview-table {
  border-radius: 6px;
  overflow: hidden;
  border: 1px solid rgba(17, 24, 39, 0.06);
}
.ax-report-md {
  font-size: 13px;
  line-height: 1.72;
  color: var(--text-title);
}
.ax-report-md :deep(h1),
.ax-report-md :deep(h2) {
  color: #111827;
  margin: 14px 0 7px;
}
.ax-report-md :deep(table) {
  width: 100%;
  border-collapse: collapse;
}
.ax-report-md :deep(td),
.ax-report-md :deep(th) {
  border: 1px solid var(--border);
  padding: 5px 8px;
  font-size: 12px;
  text-align: left;
  vertical-align: top;
}
.ax-report-md :deep(th) {
  background: var(--bg-muted);
  font-weight: 600;
}
.ax-download-row {
  text-align: center;
  padding-top: 2px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
}
.ax-primary-btn {
  height: 34px;
  padding: 0 16px;
  border-radius: 999px;
  background: rgba(17, 24, 39, 0.9);
  color: #fff;
  border: 1px solid rgba(17, 24, 39, 0.14);
  cursor: pointer;
  font-size: 12px;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 7px;
  transition: all 0.22s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow:
    0 10px 18px rgba(15, 23, 42, 0.12),
    inset 0 1px 0 rgba(255, 255, 255, 0.14);
}
.ax-primary-btn:hover {
  transform: translateY(-1px) scale(1.01);
  box-shadow:
    0 12px 22px rgba(15, 23, 42, 0.14),
    inset 0 1px 0 rgba(255, 255, 255, 0.18);
}

.ax-primary-btn:active {
  transform: scale(0.94);
}

.ax-secondary-btn,
.ax-ghost-btn {
  height: 34px;
  padding: 0 15px;
  border-radius: 999px;
  border: 1px solid rgba(0, 0, 0, 0.08);
  background: rgba(255, 255, 255, 0.92);
  color: #6B7280;
  cursor: pointer;
  font-size: 12px;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 7px;
  transition: all 0.22s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
}

.ax-btn-label {
  display: inline-flex;
  align-items: center;
  white-space: nowrap;
}

.ax-btn-icon {
  position: relative;
  width: 14px;
  height: 14px;
  display: inline-flex;
  flex-shrink: 0;
}

.ax-btn-icon-stem,
.ax-btn-icon-head,
.ax-btn-icon-tray {
  position: absolute;
  box-sizing: border-box;
}

.ax-btn-icon-stem {
  left: 6px;
  top: 1px;
  width: 2px;
  height: 6px;
  background: currentColor;
  border-radius: 999px;
}

.ax-btn-icon-head {
  left: 4px;
  top: 5px;
  width: 6px;
  height: 6px;
  border-right: 2px solid currentColor;
  border-bottom: 2px solid currentColor;
  transform: rotate(45deg);
}

.ax-btn-icon-tray {
  position: absolute;
  left: 1px;
  right: 1px;
  bottom: 0;
  height: 4px;
  border: 2px solid currentColor;
  border-top: none;
  border-radius: 0 0 3px 3px;
  box-sizing: border-box;
}

.ax-secondary-btn:hover,
.ax-ghost-btn:hover {
  border-color: rgba(26, 26, 26, 0.14);
  background: rgba(243, 244, 246, 0.92);
  color: #1A1A1A;
  transform: translateY(-1px);
  box-shadow: 0 8px 18px rgba(0, 0, 0, 0.05);
}

.ax-secondary-btn:active,
.ax-ghost-btn:active,
.ax-panel-close:active,
.ax-link-btn:active,
.ax-confirm-row:active {
  transform: scale(0.985);
}

.ax-side-report {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin: 0 14px 14px;
  padding: 14px;
  border: 1px solid rgba(0, 0, 0, 0.08);
  border-radius: 6px;
  background: linear-gradient(180deg, #F2F5F4 0%, #ffffff 100%);
}

.ax-side-report-head {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.ax-side-report-titlebar {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
}

.ax-side-fullscreen-btn {
  flex-shrink: 0;
  height: 32px;
  padding: 0 12px;
}

.ax-side-confidence {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 4px;
}

.ax-side-confidence-chip {
  display: inline-flex;
  align-items: center;
  height: 24px;
  padding: 0 10px;
  border-radius: 999px;
  font-size: 11px;
  font-weight: 600;
  border: 1px solid rgba(0, 0, 0, 0.08);
  background: #ffffff;
  color: #6B7280;
}

.ax-side-confidence-chip.is-success {
  background: #ECFDF5;
  border-color: rgba(16, 185, 129, 0.16);
  color: #10B981;
}

.ax-side-confidence-chip.is-info {
  background: #F3F4F6;
  border-color: rgba(26, 26, 26, 0.1);
  color: #1A1A1A;
}

.ax-side-confidence-chip.is-warning {
  background: #FFFBEB;
  border-color: rgba(245, 158, 11, 0.16);
  color: #F59E0B;
}

.ax-route-decision {
  margin-top: 4px;
  padding: 8px 10px;
  border-radius: 4px;
  border: 1px solid rgba(0, 0, 0, 0.08);
  background: #F2F5F4;
  color: #6B7280;
  font-size: 12px;
  line-height: 1.6;
}

.ax-route-review-note {
  margin: 0;
  padding: 8px 10px;
  border-radius: 4px;
  background: rgba(26, 26, 26, 0.04);
  color: #6B7280;
  font-size: 12px;
  line-height: 1.55;
}

.ax-side-report-kicker {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #1A1A1A;
}

.ax-side-report-title {
  margin: 0;
  font-size: 16px;
  line-height: 1.4;
  color: #111827;
}

.ax-side-report-desc {
  margin: 0;
  font-size: 12px;
  line-height: 1.65;
  color: #6B7280;
}

.ax-business-report {
  gap: 12px;
}

.ax-management-narrative {
  display: grid;
  gap: 10px;
}

.ax-management-narrative.is-dialog {
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
}

.ax-management-narrative.is-single-focus,
.ax-management-narrative.is-dialog.is-single-focus {
  grid-template-columns: minmax(0, 1fr);
}

.ax-management-narrative-card {
  padding: 12px 14px;
  border: 1px solid rgba(0, 0, 0, 0.06);
  border-radius: 6px;
  background: linear-gradient(180deg, #ffffff 0%, #F2F5F4 100%);
}

.ax-management-narrative.is-single-focus .ax-management-narrative-card {
  border-radius: 4px;
  background: #ffffff;
}

.ax-management-narrative-title {
  margin-bottom: 8px;
  color: #111827;
  font-size: 13px;
  font-weight: 800;
  line-height: 1.35;
}

.ax-management-narrative.is-single-focus .ax-management-narrative-title {
  font-size: 14px;
}

.ax-management-narrative-body {
  color: #374151;
  font-size: 13px;
  line-height: 1.75;
}

.ax-management-narrative-body :deep(p) {
  margin: 0 0 8px;
}

.ax-management-narrative-body :deep(ul) {
  margin: 0;
  padding-left: 18px;
}

.ax-management-narrative-body :deep(li) {
  margin: 4px 0;
}

.ax-business-summary {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
}

.ax-business-summary-text {
  margin: 6px 0 0;
  font-size: 13px;
  line-height: 1.75;
  color: #111827;
}

.ax-filter-answer-card {
  padding: 14px;
  border: 1px solid rgba(0, 0, 0, 0.08);
  border-radius: 4px;
  background: linear-gradient(180deg, #F2F5F4, rgba(255, 255, 255, 0.96));
  box-shadow: 0 10px 24px rgba(0, 0, 0, 0.04);
}

.ax-filter-answer-head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
}

.ax-filter-answer-list {
  display: grid;
  gap: 8px;
  margin-top: 12px;
}

.ax-filter-answer-row {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto auto;
  align-items: center;
  gap: 10px;
  width: 100%;
  min-height: 38px;
  padding: 8px 10px;
  border: 1px solid rgba(0, 0, 0, 0.22);
  border-radius: 4px;
  background: rgba(255, 255, 255, 0.82);
  color: #111827;
  text-align: left;
  cursor: pointer;
}

.ax-filter-answer-row:hover {
  border-color: rgba(26, 26, 26, 0.2);
  background: #fff;
}

.ax-filter-answer-name {
  min-width: 0;
  overflow: hidden;
  font-size: 13px;
  font-weight: 800;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.ax-filter-answer-metric {
  color: #1A1A1A;
  font-size: 12px;
  font-weight: 800;
  white-space: nowrap;
}

.ax-business-risk-pill,
.ax-office-rate {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 24px;
  padding: 0 9px;
  border-radius: 999px;
  font-size: 11px;
  font-weight: 700;
  white-space: nowrap;
}

.ax-business-risk-pill.good,
.ax-office-rate.good {
  color: #10B981;
  background: #ECFDF5;
}

.ax-business-risk-pill.warn,
.ax-office-rate.warn {
  color: #F59E0B;
  background: #FFFBEB;
}

.ax-business-risk-pill.danger,
.ax-office-rate.danger {
  color: #1d4ed8;
  background: #eff6ff;
}

.ax-business-risk-pill.neutral,
.ax-office-rate.neutral {
  color: #6B7280;
  background: #F3F4F6;
}

.ax-office-rate {
  flex-direction: column;
  align-items: flex-end;
  gap: 2px;
  line-height: 1.1;
}

.ax-office-rate small {
  font-size: 9px;
  font-weight: 600;
  color: currentColor;
  opacity: 0.8;
}

.ax-office-tag {
  margin-left: 6px;
  color: #6B7280;
  font-size: 11px;
  font-weight: 700;
}

.ax-kpi-shelf-compact .ax-kpi-card {
  min-width: calc(50% - 4px);
  padding: 10px;
}

.ax-office-overview-card {
  padding: 12px;
  border: 1px solid rgba(0, 0, 0, 0.08);
  border-radius: 5px;
  background: #ffffff;
}

.ax-office-overview-head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 10px;
}

.ax-office-overview-chart {
  width: 100%;
  height: 320px;
  overflow: hidden;
}

.ax-office-overview-dialog {
  margin-bottom: 16px;
}

.ax-office-card-list,
.ax-office-report-grid {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.ax-office-report-grid {
  gap: 14px;
}

.ax-office-card {
  border: 1px solid var(--office-accent-border, rgba(0, 0, 0, 0.08));
  border-radius: 5px;
  background: #ffffff;
  overflow: hidden;
}

.ax-office-card-dialog {
  border-radius: 6px;
  border-color: var(--office-accent-border, rgba(0, 0, 0, 0.08));
}

.ax-office-card-head {
  width: 100%;
  min-height: 58px;
  border: none;
  background: #FFFFFF;
  padding: 12px;
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
  text-align: left;
  cursor: pointer;
}

.ax-office-card .ax-office-card-head {
  background: linear-gradient(90deg, var(--office-accent-soft, #FFFFFF) 0%, #FFFFFF 72%);
  border-left: 4px solid var(--office-accent, transparent);
}

.ax-office-card-dialog .ax-office-card-head {
  background: linear-gradient(90deg, var(--office-accent-soft, #FFFFFF) 0%, #FFFFFF 72%);
  border-left: 4px solid var(--office-accent, transparent);
}

.ax-office-card-head:hover {
  background: #F2F5F4;
}

.ax-office-head-main {
  flex: 1 1 auto;
  min-width: 0;
}

.ax-office-head-actions {
  flex: 0 0 auto;
  display: inline-flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-end;
  gap: 8px;
  min-width: 0;
}

.ax-office-leaf-pill {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 24px;
  padding: 0 10px;
  border-radius: 999px;
  border: 1px solid rgba(0, 0, 0, 0.08);
  background: rgba(255, 255, 255, 0.92);
  color: #111827;
  font-size: 12px;
  font-weight: 600;
  white-space: nowrap;
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.75);
}

.ax-office-drill-toggle {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
  min-width: 48px;
  min-height: 24px;
  padding: 0 8px;
  border: 1px solid rgba(0, 0, 0, 0.08);
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.62);
  color: #6B7280;
  line-height: 1;
  opacity: 0.82;
  transition: border-color 0.18s ease, color 0.18s ease, background 0.18s ease, opacity 0.18s ease;
}

.ax-office-card-head:hover .ax-office-drill-toggle,
.ax-rep-drill-head:hover .ax-office-drill-toggle,
.ax-office-drill-toggle.is-open {
  border-color: var(--office-accent-border, rgba(29, 78, 216, 0.18));
  background: #ffffff;
  color: var(--office-accent, #1d4ed8);
  opacity: 1;
}

.ax-office-drill-toggle span {
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-size: 11px;
  font-weight: 800;
}

.ax-office-drill-toggle i {
  width: 6px;
  height: 6px;
  margin-top: -2px;
  border-right: 2px solid currentColor;
  border-bottom: 2px solid currentColor;
  transform: rotate(45deg);
  transition: transform 0.18s ease;
}

.ax-office-drill-toggle.is-open {
  background: var(--office-accent-soft, #F2F5F4);
}

.ax-office-drill-toggle.is-open i {
  margin-top: 2px;
  transform: rotate(225deg);
}

.ax-office-drill-toggle.is-small {
  min-width: 54px;
  min-height: 22px;
  padding: 0 7px;
}

.ax-office-drill-toggle.is-small span {
  font-size: 10px;
}

.ax-office-card .ax-office-card-head:hover {
  background: linear-gradient(90deg, var(--office-accent-soft, #F2F5F4) 0%, #F2F5F4 72%);
}

.ax-office-card-dialog .ax-office-card-head:hover {
  background: linear-gradient(90deg, var(--office-accent-soft, #F2F5F4) 0%, #F2F5F4 72%);
}

.ax-office-name {
  font-size: 14px;
  line-height: 1.4;
  font-weight: 700;
  color: #111827;
}

.ax-office-subtitle {
  margin-top: 4px;
  font-size: 11px;
  line-height: 1.45;
  color: #9CA3AF;
}

.ax-office-kpis {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 8px;
  padding: 10px 12px 0;
}

.ax-office-kpis span {
  min-width: 0;
  padding: 7px 8px;
  border-radius: 4px;
  background: #F2F5F4;
  color: #6B7280;
  font-size: 11px;
  line-height: 1.45;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.ax-office-copy,
.ax-chart-copy {
  margin: 0;
  color: #6B7280;
  font-size: 12px;
  line-height: 1.75;
}

.ax-office-copy {
  padding: 10px 12px 12px;
}

.ax-office-drill {
  margin: 0 12px 12px;
  position: relative;
  padding: 12px 0 0 14px;
  border-top: 1px dashed rgba(0, 0, 0, 0.1);
}

.ax-office-drill::before {
  content: '';
  position: absolute;
  left: 2px;
  top: 13px;
  bottom: 4px;
  width: 3px;
  border-radius: 999px;
  background: var(--office-accent-soft, rgba(29, 78, 216, 0.12));
  border: 1px solid var(--office-accent-border, rgba(29, 78, 216, 0.16));
}

.ax-drill-path {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  min-height: 26px;
  padding: 0 10px;
  border-radius: 999px;
  background: var(--office-accent-soft, #F2F5F4);
  color: #6B7280;
  font-size: 12px;
  font-weight: 700;
}

.ax-drill-path i {
  width: 18px;
  height: 1px;
  background: var(--office-accent, #1d4ed8);
  position: relative;
}

.ax-drill-path i::after {
  content: '';
  position: absolute;
  right: -1px;
  top: -3px;
  width: 6px;
  height: 6px;
  border-top: 1px solid var(--office-accent, #1d4ed8);
  border-right: 1px solid var(--office-accent, #1d4ed8);
  transform: rotate(45deg);
}

.ax-drill-path strong {
  color: var(--office-accent, #1d4ed8);
}

.ax-drill-insight-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 8px;
  margin-top: 10px;
}

.ax-drill-insight-card {
  min-width: 0;
  padding: 9px 10px;
  border-radius: 4px;
  border: 1px solid rgba(0, 0, 0, 0.08);
  background: #ffffff;
}

.ax-drill-insight-card span {
  display: block;
  margin-bottom: 4px;
  color: #9CA3AF;
  font-size: 11px;
  font-weight: 700;
}

.ax-drill-insight-card strong {
  display: block;
  color: #111827;
  font-size: 13px;
  line-height: 1.35;
}

.ax-drill-insight-card.is-good {
  border-color: rgba(16, 185, 129, 0.16);
  background: #ECFDF5;
}

.ax-drill-insight-card.is-risk {
  border-color: rgba(29, 78, 216, 0.14);
  background: #eff6ff;
}

.ax-chart-copy-drill {
  margin-top: 10px;
  padding: 8px 10px;
  border-radius: 4px;
  background: #FFFFFF;
}

.ax-drill-table-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  margin-bottom: -4px;
  color: #111827;
}

.ax-drill-table-head span {
  font-size: 13px;
  font-weight: 800;
}

.ax-drill-table-head small {
  color: #9CA3AF;
  font-size: 11px;
  font-weight: 500;
}

.ax-office-drill-actions {
  display: flex;
  justify-content: flex-end;
  margin: 8px 0;
}

.ax-office-chart-open {
  height: 28px;
  padding: 0 10px;
  font-size: 11px;
}

.ax-office-chart {
  width: 100%;
  height: 260px;
  overflow: hidden;
  border-radius: 4px;
  border: 1px solid rgba(0, 0, 0, 0.08);
  background: #fff;
}

.ax-office-empty-drill {
  margin-top: 8px;
  padding: 14px;
  border: 1px dashed rgba(29, 78, 216, 0.28);
  border-radius: 5px;
  background: linear-gradient(180deg, #F2F5F4 0%, #ffffff 100%);
  color: #6B7280;
  font-size: 12px;
  line-height: 1.7;
}

.ax-office-chart-dialog {
  height: 320px;
}

.ax-office-detail-wrap {
  display: grid;
  grid-template-columns: minmax(0, 1fr);
  gap: 12px;
  margin-top: 10px;
}

.ax-office-detail-wrap.is-dialog {
  grid-template-columns: minmax(0, 1fr);
}

.ax-office-detail-table {
  overflow: hidden;
  border: 1px solid rgba(0, 0, 0, 0.08);
  border-radius: 4px;
  background: #ffffff;
}

.ax-office-detail-row {
  display: grid;
  grid-template-columns: minmax(82px, 1fr) minmax(118px, 1.12fr) minmax(78px, 0.78fr) minmax(66px, 0.64fr) minmax(124px, 1fr) minmax(74px, 0.74fr);
  gap: 8px;
  align-items: center;
  min-height: 36px;
  padding: 7px 10px;
  color: #374151;
  font-size: 11px;
  line-height: 1.35;
}

.ax-office-detail-row:nth-child(odd):not(.is-head) {
  background: #F2F5F4;
}

.ax-office-detail-row.is-head {
  min-height: 32px;
  color: #9CA3AF;
  background: #F2F5F4;
  font-weight: 700;
}

.ax-detail-name {
  color: #111827;
  font-weight: 700;
}

.ax-detail-rate,
.ax-detail-tag {
  font-weight: 700;
}

.ax-detail-tag {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 22px;
  width: fit-content;
  max-width: 100%;
  padding: 0 8px;
  border-radius: 999px;
  background: #F3F4F6;
  line-height: 1;
}

.ax-detail-progress {
  min-width: 0;
}

.ax-detail-rate.good,
.ax-detail-tag.good {
  color: #10B981;
  background: #ECFDF5;
}

.ax-detail-rate.warn,
.ax-detail-tag.warn {
  color: #F59E0B;
  background: #FFFBEB;
}

.ax-detail-rate.danger,
.ax-detail-tag.danger {
  color: #1d4ed8;
  background: #eff6ff;
}

.ax-office-bars {
  display: grid;
  gap: 8px;
  align-content: start;
}

.ax-office-bar-row {
  display: grid;
  grid-template-columns: minmax(54px, 74px) minmax(0, 1fr) minmax(48px, 64px);
  gap: 8px;
  align-items: center;
  color: #6B7280;
  font-size: 11px;
  line-height: 1.35;
}

.ax-office-bar-row span {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.ax-office-bar-row strong {
  color: #111827;
  font-size: 11px;
  text-align: right;
}

.ax-office-bar-row.is-gap {
  margin-top: -2px;
}

.ax-office-bar-track {
  display: block;
  position: relative;
  height: 8px;
  width: 100%;
  overflow: hidden;
  border-radius: 999px;
  background: #F3F4F6;
}

.ax-office-bar-track i,
.ax-office-bar-track b {
  position: absolute;
  inset: 0 auto 0 0;
  min-width: 2px;
  border-radius: inherit;
}

.ax-office-bar-track .is-rate.good {
  background: #10B981;
}

.ax-office-bar-track .is-rate.warn {
  background: #F59E0B;
}

.ax-office-bar-track .is-rate.danger {
  background: #1d4ed8;
}

.ax-office-bar-track .is-gap {
  background: #F59E0B;
}

.ax-compare-matrix {
  overflow: hidden;
  border: 1px solid rgba(0, 0, 0, 0.08);
  border-radius: 4px;
  background: #ffffff;
}

.ax-compare-row {
  position: relative;
  width: 100%;
  display: grid;
  grid-template-columns: minmax(110px, 1.05fr) minmax(88px, 0.8fr) minmax(88px, 0.8fr) minmax(88px, 0.8fr) minmax(70px, 0.65fr) minmax(220px, 1.4fr) minmax(82px, 0.75fr);
  gap: 10px;
  align-items: center;
  min-height: 44px;
  padding: 9px 12px;
  border: 0;
  border-bottom: 1px solid rgba(0, 0, 0, 0.06);
  background: transparent;
  color: #374151;
  font-size: 12px;
  line-height: 1.35;
  text-align: left;
}

.ax-compare-row:not(.is-head) {
  background: linear-gradient(90deg, var(--office-accent-soft, transparent) 0%, #ffffff 46%);
}

.ax-compare-row:not(.is-head)::before {
  content: '';
  position: absolute;
  inset: 0 auto 0 0;
  width: 4px;
  background: var(--office-accent);
}

.ax-compare-row:last-child {
  border-bottom: 0;
}

button.ax-compare-row {
  cursor: pointer;
}

button.ax-compare-row:hover {
  background: linear-gradient(90deg, var(--office-accent-soft, #F2F5F4) 0%, #F2F5F4 70%);
}

.ax-compare-row.is-head {
  min-height: 36px;
  color: #9CA3AF;
  background: #F2F5F4;
  font-weight: 700;
}

.ax-compare-row span {
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.ax-compare-matrix.is-compact .ax-compare-row {
  grid-template-columns: minmax(78px, 1fr) minmax(64px, 0.75fr) minmax(64px, 0.75fr) minmax(62px, 0.75fr) minmax(58px, 0.7fr) minmax(92px, 1fr) minmax(70px, 0.72fr);
  min-height: 38px;
  padding: 8px 10px;
  gap: 7px;
  font-size: 11px;
}

.ax-compare-matrix.is-compact .ax-compare-row.is-head {
  min-height: 32px;
}

.ax-compare-matrix.is-compact .ax-office-bar-track {
  height: 7px;
}

.ax-compare-row .ax-detail-name {
  color: var(--office-accent);
}

.ax-compare-row .ax-office-bar-track .is-rate {
  background: var(--office-accent);
}

.ax-rep-drill-list {
  grid-column: 1 / -1;
  display: grid;
  gap: 8px;
  margin-top: 2px;
  padding-top: 10px;
  border-top: 1px solid rgba(0, 0, 0, 0.08);
}

.ax-rep-drill-list.is-dialog {
  margin-top: 4px;
}

.ax-rep-drill-title {
  color: #6B7280;
  font-size: 12px;
  font-weight: 700;
}

.ax-rep-drill-card {
  overflow: hidden;
  border: 1px solid rgba(0, 0, 0, 0.08);
  border-radius: 4px;
  background: #FFFFFF;
}

.ax-rep-drill-head {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  padding: 9px 10px;
  border: 0;
  background: transparent;
  color: inherit;
  cursor: pointer;
  text-align: left;
}

.ax-rep-drill-head:hover {
  background: rgba(26, 26, 26, 0.04);
}

.ax-rep-drill-name {
  display: flex;
  align-items: center;
  gap: 4px;
  color: #111827;
  font-size: 13px;
  font-weight: 800;
}

.ax-rep-drill-subtitle {
  margin-top: 2px;
  color: #9CA3AF;
  font-size: 11px;
}

.ax-rep-drill-summary {
  margin: 0;
  padding: 0 10px 9px;
  color: #6B7280;
  font-size: 12px;
  line-height: 1.6;
}

.ax-rep-person-table {
  margin: 0 10px 10px;
}

@media (max-width: 900px) {
  .ax-office-detail-wrap,
  .ax-office-detail-wrap.is-dialog {
    grid-template-columns: minmax(0, 1fr);
  }

  .ax-drill-insight-grid {
    grid-template-columns: minmax(0, 1fr);
  }

  .ax-drill-table-head {
    align-items: flex-start;
    flex-direction: column;
    gap: 3px;
  }

  .ax-office-detail-table {
    overflow-x: auto;
  }

  .ax-office-detail-row {
    min-width: 760px;
  }

  .ax-compare-matrix {
    overflow-x: auto;
  }

  .ax-compare-row {
    min-width: 860px;
  }

  .ax-management-narrative.is-dialog {
    grid-template-columns: minmax(0, 1fr);
  }
}

.ax-wide-btn {
  width: 100%;
}

.ax-side-section {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 12px;
  border-radius: 6px;
  background: #ffffff;
  border: 1px solid rgba(0, 0, 0, 0.08);
}

.ax-side-section-title {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #9CA3AF;
}

/* 内嵌图表 */
.ax-chart-embed {
  height: 188px;
  margin: 6px 0;
  border-radius: 6px;
  overflow: hidden;
  background: #fff;
  border: 1px solid rgba(0, 0, 0, 0.08);
}

.ax-chart-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 6px;
}

/* mini 表格 */
.ax-mini-table-wrap {
  margin: 0;
}
.ax-mini-table {
  border-radius: 6px;
  overflow: hidden;
}
.ax-table-more {
  text-align: center;
  padding: 5px;
  font-size: 11px;
  color: var(--text-muted);
}

.ax-mini-table :deep(.el-table__header-wrapper th) {
  background: #F2F5F4;
  color: #6B7280;
  font-size: 11px;
  font-weight: 600;
  height: 34px;
  text-align: left;
}

.ax-mini-table :deep(.el-table__body-wrapper td) {
  font-size: 11px;
  color: #111827;
  text-align: left;
}

.ax-mini-table :deep(.el-table__row:nth-child(even) td) {
  background: #F2F5F4;
}

.ax-mini-table :deep(.el-table__inner-wrapper::before) {
  display: none;
}

.ax-preview :deep(.el-table__header-wrapper th) {
  background: #F2F5F4;
  color: #6B7280;
  font-size: 11px;
  font-weight: 600;
  height: 34px;
  text-align: left;
}

.ax-preview :deep(.el-table__body-wrapper td) {
  font-size: 11px;
  color: #111827;
  text-align: left;
}

.ax-preview :deep(.el-table__row:nth-child(even) td) {
  background: #F2F5F4;
}

.ax-preview :deep(.el-table__inner-wrapper::before) {
  display: none;
}

.ax-side-extra-charts {
  display: grid;
  grid-template-columns: minmax(0, 1fr);
  gap: 12px;
  margin-top: 12px;
}

.ax-side-chart-grid {
  display: grid;
  grid-template-columns: minmax(0, 1fr);
  gap: 12px;
}

.ax-side-extra-chart-card {
  padding: 12px 12px 10px;
  border-radius: 6px;
  border: 1px solid rgba(0, 0, 0, 0.08);
  background: #FFFFFF;
}

.ax-side-extra-chart-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  margin-bottom: 8px;
}

.ax-side-extra-chart-title {
  font-size: 13px;
  font-weight: 700;
  color: #111827;
}

.ax-side-extra-chart-action {
  height: 26px;
  padding: 0 10px;
  font-size: 11px;
}

.ax-side-extra-chart-canvas {
  width: 100%;
  height: 280px;
}

.ax-insight-metric-compact {
  min-height: 180px;
}

/* 日志时间 */
.ax-log-time {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  min-height: 28px;
  padding: 0 10px;
  border-radius: 999px;
  background: #F2F5F4;
  color: var(--text-muted);
  font-size: 12px;
  margin-top: 8px;
}

.ax-log-time-label {
  color: #6B7280;
  font-weight: 600;
}

.ax-log-section {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-top: 10px;
}

.ax-log-section-title {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #9CA3AF;
}

.ax-log-inline-action {
  align-self: flex-end;
}

.ax-log-section-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
}

.ax-log-markdown {
  padding: 12px 14px;
  border-radius: 4px;
  border: 1px solid rgba(0, 0, 0, 0.08);
  background: #FFFFFF;
  font-size: 12px;
  line-height: 1.8;
  color: #111827;
}

.ax-log-markdown :deep(h1),
.ax-log-markdown :deep(h2),
.ax-log-markdown :deep(h3) {
  margin: 0 0 8px;
  color: #111827;
  font-size: 13px;
}

.ax-log-markdown :deep(p),
.ax-log-markdown :deep(ul),
.ax-log-markdown :deep(ol) {
  margin: 0 0 8px;
}

.ax-log-markdown :deep(ul),
.ax-log-markdown :deep(ol) {
  padding-left: 18px;
}

.ax-report-dialog-body {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

:deep(.ax-report-dialog .el-dialog__header) {
  display: none;
}

.ax-report-dialog-head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
  padding: 2px 2px 12px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.08);
}

.ax-report-dialog-title-block {
  min-width: 0;
  flex: 1;
}

.ax-report-dialog-title {
  margin: 6px 0 0;
  font-size: 24px;
  line-height: 1.22;
  font-weight: 700;
  color: #111827;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.ax-report-dialog-subtitle {
  margin: 7px 0 0;
  max-width: min(980px, 72vw);
  color: #6B7280;
  font-size: 14px;
  line-height: 1.45;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.ax-report-dialog-content {
  max-height: 72vh;
  overflow-y: auto;
  padding: 2px 6px 8px 0;
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.ax-report-dialog-overview {
  width: 100%;
  max-width: 1120px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: minmax(0, 1.15fr) minmax(320px, 0.85fr);
  gap: 14px;
}

.ax-report-dialog-content.is-template-comparison .ax-report-dialog-overview {
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.ax-report-dialog-content.is-template-ranking .ax-report-chart-grid {
  grid-template-columns: minmax(0, 1fr);
}

.ax-report-dialog-content.is-template-detail .ax-report-dialog-overview {
  grid-template-columns: minmax(0, 1fr);
}

.ax-report-dialog-content.is-template-detail .ax-report-stage-metrics .ax-kpi-shelf {
  grid-template-columns: repeat(4, minmax(0, 1fr));
}

.ax-report-stage-section {
  max-width: 1120px;
  width: 100%;
  margin: 0 auto;
  padding: 16px 18px 16px;
  border: 1px solid rgba(0, 0, 0, 0.08);
  border-radius: 4px;
  background: #ffffff;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.ax-report-stage-summary {
  background: linear-gradient(180deg, #ffffff 0%, #FFFFFF 100%);
}

.ax-report-stage-metrics {
  align-self: stretch;
}

.ax-report-stage-metrics .ax-kpi-shelf {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 10px;
}

.ax-report-stage-metrics .ax-kpi-card {
  min-width: 0;
}

.ax-report-stage-title {
  margin-bottom: 12px;
  font-size: 20px;
  font-weight: 700;
  line-height: 1.25;
  color: #111827;
}

.ax-report-core-conclusion {
  display: grid;
  gap: 5px;
  margin: 0 0 12px;
  padding: 12px 14px;
  border: 1px solid rgba(0, 0, 0, 0.08);
  border-radius: 4px;
  background: linear-gradient(180deg, #F2F5F4 0%, #ffffff 100%);
}

.ax-report-core-conclusion span {
  color: #1A1A1A;
  font-size: 12px;
  font-weight: 800;
}

.ax-report-core-conclusion strong {
  color: #111827;
  font-size: 15px;
  line-height: 1.7;
  font-weight: 800;
}

.ax-report-bullet-list {
  margin: 0;
  padding-left: 20px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  color: #111827;
  font-size: 14px;
  line-height: 1.8;
}

.ax-report-bullet-list-compact {
  gap: 6px;
  font-size: 13px;
  line-height: 1.7;
  margin-bottom: 12px;
}

.ax-report-sections {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.ax-report-section-card {
  padding: 12px 14px 12px;
  border-radius: 4px;
  border: 1px solid rgba(0, 0, 0, 0.08);
  background: #FFFFFF;
}

.ax-report-section-card-dialog {
  padding: 16px 18px 16px;
  border-radius: 4px;
  background: #ffffff;
}

.ax-report-section-title {
  margin-bottom: 10px;
  font-size: 18px;
  font-weight: 700;
  line-height: 1.35;
  color: #111827;
}

.ax-report-chart-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 14px;
}

.ax-report-chart-card {
  padding: 14px 14px 12px;
  border-radius: 4px;
  border: 1px solid rgba(0, 0, 0, 0.08);
  background: #ffffff;
  box-shadow: 0 8px 22px rgba(0, 0, 0, 0.06);
}

.ax-report-chart-head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 10px;
}

.ax-report-chart-title {
  font-size: 16px;
  font-weight: 700;
  color: #111827;
}

.ax-report-chart-subtitle {
  margin-top: 3px;
  font-size: 12px;
  color: #9CA3AF;
}

.ax-report-chart-canvas {
  width: 100%;
  height: 340px;
}

.ax-report-table-stack {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 10px;
}

.ax-report-table-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 14px;
}

.ax-report-table-card {
  padding: 14px 14px 12px;
  border-radius: 6px;
  border: 1px solid rgba(0, 0, 0, 0.08);
  background: #FFFFFF;
}

.ax-report-table-card-dialog {
  background: #ffffff;
}

.ax-report-table-head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 10px;
}

.ax-report-table-title {
  font-size: 16px;
  font-weight: 700;
  color: #111827;
}

.ax-report-table-desc {
  margin-top: 4px;
  font-size: 12px;
  line-height: 1.7;
  color: #9CA3AF;
}

.ax-preview-table-report {
  margin-top: 2px;
}

.ax-preview-table-report :deep(.el-table__header-wrapper th) {
  background: #F2F5F4;
  color: #6B7280;
  font-size: 11px;
  font-weight: 600;
  height: 34px;
  text-align: left;
}

.ax-preview-table-report :deep(.el-table__body-wrapper td) {
  font-size: 11px;
  color: #111827;
  text-align: left;
}

.ax-preview-table-report :deep(.el-table__row:nth-child(even) td) {
  background: #F2F5F4;
}

.ax-preview-table-report :deep(.el-table__inner-wrapper::before) {
  display: none;
}

.ax-preview-table-report-dialog :deep(.el-table__body-wrapper) {
  max-height: 360px;
  overflow-y: auto;
}

.ax-insight-metric-report {
  min-height: 280px;
}

.ax-report-md-compact {
  font-size: 12px;
  line-height: 1.8;
}

@media (max-width: 1100px) {
  .ax-report-dialog-overview {
    grid-template-columns: 1fr;
  }

  .ax-report-chart-grid {
    grid-template-columns: 1fr;
  }

  .ax-report-table-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 900px) {
  .ax-report-dialog-title {
    font-size: 21px;
  }

  .ax-report-stage-section {
    padding: 14px 14px 14px;
  }

  .ax-report-stage-title {
    font-size: 18px;
  }

  .ax-report-bullet-list {
    font-size: 13px;
  }

  .ax-report-chart-grid {
    grid-template-columns: 1fr;
  }

  .ax-report-chart-canvas,
  .ax-insight-metric-report {
    height: 240px;
    min-height: 240px;
  }
}

.ax-chart-dialog-body {
  display: flex;
  flex-direction: column;
  gap: 14px;
  min-height: 420px;
}

@keyframes ax-curtain-open {
  from {
    opacity: 0;
    clip-path: inset(0 0 100% 0 round 18px);
    transform: translateY(8px);
  }
  to {
    opacity: 1;
    clip-path: inset(0 0 0 0 round 18px);
    transform: translateY(0);
  }
}

@keyframes ax-stop-beam {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.ax-chart-dialog-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.ax-chart-dialog-kicker {
  font-size: 11px;
  letter-spacing: 0.08em;
  color: #9CA3AF;
}

.ax-chart-dialog-switch {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px;
  border-radius: 999px;
  background: #F3F4F6;
}

.ax-chart-switch-btn {
  border: none;
  background: transparent;
  color: #6B7280;
  font-size: 12px;
  line-height: 1;
  padding: 8px 12px;
  border-radius: 999px;
  cursor: pointer;
  transition: all 0.18s ease;
}

.ax-chart-switch-btn.is-active {
  background: #ffffff;
  color: #1A1A1A;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.ax-chart-dialog-canvas {
  width: 100%;
  height: 68vh;
  min-height: 420px;
}

.ax-chart-dialog-table {
  border: 1px solid rgba(0, 0, 0, 0.08);
  border-radius: 6px;
  overflow: hidden;
  background: #ffffff;
}

.ax-chart-dialog-table-meta {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 14px;
  font-size: 12px;
  color: #9CA3AF;
  background: #F2F5F4;
  border-bottom: 1px solid rgba(0, 0, 0, 0.06);
}

.ax-insight-metric-large {
  min-height: 420px;
}

:global(.ax-toast-modern.el-message) {
  min-width: 0;
  width: auto;
  max-width: min(420px, calc(100vw - 32px));
  padding: 9px 13px;
  border: 1px solid rgba(29, 78, 216, 0.12);
  border-radius: 4px;
  background:
    linear-gradient(180deg, rgba(255, 255, 255, 0.98), rgba(248, 249, 250, 0.98));
  box-shadow:
    0 10px 28px rgba(0, 0, 0, 0.08),
    inset 0 1px 0 rgba(255, 255, 255, 0.92);
  backdrop-filter: blur(10px);
}

:global(.ax-toast-modern .el-message__content) {
  color: #374151;
  font-size: 12px;
  font-weight: 760;
  line-height: 1.35;
}

:global(.ax-toast-modern .el-message__icon) {
  margin-right: 8px;
  font-size: 14px;
}

:global(.ax-toast-modern.el-message--success) {
  border-color: rgba(16, 185, 129, 0.16);
}

:global(.ax-toast-modern.el-message--success .el-message__icon) {
  color: #10B981;
}

:global(.ax-toast-stop.el-message) {
  border-color: rgba(245, 158, 11, 0.18);
  background:
    linear-gradient(180deg, rgba(255, 251, 235, 0.98), rgba(255, 251, 235, 0.98));
}

:global(.ax-toast-stop .el-message__content) {
  color: #B45309;
}

:global(.ax-toast-stop .el-message__icon) {
  color: #B45309;
}

/* 动画 */
.ax-collapse-enter-active,
.ax-collapse-leave-active {
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  overflow: hidden;
}
.ax-collapse-enter-from,
.ax-collapse-leave-to {
  opacity: 0;
  max-height: 0;
}
.ax-collapse-enter-to,
.ax-collapse-leave-from {
  opacity: 1;
  max-height: 800px;
}

.ax-slide-up-enter-active,
.ax-slide-up-leave-active {
  transition: all 0.2s ease;
}
.ax-slide-up-enter-from,
.ax-slide-up-leave-to {
  transform: translateY(10px);
  opacity: 0;
}

.ax-panel-slide-enter-active,
.ax-panel-slide-leave-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
.ax-panel-slide-enter-from,
.ax-panel-slide-leave-to {
  transform: translateX(100%);
  opacity: 0;
}

/* 滚动区 */
.ax-chat-body::-webkit-scrollbar,
.ax-panel-content::-webkit-scrollbar {
  width: 5px;
}
.ax-chat-body::-webkit-scrollbar-thumb,
.ax-panel-content::-webkit-scrollbar-thumb {
  background: var(--border);
  border-radius: 4px;
}

@media (max-width: 1280px) {
  .ax-page {
    padding: 0;
  }

  .ax-detail-panel,
  .ax-detail-panel-container {
    width: 400px;
    max-width: 42vw;
  }
}

@media (max-width: 1080px) {
  .ax-page {
    height: 100%;
    min-height: 0;
  }

  .ax-workspace {
    flex-direction: column;
  }

  .ax-detail-panel,
  .ax-detail-panel-container {
    width: 100%;
    max-width: none;
    border-left: none;
    border-top: 1px solid rgba(0, 0, 0, 0.08);
    min-height: 320px;
    max-height: 42vh;
  }

  /* 纵向堆叠时容器较矮：推理面板保底 200px（容纳完整头部+步骤条+Tab），报告占剩余并各自内部滚动 */
  .ax-detail-panel-container > .reasoning-panel {
    min-height: 200px;
  }
  .ax-detail-panel-container > .ax-side-report {
    flex: 1 1 auto;
    max-height: none;
  }
}
</style>

<style scoped>
.ax-page { background:#f2f5f4; --ax-content-width:1000px; }
.ax-workspace, .ax-chat-panel, .ax-chat-body { background:#f2f5f4; }
.ax-header-track :deep(.ax-header) { background:transparent; min-height:64px; border-color:#dfe7e2; }
.path-selector { display:flex;align-items:center;justify-content:space-between;gap:18px;padding:16px 0 8px;flex-wrap:wrap; }
.path-tabs { display:flex;gap:4px;padding:4px;background:#e9eeeb;border-radius:9px; }
.path-tabs button { display:flex;flex-direction:column;align-items:flex-start;gap:2px;padding:9px 16px;border:0;background:transparent;border-radius:6px;color:#75857c;font:inherit;cursor:pointer; }
.path-tabs button[aria-pressed="true"] { background:white;color:#195f4d;box-shadow:0 2px 6px #263d2e0a; }
.path-tabs button:disabled { cursor:not-allowed;opacity:.5; }
.path-tabs small { font-size:11px; }.path-tabs span { font-size:13px;font-weight:500; }
.path-scope,.path-policy-note { color:#7c8d82;font-size:11px; }.path-policy-note { margin-top:4px;margin-bottom:0; }
.ax-ai-meta { margin-bottom:16px; }.ax-ai-cards { gap:18px;padding-left:0;max-width:none; }.ax-ai-wrap { margin:10px 0 20px; }
.ax-ai-name { font-size:12px;color:#73867a; }.ax-ai-avatar { width:28px;height:28px; }
.ax-msg-list { gap:30px; }.ax-result-chain { background:#fff;border:1px solid #e2e9e5;border-radius:10px;padding:24px;box-shadow:0 4px 20px #203b2a04; }
.ax-inline-visual-card { box-shadow:none; }.ax-composer-track { padding-top:12px;background:#f2f5f4; }
@media(max-width:1080px){.ax-workspace{flex-direction:column}.ax-chat-panel{min-height:0;flex:1}.ax-chat-body{min-height:0}.ax-detail-panel-container{max-height:42vh}.ax-content-track{width:calc(100% - 32px)}}
@media(max-width:700px){.path-tabs{width:100%}.path-tabs button{flex:1;padding:8px}.path-scope{font-size:11px}.ax-result-chain{padding:16px}.ax-page{--ax-content-gutter:16px}}
@media(prefers-reduced-motion:reduce){.ax-page :deep(*){animation:none!important;transition:none!important;scroll-behavior:auto!important}}
</style>

<style scoped src="../styles/analysisStudio.css"></style>

<style scoped>.html-report-reader{display:block;width:100%;height:72dvh;min-height:400px;border:0;border-radius:10px;background:#f3f6fa}</style>

```

---

