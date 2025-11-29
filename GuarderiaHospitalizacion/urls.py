from . import views
from django.urls import path


urlpatterns = [
    path('indexGuarderiaHospitalizacion/', views.index_guarderia_hospitalizacion, name='index-guarderia-hospitalizacion'),
    path('nuevoServicio/', views.servicio_guarderia_crear, name='servicio_guarderia_crear'),
    path('historialGuarderia/', views.historial_guarderia, name='historial-guarderia'),

    path('editarServicioGuarderia/<int:pk>/', views.servicio_guarderia_editar, name='servicio_guarderia_editar'),

    path('eliminarServicioGuarderia/<int:pk>/', views.servicio_guarderia_crear, name='servicio_guarderia_eliminar'),   

    path('detalleServicioGuarderia/<int:pk>/', views.servicio_guarderia_detalle, name='servicio_guarderia_detalle'),

    path('guarderia/<int:guarderia_id>/pdf/', views.generar_pdf_guarderia, name='generar_pdf_guarderia'),

]
