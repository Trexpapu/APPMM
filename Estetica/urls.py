from . import views
from django.urls import path


urlpatterns = [
    path('indexEstetica/', views.indexInicioEstetica, name='index-estetica'),
    path('nuevoServicio/', views.servicio_estetica_crear, name='nuevo-servicio-estetica'),
    path('estetica/historial/', views.historial_estetica, name='historial-estetica'),
    path('estetica/<int:pk>/detalle/', views.servicio_estetica_detalle, name='servicio_estetica_detalle'),
    path('estetica/<int:pk>/editar/', views.servicio_estetica_editar, name='servicio_estetica_editar'),
    path('estetica/<int:pk>/eliminar/', views.servicio_estetica_eliminar, name='servicio_estetica_eliminar'),
    path('estetica/<int:pk>/pdf/', views.generar_pdf_estetica, name='generar_pdf_estetica'),
]
