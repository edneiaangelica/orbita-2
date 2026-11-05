import sys,json,math,subprocess,wave
from pathlib import Path
from functools import lru_cache
sys.path.insert(0,'C:/Users/USUARIO/Desktop/videos-educacionais/.deps')
from PIL import Image,ImageDraw,ImageFont
import imageio_ffmpeg
ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'assets/videos/missao-2/desafio-3/probleminhas'
TMP=ROOT/'tmp/problemas'
OUT.mkdir(parents=True,exist_ok=True);TMP.mkdir(parents=True,exist_ok=True)
FF=imageio_ffmpeg.get_ffmpeg_exe();W,H,FPS=1280,720,24
SPEECH_SPEED=.74
NAVY='#17264D';PURPLE='#723DAB';GOLD='#FFD166';TEAL='#007F87';PALE='#EFF9FC'
@lru_cache(None)
def font(n):return ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf',n)
def txt(d,x,y,s,n=40,c=NAVY,anchor='mm'):d.text((x,y),str(s),font=font(n),fill=c,anchor=anchor)
def box(d,xy,fill='white',radius=24):d.rounded_rectangle(xy,radius,fill)
def badge(d,x,y,s,r=26):
    d.ellipse((x-r,y-r,x+r,y+r),fill=GOLD,outline=TEAL,width=3);txt(d,x,y,s,26)
def wrap(s,n=75):
    lines=['']
    for word in s.split():
        if len(lines[-1])+len(word)+1>n:lines.append(word)
        else:lines[-1]+=(' ' if lines[-1] else '')+word
    return lines
sheet=Image.open(ROOT/'assets/imagens/missao-2/desafio-3/ilustracoes.png').convert('RGB')
def asset(bounds,size):
    p=sheet.crop(bounds);p.thumbnail(size,Image.Resampling.LANCZOS);return p
ana=asset((35,0,480,512),(210,330))
friend=asset((530,0,980,512),(210,330))
pedro=asset((1090,0,1450,512),(210,330))
brother=asset((80,525,460,1024),(165,225))
card=asset((590,550,925,975),(68,86))
car=asset((1030,620,1490,950),(88,63))
def cue(sc,word,fallback=1,last=False):
    matches=[e['start'] for e in sc['events'] if e['text'].lower().strip('.,!?:')==word]
    return matches[-1 if last else 0] if matches else fallback
def smooth(v):v=max(0,min(1,v));return v*v*(3-2*v)
def star(d,x,y,r=29,color=GOLD):
    pts=[]
    for j in range(10):
        a=-math.pi/2+j*math.pi/5;rr=r if j%2==0 else r*.45;pts.append((x+math.cos(a)*rr,y+math.sin(a)*rr))
    d.polygon(pts,fill=color)
def dot(d,x,y,highlight=False):
    d.ellipse((x-24,y-24,x+24,y+24),fill=GOLD if highlight else '#39ADB9',outline=PURPLE if highlight else TEAL,width=3)
def heading(d,title):txt(d,640,112,title,47,PURPLE)

source_jobs=json.loads((ROOT/'scripts/problemas.json').read_text(encoding='utf-8'))
speech_total=0
for kind,_,_ in source_jobs:
    ev=json.loads((ROOT/f'assets/sons/missao-2/desafio-3/{kind}.json').read_text(encoding='utf-8'))
    speech_total+=(ev[-1]['offset']+ev[-1]['duration']-ev[0]['offset'])/1e7
