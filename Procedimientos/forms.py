from django import forms
from .models import *
from ClientesMascotas.models import Mascotas
from django.contrib.auth.models import User


class DesparasitacionesUpdateForm(forms.ModelForm):
    class Meta:
        model = Desparasitaciones
        fields = [
            'mascota',
            'peso',
            'desparasitante',
            'fecha',
            'veterinario',
            'clinicaVeterinaria',
        ]
        widgets = {
            'fecha': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'clinicaVeterinaria': forms.Select(attrs={
                'class': 'form-control'
            }),
            'mascota': forms.Select(attrs={
                'class': 'form-control'
            }),
            'desparasitante': forms.Select(attrs={
                'class': 'form-control'
            }),
            'veterinario': forms.Select(attrs={
                'class': 'form-control'
            }),
            'peso': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Peso de la mascota en kg'
            }),
        }
        labels = {
            'mascota': '🐕 Mascota',
            'peso': '⚖️ Peso (kg)',
            'desparasitante': '🪱 Desparasitante',
            'fecha': '📅 Fecha de Desparasitación',
            'veterinario': '👨‍⚕️ Veterinario',
            'clinicaVeterinaria': '🏥 Clínica Veterinaria',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Formatear la fecha para el input type="date"
        if self.instance and self.instance.fecha:
            self.initial['fecha'] = self.instance.fecha.strftime('%Y-%m-%d')

class DesparasitacionesForm(forms.ModelForm):
    class Meta:
        model = Desparasitaciones
        fields = [
            'mascota',
            'peso',
            'desparasitante',
            'fecha',
            'veterinario',
            'clinicaVeterinaria',
        ]
        widgets = {
            'fecha': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'clinicaVeterinaria': forms.Select(attrs={
                'class': 'form-control'
            }),
            'mascota': forms.Select(attrs={
                'class': 'form-control'
            }),
            'desparasitante': forms.Select(attrs={
                'class': 'form-control'
            }),
            'veterinario': forms.Select(attrs={
                'class': 'form-control'
            }),
            'peso': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Peso de la mascota en kg'
            }),
        }
        labels = {
            'mascota': '🐕 Mascota',
            'peso': '⚖️ Peso (kg)',
            'desparasitante': '🪱 Desparasitante',
            'fecha': '📅 Fecha de Desparasitación',
            'veterinario': '👨‍⚕️ Veterinario',
            'clinicaVeterinaria': '🏥 Clínica Veterinaria',
        }


class ListaDesparasitantesForm(forms.ModelForm):
    class Meta:
        model = ListaDesparasitantes
        fields = ['desparasitante']
        widgets = {
            'desparasitante': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del desparasitante'
            }),
        }
        labels = {
            'desparasitante': '🪱 Desparasitante',
        }
class ListaDesparasitantesUpdateForm(forms.ModelForm):
    class Meta:
        model = ListaDesparasitantes
        fields = ['desparasitante']
        widgets = {
            'desparasitante': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del desparasitante'
            }),
        }
        labels = {
            'desparasitante': '🪱 Desparasitante',
        }

