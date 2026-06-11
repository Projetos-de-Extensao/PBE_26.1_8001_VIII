from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

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
)


class SolicitacaoEstagioAPITestCase(APITestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            username='estudante_teste',
            email='estudante@example.com',
            password='senha-teste',
        )
        self.estudante = Estudante.objects.create(
            usuario=self.user,
            curso='Sistemas de Informação',
            matricula='MAT-001',
        )
        self.empresa = EmpresaParceira.objects.create(
            nome_organizacao='Empresa Teste',
            cnpj='11222333000181',
            supervisor='Supervisor Teste',
        )
        self.client.force_authenticate(user=self.user)

    def test_cria_solicitacao_estagio(self):
        payload = {
            'estudante': self.estudante.id,
            'empresa': self.empresa.id,
            'carga_horaria': 30,
            'duracao_contrato': '6 meses',
            'supervisor': 'Supervisor do Estagio',
            'seguro_obrigatorio': True,
        }

        response = self.client.post('/api/solicitacoes/', payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SolicitacaoEstagio.objects.count(), 1)
        self.assertEqual(response.data['carga_horaria'], 30)
        self.assertEqual(response.data['status_atual'], 'ABERTO')
        self.assertTrue(
            RegistroAuditoria.objects.filter(
                acao='CRIACAO',
                recurso='SolicitacaoEstagio',
                objeto_id=str(response.data['id']),
                usuario=self.user,
            ).exists()
        )

    def test_nao_cria_solicitacao_com_dados_de_estagio_invalidos(self):
        payload = {
            'estudante': self.estudante.id,
            'empresa': self.empresa.id,
            'carga_horaria': 0,
            'duracao_contrato': '',
            'supervisor': '',
            'seguro_obrigatorio': False,
        }

        response = self.client.post('/api/solicitacoes/', payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data['success'])
        self.assertIn('errors', response.data)
        self.assertIn('carga_horaria', response.data)
        self.assertIn('duracao_contrato', response.data)
        self.assertIn('supervisor', response.data)
        self.assertIn('seguro_obrigatorio', response.data)

    def test_nao_cria_solicitacao_com_carga_horaria_acima_do_limite(self):
        payload = {
            'estudante': self.estudante.id,
            'empresa': self.empresa.id,
            'carga_horaria': 60,
            'duracao_contrato': '6 meses',
            'supervisor': 'Supervisor do Estagio',
            'seguro_obrigatorio': True,
        }

        response = self.client.post('/api/solicitacoes/', payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('44 horas', str(response.data['carga_horaria']))

    def test_nao_cria_solicitacao_para_estudante_inelegivel(self):
        User = get_user_model()
        user_inelegivel = User.objects.create_user(
            username='estudante_inelegivel',
            password='senha-teste',
        )
        estudante_inelegivel = Estudante.objects.create(
            usuario=user_inelegivel,
            curso='Sistemas de Informação',
            matricula='MAT-999',
            elegivel_estagio=False,
        )

        payload = {
            'estudante': estudante_inelegivel.id,
            'empresa': self.empresa.id,
            'carga_horaria': 30,
            'duracao_contrato': '6 meses',
            'supervisor': 'Supervisor do Estagio',
            'seguro_obrigatorio': True,
        }

        response = self.client.post('/api/solicitacoes/', payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('não está elegível', str(response.data['estudante']))

    def test_lista_solicitacoes_estagio(self):
        SolicitacaoEstagio.objects.create(
            estudante=self.estudante,
            empresa=self.empresa,
            carga_horaria=20,
            duracao_contrato='4 meses',
            supervisor='Supervisor do Estagio',
            seguro_obrigatorio=True,
        )

        response = self.client.get('/api/solicitacoes/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(len(response.data['results']), 1)

    def test_estudante_nao_altera_status_solicitacao_estagio(self):
        solicitacao = SolicitacaoEstagio.objects.create(
            estudante=self.estudante,
            empresa=self.empresa,
            carga_horaria=20,
            duracao_contrato='4 meses',
            supervisor='Supervisor do Estagio',
            seguro_obrigatorio=True,
        )

        response = self.client.patch(
            f'/api/solicitacoes/{solicitacao.id}/',
            {'status_atual': 'APROVADO'},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        solicitacao.refresh_from_db()
        self.assertEqual(solicitacao.status_atual, 'ABERTO')

    def test_acesso_nao_autenticado_retorna_401_ou_403(self):
        self.client.force_authenticate(user=None)

        response = self.client.get('/api/solicitacoes/')

        self.assertIn(
            response.status_code,
            [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN],
        )


class JWTAuthenticationAPITestCase(APITestCase):
    def setUp(self):
        User = get_user_model()
        self.password = 'senha-jwt-teste'
        self.user = User.objects.create_user(
            username='estudante_jwt',
            email='estudante.jwt@example.com',
            password=self.password,
        )
        self.estudante = Estudante.objects.create(
            usuario=self.user,
            curso='Sistemas de Informação',
            matricula='MAT-002',
        )
        self.empresa = EmpresaParceira.objects.create(
            nome_organizacao='Empresa JWT',
            cnpj='22333444000181',
            supervisor='Supervisor JWT',
        )

    def test_obtem_token_jwt_com_credenciais_validas(self):
        response = self.client.post(
            '/api/token/',
            {'username': self.user.username, 'password': self.password},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_renova_token_jwt_com_refresh_valido(self):
        token_response = self.client.post(
            '/api/token/',
            {'username': self.user.username, 'password': self.password},
            format='json',
        )

        response = self.client.post(
            '/api/token/refresh/',
            {'refresh': token_response.data['refresh']},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_acessa_rota_protegida_com_token_jwt_valido(self):
        token_response = self.client.post(
            '/api/token/',
            {'username': self.user.username, 'password': self.password},
            format='json',
        )
        access_token = token_response.data['access']

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.get('/api/solicitacoes/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ObjectPermissionAPITestCase(APITestCase):
    def setUp(self):
        User = get_user_model()
        self.user_a = User.objects.create_user(username='estudante_a', password='senha-a')
        self.user_b = User.objects.create_user(username='estudante_b', password='senha-b')
        self.estudante_a = Estudante.objects.create(
            usuario=self.user_a,
            curso='Sistemas de Informação',
            matricula='MAT-003',
        )
        self.estudante_b = Estudante.objects.create(
            usuario=self.user_b,
            curso='Sistemas de Informação',
            matricula='MAT-004',
        )
        self.empresa = EmpresaParceira.objects.create(
            nome_organizacao='Empresa Permissao',
            cnpj='33444555000181',
        )
        self.solicitacao_a = SolicitacaoEstagio.objects.create(
            estudante=self.estudante_a,
            empresa=self.empresa,
            carga_horaria=20,
            duracao_contrato='4 meses',
            supervisor='Supervisor A',
            seguro_obrigatorio=True,
        )
        self.solicitacao_b = SolicitacaoEstagio.objects.create(
            estudante=self.estudante_b,
            empresa=self.empresa,
            carga_horaria=30,
            duracao_contrato='6 meses',
            supervisor='Supervisor B',
            seguro_obrigatorio=True,
        )
        self.documento_a = Documento.objects.create(
            solicitacao=self.solicitacao_a,
            tipo='TCE',
        )
        self.documento_b = Documento.objects.create(
            solicitacao=self.solicitacao_b,
            tipo='TCE',
        )
        self.pendencia_a = Pendencia.objects.create(
            solicitacao=self.solicitacao_a,
            descricao='Pendencia do estudante A',
        )
        self.pendencia_b = Pendencia.objects.create(
            solicitacao=self.solicitacao_b,
            descricao='Pendencia do estudante B',
        )
        self.client.force_authenticate(user=self.user_a)

    def test_estudante_lista_apenas_suas_solicitacoes(self):
        response = self.client.get('/api/solicitacoes/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ids = [item['id'] for item in response.data['results']]
        self.assertIn(self.solicitacao_a.id, ids)
        self.assertNotIn(self.solicitacao_b.id, ids)

    def test_estudante_nao_acessa_solicitacao_de_outro_estudante(self):
        response = self.client.get(f'/api/solicitacoes/{self.solicitacao_b.id}/')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_estudante_lista_apenas_documentos_das_suas_solicitacoes(self):
        response = self.client.get('/api/documentos/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ids = [item['id'] for item in response.data['results']]
        self.assertIn(self.documento_a.id, ids)
        self.assertNotIn(self.documento_b.id, ids)

    def test_estudante_lista_apenas_pendencias_das_suas_solicitacoes(self):
        response = self.client.get('/api/pendencias/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ids = [item['id'] for item in response.data['results']]
        self.assertIn(self.pendencia_a.id, ids)
        self.assertNotIn(self.pendencia_b.id, ids)


class ProfileActionPermissionAPITestCase(APITestCase):
    def setUp(self):
        User = get_user_model()
        self.estudante_user = User.objects.create_user(username='acao_estudante', password='senha')
        self.professor_user = User.objects.create_user(username='acao_professor', password='senha')
        self.coordenador_user = User.objects.create_user(username='acao_coordenador', password='senha')
        self.estudante = Estudante.objects.create(
            usuario=self.estudante_user,
            curso='Sistemas de Informação',
            matricula='MAT-005',
        )
        self.professor = Professor.objects.create(usuario=self.professor_user)
        self.coordenador = Coordenador.objects.create(usuario=self.coordenador_user)
        self.empresa = EmpresaParceira.objects.create(
            nome_organizacao='Empresa Acao',
            cnpj='44555666000181',
            supervisor='Supervisor Acao',
        )
        self.solicitacao = SolicitacaoEstagio.objects.create(
            estudante=self.estudante,
            empresa=self.empresa,
            carga_horaria=20,
            duracao_contrato='4 meses',
            supervisor='Supervisor Acao',
            seguro_obrigatorio=True,
        )

    def criar_documentos_obrigatorios(self):
        Documento.objects.create(solicitacao=self.solicitacao, tipo='TCE')
        Documento.objects.create(solicitacao=self.solicitacao, tipo='Plano de Atividades')

    def test_coordenador_altera_status_solicitacao(self):
        self.client.force_authenticate(user=self.coordenador_user)
        self.criar_documentos_obrigatorios()

        em_analise_response = self.client.patch(
            f'/api/solicitacoes/{self.solicitacao.id}/',
            {'status_atual': 'EM_ANALISE'},
            format='json',
        )
        aprovado_response = self.client.patch(
            f'/api/solicitacoes/{self.solicitacao.id}/',
            {'status_atual': 'APROVADO'},
            format='json',
        )

        self.assertEqual(em_analise_response.status_code, status.HTTP_200_OK)
        self.assertEqual(aprovado_response.status_code, status.HTTP_200_OK)
        self.solicitacao.refresh_from_db()
        self.assertEqual(self.solicitacao.status_atual, 'APROVADO')

        historicos = HistoricoStatusSolicitacao.objects.filter(solicitacao=self.solicitacao)
        self.assertEqual(historicos.count(), 2)
        self.assertTrue(
            historicos.filter(
                status_anterior='ABERTO',
                status_novo='EM_ANALISE',
                alterado_por=self.coordenador_user,
            ).exists()
        )
        self.assertTrue(
            historicos.filter(
                status_anterior='EM_ANALISE',
                status_novo='APROVADO',
                alterado_por=self.coordenador_user,
            ).exists()
        )

    def test_bloqueia_envio_para_analise_sem_documentos_obrigatorios(self):
        self.client.force_authenticate(user=self.coordenador_user)

        response = self.client.patch(
            f'/api/solicitacoes/{self.solicitacao.id}/',
            {'status_atual': 'EM_ANALISE'},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('documentos', response.data)
        self.assertIn('TCE', str(response.data['documentos']))
        self.assertIn('Plano de Atividades', str(response.data['documentos']))
        self.solicitacao.refresh_from_db()
        self.assertEqual(self.solicitacao.status_atual, 'ABERTO')

    def test_lista_historico_status_solicitacao(self):
        self.client.force_authenticate(user=self.coordenador_user)
        HistoricoStatusSolicitacao.objects.create(
            solicitacao=self.solicitacao,
            status_anterior='ABERTO',
            status_novo='EM_ANALISE',
            alterado_por=self.coordenador_user,
            observacao='Solicitação enviada para análise.',
        )

        response = self.client.get('/api/historicos-status/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['status_anterior'], 'ABERTO')
        self.assertEqual(response.data['results'][0]['status_novo'], 'EM_ANALISE')

    def test_bloqueia_transicao_invalida_de_aberto_para_aprovado(self):
        self.client.force_authenticate(user=self.coordenador_user)

        response = self.client.patch(
            f'/api/solicitacoes/{self.solicitacao.id}/',
            {'status_atual': 'APROVADO'},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Transição de status inválida', str(response.data['status_atual']))
        self.solicitacao.refresh_from_db()
        self.assertEqual(self.solicitacao.status_atual, 'ABERTO')

    def test_exige_justificativa_para_recusar_solicitacao(self):
        self.client.force_authenticate(user=self.coordenador_user)
        self.solicitacao.status_atual = 'EM_ANALISE'
        self.solicitacao.save()

        response = self.client.patch(
            f'/api/solicitacoes/{self.solicitacao.id}/',
            {'status_atual': 'RECUSADO'},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('justificativa_recusa', response.data)
        self.solicitacao.refresh_from_db()
        self.assertEqual(self.solicitacao.status_atual, 'EM_ANALISE')

    def test_recusa_solicitacao_com_justificativa_e_registra_historico(self):
        self.client.force_authenticate(user=self.coordenador_user)
        self.solicitacao.status_atual = 'EM_ANALISE'
        self.solicitacao.save()

        response = self.client.patch(
            f'/api/solicitacoes/{self.solicitacao.id}/',
            {
                'status_atual': 'RECUSADO',
                'justificativa_recusa': 'Contrato sem assinatura da empresa.',
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.solicitacao.refresh_from_db()
        self.assertEqual(self.solicitacao.status_atual, 'RECUSADO')
        self.assertEqual(
            self.solicitacao.justificativa_recusa,
            'Contrato sem assinatura da empresa.',
        )
        self.assertTrue(
            HistoricoStatusSolicitacao.objects.filter(
                solicitacao=self.solicitacao,
                status_anterior='EM_ANALISE',
                status_novo='RECUSADO',
                observacao='Contrato sem assinatura da empresa.',
            ).exists()
        )

    def test_permite_fluxo_pendente_para_em_analise_e_recusado(self):
        self.client.force_authenticate(user=self.coordenador_user)
        self.solicitacao.status_atual = 'PENDENTE'
        self.solicitacao.save()

        em_analise_response = self.client.patch(
            f'/api/solicitacoes/{self.solicitacao.id}/',
            {'status_atual': 'EM_ANALISE'},
            format='json',
        )
        recusado_response = self.client.patch(
            f'/api/solicitacoes/{self.solicitacao.id}/',
            {
                'status_atual': 'RECUSADO',
                'justificativa_recusa': 'Pendência documental não resolvida.',
            },
            format='json',
        )

        self.assertEqual(em_analise_response.status_code, status.HTTP_200_OK)
        self.assertEqual(recusado_response.status_code, status.HTTP_200_OK)
        self.solicitacao.refresh_from_db()
        self.assertEqual(self.solicitacao.status_atual, 'RECUSADO')

    def test_bloqueia_retorno_para_analise_com_pendencia_aberta(self):
        self.client.force_authenticate(user=self.coordenador_user)
        self.solicitacao.status_atual = 'PENDENTE'
        self.solicitacao.save()
        Pendencia.objects.create(
            solicitacao=self.solicitacao,
            descricao='Enviar contrato assinado.',
        )

        response = self.client.patch(
            f'/api/solicitacoes/{self.solicitacao.id}/',
            {'status_atual': 'EM_ANALISE'},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('pendências abertas', str(response.data['status_atual']))

    def test_professor_visualiza_mas_nao_deleta_solicitacao(self):
        self.client.force_authenticate(user=self.professor_user)

        detail_response = self.client.get(f'/api/solicitacoes/{self.solicitacao.id}/')
        delete_response = self.client.delete(f'/api/solicitacoes/{self.solicitacao.id}/')

        self.assertEqual(detail_response.status_code, status.HTTP_200_OK)
        self.assertEqual(delete_response.status_code, status.HTTP_403_FORBIDDEN)

    def test_estudante_envia_documento_para_sua_solicitacao(self):
        self.client.force_authenticate(user=self.estudante_user)

        response = self.client.post(
            '/api/documentos/',
            {'solicitacao': self.solicitacao.id, 'tipo': 'TCE'},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Documento.objects.count(), 1)

    def test_estudante_nao_cria_pendencia(self):
        self.client.force_authenticate(user=self.estudante_user)

        response = self.client.post(
            '/api/pendencias/',
            {'solicitacao': self.solicitacao.id, 'descricao': 'Documento pendente'},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_coordenador_cria_pendencia(self):
        self.client.force_authenticate(user=self.coordenador_user)

        response = self.client.post(
            '/api/pendencias/',
            {'solicitacao': self.solicitacao.id, 'descricao': 'Documento pendente'},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Pendencia.objects.count(), 1)

    def test_coordenador_cria_pendencia_e_marca_solicitacao_como_pendente(self):
        self.client.force_authenticate(user=self.coordenador_user)
        self.solicitacao.status_atual = 'EM_ANALISE'
        self.solicitacao.save()

        response = self.client.post(
            '/api/pendencias/',
            {
                'solicitacao': self.solicitacao.id,
                'descricao': 'Contrato sem assinatura da empresa.',
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.solicitacao.refresh_from_db()
        self.assertEqual(self.solicitacao.status_atual, 'PENDENTE')
        self.assertTrue(
            HistoricoStatusSolicitacao.objects.filter(
                solicitacao=self.solicitacao,
                status_anterior='EM_ANALISE',
                status_novo='PENDENTE',
                observacao='Contrato sem assinatura da empresa.',
            ).exists()
        )

    def test_estudante_resolve_propria_pendencia(self):
        self.client.force_authenticate(user=self.estudante_user)
        pendencia = Pendencia.objects.create(
            solicitacao=self.solicitacao,
            descricao='Enviar contrato assinado.',
        )

        response = self.client.patch(
            f'/api/pendencias/{pendencia.id}/',
            {'estado_resolucao': 'RESOLVIDA'},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        pendencia.refresh_from_db()
        self.assertEqual(pendencia.estado_resolucao, 'RESOLVIDA')

    def test_estudante_nao_altera_descricao_da_pendencia(self):
        self.client.force_authenticate(user=self.estudante_user)
        pendencia = Pendencia.objects.create(
            solicitacao=self.solicitacao,
            descricao='Enviar contrato assinado.',
        )

        response = self.client.patch(
            f'/api/pendencias/{pendencia.id}/',
            {'descricao': 'Texto alterado pelo estudante.'},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        pendencia.refresh_from_db()
        self.assertEqual(pendencia.descricao, 'Enviar contrato assinado.')

    def test_coordenador_gerencia_empresa(self):
        self.client.force_authenticate(user=self.coordenador_user)

        response = self.client.post(
            '/api/empresas/',
            {
                'nome_organizacao': 'Empresa Coordenador',
                'cnpj': '55.666.777/0001-81',
                'supervisor': 'Supervisor Coordenador',
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_coordenador_nao_cadastra_empresa_com_cnpj_invalido(self):
        self.client.force_authenticate(user=self.coordenador_user)

        response = self.client.post(
            '/api/empresas/',
            {
                'nome_organizacao': 'Empresa CNPJ Invalido',
                'cnpj': '11.222.333/0001-82',
                'supervisor': 'Supervisor CNPJ',
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('CNPJ inválido', str(response.data['cnpj']))

    def test_coordenador_cadastra_empresa_com_cnpj_mascarado_valido(self):
        self.client.force_authenticate(user=self.coordenador_user)

        response = self.client.post(
            '/api/empresas/',
            {
                'nome_organizacao': 'Empresa CNPJ Valido',
                'cnpj': '66.777.888/0001-81',
                'supervisor': 'Supervisor CNPJ',
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['cnpj'], '66777888000181')

    def test_coordenador_cadastra_supervisor_empresa(self):
        self.client.force_authenticate(user=self.coordenador_user)

        response = self.client.post(
            '/api/supervisores/',
            {
                'empresa': self.empresa.id,
                'nome': 'Supervisor Estruturado',
                'email': 'supervisor@example.com',
                'telefone': '(61) 99999-0000',
                'cargo': 'Analista Responsável',
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SupervisorEmpresa.objects.count(), 1)
        self.assertEqual(response.data['empresa_nome'], self.empresa.nome_organizacao)

    def test_coordenador_lista_registros_de_auditoria(self):
        self.client.force_authenticate(user=self.coordenador_user)
        RegistroAuditoria.objects.create(
            usuario=self.coordenador_user,
            acao='PENDENCIA',
            recurso='Pendencia',
            objeto_id='1',
            descricao='Registro de auditoria para teste.',
        )

        response = self.client.get('/api/auditoria/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