SPEECH_SPEED=speech_total/(100-len(source_jobs)*1.1)
timeline=[];samples=bytearray();offset=0
jobs=json.loads((ROOT/'scripts/problemas.json').read_text(encoding='utf-8'))
for kind,scene,words in jobs:
    src=ROOT/f'assets/sons/missao-2/desafio-3/{kind}.mp3';wav=TMP/f'{kind}.wav'
    subprocess.run([FF,'-y','-v','error','-i',str(src),'-af',f'atempo={SPEECH_SPEED}','-ar','24000','-ac','1',str(wav)],check=True)
    with wave.open(str(wav),'rb') as f:raw=f.readframes(f.getnframes())
    ev=json.loads(src.with_suffix('.json').read_text(encoding='utf-8'))
    begin=ev[0]['offset']/1e7/SPEECH_SPEED;end=(ev[-1]['offset']+ev[-1]['duration'])/1e7/SPEECH_SPEED
    raw=raw[round(begin*24000)*2:round(end*24000)*2]
    lead=.2
    dur=len(raw)/48000;tail=.9
    length=math.ceil((lead+dur+tail)*FPS)/FPS
    events=[dict(text=e['text'],start=e['offset']/1e7/SPEECH_SPEED-begin+lead,end=(e['offset']+e['duration'])/1e7/SPEECH_SPEED-begin+lead) for e in ev]
    timeline.append(dict(kind=kind,scene=scene,text=words,start=offset,end=offset+length,events=events,lead=lead,duration=dur))
    prefix=bytes(round(lead*24000)*2)
    block=prefix+raw;block+=bytes(round(length*24000)*2-len(block));samples+=block;offset+=length
    if kind=='sua_vez':
        timeline.append(dict(kind='pausa',scene=9,text='',start=offset,end=offset+5,events=[],lead=0,duration=5))
        samples+=bytes(5*48000);offset+=5
