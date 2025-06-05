from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

# models.py
class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField ()
    vendidos = models.IntegerField (default=0)  # 👍 Perfecto
    imagen = CloudinaryField('Producto Original', blank=True, null=True)
    imagen2 = CloudinaryField('Producto Puesto', blank=True, null=True)
    estado = models.BooleanField(default=True)
    vendedor = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre


class Informacion(models.Model):
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_venta = models.DateTimeField(auto_now_add=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    vendedor = models.ForeignKey(User, on_delete=models.CASCADE)  # Necesario

    def __str__(self):
        return f"{self.producto.nombre} - ${self.precio}"


class Pedido(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    comprador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comprador')
    fecha_pedido = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Pedido de {self.producto} por {self.comprador}'