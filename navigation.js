/* A stable fullscreen document hosts subsequent pages without re-requesting permission. */
(() => {
  const embedded = window.parent !== window && window.name === 'orbita-app-frame';
  let frame = null;
  let active = false;
  const expand = '<path d="M8 3H3v5m13-5h5v5M3 16v5h5m13-5v5h-5"/>';
  const collapse = '<path d="M3 8h5V3m8 0v5h5M8 21v-5H3m13 5v-5h5"/>';
  function sync(value = Boolean(document.fullscreenElement)) {
    active = value;
    const button = document.getElementById('fullscreen');
    if (button) {
      button.innerHTML = '<svg viewBox="0 0 24 24" aria-hidden="true">' + (active ? collapse : expand) + '</svg>';
      button.title = active ? 'Sair da tela cheia' : 'Entrar em tela cheia';
      button.setAttribute('aria-label', button.title);
      button.setAttribute('aria-pressed', String(active));
    }
    frame?.contentWindow.postMessage({type:'orbita-fullscreen-state', active}, '*');
  }
  function notify(text) {
    let status = document.getElementById('navigation-status');
    if (!status) {
      status = document.createElement('div');
      status.id = 'navigation-status';
      status.setAttribute('role', 'status');
      document.body.append(status);
    }
    status.textContent = text;
    setTimeout(() => status.remove(), 4000);
  }
  async function toggle() {
    try {
      if (document.fullscreenElement) await document.exitFullscreen();
      else if (document.documentElement.requestFullscreen) await document.documentElement.requestFullscreen();
      else notify('Este navegador não oferece o modo de tela cheia.');
    } catch { notify('Não foi possível alterar a tela cheia neste navegador.'); }
  }
  function navigate(href) {
    if (embedded || !document.fullscreenElement) { window.location.href = href; return; }
    document.querySelectorAll('video,audio').forEach(media => media.pause());
    window.speechSynthesis?.cancel();
    document.dispatchEvent(new Event('orbita-mute'));
    if (!frame) {
      frame = document.createElement('iframe');
      frame.name = 'orbita-app-frame';
      frame.id = 'orbita-app-frame';
      frame.title = 'Órbita';
      frame.allow = 'fullscreen; autoplay';
      frame.allowFullscreen = true;
      // Preserve the fullscreen element and keep the original page inactive.
      [...document.body.children].forEach(node => { node.hidden = true; node.inert = true; });
      document.documentElement.classList.add('orbita-shell');
      document.body.append(frame);
      frame.addEventListener('load', () => sync());
    }
    frame.src = href;
  }
  window.addEventListener('message', event => {
    if (embedded && event.source === window.parent && event.data?.type === 'orbita-fullscreen-state') sync(event.data.active);
    if (!frame || event.source !== frame.contentWindow) return;
    if (event.data?.type === 'orbita-fullscreen-ready') sync();
    if (event.data?.type === 'orbita-fullscreen-toggle') toggle();
    if (event.data?.type === 'orbita-page-title' && typeof event.data.title === 'string') document.title = event.data.title;
  });
  document.getElementById('fullscreen')?.addEventListener('click', () => {
    if (embedded) window.parent.postMessage({type:'orbita-fullscreen-toggle'}, '*');
    else toggle();
  });
  document.getElementById('exit')?.addEventListener('click', () => navigate(new URL('index.html', location.href).href));
  // Run after page handlers, preserving in-page actions such as "back to trail".
  document.addEventListener('click', event => {
    if (event.defaultPrevented || event.button !== 0 || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
    const link = event.target.closest('a[href]');
    if (!link || link.hasAttribute('download') || (link.target && link.target !== '_self')) return;
    const url = new URL(link.href, location.href);
    const current = new URL(location.href);
    if (url.origin !== current.origin || !url.pathname.endsWith('.html')) return;
    if (url.pathname === current.pathname && url.search === current.search && url.hash) return;
    if (!embedded && document.fullscreenElement) { event.preventDefault(); navigate(url.href); }
  });
  document.addEventListener('fullscreenchange', () => { if (!embedded) sync(); });
  sync();
  if (embedded) {
    window.parent.postMessage({type:'orbita-fullscreen-ready'}, '*');
    window.parent.postMessage({type:'orbita-page-title',title:document.title}, '*');
  }
})();
