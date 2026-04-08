# gestor_recetas/urls.py
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from recetas import views  # Importa las vistas de la app 'recetas'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('recetas/', include('recetas.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('registro/', views.registro, name='registro'),
    path('home/', views.home, name='home'),
    path('cerrar-sesion/', views.cerrar_sesion, name='cerrar_sesion'),
    path('', RedirectView.as_view(url='/accounts/login/', permanent=False)),
]
