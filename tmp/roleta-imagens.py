from pathlib import Path
p=Path('roleta.js');s=p.read_text(encoding='utf-8')
s=s.replace(" const point=", " const images=['assets/imagens/mundos/aura-rubre/lamalume.png','assets/imagens/diario/papiron/planeta-papiron.png','assets/imagens/mundos/aura-rubre/mecano.png','assets/imagens/mundos/aura-rubre/aerivia.png','assets/imagens/mundos/aura-rubre/planeta-42.png','assets/imagens/mundos/aura-rubre/aura-rubre.png'];\n const point=")
a=s.index('  return `<g><path');b=s.index('\n }).join',a)
s=s[:a]+'''  return `<g><path d="M220 220 L${x1} ${y1} A204 204 0 0 1 ${x2} ${y2} Z" fill="white" stroke="${colors[i]}" stroke-width="3"/><image href="${images[i]}" x="${tx-54}" y="${ty-54}" width="108" height="108" preserveAspectRatio="xMidYMid meet"><title>${p.name}</title></image></g>`;'''+s[b:]
s=s.replace('r="44" fill="#EFFAFD"','r="44" fill="white"')
s=s.replace('<span class="planet-dot" style="background:${colors[i]}"></span>${p.name}','<span class="planet-label"><img src="${images[i]}" alt="" width="32" height="32">${p.name}</span>')
p.write_text(s,encoding='utf-8')
p=Path('roleta.css');s=p.read_text(encoding='utf-8');s+='''
/* Planetas ilustrados: roleta e painel brancos; pontuação apenas na tabela. */
.roulette-dialog{background:#fff}
.planet-label{display:flex;align-items:center;gap:10px}
.planet-label img{width:32px;height:32px;object-fit:contain;flex-shrink:0}
.roulette-info td{padding:4px 12px}
@media(min-width:721px) and (max-height:680px){.planet-label img{width:24px;height:24px}.roulette-info td{padding:3px 10px}}
''';p.write_text(s,encoding='utf-8')
p=Path('mission.html');s=p.read_text(encoding='utf-8').replace('roleta.css?v=1','roleta.css?v=planetas-2').replace('roleta.js?v=1','roleta.js?v=planetas-2');p.write_text(s,encoding='utf-8')
