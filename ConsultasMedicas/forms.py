from django import forms
from .models import *
from django.core.exceptions import ValidationError

class DocumentosConsultaForm(forms.ModelForm):
    class Meta:
        model = DocumentosConsulta
        fields = ['archivo', 'descripcion']
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
            'archivo': '📄 Documento o imagen',
            'descripcion': '📝 Descripción'
        }


class ConsultaMedicaForm(forms.ModelForm):
    class Meta:
        model = ConsultasMedicas
        fields = [
            # SECCIÓN 1: INFORMACIÓN GENERAL Y PROCEDIMIENTO
            'procedimiento',
            'clinicaVeterinaria',
            'veterinario',
            
            # SECCIÓN 2: ANAMNESIS E HISTORIAL
            'anamnesicos',
            
            # SECCIÓN 3: EXAMEN FÍSICO GENERAL
            'mucosas',
            'porcentajeHidratacion',
            'temperatura',
            'pulso',
            'frecuenciaCardiaca',
            'frecuenciaRespiratoria',
            'peso',
            'puntuacionCorporal',
            
            # SECCIÓN 4: COMPORTAMIENTO Y ACTITUD
            'actitudConPropietario',
            'actitudConVeterinario',
            
            # SECCIÓN 5: HISTORIAL MÉDICO PREVIO
            'vacunas',
            'alergias',
            'ultimaDesparasitacion',
            'ultimoDesparasitante',
            'alimento',
            'parasitos',
            'ectoparasitos',
            
            # SECCIÓN 6: EXAMEN FÍSICO ESPECÍFICO
            'examanesFisicosRealizados',
            
            # SECCIÓN 7: DIAGNÓSTICO
            'listaPosiblesProblemas',
            'listaProblemasReales',
            'diagnostico',
            'pronostico',
            
            # SECCIÓN 8: TRATAMIENTO Y SEGUIMIENTO
            'tratamiento',
            'estudiosHechos',
            'estudiosRecomendados',
            'evolucion',
            'observaciones',
        ]

        widgets = {
            # SECCIÓN 1
            'procedimiento': forms.Select(attrs={'class': 'form-control'}),
            'clinicaVeterinaria': forms.Select(attrs={'class': 'form-control'}),
            'veterinario': forms.Select(attrs={'class': 'form-control'}),
            
            # SECCIÓN 2: ANAMNESIS
            'anamnesicos': forms.Textarea(attrs={
                'rows': 4, 
                'placeholder': 'Motivo de consulta, problema actual, dieta, enfermedades previas, cirugías, tratamientos recientes, convivencia con otros animales, viajes...',
                'class': 'form-control'
            }),
            
            # SECCIÓN 3: EXAMEN FÍSICO GENERAL
            'mucosas': forms.Select(attrs={'class': 'form-control'}),
            'porcentajeHidratacion': forms.TextInput(attrs={
                'placeholder': 'Ej. 5-7% (ligera deshidratación)',
                'class': 'form-control'
            }),
            'temperatura': forms.TextInput(attrs={
                'placeholder': 'Ej. 38.5 °C',
                'class': 'form-control'
            }),
            'pulso': forms.TextInput(attrs={
                'placeholder': 'Ej. 120 lpm',
                'class': 'form-control'
            }),
            'frecuenciaCardiaca': forms.TextInput(attrs={
                'placeholder': 'Ej. 140 bpm',
                'class': 'form-control'
            }),
            'frecuenciaRespiratoria': forms.TextInput(attrs={
                'placeholder': 'Ej. 30 rpm',
                'class': 'form-control'
            }),
            'peso': forms.NumberInput(attrs={
                'step': '0.01', 
                'placeholder': 'Peso en kg',
                'class': 'form-control'
            }),
            'puntuacionCorporal': forms.Select(attrs={'class': 'form-control'}),
            
            # SECCIÓN 4: COMPORTAMIENTO
            'actitudConPropietario': forms.Textarea(attrs={
                'rows': 2,
                'placeholder': 'Comportamiento con el propietario',
                'class': 'form-control'
            }),
            'actitudConVeterinario': forms.Textarea(attrs={
                'rows': 2,
                'placeholder': 'Comportamiento durante el examen',
                'class': 'form-control'
            }),
            
            # SECCIÓN 5: HISTORIAL MÉDICO
            'vacunas': forms.Textarea(attrs={
                'rows': 2,
                'placeholder': 'Vacunas aplicadas',
                'class': 'form-control',
                'readonly': 'readonly',
                'style': 'background-color: #f8f9fa;'
            }),
            'alergias': forms.Textarea(attrs={
                'rows': 2,
                'placeholder': 'Alergias conocidas',
                'class': 'form-control'
            }),
            'ultimaDesparasitacion': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'readonly': 'readonly',
                'style': 'background-color: #f8f9fa;'
            }),
            'ultimoDesparasitante': forms.Textarea(attrs={
                'rows': 2,
                'placeholder': 'Último desparasitante aplicado',
                'class': 'form-control',
                'readonly': 'readonly',
                'style': 'background-color: #f8f9fa;'
            }),
            'alimento': forms.Textarea(attrs={
                'rows': 2,
                'placeholder': 'Tipo y cantidad de alimento',
                'class': 'form-control'
            }),
            'parasitos': forms.Textarea(attrs={
                'rows': 2,
                'placeholder': 'Parásitos detectados',
                'class': 'form-control'
            }),
            'ectoparasitos': forms.Textarea(attrs={
                'rows': 2,
                'placeholder': 'Presencia de pulgas, garrapatas, etc.',
                'class': 'form-control'
            }),
            
            # SECCIÓN 6: EXAMEN FÍSICO ESPECÍFICO
            'examanesFisicosRealizados': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Exámenes físicos realizados y hallazgos',
                'class': 'form-control'
            }),
            
            # SECCIÓN 7: DIAGNÓSTICO
            'listaPosiblesProblemas': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Lista de posibles problemas (diagnóstico diferencial)',
                'class': 'form-control'
            }),
            'listaProblemasReales': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Lista de problemas reales identificados',
                'class': 'form-control'
            }),
            'diagnostico': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Diagnóstico final',
                'class': 'form-control'
            }),
            'pronostico': forms.Textarea(attrs={
                'rows': 2,
                'placeholder': 'Pronóstico del caso',
                'class': 'form-control'
            }),
            
            # SECCIÓN 8: TRATAMIENTO Y SEGUIMIENTO
            'tratamiento': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Tratamiento prescrito, medicamentos, dosis, frecuencia...',
                'class': 'form-control'
            }),
            'estudiosHechos': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Estudios de laboratorio o imagen realizados',
                'class': 'form-control'
            }),
            'estudiosRecomendados': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Estudios recomendados para seguimiento',
                'class': 'form-control'
            }),
            'evolucion': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Evolución del paciente durante la consulta',
                'class': 'form-control'
            }),
            'observaciones': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Observaciones adicionales',
                'class': 'form-control'
            }),
        }

        labels = {
            # SECCIÓN 1
            'procedimiento': '🩺 Tipo de Procedimiento',
            'clinicaVeterinaria': '🏥 Clínica Veterinaria',
            'veterinario': '👨‍⚕️ Médico Veterinario',
            
            # SECCIÓN 2: ANAMNESIS
            'anamnesicos': '📋 Anamnesis',
            
            # SECCIÓN 3: EXAMEN FÍSICO GENERAL
            'mucosas': '👄 Mucosas',
            'porcentajeHidratacion': '💧 Porcentaje de Hidratación',
            'temperatura': '🌡️ Temperatura',
            'pulso': '💓 Pulso (LPM)',
            'frecuenciaCardiaca': '❤️ Frecuencia Cardíaca',
            'frecuenciaRespiratoria': '🌬️ Frecuencia Respiratoria',
            'peso': '⚖️ Peso (kg)',
            'puntuacionCorporal': '📊 Puntuación Corporal',
            
            # SECCIÓN 4: COMPORTAMIENTO
            'actitudConPropietario': '👤 Actitud con el Propietario',
            'actitudConVeterinario': '👨‍⚕️ Actitud con el Veterinario',
            
            # SECCIÓN 5: HISTORIAL MÉDICO
            'vacunas': '💉 Vacunas',
            'alergias': '🤧 Alergias',
            'ultimaDesparasitacion': '📅 Última Desparasitación',
            'ultimoDesparasitante': '💊 Último Desparasitante',
            'alimento': '🍖 Alimento',
            'parasitos': '🪱 Parásitos Internos',
            'ectoparasitos': '🐜 Ectoparásitos',
            
            # SECCIÓN 6: EXAMEN FÍSICO ESPECÍFICO
            'examanesFisicosRealizados': '🔍 Exámenes Físicos Realizados',
            
            # SECCIÓN 7: DIAGNÓSTICO
            'listaPosiblesProblemas': '❓ Posibles Problemas (Diferencial)',
            'listaProblemasReales': '✅ Problemas Reales Identificados',
            'diagnostico': '🩺 Diagnóstico Final',
            'pronostico': '📈 Pronóstico',
            
            # SECCIÓN 8: TRATAMIENTO Y SEGUIMIENTO
            'tratamiento': '💊 Tratamiento',
            'estudiosHechos': '🔬 Estudios Realizados',
            'estudiosRecomendados': '📋 Estudios Recomendados',
            'evolucion': '📊 Evolución',
            'observaciones': '📝 Observaciones',
        }

        help_texts = {
            'anamnesicos': 'Se incluye el motivo de la consulta y el problema actual del paciente tal como la expresa el propietario, y otra información como Dieta, Enfermedades previas, Cirugías previas, Tratamientos recientes, si Convive con otros animales, Viajes recientes...',
            'porcentajeHidratacion': '5%: leve, 6-8%: moderada, 10-12%: severa',
            'puntuacionCorporal': 'Escala de 1 a 5, donde 1 es muy delgado y 5 es obeso',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hacer campos de solo lectura
        readonly_fields = ['vacunas', 'ultimaDesparasitacion', 'ultimoDesparasitante']
        for field in readonly_fields:
            self.fields[field].widget.attrs['readonly'] = True
            self.fields[field].widget.attrs['style'] = 'background-color: #f8f9fa;'
        
        # Establecer el veterinario actual como opción por defecto
        from django.contrib.auth import get_user_model
        User = get_user_model()
        self.fields['veterinario'].queryset = User.objects.filter(is_active=True)


class ConsultaMedicaUpdateForm(forms.ModelForm):
    class Meta:
        model = ConsultasMedicas
        fields = [
            # Mismos campos que el form de creación
            'procedimiento',
            'clinicaVeterinaria',
            'veterinario',
            'anamnesicos',
            'mucosas',
            'porcentajeHidratacion',
            'temperatura',
            'pulso',
            'frecuenciaCardiaca',
            'frecuenciaRespiratoria',
            'peso',
            'puntuacionCorporal',
            'actitudConPropietario',
            'actitudConVeterinario',
            'vacunas',
            'alergias',
            'ultimaDesparasitacion',
            'ultimoDesparasitante',
            'alimento',
            'parasitos',
            'ectoparasitos',
            'examanesFisicosRealizados',
            'listaPosiblesProblemas',
            'listaProblemasReales',
            'diagnostico',
            'pronostico',
            'tratamiento',
            'estudiosHechos',
            'estudiosRecomendados',
            'evolucion',
            'observaciones',
        ]

        widgets = {
            # Mismos widgets que el form de creación
            'procedimiento': forms.Select(attrs={'class': 'form-control'}),
            'clinicaVeterinaria': forms.Select(attrs={'class': 'form-control'}),
            'veterinario': forms.Select(attrs={'class': 'form-control'}),
            'anamnesicos': forms.Textarea(attrs={
                'rows': 4, 
                'placeholder': 'Motivo de consulta, problema actual, dieta, enfermedades previas, cirugías, tratamientos recientes, convivencia con otros animales, viajes...',
                'class': 'form-control'
            }),
            'mucosas': forms.Select(attrs={'class': 'form-control'}),
            'porcentajeHidratacion': forms.TextInput(attrs={
                'placeholder': 'Ej. 5-7% (ligera deshidratación)',
                'class': 'form-control'
            }),
            'temperatura': forms.TextInput(attrs={
                'placeholder': 'Ej. 38.5 °C',
                'class': 'form-control'
            }),
            'pulso': forms.TextInput(attrs={
                'placeholder': 'Ej. 120 lpm',
                'class': 'form-control'
            }),
            'frecuenciaCardiaca': forms.TextInput(attrs={
                'placeholder': 'Ej. 140 bpm',
                'class': 'form-control'
            }),
            'frecuenciaRespiratoria': forms.TextInput(attrs={
                'placeholder': 'Ej. 30 rpm',
                'class': 'form-control'
            }),
            'peso': forms.NumberInput(attrs={
                'step': '0.01', 
                'placeholder': 'Peso en kg',
                'class': 'form-control'
            }),
            'puntuacionCorporal': forms.Select(attrs={'class': 'form-control'}),
            'actitudConPropietario': forms.Textarea(attrs={
                'rows': 2,
                'placeholder': 'Comportamiento con el propietario',
                'class': 'form-control'
            }),
            'actitudConVeterinario': forms.Textarea(attrs={
                'rows': 2,
                'placeholder': 'Comportamiento durante el examen',
                'class': 'form-control'
            }),
            'vacunas': forms.Textarea(attrs={
                'rows': 2,
                'placeholder': 'Vacunas aplicadas',
                'class': 'form-control',
                'readonly': 'readonly',
                'style': 'background-color: #f8f9fa;'
            }),
            'alergias': forms.Textarea(attrs={
                'rows': 2,
                'placeholder': 'Alergias conocidas',
                'class': 'form-control'
            }),
            'ultimaDesparasitacion': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'readonly': 'readonly',
                'style': 'background-color: #f8f9fa;'
            }),
            'ultimoDesparasitante': forms.Textarea(attrs={
                'rows': 2,
                'placeholder': 'Último desparasitante aplicado',
                'class': 'form-control',
                'readonly': 'readonly',
                'style': 'background-color: #f8f9fa;'
            }),
            'alimento': forms.Textarea(attrs={
                'rows': 2,
                'placeholder': 'Tipo y cantidad de alimento',
                'class': 'form-control'
            }),
            'parasitos': forms.Textarea(attrs={
                'rows': 2,
                'placeholder': 'Parásitos detectados',
                'class': 'form-control'
            }),
            'ectoparasitos': forms.Textarea(attrs={
                'rows': 2,
                'placeholder': 'Presencia de pulgas, garrapatas, etc.',
                'class': 'form-control'
            }),
            'examanesFisicosRealizados': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Exámenes físicos realizados y hallazgos',
                'class': 'form-control'
            }),
            'listaPosiblesProblemas': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Lista de posibles problemas (diagnóstico diferencial)',
                'class': 'form-control'
            }),
            'listaProblemasReales': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Lista de problemas reales identificados',
                'class': 'form-control'
            }),
            'diagnostico': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Diagnóstico final',
                'class': 'form-control'
            }),
            'pronostico': forms.Textarea(attrs={
                'rows': 2,
                'placeholder': 'Pronóstico del caso',
                'class': 'form-control'
            }),
            'tratamiento': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Tratamiento prescrito, medicamentos, dosis, frecuencia...',
                'class': 'form-control'
            }),
            'estudiosHechos': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Estudios de laboratorio o imagen realizados',
                'class': 'form-control'
            }),
            'estudiosRecomendados': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Estudios recomendados para seguimiento',
                'class': 'form-control'
            }),
            'evolucion': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Evolución del paciente durante la consulta',
                'class': 'form-control'
            }),
            'observaciones': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Observaciones adicionales',
                'class': 'form-control'
            }),
        }

        labels = {
            # Mismas labels que el form de creación
            'procedimiento': '🩺 Tipo de Procedimiento',
            'clinicaVeterinaria': '🏥 Clínica Veterinaria',
            'veterinario': '👨‍⚕️ Médico Veterinario',
            'anamnesicos': '📋 Anamnesis',
            'mucosas': '👄 Mucosas',
            'porcentajeHidratacion': '💧 Porcentaje de Hidratación',
            'temperatura': '🌡️ Temperatura',
            'pulso': '💓 Pulso (LPM)',
            'frecuenciaCardiaca': '❤️ Frecuencia Cardíaca',
            'frecuenciaRespiratoria': '🌬️ Frecuencia Respiratoria',
            'peso': '⚖️ Peso (kg)',
            'puntuacionCorporal': '📊 Puntuación Corporal',
            'actitudConPropietario': '👤 Actitud con el Propietario',
            'actitudConVeterinario': '👨‍⚕️ Actitud con el Veterinario',
            'vacunas': '💉 Vacunas',
            'alergias': '🤧 Alergias',
            'ultimaDesparasitacion': '📅 Última Desparasitación',
            'ultimoDesparasitante': '💊 Último Desparasitante',
            'alimento': '🍖 Alimento',
            'parasitos': '🪱 Parásitos Internos',
            'ectoparasitos': '🐜 Ectoparásitos',
            'examanesFisicosRealizados': '🔍 Exámenes Físicos Realizados',
            'listaPosiblesProblemas': '❓ Posibles Problemas (Diferencial)',
            'listaProblemasReales': '✅ Problemas Reales Identificados',
            'diagnostico': '🩺 Diagnóstico Final',
            'pronostico': '📈 Pronóstico',
            'tratamiento': '💊 Tratamiento',
            'estudiosHechos': '🔬 Estudios Realizados',
            'estudiosRecomendados': '📋 Estudios Recomendados',
            'evolucion': '📊 Evolución',
            'observaciones': '📝 Observaciones',
        }

        help_texts = {
            'anamnesicos': 'Se incluye el motivo de la consulta y el problema actual del paciente tal como la expresa el propietario, y otra información como Dieta, Enfermedades previas, Cirugías previas, Tratamientos recientes, si Convive con otros animales, Viajes recientes...',
            'porcentajeHidratacion': '5%: leve, 6-8%: moderada, 10-12%: severa',
            'puntuacionCorporal': 'Escala de 1 a 5, donde 1 es muy delgado y 5 es obeso',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hacer campos de solo lectura
        readonly_fields = ['vacunas', 'ultimaDesparasitacion', 'ultimoDesparasitante']
        for field in readonly_fields:
            self.fields[field].widget.attrs['readonly'] = True
            self.fields[field].widget.attrs['style'] = 'background-color: #f8f9fa;'


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
            'descripcion': '📝 Descripción'
        }