<template>
  <div class="studio-page">
    <!-- 无权限提示 -->
    <div v-if="!canRun" class="studio-denied">
      <el-icon class="denied-icon"><InfoFilled /></el-icon>
      <span>当前账号未开通 SQL 调试台权限，请联系管理员分配权限。</span>
    </div>

    <template v-else>
      <!-- ① 顶部深色工具栏：模式切换 + 数据集 + 行限 + 操作区 -->
      <div class="studio-topbar">
        <div class="studio-topbar-left">
          <!-- 模式切换 -->
          <div class="mode-switcher">
            <button class="mode-btn" :class="{ active: activeTab === 'sql' }" @click="activeTab = 'sql'">
              <el-icon><Monitor /></el-icon>SQL 查询
            </button>
            <button class="mode-btn" :class="{ active: activeTab === 'ask' }" @click="activeTab = 'ask'">
              <el-icon><MagicStick /></el-icon>自然语言
            </button>
          </div>

          <div class="topbar-sep"></div>

          <!-- 数据集选择 -->
          <span class="topbar-label"><el-icon><Coin /></el-icon>数据集</span>
          <el-select
            v-model="selectedDatasetId"
            filterable
            clearable
            placeholder="选择数据集..."
            class="studio-dataset-select"
            :loading="datasetsLoading"
            @change="handleDatasetChange"
          >
            <el-option v-for="item in datasets" :key="item.id" :label="datasetLabel(item)" :value="String(item.id)" />
          </el-select>

          <div class="topbar-sep"></div>

          <!-- 行限 -->
          <span class="topbar-label"><el-icon><Odometer /></el-icon>行限</span>
          <el-input-number
            v-model="limit"
            :min="1"
            :max="10000"
            :step="100"
            controls-position="right"
            class="studio-limit-input"
          />
        </div>

        <div class="studio-topbar-right">
          <!-- 刷新 -->
          <button class="topbar-icon-btn" :title="datasetsLoading ? '加载中...' : '刷新数据集'" @click="loadDatasets">
            <el-icon :class="{ 'is-loading': datasetsLoading }"><Refresh /></el-icon>
          </button>
          <!-- 悬浮窗 -->
          <button class="topbar-icon-btn" :class="{ active: floatEnabled }" title="悬浮 SQL 调试窗" @click="toggleFloat">
            <el-icon><Monitor /></el-icon>
          </button>
          <!-- 执行按钮 -->
          <button
            class="studio-run-btn"
            :disabled="(activeTab === 'sql' ? sqlLoading : askLoading)"
            @click="activeTab === 'sql' ? runSql() : runAsk()"
          >
            <el-icon v-if="!(activeTab === 'sql' ? sqlLoading : askLoading)"><VideoPlay /></el-icon>
            <el-icon v-else class="is-loading"><Loading /></el-icon>
            {{ activeTab === 'sql' ? '执行 SQL' : '生成并执行' }}
          </button>
        </div>
      </div>

      <!-- 无数据集提示 -->
      <el-alert
        v-if="!datasetsLoading && !datasets.length"
        title="当前账号没有可调试的数据集，或数据集未授权。"
        type="warning"
        :closable="false"
        show-icon
        class="studio-alert"
      />

      <!-- ② 编辑区主体 -->
      <div class="studio-editor-zone">
        <!-- 编辑器顶部状态条 -->
        <div class="editor-statusbar">
          <div class="statusbar-left">
            <span class="statusbar-mode" :class="activeTab">
              {{ activeTab === 'sql' ? '只读 SQL' : '自然语言 → SQL' }}
            </span>
            <span v-if="selectedDatasetId" class="statusbar-dataset">
              {{ datasetLabel(datasets.find(d => String(d.id) === selectedDatasetId) || {}) }}
            </span>
          </div>
          <span class="statusbar-hint">Ctrl + Enter {{ activeTab === 'sql' ? '执行' : '生成并执行' }}</span>
        </div>

        <!-- SQL 输入框 -->
        <el-input
          v-if="activeTab === 'sql'"
          v-model="sqlText"
          type="textarea"
          :rows="14"
          resize="none"
          class="studio-editor"
          placeholder="-- 输入只读 SELECT 查询
