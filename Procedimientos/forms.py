from django import forms
from .models import Operaciones
from ClientesMascotas.models import Mascotas
from django.contrib.auth.models import User

class OperacionesForm(forms.ModelForm):
    veterinario = forms.ModelChoiceField(
        queryset=User.objects.filter(is_active=True),
        required=True,
        label="👨‍⚕️ Veterinario",
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    class Meta:
        model = Operaciones
        fields = [
            'mascota',
            'veterinario',
            'fechaEntrada',
            'fechaSalida',
            'operacion',
            'descripcion',
            'complicaciones',
            'fotoAntes',
            'fotoDespues',
            'clinicaVeterinaria',
        ]
        widgets = {
            'fechaEntrada': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }),
            'fechaSalida': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }),
            'operacion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tipo de operación realizada'
            }),
            'descripcion': forms.Textarea(attrs={
                'rows': 4,
                'class': 'form-control',
                'placeholder': 'Descripción detallada de la operación'
            }),
            'complicaciones': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': 'Complicaciones durante o después de la operación'
            }),
            'fotoAntes': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'fotoDespues': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'clinicaVeterinaria': forms.Select(attrs={
                'class': 'form-control'
            }),
            'mascota': forms.Select(attrs={
                'class': 'form-control',
                'style': 'display: none;'  # Ocultamos el select original
            }),
        }
        labels = {
            'fechaEntrada': '📅 Fecha y Hora de Entrada',
            'fechaSalida': '📅 Fecha y Hora de Salida',
            'operacion': '🩺 Tipo de Operación',
            'descripcion': '📝 Descripción de la Operación',
            'complicaciones': '⚠️ Complicaciones',
            'fotoAntes': '🖼️ Foto Antes de la Operación',
            'fotoDespues': '🖼️ Foto Después de la Operación',
            'clinicaVeterinaria': '🏥 Clínica Veterinaria',
            'mascota': '🐕 Mascota',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['mascota'].queryset = Mascotas.objects.all().select_related('cliente')
        # Hacer campos opcionales
        self.fields['fechaSalida'].required = False
        self.fields['fotoAntes'].required = False
        self.fields['fotoDespues'].required = False
        
        # Ordenar veterinarios por nombre
        self.fields['veterinario'].queryset = User.objects.filter(is_active=True).order_by('first_name', 'last_name')