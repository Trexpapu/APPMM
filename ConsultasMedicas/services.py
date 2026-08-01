from django.db.models import Q
from .models import ConsultasMedicas, DocumentosConsulta
from ClientesMascotas.models import Mascotas
from django.contrib.auth.models import User
from datetime import datetime, date
from django.utils.timezone import localtime
import json
import requests
from django.db import transaction

def get_datos_mascota(mascota):
    """Obtiene diccionario de datos de la mascota para el context"""
    return {
        'nombre': mascota.nombre,
        'especie': mascota.especie,
        'raza': mascota.raza,
        'vacunas': mascota.vacunas,
        'vive': mascota.vive,
        'ultimaDesparasitacion': mascota.ultimaDesparasitacion, 
        'ultimoDesparasitante': mascota.ultimoDesparasitante,
        'fechaNacimiento': mascota.fechaNacimiento,
        'peso': mascota.peso,
        'alergias': mascota.alergias,
        'alimento': mascota.alimento,
        'sexo': mascota.get_sexo_display(),
        'cliente_nombre': mascota.cliente.nombre,
        'cliente_telefono': mascota.cliente.telefono,
        'cliente_email': mascota.cliente.email,
        'cliente_id': mascota.cliente.id,
    }

def get_ultima_consulta_data(mascota_id):
    """Devuelve los initial_data de la última consulta"""
    ultima_consulta = ConsultasMedicas.objects.filter(mascota_id=mascota_id).order_by('-fechaConsulta').first()
    initial_data = {}
    if ultima_consulta:
        exclude_fields = ['id', 'fechaConsulta', 'peso', 'vacunas', 'alergias', 'mascota', 'ultimaDesparasitacion', 'ultimoDesparasitante', 'alimento']
        for field in ConsultasMedicas._meta.get_fields():
            if field.name not in exclude_fields and hasattr(ultima_consulta, field.name):
                initial_data[field.name] = getattr(ultima_consulta, field.name)
    return initial_data

@transaction.atomic
def save_consulta(request, form, mascota_id):
    """Guarda una consulta nueva y sus documentos"""
    consulta = form.save(commit=False)
    consulta.mascota_id = mascota_id
    consulta.save()

    # Actualizar mascota (optimizado)
    mascota = Mascotas.objects.select_for_update().get(pk=mascota_id)
    updated_fields = []
    if form.cleaned_data.get('peso') and mascota.peso != form.cleaned_data.get('peso'):
        mascota.peso = form.cleaned_data.get('peso')
        updated_fields.append('peso')
    if form.cleaned_data.get('alergias') and mascota.alergias != form.cleaned_data.get('alergias'):
        mascota.alergias = form.cleaned_data.get('alergias')
        updated_fields.append('alergias')
    if form.cleaned_data.get('alimento') and mascota.alimento != form.cleaned_data.get('alimento'):
        mascota.alimento = form.cleaned_data.get('alimento')
        updated_fields.append('alimento')
    
    if updated_fields:
        mascota.save(update_fields=updated_fields)

    # Documentos (bulk_create)
    archivos = request.FILES.getlist('archivo')
    descripciones = request.POST.getlist('descripcion')
    documentos_a_crear = []
    for i, archivo in enumerate(archivos):
        if archivo:
            descripcion = descripciones[i] if i < len(descripciones) else ''
            documentos_a_crear.append(DocumentosConsulta(consulta=consulta, archivo=archivo, descripcion=descripcion))
            
    if documentos_a_crear:
        DocumentosConsulta.objects.bulk_create(documentos_a_crear)
        
    return consulta

def get_consultas_list(request):
    """Retorna las consultas y parámetros para la vista de listado"""
    consultas = ConsultasMedicas.objects.select_related('mascota', 'mascota__cliente', 'veterinario').all()
    
    query_cliente = request.GET.get('q_cliente', '').strip()
    query_mascota = request.GET.get('q_mascota', '').strip()
    query_fecha = request.GET.get('q_fecha', '').strip()
    query_veterinario = request.GET.get('q_veterinario', '').strip()
    query_veterinaria = request.GET.get('q_veterinaria', '').strip()
    query_procedimiento = request.GET.get('q_procedimiento', '').strip()
    
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
            consultas = consultas.filter(fechaConsulta__date=fecha_filtro)
        except ValueError:
            pass
    if query_veterinario:
        consultas = consultas.filter(veterinario_id=query_veterinario)
    if query_veterinaria:
        consultas = consultas.filter(clinicaVeterinaria=query_veterinaria)
    if query_procedimiento:
        consultas = consultas.filter(procedimiento=query_procedimiento)
        
    filtros_activos = any([query_cliente, query_mascota, query_fecha, query_veterinario, query_veterinaria, query_procedimiento])
    
    veterinarios = User.objects.filter(is_active=True).order_by('first_name', 'last_name')
    clinicas = ConsultasMedicas.CLINICAS
    procedimientos = ConsultasMedicas.PROCEDIMIENTOS
    
    veterinario_seleccionado = None
    if query_veterinario:
        try:
            veterinario_seleccionado = User.objects.get(id=query_veterinario)
        except User.DoesNotExist:
            pass
            
    consultas = consultas.order_by('-fechaConsulta')
    if not filtros_activos:
        consultas = consultas[:10]
        
    return {
        'consultas': consultas,
        'query_cliente': query_cliente,
        'query_mascota': query_mascota,
        'query_fecha': query_fecha,
        'query_veterinario': query_veterinario,
        'query_veterinaria': query_veterinaria,
        'query_procedimiento': query_procedimiento,
        'veterinarios': veterinarios,
        'clinicas': clinicas,
        'procedimientos': procedimientos,
        'filtros_activos': filtros_activos,
        'veterinario_seleccionado': veterinario_seleccionado,
        'veterinaria_seleccionada': query_veterinaria,
        'procedimiento_seleccionado': query_procedimiento,
    }

