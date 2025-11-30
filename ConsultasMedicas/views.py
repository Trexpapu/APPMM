from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from ClientesMascotas.models import *
from django.utils.dateparse import parse_date
from datetime import datetime
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.units import inch
from reportlab.lib import colors
from io import BytesIO
from django.utils import timezone

# Create your views here.
@login_required
def indexInicioConsultas(request):
    return render(request, 'consultasMedicas/consultasMedicasBase/indexConsultas.html')


@login_required
def nueva_consulta_desde_cita(request, mascota_id):
    """
    Vista para crear una nueva consulta médica desde una cita programada
    La mascota ya está preseleccionada y no se puede cambiar
    """
    try:
        mascota = Mascotas.objects.get(pk=mascota_id)
    except Mascotas.DoesNotExist:
        messages.error(request, "La mascota seleccionada no existe.")
        return redirect('ver-proximas-citas')
    
    # Obtener parámetro para cargar consulta previa
    cargar_prev = request.GET.get('cargar_prev')
    
    # Cargar datos iniciales de la mascota
    initial_data = {
        'peso': mascota.peso,
        'vacunas': mascota.vacunas,
        'alergias': mascota.alergias,
        'ultimaDesparasitacion': mascota.ultimaDesparasitacion, 
        'ultimoDesparasitante': mascota.ultimoDesparasitante,
        'alimento': mascota.alimento
    }
    
    # Preparar datos de la mascota para mostrar en el template
    datos_mascota = {
        'nombre': mascota.nombre,
        'especie': mascota.especie,
        'raza': mascota.raza,
        'fechaNacimiento': mascota.fechaNacimiento,
        'sexo': mascota.get_sexo_display(),
        'cliente_nombre': mascota.cliente.nombre,
        'cliente_telefono': mascota.cliente.telefono,
        'cliente_email': mascota.cliente.email,
    }
    
    # 🔹 Cargar consulta anterior SOLO si el usuario lo solicita
    if cargar_prev == "1":
        ultima_consulta = (
            ConsultasMedicas.objects.filter(mascota_id=mascota_id)
            .order_by('-fechaConsulta')
            .first()
        )
        if ultima_consulta:
            exclude_fields = ['id', 'fechaConsulta', 'peso', 'vacunas', 'alergias', 'mascota', 'ultimaDesparasitacion', 'ultimoDesparasitante']
            for field in ConsultasMedicas._meta.get_fields():
                if (field.name not in exclude_fields and 
                    hasattr(ultima_consulta, field.name)):
                    initial_data[field.name] = getattr(ultima_consulta, field.name)
            messages.info(request, "Se cargaron los datos de la última consulta.")

    # POST: Guardar nueva consulta
    if request.method == 'POST':
        form = ConsultaMedicaForm(request.POST, initial=initial_data)
        
        if form.is_valid():
            nConsulta = form.save(commit=False)
            nConsulta.mascota = mascota  # Usar la mascota de la cita
            nConsulta.veterinario = request.user
            nConsulta.save()

            # Actualizar datos de la mascota (solo peso y alergias)
            mascota.peso = form.cleaned_data.get('peso') or mascota.peso
            mascota.alergias = form.cleaned_data.get('alergias') or mascota.alergias
            mascota.alimento = form.cleaned_data.get('alimento') or mascota.alimento
            mascota.save()

            # Guardar documentos
            archivos = request.FILES.getlist('archivo')
            descripciones = request.POST.getlist('descripcion')
            
            for i, archivo in enumerate(archivos):
                if archivo:
                    descripcion = descripciones[i] if i < len(descripciones) else ''
                    DocumentosConsulta.objects.create(
                        consulta=nConsulta,
                        archivo=archivo,
                        descripcion=descripcion
                    )

            messages.success(request, "Consulta médica y documentos guardados correctamente.")
            return redirect('index-consultas')
    else:
        form = ConsultaMedicaForm(initial=initial_data)

    # 🔹 Determinar si mostrar la pregunta de cargar consulta previa
    mostrar_pregunta = False
    if not cargar_prev:
        hay_consulta_previa = ConsultasMedicas.objects.filter(mascota_id=mascota_id).exists()
        mostrar_pregunta = hay_consulta_previa

    return render(
        request,
        'consultasMedicas/consultasMedicasBase/nuevaConsultaDesdeCita.html',
        {
            'form': form,
            'mascota': mascota,
            'datos_mascota': datos_mascota,
            'mascota_id': mascota_id,
            'mostrar_pregunta': mostrar_pregunta,
        }
    )


