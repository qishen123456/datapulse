// Public, verifiable tool summaries; never render model scratchpads or prompts.
export function analysisActivity(workflow={},result=null){
  const rows=new Map()
  for(const event of workflow.events || []){
    const a=event.activity
    if(!a || typeof a!=='object')continue
    const lines=[]
    if(a.question)lines.push({label:'问题',value:String(a.question)})
    if(a.dataset_name)lines.push({label:'数据依据',value:String(a.dataset_name)})
    if(a.time_mentions?.length)lines.push({label:'问题中的时间',value:a.time_mentions.join('、')})
    if(a.kind==='assets')lines.push({label:'已读取',value:`${a.field_count ?? 0} 个字段定义 · ${a.relation_count ?? 0} 条表关联 · ${a.reference_count ?? 0} 个 SQL 参考样例`})
    if(a.public_summary)lines.push({label:'查询方案',value:String(a.public_summary)})
    if(a.methods?.length)lines.push({label:'查询聚合',value:a.methods.join('、')})
    if(a.row_count!==undefined)lines.push({label:'返回规模',value:`${a.row_count} 行`})
    if(a.columns?.length)lines.push({label:'结果字段',value:a.columns.join('、')})
    for(const text of a.checks || [])if(text)lines.push({label:'核验说明',value:String(text)})
    if(a.kind==='review')lines.push({label:'审核结果',value:a.approved===true?'审核通过；执行前仍需组织范围注入和计划预检':a.approved===false?'尚未通过，未进入执行':'审核结论未记录'})
    rows.set(`${event.branch_id || ''}:${event.dataset_id || a.dataset_name || ''}:${a.kind}`,{id:`${event.seq || rows.size}:${a.kind}`,kind:a.kind,heading:a.heading || '分析依据',status:event.status,lines,branch:event.branch_id})
  }
  if(!rows.size && result){
    for(const [index,ds] of (result.dataset_results || []).filter(ds=>ds.query_status!=='failed' && ds.agent3_review?.approved!==false && Array.isArray(ds.rows)).entries())rows.set(`snapshot-${index}`,{id:`snapshot-${index}`,kind:'data',heading:'已返回的查询事实',lines:[{label:'数据依据',value:ds.dataset_name || '授权数据集'},{label:'结果规模',value:`${ds.rows?.length || 0} 行`},{label:'结果字段',value:(ds.columns || []).join('、')}]})
  }
  return [...rows.values()]
}
export function latestAnalysisSummary(workflow={}){
  return [...(workflow.events || [])].reverse().find(e=>e.node_id && e.summary && e.summary!==e.title)?.summary || ''
}

const factDefinitions = [
  ['scope', '问题范围'], ['sources', '数据来源'], ['plan', '查询方案摘要'],
  ['aggregation', '聚合方式'], ['review', '审核结果'], ['results', '返回字段与数据量'],
]
const methodLabels = {SUM:'求和',COUNT:'计数',AVG:'平均值',MIN:'最小值',MAX:'最大值',求和:'求和',计数:'计数',平均值:'平均值',最小值:'最小值',最大值:'最大值'}
const list = value => Array.isArray(value) ? value : []
const text = value => typeof value === 'string' ? value.trim() : ''
const number = value => typeof value === 'number' && Number.isFinite(value) && value >= 0 ? value : null
const reviewLabel = approved => approved === true ? 'SQL 审核通过' : approved === false ? 'SQL 审核未通过，未获准执行' : '审核结论未记录'

