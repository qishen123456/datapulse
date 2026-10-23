import test from 'node:test'
import assert from 'node:assert/strict'
import {queuedQuestion,appendQuestion,moveQuestionUp,queuePauseReason,QUEUE_LIMIT} from '../src/state/questionQueue.js'
test('questions snapshot their submission scope and keep FIFO order',()=>{
  const settings={datasetId:64,datasetName:'燃气经营',modelId:12,flow:'advanced'}
  const first=queuedQuestion('  9月销气量  ',settings)
  settings.datasetId=66;settings.flow='basic'
  const second=queuedQuestion('安检覆盖率',settings)
  const queue=appendQuestion(appendQuestion([],first),second)
  assert.equal(queue[0].question,'9月销气量')
  assert.equal(queue[0].datasetId,64)
  assert.equal(queue[0].flow,'advanced')
  assert.equal(queue[1].datasetId,66)
  assert.notEqual(first.id,second.id)
  assert.equal(queuedQuestion('  '),null)
})
test('a full queue never consumes or silently drops a question',()=>{
  const queue=Array.from({length:QUEUE_LIMIT},(_,i)=>queuedQuestion('问题'+i))
  assert.throws(()=>appendQuestion(queue,queuedQuestion('额外问题')),/最多排队/)
  assert.equal(queue.length,5)
})
test('manual promotion preserves the other pending questions',()=>{
  const queue=['一','二','三'].map(q=>queuedQuestion(q))
  assert.deepEqual(moveQuestionUp(queue,queue[2].id).map(q=>q.question),['一','三','二'])
  assert.deepEqual(queue.map(q=>q.question),['一','二','三'])
})
test('uncertain or interrupted answers pause queue progression',()=>{
  for(const status of ['failed','partial','waiting','canceled'])assert.ok(queuePauseReason(status))
  for(const status of ['completed','empty'])assert.equal(queuePauseReason(status),'')
})
