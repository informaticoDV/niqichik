from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

from tienda import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),  # <-- esto importa las vistas como login/logout
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('', views.home, name='home'),
    path('Mitienda', views.tienda, name='tienda'),
    path('tienda/agregar/', views.agregar_producto, name='agregar_producto'),
    path('tienda/<int:producto_id>/editar/', views.editar_producto, name='editar_producto'),
    path('tienda/<int:producto_id>/editar/<str:campo>/', views.editar_campo_producto, name='editar_campo_producto'),
    path('tienda/<int:producto_id>/eliminar/', views.eliminar_producto, name='eliminar_producto'),
    path('producto/<int:producto_id>/agotado/', views.marcar_agotado, name='marcar_agotado'),
    path('producto/<int:producto_id>/disponible/', views.marcar_disponible, name='marcar_disponible'),
    path('producto/<int:producto_id>/invisible/', views.marcar_invisible, name='marcar_invisible'),
    path('producto/<int:producto_id>/visible/', views.marcar_visible, name='marcar_visible'),
    path('producto/<int:producto_id>/vender/', views.vender_producto, name='vender_producto'),
    path('informacion/', views.dashboard, name='dashboard'),
    path('producto/<slug:slug>/', views.detalle_producto, name='detalle_producto'),
    path('categoria/', views.categoria, name='categoria'),
    path('categoria/agregar/', views.agregar_categoria, name='agregar_categoria'),
    path('categoria/eliminar/<int:categoria_id>/', views.eliminar_categoria, name='eliminar_categoria'),
    path("carrito/", views.ver_carrito, name="ver_carrito"),
    path("carrito/eliminar/<int:producto_id>/", views.eliminar_del_carrito, name="eliminar_del_carrito"),
    path("carrito/ajax/agregar/", views.ajax_agregar_al_carrito, name="ajax_agregar_al_carrito"),
    path("carrito/ajax/total/", views.obtener_total_carrito, name="obtener_total_carrito"),
    path("carrito/actualizar/<str:key>/", views.actualizar_cantidad, name="actualizar_cantidad"),
    path('guardar-informacion/', views.guardar_informacion, name='guardar_informacion'),
    path('like/<int:producto_id>/', views.toggle_like, name='toggle_like'),
    path('ventas/', views.lista_ventas, name='lista_ventas'),
    path('ventas/<int:venta_id>/cambiar-estado/<str:nuevo_estado>/', views.cambiar_estado_venta,
         name='cambiar_estado_venta'),
    path('crear-venta/', views.crear_venta, name='crear_venta'),

]

handler404 = 'tienda.views.mi_error_404'

# Niqichik/urls.py (el archivo principal de urls)

handler404 = 'tienda.views.mi_error_404'


if not settings.DEBUG:
    urlpatterns += [
        re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    ]
else:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)