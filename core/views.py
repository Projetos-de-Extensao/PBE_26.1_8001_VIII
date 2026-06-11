from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import redirect, render

from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view

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
    return redirect('sistema_dashboard')


def sistema_dashboard(request):
    if request.method == 'POST':
        action = request.POST.get('action')

        try:
            if action == 'criar_estudante':
                nome = request.POST.get('nome', '').strip()
                email = request.POST.get('email', '').strip()
                username = request.POST.get('username', '').strip() or email
                curso = request.POST.get('curso', '').strip()
                matricula = request.POST.get('matricula', '').strip()

                if not nome or not email:
                    messages.error(request, 'Informe nome e e-mail para cadastrar o estudante.')
                else:
                    first_name, *last_name = nome.split()
                    usuario, created = get_user_model().objects.get_or_create(
                        username=username,
                        defaults={
                            'email': email,
                            'first_name': first_name,
                            'last_name': ' '.join(last_name),
                        },
                    )
                    if created:
                        usuario.set_password('123456')
                        usuario.save()

                    Estudante.objects.get_or_create(
                        usuario=usuario,
                        defaults={
                            'curso': curso,
                            'matricula': matricula or None,
                            'elegivel_estagio': True,
                        },
                    )
                    messages.success(request, 'Estudante cadastrado para demonstracao.')

            elif action == 'criar_empresa':
                nome = request.POST.get('nome_organizacao', '').strip()
                cnpj = request.POST.get('cnpj', '').strip()
                supervisor = request.POST.get('supervisor', '').strip()

                if not nome or not cnpj:
                    messages.error(request, 'Informe nome e CNPJ para cadastrar a empresa.')
                else:
                    EmpresaParceira.objects.get_or_create(
                        cnpj=cnpj,
                        defaults={
                            'nome_organizacao': nome,
                            'supervisor': supervisor,
                        },
                    )
                    messages.success(request, 'Empresa parceira cadastrada.')

            elif action == 'criar_solicitacao':
                estudante_id = request.POST.get('estudante')
                empresa_id = request.POST.get('empresa')
                carga_horaria = request.POST.get('carga_horaria') or 30
                duracao_contrato = request.POST.get('duracao_contrato', '').strip() or '6 meses'
                supervisor = request.POST.get('supervisor', '').strip() or 'Supervisor nao informado'
                seguro_obrigatorio = request.POST.get('seguro_obrigatorio') == 'on'

                if not estudante_id or not empresa_id:
                    messages.error(request, 'Selecione estudante e empresa para criar a solicitacao.')
                else:
                    SolicitacaoEstagio.objects.create(
                        estudante_id=estudante_id,
                        empresa_id=empresa_id,
                        carga_horaria=carga_horaria,
                        duracao_contrato=duracao_contrato,
                        supervisor=supervisor,
                        seguro_obrigatorio=seguro_obrigatorio,
                    )
                    messages.success(request, 'Solicitacao de estagio criada com status ABERTO.')

            elif action == 'atualizar_status':
                solicitacao_id = request.POST.get('solicitacao')
                status = request.POST.get('status_atual')
                justificativa = request.POST.get('justificativa_recusa', '').strip()

                solicitacao = SolicitacaoEstagio.objects.get(id=solicitacao_id)
                solicitacao.status_atual = status
                solicitacao.justificativa_recusa = justificativa
                solicitacao.save(update_fields=['status_atual', 'justificativa_recusa'])
                messages.success(request, 'Status da solicitacao atualizado.')

            elif action == 'criar_documento':
                solicitacao_id = request.POST.get('solicitacao')
                tipo = request.POST.get('tipo', '').strip()
                arquivo = request.FILES.get('arquivo')

                if not solicitacao_id or not tipo:
                    messages.error(request, 'Informe solicitacao e tipo do documento.')
                else:
                    Documento.objects.create(
                        solicitacao_id=solicitacao_id,
                        tipo=tipo,
                        arquivo=arquivo,
                    )
                    messages.success(request, 'Documento registrado na solicitacao.')

            elif action == 'criar_pendencia':
                solicitacao_id = request.POST.get('solicitacao')
                descricao = request.POST.get('descricao', '').strip()

                if not solicitacao_id or not descricao:
                    messages.error(request, 'Informe solicitacao e descricao da pendencia.')
                else:
                    Pendencia.objects.create(
                        solicitacao_id=solicitacao_id,
                        descricao=descricao,
                    )
                    SolicitacaoEstagio.objects.filter(id=solicitacao_id).update(status_atual='PENDENTE')
                    messages.success(request, 'Pendencia criada e solicitacao marcada como PENDENTE.')

        except Exception as exc:
            messages.error(request, f'Nao foi possivel concluir a acao: {exc}')

        return redirect('sistema_dashboard')

    solicitacoes = (
        SolicitacaoEstagio.objects
        .select_related('estudante__usuario', 'empresa')
        .prefetch_related('documentos', 'pendencias')
        .order_by('-id')
    )
    estudantes = Estudante.objects.select_related('usuario').order_by('usuario__first_name')
    empresas = EmpresaParceira.objects.order_by('nome_organizacao')
    documentos = Documento.objects.select_related('solicitacao').order_by('-id')[:8]
    pendencias = Pendencia.objects.select_related('solicitacao').order_by('-id')[:8]

    context = {
        'estudantes': estudantes,
        'empresas': empresas,
        'solicitacoes': solicitacoes,
        'documentos': documentos,
        'pendencias': pendencias,
        'status_choices': SolicitacaoEstagio.STATUS_CHOICES,
        'total_estudantes': estudantes.count(),
        'total_empresas': empresas.count(),
        'total_solicitacoes': solicitacoes.count(),
        'total_pendencias_abertas': Pendencia.objects.filter(estado_resolucao='ABERTA').count(),
    }
    return render(request, 'home.html', context)

