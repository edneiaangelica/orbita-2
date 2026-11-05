const rows = [
  ['3 unidades de milhar + 5 centenas', ['3.500', '350', '3.050', '3.005'], 0, 'PENSE BEM!', 'LEGAL!', '3.000 + 500 = 3.500'],
  ['5 centenas + 2 dezenas + 1 unidade', ['521', '5.210', '502', '501'], 0, 'PRESTE ATENÇÃO!', 'MUITO BOM!', '500 + 20 + 1 = 521'],
  ['1 unidade de milhar + 5 centenas + 2 dezenas', ['5.120', '1.025', '1.520', '1.250'], 2, 'TENTE DE NOVO!', 'PARABÉNS!', '1.000 + 500 + 20 = 1.520'],
  ['7 centenas + 3 unidades', ['730', '7.300', '703', '73'], 2, 'PENSE BEM!', 'VOCÊ BRILHOU!', '700 + 3 = 703'],
  ['1 unidade de milhar + 2 dezenas', ['1.200', '1.020', '1.002', '2.100'], 1, 'OLHE DIREITO!', 'ÓTIMO!', '1.000 + 20 = 1.020']
];
module.exports = rows.map(([prompt, options, answer, wrong, right, calculation], i) => ({
  id: `d3-q${i + 11}`, type: 'qt3', prompt: `Quanto é ${prompt}`,
  options, answer, difficulty: 'regular',
  success: `${right} ${calculation}!`,
  error: `${wrong} Tente fazer essa operação no quadro posicional.`
}));
