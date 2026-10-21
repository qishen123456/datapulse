<template>
  <aside class="reasoning-panel">
    <!-- 面板顶部区域 -->
    <div class="panel-header">
      <div class="panel-header-main">
        <div class="panel-badge-row">
          <span class="panel-category-badge">
            <span class="badge-dot"></span>
            数智推理透视
          </span>
          <span class="panel-status-tag" :class="`status-${status}`">
            {{ statusLabel }}
          </span>
        </div>
        <h3 class="panel-title">AI 深度决策推导</h3>
        <p class="panel-desc">透明还原业务意图拆解、口径对齐、数据提炼与归因分析全过程</p>
      </div>

      <button class="panel-close-btn" type="button" title="收起面板" @click="$emit('close')">
        <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <line x1="18" y1="6" x2="6" y2="18"/>
          <line x1="6" y1="6" x2="18" y2="18"/>
        </svg>
      </button>
    </div>

    <!-- 阶段流水步进器（4阶段直观展现） -->
    <div class="pipeline-stepper">
      <div
        v-for="(st, idx) in stages"
        :key="st.key"
        class="step-item"
        :class="{
          'is-active': currentStageIndex === idx,
          'is-done': currentStageIndex > idx || isCompleted,
          'is-pending': currentStageIndex < idx && !isCompleted
        }"
      >
        <div class="step-dot-wrap">
          <span class="step-num">{{ idx + 1 }}</span>
        </div>
        <span class="step-label">{{ st.label }}</span>
        <div v-if="idx < stages.length - 1" class="step-line"></div>
      </div>
    </div>

    <!-- 视图切换 Tab：业务推演 vs 技术溯源 -->
    <div class="panel-tabs">
      <button
        class="tab-btn"
        :class="{ 'is-active': activeTab === 'business' }"
        type="button"
        @click="activeTab = 'business'"
      >
        <svg class="tab-icon" viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <polygon points="12 2 2 7 12 12 22 7 12 2"/>
          <polyline points="2 17 12 22 22 17"/>
          <polyline points="2 12 12 17 22 12"/>
        </svg>
        <span>决策推演链</span>
      </button>
      <button
        class="tab-btn"
        :class="{ 'is-active': activeTab === 'technical' }"
        type="button"
        @click="activeTab = 'technical'"
      >
        <svg class="tab-icon" viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <polyline points="16 18 22 12 16 6"/>
          <polyline points="8 6 2 12 8 18"/>
        </svg>
        <span>底层技术溯源</span>
        <span v-if="hasSql" class="sql-badge">SQL</span>
      </button>
    </div>

    <!-- 面板滚动内容区 -->
    <div class="panel-body" ref="bodyRef">
      <!-- 空状态 -->
      <div v-if="logs.length === 0" class="empty-state">
        <div class="compass-icon-wrap">
          <svg class="compass-svg" viewBox="0 0 48 48" width="48" height="48" fill="none" stroke="#0D9488" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="24" cy="24" r="20" stroke="#CBD5E1"/>
            <polygon points="24 12 28 20 20 28 24 36 28 28 20 20" fill="rgba(13, 148, 136, 0.15)"/>
            <line x1="24" y1="4" x2="24" y2="8"/>
            <line x1="24" y1="40" x2="24" y2="44"/>
            <line x1="4" y1="24" x2="8" y2="24"/>
            <line x1="40" y1="24" x2="44" y2="24"/>
          </svg>
        </div>
        <p class="empty-title">AI 分析大脑正在就绪</p>
        <p class="empty-desc">在对话框提出业务问题，系统将在此处实时透视语义解析、指标匹配与计算推演全过程</p>
      </div>

      <!-- 视图 A：业务推演模式 -->
      <div v-else-if="activeTab === 'business'" class="business-view">
        <div
          v-for="(node, idx) in formattedLogs"
          :key="node.id || idx"
          class="reasoning-card"
          :class="`is-${node.status}`"
        >
          <!-- 卡片头部 -->
          <div class="card-header" @click="toggleCard(idx)">
            <div class="card-header-left">
              <span class="card-index-pill">{{ String(idx + 1).padStart(2, '0') }}</span>
              <span class="card-title">{{ node.title }}</span>
            </div>
            <div class="card-header-right">
              <span class="card-state-tag" :class="`tag-${node.status}`">
                {{ node.statusText }}
              </span>
              <svg
                class="card-arrow"
                :class="{ 'is-open': openMap[idx] }"
                viewBox="0 0 24 24"
                width="14"
                height="14"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
              >
                <polyline points="6 9 12 15 18 9"/>
              </svg>
            </div>
          </div>

          <!-- 卡片展开体 -->
          <transition name="card-expand">
            <div v-if="openMap[idx]" class="card-body">
              <!-- 摘要说明 -->
              <div v-if="node.summary" class="node-summary-box">
                <span class="summary-label">推导摘要</span>
                <p class="summary-text">{{ node.summary }}</p>
              </div>

              <!-- 细分推导步骤 -->
              <div v-if="node.steps && node.steps.length" class="node-steps-flow">
                <div v-for="(s, sIdx) in node.steps" :key="sIdx" class="flow-step-row">
                  <span class="flow-step-icon">✔</span>
                  <span class="flow-step-text">{{ s }}</span>
                </div>
              </div>

              <!-- 如果有 SQL、图表、表格等插槽内容 -->
              <div class="node-slot-content">
                <slot name="content" :log="node.rawLog" :index="idx"></slot>
              </div>
            </div>
          </transition>
        </div>
      </div>

      <!-- 视图 B：底层技术溯源模式 -->
      <div v-else class="technical-view">
        <div v-for="(node, idx) in formattedLogs" :key="`tech-${idx}`" class="tech-card">
          <div class="tech-card-header">
            <div class="tech-card-title-row">
              <span class="tech-tag">STAGE {{ idx + 1 }}</span>
              <span class="tech-name">{{ node.title }}</span>
            </div>
            <span class="tech-status" :class="node.status">{{ node.statusText }}</span>
          </div>

          <div class="tech-card-body">
            <!-- 详细日志流 -->
            <div class="tech-log-console">
              <div v-for="(step, sIdx) in node.steps" :key="sIdx" class="tech-line">
                <span v-if="node.time" class="tech-line-time">[{{ node.time }}]</span>
                <span class="tech-line-content">{{ step }}</span>
              </div>
            </div>

            <!-- SQL 源码展示 -->
            <div v-if="node.rawLog?.sql" class="tech-sql-box">
              <div class="tech-sql-header">
                <span>生成查询 SQL 语句</span>
              </div>
              <pre class="tech-sql-code"><code>{{ node.rawLog.sql }}</code></pre>
            </div>
          </div>
        </div>
      </div>
    </div>
  </aside>
