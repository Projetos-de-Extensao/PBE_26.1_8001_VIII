from django.http import HttpResponse

from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .auditoria import registrar_auditoria
from .models import (
    Coordenador,
    Documento,
    EmpresaParceira,
    Estudante,
    HistoricoStatusSolicitacao,
    Pendencia,
    Professor,
    RegistroAuditoria,
    SolicitacaoEstagio,
    SupervisorEmpresa,
    Usuario,
)
from .permissions import (
    DocumentoActionPermission,
    IsCoordenador,
    IsEstudante,
    IsProfessor,
    IsSolicitacaoOwnerOrStaffProfile,
    PendenciaActionPermission,
    SolicitacaoEstagioActionPermission,
)
from .serializers import (
    CoordenadorSerializer,
    DocumentoSerializer,
    EmpresaParceiraSerializer,
    EstudanteSerializer,
    HistoricoStatusSolicitacaoSerializer,
    PendenciaSerializer,
    ProfessorSerializer,
    RegistroAuditoriaSerializer,
    SolicitacaoEstagioSerializer,
    SupervisorEmpresaSerializer,
    UsuarioSerializer,
)

def home(request):
    return HttpResponse("API de Estágios Funcionando")

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated, IsCoordenador]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering_fields = ['id', 'username', 'email', 'first_name', 'last_name']
    ordering = ['id']

class EstudanteViewSet(viewsets.ModelViewSet):
    queryset = Estudante.objects.select_related('usuario').all()
    serializer_class = EstudanteSerializer
    permission_classes = [IsAuthenticated, IsEstudante]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['usuario__username', 'usuario__email', 'usuario__first_name', 'usuario__last_name']
    ordering_fields = ['id', 'usuario__username', 'usuario__email']
    ordering = ['id']

class ProfessorViewSet(viewsets.ModelViewSet):
    queryset = Professor.objects.select_related('usuario').all()
    serializer_class = ProfessorSerializer
    permission_classes = [IsAuthenticated, IsProfessor]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['usuario__username', 'usuario__email', 'usuario__first_name', 'usuario__last_name']
    ordering_fields = ['id', 'usuario__username', 'usuario__email']
    ordering = ['id']

class CoordenadorViewSet(viewsets.ModelViewSet):
    queryset = Coordenador.objects.select_related('usuario').all()
    serializer_class = CoordenadorSerializer
    permission_classes = [IsAuthenticated, IsCoordenador]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['usuario__username', 'usuario__email', 'usuario__first_name', 'usuario__last_name']
    ordering_fields = ['id', 'usuario__username', 'usuario__email']
    ordering = ['id']

class EmpresaParceiraViewSet(viewsets.ModelViewSet):
    queryset = EmpresaParceira.objects.all()
    serializer_class = EmpresaParceiraSerializer
    permission_classes = [IsAuthenticated, IsCoordenador]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['nome_organizacao', 'cnpj']
    ordering_fields = ['id', 'nome_organizacao', 'cnpj']
    ordering = ['nome_organizacao']


class SupervisorEmpresaViewSet(viewsets.ModelViewSet):
    queryset = SupervisorEmpresa.objects.select_related('empresa').all()
    serializer_class = SupervisorEmpresaSerializer
    permission_classes = [IsAuthenticated, IsCoordenador]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['nome', 'email', 'telefone', 'cargo', 'empresa__nome_organizacao']
    ordering_fields = ['id', 'nome', 'email', 'empresa__nome_organizacao', 'ativo']
    ordering = ['nome']


class SolicitacaoEstagioViewSet(viewsets.ModelViewSet):
    queryset = SolicitacaoEstagio.objects.select_related(
        'estudante__usuario',
        'empresa',
    ).all()
    serializer_class = SolicitacaoEstagioSerializer
    permission_classes = [
        IsAuthenticated,
        SolicitacaoEstagioActionPermission,
        IsSolicitacaoOwnerOrStaffProfile,
    ]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = [
        'estudante__usuario__username',
        'estudante__usuario__email',
        'estudante__usuario__first_name',
        'estudante__usuario__last_name',
        'empresa__nome_organizacao',
        'empresa__cnpj',
        'status_atual',
        'supervisor',
        'duracao_contrato',
    ]
    ordering_fields = [
        'id',
        'data_abertura',
        'status_atual',
        'score_conformidade',
        'carga_horaria',
        'duracao_contrato',
        'seguro_obrigatorio',
        'empresa__nome_organizacao',
        'estudante__usuario__username',
    ]
    ordering = ['-data_abertura', '-id']

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        if hasattr(user, 'coordenador_profile') or hasattr(user, 'professor_profile'):
            return queryset

        if hasattr(user, 'estudante_profile'):
            return queryset.filter(estudante=user.estudante_profile)

        return queryset.none()

    def perform_create(self, serializer):
        if hasattr(self.request.user, 'estudante_profile'):
            solicitacao = serializer.save(estudante=self.request.user.estudante_profile)
            registrar_auditoria(
                self.request.user,
                'CRIACAO',
                'SolicitacaoEstagio',
                solicitacao.id,
                'Solicitação de estágio criada.',
            )
            return

        solicitacao = serializer.save()
        registrar_auditoria(
            self.request.user,
            'CRIACAO',
            'SolicitacaoEstagio',
            solicitacao.id,
            'Solicitação de estágio criada.',
        )

