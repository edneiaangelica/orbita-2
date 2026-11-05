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
