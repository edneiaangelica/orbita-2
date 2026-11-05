from pathlib import Path
t=Path('scripts/render-adicao-v2.py').read_text(encoding='utf-8')
helpers=t[:t.index('sheet=Image.open')]
audio=t[t.index('timeline=[];'):t.index('def count(sc,t):')]
body=Path('scripts/cenas-problemas.py').read_text(encoding='utf-8')
assets=body[:body.index('def render(sc,t):')]
render=body[body.index('def render(sc,t):'):]
caption=t[t.index('    d.rectangle((0,610,1280,720),fill=NAVY)'):t.index("if '--preview' in sys.argv:")]
tail=t[t.index("if '--preview' in sys.argv:"):]
helpers=helpers.replace('assets/videos/missao-2/desafio-1/adicao-ate-20-v2','assets/videos/missao-2/desafio-3/probleminhas').replace('tmp/adicao-v2','tmp/problemas')
audio=audio.replace('scripts/adicao-v2.json','scripts/problemas.json').replace('assets/sons/missao-2/desafio-1/v2/','assets/sons/missao-2/desafio-3/')
audio=audio.replace("lead=0 if kind=='resposta' else .15","lead=.2").replace("tail=0 if kind=='sua_vez' else .25","tail=.9")
speed="""
source_jobs=json.loads((ROOT/'scripts/problemas.json').read_text(encoding='utf-8'))
speech_total=0
for kind,_,_ in source_jobs:
    ev=json.loads((ROOT/f'assets/sons/missao-2/desafio-3/{kind}.json').read_text(encoding='utf-8'))
    speech_total+=(ev[-1]['offset']+ev[-1]['duration']-ev[0]['offset'])/1e7
SPEECH_SPEED=speech_total/(100-len(source_jobs)*1.1)
"""
start=tail.index('    checks=');end=tail.index('\n    contact=',start)
tail=tail[:start]+"    checks=[('abertura',2),('somar',4),('ana',4),('adicao',6),('subtrair',2),('subtrair',6),('pedro',2),('subtracao',7),('lembrar',2),('dica',3),('fim',2),('adicao',9)]"+tail[end:]
tail=tail.replace('missao-2-desafio-1-adicao-ate-20-v2.mp4','missao-2-desafio-3-probleminhas.mp4').replace("'pauseSeconds':5,","'speechSpeed':SPEECH_SPEED,")
tail=tail.replace("('subtrair',6)","('subtrair',-1)").replace("('subtracao',7)","('subtracao',-1)").replace("('adicao',9)","('adicao',-1)")
tail=tail.replace("pic=render(sc,t)","pic=render(sc,sc['end']-sc['start']-.3 if t<0 else t)")
Path('scripts/render-problemas.py').write_text(helpers+assets+speed+audio+render+caption+tail,encoding='utf-8')