</template>

<script setup>
import { ref, computed, watch, reactive } from 'vue'

const props = defineProps({
  logs: {
    type: Array,
    default: () => []
  },
  status: {
    type: String,
    default: 'idle'
  }
})

defineEmits(['close'])

const activeTab = ref('business')
const openMap = reactive({})

// 4个业务推演阶段定义
const stages = [
  { key: 'intent', label: '意图拆解' },
  { key: 'metric', label: '口径对齐' },
  { key: 'extract', label: '数据萃取' },
  { key: 'insight', label: '洞察合成' }
]

const statusLabel = computed(() => {
  // 与会话状态机保持一致：idle / running / waiting_confirmation / completed / canceled / error
  const map = {
    running: '深度推演中',
    waiting_confirmation: '待口径确认',
    completed: '推演已就绪',
    canceled: '已取消',
    error: '推导中断',
    failed: '推导中断',
    idle: '推演待命中'
  }
  return map[props.status] || '准备就绪'
})

const isCompleted = computed(() => props.status === 'completed')

// 计算当前推导演进到第几个阶段
const currentStageIndex = computed(() => {
  if (props.status === 'completed') return 4
  const len = props.logs.length
  if (len === 0) return 0
  if (len <= 1) return 0
  if (len === 2) return 1
  if (len <= 4) return 2
  return 3
})

