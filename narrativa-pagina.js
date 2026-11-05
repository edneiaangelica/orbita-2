(() => {
  const video = document.querySelector('#narrative-video');
  const error = document.querySelector('#video-error');
  const showError = () => { error.hidden = false; };
  video.addEventListener('error', showError);
  video.querySelector('source').addEventListener('error', showError);
  video.addEventListener('playing', () => { error.hidden = true; });
  window.addEventListener('pagehide', () => video.pause());
})();
