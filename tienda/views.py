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
from .models import Producto, Categoria, Venta, VentaDetalle
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
    visible = request.GET.get("visible", "")

    productos_base = Producto.objects.annotate(
        slug_len=Length("slug"),
        number_part=Cast(
            Substr("slug", Length("slug") - 5, 6),
            IntegerField()
        )
    )

    if query:
        productos_base = productos_base.filter(
            Q(nombre__icontains=query) | Q(descripcion__icontains=query)| Q(slug__icontains=query)
        )

    if categoria_id:
        productos_base = productos_base.filter(categoria_id=categoria_id)


    if disponible == "1":
        productos_base = productos_base.filter(estado=True)

    if visible == "1":
        productos_base = productos_base.filter(visible=True)

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
        'disponible': disponible,
        'visible': visible,
        'page_range_custom': page_range_custom,
    })


# tienda/views.py

from django.shortcuts import render

def mi_error_404(request, exception):
    # Puedes pasar contexto si quieres, aquí va vacío
    return render(request, 'errors/404.html', status=404)



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
            # 🔁 Solo devolvemos el nuevo valor a reemplazar en pantalla
            return render(request, 'tienda/fragmento_valor_campo.html', {
                'producto': producto,
                'campo': campo,
            })

    else:
        form = CampoForm(instance=producto)

    return render(request, 'tienda/editar_campo_modal.html', {
        'form': form,
        'producto': producto,
        'campo': campo,
        'success': False,
    })




@login_required
def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id, vendedor=request.user)
    if request.method == 'POST':
        producto.delete()
        return redirect('tienda')

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

@login_required
def vender_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id, vendedor=request.user)

    if request.method == 'POST':
        if producto.stock > 0:
            producto.stock -= 1
            producto.vendidos += 1
            # Cambiar estado a 0 si stock llega a 0
            if producto.stock == 0:
                producto.estado = 0  # o False si es BooleanField

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

    ganancia_total = productos.annotate(
        ganancia_total=ExpressionWrapper(
            F('precio') * F('vendidos'),
            output_field=DecimalField(max_digits=10, decimal_places=2)
        )
    ).aggregate(total=Sum('ganancia_total'))['total'] or 0

    historial = Informacion.objects.filter(vendedor=request.user).order_by('-fecha_venta')

    return render(request, 'tienda/dashboard.html', {
        'monto_ganado': ganancia_total,
        'historial': historial
    })


from django.utils import timezone
from .models import Informacion

@login_required
def guardar_informacion(request):
    productos = Producto.objects.filter(vendedor=request.user)

    ganancia_total = productos.annotate(
        ganancia_total=ExpressionWrapper(
            F('precio') * F('vendidos'),
            output_field=DecimalField(max_digits=10, decimal_places=2)
        )
    ).aggregate(total=Sum('ganancia_total'))['total'] or 0

    if ganancia_total > 0:
        Informacion.objects.create(
            precio=ganancia_total,
            producto=productos.first(),  # Asocia cualquiera
            vendedor=request.user
        )

        # Reiniciar contador de ventas
        productos.update(vendidos=0)

    return redirect('dashboard')



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


def eliminar_del_carrito(request, producto_id):
    carrito = Carrito(request)
    producto = get_object_or_404(Producto, id=producto_id)
    carrito.eliminar(producto)
    return redirect("ver_carrito")

from django.shortcuts import get_object_or_404
from tienda.models import Producto  # ajusta según tu estructura
import urllib.parse

