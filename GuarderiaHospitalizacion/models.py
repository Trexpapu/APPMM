from django.db import models
from ClientesMascotas.models import *
# Create your models here.
class Guarderia(models.Model):
    
    CLINICAS = [
        ('Mascotas Morelia Centro', 'Mascotas Morelia Centro'),
        ('Mascotas Morelia Salida Apatzingán', 'Mascotas Morelia Salida Apatzingán'),
        ('Mascotas Morelia Mano Huevona', 'Mascotas Morelia Mano Huevona'),
    ]
    mascota = models.ForeignKey(Mascotas, on_delete=models.CASCADE)
    alimento = models.TextField(blank= True)
    accesoriosRecibidos = models.TextField(blank= True)
    estadoSalud = models.TextField(blank= True)
    tratamientos = models.TextField(blank= True)
    otrosDatos = models.TextField(blank= True)
    clinicaVeterinaria = models.CharField(
        max_length=255,
        choices=CLINICAS,
        default='Mascotas Morelia Centro'  # puedes poner un valor por defecto si quieres
    )
    fechaEntrada = models.DateField()
    fechaSalidaProgramada = models.DateField(blank= True, null = True)
    fechaSalidaReal = models.DateField(blank= True, null = True)
    pagado = models.FloatField(default=0)#esto es por si deja anticipo
    pagoTotal = models.FloatField(default=0)
    fotoAntes = models.TextField(blank=True)
    fotoDespues = models.TextField(blank= True)
