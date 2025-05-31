from django.db.models import Sum
from django.shortcuts import render
from .models import Producto
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Producto
from .forms import ProductoForm
from django.db.models import Q

def home(request):
    query = request.GET.get("q", "")
    if query:
        productos = Producto.objects.filter(
            Q(nombre__icontains=query) | Q(descripcion__icontains=query)
        )
    else:
        productos = Producto.objects.all()

    return render(request, 'tienda/home.html', {
        'productos': productos,
        'query': query,
    })



def tienda(request):
    query = request.GET.get("q", "")
    if query:
        productos = Producto.objects.filter(
            Q(nombre__icontains=query) | Q(descripcion__icontains=query)
        )
    else:
        productos = Producto.objects.all()

    return render(request, 'tienda/tienda.html', {
        'productos': productos,
        'query': query,
    })


def buscarProducto(request):
    productos = Producto.objects.all()
    return render(request, 'tienda/home.html', {'productos': productos})

@login_required
def agregar_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.vendedor = request.user
            producto.save()
            return redirect('tienda')
    else:
        form = ProductoForm()
    return render(request, 'tienda/agregar.html', {'form': form})

@login_required
def editar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id, vendedor=request.user)
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('tienda')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'tienda/editar.html', {'form': form, 'producto': producto})

@login_required
def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id, vendedor=request.user)
    if request.method == 'POST':
        producto.delete()
        return redirect('tienda')
    return render(request, 'producto/eliminar_confirmacion.html', {'producto': producto})



def dashboard(request):
    total_invertido = Producto.objects.aggregate(Sum('costo'))['costo__sum'] or 0
    total_vendido = Producto.objects.aggregate(Sum('vendido'))['vendido__sum'] or 0
    return render(request, 'tu_template.html', {
        'total_invertido': total_invertido,
        'total_vendido': total_vendido
    })

from django.views.decorators.http import require_POST
from django.shortcuts import redirect

@require_POST
def reiniciar_totales(request):
    Producto.objects.update(costo=0, vendido=0)
    return redirect('dashboard')  # o donde muestres el resumen

# views.py
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # redirige a donde tú quieras
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# views.py

from django.shortcuts import get_object_or_404, redirect
from .models import Producto
from django.contrib.auth.decorators import login_required

@login_required
def marcar_agotado(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id, vendedor=request.user)
    producto.estado = False
    producto.save()
    return redirect('tienda')  # Reemplaza con el nombre real de tu vista principal

@login_required
def marcar_disponible(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id, vendedor=request.user)
    producto.estado = True
    producto.save()
    return redirect('tienda')  # Reemplaza con el nombre real de tu vista principal

