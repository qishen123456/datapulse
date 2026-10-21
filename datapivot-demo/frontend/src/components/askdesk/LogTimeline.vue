<template>
  <div class="ax-timeline">
    <div v-if="logs.length === 0" class="ax-empty">
      <div class="ax-empty-icon" aria-hidden="true">
        <span></span><span></span><span></span>
      </div>
      <p>执行事件会在这里持续更新</p>
    </div>

    <div v-for="(log, i) in logs" :key="getNodeKey(log, i)" class="ax-log-node" :class="log.status">
      <span class="ax-node-marker" :class="log.status"></span>

      <div class="ax-node-main">
        <div class="ax-node-header" @click="$emit('toggle', i)">
          <span class="ax-node-arrow" :class="{ open: openState[i] }">▶</span>
          <span class="ax-node-icon" :class="iconClass(log)" aria-hidden="true"></span>
          <span class="ax-node-title">{{ log.title }}</span>
          <span v-if="log.status === 'running'" class="ax-spin">◌</span>
          <span class="ax-node-status" :class="log.status">{{ nodeStatusText(log) }}</span>
        </div>

        <transition name="ax-collapse">
          <div v-if="openState[i]" class="ax-node-body">
            <div class="ax-node-body-head">
              <span class="ax-node-body-label">{{ sectionLabel(log) }}</span>
            </div>

            <div v-if="log.summary && !isDurationLine(log.summary)" class="ax-node-summary">{{ log.summary }}</div>

            <div v-if="compactThought(log) && !latestLiveThought(log) && isThoughtVisible(log, i)" class="ax-node-thought">
              <span class="ax-node-thought-label">执行摘要</span>
              <p>{{ compactThought(log) }}</p>
            </div>

            <div v-if="latestLiveThought(log)" class="ax-node-live-thought">
              <div class="ax-node-live-head">
                <span class="ax-live-pulse-dot"></span>
                <span>{{ liveThoughtLabel(log) }}</span>
              </div>
              <div ref="liveLineRef" class="ax-node-live-line">
                <div
                  v-for="(line, lineIndex) in compactLiveThoughtLines(log)"
                  :key="`${lineIndex}-${line}`"
                  class="ax-node-live-check"
                  :class="{ latest: lineIndex === compactLiveThoughtLines(log).length - 1 }"
                >
                  <span class="ax-node-live-check-dot"></span>
                  <span>{{ line }}</span>
                </div>
              </div>
            </div>

            <div class="ax-log-steps">
              <div
                v-for="(line, lineIndex) in visibleDetailLines(log, i)"
                :key="`${getNodeKey(log, i)}-${lineIndex}`"
                class="ax-log-step"
              >
                <span class="ax-log-step-dot"></span>
                <span class="ax-log-step-text">{{ line }}</span>
              </div>

              <div v-if="hasPendingLines(log, i)" class="ax-log-step ax-log-step-printing">
                <span class="ax-log-step-dot"></span>
                <span class="ax-log-step-text">
                  正在整理更多细节
                  <span class="ax-print-cursor"></span>
                </span>
              </div>
            </div>

            <div v-if="isContentVisible(log, i)" class="ax-node-rich">
              <slot name="content" :log="log" :index="i"></slot>
            </div>

          </div>
        </transition>
      </div>
    </div>
  </div>
</template>

<script setup>
import { nextTick, onBeforeUnmount, reactive, ref, watch } from 'vue'

const props = defineProps({
  logs: {
    type: Array,
    default: () => []
  },
  openState: {
    type: Object,
    default: () => ({})
  }
})

defineEmits(['toggle'])

const revealState = reactive({})
const revealTimers = new Map()
const clockNow = ref(Date.now())
const liveLineRef = ref(null)
const clockTimer = setInterval(() => {
  clockNow.value = Date.now()
}, 1000)
let liveLineScrollTimer = null

const statusLabel = (status) => ({
  success: '已完成',
  running: '执行中',
  pending: '待执行',
  error: '异常',
  warning: '待确认'
}[status] || status)

const isCanceledLog = (log = {}) => /取消|停止|request-aborted|aborted|canceled|cancelled/i.test(
  `${log?.key || ''} ${log?.title || ''} ${log?.summary || ''}`,
)

const getNodeKey = (log, index) => log?.key || `${log?.title || 'node'}-${index}`

