window.ORBITA_PLANETS.push({
  previewUnlocked: true,
  id: 'tempus', name: 'Tempus', order: 8, cost: 650,
  heroImage: 'assets/imagens/diario/tempus/tempus.png',
  intro: 'Tantos relógios. Nenhuma hora certa.',
  description: 'Explore um mundo de engrenagens onde uma tarde cabe num espirro e o tempo nunca anda no mesmo compasso.',
  cards: [
    ['tempus', 'O planeta Tempus visto do Espaço', 'Enquanto na Terra uma hora tem sempre sessenta minutos, em Tempus, as coisas funcionam de um jeito completamente diferente. Visto do espaço, ele se parece com um relógio sem tampa, pois suas altas montanhas são como engrenagens.'],
    ['habitantes-de-Tempus', 'Habitantes do planeta Tempus e seus relógios', 'Os habitantes deste planeta, apesar de andarem com dezenas de relógios: nos pulsos, nos bolsos e até pendurados no pescoço, não têm controle nenhum sobre o tempo.'],
    ['tempusiano-espirrando', 'Tempusiano espirrando', 'Isso porque o tempo passa de forma diferente, dependendo do lugar e da situação. Às vezes, um espirro pode durar uma tarde inteira,'],
    ['tempusiano-trabalhando', 'Tempusiano trabalhando', 'enquanto um dia de trabalho dura apenas 20 minutos.'],
    ['familia-tempusiana-fazendo-refeicoes', 'Família tempusiana tomando café da manhã, almoçando e jantando', 'Em algumas cidades, tudo acontece tão depressa que as pessoas precisam tomar café da manhã, almoçar e jantar ao mesmo tempo.'],
    ['tempusianos-desorientados', 'Tempusianos desorientados', 'Por mais relógios que usem, o povo de Tempus nunca sabe ao certo que horas são. Dessa forma, é impossível combinar encontros, passeios ou compromissos de trabalho. Tudo em Tempus é descompassado e acontece por acaso.'],
    ['tempusiano-crianca', 'Tempusiano criança', 'Outro problema do planeta é que algumas pessoas permanecem crianças durante um tempo extraordinariamente longo,'],
    ['tempusiano-idoso', 'Tempusiano idoso', 'enquanto outras crescem e envelhecem com uma rapidez impressionante.'],
    ['crianças-e-idosos-na-escola', 'Crianças e idosos tempusianos na escola', 'Por isso, é comum ver crianças e idosos frequentando as mesmas turmas na escola.'],
    ['professora-bebê', 'Professora tempusiana', 'E o pior, às vezes, a professora tem a aparência de uma criança de 3 anos, quando, na verdade, já poderia (pelo nosso tempo) ter quarenta anos.'],
    ['garoto-tempusiano-aniversario', 'Garoto tempusiano decepcionado porque perdeu a sua festa de aniversário', 'Certa vez, depois de passar uma tarde jogando futebol, um menino voltou para casa e descobriu que seu aniversário de 9 anos já tinha passado e que os parentes e amigos já tinham ido embora levando os presentes.'],
    ['capitao-orbita-mexendo-nas-engrenagens-do-tempo', 'Capitão Órbita mexendo nas engrenagens do tempo.', 'Quando o viajante Órbita chegou ao planeta Tempus, ficou impressionado com tanta confusão e propôs mexer nas engrenagens do planeta. Acontece que o problema ficou ainda pior porque o tempo, além de desordenado, agora corria em sentido contrário.']
  ].map(([id, caption, text], index) => ({id, caption, text, number: index + 1, cost: index === 0 ? 650 : 500, image: `assets/imagens/diario/tempus/${id}.png`}))
});
