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
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from io import BytesIO
import textwrap
# Create your views here.
@login_required
def indexInicioConsultas(request):
    return render(request, 'consultasMedicas/indexConsultas.html')



@login_required
def ver_proximas_consultas(request):
    """View that renders a table with all upcoming consultations and related client/pet info."""
    query = request.GET.get('q', '').strip().lower()
    siguientesConsultas = SiguientesConsultas.objects.select_related('mascota', 'mascota__cliente', 'veterinario')

    if query:
        # Intentar parsear la fecha si el usuario busca por fecha
        fecha_busqueda = None
        try:
            fecha_busqueda = datetime.strptime(query, "%Y-%m-%d").date()
        except ValueError:
            pass

        siguientesConsultas = siguientesConsultas.filter(
            Q(mascota__cliente__nombre__icontains=query) |
            Q(mascota__cliente__email__icontains=query) |
            Q(mascota__cliente__telefono__icontains=query) |
            Q(mascota__nombre__icontains=query) |
            Q(mascota__raza__icontains=query) |
            Q(mascota__especie__icontains=query) |
            Q(veterinario__username__icontains=query) |       # buscar por username del veterinario
            Q(clinicaVeterinaria__icontains=query) |
            (Q(fechaSiguienteConsulta__date=fecha_busqueda) if fecha_busqueda else Q())
        )

    return render(
        request,
        'consultasMedicas/proximasConsultas/verProximasConsultas.html',
        {'siguientesConsultas': siguientesConsultas}
    )

@login_required
def agendar_proxima_consulta(request):
    """View to add a next consultation."""
    mascotas = Mascotas.objects.all()

    if request.method == 'POST':
        form = SiguienteConsultaForm(request.POST)
        if form.is_valid():
            proximaCita = form.save(commit=False)
            mascota_id = request.POST.get('mascota')
            if mascota_id:
                proximaCita.mascota_id = mascota_id
                proximaCita.save()
                return redirect('index-consultas')
            else:
                form.add_error(None, "Debe seleccionar una mascota antes de guardar.")
    else:
        form = SiguienteConsultaForm()
 
    return render(request, 'consultasMedicas/proximasConsultas/agendarConsulta.html', {'form': form, 'mascotas': mascotas})


@login_required
def borrar_proxima_consulta(request, pk):
    """View to delete an existing pet."""
    proxConsulta = get_object_or_404(SiguientesConsultas, pk=pk)
    proxConsulta.delete()
    return redirect('ver-proximas-consultas')


@login_required
def editar_proxima_consulta(request, pk):
    """Editar mascota con selector personalizado de cliente."""
    proxConsulta = get_object_or_404(SiguientesConsultas, pk=pk)
    mascota = Mascotas.objects.all()

    if request.method == 'POST':
        form = UpdateSiguienteConsultaForm(request.POST, instance=proxConsulta)
        if form.is_valid():
            proxConsultaEditada = form.save(commit=False)
            mascota_id = request.POST.get('mascota')
            if mascota_id:
                proxConsultaEditada.mascota_id = mascota_id
            proxConsultaEditada.save()
            return redirect('ver-proximas-consultas')
    else:
        form = UpdateSiguienteConsultaForm(instance=proxConsulta)

    return render(request, 'consultasMedicas/proximasConsultas/editarProximaConsulta.html', {
        'form': form,
        'mascotas': mascota
    })




