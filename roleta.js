(() => {
 'use strict';
 if(window.ORBITA_MISSION.id!==2)return;
 const wallet=window.OrbitaWallet,planets=wallet.planets;
 const colors=['#A0006D','#7445A5','#4A8BDF','#087F8C','#FFD166','#06D6A0'];
 const images=['assets/imagens/mundos/aura-rubre/lamalume.png','assets/imagens/diario/papiron/planeta-papiron.png','assets/imagens/mundos/aura-rubre/mecano.png','assets/imagens/mundos/aura-rubre/aerivia.png','assets/imagens/mundos/aura-rubre/planeta-42.png','assets/imagens/mundos/aura-rubre/aura-rubre.png'];
 const point=(angle,r)=>[220+Math.cos(angle*Math.PI/180)*r,220+Math.sin(angle*Math.PI/180)*r];
 const sectors=planets.map((p,i)=>{
  const a=-90+i*60,b=a+60,[x1,y1]=point(a,204),[x2,y2]=point(b,204),[tx,ty]=point(a+30,142);
  return `<g><path d="M220 220 L${x1} ${y1} A204 204 0 0 1 ${x2} ${y2} Z" fill="white" stroke="${colors[i]}" stroke-width="3"/><image href="${images[i]}" x="${tx-54}" y="${ty-54}" width="108" height="108" preserveAspectRatio="xMidYMid meet"><title>${p.name}</title></image></g>`;
 }).join('');
 const instructions='Você tem uma tentativa! Clique em Girar a roleta e espere ela parar. O planeta indicado pela seta define quantas estrelas você ganha ou perde. Confira a tabela antes de girar. Seu saldo não fica abaixo de zero.';
 const dialog=document.createElement('dialog');dialog.id='roulette-dialog';dialog.className='roulette-dialog';dialog.setAttribute('aria-labelledby','roulette-title');
 dialog.innerHTML=`<header><span class="eyebrow">SORTE OU REVÉS · MISSÃO 2</span><h2 id="roulette-title">Roleta dos planetas</h2></header><div class="roulette-layout"><div class="roulette-stage"><div class="roulette-pointer" aria-hidden="true"></div><svg id="planet-wheel" viewBox="0 0 440 440" role="img" aria-label="Roleta com seis planetas e chances iguais">${sectors}<circle cx="220" cy="220" r="44" fill="white" stroke="#4A8BDF" stroke-width="5"/><text x="220" y="235" text-anchor="middle" font-size="45" fill="#A0006D">★</text></svg><p id="roulette-attempt">1 tentativa disponível</p></div><section class="roulette-info" aria-label="Como jogar"><p>${instructions}</p><button id="roulette-read" type="button" class="subtle">◖)) Ouvir instruções</button><p id="roulette-audio-status" role="status"></p><table><thead><tr><th>Planeta</th><th>Estrelas</th></tr></thead><tbody>${planets.map((p,i)=>`<tr data-planet="${i}"><td><span class="planet-label"><img src="${images[i]}" alt="" width="32" height="32">${p.name}</span></td><td>${p.stars>0?'+':'−'}${Math.abs(p.stars)} ★</td></tr>`).join('')}</tbody></table></section></div><p id="roulette-status" role="status" aria-live="polite">Em qual planeta será que a roleta vai parar?</p><footer><button id="roulette-spin" type="button" class="primary">Girar a roleta</button><button id="roulette-close" type="button" class="subtle">Continuar a trilha</button></footer>`;
 document.body.append(dialog);
 const $=id=>document.getElementById(id),audio=new Audio('assets/sons/missao-2/roleta-instrucoes.mp3');audio.playbackRate=1.25;
 let busy=false,reading=false;
 function stopAudio(){audio.pause();audio.currentTime=0;reading=false;$('roulette-read').textContent='◖)) Ouvir instruções';}
 function result(g){
  const used=Number.isInteger(g.index);$('roulette-spin').disabled=used;$('roulette-attempt').textContent=used?'Tentativa utilizada':'1 tentativa disponível';
  dialog.querySelectorAll('[data-planet]').forEach(row=>row.classList.toggle('selected',used&&Number(row.dataset.planet)===g.index));
  if(used){
   $('planet-wheel').style.transform=`rotate(${330-g.index*60}deg)`;
   const p=planets[g.index];let msg=g.appliedDelta>0?`Você ganhou ${g.appliedDelta} estrelas!`:g.appliedDelta<0?`Você perdeu ${-g.appliedDelta} ${g.appliedDelta===-1?'estrela':'estrelas'}.`:'Seu saldo continua em zero estrelas.';
   if(g.delta<0&&g.appliedDelta!==g.delta)msg+=' O saldo não fica abaixo de zero.';
   $('roulette-status').textContent=`${p.name}! ${msg}`;
  }else $('roulette-status').textContent='Em qual planeta será que a roleta vai parar?';
 }
 async function open(){if(busy||dialog.open)return;const r=await wallet.roulette('open');if(!r.ok)return;result(r.game);dialog.showModal();}
 $('roulette-spin').onclick=async()=>{
  if(busy)return;busy=true;stopAudio();$('roulette-spin').disabled=true;$('roulette-close').disabled=true;$('roulette-status').textContent='Girando…';
  try{
   const r=await wallet.roulette('spin');if(!r.ok){$('roulette-status').textContent='Não foi possível guardar o resultado. Tente novamente.';$('roulette-spin').disabled=false;return;}
   const wheel=$('planet-wheel'),end=1800+330-r.game.index*60;
   const animation=wheel.animate([{transform:'rotate(0deg)'},{transform:`rotate(${end}deg)`}],{duration:matchMedia('(prefers-reduced-motion: reduce)').matches?250:4200,easing:'cubic-bezier(.12,.65,.12,1)',fill:'forwards'});
   await animation.finished;result(r.game);animation.cancel();
  }finally{busy=false;$('roulette-close').disabled=false;}
 };
 async function close(){if(busy)return;stopAudio();const r=await wallet.roulette('close');if(!r.ok){$('roulette-status').textContent='Não foi possível salvar. Tente novamente.';return;}dialog.close();window.dispatchEvent(new Event('orbita-luck-continue'));}
 $('roulette-close').onclick=close;dialog.addEventListener('cancel',e=>{e.preventDefault();close();});dialog.addEventListener('close',stopAudio);
 $('roulette-read').onclick=async()=>{if(reading){stopAudio();return;}window.orbitaEnableSound?.();document.getElementById('lesson')?.pause();window.speechSynthesis?.cancel();document.getElementById('narration')?.pause();audio.playbackRate=1.25;try{await audio.play();reading=true;$('roulette-read').textContent='■ Parar leitura';$('roulette-audio-status').textContent='';}catch{$('roulette-audio-status').textContent='Não foi possível iniciar a leitura. Tente novamente.';}};
 audio.onended=stopAudio;window.addEventListener('pagehide',stopAudio);document.addEventListener('orbita-mute',stopAudio);
 window.OrbitaLuck={open};
 document.querySelector('a[href="mission.html#sorte-reves"]')?.addEventListener('click',e=>{e.preventDefault();open();});
 const state=wallet.snapshot(),g=state.roulette?.['mission-2-roulette'];
 if(location.hash==='#sorte-reves'||g&&g.phase!=='closed'||state.rewards?.['mission-2-complete']&&!g)open();
})();
