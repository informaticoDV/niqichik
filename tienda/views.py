from django.template.loader import render_to_string
from .forms import *
from django.core.paginator import Paginator
from django.contrib import messages  # Asegúrate de importar esto
from django.db.models import F, Sum, ExpressionWrapper, DecimalField
from django.contrib.auth.decorators import login_required
from django.db.models import Q, IntegerField
from django.db.models.functions import Substr, Length, Cast
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .models import Producto, Categoria
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from .forms import ProductoForm
from .carrito import Carrito

def home(request):
    query = request.GET.get("q", "")
    categoria_id = request.GET.get("categoria", "")
    disponible = request.GET.get("disponible", "")

    productos_base = Producto.objects.filter(visible=True).annotate(
        slug_len=Length("slug"),
        number_part=Cast(
            Substr("slug", Length("slug") - 5, 6),
            IntegerField()
        )
    )

    if query:
        productos_base = productos_base.filter(
            Q(nombre__icontains=query) | Q(descripcion__icontains=query)
        )

    if categoria_id:
        productos_base = productos_base.filter(categoria_id=categoria_id)

    if disponible == "1":
        productos_base = productos_base.filter(estado=True)  # suponiendo que 'estado=True' significa disponible


    productos = productos_base.order_by("-number_part")

    paginator = Paginator(productos, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Calcular el rango de páginas (máximo 6)
    current_page = page_obj.number
    total_pages = paginator.num_pages

    start_page = max(current_page - 2, 1)
    end_page = start_page + 6
    if end_page > total_pages:
        end_page = total_pages
        start_page = max(end_page - 6, 1)

    page_range_custom = range(start_page, end_page + 1)

    categorias = Categoria.objects.all()  # Traemos las categorías para el filtro

    return render(request, 'tienda/home.html', {
        'page_obj': page_obj,
        'query': query,
        'categorias': categorias,
        'categoria_id': categoria_id,
        'disponible': disponible,  # <-- aquí
        'page_range_custom': page_range_custom,  # <--- nuevo
    })

def tienda(request):
    query = request.GET.get("q", "")
    categoria_id = request.GET.get("categoria", "")
    disponible = request.GET.get("disponible", "")

    productos_base = Producto.objects.annotate(
        slug_len=Length("slug"),
        number_part=Cast(
            Substr("slug", Length("slug") - 5, 6),
            IntegerField()
        )
    )

    if query:
        productos_base = productos_base.filter(
            Q(nombre__icontains=query) | Q(descripcion__icontains=query)
        )

    if categoria_id:
        productos_base = productos_base.filter(categoria_id=categoria_id)


    if disponible == "1":
        productos_base = productos_base.filter(estado=True)  # suponiendo que 'estado=True' significa disponible

    productos = productos_base.order_by("-number_part")

    paginator = Paginator(productos, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Calcular el rango de páginas (máximo 6)
    current_page = page_obj.number
    total_pages = paginator.num_pages

    start_page = max(current_page - 2, 1)
    end_page = start_page + 6
    if end_page > total_pages:
        end_page = total_pages
        start_page = max(end_page - 6, 1)

    page_range_custom = range(start_page, end_page + 1)

    categorias = Categoria.objects.all()  # Traemos las categorías para el filtro

    return render(request, 'tienda/tienda.html', {
        'page_obj': page_obj,
        'query': query,
        'categorias': categorias,
        'categoria_id': categoria_id,
        'disponible': disponible,  # <-- aquí
        'page_range_custom': page_range_custom,  # <--- nuevo
    })

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
        form = EditarProductoForm(instance=producto)  # Cambié ProductoForm por EditarProductoForm
    return render(request, 'tienda/editar.html', {'form': form, 'producto': producto})

@login_required
def editar_campo_producto(request, producto_id, campo):
    producto = get_object_or_404(Producto, pk=producto_id)

    if campo not in ProductoForm().fields:
        return HttpResponseBadRequest("Campo no válido")

    class CampoForm(forms.ModelForm):
        class Meta:
            model = Producto
            fields = [campo]

    if request.method == "POST":
        form = CampoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            # Retornar el fragmento del modal con success=True
            html_form = render_to_string('tienda/editar_campo_modal.html', {
                'form': form,
                'producto': producto,
                'campo': campo,
                'success': True,
            }, request=request)
            return HttpResponse(status=204)  # ✅ Esto es clave

    else:
        form = CampoForm(instance=producto)

    return render(request, 'tienda/editar_formulario_campo.html', {
        'form': form,
        'producto': producto,
        'campo': campo,
    })

@login_required
def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id, vendedor=request.user)
    if request.method == 'POST':
        producto.delete()
        return redirect('tienda')
    return render(request, 'tienda/eliminar_confirmacion.html', {'producto': producto})

@login_required
def categoria(request):
    categoria = Categoria.objects.all()
    return render(request, 'tienda/categoria.html', {'categoria': categoria})

@login_required
def agregar_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()  # ✅ Guarda directamente
            return redirect('categoria')  # O el nombre correcto de la URL
    else:
        form = CategoriaForm()
    return render(request, 'tienda/agregar_categoria.html', {'form': form})

@login_required
def eliminar_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    if request.method == 'POST':
        categoria.delete()
        return redirect('categoria')
    return render(request, 'tienda/eliminar_confirmacion.html', {'categoria': categoria})

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

        next_url = request.POST.get('next', 'tienda')  # url por defecto si no viene next
        return redirect(next_url)

    return render(request, 'tienda/tienda.html', {'producto': producto})

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

@login_required
def marcar_disponible(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id, vendedor=request.user)
    producto.estado = True
    producto.save()
    next_url = request.POST.get('next', '/')
    return redirect(next_url)

@require_POST
def marcar_agotado(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    producto.estado = False  # marca como agotado
    producto.save()

    next_url = request.POST.get('next', '/')
    return redirect(next_url)

@login_required
def marcar_visible(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id, vendedor=request.user)
    producto.visible = True
    producto.save()
    next_url = request.POST.get('next', '/')
    return redirect(next_url)

@require_POST
def marcar_invisible(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    producto.visible = False  # marca como agotado
    producto.save()

    next_url = request.POST.get('next', '/')
    return redirect(next_url)

def detalle_producto(request, slug):
    producto = get_object_or_404(Producto, slug=slug)
    url_absoluta = request.build_absolute_uri(producto.get_absolute_url())
    return render(request, 'tienda/detalle_producto.html', {
        'producto': producto,
        'url_absoluta': url_absoluta,
    })

from django.shortcuts import redirect
from django.urls import reverse

def agregar_al_carrito(request, producto_id):
    carrito = Carrito(request)
    producto = get_object_or_404(Producto, id=producto_id)
    carrito.agregar(producto)

    # Redirige a la misma página desde la que vino el usuario
    messages.success(request, f"{producto.nombre} fue añadido al carrito.")
    return redirect(request.META.get("HTTP_REFERER", reverse("home")))



def eliminar_del_carrito(request, producto_id):
    carrito = Carrito(request)
    producto = get_object_or_404(Producto, id=producto_id)
    carrito.eliminar(producto)
    return redirect("ver_carrito")

def ver_carrito(request):
    carrito = request.session.get("carrito", {})
    total = sum(float(item["precio"]) * item["cantidad"] for item in carrito.values())
    return render(request, "tienda/carrito.html", {
        "carrito": carrito,
        "total": total
    })

from django.http import JsonResponse
from .carrito import Carrito
from .models import Producto

def ajax_agregar_al_carrito(request):
    if request.method == "POST":
        producto_id = request.POST.get("producto_id")
        producto = Producto.objects.get(id=producto_id)
        carrito = Carrito(request)
        carrito.agregar(producto)
        return JsonResponse({"ok": True, "nombre": producto.nombre})
    return JsonResponse({"ok": False}, status=400)


def obtener_total_carrito(request):
    carrito = request.session.get("carrito", {})
    total_items = sum(item["cantidad"] for item in carrito.values())
    return JsonResponse({"total": total_items})