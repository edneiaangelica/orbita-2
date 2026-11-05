/* Local wallet: purchases and idempotent reward receipts share one balance. */
(() => {
  const key = 'orbita2-wallet-v1';
  const preview = true; // Acesso livre durante a construção do app.
  function read() {
    const raw = localStorage.getItem(key);
    if (!raw) return {coins: 0, stars: 0, purchases: [], rewards: {}};
    const value = JSON.parse(raw);
    if (!value || !Number.isSafeInteger(value.coins) || value.coins < 0 || !Array.isArray(value.purchases) || !value.purchases.every(x => typeof x === 'string')) throw new Error('invalid-wallet');
    value.stars ??= 0;
    value.rewards ??= {};
    if (!Number.isSafeInteger(value.stars) || value.stars < 0 || typeof value.rewards !== 'object' || value.rewards === null || Array.isArray(value.rewards)) throw new Error('invalid-wallet');
    return value;
  }
  function snapshot() { try { return {...read(), available: true}; } catch { return {coins: 0, purchases: [], available: false}; } }
  function refresh() {
    const state = snapshot();
    document.querySelectorAll('[title="Moedas acumuladas"] strong,[data-coin-balance]').forEach(el => el.textContent = state.available ? state.coins.toLocaleString('pt-BR') : '—');
    document.querySelectorAll('[title="Estrelas acumuladas"] strong,[data-star-balance]').forEach(el => el.textContent = state.available ? state.stars.toLocaleString('pt-BR') : '—');
    window.dispatchEvent(new Event('orbita-wallet-change'));
  }
  async function purchase(id, cost, prerequisite) {
    const commit = () => {
      try {
        const state = read();
        if (state.purchases.includes(id)) return {ok: true};
        if (prerequisite && !state.purchases.includes(prerequisite)) return {ok: false, reason: 'planet'};
        if (!Number.isSafeInteger(cost) || cost <= 0) return {ok: false, reason: 'storage'};
        if (state.coins < cost) return {ok: false, reason: 'funds'};
        localStorage.setItem(key, JSON.stringify({...state, coins: state.coins - cost, purchases: [...state.purchases, id]}));
        refresh();
        return {ok: true};
      } catch { return {ok: false, reason: 'storage'}; }
    };
    if (!navigator.locks) return {ok: false, reason: 'browser'};
    return navigator.locks.request(key, commit);
  }
  async function grant(entries) {
    const commit = () => {
      try {
        const state = read();
        for (const entry of entries) {
          if (!entry.id || !Number.isSafeInteger(entry.coins) || entry.coins < 0 || !Number.isSafeInteger(entry.stars) || entry.stars < 0) throw new Error('invalid-reward');
          if (Object.hasOwn(state.rewards, entry.id)) continue;
          state.rewards[entry.id] = {...entry};
          state.coins += entry.coins;
          state.stars += entry.stars;
        }
        localStorage.setItem(key, JSON.stringify(state));
        refresh();
        return {ok: true, state};
      } catch { return {ok: false, reason: 'storage'}; }
    };
    return navigator.locks ? navigator.locks.request(key, commit) : commit();
  }
  async function memory(mission, action, index) {
    const commit = () => {
      try {
        const state = read(), id = `mission-${mission}-memory`;
        if (!preview && !state.rewards[`mission-${mission}-complete`]) return {ok:false};
        state.memory ??= {};
        let game = state.memory[id];
        if (!game || game.version!==2 || (preview && (action==='restart'||(action==='open'&&game.phase==='closed')))) {
          game = {version:2, round:(game?.round||0)+1, phase:'offer', deck:[0,0,1,1,2,2], selected:[], matched:[], errors:0};
          for (let i=5;i>0;i--) {const j=Math.floor(Math.random()*(i+1));[game.deck[i],game.deck[j]]=[game.deck[j],game.deck[i]];}
          state.memory[id]=game;
        }
        if(action==='start'&&game.phase==='offer')game.phase='playing';
        if(action==='skip'&&game.phase==='offer')game.phase='closed';
        if(action==='close')game.phase='closed';
        if(action==='next'&&game.phase==='playing'&&game.selected.length===2)game.selected=[];
        if(action==='flip'&&game.phase==='playing'&&Number.isInteger(index)&&index>=0&&index<6&&game.selected.length<2&&!game.selected.includes(index)&&!game.matched.includes(index)) {
          game.selected.push(index);
          if(game.selected.length===2){
            const match=game.deck[game.selected[0]]===game.deck[game.selected[1]];
            if(match){game.matched.push(...game.selected);game.selected=[];}
            else game.errors++;
            if(game.matched.length===6||game.errors===3){
              game.delta=game.matched.length===6?[6,3,1][game.errors]:-3;
              game.phase='result';
              const receipt=id+'-v2-round-'+game.round;
              if(!Object.hasOwn(state.rewards,receipt)){
                const delta=Math.max(-state.stars,game.delta);
                game.appliedDelta=delta;
                state.stars+=delta;
                state.rewards[receipt]={id:receipt,scope:id,label:'Sorte ou revés',coins:0,stars:delta};
              }
            }
          }
        }
        localStorage.setItem(key,JSON.stringify(state));refresh();
        return {ok:true,game};
      }catch{return {ok:false,reason:'storage'};}
    };
    return navigator.locks?navigator.locks.request(key,commit):commit();
  }
  const planets=[{name:'Lamalume',stars:-3},{name:'Papiron',stars:-1},{name:'Mecano',stars:2},{name:'Aerívia',stars:3},{name:'Planeta 42',stars:4},{name:'Aura Rubre',stars:5}];
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
  window.OrbitaWallet = {snapshot, purchase, refresh, grant, memory, preview, roulette, planets};
  window.addEventListener('storage', e => { if (e.key === key || e.key === null) refresh(); });
  refresh();
})();
