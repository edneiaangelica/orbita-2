import sys,json,math,subprocess,wave
from pathlib import Path
from functools import lru_cache
sys.path.insert(0,'C:/Users/USUARIO/Desktop/videos-educacionais/.deps')
from PIL import Image,ImageDraw,ImageFont
import imageio_ffmpeg
ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'assets/videos/missao-2/desafio-2/subtracao-ate-20-v2'
TMP=ROOT/'tmp/subtracao-v2'
OUT.mkdir(parents=True,exist_ok=True);TMP.mkdir(parents=True,exist_ok=True)
FF=imageio_ffmpeg.get_ffmpeg_exe();W,H,FPS=1280,720,24
SPEECH_SPEED=.78
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
jobs=json.loads((ROOT/'scripts/subtracao-v2.json').read_text(encoding='utf-8'))
for kind,scene,words in jobs:
    src=ROOT/f'assets/sons/missao-2/desafio-2/v2/{kind}.mp3';wav=TMP/f'{kind}.wav'
    subprocess.run([FF,'-y','-v','error','-i',str(src),'-af',f'atempo={SPEECH_SPEED}','-ar','24000','-ac','1',str(wav)],check=True)
    with wave.open(str(wav),'rb') as f:raw=f.readframes(f.getnframes())
    ev=json.loads(src.with_suffix('.json').read_text(encoding='utf-8'))
    begin=ev[0]['offset']/1e7/SPEECH_SPEED;end=(ev[-1]['offset']+ev[-1]['duration'])/1e7/SPEECH_SPEED
    raw=raw[round(begin*24000)*2:round(end*24000)*2]
    lead=0 if kind=='resposta_conta' else .15
    dur=len(raw)/48000;tail=0 if kind=='sua_vez' else .25
    length=math.ceil((lead+dur+tail)*FPS)/FPS
    events=[dict(text=e['text'],start=e['offset']/1e7/SPEECH_SPEED-begin+lead,end=(e['offset']+e['duration'])/1e7/SPEECH_SPEED-begin+lead) for e in ev]
    timeline.append(dict(kind=kind,scene=scene,text=words,start=offset,end=offset+length,events=events,lead=lead,duration=dur))
    prefix=bytes(round(lead*24000)*2)
    block=prefix+raw;block+=bytes(round(length*24000)*2-len(block));samples+=block;offset+=length
    if kind=='sua_vez':
        timeline.append(dict(kind='pausa',scene=10,text='',start=offset,end=offset+5,events=[],lead=0,duration=5))
        samples+=bytes(5*48000);offset+=5
with wave.open(str(TMP/'narracao.wav'),'wb') as f:f.setparams((1,2,24000,0,'NONE',''));f.writeframes(samples)
def count(sc,t):return sum(t>=e['start'] for e in sc['events'])
def equation(d,a,b,result='?',highlight=None,y=116):
    xs=[460,550,640,730,840];vals=[a,'−',b,'=',result]
    for i,(x,s) in enumerate(zip(xs,vals)):
        if i==highlight:box(d,(x-56,y-49,x+56,y+49),GOLD,20)
        txt(d,x,y,s,68,PURPLE if i!=4 else TEAL)
def child(im,value):
    im.paste(think,(70,196));d=ImageDraw.Draw(im)
    box(d,(105,151,291,237),GOLD,30);txt(d,198,194,value,60)
def animated_hand(im,sc,t,x,y,initial,values,mirror=False):
    n=min(len(values),count(sc,t));current=n-1;pose_index=initial
    for j,e in enumerate(sc['events']):
        if t>=e['start']+.20:pose_index=initial+j+1
    pic=poses[min(5,pose_index)]
    if current>=0:
        delta=t-sc['events'][current]['start']-.20
        if 0<=delta<.16:pic=Image.blend(poses[initial+current],poses[initial+current+1],delta/.16)
    if mirror:pic=pic.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    im.paste(pic,(x,y));d=ImageDraw.Draw(im)
    tips=[(.16,.48),(.36,.15),(.51,.09),(.54,.14),(.70,.21)]
    if current>=0 and t<sc['events'][current]['start']+.20:
        px,py=tips[initial+current]
        if mirror:px=1-px
        badge(d,x+int(px*370),y+int(py*370),values[current],27)
    for j in range(n):badge(d,x+45+j*83,y-26,values[j],25)
    return n
def sparkle(d,t,x=840,y=116):
    if t<1.4:
        for j in range(8):
            angle=j*math.pi/4;rr=64+18*math.sin(t*4)
            sx=x+math.cos(angle)*rr;sy=y+math.sin(angle)*rr
            d.line((sx-5,sy,sx+5,sy),fill=GOLD,width=3);d.line((sx,sy-5,sx,sy+5),fill=GOLD,width=3)
