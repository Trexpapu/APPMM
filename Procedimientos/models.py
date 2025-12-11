from django.db import models 
from ClientesMascotas.models import *
from django.contrib.auth.models import User
# Create your models here.


class ListaVacunas(models.Model):
    vacuna = models.TextField()
    
    def __str__(self):
        return self.vacuna
    
class ListaDesparasitantes(models.Model):
    desparasitante = models.TextField()
    
    def __str__(self):
        return self.desparasitante

class Vacunaciones(models.Model):
    CLINICAS = [
        ('Mascotas Morelia Centro (Samuel Castañon Pte. 73 Centro 60600 Apatzingán, Mich. Número 453-227-1694)', 'Mascotas Morelia Centro (Samuel Castañon Pte. 73 Centro 60600 Apatzingán, Mich. Número 453-227-1694)'),
      
    ]
    mascota = models.ForeignKey(Mascotas, on_delete=models.CASCADE)
    vacunas = models.ForeignKey(ListaVacunas, on_delete=models.CASCADE)
    descripcion = models.TextField(blank= True)
    veterinario =  models.ForeignKey(User, on_delete=models.CASCADE)
    clinicaVeterinaria = models.CharField(
        max_length=255,
        choices=CLINICAS,
        default='Mascotas Morelia Centro (Samuel Castañon Pte. 73 Centro 60600 Apatzingán, Mich. Número 453-227-1694)'  # puedes poner un valor por defecto si quieres
    )
    fecha = models.DateField()



class Desparasitaciones(models.Model):
    CLINICAS = [
        ('Mascotas Morelia Centro (Samuel Castañon Pte. 73 Centro 60600 Apatzingán, Mich. Número 453-227-1694)', 'Mascotas Morelia Centro (Samuel Castañon Pte. 73 Centro 60600 Apatzingán, Mich. Número 453-227-1694)'),
       
    ]
    mascota = models.ForeignKey(Mascotas, on_delete=models.CASCADE)
    peso = models.DecimalField(
        max_digits=5,   # número total de dígitos
        decimal_places=3  # número de decimales fijos
    )
    desparasitante = models.ForeignKey(ListaDesparasitantes, on_delete= models.CASCADE)
    fecha = models.DateField()
    veterinario =  models.ForeignKey(User, on_delete=models.CASCADE)
    clinicaVeterinaria = models.CharField(
        max_length=255,
        choices=CLINICAS,
        default='Mascotas Morelia Centro (Samuel Castañon Pte. 73 Centro 60600 Apatzingán, Mich. Número 453-227-1694)'  # puedes poner un valor por defecto si quieres
    )

class Operaciones(models.Model):
    CLINICAS = [
        ('Mascotas Morelia Centro (Samuel Castañon Pte. 73 Centro 60600 Apatzingán, Mich. Número 453-227-1694)', 'Mascotas Morelia Centro (Samuel Castañon Pte. 73 Centro 60600 Apatzingán, Mich. Número 453-227-1694)'),
       
    ]
    mascota = models.ForeignKey(Mascotas, on_delete= models.CASCADE)
    peso = models.DecimalField(
        max_digits=5,   # número total de dígitos
        decimal_places=3  # número de decimales fijos
    )
    estadoSaludPrevio = models.TextField(blank= True)
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
        default='Mascotas Morelia Centro (Samuel Castañon Pte. 73 Centro 60600 Apatzingán, Mich. Número 453-227-1694)'  # puedes poner un valor por defecto si quieres
    )

