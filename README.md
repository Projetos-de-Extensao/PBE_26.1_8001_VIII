# Projeto Back-End 

**Integrantes**: Marco Antonio, Lucas Calil, Gabriel de Santi, Francisco Fagner, Pedro Carvalho

## Sobre 
Sistema de Validação de Estágio — IBMEC
Visão Geral

Sistema para verificar se um estágio obtido por um aluno atende às regras institucionais do IBMEC para validação acadêmica.

Objetivo

Automatizar a análise de estágios, validando critérios como elegibilidade do aluno, carga horária, relação com o curso, dados da empresa e documentação obrigatória.

Funcionalidades:

Cadastro do aluno
Cadastro do estágio
Validação automática de regras
Resultado da validação (aprovado, reprovado, pendente)
Justificativa da decisão
Histórico de validações
Regras de Negócio
aluno deve estar matriculado
estágio deve estar no período permitido
carga horária dentro do limite
atividades relacionadas ao curso
empresa com dados válidos
supervisor definido
documentação obrigatória completa

Fluxo do Sistema:

Aluno informa os dados do estágio
Sistema aplica as regras de validação
Pendências são identificadas
Resultado é exibido
Coordenação pode revisar (opcional)



## Instalação

**Linguagens**: Python, Django  
**Tecnologias**: Django REST Framework, SimpleJWT, drf-spectacular, SQLite em desenvolvimento

### Como rodar localmente

1. Crie e ative um ambiente virtual:

```bash
python -m venv .venv
.venv\Scripts\activate
```

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Configure as variáveis de ambiente.

Use o arquivo `.env.example` como referência:

```env
DJANGO_SECRET_KEY=troque-esta-chave-em-producao
DJANGO_DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
CSRF_TRUSTED_ORIGINS=
DB_ENGINE=sqlite
POSTGRES_DB=sistema_estagio
POSTGRES_USER=postgres
POSTGRES_PASSWORD=
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

4. Aplique as migrations:

```bash
python manage.py migrate
```

5. Crie um usuário administrador, se necessário:

```bash
python manage.py createsuperuser
```

6. Inicie o servidor:

```bash
python manage.py runserver
```

### Endpoints úteis

- API principal: `http://127.0.0.1:8000/api/`
- Admin Django: `http://127.0.0.1:8000/admin/`
- Obter token JWT: `http://127.0.0.1:8000/api/token/`
- Renovar token JWT: `http://127.0.0.1:8000/api/token/refresh/`
- Documentação Swagger: `http://127.0.0.1:8000/api/docs/`
- Schema OpenAPI: `http://127.0.0.1:8000/api/schema/`

### Testes

```bash
python manage.py test core
```

### Observações para produção

- Defina `DJANGO_DEBUG=False`.
- Use uma `DJANGO_SECRET_KEY` forte e exclusiva do ambiente.
- Configure `ALLOWED_HOSTS` com os domínios reais.
- Configure `CORS_ALLOWED_ORIGINS` apenas com os front-ends autorizados.
- Configure `CSRF_TRUSTED_ORIGINS` com as origens HTTPS confiáveis quando houver admin/formulários em produção.
- SQLite é usado em desenvolvimento.
- Para PostgreSQL em produção, defina `DB_ENGINE=postgresql` e preencha `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_HOST` e `POSTGRES_PORT`.
- O arquivo `Procfile` usa `gunicorn setup.wsgi:application` para provedores que suportam esse padrão.
- Antes de publicar, rode `python manage.py collectstatic`.


