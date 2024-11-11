
from django.db import models
from django.contrib.auth.models import User

class Receta(models.Model):
    nombre = models.CharField(max_length=100)
    ingredientes = models.TextField()
    preparacion = models.TextField()
    tiempo_preparacion = models.IntegerField()  # En minutos
    dificultad = models.CharField(max_length=50, choices=[
        ('fácil', 'Fácil'),
        ('intermedia', 'Intermedia'),
        ('difícil', 'Difícil')
    ])
    etiquetas = models.CharField(max_length=200, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    favoritos = models.ManyToManyField(User, related_name='favoritas', blank=True)
    def __str__(self):
        return self.nombre
