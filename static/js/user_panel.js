// Seleccionar elementos necesarios
const videoItems = document.querySelectorAll('.video-item');
const videoModal = new bootstrap.Modal(document.getElementById('videoModal'));
const videoPlayer = document.querySelector('.video-player');

// Añadir eventos a los videos
videoItems.forEach(item => {
  item.addEventListener('click', () => {
    const videoSrc = item.getAttribute('data-video');

    // Cambiar la fuente del reproductor
    videoPlayer.querySelector('source').src = videoSrc;
    videoPlayer.load();
    videoPlayer.play();

    // Mostrar el modal
    videoModal.show();
  });
});

// Pausar el video cuando se cierra el modal
document.getElementById('videoModal').addEventListener('hidden.bs.modal', () => {
  videoPlayer.pause();
});
