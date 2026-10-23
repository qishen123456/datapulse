// Run against a local Vite server. Transport fixtures exercise the real Vue app;
// they deliberately do not assert live warehouse/model accuracy.
import { createRequire } from 'node:module'
import assert from 'node:assert/strict'
import { readFile } from 'node:fs/promises'
const require = createRequire(import.meta.url)
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright')
const browser = await chromium.launch({ headless: true, executablePath: process.env.PLAYWRIGHT_CHROMIUM || undefined })
const page = await browser.newPage({ viewport: { width: 1440, height: 1000 } })
await page.addInitScript(() => { if(window===window.top)localStorage.setItem('auth_token','isolated-ui-fixture') })
page.on('console',m=>{if(m.type()==='error')console.error('BROWSER',m.text())})
page.on('requestfailed',r=>console.error('FAILED',r.url(),r.failure()?.errorText))
const errors = []
page.on('pageerror', e => errors.push(e.message))
let starts = 0, confirmations = 0, basicStarts = 0
let queueTestMode=false
let basicGates=[]
let queuedRequests=[]
let savedPolicy = null
let featureOverrides = {}
let flowConfig = { defaultFlow: "basic", advancedEnabled:true, advancedRoles:["super_admin"], datasetPolicies:{}, maxParallel:3, maxRetries:2, queryTimeoutSeconds:30, maxResultRows:10000, attachMetadata:true }
const plan = { id: 'research-ui-test', question: '9月收入为什么下降', branches: [{ id:'b1',title:'订单量变化',hypothesis:'检查订单数量变化',question:'9月订单量',dataset_id:1 },{ id:'b2',title:'产品结构变化',hypothesis:'检查产品结构变化',question:'9月产品结构',dataset_id:1 }], limits:{maxParallel:2} }
const catalog = [{id:'R14',title:'审阅研究计划',role:'主理人'},{id:'R15',title:'并行派发任务',role:'主理人'},{id:'R29',title:'提取分支证据',role:'领域专家'}]
const dataset = { dataset_id:1,dataset_name:'演示订单',columns:['战区','收入'],rows:[{'战区':'华东','收入':26},{'战区':'华南','收入':22}],row_count:2,sql:'SELECT region, SUM(revenue) AS revenue FROM demo GROUP BY region',agent3_review:{approved:true},analysis:'两战区收入合计48万元。' }
const evidence = [{...plan.branches[0],status:'completed',finding:'订单量查询已完成，结果可核对。',row_count:2,dataset_results:[dataset]},{...plan.branches[1],status:'insufficient',finding:'当前数据无法核验产品结构假设。',dataset_results:[]}]
const frame = (name, data) => `event: ${name}\ndata: ${JSON.stringify(data)}\n\n`
await page.route('**/api/**', async route => {
  const path = new URL(route.request().url()).pathname
  if (!path.startsWith('/api/')) { await route.continue(); return }
  let data = { success:true,data:{} }
  if (path === '/api/auth/me') data = { authenticated:true,user:{id:1,name:'视觉验收',username:'ui-test',role:'super_admin'} }
  else if (path === '/api/health') data = {status:'ok'}
  else if (path === '/api/feature-flags') data = {success:true,data:{features:featureOverrides}}
  else if (path === '/api/bookshelves/datasets') data = {datasets:[{id:1,dataset_name:'演示订单',dataset_code:'demo'}]}
  else if (path.includes('common-questions')) data = {questions:[]}
  else if (path === '/api/ai-models/active') data = {models:[]}
  else if (path.includes('report-history')) data = {history:[],success:true}
  else if (path === '/api/admin/ask-flow') {
    if (route.request().method() === 'PUT') { savedPolicy = route.request().postDataJSON().config; flowConfig = savedPolicy }
    data = { success:true,data:{config:flowConfig,effectiveDecision:{flow:'basic',reason:'basic_selected'}} }
  }
  else if (path === '/api/ask-chat/capabilities') data = {success:true,data:{defaultFlow:flowConfig.rolePolicies?.super_admin || flowConfig.defaultFlow,advancedAvailable:true,attachMetadata:true,authorizationScope:'fixture-scope',reportDownloadAvailable:true,scopeLabel:'当前账号授权组织 · 两条路径均强制校验'}}
  else if (path === '/api/ask-chat/stream') {
    const body = route.request().postDataJSON()
    if ((flowConfig.rolePolicies?.super_admin || flowConfig.defaultFlow) === 'basic') {
      basicStarts++
      if(queueTestMode){queuedRequests.push(body);await new Promise(resolve=>basicGates.push(resolve))}
      const result={question:'9月收入多少',requires_confirmation:false,dataset_results:[dataset],...dataset,analysis:'华东、华南收入合计48万元。',route:{dataset_ids:[1]},workflow:{run_id:'run-basic',flow:'basic',catalog:[{id:'L9',title:'受控执行'}],events:[{run_id:'run-basic',seq:2,node_id:'L9',status:'completed',title:'受控执行',summary:'已返回2行'}],status:'completed'}}
      result.workflow.events[0].activity={kind:'data',heading:'查询已返回数据',row_count:dataset.rows.length,columns:dataset.columns}
      result.workflow.events.unshift({run_id:'run-basic',seq:1.1,node_id:'L2',status:'completed',title:'匹配数据资产',summary:'已读取字段与关联依据',activity:{kind:'assets',heading:'已准备本次查询依据',dataset_name:'演示订单',field_count:64,relation_count:4,reference_count:12,question:body.question,time_mentions:['9月']}})
      result.workflow.events.splice(1,0,{run_id:'run-basic',seq:1.2,node_id:'L5',status:'completed',title:'生成查询',activity:{kind:'query',dataset_name:'演示订单',public_summary:'按战区汇总9月收入，保持月份和收入统计口径一致。',methods:['SUM'],aggregation:['按查询维度分组']}},{run_id:'run-basic',seq:1.3,node_id:'L6',status:'completed',title:'审核查询',activity:{kind:'review',approved:true}})
      if(dataset.query_status==='failed')result.workflow.events=[{run_id:'run-basic',seq:2,node_id:'L5',attempt:0,title:'生成查询',status:'failed'},{run_id:'run-basic',seq:3,node_id:'L5',attempt:1,title:'生成查询',status:'completed'},{run_id:'run-basic',seq:4,node_id:'L6',attempt:0,title:'审查查询',status:'running'},{run_id:'run-basic',seq:5,node_id:'L6',attempt:1,title:'审查查询',status:'failed'}]
      await route.fulfill({contentType:'text/event-stream',body:frame('workflow',{event:{type:'started',run_id:'run-basic',flow:'basic',seq:1}})+frame('result',result)+frame('done',{ok:true})});return
    }
    assert.ok(!body.ask_flow || body.ask_flow==='advanced')
    starts++
    const result = {authorization_scope:'fixture-scope',question:plan.question,requires_confirmation:true,confirmation_type:'research_plan',research_plan:plan,session_id:plan.id,route:{dataset_ids:[1]},workflow:{run_id:'run-plan',flow:'advanced',catalog,events:[],status:'waiting'}}
    await route.fulfill({contentType:'text/event-stream',body:frame('workflow',{event:{type:'started',run_id:'run-plan',seq:1,flow:'advanced',catalog}})+frame('result',result)+frame('done',{ok:true})});return
  } else if (path === '/api/ask-chat/confirm-by-boss/stream') {
    const body = route.request().postDataJSON()
    assert.deepEqual(body.plan_branch_ids,['b1','b2'])
    assert.ok(!body.ask_flow || body.ask_flow==='advanced')
    confirmations++
    const events = [{type:'workflow',run_id:'run-evidence',seq:2,flow:'advanced',node_id:'R15',status:'running',branches:plan.branches},...evidence.map((e,i)=>({type:'workflow',run_id:'run-evidence',seq:3+i,flow:'advanced',node_id:'R29',branch_id:e.id,status:e.status,evidence:e,title:'提取分支证据',summary:e.finding}))]
    const result = {authorization_scope:'fixture-scope',question:plan.question,requires_confirmation:false,research_plan:plan,research:{evidence,gaps:['产品结构变化'],partial:true,boundary:'描述性证据不构成因果证明。',summary:{conclusion:'已完成订单量事实查询，产品结构仍待验证。',findings:[{text:'订单量已核对。',evidence_ids:['b1']}]}},dataset_results:[dataset],workflow:{run_id:'run-evidence',flow:'advanced',catalog,events,status:'completed'}}
    await route.fulfill({contentType:'text/event-stream',body:frame('workflow',{event:{type:'started',run_id:'run-evidence',seq:1,flow:'advanced',catalog}})+events.map(event=>frame('workflow',{event})).join('')+frame('result',result)+frame('done',{ok:true})});return
  }
  await route.fulfill({contentType:'application/json',body:JSON.stringify(data)})
})
try {
  await page.goto(process.env.ASK_UI_URL || 'http://127.0.0.1:5174/ask')
  await page.getByRole('heading',{name:'让数据，回答业务问题。'}).waitFor()
  await page.screenshot({path:'/private/tmp/ask-studio-home.png',fullPage:true})
  await page.locator('.cmp-textarea').fill('9月收入多少')
  await page.locator('.cmp-textarea').press('Enter')
  await page.getByRole('heading',{name:'本次查询依据'}).waitFor()
  await page.locator('.answer-canvas').waitFor()
  await page.screenshot({path:'/private/tmp/ask-answer-default.png',fullPage:false,animations:'disabled'})
  await page.locator('.journey-evidence > summary').click()
  assert.equal(await page.locator('.query-journey .brief-fact').count(),6)
  assert.match(await page.locator('.query-journey [data-fact=plan]').innerText(),/按战区汇总9月收入/)
  assert.match(await page.locator('.query-journey [data-fact=aggregation]').innerText(),/求和.*按查询维度分组/)
  assert.match(await page.locator('.query-journey [data-fact=results]').innerText(),/返回 2 行 · 2 个字段/)
  await page.screenshot({path:'/private/tmp/ask-six-facts.png',fullPage:false,animations:'disabled'})
  await page.locator('.query-journey .brief-records > summary').click()
  await page.getByText('64 个字段定义 · 4 条表关联 · 12 个 SQL 参考样例',{exact:true}).first().waitFor()
  await page.getByRole('button',{name:'查看分析过程 ↗',exact:true}).click()
  const inspector=page.getByRole('complementary',{name:'分析过程面板'})
  await inspector.getByRole('heading',{name:'分析过程',exact:true}).waitFor()
  await inspector.getByRole('button',{name:'查询依据',exact:true}).click()
  assert.match(await inspector.locator('.inspector-sql').innerText(),/SELECT region/)
  assert.equal(await page.locator('.ax-side-report').count(),0,'inspector must not contain a second report')
  await inspector.getByRole('button',{name:'报告',exact:true}).click()
  const reportFrame=page.frameLocator('iframe[title="本轮 HTML 分析报告"]')
  await reportFrame.getByRole('heading',{name:'结果解读与业务建议'}).waitFor()
  assert.match(await reportFrame.locator('body').innerText(),/48万元/)
  await inspector.getByRole('button',{name:'放大阅读 ↗',exact:true}).click()
  await page.frameLocator('iframe[title="完整 HTML 分析报告"]').getByRole('heading',{name:'结果解读与业务建议'}).waitFor()
  await page.screenshot({path:'/private/tmp/ask-html-report.png',fullPage:true,animations:'disabled'})
  await page.locator('.ax-report-dialog-actions').getByRole('button',{name:'关闭',exact:true}).click()
  await inspector.getByRole('button',{name:'进展',exact:true}).click()
  await page.screenshot({path:'/private/tmp/ask-inspector-success.png',fullPage:true})
  await page.setViewportSize({width:390,height:900})
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1))
  const inspectorBox=await inspector.boundingBox()
  assert.ok(inspectorBox && inspectorBox.height>700 && inspectorBox.width<=390,'mobile inspector should use the screen height')
  await page.screenshot({path:'/private/tmp/ask-inspector-mobile.png',fullPage:true})
  await page.setViewportSize({width:1440,height:1000})
  await inspector.getByRole('button',{name:'收起分析过程',exact:true}).click()
  await page.locator('.answer-toolbar').getByRole('button',{name:'数据',exact:true}).click()
  assert.match(await page.locator('.answer-table').innerText(),/华东/)
  assert.ok(!(await page.locator('.answer-canvas').innerText()).includes('达成率'))
  await page.getByRole('button',{name:'聚焦第1行：华东',exact:true}).click()
  await page.getByLabel('选择对照记录').selectOption('1')
  assert.match(await page.locator('.focus-lens').innerText(), /-4/)
  await page.locator('.answer-table thead').getByRole('button',{name:'收入',exact:true}).click()
  assert.equal(await page.getByRole('button',{name:'聚焦第1行：华东',exact:true}).getAttribute('aria-pressed'),'true')
  await page.getByRole('button',{name:'把这两个对象带入追问 ↗'}).click()
  assert.match(await page.locator('.cmp-textarea').inputValue(),/华东.*华南/)
  assert.equal(basicStarts,1,'follow-up only fills a draft')
  for (const width of [768,390]) {
    await page.setViewportSize({width,height:1000})
    assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth <= window.innerWidth+1),true,`focus lens overflow at ${width}`)
  }
  await page.setViewportSize({width:1440,height:1000})
  await page.getByRole('button',{name:'清除选择 ×'}).click()
  assert.equal(await page.locator('.focus-lens').count(),0)
  await page.locator('.answer-toolbar').getByRole('button',{name:'图表',exact:true}).click()
  // Click the actual inferred bar, exercising ECharts-to-source index mapping.
  const canvas=page.locator('.answer-visual .evidence-chart canvas').first()
  await canvas.scrollIntoViewIfNeeded()
  await canvas.click({position:{x:260,y:95}})
  await page.locator('.focus-lens').waitFor()
  assert.match(await page.locator('.focus-lens').innerText(),/华东/)
  await page.getByLabel('选择对照记录').selectOption('1')

  await page.screenshot({path:'/private/tmp/ask-studio-answer.png',fullPage:true})
  assert.equal(basicStarts,1)
  featureOverrides={ask_quick_ask:{available:false},ask_report_download:{available:false},debug_execution_trace:{available:false}}
  await page.evaluate(()=>window.dispatchEvent(new CustomEvent('datapulse-feature-flags-updated')))
  await page.waitForFunction(()=>!document.querySelector('.lens-next'))
  assert.equal(await page.locator('.answer-actions button').count(),0,'console download flag is respected')
  assert.equal(await page.getByRole('button',{name:'查看分析过程 ↗',exact:true}).count(),0,'console trace flag hides the inspector entry')
  featureOverrides={}
  await page.evaluate(()=>window.dispatchEvent(new CustomEvent('datapulse-feature-flags-updated')))
  await page.locator('.lens-next').waitFor()
  await page.getByRole('button',{name:'新会话',exact:true}).click()
  await page.getByRole('dialog',{name:'开始新会话'}).getByRole('button',{name:'开始新会话',exact:true}).click()
  flowConfig.defaultFlow='advanced'
  assert.equal(await page.locator('.path-selector').count(),0)
  await page.evaluate(()=>window.dispatchEvent(new CustomEvent('datapulse-feature-flags-updated')))
  await page.locator('.cmp-textarea').fill(plan.question)
  await page.locator('.cmp-textarea').press('Enter')
  await page.getByRole('heading',{name:'先审阅研究计划'}).waitFor()
  assert.equal(starts,1)
  const checkboxes = page.locator('.plan-branch input')
  await checkboxes.nth(1).uncheck()
  assert.equal(await page.locator('.plan-actions').innerText().then(t=>t.includes('已选 1 项')),true)
  await checkboxes.nth(1).check()
  await page.screenshot({path:'/private/tmp/ask-research-plan.png',fullPage:true})
  await page.getByRole('button',{name:'确认计划，开始取证'}).click()
  await page.getByRole('heading',{name:'研究报告',exact:true}).waitFor()
  await page.getByText('已完成订单量事实查询，产品结构仍待验证。').waitFor()
  await page.locator('.evidence-compass').getByRole('button',{name:/订单量变化/}).click()
  assert.equal(await page.locator('.report-finding').count(),1)
  assert.match(await page.locator('.report-finding').innerText(),/订单量变化/)
  await page.locator('.research-report').screenshot({path:'/private/tmp/ask-evidence-compass-fixture.png'})
  await page.getByRole('button',{name:'恢复全部方向 ↗'}).click()
  assert.equal(await page.locator('.report-finding').count(),2)
  await page.getByRole('button',{name:'证据索引',exact:true}).click()
  await page.locator('.evidence-index').waitFor()
  await page.getByRole('button',{name:'边界与待补证',exact:true}).click()
  assert.match(await page.locator('.report-limits').innerText(),/产品结构变化/)
  await page.getByRole('button',{name:'结论摘要',exact:true}).click()
  assert.equal(confirmations,1)
  const downloading = page.waitForEvent('download')
  await page.getByRole('button',{name:'下载研究报告 ↗'}).click()
  const download = await downloading
  assert.ok(download.suggestedFilename().endsWith('.html'))
  const exported = await readFile(await download.path(),'utf8')
  assert.ok(exported.includes('产品结构变化') && !exported.includes('SELECT region'))
  await page.getByRole('button',{name:'查看该发现的证据 ↗'}).first().click()
  await page.locator('.evidence-drawer table').waitFor()
  assert.match(await page.locator('.evidence-drawer').innerText(),/华东/)
  await page.screenshot({path:'/private/tmp/ask-research-report.png',fullPage:true})
  for (const width of [1024,768,390]) {
    await page.setViewportSize({width,height:1000})
    assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth <= window.innerWidth+1),true,`overflow at ${width}`)
    assert.ok(await page.locator('.research-desk').evaluate(el=>el.getBoundingClientRect().width) >= 300,`research width at ${width}`)
    await page.screenshot({path:`/private/tmp/ask-research-${width}.png`,fullPage:true})
  }
  assert.equal(await page.locator('.ax-detail-panel-container').isVisible(),false)
  await page.setViewportSize({width:1440,height:1000})
  await page.goto((process.env.ASK_UI_URL || 'http://127.0.0.1:5174/ask').replace(/\/ask$/, '/admin-console?tab=ask-flow'))
  await page.getByRole('heading',{name:'双路径问数控制'}).waitFor()
  await page.locator('.ask-flow-card').filter({has:page.getByRole('heading',{name:'双路径问数控制'})}).getByRole('button',{name:'展开设置'}).click()
  await page.locator('.role-route-policy .el-select').nth(2).click()
  await page.getByRole('option',{name:'高阶研究',exact:true}).click()
  const parallelInput=page.locator('.flow-setting-item').filter({hasText:'高阶并发上限'}).locator('input')
  await parallelInput.fill('4'); await parallelInput.blur()
  const retryInput=page.locator('.flow-setting-item').filter({hasText:'全任务修复预算'}).locator('input')
  await retryInput.fill('1'); await retryInput.blur()
  const savedResponse = page.waitForResponse(r=>new URL(r.url()).pathname==='/api/admin/ask-flow' && r.request().method()==='PUT')
  await page.getByRole('button',{name:'保存流程配置'}).last().click()
  await savedResponse
  assert.equal(savedPolicy.rolePolicies.admin,'advanced')
  assert.equal(savedPolicy.maxParallel,4)
  assert.equal(savedPolicy.maxRetries,1)
  assert.equal(savedPolicy.fallbackToBasicOnError,false)
  // A failed model/query must never masquerade as an empty business scope.
  featureOverrides={}
  Object.assign(dataset,{query_status:'failed',analysis_status:'model_unavailable',rows:[],columns:[],row_count:0,sql:'',agent3_review:{approved:false},analysis:'围绕这个问题没有查到匹配数据。'})
  await page.goto(process.env.ASK_UI_URL || 'http://127.0.0.1:5174/ask')
  flowConfig.defaultFlow='basic'
  assert.equal(await page.locator('.path-selector').count(),0)
  await page.locator('.cmp-textarea').fill('复核查询失败的提示')
  await page.locator('.cmp-textarea').press('Enter')
  await page.locator('.canvas-empty h3').last().waitFor()
  assert.equal(await page.locator('.canvas-empty h3').last().innerText(),'查询未完成，请重试')
  assert.ok(!(await page.locator('.answer-canvas').last().innerText()).includes('没有查到匹配数据'))
  await page.screenshot({path:'/private/tmp/ask-query-failure.png',fullPage:true})
  await page.getByRole('button',{name:'查看分析过程 ↗',exact:true}).last().click()
  const failedInspector=page.getByRole('complementary',{name:'分析过程面板'})
  assert.equal(await failedInspector.locator('.mission-label strong').innerText(),'查询未完成')
  assert.equal(await page.locator('.journey-state').last().innerText(),'查询未完成')
  assert.equal(await failedInspector.locator('.mini-status.running').count(),0)
  assert.equal(await failedInspector.locator('.phase-rail .running').count(),0)
  assert.equal(await page.locator('.cmp-status.failed .cmp-status-dot').evaluate(el=>getComputedStyle(el).animationName),'none')
  await failedInspector.getByRole('button',{name:/诊断/}).click()
  await failedInspector.getByRole('button',{name:'定位到该步骤 ↗'}).first().waitFor()
  await page.screenshot({path:'/private/tmp/ask-inspector-failed.png',fullPage:true})
  await failedInspector.getByRole('button',{name:'进展',exact:true}).click()
  const requestsBeforeRetry=basicStarts
  await failedInspector.getByRole('button',{name:'把原问题带回输入框 ↗'}).click()
  assert.equal(await page.locator('.cmp-textarea').inputValue(),'9月收入多少')
  assert.equal(basicStarts,requestsBeforeRetry,'retry action must fill a draft rather than silently resend')
  await failedInspector.getByRole('button',{name:'收起分析过程',exact:true}).click()

  Object.assign(dataset,{query_status:'completed',analysis_status:'model_generated',agent3_review:{approved:true},sql:'SELECT region FROM demo WHERE false',analysis:'查询已执行，指定月份没有匹配记录。'})
  await page.locator('.cmp-textarea').fill('复核真实空结果的提示')
  await page.locator('.cmp-textarea').press('Enter')
  await page.getByText('查询已执行，指定月份没有匹配记录。',{exact:true}).first().waitFor()
  assert.equal(await page.locator('.canvas-empty h3').last().innerText(),'当前范围没有返回记录')
  // Hold real fetch responses to exercise typing/queueing while a request is pending.
  Object.assign(dataset,{query_status:'completed',analysis_status:'model_generated',rows:[{'战区':'华东','收入':26},{'战区':'华南','收入':22}],columns:['战区','收入'],row_count:2,agent3_review:{approved:true},sql:'SELECT region, SUM(revenue) AS revenue FROM demo GROUP BY region',analysis:'查询完成。'})
  queueTestMode=true
  await page.locator('.cmp-textarea').fill('队列测试：当前问题')
  await page.locator('.cmp-textarea').press('Enter')
  await page.getByRole('button',{name:'加入问数队列',exact:true}).waitFor()
  assert.equal(await page.locator('.cmp-textarea').isEnabled(),true)
  assert.equal(await page.locator('.cmp-activity-ribbon').count(),1)
  await page.locator('.cmp-textarea').fill('队列测试：第二问')
  await page.locator('.cmp-textarea').press('Enter')
  await page.locator('.cmp-textarea').fill('队列测试：第三问')
  await page.locator('.cmp-textarea').press('Enter')
  const queue=page.getByRole('region',{name:'待问队列'})
  await queue.waitFor()
  assert.equal(await queue.locator('.queued-list li').count(),2)
  assert.equal(queuedRequests.length,1,'pending questions must not start concurrently')
  const ringBox=await page.locator('.cmp-activity-ribbon').boundingBox()
  const inputBox=await page.locator('.cmp-dock').boundingBox()
  assert(ringBox.height>80 && Math.abs(ringBox.height-inputBox.height)<5,'running border covers all four sides of the composer')
  assert.match(await page.locator('.cmp-dock').evaluate(el=>getComputedStyle(el).animationName),/^composer-orbit/)
  await page.screenshot({path:'/private/tmp/ask-composer-perimeter.png',fullPage:true,animations:'disabled'})
  await page.locator('.cmp-textarea').fill('这是一段未发送的新草稿')
  await page.screenshot({path:'/private/tmp/ask-question-queue.png',fullPage:true,animations:'disabled'})
  await page.setViewportSize({width:390,height:1000})
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),'mobile queue overflow')
  const mobileDataset=await page.locator('.cmp-dataset-select').boundingBox()
  const mobileModel=await page.locator('.cmp-model-select').boundingBox()
  assert.ok(mobileDataset.y+mobileDataset.height<=mobileModel.y+1,'mobile dataset/model controls must not overlap')
  await page.screenshot({path:'/private/tmp/ask-question-queue-mobile.png',fullPage:true,animations:'disabled'})
  await page.setViewportSize({width:1440,height:1000})
  await page.emulateMedia({reducedMotion:'reduce'})
  assert.equal(await page.locator('.cmp-dock').evaluate(el=>getComputedStyle(el).animationName),'none')
  await page.emulateMedia({reducedMotion:'no-preference'})
  await queue.getByRole('button',{name:'暂停队列 Ⅱ',exact:true}).click()
  basicGates.shift()()
  await page.waitForFunction(()=>!document.querySelector('.cmp.is-running'))
  assert.equal(queuedRequests.length,1,'manual pause holds subsequent questions')
  assert.equal(await page.locator('.cmp-textarea').inputValue(),'这是一段未发送的新草稿')
  await queue.getByRole('button',{name:'继续队列 ▶',exact:true}).click()
  await page.waitForFunction(()=>document.querySelector('.cmp.is-running'))
  const queueDeadline=Date.now()+45000
  while(basicGates.length===0){assert.ok(Date.now()<queueDeadline,'second queued request did not start');await new Promise(resolve=>setTimeout(resolve,25))}
  assert.equal(queuedRequests[1].question,'队列测试：第二问')
  assert.equal(await page.locator('.cmp-textarea').inputValue(),'这是一段未发送的新草稿')
  basicGates.shift()()
  while(queuedRequests.length<3 || basicGates.length===0){assert.ok(Date.now()<queueDeadline,'third queued request did not start');await new Promise(resolve=>setTimeout(resolve,25))}
  assert.equal(queuedRequests[2].question,'队列测试：第三问')
  basicGates.shift()()
  await page.waitForFunction(()=>!document.querySelector('.cmp.is-running'))
  assert.equal(await page.locator('.question-queue').count(),0)
  assert.equal(await page.locator('.cmp-textarea').inputValue(),'这是一段未发送的新草稿')
  assert.deepEqual(queuedRequests.map(r=>r.ask_flow),[undefined,undefined,undefined],'user requests defer to console policy rather than a pinned path')
  await page.locator('.cmp-textarea').fill('队列测试：失败后暂停')
  await page.locator('.cmp-textarea').press('Enter')
  while(basicGates.length===0){assert.ok(Date.now()<queueDeadline,'failure test request did not start');await new Promise(resolve=>setTimeout(resolve,25))}
  await page.locator('.cmp-textarea').fill('队列测试：失败后保留的下一问')
  await page.locator('.cmp-textarea').press('Enter')
  Object.assign(dataset,{query_status:'failed',analysis_status:'model_unavailable',rows:[],columns:[],row_count:0,agent3_review:{approved:false},sql:''})
  basicGates.shift()()
  await page.waitForFunction(()=>!document.querySelector('.cmp.is-running'))
  await page.getByText('上一问未完成，请检查后继续队列',{exact:true}).waitFor()
  assert.equal(queuedRequests.length,4,'failed question must pause rather than run the next question')
  assert.equal(await page.locator('.queued-list li').count(),1)
  await page.getByRole('button',{name:'清空队列',exact:true}).click()
  queueTestMode=false
  assert.deepEqual(errors,[])
  console.log('PASS: real Vue plan selection, explicit confirmation, evidence report, drawer, responsive widths; no runtime errors')
} catch(error) { await page.screenshot({path:'/private/tmp/ask-ui-failure.png',fullPage:true}); console.error('PAGE ERRORS',errors); console.error((await page.locator('body').innerText()).slice(0,2500)); throw error } finally { await browser.close() }
