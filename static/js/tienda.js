    const imagenModal = document.getElementById('imagenModal');
    const imagenModalSrc = document.getElementById('imagenModalSrc');
    const prevBtn = document.getElementById('prevImage');
    const nextBtn = document.getElementById('nextImage');

    let currentImageIndex = 0;
    let imageUrls = [];

    // Captura todas las imágenes clickeables
    const allImgElements = document.querySelectorAll('.img-clickable');
    allImgElements.forEach(img => {
      imageUrls.push(img.getAttribute('data-img-url'));
    });

    // Mostrar imagen en el modal
    imagenModal.addEventListener('show.bs.modal', function (event) {
      const trigger = event.relatedTarget;
      const url = trigger.getAttribute('data-img-url');
      currentImageIndex = imageUrls.indexOf(url);
      imagenModalSrc.src = url;
    });

    // Botón anterior
    prevBtn.addEventListener('click', () => {
      currentImageIndex = (currentImageIndex - 1 + imageUrls.length) % imageUrls.length;
      imagenModalSrc.src = imageUrls[currentImageIndex];
    });

    // Botón siguiente
    nextBtn.addEventListener('click', () => {
      currentImageIndex = (currentImageIndex + 1) % imageUrls.length;
      imagenModalSrc.src = imageUrls[currentImageIndex];
    });