import test from 'node:test'
import assert from 'node:assert/strict'
import { numericColumns,dimensionColumn,datasetCsv,answerHtml,formatFact } from '../src/utils/answerPresentation.js'
test('facts keep null, negative values and actual units',()=>{
  const ds={columns:['org_id','branch_name','利润_元'],rows:[{org_id:'001',branch_name:'滨江',利润_元:-150},{org_id:'002',branch_name:'沙湖',利润_元:null}]}
  assert.deepEqual(numericColumns(ds),['利润_元'])
  assert.equal(dimensionColumn(ds),'branch_name')
  assert.equal(formatFact(null),'—')
  assert.equal(formatFact(-150),'-150')
  assert.ok(datasetCsv(ds).includes('"-150"'))
})
test('exports escape markup and neutralize spreadsheet formulas',()=>{
  const ds={columns:['客户','金额'],rows:[{'客户':'=HYPERLINK("x")','金额':-5}]}
  assert.ok(datasetCsv(ds).includes("'=HYPERLINK"))
  const html=answerHtml('<script>alert(1)</script>',[ds],'<img src=x onerror=x>')
  assert.ok(!html.includes('<script>'))
  assert.ok(html.includes('&lt;img'))
  assert.ok(!html.includes('达成率'))
})
test('identifiers and missing data do not become chart measures',()=>{
  assert.deepEqual(numericColumns({columns:['customer_id','序号','收入'],rows:[{customer_id:5,序号:1,收入:null}]}),[])
})

test('query failure differs from an executed empty query, including historical records', async()=>{
  const {queryFailed}=await import('../src/utils/answerPresentation.js')
  assert.equal(queryFailed({query_status:'failed',rows:[]}),true)
  assert.equal(queryFailed({agent3_review:{approved:false},rows:[]}),true)
  assert.equal(queryFailed({query_status:'completed',rows:[]}),false)
  assert.equal(queryFailed({analysis_status:'model_unavailable',query_status:'completed',rows:[{value:2}]}),false)
})

test('comparison selects varying entities instead of the shared month',()=>{
  const ds={columns:['month','branch_name','branch_code','销气量_方'],rows:[{month:'2026-09',branch_name:'经开分公司',branch_code:1,销气量_方:36060044},{month:'2026-09',branch_name:'滨江分公司',branch_code:2,销气量_方:33055044}]}
  assert.equal(dimensionColumn(ds),'branch_name')
  assert.deepEqual(numericColumns(ds),['销气量_方'])
  const html=answerHtml('9月销气量', [ds], '【核心结论】\n仅反映当月规模差异。')
  assert.match(html,/<h[34][^>]*>核心结论<\/h[34]>/)
  assert.match(html,/36,060,044/)
  assert.match(html,/class="bar-row"/)
  assert.ok(!html.includes('NaN%'))
})
test('time trend keeps date dimension when the entity is constant',()=>{
  assert.equal(dimensionColumn({columns:['branch_name','month','收入'],rows:[{branch_name:'经开',month:'2026-08',收入:1},{branch_name:'经开',month:'2026-09',收入:2}]}),'month')
  const html=answerHtml('异常值',[{columns:['名称','金额'],rows:[{名称:'A',金额:2},{名称:'B',金额:Infinity}]}])
  assert.ok(!html.includes('class="bar-row"'))
})

test('ratio metrics use percent consistently without altering quantities or existing percent units',async()=>{
 const {formatMetric,formatMetricDifference,renderMarkdownHtml}=await import('../src/utils/answerPresentation.js')
 assert.equal(formatMetric(0.0394,'环比'),'3.94%')
 assert.equal(formatMetric(-0.0778,'同比'),'-7.78%')
 assert.equal(formatMetric(0.9363,'安检覆盖率'),'93.63%')
 assert.equal(formatMetric(1.25,'同比增长率'),'125%')
 assert.equal(formatMetric(null,'环比'),'—')
 assert.equal(formatMetric('3.94%','环比'),'3.94%')
 assert.equal(formatMetric(3.94,'环比_%'),'3.94%')
 assert.equal(formatMetric(0.5,'占比_%'),'0.5%')
 assert.equal(formatMetric(93.63,'覆盖率',{report_config:{metrics:[{column:'覆盖率',format:'percent'}]}}),'93.63%')
 assert.equal(formatMetric(1018674,'增减量_方'),'1,018,674')
 assert.equal(formatMetric(2.5,'平均气价_元'),'2.5')
 assert.equal(formatMetricDifference(0.02,'覆盖率'),'2 个百分点')
 const ds={columns:['分公司','环比','增减量_方'],rows:[{'分公司':'沙湖','环比':0.0394,'增减量_方':1018674}]}
 const html=answerHtml('环比',[ds])
 assert.match(html,/3.94%/);assert.match(html,/1,018,674/)
 assert.match(renderMarkdownHtml('| 公司 | 环比 |\n| --- | --- |\n| 沙湖 | 0.0394 |'),/3.94%/)
 assert.equal(ds.rows[0]['环比'],0.0394)
})
