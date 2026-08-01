from django import forms
from .models import Clientes, Mascotas

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Clientes
        fields = ['nombre', 'email', 'telefono', 'direccion']
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Ej. Juan Pérez'}),
            'email': forms.EmailInput(attrs={'placeholder': 'ejemplo@correo.com'}),
            'telefono': forms.TextInput(attrs={'placeholder': 'Ej. 5512345678'}),
            'direccion': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Calle, número, colonia, ciudad...'
            }),
        }
        labels = {
            'nombre': '👤 Nombre completo',
            'email': '📧 Correo electrónico',
            'telefono': '📞 Número de teléfono',
            'direccion': '🏠 Dirección del cliente',
        }

    def clean_telefono(self):
        telefono = self.cleaned_data['telefono'].replace(' ', '')
        if not telefono.isdigit():
            raise forms.ValidationError("❌ El número de teléfono solo puede contener dígitos.")
        return telefono


class MascotaForm(forms.ModelForm):
    class Meta:
        model = Mascotas
        fields = ['nombre', 'especie', 'raza', 'fechaNacimiento', 'peso', 'sexo', 'alergias', 'alimento', 'vive']
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Ej. Firulais'}),
            'especie': forms.TextInput(attrs={'placeholder': 'Ej. Perro, Gato...'}),
            'raza': forms.TextInput(attrs={'placeholder': 'Ej. Labrador, Siames...'}),
            'fechaNacimiento': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'peso': forms.NumberInput(attrs={'placeholder': 'Ej. 1 (kilogramos)'}),
            'sexo': forms.Select(attrs={'class': 'form-control'}),
            'alergias': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Alergias conocidas'}),
            'alimento' : forms.Textarea(attrs={'rows': 3, 'placeholder': 'Tipo de alimento que consume'}),
            'vive': forms.CheckboxInput(attrs={'class': 'checkbox-grande'}),
        }
        labels = {
            'nombre': '🐕 Nombre de la mascota',
            'especie': '🐾 Especie',
            'raza': '🎯 Raza',
            'fechaNacimiento': '📅 Fecha de nacimiento',
            'peso': '⚖️ Peso (kg)',
            'sexo': '⚧️ Sexo de la mascota',
            'alergias': '🤧 Alergias conocidas',
            'alimento': '🍖 Tipo de alimento que consume',
            'vive': '❤️ ¿Sigue con vida?',
        }