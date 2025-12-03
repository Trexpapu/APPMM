from django.db import models
from ClientesMascotas.models import Mascotas
from django.contrib.auth.models import User
# Create your models here.
class Estetica(models.Model):
    CLINICAS = [
        ('Mascotas Morelia Centro (Samuel Castañon Pte. 73 Centro 60600 Apatzingán, Mich. Número 453-227-1694)', 'Mascotas Morelia Centro (Samuel Castañon Pte. 73 Centro 60600 Apatzingán, Mich. Número 453-227-1694)'),
    ] 
    CORTES = [
        ('De acuerdo a su raza', 'De acuerdo a su raza'),
        ('Corte a raz de piel', 'Corte a raz de piel'),
        ('Corte dejando pelo alto', 'Corte dejando pelo alto'),
        ('Otro Especifique', 'Otro Especifique'),
        ('Ninguno', 'Ninguno'),
    ] 
    mascota = models.ForeignKey(Mascotas, on_delete=models.CASCADE)
    fechaHoraIngreso = models.DateTimeField()
    fechaHoraEgreso = models.DateTimeField(blank=True, null=True)
    agregarServicioVacuna = models.BooleanField(default=False)
    agregarServicioDesparasitacion = models.BooleanField(default=False)
    condicionesDeMascota = models.TextField(blank=True)
    cortesDePeloEspeciales = models.CharField(
        max_length=300,
        choices=CORTES,
        default='De acuerdo a su raza'  # puedes poner un valor por defecto si quieres
    )
    espeficiacionCorte = models.TextField(blank=True)
    servicio = models.TextField()
    detallesServicio = models.TextField(blank=True)
    pagado = models.FloatField(default=0)#esto es por si deja anticipo
    pagoTotal = models.FloatField(default=0)
    fotoAntes = models.TextField(blank=True)
    fotoDespues = models.TextField(blank= True)
    estilista =  models.ForeignKey(User, on_delete=models.CASCADE)
    clinicaVeterinaria = models.CharField(
        max_length=255,
        choices=CLINICAS,
        default='Mascotas Morelia Centro (Samuel Castañon Pte. 73 Centro 60600 Apatzingán, Mich. Número 453-227-1694)'  # puedes poner un valor por defecto si quieres
    )