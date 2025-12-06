from django import forms
from .models import Estetica
from ClientesMascotas.models import Mascotas

class EsteticaForm(forms.ModelForm):
    class Meta:
        model = Estetica
        fields = [
            'mascota',
            'fechaHoraIngreso',
            'fechaHoraEgreso',
            'agregarServicioVacuna',
            'agregarServicioDesparasitacion',
            'condicionesDeMascota',
            'cortesDePeloEspeciales',
            'espeficiacionCorte',
            'servicio',
            'detallesServicio',
            'pagado',
            'pagoTotal',
            'fotoAntes',
            'fotoDespues',
            'estilista',
            'clinicaVeterinaria',
        ]
        widgets = {
            'fechaHoraIngreso': forms.DateTimeInput(attrs={
                'type': 'datetime-local', 
                'class': 'form-control'
            }),
            'fechaHoraEgreso': forms.DateTimeInput(attrs={
                'type': 'datetime-local', 
                'class': 'form-control'
            }),
            'condicionesDeMascota': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': 'Condiciones de la mascota al ingreso...'
            }),
            'espeficiacionCorte': forms.TextInput(attrs={  # CORREGIDO: sin style display:none
                'class': 'form-control',
                'placeholder': 'Especifique el tipo de corte...',
                'id': 'id_espeficiacionCorte'  # Agregar ID específico
            }),
            'servicio': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': 'Descripción del servicio...'
            }),
            'detallesServicio': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': 'Detalles adicionales del servicio...'
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
            'cortesDePeloEspeciales': forms.Select(attrs={
                'class': 'form-control',
                'id': 'id_cortesDePeloEspeciales'
            }),
            'estilista': forms.Select(attrs={
                'class': 'form-control'
            }),
            'mascota': forms.Select(attrs={
                'class': 'form-control',
                'style': 'display: none;'
            }),
            'agregarServicioVacuna': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'agregarServicioDesparasitacion': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
        labels = {
            'mascota': '🐕 Mascota',
            'fechaHoraIngreso': '📅 Fecha y Hora de Ingreso',
            'fechaHoraEgreso': '📅 Fecha y Hora de Egreso',
            'agregarServicioVacuna': '💉 Agregar Servicio de Vacuna',
            'agregarServicioDesparasitacion': '💊 Agregar Servicio de Desparasitación',
            'condicionesDeMascota': '💓 Condiciones de la Mascota',
            'cortesDePeloEspeciales': '✂️ Tipo de Corte de Pelo',
            'espeficiacionCorte': '✏️ Especificación del Corte',
            'servicio': '🛠️ Servicio Solicitado',
            'detallesServicio': '📝 Detalles del Servicio',
            'pagado': '💰 Pagado',
            'pagoTotal': '💰 Pago Total',
            'fotoAntes': '🖼️ Foto Antes del Servicio',
            'fotoDespues': '🖼️ Foto Después del Servicio',
            'estilista': '👨‍🔬 Estilista',
            'clinicaVeterinaria': '🏥 Clínica',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['mascota'].queryset = Mascotas.objects.all().select_related('cliente')
        # Hacer campos opcionales
        self.fields['fechaHoraEgreso'].required = False
        self.fields['fotoAntes'].required = False
        self.fields['fotoDespues'].required = False
        self.fields['condicionesDeMascota'].required = False
        self.fields['detallesServicio'].required = False
        self.fields['espeficiacionCorte'].required = False
        
        
        # Ya no necesitamos manejar el estilo aquí, lo hará el JavaScript


class EsteticaUpdateForm(forms.ModelForm):
    class Meta:
        model = Estetica
        fields = [
            'mascota',
            'fechaHoraIngreso',
            'fechaHoraEgreso',
            'agregarServicioVacuna',
            'agregarServicioDesparasitacion',
            'condicionesDeMascota',
            'cortesDePeloEspeciales',
            'espeficiacionCorte',
            'servicio',
            'detallesServicio',
            'pagado',
            'pagoTotal',
            'estilista',
            'clinicaVeterinaria',
            # EXCLUIMOS fotoAntes y fotoDespues del formulario de actualización
        ]
        widgets = {
            'fechaHoraIngreso': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local', 
                    'placeholder': 'Selecciona la nueva fecha y hora de la cita',
                    'class': 'form-control'
                },
                format='%Y-%m-%dT%H:%M'  # 🔥 Formato específico para datetime-local
            ),
            'fechaHoraEgreso': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local', 
                    'placeholder': 'Selecciona la nueva fecha y hora de la cita',
                    'class': 'form-control'
                },
                format='%Y-%m-%dT%H:%M'  # 🔥 Formato específico para datetime-local
            ),
            'condicionesDeMascota': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': 'Condiciones de la mascota al ingreso...'
            }),
            'espeficiacionCorte': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Especifique el tipo de corte...',
                'id': 'id_espeficiacionCorte_update'
            }),
            'servicio': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': 'Descripción del servicio...'
            }),
            'detallesServicio': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': 'Detalles adicionales del servicio...'
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
            'clinicaVeterinaria': forms.Select(attrs={
                'class': 'form-control'
            }),
            'cortesDePeloEspeciales': forms.Select(attrs={
                'class': 'form-control',
                'id': 'id_cortesDePeloEspeciales_update'
            }),
            'estilista': forms.Select(attrs={
                'class': 'form-control'
            }),
            'mascota': forms.Select(attrs={
                'class': 'form-control',
                'style': 'display: none;'
            }),
            'agregarServicioVacuna': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'agregarServicioDesparasitacion': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
        labels = {
            'mascota': '🐕 Mascota',
            'fechaHoraIngreso': '📅 Fecha y Hora de Ingreso',
            'fechaHoraEgreso': '📅 Fecha y Hora de Egreso',
            'agregarServicioVacuna': '💉 Agregar Servicio de Vacuna',
            'agregarServicioDesparasitacion': '💊 Agregar Servicio de Desparasitación',
            'condicionesDeMascota': '💓 Condiciones de la Mascota',
            'cortesDePeloEspeciales': '✂️ Tipo de Corte de Pelo',
            'espeficiacionCorte': '✏️ Especificación del Corte',
            'servicio': '🛠️ Servicio Solicitado',
            'detallesServicio': '📝 Detalles del Servicio',
            'pagado': '💰 Pagado',
            'pagoTotal': '💰 Pago Total',
            'estilista': '👨‍🔬 Estilista',
            'clinicaVeterinaria': '🏥 Clínica',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['mascota'].queryset = Mascotas.objects.all().select_related('cliente')
        self.fields['fechaHoraEgreso'].required = False
        self.fields['condicionesDeMascota'].required = False
        self.fields['detallesServicio'].required = False
        self.fields['espeficiacionCorte'].required = False
        
        
       