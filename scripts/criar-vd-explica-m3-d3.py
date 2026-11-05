import asyncio,json,sys,math,subprocess,wave
from pathlib import Path
from functools import lru_cache
sys.path.insert(0,'C:/Users/USUARIO/Desktop/videos-educacionais/.deps')
import edge_tts,imageio_ffmpeg
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'assets/videos/missao-3/desafio-3/vd-explica-m3-d3'
TMP=ROOT/'tmp/vd-explica-m3-d3'
OUT.mkdir(parents=True,exist_ok=True);TMP.mkdir(parents=True,exist_ok=True)
JOBS=[
('intro',1,'Olá, turma! Neste desafio, precisamos clicar em três números que, somados, deem exatamente dez. Vamos resolver este primeiro teste juntos?'),
('quatro',2,'Vou começar pelo quatro. Quanto falta para chegar a dez? Faltam seis! Vou procurar o seis no quadro.'),
('seis',3,'Quatro mais seis são dez! Mas atenção: escolhi apenas dois números, e o desafio pede três. Qual número posso acrescentar sem mudar o total?'),
('zero',4,'O zero! Somar zero não altera a quantidade. Então, quatro mais seis mais zero são dez. Agora, sim: escolhi três números!'),
('fim',5,'Agora é a vez de vocês! Observem os números, pensem nas possibilidades e confiram: escolheram três números? A soma deu dez?')]
async def voices():
 for k,s,words in JOBS:
  target=TMP/f'{k}.mp3'
  if target.exists() and target.with_suffix('.json').exists():continue
  events=[]
  voice='pt-BR-FranciscaNeural'
  spoken=words.replace('Complete,','Compléte,')
  speech=edge_tts.Communicate(spoken,voice,rate='+0%',pitch='+0Hz',boundary='WordBoundary')
  with target.open('wb') as f:
   async for ch in speech.stream():
    if ch['type']=='audio':f.write(ch['data'])
    elif ch['type']=='WordBoundary':events.append({a:ch[a] for a in ('text','offset','duration')})
  target.with_suffix('.json').write_text(json.dumps(events,ensure_ascii=False),encoding='utf-8')
  print(k+' voz pronta',flush=True)
if '--voices' in sys.argv:asyncio.run(voices());sys.exit()
FF=imageio_ffmpeg.get_ffmpeg_exe();FPS=24;W=1280;H=720
# Short transitions only; the narration controls scene length.
raws={};evs={}
for k,s,words in JOBS:
 src=TMP/f'{k}.mp3';dst=TMP/f'{k}.wav'
 subprocess.run([FF,'-v','error','-y','-i',str(src),'-ar','24000','-ac','1',str(dst)],check=True)
 ev=json.loads(src.with_suffix('.json').read_text(encoding='utf-8'));start=ev[0]['offset']/1e7;end=(ev[-1]['offset']+ev[-1]['duration'])/1e7
 with wave.open(str(dst),'rb') as f:raw=f.readframes(f.getnframes())
 # Shorten only gaps between word boundaries, retaining 120 ms on each side.
 cuts=[]
 for previous,following in zip(ev,ev[1:]):
  left=(previous['offset']+previous['duration'])/1e7+.12
  right=following['offset']/1e7-.12
  if right>left+.04:cuts.append((round(left*24000),round(right*24000)))
 first=round(start*24000);last=round(end*24000);cursor=first;pieces=[]
 for a,b in cuts:
  assert first<=a<b<=last
  pieces.append(raw[cursor*2:a*2]);cursor=b
 pieces.append(raw[cursor*2:last*2]);raws[k]=b''.join(pieces)
 evs[k]=[]
 for e in ev:
  pos=round(e['offset']/1e7*24000)
  removed=sum(b-a for a,b in cuts if b<=pos)
  evs[k].append(dict(text=e['text'],start=(pos-first-removed)/24000))
 assert all(a['start']<b['start'] for a,b in zip(evs[k],evs[k][1:]))

speed=1.25
samples=bytearray();timeline=[];offset=0
for k,s,words in JOBS:
 source=TMP/f'{k}-trim.wav';dest=TMP/f'{k}-tempo.wav'
 with wave.open(str(source),'wb') as f:f.setparams((1,2,24000,0,'NONE',''));f.writeframes(raws[k])
 subprocess.run([FF,'-v','error','-y','-i',str(source),'-af',f'atempo={speed}',str(dest)],check=True)
 with wave.open(str(dest),'rb') as f:raw=f.readframes(f.getnframes())
 dur=math.ceil((len(raw)/48000+(.1 if k!='seis' else 1.6))*FPS)/FPS
 timeline.append(dict(kind=k,scene=s,text=words,start=offset,end=offset+dur,speech_end=len(raw)/48000+.03,events=[dict(text=e['text'],start=e['start']/speed+.03) for e in evs[k]]))
 block=bytes(1440)+raw;block+=bytes(round(dur*48000)-len(block));samples+=block;offset+=dur
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
# Exact reference: blank cells remain blank, never become zeros.
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
def wrap(s,maxlen=83):
 lines=['']
 for w in s.split():
  if len(lines[-1])+len(w)>maxlen:lines.append(w)
  else:lines[-1]+=(' ' if lines[-1] else '')+w
 return lines
def render(sc,t):
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
  caption='Qual número não muda o total? Pense um pouquinho!' if k=='seis' else 'Escolha três números e confira se a soma é dez.'
 lines=wrap(caption,80)
 for j,line in enumerate(lines):text(d,640,646+j*31 if len(lines)>1 else 661,line,24,'white')
 d.rectangle((0,714,int(W*(sc['start']+t)/offset),719),fill=GOLD)
 return im
checks=[('intro',2),('quatro',2),('quatro',4),('seis',3),('zero',2),('fim',3)]
contact=Image.new('RGB',(1280,1080))
for i,(k,t) in enumerate(checks):
 sc=next(s for s in timeline if s['kind']==k);pic=render(sc,t);pic.thumbnail((640,360));contact.paste(pic,(i%2*640,i//2*360))
contact.save(OUT/'revisao.jpg')
print(f'Duração {offset:.2f}s; fator de voz {speed:.3f}',flush=True)
(OUT/'timeline.json').write_text(json.dumps(timeline,ensure_ascii=False,indent=2),encoding='utf-8')
if '--preview' in sys.argv:sys.exit()
p=subprocess.Popen([FF,'-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s','1280x720','-r',str(FPS),'-i','-','-i',str(TMP/'narracao.wav'),'-c:v','libx264','-preset','fast','-crf','20','-threads','4','-pix_fmt','yuv420p','-af','loudnorm=I=-16:TP=-1.5:LRA=11','-c:a','aac','-b:a','160k','-movflags','+faststart',str(OUT/'vd-explica-m3-d3.mp4')],stdin=subprocess.PIPE)
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







