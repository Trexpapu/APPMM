from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import EsteticaForm, EsteticaUpdateForm
from . import services, pdf_services

@login_required
def indexInicioEstetica(request):
    return render(request, 'estetica/indexEstetica.html')

@login_required
def servicio_estetica_crear(request):
    mascotas = services.get_todas_mascotas()
    mascota_id = request.GET.get('mascota') or request.POST.get('mascota')
    
    initial_data = {}
    datos_mascota = None
    mascota_obj = services.get_mascota_by_id(mascota_id)

    if mascota_obj:
        datos_mascota = services.get_datos_mascota(mascota_obj)
    else:
        mascota_id = None

    if request.method == 'POST':
        form = EsteticaForm(request.POST, request.FILES, initial=initial_data)
        if form.is_valid():
            services.save_estetica(request, form)
            messages.success(request, "Servicio de estética registrado correctamente.")
            return redirect('index-estetica')
    else:
        form = EsteticaForm(initial=initial_data)
        form.initial['estilista'] = request.user.id
    
    return render(request, 'estetica/nuevoServicio.html', {
        'form': form, 'mascotas': mascotas, 'mascota_id': mascota_id,
        'datos_mascota': datos_mascota, 'title': 'Nuevo Servicio de Estética'
    })

@login_required
def historial_estetica(request):
    """View that renders a table with all estética records and their associated information."""
    context = services.get_historial_esteticas(request)
    return render(request, 'estetica/historialServicios.html', context)

@login_required
def servicio_estetica_editar(request, pk):
    """Editar servicio de estética existente."""
    estetica = services.get_estetica_by_id(pk)
    mascotas = services.get_todas_mascotas()
    
    mascota_id = request.GET.get('mascota') or request.POST.get('mascota')
    if not mascota_id and estetica.mascota:
        mascota_id = str(estetica.mascota.id)
        
    datos_mascota = None
    mascota_obj = services.get_mascota_by_id(mascota_id)

    if mascota_obj:
        datos_mascota = services.get_datos_mascota(mascota_obj)
    else:
        mascota_id = None

    if request.method == 'POST':
        form = EsteticaUpdateForm(request.POST, instance=estetica)
        if form.is_valid():
            services.update_estetica(request, form, mascota_id, mascota_obj)
            messages.success(request, "Servicio de estética actualizado correctamente.")
            return redirect('servicio_estetica_detalle', pk=estetica.pk)
    else:
        form = EsteticaUpdateForm(instance=estetica)

    return render(request, 'estetica/editarServicio.html', {
        'form': form, 'mascotas': mascotas, 'mascota_id': mascota_id,
        'datos_mascota': datos_mascota, 'estetica_actual': estetica
    })

@login_required
def servicio_estetica_detalle(request, pk):
    """Vista para ver el detalle completo de un servicio de estética."""
    estetica = services.get_estetica_by_id(pk)
    datos_mascota = services.get_datos_mascota(estetica.mascota)
    
    return render(request, 'estetica/detalleServicio.html', {
        'estetica': estetica, 'datos_mascota': datos_mascota,
    })

@login_required
def servicio_estetica_eliminar(request, pk):
    """View to delete an existing estética service."""
    services.delete_estetica_by_id(pk)
    return redirect('historial-estetica')

@login_required
def generar_pdf_estetica(request, pk):
    """Generar PDF con los datos del servicio de estética"""
    estetica = services.get_estetica_by_id(pk)
    return pdf_services.generar_pdf_estetica(estetica)