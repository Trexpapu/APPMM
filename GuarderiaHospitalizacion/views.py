from django.shortcuts import render
from .models import *
from ClientesMascotas.models import *
from .forms import *
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from Procedimientos.views import encode_image_to_base64
from django.db.models import Q
# Create your views here.
@login_required
def index_guarderia_hospitalizacion(request):
    return render(request, 'guarderiaHospitalizacion/indexGuarderiaHospitalizacion.html')


@login_required
def servicio_guarderia_crear(request):
    mascotas = Mascotas.objects.all().select_related('cliente')
    mascota_id = request.GET.get('mascota') or request.POST.get('mascota')
    
    initial_data = {}
    datos_mascota = None

    # 🔹 Cargar datos de la mascota cuando se selecciona una
    if mascota_id:
        try:
            mascota = Mascotas.objects.get(pk=mascota_id)
            # ✅ DATOS DE MASCOTA - Siempre se cargan
            initial_data.update({
                'alimento': mascota.alimento,
            })
            
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
            }
            
        except Mascotas.DoesNotExist:
            mascota_id = None

    # 🔹 POST: Guardar nueva guardería
    if request.method == 'POST':
        form = GuarderiaForm(request.POST, request.FILES, initial=initial_data)
        if form.is_valid():
            guarderia = form.save(commit=False)
            
            # Procesar imágenes
            if 'fotoAntes' in request.FILES:
                guarderia.fotoAntes = encode_image_to_base64(request.FILES['fotoAntes'])
            if 'fotoDespues' in request.FILES:
                guarderia.fotoDespues = encode_image_to_base64(request.FILES['fotoDespues'])
            mascota = form.cleaned_data.get('mascota')
            mascotapk = mascota.pk 
            mascota = get_object_or_404(Mascotas, pk=mascotapk)
            mascota.alimento = form.cleaned_data.get('alimento') or mascota.alimento
            mascota.save()
            guarderia.save()
            messages.success(request, "Servicio de guardería registrado correctamente.")
            return redirect('index-procedimientos')
    else:
        form = GuarderiaForm(initial=initial_data)
    
    return render(request, 'guarderiaHospitalizacion/guarderia/nuevoServicio.html', {
        'form': form,
        'mascotas': mascotas,
        'mascota_id': mascota_id,
        'datos_mascota': datos_mascota,
        'title': 'Nuevo Servicio de Guardería'
    })



@login_required
def historial_guarderia(request):
    """View that renders a table with all guarderia records and their associated information."""
    guarderias = Guarderia.objects.all().select_related('mascota', 'mascota__cliente').order_by('-fechaEntrada')
    
    # Filtros
    query_cliente = request.GET.get('q_cliente', '').strip().lower()
    query_mascota = request.GET.get('q_mascota', '').strip().lower()
    query_veterinaria = request.GET.get('q_veterinaria', '')
    query_fecha_entrada = request.GET.get('q_fecha_entrada', '')
    query_estado = request.GET.get('q_estado', '')  # Nuevo filtro por estado
    
    # Aplicar filtros combinados
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
    
    if query_estado:  # Nuevo filtro por estado
        guarderias = guarderias.filter(estado=query_estado)
    
    # Datos para los filtros
    clinicas = Guarderia.CLINICAS
    estados = Guarderia.ESTADOS  # Obtenemos las opciones de estado del modelo
    
    # Determinar si hay filtros activos
    filtros_activos = any([query_cliente, query_mascota, query_veterinaria, query_fecha_entrada, query_estado])
    
    return render(request, 'guarderiaHospitalizacion/guarderia/historialGuarderia.html', {
        'guarderias': guarderias,
        'clinicas': clinicas,
        'estados': estados,  # Pasamos los estados al contexto
        'query_cliente': query_cliente,
        'query_mascota': query_mascota,
        'query_veterinaria': query_veterinaria,
        'query_fecha_entrada': query_fecha_entrada,
        'query_estado': query_estado,  # Pasamos el estado seleccionado
        'filtros_activos': filtros_activos
    })





