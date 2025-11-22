from django import forms
from .models import *
from django import forms
from django.core.exceptions import ValidationError

class SiguientesCitasForm(forms.ModelForm):
    class Meta:
        model = SiguientesCitas
        fields = ['fechaSiguienteCita', 'descripcionCita', 'tipoCita', 'asistencia' , 'clinicaVeterinaria', 'veterinario']
        widgets = {
            'fechaSiguienteCita': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'placeholder': 'Selecciona la fecha y hora de la próxima cita'}
            ),
            'descripcionCita': forms.Textarea(
                attrs={'rows': 3, 'placeholder': 'Describe brevemente el motivo de la próxima cita'}
            ),
            'tipoCita': forms.Select(
                attrs={'placeholder': 'Selecciona el tipo de cita'}
            ),
            'asistencia': forms.Select(
                attrs={'placeholder': 'Selecciona el estado de asistencia'}
            ),
            'clinicaVeterinaria': forms.Select(
                attrs={'placeholder': 'Selecciona la clínica veterinaria'}
            ),
            'veterinario': forms.Select(
                attrs={'placeholder': 'Selecciona el veterinario responsable'}
            ),
        }
        labels = {
            'fechaSiguienteCita': 'Fecha de la siguiente cita',
            'descripcionCita': 'Motivo de la siguiente cita',
            'tipoCita': 'Tipo de cita',
            'asistencia' : 'Asistencia del paciente',
            'clinicaVeterinaria': 'Clínica veterinaria',
            'veterinario': 'Veterinario responsable',
        }

    def clean(self):
        cleaned_data = super().clean()
        fecha = cleaned_data.get('fechaSiguienteCita')
        veterinario = cleaned_data.get('veterinario')

        if fecha and veterinario:
            # Verificar si ya hay una cita con el mismo veterinario en esa fecha y hora exacta
            existe = SiguientesCitas.objects.filter(
                fechaSiguienteCita=fecha,
                veterinario=veterinario
            ).exists()

            if existe:
                raise ValidationError("⚠️ El veterinario se encuentra ocupado en esa fecha y hora.")

        return cleaned_data


class UpdateSiguienteCitaForm(forms.ModelForm):
    class Meta:
        model = SiguientesCitas
        fields = ['fechaSiguienteCita', 'descripcionCita', 'tipoCita','asistencia', 'clinicaVeterinaria', 'veterinario']
        widgets = {

            'fechaSiguienteCita': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local', 
                    'placeholder': 'Selecciona la nueva fecha y hora de la cita',
                    'class': 'form-control'
                },
                format='%Y-%m-%dT%H:%M'  # 🔥 Formato específico para datetime-local
            ),

            'descripcionCita': forms.Textarea(
                attrs={'rows': 3, 'placeholder': 'Actualiza el motivo o notas de la próxima cita'}
            ),
            'tipoCita': forms.Select(
                attrs={'placeholder': 'Selecciona el tipo de cita'}
            ),
            'asistencia': forms.Select(
                attrs={'placeholder': 'Selecciona el estado de asistencia'}
            ),
            'clinicaVeterinaria': forms.Select(
                attrs={'placeholder': 'Selecciona la clínica veterinaria'}
            ),
            'veterinario': forms.Select(
                attrs={'placeholder': 'Selecciona el veterinario responsable'}
            ),
        }
        labels = {
            'fechaSiguienteCita': 'Fecha de la siguiente cita',
            'descripcionCita': 'Motivo de la siguiente cita',
            'tipoCita': 'Tipo de cita',
            'asistencia' : 'Asistencia del paciente',
            'clinicaVeterinaria': 'Clínica veterinaria',
            'veterinario': 'Veterinario responsable',
        }

    def clean(self):
        cleaned_data = super().clean()
        fecha = cleaned_data.get('fechaSiguienteCita')
        veterinario = cleaned_data.get('veterinario')

        if fecha and veterinario:
            existe = SiguientesCitas.objects.filter(
                fechaSiguienteCita=fecha,
                veterinario=veterinario
            ).exclude(id=self.instance.id).exists()

            if existe:
                raise ValidationError("⚠️ El veterinario ya se encuentra ocupado en esa fecha y hora.")

        return cleaned_data
