from pathlib import Path
import re
s=Path('scripts/criar-vd-explica-d2-m3.py').read_text(encoding='utf-8-sig')
s=s.replace("OUT=ROOT/'assets/videos/missao-2/desafio-3/vd-explica-d2-m3'","OUT=ROOT/'assets/videos/missao-3/desafio-1/vd-explica-m3-d1'").replace("TMP=ROOT/'tmp/vd-explica-d2-m3'","TMP=ROOT/'tmp/vd-explica-m3-d1'")
jobs="""JOBS=[
('intro',1,'Olá, crianças! Hoje temos um desafio matemático muito divertido: o Triângulo da Soma! Vocês estão preparados para testar sua inteligência?'),
('regras',2,'Observem este triângulo. Temos seis quadradinhos vazios e seis números aqui embaixo. A missão é arrastar cada número para um quadradinho, colocando todos eles no triângulo.'),
('cinco',2,'Mas atenção! A soma dos três números de cada lado precisa ser igual a cinco!'),
('duvida',3,'Então precisamos escolher os números com cuidado! Porque os três lados precisam dar cinco, não é?'),
('explica',3,'Isso mesmo! E todos os números precisam ser utilizados uma única vez. Vocês podem arrastar, testar e mudar os números de lugar até encontrar a solução!'),
('resolver',4,'Vamos lá! Pensem bem antes de escolher. Lembrem-se: cada lado precisa ter três números cuja soma seja cinco. Não se esqueçam de conferir os três lados!'),
('testar',4,'Vou começar a testar! Será que consigo encontrar a posição certa?'),
('fim',5,'Agora é a sua vez! Resolva o desafio e confira se a soma dos três lados é sempre cinco. Boa sorte, pequenos matemáticos!')]
"""
s=re.sub(r'JOBS=\[.*?async def voices',jobs+'async def voices',s,flags=re.S)
s=s.replace("k in ['duvida','entendi']","k in ['duvida','testar']")
a=s.index(' hold=');b=s.index(' timeline.append',a)
s=s[:a]+''' dur=math.ceil((len(raw)/48000+.35)*FPS)/FPS
 if k in ['intro','cinco','explica','testar','fim']:
  target={1:15,2:35,3:50,4:75,5:90}[s]
  dur=max(dur,target-offset)
''' +s[b:]
s=s.replace("text=words,start=offset,end=offset+dur,events=", "text=words,start=offset,end=offset+dur,speech_end=len(raw)/48000+.12,events=")
a=s.index('ASSETS=');b=s.index('def wrap(',a)
s=s[:a]+'''CHAR=Image.open(ROOT/'assets/imagens/missao-2/desafio-1/geradas/personagens.png').convert('RGB')
@lru_cache(None)
def sprite(kind,w,h):
 idx={'teacher':0,'boy':1,'happy':2}[kind]
 pic=CHAR.crop((idx*CHAR.width//3,0,(idx+1)*CHAR.width//3,CHAR.height))
 pic.thumbnail((w,h),Image.Resampling.LANCZOS)
 return pic

def person(im,kind,x,y,w=280,h=320):im.paste(sprite(kind,w,h),(x,y))

def cue(sc,word,default):
 return next((e['start'] for e in sc['events'] if e['text'].lower().strip('.,!?')==word),default)

def ease(v):
 v=max(0,min(1,v));return v*v*(3-2*v)

# Matches the six positions in the supplied reference: apex, side midpoints,
# bottom-left, base midpoint, bottom-right. Each corner belongs to two sides.
POSITIONS=[(855,175),(720,325),(990,325),(585,475),(855,475),(1125,475)]
SIDES=[(0,1,3),(0,2,5),(3,4,5)]
VALUES=[1,1,1,1,3,3]
BANK=[(630+i*90,566) for i in range(6)]
assert all(len(side)==3 for side in SIDES)
assert sum(VALUES)==10
# Check that the supplied puzzle is feasible, without exposing the solution.
import itertools
assert any(all(sum(p[i] for i in side)==5 for side in SIDES) for p in itertools.permutations(VALUES))

def tile(d,xy,value=None,bank=False,active=False):
 x,y=xy;r=30 if bank else 35
 d.rounded_rectangle((x-r,y-r,x+r,y+r),8,fill=GOLD if active else 'white',outline=TEAL if bank else '#4D91E9',width=4)
 if value is not None:text(d,x,y,str(value),39,PURPLE)

def pointer(d,x,y):
 d.polygon([(x,y),(x+5,y+30),(x+14,y+22),(x+24,y+36),(x+31,y+31),(x+22,y+17),(x+34,y+14)],fill=NAVY,outline='white',width=2)

def triangle(d,filled,highlight=None):
 for j,side in enumerate(SIDES):
  a=POSITIONS[side[0]];b=POSITIONS[side[-1]]
  d.line((a,b),fill=GOLD if j==highlight else '#A90083',width=14 if j==highlight else 10)
 for idx,xy in enumerate(POSITIONS):tile(d,xy,filled.get(idx))

def drag(d,token,slot,progress):
 ax,ay=BANK[token];bx,by=POSITIONS[slot];f=ease(progress)
 x=ax+(bx-ax)*f;y=ay+(by-ay)*f
 tile(d,(x,y),VALUES[token],active=True);pointer(d,x+16,y+14)
''' +s[b:]
a=s.index('def render(');b=s.index(' # Captions follow',a)
s=s[:a]+'''def render(sc,t):
 im=Image.new('RGB',(W,H),'#F0F7FC');d=ImageDraw.Draw(im);k=sc['kind'];scene=sc['scene']
 d.rectangle((0,0,W,9),fill=PURPLE);text(d,235,38,'MISSÃO 3 • DESAFIO 1',22,PURPLE);text(d,1095,38,f'CENA {scene} DE 5',20,TEAL)
 text(d,640,96,'Triângulo da Soma',43,PURPLE)
 who='boy' if k in ['duvida','testar'] else 'teacher'
 person(im,who,60,225,320,340)
 text(d,230,175,'Vamos testar?' if k=='testar' else 'Sua vez!' if k=='fim' else 'Pense e experimente!',27,TEAL)
 filled={};used=set();moving=None;highlight=None
 if k in ['regras','cinco','resolver']:
  highlight=int(t/1.5)%3
 if k=='regras':
  begin=cue(sc,'arrastar',6)
  if begin<=t<begin+1.4:used={0};moving=(0,0,(t-begin)/1.4)
  elif t>=begin+1.4:filled={0:1};used={0}
 if k=='cinco':
  # Return the demonstration tile so every new attempt starts from six pieces.
  if t<1.2:used={0};moving=(0,0,1-t/1.2)
 if k=='testar':
  start=cue(sc,'testar',1)+.4
  for j in range(6):
   begin=start+j*1.15
   if t>=begin+1:filled[j]=VALUES[j];used.add(j)
   elif t>=begin:used.add(j);moving=(j,j,t-begin)
  if len(filled)==6:highlight=int((t-start-7)/1.5)%3
 triangle(d,filled,highlight)
 for j,pos in enumerate(BANK):
  if j not in used:tile(d,pos,VALUES[j],bank=True)
 if moving:drag(d,*moving)
 text(d,855,526,'NÚMEROS DISPONÍVEIS',18,TEAL)
 if k=='testar' and len(filled)==6:
  sums=[sum(filled[i] for i in side) for side in SIDES]
  card(d,(45,490,420,610),'white')
  text(d,232,513,'TENTATIVA — CONFIRA!',22,PURPLE)
  text(d,232,548,f'Lados: {sums[0]}, {sums[1]} e {sums[2]}',27)
  text(d,232,583,'Ainda não! Troque os números.',21,TEAL)
 else:
  card(d,(45,510,420,605),'white')
  text(d,232,537,'CADA LADO',21,PURPLE)
  text(d,232,576,'3 números = soma 5',29,TEAL)
 if k in ['regras','cinco','resolver'] and highlight is not None:
  # The highlighted line passes through exactly three square centers.
  side=SIDES[highlight]
  for idx in side:
   x,y=POSITIONS[idx];d.rounded_rectangle((x-40,y-40,x+40,y+40),10,outline=GOLD,width=4)
''' +s[b:]
s=s.replace("lines=wrap(' '.join(e['text'] for e in active),80)","caption=' '.join(e['text'] for e in active)\n if t>sc['speech_end']+.3:\n  caption='Observe os três lados. Cada um precisa somar 5.' if k!='testar' else 'Teste, confira os três lados e mude os números de lugar.'\n lines=wrap(caption,80)")
s=re.sub(r'checks=\[.*?\]\ncontact=',"checks=[('intro',2),('regras',8),('cinco',3),('duvida',2),('explica',2),('resolver',3),('testar',4),('testar',10),('testar',12),('fim',3)]\ncontact=",s)
s=s.replace("contact=Image.new('RGB',(1280,2160))","contact=Image.new('RGB',(1280,1800))")
s=s.replace("str(OUT/'vd-explica-d2-m3.mp4')","str(OUT/'vd-explica-m3-d1.mp4')")
Path('scripts/criar-vd-explica-m3-d1.py').write_text(s,encoding='utf-8')