const hasSql = computed(() => props.logs.some(l => l.sql))

// 节点状态文案与会话日志状态对齐：success / running / pending / warning / error / canceled
const NODE_STATUS_TEXT = {
  success: '已完成',
  running: '推导中',
  pending: '等待中',
  warning: '需关注',
  error: '异常',
  canceled: '已取消'
}

// 格式化输出日志
const formattedLogs = computed(() => {
  return props.logs.map((log, index) => {
    const rawSteps = log.detailLines || (log.detail ? String(log.detail).split('\n') : [])
    const nodeStatus = log.status || 'success'
    return {
      id: log.key || `${index}`,
      title: log.title || `分析推演节点 ${index + 1}`,
      summary: log.summary,
      status: nodeStatus,
      statusText: NODE_STATUS_TEXT[nodeStatus] || '已完成',
      time: log.time || '',
      steps: rawSteps.filter(Boolean),
      rawLog: log
    }
  })
})

// 滚动容器：新日志到达/恢复历史会话时跟随到底部（执行中、待确认时）
const bodyRef = ref(null)
const FOLLOW_BOTTOM_STATUSES = ['running', 'waiting_confirmation']
const scrollToBottom = (behavior = 'auto') => {
  const el = bodyRef.value
  if (el) el.scrollTo({ top: el.scrollHeight, behavior })
}
const shouldFollowBottom = () => FOLLOW_BOTTOM_STATUSES.includes(props.status)

// 默认全部展开或展开最后一项
watch(() => props.logs.length, (newLen) => {
  if (newLen > 0) {
    props.logs.forEach((_, i) => {
      if (openMap[i] === undefined) {
        openMap[i] = true
      }
    })
  }
  if (shouldFollowBottom()) scrollToBottom('smooth')
}, { immediate: true })

// 恢复历史会话时 logs 整体替换为新数组（长度可能不变），引用变化即滚到底部
watch(() => props.logs, () => {
  if (shouldFollowBottom()) scrollToBottom('auto')
})

const toggleCard = (idx) => {
  openMap[idx] = !openMap[idx]
}
</script>

<style scoped>
.reasoning-panel {
  display: flex;
  flex-direction: column;
  height: 100%;
  min-height: 0;
  background: #fbfcfd;
  border-left: 1px solid #eef2f6;
  user-select: none;
  box-sizing: border-box;
  /* 与侧栏报告共用右侧容器：空间不足时由内部 panel-body 滚动，
     头部/步骤条绝不允许溢出绘制到报告卡片上 */
  overflow: hidden;
}

/* 顶部区域 */
.panel-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  padding: 18px 20px 14px;
  background: #ffffff;
  border-bottom: 1px solid #f1f5f9;
  flex: 0 0 auto;
}

.panel-header-main {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.panel-badge-row {
  display: flex;
  align-items: center;
  gap: 8px;
}

.panel-category-badge {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  padding: 2px 8px;
  border-radius: 4px;
  background: rgba(13, 148, 136, 0.08);
  color: #0d9488;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.02em;
}

.badge-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #0d9488;
}

.panel-status-tag {
  font-size: 11px;
  padding: 1px 7px;
  border-radius: 4px;
  font-weight: 600;
}

.status-running {
  background: #fef3c7;
  color: #d97706;
}

.status-completed {
  background: #dcfce7;
  color: #15803d;
}

.status-waiting_confirmation {
  background: #ffedd5;
  color: #c2410c;
}

.status-canceled {
  background: #fef3c7;
  color: #b45309;
}

.status-error,
.status-failed {
  background: #fee2e2;
  color: #b91c1c;
}

.status-idle {
  background: #f1f5f9;
  color: #64748b;
}

.panel-title {
  margin: 2px 0 0;
  font-size: 16px;
  font-weight: 800;
  color: #0f172a;
  letter-spacing: -0.01em;
}

