from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import base64
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Operaciones
from .forms import *
from ClientesMascotas.models import Mascotas
from django.contrib.auth.models import User
# Create your views here.
@login_required
def indexProcedimientos(request):
    return render(request, 'procedimientos/indexProcedimientos.html')




def encode_image_to_base64(image_file):
    """Función auxiliar para convertir imagen a base64"""
    if image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
    return None


@login_required
def crear_operacion(request):
    mascotas = Mascotas.objects.all().select_related('cliente')
    veterinarios = User.objects.filter(is_active=True).order_by('first_name', 'last_name')
    
    if request.method == 'POST':
        form = OperacionesForm(request.POST, request.FILES)
        if form.is_valid():
            operacion = form.save(commit=False)
            
            # Procesar imágenes
            if 'fotoAntes' in request.FILES:
                operacion.fotoAntes = encode_image_to_base64(request.FILES['fotoAntes'])
            if 'fotoDespues' in request.FILES:
                operacion.fotoDespues = encode_image_to_base64(request.FILES['fotoDespues'])
            
            operacion.save()
            messages.success(request, "Operación registrada correctamente.")
            return redirect('index-procedimientos')
    else:
        # Establecer el usuario actual como valor por defecto
        form = OperacionesForm(initial={'veterinario': request.user})
    
    return render(request, 'procedimientos/operaciones/nuevaOperacion.html', {
        'form': form,
        'mascotas': mascotas,
        'veterinarios': veterinarios,
        'title': 'Crear Nueva Operación'
    })
@login_required
def editar_operacion(request, pk):
    operacion = get_object_or_404(Operaciones, pk=pk)
    mascotas = Mascotas.objects.all().select_related('cliente')
    
    if request.method == 'POST':
        form = OperacionesUpdateForm(request.POST, instance=operacion)
        if form.is_valid():
            operacion_editada = form.save(commit=False)
            
            # Manejar fotoAntes
            if 'fotoAntes' in request.FILES and request.FILES['fotoAntes']:
                # Nueva imagen subida - convertir a base64
                operacion_editada.fotoAntes = encode_image_to_base64(request.FILES['fotoAntes'])
            else:
                # Mantener la imagen existente - NO hacer nada, ya está en la instancia
                pass  # Django automáticamente mantiene el valor existente
            
            # Manejar fotoDespues
            if 'fotoDespues' in request.FILES and request.FILES['fotoDespues']:
                # Nueva imagen subida - convertir a base64
                operacion_editada.fotoDespues = encode_image_to_base64(request.FILES['fotoDespues'])
            else:
                # Mantener la imagen existente - NO hacer nada, ya está en la instancia
                pass
            
            operacion_editada.save()
            messages.success(request, "Operación actualizada correctamente.")
            return redirect('detalle_operacion', pk=operacion.pk)
    else:
        form = OperacionesUpdateForm(instance=operacion)
    
    return render(request, 'procedimientos/operaciones/editarOperacion.html', {
        'form': form,
        'operacion': operacion,
        'mascotas': mascotas,
        'title': 'Editar Operación'
    })
