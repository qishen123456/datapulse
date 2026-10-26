export const QUEUE_LIMIT=5
// crypto.randomUUID 仅在安全上下文（HTTPS 或 localhost）可用；
// HTTP+裸 IP 访问（如云服务器演示地址）下 window.crypto.randomUUID 为 undefined，
// 裸调用会抛 TypeError 让发送链路静默死亡——统一带兜底（2026-10-25 修复"发送按钮没反应"）。
const newQueueId = () => (typeof window !== 'undefined' && window.crypto?.randomUUID)
  ? window.crypto.randomUUID()
  : `q-${Date.now()}-${Math.random().toString(16).slice(2)}`
export function queuedQuestion(question,settings={}) {
  const text=String(question || '').trim()
  if(!text)return null
  return {id:newQueueId(),question:text,createdAt:Date.now(),datasetId:settings.datasetId || null,
    datasetName:settings.datasetName || '自动选择数据集',modelId:settings.modelId || null,flow:settings.flow || 'basic'}
}
export function appendQuestion(items,item){
  if(!item)return items
  if(items.length>=QUEUE_LIMIT)throw new Error(`最多排队 ${QUEUE_LIMIT} 个问题，请先整理队列。`)
  return [...items,{...item}]
}
export function moveQuestionUp(items,id){
  const index=items.findIndex(item=>item.id===id)
  if(index<=0)return items
  const next=[...items];[next[index-1],next[index]]=[next[index],next[index-1]];return next
}
export function queuePauseReason(outcome){
  return ({waiting:'请先确认当前问题的范围或研究计划',failed:'上一问未完成，请检查后继续队列',partial:'上一问只有部分结果，请检查后继续队列',canceled:'已停止当前任务，队列也已暂停'})[outcome] || ''
}
