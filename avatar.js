(() => {
  const root = 'assets/imagens/avatar/';
  const key = 'orbita2-avatar';
  const defaults = { pele: 'avatar-base.png', rosto: 'avatar-rostos/1.png', cabelos: 'avatar-cabelos-cores/cacheado-curto-castanho.png', blusas: 'avatar-roupas/blusa-branca-azul.png', partes: 'avatar-roupas/bermuda-jeans.png', sapatos: 'avatar-sapatos/tenis-azul.png', acessorios: '' };
  const labels = { pele: 'Tom de pele', rosto: 'Rosto', cabelos: 'Cabelos', blusas: 'Blusas', partes: 'Bermudas e saias', sapatos: 'Sapatos', acessorios: 'Acessórios' };
  let saved = { ...defaults };
  try {
    const stored = JSON.parse(localStorage.getItem(key));
    for (const category in defaults) {
      const value = stored?.[category];
      if (avatarCatalog[category].includes(value) || value === defaults[category] || (value === '' && ['cabelos', 'acessorios'].includes(category))) saved[category] = value;
    }
  } catch {}
  let draft = { ...saved };
  const preview = document.querySelector('#avatar-preview');
  function draw(element, selection) {
    element.replaceChildren(...['pele', 'rosto', 'partes', 'blusas', 'sapatos', 'cabelos', 'acessorios'].filter(c => selection[c]).map(c => {
      const img = document.createElement('img'); img.src = root + selection[c]; img.alt = ''; img.draggable = false; return img;
    }));
  }
  if (!preview) {
    document.querySelectorAll('.avatar').forEach(element => { draw(element, saved); element.setAttribute('aria-label', 'Seu avatar personalizado'); });
    return;
  }
  let active = 'pele';
  const options = document.querySelector('#avatar-options');
  const status = document.querySelector('#avatar-status');
  function name(path) {
    if (!path) return 'Sem ' + (active === 'cabelos' ? 'cabelo' : 'acessório');
    const raw = path.split('/').pop().replace('.png', '').replace(/^\d+-/, '').replaceAll('-', ' ');
    if (active === 'rosto') return 'Rosto ' + raw;
    const words = { pessego: 'pêssego', ebano: 'ébano', oculos: 'óculos', tenis: 'tênis', coracao: 'coração', moleton: 'moletom' };
    return raw.replace(/\b\w+\b/g, word => words[word] || word).replace(/^./, c => c.toUpperCase());
  }
  function thumbnail(path) {
    const parts = path.split('/');
    const folder = { rosto: 'rostos', cabelos: 'cabelos', blusas: 'roupas', partes: 'roupas', sapatos: 'sapatos', acessorios: 'acessorios' }[active];
    return root + (folder ? 'avatar-previews/' + folder + '/' + parts.at(-1) : path);
  }
  function refresh() {
    draw(preview, draft);
    status.textContent = JSON.stringify(draft) === JSON.stringify(saved) ? 'Tudo pronto para sua próxima aventura.' : 'Gostou do visual? Salve seu avatar!';
    document.querySelectorAll('[data-category]').forEach(button => button.setAttribute('aria-pressed', String(button.dataset.category === active)));
    document.querySelector('#options-title').textContent = labels[active];
    const choices = [...avatarCatalog[active]];
    if (['cabelos', 'acessorios'].includes(active)) choices.unshift('');
    document.querySelector('#options-count').textContent = choices.length + ' opções';
    options.replaceChildren(...choices.map(path => {
      const button = document.createElement('button'); button.className = 'avatar-option'; button.type = 'button'; button.setAttribute('aria-pressed', String(draft[active] === path));
      if (path) { const img = document.createElement('img'); img.src = thumbnail(path); img.alt = ''; img.loading = 'lazy'; button.append(img); }
      else { const empty = document.createElement('span'); empty.className = 'empty-option'; empty.textContent = '∅'; button.append(empty); }
      const caption = document.createElement('span'); caption.textContent = name(path); button.append(caption);
      button.addEventListener('click', () => {
        draft[active] = path; draw(preview, draft);
        options.querySelectorAll('button').forEach(b => b.setAttribute('aria-pressed', String(b === button)));
        status.textContent = 'Gostou do visual? Salve seu avatar!';
      });
      return button;
    }));
  }
  for (const category in labels) {
    const button = document.createElement('button'); button.type = 'button'; button.dataset.category = category; button.textContent = labels[category];
    button.addEventListener('click', () => { active = category; refresh(); });
    document.querySelector('.avatar-categories').append(button);
  }
  document.querySelector('#avatar-save').addEventListener('click', () => {
    try { localStorage.setItem(key, JSON.stringify(draft)); saved = { ...draft }; status.textContent = 'Avatar salvo. Vamos explorar!'; toast('Seu avatar foi salvo!'); }
    catch { status.textContent = 'Não foi possível salvar neste navegador. Tente permitir o armazenamento local.'; }
  });
  document.querySelector('#avatar-random').addEventListener('click', () => { for (const c in draft) { const items = avatarCatalog[c]; draft[c] = items[Math.floor(Math.random() * items.length)]; } refresh(); });
  document.querySelector('#avatar-reset').addEventListener('click', () => { draft = { ...defaults }; refresh(); });
  refresh();
})();
