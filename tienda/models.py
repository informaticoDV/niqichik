from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.utils.text import slugify
from django.urls import reverse

# models.py
# models.py
class Producto(models.Model):
    codigo = models.CharField(max_length=6, unique=True, editable=False, null=True, blank=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    vendidos = models.IntegerField(default=0)
    imagen = CloudinaryField('Producto Original', blank=True, null=True)
    imagen2 = CloudinaryField('Producto Puesto', blank=True, null=True)
    estado = models.BooleanField(default=True)
    vendedor = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.codigo:
            ultimo = Producto.objects.all().order_by('id').last()
            if not ultimo or not ultimo.codigo:
                nuevo_codigo = "000001"
            else:
                numero = int(ultimo.codigo)
                nuevo_codigo = f"{numero + 1:06d}"
            self.codigo = nuevo_codigo

        if not self.slug:
            self.slug = slugify(f"{self.nombre}-{self.codigo}")
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('detalle_producto', kwargs={'slug': self.slug})

    def __str__(self):
        return f"{self.nombre} ({self.codigo})"

    @property
    def url_absoluta(self):
        return self.get_absolute_url()




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