-- 例如: SELECT * FROM your_table WHERE ... LIMIT 50"
          @keydown.ctrl.enter.prevent="runSql"
        />

        <!-- 自然语言输入框 -->
        <el-input
          v-if="activeTab === 'ask'"
          v-model="questionText"
          type="textarea"
          :rows="7"
          resize="none"
          class="studio-editor studio-editor--ask"
          placeholder="用业务语言描述问题，例如：本月各战区的实际开单总额排名..."
          @keydown.ctrl.enter.prevent="runAsk"
        />
      </div>

      <!-- ③ 自然语言模式：生成 SQL 预览（仅有结果时展示） -->
      <div v-if="activeTab === 'ask' && (askResult.generated_sql || askResult.final_sql)" class="studio-sql-preview">
        <div v-if="askResult.generated_sql" class="sql-pane">
          <div class="sql-pane-header">
            <span class="sql-pane-label">初步生成 SQL</span>
            <button class="sql-pane-copy" @click="copyText(askResult.generated_sql)">复制</button>
          </div>
          <pre class="sql-pane-body">{{ askResult.generated_sql }}</pre>
        </div>
        <div v-if="askResult.final_sql" class="sql-pane">
          <div class="sql-pane-header">
            <span class="sql-pane-label">最终执行 SQL（含权限注入）</span>
            <button class="sql-pane-copy" @click="copyText(askResult.final_sql)">复制</button>
          </div>
          <pre class="sql-pane-body">{{ askResult.final_sql }}</pre>
        </div>
      </div>

      <!-- ④ 结果托盘 -->
      <div class="studio-result">
        <!-- 结果头部 -->
        <div class="result-header">
          <div class="result-header-left">
            <span
              class="result-dot"
              :class="{
                'is-ok': currentResult.columns?.length,
                'is-err': currentResult.error,
              }"
            ></span>
            <strong class="result-title">查询结果</strong>
            <span v-if="currentResult.columns?.length" class="result-count">
              {{ currentResult.row_count || currentResult.rows?.length || 0 }} 行 · 最多 {{ currentResult.limit || '-' }} 行
            </span>
            <span v-else-if="!currentResult.error && !sqlLoading && !askLoading" class="result-waiting">
              等待执行
            </span>
          </div>
          <div v-if="currentResult.rows?.length && canCopy" class="result-actions">
            <button class="result-btn" @click="copyRows(currentResult, 'tsv')">
              <el-icon><CopyDocument /></el-icon>复制表格
            </button>
            <button class="result-btn" @click="copyRows(currentResult, 'json')">
              <el-icon><CopyDocument /></el-icon>JSON
            </button>
            <button class="result-btn" @click="exportRows(currentResult, 'result.csv')">
              <el-icon><Download /></el-icon>导出 CSV
            </button>
          </div>
        </div>

        <!-- 错误信息 -->
        <div v-if="currentResult.error" class="result-error">
          <el-icon><WarningFilled /></el-icon>
          <span>{{ currentResult.error }}</span>
        </div>

        <!-- 数据表格 -->
        <el-table
          v-if="currentResult.columns?.length"
          :data="currentResult.rows || []"
          border
          stripe
          size="small"
          :height="340"
          class="studio-table"
        >
          <el-table-column
            v-for="col in currentResult.columns"
            :key="col"
            :prop="col"
            :label="col"
            :min-width="130"
            show-overflow-tooltip
          >
            <template #default="{ row }">{{ formatCell(row?.[col]) }}</template>
          </el-table-column>
        </el-table>

        <!-- 空状态 -->
        <div v-else-if="!currentResult.error" class="result-empty">
          <div class="result-empty-inner">
            <svg class="result-empty-svg" viewBox="0 0 88 64" fill="none">
              <rect x="2" y="2" width="84" height="60" rx="10" fill="rgba(13,148,136,0.04)" stroke="#0d9488" stroke-width="1.5" stroke-dasharray="6 3"/>
              <rect x="12" y="18" width="20" height="3" rx="1.5" fill="#0d9488" opacity=".35"/>
              <rect x="12" y="25" width="30" height="3" rx="1.5" fill="#0d9488" opacity=".2"/>
              <rect x="12" y="32" width="24" height="3" rx="1.5" fill="#0d9488" opacity=".15"/>
              <rect x="12" y="39" width="18" height="3" rx="1.5" fill="#0d9488" opacity=".1"/>
              <circle cx="65" cy="38" r="14" fill="rgba(13,148,136,0.07)" stroke="#0d9488" stroke-width="1.5"/>
              <path d="M59 38l4 4 8-8" stroke="#0d9488" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <div class="result-empty-text">
              {{ activeTab === 'sql' ? '执行 SQL 后数据将出现在这里' : '提交问题后，AI 将生成并执行 SQL，结果将显示在这里' }}
            </div>
          </div>
        </div>

        <!-- 执行日志 -->
        <div v-if="currentResult.logs?.length" class="result-logs">
          <div class="result-logs-title">执行日志</div>
          <div
            v-for="(item, i) in currentResult.logs"
            :key="i"
            class="result-log-row"
            :class="`is-${item.level || 'info'}`"
          >
            <span class="log-level-tag">{{ item.level || 'info' }}</span>
            <span class="log-message">{{ item.message }}</span>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { computed, defineComponent, h, onMounted, onUnmounted, ref, watch } from 'vue'
