const fs = require('node:fs');
for (const file of ['index.html', 'avatar.html', 'mission.html']) {
  let html = fs.readFileSync(file, 'utf8');
  html = html.replace(/<button([^>]*?) type="button" data-soon="Diário de bordo"([^>]*?)>(.*?)<\/button>/g, '<a$1 href="diario.html"$2>$3</a>');
  if (!html.includes('src="wallet.js"')) html = html.replace('</head>', '<script src="wallet.js" defer></script></head>');
  fs.writeFileSync(file, html);
}
const source = fs.readFileSync('avatar.html', 'utf8');
const header = source.match(/<header[\s\S]*?<\/header>/)[0].replace('href="avatar.html" aria-current="page"', 'href="avatar.html"').replace('href="diario.html"', 'href="diario.html" aria-current="page"');
const notice = source.match(/<dialog id="notice">[\s\S]*?<\/dialog>/)[0];
fs.writeFileSync('diario.html', `<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Órbita 2 • Diário de bordo</title>
<link rel="icon" href="assets/imagens/icones-e-logos/favicon.png"><link rel="stylesheet" href="styles.css"><link rel="stylesheet" href="theme.css"><link rel="stylesheet" href="mobile-nav.css"><link rel="stylesheet" href="diario.css">
<script src="app.js" defer></script><script src="wallet.js" defer></script><script src="diario-data.js" defer></script><script src="diario-lamalume.js" defer></script><script src="diario-mecano.js" defer></script><script src="diario-planeta-42.js" defer></script><script src="diario-aerivia.js" defer></script><script src="diario-atria.js" defer></script><script src="diario-papiron.js" defer></script><script src="diario-tempus.js" defer></script><script src="diario-gallery.js" defer></script></head>
<body class="diary-page"><a class="skip" href="#conteudo">Ir para o conteúdo</a><div class="workspace">${header}<main id="conteudo" class="diary-main"><div class="diary-heading"><div><span class="diary-kicker">ARQUIVO DA EXPEDIÇÃO ÓRBITA</span><h1>Diário de bordo</h1><p>Escolha um planeta para abrir seu álbum.</p></div></div><div id="planet-gallery" class="planet-gallery"></div></main></div>${notice}<div class="toast" role="status" id="toast"></div></body></html>`);
fs.writeFileSync('diario-planeta.html', `<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#201a30"><title>Órbita 2 • Diário de bordo</title>
<link rel="icon" href="assets/imagens/icones-e-logos/favicon.png"><link rel="stylesheet" href="styles.css"><link rel="stylesheet" href="theme.css"><link rel="stylesheet" href="mobile-nav.css"><link rel="stylesheet" href="diario.css">
<script src="app.js" defer></script><script src="wallet.js" defer></script><script src="diario-data.js" defer></script><script src="diario-lamalume.js" defer></script><script src="diario-mecano.js" defer></script><script src="diario-planeta-42.js" defer></script><script src="diario-aerivia.js" defer></script><script src="diario-atria.js" defer></script><script src="diario-papiron.js" defer></script><script src="diario-tempus.js" defer></script><script src="diario.js" defer></script></head>
<body class="diary-page"><a class="skip" href="#conteudo">Ir para o conteúdo</a><div class="workspace">${header}
<main id="conteudo" class="diary-main">
<div class="diary-heading"><div><span class="diary-kicker">ARQUIVO DA EXPEDIÇÃO ÓRBITA</span><h1>Diário de bordo</h1><p>Cada descoberta, uma história para guardar.</p></div><span class="system-tag">9 planetas <span>✧</span> 1 estrela</span></div>
<div class="album-top-actions"><a href="diario.html" class="back-planets">← Todos os planetas</a><button type="button" id="read-full-story" class="primary">Ler texto integral</button></div><section class="planet-hero" aria-labelledby="planet-title"><div class="planet-art"><img src="assets/imagens/diario/umbralia/umbralia.png" alt="Umbrália: um planeta de carvão com torres góticas e contorno violeta" width="1024" height="1024"><span class="orbit-label">SISTEMA AURA RUBRE</span></div><div class="planet-copy"><span class="planet-tag">PLANETA 09 / UM MUNDO A DESCOBRIR</span><h2 id="planet-title">Umbrália</h2><p class="planet-intro">Um mundo de sombras.<br>Uma dupla cheia de opiniões.</p><p>Abra seu álbum e conheça os curiosos habitantes deste planeta — onde até a Morte precisa ter paciência.</p><button class="planet-unlock" id="planet-action" type="button">Desbloquear Umbrália · 650 moedas</button><p class="planet-hint" id="planet-hint"></p></div></section>
<section id="album" aria-labelledby="album-title"><div class="album-heading"><div><span class="diary-kicker">LEMBRANÇAS DE OUTRO MUNDO</span><h2 id="album-title">O álbum de Umbrália</h2><p>Desbloqueie uma imagem. Toque nela para ampliar e ler sua história.</p></div><div class="album-progress"><span id="album-count">0 de 12 descobertas</span><progress id="album-progress" max="12" value="0" aria-label="Descobertas de Umbrália"></progress></div></div><p id="wallet-status" role="status"></p><div id="album-grid" class="album-grid"></div></section>
<footer class="diary-footer">✧ Um universo de histórias espera por você. <span>Novos planetas e Aura Rubre em breve.</span></footer>
</main></div>
<dialog id="photo-viewer" class="photo-viewer" aria-labelledby="viewer-title" aria-describedby="viewer-text"><button type="button" id="viewer-close" class="viewer-close" aria-label="Fechar imagem">×</button><div class="viewer-art"><img id="viewer-image" alt=""></div><div class="viewer-copy"><span id="viewer-number" class="diary-kicker"></span><h2 id="viewer-title"></h2><p id="viewer-text"></p><div class="viewer-navigation"><button type="button" id="previous-photo">← Anterior</button><button type="button" id="next-photo">Próxima →</button></div></div></dialog>
<dialog id="full-story" class="full-story" aria-labelledby="full-story-title"><div class="full-story-heading"><h2 id="full-story-title"></h2><button type="button" id="full-story-close" aria-label="Fechar texto integral">×</button></div><div id="full-story-content"></div></dialog><dialog id="purchase-dialog" aria-labelledby="purchase-title" aria-describedby="purchase-copy"><span class="dialog-symbol">✧</span><h2 id="purchase-title"></h2><p id="purchase-copy"></p><p id="purchase-error" role="status"></p><div class="purchase-actions"><button type="button" id="purchase-confirm" class="primary"></button><button type="button" id="purchase-cancel" class="secondary">Agora não</button></div></dialog>
${notice}<div class="toast" role="status" id="toast"></div></body></html>`);