@transaction.atomic
def update_consulta(request, form, consulta):
    """Actualiza una consulta y guarda/actualiza documentos"""
    consulta_obj = form.save(commit=False)
    mascota_id = request.POST.get('mascota')
    if mascota_id:
        consulta_obj.mascota_id = mascota_id
    consulta_obj.save()

    # Actualizar descripciones de docs existentes
    documentos_existentes = DocumentosConsulta.objects.filter(consulta=consulta_obj)
    docs_to_update = []
    for documento in documentos_existentes:
        nueva_descripcion = request.POST.get(f'descripcion_existente_{documento.id}')
        if nueva_descripcion is not None and documento.descripcion != nueva_descripcion:
            documento.descripcion = nueva_descripcion
            docs_to_update.append(documento)
            
    if docs_to_update:
        DocumentosConsulta.objects.bulk_update(docs_to_update, ['descripcion'])

    # Nuevos documentos (bulk_create)
    archivos = request.FILES.getlist('archivo')
    descripciones = request.POST.getlist('descripcion')
    documentos_a_crear = []
    for i, archivo in enumerate(archivos):
        if archivo:
            descripcion = descripciones[i] if i < len(descripciones) else ''
            documentos_a_crear.append(DocumentosConsulta(consulta=consulta_obj, archivo=archivo, descripcion=descripcion))
            
    if documentos_a_crear:
        DocumentosConsulta.objects.bulk_create(documentos_a_crear)
        
    return consulta_obj

def json_serializer(obj):
    """Usar formato ISO que n8n entienda sin ambigüedad"""
    if isinstance(obj, datetime):
        local_dt = localtime(obj)
        return local_dt.isoformat()
    elif isinstance(obj, date):
        return obj.strftime("%Y-%m-%d")
    return str(obj) if obj is not None else ""

def enviar_datos_webhook(datos_mascota, datos_formulario, url="http://localhost:5678/webhook/receta"):
    datos = {
        **datos_mascota,
        **datos_formulario
    }
    if not datos.get('cliente_email'):
        return
    try:
        datos_json = json.dumps(datos, default=json_serializer)
        response = requests.post(url, data=datos_json, headers={'Content-Type': 'application/json'})
    except Exception as e:
        print("Error al enviar webhook:", e)

from django.shortcuts import get_object_or_404

def get_consulta_by_id(consulta_id):
    """Devuelve el objeto consulta por ID"""
    return get_object_or_404(ConsultasMedicas, pk=consulta_id)

def get_documentos_de_consulta(consulta):
    """Devuelve los documentos de una consulta"""
    return DocumentosConsulta.objects.filter(consulta=consulta)

def get_documento_by_id(documento_id):
    """Devuelve el objeto documento por ID"""
    return get_object_or_404(DocumentosConsulta, id=documento_id)

def delete_consulta_by_id(consulta_id):
    """Elimina una consulta por ID"""
    consulta = get_object_or_404(ConsultasMedicas, pk=consulta_id)
    consulta.delete()

def delete_documento_by_id(documento_id):
    """Elimina un documento por ID y retorna el id de la consulta"""
    documento = get_object_or_404(DocumentosConsulta, id=documento_id)
    consulta_id = documento.consulta.id
    documento.delete()
    return consulta_id

def get_mascota_by_id(mascota_id):
    """Devuelve el objeto mascota o None si no existe o no se pasa id"""
    if not mascota_id:
        return None
    try:
        return Mascotas.objects.get(pk=mascota_id)
    except Mascotas.DoesNotExist:
        return None

def get_todas_mascotas():
    """Devuelve todas las mascotas para los select"""
    return Mascotas.objects.all().select_related('cliente')
