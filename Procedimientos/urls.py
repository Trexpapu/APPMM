from . import views
from django.urls import path


urlpatterns = [
    path('indexProcedimientos/', views.indexProcedimientos, name='index-procedimientos'),
    
    path('crear/', views.crear_operacion, name='crear_operacion'),
    path('historial/', views.historial_operaciones, name='historial_operaciones'),
    path('detalle/<int:pk>/', views.detalle_operacion, name='detalle_operacion'),
    path('editar/<int:pk>/', views.editar_operacion, name='editar_operacion'),
    path('eliminar/<int:pk>/', views.eliminar_operacion, name='eliminar_operacion'),
]