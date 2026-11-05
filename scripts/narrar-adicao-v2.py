import asyncio,json,sys
from pathlib import Path
sys.path.insert(0,'C:/Users/USUARIO/Desktop/videos-educacionais/.deps')
import edge_tts
ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'assets/sons/missao-2/desafio-1/v2'
OUT.mkdir(parents=True,exist_ok=True)
async def main():
    jobs=json.loads((ROOT/'scripts/adicao-v2.json').read_text(encoding='utf-8'))
    for kind,scene,text in jobs:
        target=OUT/f'{kind}.mp3'
        if target.exists() and target.with_suffix('.json').exists():continue
        events=[]
        rate='-8%' if kind in ['conta5','conta7'] else '+12%'
        speech=edge_tts.Communicate(text,'pt-BR-FranciscaNeural',rate=rate,boundary='WordBoundary',connect_timeout=10,receive_timeout=25)
        async with asyncio.timeout(60):
            with target.open('wb') as f:
                async for chunk in speech.stream():
                    if chunk['type']=='audio':f.write(chunk['data'])
                    elif chunk['type']=='WordBoundary':events.append({k:chunk[k] for k in ('offset','duration','text')})
        target.with_suffix('.json').write_text(json.dumps(events,ensure_ascii=False),encoding='utf-8')
        print(kind+' pronta',flush=True)
asyncio.run(main())
