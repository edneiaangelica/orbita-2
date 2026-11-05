const {chromium}=require('C:/Users/USUARIO/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
(async()=>{
 const browser=await chromium.launch({headless:true,channel:'chrome'});
 const page=await browser.newPage();const errors=[];page.on('pageerror',e=>errors.push(e.message));
 const url=require('node:url').pathToFileURL(require('node:path').resolve('narrativa.html')).href;
 for(const [width,height] of [[1366,768],[390,844],[320,568],[667,375]]){
  await page.setViewportSize({width,height});await page.goto(url);await page.evaluate(()=>document.fonts.ready);
  await page.waitForFunction(()=>document.querySelector('video').readyState>=1);
  console.log(JSON.stringify({width,height,...await page.evaluate(()=>({w:document.documentElement.scrollWidth,h:document.documentElement.scrollHeight,duration:document.querySelector('video').duration}))}));
 }
 await page.locator('video').evaluate(v=>v.play());await page.waitForFunction(()=>document.querySelector('video').currentTime>0);
 await page.locator('.start').click();console.log('Leva ao início:',page.url().endsWith('inicio.html'));
 await page.goto(require('node:url').pathToFileURL(require('node:path').resolve('index.html')).href);
 console.log('Entradas para narrativa:',await page.locator('a[href="narrativa.html"]').count());
 console.log({errors});await browser.close();
})().catch(e=>{console.error(e);process.exitCode=1});