/** Six public facts. A scope is a branch + dataset, never the latest unrelated event. */
export function analysisFacts(workflow = {}, result = null) {
  workflow ||= {}
  const running = ['running', 'waiting'].includes(workflow.status)
  const missing = running ? '等待返回' : '未记录'
  const events = list(workflow.events).filter(event => !workflow.run_id || !event.run_id || event.run_id === workflow.run_id)
    .slice().sort((a,b) => (a.seq || 0) - (b.seq || 0))
  const branches = new Map()
  for (const branch of [...list(result?.research_plan?.branches), ...list(workflow.branches), ...list(result?.research?.evidence)]) {
    if (branch?.id) branches.set(String(branch.id), branch)
  }
  // Research top-level results repeat evidence; use only branch-owned results.
  const snapshots = result?.research ? list(result.research.evidence).flatMap(branch =>
    list(branch.dataset_results).map(dataset => ({dataset, branch: String(branch.id || ''), branchDataset: branch.dataset_id}))) :
    list(result?.dataset_results).map(dataset => ({dataset, branch: '', branchDataset: null}))
  const candidates = new Map()
  const addCandidate = (branch, id, name = '') => {
    if (id == null || id === '') return
    if (!candidates.has(branch)) candidates.set(branch, new Map())
    const old = candidates.get(branch).get(String(id)) || ''
    candidates.get(branch).set(String(id), text(name) || old)
  }
  for (const [id, branch] of branches) addCandidate(id, branch.dataset_id)
  for (const entry of snapshots) addCandidate(entry.branch, entry.dataset.dataset_id ?? entry.branchDataset, entry.dataset.dataset_name)
  for (const event of events) addCandidate(String(event.branch_id || ''), event.dataset_id, event.activity?.dataset_name)
  const groups = new Map()
  const scopeFor = (branch, id, name = '') => {
    const options = candidates.get(branch) || new Map()
    let resolved = id == null ? '' : String(id)
    if (!resolved && name) {
      const matching = [...options].filter(([, candidateName]) => candidateName === name)
      if (matching.length === 1) resolved = matching[0][0]
    }
    // Anonymous model/review events can only join a single unambiguous dataset.
    if (!resolved && options.size === 1) resolved = [...options.keys()][0]
    const key = `${branch || 'main'}:${resolved || (text(name) ? `name:${name}` : 'unassigned')}`
    if (!groups.has(key)) groups.set(key, {key, branch, datasetId: resolved, name: text(name) || options.get(resolved) || '', activities: new Map(), dataset: null})
    const group = groups.get(key)
    if (text(name)) group.name = text(name)
    return group
  }
  for (const event of events) {
    const activity = event.activity
    if (!activity || typeof activity !== 'object') continue
    const group = scopeFor(String(event.branch_id || ''), event.dataset_id, text(activity.dataset_name))
    group.activities.set(activity.kind, {...activity, status: event.status})
  }
  for (const entry of snapshots) {
    scopeFor(entry.branch, entry.dataset.dataset_id ?? entry.branchDataset, entry.dataset.dataset_name).dataset = entry.dataset
  }
  const labelFor = group => {
    const branch = branches.get(group.branch)
    const branchName = text(branch?.title) || (group.branch ? `分支 ${group.branch}` : '')
    return [branchName, group.name || (group.datasetId ? '授权数据集' : '未标注数据集的记录')].filter(Boolean).join(' · ')
  }
  const details = Object.fromEntries(factDefinitions.map(([id]) => [id, []]))
  const warnings = new Set()
  const append = (id, label, value) => {
    if (value && !details[id].some(item => item.label === label && item.value === value)) details[id].push({label, value})
  }
  const question = text(result?.question) || text(result?.research_plan?.question)
  if (question) append('scope', '本次问题', question)
  for (const group of groups.values()) {
    const label = labelFor(group)
    const a = group.activities
    const assets = a.get('assets') || a.get('intent')
    const query = a.get('query')
    const dataset = group.dataset
    if (!question && text(assets?.question)) append('scope', group.branch ? label : '本次问题', text(branches.get(group.branch)?.question) || text(assets.question))
    if (list(assets?.time_mentions).length) append('scope', `${label} · 时间`, assets.time_mentions.map(String).join('、'))
    if (group.name) {
      const counts = []
      if (number(assets?.field_count) !== null) counts.push(`${assets.field_count} 个字段定义`)
      if (number(assets?.relation_count) !== null) counts.push(`${assets.relation_count} 条表关联`)
      if (number(assets?.reference_count) !== null) counts.push(`${assets.reference_count} 个 SQL 参考样例`)
      append('sources', label, counts.join(' · ') || '已记录本次使用的数据集')
    }
    if (query) {
      append('plan', label, text(query.public_summary) || '查询已生成，业务方案摘要未记录')
      const methods = list(query.methods).map(method => methodLabels[String(method).toUpperCase()] || '').filter(Boolean)
      const shapes = list(query.aggregation).filter(value => typeof value === 'string')
      if (methods.length || shapes.length) append('aggregation', label, [...new Set([...methods, ...shapes])].join(' · '))
    }
    const review = dataset?.agent3_review && typeof dataset.agent3_review === 'object' ? dataset.agent3_review : a.get('review')
    if (review) {
      append('review', `${label} · SQL`, reviewLabel(review.approved))
      if (review.approved === false) warnings.add('review')
    }
    const preflight = a.get('preflight')
    if (preflight) for (const check of list(preflight.checks)) append('review', `${label} · 执行计划`, text(check))
    const checks = a.get('checks')
    if (checks) {
      for (const check of list(checks.checks)) append('review', `${label} · 数据核验`, text(check))
      if (['warning', 'failed'].includes(checks.status)) warnings.add('review')
    }
    // A rejected/failed query is not a zero-row result, even if it contains rows: [].
    const failed = dataset?.query_status === 'failed' || review?.approved === false
    const returned = dataset && !failed && Array.isArray(dataset.rows) &&
      (['completed','success'].includes(dataset.query_status) || dataset.rows.length > 0)
    const data = a.get('data')
    if (failed) {
      append('results', label, '查询未完成，不能认定为零行数据')
      warnings.add('results')
    } else if (returned || (data && !['failed','running','retrying'].includes(data.status))) {
      const rows = returned ? (number(dataset.row_count) ?? dataset.rows.length) : number(data.row_count)
      const columns = (returned ? (Array.isArray(dataset.columns) ? dataset.columns : Object.keys(dataset.rows[0] || {})) : list(data.columns)).map(String)
      const count = rows === null ? '返回行数未记录' : `返回 ${rows.toLocaleString('zh-CN')} 行`
      const fieldCount = returned ? (Array.isArray(dataset.columns) || dataset.rows.length ? columns.length : null) : (number(data.column_count) ?? (Array.isArray(data.columns) ? columns.length : null))
      append('results', label, `${count}${fieldCount !== null ? ` · ${fieldCount} 个字段` : ''}`)
      if (columns.length) append('results', `${label} · 字段`, columns.join('、') + (fieldCount > columns.length ? ` 等 ${fieldCount} 个字段` : ''))
      else if (rows !== null && rows > 0) append('results', `${label} · 字段`, '字段清单未记录')
    }
  }
  return factDefinitions.map(([id,label]) => {
    const lines = details[id]
    let value = lines[0]?.value || missing
    if (id === 'sources' && lines.length) value = lines.length === 1 ? lines[0].label : `${lines.length} 项数据来源记录`
    if (id === 'scope' && question) value = question
    if (id === 'review' && lines.length > 1) value = warnings.has(id) ? '有核验事项需要关注' : `${lines.length} 项审核与核验记录`
    if (id === 'results' && lines.length > 1) {
      const returns=lines.filter(item=>!item.label.endsWith(' · 字段'))
      value=warnings.has(id)?'部分查询未完成':returns.length===1?returns[0].value:`${returns.length} 项查询返回记录`
    }
    if (['plan','aggregation'].includes(id) && lines.length > 1) value = `${lines.length} 项${id === 'plan' ? '查询方案' : '聚合方式'}记录`
    return {id, label, value, details: lines, status: warnings.has(id) ? 'warning' : lines.length ? 'available' : 'pending'}
  })
}
