from django.shortcuts import render
from django.shortcuts import render

from .models import *
from ClientesMascotas.models import *
from .forms import *
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from Procedimientos.views import encode_image_to_base64
from django.db.models import Q
from django.http import HttpResponse
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from django.conf import settings
import os
from django.utils.timezone import localtime

# Create your views here.
def permisos(request, obj):
    if request.user.is_superuser:
        veterinario = obj.estilista.username
        veterinarioEmail = obj.estilista.email
    else: 
        veterinario = request.user.username
        veterinarioEmail = request.user.email
        obj.estilista = request.user
    return obj, veterinario, veterinarioEmail

@login_required
def indexInicioEstetica(request):
    return render(request, 'estetica/indexEstetica.html')
@login_required
def servicio_estetica_crear(request):
    mascotas = Mascotas.objects.all().select_related('cliente')
    mascota_id = request.GET.get('mascota') or request.POST.get('mascota')
    
    initial_data = {}
    datos_mascota = None

    # 🔹 Cargar datos de la mascota cuando se selecciona una
    if mascota_id:
        try:
            mascota = Mascotas.objects.get(pk=mascota_id)
            # 🔹 Preparar datos de la mascota para mostrar en el template
            datos_mascota = {
                'nombre': mascota.nombre,
                'especie': mascota.especie,
                'raza': mascota.raza,
                'fechaNacimiento': mascota.fechaNacimiento,
                'peso': mascota.peso,
                'sexo': mascota.get_sexo_display(),
                'vacunas': mascota.vacunas,
                'vive': mascota.vive,
                'alergias': mascota.alergias,
                'ultimaDesparasitacion': mascota.ultimaDesparasitacion,
                'ultimoDesparasitante': mascota.ultimoDesparasitante,
                'alimento': mascota.alimento,
                'cliente_nombre': mascota.cliente.nombre,
                'cliente_telefono': mascota.cliente.telefono,
                'cliente_email': mascota.cliente.email,
            }
            
        except Mascotas.DoesNotExist:
            mascota_id = None

    # 🔹 POST: Guardar nueva estética
    if request.method == 'POST':
        form = EsteticaForm(request.POST, request.FILES, initial=initial_data)
        if form.is_valid():
            estetica = form.save(commit=False)
            
            # Procesar imágenes
            if 'fotoAntes' in request.FILES:
                estetica.fotoAntes = encode_image_to_base64(request.FILES['fotoAntes'])
            if 'fotoDespues' in request.FILES:
                estetica.fotoDespues = encode_image_to_base64(request.FILES['fotoDespues'])

            estetica, veterinario, veterinarioEmail=  permisos(request, estetica)
            estetica.save()
            messages.success(request, "Servicio de estética registrado correctamente.")
            return redirect('index-estetica')  # Cambiar por tu URL de listado
    else:
        form = EsteticaForm(initial=initial_data)
        # Establecer el estilista actual por defecto
        form.initial['estilista'] = request.user.id
    
    return render(request, 'estetica/nuevoServicio.html', {
        'form': form,
        'mascotas': mascotas,
        'mascota_id': mascota_id,
        'datos_mascota': datos_mascota,
        'title': 'Nuevo Servicio de Estética'
    })


