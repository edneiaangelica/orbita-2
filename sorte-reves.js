(() => {
 if(window.ORBITA_MISSION.id===2)return;
 const $=id=>document.getElementById(id),dialog=$('luck-dialog');
 const names=['quadrado','redonda','triangular'];
 let busy=false,timer;
 async function action(type,index){
  if(busy)return;busy=true;clearTimeout(timer);
  try{
   const result=await window.OrbitaWallet.memory(window.ORBITA_MISSION.id,type,index);
   if(!result.ok){$('luck-status').textContent='Não foi possível salvar. Tente novamente.';return;}
   const g=result.game;
   if(g.phase==='closed'){dialog.close();if(type==='skip'||type==='close')window.dispatchEvent(new Event('orbita-luck-continue'));return;}
   $('luck-offer').hidden=g.phase!=='offer';$('luck-game').hidden=g.phase==='offer';
   $('luck-status').textContent=g.phase==='result'?(g.delta>0?`Todos os pares encontrados! Você ganhou ${g.delta} ${g.delta===1?'estrela':'estrelas'}!`:`Suas chances acabaram. ${g.appliedDelta<0?`Você perdeu ${-g.appliedDelta} estrelas.`:'Seu saldo continua em 0 estrelas.'}`):g.phase==='playing'?`${g.matched.length/2} de 3 pares · ${3-g.errors} ${3-g.errors===1?'chance restante':'chances restantes'}${g.selected.length===2?' · Tente outro par!':''}`:'';
   $('luck-cards').innerHTML=g.deck.map((n,i)=>{const matched=g.matched.includes(i),visible=matched||g.selected.includes(i)||g.phase==='result';return `<button class="memory-card ${visible?'revealed':''} ${matched?'matched':''}" type="button" data-card="${i}" aria-label="${visible?'Lamalumense '+names[n]+(matched?' — par encontrado':''):'Virar carta '+(i+1)}" ${g.phase!=='playing'||g.selected.length===2||visible?'disabled':''}>${visible?`<img src="assets/imagens/sorte-reves/lamalumense-${names[n]}.png" alt="Lamalumense ${names[n]}">`:'<span aria-hidden="true">✦</span>'}</button>`}).join('');
   $('luck-next').hidden=true;$('luck-close').hidden=false;$('luck-restart').hidden=g.phase!=='result';
   if(!dialog.open)dialog.showModal();
   if(g.phase==='playing'&&g.selected.length===2)timer=setTimeout(()=>action('next'),1100);
  }finally{busy=false;}
 }
 $('luck-start').onclick=()=>action('start');$('luck-skip').onclick=()=>action('skip');
 $('luck-next').onclick=()=>action('next');$('luck-close').onclick=()=>action('close');
 $('luck-restart').onclick=()=>action('restart');
 $('luck-cards').onclick=e=>{const card=e.target.closest('[data-card]');if(card&&!card.disabled)action('flip',Number(card.dataset.card));};
 dialog.addEventListener('cancel',e=>{e.preventDefault();action('close');});
 window.OrbitaLuck={open:()=>action('open')};
 document.querySelector('a[href="mission.html#sorte-reves"]')?.addEventListener('click',e=>{e.preventDefault();action('open');});
 if(location.hash==='#sorte-reves')action('open');
 else {const state=window.OrbitaWallet.snapshot(),game=state.memory?.[`mission-${window.ORBITA_MISSION.id}-memory`];if(game&&game.phase!=='closed'||state.rewards?.[`mission-${window.ORBITA_MISSION.id}-complete`]&&!game)action('open');}
})();
