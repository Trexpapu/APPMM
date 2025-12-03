from django.shortcuts import render

from Procedimientos.models import ListaVacunas
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
# Create your views here.
@login_required
def index_guarderia_hospitalizacion(request):
    return render(request, 'guarderiaHospitalizacion/indexGuarderiaHospitalizacion.html')


@login_required
def servicio_guarderia_crear(request):
    mascotas = Mascotas.objects.all().select_related('cliente')
    mascota_id = request.GET.get('mascota') or request.POST.get('mascota')
    
    initial_data = {}
    datos_mascota = None

    # 🔹 Cargar datos de la mascota cuando se selecciona una
    if mascota_id:
        try:
            mascota = Mascotas.objects.get(pk=mascota_id)
            # ✅ DATOS DE MASCOTA - Siempre se cargan
            initial_data.update({
                'alimento': mascota.alimento,
            })
            
            # 🔹 Preparar datos de la mascota para mostrar en el template
            datos_mascota = {
                'nombre': mascota.nombre,
                'especie': mascota.especie,
                'raza': mascota.raza,
                'fechaNacimiento': mascota.fechaNacimiento,
                'peso': mascota.peso,
                'sexo': mascota.get_sexo_display(),
                'vive': mascota.vive,
                'vacunas': mascota.vacunas,
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

    # 🔹 POST: Guardar nueva guardería
    if request.method == 'POST':
        form = GuarderiaForm(request.POST, request.FILES, initial=initial_data)
        if form.is_valid():
            guarderia = form.save(commit=False)
            
            # Procesar imágenes
            if 'fotoAntes' in request.FILES:
                guarderia.fotoAntes = encode_image_to_base64(request.FILES['fotoAntes'])
            if 'fotoDespues' in request.FILES:
                guarderia.fotoDespues = encode_image_to_base64(request.FILES['fotoDespues'])
            mascota = form.cleaned_data.get('mascota')
            mascotapk = mascota.pk 
            mascota = get_object_or_404(Mascotas, pk=mascotapk)
            mascota.alimento = form.cleaned_data.get('alimento') or mascota.alimento
            mascota.save()
            guarderia.save()
            messages.success(request, "Servicio de guardería registrado correctamente.")
            return redirect('index-guarderia-hospitalizacion')
    else:
        form = GuarderiaForm(initial=initial_data)
    
    return render(request, 'guarderiaHospitalizacion/guarderia/nuevoServicio.html', {
        'form': form,
        'mascotas': mascotas,
        'mascota_id': mascota_id,
        'datos_mascota': datos_mascota,
        'title': 'Nuevo Servicio de Guardería'
    })



@login_required
def historial_guarderia(request):
    """View that renders a table with all guarderia records and their associated information."""
    guarderias = Guarderia.objects.all().select_related('mascota', 'mascota__cliente').order_by('-fechaEntrada')
    
    # Filtros
    query_cliente = request.GET.get('q_cliente', '').strip().lower()
    query_mascota = request.GET.get('q_mascota', '').strip().lower()
    query_veterinaria = request.GET.get('q_veterinaria', '')
    query_fecha_entrada = request.GET.get('q_fecha_entrada', '')
    query_estado = request.GET.get('q_estado', '')  # Nuevo filtro por estado
    
    # Aplicar filtros combinados
    if query_cliente:
        guarderias = guarderias.filter(
            Q(mascota__cliente__nombre__icontains=query_cliente) |
            Q(mascota__cliente__email__icontains=query_cliente) |
            Q(mascota__cliente__telefono__icontains=query_cliente)
        )
    
    if query_mascota:
        guarderias = guarderias.filter(
            Q(mascota__nombre__icontains=query_mascota) |
            Q(mascota__raza__icontains=query_mascota) |
            Q(mascota__especie__icontains=query_mascota)
        )
    
    if query_veterinaria:
        guarderias = guarderias.filter(clinicaVeterinaria=query_veterinaria)
    
    if query_fecha_entrada:
        guarderias = guarderias.filter(fechaEntrada=query_fecha_entrada)
    
    if query_estado:  # Nuevo filtro por estado
        guarderias = guarderias.filter(estado=query_estado)
    
    # Datos para los filtros
    clinicas = Guarderia.CLINICAS
    estados = Guarderia.ESTADOS  # Obtenemos las opciones de estado del modelo
    
    # Determinar si hay filtros activos
    filtros_activos = any([query_cliente, query_mascota, query_veterinaria, query_fecha_entrada, query_estado])
    
    return render(request, 'guarderiaHospitalizacion/guarderia/historialGuarderia.html', {
        'guarderias': guarderias,
        'clinicas': clinicas,
        'estados': estados,  # Pasamos los estados al contexto
        'query_cliente': query_cliente,
        'query_mascota': query_mascota,
        'query_veterinaria': query_veterinaria,
        'query_fecha_entrada': query_fecha_entrada,
        'query_estado': query_estado,  # Pasamos el estado seleccionado
        'filtros_activos': filtros_activos
    })





@login_required
def servicio_guarderia_editar(request, pk):
    """Editar servicio de guardería existente."""
    guarderia = get_object_or_404(Guarderia, pk=pk)
    mascotas = Mascotas.objects.all().select_related('cliente')
    mascota_id = request.GET.get('mascota') or str(guarderia.mascota.id) if guarderia.mascota else None
    
    datos_mascota = None

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

    # 🔹 POST: Guardar cambios en la guardería
    if request.method == 'POST':
        form = GuarderiaUpdateForm(request.POST, instance=guarderia)
        if form.is_valid():
            guarderia_editada = form.save(commit=False)
            mascota_id = request.POST.get('mascota')
            if mascota_id:
                guarderia_editada.mascota_id = mascota_id
            
            # 🔹 MANEJAR FOTO ANTES - SIGUIENDO LA MISMA LÓGICA QUE OPERACIONES
            if 'fotoAntes' in request.FILES and request.FILES['fotoAntes']:
                # Nueva imagen subida - convertir a base64
                guarderia_editada.fotoAntes = encode_image_to_base64(request.FILES['fotoAntes'])
            else:
                # Mantener la imagen existente - NO hacer nada, ya está en la instancia
                pass  # Django automáticamente mantiene el valor existente
            
            # 🔹 MANEJAR FOTO DESPUÉS - SIGUIENDO LA MISMA LÓGICA QUE OPERACIONES
            if 'fotoDespues' in request.FILES and request.FILES['fotoDespues']:
                # Nueva imagen subida - convertir a base64
                guarderia_editada.fotoDespues = encode_image_to_base64(request.FILES['fotoDespues'])
            else:
                # Mantener la imagen existente - NO hacer nada, ya está en la instancia
                pass
            
            guarderia_editada.save()
            messages.success(request, "Servicio de guardería actualizado correctamente.")
            return redirect('servicio_guarderia_detalle', pk=guarderia.pk)
    else:
        form = GuarderiaUpdateForm(instance=guarderia)

    return render(request, 'guarderiaHospitalizacion/guarderia/editarServicio.html', {
        'form': form,
        'mascotas': mascotas,
        'mascota_id': mascota_id,
        'datos_mascota': datos_mascota,
        'guarderia_actual': guarderia
    })

@login_required
def servicio_guarderia_detalle(request, pk):
    """Vista para ver el detalle completo de un servicio de guardería."""
    guarderia = get_object_or_404(Guarderia, pk=pk)
    
    # Preparar datos de la mascota para mostrar
    datos_mascota = {
        'nombre': guarderia.mascota.nombre,
        'especie': guarderia.mascota.especie,
        'raza': guarderia.mascota.raza,
        'fechaNacimiento': guarderia.mascota.fechaNacimiento,
        'peso': guarderia.mascota.peso,
        'sexo': guarderia.mascota.get_sexo_display(),
        'vacunas': guarderia.mascota.vacunas,
        'alergias': guarderia.mascota.alergias,
        'ultimaDesparasitacion': guarderia.mascota.ultimaDesparasitacion,
        'ultimoDesparasitante': guarderia.mascota.ultimoDesparasitante,
        'alimento': guarderia.mascota.alimento,
        'cliente_nombre': guarderia.mascota.cliente.nombre,
        'cliente_telefono': guarderia.mascota.cliente.telefono,
        'cliente_email': guarderia.mascota.cliente.email,
        'vive': guarderia.mascota.vive,
    }
    
    return render(request, 'guarderiaHospitalizacion/guarderia/detalleServicio.html', {
        'guarderia': guarderia,
        'datos_mascota': datos_mascota,
    })




@login_required
def generar_pdf_guarderia(request, pk):
    """Generar PDF con los datos del servicio de guardería"""
    guarderia = get_object_or_404(Guarderia, id=pk)
    
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
    logo_path = os.path.join(settings.MEDIA_ROOT, 'logo.png')  # Ajusta la ruta según donde tengas tu logo
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
    story.append(Paragraph("SERVICIO DE GUARDERÍA MASCOTAS MORELIA", title_style))
    story.append(Spacer(1, 20))
    
    # Información de la mascota
    story.append(Paragraph("INFORMACIÓN DE LA MASCOTA", heading_style))
    info_mascota_data = [
        ['Nombre:', guarderia.mascota.nombre],
        ['Especie:', guarderia.mascota.especie],
        ['Raza:', guarderia.mascota.raza or 'No especificada'],
        ['Fecha de Nacimiento:', guarderia.mascota.fechaNacimiento.strftime('%d/%m/%Y') if guarderia.mascota.fechaNacimiento else 'No especificada'],
        ['Peso:', f"{guarderia.mascota.peso} kg" if guarderia.mascota.peso else 'No especificado'],
        ['Sexo:', guarderia.mascota.get_sexo_display()],
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
        ['Nombre:', guarderia.mascota.cliente.nombre],
        ['Teléfono:', guarderia.mascota.cliente.telefono or 'No especificado'],
        ['Email:', guarderia.mascota.cliente.email or 'No especificado'],
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
    
    # Datos del servicio de guardería
    story.append(Paragraph("DATOS DEL SERVICIO DE GUARDERÍA", heading_style))
    
    # Fechas y clínica
    story.append(Paragraph("<b>FECHAS Y UBICACIÓN:</b>", normal_style))
    story.append(Spacer(1, 5))
    
    fechas_data = [
        ['Fecha de Ingreso:', guarderia.fechaEntrada.strftime('%d/%m/%Y')],
        ['Fecha de Egreso Programada:', guarderia.fechaSalidaProgramada.strftime('%d/%m/%Y') if guarderia.fechaSalidaProgramada else 'No especificada'],
        ['Clínica Veterinaria:', guarderia.clinicaVeterinaria],
        ['Estado del Servicio:', guarderia.estado],
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
    
    # Información de alimentación y salud
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
    
    # Información de pagos
    story.append(Paragraph("<b>INFORMACIÓN DE PAGOS:</b>", normal_style))
    story.append(Spacer(1, 5))
    
    pagos_data = [
        ['Pagado:', f"${guarderia.pagado}"],
        ['Pago Total:', f"${guarderia.pagoTotal}"],
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
    Por medio del presente documento, el propietario de la mascota acepta los siguientes términos y condiciones durante el servicio de guardería:
    </para>
    """
    story.append(Paragraph(terminos_text, normal_style))
    story.append(Spacer(1, 10))
    
    # Incisos
    incisos = [
        "La mascota será atendida bajo el cuidado y supervisión del personal calificado de Mascotas Morelia.",
        "El propietario declara que la mascota se encuentra en buen estado de salud al momento del ingreso, salvo lo indicado en el apartado correspondiente.",
        "En caso de emergencia médica, Mascotas Morelia se reserva el derecho de proporcionar la atención veterinaria necesaria, cuyos costos serán asumidos por el propietario.",
        "El propietario autoriza a Mascotas Morelia a administrar los tratamientos y medicamentos indicados en este documento.",
        "Mascotas Morelia no se hace responsable por objetos personales (juguetes, cobijas, etc.) que puedan sufrir daño durante la estancia.",
        "El horario de recolección de mascotas es de 9:00 am a 8:00 pm. Recoger a la mascota fuera de este horario podría generar cargos adicionales.",
        "El pago del servicio debe ser liquidado en su totalidad al momento de la recolección de la mascota.",
        "En caso de no recoger a la mascota en la fecha acordada sin previo aviso, se aplicarán cargos por día adicional.",
        "El propietario se compromete a proporcionar información veraz sobre el estado de salud, comportamiento y necesidades especiales de su mascota."
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
    
    # Fecha y lugar
    fecha_lugar = f"""
    <para>
    <b>Fecha:</b> {guarderia.fechaEntrada.strftime('%d/%m/%Y')}<br/>
    <b>Lugar:</b> {guarderia.clinicaVeterinaria}
    </para>
    """
    story.append(Paragraph(fecha_lugar, normal_style))
    
    # Generar el PDF
    pdf_doc.build(story)
    buffer.seek(0)
    
    # Crear respuesta
    response = HttpResponse(buffer, content_type='application/pdf')
    filename = f"guarderia_{guarderia.mascota.nombre}_{guarderia.fechaEntrada.strftime('%Y%m%d')}.pdf"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    return response


# Vista para eliminar vacuna
@login_required
def servicio_guarderia_eliminar(request, pk):
    """View to delete an existing pet."""
    guarderia = get_object_or_404(Guarderia, pk=pk)
    guarderia.delete()
    return redirect('historial-guarderia')



@login_required
def servicio_hospitalizacion_crear(request):
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

    # 🔹 POST: Guardar nueva hospitalización
    if request.method == 'POST':
        form = HospitalizacionForm(request.POST, request.FILES, initial=initial_data)
        if form.is_valid():
            hospitalizacion = form.save(commit=False)
            
            # Procesar imágenes
            if 'fotoAntes' in request.FILES:
                hospitalizacion.fotoAntes = encode_image_to_base64(request.FILES['fotoAntes'])
            if 'fotoDespues' in request.FILES:
                hospitalizacion.fotoDespues = encode_image_to_base64(request.FILES['fotoDespues'])
            
            hospitalizacion.save()
            messages.success(request, "Servicio de hospitalización registrado correctamente.")
            return redirect('index-guarderia-hospitalizacion')  # Ajusta según tu URL
    else:
        form = HospitalizacionForm(initial=initial_data)
    
    return render(request, 'guarderiaHospitalizacion/hospitalizacion/nuevoServicio.html', {
        'form': form,
        'mascotas': mascotas,
        'mascota_id': mascota_id,
        'datos_mascota': datos_mascota,
        'title': 'Nuevo Servicio de Hospitalización'
    })


@login_required
def servicio_hospitalizacion_editar(request, pk):
    """Editar servicio de hospitalización existente."""
    hospitalizacion = get_object_or_404(Hospitalizacion, pk=pk)
    mascotas = Mascotas.objects.all().select_related('cliente')
    mascota_id = request.GET.get('mascota') or request.POST.get('mascota') or str(hospitalizacion.mascota.id) if hospitalizacion.mascota else None
    
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

    # 🔹 POST: Guardar cambios en la hospitalización
    if request.method == 'POST':
        form = HospitalizacionUpdateForm(request.POST, instance=hospitalizacion)
        if form.is_valid():
            hospitalizacion_editada = form.save(commit=False)
            
            # 🔹 ACTUALIZAR MASCOTA SI SE HA SELECCIONADO UNA NUEVA
            if mascota_id and mascota:
                hospitalizacion_editada.mascota = mascota
            
            # 🔹 MANEJAR FOTO ANTES - SIGUIENDO LA MISMA LÓGICA QUE GUARDERÍA
            if 'fotoAntes' in request.FILES and request.FILES['fotoAntes']:
                # Nueva imagen subida - convertir a base64
                hospitalizacion_editada.fotoAntes = encode_image_to_base64(request.FILES['fotoAntes'])
            else:
                # Mantener la imagen existente - NO hacer nada, ya está en la instancia
                pass  # Django automáticamente mantiene el valor existente
            
            # 🔹 MANEJAR FOTO DESPUÉS - SIGUIENDO LA MISMA LÓGICA QUE GUARDERÍA
            if 'fotoDespues' in request.FILES and request.FILES['fotoDespues']:
                # Nueva imagen subida - convertir a base64
                hospitalizacion_editada.fotoDespues = encode_image_to_base64(request.FILES['fotoDespues'])
            else:
                # Mantener la imagen existente - NO hacer nada, ya está en la instancia
                pass
            
            hospitalizacion_editada.save()
            messages.success(request, "Servicio de hospitalización actualizado correctamente.")
            return redirect('servicio_hospitalizacion_detalle', pk=hospitalizacion.pk)
    else:
        form = HospitalizacionUpdateForm(instance=hospitalizacion)

    return render(request, 'guarderiaHospitalizacion/hospitalizacion/editarServicio.html', {
        'form': form,
        'mascotas': mascotas,
        'mascota_id': mascota_id,
        'datos_mascota': datos_mascota,
        'hospitalizacion_actual': hospitalizacion
    })



@login_required
def generar_pdf_hospitalizacion(request, pk):
    """Generar PDF con los datos del servicio de hospitalización"""
    hospitalizacion = get_object_or_404(Hospitalizacion, pk=pk)
    
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
    story.append(Paragraph("SERVICIO DE HOSPITALIZACIÓN MASCOTAS MORELIA", title_style))
    story.append(Spacer(1, 20))
    
    # Información de la mascota
    story.append(Paragraph("INFORMACIÓN DE LA MASCOTA", heading_style))
    info_mascota_data = [
        ['Nombre:', hospitalizacion.mascota.nombre],
        ['Especie:', hospitalizacion.mascota.especie],
        ['Raza:', hospitalizacion.mascota.raza or 'No especificada'],
        ['Fecha de Nacimiento:', hospitalizacion.mascota.fechaNacimiento.strftime('%d/%m/%Y') if hospitalizacion.mascota.fechaNacimiento else 'No especificada'],
        ['Peso:', f"{hospitalizacion.mascota.peso} kg" if hospitalizacion.mascota.peso else 'No especificado'],
        ['Sexo:', hospitalizacion.mascota.get_sexo_display()],
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
        ['Nombre:', hospitalizacion.mascota.cliente.nombre],
        ['Teléfono:', hospitalizacion.mascota.cliente.telefono or 'No especificado'],
        ['Email:', hospitalizacion.mascota.cliente.email or 'No especificado'],
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
    
    # Datos del servicio de hospitalización
    story.append(Paragraph("DATOS DEL SERVICIO DE HOSPITALIZACIÓN", heading_style))
    
    # Fechas y clínica
    story.append(Paragraph("<b>FECHAS Y UBICACIÓN:</b>", normal_style))
    story.append(Spacer(1, 5))
    
    fechas_data = [
        ['Fecha de Ingreso:', hospitalizacion.fechaEntrada.strftime('%d/%m/%Y')],
        ['Fecha de Egreso:', hospitalizacion.fechaSalida.strftime('%d/%m/%Y') if hospitalizacion.fechaSalida else 'No especificada'],
        ['Clínica Veterinaria:', hospitalizacion.clinicaVeterinaria],
        ['Estado del Paciente:', hospitalizacion.estado],
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
    
    # Motivo y diagnóstico
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
    
    # Información de pagos
    story.append(Paragraph("<b>INFORMACIÓN DE PAGOS:</b>", normal_style))
    story.append(Spacer(1, 5))
    
    pagos_data = [
        ['Pagado:', f"${hospitalizacion.pagado}"],
        ['Pago Total:', f"${hospitalizacion.pagoTotal}"],
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
    Por medio del presente documento, el propietario de la mascota acepta los siguientes términos y condiciones durante el servicio de hospitalización:
    </para>
    """
    story.append(Paragraph(terminos_text, normal_style))
    story.append(Spacer(1, 10))
    
    # Incisos
    incisos = [
        "La mascota será atendida bajo el cuidado y supervisión del personal calificado de Mascotas Morelia.",
        "El propietario declara que la mascota se encuentra en buen estado de salud al momento del ingreso, salvo lo indicado en el apartado correspondiente.",
        "En caso de emergencia médica, Mascotas Morelia se reserva el derecho de proporcionar la atención veterinaria necesaria, cuyos costos serán asumidos por el propietario.",
        "El propietario autoriza a Mascotas Morelia a administrar los tratamientos y medicamentos indicados en este documento.",
        "Mascotas Morelia no se hace responsable por objetos personales (juguetes, cobijas, etc.) que puedan sufrir daño durante la estancia.",
        "El horario de visita es de 9:00 am a 8:00 pm. Visitas fuera de este horario deben ser coordinadas previamente.",
        "El pago del servicio debe ser liquidado en su totalidad al momento del alta de la mascota.",
        "En caso de no recoger a la mascota en la fecha acordada sin previo aviso, se aplicarán cargos por día adicional.",
        "El propietario se compromete a proporcionar información veraz sobre el estado de salud, comportamiento y necesidades especiales de su mascota.",
        "El propietario autoriza a Mascotas Morelia a tomar decisiones médicas en caso de emergencia cuando no pueda ser contactado.",
        "Todas las mascotas deben contar con vacunación al día. En caso contrario, se aplicará un cargo adicional por vacunación de emergencia.",
        "El propietario es responsable de informar sobre cualquier condición médica preexistente, alergias o medicamentos que requiera la mascota."
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
    
    # Fecha y lugar
    fecha_lugar = f"""
    <para>
    <b>Fecha:</b> {hospitalizacion.fechaEntrada.strftime('%d/%m/%Y')}<br/>
    <b>Lugar:</b> {hospitalizacion.clinicaVeterinaria}
    </para>
    """
    story.append(Paragraph(fecha_lugar, normal_style))
    
    # Generar el PDF
    pdf_doc.build(story)
    buffer.seek(0)
    
    # Crear respuesta
    response = HttpResponse(buffer, content_type='application/pdf')
    filename = f"hospitalizacion_{hospitalizacion.mascota.nombre}_{hospitalizacion.fechaEntrada.strftime('%Y%m%d')}.pdf"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    return response



@login_required
def servicio_hospitalizacion_detalle(request, pk):
    """Vista para ver el detalle completo de una hospitalización."""
    hospitalizacion = get_object_or_404(Hospitalizacion, pk=pk)
    
    # Preparar datos de la mascota para mostrar
    datos_mascota = {
        'nombre': hospitalizacion.mascota.nombre,
        'especie': hospitalizacion.mascota.especie,
        'raza': hospitalizacion.mascota.raza,
        'fechaNacimiento': hospitalizacion.mascota.fechaNacimiento,
        'peso': hospitalizacion.mascota.peso,
        'sexo': hospitalizacion.mascota.get_sexo_display(),
        'vacunas': hospitalizacion.mascota.vacunas,
        'alergias': hospitalizacion.mascota.alergias,
        'ultimaDesparasitacion': hospitalizacion.mascota.ultimaDesparasitacion,
        'ultimoDesparasitante': hospitalizacion.mascota.ultimoDesparasitante,
        'alimento': hospitalizacion.mascota.alimento,
        'cliente_nombre': hospitalizacion.mascota.cliente.nombre,
        'cliente_telefono': hospitalizacion.mascota.cliente.telefono,
        'cliente_email': hospitalizacion.mascota.cliente.email,
        'vive': hospitalizacion.mascota.vive,
    }
    
    return render(request, 'guarderiaHospitalizacion/hospitalizacion/detalleServicio.html', {
        'hospitalizacion': hospitalizacion,
        'datos_mascota': datos_mascota,
    })





@login_required
def historial_hospitalizacion(request):
    """View that renders a table with all hospitalization records and their associated information."""
    hospitalizaciones = Hospitalizacion.objects.all().select_related('mascota', 'mascota__cliente').order_by('-fechaEntrada')
    
    # Filtros
    query_cliente = request.GET.get('q_cliente', '').strip()
    query_mascota = request.GET.get('q_mascota', '').strip()
    query_veterinaria = request.GET.get('q_veterinaria', '')
    query_fecha_entrada = request.GET.get('q_fecha_entrada', '')
    query_estado = request.GET.get('q_estado', '')
    
    # Aplicar filtros combinados
    if query_cliente:
        hospitalizaciones = hospitalizaciones.filter(
            Q(mascota__cliente__nombre__icontains=query_cliente) |
            Q(mascota__cliente__email__icontains=query_cliente) |
            Q(mascota__cliente__telefono__icontains=query_cliente)
        )
    
    if query_mascota:
        hospitalizaciones = hospitalizaciones.filter(
            Q(mascota__nombre__icontains=query_mascota) |
            Q(mascota__raza__icontains=query_mascota) |
            Q(mascota__especie__icontains=query_mascota)
        )
    
    if query_veterinaria:
        hospitalizaciones = hospitalizaciones.filter(clinicaVeterinaria=query_veterinaria)
    
    if query_fecha_entrada:
        # Intentar parsear la fecha
        try:
            # Asumiendo que la fecha viene en formato YYYY-MM-DD
            fecha_parseada = query_fecha_entrada
            hospitalizaciones = hospitalizaciones.filter(fechaEntrada=fecha_parseada)
        except ValueError:
            # Si no se puede parsear, buscar como string
            hospitalizaciones = hospitalizaciones.filter(fechaEntrada__icontains=query_fecha_entrada)
    
    if query_estado:
        hospitalizaciones = hospitalizaciones.filter(estado=query_estado)
    
    # Datos para los filtros
    clinicas = Hospitalizacion.CLINICAS
    estados = Hospitalizacion.ESTADOS
    
    # Determinar si hay filtros activos
    filtros_activos = any([query_cliente, query_mascota, query_veterinaria, query_fecha_entrada, query_estado])
    
    # Obtener el nombre de la clínica seleccionada para mostrar en el mensaje
    clinica_seleccionada = ''
    if query_veterinaria:
        for clinica in clinicas:
            if clinica[0] == query_veterinaria:
                clinica_seleccionada = clinica[1]
                break
    
    # Obtener el nombre del estado seleccionado para mostrar en el mensaje
    estado_seleccionado = ''
    if query_estado:
        for estado in estados:
            if estado[0] == query_estado:
                estado_seleccionado = estado[1]
                break
    
    context = {
        'hospitalizaciones': hospitalizaciones,
        'clinicas': clinicas,
        'estados': estados,
        'query_cliente': query_cliente,
        'query_mascota': query_mascota,
        'query_veterinaria': query_veterinaria,
        'query_fecha_entrada': query_fecha_entrada,
        'query_estado': query_estado,
        'filtros_activos': filtros_activos,
        'clinica_seleccionada': clinica_seleccionada,
        'estado_seleccionado': estado_seleccionado,
    }
    
    return render(request, 'guarderiaHospitalizacion/hospitalizacion/historialHospitalizacion.html', context)


@login_required
def servicio_hospitalizacion_eliminar(request, pk):
    """View to delete an existing pet."""
    hospitalizacion = get_object_or_404(Hospitalizacion, pk=pk)
    hospitalizacion.delete()
    return redirect('historial-hospitalizacion')
