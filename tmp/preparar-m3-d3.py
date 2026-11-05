from pathlib import Path
import re
s=Path('scripts/criar-vd-explica-m3-d2-continuo.py').read_text(encoding='utf-8-sig')
s=s.replace("OUT=ROOT/'assets/videos/missao-3/desafio-2/vd-explica-m3-d2-continuo'","OUT=ROOT/'assets/videos/missao-3/desafio-3/vd-explica-m3-d3'").replace("TMP=ROOT/'tmp/vd-explica-m3-d2-fluido'","TMP=ROOT/'tmp/vd-explica-m3-d3'")
jobs="""JOBS=[
('intro',1,'Olá, turma! Neste desafio, precisamos clicar em três números que, somados, deem exatamente dez. Vamos resolver este primeiro teste juntos?'),
('quatro',2,'Vou começar pelo quatro. Quanto falta para chegar a dez? Faltam seis! Vou procurar o seis no quadro.'),
('seis',3,'Quatro mais seis são dez! Mas atenção: escolhi apenas dois números, e o desafio pede três. Qual número posso acrescentar sem mudar o total?'),
('zero',4,'O zero! Somar zero não altera a quantidade. Então, quatro mais seis mais zero são dez. Agora, sim: escolhi três números!'),
('fim',5,'Agora é a vez de vocês! Observem os números, pensem nas possibilidades e confiram: escolheram três números? A soma deu dez?')]
"""
s=re.sub(r'JOBS=\[.*?async def voices',jobs+'async def voices',s,flags=re.S)
s=s.replace('dur=math.ceil((len(raw)/48000+.10)*FPS)/FPS',"dur=math.ceil((len(raw)/48000+(.1 if k!='seis' else 1.6))*FPS)/FPS")
a=s.index('FIXED=');b=s.index('def wrap(',a)
s=s[:a]+'''# Exact reference: blank cells remain blank, never become zeros.
GRID=[9,None,3,4,5,None,None,8,None,0,None,9,3,None,None,6,8,None,None,None,None,None,3,None,None]
CHOICES=[3,15,9]
assert [GRID[i] for i in CHOICES]==[4,6,0] and sum(GRID[i] for i in CHOICES)==10
POS=[(650+(i%5)*84,151+(i//5)*84) for i in range(25)]
def pointer(d,x,y):
 d.polygon([(x,y),(x+3,y+27),(x+11,y+20),(x+21,y+32),(x+27,y+27),(x+18,y+15),(x+30,y+12)],fill=NAVY,outline='white',width=2)
def board(d,selected,click=None):
 for i,(x,y) in enumerate(POS):
  d.rounded_rectangle((x,y,x+74,y+74),7,fill=GOLD if i in selected else 'white',outline=GREEN if len(selected)==3 and i in selected else BLUE,width=4)
  if GRID[i] is not None:text(d,x+37,y+37,GRID[i],46,NAVY)
 if click:
  idx,delta=click;x,y=POS[idx]
  if 0<=delta<.65:
   radius=12+delta*34
   d.ellipse((x+37-radius,y+37-radius,x+37+radius,y+37+radius),outline=PURPLE,width=3)
   pointer(d,x+43,y+40)
''' +s[b:]
a=s.index('def render(');b=s.index(' # Captions follow',a)
s=s[:a]+'''def render(sc,t):
 im=Image.new('RGB',(W,H),BG);d=ImageDraw.Draw(im);k=sc['kind'];scene=sc['scene']
 d.rectangle((0,0,W,8),fill=PURPLE);text(d,235,36,'MISSÃO 3 • DESAFIO 3',22,PURPLE);text(d,1110,36,f'CENA {scene} DE 5',20,TEAL)
 text(d,640,94,'Clique 10 — Desafio da soma',40,PURPLE)
 person(im,'teacher',55,215,340,355)
 text(d,275,174,'Escolha 3 números. Total: 10.',26,PURPLE)
 selected=set();click=None;equation='Escolha três números'
 if k=='quatro':
  when=cue(sc,'quatro',1)
  if t>=when:selected={3};click=(3,t-when)
  equation='4 + 6 = 10' if t>=cue(sc,'seis',3) else '4 + ? = 10' if selected else 'Por onde começar?'
 elif k=='seis':
  selected={3};when=cue(sc,'seis',.5)
  if t>=when:selected.add(15);click=(15,t-when)
  equation='4 + 6 = 10'
 elif k=='zero':
  selected={3,15};when=cue(sc,'zero',.1)
  if t>=when:selected.add(9);click=(9,t-when)
  equation='4 + 6 + 0 = 10' if len(selected)==3 else 'Qual número falta escolher?'
 if k=='fim':
  selected=set(CHOICES)
  for j,v in enumerate([4,6,0]):
   x=655+j*155;card(d,(x,275,x+105,390),GOLD,14);text(d,x+52,333,v,67,PURPLE)
   if j<2:text(d,x+130,333,'+',42,TEAL)
  text(d,860,450,'4 + 6 + 0 = 10',53,TEAL)
  text(d,860,520,'3 números escolhidos',29,PURPLE)
 else:
  board(d,selected,click)
  text(d,860,585,equation,34,TEAL)
 count=len(selected);total=sum(GRID[i] for i in selected)
 card(d,(45,550,550,610),'#DAFFF3' if count==3 else 'white')
 label=f'{count} de 3 números'
 if count==2 and total==10:label+=' — falta escolher mais 1!'
 if count==3:label+=' — Desafio resolvido!'
 text(d,297,580,label,23,TEAL if count==3 else PURPLE)
''' +s[b:]
s=s.replace("caption='Observe, complete e confira!' if k=='fim' else 'Confira a soma e os números de cada linha e coluna.'","caption='Qual número não muda o total? Pense um pouquinho!' if k=='seis' else 'Escolha três números e confira se a soma é dez.'")
s=re.sub(r'checks=\[.*?\]\ncontact=',"checks=[('intro',2),('quatro',2),('quatro',4),('seis',3),('zero',2),('fim',3)]\ncontact=",s)
s=s.replace("contact=Image.new('RGB',(1280,1800))","contact=Image.new('RGB',(1280,1080))").replace("str(OUT/'vd-explica-m3-d2.mp4')","str(OUT/'vd-explica-m3-d3.mp4')")
Path('scripts/criar-vd-explica-m3-d3.py').write_text(s,encoding='utf-8')
