from django import forms
from .models import *
from django import forms
from django.core.exceptions import ValidationError
from .models import SiguientesConsultas

from django import forms
from django.core.exceptions import ValidationError
from .models import SiguientesConsultas


class SiguienteConsultaForm(forms.ModelForm):
    class Meta:
        model = SiguientesConsultas
        fields = ['fechaSiguienteConsulta', 'motivoSiguienteConsulta', 'clinicaVeterinaria', 'veterinario']
        widgets = {
            'fechaSiguienteConsulta': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'placeholder': 'Selecciona la fecha y hora de la próxima consulta'}
            ),
            'motivoSiguienteConsulta': forms.Textarea(
                attrs={'rows': 3, 'placeholder': 'Describe brevemente el motivo de la próxima consulta'}
            ),
            'clinicaVeterinaria': forms.Select(
                attrs={'placeholder': 'Selecciona la clínica veterinaria'}
            ),
            'veterinario': forms.Select(
                attrs={'placeholder': 'Selecciona el veterinario responsable'}
            ),
        }
        labels = {
            'fechaSiguienteConsulta': 'Fecha de la siguiente consulta',
            'motivoSiguienteConsulta': 'Motivo de la siguiente consulta',
            'clinicaVeterinaria': 'Clínica veterinaria',
            'veterinario': 'Veterinario responsable',
        }

    def clean(self):
        cleaned_data = super().clean()
        fecha = cleaned_data.get('fechaSiguienteConsulta')
        veterinario = cleaned_data.get('veterinario')

        if fecha and veterinario:
            # Verificar si ya hay una cita con el mismo veterinario en esa fecha y hora exacta
            existe = SiguientesConsultas.objects.filter(
                fechaSiguienteConsulta=fecha,
                veterinario=veterinario
            ).exists()

            if existe:
                raise ValidationError("⚠️ El veterinario ya tiene una cita agendada en esa fecha y hora.")

        return cleaned_data


class UpdateSiguienteConsultaForm(forms.ModelForm):
    class Meta:
        model = SiguientesConsultas
        fields = ['fechaSiguienteConsulta', 'motivoSiguienteConsulta', 'clinicaVeterinaria', 'veterinario']
        widgets = {
            'fechaSiguienteConsulta': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'placeholder': 'Selecciona la nueva fecha y hora de la consulta'}
            ),
            'motivoSiguienteConsulta': forms.Textarea(
                attrs={'rows': 3, 'placeholder': 'Actualiza el motivo o notas de la próxima consulta'}
            ),
            'clinicaVeterinaria': forms.Select(
                attrs={'placeholder': 'Selecciona la clínica veterinaria'}
            ),
            'veterinario': forms.Select(
                attrs={'placeholder': 'Selecciona el veterinario responsable'}
            ),
        }
        labels = {
            'fechaSiguienteConsulta': 'Fecha de la siguiente consulta',
            'motivoSiguienteConsulta': 'Motivo de la siguiente consulta',
            'clinicaVeterinaria': 'Clínica veterinaria',
            'veterinario': 'Veterinario responsable',
        }

    def clean(self):
        cleaned_data = super().clean()
        fecha = cleaned_data.get('fechaSiguienteConsulta')
        veterinario = cleaned_data.get('veterinario')

        if fecha and veterinario:
            existe = SiguientesConsultas.objects.filter(
                fechaSiguienteConsulta=fecha,
                veterinario=veterinario
            ).exclude(id=self.instance.id).exists()

            if existe:
                raise ValidationError("⚠️ El veterinario ya tiene otra cita agendada en esa fecha y hora.")

        return cleaned_data



class ConsultaMedicaForm(forms.ModelForm):
    class Meta:
        model = ConsultasMedicas
        fields = [
            'motivoConsulta',
            'temperatura',
            'pulso',
            'frecuenciaCardiaca',
            'puntuacionCorporal',
            'peso',
            'vacunas',
            'alergias',
            'parasitos',
            'agua',
            'alimento',
            'condicionesDeHogar',
            'ectoparasitos',
            'estudiosHechos',
            'pronosticoSignos',
            'sintomas',
            'observaciones',
            'diagnosticoDiferencial',
            'diagnostico',
            'tratamiento',
            'estudiosRecomendados',
            'evolucion',
            'clinicaVeterinaria',
            'veterinario',
        ]

        widgets = {
            'motivoConsulta': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Motivo de la consulta'}),
            'temperatura': forms.TextInput(attrs={'placeholder': 'Ej. 38.5 °C'}),
            'pulso': forms.TextInput(attrs={'placeholder': 'Ej. 90 bpm'}),
            'frecuenciaCardiaca': forms.TextInput(attrs={'placeholder': 'Ej. 100 bpm'}),
            'puntuacionCorporal': forms.TextInput(attrs={'placeholder': 'Ej. 5/9'}),
            'peso': forms.NumberInput(attrs={'step': '0.01', 'placeholder': 'Peso en gr'}),
            'vacunas': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Vacunas aplicadas'}),
            'alergias': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Alergias conocidas'}),
            'parasitos': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Parásitos detectados'}),
            'agua': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Hábitos de consumo de agua'}),
            'alimento': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Tipo de alimento'}),
            'condicionesDeHogar': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Condiciones del hogar'}),
            'ectoparasitos': forms.Textarea(attrs={'rows': 2, 'placeholder': '¿Ha tenido presencia de pulgas o garrapatas?'}),
            'pronosticoSignos': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Pronóstico y signos clínicos'}),
            'sintomas': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Síntomas observados'}),
            'observaciones': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Observaciones del veterinario'}),
            'diagnosticoDiferencial': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Diagnóstico diferencial'}),
            'diagnostico': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Diagnóstico final'}),
            'tratamiento': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Tratamiento prescrito'}),
            'estudiosHechos': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Estudios realizados'}),
            'evolucion': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Evolución del paciente'}),
            'estudiosRecomendados': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Estudios recomendados'}),
            'clinicaVeterinaria': forms.Select(),
            'veterinario': forms.Select(),
        }

        labels = {
            'motivoConsulta': 'Motivo de la consulta',
            'temperatura': 'Temperatura',
            'pulso': 'Pulso',
            'frecuenciaCardiaca': 'Frecuencia cardíaca',
            'puntuacionCorporal': 'Puntuación corporal',
            'peso': 'Peso (gr)',
            'vacunas': 'Vacunas',
            'alergias': 'Alergias',
            'parasitos': 'Parásitos',
            'agua': 'Consumo de agua',
            'alimento': 'Alimento',
            'condicionesDeHogar': 'Condiciones del hogar',
            'ectoparasitos': 'Ectoparásitos',
            'pronosticoSignos': 'Pronóstico y signos clínicos',
            'sintomas': 'Síntomas',
            'observaciones': 'Observaciones',
            'diagnosticoDiferencial': 'Diagnóstico diferencial',
            'diagnostico': 'Diagnóstico final',
            'tratamiento': 'Tratamiento',
            'estudiosHechos': 'Estudios realizados',
            'estudiosRecomendados': 'Estudios recomendados',
            'evolucion': 'Evolución del paciente',
            'clinicaVeterinaria': 'Clínica veterinaria',
            'veterinario': 'Médico veterinario',
        }