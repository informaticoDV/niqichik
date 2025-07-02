from .models import Venta

def ventas_pendientes_count(request):
    if request.user.is_authenticated:
        count = Venta.objects.filter(estado='pendiente').count()
        return {'ventas_pendientes': count}
    return {'ventas_pendientes': 0}
