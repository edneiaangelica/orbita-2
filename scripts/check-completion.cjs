const assert=require('node:assert/strict');
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const url=process.env.TEST_URL||'http://127.0.0.1:4173/mission.html';
(async()=>{
 const browser=await chromium.launch({channel:'chrome',headless:true});
 const page=await browser.newPage({viewport:{width:1280,height:1000}});
 const errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto(url);
 async function seed(errorCount=0,challenge=0){
  await page.evaluate(({errorCount,challenge})=>{
   localStorage.removeItem('orbita2-wallet-v1');
   const done=[];
   for(let c=0;c<=challenge;c++)for(let q=1;q<=(c===challenge?9:10);q++)done.push(`d${c+1}-q${q}`);
   localStorage.setItem('orbita2-mission1-v1',JSON.stringify({done,challenge,question:9,errors:{[challenge]:errorCount}}));
  },{errorCount,challenge});
  await page.reload();
  await page.locator(`[data-challenge="${challenge}"]`).first().click();
  await page.locator('#start-questions').click();
  await page.locator('[data-question="9"]').evaluate(e=>e.click());
 }
 async function answer(correct=true){
  const index=await page.evaluate(()=>window.ORBITA_MISSION.challenges[JSON.parse(localStorage.getItem('orbita2-mission1-v1')).challenge].questions[9].answer);
  await page.locator(`input[value="${correct?index:(index+1)%4}"]`).check();
  await page.locator('#check-answer').click();
 }
 for(const [mistakes,expected] of [[0,700],[1,600],[2,550],[3,450]]){
  await seed(mistakes);await answer();
  await page.waitForFunction(()=>document.querySelector('#reward-status').textContent==='Recompensas guardadas!');
  assert.equal(await page.locator('#earned-coins').textContent(),String(expected));
  assert.equal(await page.locator('#earned-stars').textContent(),'2');
  assert.equal(await page.locator('#feedback').evaluate(e=>e.open),false);
  assert.equal(await page.locator('#celebration-view').isVisible(),true);
  const before=await page.evaluate(()=>window.OrbitaWallet.snapshot().coins);
  await page.reload();await page.locator('[data-challenge="0"]').first().click();
  await page.waitForFunction(()=>!document.querySelector('#next-challenge').disabled);
  assert.equal(await page.evaluate(()=>window.OrbitaWallet.snapshot().coins),before);
 }
 await seed();await answer(false);
 await page.locator('#continue-feedback').click();
 assert.equal(await page.evaluate(()=>JSON.parse(localStorage.getItem('orbita2-mission1-v1')).errors[0]),1);
 await page.reload();await page.locator('[data-challenge="0"]').first().click();await page.locator('#start-questions').click();await page.locator('[data-question="9"]').evaluate(e=>e.click());await answer();
 await page.waitForFunction(()=>!document.querySelector('#next-challenge').disabled);
 assert.equal(await page.locator('#earned-coins').textContent(),'600');
 await page.screenshot({path:'output/desafio-concluido-desktop.png',fullPage:true});
 await page.setViewportSize({width:390,height:844});
 assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
 await page.screenshot({path:'output/desafio-concluido-mobile.png',fullPage:true});
 await page.locator('#next-challenge').click();assert.equal(await page.locator('#lesson-view').isVisible(),true);
 assert((await page.locator('#lesson-title').textContent()).includes('Desafio 2'));
 // Daily reward is shared across challenges; mission bonus is paid once.
 const secondDaily=await page.evaluate(async()=>{const w=window.OrbitaWallet;const before=w.snapshot();await w.grant([window.OrbitaRewards.daily(1,2)]);return w.snapshot().coins-before.coins;});
 assert.equal(secondDaily,0);
 await seed(0,2);await answer();await page.waitForFunction(()=>!document.querySelector('#next-challenge').disabled);
 assert.equal(await page.locator('#earned-coins').textContent(),'950');assert.equal(await page.locator('#earned-stars').textContent(),'7');
 assert.equal(await page.locator('#next-challenge').textContent(),'Voltar às trilhas');
 // An unanswered challenge cannot be skipped and nine distinct acertos cannot complete it.
 await seed();await page.locator('#back-trail').click();assert.equal(await page.locator('[data-challenge="1"]').first().isDisabled(),true);
 await page.locator('[data-challenge="0"]').first().click();await page.locator('#start-questions').click();await page.locator('[data-question="0"]').evaluate(e=>e.click());
 await page.locator('input[value="1"]').check();await page.locator('#check-answer').click();await page.locator('#continue-feedback').click();
 assert.equal(await page.locator('#celebration-view').isHidden(),true);
 assert.equal(await page.evaluate(()=>JSON.parse(localStorage.getItem('orbita2-mission1-v1')).done.length),9);
 assert.deepEqual(errors,[]);
 await browser.close();console.log('OK: faixas de moedas, 10 acertos distintos, erros persistidos, bônus diário, missão, desbloqueio, recarga sem duplicação e telas desktop/mobile.');
})().catch(e=>{console.error(e);process.exit(1)});
