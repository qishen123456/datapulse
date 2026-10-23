// Read-only visual audit against local services. Login credentials remain in the container.
import { createRequire } from 'node:module'
import { execFileSync } from 'node:child_process'
import { mkdir, writeFile } from 'node:fs/promises'
import assert from 'node:assert/strict'
const require=createRequire(import.meta.url)
const {chromium}=require(process.env.PLAYWRIGHT_MODULE || 'playwright')
const loginCode=`import requests,json
from controllers.auth import _admin_config
c=_admin_config();r=requests.post('http://127.0.0.1:5002/api/auth/login',json={'username':c['username'],'password':c['password']},timeout=10);r.raise_for_status();print(json.dumps({'token':r.json()['token']}))`
const {token}=JSON.parse(execFileSync('docker',['exec','-e','PYTHONPATH=/app/backend','askdesk-backend','python','-c',loginCode],{encoding:'utf8'}))
const browser=await chromium.launch({headless:true,executablePath:process.env.PLAYWRIGHT_CHROMIUM || undefined})
const page=await browser.newPage({viewport:{width:1440,height:1000},reducedMotion:'reduce'})
await page.addInitScript(value=>{if(window===window.top){localStorage.setItem('auth_token',value);localStorage.removeItem('datapulse_nav_collapsed')}},token)
const output=process.env.STUDIO_SCREENSHOTS || '/private/tmp/datapulse-ui-refresh'
await mkdir(output,{recursive:true})
const errors=[];page.on('pageerror',e=>errors.push(e.message))
const base=process.env.STUDIO_URL || 'http://127.0.0.1:5174'
const pages=[['ask','.cmp-textarea'],['datasets','.dataset-page'],['databases','.db-page'],['feishu-sync','.fs-page'],['agents','.agent-page'],['advanced-capabilities','.advanced-page'],['ai-models','.cs-page'],['report-config','.rc-page'],['organization-trees','.org-page'],['employee-permissions','.permission-page'],['admin-console','.console-page'],['runtime-migration','.migration-page'],['sql-debug','.studio-page']]
const checks=[]
try{
 for(const [route,selector] of pages){
  await page.goto(`${base}/${route}`)
  await page.locator(selector).waitFor({timeout:20000})
  await page.waitForLoadState('networkidle')
  await page.waitForFunction(()=>![...document.querySelectorAll('.el-loading-mask')].some(e=>e.getBoundingClientRect().height>0),{},{timeout:20000})
  await page.screenshot({path:`${output}/${route}.png`,fullPage:false,animations:'disabled'})
  const overflow=await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1)
  checks.push({route,overflow})
 }
 // Exercise the reorganized editors without saving, testing connections or triggering jobs.
 await page.goto(`${base}/ai-models`)
 await page.locator('.cs-ch-item').first().waitFor()
 await page.waitForLoadState('networkidle')
 await page.locator('.cs-ch-item').last().press('Enter')
 assert.equal(await page.locator('.cs-ch-item').last().getAttribute('aria-pressed'),'true')
 await page.getByRole('button',{name:'连接设置',exact:true}).click()
 await page.locator('.cs-config-grid').waitFor({state:'visible'})
 assert.equal(await page.locator('.cs-key-input input').getAttribute('type'),'password')
 await page.getByRole('button',{name:/^模型清单/}).click()
 await page.locator('.cs-model-panel').waitFor({state:'visible'})
 await page.getByRole('button',{name:/配置模型/}).first().click()
 await page.getByRole('dialog',{name:'编辑模型'}).waitFor()
 await page.getByRole('dialog',{name:'编辑模型'}).getByRole('button',{name:'取消',exact:true}).click()
 await page.goto(`${base}/agents`)
 await page.locator('.agent-card').last().click()
 await page.locator('.editor-section-tabs').getByRole('button',{name:/业务知识/}).click()
 await page.locator('.knowledge-section').waitFor()
 await page.locator('.editor-section-tabs').getByRole('button',{name:'角色资料'}).click()
 await page.locator('.profile-section').waitFor()
 await page.goto(`${base}/advanced-capabilities?tab=skills`)
 await page.locator('.skill-library-row').first().waitFor()
 await page.getByRole('textbox',{name:'搜索技能',exact:true}).fill('指标口径')
 await page.waitForFunction(()=>document.querySelectorAll('.skill-library-row').length===1)
 await page.locator('.skill-library-row').getByRole('button',{name:'配置',exact:true}).click()
 await page.getByRole('dialog').waitFor()
 await page.screenshot({path:`${output}/skill-editor.png`,animations:'disabled'})
 await page.keyboard.press('Escape')
 await page.goto(`${base}/datasets`)
 await page.locator('.dataset-tile').first().waitFor()
 await page.locator('.knowledge-category-nav').getByRole('button',{name:/数据模型/}).click()
 assert.equal(await page.locator('.knowledge-category-nav').getByRole('button',{name:/数据模型/}).getAttribute('aria-pressed'),'true')
 await page.locator('.dataset-properties summary').click()
 assert.equal(await page.locator('.dataset-properties').getAttribute('open'),'')
 await page.goto(`${base}/feishu-sync`)
 await page.getByRole('tab',{name:'任务配置',exact:true}).click()
 await page.locator('.fs-task-card').first().waitFor()
 await page.getByRole('tab',{name:'运行日志',exact:true}).click()
 await page.locator('.fs-log-panel').waitFor({state:'visible'})
 await page.goto(`${base}/ask`)
 await page.locator('.cmp-textarea').waitFor()
 await page.getByRole('button',{name:'账号菜单',exact:true}).click()
 const menu=page.getByRole('menu',{name:'账号设置'})
 await menu.waitFor()
 const menuBox=await menu.boundingBox(),triggerBox=await page.getByRole('button',{name:'账号菜单',exact:true}).boundingBox()
 assert.ok(menuBox.y+menuBox.height<=triggerBox.y,'account popover opens above the trigger')
 await page.screenshot({path:`${output}/account-menu.png`,animations:'disabled'})
 await page.getByRole('button',{name:'账号菜单',exact:true}).press('ArrowDown')
 assert.equal(await page.evaluate(()=>document.activeElement?.getAttribute('role')),'menuitem')
 await page.keyboard.press('Escape')
 await menu.waitFor({state:'detached'})
 await page.getByRole('button',{name:'收起侧栏',exact:true}).click()
 assert.ok(await page.locator('.workspace-nav').evaluate(e=>e.getBoundingClientRect().width<80))
 await page.getByRole('button',{name:'展开侧栏',exact:true}).click()
 for(const width of [1024,390]){
  await page.setViewportSize({width,height:900})
  for(const [route,selector] of pages.filter(([r])=>['datasets','agents','ai-models','databases','feishu-sync'].includes(r))){
   await page.goto(`${base}/${route}`)
   await page.locator(selector).waitFor({timeout:20000})
  await page.waitForLoadState('networkidle')
   await page.screenshot({path:`${output}/${route}-${width}.png`,animations:'disabled'})
   checks.push({route,width,overflow:await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1)})
  }
 }
 await writeFile(`${output}/checks.json`,JSON.stringify({checks,errors},null,2))
 assert.deepEqual(errors,[])
 assert.ok(checks.every(c=>!c.overflow),'layout extends beyond viewport; see checks.json')
 console.log('PASS: 13 module renders; model, expert, skill, dataset and sync editor interactions; account keyboard, sidebar collapse and responsive boundaries')
}finally{await browser.close()}
