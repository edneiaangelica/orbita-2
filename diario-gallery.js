(() => {
  const grid = document.getElementById('planet-gallery');
  for (const planet of [...window.ORBITA_PLANETS].sort((a,b) => a.order - b.order)) {
    const link = document.createElement('a'); link.className = 'planet-destination';
    link.href = `diario-planeta.html?planeta=${encodeURIComponent(planet.id)}`;
    link.setAttribute('aria-label', `Abrir álbum de ${planet.name}`);
    const image = document.createElement('img'); image.src = planet.heroImage; image.alt = planet.cards[0].caption; image.width = 320; image.height = 320;
    const number = document.createElement('span'); number.className = 'diary-kicker'; number.textContent = `PLANETA ${String(planet.order).padStart(2,'0')}`;
    const title = document.createElement('h2'); title.textContent = planet.name;
    link.append(image, number, title); grid.append(link);
  }
})();
