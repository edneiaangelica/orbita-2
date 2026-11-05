from pathlib import Path
import re
s=Path('scripts/criar-vd-explica-m3-d1-resolvido.py').read_text(encoding='utf-8-sig')
s=s.replace("OUT=ROOT/'assets/videos/missao-3/desafio-1/vd-explica-m3-d1-resolvido'","OUT=ROOT/'assets/videos/missao-3/desafio-2/vd-explica-m3-d2'").replace("TMP=ROOT/'tmp/vd-explica-m3-d1'","TMP=ROOT/'tmp/vd-explica-m3-d2'")
jobs="""JOBS=[
('regras',1,'Olá, crianças! Vamos resolver o quadrado da soma! Vocês devem completar os espaços com números de zero a nove. A soma de cada linha, na horizontal, e de cada coluna, na vertical, deve ser igual a dez!'),
('atencao',1,'Mas atenção: não podemos repetir números na mesma linha ou coluna. E os números que já estão no quadro devem ficar onde estão. Vamos ver como uma colega resolve?'),
('zero',2,'Vou começar pela coluna que já tem dois números! Sete mais três é igual a dez. Então, qual número falta? Zero! Acrescentar zero não muda a quantidade.'),
('sete',3,'Agora, nesta linha, temos zero mais três. Para chegar a dez, faltam sete! Vou colocar o sete aqui.'),
('escolha',4,'Aqui já temos sete. Os dois espaços precisam somar três. Vou experimentar um e dois! Vou conferir se eles não repetem nenhum número na mesma linha ou coluna.'),
('seis',5,'Na coluna do meio, um mais três são quatro. Para chegar a dez, faltam seis!'),
('um',5,'Na última coluna, dois mais sete são nove. Falta um!'),
('conferir',6,'Todas as linhas e colunas somam dez! E nenhuma tem números repetidos. O um aparece duas vezes, mas em linhas e colunas diferentes. Assim pode!'),
('fim',7,'Isso mesmo! Comece pela linha ou coluna com mais números preenchidos. Complete, teste e confira. Agora é a sua vez!')]
"""
s=re.sub(r'JOBS=\[.*?async def voices',jobs+'async def voices',s,flags=re.S)
s=re.sub(r"rate='-10%'.*?boundary='WordBoundary'", "rate='+0%',pitch='+0Hz',boundary='WordBoundary'",s)
s=s.replace('speed=0.966','speed=1.25')
s=s.replace("if k in ['intro','cinco','explica','testar','parabens']:","if k in ['atencao','zero','sete','escolha','um','conferir','fim']:")
s=s.replace('target={1:15,2:35,3:50,4:75,5:90}[s]','target={1:25,2:43,3:57,4:77,5:98,6:113,7:123}[s]')
a=s.index("NAVY=");b=s.index('def wrap(',a)
s=s[:a]+'''NAVY='#203252';PURPLE='#A0006D';TEAL='#087F85';GOLD='#FFD166';GREEN='#06D6A0';BLUE='#4A8BDF';BG='#EFFAFD'
@lru_cache(None)
def font(n):return ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf',n)
def text(d,x,y,s,n=32,c=NAVY):d.text((x,y),str(s),font=font(n),fill=c,anchor='mm')
def card(d,xy,fill='white',r=20):d.rounded_rectangle(xy,r,fill)
CHAR=Image.open(ROOT/'assets/imagens/missao-2/desafio-1/geradas/personagens.png').convert('RGB')
GIRL=Image.open(ROOT/'assets/imagens/missao-2/desafio-2/geradas/personagens.png').convert('RGB')
@lru_cache(None)
def sprite(kind,w,h):
 sheet=CHAR if kind=='teacher' else GIRL;idx=0 if kind in ['teacher','girl'] else 1
 pic=sheet.crop((idx*sheet.width//3,0,(idx+1)*sheet.width//3,sheet.height));pic.thumbnail((w,h),Image.Resampling.LANCZOS);return pic

def person(im,kind,x,y,w=335,h=355):im.paste(sprite(kind,w,h),(x,y))
def cue(sc,word,default,last=False):
 times=[e['start'] for e in sc['events'] if e['text'].lower().strip('.,!?;:')==word]
 return (times[-1] if last else times[0]) if times else default
FIXED={0:7,4:3,6:3};SOLUTION=[7,1,2,0,3,7,3,6,1]
LINES=[[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8]]
assert all(sum(SOLUTION[i] for i in line)==10 and len({SOLUTION[i] for i in line})==3 for line in LINES)
assert all(SOLUTION[i]==v for i,v in FIXED.items())
POSITIONS=[(650+(i%3)*130,157+(i//3)*130) for i in range(9)]

def board(d,values,active=None,confirmed=None,pop=None,ones=False):
 confirmed=confirmed or []
 activecells=LINES[active] if active is not None else []
 greens={i for line in confirmed for i in LINES[line]}
 for i,(x,y) in enumerate(POSITIONS):
  fill=GOLD if i in activecells else '#DAFFF3' if i in greens else 'white'
  d.rounded_rectangle((x,y,x+116,y+116),9,fill=fill,outline=GREEN if i in greens else BLUE,width=4)
  if i in values:
   size=64
   if pop and pop[0]==i:size=round(64+10*max(0,1-pop[1]/.5))
   text(d,x+58,y+58,values[i],size,NAVY if i in FIXED else PURPLE)
  if ones and i in [1,8]:d.rounded_rectangle((x-5,y-5,x+121,y+121),12,outline=GOLD,width=5)
 for line in confirmed:
  x=1085;y=190+line*55
  d.ellipse((x-13,y-13,x+13,y+13),fill=GREEN)
  d.line((x-7,y,x-2,y+5,x+8,y-6),fill=NAVY,width=3)
  text(d,1160,y,('Linha ' if line<3 else 'Coluna ')+str(line%3+1),19)
''' +s[b:]
a=s.index('def render(');b=s.index(' # Captions follow',a)
s=s[:a]+'''def render(sc,t):
 im=Image.new('RGB',(W,H),BG);d=ImageDraw.Draw(im);k=sc['kind'];scene=sc['scene']
 d.rectangle((0,0,W,8),fill=PURPLE);text(d,235,36,'MISSÃO 3 • DESAFIO 2',22,PURPLE);text(d,1110,36,f'CENA {scene} DE 7',20,TEAL)
 text(d,640,94,'Quadrado da soma',43,PURPLE)
 person(im,'teacher' if scene in [1,7] else 'happy' if scene==6 else 'girl',55,215,340,355)
 if scene==7:person(im,'happy',405,325,185,205)
 labels={1:'Vamos conhecer as regras!',2:'Comece pelo que já sabe.',3:'Complete a linha do meio.',4:'Experimente e confira.',5:'Faltam só dois espaços!',6:'Muito bem! Tudo conferido.',7:'Agora é sua vez!'}
 text(d,260,175,labels[scene],25,PURPLE)
 values=FIXED.copy();active=None;confirmed=[];pop=None;equation='Cada linha e coluna: soma 10';ones=False
 if scene>=3:values[3]=0
 if scene>=4:values[5]=7
 if scene>=5:values.update({1:1,2:2})
 if scene>=6:values=dict(enumerate(SOLUTION))
 if scene==1:
  active=0 if int(t/2)%2==0 else 3
  equation='Use números de 0 a 9'
 elif k=='zero':
  active=3;when=cue(sc,'zero',6)
  if t>=when:values[3]=0;pop=(3,t-when);confirmed=[3];equation='7 + 0 + 3 = 10'
  else:equation='7 + □ + 3 = 10'
 elif k=='sete':
  active=1;when=cue(sc,'sete',4)
  if t>=when:values[5]=7;pop=(5,t-when);confirmed=[1];equation='0 + 3 + 7 = 10'
  else:equation='0 + 3 + □ = 10'
 elif k=='escolha':
  active=0;a=cue(sc,'um',5);b=cue(sc,'dois',6,last=True)
  if t>=a:values[1]=1;pop=(1,t-a)
  if t>=b:values[2]=2;pop=(2,t-b)
  if t>b+1:
   active=[0,4,5][int((t-b-1)/1.5)%3]
  equation='7 + 1 + 2 = 10' if 2 in values else '7 + □ + □ = 10'
  if 2 in values:confirmed=[0]
 elif k=='seis':
  active=4;when=cue(sc,'seis',4)
  if t>=when:values[7]=6;pop=(7,t-when);confirmed=[4];equation='1 + 3 + 6 = 10'
  else:equation='1 + 3 + □ = 10'
 elif k=='um':
  values[7]=6;active=5;when=cue(sc,'um',3,last=True)
  if t>=when:values[8]=1;pop=(8,t-when);confirmed=[5];equation='2 + 7 + 1 = 10'
  else:equation='2 + 7 + □ = 10'
 elif k=='conferir':
  n=min(6,int(t/2.0)+1);confirmed=list(range(n));active=min(5,n-1)
  equation=' + '.join(str(SOLUTION[i]) for i in LINES[active])+' = 10'
  ones=t>=cue(sc,'um',5)
 elif k=='fim':confirmed=list(range(6));equation='Observe, complete e confira!'
 board(d,values,active,confirmed,pop,ones)
 text(d,845,582,equation,33,PURPLE if k=='fim' else TEAL)
 card(d,(45,550,545,610),'white')
 text(d,295,580,'Sem repetir na mesma linha ou coluna.',22,NAVY)
''' + s[b:]
s=re.sub(r"caption='Muito bem!.*?\n", "caption='Observe, complete e confira!' if k=='fim' else 'Confira a soma e os números de cada linha e coluna.'\n",s)
s=re.sub(r'checks=\[.*?\]\ncontact=',"checks=[('regras',3),('atencao',3),('zero',9),('sete',7),('escolha',8),('seis',6),('um',5),('conferir',3),('conferir',12),('fim',4)]\ncontact=",s)
s=s.replace("str(OUT/'vd-explica-m3-d1.mp4')","str(OUT/'vd-explica-m3-d2.mp4')").replace('render(timeline[0],2)','render(timeline[0],2)')
Path('scripts/criar-vd-explica-m3-d2.py').write_text(s,encoding='utf-8')
