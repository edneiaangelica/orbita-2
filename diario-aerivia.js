window.ORBITA_PLANETS.push({
  previewUnlocked: true,
  id: 'aerivia', name: 'Aerívia', order: 9, cost: 650,
  heroImage: 'assets/imagens/diario/aerivia/planeta-aerivia.png',
  intro: 'Rios no ar. Sentimentos nas nuvens.',
  description: 'Siga as correntes de vento por um mundo aquarelado, onde até as casas passeiam e uma vida leve pode dar muito trabalho.',
  cards: [
    ['planeta-aerivia', 'O planeta Aerívia visto do Espaço', 'Aerívia é o nono planeta do sistema estelar Aura Rubre. Visto do espaço, ele se parece um pouco com a Terra, por causa da sua cor azulada, mas, ao contrário do nosso planeta, ele não possui nenhum elemento sólido.'],
    ['rios-suspensos', 'Rios suspensos no planeta Aerívia', 'Em Aerívia, tudo flutua. Os ventos são tão fortes que carregam as gotas de água, formando rios suspensos.'],
    ['aeriviano', 'Habitante do planeta Aerívia', 'Os habitantes de Aerívia são chamados de aerivianos. Eles possuem corpos leves e elásticos, braços compridos e pés que balançam no ar como se fossem bandeirinhas e cabeças enfiadas em nuvens.'],
    ['aeriviano-alegre', 'Aeriviano de bom-humor', 'Cada aeriviano possui sua própria nuvem, que o acompanha desde o nascimento. Essas nuvens mudam de cor conforme o humor de seus donos. Quando um aeriviano está alegre, sua nuvem fica cor-de-rosa;'],
    ['aeriviano-com-medo', 'Aeriviano com medo', 'quando sente medo, a nuvem se torna roxa;'],
    ['aeriviano-zangado', 'Aeriviano zangado', 'e, quando fica zangado, pequenos relâmpagos começam a estalar sobre suas orelhas. Por esse motivo, é quase impossível esconder os sentimentos em Aerívia.'],
    ['casa-em-aerivia', 'Casa flutuante no planeta Aerívia', 'As casas também flutuam. Elas são feitas dentro de bolhas enormes, formadas por várias camadas de vapor.'],
    ['correio-em-aerivia', 'Correio em Aerívia', 'Como os ventos nunca param, as casas mudam de lugar o tempo todo. Por isso, ninguém possui endereço fixo. As cartas são entregues por pequenas correntes de ar treinadas para reconhecer o cheiro do destinatário.'],
    ['viagem-com-guarda-chuvas', 'Aeriviano viajando com guarda-chuvas', 'Em Aerívia não existem ruas. Para viajar, os habitantes aproveitam as correntes de vento. Alguns usam grandes guarda-chuvas;'],
    ['viagem-com-pipas', 'Aeriviano viajando com pipa', 'outros preferem pipas amarradas à cintura.'],
    ['aeriviana-correndo-atras-da-panela', 'Aeriviana tentando fazer o almoço', 'Apesar de viver com a cabeça nas nuvens, os aerivianos não são nada distraídos. Ao contrário, viver perseguindo a própria casa, a escola, os materiais de trabalho etc., exige muita atenção e é muito cansativo.'],
    ['o-peso-da-vida', '“Quanto pesa a vida em Aerívia?”', 'Quando o visitante Órbita chegou em Aerívia, quis saber por que os habitantes pareciam tão cansados.\n\n— Afinal, quanto pesa uma vida tão leve? — ele perguntou.']
  ].map(([id, caption, text], index) => ({id, caption, text, number: index + 1, cost: index === 0 ? 650 : 500, image: `assets/imagens/diario/aerivia/${id}.png`}))
});
