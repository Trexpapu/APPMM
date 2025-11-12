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
    """View to add a new medical consultation and optionally load last consultation data."""
    mascotas = Mascotas.objects.all()
    mascota_id = request.GET.get('mascota') or request.POST.get('mascota')
    cargar_prev = request.GET.get('cargar_prev')  # bandera para cargar la última consulta

    initial_data = {}
    mascota = None

    # 🔹 Si se seleccionó una mascota
    if mascota_id:
        try:
            mascota = Mascotas.objects.get(pk=mascota_id)
        except Mascotas.DoesNotExist:
            mascota = None

        if mascota:
            if cargar_prev == "1":
                # ✅ Cargar datos de la última consulta (excepto peso, vacunas, alergias)
                ultima_consulta = (
                    ConsultasMedicas.objects.filter(mascota_id=mascota_id)
                    .order_by('-fechaConsulta')
                    .first()
                )
                if ultima_consulta:
                    print(mascota_id)
                    exclude_fields = ['id', 'fechaConsulta', 'peso', 'vacunas', 'alergias', 'mascota']
                    for field in ConsultasMedicas._meta.get_fields():
                        if field.name not in exclude_fields and hasattr(ultima_consulta, field.name):
                            initial_data[field.name] = getattr(ultima_consulta, field.name)
                    messages.info(request, "Se cargaron los datos de la última consulta.")

                # ✅ También llenar los datos actuales de la mascota
                initial_data.update({
                    'peso': mascota.peso,
                    'vacunas': mascota.vacunas,
                    'alergias': mascota.alergias,
                })
            else:
                # ❌ No se cargaron datos previos, llenar con los datos actuales de la mascota
                initial_data.update({
                    'peso': mascota.peso,
                    'vacunas': mascota.vacunas,
                    'alergias': mascota.alergias,
                })

    # 🔹 POST: Guardar nueva consulta
    if request.method == 'POST':
        form = ConsultaMedicaForm(request.POST, initial=initial_data)
        documentos_form = DocumentosConsultaForm(request.POST, request.FILES)

        if form.is_valid():
            nConsulta = form.save(commit=False)
            mascota_id = request.POST.get('mascota')

            if mascota_id:
                nConsulta.mascota_id = mascota_id
                nConsulta.save()

                # 🐾 Actualizar datos de la mascota
                mascota = Mascotas.objects.get(pk=mascota_id)
                mascota.peso = form.cleaned_data.get('peso') or mascota.peso
                mascota.vacunas = form.cleaned_data.get('vacunas') or mascota.vacunas
                mascota.alergias = form.cleaned_data.get('alergias') or mascota.alergias
                mascota.save()

                # 📎 Guardar múltiples imágenes
                archivos = request.FILES.getlist('archivo')
                descripcion = request.POST.get('descripcion', '')
                for arch in archivos:
                    DocumentosConsulta.objects.create(
                        consulta=nConsulta,
                        archivo=arch,
                        descripcion=descripcion
                    )

                messages.success(request, "Consulta médica y documentos guardados correctamente.")
                return redirect('index-consultas')
            else:
                form.add_error(None, "Debe seleccionar una mascota antes de guardar.")
    else:
        form = ConsultaMedicaForm(initial=initial_data)
        documentos_form = DocumentosConsultaForm()

    # 🔹 Mostrar pregunta si hay consultas previas
    mostrar_pregunta = False
    if mascota_id:
        print(cargar_prev)
        hay_consulta_previa = ConsultasMedicas.objects.filter(mascota_id=mascota_id).exists()
        mostrar_pregunta = hay_consulta_previa and not cargar_prev

    return render(
        request,
        'consultasMedicas/consultasMedicasBase/nuevaConsulta.html',
        {
            'form': form,
            'documentos_form': documentos_form,
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