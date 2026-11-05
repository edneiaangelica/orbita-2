import json,re
from pathlib import Path
root=Path(__file__).resolve().parent.parent
source=Path('C:/Users/USUARIO/.codex/attachments/ae57732d-dcb9-4696-a298-8fa51883f5f7/Texto colado.txt').read_text(encoding='utf-8-sig')
sections=re.split(r'Desafio \d\s*[-–]',source)[1:]
answers=[[12,13,14,17,12,17,20,11,18,0],[7,8,10,8,10,8,7,7,6,2],[13,9,16,8,14,5,12,9,8,10]]
challenges=[]
for d,section in enumerate(sections,1):
 questions=[]
 for i,block in enumerate(re.split(r'(?:Questão\s+\d+|questao-\d+)',section)[1:],1):
  before=block.split('(feedback')[0]
  lines=[line.strip() for line in before.splitlines() if line.strip() and not line.strip().startswith(('(','GABARITO'))]
  prompt=lines[0];options=[re.sub(r'^[A-D]\)\s*','',line) for line in lines[1:] if re.match(r'^[A-D]\)',line)]
  success=re.search(r'feedback acerto:\s*“(.*?)”',block,re.S).group(1)
  error=re.search(r'feedback erro:\s*“(.*?)”',block,re.S).group(1)
  success=success.replace('16 árvores','16 cadernos');error=error.replace('sua quantidade diminui.','sua quantidade diminuiu.')
  if d==3 and i==3:error='PENSE NOVAMENTE! Ele comprou 7 cadernos e depois mais 9. Junte as duas compras para descobrir o total: 7 + 9.'
  if d==2 and i==5:error='OBSERVE COM ATENÇÃO! Retire as 4 unidades do número 14. Qual número fica depois dessa retirada?'
  q=dict(id=f'd{d}-q{i}',type='qt3' if options else 'input',prompt=prompt,answer=answers[d-1][i-1],success=success,error=error,difficulty='regular')
  if options:q['options']=options
  questions.append(q)
 titles=['Adição até resultado 20','Subtração até 20','Probleminhas até 20']
 videos=['vd-explica-m2-d1','vd-explica-m2-d2','vd-explica-d2-m3']
 challenges.append(dict(id=d,title=titles[d-1],video=f'assets/videos/missao-2/desafio-{d}/{videos[d-1]}.mp4',questions=questions))
