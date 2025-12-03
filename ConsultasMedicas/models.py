from django.db import models
from ClientesMascotas.models import Mascotas
from django.contrib.auth.models import User


# Create your models here.
class ConsultasMedicas(models.Model):
    CLINICAS = [
        ('Mascotas Morelia Centro (Samuel Castañon Pte. 73 Centro 60600 Apatzingán, Mich. Número 453-227-1694)', 'Mascotas Morelia Centro (Samuel Castañon Pte. 73 Centro 60600 Apatzingán, Mich. Número 453-227-1694)'),
    ] 
    PROCEDIMIENTOS = [
        ('Consulta', 'Consulta'),
        ('Seguimiento', 'Seguimiento'),
        ('Cirugia', 'Cirugia'),

    ]
    PUNTUACION = [
        ('1/5', '1/5'),
        ('2/5', '2/5'),
        ('3/5', '3/5'),
        ('4/5', '4/5'),
        ('5/5', '5/5'),

    ]

    MUCOSAS = [
        ('ROSADAS', 'ROSADAS'),
        ('CONGESTIONADAS', 'CONGESTIONADAS'),
        ('CIANOTICAS', 'CIANOTICAS'),
        ('PALIDAS', 'PALIDAS'),
        ('ICTERICAS', 'ICTERICAS'),

        ('NORMOCROMICAS', 'NORMOCROMICAS'),
        ('HIPOCROMICAS', 'HIPOCROMICAS'),
        ('SECAS', 'SECAS'),
        ('HUMEDAS', 'HUMEDAS'),
        ('TURGENTES', 'TURGENTES'),

        ('HIPERTROFICAS', 'HIPERTROFICAS'),
        ('ATROFICAS', 'ATROFICAS'),
        ('ULCERADAS', 'ULCERADAS'),
        ('HEMORRAGICAS', 'HEMORRAGICAS'),
        ('PETEQUIALES', 'PETEQUIALES'),

        ('ECCHIMOTICAS', 'ECCHIMOTICAS'),
        ('EDEMATOSAS', 'EDEMATOSAS'),
        ('FISURADAS', 'FISURADAS'),
        ('FIBRINOSAS', 'FIBRINOSAS'),
        ('PURULENTAS', 'PURULENTAS'),

        ('NECROTICAS', 'NECROTICAS'),
        ('GRANULOMATOSAS', 'GRANULOMATOSAS'),
        ('PIGMENTADAS', 'PIGMENTADAS'),
        ('DESCAMATIVAS', 'DESCAMATIVAS'),
        ('LACERADAS', 'LACERADAS'),

        ('ABRASIONADAS', 'ABRASIONADAS'),
        ('CONTUSIONADAS', 'CONTUSIONADAS'),
        ('PUNCTIFORMES', 'PUNCTIFORMES'),
        ('LINEALES', 'LINEALES'),
        ('ESTRELLADAS', 'ESTRELLADAS'),

        ('IRREGULARES', 'IRREGULARES'),
        ('REGULARES', 'REGULARES'),
        ('SIMETRICAS', 'SIMETRICAS'),
        ('ASIMETRICAS', 'ASIMETRICAS'),
        ('DIFUSAS', 'DIFUSAS'),

        ('LOCALIZADAS', 'LOCALIZADAS'),
        ('GENERALIZADAS', 'GENERALIZADAS'),
        ('UNILATERALES', 'UNILATERALES'),
        ('BILATERALES', 'BILATERALES'),
        ('MULTIFOCALES', 'MULTIFOCALES'),

        ('FOCALES', 'FOCALES'),
        ('CONFLUENTES', 'CONFLUENTES'),
        ('DISCRETAS', 'DISCRETAS'),
        ('PROFUNDAS', 'PROFUNDAS'),
        ('SUPERFICIALES', 'SUPERFICIALES'),

        ('AGUDAS', 'AGUDAS'),
        ('CRONICAS', 'CRONICAS'),
        ('RECURRENTES', 'RECURRENTES'),
        ('PERSISTENTES', 'PERSISTENTES'),
        ('PROGRESIVAS', 'PROGRESIVAS'),

        ('REGRESIVAS', 'REGRESIVAS'),
        ('ESTABLES', 'ESTABLES'),
        ('INESTABLES', 'INESTABLES'),
        ('REVERSIBLES', 'REVERSIBLES'),
        ('IRREVERSIBLES', 'IRREVERSIBLES'),

        ('BENIGNAS', 'BENIGNAS'),
        ('MALIGNAS', 'MALIGNAS'),
        ('PRIMARIAS', 'PRIMARIAS'),
        ('SECUNDARIAS', 'SECUNDARIAS'),
        ('IDIOPATICAS', 'IDIOPATICAS'),

        ('TRAUMATICAS', 'TRAUMATICAS'),
        ('INFECCIOSAS', 'INFECCIOSAS'),
        ('INFLAMATORIAS', 'INFLAMATORIAS'),
        ('DEGENERATIVAS', 'DEGENERATIVAS'),
        ('CONGENITAS', 'CONGENITAS'),

        ('ADQUIRIDAS', 'ADQUIRIDAS'),
        ('HEREDITARIAS', 'HEREDITARIAS'),
        ('ESPORADICAS', 'ESPORADICAS'),
        ('ENDEMICAS', 'ENDEMICAS'),
        ('EPIDEMICAS', 'EPIDEMICAS'),

        ('PANDEMICAS', 'PANDEMICAS'),
        ('ZOONOTICAS', 'ZOONOTICAS'),
        ('ANTHROPONOTICAS', 'ANTHROPONOTICAS'),
        ('VECTORIALES', 'VECTORIALES'),
        ('CONTAGIOSAS', 'CONTAGIOSAS'),

        ('NO_CONTAGIOSAS', 'NO CONTAGIOSAS'),
        ('TRANSMISIBLES', 'TRANSMISIBLES'),
        ('NO_TRANSMISIBLES', 'NO TRANSMISIBLES'),
        ('CURABLES', 'CURABLES'),
        ('INCURABLES', 'INCURABLES'),

        ('MANEJABLES', 'MANEJABLES'),
        ('NO_MANEJABLES', 'NO MANEJABLES'),
        ('PREVENIBLES', 'PREVENIBLES'),
        ('NO_PREVENIBLES', 'NO PREVENIBLES'),
        ('DIAGNOSTICABLES', 'DIAGNOSTICABLES'),

        ('NO_DIAGNOSTICABLES', 'NO DIAGNOSTICABLES'),
        ('TRATABLES', 'TRATABLES'),
        ('NO_TRATABLES', 'NO TRATABLES'),
        ('MONITORIZABLES', 'MONITORIZABLES'),
        ('NO_MONITORIZABLES', 'NO MONITORIZABLES'),

        ('PREDICTIBLES', 'PREDICTIBLES'),
        ('NO_PREDICTIBLES', 'NO PREDICTIBLES'),
        ('CONTROLABLES', 'CONTROLABLES'),
        ('NO_CONTROLABLES', 'NO CONTROLABLES'),

        ('REVERSIBLES_TEMPORALMENTE', 'REVERSIBLES TEMPORALMENTE'),
        ('IRREVERSIBLES_PERMANENTES', 'IRREVERSIBLES PERMANENTES'),
        ('PROGRESIVAS_RAPIDAS', 'PROGRESIVAS RAPIDAS'),
        ('PROGRESIVAS_LENTAS', 'PROGRESIVAS LENTAS'),
        ('ESTABLES_LONGITUDINALES', 'ESTABLES LONGITUDINALES'),

        ('INESTABLES_FLUCTUANTES', 'INESTABLES FLUCTUANTES'),
    ]

    
    mascota = models.ForeignKey(Mascotas, on_delete=models.CASCADE)
    anamnesicos = models.TextField(blank=True)
    procedimiento = models.CharField(
        max_length=255,
        choices=PROCEDIMIENTOS,
        default='Consulta'  # puedes poner un valor por defecto si quieres
    )
    mucosas = models.CharField(
        max_length=1500,
        choices=MUCOSAS,
        default='ROSADAS'
    )

    porcentajeHidratacion = models.TextField( blank=True)
    actitudConPropietario = models.TextField( blank=True)
    actitudConVeterinario = models.TextField( blank=True)
    temperatura = models.TextField( blank=True)
    pulso = models.TextField(blank=True)
    frecuenciaCardiaca = models.TextField( blank=True)
    frecuenciaRespiratoria = models.TextField( blank=True)
    puntuacionCorporal = models.CharField(
        max_length=255,
        choices=PUNTUACION,
        default='1/5'
    )
    examanesFisicosRealizados = models.TextField(blank=True)
    peso = models.FloatField()
    vacunas = models.TextField(blank=True)  
    alergias = models.TextField(blank=True)
    ultimaDesparasitacion = models.DateField(blank= True, null=True)
    ultimoDesparasitante = models.TextField(blank=True)
    alimento = models.TextField(blank=True)
    parasitos = models.TextField(blank=True)
    ectoparasitos = models.TextField(blank=True)
    pronostico = models.TextField(blank=True)
    observaciones = models.TextField(blank=True)
    listaPosiblesProblemas = models.TextField(blank=True)
    listaProblemasReales = models.TextField(blank=True)
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
        default='Mascotas Morelia Centro (Samuel Castañon Pte. 73 Centro 60600 Apatzingán, Mich. Número 453-227-1694)'  # puedes poner un valor por defecto si quieres
    )

class DocumentosConsulta(models.Model):
    consulta = models.ForeignKey(ConsultasMedicas, on_delete=models.CASCADE)
    archivo = models.FileField(upload_to='consultas/documentos')
    descripcion = models.TextField(blank= True)
    fecha = models.DateTimeField(auto_now_add=True)



