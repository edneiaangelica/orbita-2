import asyncio,json,sys,math,subprocess,wave
from pathlib import Path
from functools import lru_cache
sys.path.insert(0,'C:/Users/USUARIO/Desktop/videos-educacionais/.deps')
import edge_tts,imageio_ffmpeg
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'assets/videos/missao-3/desafio-1/vd-explica-m3-d1'
TMP=ROOT/'tmp/vd-explica-m3-d1'
OUT.mkdir(parents=True,exist_ok=True);TMP.mkdir(parents=True,exist_ok=True)
JOBS=[
('intro',1,'Olá, crianças! Hoje temos um desafio matemático muito divertido: o Triângulo da Soma! Vocês estão preparados para testar sua inteligência?'),
('regras',2,'Observem este triângulo. Temos seis quadradinhos vazios e seis números aqui embaixo. A missão é arrastar cada número para um quadradinho, colocando todos eles no triângulo.'),
('cinco',2,'Mas atenção! A soma dos três números de cada lado precisa ser igual a cinco!'),
('duvida',3,'Então precisamos escolher os números com cuidado! Porque os três lados precisam dar cinco, não é?'),
('explica',3,'Isso mesmo! E todos os números precisam ser utilizados uma única vez. Vocês podem arrastar, testar e mudar os números de lugar até encontrar a solução!'),
('resolver',4,'Vamos lá! Pensem bem antes de escolher. Lembrem-se: cada lado precisa ter três números cuja soma seja cinco. Não se esqueçam de conferir os três lados!'),
('testar',4,'Vou começar a testar! Será que consigo encontrar a posição certa?'),
('fim',5,'Agora é a sua vez! Resolva o desafio e confira se a soma dos três lados é sempre cinco. Boa sorte, pequenos matemáticos!')]
async def voices():
 for k,s,words in JOBS:
  target=TMP/f'{k}.mp3'
  if target.exists() and target.with_suffix('.json').exists():continue
  events=[]
  voice='pt-BR-FranciscaNeural'
  speech=edge_tts.Communicate(words,voice,rate='-10%' if k.startswith('conta') else '+5%',pitch='+8Hz' if k in ['duvida','testar'] else '+0Hz',boundary='WordBoundary')
  with target.open('wb') as f:
   async for ch in speech.stream():
    if ch['type']=='audio':f.write(ch['data'])
    elif ch['type']=='WordBoundary':events.append({a:ch[a] for a in ('text','offset','duration')})
  target.with_suffix('.json').write_text(json.dumps(events,ensure_ascii=False),encoding='utf-8')
  print(k+' voz pronta',flush=True)
if '--voices' in sys.argv:asyncio.run(voices());sys.exit()
FF=imageio_ffmpeg.get_ffmpeg_exe();FPS=24;W=1280;H=720
# Reserve five seconds to think and four seconds for the visual answer.
raws={};evs={}
for k,s,words in JOBS:
 src=TMP/f'{k}.mp3';dst=TMP/f'{k}.wav'
 subprocess.run([FF,'-v','error','-y','-i',str(src),'-ar','24000','-ac','1',str(dst)],check=True)
 ev=json.loads(src.with_suffix('.json').read_text(encoding='utf-8'));start=ev[0]['offset']/1e7;end=(ev[-1]['offset']+ev[-1]['duration'])/1e7
 with wave.open(str(dst),'rb') as f:raw=f.readframes(f.getnframes())
 raws[k]=raw[round(start*24000)*2:round(end*24000)*2];evs[k]=[dict(text=e['text'],start=e['offset']/1e7-start) for e in ev]
speed=0.966
samples=bytearray();timeline=[];offset=0
for k,s,words in JOBS:
 source=TMP/f'{k}-trim.wav';dest=TMP/f'{k}-tempo.wav'
 with wave.open(str(source),'wb') as f:f.setparams((1,2,24000,0,'NONE',''));f.writeframes(raws[k])
 subprocess.run([FF,'-v','error','-y','-i',str(source),'-af',f'atempo={speed}',str(dest)],check=True)
 with wave.open(str(dest),'rb') as f:raw=f.readframes(f.getnframes())
 dur=math.ceil((len(raw)/48000+.35)*FPS)/FPS
 if k in ['intro','cinco','explica','testar','fim']:
  target={1:15,2:35,3:50,4:75,5:90}[s]
  dur=max(dur,target-offset)
 timeline.append(dict(kind=k,scene=s,text=words,start=offset,end=offset+dur,speech_end=len(raw)/48000+.12,events=[dict(text=e['text'],start=e['start']/speed+.12) for e in evs[k]]))
 block=bytes(5760)+raw;block+=bytes(round(dur*48000)-len(block));samples+=block;offset+=dur
