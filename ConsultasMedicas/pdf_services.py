import os
from io import BytesIO
from django.conf import settings
from django.http import HttpResponse
from django.utils import timezone
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.units import inch
from reportlab.lib import colors

def generar_pdf_consulta(consulta, documentos):
    """Genera PDF con los datos de la consulta médica y devuelve un HttpResponse"""
    buffer = BytesIO()
    pdf_doc = SimpleDocTemplate(
        buffer, 
        pagesize=A4, 
        rightMargin=72, 
        leftMargin=72, 
        topMargin=100,  
        bottomMargin=18
    )
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CustomTitle', parent=styles['Heading1'], fontSize=16, spaceAfter=30,
        alignment=1, textColor=colors.HexColor('#2c3e50'),
    )
    heading_style = ParagraphStyle(
        'CustomHeading', parent=styles['Heading2'], fontSize=12, spaceAfter=12, spaceBefore=12,
        textColor=colors.HexColor('#2c3e50'), borderColor=colors.HexColor('#3498db'),
        borderWidth=1, borderPadding=5, backColor=colors.HexColor('#ecf0f1'),
    )
    normal_style = styles['Normal']
    normal_style.fontSize = 10
    
    story = []
    
    logo_path = os.path.join(settings.MEDIA_ROOT, 'logo.png')
    if os.path.exists(logo_path):
        try:
            logo = Image(logo_path, width=1.5*inch, height=1*inch)
            logo.hAlign = 'CENTER'
            story.append(logo)
            story.append(Spacer(1, 10))
        except:
            pass
            
    story.append(Paragraph("CONSULTA MÉDICA VETERINARIA MASCOTAS MORELIA", title_style))
    story.append(Spacer(1, 20))
    
    story.append(Paragraph("INFORMACIÓN GENERAL", heading_style))
    info_data = [
        ['Mascota:', Paragraph(consulta.mascota.nombre, normal_style)],
        ['Especie:', Paragraph(consulta.mascota.especie, normal_style)],
        ['Raza:', Paragraph(consulta.mascota.raza, normal_style)],
        ['Sexo:', consulta.mascota.sexo],
        ['Propietario:', Paragraph(consulta.mascota.cliente.nombre, normal_style)],
        ['Fecha de consulta:', timezone.localtime(consulta.fechaConsulta).strftime('%d/%m/%Y %H:%M')],
        ['Veterinario:', Paragraph(consulta.veterinario.get_full_name() or consulta.veterinario.username, normal_style)],
        ['Clínica:', Paragraph(consulta.clinicaVeterinaria, normal_style)],
        ['Procedimiento:', Paragraph(consulta.procedimiento, normal_style)],
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
    
    if consulta.anamnesicos:
        story.append(Paragraph("ANAMNESIS", heading_style))
        story.append(Paragraph(consulta.anamnesicos, normal_style))
        story.append(Spacer(1, 12))
        
    story.append(Paragraph("SIGNOS VITALES Y EXAMEN FÍSICO", heading_style))
    signos_data = []
    if consulta.temperatura: signos_data.append(['Temperatura:', consulta.temperatura])
    if consulta.pulso: signos_data.append(['Pulso:', consulta.pulso])
    if consulta.frecuenciaCardiaca: signos_data.append(['Frecuencia cardíaca:', consulta.frecuenciaCardiaca])
    if consulta.frecuenciaRespiratoria: signos_data.append(['Frecuencia respiratoria:', consulta.frecuenciaRespiratoria])
    if consulta.puntuacionCorporal: signos_data.append(['Puntuación corporal:', consulta.puntuacionCorporal])
    if consulta.mucosas: signos_data.append(['Mucosas:', consulta.mucosas])
    if consulta.porcentajeHidratacion: signos_data.append(['Porcentaje de hidratación:', consulta.porcentajeHidratacion])
    if consulta.actitudConPropietario: signos_data.append(['Actitud con propietario:', consulta.actitudConPropietario])
    if consulta.actitudConVeterinario: signos_data.append(['Actitud con veterinario:', consulta.actitudConVeterinario])
    signos_data.append(['Peso:', f"{consulta.peso} kg"])
    
    if signos_data:
        signos_table = Table(signos_data, colWidths=[2.5*inch, 3.5*inch])
        signos_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'), ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8f9fa')), ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dee2e6')),
            ('PADDING', (0, 0), (-1, -1), 4),
        ]))
        story.append(signos_table)
        story.append(Spacer(1, 8))
        
    if consulta.examanesFisicosRealizados:
        story.append(Paragraph("<b>Exámenes Físicos Realizados:</b>", normal_style))
        story.append(Paragraph(consulta.examanesFisicosRealizados, normal_style))
        story.append(Spacer(1, 12))
        
    historial_data = []
    if consulta.vacunas: historial_data.append(['Vacunas:', consulta.vacunas])
    if consulta.alergias: historial_data.append(['Alergias:', consulta.alergias])
    if consulta.ultimaDesparasitacion: historial_data.append(['Última desparasitación:', consulta.ultimaDesparasitacion.strftime('%d/%m/%Y')])
    if consulta.ultimoDesparasitante: historial_data.append(['Último desparasitante:', consulta.ultimoDesparasitante])
    if consulta.parasitos: historial_data.append(['Parásitos:', consulta.parasitos])
    
    if historial_data:
        story.append(Paragraph("HISTORIAL MÉDICO", heading_style))
        historial_table = Table(historial_data, colWidths=[2.5*inch, 3.5*inch])
        historial_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'), ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8f9fa')), ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dee2e6')),
            ('PADDING', (0, 0), (-1, -1), 4),
        ]))
        story.append(historial_table)
        story.append(Spacer(1, 12))
        
    condiciones_data = []
    if consulta.alimento: condiciones_data.append(['Alimento:', consulta.alimento])
    if consulta.ectoparasitos: condiciones_data.append(['Ectoparásitos:', consulta.ectoparasitos])
    
    if condiciones_data:
        story.append(Paragraph("ALIMENTACIÓN", heading_style))
        condiciones_table = Table(condiciones_data, colWidths=[2.5*inch, 3.5*inch])
        condiciones_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'), ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8f9fa')), ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dee2e6')),
            ('PADDING', (0, 0), (-1, -1), 4),
        ]))
        story.append(condiciones_table)
        story.append(Spacer(1, 12))
        
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
        
    if consulta.estudiosHechos or consulta.estudiosRecomendados:
        story.append(Paragraph("ESTUDIOS", heading_style))
        if consulta.estudiosHechos:
            story.append(Paragraph("<b>Realizados:</b>", normal_style))
            story.append(Paragraph(consulta.estudiosHechos, normal_style))
        if consulta.estudiosRecomendados:
            story.append(Paragraph("<b>Recomendados:</b>", normal_style))
            story.append(Paragraph(consulta.estudiosRecomendados, normal_style))
        story.append(Spacer(1, 12))
        
    if consulta.observaciones:
        story.append(Paragraph("MEDICAMENTOS APLICADOS Y COMENTARIOS", heading_style))
        story.append(Paragraph(consulta.observaciones, normal_style))
        story.append(Spacer(1, 12))
    if consulta.evolucion:
        story.append(Paragraph("EVOLUCIÓN", heading_style))
        story.append(Paragraph(consulta.evolucion, normal_style))
        story.append(Spacer(1, 12))
        
    if documentos.exists():
        story.append(Paragraph("DOCUMENTOS ADJUNTOS", heading_style))
        docs_data = [['Descripción', 'Fecha']]
        for documento in documentos:
            docs_data.append([documento.descripcion or 'Sin descripción', documento.fecha.strftime('%d/%m/%Y')])
        docs_table = Table(docs_data, colWidths=[4*inch, 2*inch])
        docs_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'), ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c3e50')), ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'), ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dee2e6')),
            ('PADDING', (0, 0), (-1, -1), 6),
        ]))
        story.append(docs_table)
        
    pdf_doc.build(story)
    buffer.seek(0)
    
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="consulta_{consulta.mascota.nombre}_{consulta.fechaConsulta.strftime("%Y%m%d")}.pdf"'
    return response