@login_required
def nueva_consulta(request):
    """
    Vista para crear una nueva consulta médica
    """
    mascotas = Mascotas.objects.all().select_related('cliente')
    mascota_id = request.GET.get('mascota') or request.POST.get('mascota')
    cargar_prev = request.GET.get('cargar_prev')

    initial_data = {}
    mascota = None
    datos_mascota = None

    # 🔹 SIEMPRE cargar datos de la mascota cuando se selecciona una
    if mascota_id:
        try:
            mascota = Mascotas.objects.get(pk=mascota_id)
            # ✅ DATOS DE MASCOTA - Siempre se cargan
            initial_data.update({
                'peso': mascota.peso,
                'vacunas': mascota.vacunas,
                'alergias': mascota.alergias,
                'ultimaDesparasitacion': mascota.ultimaDesparasitacion, 
                'ultimoDesparasitante': mascota.ultimoDesparasitante,
                'alimento': mascota.alimento,
            })
            
            # 🔹 Preparar datos de la mascota para mostrar en el template
            datos_mascota = {
                'nombre': mascota.nombre,
                'especie': mascota.especie,
                'raza': mascota.raza,
                'fechaNacimiento': mascota.fechaNacimiento,
                'sexo': mascota.get_sexo_display(),
                'cliente_nombre': mascota.cliente.nombre,
                'cliente_telefono': mascota.cliente.telefono,
                'cliente_email': mascota.cliente.email,
            }
            
            # 🔹 Cargar consulta anterior SOLO si el usuario lo solicita
            if cargar_prev == "1":
                ultima_consulta = (
                    ConsultasMedicas.objects.filter(mascota_id=mascota_id)
                    .order_by('-fechaConsulta')
                    .first()
                )
                if ultima_consulta:
                    exclude_fields = ['id', 'fechaConsulta', 'peso', 'vacunas', 'alergias', 'mascota', 'ultimaDesparasitacion', 'ultimoDesparasitante', 'alimento']
                    for field in ConsultasMedicas._meta.get_fields():
                        if (field.name not in exclude_fields and 
                            hasattr(ultima_consulta, field.name)):
                            initial_data[field.name] = getattr(ultima_consulta, field.name)
                    messages.info(request, "Se cargaron los datos de la última consulta.")
            
        except Mascotas.DoesNotExist:
            mascota = None

    # 🔹 POST: Guardar nueva consulta
    if request.method == 'POST':
        form = ConsultaMedicaForm(request.POST, initial=initial_data)
        
        if form.is_valid():
            nConsulta = form.save(commit=False)
            mascota_id = request.POST.get('mascota')

            if mascota_id:
                nConsulta.mascota_id = mascota_id
                nConsulta.veterinario = request.user
                nConsulta.save()

                # 🐾 Actualizar datos de la mascota (solo peso y alergias)
                mascota = Mascotas.objects.get(pk=mascota_id)
                mascota.peso = form.cleaned_data.get('peso') or mascota.peso
                mascota.alergias = form.cleaned_data.get('alergias') or mascota.alergias
                mascota.alimento = form.cleaned_data.get('alimento') or mascota.alimento
                # NO actualizamos vacunas, ultimaDesparasitacion ni ultimoDesparasitante aquí
                mascota.save()

                # 📎 GUARDAR DOCUMENTOS usando el modelo DocumentosConsulta
                archivos = request.FILES.getlist('archivo')
                descripciones = request.POST.getlist('descripcion')
                
                for i, archivo in enumerate(archivos):
                    if archivo:
                        descripcion = descripciones[i] if i < len(descripciones) else ''
                        documento = DocumentosConsulta(
                            consulta=nConsulta,
                            archivo=archivo,
                            descripcion=descripcion
                        )
                        documento.save()

                messages.success(request, "Consulta médica y documentos guardados correctamente.")
                return redirect('index-consultas')
            else:
                form.add_error(None, "Debe seleccionar una mascota antes de guardar.")
    else:
        form = ConsultaMedicaForm(initial=initial_data)

    # 🔹 Determinar si mostrar la pregunta de cargar consulta previa
    mostrar_pregunta = False
    if mascota_id and not cargar_prev:
        hay_consulta_previa = ConsultasMedicas.objects.filter(mascota_id=mascota_id).exists()
        mostrar_pregunta = hay_consulta_previa

    return render(
        request,
        'consultasMedicas/consultasMedicasBase/nuevaConsulta.html',
        {
            'form': form,
            'mascotas': mascotas,
            'mostrar_pregunta': mostrar_pregunta,
            'mascota_id': mascota_id,
            'datos_mascota': datos_mascota,
        }
    )



