from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import (OperacionesForm, OperacionesUpdateForm, ListaVacunasForm, 
                    VacunacionesForm, VacunacionesUpdateForm, ListaDesparasitantesForm, DesparasitacionesForm)
from django.contrib.auth.models import User
from . import services, pdf_services

@login_required
def indexProcedimientos(request):
    return render(request, 'procedimientos/indexProcedimientos.html')

# ---- OPERACIONES ----

@login_required
def crear_operacion(request):
    mascotas = services.get_todas_mascotas()
    veterinarios = User.objects.filter(is_active=True).order_by('first_name', 'last_name')
    
    if request.method == 'POST':
        form = OperacionesForm(request.POST, request.FILES)
        if form.is_valid():
            services.save_operacion(request, form)
            messages.success(request, "Operación registrada correctamente.")
            return redirect('index-procedimientos')
    else:
        form = OperacionesForm(initial={'veterinario': request.user})
    
    return render(request, 'procedimientos/operaciones/nuevaOperacion.html', {
        'form': form, 'mascotas': mascotas, 'veterinarios': veterinarios, 'title': 'Crear Nueva Operación'
    })

@login_required
def editar_operacion(request, pk):
    operacion = services.get_operacion_by_id(pk)
    mascotas = services.get_todas_mascotas()
    
    if request.method == 'POST':
        form = OperacionesUpdateForm(request.POST, instance=operacion)
        if form.is_valid():
            services.update_operacion(request, form)
            messages.success(request, "Operación actualizada correctamente.")
            return redirect('detalle_operacion', pk=operacion.pk)
    else:
        form = OperacionesUpdateForm(instance=operacion)
    
    return render(request, 'procedimientos/operaciones/editarOperacion.html', {
        'form': form, 'operacion': operacion, 'mascotas': mascotas, 'title': 'Editar Operación'
    })

@login_required
def historial_operaciones(request):
    context = services.get_historial_operaciones(request)
    context['veterinarios'] = User.objects.filter(is_active=True).order_by('first_name', 'last_name')
    return render(request, 'procedimientos/operaciones/verOperaciones.html', context)

@login_required
def detalle_operacion(request, pk):
    operacion = services.get_operacion_by_id(pk)
    foto_antes_data = f"data:image/jpeg;base64,{operacion.fotoAntes}" if operacion.fotoAntes else None
    foto_despues_data = f"data:image/jpeg;base64,{operacion.fotoDespues}" if operacion.fotoDespues else None
    
    return render(request, 'procedimientos/operaciones/detalleOperacion.html', {
        'operacion': operacion, 'foto_antes_data': foto_antes_data, 'foto_despues_data': foto_despues_data,
    })

@login_required
def eliminar_operacion(request, pk):
    services.delete_operacion_by_id(pk)
    return redirect('historial_operaciones')

@login_required
def generar_pdf_operacion(request, operacion_id):
    operacion = services.get_operacion_by_id(operacion_id)
    return pdf_services.generar_pdf_operacion(operacion)


# ---- VACUNACIONES ----

@login_required
def indexVacunas(request):
    return render(request, 'procedimientos/vacunas/indexVacunas.html')

@login_required
def lista_vacunas(request):
    context = services.get_lista_vacunas(request)
    return render(request, 'procedimientos/vacunas/verVacunas.html', context)

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
    return render(request, 'procedimientos/vacunas/agregarVacuna.html', {'form': form, 'title': 'Agregar Vacuna'})

@login_required
def editar_vacuna(request, pk):
    vacuna = services.get_lista_vacuna_by_id(pk)
    if request.method == 'POST':
        form = ListaVacunasForm(request.POST, instance=vacuna)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Vacuna actualizada exitosamente.")
            return redirect('lista_vacunas')
    else:
        form = ListaVacunasForm(instance=vacuna)
    return render(request, 'procedimientos/vacunas/editarVacuna.html', {'form': form, 'vacuna': vacuna, 'title': 'Editar Vacuna'})

@login_required
def eliminar_vacuna(request, pk):
    services.delete_lista_vacuna_by_id(pk)
    return redirect('lista_vacunas')