class DocumentoViewSet(viewsets.ModelViewSet):
    queryset = Documento.objects.select_related(
        'solicitacao__estudante__usuario',
        'solicitacao__empresa',
    ).all()
    serializer_class = DocumentoSerializer
    permission_classes = [
        IsAuthenticated,
        DocumentoActionPermission,
        IsSolicitacaoOwnerOrStaffProfile,
    ]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = [
        'tipo',
        'status',
        'solicitacao__empresa__nome_organizacao',
        'solicitacao__estudante__usuario__username',
        'solicitacao__estudante__usuario__email',
    ]
    ordering_fields = ['id', 'tipo', 'status', 'data_envio', 'solicitacao__id']
    ordering = ['-data_envio', '-id']

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        if hasattr(user, 'coordenador_profile') or hasattr(user, 'professor_profile'):
            return queryset

        if hasattr(user, 'estudante_profile'):
            return queryset.filter(solicitacao__estudante=user.estudante_profile)

        return queryset.none()

    def perform_create(self, serializer):
        solicitacao = serializer.validated_data.get('solicitacao')

        if (
            hasattr(self.request.user, 'estudante_profile')
            and solicitacao.estudante_id != self.request.user.estudante_profile.id
        ):
            raise PermissionDenied('Você não pode enviar documento para solicitação de outro estudante.')

        serializer.save()


class HistoricoStatusSolicitacaoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = HistoricoStatusSolicitacao.objects.select_related(
        'solicitacao__estudante__usuario',
        'solicitacao__empresa',
        'alterado_por',
    ).all()
    serializer_class = HistoricoStatusSolicitacaoSerializer
    permission_classes = [
        IsAuthenticated,
        SolicitacaoEstagioActionPermission,
        IsSolicitacaoOwnerOrStaffProfile,
    ]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = [
        'solicitacao__estudante__usuario__username',
        'solicitacao__empresa__nome_organizacao',
        'status_anterior',
        'status_novo',
        'alterado_por__username',
        'observacao',
    ]
    ordering_fields = ['id', 'data_alteracao', 'status_anterior', 'status_novo', 'solicitacao__id']
    ordering = ['-data_alteracao', '-id']

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        if hasattr(user, 'coordenador_profile') or hasattr(user, 'professor_profile'):
            return queryset

        if hasattr(user, 'estudante_profile'):
            return queryset.filter(solicitacao__estudante=user.estudante_profile)

        return queryset.none()


class RegistroAuditoriaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = RegistroAuditoria.objects.select_related('usuario').all()
    serializer_class = RegistroAuditoriaSerializer
    permission_classes = [IsAuthenticated, IsCoordenador]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['acao', 'recurso', 'objeto_id', 'descricao', 'usuario__username', 'usuario__email']
    ordering_fields = ['id', 'acao', 'recurso', 'objeto_id', 'data_criacao']
    ordering = ['-data_criacao', '-id']


class PendenciaViewSet(viewsets.ModelViewSet):
    queryset = Pendencia.objects.select_related(
        'solicitacao__estudante__usuario',
        'solicitacao__empresa',
    ).all()
    serializer_class = PendenciaSerializer
    permission_classes = [
        IsAuthenticated,
        PendenciaActionPermission,
        IsSolicitacaoOwnerOrStaffProfile,
    ]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = [
        'descricao',
        'estado_resolucao',
        'solicitacao__empresa__nome_organizacao',
        'solicitacao__estudante__usuario__username',
        'solicitacao__estudante__usuario__email',
    ]
    ordering_fields = ['id', 'data_criacao', 'estado_resolucao', 'solicitacao__id']
    ordering = ['-data_criacao', '-id']

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        if hasattr(user, 'coordenador_profile') or hasattr(user, 'professor_profile'):
            return queryset

        if hasattr(user, 'estudante_profile'):
            return queryset.filter(solicitacao__estudante=user.estudante_profile)

        return queryset.none()

    def perform_create(self, serializer):
        pendencia = serializer.save()
        solicitacao = pendencia.solicitacao
        registrar_auditoria(
            self.request.user,
            'PENDENCIA',
            'Pendencia',
            pendencia.id,
            f'Pendência criada para solicitação {solicitacao.id}.',
        )

        if solicitacao.status_atual == 'EM_ANALISE':
            status_anterior = solicitacao.status_atual
            solicitacao.status_atual = 'PENDENTE'
            solicitacao.save(update_fields=['status_atual'])

            HistoricoStatusSolicitacao.objects.create(
                solicitacao=solicitacao,
                status_anterior=status_anterior,
                status_novo='PENDENTE',
                alterado_por=self.request.user,
                observacao=pendencia.descricao,
            )

    def perform_update(self, serializer):
        pendencia = serializer.save()
        registrar_auditoria(
            self.request.user,
            'PENDENCIA',
            'Pendencia',
            pendencia.id,
            f'Pendência atualizada para {pendencia.estado_resolucao}.',
        )

