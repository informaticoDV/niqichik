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
        fields = ['precio', 'stock', 'descripcion', 'imagen', 'imagen2']
        widgets = {
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'imagen2': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
