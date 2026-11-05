from pathlib import Path
text=Path('scripts/narrar-adicao-v2.py').read_text(encoding='utf-8')
text=text.replace('desafio-1/v2','desafio-2/v2').replace('scripts/adicao-v2.json','scripts/subtracao-v2.json').replace("['conta5','conta7']","['retirar4','sobraram4','conta4','resposta_conta']")
Path('scripts/narrar-subtracao-v2.py').write_text(text,encoding='utf-8')
