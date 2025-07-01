from .models import Venta

def ventas_pendientes_count(request):
    if request.user.is_authenticated and request.user.is_staff:
        count = Venta.objects.filter(estado='pendiente').count()
        return {'ventas_pendientes': count}
    return {'ventas_pendientes': 0}