@login_required
def nueva_consulta(request):
    """
    Vista para crear una nueva consulta médica
    """
    mascotas = Mascotas.objects.all()
    mascota_id = request.GET.get('mascota') or request.POST.get('mascota')
    cargar_prev = request.GET.get('cargar_prev')

    initial_data = {}
    mascota = None

    # 🔹 SIEMPRE cargar datos de la mascota cuando se selecciona una
    if mascota_id:
        try:
            mascota = Mascotas.objects.get(pk=mascota_id)
            # ✅ DATOS DE MASCOTA - Siempre se cargan
            initial_data.update({
                'peso': mascota.peso,
                'vacunas': mascota.vacunas,
                'alergias': mascota.alergias,
            })
            
            # 🔹 Cargar consulta anterior SOLO si el usuario lo solicita
            if cargar_prev == "1":
                ultima_consulta = (
                    ConsultasMedicas.objects.filter(mascota_id=mascota_id)
                    .order_by('-fechaConsulta')
                    .first()
                )
                if ultima_consulta:
                    exclude_fields = ['id', 'fechaConsulta', 'peso', 'vacunas', 'alergias', 'mascota']
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

                # 🐾 Actualizar datos de la mascota
                mascota = Mascotas.objects.get(pk=mascota_id)
                mascota.peso = form.cleaned_data.get('peso') or mascota.peso
                mascota.vacunas = form.cleaned_data.get('vacunas') or mascota.vacunas
                mascota.alergias = form.cleaned_data.get('alergias') or mascota.alergias
                mascota.save()

                # 📎 GUARDAR DOCUMENTOS usando el modelo DocumentosConsulta
                # Los archivos se guardarán automáticamente en 'consultas/documentos/'
                archivos = request.FILES.getlist('archivo')
                descripciones = request.POST.getlist('descripcion')
                
                for i, archivo in enumerate(archivos):
                    if archivo:  # Solo si se subió un archivo
                        descripcion = descripciones[i] if i < len(descripciones) else ''
                        
                        # ✅ Crear instancia del modelo DocumentosConsulta
                        # El campo 'archivo' guardará automáticamente en 'media/consultas/documentos/'
                        documento = DocumentosConsulta(
                            consulta=nConsulta,
                            archivo=archivo,  # Esto usa el FileField con upload_to
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
        }
    )

