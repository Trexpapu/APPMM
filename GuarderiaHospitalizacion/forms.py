from django import forms
from .models import *
from ClientesMascotas.models import Mascotas
from django.contrib.auth.models import User



class GuarderiaForm(forms.ModelForm):
    class Meta:
        model = Guarderia
        fields = [
            'mascota',
            'alimento',
            'accesoriosRecibidos',
            'estadoSalud',
            'tratamientos',
            'otrosDatos',
            'clinicaVeterinaria',
            'fechaEntrada',
            'fechaSalidaProgramada',
            'fechaSalidaReal',
            'pagado',
            'pagoTotal',
            'fotoAntes',
            'fotoDespues',
        ]
        widgets = {
            'fechaEntrada': forms.DateInput(attrs={
                'type': 'date', 
                'class': 'form-control'
            }),
            'fechaSalidaProgramada': forms.DateInput(attrs={
                'type': 'date', 
                'class': 'form-control'
            }),
            'fechaSalidaReal': forms.DateInput(attrs={
                'type': 'date', 
                'class': 'form-control'
            }),
            'alimento': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': 'Descripción del alimento proporcionado...'
            }),
            'accesoriosRecibidos': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': 'Accesorios recibidos con la mascota...'
            }),
            'estadoSalud': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': 'Estado de salud al ingreso...'
            }),
            'tratamientos': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': 'Tratamientos médicos aplicados...'
            }),
            'otrosDatos': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': 'Otros datos relevantes...'
            }),
            'pagado': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': '0.00'
            }),
            'pagoTotal': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': '0.00'
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
                'style': 'display: none;'
            }),
        }
        labels = {
            'mascota': '🐕 Mascota',
            'alimento': '🍖 Alimento',
            'accesoriosRecibidos': '🎒 Accesorios Recibidos',
            'estadoSalud': '💓 Estado de Salud',
            'tratamientos': '💊 Tratamientos',
            'otrosDatos': '📝 Otros Datos',
            'clinicaVeterinaria': '🏥 Clínica Veterinaria',
            'fechaEntrada': '📅 Fecha de Entrada',
            'fechaSalidaProgramada': '📅 Fecha de Salida Programada',
            'fechaSalidaReal': '📅 Fecha de Salida Real',
            'pagado': '💰 Pagado',
            'pagoTotal': '💰 Pago Total',
            'fotoAntes': '🖼️ Foto Antes',
            'fotoDespues': '🖼️ Foto Después',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['mascota'].queryset = Mascotas.objects.all().select_related('cliente')
        # Hacer campos opcionales
        self.fields['fechaSalidaProgramada'].required = False
        self.fields['fechaSalidaReal'].required = False
        self.fields['fotoAntes'].required = False
        self.fields['fotoDespues'].required = False