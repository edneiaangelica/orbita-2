(() => {
  const video = document.getElementById('story-video');
  if (!video) return;
  // The first explicit play starts the narrated story with sound.
  video.addEventListener('play', () => window.orbitaEnableSound(), { once: true });
  video.addEventListener('error', () => { document.getElementById('story-error').hidden = false; });
  window.addEventListener('pagehide', () => video.pause());
})();
