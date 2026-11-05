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
