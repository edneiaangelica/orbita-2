(() => {
  const performance = errors => errors === 0 ? 500 : errors === 1 ? 400 : errors === 2 ? 350 : 250;
  const day = () => new Intl.DateTimeFormat('en-CA', {timeZone: 'America/Sao_Paulo', year: 'numeric', month: '2-digit', day: '2-digit'}).format(new Date());
  const scope = (mission, challenge, round) => `mission-${mission}-challenge-${challenge}${round===undefined?'':`-round-${round}-v2`}`;
  const daily = (mission, challenge, round) => ({id: `daily-${day()}`, scope: scope(mission, challenge, round), label: 'Jogar diariamente', coins: 100, stars: 2});
  const completion = (mission, challenge, errors, missionDone, correct=10, round) => {
    const context = scope(mission, challenge, round);
    if(correct<10)return [{id: `${context}-partial`, scope: context, label: `${correct} acertos × 50 moedas`, coins: correct*50, stars: 0}];
    const entries = [
      {id: `${context}-performance`, scope: context, label: `10 acertos · ${errors} ${errors === 1 ? 'erro' : 'erros'}`, coins: performance(errors), stars: 0},
      {id: `${context}-complete`, scope: context, label: 'Completar desafio', coins: 100, stars: 0}
    ];
    if (missionDone) entries.push({id: `mission-${mission}-complete`, scope: context, label: 'Completar missão', coins: 250, stars: 5});
    return entries;
  };
  window.OrbitaRewards = {performance, day, scope, daily, completion};
})();
