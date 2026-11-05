import sys,json,math,subprocess,re,wave
from pathlib import Path
from functools import lru_cache
sys.path.insert(0,'C:/Users/USUARIO/Desktop/videos-educacionais/.deps')
from PIL import Image,ImageDraw,ImageFont
import imageio_ffmpeg
ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'assets/videos/missao-2/desafio-2/subtracao-ate-20'
TMP=ROOT/'tmp/missao-2-desafio-2'
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
scenes=json.loads((ROOT/'scripts/missao-2-desafio-2.json').read_text(encoding='utf-8'))
timeline=[];samples=bytearray();offset=0
for i,(kind,words) in enumerate(scenes):
    src=ROOT/f'assets/sons/missao-2/desafio-2/{kind}.mp3';wav=TMP/f'{i:02}.wav'
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
art=Image.open(ROOT/'assets/imagens/missao-2/desafio-2/maos-aberta-fechada.png').convert('RGB')
mid=art.width//2
opened=art.crop((0,0,mid,art.height)).resize((370,370),Image.Resampling.LANCZOS)
closed=art.crop((mid,0,art.width,art.height)).resize((370,370),Image.Resampling.LANCZOS)
right_open=opened.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
right_closed=closed.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
def cue(sc,word,default):
    return next((e['offset']/1e7+.4 for e in sc['events'] if e['text'].strip(',.!').lower()==word),default)
