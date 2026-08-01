from django.db.models import Q
from .models import Operaciones, ListaVacunas, Vacunaciones, ListaDesparasitantes, Desparasitaciones
from ClientesMascotas.models import Mascotas
from django.shortcuts import get_object_or_404
import base64
from django.db import transaction

def encode_image_to_base64(image_file):
    if image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
    return None

def get_mascota_by_id(mascota_id):
    if not mascota_id: return None
    try: return Mascotas.objects.get(pk=mascota_id)
    except Mascotas.DoesNotExist: return None

# ---- OPERACIONES ----

def get_historial_operaciones(request):
    operaciones = Operaciones.objects.all().select_related('mascota', 'mascota__cliente', 'veterinario').order_by('-fechaEntrada')
    query_cliente = request.GET.get('q_cliente', '')
    query_mascota = request.GET.get('q_mascota', '')
    query_operacion = request.GET.get('q_operacion', '')
    query_veterinario = request.GET.get('q_veterinario', '')
    query_veterinaria = request.GET.get('q_veterinaria', '')
    query_fecha_entrada = request.GET.get('q_fecha_entrada', '')
    
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
    if query_operacion: operaciones = operaciones.filter(operacion__icontains=query_operacion)
    if query_veterinario: operaciones = operaciones.filter(veterinario_id=query_veterinario)
    if query_veterinaria: operaciones = operaciones.filter(clinicaVeterinaria=query_veterinaria)
    if query_fecha_entrada:
        try:
            from datetime import datetime
            fecha_filtro = datetime.strptime(query_fecha_entrada, '%Y-%m-%d').date()
            operaciones = operaciones.filter(fechaEntrada__date=fecha_filtro)
        except ValueError: pass

    filtros_activos = any([query_cliente, query_mascota, query_veterinaria, query_fecha_entrada, query_operacion])
    clinicas = Operaciones.CLINICAS
    if not filtros_activos: operaciones = operaciones[:10]
    
    return {
        'operaciones': operaciones, 'clinicas': clinicas,
        'query_cliente': query_cliente, 'query_mascota': query_mascota,
        'query_operacion': query_operacion, 'query_veterinario': query_veterinario,
        'query_veterinaria': query_veterinaria, 'query_fecha_entrada': query_fecha_entrada,
        'filtros_activos': filtros_activos,
    }

def get_operacion_by_id(pk):
    return get_object_or_404(Operaciones, pk=pk)

@transaction.atomic
def save_operacion(request, form):
    operacion = form.save(commit=False)
    peso = form.cleaned_data.get('peso')
    mascota_id = form.cleaned_data.get('mascota')
    mascota = Mascotas.objects.select_for_update().get(pk=mascota_id.pk)
    if mascota.peso != peso:
        mascota.peso = peso
        mascota.save(update_fields=['peso'])
    
    if 'fotoAntes' in request.FILES:
        operacion.fotoAntes = encode_image_to_base64(request.FILES['fotoAntes'])
    if 'fotoDespues' in request.FILES:
        operacion.fotoDespues = encode_image_to_base64(request.FILES['fotoDespues'])
    operacion.save()
    return operacion

def update_operacion(request, form):
    operacion_editada = form.save(commit=False)
    if 'fotoAntes' in request.FILES and request.FILES['fotoAntes']:
        operacion_editada.fotoAntes = encode_image_to_base64(request.FILES['fotoAntes'])
    if 'fotoDespues' in request.FILES and request.FILES['fotoDespues']:
        operacion_editada.fotoDespues = encode_image_to_base64(request.FILES['fotoDespues'])
    operacion_editada.save()
    return operacion_editada

def delete_operacion_by_id(pk):
    operacion = get_object_or_404(Operaciones, pk=pk)
    operacion.delete()

# ---- VACUNACIONES ----

