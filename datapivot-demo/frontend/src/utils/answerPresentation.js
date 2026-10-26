// Presentation reads returned facts only. No made-up totals, rates, or confidence.
export function queryFailed(dataset = {}) {
  return dataset.query_status === 'failed' ||
    (dataset.query_status !== 'completed' && dataset.agent3_review?.approved === false && !(dataset.rows?.length))
}
export function numericColumns(dataset = {}) {
  const rows = Array.isArray(dataset.rows) ? dataset.rows : []
  return (dataset.columns || Object.keys(rows[0] || {})).filter(key =>
    !/(^id$|_id$|_code$|编码|序号|年度$|年份$|排名)/i.test(key) &&
    rows.some(row => typeof row[key] === 'number' && Number.isFinite(row[key])))
}
export function dimensionColumn(dataset = {}, metric = '') {
  const rows = dataset.rows || []
  const columns = dataset.columns || Object.keys(rows[0] || {})
  const candidates = columns.filter(key => key !== metric && rows.some(row => typeof row[key] === 'string'))
  const varying=candidates.filter(key=>new Set(rows.map(row=>row[key]).filter(value=>value!=null)).size>1)
  const pool=varying.length?varying:candidates
  return pool.find(key=>/name|名称|分公司|组织|地区|战区|客户|区域/i.test(key)) || pool.find(key=>/月份|日期|month|date/i.test(key)) || pool[0] || ''
}
// Proportions are displayed as %, while raw query values remain unchanged.
// An explicit percent format/unit already uses percentage points (legacy report contract).
export function percentageScale(column = '', dataset = {}) {
  const name = String(column || '')
  dataset ||= {}
  const definitions = [...(Array.isArray(dataset.report_config?.metrics) ? dataset.report_config.metrics : []), ...(Array.isArray(dataset.column_metadata) ? dataset.column_metadata : [])]
  const definition = definitions.find(item => [item.column,item.key,item.name].includes(name))
  if (definition?.format === 'ratio') return 100
  if (definition?.format === 'percent' || definition?.unit === '%') return 1
  if (/%|％|百分比|百分点|(?:^|_)(?:pct|percent|percentage)(?:_|$)/i.test(name)) return 1
  if (/(?:分子|分母|增量|增减量|变化量|差额|金额|户数|气量)$|(?:_|\b)(?:元|万元|亿元|方|万方|亿方|户|户次|公里|千米|笔|次|天)$/i.test(name)) return null
  return /率|占比|环比|同比|增幅|降幅|(?:^|_)(?:rate|ratio|share|yoy|mom|growth_rate)(?:_|$)/i.test(name) ? 100 : null
}
export function formatMetric(value, column = '', dataset = {}) {
  if (typeof value === 'string' && /[%％]$/.test(value.trim())) return value
  const scale = percentageScale(column, dataset)
  if (scale === null || value == null || value === '') return formatFact(value)
  const numeric = typeof value === 'number' ? value : typeof value === 'string' && /^[-+]?\d+(?:\.\d+)?$/.test(value.trim()) ? Number(value) : NaN
  return Number.isFinite(numeric) ? `${new Intl.NumberFormat('zh-CN',{maximumFractionDigits:2}).format(numeric * scale)}%` : formatFact(value)
}
export function formatMetricDifference(value, column = '', dataset = {}) {
  const display = formatMetric(value, column, dataset)
  return percentageScale(column, dataset) === null ? display : display.replace(/%$/, ' 个百分点')
}
export function formatFact(value) {
  if (value === null || value === undefined || value === '') return '—'
  if (typeof value === 'number') return Number.isFinite(value) ? new Intl.NumberFormat('zh-CN',{maximumFractionDigits:4}).format(value) : '—'
  return typeof value === 'object' ? JSON.stringify(value) : String(value)
}
export function escapeHtml(value) {
  return String(value ?? '').replace(/[&<>"']/g, char => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]))
}
/**
 * 轻量 markdown → HTML 渲染（2026-10-25）。
 * 背景：Agent4 报告含 **加粗**、## 标题、【】节题、管道表格、列表，此前屏幕/下载均按纯文本展示，
 * "**【核心结论】 **"（闭合符前带空格）这类瑕疵语法会原文裸露，报告显得"不稳定"。
 * 安全：先整体 escapeHtml，再对白名单语法替换；不引入第三方依赖。
 */
export function renderMarkdownHtml(text) {
  const raw = String(text || '').replace(/\r\n?/g, '\n')
  if (!raw.trim()) return ''
  const inline = (value) => escapeHtml(value)
    .replace(/\*\*\s*([^*]+?)\s*\*\*/g, '<strong>$1</strong>')
    .replace(/(?<!\*)\*(?!\*)([^*\n]+?)\*(?!\*)/g, '<em>$1</em>')
    .replace(/`([^`\n]+)`/g, '<code>$1</code>')
    .replace(/\*\*/g, '')
  const splitRow = (line) => line.trim().replace(/^\|/, '').replace(/\|$/, '').split('|').map(cell => cell.trim())
  const isTableLine = (line) => /^\s*\|.*\|/.test(line)
  const isSeparator = (line) => /^\s*\|[\s:|-]*-[\s:|-]*\|?\s*$/.test(line)
  const isBullet = (line) => /^\s*(?:[-*•·]|\d+[.、)])\s+/.test(line)
  const bulletText = (line) => line.replace(/^\s*(?:[-*•·]|\d+[.、)])\s+/, '')
  const blocks = []
  const lines = raw.split('\n')
  let i = 0
  while (i < lines.length) {
    const line = lines[i]
    const trimmed = line.trim()
    if (!trimmed) { i += 1; continue }
    // 管道表格：连续的 | 行，第二行是分隔行
    if (isTableLine(line) && i + 1 < lines.length && isSeparator(lines[i + 1])) {
      const header = splitRow(line)
      i += 2
      const bodyRows = []
      while (i < lines.length && isTableLine(lines[i]) && !isSeparator(lines[i])) { bodyRows.push(splitRow(lines[i])); i += 1 }
      blocks.push(`<table class="md-table"><thead><tr>${header.map(cell => `<th>${inline(cell)}</th>`).join('')}</tr></thead><tbody>${bodyRows.map(row => `<tr>${row.map((cell,index) => `<td>${inline(formatMetric(cell,header[index] || ''))}</td>`).join('')}</tr>`).join('')}</tbody></table>`)
      continue
    }
    // 标题：## 前缀 / 独立【节题】行 / 独立整行加粗行
    const hashHeading = trimmed.match(/^(#{1,6})\s+(.+)/)
    const bracketHeading = trimmed.match(/^【([^】]+)】\s*$/)
    const boldOnly = trimmed.match(/^\*\*\s*(?:【?)([^*】]+?)(?:】?)\s*\*\*[:：]?\s*$/)
    if (hashHeading || bracketHeading || boldOnly) {
      const title = (hashHeading?.[2] || bracketHeading?.[1] || boldOnly?.[1] || '').replace(/[•●]/g, '').trim()
      if (title) blocks.push(`<h4 class="md-heading">${inline(title)}</h4>`)
      i += 1
      continue
    }
    // 列表：连续的 - / * / 1. 项
    if (isBullet(line)) {
      const items = []
      while (i < lines.length && isBullet(lines[i])) { items.push(bulletText(lines[i]).trim()); i += 1 }
      blocks.push(`<ul class="md-list">${items.map(item => `<li>${inline(item)}</li>`).join('')}</ul>`)
      continue
    }
    // 普通段落
    blocks.push(`<p>${inline(trimmed)}</p>`)
    i += 1
  }
  return blocks.join('')
}
export function datasetCsv(dataset = {}) {
  const columns = dataset.columns || Object.keys(dataset.rows?.[0] || {})
  // Spreadsheet formula injection protection, preserving actual negative numbers.
  const quote = value => {
    let text = value == null ? '' : typeof value === 'object' ? JSON.stringify(value) : String(value)
    if (typeof value === 'string' && /^[\s]*[=+@-]/.test(text)) text = "'" + text
    return '"' + text.replaceAll('"','""') + '"'
  }
  return '\uFEFF' + [columns,...(dataset.rows || []).map(row => columns.map(key => row[key]))].map(row => row.map(quote).join(',')).join('\r\n')
}
export function chartLabel(value) {
  return typeof value==='number' && Number.isFinite(value)?new Intl.NumberFormat('zh-CN',{notation:'compact',maximumFractionDigits:2}).format(value):'—'
}
function reportNarrative(text) {
  // 与屏上解读共用渲染器：加粗/标题/表格/列表在下载简报中同样生效
  return renderMarkdownHtml(text)
}
export function answerHtml(question, datasets = [], report = '') {
  const rows=datasets.reduce((n,ds)=>n+(ds.rows?.length || 0),0)
  const body=datasets.map((ds,index)=>{
    const columns=ds.columns || Object.keys(ds.rows?.[0] || {}),metric=numericColumns(ds)[0],dimension=dimensionColumn(ds,metric)
    const records=(ds.rows || []).slice(0,12),maximum=Math.max(0,...records.map(row=>typeof row[metric]==='number'?row[metric]:0))
    const canChart=dimension && metric && maximum>0 && records.every(row=>typeof row[metric]==='number' && Number.isFinite(row[metric]) && row[metric]>=0)
    const chart=canChart?`<div class="report-chart"><h3>${escapeHtml(metric)}</h3><p class="muted">按查询返回顺序展示${records.length}条 · 数值与单位以字段定义为准</p>${records.map(row=>`<div class="bar-row"><span>${escapeHtml(row[dimension])}</span><div class="bar-track"><i style="width:${Math.max(0,Math.min(100,row[metric]/maximum*100)).toFixed(3)}%"></i></div><strong>${escapeHtml(formatMetric(row[metric],metric,ds))}</strong></div>`).join('')}</div>`:''
    return `<section><div class="section-head"><small>数据依据 ${String(index+1).padStart(2,'0')}</small><h2>${escapeHtml(ds.dataset_name || '授权数据集')}</h2><p class="muted">返回 ${(ds.rows || []).length} 行 · ${columns.length} 个结果字段</p></div>${queryFailed(ds)?'<p class="warning">本结果查询未完成，不能据此判断业务数据为空。</p>':''}${ds.analysis_status==='model_unavailable'?'<p class="warning">数据可供核对，AI 解读尚未完成。</p>':''}${chart}<details open><summary>结果明细</summary><div class="table-wrap"><table><thead><tr>${columns.map(c=>`<th>${escapeHtml(c)}</th>`).join('')}</tr></thead><tbody>${(ds.rows || []).map(row=>`<tr>${columns.map(c=>`<td>${escapeHtml(formatMetric(row[c],c,ds))}</td>`).join('')}</tr>`).join('')}</tbody></table></div></details>${!report && ds.analysis?`<div class="narrative">${reportNarrative(ds.analysis)}</div>`:''}</section>`
  }).join('')
  return `<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'; img-src 'none'"><title>${escapeHtml(question)}</title><style>*{box-sizing:border-box}body{margin:0;background:#edf2f8;color:#20324d;font:14px/1.85 -apple-system,BlinkMacSystemFont,"PingFang SC",sans-serif}main{max-width:1120px;margin:30px auto;padding:0 24px 40px}header{background:#fff;border:1px solid #e2e8f0;border-top:4px solid #3c536e;border-radius:10px;padding:34px}header>small{font-size:11px;letter-spacing:2px;color:#617b9d}h1{font-size:27px;line-height:1.6;letter-spacing:-.5px;margin:14px 0 24px}h2{font-size:19px;line-height:1.6;margin:8px 0}h3{font-size:15px;margin:24px 0 12px;font-weight:600}p{margin:8px 0}.muted{font-size:12px;color:#74839a}.facts{display:flex;gap:34px;flex-wrap:wrap;border-top:1px solid #edf1f6;padding-top:18px}.facts span{color:#75849a;font-size:12px}.facts strong{font-size:22px;font-weight:500;color:#334e72;margin-right:8px}section{margin:22px 0;background:#fff;border:1px solid #e2e8f0;border-radius:10px;padding:28px 34px}.section-head>small{font-size:11px;color:#7d8fa6;letter-spacing:1px}.report-chart{margin:24px 0 32px}.bar-row{display:grid;grid-template-columns:minmax(90px,145px) minmax(60px,1fr) minmax(80px,130px);gap:16px;align-items:center;font-size:12px;margin:16px 0}.bar-row>span{overflow-wrap:anywhere}.bar-row strong{text-align:right;font-weight:500;font-variant-numeric:tabular-nums}.bar-track{background:#edf2f8;height:14px;border-radius:3px;overflow:hidden}.bar-track i{display:block;height:100%;background:#425f83;border-radius:3px}.table-wrap{overflow:auto}table{border-collapse:collapse;width:100%;font-size:12px}th,td{text-align:left;border-bottom:1px solid #e9edf3;padding:12px;white-space:nowrap}th{background:#f5f7fa;font-weight:500;color:#637894}summary{font-size:13px;font-weight:500;color:#506b8d;cursor:pointer;margin:12px 0}.narrative{margin-top:24px}.narrative p{white-space:pre-wrap;overflow-wrap:anywhere;color:#435a78;line-height:1.95}.warning{padding:12px;background:#f5f2ec;color:#806b47;font-size:12px;border-radius:6px}footer{color:#8491a2;font-size:11px;text-align:center;margin-top:30px}@media(max-width:600px){main{padding:0 12px;margin:12px auto}header,section{padding:20px}h1{font-size:21px}.bar-row{grid-template-columns:90px 1fr;gap:8px}.bar-row strong{grid-column:2;text-align:left}.facts{gap:16px}}@media print{body{background:#fff}main{margin:0;padding:0}section,header{break-inside:avoid;border-color:#ddd}tr{break-inside:avoid}}</style></head><body><main><header><small>DATAPULSE / ANALYSIS REPORT</small><h1>${escapeHtml(question || '数据分析报告')}</h1><div class="facts"><span><strong>${datasets.length}</strong>个数据来源</span><span><strong>${rows}</strong>行查询结果</span><span>本次查询快照 · 不自动刷新</span></div></header>${report?`<section class="narrative"><div class="section-head"><small>分析摘要</small><h2>结果解读与业务建议</h2></div>${reportNarrative(report)}</section>`:''}${body}<footer>DataPulse · 仅基于本次返回结果；数值、单位与分析边界以查询口径为准。</footer></main></body></html>`
}
