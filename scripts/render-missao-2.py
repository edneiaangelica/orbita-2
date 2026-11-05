import sys,json,math,subprocess,re,wave
from pathlib import Path
from functools import lru_cache
sys.path.insert(0,'C:/Users/USUARIO/Desktop/videos-educacionais/.deps')
from PIL import Image,ImageDraw,ImageFont
import imageio_ffmpeg
ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'assets/videos/missao-2/desafio-1/adicao-ate-20'
TMP=ROOT/'tmp/missao-2-desafio-1'
OUT.mkdir(parents=True,exist_ok=True);TMP.mkdir(parents=True,exist_ok=True)
FF=imageio_ffmpeg.get_ffmpeg_exe();W,H,FPS=1280,720,24
NAVY='#17264D';PURPLE='#723DAB';GOLD='#FFD166';TEAL='#007F87';PALE='#EFF9FC'
@lru_cache(None)
def font(n):return ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf',n)
def txt(d,x,y,s,n=40,c=NAVY,anchor='mm'):d.text((x,y),str(s),font=font(n),fill=c,anchor=anchor)
def box(d,xy,fill='white',radius=24,outline=None,width=2):d.rounded_rectangle(xy,radius,fill,outline,width)
def wrap(s,n=70):
    lines=['']
    for w in s.split():
        if len(lines[-1])+len(w)+1>n:lines.append(w)
        else:lines[-1]+=(' ' if lines[-1] else '')+w
    return lines
sheet=Image.open(ROOT/'assets/imagens/missao-2/desafio-1/ilustracoes.png').convert('RGB')
def panel(a,b):
    p=sheet.crop((a,130,b,sheet.height));p.thumbnail((360,440),Image.Resampling.LANCZOS);return p
boy=panel(0,550);think=panel(565,1107);hand=panel(1120,1672)
hands=Image.open(ROOT/'assets/imagens/missao-2/desafio-1/maos-4-3.png').convert('RGB')
hands.thumbnail((800,400),Image.Resampling.LANCZOS)
scenes=json.loads((ROOT/'scripts/missao-2-desafio-1.json').read_text(encoding='utf-8'))
timeline=[];samples=bytearray();offset=0
for i,(kind,words) in enumerate(scenes):
    src=ROOT/f'assets/sons/missao-2/desafio-1/{i:02}.mp3';wav=TMP/f'{i:02}.wav'
    subprocess.run([FF,'-y','-v','error','-i',str(src),'-ar','24000','-ac','1',str(wav)],check=True)
    with wave.open(str(wav),'rb') as f:raw=f.readframes(f.getnframes())
    dur=len(raw)/48000;length=math.ceil((dur+1.05)*FPS)/FPS
    events=json.loads(src.with_suffix('.json').read_text(encoding='utf-8'))
    timeline.append(dict(kind=kind,text=words,start=offset,end=offset+length,duration=dur,events=events))
    samples+=bytes(19200)+raw+bytes(round((length-dur-.4)*24000)*2)
    offset+=length
with wave.open(str(TMP/'narracao.wav'),'wb') as f:f.setparams((1,2,24000,0,'NONE',''));f.writeframes(samples)
def progress_count(sc,t,maximum):
    ev=sc['events']
    times=[x['offset']/1e7+.4 for x in ev]
    if len(times)!=maximum:times=[.4+j*sc['duration']/maximum for j in range(maximum)]
    return sum(t>=v for v in times)
def badge(d,x,y,value,active=True,r=26):
    d.ellipse((x-r,y-r,x+r,y+r),fill=GOLD if active else 'white',outline=TEAL,width=3)
    txt(d,x,y,value,27)
