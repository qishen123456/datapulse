// Read-only local UI checks. Does not send a question to external models.
import {createRequire} from 'node:module'
import {execFileSync} from 'node:child_process'
import {mkdir,writeFile} from 'node:fs/promises'
import assert from 'node:assert/strict'
const require=createRequire(import.meta.url)
const {chromium}=require(process.env.PLAYWRIGHT_MODULE || 'playwright')
const login=`import requests,json
from controllers.auth import _admin_config
c=_admin_config();r=requests.post('http://127.0.0.1:5002/api/auth/login',json={'username':c['username'],'password':c['password']},timeout=10);r.raise_for_status();print(json.dumps({'token':r.json()['token']}))`
const {token}=JSON.parse(execFileSync('docker',['exec','-e','PYTHONPATH=/app/backend','askdesk-backend','python','-c',login],{encoding:'utf8'}))
const browser=await chromium.launch({headless:true,executablePath:process.env.PLAYWRIGHT_CHROMIUM})
const page=await browser.newPage({viewport:{width:1440,height:1000},reducedMotion:'reduce'})
await page.addInitScript(t=>localStorage.setItem('auth_token',t),token)
const errors=[];page.on('pageerror',e=>errors.push(e.message))
const output=process.env.THEME_SCREENSHOTS || '/private/tmp/workspace-theme'
await mkdir(output,{recursive:true})
const results=[]
try{
  for(const path of ['/ask','/sql-debug','/datasets','/agents','/report-config','/organization-trees','/admin-console']){
    await page.goto('http://127.0.0.1:8888'+path)
    await page.locator('.studio-brandmark').waitFor()
    await page.waitForLoadState('networkidle')
    await page.waitForFunction(()=>!document.querySelector('.el-loading-mask'))
    if(path!=='/admin-console')await page.waitForFunction(()=>getComputedStyle(document.querySelector('.topnav-menu .is-active > .el-sub-menu__title, .topnav-menu .el-menu-item.is-active')).color==='rgb(29, 78, 216)')
    const theme=await page.evaluate(()=>({
      brand:document.querySelector('.topnav-brand').innerText,
      accent:getComputedStyle(document.querySelector('.studio-brandmark')).backgroundColor,
      nav:(()=>{const active=document.querySelector('.topnav-menu .is-active > .el-sub-menu__title, .topnav-menu .el-menu-item.is-active');return active?getComputedStyle(active).color:null})(),
      width:document.documentElement.scrollWidth,viewport:innerWidth,
    }))
    console.log(path,theme.accent,theme.nav)
    assert.match(theme.brand,/脉策智能/)
    assert.equal(theme.accent,'rgb(29, 78, 216)')
    if(path!=='/admin-console')assert.equal(theme.nav,'rgb(29, 78, 216)')
    assert.ok(theme.width<=theme.viewport+1,path+' page overflow')
    await page.screenshot({path:output+'/'+path.slice(1)+'.png',fullPage:true,animations:'disabled'})
    results.push({path,...theme})
  }
  await page.setViewportSize({width:390,height:900})
  await page.goto('http://127.0.0.1:8888/ask')
  await page.locator('.cmp-textarea').waitFor()
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1))
  await page.screenshot({path:output+'/ask-mobile.png',fullPage:true})
  assert.deepEqual(errors,[])
  await writeFile(output+'/checks.json',JSON.stringify({status:'passed',results,errors},null,2))
  console.log('PASS: shared brand/navigation, seven routes, mobile ask, no page errors')
}finally{
  await page.request.post('http://127.0.0.1:8888/api/auth/logout',{headers:{'X-Auth-Token':token}})
  await browser.close()
}