@login_required
def nueva_vacunacion(request):
    mascotas = services.get_todas_mascotas()
    veterinarios = User.objects.filter(is_active=True).order_by('first_name', 'last_name')
    if request.method == 'POST':
        form = VacunacionesForm(request.POST)
        if form.is_valid():
            services.save_vacunacion(request, form)
            messages.success(request, "✅ Vacunación registrada exitosamente.")
            return redirect('index-procedimientos')
    else:
        form = VacunacionesForm(initial={'veterinario': request.user})
    return render(request, 'procedimientos/vacunaciones/nuevaVacunacion.html', {
        'form': form, 'mascotas': mascotas, 'veterinarios': veterinarios,
    })

@login_required
def historial_vacunaciones(request):
    context = services.get_historial_vacunaciones(request)
    context['veterinarios'] = User.objects.filter(is_active=True).order_by('first_name', 'last_name')
    return render(request, 'procedimientos/vacunaciones/verVacunaciones.html', context)

@login_required
def editar_vacunacion(request, pk):
    vacunacion = services.get_vacunacion_by_id(pk)
    veterinarios = User.objects.filter(is_active=True).order_by('first_name', 'last_name')
    if request.method == 'POST':
        form = VacunacionesUpdateForm(request.POST, instance=vacunacion)
        if form.is_valid():
            services.update_vacunacion(request, form)
            messages.success(request, "✅ Vacunación actualizada exitosamente.")
            return redirect('historial_vacunaciones')
    else:
        form = VacunacionesUpdateForm(instance=vacunacion)
    return render(request, 'procedimientos/vacunaciones/editarVacunacion.html', {
        'form': form, 'vacunacion': vacunacion, 'veterinarios': veterinarios,
    })

@login_required
def eliminar_vacunacion(request, pk):
    services.delete_vacunacion_by_id(pk)
    return redirect('historial_vacunaciones')


# ---- DESPARASITACIONES ----

@login_required
def indexDesparasitantes(request):
    return render(request, 'procedimientos/desparasitantes/indexDesparasitantes.html')

@login_required
def lista_desparasitantes(request):
    context = services.get_lista_desparasitantes(request)
    return render(request, 'procedimientos/desparasitantes/verDesparasitantes.html', context)

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
    return render(request, 'procedimientos/desparasitantes/agregarDesparasitante.html', {'form': form, 'title': 'Agregar Desparasitante'})

@login_required
def editar_desparasitante(request, pk):
    desparasitante = services.get_lista_desparasitante_by_id(pk)
    if request.method == 'POST':
        form = ListaDesparasitantesForm(request.POST, instance=desparasitante)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Desparasitante actualizado exitosamente.")
            return redirect('lista_desparasitantes')
    else:
        form = ListaDesparasitantesForm(instance=desparasitante)
    return render(request, 'procedimientos/desparasitantes/editarDesparasitante.html', {'form': form, 'desparasitante': desparasitante, 'title': 'Editar Desparasitante'})

@login_required
def eliminar_desparasitante(request, pk):
    services.delete_lista_desparasitante_by_id(pk)
    messages.success(request, "✅ Desparasitante eliminado exitosamente.")
    return redirect('lista_desparasitantes')

@login_required
def nueva_desparasitacion(request):
    mascotas = services.get_todas_mascotas()
    veterinarios = User.objects.filter(is_active=True).order_by('first_name', 'last_name')
    if request.method == 'POST':
        form = DesparasitacionesForm(request.POST)
        if form.is_valid():
            services.save_desparasitacion(request, form)
            messages.success(request, "✅ Desparasitación registrada exitosamente.")
            return redirect('index-procedimientos')
    else:
        form = DesparasitacionesForm(initial={'veterinario': request.user})
    return render(request, 'procedimientos/desparasitaciones/nuevaDesparasitacion.html', {
        'form': form, 'mascotas': mascotas, 'veterinarios': veterinarios,
    })

@login_required
def historial_desparasitaciones(request):
    context = services.get_historial_desparasitaciones(request)
    context['veterinarios'] = User.objects.filter(is_active=True).order_by('first_name', 'last_name')
    return render(request, 'procedimientos/desparasitaciones/verDesparasitaciones.html', context)

@login_required
def eliminar_desparasitacion(request, pk):
    services.delete_desparasitacion_by_id(pk)
    messages.success(request, "✅ Desparasitación eliminada exitosamente.")
    return redirect('historial_desparasitaciones')