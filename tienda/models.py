from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = CloudinaryField('image', blank=True, null=True)
    estado = models.BooleanField(default=True)  # True: disponible, False: agotado
    vendedor = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.nombre

class Pedido(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    comprador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comprador')
    fecha_pedido = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Pedido de {self.producto} por {self.comprador}'