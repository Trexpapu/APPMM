from django.db.models import Q
from django.shortcuts import get_object_or_404
from datetime import date
from .models import Clientes, Mascotas

def get_filtered_clientes(query):
    if query:
        return Clientes.objects.filter(
            Q(nombre__icontains=query) |
            Q(email__icontains=query) |
            Q(telefono__icontains=query)
        )
    return Clientes.objects.all()[:10]

def get_filtered_mascotas(query_cliente, query_mascota):
    mascotas = Mascotas.objects.select_related('cliente').all()
    
    if query_cliente:
        mascotas = mascotas.filter(
            Q(cliente__nombre__icontains=query_cliente) |
            Q(cliente__email__icontains=query_cliente) |
            Q(cliente__telefono__icontains=query_cliente)
        )
    
    if query_mascota:
        mascotas = mascotas.filter(
            Q(nombre__icontains=query_mascota) |
            Q(raza__icontains=query_mascota) |
            Q(especie__icontains=query_mascota) |
            Q(vacunas__icontains=query_mascota) |
            Q(alergias__icontains=query_mascota)
        )
    
    filtros_activos = bool(query_cliente or query_mascota)
    if not filtros_activos:
        mascotas = mascotas[:10]
        
    return mascotas, filtros_activos

def delete_cliente(pk):
    cliente = get_object_or_404(Clientes, pk=pk)
    cliente.delete()

def save_mascota(form, cliente_id):
    if form.is_valid() and cliente_id:
        mascota = form.save(commit=False)
        mascota.cliente_id = cliente_id
        mascota.save()
        return mascota
    return None

def delete_mascota(pk):
    mascota = get_object_or_404(Mascotas, pk=pk)
    mascota.delete()

def get_cliente_details(cliente_id):
    cliente = get_object_or_404(Clientes, id=cliente_id)
    mascotas = Mascotas.objects.filter(cliente=cliente).order_by('nombre')
    mascotasVivas = mascotas.filter(vive=True).count()
    
    return {
        'cliente': cliente,
        'mascotas': mascotas,
        'mascotasVivas': mascotasVivas
    }

def get_mascota_details(mascota_id):
    mascota = get_object_or_404(Mascotas, id=mascota_id)
    
    hoy = date.today()
    edad = hoy.year - mascota.fechaNacimiento.year - (
        (hoy.month, hoy.day) < (mascota.fechaNacimiento.month, mascota.fechaNacimiento.day)
    )
    
    return {
        'mascota': mascota,
        'edad': edad,
    }