def ver_carrito(request):
    carrito = request.session.get("carrito", {})
    texto_compartir = "✨ Mi carrito en Niqi-Chik: ✨\n"
    total = 0
    nuevos_items = {}

    for key, item in carrito.items():
        codigo = item.get('codigo')
        try:
            producto = Producto.objects.get(codigo=codigo)
        except Producto.DoesNotExist:
            continue  # ignorar si el producto ya no existe

        cantidad = int(item.get('cantidad', 0))
        precio = float(item.get('precio', 0))

        # Recalcular subtotal y total
        subtotal = cantidad * precio
        total += subtotal

        # Armar texto de WhatsApp
        texto_compartir += f"• {codigo} || {producto.nombre} x{cantidad} = ${subtotal:.2f}\n"

        # Asegurarse de que cada ítem tenga stock actualizado
        nuevos_items[key] = item
        nuevos_items[key]['stock'] = producto.stock  # ⚠️ clave para el template

    # Actualizar el carrito en la sesión
    request.session['carrito'] = nuevos_items

    texto_compartir += f"Total: ${total:.2f}"
    texto_compartir_url = urllib.parse.quote(texto_compartir)

    return render(request, "tienda/carrito.html", {
        "carrito": nuevos_items,
        "total": total,
        "texto_compartir": texto_compartir_url,
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


from django.shortcuts import redirect
from django.views.decorators.http import require_POST

@require_POST
def actualizar_cantidad(request, key):
    nueva_cantidad = int(request.POST.get("cantidad", 1))
    carrito = request.session.get("carrito", {})

    if key in carrito:
        # Verificar contra el stock
        codigo = carrito[key].get("codigo")
        try:
            producto = Producto.objects.get(codigo=codigo)
            stock_disponible = producto.stock
            carrito[key]["cantidad"] = min(nueva_cantidad, stock_disponible)
        except Producto.DoesNotExist:
            pass

    request.session["carrito"] = carrito
    return redirect("ver_carrito")  # o el nombre que uses para mostrar el carrito




from django.http import JsonResponse
from .models import Producto, Like

def toggle_like(request, producto_id):
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key

    producto = Producto.objects.get(id=producto_id)
    like, created = Like.objects.get_or_create(producto=producto, session_key=session_key)

    if not created:
        like.delete()
        liked = False
    else:
        liked = True

    return JsonResponse({
        'liked': liked,
        'total_likes': producto.likes.count()
    })


from django.contrib import messages
from django.views.decorators.http import require_POST

@require_POST
def crear_venta(request):
    comprador_nombre = request.POST.get("comprador_nombre", "Anónimo")
    comprador_contacto = request.POST.get("comprador_contacto", "")
    productos_ids = request.POST.getlist("productos")
    cantidades = request.POST.getlist("cantidades")
    whatsapp_url = request.POST.get("whatsapp_url")

    venta = Venta.objects.create(
        comprador_nombre=comprador_nombre,
        comprador_contacto=comprador_contacto,
    )

    for pid, cantidad in zip(productos_ids, cantidades):
        try:
            producto_id = int(pid)
            cant = int(cantidad)
            producto = Producto.objects.filter(id=producto_id).first()
            if producto and cant > 0:
                VentaDetalle.objects.create(venta=venta, producto=producto, cantidad=cant)
        except ValueError:
            continue

    # Redirige a WhatsApp directamente
    return redirect(whatsapp_url)


@login_required
def lista_ventas(request):
    ventas = Venta.objects.all().order_by('-fecha_creacion')
    return render(request, 'tienda/lista_ventas.html', {'ventas': ventas})

@login_required
def cambiar_estado_venta(request, venta_id, nuevo_estado):
    venta = get_object_or_404(Venta, id=venta_id)

    if nuevo_estado == 'aceptada':
        # Descontar stock
        for detalle in venta.detalles.all():
            producto = detalle.producto
            if producto.stock >= detalle.cantidad:
                producto.stock -= detalle.cantidad
                producto.vendidos += detalle.cantidad
                if producto.stock == 0:
                    producto.estado = False
                    producto.visible = False
                producto.save()
            else:
                messages.error(request, f"No hay suficiente stock para {producto.nombre}")
                return redirect('lista_ventas')

    venta.estado = nuevo_estado
    venta.save()
    messages.success(request, f"Venta {venta.id} actualizada a {nuevo_estado}.")
    return redirect('lista_ventas')
