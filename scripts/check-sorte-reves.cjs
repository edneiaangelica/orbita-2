const assert=require('node:assert/strict');const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
(async()=>{const b=await chromium.launch({channel:'chrome',headless:true});try{const p=await b.newPage();await p.goto(require('node:url').pathToFileURL(require('node:path').resolve('mission.html')).href);await p.evaluate(()=>{localStorage.clear();localStorage.setItem('orbita2-wallet-v1',JSON.stringify({coins:0,stars:20,purchases:[],rewards:{}}));});await p.reload();
for(const errors of [0,1,2,3]){
 await p.getByRole('link',{name:'Sorte ou revés',exact:true}).click();await p.locator('#luck-start').waitFor();
 for(const size of [{width:1280,height:720},{width:390,height:844},{width:360,height:640}]){await p.setViewportSize(size);assert(await p.locator('#luck-dialog').evaluate(e=>e.scrollHeight<=e.clientHeight+1),'offer scroll '+JSON.stringify(size));}
 await p.screenshot({path:'output/sorte-reves-novo-convite.png'});await p.locator('#luck-start').click();
 const before=await p.evaluate(()=>window.OrbitaWallet.snapshot().stars);const deck=await p.evaluate(()=>window.OrbitaWallet.snapshot().memory['mission-1-memory'].deck);
 const pairs=[0,1,2].map(n=>deck.map((v,i)=>v===n?i:-1).filter(i=>i>=0));const miss=[pairs[0][0],pairs[1][0]];
 for(let n=0;n<errors;n++){for(const i of miss)await p.locator(`[data-card="${i}"]`).click();if(n<2)await p.waitForFunction(()=>window.OrbitaWallet.snapshot().memory['mission-1-memory'].selected.length===0);}
 if(errors<3)for(let n=0;n<3;n++){for(const i of pairs[n])await p.locator(`[data-card="${i}"]`).click();if(n<2){assert(await p.locator('#luck-restart').isHidden());assert.equal(await p.evaluate(()=>window.OrbitaWallet.snapshot().stars),before);}}
 await p.locator('#luck-restart').waitFor();assert.equal(await p.evaluate(()=>window.OrbitaWallet.snapshot().stars),before+[6,3,1,-3][errors]);assert(await p.locator('#luck-dialog').evaluate(e=>e.scrollHeight<=e.clientHeight+1));
 await p.reload();await p.locator('#luck-restart').waitFor();assert.equal(await p.evaluate(()=>window.OrbitaWallet.snapshot().stars),before+[6,3,1,-3][errors]);
 await p.locator('#luck-restart').click();await p.locator('#luck-start').waitFor();await p.locator('#luck-skip').click();await p.locator('#luck-dialog').waitFor({state:'hidden'});
}
console.log('OK: acesso sem missão; repetições; três pares obrigatórios; +6/+3/+1/-3; retorno automático; recarga sem prêmio duplicado; sem rolagem em 1280x720, 390x844 e 360x640.');
}finally{await b.close()}})().catch(e=>{console.error(e);process.exitCode=1});
