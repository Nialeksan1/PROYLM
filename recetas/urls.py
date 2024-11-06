from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_recetas, name='lista_recetas'),
    path('<int:pk>/', views.detalle_receta, name='detalle_receta'),
    path('nueva/', views.nueva_receta, name='nueva_receta'),
    path('<int:pk>/editar/', views.editar_receta, name='editar_receta'),
    path('<int:pk>/eliminar/', views.eliminar_receta, name='eliminar_receta'),
]