@login_required
def historial_estetica(request):
    """View that renders a table with all estética records and their associated information."""
    esteticas = Estetica.objects.all().select_related('mascota', 'mascota__cliente', 'estilista').order_by('-fechaHoraIngreso')
    
    # Filtros
    query_cliente = request.GET.get('q_cliente', '').strip()
    query_mascota = request.GET.get('q_mascota', '').strip()
    query_clinica = request.GET.get('q_clinica', '')
    query_fecha_ingreso = request.GET.get('q_fecha_ingreso', '')
    query_estilista = request.GET.get('q_estilista', '')
    
    # Aplicar filtros combinados
    if query_cliente:
        esteticas = esteticas.filter(
            Q(mascota__cliente__nombre__icontains=query_cliente) |
            Q(mascota__cliente__email__icontains=query_cliente) |
            Q(mascota__cliente__telefono__icontains=query_cliente)
        )
    
    if query_mascota:
        esteticas = esteticas.filter(
            Q(mascota__nombre__icontains=query_mascota) |
            Q(mascota__raza__icontains=query_mascota) |
            Q(mascota__especie__icontains=query_mascota)
        )
    
    if query_clinica:
        esteticas = esteticas.filter(clinicaVeterinaria=query_clinica)
    
    if query_fecha_ingreso:
        # Intentar parsear la fecha
        try:
            fecha_parseada = query_fecha_ingreso
            esteticas = esteticas.filter(fechaHoraIngreso__date=fecha_parseada)
        except ValueError:
            esteticas = esteticas.filter(fechaHoraIngreso__icontains=query_fecha_ingreso)
    
    if query_estilista:
        esteticas = esteticas.filter(estilista__username__icontains=query_estilista)
    
    # Datos para los filtros
    clinicas = Estetica.CLINICAS
    
    # Determinar si hay filtros activos
    filtros_activos = any([query_cliente, query_mascota, query_clinica, query_fecha_ingreso, query_estilista])
    
    # Obtener el nombre de la clínica seleccionada para mostrar en el mensaje
    clinica_seleccionada = ''
    if query_clinica:
        for clinica in clinicas:
            if clinica[0] == query_clinica:
                clinica_seleccionada = clinica[1]
                break
    if not filtros_activos:
        esteticas = esteticas[:10]
    context = {
        'esteticas': esteticas,
        'clinicas': clinicas,
        'query_cliente': query_cliente,
        'query_mascota': query_mascota,
        'query_clinica': query_clinica,
        'query_fecha_ingreso': query_fecha_ingreso,
        'query_estilista': query_estilista,
        'filtros_activos': filtros_activos,
        'clinica_seleccionada': clinica_seleccionada,
    }
    
    return render(request, 'estetica/historialServicios.html', context)

@login_required
def servicio_estetica_editar(request, pk):
    """Editar servicio de estética existente."""
    estetica = get_object_or_404(Estetica, pk=pk)
    mascotas = Mascotas.objects.all().select_related('cliente')
    mascota_id = request.GET.get('mascota') or request.POST.get('mascota') or str(estetica.mascota.id) if estetica.mascota else None
    
    datos_mascota = None
    mascota = None

    # 🔹 Cargar datos de la mascota cuando se selecciona una o la actual
    if mascota_id:
        try:
            mascota = Mascotas.objects.get(pk=mascota_id)
            # 🔹 Preparar datos de la mascota para mostrar en el template (solo información)
            datos_mascota = {
                'nombre': mascota.nombre,
                'especie': mascota.especie,
                'raza': mascota.raza,
                'fechaNacimiento': mascota.fechaNacimiento,
                'peso': mascota.peso,
                'sexo': mascota.get_sexo_display(),
                'vacunas': mascota.vacunas,
                'alergias': mascota.alergias,
                'vive': mascota.vive,
                'ultimaDesparasitacion': mascota.ultimaDesparasitacion,
                'ultimoDesparasitante': mascota.ultimoDesparasitante,
                'alimento': mascota.alimento,
                'cliente_nombre': mascota.cliente.nombre,
                'cliente_telefono': mascota.cliente.telefono,
                'cliente_email': mascota.cliente.email,
            }
            
        except Mascotas.DoesNotExist:
            mascota_id = None

    # 🔹 POST: Guardar cambios en la estética
    if request.method == 'POST':
        form = EsteticaUpdateForm(request.POST, instance=estetica)
        if form.is_valid():
            estetica_editada = form.save(commit=False)
            
            # 🔹 ACTUALIZAR MASCOTA SI SE HA SELECCIONADO UNA NUEVA
            if mascota_id and mascota:
                estetica_editada.mascota = mascota
            
            # 🔹 MANEJAR FOTO ANTES
            if 'fotoAntes' in request.FILES and request.FILES['fotoAntes']:
                # Nueva imagen subida - convertir a base64
                estetica_editada.fotoAntes = encode_image_to_base64(request.FILES['fotoAntes'])
            else:
                # Mantener la imagen existente - NO hacer nada, ya está en la instancia
                pass
            
            # 🔹 MANEJAR FOTO DESPUÉS
            if 'fotoDespues' in request.FILES and request.FILES['fotoDespues']:
                # Nueva imagen subida - convertir a base64
                estetica_editada.fotoDespues = encode_image_to_base64(request.FILES['fotoDespues'])
            else:
                # Mantener la imagen existente - NO hacer nada, ya está en la instancia
                pass
            estetica_editada, veterinario, veterinarioEmail=  permisos(request, estetica_editada)
            estetica_editada.save()
            messages.success(request, "Servicio de estética actualizado correctamente.")
            return redirect('servicio_estetica_detalle', pk=estetica.pk)
    else:
        form = EsteticaUpdateForm(instance=estetica)

    return render(request, 'estetica/editarServicio.html', {
        'form': form,
        'mascotas': mascotas,
        'mascota_id': mascota_id,
        'datos_mascota': datos_mascota,
        'estetica_actual': estetica
    })


