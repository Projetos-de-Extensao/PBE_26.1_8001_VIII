import re

from rest_framework import serializers

from .models import (
    Usuario, 
    Estudante,
    Professor,
    Coordenador,
    EmpresaParceira,
    SolicitacaoEstagio,
    Documento,
    Pendencia
                     )

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'status_ativacao']
class EstudanteSerializer(serializers.ModelSerializer):
    usuario_nome = serializers.CharField(source='usuario.get_full_name', read_only=True)
    class Meta:
        model = Estudante
        fields = ['id', 'usuario', 'usuario_nome']
class ProfessorSerializer(serializers.ModelSerializer):
    usuario_nome = serializers.CharField(source='usuario.get_full_name', read_only=True)
    class Meta:
        model = Professor
        fields = ['id', 'usuario', 'usuario_nome']
class CoordenadorSerializer(serializers.ModelSerializer):
    usuario_nome = serializers.CharField(source='usuario.get_full_name', read_only=True)
    class Meta:
        model = Coordenador
        fields = ['id', 'usuario', 'usuario_nome']
class EmpresaParceiraSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmpresaParceira
        fields = ['id', 'nome_organizacao', 'cnpj']

    def validate_cnpj(self, value):
        cnpj = re.sub(r'\D', '', value or '')

        if len(cnpj) != 14:
            raise serializers.ValidationError(
                'CNPJ inválido. Informe um CNPJ com 14 dígitos.'
            )

        return cnpj
class SolicitacaoEstagioSerializer(serializers.ModelSerializer):
    estudante_nome = serializers.CharField(source='estudante.usuario.get_full_name', read_only=True)
    empresa_nome = serializers.CharField(source='empresa.nome_organizacao', read_only=True)
    class Meta:
        model = SolicitacaoEstagio
        fields = ['id', 'data_abertura', 'status_atual', 'score_conformidade', 'estudante', 'estudante_nome', 'empresa', 'empresa_nome']
class DocumentoSerializer(serializers.ModelSerializer):
    solicitacao_id = serializers.IntegerField(source='solicitacao.id', read_only=True)
    class Meta:
        model = Documento
        fields = ['id', 'solicitacao', 'solicitacao_id', 'tipo', 'arquivo', 'data_envio', 'status']
class PendenciaSerializer(serializers.ModelSerializer):
    solicitacao_id = serializers.IntegerField(source='solicitacao.id', read_only=True)
    class Meta:
        model = Pendencia
        fields = ['id', 'solicitacao', 'solicitacao_id', 'descricao', 'data_criacao', 'estado_resolucao']
