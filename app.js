const icons = {
  home: '<path d="m3 10 9-7 9 7v10a1 1 0 0 1-1 1h-5v-7H9v7H4a1 1 0 0 1-1-1z"/>',
  route: '<circle cx="6" cy="5" r="2"/><circle cx="18" cy="19" r="2"/><path d="M8 5h8a4 4 0 0 1 0 8H8a3 3 0 0 0 0 6h8"/>',
  user: '<circle cx="12" cy="8" r="4"/><path d="M4 21v-2a8 8 0 0 1 16 0v2"/>',
  planet: '<circle cx="12" cy="12" r="7"/><ellipse cx="12" cy="12" rx="12" ry="4" transform="rotate(-30 12 12)"/>',
  chat: '<path d="M21 11a9 9 0 0 1-9 9H4l-2 2V11a9 9 0 0 1 19 0Z"/><path d="M7 10h10M7 14h6"/>',
  book: '<path d="M12 5v16M12 5C8 2 4 3 2 4v16c3-1 6-1 10 1 4-2 7-2 10-1V4c-2-1-6-2-10 1Z"/>',
  help: '<circle cx="12" cy="12" r="9"/><path d="M9 9a3 3 0 0 1 6 0c0 2-3 2-3 5M12 17h.01"/>',
  exit: '<path d="M10 4H4v16h6M10 12h11m-4-4 4 4-4 4"/>',
  expand: '<path d="M8 3H3v5m13-5h5v5M3 16v5h5m13-5v5h-5"/>',
  collapse: '<path d="M3 8h5V3m8 0v5h5M8 21v-5H3m13 5v-5h5"/>',
  sound: '<path d="m11 4-6 5H2v6h3l6 5zM15 8a6 6 0 0 1 0 8m3-11a10 10 0 0 1 0 14"/>',
  muted: '<path d="m11 4-6 5H2v6h3l6 5zM16 9l6 6m0-6-6 6"/>',
  arrow: '<path d="M4 12h16m-6-6 6 6-6 6"/>',
  flag: '<path d="M5 22V3m0 1c5-4 9 4 15 0v10c-6 4-10-4-15 0"/>',
  medal: '<circle cx="12" cy="9" r="6"/><path d="m8 14-2 8 6-3 6 3-2-8m-4-8v6m-3-3h6"/>'
};
function renderIcon(element, name) { element.innerHTML = `<svg viewBox="0 0 24 24" aria-hidden="true">${icons[name]}</svg>`; }
document.querySelectorAll('[data-icon]').forEach(element => renderIcon(element, element.dataset.icon));
const notice = document.querySelector('#notice');
function showNotice(title, message) {
  document.querySelector('#notice-title').textContent = title;
  document.querySelector('#notice-text').textContent = message;
  notice.showModal();
}
document.querySelectorAll('[data-soon]').forEach(button => button.addEventListener('click', () => {
  showNotice(`${button.dataset.soon}: em breve`, 'Estamos preparando esta parte da sua aventura. Por enquanto, conheça sua tela Início. Novas descobertas vêm aí!');
}));
notice?.addEventListener('click', event => { if (event.target === notice) { const rect = notice.getBoundingClientRect(); if (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) notice.close(); } });
let toastTimer;
function toast(message) { const element = document.querySelector('#toast'); element.textContent = message; element.classList.add('visible'); clearTimeout(toastTimer); toastTimer = setTimeout(() => element.classList.remove('visible'), 3500); }
const audio = new Audio('assets/sons/ui.mp3');
audio.volume = 0.3;
let soundEnabled = false;
try { soundEnabled = localStorage.getItem('orbita2-sound') === 'true'; } catch {}
const soundButton = document.querySelector('#sound');
window.orbitaSoundEnabled = () => soundEnabled;
window.orbitaEnableSound = () => { soundEnabled = true; try { localStorage.setItem('orbita2-sound', 'true'); } catch {} updateSound(); };
function updateSound() {
  document.querySelectorAll('video,audio').forEach(media => media.muted = !soundEnabled);
  if (!soundEnabled) { window.speechSynthesis?.cancel(); document.dispatchEvent(new Event('orbita-mute')); }
  soundButton.title = soundEnabled ? 'Desligar som' : 'Ligar som';
  soundButton.setAttribute('aria-label', soundButton.title);
  soundButton.setAttribute('aria-pressed', String(soundEnabled));
  renderIcon(soundButton.firstElementChild, soundEnabled ? 'sound' : 'muted');
}
soundButton.addEventListener('click', () => {
  soundEnabled = !soundEnabled;
  try { localStorage.setItem('orbita2-sound', String(soundEnabled)); } catch {}
  if (!soundEnabled) { audio.pause(); audio.currentTime = 0; }
  updateSound();
  toast(soundEnabled ? 'Som ligado' : 'Som desligado');
});
document.addEventListener('click', event => {
  if (soundEnabled && event.target.closest('button')) { audio.currentTime = 0; audio.play().catch(() => {}); }
});
updateSound();

// Keep sound/fullscreen accessible while the home navigation moves to the bottom.
const homeControls = document.querySelector('.home-controls');
if (homeControls) {
 const mobileMenu = matchMedia('(max-width:720px), (max-width:1000px) and (pointer:coarse)');
 const placeControls = () => { (mobileMenu.matches ? document.querySelector('.home-topbar .toolbar') : document.querySelector('.home-sidebar')).append(homeControls); };
 mobileMenu.addEventListener('change', placeControls);
 placeControls();
}