extra=[
[
('Quanto é 9 + 8?',17,'BOA DESCOBERTA! 9 + 8 = 17: uma dezena e sete unidades.','EXPERIMENTE COMPLETAR 10! Use 1 das 8 unidades para transformar 9 em 10. Depois, acrescente as 7 que restaram.'),
('Quanto é 12 + 6?',18,'VOCÊ AVANÇOU! Somar 6 a 12 leva ao 18.','SIGA A CONTAGEM! Guarde o 12 e dê seis passos para a frente, contando um número por passo.'),
('Quanto é 7 + 7?',14,'BELO RACIOCÍNIO! Duas parcelas de 7 formam 14.','USE O DOBRO! Imagine dois grupos com sete objetos e conte quantos há nos dois grupos juntos.'),
('Qual número completa 8 + ___ = 20?',12,'DESAFIO VENCIDO! 8 + 12 completa 20.','BUSQUE A PARTE QUE FALTA! Do 8 até o 10 faltam 2; do 10 até o 20 faltam mais 10. Junte esses avanços.'),
('Qual adição tem resultado 19?',2,'VOCÊ CONFERIU DIREITINHO! 12 + 7 = 19.','COMPARE AS SOMAS! Calcule cada par de parcelas e procure o resultado que vem logo antes de 20.',['9 + 9','10 + 7','12 + 7','13 + 7'])
],
[
('Quanto é 18 − 6?',12,'BEM PENSADO! Ao tirar 6 de 18, ficam 12.','CONTE PARA TRÁS! Comece no 18 e volte seis unidades. Marque um dedo para cada passo.'),
('Quanto é 17 − 8?',9,'VOCÊ ENCONTROU! 17 − 8 = 9.','PASSE PELO 10! Tire primeiro 7 de 17. Ainda falta tirar mais 1 para completar a retirada de 8.'),
('Quanto é 19 − 4?',15,'CÁLCULO CERTO! Retirar 4 de 19 deixa 15.','SEPARE AS UNIDADES! Pense em 19 como 10 mais 9. Retire 4 das 9 unidades e mantenha a dezena.'),
('Qual número completa 16 − ___ = 10?',6,'VOCÊ DESCOBRIU A RETIRADA! 16 − 6 = 10.','INVESTIGUE A DIFERENÇA! Conte quanto precisamos retirar de 16 para chegar a 10.'),
('Qual subtração tem resultado 4?',1,'ÓTIMA COMPARAÇÃO! 13 − 9 deixa exatamente 4.','VERIFIQUE CADA OPÇÃO! Faça as retiradas e veja qual delas deixa quatro unidades.',['12 − 7','13 − 9','16 − 9','18 − 10'])
],
[
('Nina tem 7 lápis azuis e 6 lápis vermelhos. Quantos lápis ela tem ao todo?',13,'BOA CONTAGEM! Nina tem 13 lápis, porque 7 + 6 = 13.','JUNTE OS GRUPOS! Os lápis azuis e vermelhos fazem parte da mesma coleção. Some 7 e 6.'),
('Pedro tem 16 figurinhas e Ana tem 11. Quantas figurinhas Pedro tem a mais que Ana?',5,'COMPARAÇÃO CERTA! Pedro tem 5 figurinhas a mais: 16 − 11 = 5.','FORME PARES! Combine uma figurinha de Pedro com uma de Ana. A diferença é a quantidade que sobra da coleção de Pedro.'),
('Uma caixa deve guardar 20 peças. Já colocamos 14. Quantas peças faltam para completar a caixa?',6,'VOCÊ COMPLETOU A IDEIA! Faltam 6 peças, pois 20 − 14 = 6.','PROCURE O QUE FALTA! Conte os passos de 14 até 20 ou calcule 20 − 14.'),
('Havia 18 livros na estante. A turma pegou 7 para ler. Quantos livros ficaram na estante?',11,'LEITURA ATENTA! Ficaram 11 livros na estante: 18 − 7 = 11.','ACOMPANHE A RETIRADA! Os sete livros usados pela turma saíram da estante. Retire 7 do total de 18.'),
('Uma turma tinha 9 bolas e recebeu mais 8. Qual operação mostra quantas bolas ela tem agora?',3,'ESCOLHA CORRETA! A turma recebeu mais bolas; 9 + 8 = 17.','OBSERVE O QUE ACONTECEU! A quantidade de bolas aumentou com a chegada de oito novas. Escolha a operação que junta as duas quantidades.',['9 − 8 = 1','9 + 9 = 18','17 − 8 = 9','9 + 8 = 17'])
]]
for c,rows in zip(challenges,extra):
 for i,row in enumerate(rows,11):
  prompt,answer,success,error,*options=row
  q=dict(id=f'd{c["id"]}-q{i}',type='qt3' if options else 'input',prompt=prompt,answer=answer,success=success,error=error,difficulty='regular')
  if options:q['options']=options[0]
  c['questions'].append(q)
mission=dict(id=2,title='Adição e subtração até 20',grade='3º ano do Ensino Fundamental',challenges=challenges)
(root/'mission-2-data.js').write_text('window.ORBITA_MISSION_2 = '+json.dumps(mission,ensure_ascii=False,indent=2)+';\n',encoding='utf-8')
jobs=[]
for c in challenges:
 assert len(c['questions'])==15
 assert (root/c['video']).exists()
 for q in c['questions']:
  for field in ['prompt','success','error']:
   spoken=q[field].replace('−',' menos ').replace(' - ',' menos ').replace('+',' mais ').replace('=',' igual a ').replace('___','qual número')
   jobs.append(dict(id=q['id']+'-'+field,text=spoken))
(root/'scripts/audio-missao-2.json').write_text(json.dumps(jobs,ensure_ascii=False,indent=2),encoding='utf-8')
print('45 questões, 135 falas e 3 vídeos preparados.')
