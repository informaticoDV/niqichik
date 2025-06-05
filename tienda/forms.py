# forms.py

from django import forms
from .models import Producto

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'precio','stock','descripcion', 'imagen', 'imagen2']  # Asegúrate de incluir todos los que quieres editar

class EditarProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['precio', 'stock', 'imagen' , 'imagen2']  # Asegúrate de incluir todos los que quieres editar