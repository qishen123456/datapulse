import test from 'node:test'
import assert from 'node:assert/strict'
import {analysisActivity} from '../src/utils/analysisActivity.js'
test('public evidence keeps executed data while dropping arbitrary notes and scratchpads',()=>{
 const entries=analysisActivity({events:[{seq:1,activity:{kind:'assets',heading:'依据',dataset_name:'燃气数据',field_count:64,relation_count:4,reference_count:12,question:'9月销气量',time_mentions:['9月'],thought:'private'}}]})
 assert.match(JSON.stringify(entries),/64 个字段定义/)
 assert(!JSON.stringify(entries).includes('private'))
})
test('failed queries never synthesize returned evidence',()=>{
 assert.deepEqual(analysisActivity({}, {dataset_results:[{query_status:'failed',rows:[],columns:[]}]}),[])
 assert.equal(analysisActivity({}, {dataset_results:[{query_status:'success',rows:[],columns:['销气量']}]}).length,1)
})
test('retries replace evidence only in their own branch and dataset',()=>{
 const events=[{seq:1,branch_id:'a',dataset_id:64,activity:{kind:'data',row_count:2}},{seq:2,branch_id:'b',dataset_id:64,activity:{kind:'data',row_count:3}},{seq:3,branch_id:'a',dataset_id:64,activity:{kind:'data',row_count:4}}]
 const entries=analysisActivity({events});assert.equal(entries.length,2);assert.match(JSON.stringify(entries),/4 行/);assert(!JSON.stringify(entries).includes('2 行'))
})

import {analysisFacts} from '../src/utils/analysisActivity.js'
const fact=(workflow,result,id)=>analysisFacts(workflow,result).find(f=>f.id===id)
test('six facts distinguish waiting, missing approval and true zero rows',()=>{
 const waiting=analysisFacts({status:'running'});assert.equal(waiting.length,6);assert.ok(waiting.every(f=>f.value==='等待返回'))
 assert.equal(fact({},null,'plan').value,'未记录')
 const workflow={events:[{seq:1,activity:{kind:'review'}}]}
 assert(!JSON.stringify(analysisActivity(workflow)).includes('审核通过'))
 assert.equal(fact(workflow,null,'review').value,'审核结论未记录')
 const empty={dataset_results:[{dataset_id:1,dataset_name:'燃气',query_status:'completed',rows:[],columns:['销气量']} ]}
 assert.match(fact({},empty,'results').value,/返回 0 行 · 1 个字段/)
 assert.match(fact({},{dataset_results:[{...empty.dataset_results[0],query_status:'failed'}]},'results').value,/不能认定为零行/)
})
test('facts expose public plan and methods without SQL or model scratchpads',()=>{
 const w={run_id:'new',events:[{run_id:'old',seq:1,activity:{kind:'query',public_summary:'OLD'}},{run_id:'new',seq:2,dataset_id:1,activity:{kind:'query',dataset_name:'经营',public_summary:'按分公司汇总九月销气量',methods:['SUM'],aggregation:['按查询维度分组'],thought:'PRIVATE',sql:'SELECT SECRET'}}]}
 const f=analysisFacts(w);assert.match(f.find(f=>f.id==='plan').value,/按分公司/);assert.match(f.find(f=>f.id==='aggregation').value,/求和/);assert(!JSON.stringify(f).match(/OLD|PRIVATE|SECRET/))
})
test('research evidence stays attached to its branch and is not counted twice',()=>{
 const ds=(name,rows,approved)=>({dataset_id:name,dataset_name:name,query_status:approved?'completed':'failed',rows,columns:['数量'],agent3_review:{approved}})
 const a=ds('经营',[{数量:2}],true),b=ds('安全',[],false)
 const result={research:{evidence:[{id:'a',title:'经营趋势',dataset_results:[a]},{id:'b',title:'安全核验',dataset_results:[b]}]},dataset_results:[a,b]}
 const facts=analysisFacts({},result),review=facts.find(f=>f.id==='review'),returns=facts.find(f=>f.id==='results')
 assert.equal(review.details.length,2);assert.equal(review.details[0].label,'经营趋势 · 经营 · SQL');assert.match(review.details[1].value,/未通过/)
 assert.equal(returns.details.filter(d=>!d.label.endsWith(' · 字段')).length,2);assert.equal(returns.status,'warning')
})
test('anonymous review is not attached to an arbitrary dataset',()=>{
 const w={events:[{seq:1,dataset_id:1,activity:{kind:'assets',dataset_name:'经营'}},{seq:2,dataset_id:2,activity:{kind:'assets',dataset_name:'安全'}},{seq:3,activity:{kind:'review',approved:true}}]}
 const review=fact(w,null,'review');assert.match(review.details[0].label,/未标注数据集/);assert(!review.details[0].label.includes('经营'))
})
test('retries replace only their own review; unknown counts remain unknown',()=>{
 const w={events:[{seq:1,dataset_id:1,activity:{kind:'review',approved:false}},{seq:2,dataset_id:1,activity:{kind:'review',approved:true}},{seq:3,dataset_id:1,status:'completed',activity:{kind:'data'}}]}
 assert.equal(fact(w,null,'review').value,'SQL 审核通过')
 assert.equal(fact(w,null,'results').value,'返回行数未记录')
})
