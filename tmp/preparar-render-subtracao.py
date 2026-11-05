from pathlib import Path
p=Path('scripts/render-missao-2.py').read_text(encoding='utf-8')
before=p[:p.index('def render(sc,t):')]
after=p[p.index("if '--preview' in sys.argv:"):]
before=before.replace("OUT=ROOT/'assets/videos/missao-2/desafio-1/adicao-ate-20'","OUT=ROOT/'assets/videos/missao-2/desafio-2/subtracao-ate-20'")
before=before.replace("TMP=ROOT/'tmp/missao-2-desafio-1'","TMP=ROOT/'tmp/missao-2-desafio-2'")
before=before.replace("scripts/missao-2-desafio-1.json","scripts/missao-2-desafio-2.json").replace('assets/sons/missao-2/desafio-1/','assets/sons/missao-2/desafio-2/')
after=after.replace('[0,3,4,9,12,13,14,17]','[0,3,5,9,13,14,15,19]').replace('missao-2-desafio-1-adicao-ate-20.mp4','missao-2-desafio-2-subtracao-ate-20.mp4')
after=after.replace("'-c:a','aac'","'-ar','48000','-c:a','aac'")
body=Path('scripts/cenas-subtracao.py').read_text(encoding='utf-8')
before=before.replace('/{i:02}.mp3','/{kind}.mp3')
after=after.replace('[0,3,5,9,13,14,15,19]','[3,5,6,8,9,13,17,18]')
Path('scripts/render-missao-2-desafio-2.py').write_text(before+body+'\n'+after,encoding='utf-8')
