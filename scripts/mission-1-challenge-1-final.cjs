const success = 'PERFEITO! Você recompôs corretamente o número e respeitou a posição ocupada por cada algarismo.';
const error = 'ANALISE MAIS UMA VEZ! Observe em quais ordens há zero e não troque a posição das centenas, dezenas e unidades.';
const rows = [
  [['221', '2.221', '20.021', '2021'], 0, '200 + 20 + 1'],
  [['391', '3.009', '3.019', '319'], 3, '300 + 10 + 9'],
  [['1.003', '1.030', '3.100', '1.300'], 3, '1.000 + 300'],
  [['3.604', '3.640', '3.064', '3.046'], 1, '3.000 + 600 + 40'],
  [['1.400', '1.040', '1.004', '4.100'], 1, '1.000 + 0 + 40']
];
module.exports = rows.map(([options, answer, imageAlt], i) => ({
  id: `d1-q${i + 11}`, type: 'qt1', prompt: 'Quanto é?', options, answer,
  success, error, imageAlt, difficulty: 'regular',
  image: `assets/imagens/questoes/3-ano/desafio-1/missao-1/m1-d1-q${i + 11}.png`,
  errors: options.map(value => {
    const digits = value.replaceAll('.', '');
    const terms = [...digits].map((digit, index) => Number(digit) * 10 ** (digits.length - index - 1));
    const decomposition = terms.filter(Boolean).map(n => n.toLocaleString('pt-BR')).join(' + ');
    const names = ['unidades', 'dezenas', 'centenas', 'unidades de milhar', 'dezenas de milhar'];
    const zeros = [...digits].flatMap((digit, index) => digit === '0' ? [`0 ${names[digits.length - index - 1]}`] : []);
    return `ANALISE MAIS UMA VEZ! O número que você escolheu corresponde a ${decomposition}.${zeros.length ? ` Há ${zeros.join(' e ')}.` : ''} Observe em quais ordens há zero e não troque a posição dos algarismos.`;
  })
}));
