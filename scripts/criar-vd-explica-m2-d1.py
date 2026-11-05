import asyncio,json,sys,math,subprocess,wave
from pathlib import Path
from functools import lru_cache
sys.path.insert(0,'C:/Users/USUARIO/Desktop/videos-educacionais/.deps')
import edge_tts,imageio_ffmpeg
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'assets/videos/missao-2/desafio-1/vd-explica-m2-d1'
TMP=ROOT/'tmp/vd-explica-m2-d1'
OUT.mkdir(parents=True,exist_ok=True);TMP.mkdir(parents=True,exist_ok=True)
JOBS=[
('intro',1,'Olá, crianças! Hoje vamos aprender a fazer adições usando os dedos das nossas mãos. Vamos lá?'),
('exemplo',2,'Quanto é quatro mais três? Levantamos quatro dedos de uma mão e três da outra. Agora contamos todos os dedos levantados!'),
('conta7',2,'Um, dois, três, quatro, cinco, seis, sete!'),
('resultado7',2,'Então, quatro mais três é igual a sete!'),
('duvida',3,'Mas, professora, e quando o resultado passa de dez? Não temos dedos suficientes!'),
('guardar',4,'Podemos guardar o maior número na cabeça e contar o outro nos dedos. Vamos guardar o oito!'),
('dedos7',4,'Agora levantamos sete dedos. O oito já está guardado! Começamos pelo próximo número e contamos um número para cada dedo.'),
('conta15',4,'Nove, dez, onze, doze, treze, quatorze, quinze!'),
('resultado15',4,'Contamos mais sete e chegamos ao quinze! Oito mais sete é igual a quinze!'),
('pergunta',5,'Você pode usar essa estratégia em outras adições também! Agora, quanto é nove mais quatro? Guarde o nove na cabeça, levante quatro dedos e conte a partir do próximo número!'),
('resposta',5,'Chegou ao treze? Muito bem!'),
('fim',5,'Agora vamos praticar!')]
async def voices():
 for k,s,words in JOBS:
  target=TMP/f'{k}.mp3'
  if target.exists() and target.with_suffix('.json').exists():continue
  events=[]
  voice='pt-BR-AntonioNeural' if k=='duvida' else 'pt-BR-FranciscaNeural'
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
speed=sum(len(r)/48000 for r in raws.values())/(90-9-len(JOBS)*.35)
samples=bytearray();timeline=[];offset=0
for k,s,words in JOBS:
 if k=='resposta':
  for kind,dur in [('pausa',5),('visual13',4)]:
   timeline.append(dict(kind=kind,scene=5,text='',start=offset,end=offset+dur,events=[]));samples+=bytes(round(dur*48000));offset+=dur
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
def person(d,x,y,teacher=True,mood='happy',scale=1):
 # Original vector characters with expressive faces and raised arms.
 def ell(a,fill):d.ellipse(tuple((x+v*scale if i%2==0 else y+v*scale) for i,v in enumerate(a)),fill=fill)
 def line(a,fill,width):d.line([(x+a[i]*scale,y+a[i+1]*scale) for i in range(0,len(a),2)],fill=fill,width=round(width*scale))
 ell((-77,-105,77,75) if teacher else (-63,-94,63,25),'#55352D');ell((-59,-84,59,51),SKIN)
 ell((-65,-104,55,-48),'#55352D');ell((-37,-27,-26,-14),NAVY);ell((25,-27,36,-14),NAVY)
 if mood=='doubt':line((-14,23,0,17,14,23),NAVY,3)
 else:
  ell((-22,7,22,33),'#A94A54');ell((-18,7,18,17),'white')
 if teacher:
  for a in [-47,12]:
   d.rounded_rectangle((x+a*scale,y-35*scale,x+(a+36)*scale,y-5*scale),8,outline=PURPLE,width=3)
  line((-10,-23,12,-23),PURPLE,3)
 d.polygon([(x-48*scale,y+55*scale),(x+48*scale,y+55*scale),(x+85*scale,y+220*scale),(x-85*scale,y+220*scale)],fill=PURPLE if teacher else TEAL)
 line((-44,82,-105,130,-130,60),SKIN,23);line((44,82,105,130,130,60),SKIN,23)
 ell((-145,35,-116,73),SKIN);ell((116,35,145,73),SKIN)
 text(d,x,y+150*scale,'+' if teacher else '8',round(45*scale),'white')
def hand(d,x,y,n,labels=None):
 # Four vertical fingers plus a side thumb; folded fingers are explicitly shown.
 card(d,(x+24,y+120,x+158,y+250),SKIN,36)
 tips=[]
 for i,length in enumerate([99,128,113,83]):
  xx=x+29+i*32
  if i<n:
   card(d,(xx,y+120-length,xx+27,y+154),SKIN,13);tips.append((xx+13,y+120-length+12))
  else:
   card(d,(xx,y+123,xx+27,y+174),'#E7A47D',12)
 if n==5:
  d.line((x+38,y+174,x-8,y+103),fill=SKIN,width=29);d.ellipse((x-23,y+87,x+7,y+117),fill=SKIN);tips.append((x-8,y+102))
 else:card(d,(x+1,y+174,x+74,y+205),'#E7A47D',15)
 card(d,(x+57,y+224,x+127,y+279),SKIN,10)
 if labels:
  for (xx,yy),v in zip(tips,labels):
   d.ellipse((xx-22,yy-25,xx+22,yy+19),fill=GOLD,outline=TEAL,width=3);text(d,xx,yy-3,v,23)
