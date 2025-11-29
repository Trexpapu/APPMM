from django.db import models
from ClientesMascotas.models import *
# Create your models here.
class Guarderia(models.Model):
    
    CLINICAS = [
        ('Mascotas Morelia Centro', 'Mascotas Morelia Centro'),
        ('Mascotas Morelia Salida Apatzingán', 'Mascotas Morelia Salida Apatzingán'),
        ('Mascotas Morelia Mano Huevona', 'Mascotas Morelia Mano Huevona'),
    ]
    ESTADOS = [
        ('En guardería', 'En guardería'),
        ('Alta', 'Alta'),
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
    estado = models.CharField(
        max_length=255,
        choices=ESTADOS,
        default='En guardería'
    )
    fechaEntrada = models.DateField()
    fechaSalidaProgramada = models.DateField(blank= True, null = True)
    fechaSalidaReal = models.DateField(blank= True, null = True)
    pagado = models.FloatField(default=0)#esto es por si deja anticipo
    pagoTotal = models.FloatField(default=0)
    fotoAntes = models.TextField(blank=True)
    fotoDespues = models.TextField(blank= True)

class Hospitalizacion(models.Model):

    CLINICAS = [
        ('Mascotas Morelia Centro', 'Mascotas Morelia Centro'),
        ('Mascotas Morelia Salida Apatzingán', 'Mascotas Morelia Salida Apatzingán'),
        ('Mascotas Morelia Mano Huevona', 'Mascotas Morelia Mano Huevona'),
    ]

    ESTADOS = [
        ('Hospitalizado', 'Hospitalizado'),
        ('Alta', 'Alta'),
    ]

    # Relación con la mascota
    mascota = models.ForeignKey(Mascotas, on_delete=models.CASCADE)

    # Información del ingreso
    motivoIngreso = models.TextField(blank=True)
    diagnostico = models.TextField(blank=True)

    # Datos médicos
    estadoSaludPrevio = models.TextField(blank=True)
    tratamientos = models.TextField(blank=True)
    evolucion = models.TextField(blank=True)

    # Datos complementarios
    otrosDatos = models.TextField(blank=True)

    # Fotos (formato base64)
    fotoAntes = models.TextField(blank=True)
    fotoDespues = models.TextField(blank=True)

    # Clínica
    clinicaVeterinaria = models.CharField(
        max_length=255,
        choices=CLINICAS,
        default='Mascotas Morelia Centro'
    )

    # Fechas
    fechaEntrada = models.DateField()
    fechaSalida = models.DateField(blank=True, null=True)

    # Alta
    recomendacionesAlta = models.TextField(blank=True)

    # Costos (opcional pero recomendado)
    costoEstimado = models.FloatField(default=0)
    costoFinal = models.FloatField(default=0)

    # Estado del paciente
    estado = models.CharField(
        max_length=255,
        choices=ESTADOS,
        default='Hospitalizado'
    )

    def __str__(self):
        return f"Hospitalización de {self.mascota.nombre} - {self.fechaEntrada}"
