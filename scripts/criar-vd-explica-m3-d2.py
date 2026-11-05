import asyncio,json,sys,math,subprocess,wave
from pathlib import Path
from functools import lru_cache
sys.path.insert(0,'C:/Users/USUARIO/Desktop/videos-educacionais/.deps')
import edge_tts,imageio_ffmpeg
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'assets/videos/missao-3/desafio-2/vd-explica-m3-d2'
TMP=ROOT/'tmp/vd-explica-m3-d2'
OUT.mkdir(parents=True,exist_ok=True);TMP.mkdir(parents=True,exist_ok=True)
JOBS=[
('regras',1,'Olá, crianças! Vamos resolver o quadrado da soma! Vocês devem completar os espaços com números de zero a nove. A soma de cada linha, na horizontal, e de cada coluna, na vertical, deve ser igual a dez!'),
('atencao',1,'Mas atenção: não podemos repetir números na mesma linha ou coluna. E os números que já estão no quadro devem ficar onde estão. Vamos ver como uma colega resolve?'),
('zero',2,'Vou começar pela coluna que já tem dois números! Sete mais três é igual a dez. Então, qual número falta? Zero! Acrescentar zero não muda a quantidade.'),
('sete',3,'Agora, nesta linha, temos zero mais três. Para chegar a dez, faltam sete! Vou colocar o sete aqui.'),
('escolha',4,'Aqui já temos sete. Os dois espaços precisam somar três. Vou experimentar um e dois! Vou conferir se eles não repetem nenhum número na mesma linha ou coluna.'),
('seis',5,'Na coluna do meio, um mais três são quatro. Para chegar a dez, faltam seis!'),
('um',5,'Na última coluna, dois mais sete são nove. Falta um!'),
('conferir',6,'Todas as linhas e colunas somam dez! E nenhuma tem números repetidos. O um aparece duas vezes, mas em linhas e colunas diferentes. Assim pode!'),
('fim',7,'Isso mesmo! Comece pela linha ou coluna com mais números preenchidos. Complete, teste e confira. Agora é a sua vez!')]
async def voices():
 for k,s,words in JOBS:
  target=TMP/f'{k}.mp3'
  if target.exists() and target.with_suffix('.json').exists():continue
  events=[]
  voice='pt-BR-FranciscaNeural'
  speech=edge_tts.Communicate(words,voice,rate='+0%',pitch='+0Hz',boundary='WordBoundary')
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
speed=1.25
samples=bytearray();timeline=[];offset=0
for k,s,words in JOBS:
 source=TMP/f'{k}-trim.wav';dest=TMP/f'{k}-tempo.wav'
 with wave.open(str(source),'wb') as f:f.setparams((1,2,24000,0,'NONE',''));f.writeframes(raws[k])
 subprocess.run([FF,'-v','error','-y','-i',str(source),'-af',f'atempo={speed}',str(dest)],check=True)
 with wave.open(str(dest),'rb') as f:raw=f.readframes(f.getnframes())
 dur=math.ceil((len(raw)/48000+.35)*FPS)/FPS
 if k in ['atencao','zero','sete','escolha','um','conferir','fim']:
  target={1:25,2:43,3:57,4:77,5:98,6:113,7:123}[s]
  dur=max(dur,target-offset)
 timeline.append(dict(kind=k,scene=s,text=words,start=offset,end=offset+dur,speech_end=len(raw)/48000+.12,events=[dict(text=e['text'],start=e['start']/speed+.12) for e in evs[k]]))
 block=bytes(5760)+raw;block+=bytes(round(dur*48000)-len(block));samples+=block;offset+=dur
with wave.open(str(TMP/'narracao.wav'),'wb') as f:f.setparams((1,2,24000,0,'NONE',''));f.writeframes(samples)
NAVY='#203252';PURPLE='#A0006D';TEAL='#087F85';GOLD='#FFD166';GREEN='#06D6A0';BLUE='#4A8BDF';BG='#EFFAFD'
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
def wrap(s,maxlen=83):
 lines=['']
 for w in s.split():
  if len(lines[-1])+len(w)>maxlen:lines.append(w)
  else:lines[-1]+=(' ' if lines[-1] else '')+w
 return lines
def render(sc,t):
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
  caption='Observe, complete e confira!' if k=='fim' else 'Confira a soma e os números de cada linha e coluna.'
 lines=wrap(caption,80)
 for j,line in enumerate(lines):text(d,640,646+j*31 if len(lines)>1 else 661,line,24,'white')
 d.rectangle((0,714,int(W*(sc['start']+t)/offset),719),fill=GOLD)
 return im
checks=[('regras',3),('atencao',3),('zero',9),('sete',7),('escolha',8),('seis',6),('um',5),('conferir',3),('conferir',12),('fim',4)]
contact=Image.new('RGB',(1280,1800))
for i,(k,t) in enumerate(checks):
 sc=next(s for s in timeline if s['kind']==k);pic=render(sc,t);pic.thumbnail((640,360));contact.paste(pic,(i%2*640,i//2*360))
contact.save(OUT/'revisao.jpg')
print(f'Duração {offset:.2f}s; fator de voz {speed:.3f}',flush=True)
(OUT/'timeline.json').write_text(json.dumps(timeline,ensure_ascii=False,indent=2),encoding='utf-8')
if '--preview' in sys.argv:sys.exit()
p=subprocess.Popen([FF,'-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s','1280x720','-r',str(FPS),'-i','-','-i',str(TMP/'narracao.wav'),'-c:v','libx264','-preset','fast','-crf','20','-threads','4','-pix_fmt','yuv420p','-af','loudnorm=I=-16:TP=-1.5:LRA=11','-c:a','aac','-b:a','160k','-movflags','+faststart',str(OUT/'vd-explica-m3-d2.mp4')],stdin=subprocess.PIPE)
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







