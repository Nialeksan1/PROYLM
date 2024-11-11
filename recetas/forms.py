from django import forms
from .models import Receta
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RecetaForm(forms.ModelForm):
    class Meta:
        model = Receta
        fields = ['nombre', 'ingredientes', 'preparacion', 'tiempo_preparacion', 'dificultad', 'etiquetas']

class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']




class RecetaForm(forms.ModelForm):
    class Meta:
        model = Receta
        fields = ['nombre', 'ingredientes', 'preparacion', 'tiempo_preparacion', 'dificultad', 'etiquetas']
        widgets = {
            'ingredientes': forms.Textarea(attrs={'cols': 80, 'rows': 5}),  # Mejora la visualización para los ingredientes
            'preparacion': forms.Textarea(attrs={'cols': 80, 'rows': 10}),  # Mejora la visualización para la descripción de la preparación
            'etiquetas': forms.Textarea(attrs={'cols': 80, 'rows': 3}),  # Mejora la visualización para las etiquetas (aunque es un campo de texto)
        }