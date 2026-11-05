import asyncio, json, sys
from pathlib import Path
sys.path.insert(0, 'C:/Users/USUARIO/Desktop/videos-educacionais/.deps')
import edge_tts
ROOT=Path(__file__).resolve().parent.parent
texts=json.loads((ROOT/'scripts/narrativa-texto.json').read_text(encoding='utf-8-sig'))
async def main():
    for i,text in enumerate(texts,1):
        target=ROOT/f'assets/sons/narrativa/cena-{i:02d}.mp3'
        if target.exists() and target.stat().st_size>1000: continue
        await edge_tts.Communicate(text,'pt-BR-FranciscaNeural',rate='-8%').save(str(target))
        print(f'Cena {i}: Francisca pronta',flush=True)
asyncio.run(main())
