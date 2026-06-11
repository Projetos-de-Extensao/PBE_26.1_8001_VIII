from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models


class Usuario(AbstractUser):
    status_ativacao = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.get_full_name()} ({self.email})"

class Estudante(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='estudante_profile')
    curso = models.CharField(max_length=255, blank=True)
    matricula = models.CharField(max_length=50, unique=True, null=True, blank=True)
    elegivel_estagio = models.BooleanField(default=True)
    
    def __str__(self):
        return self.usuario.get_full_name()

class Professor(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='professor_profile')
    
    def __str__(self):
        return self.usuario.get_full_name()

class Coordenador(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='coordenador_profile')
    
    def __str__(self):
        return self.usuario.get_full_name()


# 2. Entidades do Ecossistema de Estágio
class EmpresaParceira(models.Model):
    nome_organizacao = models.CharField(max_length=255)
    cnpj = models.CharField(max_length=18, unique=True)
    supervisor = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.nome_organizacao


class SupervisorEmpresa(models.Model):
    empresa = models.ForeignKey(EmpresaParceira, on_delete=models.CASCADE, related_name='supervisores')
    nome = models.CharField(max_length=255)
    email = models.EmailField(blank=True)
    telefone = models.CharField(max_length=30, blank=True)
    cargo = models.CharField(max_length=100, blank=True)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nome} - {self.empresa}"


class SolicitacaoEstagio(models.Model):
    STATUS_CHOICES = [
        ('ABERTO', 'Aberto'),
        ('EM_ANALISE', 'Em Análise'),
        ('APROVADO', 'Aprovado'),
        ('RECUSADO', 'Recusado'),
        ('PENDENTE', 'Com Pendências'),
    ]

    data_abertura = models.DateField(auto_now_add=True)
    status_atual = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ABERTO')
    score_conformidade = models.FloatField(default=0.0)
    carga_horaria = models.PositiveIntegerField(default=0)
    duracao_contrato = models.CharField(max_length=100, blank=True)
    supervisor = models.CharField(max_length=255, blank=True)
    seguro_obrigatorio = models.BooleanField(default=False)
    justificativa_recusa = models.TextField(blank=True)
    
    # Relacionamentos (As chaves estrangeiras que ligam as tabelas)
    estudante = models.ForeignKey(Estudante, on_delete=models.CASCADE, related_name='solicitacoes')
    empresa = models.ForeignKey(EmpresaParceira, on_delete=models.CASCADE, related_name='solicitacoes')

    def __str__(self):
        return f"Solicitação {self.id} - {self.estudante}"


class HistoricoStatusSolicitacao(models.Model):
    solicitacao = models.ForeignKey(
        SolicitacaoEstagio,
        on_delete=models.CASCADE,
        related_name='historico_status',
    )
    status_anterior = models.CharField(max_length=20, choices=SolicitacaoEstagio.STATUS_CHOICES)
    status_novo = models.CharField(max_length=20, choices=SolicitacaoEstagio.STATUS_CHOICES)
    alterado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='historicos_status_solicitacao',
    )
    data_alteracao = models.DateTimeField(auto_now_add=True)
    observacao = models.TextField(blank=True)

    class Meta:
        ordering = ['-data_alteracao', '-id']

    def __str__(self):
        return f"Solicitação {self.solicitacao_id}: {self.status_anterior} -> {self.status_novo}"


class RegistroAuditoria(models.Model):
    ACAO_CHOICES = [
        ('CRIACAO', 'Criação'),
        ('ATUALIZACAO', 'Atualização'),
        ('STATUS', 'Mudança de Status'),
        ('PENDENCIA', 'Pendência'),
    ]

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='registros_auditoria',
    )
    acao = models.CharField(max_length=20, choices=ACAO_CHOICES)
    recurso = models.CharField(max_length=100)
    objeto_id = models.CharField(max_length=50, blank=True)
    descricao = models.TextField(blank=True)
    data_criacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-data_criacao', '-id']

    def __str__(self):
        return f"{self.acao} {self.recurso} #{self.objeto_id}"


class Documento(models.Model):
    STATUS_DOC = [
        ('ENVIADO', 'Enviado'),
        ('VALIDADO', 'Validado'),
        ('REJEITADO', 'Rejeitado'),
    ]

    solicitacao = models.ForeignKey(SolicitacaoEstagio, on_delete=models.CASCADE, related_name='documentos')
    tipo = models.CharField(max_length=100)  # Ex: TCE, Plano de Atividades
    arquivo = models.FileField(upload_to='documentos/', null=True, blank=True)
    data_envio = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_DOC, default='ENVIADO')

    def __str__(self):
        return f"{self.tipo} - Ref: {self.solicitacao.id}"


class Pendencia(models.Model):
    ESTADO_RESOLUCAO = [
        ('ABERTA', 'Aberta'),
        ('RESOLVIDA', 'Resolvida'),
    ]

    solicitacao = models.ForeignKey(SolicitacaoEstagio, on_delete=models.CASCADE, related_name='pendencias')
    descricao = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)
    estado_resolucao = models.CharField(max_length=20, choices=ESTADO_RESOLUCAO, default='ABERTA')

    def __str__(self):
        return f"Pendência (Solicitação {self.solicitacao.id})"
