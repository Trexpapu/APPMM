from django import forms
from .models import *
from django import forms
from django.core.exceptions import ValidationError

class DocumentosConsultaForm(forms.ModelForm):
    class Meta:
        model = DocumentosConsulta
        fields = ['archivo', 'descripcion']  # ✅ Agregar archivo aquí
        widgets = {
            'archivo': forms.FileInput(attrs={
                'accept': 'image/*, .pdf, .doc, .docx, .txt'
            }),
            'descripcion': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Describe brevemente el documento',
                'class': 'form-control'
            }),
        }
    labels = {
        'archivo': 'Documento o imagen',
        'descripcion': 'Descripción'
    }

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
                attrs={
                    'type': 'datetime-local', 
                    'placeholder': 'Selecciona la nueva fecha y hora de la consulta',
                    'class': 'form-control'
                },
                format='%Y-%m-%dT%H:%M'  # 🔥 Formato específico para datetime-local
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


# forms.py
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
            'pulso': forms.TextInput(attrs={'placeholder': 'Ej. 100'}),
            'frecuenciaCardiaca': forms.TextInput(attrs={'placeholder': 'Ej. 100 bpm'}),
            'puntuacionCorporal': forms.TextInput(attrs={'placeholder': 'Ej. 5/9'}),
            'peso': forms.NumberInput(attrs={'step': '0.1', 'placeholder': 'Peso en kg'}),
            'vacunas': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Vacunas aplicadas', 'readonly': 'readonly', 'style': 'background-color: #f8f9fa;'}),
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
            'pulso': 'Pulso (LPM)',
            'frecuenciaCardiaca': 'Frecuencia cardíaca',
            'puntuacionCorporal': 'Puntuación corporal',
            'peso': 'Peso (kg)',
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hacer el campo vacunas readonly
        self.fields['vacunas'].widget.attrs['readonly'] = True
        self.fields['vacunas'].widget.attrs['style'] = 'background-color: #f8f9fa;'
        
        # Establecer el veterinario actual como opción por defecto
        from django.contrib.auth import get_user_model
        User = get_user_model()
        self.fields['veterinario'].queryset = User.objects.filter(is_active=True)

class ConsultaMedicaUpdateForm(forms.ModelForm):
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
            'motivoConsulta': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Motivo de la consulta', 'class': 'form-control'}),
            'temperatura': forms.TextInput(attrs={'placeholder': 'Ej. 38.5 °C', 'class': 'form-control'}),
            'pulso': forms.TextInput(attrs={'placeholder': 'Ej. 100', 'class': 'form-control'}),
            'frecuenciaCardiaca': forms.TextInput(attrs={'placeholder': 'Ej. 100 bpm', 'class': 'form-control'}),
            'puntuacionCorporal': forms.TextInput(attrs={'placeholder': 'Ej. 5/9', 'class': 'form-control'}),
            'peso': forms.NumberInput(attrs={'step': '0.01', 'placeholder': 'Peso en kg', 'class': 'form-control'}),
            'vacunas': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Vacunas aplicadas', 'class': 'form-control', 'readonly': 'readonly', 'style': 'background-color: #f8f9fa;'}),
            'alergias': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Alergias conocidas', 'class': 'form-control'}),
            'parasitos': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Parásitos detectados', 'class': 'form-control'}),
            'agua': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Hábitos de consumo de agua', 'class': 'form-control'}),
            'alimento': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Tipo de alimento', 'class': 'form-control'}),
            'condicionesDeHogar': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Condiciones del hogar', 'class': 'form-control'}),
            'ectoparasitos': forms.Textarea(attrs={'rows': 2, 'placeholder': '¿Ha tenido presencia de pulgas o garrapatas?', 'class': 'form-control'}),
            'pronosticoSignos': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Pronóstico y signos clínicos', 'class': 'form-control'}),
            'sintomas': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Síntomas observados', 'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Observaciones del veterinario', 'class': 'form-control'}),
            'diagnosticoDiferencial': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Diagnóstico diferencial', 'class': 'form-control'}),
            'diagnostico': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Diagnóstico final', 'class': 'form-control'}),
            'tratamiento': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Tratamiento prescrito', 'class': 'form-control'}),
            'estudiosHechos': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Estudios realizados', 'class': 'form-control'}),
            'evolucion': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Evolución del paciente', 'class': 'form-control'}),
            'estudiosRecomendados': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Estudios recomendados', 'class': 'form-control'}),
            'clinicaVeterinaria': forms.Select(attrs={'class': 'form-control'}),
            'veterinario': forms.Select(attrs={'class': 'form-control'}),
        }

        labels = {
            'motivoConsulta': 'Motivo de la consulta',
            'temperatura': 'Temperatura',
            'pulso': 'Pulso (LPM)',
            'frecuenciaCardiaca': 'Frecuencia cardíaca',
            'puntuacionCorporal': 'Puntuación corporal',
            'peso': 'Peso (kg)',
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hacer el campo vacunas readonly
        self.fields['vacunas'].widget.attrs['readonly'] = True
        self.fields['vacunas'].widget.attrs['style'] = 'background-color: #f8f9fa;'

class DocumentoConsultaUpdateForm(forms.ModelForm):
    class Meta:
        model = DocumentosConsulta
        fields = ['descripcion']
        widgets = {
            'descripcion': forms.Textarea(attrs={
                'rows': 2,
                'placeholder': 'Descripción del documento',
                'class': 'form-control'
            }),
        }
        labels = {
            'descripcion': 'Descripción'
        }