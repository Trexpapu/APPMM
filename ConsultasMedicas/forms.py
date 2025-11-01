from django import forms
from .models import *


class SiguienteConsultaForm(forms.ModelForm):
    class Meta:
        model = SiguientesConsultas
        fields = [ 'fechaSiguienteConsulta', 'motivoSiguienteConsulta', 'clinicaVeterinaria', 'veterinario']
        widgets = {
            
            'fechaSiguienteConsulta': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'motivoSiguienteConsulta': forms.Textarea(attrs={'rows': 3}),
        }
