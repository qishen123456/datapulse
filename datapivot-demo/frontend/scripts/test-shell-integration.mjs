// Browser fixtures for the integrated navigation and capability editing UI.
// Run against a local Vite server. Transport fixtures exercise the real Vue app;
// they deliberately do not assert live warehouse/model accuracy.
import { createRequire } from 'node:module'
import assert from 'node:assert/strict'
import { readFile } from 'node:fs/promises'
const require = createRequire(import.meta.url)
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright')
const browser = await chromium.launch({ headless: true, executablePath: process.env.PLAYWRIGHT_CHROMIUM || undefined })
const page = await browser.newPage({ viewport: { width: 1440, height: 1000 } })
await page.addInitScript(() => localStorage.setItem('auth_token','isolated-ui-fixture'))
page.on('console',m=>{if(m.type()==='error')console.error('BROWSER',m.text())})
page.on('requestfailed',r=>console.error('FAILED',r.url(),r.failure()?.errorText))
const errors = []
page.on('pageerror', e => errors.push(e.message))
let skillsConfig={"version": 1, "enabled": true, "description": "维护高阶研究 Skills、并行预算与报告口径；研究工作台按计划和真实证据呈现结果。", "execution": {"emitSkillTrace": true, "preserveFinalReportContract": true, "assetPreviewLimit": 3, "fallbackToBasicEngine": false}, "skills": [{"key": "organization_scope", "label": "组织范围校验", "stage": "stability.row_security", "toolType": "dataset", "enabled": true, "order": 1, "description": "沿用组织树与账号授权，在数据集准入和 SQL 执行前强制校验。", "runtime": {"flows": ["basic", "advanced"], "promptEditable": false, "parameterEditable": false, "executor": "deterministic", "roles": []}}, {"key": "schema_link", "label": "字段关联与剪枝", "stage": "stability.context", "toolType": "dataset", "enabled": true, "order": 2, "description": "局部向量检索字段，保留组织、时间及关联键；完整元数据继续参与确定性校验。", "config": {"fieldLimit": 80}, "runtime": {"flows": ["basic", "advanced"], "promptEditable": false, "parameterEditable": true, "executor": "deterministic", "roles": []}}, {"key": "semantic_align", "label": "指标口径对齐", "stage": "stability.semantic", "toolType": "dataset", "enabled": true, "order": 3, "description": "读取指标定义与业务口径，将消歧要求传给主理人和查询专家。", "runtime": {"flows": ["basic", "advanced"], "promptEditable": true, "parameterEditable": false, "executor": "prompt", "roles": [1, 2]}}, {"key": "explain_guard", "label": "执行计划预检", "stage": "stability.explain", "toolType": "sql", "enabled": true, "order": 4, "description": "执行前进行只读、方言与 EXPLAIN 预检，拒绝高风险关联。", "runtime": {"flows": ["basic", "advanced"], "promptEditable": false, "parameterEditable": false, "executor": "deterministic", "roles": []}}, {"key": "result_assertions", "label": "数据合理性断言", "stage": "stability.assert", "toolType": "fact", "enabled": true, "order": 5, "description": "检查空结果、全空字段、非有限数值和结果规模，不把无记录解释成业务值为零。", "runtime": {"flows": ["basic", "advanced"], "promptEditable": false, "parameterEditable": false, "executor": "deterministic", "roles": []}}, {"key": "dataset_route", "label": "数据集路由 Skill", "stage": "advanced.skill.dataset_route", "toolType": "dataset", "enabled": true, "order": 10, "description": "根据问题、数据集名称、业务域和路由词识别候选数据资产。", "runtime": {"flows": ["basic", "advanced"], "promptEditable": true, "parameterEditable": false, "executor": "prompt", "roles": [1]}}, {"key": "asset_pack", "label": "资产打包 Skill", "stage": "advanced.skill.asset_pack", "toolType": "dataset", "enabled": true, "order": 20, "description": "读取字段字典、DDL、LLD、Golden SQL、常见问题和报告模板。", "runtime": {"flows": ["basic", "advanced"], "promptEditable": true, "parameterEditable": false, "executor": "prompt", "roles": [2]}}, {"key": "route_guard", "label": "路由守门 Skill", "stage": "advanced.skill.route_guard", "toolType": "dataset", "enabled": true, "order": 25, "description": "结合组织树和候选数据集得分判断是否自动锁定、提示确认或识别错配。", "runtime": {"flows": ["basic", "advanced"], "promptEditable": true, "parameterEditable": false, "executor": "prompt", "roles": [1]}}, {"key": "planner", "label": "任务规划 Planner", "stage": "advanced.planner", "toolType": "fact", "enabled": true, "order": 30, "description": "识别排名、对比、下钻、汇总等意图，规划后续工具链路。", "runtime": {"flows": ["advanced"], "promptEditable": true, "parameterEditable": false, "executor": "prompt", "roles": [1]}}, {"key": "golden_sql", "label": "Golden SQL Skill", "stage": "advanced.skill.golden_sql", "toolType": "sql", "enabled": true, "order": 40, "description": "优先检索人工确认过的 SQL 样例，作为生成或改写依据。", "runtime": {"flows": ["basic", "advanced"], "promptEditable": true, "parameterEditable": false, "executor": "prompt", "roles": [2]}}, {"key": "sql_generate", "label": "SQL 生成 Skill", "stage": "advanced.skill.sql_generate", "toolType": "sql", "enabled": true, "order": 50, "description": "基于数据资产与业务口径生成查询语句。", "runtime": {"flows": ["basic", "advanced"], "promptEditable": true, "parameterEditable": false, "executor": "prompt", "roles": [2]}}, {"key": "sql_review", "label": "SQL 复核 Skill", "stage": "advanced.skill.sql_review", "toolType": "sql", "enabled": true, "order": 60, "description": "检查只读安全、字段来源、统计口径和组织路径。", "runtime": {"flows": ["basic", "advanced"], "promptEditable": true, "parameterEditable": false, "executor": "prompt", "roles": [3]}}, {"key": "sql_execute", "label": "SQL 执行 Skill", "stage": "advanced.skill.sql_execute", "toolType": "sql", "enabled": true, "order": 70, "description": "复用现有数据源路由执行 SQL，不重复造连接层。", "runtime": {"flows": ["basic", "advanced"], "promptEditable": false, "parameterEditable": false, "executor": "deterministic", "roles": []}}, {"key": "sql_quality", "label": "SQL 质量门 Skill", "stage": "advanced.skill.sql_quality", "toolType": "sql", "enabled": true, "order": 75, "description": "检查 SQL 只读安全、字段映射、表映射、复核结论和首次结果质量。", "runtime": {"flows": ["advanced"], "promptEditable": false, "parameterEditable": false, "executor": "diagnostic", "roles": []}}, {"key": "template_policy", "label": "模板策略 Skill", "stage": "advanced.skill.template_policy", "toolType": "report", "enabled": true, "order": 78, "description": "检查排名/TopN 是否跟随报告模板和本轮 queryIntent，避免固定 Top3。", "runtime": {"flows": ["advanced"], "promptEditable": false, "parameterEditable": false, "executor": "diagnostic", "roles": []}}, {"key": "pandas_analyze", "label": "Pandas 加工 Skill", "stage": "advanced.skill.pandas_analyze", "toolType": "python", "enabled": true, "order": 80, "description": "对 SQL 结果做排名、差异、TopN、缺口和组织路径加工。", "runtime": {"flows": ["advanced"], "promptEditable": false, "parameterEditable": false, "executor": "diagnostic", "roles": []}}, {"key": "self_check", "label": "结果自检 Skill", "stage": "advanced.skill.self_check", "toolType": "fact", "enabled": true, "order": 90, "description": "检查空结果、数据集不匹配、风险阈值和报告完整性。", "runtime": {"flows": ["advanced"], "promptEditable": false, "parameterEditable": false, "executor": "diagnostic", "roles": []}}, {"key": "answer_contract", "label": "答案契约 Skill", "stage": "advanced.skill.answer_contract", "toolType": "report", "enabled": true, "order": 95, "description": "检查核心结论是否优先直接回答用户问题，并提示关键证据与风险。", "runtime": {"flows": ["advanced"], "promptEditable": false, "parameterEditable": false, "executor": "diagnostic", "roles": []}}, {"key": "conclusion_advice", "label": "结论建议 Skill", "stage": "advanced.skill.conclusion_advice", "toolType": "report", "enabled": true, "order": 97, "description": "基于结果证据生成核心结论重写建议，不改写现有报告。", "runtime": {"flows": ["advanced"], "promptEditable": false, "parameterEditable": false, "executor": "diagnostic", "roles": []}}, {"key": "evidence_vote", "label": "多信号择优 Skill", "stage": "advanced.skill.evidence_vote", "toolType": "fact", "enabled": true, "order": 98, "description": "汇总路由、SQL、Pandas、答案契约和自检信号，给出采信建议。", "runtime": {"flows": ["advanced"], "promptEditable": false, "parameterEditable": false, "executor": "diagnostic", "roles": []}}, {"key": "report_compose", "label": "报告组装 Skill", "stage": "advanced.skill.report_compose", "toolType": "report", "enabled": true, "order": 100, "description": "保持现有 report_spec/dataset_results 契约，组装最终报告。", "runtime": {"flows": ["basic", "advanced"], "promptEditable": true, "parameterEditable": false, "executor": "prompt", "roles": [4]}}], "mcp": {"enabled": false, "servers": [], "notes": "第一阶段只做配置和诊断占位，稳定后再接真实 MCP 工具调用。"}, "sqlServer": {"enabled": false, "reuseDataSources": true, "driver": "ODBC Driver 18 for SQL Server", "notes": "优先复用数据连接管理里的 SQL Server 数据源；驱动和镜像依赖在第二阶段校验。"}};let savedSkills=null;
let starts = 0, confirmations = 0, basicStarts = 0
let queueTestMode=false
let basicGates=[]
let queuedRequests=[]
let savedPolicy = null
let featureOverrides = {}
let flowConfig = { defaultFlow: "basic", advancedEnabled:true, advancedRoles:["super_admin"], datasetPolicies:{}, maxParallel:3, maxRetries:2, queryTimeoutSeconds:30, maxResultRows:10000, attachMetadata:true }
const plan = { id: 'research-ui-test', question: '9月收入为什么下降', branches: [{ id:'b1',title:'订单量变化',hypothesis:'检查订单数量变化',question:'9月订单量',dataset_id:1 },{ id:'b2',title:'产品结构变化',hypothesis:'检查产品结构变化',question:'9月产品结构',dataset_id:1 }], limits:{maxParallel:2} }
const catalog = [{id:'R14',title:'审阅研究计划',role:'主理人'},{id:'R15',title:'并行派发任务',role:'主理人'},{id:'R29',title:'提取分支证据',role:'领域专家'}]
const dataset = { dataset_id:1,dataset_name:'演示订单',columns:['战区','收入'],rows:[{'战区':'华东','收入':26},{'战区':'华南','收入':22}],row_count:2,sql:'SELECT region, revenue FROM demo',agent3_review:{approved:true},analysis:'两战区收入合计48万元。' }
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
  else if (path.includes('report-history')) data = {history:[0,1,3].map((days,i)=>({id:'hist-'+i,title:'旧截断标题',question:'截至2026年9月底各分公司管网里程和GIS入库率 '+i,datasetName:'江城燃气 · 安全与管网治理',updatedAt:new Date(Date.now()-days*86400000).toISOString(),reportSnapshot:{question:'截至2026年9月底各分公司管网里程和GIS入库率 '+i,result:{dataset_results:[dataset]}}})),success:true}
  else if(path==='/api/admin/advanced-capabilities'){if(route.request().method()==='PUT'){savedSkills=route.request().postDataJSON().config;skillsConfig=savedSkills}data={success:true,data:{config:skillsConfig}}}
  else if(path==='/api/agents')data={agents:[1,2,3,4].map(agent_no=>({agent_no,name:['','主理人 · 路由与研究规划','查询专家','核验专家','分析与报告专家'][agent_no],role_summary:'角色职责',system_prompt:'已配置的执行指令',knowledge_base:['业务规则']}))}

  else if (path === '/api/admin/ask-flow') {
    if (route.request().method() === 'PUT') { savedPolicy = route.request().postDataJSON().config; flowConfig = savedPolicy }
    data = { success:true,data:{config:flowConfig,effectiveDecision:{flow:'basic',reason:'basic_selected'}} }
  }
  else if (path === '/api/ask-chat/capabilities') data = {success:true,data:{defaultFlow:'basic',advancedAvailable:true,attachMetadata:true,authorizationScope:'fixture-scope',reportDownloadAvailable:true,scopeLabel:'当前账号授权组织 · 两条路径均强制校验'}}
  else if (path === '/api/ask-chat/stream') {
    const body = route.request().postDataJSON()
    if (body.ask_flow === 'basic') {
      basicStarts++
      if(queueTestMode){queuedRequests.push(body);await new Promise(resolve=>basicGates.push(resolve))}
      const result={question:'9月收入多少',requires_confirmation:false,dataset_results:[dataset],...dataset,analysis:'华东、华南收入合计48万元。',route:{dataset_ids:[1]},workflow:{run_id:'run-basic',flow:'basic',catalog:[{id:'L9',title:'受控执行'}],events:[{run_id:'run-basic',seq:2,node_id:'L9',status:'completed',title:'受控执行',summary:'已返回2行'}],status:'completed'}}
      if(dataset.query_status==='failed')result.workflow.events=[{run_id:'run-basic',seq:2,node_id:'L5',attempt:0,title:'生成查询',status:'failed'},{run_id:'run-basic',seq:3,node_id:'L5',attempt:1,title:'生成查询',status:'completed'},{run_id:'run-basic',seq:4,node_id:'L6',attempt:0,title:'审查查询',status:'running'},{run_id:'run-basic',seq:5,node_id:'L6',attempt:1,title:'审查查询',status:'failed'}]
      await route.fulfill({contentType:'text/event-stream',body:frame('workflow',{event:{type:'started',run_id:'run-basic',flow:'basic',seq:1}})+frame('result',result)+frame('done',{ok:true})});return
    }
    assert.equal(body.ask_flow,'advanced')
    starts++
    const result = {authorization_scope:'fixture-scope',question:plan.question,requires_confirmation:true,confirmation_type:'research_plan',research_plan:plan,session_id:plan.id,route:{dataset_ids:[1]},workflow:{run_id:'run-plan',flow:'advanced',catalog,events:[],status:'waiting'}}
    await route.fulfill({contentType:'text/event-stream',body:frame('workflow',{event:{type:'started',run_id:'run-plan',seq:1,flow:'advanced',catalog}})+frame('result',result)+frame('done',{ok:true})});return
  } else if (path === '/api/ask-chat/confirm-by-boss/stream') {
    const body = route.request().postDataJSON()
    assert.deepEqual(body.plan_branch_ids,['b1','b2'])
    assert.equal(body.ask_flow,'advanced')
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
  assert.equal(await page.locator('.doubao-sidebar').count(),0)
  await page.waitForTimeout(400)
  const profile=await page.locator('.workspace-nav .topnav-user-chip').boundingBox()
  assert(profile.y>800)
  await page.locator('.workspace-nav .topnav-user-chip').click()
  await page.locator('.topnav-user-dropdown').waitFor()
  const pop=await page.locator('.topnav-user-dropdown').boundingBox();assert(pop.y+pop.height<profile.y+5)
  await page.locator('.workspace-nav .topnav-user-chip').click()
  await page.getByRole('button',{name:'最近分析',exact:true}).click()
  const history=page.locator('.analysis-history-drawer')
  await history.waitFor()
  await page.waitForTimeout(400)
  assert.equal(await history.locator('.history-record').count(),3)
  assert((await history.innerText()).includes('GIS入库率'))
  await history.getByRole('textbox',{name:'搜索历史分析'}).fill('不存在的数据')
  await history.getByText('没有找到相关分析').waitFor()
  await history.getByRole('textbox',{name:'搜索历史分析'}).fill('')
  await page.screenshot({path:'/private/tmp/dp-new-history.png',fullPage:true,animations:'disabled'})
  await page.keyboard.press('Escape')
  await page.locator('.workspace-nav-link').filter({hasText:'专家协作'}).click()
  await page.getByRole('heading',{name:'专家协作',exact:true}).waitFor()
  assert(!(await page.locator('.agent-page').innerText()).includes('AGENT'))
  await page.screenshot({path:'/private/tmp/dp-new-roles.png',fullPage:true,animations:'disabled'})
  await page.getByRole('button',{name:'查看绑定技能 ↗'}).click()
  await page.getByRole('tab',{name:'技能配置'}).waitFor()
  await page.getByRole('button',{name:'SQL 生成 Skill',exact:true}).click()
  const editor=page.locator('.skill-editor-drawer')
  await editor.getByLabel('执行指令',{exact:true}).fill('必须核对组织与时间粒度，再生成查询')
  await editor.getByRole('button',{name:'保存配置',exact:true}).click()
  await editor.waitFor({state:'hidden'})
  assert(savedSkills.skills.find(s=>s.key==='sql_generate').prompt.includes('核对组织'))
  await page.reload()
  await page.getByRole('button',{name:'SQL 生成 Skill',exact:true}).click()
  await editor.waitFor()
  await page.waitForTimeout(400)
  assert((await editor.getByLabel('执行指令',{exact:true}).inputValue()).includes('核对组织'))
  await page.screenshot({path:'/private/tmp/dp-new-skills.png',fullPage:true,animations:'disabled'})
  await page.keyboard.press('Escape')
  await page.getByRole('button',{name:'字段关联与剪枝',exact:true}).click()
  await editor.getByRole('spinbutton').fill('32')
  await editor.getByRole('button',{name:'保存配置',exact:true}).click()
  await editor.waitFor({state:'hidden'})
  assert.equal(savedSkills.skills.find(s=>s.key==='schema_link').config.fieldLimit,32)
  for(const width of [390,320]){
    await page.setViewportSize({width,height:844})
    await page.getByRole('button',{name:'展开导航'}).click()
    await page.locator('.workspace-nav-link').filter({hasText:'问数助手'}).click()
    await page.getByRole('button',{name:'最近分析',exact:true}).click()
    await history.waitFor()
  await page.waitForTimeout(400)
    const box=await history.boundingBox();assert(box.width<=width+1)
    await page.screenshot({path:'/private/tmp/dp-new-history-'+width+'.png',fullPage:true,animations:'disabled'})
    await page.keyboard.press('Escape')
  }
  assert.deepEqual(errors,[])
  console.log('PASS: global navigation, bottom profile, history search, full titles, roles, skill save/reload, schema parameter, mobile 390/320')
}finally{await browser.close()}
