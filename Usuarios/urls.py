from . import views
from django.urls import path

urlpatterns = [
    path('', views.user_login, name='login'),
    path('index/', views.index, name='index'),
    path('usuarios/', views.ver_usuarios, name='ver_usuarios'),
    path('usuarios/agregar/', views.agregar_usuario, name='agregar_usuario'),
    path('usuarios/editar/<int:pk>/', views.editar_usuario, name='editar_usuario'),
    path('usuarios/borrar/<int:pk>/', views.borrar_usuario, name='borrar_usuario'),
]
