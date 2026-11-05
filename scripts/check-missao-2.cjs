const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict'),path=require('node:path');
const {pathToFileURL}=require('node:url');
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'C:/Users/USUARIO/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const context={window:{}};vm.runInNewContext(fs.readFileSync('mission-2-data.js','utf8'),context);const m=context.window.ORBITA_MISSION_2;
assert.equal(m.id,2);assert.equal(m.challenges.length,3);
const expected=[[12,13,14,17,12,17,20,11,18,0,17,18,14,12,2],[7,8,10,8,10,8,7,7,6,2,12,9,15,6,1],[13,9,16,8,14,5,12,9,8,10,13,5,6,11,3]];
for(const [ci,c] of m.challenges.entries()){
 assert.equal(c.questions.length,15);assert(fs.existsSync(c.video));
 assert.equal(new Set(c.questions.map(q=>q.success)).size,15);assert.equal(new Set(c.questions.map(q=>q.error)).size,15);
 c.questions.forEach((q,i)=>{assert.equal(q.answer,expected[ci][i],q.id);assert(q.prompt&&q.success&&q.error);if(q.type==='qt3'){assert.equal(q.options.length,4);assert(q.options[q.answer]);}else assert.equal(q.type,'input');});
}
assert(m.challenges[2].questions[2].success.includes('16 cadernos'));
(async()=>{
 const b=await chromium.launch({channel:'chrome',headless:true});const p=await b.newPage({viewport:{width:1366,height:900}});const errors=[];p.on('pageerror',e=>errors.push(e.message));
 const url=pathToFileURL(path.resolve('mission.html')).href;
 await p.goto(url);assert.equal(await p.locator('.trail-mission').count(),2);
 await p.evaluate(()=>localStorage.setItem('orbita2-mission1-v2',JSON.stringify({done:['d1-q1'],attempted:['d1-q1'],challenge:0,question:0,errors:{},rounds:{}})));
 await p.locator('[data-mission="2"][data-challenge="0"]').click();await p.waitForURL(/mission=2/);
 assert.equal(await p.evaluate(()=>window.ORBITA_MISSION.id),2);
 assert.equal(await p.locator('#lesson').getAttribute('src'),m.challenges[0].video);
 await p.locator('#start-questions').click();await p.locator('#typed-answer').fill('11');await p.locator('#check-answer').click();
 await p.locator('#feedback[open]').waitFor();assert((await p.locator('#feedback-text').textContent()).includes('Guarde o 7'));
 await p.locator('#continue-feedback').click();assert((await p.locator('#question-count').textContent()).includes('QUESTÃO 1 DE 15'));
 await p.locator('#typed-answer').fill('12');await p.locator('#check-answer').click();await p.locator('#feedback[open]').waitFor();assert((await p.locator('#feedback-text').textContent()).includes('igual a 12'));
 await p.locator('#continue-feedback').click();await p.locator('#read-question').click();assert((await p.locator('#narration').getAttribute('src')).includes('missao-2/d1-q2-prompt.mp3'));
 for(let ci=0;ci<3;ci++){
  await p.goto(url+`?mission=2&challenge=${ci+1}`);assert.equal(await p.locator('#lesson').getAttribute('src'),m.challenges[ci].video);
  await p.locator('#start-questions').click();
  for(let qi=0;qi<15;qi++){
   await p.locator(`[data-question="${qi}"]`).evaluate(el=>el.click());
   assert.equal(await p.locator('#question-title').textContent(),m.challenges[ci].questions[qi].prompt);
   assert.equal(await p.locator('#typed-answer').count(),m.challenges[ci].questions[qi].type==='input'?1:0);
  }
  const q=m.challenges[ci].questions[14];await p.locator(`input[name="answer"][value="${q.answer}"]`).check();await p.locator('#check-answer').click();await p.locator('#feedback[open]').waitFor();assert.equal(await p.locator('#feedback-text').textContent(),q.success);await p.locator('#close-feedback').click();
 }
 const original=await p.evaluate(()=>JSON.parse(localStorage.getItem('orbita2-mission1-v2')));assert.deepEqual(original.done,['d1-q1']);
 const progress=await p.evaluate(()=>JSON.parse(localStorage.getItem('orbita2-mission2-v2')));assert(progress.done.includes('d1-q1'));assert(progress.done.includes('d3-q15'));
 await p.reload();assert((await p.evaluate(()=>JSON.parse(localStorage.getItem('orbita2-mission2-v2')).done)).includes('d3-q15'));
 await p.goto(url+'?mission=2');await p.screenshot({path:'output/missao-2-trilha.png'});
 await p.setViewportSize({width:390,height:844});await p.locator('[data-mission="2"][data-challenge="2"]').click();await p.locator('#start-questions').click();await p.locator('[data-question="14"]').evaluate(el=>el.click());
 assert(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));await p.screenshot({path:'output/missao-2-mobile.png',fullPage:true});
 assert.deepEqual(errors,[]);await b.close();console.log('OK: 45 gabaritos e telas, 3 vídeos, feedbacks de erro/acerto, quiz, áudio isolado, progresso separado/persistente e layout móvel.');
})().catch(e=>{console.error(e);process.exit(1)});