.panel-desc {
  margin: 0;
  font-size: 11.5px;
  color: #64748b;
  line-height: 1.4;
}

.panel-close-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  border-radius: 6px;
  border: 1px solid #e2e8f0;
  background: #ffffff;
  color: #64748b;
  cursor: pointer;
  transition: all 0.15s ease;
}

.panel-close-btn:hover {
  background: #f1f5f9;
  color: #0f172a;
}

/* 4步流水进度指示条 */
.pipeline-stepper {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 18px;
  background: #ffffff;
  border-bottom: 1px solid #f1f5f9;
  flex: 0 0 auto;
}

.step-item {
  display: flex;
  align-items: center;
  gap: 6px;
  position: relative;
  flex: 1;
}

.step-item:last-child {
  flex: none;
}

.step-dot-wrap {
  width: 18px;
  height: 18px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 10px;
  font-weight: 700;
  background: #f1f5f9;
  color: #94a3b8;
  transition: all 0.2s ease;
}

.step-label {
  font-size: 11px;
  font-weight: 600;
  color: #94a3b8;
  white-space: nowrap;
}

.step-line {
  flex: 1;
  height: 1.5px;
  background: #e2e8f0;
  margin: 0 6px;
}

.step-item.is-done .step-dot-wrap {
  background: #0d9488;
  color: #ffffff;
}

.step-item.is-done .step-label {
  color: #0f172a;
}

.step-item.is-done .step-line {
  background: #0d9488;
}

.step-item.is-active .step-dot-wrap {
  background: #fef08a;
  color: #854d0e;
  box-shadow: 0 0 0 3px rgba(234, 179, 8, 0.2);
}

.step-item.is-active .step-label {
  color: #0d9488;
  font-weight: 700;
}

/* 标签切换栏 */
.panel-tabs {
  display: flex;
  padding: 6px 14px;
  gap: 8px;
  background: #f8fafc;
  border-bottom: 1px solid #eef2f6;
  flex: 0 0 auto;
}

.tab-btn {
  flex: 1;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  height: 32px;
  border-radius: 6px;
  border: 1px solid transparent;
  background: transparent;
  color: #64748b;
  font-size: 12.5px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.15s ease;
}

.tab-btn:hover {
  color: #0f172a;
  background: rgba(0, 0, 0, 0.03);
}

.tab-btn.is-active {
  background: #ffffff;
  color: #0d9488;
  border-color: #e2e8f0;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
}

.sql-badge {
  font-size: 9px;
  background: #0d9488;
  color: #ffffff;
  padding: 1px 4px;
  border-radius: 3px;
  font-weight: 700;
}

/* 滚动主体 */
.panel-body {
  flex: 1;
  overflow-y: auto;
  padding: 14px 16px;
  display: flex;
  flex-direction: column;
}

/* 空状态 */
.empty-state {
  margin: auto;
  text-align: center;
  padding: 40px 20px;
  max-width: 280px;
}

.compass-icon-wrap {
  margin-bottom: 14px;
}

.empty-title {
  font-size: 14px;
  font-weight: 700;
  color: #334155;
  margin: 0 0 6px;
}

.empty-desc {
  font-size: 12px;
  color: #94a3b8;
  line-height: 1.5;
  margin: 0;
}

