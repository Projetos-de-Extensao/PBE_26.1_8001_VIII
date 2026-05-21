"""
URL configuration for setup project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
<<<<<<< HEAD

from django.contrib import admin
from django.urls import path, include

from rest_framework.routers import DefaultRouter

from core.views import (
    home,
    UsuarioViewSet,
    EstudanteViewSet,
    ProfessorViewSet,
    CoordenadorViewSet,
    EmpresaParceiraViewSet,
    SolicitacaoEstagioViewSet,
    DocumentoViewSet,
    PendenciaViewSet,
)

from django.conf import settings
from django.conf.urls.static import static


router = DefaultRouter()

router.register(r'usuarios', UsuarioViewSet)
router.register(r'estudantes', EstudanteViewSet)
router.register(r'professores', ProfessorViewSet)
router.register(r'coordenadores', CoordenadorViewSet)
router.register(r'empresas', EmpresaParceiraViewSet)
router.register(r'solicitacoes', SolicitacaoEstagioViewSet)
router.register(r'documentos', DocumentoViewSet)
router.register(r'pendencias', PendenciaViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('api/', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
=======
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
]
>>>>>>> 721beea9b8ef3518ddc1c3c7d237a09c592b88db