@login_required
def servicio_estetica_detalle(request, pk):
    """Vista para ver el detalle completo de un servicio de estética."""
    estetica = get_object_or_404(Estetica, pk=pk)
    
    # Preparar datos de la mascota para mostrar
    datos_mascota = {
        'nombre': estetica.mascota.nombre,
        'especie': estetica.mascota.especie,
        'raza': estetica.mascota.raza,
        'fechaNacimiento': estetica.mascota.fechaNacimiento,
        'peso': estetica.mascota.peso,
        'sexo': estetica.mascota.get_sexo_display(),
        'vacunas': estetica.mascota.vacunas,
        'alergias': estetica.mascota.alergias,
        'ultimaDesparasitacion': estetica.mascota.ultimaDesparasitacion,
        'ultimoDesparasitante': estetica.mascota.ultimoDesparasitante,
        'alimento': estetica.mascota.alimento,
        'cliente_nombre': estetica.mascota.cliente.nombre,
        'cliente_telefono': estetica.mascota.cliente.telefono,
        'cliente_email': estetica.mascota.cliente.email,
        'vive': estetica.mascota.vive,
    }
    
    return render(request, 'estetica/detalleServicio.html', {
        'estetica': estetica,
        'datos_mascota': datos_mascota,
    })

@login_required
def servicio_estetica_eliminar(request, pk):
    """View to delete an existing estética service."""
    estetica = get_object_or_404(Estetica, pk=pk)
    estetica.delete()
    return redirect('historial-estetica')



