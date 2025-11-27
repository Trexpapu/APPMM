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
            peso = form.cleaned_data.get('peso')
            mascota_id = form.cleaned_data.get('mascota')
            mascota = Mascotas.objects.get(pk = mascota_id.pk)
            mascota.peso = peso
            mascota.save()
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



@login_required
def nueva_vacunacion(request):
    mascotas = Mascotas.objects.all().select_related('cliente')
    veterinarios = User.objects.filter(is_active=True).order_by('first_name', 'last_name')
    
    if request.method == 'POST':
        form = VacunacionesForm(request.POST)
        if form.is_valid():
            vacunacion = form.save()
            
            # Actualizar las vacunas de la mascota
            mascota = vacunacion.mascota
            vacunas_data = Vacunaciones.objects.filter(mascota=mascota)
            vacunas_cleaned_data = ", ".join([str(v.vacunas) for v in vacunas_data])
            
            mascota.vacunas = vacunas_cleaned_data
            mascota.save()
            
            messages.success(request, "✅ Vacunación registrada exitosamente.")
            return redirect('index-procedimientos')
    else:
        # Establecer valores por defecto
        initial_data = {
            'veterinario': request.user
        }
        form = VacunacionesForm(initial=initial_data)
    
    return render(request, 'procedimientos/vacunaciones/nuevaVacunacion.html', {
        'form': form, 
        'mascotas': mascotas,
        'veterinarios': veterinarios,
    })


@login_required
def historial_vacunaciones(request):
    """View that renders a table with all vaccinations and their associated information."""
    vacunaciones = Vacunaciones.objects.all().select_related(
        'mascota', 'mascota__cliente', 'veterinario', 'vacunas'
    ).order_by('-fecha')
    
    # Filtros
    query_cliente = request.GET.get('q_cliente', '').strip().lower()
    query_mascota = request.GET.get('q_mascota', '').strip().lower()
    query_veterinario = request.GET.get('q_veterinario', '')  # Cambiado para usar ID
    query_veterinaria = request.GET.get('q_veterinaria', '')
    query_vacuna = request.GET.get('q_vacuna', '').strip().lower()
    query_fecha = request.GET.get('q_fecha', '')
    
    # Aplicar filtros combinados
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
    
    # CAMBIO IMPORTANTE: Ahora filtra por ID en lugar de por nombre
    if query_veterinario:
        vacunaciones = vacunaciones.filter(veterinario_id=query_veterinario)
    
    if query_veterinaria:
        vacunaciones = vacunaciones.filter(clinicaVeterinaria=query_veterinaria)
    
    if query_vacuna:
        vacunaciones = vacunaciones.filter(vacunas__vacuna__icontains=query_vacuna)
    
    if query_fecha:
        vacunaciones = vacunaciones.filter(fecha=query_fecha)
    
    # Datos para los filtros
    veterinarios = User.objects.filter(is_active=True).order_by('first_name', 'last_name')
    clinicas = Vacunaciones.CLINICAS
    vacunas_lista = ListaVacunas.objects.all().order_by('vacuna')
    
    # Determinar si hay filtros activos
    filtros_activos = any([query_cliente, query_mascota, query_veterinario, 
                          query_veterinaria, query_vacuna, query_fecha])
    
    return render(request, 'procedimientos/vacunaciones/verVacunaciones.html', {
        'vacunaciones': vacunaciones,
        'veterinarios': veterinarios,
        'clinicas': clinicas,
        'vacunas_lista': vacunas_lista,
        'query_cliente': query_cliente,
        'query_mascota': query_mascota,
        'query_veterinario': query_veterinario,
        'query_veterinaria': query_veterinaria,
        'query_vacuna': query_vacuna,
        'query_fecha': query_fecha,
        'filtros_activos': filtros_activos
    })

@login_required
def editar_vacunacion(request, pk):
    vacunacion = get_object_or_404(Vacunaciones, pk=pk)
    veterinarios = User.objects.filter(is_active=True).order_by('first_name', 'last_name')
    
    if request.method == 'POST':
        form = VacunacionesUpdateForm(request.POST, instance=vacunacion)
        if form.is_valid():
            vacunacion_actualizada = form.save()
            
            # Actualizar las vacunas de la mascota
            mascota = vacunacion_actualizada.mascota
            vacunas_data = Vacunaciones.objects.filter(mascota=mascota)
            vacunas_cleaned_data = ", ".join([str(v.vacunas) for v in vacunas_data])
            
            mascota.vacunas = vacunas_cleaned_data
            mascota.save()
            
            messages.success(request, "✅ Vacunación actualizada exitosamente.")
            return redirect('historial_vacunaciones')
    else:
        form = VacunacionesUpdateForm(instance=vacunacion)
    
    return render(request, 'procedimientos/vacunaciones/editarVacunacion.html', {
        'form': form,
        'vacunacion': vacunacion,
        'veterinarios': veterinarios,
    })


# Vista para eliminar vacuna
@login_required
def eliminar_vacunacion(request, pk):
    """View to delete an existing pet."""
    vacunacion = get_object_or_404(Vacunaciones, pk=pk)
    mascota = vacunacion.mascota
    vacunacion.delete()
    # Actualizar las vacunas de la mascota
    
    vacunas_data = Vacunaciones.objects.filter(mascota=mascota)
    vacunas_cleaned_data = ", ".join([str(v.vacunas) for v in vacunas_data])
    mascota.vacunas = vacunas_cleaned_data
    mascota.save()
    return redirect('historial_vacunaciones')


