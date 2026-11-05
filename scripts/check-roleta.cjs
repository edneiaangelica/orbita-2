const assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm');
const source=fs.readFileSync('wallet.js','utf8');
(async()=>{
 for(let index=0;index<6;index++){
  const data=new Map();data.set('orbita2-wallet-v1',JSON.stringify({coins:100,stars:10,purchases:[],rewards:{}}));
  const context={window:{dispatchEvent(){},addEventListener(){}},document:{querySelectorAll:()=>[]},localStorage:{getItem:k=>data.get(k)||null,setItem:(k,v)=>data.set(k,v)},navigator:{locks:{request:async(k,fn)=>fn()}},crypto:{getRandomValues:a=>{a[0]=index;return a}},Event:class{}};
  vm.runInNewContext(source,context);const w=context.window.OrbitaWallet;
  await w.roulette('open');const r=await w.roulette('spin');assert.equal(r.game.index,index);assert.equal(w.snapshot().stars,10+[-3,-1,2,3,4,5][index]);
  await w.roulette('close');await w.roulette('open');await w.roulette('spin');assert.equal(w.snapshot().stars,10+[-3,-1,2,3,4,5][index]);assert.equal(Object.keys(w.snapshot().rewards).length,1);
  data.set('orbita2-wallet-v1',JSON.stringify({coins:0,stars:0,purchases:[],rewards:{}}));await w.roulette('spin');assert(w.snapshot().stars>=0);
 }
 const {chromium}=require('C:/Users/USUARIO/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');const b=await chromium.launch({channel:'chrome',headless:true});const p=await b.newPage({viewport:{width:1366,height:768}});const errors=[];p.on('pageerror',e=>errors.push(e.message));
 const url=require('url').pathToFileURL(require('path').resolve('mission.html')).href;
 await p.goto(url+'?mission=2#sorte-reves');await p.locator('#roulette-dialog[open]').waitFor();
 for(const [width,height] of [[1366,768],[1280,720],[1024,600]]){await p.setViewportSize({width,height});assert(await p.locator('#roulette-dialog').evaluate(d=>d.scrollHeight<=d.clientHeight+1),`${width}x${height} scroll`);}
 await p.setViewportSize({width:1366,height:768});await p.screenshot({path:'output/roleta-planetas.png'});
 await p.locator('#roulette-read').click();await p.waitForFunction(()=>document.getElementById('roulette-read').textContent.includes('Parar'));
 await p.locator('#roulette-spin').click();assert(await p.locator('#roulette-spin').isDisabled());await p.waitForFunction(()=>document.getElementById('roulette-attempt').textContent==='Tentativa utilizada');
 const before=await p.evaluate(()=>window.OrbitaWallet.snapshot());const game=before.roulette['mission-2-roulette'];assert.equal(await p.locator('#planet-wheel').evaluate(e=>e.style.transform),`rotate(${330-game.index*60}deg)`);
 await p.reload();await p.locator('#roulette-dialog[open]').waitFor();assert(await p.locator('#roulette-spin').isDisabled());assert.equal((await p.evaluate(()=>window.OrbitaWallet.snapshot())).stars,before.stars);
 await p.setViewportSize({width:390,height:844});assert(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));await p.screenshot({path:'output/roleta-planetas-mobile.png'});
 await p.locator('#roulette-close').click();await p.locator('#roulette-dialog[open]').waitFor({state:'hidden'});assert.equal(await p.locator('#roulette-dialog[open]').count(),0);
 // Completing mission 2 offers the wheel without a manual hash link.
 await p.evaluate(()=>{const s=window.OrbitaWallet.snapshot();delete s.available;delete s.roulette;delete s.rewards['mission-2-roulette'];s.rewards['mission-2-complete']={id:'mission-2-complete',coins:250,stars:5};localStorage.setItem('orbita2-wallet-v1',JSON.stringify(s));});
 await p.goto(url+'?mission=2');await p.locator('#roulette-dialog[open]').waitFor();
 await p.goto(url+'?mission=1#sorte-reves');await p.locator('#luck-dialog[open]').waitFor();assert.equal(await p.locator('#roulette-dialog').count(),0);
 assert.deepEqual(errors,[]);await b.close();console.log('OK: seis resultados, ganhos/perdas, saldo mínimo, giro único persistente, seta, áudio, fim da missão 2, memória da missão 1 e telas PC/celular.');
})().catch(e=>{console.error(e);process.exit(1)});

