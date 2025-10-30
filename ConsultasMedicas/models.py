from django.db import models
from ClientesMascotas.models import Mascotas
from django.contrib.auth.models import User
# Create your models here.
class ConsultasMedicas(models.Model):
    CLINICAS = [
        ('m1', 'Mascotas Morelia Centro'),
        ('m2', 'Mascotas Morelia Salida Apatzingán'),
        ('m3', 'Mascotas Morelia Mano Huevona'),
    ] 
    mascota = models.ForeignKey(Mascotas, on_delete=models.CASCADE)
    motivoConsulta = models.TextField(blank=True)
    temperatura = models.TextField( blank=True)
    pulso = models.TextField(blank=True)
    frecuenciaCardiaca = models.TextField( blank=True)
    puntuacionCorporal = models.TextField(blank=True)
    parasitos = models.TextField(blank=True)
    agua = models.TextField(blank=True)
    alimento = models.TextField(blank=True)
    condicionesDeHogar = models.TextField(blank=True)
    ectoparasitos = models.TextField(blank=True)
    sintomas = models.TextField(blank=True) 
    observaciones = models.TextField(blank=True)
    diagnostico = models.TextField(blank=True) 
    recetaMedica = models.TextField(blank=True) 
    fechaConsulta = models.DateField(auto_now_add=True)
    veterinario =  models.ForeignKey(User, on_delete=models.CASCADE)
    clinicaVeterinaria = models.CharField(
        max_length=255,
        choices=CLINICAS,
        default='m1'  # puedes poner un valor por defecto si quieres
    )

class SiguientesConsultas(models.Model):
    fechaSiguienteConsulta = models.DateField()
    motivoSiguienteConsulta = models.TextField(blank=True)

class Desparasitaciones(models.Model):
    mascota = models.ForeignKey(Mascotas, on_delete=models.CASCADE)
    fechaUltimaDesparasitacion = models.DateField(blank= True, null=True)
    Desparasitante = models.TextField(blank=True)
    proximaDesparasitacion = models.DateField(blank= True, null=True)