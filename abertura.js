(() => {
  const scene = document.querySelector('.scene');
  const mobileScene = matchMedia('(max-width:700px), (max-width:1100px) and (max-height:600px) and (pointer:coarse)');
  const describeScene = () => scene?.setAttribute('aria-label', mobileScene.matches
    ? 'Teleco flutuando ao lado do planeta Aerívia, estrelas e conquistas.'
    : 'Teleco flutuando entre os mundos Mecano, Aerívia e Papiron, estrelas e conquistas.');
  mobileScene.addEventListener('change', describeScene);
  describeScene();
  const fullscreen = document.querySelector('#fullscreen');
  const sound = document.querySelector('#sound');
  const status = document.querySelector('#status');
  const paths = {
    expand: '<path d="M8 3H3v5m13-5h5v5M3 16v5h5m13-5v5h-5"/>',
    collapse: '<path d="M3 8h5V3m8 0v5h5M8 21v-5H3m13 5v-5h5"/>',
    sound: '<path d="m11 4-6 5H2v6h3l6 5zM15 8a6 6 0 0 1 0 8m3-11a10 10 0 0 1 0 14"/>',
    muted: '<path d="m11 4-6 5H2v6h3l6 5zM16 9l6 6m0-6-6 6"/>'
  };
  function update(button, icon, label, pressed) {
    button.innerHTML = '<svg viewBox="0 0 24 24" aria-hidden="true">' + paths[icon] + '</svg>';
    button.title = label;
    button.setAttribute('aria-label', label);
    button.setAttribute('aria-pressed', String(pressed));
  }
  let timer;
  function announce(text) {
    status.textContent = text;
    clearTimeout(timer);
    timer = setTimeout(() => { status.textContent = ''; }, 3000);
  }
  const audio = new Audio('assets/sons/ui.mp3');
  audio.volume = 0.3;
  let enabled = false;
  try { enabled = localStorage.getItem('orbita2-sound') === 'true'; } catch {}
  const syncSound = () => update(sound, enabled ? 'sound' : 'muted', enabled ? 'Desligar som' : 'Ligar som', enabled);
  sound.addEventListener('click', () => {
    enabled = !enabled;
    try { localStorage.setItem('orbita2-sound', String(enabled)); } catch {}
    if (!enabled) { audio.pause(); audio.currentTime = 0; }
    syncSound();
    announce(enabled ? 'Som ligado' : 'Som desligado');
  });
  document.addEventListener('click', event => {
    const target = event.target.closest('button,a');
    if (enabled && target && target.getAttribute('aria-disabled') !== 'true') {
      audio.currentTime = 0;
      audio.play().catch(() => {});
    }
  });
  syncSound();
})();