const detailLines = (log) => {
  const summaryKey = normalizeDisplayLine(log?.summary)
  const withoutSummaryDuplicate = (lines) => lines.filter(line => normalizeDisplayLine(line) !== summaryKey)
  if (Array.isArray(log?.detailLines) && log.detailLines.length > 0) {
    return uniqueDisplayLines(withoutSummaryDuplicate(log.detailLines)
      .map(item => String(item || '').trim())
      .filter(Boolean)
      .filter(line => !isDurationLine(line) && !isRedundantRealtimePrintLine(line)))
  }

  const lines = [`开始执行任务：${log?.title || '执行节点'}`]

  if (log?.detail) {
    lines.push(
      ...String(log.detail)
        .split(/\n+/)
        .map(item => item.trim())
        .filter(Boolean)
    )
  }

  if (log?.status === 'success') lines.push('当前节点执行完成。')
  if (log?.status === 'running') lines.push('当前节点仍在执行中。')
  if (log?.status === 'warning') lines.push('当前节点等待进一步确认。')
  if (log?.status === 'error') lines.push('当前节点执行失败，请查看错误信息。')

  return uniqueDisplayLines(lines.filter(line => !isDurationLine(line) && !isRedundantRealtimePrintLine(line)))
}

const isDurationLine = (line) => {
  const text = String(line || '')
    .trim()
    .replace(/^[•·\-\s]+/, '')
    .replace(/[。；;,.，、\s]+$/g, '')
  return /节点耗时|当前节点耗时|当前节点已运行|^已运行\s*[\dm.\s]+s?$|^耗时\s*[\dm.\s]+s?$/i.test(text)
}

const isRedundantRealtimePrintLine = (line) => {
  const text = normalizeDisplayLine(line)
  return text.includes('模型正在实时返回真实内容') && text.includes('逐段打印')
}

const normalizeDisplayLine = (line) => String(line || '')
  .trim()
  .replace(/\s+/g, ' ')
  .replace(/[。；;,.，、\s]+$/g, '')

const uniqueDisplayLines = (lines = []) => {
  const seen = new Set()
  return lines.filter((line) => {
    const key = normalizeDisplayLine(line)
    if (!key || seen.has(key)) return false
    seen.add(key)
    return true
  })
}

const iconClass = (log) => {
  const toolType = log?.toolType || ''
  if (toolType === 'sql') return 'sql'
  if (toolType === 'dataset') return 'dataset'
  if (toolType === 'report' || toolType === 'fact') return 'report'
  if (toolType === 'confirm') return 'confirm'
  if (toolType === 'python') return 'python'
  const text = `${log?.key || ''} ${log?.title || ''}`
  if (/sql|查询/i.test(text)) return 'sql'
  if (/数据表|数据集|schema/i.test(text)) return 'dataset'
  if (/结果|报告|分析|事实|计划/i.test(text)) return 'report'
  if (/确认|口径/i.test(text)) return 'confirm'
  if (/python|pandas/i.test(text)) return 'python'
  return 'default'
}

const sectionLabel = (log) => {
  if (log?.kind === 'report-stage') return '报告节点'
  if (log?.kind === 'fact-update') return '事实更新'
  if (log?.kind === 'confirmation') return '确认节点'
  return '执行记录'
}

const formatDuration = (duration) => {
  const value = Number(duration)
  if (!Number.isFinite(value) || value <= 0) return ''
  const totalSeconds = Math.max(1, Math.round(value / 1000))
  const minutes = Math.floor(totalSeconds / 60)
  const remain = totalSeconds % 60
  if (minutes > 0) return `${minutes}m ${remain}s`
  return `${totalSeconds}s`
}

const nodeDurationLabel = (log) => {
  const startedAtMs = Number(log?.startedAtMs)
  if (log?.status === 'running' && Number.isFinite(startedAtMs)) {
    return formatDuration(clockNow.value - startedAtMs)
  }
  return log?.durationLabel || log?.elapsedLabel || ''
}

const nodeStatusText = (log) => {
  const base = isCanceledLog(log) ? '已取消' : statusLabel(log?.status)
  const duration = nodeDurationLabel(log)
  if (!duration || log?.status === 'pending') return base
  return `${base} ${duration}`
}

