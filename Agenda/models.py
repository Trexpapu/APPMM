from django.db import models
from ClientesMascotas.models import Mascotas
from django.contrib.auth.models import User
# Create your models here.
class SiguientesCitas(models.Model):
    CLINICAS = [
        ('Mascotas Morelia Centro', 'Mascotas Morelia Centro'),
        ('Mascotas Morelia Salida Apatzingán', 'Mascotas Morelia Salida Apatzingán'),
        ('Mascotas Morelia Mano Huevona', 'Mascotas Morelia Mano Huevona'),
    ]
    ESTADOS_ASISTENCIAS = [
        ('Pendiente', 'Pendiente'),
        ('Si asistió', 'Si asistió'),
        ('No asistió', 'No asistió'),
    ] 
    TIPOS_CITA = [
        ('Consulta', 'Consulta'),
        ('Operación médica', 'Operación médica'),
        ('Desparasitación', 'Desparasitación'),
        ('Vacunación', 'Vacunación'),
        ('Servicio de estética', 'Servicio de estética'),
    ] 
    
    fechaSiguienteCita = models.DateTimeField()
    descripcionCita = models.TextField(blank=True)
    tipoCita = models.CharField(
        max_length=64,
        choices= TIPOS_CITA, 
        default= 'Consulta'
    )
    asistencia = models.CharField(
        max_length=64,
        choices= ESTADOS_ASISTENCIAS, 
        default= 'Pendiente'
    )
    veterinario =  models.ForeignKey(User, on_delete=models.CASCADE)
    mascota = models.ForeignKey(Mascotas, on_delete=models.CASCADE)
    clinicaVeterinaria = models.CharField(
        max_length=255,
        choices=CLINICAS,
        default='Mascotas Morelia Centro'  # puedes poner un valor por defecto si quieres
    )
