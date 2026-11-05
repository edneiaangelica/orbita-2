(() => {
 'use strict';
 const mission=window.ORBITA_MISSION;
 const $=id=>document.getElementById(id);
 const esc=value=>String(value).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
 const key=`orbita2-mission${mission.id}-v2`;
 const params=new URLSearchParams(window.location.search);
 const requestedChallenge=params.has('challenge')?Number(params.get('challenge'))-1:null;
 let saved={done:[],attempted:[],challenge:0,question:0,errors:{},rounds:{}};
 try{const parsed=JSON.parse(localStorage.getItem(key));if(parsed&&Array.isArray(parsed.done)) saved={...saved,...parsed};}catch{}
 const validIds=new Set(mission.challenges.flatMap(c=>c.questions.map(q=>q.id)));
 let done=new Set(saved.done.filter(id=>validIds.has(id)));
 const attempted=new Set((saved.attempted||[]).filter(id=>validIds.has(id)));
 const attempts=saved.attempts&&typeof saved.attempts==='object'?saved.attempts:{};
 const rounds=saved.rounds||{};
 const round=()=>rounds[ci]||0;
 const answered=c=>c.questions.filter(item=>attempted.has(item.id)).length;
 const errors=saved.errors&&typeof saved.errors==='object'?saved.errors:{};
 let checking=false;
 let retryFeedback=false,reviewAttempts=0;
 const target=10;
 // Acesso temporário para revisão de todas as questões da trilha.
 const freeAccess=true;
 const unlocked=i=>freeAccess||i===0||count(mission.challenges[i-1])>=target;
 let ci=Number.isInteger(saved.challenge)&&saved.challenge>=0&&saved.challenge<3?saved.challenge:0;
 if(Number.isInteger(requestedChallenge)&&requestedChallenge>=0&&requestedChallenge<mission.challenges.length)ci=requestedChallenge;
 let qi=Number.isInteger(saved.question)&&saved.question>=0&&saved.question<15?saved.question:0;
 let order=[],money=[],feedbackText='',feedbackAudio='',dragIndex=null,screen='trail';
 let playback=null,utterance=null,voiceList=[],speechToken=0;
 const q=()=>mission.challenges[ci].questions[qi];
 const count=c=>c.questions.filter(item=>done.has(item.id)).length;
 function save(){try{localStorage.setItem(key,JSON.stringify({done:[...done],attempted:[...attempted],attempts,rounds,challenge:ci,question:qi,errors}));$('saved-status').textContent='Progresso salvo neste navegador';}catch{$('saved-status').textContent='Progresso disponível apenas nesta sessão';}}
 function stop(){speechToken++;if(playback){playback.pause();playback=null;}$('narration').hidden=true;if(window.speechSynthesis) speechSynthesis.cancel();utterance=null;$('audio-status').textContent='';}
 function normalizeSpeech(text){return text.replace(/(\d)\.(?=\d{3}\b)/g,'$1').replace(/>/g,' maior que ').replace(/</g,' menor que ').replace(/=/g,' igual a ').replace(/\+/g,' mais ').replace(/[-−]/g,' menos ').replace(/%/g,' por cento ').replace(/@/g,' arroba ').replace(/___/g,' espaço para o sinal ').replace(/\b0\b/g,'zero');}
 function questionText(item){return item.prompt;}
 function voices(){
  voiceList=window.speechSynthesis?speechSynthesis.getVoices().filter(v=>/^pt[-_]BR$/i.test(v.lang)):[];
  const selected=$('voice-select').value;
  $('voice-select').innerHTML='<option value="recorded">Francisca • Português brasileiro</option>'+voiceList.map((v,i)=>`<option value="${i}">${esc(v.name)} • ${esc(v.lang)}</option>`).join('');
  if([...$('voice-select').options].some(o=>o.value===selected))$('voice-select').value=selected;
  $('voice-description').textContent='Ouça a questão e o feedback sem esconder os textos e as imagens.';
 }
 function browserSpeak(text,token){
  if(token!==speechToken)return;
  const selected=voiceList[Number($('voice-select').value)]||voiceList.find(v=>/Francisca|Maria/i.test(v.name))||voiceList[0];
  if(!window.speechSynthesis||!selected){$('audio-status').textContent='Não foi possível reproduzir o áudio. Confira a saída de som e tente novamente.';return;}
  utterance=new SpeechSynthesisUtterance(normalizeSpeech(text));utterance.lang='pt-BR';utterance.voice=selected;utterance.rate=.9;
  utterance.onstart=()=>{if(token===speechToken)$('audio-status').textContent=`Lendo com ${selected.name}…`;};
  utterance.onend=()=>{if(token===speechToken){$('audio-status').textContent='Leitura concluída.';utterance=null;}};
  utterance.onerror=e=>{if(token===speechToken&&e.error!=='interrupted'&&e.error!=='canceled')$('audio-status').textContent='A leitura não iniciou. Verifique o volume do dispositivo e tente outra voz.';};
  speechSynthesis.resume();speechSynthesis.speak(utterance);
 }
 function read(text,file){
  window.orbitaEnableSound();stop();$('lesson').pause();const token=speechToken;
  if($('voice-select').value!=='recorded'){browserSpeak(text,token);return;}
  playback=$('narration');playback.src=`assets/sons/missao-${mission.id}/${file}.mp3`;playback.volume=1;playback.hidden=false;
  playback.onended=()=>{if(token===speechToken)$('audio-status').textContent='Leitura concluída.';};
  playback.play().then(()=>{if(token===speechToken)$('audio-status').textContent='Lendo com Francisca • Português brasileiro…';}).catch(()=>browserSpeak(text,token));
 }
 function chrome(){
  $('challenges').hidden=true;
  document.body.dataset.screen=screen;
  $('screen-title').textContent=screen==='trail'?'Trilhas':screen==='lesson'?`Missão ${mission.id} - ${mission.title}`:`Desafio ${ci+1} - ${mission.challenges[ci].title}`;
  $('back-trail').title='Trilhas';
  $('back-trail').href=screen==='trail'?'mission.html':'#trilhas';
  $('total-done').textContent=`${done.size} / 45`;
  $('challenges').innerHTML=mission.challenges.map((c,i)=>`<button type="button" class="challenge-tab" data-challenge="${i}" aria-current="${i===ci}" ${unlocked(i)?'':'disabled'}><span class="num">${i+1}</span><span><strong>${esc(c.title)}</strong><small>DESAFIO ${i+1}${unlocked(i)?'':' · Conclua o desafio anterior'}</small></span></button>`).join('');
  $('question-map').innerHTML=mission.challenges[ci].questions.map((item,i)=>`<button type="button" data-question="${i}" aria-current="${qi===i}" aria-label="Questão ${i+1}">${i+1}</button>`).join('');
  $('challenge-progress').max=target;$('challenge-progress').value=Math.min(count(mission.challenges[ci]),target);
 }
 function lesson(){if(!unlocked(ci))return;$('celebration-view').hidden=true;stop();screen='lesson';$('trail-view').hidden=true;$('learning-view').hidden=true;$('lesson-view').hidden=false;$('lesson-title').textContent=`Desafio ${ci+1} • ${mission.challenges[ci].title}`;$('lesson').src=mission.challenges[ci].video;$('video-status').textContent='';chrome();save();}
 function trail(){$('celebration-view').hidden=true;stop();screen='trail';$('lesson').pause();$('lesson-view').hidden=true;$('learning-view').hidden=true;$('trail-view').hidden=false;chrome();$('mission-list').innerHTML=(window.ORBITA_MISSIONS||[mission]).map(m=>`<article class="trail-mission"><h3>Missão ${m.id} - ${esc(m.title)}</h3><div ${m.id===mission.id?'id="trail-challenges"':''} class="challenge-tabs">${m.challenges.map((c,i)=>`<button type="button" class="challenge-tab" data-mission="${m.id}" data-challenge="${i}" ${m.id===mission.id&&!unlocked(i)?'disabled':''}><span class="num">${i+1}</span><span><strong>${esc(c.title)}</strong><small>DESAFIO ${i+1}</small></span></button>`).join('')}</div></article>`).join('');}
 function question(focus=false,retry=false){
  if(!retry)reviewAttempts=0;
  retryFeedback=false;
  if(!freeAccess&&(count(mission.challenges[ci])>=target||answered(mission.challenges[ci])===mission.challenges[ci].questions.length)){complete();return;}
  stop();screen='questions';$('lesson').pause();$('celebration-view').hidden=true;$('trail-view').hidden=true;$('lesson-view').hidden=true;$('learning-view').hidden=false;
  const item=q();order=[...(item.items||[])];money=[];feedbackText='';$('feedback').close();$('completion').hidden=true;
  $('question-count').textContent=`DESAFIO ${ci+1} • QUESTÃO ${qi+1} DE 15`;
  $('question-level').hidden=item.difficulty==='easy';$('question-level').textContent=item.difficulty==='easy'?'':'Vamos explorar';
  $('question-title').textContent=item.prompt;
  $('question-visual').innerHTML=item.image?`<img class="question-image" src="${esc(item.image)}" alt="${esc(item.imageAlt||'Ilustração da questão')}">`:'';
  const img=$('question-visual').querySelector('img');if(img)img.onerror=()=>{img.replaceWith(Object.assign(document.createElement('p'),{className:'image-description',textContent:item.imageAlt||'Não foi possível carregar a imagem.'}));};
  renderAnswers();$('check-answer').disabled=!freeAccess&&attempted.has(item.id);$('answers').inert=!freeAccess&&attempted.has(item.id);$('previous').disabled=qi===0;$('next').textContent='Próxima →';chrome();save();if(focus)$('question-title').focus();
 }
 function renderAnswers(){
  const item=q();
  if(item.type==='at1'){
   $('answers').innerHTML='<p class="hint">Arraste os cartões ou use as setas para mudar a ordem.</p><ol class="order-list">'+order.map((n,i)=>`<li class="order-card" draggable="true" data-order="${i}"><strong>${esc(n)}</strong><button type="button" data-move="${i}" data-direction="-1" aria-label="Mover ${esc(n)} para a esquerda" ${i===0?'disabled':''}>←</button><button type="button" data-move="${i}" data-direction="1" aria-label="Mover ${esc(n)} para a direita" ${i===order.length-1?'disabled':''}>→</button></li>`).join('')+'</ol>';return;
  }
  if(item.type==='at2'){
   $('answers').innerHTML='<p class="hint">Arraste ou clique no dinheiro. Clique em um valor na área de pagamento para removê-lo.</p><div class="money-bank">'+item.denominations.map((n,i)=>`<button type="button" draggable="true" data-money="${i}" class="subtle">R$ ${(n/100).toFixed(2).replace('.',',')}</button>`).join('')+'</div><div class="money-drop" id="money-drop" aria-label="Área de pagamento">'+money.map((n,i)=>`<button type="button" data-remove="${i}" class="subtle">R$ ${(n/100).toFixed(2).replace('.',',')} ×</button>`).join('')+`<p>Total: R$ ${(money.reduce((a,b)=>a+b,0)/100).toFixed(2).replace('.',',')}</p></div>`;return;
  }
  if(item.type==='input'){$('answers').innerHTML='<label for="typed-answer">Digite sua resposta</label><input class="input-answer" id="typed-answer" inputmode="decimal" autocomplete="off" required>';return;}
  $('answers').innerHTML='<div class="options">'+item.options.map((o,i)=>{const opt=typeof o==='object'?o:{label:o};return `<label class="option"><input type="radio" name="answer" value="${i}" required><span class="letter">${'ABCD'[i]}</span><span>${opt.image?`<img src="${esc(opt.image)}" alt="${esc(opt.label)}">`:esc(opt.label)}</span></label>`;}).join('')+'</div>';
 }
 async function check(event){
  event.preventDefault();if(checking||(!freeAccess&&attempted.has(q().id)))return;stop();const item=q();let answer,correct;
  if(item.type==='at1'){answer=order;correct=JSON.stringify(answer)===JSON.stringify(item.answer);}
  else if(item.type==='at2'){answer=money.reduce((a,b)=>a+b,0);correct=answer===item.answer;}
  else if(item.type==='input'){answer=$('typed-answer').value.trim().replaceAll('.','').replace(',','.');correct=answer!==''&&Number(answer)===Number(item.answer);}
  else {const selected=document.querySelector('input[name="answer"]:checked');if(!selected)return;answer=Number(selected.value);correct=answer===item.answer;}
  const wasComplete=count(mission.challenges[ci])>=target;
  if(wasComplete&&!freeAccess){await complete();return;}
  const review=freeAccess&&(wasComplete||attempted.has(item.id));
  if(review)reviewAttempts++;
  checking=true;$('learning-view').inert=true;$('check-answer').disabled=true;
  if(!review){
  attempts[item.id]=(Number(attempts[item.id])||0)+1;
  if(correct||attempts[item.id]>=2)attempted.add(item.id);
  if(!wasComplete&&!done.has(item.id)&&!correct)errors[ci]=(Number(errors[ci])||0)+1;
  if(correct)done.add(item.id);
  save();chrome();
  }
  try {
  if(!review){
  const daily=window.OrbitaRewards.daily(mission.id,mission.challenges[ci].id,round());
  await window.OrbitaWallet.grant([daily]);
  if(!wasComplete&&count(mission.challenges[ci])>=target){await complete();return;}
  }
  retryFeedback=!correct&&(review?reviewAttempts<2:!attempted.has(item.id));
  feedbackText=correct?item.success:item.errors?.[answer]||item.error;
  feedbackAudio=`${item.id}-${correct?'success':item.errors?.[answer]?`error-${answer}`:'error'}`;
  $('feedback-text').textContent=feedbackText;$('feedback').classList.toggle('correct',correct);
  $('feedback-title').textContent=correct?'Muito bem!':retryFeedback?'Você tem mais uma chance!':'Observe a explicação';
  $('feedback-mascot').src=`assets/imagens/feedbacks/mascote-${correct?'acerto':'erro'}.png`;
  $('continue-feedback').textContent=retryFeedback?'Tentar mais uma vez':freeAccess?'Continuar':answered(mission.challenges[ci])===15?'Ver resultado':'Continuar';
  $('feedback').showModal();
  } finally {checking=false;$('learning-view').inert=false;$('check-answer').disabled=!freeAccess&&attempted.has(item.id);$('answers').inert=!freeAccess&&attempted.has(item.id);}
 }
 async function complete(){
  const n=count(mission.challenges[ci]);
  const won=n>=target;
  if(!won&&answered(mission.challenges[ci])<mission.challenges[ci].questions.length)return;
  stop();$('feedback').close();$('lesson').pause();screen='celebration';
  $('trail-view').hidden=true;$('lesson-view').hidden=true;$('learning-view').hidden=true;
  $('celebration-view').hidden=false;
  const missionDone=mission.challenges.every(c=>count(c)>=target);
  $('celebration-title').textContent=won?'Parabéns! Desafio concluído!':'Rodada encerrada!';
  $('celebration-detail').textContent=!won?`Você acertou ${n} de 15 questões e ganhou ${n*50} moedas pelos acertos. Alcance 10 acertos em uma nova rodada para avançar.`:missionDone?'Você acertou 10 questões e completou a missão!':'Você acertou 10 questões. Mais uma conquista na sua jornada!';
  $('next-challenge').textContent=!won?'Tentar o desafio novamente':ci<mission.challenges.length-1?'Encarar o próximo desafio':'Voltar às trilhas';
  $('next-challenge').disabled=true;
  $('reward-status').textContent='Guardando suas recompensas…';
  $('reward-retry').hidden=true;
  $('reward-lines').replaceChildren();$('earned-coins').textContent='…';$('earned-stars').textContent='…';
  $('confetti').innerHTML=Array.from({length:55},(_,i)=>`<i style="--x:${(i*37)%100}%;--delay:${-(i%11)*.37}s;--duration:${3+i%4*.4}s;--color:${['#a0006d','#00bddd','#ffc83d','#6bc790','#8660d7'][i%5]};--angle:${i*29}deg"></i>`).join('');
  chrome();save();$('celebration-title').focus();
  $('confetti').hidden=!won;
  const result=await window.OrbitaWallet.grant([window.OrbitaRewards.daily(mission.id,mission.challenges[ci].id,round()),...window.OrbitaRewards.completion(mission.id,mission.challenges[ci].id,Number(errors[ci])||0,missionDone,n,round())]);
  if(!result.ok){$('reward-status').textContent='Não foi possível guardar suas recompensas. Tente novamente para continuar.';$('reward-retry').hidden=false;return;}
  const context=window.OrbitaRewards.scope(mission.id,mission.challenges[ci].id,round());
  const receipts=Object.values(result.state.rewards).filter(r=>r.scope===context);
  $('earned-coins').textContent=receipts.reduce((sum,r)=>sum+r.coins,0).toLocaleString('pt-BR');
  $('earned-stars').textContent=receipts.reduce((sum,r)=>sum+r.stars,0).toLocaleString('pt-BR');
  $('reward-lines').innerHTML=receipts.map(r=>`<li><span>${esc(r.label)}</span><strong>+${r.coins} moedas${r.stars?` · +${r.stars} estrelas`:''}</strong></li>`).join('');
  $('reward-status').textContent='Recompensas guardadas!';$('next-challenge').disabled=false;
  if(missionDone)window.OrbitaLuck?.open();
 }
 $('reward-retry').onclick=()=>complete();
 $('next-challenge').onclick=()=>{$('celebration-view').hidden=true;if(count(mission.challenges[ci])<target){mission.challenges[ci].questions.forEach(item=>{done.delete(item.id);attempted.delete(item.id);delete attempts[item.id];});errors[ci]=0;rounds[ci]=round()+1;qi=0;save();lesson();}else if(ci<mission.challenges.length-1){ci++;qi=0;lesson();}else trail();};
 $('mission-list').addEventListener('click',e=>{
  const b=e.target.closest('[data-mission][data-challenge]');if(!b)return;
  const selected=Number(b.dataset.mission),challenge=Number(b.dataset.challenge);
  if(selected!==mission.id){window.location.href=`mission.html?mission=${selected}&challenge=${challenge+1}`;return;}
  if(unlocked(challenge)){ci=challenge;qi=0;lesson();}
 });
 $('question-map').addEventListener('click',e=>{const b=e.target.closest('[data-question]');if(b){qi=Number(b.dataset.question);question(true);}});
 $('play-lesson').onclick=async()=>{
  stop();$('video-status').textContent='';
  const video=$('lesson');if(video.ended)video.currentTime=0;
  try{await video.play();}catch{$('video-status').textContent='Não foi possível iniciar o vídeo. Tente novamente ou use os controles do vídeo.';}
 };
 $('start-questions').onclick=()=>{if(freeAccess){qi=0;question(true);return;}const first=mission.challenges[ci].questions.findIndex(item=>!attempted.has(item.id));if(first>=0)qi=first;question(true);};
 $('review-lesson').onclick=()=>lesson();
 $('previous').onclick=()=>{if(qi>0){qi--;question(true);}};
 $('next').onclick=()=>{const questions=mission.challenges[ci].questions;if(freeAccess){qi=(qi+1)%questions.length;question(true);return;}const next=questions.findIndex((item,i)=>i>qi&&!attempted.has(item.id));const first=questions.findIndex(item=>!attempted.has(item.id));if(next>=0||first>=0){qi=next>=0?next:first;question(true);}else complete();};
 $('answer-form').addEventListener('submit',check);
 // Enter confirms an answer or advances feedback, once per key press.
 document.addEventListener('keydown',event=>{
  if(event.key!=='Enter'||event.isComposing||event.ctrlKey||event.altKey||event.metaKey||event.shiftKey)return;
  const feedback=$('feedback');
  if(document.querySelector('dialog[open]:not(#feedback)'))return;
  if(feedback.open){
   event.preventDefault();
   if(!event.repeat&&!checking&&!$('continue-feedback').disabled)$('continue-feedback').click();
   return;
  }
  if(screen!=='questions')return;
  const control=event.target.closest('button,a,select,textarea,audio,video,summary,[contenteditable="true"]');
  if(control&&control!==$('check-answer'))return;
  event.preventDefault();
  if(event.repeat||checking||$('check-answer').disabled)return;
  $('answer-form').requestSubmit($('check-answer'));
 });

 $('answers').addEventListener('change',()=>{$('feedback').close();stop();});
 $('answers').addEventListener('click',e=>{
  if(e.target.closest('[data-move],[data-money],[data-remove]'))stop();
  const b=e.target.closest('[data-move]');if(b){const i=Number(b.dataset.move),j=i+Number(b.dataset.direction);if(j>=0&&j<order.length){[order[i],order[j]]=[order[j],order[i]];renderAnswers();$('feedback').close();const focus=$('answers').querySelector(`[data-move="${j}"][data-direction="${b.dataset.direction}"]`);if(focus&&!focus.disabled)focus.focus();}}
  const cash=e.target.closest('[data-money]');if(cash){money.push(q().denominations[Number(cash.dataset.money)]);renderAnswers();$('feedback').close();}
  const remove=e.target.closest('[data-remove]');if(remove){money.splice(Number(remove.dataset.remove),1);renderAnswers();$('feedback').close();}
 });
 $('answers').addEventListener('dragstart',e=>{const item=e.target.closest('[data-order],[data-money]');if(!item)return;dragIndex=Number(item.dataset.order??item.dataset.money);e.dataTransfer.setData('text/plain',String(dragIndex));e.dataTransfer.effectAllowed='move';});
 $('answers').addEventListener('dragover',e=>{if(e.target.closest('[data-order],.money-drop'))e.preventDefault();});
 $('answers').addEventListener('drop',e=>{e.preventDefault();if(dragIndex===null)return;const target=e.target.closest('[data-order]');if(target&&q().type==='at1'){const n=order.splice(dragIndex,1)[0];order.splice(Number(target.dataset.order),0,n);}else if(e.target.closest('.money-drop')&&q().type==='at2')money.push(q().denominations[dragIndex]);dragIndex=null;renderAnswers();$('feedback').close();});
 $('answers').addEventListener('dragend',()=>dragIndex=null);
 $('read-question').onclick=()=>read(questionText(q()),`${q().id}-prompt`);
 $('read-feedback').onclick=()=>{ $('feedback-audio').append($('narration'),$('audio-status'));read(feedbackText,feedbackAudio); };
 $('close-feedback').onclick=()=>$('feedback').close();
 $('continue-feedback').onclick=()=>{$('feedback').close();if(retryFeedback)question(true,true);else $('next').click();};
 $('feedback').addEventListener('close',()=>{stop();$('narration-home').append($('narration'),$('audio-status'));});
 $('feedback').addEventListener('click',e=>{if(e.target===$('feedback')){const r=$('feedback').getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)$('feedback').close();}});
 $('stop-audio').onclick=stop;$('voice-select').onchange=stop;
 $('lesson').addEventListener('play',stop);
 $('lesson').addEventListener('error',()=>{$('video-status').textContent='Não foi possível carregar o vídeo. Recarregue a página ou continue para as questões.';});
 window.addEventListener('pagehide',stop);
 if(window.speechSynthesis)speechSynthesis.addEventListener('voiceschanged',voices);
 $('back-trail').addEventListener('click',e=>{if(screen!=='trail'){e.preventDefault();if(!checking)trail();}});
 document.addEventListener('orbita-mute',stop);
 window.addEventListener('orbita-luck-continue',trail);
 voices();
 if(Number.isInteger(requestedChallenge)&&requestedChallenge>=0&&requestedChallenge<mission.challenges.length)lesson();else trail();
})();