@login_required
def historial_operaciones(request):
    operaciones = Operaciones.objects.all().select_related(
        'mascota', 'mascota__cliente', 'veterinario'
    ).order_by('-fechaEntrada')
    
    # Filtros
    query_cliente = request.GET.get('q_cliente', '')
    query_mascota = request.GET.get('q_mascota', '')
    query_operacion = request.GET.get('q_operacion', '')
    query_veterinario = request.GET.get('q_veterinario', '')
    query_veterinaria = request.GET.get('q_veterinaria', '')
    query_fecha_entrada = request.GET.get('q_fecha_entrada', '')
    
    # Aplicar filtros
    if query_cliente:
        operaciones = operaciones.filter(
            Q(mascota__cliente__nombre__icontains=query_cliente) |
            Q(mascota__cliente__email__icontains=query_cliente) |
            Q(mascota__cliente__telefono__icontains=query_cliente)
        )
    
    if query_mascota:
        operaciones = operaciones.filter(
            Q(mascota__nombre__icontains=query_mascota) |
            Q(mascota__raza__icontains=query_mascota) |
            Q(mascota__especie__icontains=query_mascota)
        )
    
    if query_operacion:
        operaciones = operaciones.filter(operacion__icontains=query_operacion)
    
    if query_veterinario:
        operaciones = operaciones.filter(veterinario_id=query_veterinario)
    
    if query_veterinaria:
        operaciones = operaciones.filter(clinicaVeterinaria=query_veterinaria)
    
    if query_fecha_entrada:
        try:
            from datetime import datetime
            fecha_filtro = datetime.strptime(query_fecha_entrada, '%Y-%m-%d').date()
            operaciones = operaciones.filter(fechaEntrada__date=fecha_filtro)
        except ValueError:
            pass
    
    # Datos para filtros
    veterinarios = User.objects.filter(is_active=True).order_by('first_name', 'last_name')
    clinicas = Operaciones.CLINICAS
    
    context = {
        'operaciones': operaciones,
        'veterinarios': veterinarios,
        'clinicas': clinicas,
        'query_cliente': query_cliente,
        'query_mascota': query_mascota,
        'query_operacion': query_operacion,
        'query_veterinario': query_veterinario,
        'query_veterinaria': query_veterinaria,
        'query_fecha_entrada': query_fecha_entrada,
    }
    
    return render(request, 'procedimientos/operaciones/verOperaciones.html', context)

@login_required
def detalle_operacion(request, pk):
    operacion = get_object_or_404(Operaciones, pk=pk)
    
    # Decodificar imágenes para mostrar
    foto_antes_data = None
    foto_despues_data = None
    
    if operacion.fotoAntes:
        foto_antes_data = f"data:image/jpeg;base64,{operacion.fotoAntes}"
    if operacion.fotoDespues:
        foto_despues_data = f"data:image/jpeg;base64,{operacion.fotoDespues}"
    
    return render(request, 'procedimientos/operaciones/detalleOperacion.html', {
        'operacion': operacion,
        'foto_antes_data': foto_antes_data,
        'foto_despues_data': foto_despues_data,
    })

@login_required
def eliminar_operacion(request, pk):
    """View to delete an existing pet."""
    operacion = get_object_or_404(Operaciones, pk=pk)
    operacion.delete()
    return redirect('historial_operaciones')



# Vista para listar vacunas
@login_required
def lista_vacunas(request):
    vacunas = ListaVacunas.objects.all().order_by('vacuna')
    
    # Filtro por nombre de vacuna
    query_vacuna = request.GET.get('q_vacuna', '')
    if query_vacuna:
        vacunas = vacunas.filter(vacuna__icontains=query_vacuna)
    
    context = {
        'vacunas': vacunas,
        'query_vacuna': query_vacuna,
    }
    
    return render(request, 'procedimientos/vacunas/verVacunas.html', context)

# Vista para agregar vacuna
@login_required
def agregar_vacuna(request):
    if request.method == 'POST':
        form = ListaVacunasForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Vacuna agregada exitosamente.")
            return redirect('lista_vacunas')
    else:
        form = ListaVacunasForm()
    
    return render(request, 'procedimientos/vacunas/agregarVacuna.html', {
        'form': form,
        'title': 'Agregar Vacuna'
    })

# Vista para editar vacuna
@login_required
def editar_vacuna(request, pk):
    vacuna = get_object_or_404(ListaVacunas, pk=pk)
    
    if request.method == 'POST':
        form = ListaVacunasForm(request.POST, instance=vacuna)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Vacuna actualizada exitosamente.")
            return redirect('lista_vacunas')
    else:
        form = ListaVacunasForm(instance=vacuna)
    
    return render(request, 'procedimientos/vacunas/editarVacuna.html', {
        'form': form,
        'vacuna': vacuna,
        'title': 'Editar Vacuna'
    })

# Vista para eliminar vacuna
@login_required
def eliminar_vacuna(request, pk):
    """View to delete an existing pet."""
    vacuna = get_object_or_404(ListaVacunas, pk=pk)
    vacuna.delete()
    return redirect('lista_vacunas')


@login_required
def indexVacunas(request):
    return render(request, 'procedimientos/vacunas/indexVacunas.html')
