from pathlib import Path
import re
s=Path('scripts/criar-vd-explica-m2-d2-voz-1-25.py').read_text(encoding='utf-8-sig')
s=s.replace("OUT=ROOT/'assets/videos/missao-2/desafio-2/vd-explica-m2-d2-voz-1-25'","OUT=ROOT/'assets/videos/missao-2/desafio-3/vd-explica-d2-m3'").replace("TMP=ROOT/'tmp/vd-explica-m2-d2'","TMP=ROOT/'tmp/vd-explica-d2-m3'")
jobs="""JOBS=[
('intro',1,'Olá, crianças! Vocês sabem descobrir se um probleminha deve ser resolvido com adição ou subtração?'),
('adicao',2,'Usamos a adição quando queremos juntar quantidades, quando acrescentamos alguma coisa ou quando precisamos descobrir o total!'),
('macas',2,'Quatro maçãs mais três maçãs: estamos juntando!'),
('carros',2,'Ele tinha cinco carrinhos e ganhou mais dois: estamos acrescentando!'),
('total',2,'Se queremos descobrir quantos brinquedos há ao todo, também usamos a adição!'),
('duvida',3,'E quando precisamos tirar ou descobrir a diferença entre duas quantidades?'),
('subtracao',3,'Então podemos usar a subtração! Ela aparece quando retiramos, quando comparamos quantidades ou quando queremos descobrir quanto falta!'),
('balas',3,'Ela tinha oito balas e comeu três: estamos retirando!'),
('figurinhas',3,'Ele tem três figurinhas a mais que ela: estamos comparando!'),
('faltam',3,'Já temos sete e precisamos de dez. Quanto falta? Três! Também usamos a subtração!'),
('revisao',4,'Vamos lembrar: adição é juntar, acrescentar e descobrir o total. Subtração é retirar, comparar e descobrir quanto falta!'),
('entendi',4,'Agora entendi! Mas precisamos prestar bastante atenção no que o probleminha está perguntando!'),
('fim',4,'Isso mesmo! Leiam com atenção, descubram o que está acontecendo e só depois escolham a operação. Agora é a sua vez de praticar! Até a próxima aula!')]
"""
s=re.sub(r'JOBS=\[.*?async def voices',jobs+'async def voices',s,flags=re.S)
s=s.replace("pitch='+8Hz' if k=='duvida' else '+0Hz'","pitch='+8Hz' if k in ['duvida','entendi'] else '+0Hz'")
s=re.sub(r'speed=1.25\*sum.*?\n','speed=0.966\n',s)
a=s.index(" if k=='sobraram':",s.index('samples=bytearray()'));b=s.index(' source=TMP/',a);s=s[:a]+s[b:]
a=s.index("CHAR=Image.open");b=s.index('def wrap(',a)
s=s[:a]+'''ASSETS=ROOT/'assets/imagens/missao-2/desafio-3/geradas'
CHAR=Image.open(ROOT/'assets/imagens/missao-2/desafio-1/geradas/personagens.png').convert('RGB')
GIRL=Image.open(ROOT/'assets/imagens/missao-2/desafio-2/geradas/personagens.png').convert('RGB')
TEACHER=Image.open(ASSETS/'professora.png').convert('RGB')
OBJECTS=Image.open(ASSETS/'objetos.png').convert('RGBA')
@lru_cache(None)
def sprite(kind,w,h):
 if kind=='signs':pic=TEACHER.copy()
 else:
  sheet=GIRL if kind=='girl' else CHAR
  idx={'teacher':0,'boy':1,'happy':2,'girl':0}[kind]
  pic=sheet.crop((idx*sheet.width//3,0,(idx+1)*sheet.width//3,sheet.height))
 pic.thumbnail((w,h),Image.Resampling.LANCZOS)
 return pic

def person(im,kind,x,y,w=250,h=300):im.paste(sprite(kind,w,h),(x,y))
@lru_cache(None)
def obj(kind,size):
 idx={'apple':0,'car':1,'toy':2,'candy':3,'sticker':4,'basket':5}[kind]
 col,row=idx%3,idx//3
 pic=OBJECTS.crop((col*OBJECTS.width//3,row*OBJECTS.height//2,(col+1)*OBJECTS.width//3,(row+1)*OBJECTS.height//2))
 pic.thumbnail((size,size),Image.Resampling.LANCZOS)
 return pic

def item(im,kind,x,y,size=80,opacity=1):
 pic=obj(kind,size)
 if opacity<1:
  pic=pic.copy();pic.putalpha(pic.getchannel('A').point(lambda v:round(v*opacity)))
 im.paste(pic,(round(x),round(y)),pic)

def grid(im,kind,n,x,y,cols=5,size=76,gap=12):
 for j in range(n):item(im,kind,x+(j%cols)*(size+gap),y+(j//cols)*(size+gap),size)

def cue(sc,word,default):
 return next((e['start'] for e in sc['events'] if e['text'].lower().strip('.,!?')==word),default)

def ease(v):return max(0,min(1,v))**2*(3-2*max(0,min(1,v)))

def panels(d,mode):
 # Concept boards deliberately use complete ideas instead of isolated keyword cues.
 for x,color,title,lines in [(345,PURPLE,'ADIÇÃO',['Juntar quantidades','Acrescentar','Descobrir o total']),(790,TEAL,'SUBTRAÇÃO',['Retirar','Comparar quantidades','Descobrir quanto falta'])]:
  card(d,(x,205,x+405,515),'white')
  card(d,(x,205,x+405,280),color)
  text(d,x+202,244,title,32,'white')
  for j,line in enumerate(lines):text(d,x+202,330+j*65,line,25,color)
''' + s[b:]
a=s.index('def render(');b=s.index('checks=[',a)
s=s[:a]+'''def render(sc,t):
 im=Image.new('RGB',(W,H),'#F0F7FC');d=ImageDraw.Draw(im);k=sc['kind'];scene=sc['scene']
 d.rectangle((0,0,W,9),fill=PURPLE);text(d,235,38,'MISSÃO 2 • DESAFIO 3',22,PURPLE);text(d,1095,38,f'CENA {scene} DE 4',20,TEAL)
 titles={1:'Como descobrir a operação?',2:'As ideias da adição',3:'As ideias da subtração',4:'Vamos lembrar?'}
 text(d,640,96,titles[scene],39,PURPLE)
 duration=sc['end']-sc['start']
 if k=='intro':
  person(im,'signs',50,174,650,430)
  text(d,955,260,'Juntar ou tirar?',37,PURPLE)
  text(d,955,350,'O que acontece',30)
  text(d,955,395,'no probleminha?',30)
 elif k in ['adicao','subtracao']:
  addition=k=='adicao';person(im,'teacher',30,280,250,295)
  words=['JUNTAR','ACRESCENTAR','TOTAL'] if addition else ['RETIRAR','COMPARAR','QUANTO FALTA']
  icons=['apple','car','toy'] if addition else ['candy','sticker','toy']
  for j,(word,icon) in enumerate(zip(words,icons)):
   x=325+j*302;card(d,(x,220,x+280,540),'white')
   text(d,x+140,270,word,25,PURPLE if addition else TEAL)
   item(im,icon,x+65,315,150)
   text(d,x+140,505,'+' if addition else '−',45,PURPLE if addition else TEAL)
 elif k=='duvida':
  person(im,'boy',130,200,355,390)
  text(d,870,280,'Tirar?',45,PURPLE)
  text(d,870,390,'Descobrir a diferença?',35,TEAL)
 elif k in ['macas','carros','total','balas','figurinhas','faltam']:
  eq={'macas':'4 + 3 = 7','carros':'5 + 2 = 7','total':'6 + 4 = 10','balas':'8 − 3 = 5','figurinhas':'9 − 6 = 3','faltam':'10 − 7 = 3'}[k]
  idea={'macas':'JUNTAR','carros':'ACRESCENTAR','total':'DESCOBRIR O TOTAL','balas':'RETIRAR','figurinhas':'COMPARAR','faltam':'DESCOBRIR QUANTO FALTA'}[k]
  text(d,800,177,eq,61,TEAL)
  text(d,800,592,idea,27,PURPLE)
  person(im,'boy' if k in ['carros','figurinhas'] else 'girl' if k=='balas' else 'teacher',30,290,245,280)
  if k=='macas':
   # A visible basket holds four apples; three more move into its upper row.
   item(im,'basket',460,300,380)
   for j in range(4):item(im,'apple',485+j*72,430,72)
   f=ease((t-cue(sc,'três',1.7))/.85)
   for j in range(3):
    x=(920+j*85)*(1-f)+(520+j*80)*f;y=285*(1-f)+365*f
    item(im,'apple',x,y,76)
   text(d,1060,466,'+ 3',40,PURPLE)
  elif k=='carros':
   card(d,(335,260,1200,535),'white')
   grid(im,'car',5,365,292,cols=5,size=100,gap=50)
   f=ease((t-cue(sc,'ganhou',2))/.8)
   for j in range(2):item(im,'car',500+j*180,430+(1-f)*130,100,opacity=f)
   text(d,800,548,'5 carrinhos + 2 novos',27)
  elif k=='total':
   for x,n in [(350,6),(810,4)]:
    card(d,(x,275,x+370,545),'#E3D0B1');card(d,(x+12,286,x+358,524),'#FFF6E9')
    grid(im,'toy',n,x+35,300,cols=3,size=92,gap=18)
    text(d,x+185,555,f'{n} brinquedos',27)
   text(d,765,413,'+',45,PURPLE)
  elif k=='balas':
   grid(im,'candy',5,350,285,cols=5,size=98,gap=40)
   f=ease((t-cue(sc,'comeu',2))/.9)
   for j in range(3):item(im,'candy',500+j*165-(f*380),430-f*90,98,opacity=1-f)
   text(d,800,545,'3 balas comidas' if f>.95 else '8 balas',29)
  elif k=='figurinhas':
   # Six aligned pairs make the three unpaired stickers visually explicit.
   text(d,350,306,'Menino: 9',24,PURPLE);text(d,350,460,'Menina: 6',24,TEAL)
   for row,n in enumerate([9,6]):
    for j in range(n):
     x=455+j*80;y=255+row*155
     if row==0 and j>=6:card(d,(x-3,y-3,x+73,y+91),GOLD,9)
     item(im,'sticker',x,y,74)
   text(d,1020,505,'3 a mais',31,PURPLE)
  elif k=='faltam':
   card(d,(365,250,1195,550),'#E3D0B1');card(d,(380,263,1180,537),'#FFF6E9')
   for j in range(10):
    x=420+j%5*145;y=280+j//5*125
    if j<7:item(im,'toy',x,y,105)
    else:
     d.rounded_rectangle((x+8,y+4,x+98,y+105),12,outline=TEAL,width=3)
     text(d,x+53,y+55,'?',42,TEAL)
   text(d,800,560,'7 brinquedos + 3 espaços vazios',26)
 elif k in ['revisao','entendi','fim']:
  person(im,'happy' if k=='entendi' else 'teacher',30,280,270,300)
  panels(d,k)
  text(d,795,572,'Leia a pergunta antes de escolher a operação.',26,PURPLE)
 # Captions follow word timestamps and preserve punctuation from the script.
 card(d,(25,620,1255,705),NAVY,18)
 words=sc['text'].split();cursor=0;chunks=[];group=[]
 for e in sc['events']:
  count=len(e['text'].split());cap=' '.join(words[cursor:cursor+count]);cursor+=count
  if sum(len(v['text'])+1 for v in group)+len(cap)>100:
   chunks.append(group);group=[]
  group.append(dict(text=cap,start=e['start']))
 if group:chunks.append(group)
 active=next((c for c in reversed(chunks) if t>=c[0]['start']),chunks[0])
 lines=wrap(' '.join(e['text'] for e in active),80)
 for j,line in enumerate(lines):text(d,640,646+j*31 if len(lines)>1 else 661,line,24,'white')
 d.rectangle((0,714,int(W*(sc['start']+t)/offset),719),fill=GOLD)
 return im
''' + s[b:]
s=re.sub(r'checks=\[.*?\]\ncontact=',"checks=[('intro',2),('adicao',2),('macas',3),('carros',4),('total',2),('duvida',2),('subtracao',2),('balas',4),('figurinhas',2),('faltam',2),('revisao',2),('fim',2)]\ncontact=",s)
s=s.replace("contact=Image.new('RGB',(1280,1080))","contact=Image.new('RGB',(1280,2160))")
s=s.replace("str(OUT/'vd-explica-m2-d2.mp4')","str(OUT/'vd-explica-d2-m3.mp4')")
Path('scripts/criar-vd-explica-d2-m3.py').write_text(s,encoding='utf-8')
