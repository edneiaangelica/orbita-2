from pathlib import Path
import re
p=Path('scripts/criar-vd-explica-m2-d1-geradas.py')
s=p.read_text(encoding='utf-8-sig')
s=s.replace("OUT=ROOT/'assets/videos/missao-2/desafio-1/vd-explica-m2-d1-imagens-geradas'","OUT=ROOT/'assets/videos/missao-2/desafio-2/vd-explica-m2-d2'").replace("TMP=ROOT/'tmp/vd-explica-m2-d1'","TMP=ROOT/'tmp/vd-explica-m2-d2'")
jobs="""JOBS=[
('intro',1,'Olá, crianças! Hoje vamos aprender a fazer continhas de subtração usando os dedos das nossas mãos! Vamos descobrir como é fácil?'),
('exemplo',2,'Vamos começar! Quanto é oito menos três? Primeiro, levantamos oito dedinhos. Agora vamos abaixar três dedos, porque estamos tirando três!'),
('sobraram',2,'Vamos contar os dedinhos que sobraram:'),
('conta5',2,'Um, dois, três, quatro, cinco!'),
('resultado5',2,'Muito bem! Oito menos três é igual a cinco!'),
('duvida',3,'Mas, professora, e quando o número é tão grande que não conseguimos mostrar tudo nos dedos?'),
('guardar',4,'Temos um truque especial! Guardamos o número maior na cabeça. Neste caso, o quinze!'),
('dedos7',4,'Agora mostramos o número menor nos dedos: sete dedinhos! Vamos contar para trás, começando do quinze. Cada número que falamos corresponde a um dedinho que abaixamos!'),
('conta8',4,'Quatorze, treze, doze, onze, dez, nove, oito!'),
('resultado8',4,'Contamos sete números para trás e chegamos ao oito! Então, quinze menos sete é igual a oito!'),
('fim',5,'Aprenderam? Guardamos o número maior na cabeça, mostramos o menor nos dedos e contamos para trás! Agora é sua vez de praticar! Até a próxima aula!')]
"""
s=re.sub(r'JOBS=\[.*?async def voices',jobs+'async def voices',s,flags=re.S)
s=s.replace("voice='pt-BR-AntonioNeural' if k=='duvida' else 'pt-BR-FranciscaNeural'","voice='pt-BR-FranciscaNeural'")
s=s.replace("(90-9-len(JOBS)*.35)","(90-2.5-len(JOBS)*.35)")
a=s.index(" if k=='resposta':",s.index('samples=bytearray()'));b=s.index(' source=TMP/',a)
s=s[:a]+""" if k=='sobraram':
  dur=2.5
  timeline.append(dict(kind='abaixa3',scene=2,text='Vamos abaixar três dedos.',start=offset,end=offset+dur,events=[]))
  samples+=bytes(round(dur*48000));offset+=dur
"""+s[b:]
a=s.index('@lru_cache(None)\ndef character_sprite');b=s.index('def wrap(',a)
s=s[:a]+'''NEWCHAR=Image.open(ROOT/'assets/imagens/missao-2/desafio-2/geradas/personagens.png').convert('RGB')
EXTRA=Image.open(ROOT/'assets/imagens/missao-2/desafio-2/geradas/maos-1-0.png').convert('RGB')
@lru_cache(None)
def sprite(kind,w,h):
 sheet=CHAR if kind=='teacher' else NEWCHAR
 idx={'teacher':0,'girl':0,'happy':1,'thumb':2}[kind]
 return sheet.crop((idx*sheet.width//3,0,(idx+1)*sheet.width//3,sheet.height)).resize((w,h),Image.Resampling.LANCZOS)
def person(im,kind,x,y,w=285,h=305):im.paste(sprite(kind,w,h),(x,y))
@lru_cache(None)
def hand_sprite(n,flip=False):
 if n>=2:
  idx={5:0,4:1,3:2,2:3}[n]
  pic=HANDS.crop((idx*HANDS.width//4,0,(idx+1)*HANDS.width//4,HANDS.height))
 else:
  idx=1-n
  # Match the wrist and palm scale of the other four poses.
  pic=EXTRA.crop((idx*EXTRA.width//2+155,0,idx*EXTRA.width//2+735,EXTRA.height))
 pic=pic.resize((260,347),Image.Resampling.LANCZOS)
 return pic.transpose(Image.Transpose.FLIP_LEFT_RIGHT) if flip else pic
TIPS={5:[(.14,.44),(.34,.10),(.58,.05),(.79,.10),(.95,.24)],4:[(.32,.11),(.52,.05),(.72,.10),(.92,.23)],3:[(.35,.11),(.55,.05),(.77,.10)],2:[(.32,.11),(.66,.06)],1:[(.36,.07)],0:[]}
def mark(d,x,y,n,index,value,flip=False):
 u,v=TIPS[n][index];xx=x+(1-u if flip else u)*260;yy=y+v*347
 d.ellipse((xx-24,yy-24,xx+24,yy+24),fill=GOLD,outline=TEAL,width=3);text(d,xx,yy,value,25)
def hands(im,left,right):
 im.paste(hand_sprite(left),(490,234));im.paste(hand_sprite(right,True),(900,234))
def nextfinger(n):return 0 if n in [5,1] else n-1
''' + s[b:]
a=s.index('def render(');b=s.index(" card(d,(25,620",a)
s=s[:a]+'''def render(sc,t):
 im=Image.new('RGB',(W,H),'#F0F7FC');d=ImageDraw.Draw(im);k=sc['kind'];scene=sc['scene']
 d.rectangle((0,0,W,9),fill=PURPLE);text(d,235,38,'MISSÃO 2 • DESAFIO 2',22,PURPLE);text(d,1095,38,f'CENA {scene} DE 5',20,TEAL)
 titles={1:'Vamos subtrair com os dedos!',2:'Levante oito. Abaixe três.',3:'E quando não cabe nas mãos?',4:'Guarde o 15 e conte para trás',5:'Agora é sua vez de praticar!'}
 text(d,640,96,titles[scene],38,PURPLE)
 if scene==1:
  person(im,'teacher',100,200,370,390)
  im.paste(hand_sprite(5),(625,240));im.paste(hand_sprite(5,True),(925,240))
  text(d,890,180,'Subtração até 20',47,TEAL)
 elif scene==3:
  person(im,'girl',140,205,370,390)
  text(d,870,285,'Só temos 10 dedos…',39)
  text(d,870,390,'Como mostrar o 15?',37,PURPLE)
 elif scene==5:
  person(im,'happy',80,225,340,355);person(im,'thumb',865,220,340,360)
  for j,line in enumerate(['Guarde na cabeça.','Mostre nos dedos.','Conte para trás!']):text(d,640,285+j*70,line,31,PURPLE if j==2 else NAVY)
  text(d,640,570,'Até a próxima aula!',34,TEAL)
 else:
  person(im,'teacher' if scene==2 else 'girl',55,285,285,300)
  if scene==4:
   card(d,(108,166,282,238),GOLD);text(d,195,202,'15',51);d.ellipse((187,248,202,263),fill=GOLD)
  left,right=(5,3) if scene==2 else (5,2)
  n=0;active=None
  if k=='abaixa3':
   n=min(3,int(t/.8));right=3-n
   if n<3 and t% .8 <.25:active=('right',right,nextfinger(right),n+1)
   elif n<3:right-=1
  if k in ['sobraram','conta5','resultado5']:right=0
  if k=='conta8':
   begun=[e for e in sc['events'] if t>=e['start']]
   n=len(begun)
   folded=sum(t>=e['start']+.25 for e in sc['events'])
   remaining=7-folded;left=min(5,remaining);right=max(0,remaining-5)
   if n>folded:
    side='right' if right else 'left';pose=right if right else left
    active=(side,pose,nextfinger(pose),15-n)
  if k=='resultado8':left=right=0;n=7
  hands(im,left,right)
  result='5' if k=='resultado5' else '8' if k=='resultado8' or k=='conta8' and n==7 else '?'
  text(d,820,176,('8 − 3 = ' if scene==2 else '15 − 7 = ')+result,66,TEAL)
  if active:
   side,pose,idx,value=active;mark(d,900 if side=='right' else 490,234,pose,idx,value,side=='right')
  if k in ['conta5','resultado5']:
   c=sum(t>=e['start'] for e in sc['events']) if k=='conta5' else 5
   for j in range(c):mark(d,490,234,5,j,j+1)
  if scene==2:text(d,820,602,'5 dedos levantados' if k in ['sobraram','conta5','resultado5'] else 'Tirar 3 é abaixar 3 dedos.',26,TEAL)
  else:
   text(d,815,602,'O 15 fica guardado. O primeiro número é 14.',25,TEAL)
   if k in ['conta8','resultado8']:
    text(d,822,360,15-n,65,PURPLE)
    text(d,822,421,f'{n} de 7',24)
''' + s[b:]
s=s.replace("checks=[('intro',3),('conta7',2),('duvida',2),('guardar',2),('conta15',3),('visual13',3.5)]","checks=[('intro',3),('abaixa3',1),('conta5',3),('duvida',2),('conta8',3),('fim',3)]")
s=s.replace("str(OUT/'vd-explica-m2-d1.mp4')","str(OUT/'vd-explica-m2-d2.mp4')")
s=s.replace(" if k=='pausa':caption='Guarde o 9. Levante 4 dedos. Conte a partir do 10.'\n if k=='visual13':caption='   '.join(str(j) for j in range(10,10+n))\n",'')
Path('scripts/criar-vd-explica-m2-d2.py').write_text(s,encoding='utf-8')