@login_required
def ver_consultas(request):
    """View that renders a table with all consultations and related info."""
    # Obtener todos los registros inicialmente
    consultas = ConsultasMedicas.objects.select_related(
        'mascota', 'mascota__cliente', 'veterinario'
    ).all()
    
    # Obtener parámetros de filtro
    query_cliente = request.GET.get('q_cliente', '').strip()
    query_mascota = request.GET.get('q_mascota', '').strip()
    query_fecha = request.GET.get('q_fecha', '').strip()
    query_veterinario = request.GET.get('q_veterinario', '').strip()
    query_veterinaria = request.GET.get('q_veterinaria', '').strip()
    
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
            consultas = consultas.filter(fechaConsulta__date=fecha_filtro)
        except ValueError:
            # Si la fecha no es válida, ignorar el filtro
            pass
    
    if query_veterinario:
        consultas = consultas.filter(veterinario_id=query_veterinario)
    
    if query_veterinaria:
        consultas = consultas.filter(clinicaVeterinaria=query_veterinaria)
    
    # Obtener datos para los dropdowns
    veterinarios = User.objects.filter(is_active=True).order_by('first_name', 'last_name')
    clinicas = ConsultasMedicas.CLINICAS
    
    # Verificar si hay filtros activos
    filtros_activos = any([query_cliente, query_mascota, query_fecha, query_veterinario, query_veterinaria])
    
    # Obtener objetos para mostrar en los resultados
    veterinario_seleccionado = None
    if query_veterinario:
        try:
            veterinario_seleccionado = User.objects.get(id=query_veterinario)
        except User.DoesNotExist:
            pass
    
    veterinaria_seleccionada = query_veterinaria
    
    # Ordenar de la más nueva a la más vieja
    consultas = consultas.order_by('-fechaConsulta')
    
    context = {
        'consultas': consultas,
        'query_cliente': query_cliente,
        'query_mascota': query_mascota,
        'query_fecha': query_fecha,
        'query_veterinario': query_veterinario,
        'query_veterinaria': query_veterinaria,
        'veterinarios': veterinarios,
        'clinicas': clinicas,
        'filtros_activos': filtros_activos,
        'veterinario_seleccionado': veterinario_seleccionado,
        'veterinaria_seleccionada': veterinaria_seleccionada,
    }
    
    return render(
        request,
        'consultasMedicas/consultasMedicasBase/verConsultas.html',
        context
    )




@login_required
def detalle_consulta(request, consulta_id):
    """Vista para ver los detalles de una consulta médica específica"""
    consulta = get_object_or_404(ConsultasMedicas, id=consulta_id)
    documentos = DocumentosConsulta.objects.filter(consulta=consulta)
    
    return render(request, 'consultasMedicas/consultasMedicasBase/verDetalleConsulta.html', {
        'consulta': consulta,
        'documentos': documentos
    })

