# gestor_recetas/urls.py
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from recetas import views  # Importa las vistas de la app 'recetas'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('recetas/', include('recetas.urls')),  # Incluye las URLs de la app de recetas
    path('accounts/', include('django.contrib.auth.urls')),  # Agrega URLs de autenticación de Django
    path('registro/', views.registro, name='registro'),  # Ruta para la vista de registro
    path('', RedirectView.as_view(url='/accounts/login/', permanent=False)),  # Redirige la URL raíz a la página de login
       path('home/', views.home, name='home'),
]
