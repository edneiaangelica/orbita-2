window.ORBITA_PLANETS.push({
  previewUnlocked: true,
  id: 'planeta-42', name: 'Planeta 42', order: 4, cost: 650,
  heroImage: 'assets/imagens/diario/planeta-42/planeta-42.png',
  intro: 'Cabeças nas contas. Um mundo inteiro nas nuvens.',
  description: 'Atravesse a névoa e conheça os matemáticos que contam tudo — e que não podem perder a conta!',
  cards: [
    ['planeta-42', 'Planeta 42 visto do espaço.', 'A cem anos-luz de distância, já é possível avistar a enorme névoa que envolve o Planeta 42.'],
    ['planeta-enfumaçado', 'Atmosfera do Planeta 42.', 'Essa névoa nada mais é do que a fumaça que sai dos cérebros dos nove bilhões de seres vivos que habitam o planeta.\n\n— E por que sai fumaça do cérebro deles? — alguém pode perguntar.\n\nEu posso responder: é porque a população do Planeta 42 é formada por matemáticos que passam o dia e a noite fazendo contas.'],
    ['habitante-planeta-42', 'Matemático envolvido pela fumaça do seu pensamento.', 'Eles pensam tanto, mas tanto, que a fumaça começa a sair de suas cabeças.\n\nE, por falar em cabeça, a dos habitantes do Planeta 42 é duas vezes maior que o restante do corpo. Seus braços e pernas são curtos, e eles possuem somente três dedos em cada mão. Se não fosse a enorme quantidade de cabelo sobre suas cabeças e, no caso dos homens, as longas barbas em seus queixos, eu diria que essas criaturas se parecem com bebês que ainda estão se formando na barriga de suas mães.'],
    ['cidade-no-planeta-42', 'A capital do Planeta 42.', 'Apesar de muito inteligentes, os matemáticos são pouco criativos. Prova disso é que tudo se parece no Planeta 42. As casas são formadas por figuras geométricas simétricas, as copas das árvores são círculos perfeitos e as ruas são todas retas.'],
    ['parque-de-diversao-planeta-42', 'Parque de diversões do Planeta 42.', 'Tudo é muito cinzento no Planeta 42, até mesmo os parques de diversões. Em vez de escorregadores e balanços, as crianças brincam com números e sinais das operações matemáticas.'],
    ['bebe-planeta-42', 'Nascimento de um bebê no Planeta 42.', 'Quando nascem, os bebês não ganham ursinhos de pelúcia nem roupinhas do Homem-Aranha. Cada um recebe logo uma calculadora.'],
    ['matematico-contando-estrelas', 'Matemático especialista na contagem de estrelas.', 'Mas que contas fazem os matemáticos do Planeta 42?\n\nOra, eles contam tudo!\n\nContam as estrelas do céu.'],
    ['matematico-contando-areia', 'Matemático especialista na contagem de grãos de areia.', 'Contam os grãos de areia das praias.'],
    ['matematico-contando-gotas-do-mar', 'Matemático especialista na contagem de gotas de água do mar.', 'Contam as gotas de água dos mares.'],
    ['matematico-contando-a-chuva', 'Matemático especialista na contagem de pingos de chuva.', 'Quando chove, contam até mesmo os pingos de chuva.'],
    ['matematico-doente', 'Matemático que perdeu a conta.', 'E não há nada mais triste do que um matemático do Planeta 42 quando perde a conta. É como se ele ficasse doente.'],
    ['matematico-conversando-com-capitao', 'O capitão da Expedição Órbita conversando com um matemático do Planeta 42.', 'O mais impressionante é que quando o capitão da Expedição Órbita chegou ao planeta 42 e perguntou:\n\n— Quantas são as estrelas do céu? Quantos são os grãos de areia da praia? E as gotas de água do mar? E os pingos da chuva?\n\nNenhum matemático soube responder.']
  ].map(([id, caption, text], index) => ({id, caption, text, number: index + 1, cost: index === 0 ? 650 : 500, image: `assets/imagens/diario/planeta-42/${id}.png`}))
});
