const assert=require('node:assert/strict');
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
(async()=>{const browser=await chromium.launch({channel:'chrome',headless:true});try{
 const page=await browser.newPage();await page.goto(require('node:url').pathToFileURL(require('node:path').resolve('mission.html')).href);
 for(const [wrong,attempts,coins] of [[0,10,700],[1,11,600],[6,15,550],[15,15,100]]){
  await page.evaluate(()=>localStorage.clear());await page.reload();await page.locator('[data-challenge="0"]').first().click();await page.locator('#start-questions').click();
  for(let i=0;i<attempts;i++){
   const answer=await page.evaluate(i=>window.ORBITA_MISSION.challenges[0].questions[i].answer,i);
   await page.locator(`input[value="${i<wrong?(answer+1)%4:answer}"]`).check();await page.locator('#check-answer').click();
   if(i===attempts-1&&wrong<6)break;
   await page.waitForFunction(()=>document.querySelector('#feedback').open);
   await page.locator('#continue-feedback').click();
  }
  await page.waitForFunction(()=>document.querySelector('#reward-status').textContent==='Recompensas guardadas!'&&!document.querySelector('#celebration-view').hidden);
  assert.equal(await page.locator('#earned-coins').textContent(),String(coins));
  const state=await page.evaluate(()=>JSON.parse(localStorage.getItem('orbita2-mission1-v2')));
  assert.equal(state.attempted.length,attempts);assert.equal(state.done.length,attempts-wrong);
  const before=await page.evaluate(()=>window.OrbitaWallet.snapshot().coins);
  await page.reload();await page.locator('[data-challenge="0"]').first().click();assert(await page.locator('#lesson-view').isVisible());await page.locator('#start-questions').click();await page.waitForFunction(()=>!document.querySelector('#next-challenge').disabled);
  assert.equal(await page.evaluate(()=>window.OrbitaWallet.snapshot().coins),before);
  await page.locator('#next-challenge').click();await page.locator('#start-questions').click();
  assert((await page.locator('#question-count').textContent()).includes(wrong<6?'DESAFIO 2':'DESAFIO 1'));
  console.log(`OK: ${attempts-wrong} acertos em ${attempts} questões, ${coins} moedas incluindo bônus diário, sem duplicação.`);
 }
 // A wrong answer stays wrong after closing the feedback and reloading.
 await page.evaluate(()=>localStorage.clear());await page.reload();await page.locator('[data-challenge="0"]').first().click();await page.locator('#start-questions').click();await page.locator('input[value="0"]').check();await page.locator('#check-answer').click();await page.waitForFunction(()=>document.querySelector('#feedback').open);await page.locator('#close-feedback').click();assert(await page.locator('#check-answer').isDisabled());await page.reload();await page.locator('[data-challenge="0"]').first().click();await page.locator('#start-questions').click();assert((await page.locator('#question-count').textContent()).includes('QUESTÃO 2'));
 console.log('OK: tentativa incorreta não pode ser refeita; retomada na próxima questão.');
}finally{await browser.close()}})().catch(e=>{console.error(e);process.exitCode=1});
