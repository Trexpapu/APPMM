import os
from io import BytesIO
from django.conf import settings
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.units import inch
from reportlab.lib import colors

def generar_pdf_guarderia(guarderia):
    """Generar PDF con los datos del servicio de guardería"""
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
            
    story.append(Paragraph("SERVICIO DE GUARDERÍA MASCOTAS MORELIA", title_style))
    story.append(Spacer(1, 20))
    
    story.append(Paragraph("INFORMACIÓN DE LA MASCOTA", heading_style))
    info_mascota_data = [
        ['Nombre:', Paragraph(guarderia.mascota.nombre, normal_style)],
        ['Especie:', guarderia.mascota.especie],
        ['Raza:', guarderia.mascota.raza or 'No especificada'],
        ['Fecha de Nacimiento:', guarderia.mascota.fechaNacimiento.strftime('%d/%m/%Y') if guarderia.mascota.fechaNacimiento else 'No especificada'],
        ['Peso:', f"{guarderia.mascota.peso} kg" if guarderia.mascota.peso else 'No especificado'],
        ['Sexo:', guarderia.mascota.get_sexo_display()],
    ]
    info_mascota_table = Table(info_mascota_data, colWidths=[2*inch, 4*inch])
    info_mascota_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'), ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8f9fa')), ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'), ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'), ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dee2e6')),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(info_mascota_table)
    story.append(Spacer(1, 20))
    
    story.append(Paragraph("INFORMACIÓN DEL PROPIETARIO", heading_style))
    info_cliente_data = [
        ['Nombre:', Paragraph(guarderia.mascota.cliente.nombre, normal_style)],
        ['Teléfono:', guarderia.mascota.cliente.telefono or 'No especificado'],
        ['Email:', Paragraph(guarderia.mascota.cliente.email, normal_style) or 'No especificado'],
    ]
    info_cliente_table = Table(info_cliente_data, colWidths=[2*inch, 4*inch])
    info_cliente_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'), ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8f9fa')), ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'), ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'), ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dee2e6')),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(info_cliente_table)
    story.append(Spacer(1, 20))
    
    story.append(Paragraph("DATOS DEL SERVICIO DE GUARDERÍA", heading_style))
    story.append(Paragraph("<b>FECHAS Y UBICACIÓN:</b>", normal_style))
    story.append(Spacer(1, 5))
    
    fechas_data = [
        ['Fecha de Ingreso:', guarderia.fechaEntrada.strftime('%d/%m/%Y')],
        ['Fecha de Egreso Programada:', guarderia.fechaSalidaProgramada.strftime('%d/%m/%Y') if guarderia.fechaSalidaProgramada else 'No especificada'],
        ['Clínica Veterinaria:', Paragraph(guarderia.clinicaVeterinaria, normal_style)],
        ['Estado del Servicio:', guarderia.estado],
    ]
    fechas_table = Table(fechas_data, colWidths=[2.5*inch, 3.5*inch])
    fechas_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'), ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8f9fa')), ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dee2e6')),
        ('PADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(fechas_table)
    story.append(Spacer(1, 12))
    
    if guarderia.alimento:
        story.append(Paragraph("<b>ALIMENTACIÓN DE LA MASCOTA:</b>", normal_style))
        story.append(Paragraph(guarderia.alimento, normal_style))
        story.append(Spacer(1, 8))
    
    if guarderia.estadoSalud:
        story.append(Paragraph("<b>ESTADO DE SALUD AL INGRESO:</b>", normal_style))
        story.append(Paragraph(guarderia.estadoSalud, normal_style))
        story.append(Spacer(1, 8))
    
    if guarderia.tratamientos:
        story.append(Paragraph("<b>TRATAMIENTOS DURANTE ESTADÍA:</b>", normal_style))
        story.append(Paragraph(guarderia.tratamientos, normal_style))
        story.append(Spacer(1, 8))
    
    if guarderia.accesoriosRecibidos:
        story.append(Paragraph("<b>ACCESORIOS RECIBIDOS:</b>", normal_style))
        story.append(Paragraph(guarderia.accesoriosRecibidos, normal_style))
        story.append(Spacer(1, 8))
    
    if guarderia.otrosDatos:
        story.append(Paragraph("<b>OTROS DATOS RELEVANTES:</b>", normal_style))
        story.append(Paragraph(guarderia.otrosDatos, normal_style))
        story.append(Spacer(1, 8))
        
    story.append(Paragraph("<b>INFORMACIÓN DE PAGOS:</b>", normal_style))
    story.append(Spacer(1, 5))
    pagos_data = [['Pagado:', f"${guarderia.pagado}"], ['Pago Total:', f"${guarderia.pagoTotal}"]]
    pagos_table = Table(pagos_data, colWidths=[2.5*inch, 3.5*inch])
    pagos_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'), ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8f9fa')), ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dee2e6')),
        ('PADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(pagos_table)
    story.append(Spacer(1, 20))
    
    story.append(Paragraph("TÉRMINOS Y CONDICIONES", heading_style))
    terminos_text = "<para>Por medio del presente documento, el propietario de la mascota acepta los siguientes términos y condiciones durante el servicio de guardería:</para>"
    story.append(Paragraph(terminos_text, normal_style))
    story.append(Spacer(1, 10))
    
    incisos = [
        "Entregar el carnet de la mascota debidamente actualizado.",
        "Aprobar el tratamiento de ingreso o extemporáneo en caso de ser necesario.",
        "Liquidar por anticipo el costo presupuestado del servicio.",
        "Presentar factura o comprobantes de procedencia en caso de animales exóticos o aquellos que así lo requieran.",
        "Si la estancia de la mascota excede los días previstos, se cobrará un cargo adicional al momento de recogerla.",
        "Mascotas Morelia no se hace responsable por objetos personales (juguetes, cobijas, etc.) que puedan sufrir daño durante la estancia.",
        "Mascotas Morelia no se responsabiliza por el fallecimiento de la mascota cuando sea por causas de fuerza mayor o si no se autorizó la intervención correspondiente.",
        "La mascota únicamente será entregada al propietario o a la persona que presente el contrarrecibo expedido por Mascotas Morelia."
    ]
    for i, inciso in enumerate(incisos, 1):
        story.append(Paragraph(f"<b>{i}.</b> {inciso}", normal_style))
        story.append(Spacer(1, 5))
        
    story.append(Spacer(1, 20))
    story.append(Paragraph("CONFORMIDAD Y ACEPTACIÓN", heading_style))
    firma_text = "<para>El propietario declara haber leído y comprendido los términos y condiciones anteriores, y acepta cumplir con lo establecido en este documento.</para>"
    story.append(Paragraph(firma_text, normal_style))
    story.append(Spacer(1, 30))
    
    firma_data = [['', ''], ['_________________________', '_________________________'], ['Nombre del Propietario', 'Firma del Propietario']]
    firma_table = Table(firma_data, colWidths=[3*inch, 3*inch])
    firma_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'), ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'), ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(firma_table)
    story.append(Spacer(1, 20))
    
    fecha_lugar = f"<para><b>Fecha:</b> {guarderia.fechaEntrada.strftime('%d/%m/%Y')}<br/><b>Lugar:</b> {guarderia.clinicaVeterinaria}</para>"
    story.append(Paragraph(fecha_lugar, normal_style))
    
    pdf_doc.build(story)
    buffer.seek(0)
    
    response = HttpResponse(buffer, content_type='application/pdf')
    filename = f"guarderia_{guarderia.mascota.nombre}_{guarderia.fechaEntrada.strftime('%Y%m%d')}.pdf"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response


