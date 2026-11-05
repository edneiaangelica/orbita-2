const assert=require('node:assert/strict');
const {chromium}=require('C:/Users/USUARIO/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
(async()=>{
 const b=await chromium.launch({channel:'chrome',headless:true});const p=await b.newPage();
 const url=require('url').pathToFileURL(require('path').resolve('mission.html')).href;
 await p.goto(url+'?mission=2&challenge=1');await p.locator('#start-questions').click();
 await p.locator('#typed-answer').fill('11');await p.keyboard.press('Enter');await p.locator('#feedback[open]').waitFor();
 await p.keyboard.down('Enter');await p.locator('#feedback[open]').waitFor({state:'hidden'});
 assert((await p.locator('#question-count').textContent()).includes('QUESTÃO 1 DE 15'));
 await p.keyboard.down('Enter');assert.equal(await p.locator('#feedback[open]').count(),0);await p.keyboard.up('Enter');
 await p.locator('#typed-answer').fill('12');await p.keyboard.press('Enter');await p.locator('#feedback[open]').waitFor();
 assert((await p.locator('#feedback-text').textContent()).includes('igual a 12'));
 await p.keyboard.press('Enter');await p.locator('#feedback[open]').waitFor({state:'hidden'});assert((await p.locator('#question-count').textContent()).includes('QUESTÃO 2 DE 15'));
 await p.locator('[data-question="9"]').evaluate(e=>e.click());await p.locator('input[name="answer"][value="0"]').check();await p.keyboard.press('Enter');await p.locator('#feedback[open]').waitFor();assert((await p.locator('#feedback-text').textContent()).includes('ACERTOU'));
 await p.keyboard.press('Enter');await p.locator('#feedback[open]').waitFor({state:'hidden'});assert((await p.locator('#question-count').textContent()).includes('QUESTÃO 11 DE 15'));
 await b.close();console.log('OK: Enter confere resposta digitada e quiz, continua feedback, respeita nova tentativa e ignora tecla mantida pressionada.');
})().catch(e=>{console.error(e);process.exit(1)});
