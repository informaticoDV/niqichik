# forms.py

from django import forms
from .models import Producto, Categoria

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'categoria', 'precio','stock','descripcion', 'imagen', 'imagen2']  # Asegúrate de incluir todos los que quieres editar
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),  # <- CORREGIDO aquí
            'categoria': forms.Select(attrs={'class': 'form-control'}),  # <- CORREGIDO aquí
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'imagen2': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class EditarProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre','categoria', 'precio', 'stock', 'descripcion', 'imagen', 'imagen2']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),  # <- CORREGIDO aquí
            'categoria': forms.Select(attrs={'class': 'form-control'}),  # <- CORREGIDO aquí
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'imagen2': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion']  # Asegúrate de incluir todos los que quieres editar