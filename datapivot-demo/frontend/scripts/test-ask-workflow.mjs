import test from 'node:test'
import assert from 'node:assert/strict'
import { emptyWorkflow, reduceWorkflow, workflowNodes } from '../src/state/askWorkflow.js'

test('parallel branches and attempts retain independent state', () => {
  let state = reduceWorkflow(emptyWorkflow(), {type:'started',run_id:'r1',flow:'advanced',seq:1,catalog:[]})
  for (const event of [{seq:2,branch_id:'b1',node_id:'R19',status:'running'},{seq:3,branch_id:'b2',node_id:'R19',status:'completed'},{seq:4,branch_id:'b1',node_id:'R19',status:'failed'},{seq:5,branch_id:'b1',node_id:'R19',attempt:1,status:'running'}]) {
    state = reduceWorkflow(state,{run_id:'r1',...event})
  }
  const nodes=workflowNodes(state)
  assert.equal(nodes.length,3)
  assert.equal(nodes.find(n=>n.branch_id==='b2').status,'completed')
  assert.equal(nodes.find(n=>n.branch_id==='b1'&&!n.attempt).status,'failed')
})
test('duplicate and stale frames never overwrite the current task', () => {
  let state=reduceWorkflow(emptyWorkflow(),{type:'started',run_id:'r2',seq:1})
  state=reduceWorkflow(state,{run_id:'r2',seq:2,node_id:'L9',status:'completed'})
  const duplicate=reduceWorkflow(state,{run_id:'r2',seq:2,node_id:'L9',status:'running'})
  assert.equal(duplicate,state)
  assert.equal(reduceWorkflow(state,{run_id:'r1',seq:9,node_id:'L9',status:'failed'}),state)
})
test('evidence updates replace only their own branch', () => {
  let state=reduceWorkflow(emptyWorkflow(),{type:'started',run_id:'r',seq:1})
  for(const [seq,id,status] of [[2,'b1','completed'],[3,'b2','failed'],[4,'b1','insufficient']])state=reduceWorkflow(state,{run_id:'r',seq,evidence:{id,status}})
  assert.equal(state.evidence.length,2)
  assert.equal(state.evidence.find(e=>e.id==='b2').status,'failed')
  assert.equal(state.evidence.find(e=>e.id==='b1').status,'insufficient')
})


test('research export escapes source content and preserves evidence gaps', async () => {
  const { buildResearchReportHtml } = await import('../src/utils/researchReport.js')
  const html=buildResearchReportHtml({question:'<script>alert(1)</script>',research:{partial:true,gaps:['缺口'],summary:{conclusion:'证据不足'},evidence:[{title:'方向',status:'insufficient',finding:'待验证',dataset_results:[]}]}})
  assert.ok(!html.includes('<script>'))
  assert.ok(html.includes('&lt;script&gt;'))
  assert.ok(html.includes('待补证') && html.includes('缺口'))
})

test('late starts and out-of-order node frames cannot rewind a task', async()=>{
  const {workflowStages}=await import('../src/state/askWorkflow.js')
  let state=reduceWorkflow(emptyWorkflow(),{type:'started',run_id:'current',seq:1})
  assert.equal(reduceWorkflow(state,{type:'started',run_id:'old',seq:99}),state)
  state=reduceWorkflow(state,{run_id:'current',seq:4,node_id:'L5',status:'completed'})
  state=reduceWorkflow(state,{run_id:'current',seq:3,node_id:'L5',status:'running'})
  assert.equal(workflowStages(state,'running')[0].status,'completed')
})
test('retry attempts fold into one visible step, terminal tasks leave no running badges', async()=>{
  const {workflowStages}=await import('../src/state/askWorkflow.js')
  const workflow={run_id:'r',events:[
    {run_id:'r',seq:1,node_id:'L5',attempt:0,status:'failed'},
    {run_id:'r',seq:2,node_id:'L5',attempt:1,status:'completed'},
    {run_id:'r',seq:3,node_id:'L6',status:'running'},
    {run_id:'r',seq:4,node_id:'L6',attempt:1,status:'retrying'}]}
  const nodes=workflowStages(workflow,'failed')
  assert.equal(nodes.length,2)
  assert.equal(nodes[0].status,'completed')
  assert.equal(nodes[0].attempts,2)
  assert.equal(nodes[1].status,'interrupted')
  assert.ok(!nodes.some(n=>['running','retrying'].includes(n.status)))
})
test('request completion never masks a failed query, incomplete AI or a valid empty result',async()=>{
  const {taskOutcome}=await import('../src/state/askWorkflow.js')
  const ds={query_status:'completed',analysis_status:'model_generated',agent3_review:{approved:true},rows:[{value:5}]}
  assert.equal(taskOutcome({dataset_results:[ds]}).status,'completed')
  assert.equal(taskOutcome({dataset_results:[{...ds,rows:[]}]}).status,'empty')
  assert.equal(taskOutcome({dataset_results:[{...ds,analysis_status:'model_unavailable'}]}).status,'partial')
  assert.equal(taskOutcome({dataset_results:[{...ds,query_status:'failed',rows:[]}]}).status,'failed')
  assert.equal(taskOutcome({requires_confirmation:true},{workflow:{status:'waiting'}}).status,'waiting')
  assert.equal(taskOutcome({aborted:true}).status,'canceled')
  assert.equal(taskOutcome({dataset_results:[ds]},{busy:true,workflow:{status:'running'}}).status,'running')
})
test('finished event settles streaming status before the result body arrives',async()=>{
  const {taskOutcome}=await import('../src/state/askWorkflow.js')
  let state=reduceWorkflow(emptyWorkflow(),{type:'started',run_id:'r',seq:1})
  state=reduceWorkflow(state,{type:'finished',run_id:'r',seq:2,status:'failed',outcome:{status:'failed',label:'查询未完成'}})
  assert.equal(taskOutcome(null,{busy:true,workflow:state}).status,'failed')
})
test('dataset-free model events join a uniquely scoped stage without merging distinct datasets',async()=>{
  const {workflowStages}=await import('../src/state/askWorkflow.js')
  const events=[{seq:1,node_id:'L6',status:'running'},{seq:2,node_id:'L6',dataset_id:64,status:'failed'}]
  assert.equal(workflowStages({events},'failed').length,1)
  assert.equal(workflowStages({events},'failed')[0].status,'failed')
  const ambiguous=[...events,{seq:3,node_id:'L6',dataset_id:65,status:'completed'}]
  assert.equal(workflowStages({events:ambiguous},'failed').length,3)
})
