from . import views
from django.urls import path


urlpatterns = [
    path('index/', views.index, name='index'),
    path('index-cliente/', views.indexClientes, name='indexCliente'),
    path('index-mascota/', views.indexMascotas, name='indexMascota'),
    path('ver-clientes/', views.ver_clientes, name='ver_clientes'),
    path('agregar-cliente/', views.agregar_cliente, name='agregar_cliente'),
    path('editar-cliente/<int:pk>/', views.editar_cliente, name='editar_cliente'),
    path('borrar-cliente/<int:pk>/', views.borrar_cliente, name='borrar_cliente'),
    path('ver-mascotas/', views.ver_mascotas, name='ver_mascotas'),
    path('agregar-mascota/', views.agregar_mascota, name='agregar_mascota'),
    path('editar-mascota/<int:pk>/', views.editar_mascota, name='editar_mascota'),
    path('borrar-mascota/<int:pk>/', views.borrar_mascota, name='borrar_mascota'),
    path('', views.user_login, name='login'),
]