@login_required
def ver_consultas(request):
    """View that renders a table with all consultations and related info."""
    query = request.GET.get('q', '').strip().lower()
    consultas = ConsultasMedicas.objects.select_related('mascota', 'mascota__cliente', 'veterinario')

    if query:
        fecha_busqueda = None
        try:
            # Intenta parsear la fecha ingresada (formato YYYY-MM-DD)
            fecha_busqueda = datetime.strptime(query, "%Y-%m-%d").date()
        except ValueError:
            pass

        filtros = (
            Q(mascota__cliente__nombre__icontains=query) |
            Q(mascota__cliente__email__icontains=query) |
            Q(mascota__cliente__telefono__icontains=query) |
            Q(mascota__nombre__icontains=query) |
            Q(mascota__raza__icontains=query) |
            Q(mascota__especie__icontains=query) |
            Q(veterinario__username__icontains=query) |
            Q(clinicaVeterinaria__icontains=query)
        )

        # 🔹 Si se detectó una fecha, agregar un rango (todo ese día)
        if fecha_busqueda:
            inicio_dia = datetime.combine(fecha_busqueda, datetime.min.time())
            fin_dia = datetime.combine(fecha_busqueda, datetime.max.time())
            filtros |= Q(fechaConsulta__range=(inicio_dia, fin_dia))

        consultas = consultas.filter(filtros)

    # 🔹 Ordenar de la más nueva a la más vieja
    consultas = consultas.order_by('-fechaConsulta')

    return render(
        request,
        'consultasMedicas/consultasMedicasBase/verConsultas.html',
        {'consultas': consultas}
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
def generar_pdf_consulta(request, consulta_id):
    """Generar PDF con los datos de la consulta médica"""
    consulta = get_object_or_404(ConsultasMedicas, id=consulta_id)
    documentos = DocumentosConsulta.objects.filter(consulta=consulta)
    
    # Crear el PDF en memoria
    buffer = BytesIO()
    pdf_doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)  # 🔥 Cambiado a pdf_doc
    styles = getSampleStyleSheet()
    
    # Estilos personalizados
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=30,
        alignment=1,  # Centrado
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=12,
        spaceAfter=12,
        spaceBefore=12,
        textColor=colors.HexColor('#2c3e50'),
    )
    
    normal_style = styles['Normal']
    
    # Contenido del PDF
    story = []
    
    # Título
    story.append(Paragraph("CONSULTA MÉDICA VETERINARIA", title_style))
    story.append(Spacer(1, 20))
    
    # Información básica
    story.append(Paragraph("INFORMACIÓN GENERAL", heading_style))
    info_data = [
        ['Mascota:', consulta.mascota.nombre],
        ['Especie:', consulta.mascota.especie],
        ['Raza:', consulta.mascota.raza],
        ['Propietario:', consulta.mascota.cliente.nombre],
        ['Fecha de consulta:', consulta.fechaConsulta.strftime('%d/%m/%Y %H:%M')],
        ['Veterinario:', consulta.veterinario.get_full_name() or consulta.veterinario.username],
        ['Clínica:', consulta.clinicaVeterinaria],
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
    
    # Motivo de consulta
    if consulta.motivoConsulta:
        story.append(Paragraph("MOTIVO DE CONSULTA", heading_style))
        story.append(Paragraph(consulta.motivoConsulta, normal_style))
        story.append(Spacer(1, 12))
    
    # Signos vitales
    story.append(Paragraph("SIGNOS VITALES Y EXAMEN FÍSICO", heading_style))
    signos_data = []
    if consulta.temperatura:
        signos_data.append(['Temperatura:', consulta.temperatura])
    if consulta.pulso:
        signos_data.append(['Pulso:', consulta.pulso])
    if consulta.frecuenciaCardiaca:
        signos_data.append(['Frecuencia cardíaca:', consulta.frecuenciaCardiaca])
    if consulta.puntuacionCorporal:
        signos_data.append(['Puntuación corporal:', consulta.puntuacionCorporal])
    signos_data.append(['Peso:', f"{consulta.peso} gr"])
    
    if signos_data:
        signos_table = Table(signos_data, colWidths=[2*inch, 4*inch])
        signos_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8f9fa')),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dee2e6')),
            ('PADDING', (0, 0), (-1, -1), 4),
        ]))
        story.append(signos_table)
        story.append(Spacer(1, 12))
    
    # Historial médico
    historial_data = []
    if consulta.vacunas:
        historial_data.append(['Vacunas:', consulta.vacunas])
    if consulta.alergias:
        historial_data.append(['Alergias:', consulta.alergias])
    if consulta.parasitos:
        historial_data.append(['Parásitos:', consulta.parasitos])
    
    if historial_data:
        story.append(Paragraph("HISTORIAL MÉDICO", heading_style))
        for item in historial_data:
            story.append(Paragraph(f"<b>{item[0]}</b> {item[1]}", normal_style))
        story.append(Spacer(1, 12))
    
    # Condiciones y hábitos
    condiciones_data = []
    if consulta.agua:
        condiciones_data.append(['Consumo de agua:', consulta.agua])
    if consulta.alimento:
        condiciones_data.append(['Alimento:', consulta.alimento])
    if consulta.condicionesDeHogar:
        condiciones_data.append(['Condiciones del hogar:', consulta.condicionesDeHogar])
    if consulta.ectoparasitos:
        condiciones_data.append(['Ectoparásitos:', consulta.ectoparasitos])
    
    if condiciones_data:
        story.append(Paragraph("CONDICIONES Y HÁBITOS", heading_style))
        condiciones_table = Table(condiciones_data, colWidths=[2*inch, 4*inch])
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
    if consulta.sintomas:
        story.append(Paragraph("SÍNTOMAS", heading_style))
        story.append(Paragraph(consulta.sintomas, normal_style))
        story.append(Spacer(1, 12))
    
    if consulta.diagnostico:
        story.append(Paragraph("DIAGNÓSTICO", heading_style))
        story.append(Paragraph(consulta.diagnostico, normal_style))
        story.append(Spacer(1, 12))
    
    if consulta.tratamiento:
        story.append(Paragraph("TRATAMIENTO", heading_style))
        story.append(Paragraph(consulta.tratamiento, normal_style))
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
        for documento_obj in documentos:  # 🔥 Cambiado a documento_obj para evitar conflicto
            docs_data.append([
                documento_obj.descripcion or 'Sin descripción', 
                documento_obj.fecha.strftime('%d/%m/%Y')
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
    pdf_doc.build(story)  # 🔥 Usando pdf_doc en lugar de doc
    buffer.seek(0)
    
    # Crear respuesta
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="consulta_{consulta.mascota.nombre}_{consulta.fechaConsulta.strftime("%Y%m%d")}.pdf"'
    
    return response