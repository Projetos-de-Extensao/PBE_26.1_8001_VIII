from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

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
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
