from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from ClientesMascotas.models import *
from django.utils.dateparse import parse_date
from datetime import datetime

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
    """View to add a next consultation."""
    mascotas = Mascotas.objects.all()

    if request.method == 'POST':
        form = ConsultaMedicaForm(request.POST)
        if form.is_valid():
            nConsulta = form.save(commit=False)
            mascota_id = request.POST.get('mascota')
            if mascota_id:
                nConsulta.mascota_id = mascota_id
                nConsulta.save()
                return redirect('index-consultas')
            else:
                form.add_error(None, "Debe seleccionar una mascota antes de guardar.")
    else:
        form = ConsultaMedicaForm()
 
    return render(request, 'consultasMedicas/consultasMedicasBase/nuevaConsulta.html', {'form': form, 'mascotas': mascotas})

