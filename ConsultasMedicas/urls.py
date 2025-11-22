from . import views
from django.urls import path


urlpatterns = [
    path('indexConsultas/', views.indexInicioConsultas, name='index-consultas'),
    path('CrearNuevaConsulta/', views.nueva_consulta, name='nueva-consulta'),
    path('VerConsultas/', views.ver_consultas, name='ver-consultas'),
    # Detalle de consulta
    path('consulta/<int:consulta_id>/', views.detalle_consulta, name='detalle-consulta'),
    # Descargar documento
    path('documento/<int:documento_id>/descargar/', views.descargar_documento, name='descargar_documento'),
    # Generar PDF
    path('consulta/<int:consulta_id>/pdf/', views.generar_pdf_consulta, name='generar_pdf_consulta'),

    path('consulta/<int:consulta_id>/editar/', views.editar_consulta, name='editar_consulta'),
    
    # Eliminar documento
    path('documento/<int:documento_id>/eliminar/', views.eliminar_documento, name='eliminar_documento'),
 
    path('borrarConsultas/<int:pk>/', views.borrar_consulta, name='borrar-consultas'),
]
