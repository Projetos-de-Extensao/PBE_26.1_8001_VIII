from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (
    Coordenador,
    Documento,
    EmpresaParceira,
    Estudante,
    Pendencia,
    Professor,
    SolicitacaoEstagio,
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
    list_display = ('id', 'usuario')
    search_fields = ('usuario__username', 'usuario__email', 'usuario__first_name', 'usuario__last_name')


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
    )


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
