from django.shortcuts import render, get_object_or_404, redirect
from .models import Receta
from .forms import RecetaForm

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