def generar_pdf_hospitalizacion(hospitalizacion):
    """Generar PDF con los datos del servicio de hospitalización"""
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
            
    story.append(Paragraph("SERVICIO DE HOSPITALIZACIÓN MASCOTAS MORELIA", title_style))
    story.append(Spacer(1, 20))
    
    story.append(Paragraph("INFORMACIÓN DE LA MASCOTA", heading_style))
    info_mascota_data = [
        ['Nombre:', Paragraph(hospitalizacion.mascota.nombre, normal_style)],
        ['Especie:', hospitalizacion.mascota.especie],
        ['Raza:', hospitalizacion.mascota.raza or 'No especificada'],
        ['Fecha de Nacimiento:', hospitalizacion.mascota.fechaNacimiento.strftime('%d/%m/%Y') if hospitalizacion.mascota.fechaNacimiento else 'No especificada'],
        ['Peso:', f"{hospitalizacion.mascota.peso} kg" if hospitalizacion.mascota.peso else 'No especificado'],
        ['Sexo:', hospitalizacion.mascota.get_sexo_display()],
    ]
    info_mascota_table = Table(info_mascota_data, colWidths=[2*inch, 4*inch])
    info_mascota_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'), ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8f9fa')), ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'), ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'), ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dee2e6')),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(info_mascota_table)
    story.append(Spacer(1, 20))
    
    story.append(Paragraph("INFORMACIÓN DEL PROPIETARIO", heading_style))
    info_cliente_data = [
        ['Nombre:', Paragraph(hospitalizacion.mascota.cliente.nombre, normal_style)],
        ['Teléfono:', hospitalizacion.mascota.cliente.telefono or 'No especificado'],
        ['Email:', Paragraph(hospitalizacion.mascota.cliente.email, normal_style) or 'No especificado'],
    ]
    info_cliente_table = Table(info_cliente_data, colWidths=[2*inch, 4*inch])
    info_cliente_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'), ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8f9fa')), ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'), ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'), ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dee2e6')),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(info_cliente_table)
    story.append(Spacer(1, 20))
    
    story.append(Paragraph("DATOS DEL SERVICIO DE HOSPITALIZACIÓN", heading_style))
    story.append(Paragraph("<b>FECHAS Y UBICACIÓN:</b>", normal_style))
    story.append(Spacer(1, 5))
    fechas_data = [
        ['Fecha de Ingreso:', hospitalizacion.fechaEntrada.strftime('%d/%m/%Y')],
        ['Fecha de Egreso:', hospitalizacion.fechaSalida.strftime('%d/%m/%Y') if hospitalizacion.fechaSalida else 'No especificada'],
        ['Clínica Veterinaria:', Paragraph(hospitalizacion.clinicaVeterinaria, normal_style)],
        ['Estado del Paciente:', hospitalizacion.estado],
    ]
    fechas_table = Table(fechas_data, colWidths=[2.5*inch, 3.5*inch])
    fechas_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'), ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8f9fa')), ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dee2e6')),
        ('PADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(fechas_table)
    story.append(Spacer(1, 12))
    
    if hospitalizacion.motivo:
        story.append(Paragraph("<b>MOTIVO DE HOSPITALIZACIÓN:</b>", normal_style))
        story.append(Paragraph(hospitalizacion.motivo, normal_style))
        story.append(Spacer(1, 8))
    
    if hospitalizacion.diagnostico:
        story.append(Paragraph("<b>DIAGNÓSTICO:</b>", normal_style))
        story.append(Paragraph(hospitalizacion.diagnostico, normal_style))
        story.append(Spacer(1, 8))
    
    if hospitalizacion.observaciones:
        story.append(Paragraph("<b>OBSERVACIONES:</b>", normal_style))
        story.append(Paragraph(hospitalizacion.observaciones, normal_style))
        story.append(Spacer(1, 8))
    
    if hospitalizacion.tratamientos:
        story.append(Paragraph("<b>TRATAMIENTOS REQUERIDOS:</b>", normal_style))
        story.append(Paragraph(hospitalizacion.tratamientos, normal_style))
        story.append(Spacer(1, 8))
    
    if hospitalizacion.evolucion:
        story.append(Paragraph("<b>EVOLUCIÓN DEL PACIENTE:</b>", normal_style))
        story.append(Paragraph(hospitalizacion.evolucion, normal_style))
        story.append(Spacer(1, 8))
    
    if hospitalizacion.otrosDatos:
        story.append(Paragraph("<b>OTROS DATOS RELEVANTES:</b>", normal_style))
        story.append(Paragraph(hospitalizacion.otrosDatos, normal_style))
        story.append(Spacer(1, 8))
        
    story.append(Paragraph("<b>INFORMACIÓN DE PAGOS:</b>", normal_style))
    story.append(Spacer(1, 5))
    pagos_data = [['Pagado:', f"${hospitalizacion.pagado}"], ['Pago Total:', f"${hospitalizacion.pagoTotal}"]]
    pagos_table = Table(pagos_data, colWidths=[2.5*inch, 3.5*inch])
    pagos_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'), ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8f9fa')), ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dee2e6')),
        ('PADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(pagos_table)
    story.append(Spacer(1, 20))
    
    story.append(Paragraph("TÉRMINOS Y CONDICIONES", heading_style))
    terminos_text = "<para>Por medio del presente documento, el propietario de la mascota acepta los siguientes términos y condiciones durante el servicio de hospitalización:</para>"
    story.append(Paragraph(terminos_text, normal_style))
    story.append(Spacer(1, 10))
    
    incisos = [
        "En caso de emergencia médica, Mascotas Morelia se reserva el derecho de proporcionar la atención veterinaria necesaria, cuyos costos serán asumidos por el propietario.",
        "El pago del servicio deberá liquidarse en su totalidad al momento del alta de la mascota.",
        "Si la mascota no es recogida en la fecha acordada, se aplicarán cargos por cada día adicional.",
        "El propietario autoriza a Mascotas Morelia a tomar decisiones médicas en caso de emergencia cuando no pueda ser contactado.",
        "El propietario es responsable de informar sobre cualquier condición médica preexistente, alergias o medicamentos que requiera la mascota.",
        "Mascotas Morelia no se hace responsable por el fallecimiento de la mascota."
    ]
    for i, inciso in enumerate(incisos, 1):
        story.append(Paragraph(f"<b>{i}.</b> {inciso}", normal_style))
        story.append(Spacer(1, 5))
        
    story.append(Spacer(1, 20))
    story.append(Paragraph("CONFORMIDAD Y ACEPTACIÓN", heading_style))
    firma_text = "<para>El propietario declara haber leído y comprendido los términos y condiciones anteriores, y acepta cumplir con lo establecido en este documento.</para>"
    story.append(Paragraph(firma_text, normal_style))
    story.append(Spacer(1, 30))
    
    firma_data = [['', ''], ['_________________________', '_________________________'], ['Nombre del Propietario', 'Firma del Propietario']]
    firma_table = Table(firma_data, colWidths=[3*inch, 3*inch])
    firma_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'), ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'), ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(firma_table)
    story.append(Spacer(1, 20))
    
    fecha_lugar = f"<para><b>Fecha:</b> {hospitalizacion.fechaEntrada.strftime('%d/%m/%Y')}<br/><b>Lugar:</b> {hospitalizacion.clinicaVeterinaria}</para>"
    story.append(Paragraph(fecha_lugar, normal_style))
    
    pdf_doc.build(story)
    buffer.seek(0)
    
    response = HttpResponse(buffer, content_type='application/pdf')
    filename = f"hospitalizacion_{hospitalizacion.mascota.nombre}_{hospitalizacion.fechaEntrada.strftime('%Y%m%d')}.pdf"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response
