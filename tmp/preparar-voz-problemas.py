from pathlib import Path
text=Path('scripts/narrar-adicao-v2.py').read_text(encoding='utf-8')
text=text.replace('desafio-1/v2','desafio-3').replace('scripts/adicao-v2.json','scripts/problemas.json')
Path('scripts/narrar-problemas.py').write_text(text,encoding='utf-8')
