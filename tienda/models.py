from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.utils.text import slugify
from django.urls import reverse

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    codigo = models.CharField(max_length=6, unique=True, editable=False, null=True, blank=True)
    nombre = models.CharField(max_length=100)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    vendidos = models.IntegerField(default=0)
    imagen = CloudinaryField('Producto Original', blank=True, null=True)
    imagen2 = CloudinaryField('Producto Puesto', blank=True, null=True)
    estado = models.BooleanField(default=True)
    visible = models.BooleanField(default=True)
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
    def total_likes(self):
        return self.likes.count()

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


class Like(models.Model):
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE, related_name='likes')
    session_key = models.CharField(max_length=40)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('producto', 'session_key')

class NotificacionInteres(models.Model):
    productos = models.ManyToManyField(Producto)
    comprador_nombre = models.CharField(max_length=100)
    comprador_contacto = models.CharField(max_length=100, blank=True, null=True)  # WhatsApp o email
    fecha = models.DateTimeField(auto_now_add=True)
    procesado = models.BooleanField(default=False)

    def __str__(self):
        return f"Interés de {self.comprador_nombre} el {self.fecha.strftime('%d-%m-%Y %H:%M')}"

class Venta(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('aceptada', 'Aceptada'),
        ('cancelada', 'Cancelada'),
    ]

    comprador_nombre = models.CharField(max_length=100)
    comprador_contacto = models.CharField(max_length=100, blank=True, null=True)  # WhatsApp/email
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')

    def __str__(self):
        return f"Venta #{self.id} - {self.comprador_nombre} ({self.estado})"


class VentaDetalle(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"

