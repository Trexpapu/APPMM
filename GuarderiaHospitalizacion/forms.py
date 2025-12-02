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
            'estado',
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
            'estado': forms.Select(attrs={
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
            'estado': '📋 Estado',
            'fechaEntrada': '📅 Fecha de Entrada',
            'fechaSalidaProgramada': '📅 Fecha de Salida Programada',
            'fechaSalidaReal': '📅 Fecha de Salida Real',
            'pagado': '💰 Pagado',
            'pagoTotal': '💰 Pago Total',
            'fotoAntes': '🖼️ Foto de Ingreso',
            'fotoDespues': '🖼️ Foto de Egreso',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['mascota'].queryset = Mascotas.objects.all().select_related('cliente')
        # Hacer campos opcionales
        self.fields['fechaSalidaProgramada'].required = False
        self.fields['fechaSalidaReal'].required = False
        self.fields['fotoAntes'].required = False
        self.fields['fotoDespues'].required = False




class GuarderiaUpdateForm(forms.ModelForm):
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
            'estado',
            'fechaEntrada',
            'fechaSalidaProgramada',
            'fechaSalidaReal',
            'pagado',
            'pagoTotal',
            # EXCLUIMOS fotoAntes y fotoDespues del formulario
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
            # REMOVEMOS los widgets de fotoAntes y fotoDespues
            'clinicaVeterinaria': forms.Select(attrs={
                'class': 'form-control'
            }),
            'estado': forms.Select(attrs={
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
            'estado': '📋 Estado',
            'fechaEntrada': '📅 Fecha de Entrada',
            'fechaSalidaProgramada': '📅 Fecha de Salida Programada',
            'fechaSalidaReal': '📅 Fecha de Salida Real',
            'pagado': '💰 Pagado',
            'pagoTotal': '💰 Pago Total',
            # REMOVEMOS las labels de fotoAntes y fotoDespues
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['mascota'].queryset = Mascotas.objects.all().select_related('cliente')
        # Hacer campos opcionales
        self.fields['fechaSalidaProgramada'].required = False
        self.fields['fechaSalidaReal'].required = False
        
        # Si estamos editando, mostrar las fechas actuales formateadas correctamente
        if self.instance and self.instance.fechaEntrada:
            self.initial['fechaEntrada'] = self.instance.fechaEntrada.strftime('%Y-%m-%d')
        
        if self.instance and self.instance.fechaSalidaProgramada:
            self.initial['fechaSalidaProgramada'] = self.instance.fechaSalidaProgramada.strftime('%Y-%m-%d')
            
        if self.instance and self.instance.fechaSalidaReal:
            self.initial['fechaSalidaReal'] = self.instance.fechaSalidaReal.strftime('%Y-%m-%d')



from django import forms
from .models import Hospitalizacion
from ClientesMascotas.models import Mascotas

class HospitalizacionForm(forms.ModelForm):
    class Meta:
        model = Hospitalizacion
        fields = [
            'mascota', 'motivo', 'diagnostico', 'observaciones', 
            'tratamientos', 'evolucion', 'otrosDatos', 'fotoAntes', 
            'fotoDespues', 'clinicaVeterinaria', 'fechaEntrada', 
            'fechaSalida', 'estado', 'pagado', 'pagoTotal'
        ]
        widgets = {
            'mascota': forms.Select(attrs={
                'class': 'form-control',
                'style': 'display: none;'
            }),
            'motivo': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': 'Motivo de la hospitalización...'
            }),
            'diagnostico': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': 'Diagnóstico del paciente...'
            }),
            'observaciones': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': 'Observaciones del paciente durante la hospitalización...'
            }),
            'tratamientos': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': 'Tratamientos aplicados...'
            }),
            'evolucion': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': 'Evolución del paciente...'
            }),
            'otrosDatos': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': 'Otros datos relevantes...'
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
            'fechaEntrada': forms.DateInput(attrs={
                'type': 'date', 
                'class': 'form-control'
            }),
            'fechaSalida': forms.DateInput(attrs={
                'type': 'date', 
                'class': 'form-control'
            }),
            'estado': forms.Select(attrs={
                'class': 'form-control'
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
        }
        labels = {
            'mascota': '🐕 Mascota',
            'motivo': '🏥 Motivo de Hospitalización',
            'diagnostico': '🩺 Diagnóstico',
            'observaciones': '📝 Observaciones',
            'tratamientos': '💊 Tratamientos',
            'evolucion': '📈 Evolución',
            'otrosDatos': '📋 Otros Datos',
            'fotoAntes': '🖼️ Foto al Ingreso',
            'fotoDespues': '🖼️ Foto al Egreso',
            'clinicaVeterinaria': '🏥 Clínica Veterinaria',
            'fechaEntrada': '📅 Fecha de Ingreso',
            'fechaSalida': '📅 Fecha de Salida',
            'estado': '📊 Estado',
            'pagado': '💰 Pagado',
            'pagoTotal': '💰 Pago Total',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['mascota'].queryset = Mascotas.objects.all().select_related('cliente')
        # Hacer campos opcionales
        self.fields['fechaSalida'].required = False
        self.fields['fotoAntes'].required = False
        self.fields['fotoDespues'].required = False


class HospitalizacionUpdateForm(forms.ModelForm):
    class Meta:
        model = Hospitalizacion
        fields = [
            'motivo', 'diagnostico', 'observaciones', 
            'tratamientos', 'evolucion', 'otrosDatos',
            'clinicaVeterinaria', 'fechaEntrada', 
            'fechaSalida', 'estado', 'pagado', 'pagoTotal'
            # EXCLUIMOS fotoAntes y fotoDespues del formulario de actualización
        ]
        widgets = {
            'motivo': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': 'Motivo de la hospitalización...'
            }),
            'diagnostico': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': 'Diagnóstico del paciente...'
            }),
            'observaciones': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': 'Observaciones del paciente durante la hospitalización...'
            }),
            'tratamientos': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': 'Tratamientos aplicados...'
            }),
            'evolucion': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': 'Evolución del paciente...'
            }),
            'otrosDatos': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': 'Otros datos relevantes...'
            }),
            'clinicaVeterinaria': forms.Select(attrs={
                'class': 'form-control'
            }),
            'fechaEntrada': forms.DateInput(attrs={
                'type': 'date', 
                'class': 'form-control'
            }),
            'fechaSalida': forms.DateInput(attrs={
                'type': 'date', 
                'class': 'form-control'
            }),
            'estado': forms.Select(attrs={
                'class': 'form-control'
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
        }
        labels = {
            'motivo': '🏥 Motivo de Hospitalización',
            'diagnostico': '🩺 Diagnóstico',
            'observaciones': '📝 Observaciones',
            'tratamientos': '💊 Tratamientos',
            'evolucion': '📈 Evolución',
            'otrosDatos': '📋 Otros Datos',
            'clinicaVeterinaria': '🏥 Clínica Veterinaria',
            'fechaEntrada': '📅 Fecha de Ingreso',
            'fechaSalida': '📅 Fecha de Salida',
            'estado': '📊 Estado',
            'pagado': '💰 Pagado',
            'pagoTotal': '💰 Pago Total',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hacer campo opcional
        self.fields['fechaSalida'].required = False
        
        # Si estamos editando, mostrar las fechas actuales formateadas correctamente
        if self.instance and self.instance.fechaEntrada:
            self.initial['fechaEntrada'] = self.instance.fechaEntrada.strftime('%Y-%m-%d')
            
        if self.instance and self.instance.fechaSalida:
            self.initial['fechaSalida'] = self.instance.fechaSalida.strftime('%Y-%m-%d')