from pathlib import Path
p=Path('mission.html');s=p.read_text(encoding='utf-8');s=s.replace('<button type="button" id="start-questions" class="primary">Responder às questões</button>','<div class="lesson-actions"><button type="button" id="play-lesson" class="primary">Assistir videoaula</button><button type="button" id="start-questions" class="primary">Responder às questões</button></div>');s=s.replace('mission.js?v=missions-20261103','mission.js?v=play-lesson-1').replace('mission.css?v=trilha-colorida-1','mission.css?v=play-lesson-1');p.write_text(s,encoding='utf-8')
p=Path('mission.js');s=p.read_text(encoding='utf-8');s=s.replace(" $('start-questions').onclick=", """ $('play-lesson').onclick=async()=>{
  stop();$('video-status').textContent='';
  const video=$('lesson');if(video.ended)video.currentTime=0;
  try{await video.play();}catch{$('video-status').textContent='Não foi possível iniciar o vídeo. Tente novamente ou use os controles do vídeo.';}
 };
 $('start-questions').onclick=""");p.write_text(s,encoding='utf-8')
p=Path('mission.css');s=p.read_text(encoding='utf-8');s+='\n.lesson-actions{display:flex;justify-content:center;gap:12px;flex-wrap:wrap}\n';p.write_text(s,encoding='utf-8')