import { ElMessage, ElTable, ElTableColumn } from 'element-plus'
import {
  Coin, CopyDocument, Download, InfoFilled, Loading,
  MagicStick, Monitor, Odometer, Refresh, VideoPlay, WarningFilled,
} from '@element-plus/icons-vue'
import { askBookshelfDatasetSqlDebug, getBookshelfDatasets, previewBookshelfDatasetSql } from '../api/index'
import { useFeatureFlags } from '../state/featureFlags'

defineOptions({ name: 'SqlDebug' })

const STATE_KEY = 'datapulse_sql_debug_page_state'
const FLOAT_ENABLED_KEY = 'datapulse_sql_debug_float_enabled'
const FLOAT_TOGGLE_EVENT = 'datapulse-sql-debug-float-toggle'

const createEmptyResult = () => ({
  columns: [],
  rows: [],
  row_count: 0,
  limit: 100,
  logs: [],
  error: '',
  generated_sql: '',
  final_sql: '',
})

const formatCell = (value) => {
  if (value === null || value === undefined) return ''
  if (typeof value === 'object') return JSON.stringify(value)
  return String(value)
}

const { isFeatureEnabled, loadFeatureFlags } = useFeatureFlags()
const canRun = computed(() => isFeatureEnabled('dataset_sql_preview_run'))
const canCopy = computed(() => isFeatureEnabled('dataset_sql_preview_copy'))

const datasets = ref([])
const datasetsLoading = ref(false)
const selectedDatasetId = ref('')
const activeTab = ref('sql')
const limit = ref(100)
const sqlText = ref('')
const questionText = ref('')
const sqlLoading = ref(false)
const askLoading = ref(false)
const sqlResult = ref(createEmptyResult())
const askResult = ref(createEmptyResult())
const floatEnabled = ref(false)

// 当前活动结果（随 Tab 切换）
const currentResult = computed(() => activeTab.value === 'sql' ? sqlResult.value : askResult.value)

const datasetLabel = (item) => {
  const name = item?.dataset_name || item?.dataset_code || `数据集 ${item?.id || ''}`
  const source = item?.source_name || item?.source_id
  return source ? `${name} · ${source}` : name
}

const persistState = () => {
  localStorage.setItem(STATE_KEY, JSON.stringify({
    selectedDatasetId: selectedDatasetId.value,
    activeTab: activeTab.value,
    limit: limit.value,
  }))
}

const restoreState = () => {
  try {
    const saved = JSON.parse(localStorage.getItem(STATE_KEY) || 'null') || {}
    selectedDatasetId.value = saved.selectedDatasetId ? String(saved.selectedDatasetId) : ''
    activeTab.value = saved.activeTab || 'sql'
    limit.value = Number(saved.limit) || 100
  } catch {
    selectedDatasetId.value = ''
  }
}

const restoreFloatState = () => {
  floatEnabled.value = localStorage.getItem(FLOAT_ENABLED_KEY) === '1'
}

const toggleFloat = () => {
  floatEnabled.value = !floatEnabled.value
  localStorage.setItem(FLOAT_ENABLED_KEY, floatEnabled.value ? '1' : '0')
  window.dispatchEvent(new CustomEvent(FLOAT_TOGGLE_EVENT, {
    detail: { enabled: floatEnabled.value },
  }))
  ElMessage.success(floatEnabled.value ? 'SQL 调试悬浮已开启' : 'SQL 调试悬浮已关闭')
}

const handleFloatToggle = (event) => {
  floatEnabled.value = Boolean(event?.detail?.enabled)
}

