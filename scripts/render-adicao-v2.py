import sys,json,math,subprocess,wave
from pathlib import Path
from functools import lru_cache
sys.path.insert(0,'C:/Users/USUARIO/Desktop/videos-educacionais/.deps')
from PIL import Image,ImageDraw,ImageFont
import imageio_ffmpeg
ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'assets/videos/missao-2/desafio-1/adicao-ate-20-v2'
TMP=ROOT/'tmp/adicao-v2'
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
sheet=Image.open(ROOT/'assets/imagens/missao-2/desafio-1/ilustracoes.png').convert('RGB')
def panel(a,b):
    p=sheet.crop((a,130,b,sheet.height));p.thumbnail((320,405),Image.Resampling.LANCZOS);return p
boy=panel(0,550);think=panel(565,1107)
hands=Image.open(ROOT/'assets/imagens/missao-2/desafio-1/maos-4-3.png').convert('RGB').resize((800,400),Image.Resampling.LANCZOS)
sprite=Image.open(ROOT/'assets/imagens/missao-2/desafio-1/v2/poses.png').convert('RGB')
poses=[]
for row in range(2):
    for col in range(3):
        poses.append(sprite.crop((col*sprite.width//3,row*sprite.height//2,(col+1)*sprite.width//3,(row+1)*sprite.height//2)).resize((370,370),Image.Resampling.LANCZOS))
timeline=[];samples=bytearray();offset=0
jobs=json.loads((ROOT/'scripts/adicao-v2.json').read_text(encoding='utf-8'))
for kind,scene,words in jobs:
    src=ROOT/f'assets/sons/missao-2/desafio-1/v2/{kind}.mp3';wav=TMP/f'{kind}.wav'
    subprocess.run([FF,'-y','-v','error','-i',str(src),'-af',f'atempo={SPEECH_SPEED}','-ar','24000','-ac','1',str(wav)],check=True)
    with wave.open(str(wav),'rb') as f:raw=f.readframes(f.getnframes())
    ev=json.loads(src.with_suffix('.json').read_text(encoding='utf-8'))
    begin=ev[0]['offset']/1e7/SPEECH_SPEED;end=(ev[-1]['offset']+ev[-1]['duration'])/1e7/SPEECH_SPEED
    raw=raw[round(begin*24000)*2:round(end*24000)*2]
    lead=0 if kind=='resposta' else .15
    dur=len(raw)/48000;tail=0 if kind=='sua_vez' else .25
    length=math.ceil((lead+dur+tail)*FPS)/FPS
    events=[dict(text=e['text'],start=e['offset']/1e7/SPEECH_SPEED-begin+lead,end=(e['offset']+e['duration'])/1e7/SPEECH_SPEED-begin+lead) for e in ev]
    timeline.append(dict(kind=kind,scene=scene,text=words,start=offset,end=offset+length,events=events,lead=lead,duration=dur))
    prefix=bytes(round(lead*24000)*2)
    block=prefix+raw;block+=bytes(round(length*24000)*2-len(block));samples+=block;offset+=length
    if kind=='sua_vez':
        timeline.append(dict(kind='pausa',scene=9,text='',start=offset,end=offset+5,events=[],lead=0,duration=5))
        samples+=bytes(5*48000);offset+=5
with wave.open(str(TMP/'narracao.wav'),'wb') as f:f.setparams((1,2,24000,0,'NONE',''));f.writeframes(samples)
def count(sc,t):return sum(t>=e['start'] for e in sc['events'])
def equation(d,a,b,result='?',highlight=None,y=116):
    xs=[460,550,640,730,840];vals=[a,'+',b,'=',result]
    for i,(x,s) in enumerate(zip(xs,vals)):
        if i==highlight:box(d,(x-56,y-49,x+56,y+49),GOLD,20)
        txt(d,x,y,s,68,PURPLE if i!=4 else TEAL)
def child(im,value):
    im.paste(think,(70,196));d=ImageDraw.Draw(im)
    box(d,(105,151,291,237),GOLD,30);txt(d,198,194,value,60)
def render(sc,t):
    im=Image.new('RGB',(W,H),PALE);d=ImageDraw.Draw(im);k=sc['kind']
    d.rectangle((0,0,W,8),fill=PURPLE)
    txt(d,40,37,'MISSÃO 2  /  DESAFIO 1',22,PURPLE,'lm')
    txt(d,1240,37,f'{sc["scene"]} / 9',22,TEAL,'rm')
    if k=='abertura':
        im.paste(boy,(85,155+round(math.sin(t*2)*3)));d=ImageDraw.Draw(im)
        txt(d,835,215,'Adição até 20',66,PURPLE)
        txt(d,835,300,'Vamos fazer continhas de mais!',30)
        for j,s in enumerate(['4','+','3','8','+','5']):
            x=535+j*112;y=430+round(10*math.sin(t*2+j));badge(d,x,y,s,40)
    elif k in ['dedos','conta7']:
        n=count(sc,t) if k=='conta7' else 0
        equation(d,4,3,7 if n==7 else '?')
        # The two hands rise into their settled positions as they are mentioned.
        if k=='dedos':
            leftcue=next((e['start'] for e in sc['events'] if e['text'].lower().strip('.,')=='levantamos'),3)
            rightcue=next((e['start'] for e in sc['events'] if e['start']>leftcue and e['text'].lower().strip('.,')=='três'),leftcue+2)
            for j,when in enumerate([leftcue,rightcue]):
                reveal=max(0,min(1,(t-when)/.45))
                if reveal>0:
                    p=hands.crop((400*j,0,400*(j+1),400));im.paste(p,(240+j*400,180+round((1-reveal)*100)))
        else:im.paste(hands,(240,180))
        d=ImageDraw.Draw(im)
        for j,(x,y) in enumerate([(.11,.14),(.20,.08),(.28,.14),(.36,.27),(.68,.18),(.77,.08),(.86,.17)]):
            if j<n:badge(d,240+int(x*800),180+int(y*400),j+1,24)
    elif k=='desafio':
        equation(d,8,5)
        im.paste(poses[0],(205,195));im.paste(poses[0].transpose(Image.Transpose.FLIP_LEFT_RIGHT),(705,195));d=ImageDraw.Draw(im)
        txt(d,640,353,'?',90,PURPLE)
        txt(d,640,579,'E quando passa de 10?',29)
    elif k=='relembra':
        txt(d,640,120,'Como continuar a contagem',48,PURPLE)
        items=[('1','Guarde um número','8 na cabeça'),('2','Represente o outro\nnos dedos','5 dedos'),('3','Continue contando','9, 10, 11, 12, 13')]
        for j,(num,title,sub) in enumerate(items):
            x=50+j*415;box(d,(x,230,x+350,465),'white')
            badge(d,x+175,270,num,29)
            for z,line in enumerate(title.split('\n')):txt(d,x+175,330+z*32,line,27)
            txt(d,x+175,413,sub,27,TEAL)
            if j<2:txt(d,x+381,350,'→',46,TEAL)
        txt(d,640,535,'Não conte o 8 novamente. Comece pelo 9!',33,PURPLE)
    else:
        isquiz=k in ['sua_vez','pausa','resposta'];a,b=(9,4) if isquiz else (8,5)
        res=13 if k in ['resultado','resposta'] else '?'
        equation(d,a,b,res,0 if k=='oito' else 2 if k=='cinco' else None)
        child(im,a);d=ImageDraw.Draw(im)
        if k=='oito':
            txt(d,830,300,'Guarde o 8 na cabeça.',43,TEAL)
            txt(d,830,382,'Vamos acrescentar 5.',32)
        else:
            hx,hy=790,205
            if k=='conta5':
                n=count(sc,t);pose_index=0;current=-1
                for j,e in enumerate(sc['events']):
                    if t>=e['start']:
                        current=j
                        if t>=e['start']+.20:pose_index=j+1
                pic=poses[min(pose_index,5)]
                if current>=0:
                    delta=t-sc['events'][current]['start']-.20
                    if 0<=delta<.16:pic=Image.blend(poses[current],poses[current+1],delta/.16)
                im.paste(pic,(hx,hy));d=ImageDraw.Draw(im)
                tips=[(.16,.48),(.36,.15),(.51,.09),(.54,.14),(.70,.21)]
                if current>=0 and t<sc['events'][current]['start']+.20:
                    x,y=tips[current];badge(d,hx+int(x*370),hy+int(y*370),9+current,27)
                for j in range(n):badge(d,807+j*77,182,9+j,26)
                txt(d,570,330,8+n,84,TEAL);txt(d,570,406,'CONTAGEM',23)
            else:
                pose=5 if k=='resultado' else 1 if isquiz else 0
                im.paste(poses[pose],(hx,hy));d=ImageDraw.Draw(im)
                txt(d,565,330,'+4' if isquiz else '+5',68,TEAL)
                if k=='resultado':
                    for j in range(5):badge(d,807+j*77,182,9+j,26)
                if k=='pausa':
                    txt(d,570,430,'Sua vez!',31,PURPLE)
                    for j in range(5):
                        x=485+j*42;d.ellipse((x-10,490,x+10,510),fill=GOLD if t<5-j else '#C3DCE4')
                if k=='sua_vez':txt(d,570,435,'Quanto deu?',30,PURPLE)
                if k in ['resultado','resposta']:
                    txt(d,570,455,'Muito bem!',31,PURPLE)
                    if t<1.4:
                        for j in range(8):
                            angle=j*math.pi/4;rr=64+18*math.sin(t*4)
                            x=840+math.cos(angle)*rr;y=116+math.sin(angle)*rr
                            d.line((x-5,y,x+5,y),fill=GOLD,width=3);d.line((x,y-5,x,y+5),fill=GOLD,width=3)
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
    checks=[('abertura',2),('conta7',3),('desafio',3),('oito',2),('cinco',2),('conta5',.8),('conta5',2),('conta5',3.5),('resultado',.8),('relembra',2),('pausa',2),('resposta',1)]
    contact=Image.new('RGB',(1280,2160))
    for i,(k,t) in enumerate(checks):
        sc=next(s for s in timeline if s['kind']==k);pic=render(sc,t);pic.thumbnail((640,360));contact.paste(pic,((i%2)*640,(i//2)*360))
    contact.save(OUT/'revisao.jpg');print(f'Duração: {offset:.2f}s');sys.exit()
p=subprocess.Popen([FF,'-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s','1280x720','-r',str(FPS),'-i','-','-i',str(TMP/'narracao.wav'),'-c:v','libx264','-preset','fast','-crf','20','-threads','4','-pix_fmt','yuv420p','-af','loudnorm=I=-16:TP=-1.5:LRA=11','-ar','48000','-c:a','aac','-b:a','160k','-movflags','+faststart',str(OUT/'missao-2-desafio-1-adicao-ate-20-v2.mp4')],stdin=subprocess.PIPE)
for sc in timeline:
    for fr in range(round((sc['end']-sc['start'])*FPS)):p.stdin.write(render(sc,fr/FPS).tobytes())
    print(sc['kind']+' renderizada',flush=True)
p.stdin.close()
if p.wait():raise RuntimeError('Falha de renderização')
def stamp(t):
    ms=round(t*1000);return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02}.{ms%1000:03}'
(OUT/'legendas.vtt').write_text('WEBVTT\n\n'+'\n\n'.join(f'{stamp(s["start"])} --> {stamp(s["end"])}\n{s["text"]}' for s in timeline if s['text']),encoding='utf-8')
(OUT/'timeline.json').write_text(json.dumps({'duration':offset,'pauseSeconds':5,'scenes':timeline},ensure_ascii=False,indent=2),encoding='utf-8')
render(timeline[0],2).save(OUT/'poster.jpg')
print(f'Pronto: {offset:.2f} segundos',flush=True)
