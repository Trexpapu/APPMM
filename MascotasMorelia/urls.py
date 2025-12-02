"""
URL configuration for MascotasMorelia project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Rutas de tus apps
    path('', include('ClientesMascotas.urls')),
    path('consultas/', include('ConsultasMedicas.urls')),
    path('agenda/', include('Agenda.urls')),
    path('procedimientos/', include('Procedimientos.urls')),
    path('guarderia-Hospitalizacion/', include('GuarderiaHospitalizacion.urls')),
    path('Estetica/', include('Estetica.urls')),
]

# Solo servir archivos multimedia en modo DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
