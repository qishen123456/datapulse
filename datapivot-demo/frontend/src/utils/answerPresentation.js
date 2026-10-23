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
export function formatFact(value) {
  if (value === null || value === undefined || value === '') return '—'
  if (typeof value === 'number') return Number.isFinite(value) ? new Intl.NumberFormat('zh-CN',{maximumFractionDigits:4}).format(value) : '—'
  return typeof value === 'object' ? JSON.stringify(value) : String(value)
}
export function escapeHtml(value) {
  return String(value ?? '').replace(/[&<>"']/g, char => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]))
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
  return String(text || '').split(/\r?\n/).map(line=>{
    const trimmed=line.trim();if(!trimmed)return ''
    const heading=trimmed.match(/^【([^】]+)】/) || trimmed.match(/^#{1,6}\s+(.+)/)
    if(heading){const rest=trimmed.slice(heading[0].length).trim();return `<h3>${escapeHtml(heading[1].replace(/[•●]/g,''))}</h3>${rest?`<p>${escapeHtml(rest)}</p>`:''}`}
    return `<p>${escapeHtml(trimmed.replace(/\*\*/g,''))}</p>`
  }).join('')
}
export function answerHtml(question, datasets = [], report = '') {
  const rows=datasets.reduce((n,ds)=>n+(ds.rows?.length || 0),0)
  const body=datasets.map((ds,index)=>{
    const columns=ds.columns || Object.keys(ds.rows?.[0] || {}),metric=numericColumns(ds)[0],dimension=dimensionColumn(ds,metric)
    const records=(ds.rows || []).slice(0,12),maximum=Math.max(0,...records.map(row=>typeof row[metric]==='number'?row[metric]:0))
    const canChart=dimension && metric && maximum>0 && records.every(row=>typeof row[metric]==='number' && Number.isFinite(row[metric]) && row[metric]>=0)
    const chart=canChart?`<div class="report-chart"><h3>${escapeHtml(metric)}</h3><p class="muted">按查询返回顺序展示${records.length}条 · 数值与单位以字段定义为准</p>${records.map(row=>`<div class="bar-row"><span>${escapeHtml(row[dimension])}</span><div class="bar-track"><i style="width:${Math.max(0,Math.min(100,row[metric]/maximum*100)).toFixed(3)}%"></i></div><strong>${escapeHtml(formatFact(row[metric]))}</strong></div>`).join('')}</div>`:''
    return `<section><div class="section-head"><small>数据依据 ${String(index+1).padStart(2,'0')}</small><h2>${escapeHtml(ds.dataset_name || '授权数据集')}</h2><p class="muted">返回 ${(ds.rows || []).length} 行 · ${columns.length} 个结果字段</p></div>${queryFailed(ds)?'<p class="warning">本结果查询未完成，不能据此判断业务数据为空。</p>':''}${ds.analysis_status==='model_unavailable'?'<p class="warning">数据可供核对，AI 解读尚未完成。</p>':''}${chart}<details open><summary>结果明细</summary><div class="table-wrap"><table><thead><tr>${columns.map(c=>`<th>${escapeHtml(c)}</th>`).join('')}</tr></thead><tbody>${(ds.rows || []).map(row=>`<tr>${columns.map(c=>`<td>${escapeHtml(formatFact(row[c]))}</td>`).join('')}</tr>`).join('')}</tbody></table></div></details>${!report && ds.analysis?`<div class="narrative">${reportNarrative(ds.analysis)}</div>`:''}</section>`
  }).join('')
  return `<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'; img-src 'none'"><title>${escapeHtml(question)}</title><style>*{box-sizing:border-box}body{margin:0;background:#f3f6fa;color:#20324d;font:14px/1.85 -apple-system,BlinkMacSystemFont,"PingFang SC",sans-serif}main{max-width:1120px;margin:30px auto;padding:0 24px 40px}header{background:#fff;border:1px solid #e2e8f0;border-top:4px solid #254e86;border-radius:10px;padding:34px}header>small{font-size:11px;letter-spacing:2px;color:#617b9d}h1{font-size:27px;line-height:1.6;letter-spacing:-.5px;margin:14px 0 24px}h2{font-size:19px;line-height:1.6;margin:8px 0}h3{font-size:15px;margin:24px 0 12px;font-weight:600}p{margin:8px 0}.muted{font-size:12px;color:#74839a}.facts{display:flex;gap:34px;flex-wrap:wrap;border-top:1px solid #edf1f6;padding-top:18px}.facts span{color:#75849a;font-size:12px}.facts strong{font-size:22px;font-weight:500;color:#334e72;margin-right:8px}section{margin:22px 0;background:#fff;border:1px solid #e2e8f0;border-radius:10px;padding:28px 34px}.section-head>small{font-size:11px;color:#7d8fa6;letter-spacing:1px}.report-chart{margin:24px 0 32px}.bar-row{display:grid;grid-template-columns:minmax(90px,145px) minmax(60px,1fr) minmax(80px,130px);gap:16px;align-items:center;font-size:12px;margin:16px 0}.bar-row>span{overflow-wrap:anywhere}.bar-row strong{text-align:right;font-weight:500;font-variant-numeric:tabular-nums}.bar-track{background:#f0f4f9;height:14px;border-radius:3px;overflow:hidden}.bar-track i{display:block;height:100%;background:#3866a5;border-radius:3px}.table-wrap{overflow:auto}table{border-collapse:collapse;width:100%;font-size:12px}th,td{text-align:left;border-bottom:1px solid #e9edf3;padding:12px;white-space:nowrap}th{background:#f7f9fc;font-weight:500;color:#637894}summary{font-size:13px;font-weight:500;color:#506b8d;cursor:pointer;margin:12px 0}.narrative{margin-top:24px}.narrative p{white-space:pre-wrap;overflow-wrap:anywhere;color:#435a78;line-height:1.95}.warning{padding:12px;background:#fff7e9;color:#986720;font-size:12px;border-radius:6px}footer{color:#8491a2;font-size:11px;text-align:center;margin-top:30px}@media(max-width:600px){main{padding:0 12px;margin:12px auto}header,section{padding:20px}h1{font-size:21px}.bar-row{grid-template-columns:90px 1fr;gap:8px}.bar-row strong{grid-column:2;text-align:left}.facts{gap:16px}}@media print{body{background:#fff}main{margin:0;padding:0}section,header{break-inside:avoid;border-color:#ddd}tr{break-inside:avoid}}</style></head><body><main><header><small>DATAPULSE / ANALYSIS REPORT</small><h1>${escapeHtml(question || '数据分析报告')}</h1><div class="facts"><span><strong>${datasets.length}</strong>个数据来源</span><span><strong>${rows}</strong>行查询结果</span><span>本次查询快照 · 不自动刷新</span></div></header>${report?`<section class="narrative"><div class="section-head"><small>分析摘要</small><h2>结果解读与业务建议</h2></div>${reportNarrative(report)}</section>`:''}${body}<footer>DataPulse · 仅基于本次返回结果；数值、单位与分析边界以查询口径为准。</footer></main></body></html>`
}
