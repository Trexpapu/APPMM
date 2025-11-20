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
    query_cliente = request.GET.get('q_cliente', '').strip().lower()
    query_mascota = request.GET.get('q_mascota', '').strip().lower()
    
    mascotas = Mascotas.objects.select_related('cliente').all()
    
    # Aplicar filtros combinados
    if query_cliente:
        mascotas = mascotas.filter(
            Q(cliente__nombre__icontains=query_cliente) |
            Q(cliente__email__icontains=query_cliente) |
            Q(cliente__telefono__icontains=query_cliente)
        )
    
    if query_mascota:
        mascotas = mascotas.filter(
            Q(nombre__icontains=query_mascota) |
            Q(raza__icontains=query_mascota) |
            Q(especie__icontains=query_mascota) |
            Q(vacunas__icontains=query_mascota) |
            Q(alergias__icontains=query_mascota)
        )
    
    # Determinar si hay filtros activos
    filtros_activos = query_cliente or query_mascota
    
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
    clientes = Clientes.objects.all()  # obtenemos los clientes antes por claridad

    if request.method == 'POST':
        form = MascotaForm(request.POST)
        if form.is_valid():
            mascota = form.save(commit=False)  # no guarda todavía
            cliente_id = request.POST.get('cliente')  # obtenemos el cliente seleccionado del select
            if cliente_id:  # si el usuario eligió un cliente
                mascota.cliente_id = cliente_id  # asignamos el cliente manualmente
                mascota.save()  # guardamos ahora sí
                return redirect('indexMascota')
            else:
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
        form = MascotaUpdateForm(request.POST, instance=mascota)
        if form.is_valid():
            mascota_editada = form.save(commit=False)
            cliente_id = request.POST.get('cliente')
            if cliente_id:
                mascota_editada.cliente_id = cliente_id
            mascota_editada.save()
            return redirect('ver_mascotas')
    else:
        form = MascotaUpdateForm(instance=mascota)

    return render(request, 'clientesMascotas/Mascotas/editarMascota.html', {
        'form': form,
        'clientes': clientes
    })




@login_required
def borrar_mascota(request, pk):
    """View to delete an existing pet."""
    mascota = get_object_or_404(Mascotas, pk=pk)
    mascota.delete()
    return redirect('ver_mascotas')




@login_required
def detalle_cliente(request, cliente_id):
    """Vista para mostrar el detalle de un cliente y sus mascotas"""
    cliente = get_object_or_404(Clientes, id=cliente_id)
    mascotas = Mascotas.objects.filter(cliente=cliente).order_by('nombre')
    mascotasVivas = Mascotas.objects.filter(cliente=cliente, vive = True).count()
    
    context = {
        'cliente': cliente,
        'mascotas': mascotas,
        'mascotasVivas': mascotasVivas
    }
    return render(request, 'clientesMascotas/Clientes/detalleCliente.html', context)

@login_required
def detalle_mascota(request, mascota_id):
    """Vista para mostrar el detalle de una mascota específica"""
    mascota = get_object_or_404(Mascotas, id=mascota_id)
    
    # Calcular edad aproximada
    from datetime import date
    hoy = date.today()
    edad = hoy.year - mascota.fechaNacimiento.year - (
        (hoy.month, hoy.day) < (mascota.fechaNacimiento.month, mascota.fechaNacimiento.day)
    )
    
    context = {
        'mascota': mascota,
        'edad': edad,
    }
    return render(request, 'clientesMascotas/Mascotas/DetalleMascota.html', context)


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