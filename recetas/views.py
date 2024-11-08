from django.shortcuts import render, get_object_or_404, redirect
from .models import Receta
from .forms import RecetaForm, RegistroForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages

def lista_recetas(request):
    recetas = Receta.objects.all()
    return render(request, 'recetas/lista.html', {'recetas': recetas})

def detalle_receta(request, pk):
    receta = get_object_or_404(Receta, pk=pk)
    return render(request, 'recetas/detalle.html', {'receta': receta})

def nueva_receta(request):
    if request.method == "POST":
        form = RecetaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_recetas')
    else:
        form = RecetaForm()
    return render(request, 'recetas/editar.html', {'form': form})

def editar_receta(request, pk):
    receta = get_object_or_404(Receta, pk=pk)
    if request.method == "POST":
        form = RecetaForm(request.POST, instance=receta)
        if form.is_valid():
            form.save()
            return redirect('detalle_receta', pk=receta.pk)
    else:
        form = RecetaForm(instance=receta)
    return render(request, 'recetas/editar.html', {'form': form})

def eliminar_receta(request, pk):
    receta = get_object_or_404(Receta, pk=pk)
    receta.delete()
    return redirect('lista_recetas')

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Inicia sesión automáticamente después de registrarse
            messages.success(request, 'Cuenta creada exitosamente. Ahora puedes usar la aplicación.')
            return redirect('home')  # Redirige a la página principal
    else:
        form = RegistroForm()
    return render(request, 'recetas/registro.html', {'form': form})

def iniciar_sesion(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'recetas/iniciar_sesion.html', {'form': form})

def cerrar_sesion(request):
    logout(request)
    return redirect('home')
