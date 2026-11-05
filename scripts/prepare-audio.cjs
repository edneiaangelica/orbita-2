const fs=require('node:fs');const vm=require('node:vm');const context={window:{}};vm.runInNewContext(fs.readFileSync('mission-data.js','utf8'),context);
const normalize=s=>s.replace(/(\d)\.(?=\d{3}\b)/g,'$1').replace(/>/g,' maior que ').replace(/</g,' menor que ').replace(/=/g,' igual a ').replace(/\+/g,' mais ').replace(/[−]/g,' menos ').replace(/%/g,' por cento ').replace(/@/g,' arroba ').replace(/___/g,' espaço para o sinal ');
const jobs=[];
for(const c of context.window.ORBITA_MISSION.challenges)for(const q of c.questions){
 const text=q.prompt;
 jobs.push({id:`${q.id}-prompt`,text:normalize(text)},{id:`${q.id}-success`,text:normalize(q.success)},{id:`${q.id}-error`,text:normalize(q.error)});
 (q.errors||[]).forEach((text,i)=>{if(text)jobs.push({id:`${q.id}-error-${i}`,text:normalize(text)});});
}
fs.writeFileSync('scripts/audio-manifest.json',JSON.stringify(jobs,null,2));console.log(`${jobs.length} áudios preparados`);
