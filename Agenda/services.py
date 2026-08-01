from django.db.models import Q, Case, When, Value
from django.utils import timezone
from datetime import datetime, date
from django.utils.timezone import localtime
from django.shortcuts import get_object_or_404
from .models import SiguientesCitas
from ClientesMascotas.models import Mascotas

def get_mascota_by_id(mascota_id):
    if not mascota_id: return None
    try: return Mascotas.objects.get(pk=mascota_id)
    except Mascotas.DoesNotExist: return None

def get_todas_mascotas():
    return Mascotas.objects.all().select_related('cliente')

def get_datos_mascota(mascota):
    return {
        'nombre': mascota.nombre,
        'especie': mascota.especie,
        'raza': mascota.raza,
        'fechaNacimiento': mascota.fechaNacimiento,
        'peso': mascota.peso,
        'sexo': mascota.get_sexo_display(),
        'vacunas': mascota.vacunas,
        'alergias': mascota.alergias,
        'ultimaDesparasitacion': mascota.ultimaDesparasitacion,
        'ultimoDesparasitante': mascota.ultimoDesparasitante,
        'alimento': mascota.alimento,
        'cliente_nombre': mascota.cliente.nombre,
        'cliente_telefono': mascota.cliente.telefono,
        'cliente_email': mascota.cliente.email,
        'cliente_direccion': mascota.cliente.direccion,
    }

def get_proximas_citas(request):
    consultas = SiguientesCitas.objects.all().select_related('mascota', 'mascota__cliente', 'veterinario').order_by('fechaSiguienteCita')
    
    query_cliente = request.GET.get('q_cliente', '').strip()
    query_mascota = request.GET.get('q_mascota', '').strip()
    query_fecha = request.GET.get('q_fecha', '')
    query_veterinario = request.GET.get('q_veterinario', '')
    query_veterinaria = request.GET.get('q_veterinaria', '')
    query_asistencia = request.GET.get('q_asistencia', '')
    query_tipo_cita = request.GET.get('q_tipo_cita', '')
    
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
        except ValueError: pass
    
    if query_veterinario: consultas = consultas.filter(veterinario_id=query_veterinario)
    if query_veterinaria: consultas = consultas.filter(clinicaVeterinaria=query_veterinaria)
    if query_asistencia: consultas = consultas.filter(asistencia=query_asistencia)
    if query_tipo_cita: consultas = consultas.filter(tipoCita=query_tipo_cita)
    
    clinicas = SiguientesCitas.CLINICAS
    estados_asistencia = SiguientesCitas.ESTADOS_ASISTENCIAS
    tipos_cita = SiguientesCitas.TIPOS_CITA
    
    filtros_activos = any([query_cliente, query_mascota, query_fecha, query_veterinario, query_veterinaria, query_asistencia, query_tipo_cita])
    
    consultas = consultas.order_by(
         Case(When(fechaSiguienteCita__lt=timezone.now(), then=Value(1)), default=Value(0)),
         'fechaSiguienteCita'
    )
    if not filtros_activos: consultas = consultas[:10]
    
    return {
        'siguientesConsultas': consultas, 'clinicas': clinicas,
        'estados_asistencia': estados_asistencia, 'tipos_cita': tipos_cita,
        'query_cliente': query_cliente, 'query_mascota': query_mascota, 'query_fecha': query_fecha,
        'query_veterinario': query_veterinario, 'query_veterinaria': query_veterinaria,
        'query_asistencia': query_asistencia, 'query_tipo_cita': query_tipo_cita,
        'filtros_activos': filtros_activos,
        'veterinaria_seleccionada': query_veterinaria, 'asistencia_seleccionada': query_asistencia, 'tipo_cita_seleccionado': query_tipo_cita
    }

def get_cita_by_id(pk):
    return get_object_or_404(SiguientesCitas, pk=pk)

def delete_cita_by_id(pk):
    cita = get_object_or_404(SiguientesCitas, pk=pk)
    cita.delete()

def save_cita(form, mascota_id):
    proximaCita = form.save(commit=False)
    if mascota_id: proximaCita.mascota_id = mascota_id
    proximaCita.save()
    return proximaCita

def update_cita(form, mascota_id):
    proximaCita = form.save(commit=False)
    if mascota_id: proximaCita.mascota_id = mascota_id
    proximaCita.save()
    return proximaCita