@login_required
def servicio_guarderia_editar(request, pk):
    """Editar servicio de guardería existente."""
    guarderia = get_object_or_404(Guarderia, pk=pk)
    mascotas = Mascotas.objects.all().select_related('cliente')
    mascota_id = request.GET.get('mascota') or str(guarderia.mascota.id) if guarderia.mascota else None
    
    datos_mascota = None

    # 🔹 Cargar datos de la mascota cuando se selecciona una o la actual
    if mascota_id:
        try:
            mascota = Mascotas.objects.get(pk=mascota_id)
            # 🔹 Preparar datos de la mascota para mostrar en el template (solo información)
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
            }
            
        except Mascotas.DoesNotExist:
            mascota_id = None

    # 🔹 POST: Guardar cambios en la guardería
    if request.method == 'POST':
        form = GuarderiaUpdateForm(request.POST, instance=guarderia)
        if form.is_valid():
            guarderia_editada = form.save(commit=False)
            mascota_id = request.POST.get('mascota')
            if mascota_id:
                guarderia_editada.mascota_id = mascota_id
            
            # 🔹 MANEJAR FOTO ANTES - SIGUIENDO LA MISMA LÓGICA QUE OPERACIONES
            if 'fotoAntes' in request.FILES and request.FILES['fotoAntes']:
                # Nueva imagen subida - convertir a base64
                guarderia_editada.fotoAntes = encode_image_to_base64(request.FILES['fotoAntes'])
            else:
                # Mantener la imagen existente - NO hacer nada, ya está en la instancia
                pass  # Django automáticamente mantiene el valor existente
            
            # 🔹 MANEJAR FOTO DESPUÉS - SIGUIENDO LA MISMA LÓGICA QUE OPERACIONES
            if 'fotoDespues' in request.FILES and request.FILES['fotoDespues']:
                # Nueva imagen subida - convertir a base64
                guarderia_editada.fotoDespues = encode_image_to_base64(request.FILES['fotoDespues'])
            else:
                # Mantener la imagen existente - NO hacer nada, ya está en la instancia
                pass
            
            guarderia_editada.save()
            messages.success(request, "Servicio de guardería actualizado correctamente.")
            return redirect('servicio_guarderia_detalle', pk=guarderia.pk)
    else:
        form = GuarderiaUpdateForm(instance=guarderia)

    return render(request, 'guarderiaHospitalizacion/guarderia/editarServicio.html', {
        'form': form,
        'mascotas': mascotas,
        'mascota_id': mascota_id,
        'datos_mascota': datos_mascota,
        'guarderia_actual': guarderia
    })

@login_required
def servicio_guarderia_detalle(request, pk):
    """Vista para ver el detalle completo de un servicio de guardería."""
    guarderia = get_object_or_404(Guarderia, pk=pk)
    
    # Preparar datos de la mascota para mostrar
    datos_mascota = {
        'nombre': guarderia.mascota.nombre,
        'especie': guarderia.mascota.especie,
        'raza': guarderia.mascota.raza,
        'fechaNacimiento': guarderia.mascota.fechaNacimiento,
        'peso': guarderia.mascota.peso,
        'sexo': guarderia.mascota.get_sexo_display(),
        'vacunas': guarderia.mascota.vacunas,
        'alergias': guarderia.mascota.alergias,
        'ultimaDesparasitacion': guarderia.mascota.ultimaDesparasitacion,
        'ultimoDesparasitante': guarderia.mascota.ultimoDesparasitante,
        'alimento': guarderia.mascota.alimento,
        'cliente_nombre': guarderia.mascota.cliente.nombre,
        'cliente_telefono': guarderia.mascota.cliente.telefono,
        'cliente_email': guarderia.mascota.cliente.email,
        'vive': guarderia.mascota.vive,
    }
    
    return render(request, 'guarderiaHospitalizacion/guarderia/detalleServicio.html', {
        'guarderia': guarderia,
        'datos_mascota': datos_mascota,
    })