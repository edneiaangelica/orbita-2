const assert=require('node:assert/strict');
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
(async()=>{const browser=await chromium.launch({channel:'chrome',headless:true});try{
 const page=await browser.newPage();await page.goto(require('node:url').pathToFileURL(require('node:path').resolve('mission.html')).href);
 async function open(){await page.reload();await page.locator('[data-challenge="0"]').first().click();await page.locator('#start-questions').click();}
 async function answer(index){await page.locator(`input[value="${index}"]`).check();await page.locator('#check-answer').click();await page.waitForFunction(()=>document.querySelector('#feedback').open||!document.querySelector('#celebration-view').hidden);}
 await page.evaluate(()=>localStorage.clear());await open();
 await answer(0);assert.equal(await page.locator('#continue-feedback').textContent(),'Tentar mais uma vez');
 await page.locator('#continue-feedback').click();assert((await page.locator('#question-count').textContent()).includes('QUESTÃO 1 DE'));
 await open();assert((await page.locator('#question-count').textContent()).includes('QUESTÃO 1 DE'));
 await answer(0);await page.locator('#continue-feedback').click();assert((await page.locator('#question-count').textContent()).includes('QUESTÃO 2 DE'));
 await page.locator('[data-question="0"]').evaluate(e=>e.click());assert(await page.locator('#check-answer').isDisabled());
 await page.locator('[data-question="1"]').evaluate(e=>e.click());await answer(0);await page.locator('#continue-feedback').click();await answer(3);await page.locator('#continue-feedback').click();
 let state=await page.evaluate(()=>JSON.parse(localStorage.getItem('orbita2-mission1-v2')));
 assert.equal(state.attempts['d1-q1'],2);assert.equal(state.attempts['d1-q2'],2);assert.deepEqual(state.done,['d1-q2']);assert.equal(state.errors[0],3);
 // The tenth correct answer on the second try immediately wins.
 await page.evaluate(()=>{localStorage.clear();const done=Array.from({length:9},(_,i)=>`d1-q${i+1}`);localStorage.setItem('orbita2-mission1-v2',JSON.stringify({done,attempted:done,attempts:{},challenge:0,question:9,errors:{}}));});await open();await answer(0);await page.locator('#continue-feedback').click();await answer(1);await page.waitForFunction(()=>document.querySelector('#reward-status').textContent==='Recompensas guardadas!');assert.equal(await page.locator('#earned-coins').textContent(),'600');assert(await page.locator('#celebration-view').isVisible());
 console.log('OK: segunda chance, persistência após recarga, limite de duas tentativas, acerto na segunda e vitória no décimo acerto.');
}finally{await browser.close()}})().catch(e=>{console.error(e);process.exitCode=1});
