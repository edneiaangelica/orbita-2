const {chromium}=require('C:/Users/USUARIO/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
(async()=>{
 const browser=await chromium.launch({headless:true,channel:'chrome'});const page=await browser.newPage();const errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto(require('node:url').pathToFileURL(require('node:path').resolve('index.html')).href);
 await page.locator('#fullscreen').click();await page.waitForFunction(()=>!!document.fullscreenElement);
 await page.locator('.student').click();const frame=page.frameLocator('#orbita-app-frame');
 await frame.locator('.start').waitFor();console.log('narrativa fullscreen',await page.evaluate(()=>!!document.fullscreenElement));
 await frame.locator('.start').click();await frame.locator('.home-page').waitFor();console.log('home video',await frame.locator('video').count());
 for(const target of ['mission.html','avatar.html','diario.html']){
  await frame.locator('a[href="'+target+'"]').first().click();await frame.locator('#fullscreen').waitFor();
  console.log(target,await page.evaluate(()=>!!document.fullscreenElement),await frame.locator('#fullscreen').getAttribute('aria-pressed'));
 }
 await frame.locator('a[href*="diario-planeta.html"]').first().click();await frame.locator('#fullscreen').waitFor();
 console.log('planeta fullscreen',await page.evaluate(()=>!!document.fullscreenElement));
 await frame.locator('#fullscreen').click();await page.waitForFunction(()=>!document.fullscreenElement);
 await frame.locator('#fullscreen').click();await page.waitForFunction(()=>!!document.fullscreenElement);
 await frame.locator('#exit').click();await frame.locator('.student').waitFor();
 console.log('sair abertura fullscreen',await page.evaluate(()=>!!document.fullscreenElement));
 console.log({errors});await browser.close();
})().catch(e=>{console.error(e);process.exitCode=1});
