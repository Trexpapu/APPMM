from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import GuarderiaForm, GuarderiaUpdateForm, HospitalizacionForm, HospitalizacionUpdateForm
from . import services, pdf_services

@login_required
def index_guarderia_hospitalizacion(request):
    return render(request, 'guarderiaHospitalizacion/indexGuarderiaHospitalizacion.html')

# ---- GUARDERIA ----

@login_required
def servicio_guarderia_crear(request):
    mascotas = services.get_todas_mascotas()
    mascota_id = request.GET.get('mascota') or request.POST.get('mascota')
    
    initial_data = {}
    datos_mascota = None
    mascota_obj = services.get_mascota_by_id(mascota_id)

    if mascota_obj:
        initial_data.update({'alimento': mascota_obj.alimento})
        datos_mascota = services.get_datos_mascota(mascota_obj)
        datos_mascota_n8n = services.get_datos_mascota_n8n(mascota_obj)
    else:
        mascota_id = None

    if request.method == 'POST':
        form = GuarderiaForm(request.POST, request.FILES, initial=initial_data)
        if form.is_valid():
            guarderia = services.save_guarderia(request, form)
            messages.success(request, "Servicio de guardería registrado correctamente.")
            datos_formulario = {
                'ID': str(guarderia.pk),
                'fecha_salida': form.cleaned_data["fechaSalidaProgramada"],
                'anticipo' : form.cleaned_data["pagado"],
                'pago_total' : form.cleaned_data["pagoTotal"],
                'veterinaria' : form.cleaned_data["clinicaVeterinaria"],
                'sheet': 'guarderia'
            }
            services.enviar_datos(datos_mascota_n8n, datos_formulario, "http://localhost:5678/webhook/agregar")
            return redirect('index-guarderia-hospitalizacion')
    else:
        form = GuarderiaForm(initial=initial_data)
    
    return render(request, 'guarderiaHospitalizacion/guarderia/nuevoServicio.html', {
        'form': form, 'mascotas': mascotas, 'mascota_id': mascota_id,
        'datos_mascota': datos_mascota, 'title': 'Nuevo Servicio de Guardería'
    })

@login_required
def historial_guarderia(request):
    context = services.get_historial_guarderia(request)
    return render(request, 'guarderiaHospitalizacion/guarderia/historialGuarderia.html', context)

@login_required
def servicio_guarderia_editar(request, pk):
    guarderia = services.get_guarderia_by_id(pk)
    mascotas = services.get_todas_mascotas()
    mascota_id = request.GET.get('mascota') or (str(guarderia.mascota.id) if guarderia.mascota else None)
    
    datos_mascota = None
    mascota_obj = services.get_mascota_by_id(mascota_id)

    if mascota_obj:
        datos_mascota = services.get_datos_mascota(mascota_obj)
        datos_mascota_n8n = services.get_datos_mascota_n8n(mascota_obj)
    else:
        mascota_id = None

    if request.method == 'POST':
        form = GuarderiaUpdateForm(request.POST, instance=guarderia)
        if form.is_valid():
            guarderia_editada = services.update_guarderia(request, form, request.POST.get('mascota'))
            messages.success(request, "Servicio de guardería actualizado correctamente.")
            datos_formulario = {
                'ID': str(guarderia_editada.pk),
                'fecha_salida': form.cleaned_data["fechaSalidaProgramada"],
                'anticipo' : form.cleaned_data["pagado"],
                'pago_total' : form.cleaned_data["pagoTotal"],
                'veterinaria' : form.cleaned_data["clinicaVeterinaria"],
                'sheet': 'guarderia'
            }
            services.enviar_datos(datos_mascota_n8n, datos_formulario, "http://localhost:5678/webhook/editar-datos")
            return redirect('servicio_guarderia_detalle', pk=guarderia.pk)
    else:
        form = GuarderiaUpdateForm(instance=guarderia)

    return render(request, 'guarderiaHospitalizacion/guarderia/editarServicio.html', {
        'form': form, 'mascotas': mascotas, 'mascota_id': mascota_id,
        'datos_mascota': datos_mascota, 'guarderia_actual': guarderia
    })

@login_required
def servicio_guarderia_detalle(request, pk):
    guarderia = services.get_guarderia_by_id(pk)
    datos_mascota = services.get_datos_mascota(guarderia.mascota)
    return render(request, 'guarderiaHospitalizacion/guarderia/detalleServicio.html', {
        'guarderia': guarderia, 'datos_mascota': datos_mascota,
    })

@login_required
def generar_pdf_guarderia(request, pk):
    guarderia = services.get_guarderia_by_id(pk)
    return pdf_services.generar_pdf_guarderia(guarderia)

@login_required
def servicio_guarderia_eliminar(request, pk):
    services.delete_guarderia_by_id(pk)
    return redirect('historial-guarderia')


