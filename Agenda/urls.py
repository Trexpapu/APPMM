from . import views
from django.urls import path


urlpatterns = [
    path('indexAgenda/', views.indexAgenda, name='index-agenda'),
    path('agendarCita/', views.agendar_proxima_cita, name='agendar-cita'),
    path('verProximasCitas/', views.ver_proximas_citas, name='ver-proximas-citas'),
    path('borrarProximasCitas/<int:pk>/', views.borrar_proxima_cita, name='borrar-proximas-citas'),
    path('editarProximasCitas/<int:pk>/', views.editar_proxima_cita, name='editar-proximas-citas'),
]