with wave.open(str(TMP/'narracao.wav'),'wb') as f:f.setparams((1,2,24000,0,'NONE',''));f.writeframes(samples)
def render(sc,t):
    im=Image.new('RGB',(W,H),PALE);d=ImageDraw.Draw(im);k=sc['kind']
    d.rectangle((0,0,W,8),fill=PURPLE)
    txt(d,40,37,'MISSÃO 2  /  DESAFIO 3',22,PURPLE,'lm');txt(d,1240,37,f'{sc["scene"]} / 10',22,TEAL,'rm')
    if k=='abertura':
        im.paste(ana,(90,235));d=ImageDraw.Draw(im)
        txt(d,815,178,'Probleminhas de',49,PURPLE);txt(d,815,244,'adição e subtração',49,PURPLE)
        for j,s in enumerate(['+','−']):badge(d,690+j*260,410+round(8*math.sin(t*2+j)),s,61)
        txt(d,820,535,'Qual operação usar?',33,TEAL)
    elif k=='somar':
        heading(d,'Juntar e acrescentar')
        p=smooth((t-cue(sc,'juntar',1.5))/1.5)
        for j in range(7):
            sx=275+(j%4)*92 if j<4 else 830+(j-4)*92
            ex=365+(j%4)*170;ey=320+(j//4)*100
            star(d,sx+(ex-sx)*p,330+(ey-330)*p,33)
        txt(d,640,205,'+',75,TEAL)
        box(d,(225,506,575,575),'white');box(d,(705,506,1055,575),'white')
        txt(d,400,540,'Juntar',35,TEAL);txt(d,880,540,'Acrescentar',35,TEAL)
    elif k in ['ana','adicao']:
        heading(d,'As figurinhas de Ana' if k=='ana' else 'Vamos descobrir o total!')
        im.paste(ana,(30,240));im.paste(friend,(1040,240));d=ImageDraw.Draw(im)
        txt(d,130,587,'Ana',25,TEAL);txt(d,1140,587,'Amiga',25,TEAL)
        join=smooth((t-cue(sc,'juntamos',2))/1.6) if k=='adicao' else 0
        gain=smooth((t-cue(sc,'ganhou',2))/1.4) if k=='ana' else 1
        for j in range(13):
            sx=310+(j%4)*85 if j<8 else 770+((j-8)%3)*85
            sy=245+(j//4)*117 if j<8 else 245+((j-8)//3)*117
            ex=337+(j%5)*112;ey=224+(j//5)*108
            x=sx+(ex-sx)*join;y=sy+(ey-sy)*join
            if j>=8 and k=='ana':
                if t<cue(sc,'ganhou',2):continue
                x=1075+(x-1075)*gain;y=370+(y-370)*gain
            im.paste(card,(round(x),round(y)))
        d=ImageDraw.Draw(im)
        if k=='ana':
            txt(d,470,198,'8 figurinhas',30,TEAL)
            if gain>0:txt(d,875,198,'+ 5 figurinhas',30,TEAL)
            txt(d,640,568,'Quantas figurinhas ao todo?',30,PURPLE)
        else:
            result=t>=cue(sc,'treze',sc['duration']-.5,last=True)
            if t<cue(sc,'juntamos',2):eq='A quantidade aumentou!'
            elif result:eq='8 + 5 = 13'
            else:eq='8 + 5 = ?'
            txt(d,640,564,eq,51 if '+' in eq else 31,TEAL)
    elif k=='subtrair':
        heading(d,'Retirar, descobrir o que sobrou ou comparar')
        split=cue(sc,'diferença',sc['duration']*.55)
        if t<split:
            p=smooth((t-cue(sc,'retirar',1))/1.5)
            for j in range(8):
                x=350+(j%4)*110;y=285+(j//4)*110
                if j>=5:x+=p*420;y+=p*55
                dot(d,x,y,j>=5)
            txt(d,190,320,'−',76,TEAL)
            txt(d,640,535,'Uma parte sai. Quanto sobra?',34,TEAL)
        else:
            txt(d,640,213,'Comparando duas quantidades',30,TEAL)
            for row,num in enumerate([5,3]):
                for j in range(num):dot(d,440+j*105,315+row*110,j>=3)
                txt(d,315,315+row*110,num,48,PURPLE)
            txt(d,640,535,'5 − 3 = 2  →  duas bolinhas a mais',33,TEAL)
    elif k in ['pedro','subtracao']:
        heading(d,'Os carrinhos de Pedro' if k=='pedro' else 'Vamos descobrir quanto sobrou!')
        im.paste(pedro,(65,230));im.paste(brother,(1050,175));d=ImageDraw.Draw(im)
        txt(d,160,587,'Pedro',25,TEAL);txt(d,1130,414,'Irmão',25,TEAL)
        p=smooth((t-cue(sc,'deu',2)) / 1.8) if k=='pedro' else 1
        for j in range(15):
            sx=310+(j%5)*104;sy=225+(j//5)*110
            if j>=11:
                z=j-11;ex=940+(z%2)*106;ey=433+(z//2)*82
                x=sx+(ex-sx)*p;y=sy+(ey-sy)*p
            else:x,y=sx,sy
            if (j>=11 and p>0) or (j<11 and k=='subtracao'):
                d=ImageDraw.Draw(im);box(d,(round(x)-5,round(y)-5,round(x)+93,round(y)+68),GOLD,13)
            im.paste(car,(round(x),round(y)))
        d=ImageDraw.Draw(im)
        if k=='pedro':txt(d,590,566,'15 carrinhos → deu 4',35,TEAL)
        else:
            result=t>=cue(sc,'onze',sc['duration']-.5,last=True)
            txt(d,590,566,'15 − 4 = 11' if result else '15 − 4 = ?',51,TEAL)
    elif k=='lembrar':
        heading(d,'Vamos lembrar?')
        for x,col in [(65,TEAL),(675,PURPLE)]:box(d,(x,205,x+540,570),'white')
        txt(d,335,257,'Adição (+)',43,TEAL);txt(d,945,257,'Subtração (−)',43,PURPLE)
        txt(d,335,330,'Juntar e acrescentar',31);txt(d,945,320,'Retirar e encontrar',30);txt(d,945,362,'a diferença',30)
        for j in range(3):im.paste(card,(220+j*83,398))
        for j in range(3):im.paste(car,(805+j*96,413))
        d=ImageDraw.Draw(im);txt(d,335,530,'8 + 5 = 13',39,TEAL);txt(d,945,530,'15 − 4 = 11',39,PURPLE)
    elif k=='dica':
        heading(d,'Entenda a história!')
        box(d,(100,195,1180,315),'white')
        txt(d,640,228,'Ana tinha 8 figurinhas e ganhou 5.',32)
        txt(d,640,278,'Quantas figurinhas ela tem agora?',32)
        x=160+min(1,t/max(1,sc['duration']-1))*960;y=267
        d.ellipse((x-34,y-34,x+34,y+34),outline=TEAL,width=6);d.line((x+25,y+25,x+54,y+54),fill=TEAL,width=9)
        for j,line in enumerate(['O que aconteceu?','O que eu sei?','O que preciso descobrir?']):
            box(d,(250,350+j*76,1030,411+j*76),'white');txt(d,640,380+j*76,line,31,PURPLE)
    elif k=='fim':
        txt(d,640,112,'Entenda a história e escolha a operação!',43,PURPLE)
        im.paste(ana,(170,215));im.paste(pedro,(890,215));d=ImageDraw.Draw(im)
        txt(d,640,280,'8 + 5 = 13',60,TEAL);txt(d,640,390,'15 − 4 = 11',60,PURPLE)
        txt(d,640,550,'Leia. Pense. Resolva!',35,TEAL)
    d.rectangle((0,610,1280,720),fill=NAVY)
    if k=='pausa':txt(d,640,657,'Pense e conte nos dedos…',29,'white')
    else:
        # Caption chunks follow the actual spoken word offsets.
        chunks=[];chunk=[];size=0
        words=sc['text'].split();cursor=0
        for e in sc['events']:
            num=len(e['text'].split());caption=' '.join(words[cursor:cursor+num]);cursor+=num
            entry=dict(e,text=caption)
            if size+len(caption)>116 and chunk:chunks.append(chunk);chunk=[];size=0
            chunk.append(entry);size+=len(caption)+1
        if chunk:chunks.append(chunk)
        active=next((c for c in reversed(chunks) if t>=c[0]['start']),chunks[0])
        for j,line in enumerate(wrap(' '.join(e['text'] for e in active))):txt(d,640,643+j*33,line,25,'white')
    d.rectangle((0,714,int(W*(sc['start']+t)/offset),720),fill=GOLD)
    return im
if '--preview' in sys.argv:
    checks=[('abertura',2),('somar',4),('ana',4),('adicao',6),('subtrair',2),('subtrair',-1),('pedro',2),('subtracao',-1),('lembrar',2),('dica',3),('fim',2),('adicao',-1)]
    contact=Image.new('RGB',(1280,2160))
    for i,(k,t) in enumerate(checks):
        sc=next(s for s in timeline if s['kind']==k);pic=render(sc,sc['end']-sc['start']-.3 if t<0 else t);pic.thumbnail((640,360));contact.paste(pic,((i%2)*640,(i//2)*360))
    contact.save(OUT/'revisao.jpg');print(f'Duração: {offset:.2f}s');sys.exit()
p=subprocess.Popen([FF,'-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s','1280x720','-r',str(FPS),'-i','-','-i',str(TMP/'narracao.wav'),'-c:v','libx264','-preset','fast','-crf','20','-threads','4','-pix_fmt','yuv420p','-af','loudnorm=I=-16:TP=-1.5:LRA=11','-ar','48000','-c:a','aac','-b:a','160k','-movflags','+faststart',str(OUT/'missao-2-desafio-3-probleminhas.mp4')],stdin=subprocess.PIPE)
for sc in timeline:
    for fr in range(round((sc['end']-sc['start'])*FPS)):p.stdin.write(render(sc,fr/FPS).tobytes())
    print(sc['kind']+' renderizada',flush=True)
p.stdin.close()
if p.wait():raise RuntimeError('Falha de renderização')
def stamp(t):
    ms=round(t*1000);return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02}.{ms%1000:03}'
(OUT/'legendas.vtt').write_text('WEBVTT\n\n'+'\n\n'.join(f'{stamp(s["start"])} --> {stamp(s["end"])}\n{s["text"]}' for s in timeline if s['text']),encoding='utf-8')
(OUT/'timeline.json').write_text(json.dumps({'duration':offset,'speechSpeed':SPEECH_SPEED,'scenes':timeline},ensure_ascii=False,indent=2),encoding='utf-8')
render(timeline[0],2).save(OUT/'poster.jpg')
print(f'Pronto: {offset:.2f} segundos',flush=True)