class VacunacionesUpdateForm(forms.ModelForm):
    class Meta:
        model = Vacunaciones
        fields = [
            'mascota',
            'vacunas',
            'descripcion',
            'veterinario',
            'clinicaVeterinaria',
            'fecha',
        ]
        widgets = {
            'fecha': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'descripcion': forms.Textarea(attrs={
                'rows': 4,
                'class': 'form-control',
                'placeholder': 'Descripción de la vacunación'
            }),
            'clinicaVeterinaria': forms.Select(attrs={
                'class': 'form-control'
            }),
            'mascota': forms.Select(attrs={
                'class': 'form-control'
            }),
            'vacunas': forms.Select(attrs={
                'class': 'form-control'
            }),
            'veterinario': forms.Select(attrs={
                'class': 'form-control'
            }),
        }
        labels = {
            'mascota': '🐕 Mascota',
            'vacunas': '💉 Vacuna',
            'descripcion': '📝 Descripción',
            'veterinario': '👨‍⚕️ Veterinario',
            'clinicaVeterinaria': '🏥 Clínica Veterinaria',
            'fecha': '📅 Fecha de Vacunación',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Formatear la fecha para el input type="date"
        if self.instance and self.instance.fecha:
            self.initial['fecha'] = self.instance.fecha.strftime('%Y-%m-%d')


class VacunacionesForm(forms.ModelForm):
    class Meta:
        model = Vacunaciones
        fields = [
            'mascota',
            'vacunas',
            'descripcion',
            'veterinario',
            'clinicaVeterinaria',
            'fecha',
        ]
        widgets = {
            'fecha': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'descripcion': forms.Textarea(attrs={
                'rows': 4,
                'class': 'form-control',
                'placeholder': 'Descripción de la vacunación'
            }),
            'clinicaVeterinaria': forms.Select(attrs={
                'class': 'form-control'
            }),
            'mascota': forms.Select(attrs={
                'class': 'form-control'
            }),
            'vacunas': forms.Select(attrs={
                'class': 'form-control'
            }),
            'veterinario': forms.Select(attrs={
                'class': 'form-control'
            }),
        }
        labels = {
            'mascota': '🐕 Mascota',
            'vacunas': '💉 Vacuna',
            'descripcion': '📝 Descripción',
            'veterinario': '👨‍⚕️ Veterinario',
            'clinicaVeterinaria': '🏥 Clínica Veterinaria',
            'fecha': '📅 Fecha de Vacunación',
        }

class ListaVacunasForm(forms.ModelForm):
    class Meta:
        model = ListaVacunas
        fields = ['vacuna']
        widgets = {
            'vacuna': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de la vacuna'
            }),
        }
        labels = {
            'vacuna': '💉 Vacuna',
        }

# Puedes usar el mismo form para editar o crear uno específico si necesitas diferencias
class ListaVacunasUpdateForm(forms.ModelForm):
    class Meta:
        model = ListaVacunas
        fields = ['vacuna']
        widgets = {
            'vacuna': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de la vacuna'
            }),
        }
        labels = {
            'vacuna': '💉 Vacuna',
        }


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
            'peso',
            'estadoSaludPrevio',
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
            'peso': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': 'Peso de la mascota en kg'
            }),
            'estadoSaludPrevio': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': 'Estado de salud previo a la operación'
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
            'fechaEntrada': '📅 Fecha y Hora de Inicio de la Operación',
            'fechaSalida': '📅 Fecha y Hora de Fin de la Operación',
            'operacion': '🩺 Tipo de Operación',
            'descripcion': '📝 Descripción de la Operación',
            'peso': '⚖️ Peso (kg)',
            'estadoSaludPrevio': '💓 Estado de Salud Previo a la Operación',
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



class OperacionesUpdateForm(forms.ModelForm):
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
            'peso',
            'estadoSaludPrevio',
            'complicaciones',
            'clinicaVeterinaria',
            # EXCLUIMOS fotoAntes y fotoDespues del formulario
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
            
            'peso': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': 'Peso de la mascota en kg'
            }),
            'estadoSaludPrevio': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': 'Estado de salud previo a la operación'
            }),
            'complicaciones': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': 'Complicaciones durante o después de la operación'
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
            'fechaEntrada': '📅 Fecha y Hora de Inicio de la Operación',
            'fechaSalida': '📅 Fecha y Hora de Fin de la Operación',
            'operacion': '🩺 Tipo de Operación',
            'descripcion': '📝 Descripción de la Operación',
            'peso': '⚖️ Peso (kg)',
            'estadoSaludPrevio': '💓 Estado de Salud Previo a la Operación',
            'complicaciones': '⚠️ Complicaciones',
            'clinicaVeterinaria': '🏥 Clínica Veterinaria',
            'mascota': '🐕 Mascota',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['mascota'].queryset = Mascotas.objects.all().select_related('cliente')
        
        # Hacer campos opcionales
        self.fields['fechaSalida'].required = False
        
        # Ordenar veterinarios por nombre
        self.fields['veterinario'].queryset = User.objects.filter(is_active=True).order_by('first_name', 'last_name')
        
        # Formatear fechas para el input datetime-local
        if self.instance and self.instance.fechaEntrada:
            self.initial['fechaEntrada'] = self.instance.fechaEntrada.strftime('%Y-%m-%dT%H:%M')
        
        if self.instance and self.instance.fechaSalida:
            self.initial['fechaSalida'] = self.instance.fechaSalida.strftime('%Y-%m-%dT%H:%M')