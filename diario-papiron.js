window.ORBITA_PLANETS.push({
  previewUnlocked: true,
  id: 'papiron', name: 'Papiron', order: 6, cost: 650,
  heroImage: 'assets/imagens/diario/papiron/planeta-papiron.png',
  intro: 'Um mundo de dobraduras. Uma história que não sai do papel.',
  description: 'Entre filas, formulários e aviõezinhos, descubra os curiosos habitantes de um planeta feito de papel.',
  cards: [
  [
    "planeta-papiron",
    "O planeta Papiron visto do espaço",
    "Na órbita da estrela Aura Rubre, existe um planeta que parece uma bola de papel amassado. O nome dele é Papiron. Neste planeta nunca chove e o fogo ainda não foi inventado; o que é muito bom, pois quase tudo lá é feito de papel."
  ],
  [
    "papirense",
    "Habitante do planeta Papiron",
    "Os papirenses parecem feitos de dobraduras, com pés muito largos e joelhos que se desdobram, formando uma cadeirinha."
  ],
  [
    "papirenses-em-fila",
    "Fila no planeta Papiron",
    "Isso é muito útil, pois, em Papiron, a população tem que aguentar longas esperas."
  ],
  [
    "papirense-trabalhando",
    "Excesso de formulários no planeta Papiron",
    "Tudo o que se vai fazer, neste mundo, depende de uma autorização do governo e, para conseguir essa autorização é preciso enfrentar muitas filas e preencher inúmeros formulários. Às vezes é preciso preencher formulários para conseguir formulários!"
  ],
  [
    "papirense-na-fila-da-borracha",
    "Papirense na fila para conseguir uma borracha",
    "Quem erra ao preencher um formulário, precisa entrar em outra fila para conseguir uma borracha."
  ],
  [
    "lojas-vazias",
    "Comércio vazio no planeta Papiron",
    "Acostumados à espera, os papirenses fazem tudo devagar. Durante muito tempo, essa vida tranquila ajudou os habitantes a viver cerca de 300 anos. Mas as filas cresceram tanto que passou a faltar tempo para estudar, trabalhar e cuidar da saúde. As lojas vendem menos, faltam produtos e a economia vai de mal a pior."
  ],
  [
    "comissao-de-cientistas",
    "Cientistas discutem a situação econômica do planeta",
    "Diante de tantos problemas, os governantes nomearam uma comissão de cientistas para estudar a situação econômica em Papiron."
  ],
  [
    "relatorio",
    "Relatório produzido pela comissão de cientistas em Papiron",
    "Essa comissão já produziu um relatório que precisa de um caminhão para ser transportado. Mas, até hoje, nada foi feito para melhorar a situação do planeta."
  ],
  [
    "comissao-trabalhando",
    "comissão de cientistas trabalhando em Papiron",
    "Os cientistas compreendem bem o problema do planeta. Já fizeram planos de ação, já calcularam os gastos, definiram os orçamentos."
  ],
  [
    "papirense-coçando-a-cabeça",
    "Trabalhador papirense preso na burocracia",
    "Mas, quando chega na hora da realização, nada sai do lugar. Isso porque, quando alguém decide dar o primeiro passo precisa, antes, enfrentar diversas filas para preencher inúmeros formulários. E sempre falta alguma assinatura ou algum carimbo. Assim, nada sai do papel."
  ],
  [
    "visitante-orbita-em-papiron",
    "Visitante Órbita é recebido com formulários em Papiron.",
    "Quando o viajante Órbita chegou em Papiron, foi recebido com um monte de formulários."
  ],
  [
    "aviaozinhos",
    "Viajante Órbita faz aviõezinhos com os formulários de Papiron",
    "Sem saber o porquê de toda aquela papelada, ele resolve fazer aviãozinhos de papel e deixa os papirenses desesperados."
  ]
]
  .map(([id, caption, text], index) => ({id, caption, text, number: index + 1, cost: index === 0 ? 650 : 500, image: `assets/imagens/diario/papiron/${id}.png`}))
});