# ---- HOSPITALIZACION ----

@login_required
def servicio_hospitalizacion_crear(request):
    mascotas = services.get_todas_mascotas()
    mascota_id = request.GET.get('mascota') or request.POST.get('mascota')
    
    initial_data = {}
    datos_mascota = None
    mascota_obj = services.get_mascota_by_id(mascota_id)

    if mascota_obj:
        datos_mascota = services.get_datos_mascota(mascota_obj)
        datos_mascota_n8n = services.get_datos_mascota_n8n(mascota_obj)
    else:
        mascota_id = None

    if request.method == 'POST':
        form = HospitalizacionForm(request.POST, request.FILES, initial=initial_data)
        if form.is_valid():
            hospitalizacion = services.save_hospitalizacion(request, form)
            messages.success(request, "Servicio de hospitalización registrado correctamente.")
            datos_formulario = {
                'ID': str(hospitalizacion.pk),
                'fecha_salida': form.cleaned_data["fechaSalida"],
                'anticipo' : form.cleaned_data["pagado"],
                'pago_total' : form.cleaned_data["pagoTotal"],
                'veterinaria' : form.cleaned_data["clinicaVeterinaria"],
                'sheet': 'hospitalizacion'
            }
            services.enviar_datos(datos_mascota_n8n, datos_formulario, "http://localhost:5678/webhook/agregar")
            return redirect('index-guarderia-hospitalizacion')
    else:
        form = HospitalizacionForm(initial=initial_data)
    
    return render(request, 'guarderiaHospitalizacion/hospitalizacion/nuevoServicio.html', {
        'form': form, 'mascotas': mascotas, 'mascota_id': mascota_id,
        'datos_mascota': datos_mascota, 'title': 'Nuevo Servicio de Hospitalización'
    })

@login_required
def historial_hospitalizacion(request):
    context = services.get_historial_hospitalizacion(request)
    return render(request, 'guarderiaHospitalizacion/hospitalizacion/historialHospitalizacion.html', context)

@login_required
def servicio_hospitalizacion_editar(request, pk):
    hospitalizacion = services.get_hospitalizacion_by_id(pk)
    mascotas = services.get_todas_mascotas()
    mascota_id = request.GET.get('mascota') or request.POST.get('mascota') or (str(hospitalizacion.mascota.id) if hospitalizacion.mascota else None)
    
    datos_mascota = None
    mascota_obj = services.get_mascota_by_id(mascota_id)

    if mascota_obj:
        datos_mascota = services.get_datos_mascota(mascota_obj)
        datos_mascota_n8n = services.get_datos_mascota_n8n(mascota_obj)
    else:
        mascota_id = None

    if request.method == 'POST':
        form = HospitalizacionUpdateForm(request.POST, instance=hospitalizacion)
        if form.is_valid():
            hospitalizacion_editada = services.update_hospitalizacion(request, form, mascota_id, mascota_obj)
            messages.success(request, "Servicio de hospitalización actualizado correctamente.")
            datos_formulario = {
                'ID': str(hospitalizacion_editada.pk),
                'fecha_salida': form.cleaned_data["fechaSalida"],
                'anticipo' : form.cleaned_data["pagado"],
                'pago_total' : form.cleaned_data["pagoTotal"],
                'veterinaria' : form.cleaned_data["clinicaVeterinaria"],
                'sheet': 'hospitalizacion'
            }
            services.enviar_datos(datos_mascota_n8n, datos_formulario, "http://localhost:5678/webhook/editar-datos")
            return redirect('servicio_hospitalizacion_detalle', pk=hospitalizacion.pk)
    else:
        form = HospitalizacionUpdateForm(instance=hospitalizacion)

    return render(request, 'guarderiaHospitalizacion/hospitalizacion/editarServicio.html', {
        'form': form, 'mascotas': mascotas, 'mascota_id': mascota_id,
        'datos_mascota': datos_mascota, 'hospitalizacion_actual': hospitalizacion
    })

@login_required
def servicio_hospitalizacion_detalle(request, pk):
    hospitalizacion = services.get_hospitalizacion_by_id(pk)
    datos_mascota = services.get_datos_mascota(hospitalizacion.mascota)
    return render(request, 'guarderiaHospitalizacion/hospitalizacion/detalleServicio.html', {
        'hospitalizacion': hospitalizacion, 'datos_mascota': datos_mascota,
    })

@login_required
def generar_pdf_hospitalizacion(request, pk):
    hospitalizacion = services.get_hospitalizacion_by_id(pk)
    return pdf_services.generar_pdf_hospitalizacion(hospitalizacion)

@login_required
def servicio_hospitalizacion_eliminar(request, pk):
    services.delete_hospitalizacion_by_id(pk)
    return redirect('historial-hospitalizacion')
