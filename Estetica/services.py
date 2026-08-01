from django.db.models import Q
from .models import Estetica
from ClientesMascotas.models import Mascotas
from django.shortcuts import get_object_or_404
from django.db import transaction
import base64

def encode_image_to_base64(image_file):
    if image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
    return None


def get_mascota_by_id(mascota_id):
    if not mascota_id:
        return None
    try:
        return Mascotas.objects.get(pk=mascota_id)
    except Mascotas.DoesNotExist:
        return None

def get_todas_mascotas():
    return Mascotas.objects.all().select_related('cliente')

def get_datos_mascota(mascota):
    """Devuelve diccionario con la información de la mascota"""
    return {
        'nombre': mascota.nombre,
        'especie': mascota.especie,
        'raza': mascota.raza,
        'fechaNacimiento': mascota.fechaNacimiento,
        'peso': mascota.peso,
        'sexo': mascota.get_sexo_display(),
        'vacunas': mascota.vacunas,
        'alergias': mascota.alergias,
        'vive': mascota.vive,
        'ultimaDesparasitacion': mascota.ultimaDesparasitacion,
        'ultimoDesparasitante': mascota.ultimoDesparasitante,
        'alimento': mascota.alimento,
        'cliente_nombre': mascota.cliente.nombre,
        'cliente_telefono': mascota.cliente.telefono,
        'cliente_email': mascota.cliente.email,
    }

@transaction.atomic
def save_estetica(request, form):
    estetica = form.save(commit=False)
    
    mascota = form.cleaned_data.get('mascota')
    mascota_obj = Mascotas.objects.select_for_update().get(pk=mascota.pk)
    
    nuevo_peso = form.cleaned_data.get('peso')
    if nuevo_peso and mascota_obj.peso != nuevo_peso:
        mascota_obj.peso = nuevo_peso
        mascota_obj.save(update_fields=['peso'])
        
    if 'fotoAntes' in request.FILES:
        estetica.fotoAntes = encode_image_to_base64(request.FILES['fotoAntes'])
    if 'fotoDespues' in request.FILES:
        estetica.fotoDespues = encode_image_to_base64(request.FILES['fotoDespues'])
        
    estetica.save()
    return estetica

def update_estetica(request, form, mascota_id, mascota_obj):
    """Actualiza un registro de estética"""
    estetica_editada = form.save(commit=False)
    if mascota_id and mascota_obj:
        estetica_editada.mascota = mascota_obj
    if 'fotoAntes' in request.FILES and request.FILES['fotoAntes']:
        estetica_editada.fotoAntes = encode_image_to_base64(request.FILES['fotoAntes'])
    if 'fotoDespues' in request.FILES and request.FILES['fotoDespues']:
        estetica_editada.fotoDespues = encode_image_to_base64(request.FILES['fotoDespues'])
    estetica_editada.save()
    return estetica_editada

def get_historial_esteticas(request):
    """Devuelve queryset filtrado y variables de contexto para el historial"""
    esteticas = Estetica.objects.all().select_related('mascota', 'mascota__cliente', 'estilista').order_by('-fechaHoraIngreso')
    
    query_cliente = request.GET.get('q_cliente', '').strip()
    query_mascota = request.GET.get('q_mascota', '').strip()
    query_clinica = request.GET.get('q_clinica', '')
    query_fecha_ingreso = request.GET.get('q_fecha_ingreso', '')
    query_estilista = request.GET.get('q_estilista', '')
    
    if query_cliente:
        esteticas = esteticas.filter(
            Q(mascota__cliente__nombre__icontains=query_cliente) |
            Q(mascota__cliente__email__icontains=query_cliente) |
            Q(mascota__cliente__telefono__icontains=query_cliente)
        )
    if query_mascota:
        esteticas = esteticas.filter(
            Q(mascota__nombre__icontains=query_mascota) |
            Q(mascota__raza__icontains=query_mascota) |
            Q(mascota__especie__icontains=query_mascota)
        )
    if query_clinica:
        esteticas = esteticas.filter(clinicaVeterinaria=query_clinica)
    if query_fecha_ingreso:
        try:
            esteticas = esteticas.filter(fechaHoraIngreso__date=query_fecha_ingreso)
        except ValueError:
            esteticas = esteticas.filter(fechaHoraIngreso__icontains=query_fecha_ingreso)
    if query_estilista:
        esteticas = esteticas.filter(estilista__username__icontains=query_estilista)
    
    clinicas = Estetica.CLINICAS
    filtros_activos = any([query_cliente, query_mascota, query_clinica, query_fecha_ingreso, query_estilista])
    
    clinica_seleccionada = ''
    if query_clinica:
        for clinica in clinicas:
            if clinica[0] == query_clinica:
                clinica_seleccionada = clinica[1]
                break
                
    if not filtros_activos:
        esteticas = esteticas[:10]
        
    return {
        'esteticas': esteticas,
        'clinicas': clinicas,
        'query_cliente': query_cliente,
        'query_mascota': query_mascota,
        'query_clinica': query_clinica,
        'query_fecha_ingreso': query_fecha_ingreso,
        'query_estilista': query_estilista,
        'filtros_activos': filtros_activos,
        'clinica_seleccionada': clinica_seleccionada,
    }

def get_estetica_by_id(pk):
    return get_object_or_404(Estetica, pk=pk)

def delete_estetica_by_id(pk):
    estetica = get_object_or_404(Estetica, pk=pk)
    estetica.delete()
