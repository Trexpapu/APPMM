
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from ClientesMascotas.models import *
from ConsultasMedicas.urls import *
from datetime import datetime
from django.contrib import messages
import requests
import json
from django.contrib.auth.decorators import login_required
from datetime import date, datetime
from django.utils.timezone import localtime
# Create your views here.
from django.db.models import Case, When, Value
from django.utils import timezone
from datetime import datetime

def permisos(request, obj):
    if request.user.is_superuser:
        veterinario = obj.veterinario.username
        veterinarioEmail = obj.veterinario.email
    else: 
        veterinario = request.user.username
        veterinarioEmail = request.user.email
        obj.veterinario = request.user
    return obj, veterinario, veterinarioEmail
    
@login_required
def indexAgenda(request):
    return render(request, 'agenda/proximasCitas/indexAgenda.html')



@login_required
def ver_proximas_citas(request):
    # Obtener todos los registros inicialmente, ordenados por fecha más cercana primero
    consultas = SiguientesCitas.objects.all().select_related(
        'mascota', 'mascota__cliente', 'veterinario'
    ).order_by('fechaSiguienteCita')  # ASCENDENTE: más cercanas primero
    
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
    
    
    # Si quieres separar las citas pasadas y ponerlas al final:
    consultas = consultas.order_by(
         Case(
             When(fechaSiguienteCita__lt=timezone.now(), then=Value(1)),
             default=Value(0)
         ),
         'fechaSiguienteCita'
     )
    
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




def json_serializer(obj):
    """Usar formato ISO que n8n entienda sin ambigüedad"""
    if isinstance(obj, datetime):
        local_dt = localtime(obj)
        # Formato ISO 8601: 2025-12-05T18:30:00-05:00
        return local_dt.isoformat()
    
    elif isinstance(obj, date):
        return obj.strftime("%Y-%m-%d")
    
    return str(obj) if obj is not None else ""

def enviar_datos(datos_mascota, datos_formulario, url= "http://localhost:5678/webhook/agregar"):
    datos = {
        **datos_mascota,
        **datos_formulario
    }
    if datos.get('cliente_email') == "" or datos.get('cliente_email') == None:
        return
    # Convertir el diccionario a una cadena JSON manualmente, usando nuestro serializador personalizado
    try:
        datos_json = json.dumps(datos, default=json_serializer)
    except TypeError as e:
        print(f"Error al serializar los datos: {e}")
        return

    # Enviar la solicitud con el JSON ya serializado
    try:
        response = requests.post(url, data=datos_json, headers={'Content-Type': 'application/json'})
        print("Respuesta:", response.text)
    except Exception as e:
        print("Error:", e)


def borrar_datos(datos_, url= "http://localhost:5678/webhook/eliminar-datos"):
    datos = {
        **datos_,
        
    }
    # Convertir el diccionario a una cadena JSON manualmente, usando nuestro serializador personalizado
    try:
        datos_json = json.dumps(datos, default=json_serializer)
    except TypeError as e:
        print(f"Error al serializar los datos: {e}")
        return

    # Enviar la solicitud con el JSON ya serializado
    try:
        response = requests.post(url, data=datos_json, headers={'Content-Type': 'application/json'})
        print("Respuesta:", response.text)
    except Exception as e:
        print("Error:", e)


