from django.db import models 
from ClientesMascotas.models import *
from django.contrib.auth.models import User
# Create your models here.
class ListaVacunas(models.Model):
    vacuna = models.TextField()
class ListaDesparasitantes(models.Model):
    desparasitante = models.TextField()

class Vacunaciones(models.Model):
    CLINICAS = [
        ('Mascotas Morelia Centro', 'Mascotas Morelia Centro'),
        ('Mascotas Morelia Salida Apatzingán', 'Mascotas Morelia Salida Apatzingán'),
        ('Mascotas Morelia Mano Huevona', 'Mascotas Morelia Mano Huevona'),
    ]
    mascota = models.ForeignKey(Mascotas, on_delete=models.CASCADE)
    vacunas = models.ForeignKey(ListaVacunas, on_delete=models.CASCADE)
    descripcion = models.TextField(blank= True)
    veterinario =  models.ForeignKey(User, on_delete=models.CASCADE)
    clinicaVeterinaria = models.CharField(
        max_length=255,
        choices=CLINICAS,
        default='Mascotas Morelia Centro'  # puedes poner un valor por defecto si quieres
    )
    fecha = models.DateField()



class Desparasitaciones(models.Model):
    CLINICAS = [
        ('Mascotas Morelia Centro', 'Mascotas Morelia Centro'),
        ('Mascotas Morelia Salida Apatzingán', 'Mascotas Morelia Salida Apatzingán'),
        ('Mascotas Morelia Mano Huevona', 'Mascotas Morelia Mano Huevona'),
    ]
    mascota = models.ForeignKey(Mascotas, on_delete=models.CASCADE)
    desparasitante = models.ForeignKey(ListaDesparasitantes, on_delete= models.CASCADE)
    fecha = models.DateField()
    
    veterinario =  models.ForeignKey(User, on_delete=models.CASCADE)
    clinicaVeterinaria = models.CharField(
        max_length=255,
        choices=CLINICAS,
        default='Mascotas Morelia Centro'  # puedes poner un valor por defecto si quieres
    )

class Operaciones(models.Model):
    CLINICAS = [
        ('Mascotas Morelia Centro', 'Mascotas Morelia Centro'),
        ('Mascotas Morelia Salida Apatzingán', 'Mascotas Morelia Salida Apatzingán'),
        ('Mascotas Morelia Mano Huevona', 'Mascotas Morelia Mano Huevona'),
    ]
    mascota = models.ForeignKey(Mascotas, on_delete= models.CASCADE)
    fechaEntrada = models.DateTimeField()
    fechaSalida = models.DateTimeField(blank= True, null = True)
    operacion = models.TextField()
    descripcion = models.TextField(blank= True)
    complicaciones = models.TextField(blank= True)
    fotoAntes = models.TextField(blank=True)
    fotoDespues = models.TextField(blank= True)
    veterinario =  models.ForeignKey(User, on_delete=models.CASCADE)
    clinicaVeterinaria = models.CharField(
        max_length=255,
        choices=CLINICAS,
        default='Mascotas Morelia Centro'  # puedes poner un valor por defecto si quieres
    )

