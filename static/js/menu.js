function toggleMenu() {
    const menu = document.getElementById("menuDerecho");
    menu.classList.toggle("abierto");
  }

  document.body.addEventListener('htmx:afterRequest', function (event) {
  const xhr = event.detail.xhr;

  // Si la respuesta fue exitosa
  if (xhr.status === 204 || xhr.status === 200) {
    const form = event.target.closest("form");
    if (!form || !form.id) return;

    const partes = form.id.split("-");
    if (partes.length < 3) return;

    const campo = partes[1];
    const productoId = partes[2];

    // Actualizar valor en la tabla
    const input = form.querySelector(`[name="${campo}"]`);
    if (input) {
      const nuevoValor = input.options ? input.options[input.selectedIndex].text : input.value;
      const valorDiv = document.getElementById(`valor-${campo}-${productoId}`);
      if (valorDiv) {
        valorDiv.textContent = nuevoValor;
      }
    }

    // Cerrar modal correctamente
    const modalElement = form.closest(".modal");
    if (modalElement) {
      // Forzar cierre usando Bootstrap
      const modalInstance = bootstrap.Modal.getInstance(modalElement) || new bootstrap.Modal(modalElement);
      modalInstance.hide();

      // Esperamos un poco y limpiamos todo manualmente
      setTimeout(() => {
        modalElement.classList.remove("show");
        modalElement.setAttribute("aria-hidden", "true");
        modalElement.removeAttribute("aria-modal");
        modalElement.style.display = "none";

        document.body.classList.remove("modal-open");
        document.body.style.overflow = "auto";  // Esto es clave
        document.body.style.paddingRight = "";

        // Remueve backdrop si quedó pegado
        document.querySelectorAll(".modal-backdrop").forEach(b => b.remove());
      }, 300); // Espera el tiempo de la animación
    }
  }

});