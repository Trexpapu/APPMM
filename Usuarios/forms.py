from django import forms
from django.contrib.auth.models import User

class UsuarioForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña', 'class': 'form-control'}), label='Contraseña')
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirmar contraseña', 'class': 'form-control'}), label='Confirmar Contraseña')
    is_superuser = forms.BooleanField(required=False, label='¿Será administrador (Super Usuario)?', widget=forms.CheckboxInput(attrs={'class': 'checkbox-grande'}))

    class Meta:
        model = User
        fields = ['first_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Ej. Juan Pérez', 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'placeholder': 'ejemplo@correo.com', 'class': 'form-control'}),
        }
        labels = {
            'first_name': '👤 Nombre completo',
            'email': '📧 Correo',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['email'].required = True

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "❌ Las contraseñas no coinciden.")

        return cleaned_data

class UsuarioUpdateForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Dejar en blanco para no cambiar', 'class': 'form-control'}), label='Contraseña (opcional)', required=False)
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirmar contraseña', 'class': 'form-control'}), label='Confirmar Contraseña (opcional)', required=False)
    is_superuser = forms.BooleanField(required=False, label='¿Será administrador (Super Usuario)?', widget=forms.CheckboxInput(attrs={'class': 'checkbox-grande'}))

    class Meta:
        model = User
        fields = ['first_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Ej. Juan Pérez', 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'placeholder': 'ejemplo@correo.com', 'class': 'form-control'}),
        }
        labels = {
            'first_name': '👤 Nombre completo',
            'email': '📧 Correo',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['email'].required = True

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password or confirm_password:
            if password != confirm_password:
                self.add_error('confirm_password', "❌ Las contraseñas no coinciden.")

        return cleaned_data
