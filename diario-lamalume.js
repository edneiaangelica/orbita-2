window.ORBITA_PLANETS.push({
  previewUnlocked: true,
  id: 'lamalume', name: 'Lamalume', order: 2, cost: 650,
  heroImage: 'assets/imagens/diario/lamalume/planeta-lamalume.png',
  intro: 'Um mar de lama. Um festival de formas e sorrisos.',
  description: 'Conheça os lamalumenses: criaturas fofas, cheias de personalidade e muito orgulhosas da própria beleza.',
  cards: [
    ['planeta-lamalume', 'O planeta Lamalume visto do espaço.', 'Muito além das rotas conhecidas, depois das dobras do tempo e da imaginação, existe um planeta chamado Lamalume. Visto do espaço, ele parece uma enorme bola de chocolate derretido.'],
    ['chuva-em-lamalume', 'Os habitantes do planeta Lamalume', 'Toda a superfície do planeta Lamalume é coberta pelo Grande Lago de Lama, porque chove a maior parte do tempo. Neste grande lago, vivem criaturas totalmente feitas de lama.'],
    ['problema-da-vaidade', 'Vaidade: maior motivo de conflito entre os lamalumenses', 'Embora, em tempos líquidos, ninguém possa distinguir um lamalumense do outro, essas criaturas são muito orgulhosas da sua beleza física; tanto que o maior problema político de Lamalume é a vaidade extrema dos seus habitantes. Cada lamalumense se considera mais bonito que o outro e não admite nenhuma crítica à sua aparência.'],
    ['sol-de-lamalume', 'A estrela Aura Rubre vista do planeta Lamalume', 'Devido à sua órbita elíptica, uma vez por ano, o planeta Lamalume fica bem perto da estrela Aura Rubre. É o período que os lamalumenses chamam de tempo seco, que seria o equivalente ao nosso verão.'],
    ['saindo-da-lama', 'O período seco em Lamalume', 'O calor seca uma parte do planeta e as criaturas de lama saem do lago, se separam dos outros e dão formas aos seus corpos.'],
    ['lamalumense-de-bigode', 'Lamalumense desenhando um bigode no rosto.', 'Alguns tomam formas compridas como cipós, e passam horas desenhando um bigode.'],
    ['lamalumense-redonda', 'Lamalumense fazendo covinhas nas bochechas', 'Outros preferem contornos arredondados e gostam de fazer covinhas nas bochechas, com os dedos.'],
    ['lamalumense-quadrado', 'Lamalumense quadrado, esculpindo dentes perfeitos', 'Há também quem se molde em formas quadradas e dê a si mesmo dentes perfeitos, embora eles não precisem de dentes para comer, pois se alimentam de lama.'],
    ['lamalumense-triangular', 'Lamalumense triangular, moldando um nariz', 'Também não faltam os que preferem a forma triangular, moldando narizes finos e compridos.'],
    ['concepcao', 'Dois lamalumenses em ritual de amor e reprodução', 'É durante esse festival de formas que acontecem os encontros amorosos. Quando dois lamalumenses desejam continuar ligados, eles retiram um pequeno punhado de lama de seus próprios corpos e misturam as duas porções dentro de uma concha.'],
    ['nascimento', 'Nascimento de um bebê em Lamalume', 'A concha é enterrada na margem do lago e se transforma em um casulo de barro. Depois das primeiras chuvas, o casulo se abre e um pequeno monstrinho de lama escorrega para dentro do lago.'],
    ['pergunta', 'Visitante. Órbita em Lamalume', 'Uma coisa curiosa sobre o planeta Lamalume é que seus habitantes adoram receber visitantes. Quando chega alguém de outro planeta, os homens de lama correm em sua direção com uma única pergunta nos lábios (que aliás é tudo o quanto desejam saber):\n— Sou bonito?']
  ].map(([id, caption, text], index) => ({id, caption, text, number: index + 1, cost: index === 0 ? 650 : 500, image: `assets/imagens/diario/lamalume/${id}.png`}))
});
