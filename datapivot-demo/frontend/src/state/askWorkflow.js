// Pure reducer: concurrent nodes are keyed by run, branch, node and attempt.
export const emptyWorkflow = () => ({ run_id: '', flow: 'basic', catalog: [], events: [], branches: [], evidence: [], status: 'idle' })
export function reduceWorkflow(previous, event) {
  const state = previous || emptyWorkflow()
  if (!event || !event.run_id) return state
  if (state.run_id && event.run_id !== state.run_id) return state
  const next = event.type === 'started' ? { ...emptyWorkflow(), run_id: event.run_id, flow: event.flow, status: 'running', catalog: event.catalog || [] } : { ...state }
  if (next.run_id && event.run_id !== next.run_id) return state
  if (next.events.some(e => e.seq === event.seq)) return state
  next.run_id = event.run_id
  next.flow = event.flow || next.flow
  next.events = [...next.events, event].slice(-300)
  if (event.branches) next.branches = event.branches
  if (event.evidence) next.evidence = [...next.evidence.filter(e => e.id !== event.evidence.id), event.evidence]
  if (event.type === 'finished') {
    next.status = event.status
    next.outcome = event.outcome
  }
  return next
}
export function workflowNodes(workflow) {
  const nodes = new Map()
  for (const event of [...(workflow?.events || [])].sort((a,b)=>(a.seq || 0)-(b.seq || 0))) {
    if (workflow?.run_id && event.run_id && event.run_id !== workflow.run_id) continue
    if (!event.node_id) continue
    const key = [event.branch_id || 'main', event.dataset_id || '', event.node_id, event.attempt || 0].join(':')
    nodes.set(key, { ...event, key })
  }
  return [...nodes.values()]
}

const labels={idle:'等待提问',running:'正在分析',waiting:'等待确认',completed:'分析已完成',empty:'查询完成，无匹配记录',partial:'部分结果可用',failed:'查询未完成',canceled:'已停止'}
const descriptions={idle:'开始提问后，这里会同步真实进展。',running:'正在处理本次问题，进展随真实执行事件更新。',waiting:'确认本次范围与计划后继续执行。',completed:'可以查看本次结果、数据与查询依据。',empty:'查询已执行，请核对时间、筛选条件与授权范围。',partial:'保留已返回的结果，未完成的查询或 AI 解读仍需重试。',failed:'查询生成、审核或执行未完成，不能据此判断业务数据为空。',canceled:'任务已经停止，未完成步骤不会显示为成功。'}
export function taskOutcome(result, {status='',busy=false,workflow={}}={}) {
  let state='idle'
  let detail=null
  const canceled=result?.aborted || status==='canceled' || workflow.status==='canceled'
  if(canceled)state='canceled'
  else if((busy || status==='running') && !['completed','empty','partial','failed','waiting'].includes(workflow.status))state='running'
  else if(result?.error || status==='error')state='failed'
  else if(result?.requires_confirmation)state='waiting'
  else if(result?.outcome || workflow.outcome){detail=result?.outcome || workflow.outcome;state=detail.status}
  else if(result){
    const research=result.research
    const datasets=research?(research.evidence || []).flatMap(e=>e.dataset_results || []):(result.dataset_results || [])
    const failed=datasets.filter(d=>d.query_status==='failed' || d.agent3_review?.approved===false || (!d.rows?.length && d.analysis_status==='model_unavailable'))
    const rows=datasets.reduce((n,d)=>n+(d.rows?.length || 0),0)
    if(research && (research.partial || research.summary_review?.status!=='completed'))state=(research.evidence || []).some(e=>e.status==='completed')?'partial':'failed'
    else if(!datasets.length)state=research && !research.partial?'completed':'failed'
    else if(failed.length===datasets.length)state='failed'
    else if(failed.length || datasets.some(d=>['model_unavailable','deterministic'].includes(d.analysis_status)))state='partial'
    else state=rows?'completed':'empty'
  }else if(['failed','waiting','partial','empty','canceled'].includes(workflow.status))state=workflow.status
  else if(busy || status==='running')state='running'
  return {status:state,label:detail?.label || labels[state] || labels.idle,description:detail?.description || descriptions[state] || descriptions.idle}
}

export function workflowStages(workflow, outcome='running') {
  const groups=new Map()
  const recorded=workflowNodes(workflow)
  // Model calls omit dataset_id; attach them only when the phase's dataset is unambiguous.
  const scope=new Map()
  for(const event of recorded){
    const key=[event.branch_id || 'main',event.node_id].join(':')
    if(!scope.has(key))scope.set(key,new Set())
    if(event.dataset_id)scope.get(key).add(String(event.dataset_id))
  }
  for(const event of recorded){
    const candidates=scope.get([event.branch_id || 'main',event.node_id].join(':'))
    const dataset=event.dataset_id || (candidates.size===1?[...candidates][0]:'')
    const key=[event.branch_id || 'main',dataset,event.node_id].join(':')
    const previous=groups.get(key)
    if(!previous)groups.set(key,{...event,key,history:[event]})
    else {
      const attempts=new Map()
      for(const item of [...previous.history,event].sort((a,b)=>(a.seq || 0)-(b.seq || 0)))attempts.set(item.attempt || 0,item)
      const history=[...attempts.values()].sort((a,b)=>(a.seq || 0)-(b.seq || 0))
      groups.set(key,{...history.at(-1),key,history})
    }
  }
  return [...groups.values()].map(node=>{
    const status={success:'completed',response:'completed',request:'running',error:'failed',retry:'retrying',fallback:'failed',rejected:'failed'}[node.status] || node.status
    const settled=outcome!=='running' && ['running','retrying','pending'].includes(status)
    return {...node,status:settled?'interrupted':status,attempts:node.history.length}
  }).sort((a,b)=>(a.seq || 0)-(b.seq || 0))
}

export function analysisPhases(workflow, outcome='running') {
  const stages=workflowStages(workflow,outcome)
  const definitions=[['理解问题','确认问题与授权范围'],['准备查询','匹配数据与生成查询'],['查询与核验','审核、执行与合理性检查'],['形成回答','解读、复核与结果交付']]
  const phase=node=>{
    const id=node.node_id || ''
    if(id.startsWith('R')){const n=Number(id.slice(1));return n<=14?0:n<=20 || n===26 || n===27?1:n<=30?2:3}
    return ['L0','L1'].includes(id)?0:['L2','L3','L4','L5','LR'].includes(id)?1:['L6','L7','L8','L9','L10'].includes(id)?2:3
  }
  return definitions.map(([title,description],index)=>{
    const nodes=stages.filter(n=>phase(n)===index)
    const latest=nodes.at(-1)
    const status=nodes.some(n=>['running','retrying'].includes(n.status))?'running':nodes.some(n=>['failed','warning','interrupted'].includes(n.status))?'warning':nodes.length?'completed':outcome==='running' || outcome==='idle' || outcome==='waiting'?'planned':'unrecorded'
    return {id:index,title,description,status,nodes,latest}
  })
}
