document.querySelectorAll('.btn-like').forEach(btn => {
  btn.addEventListener('click', function () {
    const productoId = this.dataset.productoId;
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch(`/like/${productoId}/`, {
      method: 'POST',
      headers: {
        'X-CSRFToken': csrfToken,
        'Accept': 'application/json'
      }
    })
    .then(res => res.json())
    .then(data => {
      const likeCountSpan = this.querySelector('.like-count');
      likeCountSpan.textContent = data.liked ? ' ' : 'Me gusta';
    })
    .catch(err => console.error(err));
  });
});

document.addEventListener("DOMContentLoaded", function () {
  const botones = document.querySelectorAll(".btn-agregar-carrito");
  botones.forEach(boton => {
    boton.addEventListener("click", function () {
      const productoId = this.getAttribute("data-producto-id");

      fetch(URL_AGREGAR_CARRITO, {
        method: "POST",
        headers: {
          "X-CSRFToken": CSRF_TOKEN,
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: `producto_id=${productoId}`
      })
      .then(response => response.json())
      .then(data => {
        if (data.ok) {
          mostrarAlerta(`✔ ${data.nombre} añadido al carrito`);
          actualizarContadorCarrito();
        }
      })
      .catch(err => console.error(err));
    });
  });

  actualizarContadorCarrito();

  function mostrarAlerta(mensaje) {
    const alerta = document.getElementById("alerta-carrito");
    alerta.innerHTML = `
      ${mensaje} <br>
      <a href="${URL_VER_CARRITO}" class="btn btn-sm btn-light mt-2">🛒 Ver carrito</a>
    `;
    alerta.style.display = "block";
    setTimeout(() => {
      alerta.style.display = "none";
      alerta.innerHTML = "";
    }, 3000);
  }

  function actualizarContadorCarrito() {
    fetch(URL_TOTAL_CARRITO)
      .then(response => response.json())
      .then(data => {
        const contador = document.getElementById("contador-carrito");
        if (contador) {
          contador.textContent = data.total;
        }
      })
      .catch(err => console.error(err));
  }

  const eliminarLinks = document.querySelectorAll(".btn-eliminar-carrito");
  eliminarLinks.forEach(link => {
    link.addEventListener("click", function (e) {
      if (!confirm("¿Estás seguro que deseas eliminar este producto?")) {
        e.preventDefault();
      } else {
        setTimeout(() => actualizarContadorCarrito(), 500);
      }
    });
  });

  // Modal de imágenes
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
});