@login_required
def descargar_documento(request, documento_id):
    """Vista para descargar un documento específico"""
    documento = get_object_or_404(DocumentosConsulta, id=documento_id)
    
    # Verificar que el documento pertenece a una consulta accesible
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
    consulta = get_object_or_404(ConsultasMedicas, id=consulta_id)
    documentos_existentes = DocumentosConsulta.objects.filter(consulta=consulta)
    
    mascota_seleccionada = consulta.mascota
    mascotas = Mascotas.objects.all()
    
    # 🔹 Preparar datos de la mascota para mostrar (solo información, no para cargar en el form)
    datos_mascota = {
        'nombre': mascota_seleccionada.nombre,
        'especie': mascota_seleccionada.especie,
        'raza': mascota_seleccionada.raza,
        'fechaNacimiento': mascota_seleccionada.fechaNacimiento,
        'sexo': mascota_seleccionada.get_sexo_display(),
        'cliente_nombre': mascota_seleccionada.cliente.nombre,
        'cliente_telefono': mascota_seleccionada.cliente.telefono,
        'cliente_email': mascota_seleccionada.cliente.email,
    }

    if request.method == 'POST':
        form = ConsultaMedicaUpdateForm(request.POST, instance=consulta)
        
        if form.is_valid():
            consulta_editada = form.save(commit=False)
            mascota_id = request.POST.get('mascota')
            if mascota_id:
                consulta_editada.mascota_id = mascota_id
            consulta_editada.save()

            # 🚫 NO actualizamos los datos de la mascota en la edición de consulta
            # Los datos se mantienen solo en la consulta, no en la mascota

            # ✏️ Actualizar descripciones de documentos existentes
            for documento in documentos_existentes:
                nueva_descripcion = request.POST.get(f'descripcion_existente_{documento.id}')
                if nueva_descripcion is not None:
                    documento.descripcion = nueva_descripcion
                    documento.save()

            # 📎 Guardar nuevos documentos
            archivos = request.FILES.getlist('archivo')
            descripciones = request.POST.getlist('descripcion')
            
            for i, archivo in enumerate(archivos):
                if archivo:
                    descripcion = descripciones[i] if i < len(descripciones) else ''
                    DocumentosConsulta.objects.create(
                        consulta=consulta_editada,
                        archivo=archivo,
                        descripcion=descripcion
                    )

            messages.success(request, "Consulta médica y documentos actualizados correctamente.")
            return redirect('detalle-consulta', consulta_id=consulta.id)
    else:
        form = ConsultaMedicaUpdateForm(instance=consulta)

    return render(
        request,
        'consultasMedicas/consultasMedicasBase/editarConsulta.html',
        {
            'form': form,
            'consulta': consulta,
            'documentos_existentes': documentos_existentes,
            'mascotas': mascotas,
            'mascota_seleccionada': mascota_seleccionada,
            'datos_mascota': datos_mascota,
        }
    )

@login_required
def eliminar_documento(request, documento_id):
    """Vista para eliminar un documento específico"""
    documento = get_object_or_404(DocumentosConsulta, id=documento_id)
    consulta_id = documento.consulta.id
    
    if request.method == 'POST':
        documento.delete()
        messages.success(request, "Documento eliminado correctamente.")
        return redirect('editar_consulta', consulta_id=consulta_id)
    
    return redirect('editar_consulta', consulta_id=consulta_id)




@login_required
def borrar_consulta(request, pk):
    """View to delete an existing pet."""
    consulta = get_object_or_404(ConsultasMedicas, pk=pk)
    consulta.delete()
    return redirect('ver-consultas')



