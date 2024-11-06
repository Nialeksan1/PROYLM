from django.contrib import admin
from django.urls import path, include  # Aquí se importa 'include'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('recetas/', include('recetas.urls')),  # Incluye las URLs de la app 'recetas'
]
