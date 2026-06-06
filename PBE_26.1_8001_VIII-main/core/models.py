from django.db import models

from django.contrib.auth.models import AbstractUser


class Usuario(AbstractUser):
    status_ativacao = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.get_full_name()} ({self.email})"

class Estudante(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='estudante_profile')
    
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

    def __str__(self):
        return self.nome_organizacao


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
    
    # Relacionamentos (As chaves estrangeiras que ligam as tabelas)
    estudante = models.ForeignKey(Estudante, on_delete=models.CASCADE, related_name='solicitacoes')
    empresa = models.ForeignKey(EmpresaParceira, on_delete=models.CASCADE, related_name='solicitacoes')

    def __str__(self):
        return f"Solicitação {self.id} - {self.estudante}"


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
    estado_resolucao = models.CharField(max_length=20, choices=ESTADO_RESOLUCAO, default='ABERTA')

    def __str__(self):
        return f"Pendência (Solicitação {self.solicitacao.id})"
