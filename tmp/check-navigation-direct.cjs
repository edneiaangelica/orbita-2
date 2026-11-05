const {chromium}=require('C:/Users/USUARIO/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
(async()=>{const browser=await chromium.launch({headless:true,channel:'chrome'});const page=await browser.newPage();const errors=[];page.on('pageerror',e=>errors.push(e.message));const url=f=>require('node:url').pathToFileURL(require('node:path').resolve(f)).href;
for(const f of ['index.html','narrativa.html','inicio.html','mission.html','avatar.html','diario.html','diario-planeta.html']){
await page.goto(url(f)); console.log(f,'fullscreen controls:',await page.locator('#fullscreen').count());
if(await page.locator('#exit').count()){await page.locator('#exit').click();await page.waitForURL('**/index.html');}
}
for(const width of [1366,390]){await page.setViewportSize({width,height:width===390?844:768});await page.goto(url('inicio.html'));await page.screenshot({path:'output/inicio-sem-video-'+width+'.png'});}
console.log({errors});await browser.close();})().catch(e=>{console.error(e);process.exitCode=1});
