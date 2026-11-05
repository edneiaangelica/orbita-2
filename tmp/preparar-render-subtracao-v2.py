from pathlib import Path
text=Path('scripts/render-adicao-v2.py').read_text(encoding='utf-8')
before=text[:text.index('def render(sc,t):')]
caption=text[text.index('    d.rectangle((0,610,1280,720),fill=NAVY)'):text.index("if '--preview' in sys.argv:")]
tail=text[text.index("if '--preview' in sys.argv:"):]
before=before.replace('assets/videos/missao-2/desafio-1/adicao-ate-20-v2','assets/videos/missao-2/desafio-2/subtracao-ate-20-v2').replace('tmp/adicao-v2','tmp/subtracao-v2')
before=before.replace('scripts/adicao-v2.json','scripts/subtracao-v2.json').replace('assets/sons/missao-2/desafio-1/v2/','assets/sons/missao-2/desafio-2/v2/')
before=before.replace('SPEECH_SPEED=.74','SPEECH_SPEED=.78')
before=before.replace("kind=='resposta'","kind=='resposta_conta'").replace("kind='pausa',scene=9","kind='pausa',scene=10").replace("vals=[a,'+',b,'=',result]","vals=[a,'−',b,'=',result]")
start=tail.index('    checks=');end=tail.index('\n    contact=',start)
tail=tail[:start]+"    checks=[('abertura',2),('retirar4',1.5),('retirar4',3),('sobraram4',2),('resultado4',1),('desafio',2),('quinze',2),('conta4',2),('resultado',1),('relembra',2),('pausa',2),('resposta_conta',1.5)]"+tail[end:]
tail=tail.replace('missao-2-desafio-1-adicao-ate-20-v2.mp4','missao-2-desafio-2-subtracao-ate-20-v2.mp4')
Path('scripts/render-subtracao-v2.py').write_text(before+Path('scripts/cenas-subtracao-v2.py').read_text(encoding='utf-8')+caption+tail,encoding='utf-8')
