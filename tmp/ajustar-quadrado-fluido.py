from pathlib import Path
import shutil
s=Path('scripts/criar-vd-explica-m3-d2.py').read_text(encoding='utf-8-sig')
s=s.replace("OUT=ROOT/'assets/videos/missao-3/desafio-2/vd-explica-m3-d2'","OUT=ROOT/'assets/videos/missao-3/desafio-2/vd-explica-m3-d2-fluido'").replace("TMP=ROOT/'tmp/vd-explica-m3-d2'","TMP=ROOT/'tmp/vd-explica-m3-d2-fluido'")
s=s.replace("speech=edge_tts.Communicate(words,voice,", "spoken=words.replace('Complete,','Compléte,')\n  speech=edge_tts.Communicate(spoken,voice,")
s=s.replace('dur=math.ceil((len(raw)/48000+.35)*FPS)/FPS','dur=math.ceil((len(raw)/48000+.30)*FPS)/FPS')
s=s.replace(" if k in ['atencao','zero','sete','escolha','um','conferir','fim']:\n  target={1:25,2:43,3:57,4:77,5:98,6:113,7:123}[s]\n  dur=max(dur,target-offset)\n",'')
s=s.replace('n=min(6,int(t/2.0)+1);','n=min(6,int(t/max(.5,(sc["speech_end"]-.6)/6))+1);')
s=s.replace("('zero',9),('sete',7),('escolha',8),('seis',6),('um',5),('conferir',3),('conferir',12)","('zero',6),('sete',4),('escolha',6),('seis',3),('um',2.5),('conferir',2),('conferir',6)")
s=s.replace("# Reserve five seconds to think and four seconds for the visual answer.","# Short transitions only; the narration controls scene length.")
Path('scripts/criar-vd-explica-m3-d2-fluido.py').write_text(s,encoding='utf-8')
dest=Path('tmp/vd-explica-m3-d2-fluido');dest.mkdir(exist_ok=True)
for src in Path('tmp/vd-explica-m3-d2').iterdir():
 if src.suffix in ['.mp3','.json'] and src.stem!='fim':shutil.copy2(src,dest/src.name)