@extend_schema_view(
    list=extend_schema(summary='Listar usuários', tags=['Usuários e Perfis']),
    retrieve=extend_schema(summary='Detalhar usuário', tags=['Usuários e Perfis']),
    create=extend_schema(summary='Criar usuário', tags=['Usuários e Perfis']),
    update=extend_schema(summary='Atualizar usuário', tags=['Usuários e Perfis']),
    partial_update=extend_schema(summary='Atualizar parcialmente usuário', tags=['Usuários e Perfis']),
    destroy=extend_schema(summary='Remover usuário', tags=['Usuários e Perfis']),
)
class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated, IsCoordenador]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering_fields = ['id', 'username', 'email', 'first_name', 'last_name']
    ordering = ['id']

@extend_schema_view(
    list=extend_schema(summary='Listar estudantes', tags=['Usuários e Perfis']),
    retrieve=extend_schema(summary='Detalhar estudante', tags=['Usuários e Perfis']),
    create=extend_schema(summary='Criar estudante', tags=['Usuários e Perfis']),
    update=extend_schema(summary='Atualizar estudante', tags=['Usuários e Perfis']),
    partial_update=extend_schema(summary='Atualizar parcialmente estudante', tags=['Usuários e Perfis']),
    destroy=extend_schema(summary='Remover estudante', tags=['Usuários e Perfis']),
)
class EstudanteViewSet(viewsets.ModelViewSet):
    queryset = Estudante.objects.select_related('usuario').all()
    serializer_class = EstudanteSerializer
    permission_classes = [IsAuthenticated, IsEstudante]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['usuario__username', 'usuario__email', 'usuario__first_name', 'usuario__last_name']
    ordering_fields = ['id', 'usuario__username', 'usuario__email']
    ordering = ['id']

@extend_schema_view(
    list=extend_schema(summary='Listar professores', tags=['Usuários e Perfis']),
    retrieve=extend_schema(summary='Detalhar professor', tags=['Usuários e Perfis']),
    create=extend_schema(summary='Criar professor', tags=['Usuários e Perfis']),
    update=extend_schema(summary='Atualizar professor', tags=['Usuários e Perfis']),
    partial_update=extend_schema(summary='Atualizar parcialmente professor', tags=['Usuários e Perfis']),
    destroy=extend_schema(summary='Remover professor', tags=['Usuários e Perfis']),
)
class ProfessorViewSet(viewsets.ModelViewSet):
    queryset = Professor.objects.select_related('usuario').all()
    serializer_class = ProfessorSerializer
    permission_classes = [IsAuthenticated, IsProfessor]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['usuario__username', 'usuario__email', 'usuario__first_name', 'usuario__last_name']
    ordering_fields = ['id', 'usuario__username', 'usuario__email']
    ordering = ['id']

@extend_schema_view(
    list=extend_schema(summary='Listar coordenadores', tags=['Usuários e Perfis']),
    retrieve=extend_schema(summary='Detalhar coordenador', tags=['Usuários e Perfis']),
    create=extend_schema(summary='Criar coordenador', tags=['Usuários e Perfis']),
    update=extend_schema(summary='Atualizar coordenador', tags=['Usuários e Perfis']),
    partial_update=extend_schema(summary='Atualizar parcialmente coordenador', tags=['Usuários e Perfis']),
    destroy=extend_schema(summary='Remover coordenador', tags=['Usuários e Perfis']),
)
class CoordenadorViewSet(viewsets.ModelViewSet):
    queryset = Coordenador.objects.select_related('usuario').all()
    serializer_class = CoordenadorSerializer
    permission_classes = [IsAuthenticated, IsCoordenador]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['usuario__username', 'usuario__email', 'usuario__first_name', 'usuario__last_name']
    ordering_fields = ['id', 'usuario__username', 'usuario__email']
    ordering = ['id']

