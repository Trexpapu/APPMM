
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from ClientesMascotas.models import *

from datetime import datetime

from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required
def indexAgenda(request):
    return render(request, 'agenda/proximasCitas/indexAgenda.html')


def ver_proximas_citas(request):
    # Obtener todos los registros inicialmente
    consultas = SiguientesCitas.objects.all().select_related(
        'mascota', 'mascota__cliente', 'veterinario'
    ).order_by('fechaSiguienteCita')
    
    # Inicializar variables de filtro
    query_cliente = request.GET.get('q_cliente', '')
    query_mascota = request.GET.get('q_mascota', '')
    query_fecha = request.GET.get('q_fecha', '')
    query_veterinario = request.GET.get('q_veterinario', '')
    query_veterinaria = request.GET.get('q_veterinaria', '')
    query_asistencia = request.GET.get('q_asistencia', '')
    query_tipo_cita = request.GET.get('q_tipo_cita', '')
    
    # Aplicar filtros
    if query_cliente:
        consultas = consultas.filter(
            Q(mascota__cliente__nombre__icontains=query_cliente) |
            Q(mascota__cliente__email__icontains=query_cliente) |
            Q(mascota__cliente__telefono__icontains=query_cliente)
        )
    
    if query_mascota:
        consultas = consultas.filter(
            Q(mascota__nombre__icontains=query_mascota) |
            Q(mascota__raza__icontains=query_mascota) |
            Q(mascota__especie__icontains=query_mascota)
        )
    
    if query_fecha:
        try:
            fecha_filtro = datetime.strptime(query_fecha, '%Y-%m-%d').date()
            consultas = consultas.filter(fechaSiguienteCita__date=fecha_filtro)
        except ValueError:
            # Si la fecha no es válida, ignorar el filtro
            pass
    
    if query_veterinario:
        consultas = consultas.filter(veterinario_id=query_veterinario)
    
    if query_veterinaria:
        consultas = consultas.filter(clinicaVeterinaria=query_veterinaria)
    
    if query_asistencia:
        consultas = consultas.filter(asistencia=query_asistencia)
    
    if query_tipo_cita:
        consultas = consultas.filter(tipoCita=query_tipo_cita)
    
    # Obtener datos para los dropdowns
    veterinarios = User.objects.filter(is_active=True).order_by('first_name', 'last_name')
    
    # Obtener las opciones de clínicas del modelo
    clinicas = SiguientesCitas.CLINICAS
    estados_asistencia = SiguientesCitas.ESTADOS_ASISTENCIAS
    tipos_cita = SiguientesCitas.TIPOS_CITA
    
    # Verificar si hay filtros activos
    filtros_activos = any([
        query_cliente, query_mascota, query_fecha, 
        query_veterinario, query_veterinaria, query_asistencia, query_tipo_cita
    ])
    
    # Obtener objetos para mostrar en los resultados
    veterinario_seleccionado = None
    if query_veterinario:
        try:
            veterinario_seleccionado = User.objects.get(id=query_veterinario)
        except User.DoesNotExist:
            pass
    
    veterinaria_seleccionada = query_veterinaria
    asistencia_seleccionada = query_asistencia
    tipo_cita_seleccionado = query_tipo_cita
    
    consultas = consultas.order_by('-fechaSiguienteCita')
    
    context = {
        'siguientesConsultas': consultas,
        'query_cliente': query_cliente,
        'query_mascota': query_mascota,
        'query_fecha': query_fecha,
        'query_veterinario': query_veterinario,
        'query_veterinaria': query_veterinaria,
        'query_asistencia': query_asistencia,
        'query_tipo_cita': query_tipo_cita,
        'veterinarios': veterinarios,
        'clinicas': clinicas,
        'estados_asistencia': estados_asistencia,
        'tipos_cita': tipos_cita,
        'filtros_activos': filtros_activos,
        'veterinario_seleccionado': veterinario_seleccionado,
        'veterinaria_seleccionada': veterinaria_seleccionada,
        'asistencia_seleccionada': asistencia_seleccionada,
        'tipo_cita_seleccionado': tipo_cita_seleccionado,
    }
    
    return render(request, 'agenda/proximasCitas/verProximasCitas.html', context)


@login_required
def agendar_proxima_cita(request):
    """View to add a next consultation."""
    mascotas = Mascotas.objects.all()

    if request.method == 'POST':
        form = SiguientesCitasForm(request.POST)
        if form.is_valid():
            proximaCita = form.save(commit=False)
            mascota_id = request.POST.get('mascota')
            if mascota_id:
                proximaCita.mascota_id = mascota_id
                proximaCita.save()
                return redirect('index-agenda')
            else:
                form.add_error(None, "Debe seleccionar una mascota antes de guardar.")
    else:
        form = SiguientesCitasForm()
 
    return render(request, 'agenda/proximasCitas/agendarCita.html', {'form': form, 'mascotas': mascotas})


@login_required
def borrar_proxima_cita(request, pk):
    """View to delete an existing pet."""
    proxConsulta = get_object_or_404(SiguientesCitas, pk=pk)
    proxConsulta.delete()
    return redirect('ver-proximas-citas')


@login_required
def editar_proxima_cita(request, pk):
    """Editar mascota con selector personalizado de cliente."""
    proxConsulta = get_object_or_404(SiguientesCitas, pk=pk)
    mascota = Mascotas.objects.all()

    if request.method == 'POST':
        form = UpdateSiguienteCitaForm(request.POST, instance=proxConsulta)
        if form.is_valid():
            proxConsultaEditada = form.save(commit=False)
            mascota_id = request.POST.get('mascota')
            if mascota_id:
                proxConsultaEditada.mascota_id = mascota_id
            proxConsultaEditada.save()
            return redirect('ver-proximas-citas')
    else:
        form = UpdateSiguienteCitaForm(instance=proxConsulta)

    return render(request, 'agenda/proximasCitas/editarProximaCita.html', {
        'form': form,
        'mascotas': mascota
    })