@login_required
def agregar_desparasitante(request):
    if request.method == 'POST':
        form = ListaDesparasitantesForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Desparasitante agregado exitosamente.")
            return redirect('lista_desparasitantes')
    else:
        form = ListaDesparasitantesForm()
        
    return render(request, 'procedimientos/desparasitantes/agregarDesparasitante.html', {
        'form': form,
        'title': 'Agregar Desparasitante'
    })


@login_required
def lista_desparasitantes(request):
    desparasitantes = ListaDesparasitantes.objects.all().order_by('desparasitante')
    
    # Filtro por nombre de desparasitante
    query_desparasitante = request.GET.get('q_desparasitante', '')
    if query_desparasitante:
        desparasitantes = desparasitantes.filter(desparasitante__icontains=query_desparasitante)
    
    context = {
        'desparasitantes': desparasitantes,
        'query_desparasitante': query_desparasitante,
    }
    
    return render(request, 'procedimientos/desparasitantes/verDesparasitantes.html', context)



@login_required
def editar_desparasitante(request, pk):
    desparasitante = get_object_or_404(ListaDesparasitantes, pk=pk)
    
    if request.method == 'POST':
        form = ListaDesparasitantesForm(request.POST, instance=desparasitante)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Desparasitante actualizado exitosamente.")
            return redirect('lista_desparasitantes')
    else:
        form = ListaDesparasitantesForm(instance=desparasitante)
    
    return render(request, 'procedimientos/desparasitantes/editarDesparasitante.html', {
        'form': form,
        'desparasitante': desparasitante,
        'title': 'Editar Desparasitante'
    })

@login_required
def eliminar_desparasitante(request, pk):
    desparasitante = get_object_or_404(ListaDesparasitantes, pk=pk)
    desparasitante.delete()
    messages.success(request, "✅ Desparasitante eliminado exitosamente.")
    return redirect('lista_desparasitantes')

@login_required
def indexDesparasitantes(request):
    return render(request, 'procedimientos/desparasitantes/indexDesparasitantes.html')






@login_required
def nueva_desparasitacion(request):
    mascotas = Mascotas.objects.all().select_related('cliente')
    veterinarios = User.objects.filter(is_active=True).order_by('first_name', 'last_name')
    
    if request.method == 'POST':
        form = DesparasitacionesForm(request.POST)
        if form.is_valid():
            # Guardar la desparasitación
            desparasitacion = form.save()
            
            # Actualizar datos de mascota
            mascota = desparasitacion.mascota
            mascota.ultimaDesparasitacion = desparasitacion.fecha
            mascota.ultimoDesparasitante = str(desparasitacion.desparasitante)
            mascota.peso = desparasitacion.peso  # Actualizar el peso con el nuevo valor
            mascota.save()
            
            messages.success(request, "✅ Desparasitación registrada exitosamente.")
            return redirect('index-procedimientos')
    else:
        # Establecer valores por defecto
        initial_data = {
            'veterinario': request.user
        }
        form = DesparasitacionesForm(initial=initial_data)
    
    return render(request, 'procedimientos/desparasitaciones/nuevaDesparasitacion.html', {
        'form': form, 
        'mascotas': mascotas,
        'veterinarios': veterinarios,
    })


@login_required
def historial_desparasitaciones(request):
    """View that renders a table with all deworming records and their associated information."""
    desparasitaciones = Desparasitaciones.objects.all().select_related(
        'mascota', 'mascota__cliente', 'veterinario', 'desparasitante'
    ).order_by('-fecha')
    
    # Filtros
    query_cliente = request.GET.get('q_cliente', '').strip().lower()
    query_mascota = request.GET.get('q_mascota', '').strip().lower()
    query_veterinario = request.GET.get('q_veterinario', '')
    query_veterinaria = request.GET.get('q_veterinaria', '')
    query_desparasitante = request.GET.get('q_desparasitante', '').strip().lower()
    query_fecha = request.GET.get('q_fecha', '')
    
    # Aplicar filtros combinados
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
    
    if query_veterinario:
        desparasitaciones = desparasitaciones.filter(veterinario_id=query_veterinario)
    
    if query_veterinaria:
        desparasitaciones = desparasitaciones.filter(clinicaVeterinaria=query_veterinaria)
    
    if query_desparasitante:
        desparasitaciones = desparasitaciones.filter(desparasitante__desparasitante__icontains=query_desparasitante)
    
    if query_fecha:
        desparasitaciones = desparasitaciones.filter(fecha=query_fecha)
    
    # Datos para los filtros
    veterinarios = User.objects.filter(is_active=True).order_by('first_name', 'last_name')
    clinicas = Desparasitaciones.CLINICAS
    desparasitantes_lista = ListaDesparasitantes.objects.all().order_by('desparasitante')
    
    # Determinar si hay filtros activos
    filtros_activos = any([query_cliente, query_mascota, query_veterinario, 
                          query_veterinaria, query_desparasitante, query_fecha])
    
    return render(request, 'procedimientos/desparasitaciones/verDesparasitaciones.html', {
        'desparasitaciones': desparasitaciones,
        'veterinarios': veterinarios,
        'clinicas': clinicas,
        'desparasitantes_lista': desparasitantes_lista,
        'query_cliente': query_cliente,
        'query_mascota': query_mascota,
        'query_veterinario': query_veterinario,
        'query_veterinaria': query_veterinaria,
        'query_desparasitante': query_desparasitante,
        'query_fecha': query_fecha,
        'filtros_activos': filtros_activos
    })


@login_required
def eliminar_desparasitacion(request, pk):
    
    desparasitacion = get_object_or_404(Desparasitaciones, pk=pk)
    desparasitacion.delete()
    messages.success(request, "✅ Desparasitación eliminada exitosamente.")
    return redirect('historial_desparasitaciones')