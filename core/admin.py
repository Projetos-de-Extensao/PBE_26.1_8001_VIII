from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

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


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'status_ativacao', 'is_staff')
    list_filter = ('status_ativacao', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    fieldsets = UserAdmin.fieldsets + (
        ('Status do sistema', {'fields': ('status_ativacao',)}),
    )


@admin.register(Estudante)
class EstudanteAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'matricula', 'curso', 'elegivel_estagio')
    list_filter = ('elegivel_estagio', 'curso')
    search_fields = (
        'usuario__username',
        'usuario__email',
        'usuario__first_name',
        'usuario__last_name',
        'matricula',
        'curso',
    )


@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario')
    search_fields = ('usuario__username', 'usuario__email', 'usuario__first_name', 'usuario__last_name')


@admin.register(Coordenador)
class CoordenadorAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario')
    search_fields = ('usuario__username', 'usuario__email', 'usuario__first_name', 'usuario__last_name')


@admin.register(EmpresaParceira)
class EmpresaParceiraAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome_organizacao', 'cnpj', 'supervisor')
    search_fields = ('nome_organizacao', 'cnpj', 'supervisor')


@admin.register(SupervisorEmpresa)
class SupervisorEmpresaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'empresa', 'email', 'telefone', 'cargo', 'ativo')
    list_filter = ('ativo', 'empresa')
    search_fields = ('nome', 'email', 'telefone', 'cargo', 'empresa__nome_organizacao')


@admin.register(SolicitacaoEstagio)
class SolicitacaoEstagioAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'estudante',
        'empresa',
        'status_atual',
        'carga_horaria',
        'duracao_contrato',
        'supervisor',
        'seguro_obrigatorio',
        'score_conformidade',
        'data_abertura',
    )
    list_filter = ('status_atual', 'seguro_obrigatorio', 'data_abertura', 'empresa')
    search_fields = (
        'estudante__usuario__username',
        'estudante__usuario__email',
        'estudante__usuario__first_name',
        'estudante__usuario__last_name',
        'empresa__nome_organizacao',
        'empresa__cnpj',
        'supervisor',
        'duracao_contrato',
        'justificativa_recusa',
    )


@admin.register(HistoricoStatusSolicitacao)
class HistoricoStatusSolicitacaoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'solicitacao',
        'status_anterior',
        'status_novo',
        'alterado_por',
        'data_alteracao',
    )
    list_filter = ('status_anterior', 'status_novo', 'data_alteracao')
    search_fields = (
        'solicitacao__id',
        'alterado_por__username',
        'alterado_por__email',
        'observacao',
    )
    readonly_fields = (
        'solicitacao',
        'status_anterior',
        'status_novo',
        'alterado_por',
        'data_alteracao',
    )


@admin.register(RegistroAuditoria)
class RegistroAuditoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'acao', 'recurso', 'objeto_id', 'usuario', 'data_criacao')
    list_filter = ('acao', 'recurso', 'data_criacao')
    search_fields = ('recurso', 'objeto_id', 'descricao', 'usuario__username', 'usuario__email')
    readonly_fields = ('usuario', 'acao', 'recurso', 'objeto_id', 'descricao', 'data_criacao')


@admin.register(Documento)
class DocumentoAdmin(admin.ModelAdmin):
    list_display = ('id', 'tipo', 'solicitacao', 'status', 'data_envio')
    list_filter = ('status', 'tipo', 'data_envio')
    search_fields = ('tipo', 'solicitacao__id', 'solicitacao__estudante__usuario__username')


@admin.register(Pendencia)
class PendenciaAdmin(admin.ModelAdmin):
    list_display = ('id', 'solicitacao', 'estado_resolucao', 'data_criacao')
    list_filter = ('estado_resolucao', 'data_criacao')
    search_fields = ('descricao', 'solicitacao__id', 'solicitacao__estudante__usuario__username')
