import asyncio, json, sys
from pathlib import Path
sys.path.insert(0, 'C:/Users/USUARIO/Desktop/videos-educacionais/.deps')
import edge_tts
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'assets/sons/missao-2'
OUT.mkdir(parents=True, exist_ok=True)
jobs = json.loads((ROOT/'scripts/audio-missao-2.json').read_text(encoding='utf-8'))
only = sys.argv[1] if len(sys.argv)>1 else None
if only:
    if only == '--prompts':
        jobs = [job for job in jobs if job['id'].endswith('-prompt')]
    elif only in ('--d1-final', '--d2-final', '--d3-final'):
        challenge = only[2:4]
        jobs = [job for job in jobs if any(job['id'].startswith(f'{challenge}-q{n}-') for n in range(11, 16))]
    else:
        jobs = [job for job in jobs if job['id'] == only]
async def main():
    sem = asyncio.Semaphore(4)
    failures = []
    async def generate(job):
        target=OUT/(job['id']+'.mp3')
        if not only and target.exists() and target.stat().st_size > 1000: return
        async with sem:
            for attempt in range(3):
                try:
                    await asyncio.wait_for(edge_tts.Communicate(job['text'], 'pt-BR-FranciscaNeural', rate='-8%', connect_timeout=10, receive_timeout=25).save(str(target)), timeout=40)
                    print(job['id'], flush=True)
                    return
                except Exception as error:
                    print('Retry', job['id'], type(error).__name__, flush=True)
                    if attempt==2: failures.append((job['id'], str(error)))
                    else: await asyncio.sleep(2)
    await asyncio.gather(*(generate(job) for job in jobs))
    print(json.dumps({'expected':len(jobs),'files':len(list(OUT.glob('*.mp3'))),'failures':failures},ensure_ascii=False), flush=True)
    if failures: sys.exit(1)
asyncio.run(main())
