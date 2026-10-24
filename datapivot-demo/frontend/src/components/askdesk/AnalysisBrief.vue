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
