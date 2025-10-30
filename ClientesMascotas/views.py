from django.shortcuts import render, redirect, get_object_or_404
from .models import Clientes, Mascotas
from .forms import ClienteForm, MascotaForm, MascotaUpdateForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db.models import Q

# Create your views here.
@login_required
def index(request):
    # render the top-level index template (templates/index.html)
    return render(request, 'index.html')
@login_required
def indexClientes(request):
    return render(request, 'clientesMascotas/Clientes/indexCliente.html')
@login_required
def indexMascotas(request):
    return render(request, 'clientesMascotas/Mascotas/indexMascota.html')

@login_required
def ver_clientes(request):
    """View that renders a table with all clients or filters them based on a query."""
    query = request.GET.get('q', '').strip().lower()  # Remove replace to keep spaces intact
    if query:
        clientes = Clientes.objects.filter(
            Q(nombre__icontains=query) |
            Q(email__icontains=query) |
            Q(telefono__icontains=query)
        )
    else:
        clientes = Clientes.objects.all()
    return render(request, 'clientesMascotas/Clientes/VerClientes.html', {'clientes': clientes})


@login_required
def ver_mascotas(request):
    """View that renders a table with all pets and their associated client information."""
    query = request.GET.get('q', '').strip().lower()  # Remove replace to keep spaces intact
    if query:
        mascotas = Mascotas.objects.select_related('cliente').filter(
            Q(cliente__nombre__icontains=query) |
            Q(cliente__email__icontains=query) |
            Q(cliente__telefono__icontains=query) |
            Q(nombre__icontains=query) |
            Q(raza__icontains=query) |
            Q(especie__icontains=query)
        )
    else:
        mascotas = Mascotas.objects.select_related('cliente').all()
    return render(request, 'clientesMascotas/Mascotas/verMascotas.html', {'mascotas': mascotas})


@login_required
def agregar_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('indexCliente')
    else:
        form = ClienteForm()
    return render(request, 'clientesMascotas/Clientes/agregarCliente.html', {'form': form})


@login_required
def editar_cliente(request, pk):
    cliente = Clientes.objects.get(pk=pk)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('ver_clientes')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'clientesMascotas/Clientes/editarCliente.html', {'form': form, 'cliente': cliente})


@login_required
def borrar_cliente(request, pk):
    cliente = get_object_or_404(Clientes, pk=pk)
    cliente.delete()
    return redirect('ver_clientes')


@login_required
def agregar_mascota(request):
    """View to add a new pet, with a dropdown to select the client."""
    if request.method == 'POST':
        form = MascotaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('indexMascota')
    else:
        form = MascotaForm()
    clientes = Clientes.objects.all()
    return render(request, 'clientesMascotas/Mascotas/agregarMascota.html', {'form': form, 'clientes': clientes})


@login_required
def editar_mascota(request, pk):
    """View to edit an existing pet."""
    mascota = get_object_or_404(Mascotas, pk=pk)
    if request.method == 'POST':
        form = MascotaUpdateForm(request.POST, instance=mascota)
        if form.is_valid():
            form.save()
            return redirect('ver_mascotas')
    else:
        form = MascotaUpdateForm(instance=mascota)
    clientes = Clientes.objects.all()  # Fetch all clients for the dropdown
    return render(request, 'clientesMascotas/Mascotas/editarMascota.html', {'form': form, 'clientes': clientes})


@login_required
def borrar_mascota(request, pk):
    """View to delete an existing pet."""
    mascota = get_object_or_404(Mascotas, pk=pk)
    mascota.delete()
    return redirect('ver_mascotas')


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