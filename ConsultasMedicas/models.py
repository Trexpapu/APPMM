from django.db import models
from ClientesMascotas.models import Mascotas
from django.contrib.auth.models import User


# Create your models here.
class ConsultasMedicas(models.Model):
    CLINICAS = [
        ('Mascotas Morelia Centro', 'Mascotas Morelia Centro'),
        ('Mascotas Morelia Salida Apatzingán', 'Mascotas Morelia Salida Apatzingán'),
        ('Mascotas Morelia Mano Huevona', 'Mascotas Morelia Mano Huevona'),
    ] 
    
    mascota = models.ForeignKey(Mascotas, on_delete=models.CASCADE)
    motivoConsulta = models.TextField(blank=True)
    temperatura = models.TextField( blank=True)
    pulso = models.TextField(blank=True)
    frecuenciaCardiaca = models.TextField( blank=True)
    puntuacionCorporal = models.TextField(blank=True)
    peso = models.FloatField()
    vacunas = models.TextField(blank=True)  
    alergias = models.TextField(blank=True)
    ultimaDesparasitacion = models.DateField(blank= True, null=True)
    ultimoDesparasitante = models.TextField(blank=True)
    parasitos = models.TextField(blank=True)
    agua = models.TextField(blank=True)
    alimento = models.TextField(blank=True)
    condicionesDeHogar = models.TextField(blank=True)
    ectoparasitos = models.TextField(blank=True)
    pronosticoSignos = models.TextField(blank=True)
    sintomas = models.TextField(blank=True) 
    observaciones = models.TextField(blank=True)
    diagnosticoDiferencial = models.TextField(blank=True) 
    diagnostico = models.TextField(blank=True) 
    tratamiento = models.TextField(blank=True) 
    estudiosHechos = models.TextField(blank=True) 
    estudiosRecomendados = models.TextField(blank=True) 
    evolucion = models.TextField(blank=True)
    fechaConsulta = models.DateTimeField(auto_now_add=True)
    veterinario =  models.ForeignKey(User, on_delete=models.CASCADE)
    clinicaVeterinaria = models.CharField(
        max_length=255,
        choices=CLINICAS,
        default='Mascotas Morelia Centro'  # puedes poner un valor por defecto si quieres
    )

class DocumentosConsulta(models.Model):
    consulta = models.ForeignKey(ConsultasMedicas, on_delete=models.CASCADE)
    archivo = models.FileField(upload_to='consultas/documentos')
    descripcion = models.TextField(blank= True)
    fecha = models.DateTimeField(auto_now_add=True)



class SiguientesConsultas(models.Model):
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
    
    fechaSiguienteConsulta = models.DateTimeField()
    motivoSiguienteConsulta = models.TextField(blank=True)
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