/* 卡片布局（业务视图） */
.business-view {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.reasoning-card {
  border-radius: 8px;
  border: 1px solid #eef2f6;
  background: #ffffff;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.02);
  overflow: hidden;
  transition: all 0.2s ease;
}

.reasoning-card:hover {
  border-color: #cbd5e1;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 14px;
  cursor: pointer;
  background: #ffffff;
}

.card-header-left {
  display: flex;
  align-items: center;
  gap: 8px;
  min-width: 0;
}

.card-index-pill {
  font-size: 10px;
  font-weight: 800;
  color: #0d9488;
  background: rgba(13, 148, 136, 0.1);
  padding: 2px 5px;
  border-radius: 4px;
}

.card-title {
  font-size: 13px;
  font-weight: 700;
  color: #1e293b;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.card-header-right {
  display: flex;
  align-items: center;
  gap: 6px;
}

.card-state-tag {
  font-size: 11px;
  padding: 1px 6px;
  border-radius: 3px;
  font-weight: 600;
}

.tag-success {
  color: #059669;
  background: #ecfdf5;
}

.tag-running {
  color: #d97706;
  background: #fef3c7;
}

.tag-pending {
  color: #64748b;
  background: #f1f5f9;
}

.tag-warning {
  color: #b45309;
  background: #fef3c7;
}

.tag-error,
.tag-canceled {
  color: #b91c1c;
  background: #fee2e2;
}

/* 卡片按节点状态给左侧色条，扫一眼即可分辨执行情况 */
.reasoning-card {
  border-left: 3px solid transparent;
}

.reasoning-card.is-success {
  border-left-color: #10b981;
}

.reasoning-card.is-running {
  border-left-color: #f59e0b;
}

.reasoning-card.is-pending {
  border-left-color: #cbd5e1;
}

.reasoning-card.is-warning {
  border-left-color: #f59e0b;
}

.reasoning-card.is-error,
.reasoning-card.is-canceled {
  border-left-color: #ef4444;
}

.card-arrow {
  color: #94a3b8;
  transition: transform 0.2s ease;
}

.card-arrow.is-open {
  transform: rotate(180deg);
}

.card-body {
  padding: 0 14px 14px;
  border-top: 1px solid #f8fafc;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.node-slot-content {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-top: 2px;
}

/* 卡片展开/收起过渡 */
.card-expand-enter-active,
.card-expand-leave-active {
  transition: opacity 0.2s ease;
}

.card-expand-enter-from,
.card-expand-leave-to {
  opacity: 0;
}

.node-summary-box {
  margin-top: 10px;
  padding: 8px 10px;
  background: #f8fafc;
  border-left: 3px solid #0d9488;
  border-radius: 0 6px 6px 0;
}

.summary-label {
  font-size: 10.5px;
  font-weight: 700;
  color: #0d9488;
}

.summary-text {
  margin: 3px 0 0;
  font-size: 12px;
  color: #475569;
  line-height: 1.45;
}

.node-steps-flow {
  display: flex;
  flex-direction: column;
  gap: 5px;
  margin-top: 4px;
}

.flow-step-row {
  display: flex;
  align-items: flex-start;
  gap: 6px;
  font-size: 12px;
  color: #475569;
  line-height: 1.4;
}

.flow-step-icon {
  color: #0d9488;
  font-size: 11px;
  margin-top: 1px;
}

/* 技术视图 */
.technical-view {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.tech-card {
  border-radius: 8px;
  background: #ffffff;
  border: 1px solid #e2e8f0;
  padding: 12px;
}

.tech-card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 8px;
}

.tech-tag {
  font-size: 9.5px;
  font-weight: 800;
  background: #334155;
  color: #ffffff;
  padding: 1px 5px;
  border-radius: 3px;
  letter-spacing: 0.05em;
}

.tech-name {
  font-size: 12.5px;
  font-weight: 700;
  color: #0f172a;
  margin-left: 6px;
}

.tech-log-console {
  background: #0f172a;
  border-radius: 6px;
  padding: 10px 12px;
  font-family: ui-monospace, 'JetBrains Mono', monospace;
  font-size: 11px;
  color: #94a3b8;
  max-height: 140px;
  overflow-y: auto;
  line-height: 1.5;
}

.tech-line-time {
  color: #64748b;
  margin-right: 6px;
}

.tech-line-content {
  color: #cbd5e1;
}

.tech-sql-box {
  margin-top: 10px;
}

.tech-sql-header {
  font-size: 11px;
  font-weight: 700;
  color: #475569;
  margin-bottom: 4px;
}

.tech-sql-code {
  margin: 0;
  padding: 10px;
  border-radius: 6px;
  background: #1e293b;
  color: #38bdf8;
  font-size: 11.5px;
  overflow-x: auto;
  line-height: 1.5;
}
</style>
