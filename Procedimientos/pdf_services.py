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
from django.utils.timezone import localtime

def generar_pdf_operacion(operacion):
    """Generar PDF con los datos de la operación"""
    fecha_entrada = localtime(operacion.fechaEntrada)
    fecha_salida = localtime(operacion.fechaSalida) if operacion.fechaSalida else None
    
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
            
    story.append(Paragraph("REPORTE DE OPERACIÓN MASCOTAS MORELIA", title_style))
    story.append(Spacer(1, 20))
    
    story.append(Paragraph("INFORMACIÓN DE LA MASCOTA", heading_style))
    info_mascota_data = [
        ['Nombre:', Paragraph(operacion.mascota.nombre, normal_style)],
        ['Especie:', operacion.mascota.especie],
        ['Raza:', operacion.mascota.raza or 'No especificada'],
        ['Fecha de Nacimiento:', operacion.mascota.fechaNacimiento.strftime('%d/%m/%Y') if operacion.mascota.fechaNacimiento else 'No especificada'],
        ['Peso:', f"{operacion.peso} kg"],
        ['Sexo:', operacion.mascota.get_sexo_display()],
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
        ['Nombre:', Paragraph(operacion.mascota.cliente.nombre, normal_style)],
        ['Teléfono:', operacion.mascota.cliente.telefono or 'No especificado'],
        ['Email:', Paragraph(operacion.mascota.cliente.email, normal_style) or 'No especificado'],
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
    
    story.append(Paragraph("DATOS DE LA OPERACIÓN", heading_style))
    story.append(Paragraph("<b>FECHAS Y UBICACIÓN:</b>", normal_style))
    story.append(Spacer(1, 5))
    fechas_data = [
        ['Fecha y Hora de Inicio de la Operación:', fecha_entrada.strftime('%d/%m/%Y %H:%M')],
        ['Fecha y Hora de Fin de la Operación:', fecha_salida.strftime('%d/%m/%Y %H:%M') if operacion.fechaSalida else 'Pendiente'],
        ['Clínica Veterinaria:', Paragraph(operacion.clinicaVeterinaria, normal_style)],
        ['Veterinario Responsable:', Paragraph(operacion.veterinario.get_full_name(), normal_style) or Paragraph(operacion.veterinario.username, normal_style)],
    ]
    fechas_table = Table(fechas_data, colWidths=[2.5*inch, 3.5*inch])
    fechas_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'), ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8f9fa')), ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dee2e6')),
        ('PADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(fechas_table)
    story.append(Spacer(1, 12))
    
    story.append(Paragraph("<b>OPERACIÓN REALIZADA:</b>", normal_style))
    story.append(Paragraph(operacion.operacion, normal_style))
    story.append(Spacer(1, 8))
    
    if operacion.descripcion:
        story.append(Paragraph("<b>DESCRIPCIÓN DETALLADA:</b>", normal_style))
        story.append(Paragraph(operacion.descripcion, normal_style))
        story.append(Spacer(1, 8))
    
    if operacion.estadoSaludPrevio:
        story.append(Paragraph("<b>ESTADO DE SALUD PREVIO A LA OPERACIÓN:</b>", normal_style))
        story.append(Paragraph(operacion.estadoSaludPrevio, normal_style))
        story.append(Spacer(1, 8))
    
    if operacion.complicaciones:
        story.append(Paragraph("<b>COMPLICACIONES DURANTE LA OPERACIÓN:</b>", normal_style))
        story.append(Paragraph(operacion.complicaciones, normal_style))
        story.append(Spacer(1, 8))
    
    story.append(Spacer(1, 20))
    story.append(Paragraph("TÉRMINOS Y CONDICIONES", heading_style))
    terminos_text = "<para>Por medio del presente documento, el propietario de la mascota acepta los siguientes términos y condiciones en relación con la operación realizada:</para>"
    story.append(Paragraph(terminos_text, normal_style))
    story.append(Spacer(1, 10))
    
    incisos = [
        "El propietario autoriza la realización de la operación descrita en este documento bajo el consentimiento informado.",
        "El propietario reconoce que ha sido informado sobre los riesgos y beneficios de la operación y ha aclarado todas sus dudas.",
        "El propietario comprende que, aunque se toman todas las precauciones, existen riesgos inherentes a cualquier procedimiento quirúrgico.",
        "El propietario se compromete a seguir las indicaciones postoperatorias proporcionadas por el veterinario, incluyendo administración de medicamentos, cuidados y controles.",
        "El propietario autoriza a Mascotas Morelia a realizar los procedimientos adicionales que sean necesarios en caso de complicaciones durante la operación.",
        "El propietario se hace responsable de los costos adicionales que puedan surgir por complicaciones o por la necesidad de procedimientos adicionales.",
        "El propietario se compromete a llevar a la mascota a los controles postoperatorios en las fechas indicadas.",
        "Mascotas Morelia no se hace responsable por complicaciones que surjan debido al incumplimiento de las indicaciones postoperatorias por parte del propietario.",
        "El propietario declara que la información proporcionada sobre la salud de su mascota es veraz y completa.",
        "El propietario autoriza el uso de anestesia y otros medicamentos necesarios para el procedimiento."
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
    
    fecha_lugar = f"<para><b>Fecha:</b> {fecha_entrada.strftime('%d/%m/%Y')}<br/><b>Lugar:</b> {operacion.clinicaVeterinaria}</para>"
    story.append(Paragraph(fecha_lugar, normal_style))
    
    pdf_doc.build(story)
    buffer.seek(0)
    
    response = HttpResponse(buffer, content_type='application/pdf')
    filename = f"operacion_{operacion.mascota.nombre}_{fecha_entrada.strftime('%Y%m%d')}.pdf"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response
