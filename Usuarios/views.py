from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from .forms import UsuarioForm, UsuarioUpdateForm
from . import services

def is_superuser(user):
    return user.is_authenticated and user.is_superuser

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'login.html', {'error': 'Credenciales inválidas'})
    return render(request, 'login.html')

@login_required
def index(request):
    return render(request, 'index.html')

@user_passes_test(is_superuser)
def ver_usuarios(request):
    usuarios = services.get_all_usuarios()
    return render(request, 'usuarios/verUsuarios.html', {'usuarios': usuarios})

@user_passes_test(is_superuser)
def agregar_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            services.save_usuario(form)
            return redirect('ver_usuarios')
    else:
        form = UsuarioForm()
    return render(request, 'usuarios/agregarUsuario.html', {'form': form})

@user_passes_test(is_superuser)
def editar_usuario(request, pk):
    usuario = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UsuarioUpdateForm(request.POST, instance=usuario)
        if form.is_valid():
            services.update_usuario(form, usuario)
            return redirect('ver_usuarios')
    else:
        form = UsuarioUpdateForm(instance=usuario, initial={'is_superuser': usuario.is_superuser})
    return render(request, 'usuarios/editarUsuario.html', {'form': form, 'usuario': usuario})

@user_passes_test(is_superuser)
def borrar_usuario(request, pk):
    services.delete_usuario(pk)
    return redirect('ver_usuarios')
