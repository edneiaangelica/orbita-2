from pathlib import Path
p=Path('wallet.js');s=p.read_text(encoding='utf-8');needle='  window.OrbitaWallet = {snapshot, purchase, refresh, grant, memory, preview};'
new='''  const planets=[{name:'Lamalume',stars:-3},{name:'Papiron',stars:-1},{name:'Mecano',stars:2},{name:'Aerívia',stars:3},{name:'Planeta 42',stars:4},{name:'Aura Rubre',stars:5}];
  async function roulette(action){
    const commit=()=>{
      try{
        const state=read(),id='mission-2-roulette';
        if(!preview&&!state.rewards['mission-2-complete'])return {ok:false,reason:'locked'};
        state.roulette??={};let game=state.roulette[id]||{phase:'offer'};
        if(action==='spin'&&!Number.isInteger(game.index)){
          const random=new Uint32Array(1);do{crypto.getRandomValues(random);}while(random[0]>=4294967292);
          const index=random[0]%6,planet=planets[index],delta=Math.max(-state.stars,planet.stars);
          game={phase:'result',index,delta:planet.stars,appliedDelta:delta};
          if(state.rewards[id])return {ok:false,reason:'used'};
          state.stars+=delta;state.rewards[id]={id,scope:id,label:'Roleta dos planetas • '+planet.name,coins:0,stars:delta};
        }
        if(action==='close')game.phase='closed';
        if(action==='open')game.phase=Number.isInteger(game.index)?'result':'offer';
        state.roulette[id]=game;localStorage.setItem(key,JSON.stringify(state));refresh();return {ok:true,game};
      }catch{return {ok:false,reason:'storage'};}
    };
    return navigator.locks?navigator.locks.request(key,commit):commit();
  }
  window.OrbitaWallet = {snapshot, purchase, refresh, grant, memory, preview, roulette, planets};'''
assert needle in s;s=s.replace(needle,new);p.write_text(s,encoding='utf-8')
p=Path('sorte-reves.js');s=p.read_text(encoding='utf-8').replace("(() => {","(() => {\n if(window.ORBITA_MISSION.id===2)return;",1);p.write_text(s,encoding='utf-8')
p=Path('mission.html');s=p.read_text(encoding='utf-8');s=s.replace('wallet.js?v=preview-memory-2','wallet.js?v=roulette-1').replace('sorte-reves.js?v=5','sorte-reves.js?v=roulette-1');s=s.replace('</head>','<link rel="stylesheet" href="roleta.css?v=1"><script src="roleta.js?v=1" defer></script></head>');p.write_text(s,encoding='utf-8')