@login_required
def agendar_proxima_cita(request):
    """View to add a next consultation."""
    mascotas = Mascotas.objects.all().select_related('cliente')
    mascota_id = request.GET.get('mascota') or request.POST.get('mascota')
    
    datos_mascota = None

    # 🔹 Cargar datos de la mascota cuando se selecciona una
    if mascota_id:
        try:
            mascota = Mascotas.objects.get(pk=mascota_id)
            # 🔹 Preparar datos de la mascota para mostrar en el template
            datos_mascota = {
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
            datos_mascota_n8n = {
                'nombre': mascota.nombre,
                'especie': mascota.especie,
                'raza': mascota.raza,
                'peso': mascota.peso,
                'sexo': mascota.get_sexo_display(),
                'cliente_nombre': mascota.cliente.nombre,
                'cliente_email': mascota.cliente.email,
            }

            
        except Mascotas.DoesNotExist:
            mascota_id = None

    # 🔹 POST: Guardar nueva cita
    if request.method == 'POST':

        form = SiguientesCitasForm(request.POST)
        if form.is_valid():
            proximaCita = form.save(commit=False)
            mascota_id = request.POST.get('mascota')
                

            if mascota_id:
                proximaCita.mascota_id = mascota_id
                #validacion 
                proximaCita, veterinario, veterinarioEmail=  permisos(request, proximaCita)
                proximaCita.save()
                messages.success(request, "Cita agendada correctamente.")
                datos_formulario = {
                    'ID': str(proximaCita.pk),
                    'fecha_cita': form.cleaned_data["fechaSiguienteCita"],
                    'motivo' : form.cleaned_data["descripcionCita"],
                    'tipo_cita' : form.cleaned_data["tipoCita"],
                    'veterinaria' : form.cleaned_data["clinicaVeterinaria"],
                    'veterinario': str(veterinario), 
                    'correo_veterinario': str(veterinarioEmail), 
                    'mensaje_Enviado' : "no", 
                    'sheet': 'agenda'
                }
                
                enviar_datos(datos_mascota_n8n, datos_formulario)
                return redirect('index-agenda')
            else:
                form.add_error(None, "Debe seleccionar una mascota antes de guardar.")
    else:
        form = SiguientesCitasForm(initial={'veterinario': request.user})
 
    return render(request, 'agenda/proximasCitas/agendarCita.html', {
        'form': form, 
        'mascotas': mascotas,
        'mascota_id': mascota_id,
        'datos_mascota': datos_mascota
    })

@login_required
def borrar_proxima_cita(request, pk):
    """View to delete an existing pet."""
    proxConsulta = get_object_or_404(SiguientesCitas, pk=pk)
    proxConsulta.delete()
    datos_ = {
        'ID': str(pk),
        'sheet': 'agenda'
    }
    borrar_datos(datos_)
    return redirect('ver-proximas-citas')

@login_required
def editar_proxima_cita(request, pk):
    """Editar mascota con selector personalizado de cliente."""
    proxConsulta = get_object_or_404(SiguientesCitas, pk=pk)
    mascotas = Mascotas.objects.all().select_related('cliente')
    mascota_id = request.GET.get('mascota') or str(proxConsulta.mascota.id) if proxConsulta.mascota else None
    
    initial_data = {}
    datos_mascota = None

    # 🔹 Cargar datos de la mascota cuando se selecciona una o la actual
    if mascota_id:
        try:
            mascota = Mascotas.objects.get(pk=mascota_id)
            # 🔹 Preparar datos de la mascota para mostrar en el template
            datos_mascota = {
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
            datos_mascota_n8n = {
                'nombre': mascota.nombre,
                'especie': mascota.especie,
                'raza': mascota.raza,
                'peso': mascota.peso,
                'sexo': mascota.get_sexo_display(),
                'cliente_nombre': mascota.cliente.nombre,
                'cliente_email': mascota.cliente.email,
            }
            
        except Mascotas.DoesNotExist:
            mascota_id = None

    # 🔹 POST: Guardar cambios en la cita
    if request.method == 'POST':
        form = UpdateSiguienteCitaForm(request.POST, instance=proxConsulta)
        if form.is_valid():
            proxConsultaEditada = form.save(commit=False)
            mascota_id = request.POST.get('mascota')
            if mascota_id:
                proxConsultaEditada.mascota_id = mascota_id
            proxConsultaEditada.save()
            if proxConsultaEditada.asistencia == 'Pendiente':
                datos_formulario = {
                    'ID': str(proxConsultaEditada.pk),
                    'fecha_cita': form.cleaned_data["fechaSiguienteCita"],
                    'motivo' : form.cleaned_data["descripcionCita"],
                    'tipo_cita' : form.cleaned_data["tipoCita"],
                    'veterinaria' : form.cleaned_data["clinicaVeterinaria"],
                    'veterinario': str(request.user), 
                    'correo_veterinario': str(request.user.email), 
                    'mensaje_Enviado' : "no", 
                    'sheet': 'agenda'
                }
                enviar_datos(datos_mascota_n8n, datos_formulario, "http://localhost:5678/webhook/editar-datos")
            messages.success(request, "Cita actualizada correctamente.")
            return redirect('ver-proximas-citas')
    else:
        form = UpdateSiguienteCitaForm(instance=proxConsulta)

    return render(request, 'agenda/proximasCitas/editarProximaCita.html', {
        'form': form,
        'mascotas': mascotas,
        'mascota_id': mascota_id,
        'datos_mascota': datos_mascota,
        'cita_actual': proxConsulta
    })


    
def atender_cita(request, pk):
    cita = get_object_or_404(SiguientesCitas, pk=pk)
    cita.asistencia = 'Si asistió'
    cita.save()
    mascota = cita.mascota
    
    if cita.tipoCita == 'Consulta':
        return redirect('nueva-consulta')
    
    elif cita.tipoCita == 'Operación médica':
        return redirect('crear_operacion')
    
    elif cita.tipoCita == 'Desparasitación':
        return redirect('nueva_desparasitacion')
    
    elif cita.tipoCita == 'Vacunación':
        return redirect('nueva_vacunacion')
    
    elif cita.tipoCita == 'Servicio de estética':
        return redirect('nuevo-servicio-estetica')
    else:
        return redirect('ver-proximas-citas')