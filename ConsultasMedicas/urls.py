from . import views
from django.urls import path


urlpatterns = [
    path('indexConsultas/', views.indexInicioConsultas, name='index-consultas'),
    path('AgendarConsulta/', views.agendar_proxima_consulta, name='agendar-consultas'),
    path('verProximasConsultas/', views.ver_proximas_consultas, name='ver-proximas-consultas'),
]