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
        fields = [
            'id',
            'data_abertura',
            'status_atual',
            'score_conformidade',
            'carga_horaria',
            'duracao_contrato',
            'supervisor',
            'seguro_obrigatorio',
            'estudante',
            'estudante_nome',
            'empresa',
            'empresa_nome',
        ]
        extra_kwargs = {
            'estudante': {
                'error_messages': {
                    'required': 'O estudante é obrigatório.',
                    'null': 'O estudante é obrigatório.',
                    'does_not_exist': 'Estudante informado não existe.',
                },
            },
            'empresa': {
                'error_messages': {
                    'required': 'A empresa é obrigatória.',
                    'null': 'A empresa é obrigatória.',
                    'does_not_exist': 'Empresa informada não existe.',
                },
            },
            'status_atual': {
                'error_messages': {
                    'invalid_choice': 'Status inválido para solicitação de estágio.',
                },
            },
        }

    def validate(self, attrs):
        errors = {}

        if self.instance is None and not attrs.get('estudante'):
            errors['estudante'] = 'O estudante é obrigatório.'
        elif attrs.get('estudante') is None and 'estudante' in attrs:
            errors['estudante'] = 'O estudante é obrigatório.'

        if self.instance is None and not attrs.get('empresa'):
            errors['empresa'] = 'A empresa é obrigatória.'
        elif attrs.get('empresa') is None and 'empresa' in attrs:
            errors['empresa'] = 'A empresa é obrigatória.'

        status_atual = attrs.get('status_atual')
        status_permitidos = {status for status, _ in SolicitacaoEstagio.STATUS_CHOICES}

        if status_atual is not None and status_atual not in status_permitidos:
            errors['status_atual'] = 'Status inválido para solicitação de estágio.'

        if errors:
            raise serializers.ValidationError(errors)

        return attrs
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
