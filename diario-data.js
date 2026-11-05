window.ORBITA_DIARY = {
  previewUnlocked: true,
  id: 'umbralia', name: 'Umbrália', order: 9, cost: 650,
  heroImage: 'assets/imagens/diario/umbralia/umbralia.png',
  intro: 'Um mundo de sombras. Uma dupla cheia de opiniões.',
  description: 'Abra seu álbum e conheça os curiosos habitantes deste planeta — onde até a Morte precisa ter paciência.',
  cards: [
    ['umbralia', 'O planeta Umbrália vista do espaço', 'Entre os mundos que giram ao redor de Aura Rubre, existe um planeta chamado Umbrália. Visto do espaço, ele parece uma enorme bola de carvão.'],
    ['a-morte-e-a-gadanha', 'A morte e a Gadanha', 'Neste planeta vivem duas figuras muito importantes: a Morte e a Gadanha.'],
    ['a-morte', 'A morte com seu livro', 'A Morte é alta, usa um longo manto preto e carrega um livro no qual deveriam estar escritos os nomes das pessoas que chegaram ao fim da vida.'],
    ['a-gadanha-nervosa', 'A Gadanha irritada', 'Já a Gadanha é uma foice com olhos no cabo, boca na lâmina e um temperamento bastante afiado.'],
    ['a-morte-e-a-gadanha-brigando', 'A morte e a Gadanha brigando', 'Em teoria, as duas deveriam trabalhar juntas. A Morte escolheria quem deveria partir e a Gadanha realizaria o corte final. Na prática, elas nunca concordam sobre nada.'],
    ['gadanha-discordando-da-morte', 'A Gadanha discordando da morte', 'Quando a Morte escolhe uma pessoa, a Gadanha diz que ainda é cedo.'],
    ['morte-discordando-da-gadanha', 'A morte discordando da Gadanha', 'Quando a Gadanha aponta para alguém, a Morte afirma que aquela pessoa ainda possui assuntos pendentes.'],
    ['umbralhense', 'Umbralhense', 'Os habitantes do planeta são chamados de umbralhenses. Eles possuem pele acinzentada, olhos muito grandes e três orelhas capazes de girar em todas as direções. Assim, conseguem perceber rapidamente se quem se aproxima é a Morte, arrastando seu manto, ou a Gadanha, fazendo sua lâmina raspar pelo chão.'],
    ['o-equilibrio-dos-umbralhenses', 'O difícil equilíbrio dos umbralhenses', 'Como as discussões entre a Morte e a Gadanha podem durar meses ou até anos, os habitantes de Umbrália possuem uma das maiores expectativas de vida de todo o sistema de Aura Rubre. A maior preocupação dos umbralhenses é agradar às duas sem favorecer nenhuma delas. Isso, porém, é quase impossível, pois tudo aquilo que agrada à Morte costuma desagradar à Gadanha — e o contrário também acontece.'],
    ['a-morte-comendo-macarrão', 'A morte comendo macarrão com uma família de umbralhenses', 'A Morte, por exemplo, gosta muito de macarrão. Já a Gadanha prefere pizza e, como ninguém sabe qual das duas aparecerá para o jantar, todas as casas preparam os dois pratos. Se a Morte chega, a família coloca o macarrão sobre a mesa e esconde a pizza dentro do armário.'],
    ['a-gadanha-comendo-pizza', 'A gadanha comendo pizza com uma família de umbralhenses', 'Se a Gadanha aparece, o macarrão vai para debaixo da cama e a pizza é servida.'],
    ['capitao-orbita-fugindo-de-umbralia', 'Capitão da Expedição Órbita foge do planeta Umbrália', 'Quando o capitão da expedição Órbita chegou no planeta Umbrália, a Morte e a Gadanha quiseram logo saber o que ele trazia para agradá-las. E, como ele não havia levado nada, a morte anotou o nome dele no seu livro e a Gadanha afiou a sua lâmina.']
  ].map(([id, caption, text], index) => ({id, caption, text, number: index + 1, cost: index === 0 ? 650 : 500, image: `assets/imagens/diario/umbralia/${id}.png`}))
};
window.ORBITA_PLANETS = [window.ORBITA_DIARY];
