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
