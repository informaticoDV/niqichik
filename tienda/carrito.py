class Carrito:
    def __init__(self, request):
        self.session = request.session
        carrito = self.session.get("carrito")

        if not carrito:
            carrito = self.session["carrito"] = {}

        self.carrito = carrito

    def agregar(self, producto):
        producto_id = str(producto.id)
        if producto_id not in self.carrito:
            self.carrito[producto_id] = {
                "nombre": producto.nombre,
                "precio": str(producto.precio),
                "cantidad": 1,
                "imagen": producto.imagen.url if producto.imagen else "",
                "codigo": producto.codigo,  # ✅ AÑADE ESTA LÍNEA
            }
        else:
            self.carrito[producto_id]["cantidad"] += 1
        self.guardar()

    def eliminar(self, producto):
        producto_id = str(producto.id)
        if producto_id in self.carrito:
            del self.carrito[producto_id]
            self.guardar()

    def limpiar(self):
        self.session["carrito"] = {}
        self.session.modified = True

    def guardar(self):
        self.session["carrito"] = self.carrito
        self.session.modified = True
