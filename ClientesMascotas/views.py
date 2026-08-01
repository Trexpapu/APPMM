from django.shortcuts import render, redirect, get_object_or_404
from .models import Clientes, Mascotas
from .forms import ClienteForm, MascotaForm
from . import services
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

# Moved index view to Usuarios app

@login_required
def indexClientes(request):
    return render(request, 'clientesMascotas/Clientes/indexCliente.html')

@login_required
def indexMascotas(request):
    return render(request, 'clientesMascotas/Mascotas/indexMascota.html')

@login_required
def ver_clientes(request):
    """View that renders a table with all clients or filters them based on a query."""
    query = request.GET.get('q', '').strip()
    clientes = services.get_filtered_clientes(query)
    
    return render(request, 'clientesMascotas/Clientes/VerClientes.html', {
        'clientes': clientes,
        'query': query
    })

@login_required
def ver_mascotas(request):
    """View that renders a table with all pets and their associated client information."""
    query_cliente = request.GET.get('q_cliente', '').strip().lower()
    query_mascota = request.GET.get('q_mascota', '').strip().lower()
    
    mascotas, filtros_activos = services.get_filtered_mascotas(query_cliente, query_mascota)
    
    return render(request, 'clientesMascotas/Mascotas/verMascotas.html', {
        'mascotas': mascotas,
        'query_cliente': query_cliente,
        'query_mascota': query_mascota,
        'filtros_activos': filtros_activos
    })

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
    cliente = get_object_or_404(Clientes, pk=pk)
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
    services.delete_cliente(pk)
    return redirect('ver_clientes')

@login_required
def agregar_mascota(request):
    """View to add a new pet, with a dropdown to select the client."""
    clientes = Clientes.objects.all()

    if request.method == 'POST':
        form = MascotaForm(request.POST)
        cliente_id = request.POST.get('cliente')
        
        if form.is_valid() and cliente_id:
            services.save_mascota(form, cliente_id)
            return redirect('indexMascota')
        elif not cliente_id:
            form.add_error(None, "Debe seleccionar un cliente antes de guardar.")
    else:
        form = MascotaForm()

    return render(
        request,
        'clientesMascotas/Mascotas/agregarMascota.html',
        {'form': form, 'clientes': clientes}
    )

@login_required
def editar_mascota(request, pk):
    """Editar mascota con selector personalizado de cliente."""
    mascota = get_object_or_404(Mascotas, pk=pk)
    clientes = Clientes.objects.all()

    if request.method == 'POST':
        form = MascotaForm(request.POST, instance=mascota)
        cliente_id = request.POST.get('cliente')
        
        if form.is_valid() and cliente_id:
            services.save_mascota(form, cliente_id)
            return redirect('ver_mascotas')
        elif not cliente_id:
            form.add_error(None, "Debe seleccionar un cliente antes de guardar.")
    else:
        form = MascotaForm(instance=mascota)

    return render(request, 'clientesMascotas/Mascotas/editarMascota.html', {
        'form': form,
        'clientes': clientes
    })

@login_required
def borrar_mascota(request, pk):
    """View to delete an existing pet."""
    services.delete_mascota(pk)
    return redirect('ver_mascotas')

@login_required
def detalle_cliente(request, cliente_id):
    """Vista para mostrar el detalle de un cliente y sus mascotas"""
    context = services.get_cliente_details(cliente_id)
    return render(request, 'clientesMascotas/Clientes/detalleCliente.html', context)

@login_required
def detalle_mascota(request, mascota_id):
    """Vista para mostrar el detalle de una mascota específica"""
    context = services.get_mascota_details(mascota_id)
    return render(request, 'clientesMascotas/Mascotas/DetalleMascota.html', context)

# Moved user_login view to Usuarios app