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

try{
 for(const width of [1440,1024,768,390,375]){
 await page.setViewportSize({width,height:1000});
 for(const tab of ['dashboard','permissions','ask-flow','fields','data','logs']){
 await page.goto(`${base}/admin-console?tab=${tab}`);await page.waitForLoadState('networkidle');await page.locator('.console-hero').waitFor({timeout:20000}).catch(async e=>{await page.screenshot({path:output+'/failure.png'});throw e});
 const layout=await page.evaluate(()=>{const r=s=>document.querySelector(s)?.getBoundingClientRect();return {overflow:document.documentElement.scrollWidth>innerWidth+1,heading:r('.console-hero')?.toJSON(),nav:r('.console-tabs')?.toJSON(),main:r('.console-command-layout')?.toJSON()}});
 assert.equal(layout.overflow,false,`overflow ${tab} ${width}`);
 assert.ok(layout.heading.bottom<=layout.main.top+2,`heading overlap ${tab} ${width}`);
 if(width>1100)assert.ok(layout.nav.right<=layout.main.left+2,`nav overlap ${tab} ${width}`);
 else assert.ok(layout.nav.bottom<=layout.main.top+2,`mobile nav overlap ${tab} ${width}`);
 if(width<=600 && ['permissions','fields'].includes(tab)){if(tab==='fields' && !await page.locator('.matrix-head:visible').count())await page.locator('.module-card-head').first().click();await page.locator('#console-mobile-role').selectOption('admin');assert.equal(await page.locator('.matrix-head:visible').first().locator('.role-head:visible').count(),1);await page.locator('#console-mobile-role').selectOption('user');}
 await page.screenshot({path:`${output}/${tab}-${width}.png`});
 }
 }
 assert.deepEqual(errors,[]);console.log('PASS: six console sections at five widths; no overflow, header/navigation overlap or runtime errors');
}catch(e){console.log(errors);throw e}finally{await browser.close()}
