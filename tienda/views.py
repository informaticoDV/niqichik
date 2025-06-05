from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from .forms import ProductoForm, EditarProductoForm
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Producto, Informacion

def home(request):
    query = request.GET.get("q", "")
    if query:
        productos = Producto.objects.filter(
            Q(nombre__icontains=query) | Q(descripcion__icontains=query)
        )
    else:
        productos = Producto.objects.all()

    paginator = Paginator(productos, 8)  # 8 productos por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'tienda/home.html', {
        'page_obj': page_obj,
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

    paginator = Paginator(productos, 8)  # 8 productos por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'tienda/tienda.html', {
        'page_obj': page_obj,
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
        form = EditarProductoForm(request.POST, request.FILES, instance=producto)
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
    return render(request, 'tienda/eliminar_confirmacion.html', {'producto': producto})

# views.py
from .models import Producto, Informacion
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages  # Asegúrate de importar esto

@login_required
def vender_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id, vendedor=request.user)

    if request.method == 'POST':
        if producto.stock > 0:
            producto.stock -= 1
            producto.vendidos += 1
            producto.save()
            messages.success(request, "Producto vendido correctamente.")
        else:
            messages.error(request, "No se puede vender. El producto no tiene stock.")

        return redirect('tienda')

    return render(request, 'tienda/tienda.html', {'producto': producto})


from .models import Informacion
from django.db.models import Sum

from .models import Producto
from django.db.models import F, Sum, ExpressionWrapper, DecimalField

@login_required
def dashboard(request):
    productos = Producto.objects.filter(vendedor=request.user)

    # Calcula ganancia = (precio) * vendidos
    ganancia_total = productos.annotate(
        ganancia_unitaria=ExpressionWrapper(
            F('precio'),
            output_field=DecimalField(max_digits=10, decimal_places=2)
        ),
        ganancia_total=ExpressionWrapper(
            ((F('precio') * F('vendidos'))),
            output_field=DecimalField(max_digits=10, decimal_places=2)
        )
    ).aggregate(total=Sum('ganancia_total'))['total'] or 0


    return render(request, 'tienda/dashboard.html', {
        'monto_ganado': ganancia_total,
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