def get_historial_vacunaciones(request):
    vacunaciones = Vacunaciones.objects.all().select_related('mascota', 'mascota__cliente', 'veterinario', 'vacunas').order_by('-fecha')
    query_cliente = request.GET.get('q_cliente', '').strip().lower()
    query_mascota = request.GET.get('q_mascota', '').strip().lower()
    query_veterinario = request.GET.get('q_veterinario', '')
    query_veterinaria = request.GET.get('q_veterinaria', '')
    query_vacuna = request.GET.get('q_vacuna', '').strip().lower()
    query_fecha = request.GET.get('q_fecha', '')
    
    if query_cliente:
        vacunaciones = vacunaciones.filter(
            Q(mascota__cliente__nombre__icontains=query_cliente) |
            Q(mascota__cliente__email__icontains=query_cliente) |
            Q(mascota__cliente__telefono__icontains=query_cliente)
        )
    if query_mascota:
        vacunaciones = vacunaciones.filter(
            Q(mascota__nombre__icontains=query_mascota) |
            Q(mascota__raza__icontains=query_mascota) |
            Q(mascota__especie__icontains=query_mascota)
        )
    if query_veterinario: vacunaciones = vacunaciones.filter(veterinario_id=query_veterinario)
    if query_veterinaria: vacunaciones = vacunaciones.filter(clinicaVeterinaria=query_veterinaria)
    if query_vacuna: vacunaciones = vacunaciones.filter(vacunas__vacuna__icontains=query_vacuna)
    if query_fecha: vacunaciones = vacunaciones.filter(fecha=query_fecha)
        
    clinicas = Vacunaciones.CLINICAS
    vacunas_lista = ListaVacunas.objects.all().order_by('vacuna')
    filtros_activos = any([query_cliente, query_mascota, query_veterinario, query_veterinaria, query_vacuna, query_fecha])
    
    if not filtros_activos: vacunaciones = vacunaciones[:10]
    
    return {
        'vacunaciones': vacunaciones, 'clinicas': clinicas, 'vacunas_lista': vacunas_lista,
        'query_cliente': query_cliente, 'query_mascota': query_mascota,
        'query_veterinario': query_veterinario, 'query_veterinaria': query_veterinaria,
        'query_vacuna': query_vacuna, 'query_fecha': query_fecha,
        'filtros_activos': filtros_activos
    }

def get_vacunacion_by_id(pk):
    return get_object_or_404(Vacunaciones, pk=pk)

@transaction.atomic
def save_vacunacion(request, form):
    vacunacion = form.save(commit=False)
    vacunacion.save()
    _update_mascota_vacunas(vacunacion.mascota)
    return vacunacion

@transaction.atomic
def update_vacunacion(request, form):
    vacunacion = form.save(commit=False)
    vacunacion.save()
    _update_mascota_vacunas(vacunacion.mascota)
    return vacunacion

@transaction.atomic
def delete_vacunacion_by_id(pk):
    vacunacion = get_object_or_404(Vacunaciones, pk=pk)
    mascota = vacunacion.mascota
    vacunacion.delete()
    _update_mascota_vacunas(mascota)

def _update_mascota_vacunas(mascota_obj):
    mascota = Mascotas.objects.select_for_update().get(pk=mascota_obj.pk)
    vacunas_data = Vacunaciones.objects.filter(mascota=mascota)
    vacunas_cleaned_data = ", ".join([str(v.vacunas) for v in vacunas_data])
    if mascota.vacunas != vacunas_cleaned_data:
        mascota.vacunas = vacunas_cleaned_data
        mascota.save(update_fields=['vacunas'])

# ---- LISTA VACUNAS ----

def get_lista_vacunas(request):
    vacunas = ListaVacunas.objects.all().order_by('vacuna')
    query_vacuna = request.GET.get('q_vacuna', '')
    if query_vacuna:
        vacunas = vacunas.filter(vacuna__icontains=query_vacuna)
    return {'vacunas': vacunas, 'query_vacuna': query_vacuna}

def get_lista_vacuna_by_id(pk):
    return get_object_or_404(ListaVacunas, pk=pk)

def delete_lista_vacuna_by_id(pk):
    vacuna = get_object_or_404(ListaVacunas, pk=pk)
    vacuna.delete()


# ---- DESPARASITACIONES ----