def render(sc,t):
    im=Image.new('RGB',(W,H),PALE);d=ImageDraw.Draw(im)
    d.rectangle((0,0,W,9),fill=PURPLE)
    txt(d,48,39,'MISSÃO 2  /  DESAFIO 2',22,PURPLE,'lm')
    txt(d,1232,39,'SUBTRAÇÃO ATÉ 20',22,TEAL,'rm')
    k=sc['kind'];bob=round(3*math.sin(t*2))
    if k in ['intro','question','end','bye']:
        im.paste(boy,(70,140+bob));d=ImageDraw.Draw(im)
        titles={'intro':('Vamos subtrair?','Subtração até 20'),'question':('E se o primeiro número','for maior que 10?'),'end':('Você conseguiu!','Guarde o primeiro número.\nConte de trás para frente.'),'bye':('Até a próxima aula!','Continue praticando!')}
        title,sub=titles[k];txt(d,840,220,title,43,PURPLE)
        for j,line in enumerate(sub.split('\n')):txt(d,840,305+j*54,line,32)
        if k=='intro':txt(d,840,420,'8 − 4      15 − 4',54,TEAL)
        if k=='end':txt(d,840,440,'15 − 4 = 11',60,TEAL)
    elif k in ['hands','example','eight','prepare_remove','count_remove','lower_now','prepare_remain','count_remain','left']:
        low=1 if k in ['prepare_remain','count_remain','left'] else max(0,min(1,(t-cue(sc,'baixamos',.6))/.75)) if k=='lower_now' else 0
        title='Vamos usar os dedos das mãos' if k=='hands' else '8 − 4 = 4' if k=='left' else '8 − 4 = ?'
        txt(d,640,112,title,45 if k=='hands' else 60,PURPLE)
        im.paste(opened,(190,180));im.paste(Image.blend(right_open,right_closed,low),(720,180));d=ImageDraw.Draw(im)
        if low>0:txt(d,900,565,'Dedos abaixados',27,PURPLE)
        else:txt(d,900,565,'Vamos baixar estes dedos',25,TEAL)
        txt(d,375,565,'Sobraram 4 dedos' if k=='left' else 'Dedos que ficam levantados',25,TEAL)
        tips=[(.31,.14),(.51,.08),(.67,.15),(.83,.29)]
        if k in ['count_remove','count_remain','left']:
            n=4 if k=='left' else progress_count(sc,t,4)
            for j,(x,y) in enumerate(tips):
                if j<n:
                    px=720+int(370*(1-x)) if k=='count_remove' else 190+int(370*x)
                    badge(d,px,180+int(370*y),j+1,True,23)
        if k=='eight':
            for j in range(8):badge(d,465+j*50,160,j+1,True,20)
    else:
        titles={'strategy':'Guarde na cabeça. Conte para trás.','sum':'Vamos resolver: 15 − 4','head':'Guarde o 15 na cabeça','four':'Levante 4 dedos para retirar 4','ready':'Volte um número para cada dedo','start':'Vamos começar pelo 14!','count':'Um dedo, uma unidade a menos','result':'15 − 4 = 11','remember':'O 15 não é contado novamente','units':'Cada dedo representa uma retirada','back':'Conte de trás para frente!'}
        txt(d,640,110,titles[k],42,PURPLE)
        im.paste(think,(80,174+bob));d=ImageDraw.Draw(im)
        box(d,(124,153,316,235),GOLD,28);txt(d,220,194,'15',60)
        if k=='head':
            txt(d,830,300,'O 15 fica guardado.',43,TEAL)
            txt(d,830,378,'O próximo número é 14.',33)
        else:
            hx,hy=800,170
            im.paste(opened,(hx,hy));d=ImageDraw.Draw(im)
            n=progress_count(sc,t,4) if k=='count' else 4 if k in ['result','back'] else 0
            for j,(x,y) in enumerate([(.31,.14),(.51,.08),(.67,.15),(.83,.29)]):
                if j<n:badge(d,hx+int(370*x),hy+int(370*y),14-j,True,25)
            if k in ['count','result','back']:
                txt(d,625,280,'RESTAM',24,TEAL);txt(d,625,360,15-n,82,TEAL)
                txt(d,625,438,f'{n} de 4 retiradas',25)
            else:
                txt(d,625,285,'RETIRAR',24,TEAL);txt(d,625,365,'4',82,TEAL)
            if k=='remember':
                box(d,(430,478,765,548),GOLD);txt(d,597,513,'Comece pelo 14!',29)
            else:
                # Standard number line: decreasing values move to the left.
                d.line((465,563,1135,563),fill='#C3DCE4',width=5)
                for j in range(5):
                    x=1135-j*167
                    badge(d,x,563,15-j,j<=n,25)
                    if j>0 and j<=n:
                        ax=x+84;d.line((ax+24,548,ax-24,548),fill=TEAL,width=3)
                        d.polygon([(ax-24,548),(ax-12,540),(ax-12,556)],fill=TEAL)
    lines=wrap(sc['text'],76);chunks=[lines[j:j+2] for j in range(0,len(lines),2)]
    part=min(len(chunks)-1,max(0,int((t-.4)/max(.1,sc['duration'])*len(chunks))))
    d.rectangle((0,610,1280,720),fill=NAVY)
    for j,line in enumerate(chunks[part]):txt(d,640,641+j*34,line,26,'white')
    d.rectangle((0,714,int(W*(sc['start']+t)/offset),720),fill=GOLD)
    return im

if '--preview' in sys.argv:
    thumbs=[]
    for n in [3,5,6,8,9,13,17,18]:
        sc=timeline[n];im=render(sc,(sc['end']-sc['start'])*.7);im.thumbnail((640,360));thumbs.append(im)
    contact=Image.new('RGB',(1280,1440))
    for j,im in enumerate(thumbs):contact.paste(im,((j%2)*640,(j//2)*360))
    contact.save(OUT/'revisao.jpg');sys.exit()
cmd=[FF,'-y','-v','error','-f','rawvideo','-vcodec','rawvideo','-pix_fmt','rgb24','-s','1280x720','-r',str(FPS),'-i','-','-i',str(TMP/'narracao.wav'),'-c:v','libx264','-preset','fast','-crf','20','-threads','4','-pix_fmt','yuv420p','-af','loudnorm=I=-16:TP=-1.5:LRA=11','-ar','48000','-c:a','aac','-b:a','160k','-movflags','+faststart',str(OUT/'missao-2-desafio-2-subtracao-ate-20.mp4')]
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
