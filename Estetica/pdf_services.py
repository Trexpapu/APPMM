import os
from io import BytesIO
from django.conf import settings
from django.http import HttpResponse
from django.utils.timezone import localtime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.units import inch
from reportlab.lib import colors

def generar_pdf_estetica(estetica):
    """Generar PDF con los datos del servicio de estética"""
    fecha_ingreso_local = localtime(estetica.fechaHoraIngreso)
    fecha_egreso_local = localtime(estetica.fechaHoraEgreso) if estetica.fechaHoraEgreso else None
    
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
            
    story.append(Paragraph("SERVICIO DE ESTÉTICA MASCOTAS MORELIA", title_style))
    story.append(Spacer(1, 20))
    
    story.append(Paragraph("INFORMACIÓN DE LA MASCOTA", heading_style))
    info_mascota_data = [
        ['Nombre:', estetica.mascota.nombre],
        ['Especie:', estetica.mascota.especie],
        ['Raza:', estetica.mascota.raza or 'No especificada'],
        ['Fecha de Nacimiento:', estetica.mascota.fechaNacimiento.strftime('%d/%m/%Y') if estetica.mascota.fechaNacimiento else 'No especificada'],
        ['Peso:', f"{estetica.mascota.peso} kg" if estetica.mascota.peso else 'No especificado'],
        ['Sexo:', estetica.mascota.get_sexo_display()],
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
        ['Nombre:', Paragraph(estetica.mascota.cliente.nombre, normal_style)],
        ['Teléfono:', estetica.mascota.cliente.telefono or 'No especificado'],
        ['Email:', Paragraph(estetica.mascota.cliente.email, normal_style) or 'No especificado'],
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
    
    story.append(Paragraph("DATOS DEL SERVICIO DE ESTÉTICA", heading_style))
    story.append(Paragraph("<b>FECHAS Y UBICACIÓN:</b>", normal_style))
    story.append(Spacer(1, 5))
    
    fechas_data = [
        ['Fecha de Ingreso:', fecha_ingreso_local.strftime('%d/%m/%Y %H:%M')],
        ['Fecha de Egreso:', fecha_egreso_local.strftime('%d/%m/%Y %H:%M') if fecha_egreso_local else 'No especificada'],
        ['Clínica Veterinaria:', Paragraph(estetica.clinicaVeterinaria, normal_style)],
        ['Estilista:', Paragraph(estetica.estilista.get_full_name(), normal_style) or Paragraph(estetica.estilista.username, normal_style)],
    ]
    fechas_table = Table(fechas_data, colWidths=[2.5*inch, 3.5*inch])
    fechas_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'), ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8f9fa')), ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dee2e6')),
        ('PADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(fechas_table)
    story.append(Spacer(1, 12))
    
    story.append(Paragraph("<b>SERVICIOS ADICIONALES:</b>", normal_style))
    story.append(Spacer(1, 5))
    
    servicios_adicionales = []
    if estetica.agregarServicioVacuna: servicios_adicionales.append("Vacunación")
    if estetica.agregarServicioDesparasitacion: servicios_adicionales.append("Desparasitación")
    servicios_text = ", ".join(servicios_adicionales) if servicios_adicionales else "Ninguno"
    story.append(Paragraph(servicios_text, normal_style))
    story.append(Spacer(1, 12))
    
    story.append(Paragraph("<b>TIPO DE CORTE:</b>", normal_style))
    story.append(Spacer(1, 5))
    corte_text = estetica.get_cortesDePeloEspeciales_display()
    if estetica.cortesDePeloEspeciales == 'Otro Especifique' and estetica.espeficiacionCorte:
        corte_text += f" ({estetica.espeficiacionCorte})"
    story.append(Paragraph(corte_text, normal_style))
    story.append(Spacer(1, 12))
    
    if estetica.condicionesDeMascota:
        story.append(Paragraph("<b>CONDICIONES DE LA MASCOTA AL INGRESO:</b>", normal_style))
        story.append(Paragraph(estetica.condicionesDeMascota, normal_style))
        story.append(Spacer(1, 12))
        
    if estetica.servicio:
        story.append(Paragraph("<b>SERVICIO SOLICITADO:</b>", normal_style))
        story.append(Paragraph(estetica.servicio, normal_style))
        story.append(Spacer(1, 12))
        
    if estetica.detallesServicio:
        story.append(Paragraph("<b>DETALLES DEL SERVICIO:</b>", normal_style))
        story.append(Paragraph(estetica.detallesServicio, normal_style))
        story.append(Spacer(1, 12))
        
    story.append(Paragraph("<b>INFORMACIÓN DE PAGOS:</b>", normal_style))
    story.append(Spacer(1, 5))
    pagos_data = [['Pagado:', f"${estetica.pagado}"], ['Pago Total:', f"${estetica.pagoTotal}"]]
    pagos_table = Table(pagos_data, colWidths=[2.5*inch, 3.5*inch])
    pagos_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'), ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8f9fa')), ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dee2e6')),
        ('PADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(pagos_table)
    story.append(Spacer(1, 20))
    
    story.append(Paragraph("TÉRMINOS Y CONDICIONES", heading_style))
    terminos_text = "<para>Por medio del presente documento, el propietario de la mascota acepta los siguientes términos y condiciones durante el servicio de estética:</para>"
    story.append(Paragraph(terminos_text, normal_style))
    story.append(Spacer(1, 10))
    
    incisos = [
        "Nuestro servicio incluye baño, limpieza de oídos, corte de uñas, corte de pelo (si se desea) y lavado de dientes (solo si la mascota está acostumbrada).",
        "Mascotas Morelia no se hace responsable por el fallecimiento de la mascota debido a causas mayores.",
        "Si la mascota presenta conductas agresivas, no será posible realizar el servicio."
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
    
    fecha_lugar = f"<para><b>Fecha:</b> {fecha_ingreso_local.strftime('%d/%m/%Y')}<br/><b>Lugar:</b> {estetica.clinicaVeterinaria}</para>"
    story.append(Paragraph(fecha_lugar, normal_style))
    
    pdf_doc.build(story)
    buffer.seek(0)
    
    response = HttpResponse(buffer, content_type='application/pdf')
    filename = f"estetica_{estetica.mascota.nombre}_{fecha_ingreso_local.strftime('%Y%m%d')}.pdf"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response