const loadDatasets = async () => {
  datasetsLoading.value = true
  try {
    const response = await getBookshelfDatasets()
    datasets.value = response?.datasets || []
    const currentExists = datasets.value.some(item => String(item.id) === String(selectedDatasetId.value))
    if (!currentExists) {
      selectedDatasetId.value = datasets.value.length ? String(datasets.value[0].id) : ''
    }
  } finally {
    datasetsLoading.value = false
  }
}

const handleDatasetChange = () => {
  sqlResult.value = createEmptyResult()
  askResult.value = createEmptyResult()
}

const ensureDataset = () => {
  if (!selectedDatasetId.value) {
    ElMessage.warning('请先选择数据集')
    return false
  }
  return true
}

const normalizeErrorResult = (error, fallback) => ({
  ...fallback,
  error: error?.response?.data?.error || error?.message || '执行失败',
  logs: error?.response?.data?.logs || fallback.logs || [],
})

const runSql = async () => {
  if (!ensureDataset()) return
  if (!String(sqlText.value || '').trim()) {
    ElMessage.warning('请输入 SQL')
    return
  }
  sqlLoading.value = true
  sqlResult.value = createEmptyResult()
  try {
    const response = await previewBookshelfDatasetSql(selectedDatasetId.value, {
      sql: sqlText.value,
      limit: limit.value,
    })
    sqlResult.value = { ...createEmptyResult(), ...response, logs: [{ level: 'info', message: 'SQL 执行完成' }] }
  } catch (error) {
    sqlResult.value = normalizeErrorResult(error, createEmptyResult())
  } finally {
    sqlLoading.value = false
  }
}

const runAsk = async () => {
  if (!ensureDataset()) return
  if (!String(questionText.value || '').trim()) {
    ElMessage.warning('请输入问题')
    return
  }
  askLoading.value = true
  askResult.value = createEmptyResult()
  try {
    const response = await askBookshelfDatasetSqlDebug(selectedDatasetId.value, {
      question: questionText.value,
      limit: limit.value,
    })
    askResult.value = {
      ...createEmptyResult(),
      ...response,
      final_sql: response?.preview_sql || response?.final_sql || '',
    }
  } catch (error) {
    const payload = error?.response?.data || {}
    askResult.value = normalizeErrorResult(error, {
      ...createEmptyResult(),
      generated_sql: payload.generated_sql || '',
      final_sql: payload.final_sql || '',
      logs: payload.logs || [],
    })
  } finally {
    askLoading.value = false
  }
}

const copyText = async (text) => {
  const content = String(text || '')
  if (!content) return
  try {
    await navigator.clipboard.writeText(content)
  } catch {
    const textarea = document.createElement('textarea')
    textarea.value = content
    textarea.style.position = 'fixed'
    textarea.style.opacity = '0'
    document.body.appendChild(textarea)
    textarea.select()
    document.execCommand('copy')
    document.body.removeChild(textarea)
  }
  ElMessage.success('已复制')
}

const rowsToTsv = (result) => [
  result.columns.join('\t'),
  ...(result.rows || []).map(row => result.columns.map(column => formatCell(row?.[column]).replace(/\t/g, ' ').replace(/\r?\n/g, ' ')).join('\t')),
].join('\n')

