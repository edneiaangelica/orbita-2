const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const context={window:{}};vm.runInNewContext(fs.readFileSync('mission-data.js','utf8'),context);const mission=context.window.ORBITA_MISSION;
assert.equal(mission.challenges.length,3);const ids=new Set();
const expected=[[1,3,0,1,2,3,0,2,1,1],[1,2,0,null,null,3,2,0,1,0],[0,2,3,0,1,3,1,2,2,0]];
for(const [di,c] of mission.challenges.entries()){
 assert.equal(c.questions.length,15);assert(fs.existsSync(c.video));
 c.questions.forEach((q,i)=>{
  assert(!ids.has(q.id));ids.add(q.id);assert(q.prompt&&q.success&&q.error,`Texto ausente: ${q.id}`);
  assert.equal(q.difficulty,'regular');
  if(q.image)assert(fs.existsSync(q.image),q.image);
  if(i>=10&&di<2)assert(q.image,`Imagem nova ausente: ${q.id}`);
  if(i>=10&&di===2){assert.equal(q.type,'qt3');assert.equal(q.answer,[0,0,2,2,1][i-10]);assert(!q.image);}
  if(q.type==='at1')assert.deepEqual([...q.items].sort(),[...q.answer].sort());
  else{assert.equal(q.options.length,4);assert(q.answer>=0&&q.answer<4);}
  if(i<10&&expected[di][i]!==null)assert.equal(q.answer,expected[di][i],`Gabarito original: ${q.id}`);
  for(const text of [q.success,q.error,...(q.errors||[])])assert(!/correspondente à opção|\(escrever|\(decomposição/.test(text),`Feedback incompleto: ${q.id}`);
 });
}
const audio=JSON.parse(fs.readFileSync('scripts/audio-manifest.json','utf8'));
for(const job of audio){assert(job.text);assert(fs.statSync(`assets/sons/missao-1/${job.id}.mp3`).size>1000,job.id);}
const html=fs.readFileSync('mission.html','utf8');const domIds=[...html.matchAll(/\bid="([^"]+)"/g)].map(m=>m[1]);assert.equal(new Set(domIds).size,domIds.length);
for(const m of fs.readFileSync('mission.js','utf8').matchAll(/\$\('([^']+)'\)/g))assert(domIds.includes(m[1])||['typed-answer'].includes(m[1]),`Elemento ausente: ${m[1]}`);
assert(fs.readFileSync('inicio.html','utf8').includes('href="mission.html"'));
console.log(`OK: 45 questões, imagens, gabaritos, feedbacks, ${audio.length} arquivos de áudio, videoaulas e vínculos da interface.`);
