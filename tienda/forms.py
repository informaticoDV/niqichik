# forms.py

from django import forms
from .models import Producto

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'precio', 'descripcion', 'imagen']  # Asegúrate de incluir todos los que quieres editar

class EditarProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['precio', 'descripcion']  # Asegúrate de incluir todos los que quieres editar