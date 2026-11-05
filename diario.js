(() => {
  const planets = window.ORBITA_PLANETS;
  const planet = planets.find(p => p.id === new URLSearchParams(location.search).get('planeta')) || planets.find(p => p.id === 'lamalume') || planets[0];
  const wallet = window.OrbitaWallet;
  if(wallet.preview)planet.previewUnlocked=true;
  const $ = id => document.getElementById(id);
  const ownedId = card => `diary:${planet.id}:${card.id}`;
  const planetId = () => ownedId(planet.cards[0]);
  const isOwned = card => planet.previewUnlocked || wallet.snapshot().purchases.includes(ownedId(card));
  const grid = $('album-grid');
  const viewer = $('photo-viewer');
  const confirm = $('purchase-dialog');
  let pending = null, current = 0;
  const fullText = $('full-story');
  $('full-story-title').textContent = `${planet.name} — Texto integral`;
  $('full-story-content').replaceChildren(...planet.cards.map(card => {
    const p = document.createElement('p'); p.textContent = card.text; return p;
  }));
  $('read-full-story').addEventListener('click', () => fullText.showModal());
  $('full-story-close').addEventListener('click', () => fullText.close());
  function render() {
    window.ORBITA_DIARY = planet;
    document.body.dataset.planet = planet.id;
    document.title = `Órbita 2 • ${planet.name}`;
    $('planet-title').textContent = planet.name;
    const hero = document.querySelector('.planet-art > img'); hero.src = planet.heroImage; hero.alt = planet.cards[0].caption;
    document.querySelector('.planet-tag').textContent = `PLANETA ${String(planet.order).padStart(2,'0')} / UM MUNDO A DESCOBRIR`;
    document.querySelector('.planet-intro').textContent = planet.intro;
    document.querySelector('.planet-intro + p').textContent = planet.description;
    $('album-title').textContent = `O álbum de ${planet.name}`;
    document.querySelector('.album-heading p').textContent = planet.previewUnlocked ? 'Toque em uma imagem para ampliar e ler sua história.' : 'Desbloqueie uma imagem. Toque nela para ampliar e ler sua história.';
    $('album-progress').max = planet.cards.length;
    $('album-progress').setAttribute('aria-label', `Descobertas de ${planet.name}`);
    const state = wallet.snapshot();
    const count = planet.cards.filter(isOwned).length;
    $('album-count').textContent = `${count} de ${planet.cards.length} descobertas`;
    $('album-progress').value = count;
    $('planet-action').textContent = count ? 'Explorar meu álbum ↓' : `Desbloquear ${planet.name} · ${planet.cost} moedas`;
    $('planet-hint').textContent = planet.previewUnlocked ? 'Planeta e todas as imagens liberados para explorar.' : count ? 'Planeta desbloqueado. Sua próxima descoberta está logo abaixo.' : 'Inclui a primeira imagem do álbum. As demais custam 500 moedas cada.';
    $('wallet-status').textContent = planet.previewUnlocked || state.available ? '' : 'Não foi possível acessar seu saldo. Permita o armazenamento do navegador para continuar.';
    grid.replaceChildren(...planet.cards.map(card => {
      const owned = isOwned(card);
      const article = document.createElement('article'); article.className = `album-card ${owned ? 'is-owned' : 'is-locked'}`;
      const imageButton = document.createElement('button'); imageButton.className = 'card-image'; imageButton.type = 'button';
      imageButton.setAttribute('aria-label', `${owned ? 'Ampliar' : 'Desbloquear'}: ${card.caption}`);
      const img = document.createElement('img'); img.src = card.image; img.alt = card.caption; img.loading = 'lazy'; img.width = 1536; img.height = 1024;
      const number = document.createElement('span'); number.className = 'card-number'; number.textContent = String(card.number).padStart(2, '0');
      const badge = document.createElement('span'); badge.className = 'card-state'; badge.textContent = owned ? '✓ No seu álbum · Ampliar' : '◇ Descoberta bloqueada';
      imageButton.append(img, number, badge); imageButton.addEventListener('click', () => activate(card));
      const copy = document.createElement('div'); copy.className = 'card-copy';
      const h = document.createElement('h3'); h.textContent = card.caption;
      const p = document.createElement('p'); p.textContent = card.text;
      copy.append(h, p);
      if (!owned) { const price = document.createElement('span'); price.className = 'card-price'; price.textContent = `${card.cost} moedas`; copy.append(price); }
      article.append(imageButton, copy); return article;
    }));
  }
  function activate(card) {
    if (isOwned(card)) { openPhoto(card.number - 1); return; }
    if (card.number !== 1 && !wallet.snapshot().purchases.includes(planetId())) {
      showNotice('Primeiro, uma nova órbita!', `Desbloqueie o planeta ${planet.name} por ${planet.cost} moedas para começar sua coleção. A primeira imagem já está incluída.`); return;
    }
    pending = card;
    $('purchase-title').textContent = card.number === 1 ? `Desbloquear ${planet.name}` : card.caption;
    $('purchase-copy').textContent = `Esta descoberta custa ${card.cost} moedas. Seu saldo é de ${wallet.snapshot().coins.toLocaleString('pt-BR')} moedas.`;
    $('purchase-error').textContent = '';
    $('purchase-confirm').textContent = `Desbloquear por ${card.cost} moedas`;
    $('purchase-confirm').disabled = false; confirm.showModal();
  }
  function openPhoto(index) {
    const card = planet.cards[index]; if (!card || !isOwned(card)) return;
    current = index; $('viewer-image').src = card.image; $('viewer-image').alt = card.caption;
    $('viewer-title').textContent = card.caption; $('viewer-text').textContent = card.text;
    $('viewer-number').textContent = `${planet.name.toLocaleUpperCase('pt-BR')} / DESCOBERTA ${String(card.number).padStart(2, '0')}`;
    $('previous-photo').disabled = !planet.cards.slice(0, index).some(isOwned);
    $('next-photo').disabled = !planet.cards.slice(index + 1).some(isOwned);
    if (!viewer.open) viewer.showModal();
  }
  function move(direction) { for (let i = current + direction; i >= 0 && i < planet.cards.length; i += direction) { if (isOwned(planet.cards[i])) { openPhoto(i); break; } } }
  $('planet-action').addEventListener('click', () => isOwned(planet.cards[0]) ? $('album').scrollIntoView({behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth'}) : activate(planet.cards[0]));
  $('purchase-confirm').addEventListener('click', async () => {
    if (!pending) return;
    const card = pending; $('purchase-confirm').disabled = true;
    const result = await wallet.purchase(ownedId(card), card.cost, card.number === 1 ? null : planetId());
    if (result.ok) { confirm.close(); render(); openPhoto(card.number - 1); }
    else {
      $('purchase-error').textContent = ({funds: 'Você ainda não tem moedas suficientes para esta descoberta.', planet: 'Desbloqueie o planeta primeiro.', storage: 'Não foi possível salvar a compra. Nenhuma moeda foi descontada.', browser: 'Abra o app em um navegador atualizado e uma conexão segura para desbloquear imagens.'})[result.reason];
      $('purchase-confirm').disabled = false;
    }
  });
  $('purchase-cancel').addEventListener('click', () => confirm.close());
  $('viewer-close').addEventListener('click', () => viewer.close());
  viewer.addEventListener('close', () => grid.children[current]?.querySelector('.card-image').focus({preventScroll: true}));
  $('previous-photo').addEventListener('click', () => move(-1)); $('next-photo').addEventListener('click', () => move(1));
  viewer.addEventListener('keydown', e => { if (e.key === 'ArrowRight') move(1); if (e.key === 'ArrowLeft') move(-1); });
  for (const dialog of [viewer, confirm, fullText]) dialog.addEventListener('click', e => { if (e.target === dialog) { const r = dialog.getBoundingClientRect(); if (e.clientX < r.left || e.clientX > r.right || e.clientY < r.top || e.clientY > r.bottom) dialog.close(); } });
  window.addEventListener('orbita-wallet-change', render);
  render();
})();
