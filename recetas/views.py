from django.core.paginator import Paginator
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from .models import Receta
from .forms import RecetaForm, RegistroForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def lista_recetas(request):
    recetas = Receta.objects.select_related('user').all()
    query = request.GET.get('q')
    if query:
        recetas = recetas.filter(nombre__icontains=query)
    paginator = Paginator(recetas, 12)
    page = request.GET.get('page')
    recetas = paginator.get_page(page)
    return render(request, 'recetas/lista.html', {'recetas': recetas, 'query': query or ''})


def detalle_receta(request, pk):
    receta = get_object_or_404(Receta.objects.select_related('user').prefetch_related('favoritos'), pk=pk)
    return render(request, 'recetas/detalle_receta.html', {'receta': receta})


@login_required
def nueva_receta(request):
    if request.method == 'POST':
        form = RecetaForm(request.POST)
        if form.is_valid():
            receta = form.save(commit=False)
            receta.user = request.user
            receta.save()
            messages.success(request, 'Receta creada correctamente.')
            return redirect('home')
    else:
        form = RecetaForm()
    return render(request, 'recetas/nueva_receta.html', {'form': form})


@login_required
def editar_receta(request, pk):
    receta = get_object_or_404(Receta, pk=pk)

    if receta.user != request.user:
        return HttpResponseForbidden('No tienes permiso para editar esta receta.')

    if request.method == 'POST':
        form = RecetaForm(request.POST, instance=receta)
        if form.is_valid():
            form.save()
            messages.success(request, 'Receta actualizada correctamente.')
            return redirect('detalle_receta', pk=receta.pk)
    else:
        form = RecetaForm(instance=receta)

    return render(request, 'recetas/editar_receta.html', {'form': form, 'receta': receta})


@login_required
def eliminar_receta(request, pk):
    receta = get_object_or_404(Receta, pk=pk)

    if receta.user != request.user:
        return HttpResponseForbidden('No tienes permiso para eliminar esta receta.')

    if request.method == 'POST':
        receta.delete()
        messages.success(request, 'Receta eliminada correctamente.')
        return redirect('lista_recetas')

    return render(request, 'recetas/eliminar_receta.html', {'receta': receta})


def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Cuenta creada exitosamente.')
            return redirect('home')
    else:
        form = RegistroForm()
    return render(request, 'recetas/registro.html', {'form': form})


def iniciar_sesion(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'recetas/iniciar_sesion.html', {'form': form})


@require_POST
def cerrar_sesion(request):
    logout(request)
    return redirect('login')


@login_required
def home(request):
    mis_recetas = Receta.objects.filter(user=request.user)
    favoritas = Receta.objects.filter(favoritos=request.user).select_related('user')
    return render(request, 'recetas/home.html', {
        'mis_recetas': mis_recetas,
        'favoritas': favoritas,
    })


@login_required
@require_POST
def agregar_favorito(request, pk):
    receta = get_object_or_404(Receta, pk=pk)
    receta.favoritos.add(request.user)
    messages.success(request, f'"{receta.nombre}" agregada a favoritos.')
    return redirect('detalle_receta', pk=receta.pk)


@login_required
@require_POST
def quitar_favorito(request, pk):
    receta = get_object_or_404(Receta, pk=pk)
    receta.favoritos.remove(request.user)
    messages.info(request, f'"{receta.nombre}" eliminada de favoritos.')
    return redirect('detalle_receta', pk=receta.pk)
