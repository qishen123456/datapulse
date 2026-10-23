// Live services, no transport fixtures. Uses only the local simulated gas dataset.
import { createRequire } from 'node:module'
import { execFileSync } from 'node:child_process'
import { mkdir,writeFile } from 'node:fs/promises'
import assert from 'node:assert/strict'
const require=createRequire(import.meta.url)
const {chromium}=require(process.env.PLAYWRIGHT_MODULE || 'playwright')
const loginCode=`import requests,json
from controllers.auth import _admin_config
c=_admin_config();r=requests.post('http://127.0.0.1:5002/api/auth/login',json={'username':c['username'],'password':c['password']},timeout=10);r.raise_for_status();print(json.dumps({'token':r.json()['token']}))`
const {token}=JSON.parse(execFileSync('docker',['exec','-e','PYTHONPATH=/app/backend','askdesk-backend','python','-c',loginCode],{encoding:'utf8'}))
const browser=await chromium.launch({headless:true,executablePath:process.env.PLAYWRIGHT_CHROMIUM || undefined})
const page=await browser.newPage({viewport:{width:1440,height:1100},reducedMotion:'reduce'})
await page.addInitScript(value=>localStorage.setItem('auth_token',value),token)
const errors=[];page.on('pageerror',e=>errors.push(e.message))
const output=process.env.GAS_STUDIO_SCREENSHOTS || '/private/tmp/gas-studio-live'
await mkdir(output,{recursive:true})
let originalFlowConfig=null
try{
  await page.goto('http://127.0.0.1:8888/ask')
  await page.locator('.cmp-textarea').waitFor()
  assert.equal(await page.locator('.path-selector').count(),0,'path selection is console-controlled')
  await page.waitForFunction(()=>!document.querySelector('.el-loading-mask'))
  await page.screenshot({path:output+'/首页.png',fullPage:true,animations:'disabled'})
  await page.locator('.cmp-dataset-select').click()
  await page.getByRole('option',{name:process.env.GAS_LIVE_DATASET || '江城燃气·经营与供销差',exact:true}).click()
  await page.locator('.cmp-textarea').fill(process.env.GAS_LIVE_QUESTION || '2026年9月各分公司销气量排名')
  const started=Date.now()
  const ordinaryResponse=page.waitForResponse(r=>new URL(r.url()).pathname==='/api/ask-chat/stream' && r.request().method()==='POST',{timeout:180000})
  await page.locator('.cmp-textarea').press('Enter')
  await page.locator('.analysis-brief').getByText('已准备本次查询依据',{exact:true}).first().waitFor({timeout:120000})
  await page.screenshot({path:output+'/执行中的分析依据.png',fullPage:true,animations:'disabled'})
  if(process.env.GAS_LIVE_INSPECTOR==='1'){
    await page.getByRole('button',{name:'分析过程',exact:true}).click()
    const panel=page.getByRole('complementary',{name:'分析过程面板'})
    await panel.locator('.phase-rail .running').first().waitFor({timeout:30000})
    assert.equal(await panel.locator('.mission-label strong').innerText(),'正在分析')
    await page.screenshot({path:output+'/实时分析过程.png',fullPage:true,animations:'disabled'})
    await panel.getByRole('button',{name:'收起分析过程',exact:true}).click()
  }
  await page.locator('.answer-canvas').waitFor({timeout:180000})
  const stream=await (await ordinaryResponse).text()
  const frames=stream.split(/\n\n/).map(frame=>{const data=frame.split('\n').filter(line=>line.startsWith('data: ')).map(line=>line.slice(6)).join('\n');return data?{event:frame.match(/event: (\w+)/)?.[1],data:JSON.parse(data)}:null}).filter(Boolean)
  const answer=frames.find(frame=>frame.event==='result')?.data
  assert.equal(answer?.dataset_results?.[0]?.analysis_status,'model_generated','exact example must be interpreted by AI')
  const traces=frames.filter(frame=>frame.event==='trace').map(frame=>frame.data.event || frame.data)
  const modelStages=['agent2.sql_generate','agent4.analysis'].filter(stage=>traces.some(event=>event.stage===stage && event.status==='response'))
  assert.deepEqual(modelStages,['agent2.sql_generate','agent4.analysis'],'must observe real model responses for SQL and interpretation')
  assert.ok(!(await page.locator('.answer-canvas').last().innerText()).includes('达成率'))
  await page.locator('.answer-canvas').last().scrollIntoViewIfNeeded()
  await page.locator('.answer-canvas .evidence-chart canvas').last().waitFor()
  await page.screenshot({path:output+'/普通问数.png',fullPage:true,animations:'disabled'})
  await page.locator('.answer-toolbar').last().getByRole('button',{name:'数据',exact:true}).click()
  assert.match(await page.locator('.answer-table').last().innerText(),/经开分公司/)
  const activities=answer.workflow.events.map(e=>e.activity).filter(Boolean)
  assert(activities.some(a=>a.kind==='assets'),'must expose actual context')
  assert(activities.some(a=>a.kind==='data'),'must expose actual returned rows')
  const basicMs=Date.now()-started
  if(process.env.GAS_LIVE_INSPECTOR==='1'){
    await page.getByRole('button',{name:'查看分析过程 ↗',exact:true}).last().click()
    const panel=page.getByRole('complementary',{name:'分析过程面板'})
    assert.equal(await panel.locator('.mission-label strong').innerText(),await page.locator('.journey-state').last().innerText())
    assert.equal(await panel.locator('.phase-rail .running').count(),0)
    assert.equal(await panel.locator('.step-detail .running').count(),0)
    await page.screenshot({path:output+'/完成后的分析过程.png',fullPage:true,animations:'disabled'})
    await panel.getByRole('button',{name:'查询依据',exact:true}).click()
    assert.ok((await panel.locator('.inspector-sql').innerText()).includes('SELECT'))
    await page.screenshot({path:output+'/查询依据面板.png',fullPage:true,animations:'disabled'})
    await panel.getByRole('button',{name:'收起分析过程',exact:true}).click()
  }
  await page.locator('.row-focus-button').first().click()
  await page.getByLabel('选择对照记录').selectOption('1')
  assert.match(await page.locator('.focus-lens').innerText(),/差值（右 − 左）/)
  await page.getByRole('button',{name:'把这两个对象带入追问 ↗'}).click()
  assert.match(await page.locator('.cmp-textarea').inputValue(),/基于上一问/)
  await page.locator('.answer-toolbar').last().getByRole('button',{name:'图表',exact:true}).click()
  await page.locator('.focus-lens').scrollIntoViewIfNeeded()
  await page.screenshot({path:output+'/数据聚焦对照.png',fullPage:true,animations:'disabled'})
  await page.setViewportSize({width:390,height:1000})
  assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),true)
  await page.locator('.focus-lens').scrollIntoViewIfNeeded()
  await page.screenshot({path:output+'/聚焦镜_手机.png',fullPage:true,animations:'disabled'})
  await page.setViewportSize({width:1440,height:1100})
  if(process.env.GAS_LIVE_BASIC_ONLY==='1'){
    const response=await page.request.get(`http://127.0.0.1:8888/api/datasets/${process.env.GAS_LIVE_DATASET_ID || 64}/report-config`,{headers:{'X-Auth-Token':token}})
    const reportConfig=await response.json()
    assert.equal((reportConfig.config || reportConfig.default_config)?.profile,'generic')
    assert.deepEqual(errors,[])
    await writeFile(output+'/普通结果验收.json',JSON.stringify({status:'passed',basicUiMs:basicMs,reportProfile:'generic',analysisStatus:answer.dataset_results[0].analysis_status,modelStages,errors},null,2))
    console.log('PASS: live ordinary answer, chart/data, generic report config, latest deployment')
  }else{
  await page.getByRole('button',{name:'新会话',exact:true}).click()
  await page.getByRole('dialog',{name:'开始新会话'}).getByRole('button',{name:'开始新会话',exact:true}).click()
  const flowRead=await page.request.get('http://127.0.0.1:8888/api/admin/ask-flow',{headers:{'X-Auth-Token':token}})
  assert.equal(flowRead.status(),200)
  originalFlowConfig=(await flowRead.json()).data.config
  const rolePolicy={...originalFlowConfig,advancedEnabled:true,advancedRoles:[...new Set([...(originalFlowConfig.advancedRoles || []),'super_admin'])],rolePolicies:{...originalFlowConfig.rolePolicies,super_admin:'advanced'}}
  const flowWrite=await page.request.put('http://127.0.0.1:8888/api/admin/ask-flow',{headers:{'X-Auth-Token':token},data:{config:rolePolicy}})
  assert.equal(flowWrite.status(),200)
  await page.evaluate(()=>window.dispatchEvent(new CustomEvent('datapulse-feature-flags-updated')))

  await page.locator('.cmp-textarea').fill('分析2026年9月分公司销气量与估抄率的差异，先分别核验这两个指标')
  await page.locator('.cmp-textarea').press('Enter')
  await page.getByRole('heading',{name:'先审阅研究计划'}).waitFor({timeout:120000})
  await page.screenshot({path:output+'/研究计划.png',fullPage:true,animations:'disabled'})
  const boxes=page.locator('.plan-branch input')
  for(let i=2;i<await boxes.count();i++)await boxes.nth(i).uncheck()
  await page.getByRole('button',{name:'确认计划，开始取证'}).click()
  await page.getByRole('heading',{name:'研究报告',exact:true}).waitFor({timeout:180000})
  await page.locator('.research-report').scrollIntoViewIfNeeded()
  assert.ok((await page.locator('.research-report').innerText()).includes('DATAPULSE / RESEARCH NOTE'))
  await page.screenshot({path:output+'/研究报告.png',fullPage:true,animations:'disabled'})
  await page.getByRole('button',{name:'证据索引',exact:true}).click()
  await page.screenshot({path:output+'/证据索引.png',fullPage:true,animations:'disabled'})
  await page.setViewportSize({width:390,height:1000})
  assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),true)
  await page.screenshot({path:output+'/手机布局.png',fullPage:true,animations:'disabled'})
  assert.deepEqual(errors,[])
  await writeFile(output+'/结果.json',JSON.stringify({status:'passed',basicUiMs:basicMs,transport:'real',errors},null,2))
  console.log('PASS: live ordinary query, advanced plan approval, evidence report, mobile layout; screenshots saved')
  }
}finally{
  if(originalFlowConfig)await page.request.put('http://127.0.0.1:8888/api/admin/ask-flow',{headers:{'X-Auth-Token':token},data:{config:originalFlowConfig}})
  await page.request.post('http://127.0.0.1:8888/api/auth/logout',{headers:{'X-Auth-Token':token}})
  await browser.close()
}