with wave.open(str(TMP/'narracao.wav'),'wb') as f:f.setparams((1,2,24000,0,'NONE',''));f.writeframes(samples)
NAVY='#203252';PURPLE='#6941AC';TEAL='#087F85';GOLD='#FFD46B';SKIN='#F5B98F'
@lru_cache(None)
def font(n):return ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf',n)
def text(d,x,y,s,n=32,c=NAVY):d.text((x,y),str(s),font=font(n),fill=c,anchor='mm')
def card(d,xy,fill='white',r=24):d.rounded_rectangle(xy,r,fill)
CHAR=Image.open(ROOT/'assets/imagens/missao-2/desafio-1/geradas/personagens.png').convert('RGB')
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
POSITIONS=[(855,165),(760,325),(950,325),(665,485),(855,485),(1045,485)]
SIDES=[(0,1,3),(0,2,5),(3,4,5)]
VALUES=[1,1,1,1,3,3]
BANK=[(630+i*90,578) for i in range(6)]
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
def wrap(s,maxlen=83):
 lines=['']
 for w in s.split():
  if len(lines[-1])+len(w)>maxlen:lines.append(w)
  else:lines[-1]+=(' ' if lines[-1] else '')+w
 return lines
def render(sc,t):
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
 text(d,855,533,'NÚMEROS DISPONÍVEIS',18,TEAL)
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
 caption=' '.join(e['text'] for e in active)
 if t>sc['speech_end']+.3:
  caption='Observe os três lados. Cada um precisa somar 5.' if k!='testar' else 'Teste, confira os três lados e mude os números de lugar.'
 lines=wrap(caption,80)
 for j,line in enumerate(lines):text(d,640,646+j*31 if len(lines)>1 else 661,line,24,'white')
 d.rectangle((0,714,int(W*(sc['start']+t)/offset),719),fill=GOLD)
 return im
checks=[('intro',2),('regras',8),('cinco',3),('duvida',2),('explica',2),('resolver',3),('testar',4),('testar',10),('testar',12),('fim',3)]
contact=Image.new('RGB',(1280,1800))
for i,(k,t) in enumerate(checks):
 sc=next(s for s in timeline if s['kind']==k);pic=render(sc,t);pic.thumbnail((640,360));contact.paste(pic,(i%2*640,i//2*360))
contact.save(OUT/'revisao.jpg')
print(f'Duração {offset:.2f}s; fator de voz {speed:.3f}',flush=True)
(OUT/'timeline.json').write_text(json.dumps(timeline,ensure_ascii=False,indent=2),encoding='utf-8')
if '--preview' in sys.argv:sys.exit()
p=subprocess.Popen([FF,'-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s','1280x720','-r',str(FPS),'-i','-','-i',str(TMP/'narracao.wav'),'-c:v','libx264','-preset','fast','-crf','20','-threads','4','-pix_fmt','yuv420p','-af','loudnorm=I=-16:TP=-1.5:LRA=11','-c:a','aac','-b:a','160k','-movflags','+faststart',str(OUT/'vd-explica-m3-d1.mp4')],stdin=subprocess.PIPE)
for sc in timeline:
 for fr in range(round((sc['end']-sc['start'])*FPS)):p.stdin.write(render(sc,fr/FPS).tobytes())
 print(sc['kind']+' renderizada',flush=True)
p.stdin.close()
if p.wait():raise RuntimeError('Falha no vídeo')
def stamp(t):
 ms=round(t*1000);return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02}.{ms%1000:03}'
(OUT/'legendas.vtt').write_text('WEBVTT\n\n'+'\n\n'.join(f'{stamp(s["start"])} --> {stamp(s["end"])}\n{s["text"]}' for s in timeline if s['text']),encoding='utf-8')
render(timeline[0],2).save(OUT/'poster.jpg')
print('Vídeo concluído',flush=True)