const latestLiveThought = (log) => {
  if (log?.status !== 'running') return ''
  if (Array.isArray(log?.liveThoughtLines) && log.liveThoughtLines.length > 0) {
    return log.liveThoughtLines[log.liveThoughtLines.length - 1]
  }
  if (Array.isArray(log?.thoughtLines) && log.thoughtLines.length > 0 && log?.status === 'running') {
    return log.thoughtLines[log.thoughtLines.length - 1]
  }
  return ''
}

const isReportNode = (log = {}) => /报告|分析结论|经营分析|agent4/i.test(`${log?.key || ''} ${log?.title || ''}`)

const isJsonLike = (value) => {
  const text = String(value || '').trim()
  return text.startsWith('{') || text.startsWith('[') || /^```json/i.test(text)
}

const parseJsonPreview = (value) => {
  const text = String(value || '')
    .trim()
    .replace(/^```json\s*/i, '')
    .replace(/```$/i, '')
    .trim()
  try {
    return JSON.parse(text)
  } catch (error) {
    return null
  }
}

const structuredProgressPreview = (value, log = {}) => {
  const raw = String(value || '').trim()
  const scope = `${log?.key || ''} ${log?.title || ''} ${log?.summary || ''}`
  if (/^SQL片段：/i.test(raw)) {
    return raw.replace(/\s+/g, ' ').slice(0, 150)
  }
  if (/<\/?think>|dataset_id|option_id|score_hint|confirm_question|need_confirm/i.test(raw)) {
    if (/理解|路由|口径|agent1/i.test(scope)) return '正在识别问题意图，并比较候选数据范围。'
    if (/确认|confirm/i.test(scope)) return '正在整理需要确认的统计口径。'
    return '正在接收后端实时执行进度。'
  }
  if (/WITH\s+|SELECT\s+|FROM\s+/i.test(raw) || /生成.*SQL|SQL/i.test(scope)) {
    return /复核|校验|review|agent3/i.test(scope)
      ? '模型正在复核 SQL 口径，完整语句已放到下方详情。'
      : '模型正在生成 SQL，完整语句已放到下方详情。'
  }
  if (!isJsonLike(raw)) return ''

  const data = parseJsonPreview(raw)
  if (data?.need_confirm || data?.confirm_question || Array.isArray(data?.options)) {
    return '模型正在判断是否需要口径确认，确认项会整理成可读卡片。'
  }
  if (data?.sql) return '模型正在生成 SQL，完整语句已放到下方详情。'
  if (data?.analysis || data?.report || data?.conclusion) return '模型正在生成分析摘要，完整报告会在下方展示。'
  return '模型正在返回结构化结果，系统会整理成可读内容。'
}

const cleanupMarkdownPreview = (value) => String(value || '')
  .replace(/```[\s\S]*?```/g, ' ')
  .replace(/`([^`]+)`/g, '$1')
  .replace(/^#{1,6}\s*/gm, '')
  .replace(/\*\*([^*]+)\*\*/g, '$1')
  .replace(/^\s*[•*-]\s*/gm, '')
  .replace(/\s*->\s*/g, '：')
  .replace(/\s+/g, ' ')
  .trim()

const pickReportConclusion = (text) => {
  const cleaned = cleanupMarkdownPreview(text)
  const match = cleaned.match(/核心结论[:：]?\s*([^。！？\n]{8,120}[。！？]?)/)
  if (match?.[1]) return `报告摘要：${match[1].trim()}`
  const firstSentence = cleaned.split(/[。！？]/).find(item => item.trim().length >= 8)
  return firstSentence ? `报告摘要：${firstSentence.trim()}。` : cleaned
}

const compactPreview = (value, log = {}, limit = 120) => {
  const raw = String(value || '').trim()
  if (!raw) return ''
  const structured = structuredProgressPreview(raw, log)
  if (structured) return structured
  const text = isReportNode(log) ? pickReportConclusion(raw) : cleanupMarkdownPreview(raw)
  if (text.length <= limit) return text
  return `${text.slice(0, limit).replace(/[，、；：,.:\s]+$/, '')}...`
}

const compactThought = (log) => {
  if (log?.markdown && log?.status !== 'running') return ''
  return compactPreview(log?.thought, log, 112)
}

const compactLiveThoughtLines = (log) => {
  const lines = Array.isArray(log?.liveThoughtLines) && log.liveThoughtLines.length > 0
    ? log.liveThoughtLines
    : [latestLiveThought(log)]
  return Array.from(new Set(
    lines
      .map(line => compactPreview(line, log, 128))
      .filter(Boolean)
      .filter(line => line !== '模型正在实时返回真实内容，已切换为逐段打印。')
  )).slice(-4)
}

const liveThoughtLabel = (log) => {
  if (log?.liveThoughtSource === 'llm-reasoning') return '实时推理进度'
  if (log?.liveThoughtSource === 'llm-stream') return '实时生成进度'
  return '执行摘要'
}

const buildRevealSignature = (log) => {
  const lines = detailLines(log)
  return [
    log?.status || '',
    lines.length,
    log?.sql ? 'has-sql' : '',
    log?.markdown ? 'has-markdown' : '',
    log?.chartData ? 'has-chart' : '',
    Array.isArray(log?.tableRows) ? log.tableRows.length : 0,
    Array.isArray(log?.charts) ? log.charts.length : 0
  ].join('::')
}

const ensureRevealState = (key) => {
  if (!revealState[key]) {
    revealState[key] = {
      signature: '',
      thoughtVisible: false,
      visibleSteps: 0,
      contentVisible: false,
      initialized: false
    }
  }
  return revealState[key]
}

const clearNodeTimers = (key) => {
  const handles = revealTimers.get(key) || []
  handles.forEach((handle) => {
    clearTimeout(handle)
    clearInterval(handle)
  })
  revealTimers.delete(key)
}

const pushTimer = (key, handle) => {
  const current = revealTimers.get(key) || []
  current.push(handle)
  revealTimers.set(key, current)
}

const hasRichContent = (log) => {
  if (log?.sql) return true
  if (log?.markdown) return true
  if (Array.isArray(log?.tableRows) && log.tableRows.length > 0) return true
  if (Array.isArray(log?.charts) && log.charts.length > 0) return true
  if (Array.isArray(log?.tables) && log.tables.length > 0) return true
  if (Array.isArray(log?.codeBlocks) && log.codeBlocks.length > 0) return true
  if (log?.chartData) return true
  return false
}

const startReveal = (log, index) => {
  const key = getNodeKey(log, index)
  const state = ensureRevealState(key)
  const lines = detailLines(log)
  const rich = hasRichContent(log)

  clearNodeTimers(key)
  state.signature = buildRevealSignature(log)
  state.initialized = true
  state.thoughtVisible = !log?.thought
  state.visibleSteps = 0
  state.contentVisible = false

  if (log?.thought) {
    pushTimer(key, setTimeout(() => {
      state.thoughtVisible = true
    }, 120))
  }

  if (lines.length === 0) {
    pushTimer(key, setTimeout(() => {
      state.contentVisible = true
    }, log?.thought ? 240 : 120))
    return
  }

  let cursor = 0
  const revealNext = () => {
    cursor = Math.min(cursor + 1, lines.length)
    state.visibleSteps = cursor

    if (cursor >= lines.length) {
      clearNodeTimers(key)
      if (rich) {
        pushTimer(key, setTimeout(() => {
          state.contentVisible = true
        }, 140))
      } else {
        state.contentVisible = true
      }
    }
  }

  const starter = setTimeout(() => {
    revealNext()
    const interval = setInterval(() => {
      revealNext()
      if (cursor >= lines.length) {
        clearInterval(interval)
      }
    }, 180)
    pushTimer(key, interval)
  }, log?.thought ? 190 : 80)

  pushTimer(key, starter)
}

const syncRevealState = () => {
  const activeKeys = new Set()

  props.logs.forEach((log, index) => {
    const key = getNodeKey(log, index)
    activeKeys.add(key)
    const state = ensureRevealState(key)
    const signature = buildRevealSignature(log)

    if (props.openState[index]) {
      if (!state.initialized || state.signature !== signature) {
        startReveal(log, index)
      }
    } else {
      clearNodeTimers(key)
      state.signature = signature
      state.initialized = false
      state.thoughtVisible = true
      state.visibleSteps = detailLines(log).length
      state.contentVisible = true
    }
  })

  Object.keys(revealState).forEach((key) => {
    if (!activeKeys.has(key)) {
      clearNodeTimers(key)
      delete revealState[key]
    }
  })
}

const visibleDetailLines = (log, index) => {
  const key = getNodeKey(log, index)
  const state = ensureRevealState(key)
  return detailLines(log).slice(0, state.visibleSteps)
}

const hasPendingLines = (log, index) => {
  const key = getNodeKey(log, index)
  const state = ensureRevealState(key)
  return state.visibleSteps < detailLines(log).length
}

const isThoughtVisible = (log, index) => {
  const key = getNodeKey(log, index)
  return ensureRevealState(key).thoughtVisible
}

const isContentVisible = (log, index) => {
  const key = getNodeKey(log, index)
  return ensureRevealState(key).contentVisible
}

watch(
  () => props.logs.map((log, index) => ({
    key: getNodeKey(log, index),
    open: Boolean(props.openState[index]),
    signature: buildRevealSignature(log)
  })),
  syncRevealState,
  { deep: true, immediate: true }
)

const clearLiveLineScrollTimer = () => {
  if (liveLineScrollTimer) {
    clearInterval(liveLineScrollTimer)
    liveLineScrollTimer = null
  }
}

const scrollLiveLineToBottom = () => nextTick(() => {
  const el = Array.isArray(liveLineRef.value)
    ? liveLineRef.value[liveLineRef.value.length - 1]
    : liveLineRef.value
  if (!el) return
  el.scrollTop = el.scrollHeight
})

watch(
  () => props.logs.map(log => `${log?.status || ''}:${Array.isArray(log?.liveThoughtLines) ? log.liveThoughtLines.join('|') : ''}:${log?.pulseText || ''}:${log?.streamText || ''}`).join('||'),
  () => {
    clearLiveLineScrollTimer()
    scrollLiveLineToBottom()
    liveLineScrollTimer = setInterval(scrollLiveLineToBottom, 300)
  },
  { immediate: true }
)

onBeforeUnmount(() => {
  clearInterval(clockTimer)
  clearLiveLineScrollTimer()
  Array.from(revealTimers.keys()).forEach(clearNodeTimers)
})
</script>

<style scoped>
.ax-timeline {
  padding: 18px 18px 20px;
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.ax-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 520px;
  padding: 72px 20px 56px;
  color: var(--text-muted);
  text-align: center;
}

.ax-empty-icon {
  position: relative;
  width: 148px;
  height: 120px;
  border-radius: 8px;
  border: 0;
  background: transparent;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  gap: 8px;
  padding: 34px 34px 0;
  margin-bottom: 26px;
  box-shadow: none;
}

.ax-empty-icon span {
  position: relative;
  z-index: 1;
  height: 8px;
  border-radius: 999px;
  background: rgba(17, 24, 39, 0.1);
}

.ax-empty-icon span:nth-child(1) { width: 70%; }
.ax-empty-icon span:nth-child(2) { width: 100%; }
.ax-empty-icon span:nth-child(3) { width: 55%; }

.ax-empty-icon::before {
  content: '';
  position: absolute;
  left: 24px;
  right: 24px;
  top: 20px;
  height: 86px;
  border-radius: 8px;
  background:
    linear-gradient(180deg, rgba(255, 255, 255, 0.96) 0%, rgba(247, 248, 250, 0.96) 100%);
  border: 1px solid rgba(17, 24, 39, 0.06);
  box-shadow:
    0 18px 34px rgba(15, 23, 42, 0.055),
    inset 0 -4px 0 rgba(13, 148, 136, 0.06);
  transform: perspective(260px) rotateX(18deg);
}

.ax-empty-icon::after {
  content: '';
  position: absolute;
  right: 19px;
  bottom: 10px;
  width: 42px;
  height: 42px;
  border-radius: 50%;
  border: 6px solid rgba(13, 148, 136, 0.68);
  background: rgba(255, 255, 255, 0.78);
  box-shadow: 0 14px 24px rgba(13, 148, 136, 0.12);
}

.ax-empty p {
  margin: 0;
  color: #111827;
  font-size: 17px;
  font-weight: 800;
  line-height: 1.45;
}

.ax-log-node {
  position: relative;
  display: flex;
  gap: 10px;
  padding-bottom: 1px;
}

.ax-log-node:not(:last-child)::after {
  content: '';
  position: absolute;
  left: 7px;
  top: 16px;
  bottom: -16px;
  width: 1px;
  background: linear-gradient(180deg, rgba(229, 231, 235, 1) 0%, rgba(229, 231, 235, 0.32) 100%);
}

.ax-node-marker {
  position: relative;
  z-index: 1;
  width: 14px;
  height: 14px;
  border-radius: 50%;
  margin-top: 13px;
  flex-shrink: 0;
  background: #D1D5DB;
  border: 2px solid #fff;
  box-shadow: 0 0 0 1px #E5E7EB;
}

.ax-node-marker.success {
  background: #10B981;
  box-shadow: 0 0 0 1px rgba(16, 185, 129, 0.16);
}

.ax-node-marker.running {
  background: #1A1A1A;
  box-shadow: 0 0 0 1px rgba(26, 26, 26, 0.16);
}

.ax-node-marker.error {
  background: #1A1A1A;
  box-shadow: 0 0 0 1px rgba(26, 26, 26, 0.16);
}

.ax-node-marker.warning {
  background: #F59E0B;
  box-shadow: 0 0 0 1px rgba(245, 158, 11, 0.16);
}

.ax-node-main {
  flex: 1;
  min-width: 0;
  padding-right: 1px;
}

.ax-node-header {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 0;
  cursor: pointer;
  background: transparent;
  transition: background 0.1s;
}

.ax-node-arrow {
  font-size: 12px;
  color: #9CA3AF;
  transition: transform 0.2s;
  flex-shrink: 0;
}

.ax-node-arrow.open {
  transform: rotate(90deg);
}

.ax-node-icon {
  width: 18px;
  height: 18px;
  border-radius: 6px;
  background: linear-gradient(180deg, #F2F5F4 0%, #FFFFFF 100%);
  border: 1px solid rgba(17, 24, 39, 0.12);
  position: relative;
  flex-shrink: 0;
}

.ax-node-icon::before,
.ax-node-icon::after {
  content: '';
  position: absolute;
  left: 3px;
  right: 3px;
  height: 1px;
  background: rgba(26, 26, 26, 0.46);
}

.ax-node-icon::before { top: 5px; }
.ax-node-icon::after { top: 9px; }

.ax-node-icon.dataset {
  background: linear-gradient(180deg, #ECFDF5 0%, #ECFDF5 100%);
  border-color: rgba(16, 185, 129, 0.16);
}

.ax-node-icon.dataset::before,
.ax-node-icon.dataset::after {
  background: rgba(16, 185, 129, 0.4);
}

.ax-node-icon.report {
  background: linear-gradient(180deg, #FFFBEB 0%, #FFFBEB 100%);
  border-color: rgba(245, 158, 11, 0.18);
}

.ax-node-icon.report::before,
.ax-node-icon.report::after {
  background: rgba(245, 158, 11, 0.45);
}

.ax-node-icon.confirm {
  background: linear-gradient(180deg, #F0FDFA 0%, #F0FDFA 100%);
  border-color: rgba(26, 26, 26, 0.16);
}

.ax-node-icon.confirm::before,
.ax-node-icon.confirm::after {
  background: rgba(26, 26, 26, 0.4);
}

.ax-node-icon.python {
  background: linear-gradient(180deg, #F0FDFA 0%, #F0FDFA 100%);
  border-color: rgba(107, 114, 128, 0.16);
}

.ax-node-icon.python::before,
.ax-node-icon.python::after {
  background: rgba(107, 114, 128, 0.4);
}

.ax-node-title {
  flex: 1;
  font-size: 12px;
  font-weight: 700;
  color: #111827;
  line-height: 1.4;
}

.ax-node-status {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  justify-content: flex-end;
  min-width: 64px;
  padding: 0 1px;
  font-size: 11px;
  font-weight: 600;
  white-space: nowrap;
  letter-spacing: 0.01em;
  font-variant-numeric: tabular-nums;
}

.ax-node-status::before {
  content: '';
  width: 5px;
  height: 5px;
  border-radius: 50%;
  background: currentColor;
  opacity: 0.9;
}

.ax-node-status.success { color: #10B981; }
.ax-node-status.running { color: #1A1A1A; }
.ax-node-status.error { color: #1A1A1A; }
.ax-node-status.pending { color: #9CA3AF; }
.ax-node-status.warning { color: #F59E0B; }

.ax-spin {
  color: #1A1A1A;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.ax-node-body {
  margin: 4px 0 0;
  padding: 12px 14px;
  background: linear-gradient(180deg, #ffffff 0%, #fbfcfd 100%);
  border: 1px solid rgba(229, 231, 235, 0.95);
  border-radius: 6px;
  box-shadow: 0 10px 18px rgba(15, 23, 42, 0.035);
}

.ax-node-body-head {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  gap: 8px;
  margin-bottom: 7px;
}

.ax-node-body-label {
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #9CA3AF;
}

.ax-log-steps {
  display: flex;
  flex-direction: column;
  gap: 5px;
  margin-bottom: 7px;
}

.ax-node-summary {
  margin-bottom: 7px;
  font-size: 10px;
  line-height: 1.6;
  color: #111827;
}

.ax-node-thought {
  margin-bottom: 7px;
  padding: 7px 9px;
  border-radius: 4px;
  background: #F2F5F4;
  border: 1px solid rgba(229, 230, 235, 0.9);
}

.ax-node-thought-label {
  display: inline-flex;
  margin-bottom: 4px;
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #9CA3AF;
}

.ax-node-thought p {
  margin: 0;
  font-size: 10px;
  line-height: 1.55;
  color: #6B7280;
}

.ax-node-live-thought {
  margin: 0 0 8px;
  padding: 6px 8px;
  height: 92px;
  box-sizing: border-box;
  border-radius: 4px;
  border: 1px solid rgba(229, 233, 242, 0.74);
  background: linear-gradient(180deg, #FFFFFF 0%, #F2F5F4 100%);
  overflow: hidden;
}

.ax-node-live-head {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-bottom: 3px;
  font-size: 9px;
  font-weight: 600;
  letter-spacing: 0.04em;
  color: #9CA3AF;
}

.ax-live-pulse-dot {
  width: 3px;
  height: 3px;
  border-radius: 50%;
  background: #1A1A1A;
  box-shadow: 0 0 0 2px rgba(26, 26, 26, 0.05);
  animation: saLivePulse 1.3s ease-in-out infinite;
}

.ax-node-live-line {
  height: 60px;
  overflow-y: auto;
  padding-right: 3px;
  white-space: normal;
  font-size: 10px;
  line-height: 1.55;
  color: #6B7280;
}

.ax-node-live-line::-webkit-scrollbar {
  width: 3px;
}

.ax-node-live-line::-webkit-scrollbar-thumb {
  background: #D1D5DB;
  border-radius: 4px;
}

.ax-node-live-check {
  display: flex;
  align-items: flex-start;
  gap: 6px;
  min-height: 18px;
  color: #9CA3AF;
}

.ax-node-live-check.latest {
  color: #6B7280;
}

.ax-node-live-check-dot {
  width: 4px;
  height: 4px;
  margin-top: 6px;
  border-radius: 50%;
  background: #9CA3AF;
  flex-shrink: 0;
}

.ax-node-live-check.latest .ax-node-live-check-dot {
  background: #1A1A1A;
  box-shadow: 0 0 0 3px rgba(26, 26, 26, 0.06);
}

.ax-log-step {
  display: flex;
  align-items: flex-start;
  gap: 8px;
}

.ax-log-step-dot {
  width: 6px;
  height: 6px;
  margin-top: 7px;
  border-radius: 50%;
  background: #1A1A1A;
  flex-shrink: 0;
}

.ax-log-step-text {
  font-size: 10px;
  color: #6B7280;
  line-height: 1.6;
}

.ax-log-step-printing .ax-log-step-text {
  color: #9CA3AF;
}

.ax-print-cursor {
  display: inline-flex;
  width: 7px;
  height: 12px;
  margin-left: 5px;
  border-right: 2px solid #1A1A1A;
  animation: blink 0.9s steps(1, end) infinite;
  vertical-align: -2px;
}

@keyframes blink {
  0%, 49% { opacity: 1; }
  50%, 100% { opacity: 0; }
}

@keyframes saLivePulse {
  0%, 100% {
    transform: scale(0.9);
    opacity: 0.62;
  }
  50% {
    transform: scale(1.12);
    opacity: 1;
  }
}

.ax-node-rich {
  animation: none;
}

@keyframes revealContent {
  from {
    opacity: 0;
    transform: translateY(4px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.ax-log-time {
  font-size: 10px;
  color: #9CA3AF;
  margin-top: 4px;
}

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
  max-height: 1200px;
}
</style>
