from . import views
from django.urls import path


urlpatterns = [
    path('indexProcedimientos/', views.indexProcedimientos, name='index-procedimientos'),

    path('operacion/crear/', views.crear_operacion, name='crear_operacion'),
    path('operacion/historial/', views.historial_operaciones, name='historial_operaciones'),
    path('operacion/detalle/<int:pk>/', views.detalle_operacion, name='detalle_operacion'),
    path('operacion/editar/<int:pk>/', views.editar_operacion, name='editar_operacion'),
    path('operacion/eliminar/<int:pk>/', views.eliminar_operacion, name='eliminar_operacion'),




    
    path('vacunas/', views.indexVacunas, name='index_vacunas'),
    path('vacunas/lista', views.lista_vacunas, name='lista_vacunas'),
    path('vacunas/agregar/', views.agregar_vacuna, name='agregar_vacuna'),
    path('vacunas/editar/<int:pk>/', views.editar_vacuna, name='editar_vacuna'),
    path('vacunas/eliminar/<int:pk>/', views.eliminar_vacuna, name='eliminar_vacuna'),


    path('vacunacion/crear/', views.nueva_vacunacion, name='nueva_vacunacion'),
    path('vacunacion/historial/', views.historial_vacunaciones, name='historial_vacunaciones'),
    
    path('vacunacion/editar/<int:pk>/', views.editar_vacunacion, name='editar_vacunacion'), 
    path('vacunacion/eliminar/<int:pk>/', views.eliminar_vacunacion, name='eliminar_vacunacion'),

    path('desparasitantes/', views.indexDesparasitantes, name='index_desparasitantes'),
    path('desparasitantes/lista', views.lista_desparasitantes, name='lista_desparasitantes'),
    path('desparasitantes/crear', views.agregar_desparasitante, name='agregar_desparasitante'),
    path('desparasitantes/editar/<int:pk>/', views.editar_desparasitante, name='editar_desparasitante'),
    path('desparasitantes/eliminar/<int:pk>/', views.eliminar_desparasitante, name='eliminar_desparasitante'),

    path('desparasitacion/historial/', views.historial_desparasitaciones, name='historial_desparasitaciones'),
    path('desparasitacion/crear/', views.nueva_desparasitacion, name='nueva_desparasitacion'),
    path('desparasitacion/eliminar/<int:pk>/', views.eliminar_desparasitacion, name='eliminar_desparasitacion'),
]
