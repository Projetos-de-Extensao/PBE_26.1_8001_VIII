import re

from rest_framework import serializers

from .auditoria import registrar_auditoria
from .models import (
    Usuario, 
    Estudante,
    Professor,
    Coordenador,
    EmpresaParceira,
    HistoricoStatusSolicitacao,
    SolicitacaoEstagio,
    SupervisorEmpresa,
    Documento,
    Pendencia,
    RegistroAuditoria,
                     )

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'status_ativacao']
class EstudanteSerializer(serializers.ModelSerializer):
    usuario_nome = serializers.CharField(source='usuario.get_full_name', read_only=True)
    class Meta:
        model = Estudante
        fields = ['id', 'usuario', 'usuario_nome', 'curso', 'matricula', 'elegivel_estagio']
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
        fields = ['id', 'nome_organizacao', 'cnpj', 'supervisor']

    def validate_cnpj(self, value):
        cnpj = re.sub(r'\D', '', value or '')

        if len(cnpj) != 14:
            raise serializers.ValidationError(
                'CNPJ inválido. Informe um CNPJ com 14 dígitos.'
            )

        if len(set(cnpj)) == 1 or not self._cnpj_tem_digitos_validos(cnpj):
            raise serializers.ValidationError(
                'CNPJ inválido. Verifique os dígitos informados.'
            )

        return cnpj

    def _cnpj_tem_digitos_validos(self, cnpj):
        def calcular_digito(digitos, pesos):
            soma = sum(int(digito) * peso for digito, peso in zip(digitos, pesos))
            resto = soma % 11
            return '0' if resto < 2 else str(11 - resto)

        primeiro_digito = calcular_digito(cnpj[:12], [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2])
        segundo_digito = calcular_digito(
            cnpj[:12] + primeiro_digito,
            [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2],
        )

        return cnpj[-2:] == primeiro_digito + segundo_digito


