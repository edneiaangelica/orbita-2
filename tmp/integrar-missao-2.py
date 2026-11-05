from pathlib import Path
p=Path('mission.html');s=p.read_text(encoding='utf-8')
s=s.replace('<script src="mission-data.js?v=d2-final-20261102" defer></script>','<script src="mission-data.js?v=missions-20261103" defer></script><script src="mission-2-data.js?v=1" defer></script><script src="mission-catalog.js?v=1" defer></script>')
s=s.replace('mission.js?v=luck-1','mission.js?v=missions-20261103')
s=s.replace('<article class="trail-mission"><h3>Missão 1 - Os números</h3><p hidden><span id="total-done"></span></p><div id="trail-challenges" class="challenge-tabs"></div></article>','<p hidden><span id="total-done"></span></p><div id="mission-list"><article class="trail-mission"><h3>Missão 1 - Os números</h3><div id="trail-challenges" class="challenge-tabs"></div></article></div>')
p.write_text(s,encoding='utf-8')
Path('mission-catalog.js').write_text('''(() => {
 'use strict';
 const missions=[window.ORBITA_MISSION,window.ORBITA_MISSION_2];
 const requested=Number(new URLSearchParams(window.location.search).get('mission'));
 window.ORBITA_MISSIONS=missions;
 window.ORBITA_MISSION=missions.find(m=>m.id===requested)||missions[0];
 document.title=`Órbita 2 • ${window.ORBITA_MISSION.title}`;
})();
''',encoding='utf-8')
p=Path('mission.js');s=p.read_text(encoding='utf-8')
s=s.replace("const key='orbita2-mission1-v2';","const key=`orbita2-mission${mission.id}-v2`;\n const params=new URLSearchParams(window.location.search);\n const requestedChallenge=params.has('challenge')?Number(params.get('challenge'))-1:null;")
s=s.replace('let qi=Number.isInteger(saved.question)',"if(Number.isInteger(requestedChallenge)&&requestedChallenge>=0&&requestedChallenge<mission.challenges.length)ci=requestedChallenge;\n let qi=Number.isInteger(saved.question)")
s=s.replace('assets/sons/missao-1/${file}.mp3','assets/sons/missao-${mission.id}/${file}.mp3')
s=s.replace(".replace(/[−]/g,' menos ')",".replace(/[-−]/g,' menos ')")
s=s.replace("$('trail-challenges').innerHTML=$('challenges').innerHTML;", """$('mission-list').innerHTML=(window.ORBITA_MISSIONS||[mission]).map(m=>`<article class="trail-mission"><h3>Missão ${m.id} - ${esc(m.title)}</h3><div ${m.id===mission.id?'id="trail-challenges"':''} class="challenge-tabs">${m.challenges.map((c,i)=>`<button type="button" class="challenge-tab" data-mission="${m.id}" data-challenge="${i}" ${m.id===mission.id&&!unlocked(i)?'disabled':''}><span class="num">${i+1}</span><span><strong>${esc(c.title)}</strong><small>DESAFIO ${i+1}</small></span></button>`).join('')}</div></article>`).join('');""")
s=s.replace("$('trail-challenges').addEventListener('click',e=>{const b=e.target.closest('[data-challenge]');if(b&&unlocked(Number(b.dataset.challenge))){ci=Number(b.dataset.challenge);qi=0;lesson();}});", """$('mission-list').addEventListener('click',e=>{
  const b=e.target.closest('[data-mission][data-challenge]');if(!b)return;
  const selected=Number(b.dataset.mission),challenge=Number(b.dataset.challenge);
  if(selected!==mission.id){window.location.href=`mission.html?mission=${selected}&challenge=${challenge+1}`;return;}
  if(unlocked(challenge)){ci=challenge;qi=0;lesson();}
 });""")
s=s.replace('voices();trail();',"voices();\n if(Number.isInteger(requestedChallenge)&&requestedChallenge>=0&&requestedChallenge<mission.challenges.length)lesson();else trail();")
p.write_text(s,encoding='utf-8')
p=Path('mission.css');s=p.read_text(encoding='utf-8');s+='\n#mission-list{display:grid;gap:18px;margin-bottom:20px}\n';p.write_text(s,encoding='utf-8')
# Keep the existing mission usable after its video folders were reorganized.
p=Path('mission-data.js');s=p.read_text(encoding='utf-8')
for i in range(1,4):s=s.replace(f'assets/videos/missao-1/missao-{i}/',f'assets/videos/missao-1/desafio-{i}/')
p.write_text(s,encoding='utf-8')
s=Path('scripts/generate-audio.py').read_text(encoding='utf-8').replace("OUT = ROOT / 'assets/sons/missao-1'","OUT = ROOT / 'assets/sons/missao-2'").replace("scripts/audio-manifest.json","scripts/audio-missao-2.json")
Path('scripts/generate-audio-missao-2.py').write_text(s,encoding='utf-8')