@login_required
def generar_pdf_estetica(request, pk):
    """Generar PDF con los datos del servicio de estética"""
    estetica = get_object_or_404(Estetica, pk=pk)
    
    # Convertir las fechas a la zona horaria local
    fecha_ingreso_local = localtime(estetica.fechaHoraIngreso)
    fecha_egreso_local = localtime(estetica.fechaHoraEgreso) if estetica.fechaHoraEgreso else None
    
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
    story.append(Paragraph("SERVICIO DE ESTÉTICA MASCOTAS MORELIA", title_style))
    story.append(Spacer(1, 20))
    
    # Información de la mascota
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
    story.append(info_mascota_table)
    story.append(Spacer(1, 20))
    
    # Información del dueño
    story.append(Paragraph("INFORMACIÓN DEL PROPIETARIO", heading_style))
    info_cliente_data = [
        ['Nombre:', estetica.mascota.cliente.nombre],
        ['Teléfono:', estetica.mascota.cliente.telefono or 'No especificado'],
        ['Email:', estetica.mascota.cliente.email or 'No especificado'],
    ]
    
    info_cliente_table = Table(info_cliente_data, colWidths=[2*inch, 4*inch])
    info_cliente_table.setStyle(TableStyle([
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
    story.append(info_cliente_table)
    story.append(Spacer(1, 20))
    
    # Datos del servicio de estética
    story.append(Paragraph("DATOS DEL SERVICIO DE ESTÉTICA", heading_style))
    
    # Fechas y clínica
    story.append(Paragraph("<b>FECHAS Y UBICACIÓN:</b>", normal_style))
    story.append(Spacer(1, 5))
    
    fechas_data = [
        ['Fecha de Ingreso:', fecha_ingreso_local.strftime('%d/%m/%Y %H:%M')],
        ['Fecha de Egreso:', fecha_egreso_local.strftime('%d/%m/%Y %H:%M') if fecha_egreso_local else 'No especificada'],
        ['Clínica Veterinaria:', estetica.clinicaVeterinaria],
        ['Estilista:', estetica.estilista.get_full_name() or estetica.estilista.username],
    ]
    
    fechas_table = Table(fechas_data, colWidths=[2.5*inch, 3.5*inch])
    fechas_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8f9fa')),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dee2e6')),
        ('PADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(fechas_table)
    story.append(Spacer(1, 12))
    
    # Servicios adicionales
    story.append(Paragraph("<b>SERVICIOS ADICIONALES:</b>", normal_style))
    story.append(Spacer(1, 5))
    
    servicios_adicionales = []
    if estetica.agregarServicioVacuna:
        servicios_adicionales.append("Vacunación")
    if estetica.agregarServicioDesparasitacion:
        servicios_adicionales.append("Desparasitación")
    
    servicios_text = ", ".join(servicios_adicionales) if servicios_adicionales else "Ninguno"
    story.append(Paragraph(servicios_text, normal_style))
    story.append(Spacer(1, 12))
    
    # Tipo de corte
    story.append(Paragraph("<b>TIPO DE CORTE:</b>", normal_style))
    story.append(Spacer(1, 5))
    
    corte_text = estetica.get_cortesDePeloEspeciales_display()
    if estetica.cortesDePeloEspeciales == 'Otro Especifique' and estetica.espeficiacionCorte:
        corte_text += f" ({estetica.espeficiacionCorte})"
    
    story.append(Paragraph(corte_text, normal_style))
    story.append(Spacer(1, 12))
    
    # Condiciones de la mascota
    if estetica.condicionesDeMascota:
        story.append(Paragraph("<b>CONDICIONES DE LA MASCOTA AL INGRESO:</b>", normal_style))
        story.append(Paragraph(estetica.condicionesDeMascota, normal_style))
        story.append(Spacer(1, 12))
    
    # Servicio solicitado
    if estetica.servicio:
        story.append(Paragraph("<b>SERVICIO SOLICITADO:</b>", normal_style))
        story.append(Paragraph(estetica.servicio, normal_style))
        story.append(Spacer(1, 12))
    
    # Detalles del servicio
    if estetica.detallesServicio:
        story.append(Paragraph("<b>DETALLES DEL SERVICIO:</b>", normal_style))
        story.append(Paragraph(estetica.detallesServicio, normal_style))
        story.append(Spacer(1, 12))
    
    # Información de pagos
    story.append(Paragraph("<b>INFORMACIÓN DE PAGOS:</b>", normal_style))
    story.append(Spacer(1, 5))
    
    pagos_data = [
        ['Pagado:', f"${estetica.pagado}"],
        ['Pago Total:', f"${estetica.pagoTotal}"],
    ]
    
    pagos_table = Table(pagos_data, colWidths=[2.5*inch, 3.5*inch])
    pagos_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8f9fa')),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dee2e6')),
        ('PADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(pagos_table)
    story.append(Spacer(1, 20))
    
    # Términos y condiciones
    story.append(Paragraph("TÉRMINOS Y CONDICIONES", heading_style))
    
    terminos_text = """
    <para>
    Por medio del presente documento, el propietario de la mascota acepta los siguientes términos y condiciones durante el servicio de estética:
    </para>
    """
    story.append(Paragraph(terminos_text, normal_style))
    story.append(Spacer(1, 10))
    
    # Incisos específicos para estética
    incisos = [
        "La mascota será atendida bajo el cuidado y supervisión del personal calificado de Mascotas Morelia.",
        "El propietario declara que la mascota se encuentra en buen estado de salud al momento del ingreso, salvo lo indicado en el apartado correspondiente.",
        "En caso de que la mascota presente algún problema de salud durante el servicio, Mascotas Morelia se reserva el derecho de proporcionar la atención veterinaria necesaria, cuyos costos serán asumidos por el propietario.",
        "El propietario autoriza a Mascotas Morelia a realizar el corte de pelo, baño y otros servicios de estética según lo acordado.",
        "Mascotas Morelia no se hace responsable por reacciones alérgicas a productos de estética si el propietario no informó previamente sobre alergias conocidas.",
        "El horario de visita es de 9:00 am a 8:00 pm. Visitas fuera de este horario deben ser coordinadas previamente.",
        "El pago del servicio debe ser liquidado en su totalidad al momento del retiro de la mascota.",
        "En caso de no recoger a la mascota en la fecha acordada sin previo aviso, se aplicarán cargos por día adicional.",
        "El propietario se compromete a proporcionar información veraz sobre el estado de salud, comportamiento y necesidades especiales de su mascota.",
        "El propietario autoriza a Mascotas Morelia a tomar decisiones en caso de emergencia cuando no pueda ser contactado.",
        "Todas las mascotas deben contar con vacunación al día. En caso contrario, se aplicará un cargo adicional por vacunación de emergencia.",
        "El propietario es responsable de informar sobre cualquier condición médica preexistente, alergias o medicamentos que requiera la mascota.",
        "Mascotas Morelia se reserva el derecho de negar el servicio si la mascota muestra conductas agresivas que pongan en riesgo al personal.",
        "El propietario acepta que las fotos tomadas antes y después del servicio podrán ser utilizadas con fines promocionales de la clínica.",
        "El propietario recoge a su mascota en el horario acordado; de lo contrario, se aplicará un cargo extra por cuidado extendido."
    ]
    
    for i, inciso in enumerate(incisos, 1):
        story.append(Paragraph(f"<b>{i}.</b> {inciso}", normal_style))
        story.append(Spacer(1, 5))
    
    story.append(Spacer(1, 20))
    
    # Firma
    story.append(Paragraph("CONFORMIDAD Y ACEPTACIÓN", heading_style))
    
    firma_text = """
    <para>
    El propietario declara haber leído y comprendido los términos y condiciones anteriores, y acepta cumplir con lo establecido en este documento.
    </para>
    """
    story.append(Paragraph(firma_text, normal_style))
    story.append(Spacer(1, 30))
    
    # Espacio para firma
    firma_data = [
        ['', ''],
        ['_________________________', '_________________________'],
        ['Nombre del Propietario', 'Firma del Propietario'],
    ]
    
    firma_table = Table(firma_data, colWidths=[3*inch, 3*inch])
    firma_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(firma_table)
    story.append(Spacer(1, 20))
    
    # Fecha y lugar (usando la fecha local)
    fecha_lugar = f"""
    <para>
    <b>Fecha:</b> {fecha_ingreso_local.strftime('%d/%m/%Y')}<br/>
    <b>Lugar:</b> {estetica.clinicaVeterinaria}
    </para>
    """
    story.append(Paragraph(fecha_lugar, normal_style))
    
    # Generar el PDF
    pdf_doc.build(story)
    buffer.seek(0)
    
    # Crear respuesta
    response = HttpResponse(buffer, content_type='application/pdf')
    filename = f"estetica_{estetica.mascota.nombre}_{fecha_ingreso_local.strftime('%Y%m%d')}.pdf"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    return response