class SupervisorEmpresaSerializer(serializers.ModelSerializer):
    empresa_nome = serializers.CharField(source='empresa.nome_organizacao', read_only=True)

    class Meta:
        model = SupervisorEmpresa
        fields = ['id', 'empresa', 'empresa_nome', 'nome', 'email', 'telefone', 'cargo', 'ativo']

    def validate_nome(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError('O nome do supervisor é obrigatório.')

        return value.strip()


class SolicitacaoEstagioSerializer(serializers.ModelSerializer):
    DOCUMENTOS_OBRIGATORIOS = {
        'TCE': 'TCE',
        'PLANO_ATIVIDADES': 'Plano de Atividades',
    }
    DOCUMENTOS_ALIASES = {
        'PLANO_DE_ATIVIDADES': 'PLANO_ATIVIDADES',
    }
    TRANSICOES_STATUS = {
        'ABERTO': {'EM_ANALISE'},
        'EM_ANALISE': {'APROVADO', 'RECUSADO', 'PENDENTE'},
        'PENDENTE': {'EM_ANALISE', 'RECUSADO'},
        'APROVADO': set(),
        'RECUSADO': set(),
    }

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
            'justificativa_recusa',
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

        estudante = attrs.get('estudante')
        if estudante is None and self.instance is not None:
            estudante = self.instance.estudante

        if estudante is not None:
            if not estudante.elegivel_estagio:
                errors['estudante'] = 'O estudante não está elegível para estágio.'
            elif not estudante.curso or not estudante.curso.strip() or not estudante.matricula:
                errors['estudante'] = (
                    'O estudante precisa ter curso e matrícula cadastrados para abrir solicitação.'
                )

        if self.instance is None and not attrs.get('empresa'):
            errors['empresa'] = 'A empresa é obrigatória.'
        elif attrs.get('empresa') is None and 'empresa' in attrs:
            errors['empresa'] = 'A empresa é obrigatória.'

        carga_horaria = self._valor_final(attrs, 'carga_horaria')
        duracao_contrato = self._valor_final(attrs, 'duracao_contrato')
        supervisor = self._valor_final(attrs, 'supervisor')
        seguro_obrigatorio = self._valor_final(attrs, 'seguro_obrigatorio')

        if carga_horaria in [None, '']:
            errors['carga_horaria'] = 'A carga horária é obrigatória.'
        elif carga_horaria <= 0:
            errors['carga_horaria'] = 'A carga horária deve ser maior que zero.'
        elif carga_horaria > 44:
            errors['carga_horaria'] = 'A carga horária semanal não deve ultrapassar 44 horas.'

        if not duracao_contrato or not str(duracao_contrato).strip():
            errors['duracao_contrato'] = 'A duração do contrato é obrigatória.'

        if not supervisor or not str(supervisor).strip():
            errors['supervisor'] = 'O supervisor do estágio é obrigatório.'

        if seguro_obrigatorio is not True:
            errors['seguro_obrigatorio'] = 'O seguro obrigatório deve estar confirmado.'

        status_atual = attrs.get('status_atual')
        status_permitidos = {status for status, _ in SolicitacaoEstagio.STATUS_CHOICES}

        if status_atual is not None and status_atual not in status_permitidos:
            errors['status_atual'] = 'Status inválido para solicitação de estágio.'

        if self.instance is not None and status_atual is not None:
            status_anterior = self.instance.status_atual
            status_nao_mudou = status_atual == status_anterior
            status_permitido = status_atual in self.TRANSICOES_STATUS.get(status_anterior, set())

            if not status_nao_mudou and not status_permitido:
                errors['status_atual'] = (
                    f'Transição de status inválida: {status_anterior} -> {status_atual}.'
                )

            if status_anterior == 'ABERTO' and status_atual == 'EM_ANALISE':
                documentos_faltantes = self._documentos_obrigatorios_faltantes()
                if documentos_faltantes:
                    errors['documentos'] = (
                        'Envie os documentos obrigatórios antes de encaminhar para análise: '
                        f'{", ".join(documentos_faltantes)}.'
                    )

            if (
                status_anterior == 'PENDENTE'
                and status_atual == 'EM_ANALISE'
                and self.instance.pendencias.filter(estado_resolucao='ABERTA').exists()
            ):
                errors['status_atual'] = (
                    'Resolva todas as pendências abertas antes de retornar a solicitação para análise.'
                )

        if status_atual == 'RECUSADO':
            justificativa_recusa = attrs.get(
                'justificativa_recusa',
                self.instance.justificativa_recusa if self.instance else '',
            )
            if not justificativa_recusa or not justificativa_recusa.strip():
                errors['justificativa_recusa'] = (
                    'A justificativa da recusa é obrigatória ao recusar uma solicitação.'
                )

        if errors:
            raise serializers.ValidationError(errors)

        return attrs

    def _normalizar_tipo_documento(self, tipo):
        tipo_normalizado = re.sub(r'\W+', '_', tipo or '').strip('_').upper()
        return self.DOCUMENTOS_ALIASES.get(tipo_normalizado, tipo_normalizado)

    def _valor_final(self, attrs, campo):
        if campo in attrs:
            return attrs.get(campo)

        if self.instance is not None:
            return getattr(self.instance, campo)

        return None

    def _documentos_obrigatorios_faltantes(self):
        documentos_enviados = {
            self._normalizar_tipo_documento(tipo)
            for tipo in self.instance.documentos.exclude(status='REJEITADO').values_list('tipo', flat=True)
        }

        return [
            nome
            for codigo, nome in self.DOCUMENTOS_OBRIGATORIOS.items()
            if codigo not in documentos_enviados
        ]

    def update(self, instance, validated_data):
        status_anterior = instance.status_atual
        instance = super().update(instance, validated_data)
        status_novo = instance.status_atual

        if status_anterior != status_novo:
            request = self.context.get('request')
            alterado_por = request.user if request and request.user.is_authenticated else None

            HistoricoStatusSolicitacao.objects.create(
                solicitacao=instance,
                status_anterior=status_anterior,
                status_novo=status_novo,
                alterado_por=alterado_por,
                observacao=instance.justificativa_recusa if status_novo == 'RECUSADO' else '',
            )
            registrar_auditoria(
                alterado_por,
                'STATUS',
                'SolicitacaoEstagio',
                instance.id,
                f'Status alterado de {status_anterior} para {status_novo}.',
            )

        return instance


class HistoricoStatusSolicitacaoSerializer(serializers.ModelSerializer):
    alterado_por_username = serializers.CharField(source='alterado_por.username', read_only=True)

    class Meta:
        model = HistoricoStatusSolicitacao
        fields = [
            'id',
            'solicitacao',
            'status_anterior',
            'status_novo',
            'alterado_por',
            'alterado_por_username',
            'data_alteracao',
            'observacao',
        ]
        read_only_fields = fields


class RegistroAuditoriaSerializer(serializers.ModelSerializer):
    usuario_username = serializers.CharField(source='usuario.username', read_only=True)

    class Meta:
        model = RegistroAuditoria
        fields = [
            'id',
            'usuario',
            'usuario_username',
            'acao',
            'recurso',
            'objeto_id',
            'descricao',
            'data_criacao',
        ]
        read_only_fields = fields


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

    def validate(self, attrs):
        request = self.context.get('request')
        user = request.user if request else None
        errors = {}

        if self.instance is None:
            estado_resolucao = attrs.get('estado_resolucao', 'ABERTA')
            if estado_resolucao != 'ABERTA':
                errors['estado_resolucao'] = 'Uma pendência nova deve ser criada como aberta.'

        if self.instance is not None and hasattr(user, 'estudante_profile'):
            campos_permitidos = {'estado_resolucao'}
            campos_recebidos = set(attrs)

            if campos_recebidos - campos_permitidos:
                errors['non_field_errors'] = (
                    'Estudantes podem apenas marcar suas pendências como resolvidas.'
                )

            if attrs.get('estado_resolucao') != 'RESOLVIDA':
                errors['estado_resolucao'] = (
                    'Estudantes podem apenas marcar pendências como resolvidas.'
                )

        if errors:
            raise serializers.ValidationError(errors)

        return attrs
