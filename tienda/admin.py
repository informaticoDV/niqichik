from django.contrib import admin
from .models import Producto, Pedido, Informacion, Categoria, Venta

admin.site.register(Producto)
admin.site.register(Pedido)
admin.site.register(Informacion)
admin.site.register(Categoria)
admin.site.register(Venta)
