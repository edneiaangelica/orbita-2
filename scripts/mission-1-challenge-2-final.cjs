const rows = [
  [['1.937', '3.791', '7.193', '9.731'], 3, 'TENTE NOVAMENTE!', 'EXCELENTE!'],
  [['237', '491', '368', '754'], 3, 'NÃO É ISSO!', 'PARABÉNS!'],
  [['701', '710', '790', '801'], 3, 'OBSERVE COM ATENÇÃO!', 'VOCÊ É DEMAIS!'],
  [['31', '19', '29', '13'], 0, 'VAMOS TENTAR DE NOVO!', 'PARABÉNS!'],
  [['150', '149', '194', '130'], 2, 'OLHE OUTRA VEZ!', 'É ISSO MESMO!']
];
module.exports = rows.map(([options, answer, wrong, right], i) => ({
  id: `d2-q${i + 11}`, type: 'qt1', prompt: 'Marque o número maior:',
  options, answer, difficulty: 'regular',
  image: 'assets/imagens/questoes/3-ano/desafio-1/missao-2/m1-d2-q11.png',
  imageAlt: 'Menino pensando, com um ponto de interrogação.',
  success: `${right} O número ${options[answer]} é o maior`,
  error: `${wrong} Escolha o maior número entre as alternativas.`,
  errors: options.map(value => `${wrong} O número ${value} não é o número maior`)
}));