def render(sc,t):
    im=Image.new('RGB',(W,H),PALE);d=ImageDraw.Draw(im)
    d.rectangle((0,0,W,9),fill=PURPLE)
    txt(d,48,39,'MISSÃO 2  /  DESAFIO 1',22,PURPLE,'lm')
    txt(d,1232,39,'ADIÇÃO ATÉ 20',22,TEAL,'rm')
    k=sc['kind'];bob=int(3*math.sin(t*2))
    first=k in ['hands10','example','hands7','count7','easy']
    intro=k in ['intro','question','end','bye']
    if intro:
        im.paste(boy,(70,139+bob));d=ImageDraw.Draw(im)
        titles={'intro':('Vamos somar?','Adição até 20'),'question':('E quando passa de 10?','Vamos aprender outro jeito!'),'end':('Você conseguiu!','Guarde um número.\nConte o outro nos dedos.'),'bye':('Até a próxima aula!','Continue praticando!')}
        title,sub=titles[k];txt(d,840,220,title,43,PURPLE)
        for j,line in enumerate(sub.split('\n')):txt(d,840,305+j*54,line,34)
        if k=='intro':txt(d,840,420,'4 + 3       8 + 5',58,TEAL)
        if k=='end':txt(d,840,440,'8 + 5 = 13',65,TEAL)
    elif first:
        title='Até 10, podemos usar as duas mãos' if k=='hands10' else '4 + 3'+(' = 7' if k=='easy' or (k=='count7' and progress_count(sc,t,7)==7) else '')
        txt(d,640,116,title,42 if k=='hands10' else 64,PURPLE)
        if k=='hands10':
            im.paste(hand,(290,160));im.paste(hand.transpose(Image.Transpose.FLIP_LEFT_RIGHT),(705,160));d=ImageDraw.Draw(im)
            txt(d,640,370,'+',52,TEAL);txt(d,640,535,'5 + 5 = 10',37)
        else:
            im.paste(hands,((W-hands.width)//2,170));d=ImageDraw.Draw(im)
            n=progress_count(sc,t,7) if k=='count7' else (7 if k=='easy' else 0)
            tips=[(.11,.14),(.20,.08),(.28,.14),(.36,.27),(.68,.18),(.77,.08),(.86,.17)]
            for j,(px,py) in enumerate(tips):
                if j<n:badge(d,(W-hands.width)//2+int(px*hands.width),170+int(py*hands.height),j+1,True,23)
            for j in range(7):badge(d,424+j*72,548,j+1,j<n,25)
            txt(d,640,340,'+',48,TEAL)
    else:
        title={'strategy':'Guarde na cabeça + conte nos dedos','sum':'Vamos resolver: 8 + 5','head':'Guarde o 8 na cabeça','five':'Levante 5 dedos','ready':'Comece a contar depois do 8','count5':'Um dedo, mais uma unidade','result':'8 + 5 = 13','remember':'O 8 não é contado novamente','units':'Cada dedo acrescenta 1'}.get(k,'8 + 5')
        txt(d,640,112,title,44,PURPLE)
        im.paste(think,(100,181+bob));d=ImageDraw.Draw(im)
        box(d,(145,155,330,236),GOLD,30);txt(d,237,194,'8',62)
        if k=='head':
            txt(d,820,300,'O 8 fica guardado.',44,TEAL)
            txt(d,820,375,'A contagem começa no 9.',33)
        if k!='head':
            hx,hy=780,165;im.paste(hand,(hx,hy));d=ImageDraw.Draw(im)
            n=progress_count(sc,t,5) if k=='count5' else (5 if k=='result' else 0)
            # Positions correspond to thumb, index, middle, ring and little finger in the generated panel.
            coords=[(.12,.49),(.34,.20),(.54,.12),(.72,.21),(.88,.33)]
            for j,(x,y) in enumerate(coords):
                if j<n:badge(d,hx+int(x*hand.width),hy+int(y*hand.height),9+j,True,24)
            txt(d,640,290,'+',58,TEAL)
            txt(d,640,402,str(8+n) if n else '5',80,TEAL)
            if n:txt(d,640,465,'TOTAL',22,TEAL)
            if k in ['count5','result','ready','units']:
                for j in range(6):
                    x=460+j*123;d.line((460,554,1075,554),fill='#C3DCE4',width=5)
                for j in range(6):badge(d,460+j*123,554,8+j,j<=n,26)
            else:txt(d,930,560,'5 dedos = +5',30,TEAL)
        if k=='remember':box(d,(420,456,760,536),GOLD);txt(d,590,496,'Comece pelo 9!',31)
    # Short readable captions, split using speech word boundaries when available.
    lines=wrap(sc['text'],76);chunks=[lines[j:j+2] for j in range(0,len(lines),2)]
    part=min(len(chunks)-1,max(0,int((t-.4)/max(.1,sc['duration'])*len(chunks))))
    d.rectangle((0,610,1280,720),fill=NAVY)
    for j,line in enumerate(chunks[part]):txt(d,640,641+j*34,line,26,'white')
    d.rectangle((0,714,int(W*(sc['start']+t)/offset),720),fill=GOLD)
    return im
if '--preview' in sys.argv:
    thumbs=[]
    for n in [0,3,4,9,12,13,14,17]:
        sc=timeline[n];im=render(sc,(sc['end']-sc['start'])*.7);im.thumbnail((640,360));thumbs.append(im)
    contact=Image.new('RGB',(1280,1440))
    for j,im in enumerate(thumbs):contact.paste(im,((j%2)*640,(j//2)*360))
    contact.save(OUT/'revisao.jpg');sys.exit()
cmd=[FF,'-y','-v','error','-f','rawvideo','-vcodec','rawvideo','-pix_fmt','rgb24','-s','1280x720','-r',str(FPS),'-i','-','-i',str(TMP/'narracao.wav'),'-c:v','libx264','-preset','fast','-crf','20','-threads','4','-pix_fmt','yuv420p','-af','loudnorm=I=-16:TP=-1.5:LRA=11','-c:a','aac','-b:a','160k','-movflags','+faststart',str(OUT/'missao-2-desafio-1-adicao-ate-20.mp4')]
p=subprocess.Popen(cmd,stdin=subprocess.PIPE)
for sc in timeline:
    for frame in range(round((sc['end']-sc['start'])*FPS)):p.stdin.write(render(sc,frame/FPS).tobytes())
    print(sc['kind']+' renderizada',flush=True)
p.stdin.close()
if p.wait():raise RuntimeError('FFmpeg falhou')
def stamp(t):
    ms=round(t*1000);return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02}.{ms%1000:03}'
(OUT/'legendas.vtt').write_text('WEBVTT\n\n'+'\n\n'.join(f'{stamp(s["start"]+.4)} --> {stamp(s["end"]-.3)}\n{s["text"]}' for s in timeline),encoding='utf-8')
(OUT/'timeline.json').write_text(json.dumps({'duration':offset,'voice':'pt-BR-FranciscaNeural','scenes':timeline},ensure_ascii=False,indent=2),encoding='utf-8')
render(timeline[0],2).save(OUT/'poster.jpg')
print(f'Pronto: {offset:.2f} segundos',flush=True)