def generar_pdf_receta(datos_form, datos_mascota, mascota_obj):
    buffer = BytesIO()
    pdf_doc = SimpleDocTemplate(
        buffer, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=100, bottomMargin=18
    )
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CustomTitle', parent=styles['Heading1'], fontSize=16, spaceAfter=30,
        alignment=1, textColor=colors.HexColor('#2c3e50'),
    )
    heading_style = ParagraphStyle(
        'CustomHeading', parent=styles['Heading2'], fontSize=12, spaceAfter=12, spaceBefore=12,
        textColor=colors.HexColor('#2c3e50'), borderColor=colors.HexColor('#3498db'),
        borderWidth=1, borderPadding=5, backColor=colors.HexColor('#ecf0f1'),
    )
    normal_style = styles['Normal']
    normal_style.fontSize = 10
    
    receta_style = ParagraphStyle(
        'RecetaStyle', parent=styles['Normal'], fontSize=10, spaceAfter=6, leftIndent=20, firstLineIndent=-20,
    )
    
    story = []
    
    logo_path = os.path.join(settings.MEDIA_ROOT, 'logo.png')
    if os.path.exists(logo_path):
        try:
            logo = Image(logo_path, width=1.5*inch, height=1*inch)
            logo.hAlign = 'CENTER'
            story.append(logo)
            story.append(Spacer(1, 10))
        except:
            pass
            
    story.append(Paragraph("RECETA MÉDICA VETERINARIA", title_style))
    story.append(Spacer(1, 20))
    
    fecha_formateada = datos_form['fecha'].strftime('%d/%m/%Y')
    info_header = [
        [Paragraph(f"<b>Clínica:</b> {datos_form['veterinaria']}"), Paragraph(f"<b>Fecha:</b> {fecha_formateada}")],
        [Paragraph(f"<b>Veterinario:</b> {datos_form['veterinario'].get_full_name() or datos_form['veterinario'].username}")]
    ]
    header_table = Table(info_header, colWidths=[3.5*inch, 2.5*inch])
    header_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'), ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black), ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'), ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 20))
    
    story.append(Paragraph("DATOS DE LA MASCOTA Y PROPIETARIO", heading_style))
    fecha_nacimiento = datos_mascota['fechaNacimiento'] if datos_mascota else mascota_obj.fechaNacimiento
    fecha_nac_str = fecha_nacimiento.strftime('%d/%m/%Y') if fecha_nacimiento else 'No registrada'
    peso = datos_mascota['peso'] if datos_mascota else mascota_obj.peso
    peso_str = f"{peso} kg" if peso else 'No registrado'
    cliente_nombre = datos_mascota['cliente_nombre'] if datos_mascota else mascota_obj.cliente.nombre
    cliente_telefono = datos_mascota['cliente_telefono'] if datos_mascota else mascota_obj.cliente.telefono
    cliente_email = datos_mascota['cliente_email'] if datos_mascota else mascota_obj.cliente.email
    
    paciente_data = [
        ['Paciente:', datos_mascota['nombre'] if datos_mascota else mascota_obj.nombre],
        ['Especie:', datos_mascota['especie'] if datos_mascota else mascota_obj.especie],
        ['Raza:', datos_mascota['raza'] if datos_mascota else mascota_obj.raza],
        ['Sexo:', datos_mascota['sexo'] if datos_mascota else mascota_obj.get_sexo_display()],
        ['Fecha Nacimiento:', fecha_nac_str],
        ['Peso:', peso_str],
        ['Propietario:', cliente_nombre],
        ['Teléfono:', cliente_telefono],
        ['Email:', cliente_email],
    ]
    paciente_table = Table(paciente_data, colWidths=[2*inch, 4*inch])
    paciente_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'), ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8f9fa')), ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'), ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'), ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dee2e6')),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(paciente_table)
    story.append(Spacer(1, 20))
    
    story.append(Paragraph("HISTORIAL MÉDICO RELEVANTE", heading_style))
    historial_data = []
    vacunas = datos_mascota['vacunas'] if datos_mascota and datos_mascota['vacunas'] else mascota_obj.vacunas
    if vacunas: historial_data.append(['Vacunas:', vacunas])
    alergias = datos_mascota['alergias'] if datos_mascota and datos_mascota['alergias'] else mascota_obj.alergias
    if alergias: historial_data.append(['Alergias:', alergias])
    ultima_desparasitacion = datos_mascota['ultimaDesparasitacion'] if datos_mascota else mascota_obj.ultimaDesparasitacion
    if ultima_desparasitacion:
        fecha_desparasitacion = ultima_desparasitacion.strftime('%d/%m/%Y') if hasattr(ultima_desparasitacion, 'strftime') else str(ultima_desparasitacion)
        historial_data.append(['Última desparasitación:', fecha_desparasitacion])
    ultimo_desparasitante = datos_mascota['ultimoDesparasitante'] if datos_mascota and datos_mascota['ultimoDesparasitante'] else mascota_obj.ultimoDesparasitante
    if ultimo_desparasitante: historial_data.append(['Último desparasitante:', ultimo_desparasitante])
    
    if historial_data:
        historial_table = Table(historial_data, colWidths=[2.5*inch, 3.5*inch])
        historial_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'), ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8f9fa')), ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dee2e6')),
            ('PADDING', (0, 0), (-1, -1), 4),
        ]))
        story.append(historial_table)
    else:
        story.append(Paragraph("No hay historial médico registrado.", normal_style))
        
    story.append(Spacer(1, 20))
    story.append(Paragraph("RECETA MÉDICA", heading_style))
    descripcion = datos_form['descripcion']
    lineas_descripcion = descripcion.split('\n')
    for linea in lineas_descripcion:
        if linea.strip():
            if linea.strip().startswith(('-', '•', '*', '1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.')):
                story.append(Paragraph(f"• {linea.strip()}", receta_style))
            else:
                story.append(Paragraph(linea.strip(), normal_style))
            story.append(Spacer(1, 4))
            
    story.append(Spacer(1, 30))
    story.append(Paragraph("INFORMACIÓN DE CONTACTO", heading_style))
    contacto_text = """
        <b></b>
        • Para dudas o aclaraciones, comunícate con la clínica al número 453-227-1694 o al correo mascotasmoreliaapatzingan@gmail.com<br/>
        • En caso de emergencia, acude al hospital veterinario más cercano.<br/>
        """
    story.append(Paragraph(contacto_text, normal_style))
    
    pdf_doc.build(story)
    buffer.seek(0)
    
    response = HttpResponse(buffer, content_type='application/pdf')
    nombre_mascota = datos_mascota['nombre'] if datos_mascota else mascota_obj.nombre
    nombre_limpio = nombre_mascota.replace(' ', '_').replace('/', '_')
    fecha_str = datos_form['fecha'].strftime("%Y%m%d")
    response['Content-Disposition'] = f'attachment; filename="receta_{nombre_limpio}_{fecha_str}.pdf"'
    
    return response
