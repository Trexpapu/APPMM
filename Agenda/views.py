from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import SiguientesCitasForm, UpdateSiguienteCitaForm
from . import services
from .models import SiguientesCitas
@login_required
def indexAgenda(request):
    return render(request, 'agenda/proximasCitas/indexAgenda.html')

@login_required
def ver_proximas_citas(request):
    context = services.get_proximas_citas(request)
    context['veterinarios'] = User.objects.filter(is_active=True).order_by('first_name', 'last_name')
    
    veterinario_seleccionado = None
    if context.get('query_veterinario'):
        try:
            veterinario_seleccionado = User.objects.get(id=context.get('query_veterinario'))
        except User.DoesNotExist: pass
    context['veterinario_seleccionado'] = veterinario_seleccionado

    return render(request, 'agenda/proximasCitas/verProximasCitas.html', context)

@login_required
def agendar_proxima_cita(request):
    mascotas = services.get_todas_mascotas()
    mascota_id = request.GET.get('mascota') or request.POST.get('mascota')
    
    datos_mascota = None
    mascota_obj = services.get_mascota_by_id(mascota_id)
    if mascota_obj:
        datos_mascota = services.get_datos_mascota(mascota_obj)
    else:
        mascota_id = None

    if request.method == 'POST':
        form = SiguientesCitasForm(request.POST)
        if form.is_valid():
            if mascota_id:
                proximaCita = services.save_cita(form, mascota_id)
                messages.success(request, "Cita agendada correctamente.")
                return redirect('index-agenda')
            else:
                form.add_error(None, "Debe seleccionar una mascota antes de guardar.")
    else:
        form = SiguientesCitasForm(initial={'veterinario': request.user})
 
    return render(request, 'agenda/proximasCitas/agendarCita.html', {
        'form': form, 'mascotas': mascotas, 'mascota_id': mascota_id, 'datos_mascota': datos_mascota
    })

@login_required
def borrar_proxima_cita(request, pk):
    services.delete_cita_by_id(pk)
    return redirect('ver-proximas-citas')

@login_required
def editar_proxima_cita(request, pk):
    proxConsulta = services.get_cita_by_id(pk)
    mascotas = services.get_todas_mascotas()
    mascota_id = request.GET.get('mascota') or (str(proxConsulta.mascota.id) if proxConsulta.mascota else None)
    
    datos_mascota = None
    mascota_obj = services.get_mascota_by_id(mascota_id)
    if mascota_obj:
        datos_mascota = services.get_datos_mascota(mascota_obj)
    else:
        mascota_id = None

    if request.method == 'POST':
        form = UpdateSiguienteCitaForm(request.POST, instance=proxConsulta)
        if form.is_valid():
            if mascota_id:
                proximaCita = services.update_cita(form, mascota_id)
                messages.success(request, "Cita actualizada correctamente.")
                return redirect('ver-proximas-citas')
    else:
        form = UpdateSiguienteCitaForm(instance=proxConsulta)

    return render(request, 'agenda/proximasCitas/editarProximaCita.html', {
        'form': form, 'mascotas': mascotas, 'mascota_id': mascota_id, 'datos_mascota': datos_mascota, 'cita_actual': proxConsulta
    })
    
@login_required
def atender_cita(request, pk):
    
    SiguientesCitas.objects.filter(pk=pk).update(asistencia='Si asistió')
    cita = services.get_cita_by_id(pk)
    
    if cita.tipoCita == 'Consulta': return redirect('nueva-consulta')
    elif cita.tipoCita == 'Operación médica': return redirect('crear_operacion')
    elif cita.tipoCita == 'Desparasitación': return redirect('nueva_desparasitacion')
    elif cita.tipoCita == 'Vacunación': return redirect('nueva_vacunacion')
    elif cita.tipoCita == 'Servicio de estética': return redirect('nuevo-servicio-estetica')
    else: return redirect('ver-proximas-citas')