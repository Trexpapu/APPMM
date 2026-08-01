from django.db.models import Q
from .models import Guarderia, Hospitalizacion
from ClientesMascotas.models import Mascotas
from django.shortcuts import get_object_or_404
from django.db import transaction
import base64

def encode_image_to_base64(image_file):
    if image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
    return None
from datetime import datetime, date
from django.utils.timezone import localtime
import requests
import json

def json_serializer(obj):
    """Usar formato ISO que n8n entienda sin ambigüedad"""
    if isinstance(obj, datetime):
        local_dt = localtime(obj)
        return local_dt.isoformat()
    elif isinstance(obj, date):
        return obj.strftime("%Y-%m-%d")
    return str(obj) if obj is not None else ""

def enviar_datos(datos_mascota, datos_formulario, url):
    datos = {**datos_mascota, **datos_formulario}
    if not datos.get('cliente_email'):
        return
    try:
        datos_json = json.dumps(datos, default=json_serializer)
        response = requests.post(url, data=datos_json, headers={'Content-Type': 'application/json'})
    except Exception as e:
        print("Error:", e)

def borrar_datos(datos_, url="http://localhost:5678/webhook/eliminar-datos"):
    datos = {**datos_}
    try:
        datos_json = json.dumps(datos, default=json_serializer)
        response = requests.post(url, data=datos_json, headers={'Content-Type': 'application/json'})
    except Exception as e:
        print("Error:", e)

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
        'vive': mascota.vive,
        'alergias': mascota.alergias,
        'ultimaDesparasitacion': mascota.ultimaDesparasitacion,
        'ultimoDesparasitante': mascota.ultimoDesparasitante,
        'alimento': mascota.alimento,
        'cliente_nombre': mascota.cliente.nombre,
        'cliente_telefono': mascota.cliente.telefono,
        'cliente_email': mascota.cliente.email,
    }

def get_datos_mascota_n8n(mascota):
    return {
        'nombre': mascota.nombre,
        'especie': mascota.especie,
        'raza': mascota.raza,
        'peso': mascota.peso,
        'sexo': mascota.get_sexo_display(),
        'cliente_nombre': mascota.cliente.nombre,
        'cliente_email': mascota.cliente.email,
    }

# ---- GUARDERIA ----

def get_historial_guarderia(request):
    guarderias = Guarderia.objects.all().select_related('mascota', 'mascota__cliente').order_by('-fechaEntrada')
    query_cliente = request.GET.get('q_cliente', '').strip().lower()
    query_mascota = request.GET.get('q_mascota', '').strip().lower()
    query_veterinaria = request.GET.get('q_veterinaria', '')
    query_fecha_entrada = request.GET.get('q_fecha_entrada', '')
    query_estado = request.GET.get('q_estado', '')
    
    if query_cliente:
        guarderias = guarderias.filter(
            Q(mascota__cliente__nombre__icontains=query_cliente) |
            Q(mascota__cliente__email__icontains=query_cliente) |
            Q(mascota__cliente__telefono__icontains=query_cliente)
        )
    if query_mascota:
        guarderias = guarderias.filter(
            Q(mascota__nombre__icontains=query_mascota) |
            Q(mascota__raza__icontains=query_mascota) |
            Q(mascota__especie__icontains=query_mascota)
        )
    if query_veterinaria:
        guarderias = guarderias.filter(clinicaVeterinaria=query_veterinaria)
    if query_fecha_entrada:
        guarderias = guarderias.filter(fechaEntrada=query_fecha_entrada)
    if query_estado:
        guarderias = guarderias.filter(estado=query_estado)
        
    clinicas = Guarderia.CLINICAS
    estados = Guarderia.ESTADOS
    filtros_activos = any([query_cliente, query_mascota, query_veterinaria, query_fecha_entrada, query_estado])
    
    if not filtros_activos: guarderias = guarderias[:10]
    return {
        'guarderias': guarderias, 'clinicas': clinicas, 'estados': estados,
        'query_cliente': query_cliente, 'query_mascota': query_mascota,
        'query_veterinaria': query_veterinaria, 'query_fecha_entrada': query_fecha_entrada,
        'query_estado': query_estado, 'filtros_activos': filtros_activos
    }

def get_guarderia_by_id(pk):
    return get_object_or_404(Guarderia, pk=pk)

@transaction.atomic
def save_guarderia(request, form):
    guarderia = form.save(commit=False)
    if 'fotoAntes' in request.FILES:
        guarderia.fotoAntes = encode_image_to_base64(request.FILES['fotoAntes'])
    if 'fotoDespues' in request.FILES:
        guarderia.fotoDespues = encode_image_to_base64(request.FILES['fotoDespues'])
    mascota = form.cleaned_data.get('mascota')
    mascota_obj = Mascotas.objects.select_for_update().get(pk=mascota.pk)
    
    nuevo_alimento = form.cleaned_data.get('alimento')
    if nuevo_alimento and mascota_obj.alimento != nuevo_alimento:
        mascota_obj.alimento = nuevo_alimento
        mascota_obj.save(update_fields=['alimento'])
        
    guarderia.save()
    return guarderia