@login_required
def generar_pdf_consulta(request, consulta_id):
    """Generar PDF con los datos de la consulta médica"""
    consulta = get_object_or_404(ConsultasMedicas, id=consulta_id)
    documentos = DocumentosConsulta.objects.filter(consulta=consulta)
    
    # Crear el PDF en memoria
    buffer = BytesIO()
    pdf_doc = SimpleDocTemplate(
        buffer, 
        pagesize=A4, 
        rightMargin=72, 
        leftMargin=72, 
        topMargin=100,  # Más espacio arriba para el logo
        bottomMargin=18
    )
    styles = getSampleStyleSheet()
    
    # Estilos personalizados
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=30,
        alignment=1,  # Centrado
        textColor=colors.HexColor('#2c3e50'),
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=12,
        spaceAfter=12,
        spaceBefore=12,
        textColor=colors.HexColor('#2c3e50'),
        borderColor=colors.HexColor('#3498db'),
        borderWidth=1,
        borderPadding=5,
        backColor=colors.HexColor('#ecf0f1'),
    )
    
    normal_style = styles['Normal']
    normal_style.fontSize = 10
    
    # Contenido del PDF
    story = []
    
    # Logo (si existe)
    logo_path = os.path.join(settings.MEDIA_ROOT, 'logo.png')
    if os.path.exists(logo_path):
        try:
            logo = Image(logo_path, width=1.5*inch, height=1*inch)
            logo.hAlign = 'CENTER'
            story.append(logo)
            story.append(Spacer(1, 10))
        except:
            # Si hay error cargando la imagen, continuar sin logo
            pass
    
    # Título
    story.append(Paragraph("CONSULTA MÉDICA VETERINARIA MASCOTAS MORELIA", title_style))
    story.append(Spacer(1, 20))
    
    # Información básica
    story.append(Paragraph("INFORMACIÓN GENERAL", heading_style))
    info_data = [
        ['Mascota:', consulta.mascota.nombre],
        ['Especie:', consulta.mascota.especie],
        ['Raza:', consulta.mascota.raza],
        ['Sexo:', consulta.mascota.sexo],
        ['Propietario:', consulta.mascota.cliente.nombre],
        ['Fecha de consulta:', timezone.localtime(consulta.fechaConsulta).strftime('%d/%m/%Y %H:%M')],
        ['Veterinario:', consulta.veterinario.get_full_name() or consulta.veterinario.username],
        ['Clínica:', consulta.clinicaVeterinaria],
        ['Procedimiento:', consulta.procedimiento],
    ]
    
    info_table = Table(info_data, colWidths=[2*inch, 4*inch])
    info_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8f9fa')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dee2e6')),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(info_table)
    story.append(Spacer(1, 20))
    
    # Anamnesis
    if consulta.anamnesicos:
        story.append(Paragraph("ANAMNESIS", heading_style))
        story.append(Paragraph(consulta.anamnesicos, normal_style))
        story.append(Spacer(1, 12))
    
    # Signos vitales y examen físico
    story.append(Paragraph("SIGNOS VITALES Y EXAMEN FÍSICO", heading_style))
    signos_data = []
    if consulta.temperatura:
        signos_data.append(['Temperatura:', consulta.temperatura])
    if consulta.pulso:
        signos_data.append(['Pulso:', consulta.pulso])
    if consulta.frecuenciaCardiaca:
        signos_data.append(['Frecuencia cardíaca:', consulta.frecuenciaCardiaca])
    if consulta.frecuenciaRespiratoria:
        signos_data.append(['Frecuencia respiratoria:', consulta.frecuenciaRespiratoria])
    if consulta.puntuacionCorporal:
        signos_data.append(['Puntuación corporal:', consulta.puntuacionCorporal])
    if consulta.mucosas:
        signos_data.append(['Mucosas:', consulta.mucosas])
    if consulta.porcentajeHidratacion:
        signos_data.append(['Porcentaje de hidratación:', consulta.porcentajeHidratacion])
    if consulta.actitudConPropietario:
        signos_data.append(['Actitud con propietario:', consulta.actitudConPropietario])
    if consulta.actitudConVeterinario:
        signos_data.append(['Actitud con veterinario:', consulta.actitudConVeterinario])
    
    signos_data.append(['Peso:', f"{consulta.peso} kg"])
    
    if signos_data:
        signos_table = Table(signos_data, colWidths=[2.5*inch, 3.5*inch])
        signos_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8f9fa')),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dee2e6')),
            ('PADDING', (0, 0), (-1, -1), 4),
        ]))
        story.append(signos_table)
        story.append(Spacer(1, 8))
    
    if consulta.examanesFisicosRealizados:
        story.append(Paragraph("<b>Exámenes Físicos Realizados:</b>", normal_style))
        story.append(Paragraph(consulta.examanesFisicosRealizados, normal_style))
        story.append(Spacer(1, 12))
    
    # Historial médico
    historial_data = []
    if consulta.vacunas:
        historial_data.append(['Vacunas:', consulta.vacunas])
    if consulta.alergias:
        historial_data.append(['Alergias:', consulta.alergias])
    if consulta.ultimaDesparasitacion:
        historial_data.append(['Última desparasitación:', consulta.ultimaDesparasitacion.strftime('%d/%m/%Y')])
    if consulta.ultimoDesparasitante:
        historial_data.append(['Último desparasitante:', consulta.ultimoDesparasitante])
    if consulta.parasitos:
        historial_data.append(['Parásitos:', consulta.parasitos])
    
    if historial_data:
        story.append(Paragraph("HISTORIAL MÉDICO", heading_style))
        historial_table = Table(historial_data, colWidths=[2.5*inch, 3.5*inch])
        historial_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8f9fa')),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dee2e6')),
            ('PADDING', (0, 0), (-1, -1), 4),
        ]))
        story.append(historial_table)
        story.append(Spacer(1, 12))
    
    # Condiciones y hábitos
    condiciones_data = []
    if consulta.alimento:
        condiciones_data.append(['Alimento:', consulta.alimento])
    if consulta.ectoparasitos:
        condiciones_data.append(['Ectoparásitos:', consulta.ectoparasitos])
    
    if condiciones_data:
        story.append(Paragraph("ALIMENTACIÓN", heading_style))
        condiciones_table = Table(condiciones_data, colWidths=[2.5*inch, 3.5*inch])
        condiciones_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8f9fa')),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dee2e6')),
            ('PADDING', (0, 0), (-1, -1), 4),
        ]))
        story.append(condiciones_table)
        story.append(Spacer(1, 12))
    
    # Diagnóstico y tratamiento
    if consulta.listaPosiblesProblemas:
        story.append(Paragraph("LISTA DE POSIBLES PROBLEMAS", heading_style))
        story.append(Paragraph(consulta.listaPosiblesProblemas, normal_style))
        story.append(Spacer(1, 12))
    
    if consulta.listaProblemasReales:
        story.append(Paragraph("LISTA DE PROBLEMAS REALES", heading_style))
        story.append(Paragraph(consulta.listaProblemasReales, normal_style))
        story.append(Spacer(1, 12))
    
    if consulta.diagnostico:
        story.append(Paragraph("DIAGNÓSTICO", heading_style))
        story.append(Paragraph(consulta.diagnostico, normal_style))
        story.append(Spacer(1, 12))
    
    if consulta.tratamiento:
        story.append(Paragraph("TRATAMIENTO", heading_style))
        story.append(Paragraph(consulta.tratamiento, normal_style))
        story.append(Spacer(1, 12))
    
    if consulta.pronostico:
        story.append(Paragraph("PRONÓSTICO", heading_style))
        story.append(Paragraph(consulta.pronostico, normal_style))
        story.append(Spacer(1, 12))
    
    # Estudios
    if consulta.estudiosHechos or consulta.estudiosRecomendados:
        story.append(Paragraph("ESTUDIOS", heading_style))
        if consulta.estudiosHechos:
            story.append(Paragraph("<b>Realizados:</b>", normal_style))
            story.append(Paragraph(consulta.estudiosHechos, normal_style))
        if consulta.estudiosRecomendados:
            story.append(Paragraph("<b>Recomendados:</b>", normal_style))
            story.append(Paragraph(consulta.estudiosRecomendados, normal_style))
        story.append(Spacer(1, 12))
    
    # Observaciones y evolución
    if consulta.observaciones:
        story.append(Paragraph("OBSERVACIONES", heading_style))
        story.append(Paragraph(consulta.observaciones, normal_style))
        story.append(Spacer(1, 12))
    
    if consulta.evolucion:
        story.append(Paragraph("EVOLUCIÓN", heading_style))
        story.append(Paragraph(consulta.evolucion, normal_style))
        story.append(Spacer(1, 12))
    
    # Documentos adjuntos
    if documentos.exists():
        story.append(Paragraph("DOCUMENTOS ADJUNTOS", heading_style))
        docs_data = [['Descripción', 'Fecha']]
        for documento in documentos:
            docs_data.append([
                documento.descripcion or 'Sin descripción', 
                documento.fecha.strftime('%d/%m/%Y')
            ])
        
        docs_table = Table(docs_data, colWidths=[4*inch, 2*inch])
        docs_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dee2e6')),
            ('PADDING', (0, 0), (-1, -1), 6),
        ]))
        story.append(docs_table)
    
    # Generar el PDF
    pdf_doc.build(story)
    buffer.seek(0)
    
    # Crear respuesta
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="consulta_{consulta.mascota.nombre}_{consulta.fechaConsulta.strftime("%Y%m%d")}.pdf"'
    
    return response