function csvCell(value) {
  const text = String(value ?? '')
  return /[",\r\n]/.test(text) ? `"${text.replace(/"/g, '""')}"` : text
}

const rowsToCsv = (result) => [
  result.columns.map(csvCell).join(','),
  ...(result.rows || []).map(row => result.columns.map(column => csvCell(formatCell(row?.[column]))).join(',')),
].join('\n')

const copyRows = (result, mode) => {
  if (!canCopy.value || !result?.rows?.length) return
  copyText(mode === 'json' ? JSON.stringify(result.rows, null, 2) : rowsToTsv(result))
}

const exportRows = (result, filename) => {
  if (!canCopy.value || !result?.rows?.length) return
  const blob = new Blob([`\uFEFF${rowsToCsv(result)}`], { type: 'text/csv;charset=utf-8' })
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = filename
  link.click()
  URL.revokeObjectURL(url)
}

watch([selectedDatasetId, activeTab, limit], persistState)

onMounted(async () => {
  restoreState()
  restoreFloatState()
  await loadFeatureFlags()
  await loadDatasets()
  window.addEventListener(FLOAT_TOGGLE_EVENT, handleFloatToggle)
})

onUnmounted(() => {
  window.removeEventListener(FLOAT_TOGGLE_EVENT, handleFloatToggle)
})
</script>

<style scoped>
/* ============================================================
   整体页面
   ============================================================ */
.studio-page {
  display: flex;
  flex-direction: column;
  min-height: calc(100vh - 100px);
  background: transparent;
  border-radius: 0;
  overflow: hidden;
}

/* ============================================================
   无权限状态
   ============================================================ */
.studio-denied {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 20px 24px;
  background: #fef2f2;
  color: #b91c1c;
  font-size: 14px;
}

.studio-denied .denied-icon {
  font-size: 18px;
  flex-shrink: 0;
}

/* ============================================================
   ① 顶部深色工具栏
   ============================================================ */
.studio-topbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding: 0 16px;
  height: 52px;
  background: #f8fafc;
  border-bottom: 1px solid #e2e8f0;
  flex-shrink: 0;
}

.studio-topbar-left {
  display: flex;
  align-items: center;
  gap: 10px;
  flex: 1;
  min-width: 0;
}

.studio-topbar-right {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-shrink: 0;
}

/* 模式切换按钮组 */
.mode-switcher {
  display: flex;
  align-items: center;
  gap: 2px;
  background: #edf2f7;
  border-radius: 8px;
  padding: 3px;
  flex-shrink: 0;
}

.mode-btn {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  padding: 5px 12px;
  border: none;
  border-radius: 6px;
  background: transparent;
  color: #64748b;
  font-size: 12.5px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.18s ease;
  white-space: nowrap;
}

.mode-btn .el-icon {
  font-size: 13px;
}

.mode-btn:hover {
  background: rgba(29, 78, 216, 0.08);
  color: #1d4ed8;
}

.mode-btn.active {
  background: #1d4ed8;
  color: #ffffff;
  box-shadow: 0 2px 8px rgba(29, 78, 216, 0.25);
}

/* 分隔线 */
.topbar-sep {
  width: 1px;
  height: 20px;
  background: #e2e8f0;
  flex-shrink: 0;
}

/* 标签文字 */
.topbar-label {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  color: #64748b;
  font-size: 12px;
  white-space: nowrap;
  flex-shrink: 0;
}

.topbar-label .el-icon {
  color: #1d4ed8;
  font-size: 14px;
}

/* 数据集选择器 */
.studio-dataset-select {
  width: 320px;
  max-width: 100%;
}

:deep(.studio-dataset-select .el-input__wrapper) {
  border-radius: 7px !important;
  box-shadow: 0 0 0 1px #cbd5e1 inset !important;
  transition: all 0.2s;
}

:deep(.studio-dataset-select .el-input__wrapper:hover) {
  box-shadow: 0 0 0 1px #1d4ed8 inset !important;
}

:deep(.studio-dataset-select .el-input__wrapper.is-focus) {
  box-shadow: 0 0 0 1.5px #1d4ed8 inset, 0 0 0 3px rgba(29, 78, 216, 0.12) !important;
}

/* 行限输入 */
.studio-limit-input {
  width: 110px;
}

:deep(.studio-limit-input .el-input__wrapper) {
  border-radius: 7px !important;
}

/* 右侧图标按钮 */
.topbar-icon-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border: 1px solid #e2e8f0;
  border-radius: 7px;
  background: #ffffff;
  color: #64748b;
  cursor: pointer;
  transition: all 0.18s ease;
  font-size: 15px;
}

.topbar-icon-btn:hover {
  border-color: #1d4ed8;
  color: #1d4ed8;
  background: rgba(29, 78, 216, 0.05);
}

.topbar-icon-btn.active {
  background: rgba(29, 78, 216, 0.1);
  border-color: #1d4ed8;
  color: #1d4ed8;
}

/* 执行按钮 */
.studio-run-btn {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  padding: 0 18px;
  height: 34px;
  border: none;
  border-radius: 8px;
  background: linear-gradient(135deg, #1d4ed8, #1e40af);
  color: #ffffff;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 2px 8px rgba(29, 78, 216, 0.3);
  white-space: nowrap;
}

.studio-run-btn .el-icon {
  font-size: 15px;
}

.studio-run-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, #1e40af, #1e3a8a);
  box-shadow: 0 4px 14px rgba(29, 78, 216, 0.4);
  transform: translateY(-1px);
}

.studio-run-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

/* 无数据集提示 */
.studio-alert {
  border-radius: 0;
  border-left: none;
  border-right: none;
}

/* ============================================================
   ② 编辑器区域
   ============================================================ */
.studio-editor-zone {
  display: flex;
  flex-direction: column;
  background: #0d1117;
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
}

/* 编辑器顶部状态条 */
.editor-statusbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 6px 14px;
  background: #161b27;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  flex-shrink: 0;
}

.statusbar-left {
  display: flex;
  align-items: center;
  gap: 10px;
}

.statusbar-mode {
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.04em;
  padding: 2px 8px;
  border-radius: 4px;
}

.statusbar-mode.sql {
  color: #5eead4;
  background: rgba(29, 78, 216, 0.15);
}

.statusbar-mode.ask {
  color: #a5b4fc;
  background: rgba(99, 102, 241, 0.15);
}

.statusbar-dataset {
  color: rgba(148, 163, 184, 0.7);
  font-size: 11.5px;
  max-width: 300px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.statusbar-hint {
  color: rgba(100, 116, 139, 0.8);
  font-size: 11px;
}

/* 代码编辑器 */
.studio-editor {
  font-family: ui-monospace, 'JetBrains Mono', 'Fira Code', SFMono-Regular, Menlo, Consolas, monospace;
}

:deep(.studio-editor .el-textarea__inner) {
  font-family: ui-monospace, 'JetBrains Mono', 'Fira Code', SFMono-Regular, Menlo, Consolas, monospace !important;
  font-size: 13.5px !important;
  line-height: 1.7 !important;
  background: #0d1117 !important;
  color: #e2e8f0 !important;
  border: none !important;
  border-radius: 0 !important;
  box-shadow: none !important;
  padding: 18px 20px !important;
  caret-color: #1d4ed8;
  resize: none !important;
}

:deep(.studio-editor .el-textarea__inner::placeholder) {
  color: #94a3b8 !important;
  font-style: italic;
}

:deep(.studio-editor .el-textarea__inner:focus) {
  background: #0d1117 !important;
  box-shadow: none !important;
  border: none !important;
  outline: none !important;
}

/* 自然语言模式：浅色背景，区别于SQL的纯暗色 */
:deep(.studio-editor--ask .el-textarea__inner) {
  background: #111827 !important;
  color: #c9d1d9 !important;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
  font-size: 14px !important;
  font-style: normal;
}

:deep(.studio-editor--ask .el-textarea__inner::placeholder) {
  color: #94a3b8 !important;
  font-style: normal;
}

/* ============================================================
   ③ 自然语言模式的生成 SQL 预览
   ============================================================ */
.studio-sql-preview {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
}

.sql-pane {
  border-right: 1px solid rgba(255, 255, 255, 0.06);
  background: #090d16;
  overflow: hidden;
}

.sql-pane:last-child {
  border-right: none;
}

.sql-pane-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 14px;
  background: rgba(255, 255, 255, 0.03);
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.sql-pane-label {
  color: rgba(148, 163, 184, 0.8);
  font-size: 11.5px;
  font-weight: 600;
}

.sql-pane-copy {
  padding: 3px 8px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 4px;
  background: transparent;
  color: rgba(148, 163, 184, 0.7);
  font-size: 11px;
  cursor: pointer;
  transition: all 0.15s;
}

.sql-pane-copy:hover {
  background: rgba(29, 78, 216, 0.2);
  border-color: #1d4ed8;
  color: #5eead4;
}

.sql-pane-body {
  margin: 0;
  padding: 14px;
  min-height: 120px;
  max-height: 240px;
  overflow: auto;
  color: #9ecf8c;
  font-family: ui-monospace, 'JetBrains Mono', monospace;
  font-size: 12px;
  line-height: 1.65;
  white-space: pre-wrap;
  word-break: break-word;
}

/* ============================================================
   ④ 结果托盘
   ============================================================ */
.studio-result {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: #ffffff;
  min-height: 0;
}

.result-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 18px;
  border-bottom: 1px solid #e2e8f0;
  background: #f8fafc;
  flex-shrink: 0;
  gap: 12px;
  flex-wrap: wrap;
}

.result-header-left {
  display: flex;
  align-items: center;
  gap: 10px;
}

/* 状态指示灯 */
.result-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #cbd5e1;
  flex-shrink: 0;
  transition: all 0.3s ease;
}

.result-dot.is-ok {
  background: #1d4ed8;
  box-shadow: 0 0 0 3px rgba(29, 78, 216, 0.15);
}

.result-dot.is-err {
  background: #dc2626;
  box-shadow: 0 0 0 3px rgba(220, 38, 38, 0.15);
}

.result-title {
  color: #1e293b;
  font-size: 13.5px;
  font-weight: 700;
}

.result-count {
  color: #1d4ed8;
  font-size: 12px;
  font-weight: 500;
  background: rgba(29, 78, 216, 0.08);
  padding: 2px 10px;
  border-radius: 20px;
  border: 1px solid rgba(29, 78, 216, 0.2);
}

.result-waiting {
  color: #94a3b8;
  font-size: 12px;
}

.result-actions {
  display: flex;
  align-items: center;
  gap: 6px;
}

.result-btn {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  padding: 5px 12px;
  border: 1px solid #e2e8f0;
  border-radius: 7px;
  background: #ffffff;
  color: #475569;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.15s ease;
}

.result-btn .el-icon {
  font-size: 13px;
}

.result-btn:hover {
  border-color: #1d4ed8;
  color: #1d4ed8;
  background: rgba(29, 78, 216, 0.04);
}

/* 错误提示 */
.result-error {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  margin: 14px 18px;
  padding: 12px 14px;
  border: 1px solid rgba(220, 38, 38, 0.2);
  border-radius: 8px;
  background: #fef2f2;
  color: #b91c1c;
  font-size: 13px;
  line-height: 1.5;
}

.result-error .el-icon {
  font-size: 16px;
  margin-top: 1px;
  flex-shrink: 0;
}

/* 数据表格 */
.studio-table {
  margin: 0;
}

:deep(.studio-table .el-table__header-wrapper th) {
  background: #f8fafc !important;
  color: #334155 !important;
  font-size: 12px !important;
  font-weight: 700 !important;
}

:deep(.studio-table .el-table__body td) {
  font-size: 12.5px;
  color: #475569;
}

:deep(.studio-table .el-table__body tr.el-table__row--striped td) {
  background: #fafbfc !important;
}

/* 空状态 */
.result-empty {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 48px 24px;
}

.result-empty-inner {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 14px;
  text-align: center;
}

.result-empty-svg {
  width: 88px;
  height: auto;
  opacity: 0.85;
}

.result-empty-text {
  color: #64748b;
  font-size: 13.5px;
  max-width: 380px;
  line-height: 1.6;
  margin: 0;
}

/* 日志区 */
.result-logs {
  margin: 14px 18px;
  padding: 12px 14px;
  border-radius: 8px;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  flex-shrink: 0;
}

.result-logs-title {
  color: #334155;
  font-size: 11.5px;
  font-weight: 700;
  margin-bottom: 8px;
  text-transform: uppercase;
  letter-spacing: 0.06em;
}

.result-log-row {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding: 3px 0;
  font-size: 12px;
  line-height: 1.5;
}

.log-level-tag {
  flex-shrink: 0;
  width: 40px;
  color: #94a3b8;
  font-weight: 600;
  text-transform: uppercase;
  font-size: 11px;
}

.log-message {
  color: #475569;
}

.result-log-row.is-error .log-level-tag {
  color: #dc2626;
}

.result-log-row.is-error .log-message {
  color: #b91c1c;
}

/* ============================================================
   动画
   ============================================================ */
@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.is-loading {
  animation: spin 0.9s linear infinite;
}

/* ============================================================
   响应式
   ============================================================ */
@media (max-width: 1100px) {
  .studio-topbar {
    flex-wrap: wrap;
    height: auto;
    padding: 10px 14px;
    gap: 10px;
  }

  .studio-topbar-left {
    flex-wrap: wrap;
    gap: 8px;
  }

  .studio-dataset-select {
    width: 240px;
  }

  .studio-sql-preview {
    grid-template-columns: 1fr;
  }

  .sql-pane {
    border-right: none;
    border-bottom: 1px solid rgba(255, 255, 255, 0.06);
  }
}

@media (max-width: 768px) {
  .studio-topbar-left {
    flex-direction: column;
    align-items: flex-start;
  }

  .studio-dataset-select {
    width: 100%;
  }

  .topbar-sep {
    display: none;
  }
}
</style>
