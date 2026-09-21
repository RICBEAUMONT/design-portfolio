(() => {
  const previews = document.querySelectorAll('[data-autoplay-preview]');
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');

  const updatePlayback = () => {
    previews.forEach((preview) => {
      if (reducedMotion.matches) {
        preview.pause();
        preview.currentTime = 0;
        return;
      }

      preview.play().catch(() => {
        // The poster remains visible if the browser blocks autoplay.
      });
    });
  };

  updatePlayback();
  reducedMotion.addEventListener('change', updatePlayback);
})();
