import asyncio,json,sys,math,subprocess,wave
from pathlib import Path
from functools import lru_cache
sys.path.insert(0,'C:/Users/USUARIO/Desktop/videos-educacionais/.deps')
import edge_tts,imageio_ffmpeg
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'assets/videos/missao-2/desafio-2/vd-explica-m2-d2-voz-1-25'
TMP=ROOT/'tmp/vd-explica-m2-d2'
OUT.mkdir(parents=True,exist_ok=True);TMP.mkdir(parents=True,exist_ok=True)
JOBS=[
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
async def voices():
 for k,s,words in JOBS:
  target=TMP/f'{k}.mp3'
  if target.exists() and target.with_suffix('.json').exists():continue
  events=[]
  voice='pt-BR-FranciscaNeural'
  speech=edge_tts.Communicate(words,voice,rate='-10%' if k.startswith('conta') else '+5%',pitch='+8Hz' if k=='duvida' else '+0Hz',boundary='WordBoundary')
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
speed=1.25*sum(len(r)/48000 for r in raws.values())/(90-2.5-len(JOBS)*.35)
samples=bytearray();timeline=[];offset=0
for k,s,words in JOBS:
 if k=='sobraram':
  dur=2.5
  timeline.append(dict(kind='abaixa3',scene=2,text='Vamos abaixar três dedos.',start=offset,end=offset+dur,events=[]))
  samples+=bytes(round(dur*48000));offset+=dur
 source=TMP/f'{k}-trim.wav';dest=TMP/f'{k}-tempo.wav'
 with wave.open(str(source),'wb') as f:f.setparams((1,2,24000,0,'NONE',''));f.writeframes(raws[k])
 subprocess.run([FF,'-v','error','-y','-i',str(source),'-af',f'atempo={speed}',str(dest)],check=True)
 with wave.open(str(dest),'rb') as f:raw=f.readframes(f.getnframes())
 dur=math.ceil((len(raw)/48000+.35)*FPS)/FPS
 timeline.append(dict(kind=k,scene=s,text=words,start=offset,end=offset+dur,events=[dict(text=e['text'],start=e['start']/speed+.12) for e in evs[k]]))
 block=bytes(5760)+raw;block+=bytes(round(dur*48000)-len(block));samples+=block;offset+=dur
with wave.open(str(TMP/'narracao.wav'),'wb') as f:f.setparams((1,2,24000,0,'NONE',''));f.writeframes(samples)
NAVY='#203252';PURPLE='#6941AC';TEAL='#087F85';GOLD='#FFD46B';SKIN='#F5B98F'
@lru_cache(None)
def font(n):return ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf',n)
def text(d,x,y,s,n=32,c=NAVY):d.text((x,y),str(s),font=font(n),fill=c,anchor='mm')
def card(d,xy,fill='white',r=24):d.rounded_rectangle(xy,r,fill)
CHAR=Image.open(ROOT/'assets/imagens/missao-2/desafio-1/geradas/personagens.png').convert('RGB')
HANDS=Image.open(ROOT/'assets/imagens/missao-2/desafio-1/geradas/maos.png').convert('RGB')
NEWCHAR=Image.open(ROOT/'assets/imagens/missao-2/desafio-2/geradas/personagens.png').convert('RGB')
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
def wrap(s,maxlen=83):
 lines=['']
 for w in s.split():
  if len(lines[-1])+len(w)>maxlen:lines.append(w)
  else:lines[-1]+=(' ' if lines[-1] else '')+w
 return lines
def render(sc,t):
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
 card(d,(25,620,1255,705),NAVY,18)
 caption=sc['text']
 if sc['events']:
  # Display short, word-timed caption groups.
  chunks=[];group=[]
  for e in sc['events']:
   if sum(len(v['text'])+1 for v in group)+len(e['text'])>94:chunks.append(group);group=[]
   group.append(e)
  if group:chunks.append(group)
  active=next((c for c in reversed(chunks) if t>=c[0]['start']),chunks[0]);caption=' '.join(e['text'] for e in active)
 lines=wrap(caption)
 for j,line in enumerate(lines):text(d,640,650+(j*30 if len(lines)>1 else 12),line,25,'white')
 d.rectangle((0,714,int(W*(sc['start']+t)/offset),719),fill=GOLD)
 return im
checks=[('intro',3),('abaixa3',1),('conta5',3),('duvida',2),('conta8',3),('fim',3)]
contact=Image.new('RGB',(1280,1080))
for i,(k,t) in enumerate(checks):
 sc=next(s for s in timeline if s['kind']==k);pic=render(sc,t);pic.thumbnail((640,360));contact.paste(pic,(i%2*640,i//2*360))
contact.save(OUT/'revisao.jpg')
print(f'Duração {offset:.2f}s; fator de voz {speed:.3f}',flush=True)
(OUT/'timeline.json').write_text(json.dumps(timeline,ensure_ascii=False,indent=2),encoding='utf-8')
if '--preview' in sys.argv:sys.exit()
p=subprocess.Popen([FF,'-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s','1280x720','-r',str(FPS),'-i','-','-i',str(TMP/'narracao.wav'),'-c:v','libx264','-preset','fast','-crf','20','-threads','4','-pix_fmt','yuv420p','-af','loudnorm=I=-16:TP=-1.5:LRA=11','-c:a','aac','-b:a','160k','-movflags','+faststart',str(OUT/'vd-explica-m2-d2.mp4')],stdin=subprocess.PIPE)
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




