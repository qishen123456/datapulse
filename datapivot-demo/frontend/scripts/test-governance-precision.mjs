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

try {
 await page.goto(`${base}/agents`); await page.locator('.prompt-input textarea').waitFor();
 const original = await page.locator('.prompt-input textarea').inputValue();
 await page.getByRole('button',{name:'全屏编辑',exact:true}).click();
 await page.locator('.editor-expanded').waitFor();
 await page.getByRole('button',{name:'插入结构',exact:true}).click();
 assert.ok((await page.locator('.prompt-input textarea').inputValue()).startsWith(original));
 await page.locator('.prompt-input textarea').press('Escape');
 assert.equal(await page.locator('.editor-expanded').count(),0);
 await page.goto(`${base}/organization-trees`); await page.locator('.tree-node-button').first().waitFor({timeout:1000}).catch(()=>{});
 await page.locator('.tree-node-row button').first().click(); await page.locator('.copy-code').waitFor();
 assert.ok(await page.locator('.copy-code').innerText());
 await page.goto(`${base}/employee-permissions`); await page.getByRole('button',{name:/更多账号操作/}).first().click();
 await page.getByRole('menuitem',{name:'删除账号…'}).waitFor(); await page.keyboard.press('Escape');
 await page.goto(`${base}/runtime-migration`); await page.locator('.upload-zone').waitFor();
 await page.locator('.upload-zone').evaluate(el=>{const dt=new DataTransfer();dt.items.add(new File(['{}'],'ui-preview.json',{type:'application/json'}));el.dispatchEvent(new DragEvent('drop',{bubbles:true,dataTransfer:dt}));});
 await page.getByText('ui-preview.json',{exact:true}).waitFor();
 await page.goto(`${base}/report-config`); await page.locator('.rc-ds-item').first().click();
 await page.locator('.rc-main-header').waitFor(); await page.waitForLoadState('networkidle');
 await page.screenshot({path:`${output}/report-config-selected.png`});
 const shelf=await page.locator('.rc-sidebar').boundingBox(); const editor=await page.locator('.rc-main').boundingBox();
 assert.ok(shelf.y+shelf.height<=editor.y+2,'dataset shelf is above report editor');
 for(const width of [1440,390]) {
  await page.setViewportSize({width,height:1000});
  for(const route of ['agents','organization-trees','employee-permissions','runtime-migration','report-config','admin-console?tab=permissions']){
   await page.goto(`${base}/${route}`);await page.waitForLoadState('networkidle');
   assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1),false,`overflow ${route} ${width}`);
   await page.screenshot({path:`${output}/${route.split('?')[0]}-${width}.png`});
  }
 }
 assert.deepEqual(errors,[]); console.log('PASS: instruction editor, organization inspector, account menu, JSON drop, report shelf, six governance pages desktop/mobile. No configuration saved.');
} finally {await browser.close()}