def get_historial_desparasitaciones(request):
    desparasitaciones = Desparasitaciones.objects.all().select_related('mascota', 'mascota__cliente', 'veterinario', 'desparasitante').order_by('-fecha')
    query_cliente = request.GET.get('q_cliente', '').strip().lower()
    query_mascota = request.GET.get('q_mascota', '').strip().lower()
    query_veterinario = request.GET.get('q_veterinario', '')
    query_veterinaria = request.GET.get('q_veterinaria', '')
    query_desparasitante = request.GET.get('q_desparasitante', '').strip().lower()
    query_fecha = request.GET.get('q_fecha', '')
    
    if query_cliente:
        desparasitaciones = desparasitaciones.filter(
            Q(mascota__cliente__nombre__icontains=query_cliente) |
            Q(mascota__cliente__email__icontains=query_cliente) |
            Q(mascota__cliente__telefono__icontains=query_cliente)
        )
    if query_mascota:
        desparasitaciones = desparasitaciones.filter(
            Q(mascota__nombre__icontains=query_mascota) |
            Q(mascota__raza__icontains=query_mascota) |
            Q(mascota__especie__icontains=query_mascota)
        )
    if query_veterinario: desparasitaciones = desparasitaciones.filter(veterinario_id=query_veterinario)
    if query_veterinaria: desparasitaciones = desparasitaciones.filter(clinicaVeterinaria=query_veterinaria)
    if query_desparasitante: desparasitaciones = desparasitaciones.filter(desparasitante__desparasitante__icontains=query_desparasitante)
    if query_fecha: desparasitaciones = desparasitaciones.filter(fecha=query_fecha)
        
    clinicas = Desparasitaciones.CLINICAS
    desparasitantes_lista = ListaDesparasitantes.objects.all().order_by('desparasitante')
    filtros_activos = any([query_cliente, query_mascota, query_veterinario, query_veterinaria, query_desparasitante, query_fecha])
    
    if not filtros_activos: desparasitaciones = desparasitaciones[:10]
    
    return {
        'desparasitaciones': desparasitaciones, 'clinicas': clinicas, 'desparasitantes_lista': desparasitantes_lista,
        'query_cliente': query_cliente, 'query_mascota': query_mascota,
        'query_veterinario': query_veterinario, 'query_veterinaria': query_veterinaria,
        'query_desparasitante': query_desparasitante, 'query_fecha': query_fecha,
        'filtros_activos': filtros_activos
    }

def get_desparasitacion_by_id(pk):
    return get_object_or_404(Desparasitaciones, pk=pk)

@transaction.atomic
def save_desparasitacion(request, form):
    desparasitacion = form.save(commit=False)
    mascota = Mascotas.objects.select_for_update().get(pk=desparasitacion.mascota.pk)
    
    update_fields = []
    if mascota.ultimaDesparasitacion != desparasitacion.fecha:
        mascota.ultimaDesparasitacion = desparasitacion.fecha
        update_fields.append('ultimaDesparasitacion')
    
    ultimo_desparasitante_str = str(desparasitacion.desparasitante)
    if mascota.ultimoDesparasitante != ultimo_desparasitante_str:
        mascota.ultimoDesparasitante = ultimo_desparasitante_str
        update_fields.append('ultimoDesparasitante')
        
    if mascota.peso != desparasitacion.peso:
        mascota.peso = desparasitacion.peso
        update_fields.append('peso')
        
    if update_fields:
        mascota.save(update_fields=update_fields)
        
    desparasitacion.save()
    return desparasitacion

def delete_desparasitacion_by_id(pk):
    desparasitacion = get_object_or_404(Desparasitaciones, pk=pk)
    desparasitacion.delete()

# ---- LISTA DESPARASITANTES ----

def get_lista_desparasitantes(request):
    desparasitantes = ListaDesparasitantes.objects.all().order_by('desparasitante')
    query_desparasitante = request.GET.get('q_desparasitante', '')
    if query_desparasitante:
        desparasitantes = desparasitantes.filter(desparasitante__icontains=query_desparasitante)
    return {'desparasitantes': desparasitantes, 'query_desparasitante': query_desparasitante}

def get_lista_desparasitante_by_id(pk):
    return get_object_or_404(ListaDesparasitantes, pk=pk)

def delete_lista_desparasitante_by_id(pk):
    desparasitante = get_object_or_404(ListaDesparasitantes, pk=pk)
    desparasitante.delete()
