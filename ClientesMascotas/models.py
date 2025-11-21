from django.db import models


# Create your models here.
class Clientes(models.Model):
    nombre = models.CharField(max_length=255)
    email = models.EmailField(unique=True, blank = True)
    telefono = models.CharField(max_length=20, unique = True)
    direccion = models.TextField(blank=True)

class Mascotas(models.Model):
    SEXOS = [
        ('macho', 'macho'),
        ('hembra', 'hembra'),
    ] 
    cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=255)
    especie = models.CharField(max_length=255)
    raza = models.CharField(max_length=255)
    fechaNacimiento = models.DateField()
    peso = models.FloatField()
    vacunas = models.TextField(blank=True)  
    ultimaDesparasitacion = models.DateField(blank= True, null=True)
    ultimoDesparasitante = models.TextField(blank=True)
    alergias = models.TextField(blank=True)
    vive = models.BooleanField(default=True)
    sexo = models.CharField(
        max_length=20,
        choices=SEXOS,
        default='macho'  # puedes poner un valor por defecto si quieres
    )