def update_guarderia(request, form, mascota_id):
    guarderia_editada = form.save(commit=False)
    if mascota_id: guarderia_editada.mascota_id = mascota_id
    if 'fotoAntes' in request.FILES and request.FILES['fotoAntes']:
        guarderia_editada.fotoAntes = encode_image_to_base64(request.FILES['fotoAntes'])
    if 'fotoDespues' in request.FILES and request.FILES['fotoDespues']:
        guarderia_editada.fotoDespues = encode_image_to_base64(request.FILES['fotoDespues'])
    guarderia_editada.save()
    return guarderia_editada

def delete_guarderia_by_id(pk):
    guarderia = get_object_or_404(Guarderia, pk=pk)
    guarderia.delete()
    borrar_datos({'ID': str(pk), 'sheet': 'guarderia'})

# ---- HOSPITALIZACION ----

def get_historial_hospitalizacion(request):
    hospitalizaciones = Hospitalizacion.objects.all().select_related('mascota', 'mascota__cliente').order_by('-fechaEntrada')
    query_cliente = request.GET.get('q_cliente', '').strip()
    query_mascota = request.GET.get('q_mascota', '').strip()
    query_veterinaria = request.GET.get('q_veterinaria', '')
    query_fecha_entrada = request.GET.get('q_fecha_entrada', '')
    query_estado = request.GET.get('q_estado', '')
    
    if query_cliente:
        hospitalizaciones = hospitalizaciones.filter(
            Q(mascota__cliente__nombre__icontains=query_cliente) |
            Q(mascota__cliente__email__icontains=query_cliente) |
            Q(mascota__cliente__telefono__icontains=query_cliente)
        )
    if query_mascota:
        hospitalizaciones = hospitalizaciones.filter(
            Q(mascota__nombre__icontains=query_mascota) |
            Q(mascota__raza__icontains=query_mascota) |
            Q(mascota__especie__icontains=query_mascota)
        )
    if query_veterinaria:
        hospitalizaciones = hospitalizaciones.filter(clinicaVeterinaria=query_veterinaria)
    if query_fecha_entrada:
        try: hospitalizaciones = hospitalizaciones.filter(fechaEntrada=query_fecha_entrada)
        except ValueError: hospitalizaciones = hospitalizaciones.filter(fechaEntrada__icontains=query_fecha_entrada)
    if query_estado:
        hospitalizaciones = hospitalizaciones.filter(estado=query_estado)
        
    clinicas = Hospitalizacion.CLINICAS
    estados = Hospitalizacion.ESTADOS
    filtros_activos = any([query_cliente, query_mascota, query_veterinaria, query_fecha_entrada, query_estado])
    
    clinica_seleccionada = next((c[1] for c in clinicas if c[0] == query_veterinaria), '')
    estado_seleccionado = next((e[1] for e in estados if e[0] == query_estado), '')

    if not filtros_activos: hospitalizaciones = hospitalizaciones[:10]
    
    return {
        'hospitalizaciones': hospitalizaciones, 'clinicas': clinicas, 'estados': estados,
        'query_cliente': query_cliente, 'query_mascota': query_mascota,
        'query_veterinaria': query_veterinaria, 'query_fecha_entrada': query_fecha_entrada,
        'query_estado': query_estado, 'filtros_activos': filtros_activos,
        'clinica_seleccionada': clinica_seleccionada, 'estado_seleccionado': estado_seleccionado,
    }

def get_hospitalizacion_by_id(pk):
    return get_object_or_404(Hospitalizacion, pk=pk)

def save_hospitalizacion(request, form):
    hospitalizacion = form.save(commit=False)
    if 'fotoAntes' in request.FILES:
        hospitalizacion.fotoAntes = encode_image_to_base64(request.FILES['fotoAntes'])
    if 'fotoDespues' in request.FILES:
        hospitalizacion.fotoDespues = encode_image_to_base64(request.FILES['fotoDespues'])
    hospitalizacion.save()
    return hospitalizacion

def update_hospitalizacion(request, form, mascota_id, mascota_obj):
    hospitalizacion_editada = form.save(commit=False)
    if mascota_id and mascota_obj: hospitalizacion_editada.mascota = mascota_obj
    if 'fotoAntes' in request.FILES and request.FILES['fotoAntes']:
        hospitalizacion_editada.fotoAntes = encode_image_to_base64(request.FILES['fotoAntes'])
    if 'fotoDespues' in request.FILES and request.FILES['fotoDespues']:
        hospitalizacion_editada.fotoDespues = encode_image_to_base64(request.FILES['fotoDespues'])
    hospitalizacion_editada.save()
    return hospitalizacion_editada

def delete_hospitalizacion_by_id(pk):
    hospitalizacion = get_object_or_404(Hospitalizacion, pk=pk)
    hospitalizacion.delete()
    borrar_datos({'ID': str(pk), 'sheet': 'hospitalizacion'})
