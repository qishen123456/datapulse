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
 for(const width of [1440,390]){
 await page.setViewportSize({width,height:1000});
 for(const route of ['databases','datasets','ai-models','feishu-sync']){
 await page.goto(`${base}/${route}`);await page.waitForLoadState('networkidle');
 assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1),false,route);
 await page.screenshot({path:`${output}/${route}-${width}.png`});
 }
 }
 assert.deepEqual(errors,[]);console.log('PASS: asset interiors at desktop/mobile; no overflow or runtime errors');
}finally{await browser.close()}
