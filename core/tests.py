from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from .models import EmpresaParceira, Estudante, SolicitacaoEstagio


class SolicitacaoEstagioAPITestCase(APITestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            username='estudante_teste',
            email='estudante@example.com',
            password='senha-teste',
        )
        self.estudante = Estudante.objects.create(usuario=self.user)
        self.empresa = EmpresaParceira.objects.create(
            nome_organizacao='Empresa Teste',
            cnpj='12345678000190',
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

    def test_altera_status_solicitacao_estagio(self):
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

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        solicitacao.refresh_from_db()
        self.assertEqual(solicitacao.status_atual, 'APROVADO')

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
        self.estudante = Estudante.objects.create(usuario=self.user)
        self.empresa = EmpresaParceira.objects.create(
            nome_organizacao='Empresa JWT',
            cnpj='12345678000191',
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