def wrap(s,maxlen=83):
 lines=['']
 for w in s.split():
  if len(lines[-1])+len(w)>maxlen:lines.append(w)
  else:lines[-1]+=(' ' if lines[-1] else '')+w
 return lines
def render(sc,t):
 im=Image.new('RGB',(W,H),'#F0F7FC');d=ImageDraw.Draw(im);k=sc['kind'];scene=sc['scene']
 d.rectangle((0,0,W,9),fill=PURPLE);text(d,235,38,'MISSÃO 2 • DESAFIO 1',22,PURPLE);text(d,1095,38,f'CENA {scene} DE 5',20,TEAL)
 titles={1:'Vamos somar com os dedos!',2:'Conte todos os dedos levantados',3:'E quando passa de dez?',4:'Guarde e continue a contagem',5:'Agora é sua vez!'}
 text(d,640,96,titles[scene],38,PURPLE)
 if scene==1:
  person(d,350,300,True,scale=1.1);hand(d,650,265,5);hand(d,930,265,5)
  text(d,860,190,'Adição até 20',52,TEAL)
 elif scene==3:
  person(d,350,300,False,'doubt',1.05);text(d,830,270,'Só temos 10 dedos…',44);text(d,830,380,'Como continuar?',42,PURPLE)
 else:
  quiz=scene==5;a,b=(9,4) if quiz else (8,7) if scene==4 else (4,3)
  n=sum(t>=e['start'] for e in sc['events']) if k in ['conta7','conta15'] else min(4,int(t)+1) if k=='visual13' else 0
  result=7 if k=='resultado7' or k=='conta7' and n>=7 else 15 if k=='resultado15' or k=='conta15' and n>=7 else 13 if k in ['resposta','fim'] or k=='visual13' and n==4 else '?'
  text(d,825,177,f'{a} + {b} = {result}',66,TEAL)
  person(d,200,330,scene==2,'happy',.80)
  if scene>=4:
   card(d,(116,160,285,233),GOLD);d.ellipse((183,242,201,260),fill=GOLD);text(d,200,197,a,51)
  if scene==2:
   labels=list(range(1,n+1)) if k=='conta7' else list(range(1,8)) if k=='resultado7' else []
   hand(d,560,300,4,labels[:4]);hand(d,905,300,3,labels[4:]);text(d,820,440,'+',48,PURPLE)
  elif quiz:
   labels=list(range(10,10+n)) if k=='visual13' else list(range(10,14)) if k in ['resposta','fim'] else []
   hand(d,840,300,4,labels)
   text(d,565,350,'9 na cabeça',29,PURPLE)
   text(d,565,403,'Comece pelo 10!',27)
   if k=='pausa':
    text(d,565,478,'Pense e conte…',27,TEAL)
    for j in range(5):d.ellipse((475+j*40,520,491+j*40,536),fill=GOLD if t<5-j else '#CEDDE8')
   if k=='fim':text(d,640,601,'Agora vamos praticar!!!',34,PURPLE)
  else:
   labels=list(range(9,9+n)) if k=='conta15' else list(range(9,16)) if k=='resultado15' else []
   hand(d,565,300,5,labels[:5]);hand(d,930,300,2,labels[5:]);text(d,825,440,'+',48,PURPLE)
   text(d,820,601,'O 8 está guardado. Comece pelo 9!',28)
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
 if k=='pausa':caption='Guarde o 9. Levante 4 dedos. Conte a partir do 10.'
 if k=='visual13':caption='   '.join(str(j) for j in range(10,10+n))
 lines=wrap(caption)
 for j,line in enumerate(lines):text(d,640,650+(j*30 if len(lines)>1 else 12),line,25,'white')
 d.rectangle((0,714,int(W*(sc['start']+t)/offset),719),fill=GOLD)
 return im
checks=[('intro',3),('conta7',2),('duvida',2),('guardar',2),('conta15',3),('visual13',3.5)]
contact=Image.new('RGB',(1280,1080))
for i,(k,t) in enumerate(checks):
 sc=next(s for s in timeline if s['kind']==k);pic=render(sc,t);pic.thumbnail((640,360));contact.paste(pic,(i%2*640,i//2*360))
contact.save(OUT/'revisao.jpg')
print(f'Duração {offset:.2f}s; fator de voz {speed:.3f}',flush=True)
(OUT/'timeline.json').write_text(json.dumps(timeline,ensure_ascii=False,indent=2),encoding='utf-8')
if '--preview' in sys.argv:sys.exit()
p=subprocess.Popen([FF,'-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s','1280x720','-r',str(FPS),'-i','-','-i',str(TMP/'narracao.wav'),'-c:v','libx264','-preset','fast','-crf','20','-threads','4','-pix_fmt','yuv420p','-af','loudnorm=I=-16:TP=-1.5:LRA=11','-c:a','aac','-b:a','160k','-movflags','+faststart',str(OUT/'vd-explica-m2-d1.mp4')],stdin=subprocess.PIPE)
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

