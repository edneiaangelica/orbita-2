const {chromium}=require('C:/Users/USUARIO/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
(async()=>{
 const browser=await chromium.launch({headless:true,channel:'chrome'});
 const page=await browser.newPage({reducedMotion:'reduce'});const errors=[];page.on('pageerror',e=>errors.push(e.message));
 for(const [width,height] of [[1366,768],[1280,720],[390,844],[360,640],[320,568],[667,375],[844,390]]){
  await page.setViewportSize({width,height});await page.goto(require('node:url').pathToFileURL(require('node:path').resolve('index.html')).href);await page.evaluate(()=>document.fonts.ready);
  console.log(JSON.stringify({width,height,...await page.evaluate(()=>({scrollWidth:document.documentElement.scrollWidth,scrollHeight:document.documentElement.scrollHeight,brokenImages:[...document.images].filter(i=>!i.complete||!i.naturalWidth).map(i=>i.src)}))}));
  if(width===390||width===1366) await page.screenshot({path:'output/abertura-'+width+'.png'});
 }
 await page.locator('#sound').click();if(await page.locator('#sound').getAttribute('aria-pressed')!=='true')throw Error('Som não ativou');
 await page.locator('#sound').click();if(await page.locator('#sound').getAttribute('aria-pressed')!=='false')throw Error('Som não desativou');
 await page.locator('#fullscreen').click();console.log('fullscreen:',await page.evaluate(()=>!!document.fullscreenElement));
 await page.locator('.teacher').dispatchEvent('click');console.log('teacher unchanged:',page.url().endsWith('index.html'));
 console.log({errors});await browser.close();
})().catch(e=>{console.error(e);process.exitCode=1});
