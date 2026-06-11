from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from core.views import (
    home,
    sistema_dashboard,
    UsuarioViewSet,
    EstudanteViewSet,
    ProfessorViewSet,
    CoordenadorViewSet,
    EmpresaParceiraViewSet,
    HistoricoStatusSolicitacaoViewSet,
    SolicitacaoEstagioViewSet,
    SupervisorEmpresaViewSet,
    DocumentoViewSet,
    PendenciaViewSet,
    RegistroAuditoriaViewSet,
)

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)
router.register(r'estudantes', EstudanteViewSet)
router.register(r'professores', ProfessorViewSet)
router.register(r'coordenadores', CoordenadorViewSet)
router.register(r'empresas', EmpresaParceiraViewSet)
router.register(r'supervisores', SupervisorEmpresaViewSet)
router.register(r'solicitacoes', SolicitacaoEstagioViewSet)
router.register(r'historicos-status', HistoricoStatusSolicitacaoViewSet)
router.register(r'auditoria', RegistroAuditoriaViewSet)
router.register(r'documentos', DocumentoViewSet)
router.register(r'pendencias', PendenciaViewSet)


class DocumentedTokenObtainPairView(TokenObtainPairView):
    @extend_schema(
        summary='Obter token JWT',
        description='Recebe usuário e senha e retorna tokens de acesso e refresh.',
        tags=['Autenticação'],
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class DocumentedTokenRefreshView(TokenRefreshView):
    @extend_schema(
        summary='Renovar token JWT',
        description='Recebe um refresh token válido e retorna um novo access token.',
        tags=['Autenticação'],
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('sistema/', sistema_dashboard, name='sistema_dashboard'),
    path('api/', include(router.urls)),
    path('api/token/', DocumentedTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', DocumentedTokenRefreshView.as_view(), name='token_refresh'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
