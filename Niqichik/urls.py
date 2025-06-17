from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
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
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)