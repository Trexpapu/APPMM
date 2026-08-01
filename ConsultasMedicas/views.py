from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
import os
from .forms import ConsultaMedicaForm, DocumentoConsultaUpdateForm, RecetaMedicaForm
from . import services, pdf_services

@login_required
def indexInicioConsultas(request):
    return render(request, 'consultasMedicas/consultasMedicasBase/indexConsultas.html')

@login_required
def nueva_consulta(request):
    """Vista para crear una nueva consulta médica"""
    mascotas = services.get_todas_mascotas()
    mascota_id = request.GET.get('mascota') or request.POST.get('mascota')
    cargar_prev = request.GET.get('cargar_prev')

    initial_data = {}
    datos_mascota = None
    mascota = services.get_mascota_by_id(mascota_id)

    if mascota:
        datos_mascota = services.get_datos_mascota(mascota)
        initial_data.update({
            'peso': mascota.peso, 'vacunas': mascota.vacunas, 'alergias': mascota.alergias,
            'ultimaDesparasitacion': mascota.ultimaDesparasitacion, 
            'ultimoDesparasitante': mascota.ultimoDesparasitante, 'alimento': mascota.alimento
        })
        
        if cargar_prev == "1":
            prev_data = services.get_ultima_consulta_data(mascota_id)
            if prev_data:
                initial_data.update(prev_data)
                messages.info(request, "Se cargaron los datos de la última consulta.")
    else:
        mascota_id = None

    if request.method == 'POST':
        form = ConsultaMedicaForm(request.POST, initial=initial_data)
        if form.is_valid():
            if mascota_id:
                services.save_consulta(request, form, mascota_id)
                messages.success(request, "Consulta médica y documentos guardados correctamente.")
                return redirect('index-consultas')
            else:
                form.add_error(None, "Debe seleccionar una mascota antes de guardar.")
    else:
        form = ConsultaMedicaForm(initial=initial_data)

    mostrar_pregunta = False
    if mascota_id and not cargar_prev:
        mostrar_pregunta = bool(services.get_ultima_consulta_data(mascota_id))

    return render(
        request, 'consultasMedicas/consultasMedicasBase/nuevaConsulta.html',
        {
            'form': form, 'mascotas': mascotas, 'mostrar_pregunta': mostrar_pregunta,
            'mascota_id': mascota_id, 'datos_mascota': datos_mascota,
        }
    )

@login_required
def ver_consultas(request):
    """View that renders a table with all consultations and related info."""
    context = services.get_consultas_list(request)
    return render(request, 'consultasMedicas/consultasMedicasBase/verConsultas.html', context)

@login_required
def detalle_consulta(request, consulta_id):
    """Vista para ver los detalles de una consulta médica específica"""
    consulta = services.get_consulta_by_id(consulta_id)
    documentos = services.get_documentos_de_consulta(consulta)
    return render(request, 'consultasMedicas/consultasMedicasBase/verDetalleConsulta.html', {
        'consulta': consulta, 'documentos': documentos
    })

@login_required
def descargar_documento(request, documento_id):
    """Vista para descargar un documento específico"""
    documento = services.get_documento_by_id(documento_id)
    if documento.consulta:
        file_path = documento.archivo.path
        if os.path.exists(file_path):
            with open(file_path, 'rb') as file:
                response = HttpResponse(file.read(), content_type='application/octet-stream')
                response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
                return response
    return HttpResponse("Archivo no encontrado", status=404)

@login_required
def editar_consulta(request, consulta_id):
    """Vista para editar una consulta médica existente"""
    consulta = services.get_consulta_by_id(consulta_id)
    documentos_existentes = services.get_documentos_de_consulta(consulta)
    mascota_seleccionada = consulta.mascota
    mascotas = services.get_todas_mascotas()
    datos_mascota = services.get_datos_mascota(mascota_seleccionada)

    if request.method == 'POST':
        form = ConsultaMedicaForm(request.POST, instance=consulta)
        if form.is_valid():
            services.update_consulta(request, form, consulta)
            messages.success(request, "Consulta médica y documentos actualizados correctamente.")
            return redirect('detalle-consulta', consulta_id=consulta.id)
    else:
        form = ConsultaMedicaForm(instance=consulta)

    return render(request, 'consultasMedicas/consultasMedicasBase/editarConsulta.html', {
        'form': form, 'consulta': consulta, 'documentos_existentes': documentos_existentes,
        'mascotas': mascotas, 'mascota_seleccionada': mascota_seleccionada, 'datos_mascota': datos_mascota,
    })

@login_required
def eliminar_documento(request, documento_id):
    """Vista para eliminar un documento específico"""
    if request.method == 'POST':
        consulta_id = services.delete_documento_by_id(documento_id)
        messages.success(request, "Documento eliminado correctamente.")
        return redirect('editar_consulta', consulta_id=consulta_id)
    
    # Si no es POST, solo devolvemos a la consulta
    documento = services.get_documento_by_id(documento_id)
    return redirect('editar_consulta', consulta_id=documento.consulta.id)

@login_required
def borrar_consulta(request, pk):
    """View to delete an existing consultation."""
    services.delete_consulta_by_id(pk)
    return redirect('ver-consultas')

@login_required
def generar_pdf_consulta(request, consulta_id):
    """Generar PDF con los datos de la consulta médica"""
    consulta = services.get_consulta_by_id(consulta_id)
    documentos = services.get_documentos_de_consulta(consulta)
    return pdf_services.generar_pdf_consulta(consulta, documentos)

@login_required
def receta_medica(request):
    """Vista para generar recetas médicas"""
    form = RecetaMedicaForm(request.POST or None)
    mascota_id = request.GET.get('mascota')
    datos_mascota = None
    mascota_obj = services.get_mascota_by_id(mascota_id)
    
    if mascota_obj:
        datos_mascota = services.get_datos_mascota(mascota_obj)
        if form.is_bound:
            form.data = form.data.copy()
            form.data['mascota'] = mascota_id
        else:
            form.initial['mascota'] = mascota_id
    elif mascota_id:
        mascota_id = None
        messages.error(request, "Mascota no encontrada")
    
    if request.method == 'POST' and form.is_valid():
        mascota_obj_form = form.cleaned_data['mascota']
        if request.POST.get('preview'):
            datos_receta = {
                'mascota': mascota_obj_form, 'veterinario': form.cleaned_data['veterinario'],
                'veterinaria': form.cleaned_data['veterinaria'], 'fecha': form.cleaned_data['fecha'],
                'descripcion': form.cleaned_data['descripcion']
            }
            services.enviar_datos_webhook(datos_mascota, datos_receta)
        else:
            return pdf_services.generar_pdf_receta(form.cleaned_data, datos_mascota, mascota_obj_form)
    
    return render(request, 'consultasMedicas/consultasMedicasBase/recetaMedica.html', {
        'form': form, 'mascota_id': mascota_id, 'datos_mascota': datos_mascota,
    })