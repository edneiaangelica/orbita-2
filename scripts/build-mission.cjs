const fs = require('node:fs');
const raw = fs.readFileSync('docs/missao-1-original.txt','utf8');
const titles = ['Leitura e escrita de números','Comparação entre números','Valor posicional'];
const clean = s => s.replace(/[“”]/g,'').trim();
const challenges = raw.split(/Desafio \d\s*[-–]/).slice(1).map((part, di) => ({id:di+1,title:titles[di],video:`assets/videos/missao-1/missao-${di+1}/vd-explica-d1-m${di+1}.mp4`,questions:part.split(/questao\s*[-–]\s*\d+/i).slice(1).map((block,qi)=>{
 const lines=block.trim().split(/\r?\n/).map(s=>s.trim()).filter(Boolean);
 const type=lines[0].includes('arrastar')?'at1':lines[0].includes('3')?'qt3':'qt1';
 const prompt=lines[1].replace(/\s*\(imagem:.*?\)/,'').trim();
 const options=lines.filter(l=>/^[A-D]\)/.test(l)).map(l=>clean(l.slice(2).split('(feedback')[0]));
 const fb=kind=>{const line=lines.find(l=>l.startsWith(`(feedback ${kind}:`)); return line?clean(line.slice(line.indexOf(':')+1).split(') Ex:')[0].replace(/\)\s*$/,'')):''};
 const answer=block.match(/GABARITO:\s*([A-D])/);
 const q={id:`d${di+1}-q${qi+1}`,type,prompt,options,answer:answer?answer[1].charCodeAt(0)-65:null,success:fb('acerto'),error:fb('erro'),difficulty:'regular'};
 if(type==='qt1') q.image=`assets/imagens/questoes/3-ano/desafio-1/missao-${di+1}/quiz-d1-m${di+1}-q${qi+1}.png`;
 if(type==='at1') {q.items=lines[2].replace(/\.$/,'').split(',').map(s=>s.trim());q.answer=[...q.items].sort((a,b)=>Number(a.replace('.',''))-Number(b.replace('.',''))); if(prompt.includes('DECRESCENTE'))q.answer.reverse();}
 return q;
})}));
const alts=['3 centenas, 6 dezenas e 4 unidades.','4 centenas, 4 dezenas e 8 unidades.','8 centenas e 7 unidades.','3 centenas e 9 dezenas.','3 milhares, 2 centenas, 3 dezenas e 4 unidades.','TREZENTOS E CINQUENTA E QUATRO','MIL QUATROCENTOS E NOVE','3.009','1 unidade de milhar, 2 centenas, 3 dezenas e 5 unidades.','1 unidade de milhar, 9 centenas, 0 dezenas e 3 unidades.'];
challenges[0].questions.forEach((q,i)=>q.imageAlt=alts[i]);
const errors={5:['345 é trezentos e quarenta e cinco.','435 é quatrocentos e trinta e cinco.','543 é quinhentos e quarenta e três.'],6:['','1.490 é mil quatrocentos e noventa.','1000.400.9 não é uma escrita válida de um número natural. Não separamos cada ordem com um ponto.','1.499 é mil quatrocentos e noventa e nove.'],7:['Trezentos e nove é 309.','Trezentos e noventa é 390.','','Três mil e noventa é 3.090.']};
for(const [index,texts] of Object.entries(errors)){const q=challenges[0].questions[index];q.errors=texts.map(t=>`Tente novamente! ${t} Observe a representação e confira cada ordem.`);q.error='Tente novamente! Confira cada ordem do número.';}
const decomposition = value => {const n=Number(value.replaceAll('.',''));return `${Math.floor(n/1000)} unidade(s) de milhar, ${Math.floor(n/100)%10} centena(s), ${Math.floor(n/10)%10} dezena(s) e ${n%10} unidade(s)`;};
for(const i of [8,9]){const q=challenges[0].questions[i];q.errors=q.options.map(v=>`Observe novamente! ${v} corresponde a ${decomposition(v)}. Compare com a decomposição da imagem.`);q.error='Confira a quantidade em cada ordem.';}
challenges[1].questions[5].errors=['Resposta incorreta! 20 dezenas = 200. Compare com as outras quantidades.','Resposta incorreta! 3 centenas = 300. Compare com as outras quantidades.','Resposta incorreta! 1 unidade de milhar = 1.000. Compare com as outras quantidades.'];
challenges[1].questions[5].error='Transforme cada quantidade em um número e compare.';
['5 + 4, espaço para o sinal, 3 + 6.','100 + 100, espaço para o sinal, 200 − 100.','500 + 500, espaço para o sinal, 1.500 − 500.','1.500 + 1.500, espaço para o sinal, 2.000 − 1.000.'].forEach((alt,i)=>challenges[1].questions[i+6].imageAlt=alt);
const extra=[
 [
 ['Quantos cubinhos aparecem na figura?',['3','4','5','6'],2,'Muito bem! Contando um a um, encontramos 5 cubinhos.','Conte os cubinhos da esquerda para a direita, sem pular nenhum.','Cinco cubinhos separados.'],
 ['Qual número a figura representa?',['10','12','21','2'],1,'Isso mesmo! Uma dezena vale 10. Com mais 2 unidades, temos 12.','A barrinha vale 10. Acrescente os dois cubinhos.','Uma barrinha com dez cubinhos e dois cubinhos separados.'],
 ['Como escrevemos o número do cartão em algarismos?',['12','2','20','30'],2,'Muito bem! Vinte se escreve 20: duas dezenas e nenhuma unidade.','Vinte tem duas dezenas. Procure o 2 seguido do zero.','VINTE'],
 ['Como lemos o número do cartão?',['Treze','Trinta','Três','Vinte'],1,'Você acertou! 30 se lê trinta.','Observe o 3 na casa das dezenas: são três dezenas.','30'],
 ['Qual número corresponde à decomposição da imagem?',['41','10','40','14'],3,'Excelente! 10 mais 4 é igual a 14.','Comece no 10 e conte mais quatro unidades.','10 + 4']
 ],
 [
 ['Qual é o sucessor de 9?',['8','10','11','7'],1,'Isso mesmo! 10 vem logo depois de 9.','Sucessor é o próximo número. Conte: oito, nove…','Sequência: 8, 9, espaço vazio.'],
 ['Qual é o antecessor de 10?',['11','8','9','12'],2,'Muito bem! 9 vem imediatamente antes de 10.','Antecessor é o número anterior. Volte uma unidade a partir de 10.','Sequência: espaço vazio, 10, 11.'],
 ['Qual número fica entre 4 e 6?',['3','7','5','8'],2,'Você acertou! A sequência é 4, 5, 6.','Conte a partir de quatro e pare no seis. Qual número você falou no meio?','Sequência: 4, espaço vazio, 6.'],
 ['Qual sinal completa: 7 ___ 3?',['<','=','>','+'],2,'Muito bem! 7 é maior que 3. Usamos o sinal de maior: >.','Compare as quantidades. A abertura do sinal fica voltada para o maior número.','Cartões com 7 e 3.'],
 ['Arraste os números para colocá-los em ordem CRESCENTE.',['6','2','4'],null,'Excelente! A ordem crescente é 2, 4, 6.','Comece pelo menor número, depois coloque o do meio e termine com o maior.','Cartões com os números 6, 2 e 4.']
 ],
 [
 ['No número 23, qual algarismo está na casa das unidades?',['2','3','5','0'],1,'Isso mesmo! O 3 está na casa das unidades.','As unidades ficam na primeira posição da direita para a esquerda.','Quadro: dezenas, 2; unidades, 3.'],
 ['No número 41, qual algarismo está na casa das dezenas?',['1','0','5','4'],3,'Muito bem! O 4 está na casa das dezenas.','No quadro, procure a coluna das dezenas, à esquerda das unidades.','Quadro: dezenas, 4; unidades, 1.'],
 ['No número 35, quanto vale o algarismo 3?',['3','30','300','5'],1,'Você acertou! O 3 representa três dezenas, ou seja, 30.','Cada dezena vale 10. Pense em 10 + 10 + 10.','Quadro: dezenas, 3; unidades, 5.'],
 ['Se acrescentarmos 1 dezena ao número 20, qual será o resultado?',['21','10','30','200'],2,'Muito bem! Uma dezena vale 10, e 20 + 10 = 30.','Acrescentar uma dezena é somar 10, e não apenas 1.','20 + 10'],
 ['No número 102, qual algarismo está na casa das dezenas?',['1','2','3','0'],3,'Excelente! O zero ocupa a casa das dezenas em 102.','Observe a coluna do meio: ela fica entre centenas e unidades.','Quadro: centenas, 1; dezenas, 0; unidades, 2.']
 ]
];
extra.forEach((list,di)=>list.forEach(([prompt,options,answer,success,error,imageAlt],i)=>{const id=`d${di+1}-q${i+11}`;const q={id,type:'qt1',prompt,options,answer,success,error,imageAlt,difficulty:'easy',image:`assets/imagens/missao-1-novas/${id==='d1-q12'?id+'-corrigida':id}.png`};if(answer===null){q.type='at1';q.items=options;q.options=[];q.answer=['2','4','6'];}challenges[di].questions.push(q);}));
challenges[0].questions.splice(10, 5, ...require('./mission-1-challenge-1-final.cjs'));
challenges[1].questions.splice(10, 5, ...require('./mission-1-challenge-2-final.cjs'));
challenges[2].questions.splice(10, 5, ...require('./mission-1-challenge-3-final.cjs'));
const data={id:1,title:'Os números',grade:'3º ano do Ensino Fundamental',challenges};
fs.writeFileSync('mission-data.js','window.ORBITA_MISSION = '+JSON.stringify(data,null,2)+';\n');
console.log(challenges.map(c=>`${c.title}: ${c.questions.length} questões`).join('\n'));

