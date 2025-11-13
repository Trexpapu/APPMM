from . import views
from django.urls import path


urlpatterns = [
    path('indexConsultas/', views.indexInicioConsultas, name='index-consultas'),
    path('AgendarConsulta/', views.agendar_proxima_consulta, name='agendar-consultas'),
    path('verProximasConsultas/', views.ver_proximas_consultas, name='ver-proximas-consultas'),
    path('borrarProximasConsultas/<int:pk>/', views.borrar_proxima_consulta, name='borrar-proximas-consultas'),
    path('editarProximasConsultas/<int:pk>/', views.editar_proxima_consulta, name='editar-proximas-consultas'),
    path('CrearNuevaConsulta/', views.nueva_consulta, name='nueva-consulta'),
    path('VerConsultas/', views.ver_consultas, name='ver-consultas'),
    # Detalle de consulta
    path('consulta/<int:consulta_id>/', views.detalle_consulta, name='detalle-consulta'),
    # Descargar documento
    path('documento/<int:documento_id>/descargar/', views.descargar_documento, name='descargar_documento'),
    # Generar PDF
    path('consulta/<int:consulta_id>/pdf/', views.generar_pdf_consulta, name='generar_pdf_consulta'),

]