def render(sc,t):
    im=Image.new('RGB',(W,H),PALE);d=ImageDraw.Draw(im);k=sc['kind']
    d.rectangle((0,0,W,8),fill=PURPLE)
    txt(d,40,37,'MISSÃO 2  /  DESAFIO 2',22,PURPLE,'lm')
    txt(d,1240,37,f'{sc["scene"]} / 10',22,TEAL,'rm')
    if k=='abertura':
        im.paste(boy,(85,155+round(math.sin(t*2)*3)));d=ImageDraw.Draw(im)
        txt(d,835,215,'Subtração até 20',58,PURPLE)
        txt(d,835,300,'Vamos fazer continhas de menos!',29)
        for j,s in enumerate(['8','−','4','15','−','4']):
            x=535+j*112;y=430+round(10*math.sin(t*2+j));badge(d,x,y,s,40)
    elif k in ['dedos','retirar4','conferir','sobraram4','resultado4']:
        equation(d,8,4,4 if k=='resultado4' else '?')
        im.paste(poses[1],(200,210))
        if k=='retirar4':animated_hand(im,sc,t,710,210,1,[1,2,3,4],True)
        else:im.paste(poses[1 if k=='dedos' else 5].transpose(Image.Transpose.FLIP_LEFT_RIGHT),(710,210))
        d=ImageDraw.Draw(im)
        if k in ['dedos','retirar4']:
            txt(d,895,589,'Abaixamos quatro dedos',25,TEAL)
        else:txt(d,895,589,'Quatro dedos abaixados',25,TEAL)
        if k in ['sobraram4','resultado4']:
            n=4 if k=='resultado4' else count(sc,t)
            for j,(x,y) in enumerate([(.36,.15),(.51,.09),(.67,.15),(.79,.29)]):
                if j<n:badge(d,200+int(x*370),210+int(y*370),j+1,25)
            txt(d,385,589,'Sobraram quatro!' if k=='resultado4' else 'Vamos conferir!',26,PURPLE)
        if k=='resultado4':sparkle(d,t)
    elif k=='desafio':
        equation(d,15,4,'?',0)
        im.paste(boy,(85,180));d=ImageDraw.Draw(im)
        txt(d,820,290,'O primeiro número',39,PURPLE)
        txt(d,820,350,'é maior que 10?',39,PURPLE)
        txt(d,820,450,'Guarde na cabeça e conte para trás!',27,TEAL)
    elif k=='relembra':
        txt(d,640,100,'Como contar de trás para frente',44,PURPLE)
        box(d,(155,158,345,231),GOLD,29);txt(d,250,195,'15',49)
        d.ellipse((185,232,207,254),fill=GOLD);d.ellipse((170,256,182,268),fill=GOLD)
        txt(d,480,194,'→',45,TEAL);badge(d,610,195,'14',33)
        txt(d,900,194,'Primeiro número da contagem',26,TEAL)
        items=[('1','Guarde o primeiro\nnúmero'),('2','Mostre quanto retirar\nnos dedos'),('3','Conte para trás')]
        for j,(num,title) in enumerate(items):
            x=50+j*415;box(d,(x,295,x+350,490),'white')
            badge(d,x+175,333,num,26)
            for z,line in enumerate(title.split('\n')):txt(d,x+175,392+z*34,line,26)
            if j<2:txt(d,x+381,393,'→',46,TEAL)
        txt(d,640,548,'Não conte o 15 novamente. Comece pelo 14!',32,PURPLE)
    else:
        isquiz=k in ['sua_vez','pausa','resposta_conta','resposta'];a,b=(16,3) if isquiz else (15,4)
        result=11 if k=='resultado' else 13 if k=='resposta' else '?'
        equation(d,a,b,result,0 if k=='quinze' else 2 if k=='quatro' else None)
        child(im,a);d=ImageDraw.Draw(im)
        if k=='quinze':
            txt(d,830,300,'Guarde o 15 na cabeça.',42,TEAL)
            txt(d,830,382,'Vamos retirar 4.',32)
        elif k in ['conta4','resposta_conta']:
            values=[15,14,13] if isquiz else [14,13,12,11]
            n=animated_hand(im,sc,t,790,210,2 if isquiz else 1,values)
            d=ImageDraw.Draw(im);txt(d,570,330,a-n,84,TEAL);txt(d,570,406,'CONTAGEM',23)
            txt(d,570,473,f'{n} de {b} retiradas',25,PURPLE)
        else:
            pose=5 if k in ['resultado','resposta'] else 2 if isquiz else 1
            im.paste(poses[pose],(790,210));d=ImageDraw.Draw(im)
            txt(d,565,330,'−3' if isquiz else '−4',68,TEAL)
            if k=='pausa':
                txt(d,570,430,'Sua vez!',31,PURPLE)
                for j in range(5):
                    x=485+j*42;d.ellipse((x-10,490,x+10,510),fill=GOLD if t<5-j else '#C3DCE4')
            if k=='sua_vez':txt(d,570,435,'Quanto deu?',30,PURPLE)
            if k in ['resultado','resposta']:
                vals=[15,14,13] if isquiz else [14,13,12,11]
                for j,num in enumerate(vals):badge(d,835+j*83,184,num,25)
                txt(d,570,455,'Muito bem!',31,PURPLE);sparkle(d,t)
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
    checks=[('abertura',2),('retirar4',1.5),('retirar4',3),('sobraram4',2),('resultado4',1),('desafio',2),('quinze',2),('conta4',2),('resultado',1),('relembra',2),('pausa',2),('resposta_conta',1.5)]
    contact=Image.new('RGB',(1280,2160))
    for i,(k,t) in enumerate(checks):
        sc=next(s for s in timeline if s['kind']==k);pic=render(sc,t);pic.thumbnail((640,360));contact.paste(pic,((i%2)*640,(i//2)*360))
    contact.save(OUT/'revisao.jpg');print(f'Duração: {offset:.2f}s');sys.exit()
p=subprocess.Popen([FF,'-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s','1280x720','-r',str(FPS),'-i','-','-i',str(TMP/'narracao.wav'),'-c:v','libx264','-preset','fast','-crf','20','-threads','4','-pix_fmt','yuv420p','-af','loudnorm=I=-16:TP=-1.5:LRA=11','-ar','48000','-c:a','aac','-b:a','160k','-movflags','+faststart',str(OUT/'missao-2-desafio-2-subtracao-ate-20-v2.mp4')],stdin=subprocess.PIPE)
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
