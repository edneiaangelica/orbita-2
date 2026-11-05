from pathlib import Path
s=Path('scripts/criar-vd-explica-m3-d2-fluido.py').read_text(encoding='utf-8-sig')
s=s.replace("OUT=ROOT/'assets/videos/missao-3/desafio-2/vd-explica-m3-d2-fluido'","OUT=ROOT/'assets/videos/missao-3/desafio-2/vd-explica-m3-d2-continuo'")
old=" raws[k]=raw[round(start*24000)*2:round(end*24000)*2];evs[k]=[dict(text=e['text'],start=e['offset']/1e7-start) for e in ev]"
new=''' # Shorten only gaps between word boundaries, retaining 120 ms on each side.
 cuts=[]
 for previous,following in zip(ev,ev[1:]):
  left=(previous['offset']+previous['duration'])/1e7+.12
  right=following['offset']/1e7-.12
  if right>left+.04:cuts.append((round(left*24000),round(right*24000)))
 first=round(start*24000);last=round(end*24000);cursor=first;pieces=[]
 for a,b in cuts:
  assert first<=a<b<=last
  pieces.append(raw[cursor*2:a*2]);cursor=b
 pieces.append(raw[cursor*2:last*2]);raws[k]=b''.join(pieces)
 evs[k]=[]
 for e in ev:
  pos=round(e['offset']/1e7*24000)
  removed=sum(b-a for a,b in cuts if b<=pos)
  evs[k].append(dict(text=e['text'],start=(pos-first-removed)/24000))
 assert all(a['start']<b['start'] for a,b in zip(evs[k],evs[k][1:]))
'''
assert old in s;s=s.replace(old,new)
s=s.replace('len(raw)/48000+.30','len(raw)/48000+.10').replace('len(raw)/48000+.12','len(raw)/48000+.03').replace("e['start']/speed+.12","e['start']/speed+.03").replace('block=bytes(5760)+raw','block=bytes(1440)+raw')
Path('scripts/criar-vd-explica-m3-d2-continuo.py').write_text(s,encoding='utf-8')