@extend_schema_view(
    list=extend_schema(summary='Listar empresas parceiras', tags=['Empresas']),
    retrieve=extend_schema(summary='Detalhar empresa parceira', tags=['Empresas']),
    create=extend_schema(summary='Cadastrar empresa parceira', tags=['Empresas']),
    update=extend_schema(summary='Atualizar empresa parceira', tags=['Empresas']),
    partial_update=extend_schema(summary='Atualizar parcialmente empresa parceira', tags=['Empresas']),
    destroy=extend_schema(summary='Remover empresa parceira', tags=['Empresas']),
)
class EmpresaParceiraViewSet(viewsets.ModelViewSet):
    queryset = EmpresaParceira.objects.all()
    serializer_class = EmpresaParceiraSerializer
    permission_classes = [IsAuthenticated, IsCoordenador]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['nome_organizacao', 'cnpj']
    ordering_fields = ['id', 'nome_organizacao', 'cnpj']
    ordering = ['nome_organizacao']


@extend_schema_view(
    list=extend_schema(summary='Listar supervisores de empresa', tags=['Empresas']),
    retrieve=extend_schema(summary='Detalhar supervisor de empresa', tags=['Empresas']),
    create=extend_schema(summary='Cadastrar supervisor de empresa', tags=['Empresas']),
    update=extend_schema(summary='Atualizar supervisor de empresa', tags=['Empresas']),
    partial_update=extend_schema(summary='Atualizar parcialmente supervisor de empresa', tags=['Empresas']),
    destroy=extend_schema(summary='Remover supervisor de empresa', tags=['Empresas']),
)
class SupervisorEmpresaViewSet(viewsets.ModelViewSet):
    queryset = SupervisorEmpresa.objects.select_related('empresa').all()
    serializer_class = SupervisorEmpresaSerializer
    permission_classes = [IsAuthenticated, IsCoordenador]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['nome', 'email', 'telefone', 'cargo', 'empresa__nome_organizacao']
    ordering_fields = ['id', 'nome', 'email', 'empresa__nome_organizacao', 'ativo']
    ordering = ['nome']


@extend_schema_view(
    list=extend_schema(
        summary='Listar solicitações de estágio',
        description='Estudantes visualizam apenas suas próprias solicitações. Professores e coordenadores visualizam todas.',
        tags=['Solicitações'],
    ),
    retrieve=extend_schema(summary='Detalhar solicitação de estágio', tags=['Solicitações']),
    create=extend_schema(summary='Criar solicitação de estágio', tags=['Solicitações']),
    update=extend_schema(summary='Atualizar solicitação de estágio', tags=['Solicitações']),
    partial_update=extend_schema(
        summary='Atualizar parcialmente solicitação de estágio',
        description='Usado também para transições de status, como EM_ANALISE, APROVADO, RECUSADO e PENDENTE.',
        tags=['Solicitações'],
    ),
    destroy=extend_schema(summary='Remover solicitação de estágio', tags=['Solicitações']),
)
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

@extend_schema_view(
    list=extend_schema(summary='Listar documentos', tags=['Documentos']),
    retrieve=extend_schema(summary='Detalhar documento', tags=['Documentos']),
    create=extend_schema(summary='Enviar documento', tags=['Documentos']),
    update=extend_schema(summary='Atualizar documento', tags=['Documentos']),
    partial_update=extend_schema(summary='Atualizar parcialmente documento', tags=['Documentos']),
    destroy=extend_schema(summary='Remover documento', tags=['Documentos']),
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


@extend_schema_view(
    list=extend_schema(summary='Listar histórico de status', tags=['Solicitações']),
    retrieve=extend_schema(summary='Detalhar registro de histórico de status', tags=['Solicitações']),
)
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


@extend_schema_view(
    list=extend_schema(summary='Listar registros de auditoria', tags=['Auditoria']),
    retrieve=extend_schema(summary='Detalhar registro de auditoria', tags=['Auditoria']),
)
class RegistroAuditoriaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = RegistroAuditoria.objects.select_related('usuario').all()
    serializer_class = RegistroAuditoriaSerializer
    permission_classes = [IsAuthenticated, IsCoordenador]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['acao', 'recurso', 'objeto_id', 'descricao', 'usuario__username', 'usuario__email']
    ordering_fields = ['id', 'acao', 'recurso', 'objeto_id', 'data_criacao']
    ordering = ['-data_criacao', '-id']


@extend_schema_view(
    list=extend_schema(summary='Listar pendências', tags=['Pendências']),
    retrieve=extend_schema(summary='Detalhar pendência', tags=['Pendências']),
    create=extend_schema(summary='Criar pendência', tags=['Pendências']),
    update=extend_schema(summary='Atualizar pendência', tags=['Pendências']),
    partial_update=extend_schema(summary='Atualizar parcialmente pendência', tags=['Pendências']),
    destroy=extend_schema(summary='Remover pendência', tags=['Pendências']),
)
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

