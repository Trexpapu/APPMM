from django import forms
from .models import Clientes, Mascotas

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Clientes
        fields = ['nombre', 'email', 'telefono', 'direccion']
        widgets = {
            'direccion': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_telefono(self):
        telefono = self.cleaned_data['telefono'].replace(' ', '')
        if not telefono.isdigit():
            raise forms.ValidationError("El número de teléfono solo puede contener dígitos.")
        return telefono

class ClienteUpdateForm(forms.ModelForm):
    class Meta:
        model = Clientes
        fields = ['nombre', 'email', 'telefono', 'direccion']
        widgets = {
            'direccion': forms.Textarea(attrs={'rows': 3}),
        }

class MascotaForm(forms.ModelForm):
    class Meta:
        model = Mascotas
        fields = ['nombre', 'especie', 'raza', 'fechaNacimiento', 'peso', 'vacunas', 'alergias', 'vive']
        widgets = {
            'fechaNacimiento': forms.DateInput(attrs={'type': 'date'}),
            'vacunas': forms.Textarea(attrs={'rows': 3}),
            'alergias': forms.Textarea(attrs={'rows': 3}),
            'vive': forms.CheckboxInput(attrs={'class': 'checkbox-grande'}),
        }



class MascotaUpdateForm(forms.ModelForm):
    class Meta:
        model = Mascotas
        fields = ['nombre', 'especie', 'raza', 'fechaNacimiento', 'peso', 'vacunas', 'alergias', 'vive']
        widgets = {
            'fechaNacimiento': forms.DateInput(attrs={'type': 'date'}),
            'vacunas': forms.Textarea(attrs={'rows': 3}),
            'alergias': forms.Textarea(attrs={'rows': 3}),
            'vive': forms.CheckboxInput(attrs={'class': 'checkbox-grande'}),
        }

