from django.shortcuts import render
from .models import *
from ClientesMascotas.models import *
from .forms import *
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from Procedimientos.views import encode_image_to_base64
# Create your views here.
@login_required
def index_guarderia_hospitalizacion(request):
    return render(request, 'guarderiaHospitalizacion/indexGuarderiaHospitalizacion.html')

@login_required
def servicio_guarderia_crear(request):
    mascotas = Mascotas.objects.all().select_related('cliente')
    
    if request.method == 'POST':
        form = GuarderiaForm(request.POST, request.FILES)
        if form.is_valid():
            guarderia = form.save(commit=False)
            
            # Procesar imágenes
            if 'fotoAntes' in request.FILES:
                guarderia.fotoAntes = encode_image_to_base64(request.FILES['fotoAntes'])
            if 'fotoDespues' in request.FILES:
                guarderia.fotoDespues = encode_image_to_base64(request.FILES['fotoDespues'])
            
            guarderia.save()
            messages.success(request, "Servicio de guardería registrado correctamente.")
            return redirect('index-procedimientos')
    else:
        form = GuarderiaForm()
    
    return render(request, 'guarderiaHospitalizacion/guarderia/nuevoServicio.html', {
        'form': form,
        'mascotas': mascotas,
        'title': 'Nuevo Servicio de Guardería'
    })