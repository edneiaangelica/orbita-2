window.ORBITA_PLANETS.push({
  previewUnlocked: true,
  id: 'atria', name: 'Átria', order: 7, cost: 650,
  heroImage: 'assets/imagens/diario/atria/atria.png',
  intro: 'Um mundo de cores. Uma paisagem em movimento.',
  description: 'Conheça os orelhudos atrianos e explore um planeta onde casas, rios e montanhas saem para passear.',
  cards: [
  [
    "atria",
    "O planeta Átria visto do espaço",
    "O planeta Átria não é exatamente redondo, parece um pouco amassado, como uma bola de futebol esquecida debaixo de um sofá. É cor-de-rosa e, em volta dele, existem 4 anéis coloridos."
  ],
  [
    "atriano-monocromático",
    "Atriano monocromático",
    "Os habitantes de Átria têm orelhas tão grandes que nem precisam de paraquedas para pular de lugares altos. Além de orelhudos, os atrianos são muito coloridos. Cada um deles possui, pelo menos, 3 cores diferentes. Há os monocromáticos, com três tons de azul diferentes;"
  ],
  [
    "atriano-complementar",
    "Atriano complementar",
    "os complementares, que são, em geral, azul, laranja, vermelho e verde;"
  ],
  [
    "atriano-triadico",
    "Atriano triádico",
    "os triádicos: Laranja, Verde e Roxo"
  ],
  [
    "atrianos-coloridos",
    "População do planeta Átria",
    "e atrianos de todas as cores que você imaginar."
  ],
  [
    "atrianos-cumprimentando",
    "Cumprimento dos atrianos",
    "Os atrianos são muito simpáticos, mas, em vez de dar a mão para cumprimentar, como nós fazemos, eles dão 3 pulinhos e espirram purpurina pelo nariz."
  ],
  [
    "casa-em-atria",
    "Casa no planeta Átria",
    "Em Átria, todas as casas têm pernas de galinha. Assim, se algum habitante precisa se deslocar, não usa carro, ônibus ou avião. Ele vai na própria casa mesmo."
  ],
  [
    "casas-juntas",
    "Moradores de Átria conversando de suas casas",
    "É bastante comum duas casas se encontrarem, quando seus moradores querem conversar."
  ],
  [
    "montanha-com-pernas",
    "Montanha viajando pelo planeta Átria",
    "E não são só as casas que têm pernas e saem do lugar. As montanhas também viajam por todo o planeta,"
  ],
  [
    "rio-com-pernas",
    "Rio viajando pelo planeta Átria",
    "os rios"
  ],
  [
    "arvore-com-pernas",
    "Árvore viajando pelo planeta Átria",
    "e até as árvores."
  ],
  [
    "viajante-orbita-em-atria",
    "Como desenhar o mapa de Átria?",
    "O viajante Órbita achou o planeta muito divertido, apesar disso, ele ficou preocupado com uma questão: “Se tudo em Átria muda de lugar, como é que os cartógrafos podem desenhar um mapa do planeta?”"
  ]
]
  .map(([id, caption, text], index) => ({id, caption, text, number: index + 1, cost: index === 0 ? 650 : 500, image: `assets/imagens/diario/atria/${id}.png`}))
});

