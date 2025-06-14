"""
URL configuration for Niqichik project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
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


    path('nuevoproducto', views.home, name='cargarProducto'),
    path('buscar', views.home, name='buscarProducto'),
    path('reiniciar/', views.reiniciar_totales, name='reiniciar_totales'),
    path('accounts/', include('allauth.urls')),  # Login/registro con Google
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)