import re
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.utils.text import slugify

def clean_username_from_name(name):
    # Quitar espacios en los extremos y conservar mayúsculas/minúsculas
    username = name.strip()
    # Reemplazar espacios por guiones bajos
    username = re.sub(r'\s+', '_', username)
    # Mantener solo caracteres válidos para el username de Django (letras, números, _, @, +, ., -)
    username = re.sub(r'[^\w.@+-]', '', username)
    return username

def generate_unique_username(name, exclude_user_id=None):
    base_username = clean_username_from_name(name)
    if not base_username:
        base_username = 'usuario'
        
    username = base_username
    counter = 1
    
    while True:
        qs = User.objects.filter(username=username)
        if exclude_user_id:
            qs = qs.exclude(id=exclude_user_id)
        if not qs.exists():
            break
        username = f"{base_username}_{counter}"
        counter += 1
        
    return username

def get_all_usuarios():
    return User.objects.all().order_by('first_name')

def save_usuario(form):
    if form.is_valid():
        user = form.save(commit=False)
        # Generar un username único a partir del Nombre Completo (first_name)
        user.username = generate_unique_username(form.cleaned_data['first_name'])
        user.set_password(form.cleaned_data['password'])
        user.is_superuser = form.cleaned_data['is_superuser']
        user.is_staff = form.cleaned_data['is_superuser']  # Permite entrar al panel admin de django si es superuser
        user.save()
        return user
    return None

def update_usuario(form, user):
    if form.is_valid():
        user.first_name = form.cleaned_data['first_name']
        user.email = form.cleaned_data['email']
        # Regenerar/actualizar el username a partir del nuevo Nombre Completo, evitando colisión con el propio id
        user.username = generate_unique_username(form.cleaned_data['first_name'], exclude_user_id=user.id)
        if form.cleaned_data.get('password'):
            user.set_password(form.cleaned_data['password'])
        user.is_superuser = form.cleaned_data['is_superuser']
        user.is_staff = form.cleaned_data['is_superuser']
        user.save()
        return user
    return None

def delete_usuario(pk):
    user = get_object_or_404(User, pk=pk)
    user.delete()
