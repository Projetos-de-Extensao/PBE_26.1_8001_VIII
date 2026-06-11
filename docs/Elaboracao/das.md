---
id: documento_de_arquitetura
title: Documento de Arquitetura
---

# Documento de Arquitetura de Software (DAS)

## Sistema

Sistema Validador de Estágio.

## Introdução

Este documento descreve a arquitetura atual do backend do Sistema Validador de Estágio. O sistema foi implementado com Django e Django REST Framework, com foco na exposição de uma API REST para cadastro, acompanhamento e validação de solicitações de estágio.

## Escopo Arquitetural

O escopo descrito neste documento contempla o backend do projeto. A aplicação centraliza regras e dados relacionados a usuários, perfis, empresas parceiras, solicitações de estágio, documentos e pendências.

O projeto não inclui, neste momento, um frontend completo no repositório. A API foi preparada para ser consumida por clientes externos por meio de rotas REST sob `/api/`.

## Tecnologias Utilizadas

- Python como linguagem principal.
- Django como framework backend.
- Django REST Framework para construção da API.
- drf-spectacular para geração de documentação OpenAPI e Swagger.
- django-cors-headers para configuração de CORS.
- SQLite como banco de dados em desenvolvimento.
- PostgreSQL recomendado para ambientes de produção.

## Padrão Arquitetural

O projeto segue o padrão MVT do Django:

- Model: representa as entidades do domínio e a estrutura persistida no banco de dados.
- View: no projeto, as ViewSets do Django REST Framework recebem requisições e expõem operações da API.
- Template: não é o foco principal do sistema, pois a entrega atual é uma API REST.

No contexto da API, serializers fazem a conversão entre models e representações JSON, além de centralizarem validações de entrada.

## Organização do Projeto

O app principal do sistema é `core`.

Responsabilidades principais:

- `core/models.py`: define entidades como `Usuario`, `Estudante`, `Professor`, `Coordenador`, `EmpresaParceira`, `SolicitacaoEstagio`, `Documento` e `Pendencia`.
- `core/serializers.py`: define a representação da API e validações de dados.
- `core/views.py`: define ViewSets, permissões, busca, ordenação, paginação e otimizações de queryset.
- `core/admin.py`: registra os models no Django Admin.
- `core/permissions.py`: define permissões iniciais por perfil de usuário.
- `setup/settings.py`: centraliza configurações do Django, DRF, CORS, autenticação, paginação e OpenAPI.
- `setup/urls.py`: centraliza rotas administrativas, rotas da API e documentação OpenAPI.

## Visão de API

As rotas REST são centralizadas sob `/api/` por meio de um `DefaultRouter` do Django REST Framework.

Recursos expostos:

- `/api/usuarios/`
- `/api/estudantes/`
- `/api/professores/`
- `/api/coordenadores/`
- `/api/empresas/`
- `/api/solicitacoes/`
- `/api/documentos/`
- `/api/pendencias/`

A documentação OpenAPI está disponível em:

- `/api/schema/`
- `/api/docs/`

## Visão de Dados

O banco utilizado em desenvolvimento é SQLite, configurado como `db.sqlite3`. Para produção, recomenda-se PostgreSQL por oferecer maior robustez, controle de concorrência, recursos de administração e melhor adequação a ambientes multiusuário.

Principais entidades:

- `Usuario`: usuário autenticável do sistema.
- `Estudante`: perfil de estudante vinculado a um usuário.
- `Professor`: perfil de professor vinculado a um usuário.
- `Coordenador`: perfil de coordenador vinculado a um usuário.
- `EmpresaParceira`: empresa relacionada à solicitação de estágio, com CNPJ e supervisor.
- `SolicitacaoEstagio`: solicitação central do fluxo de validação.
- `Documento`: arquivo enviado para uma solicitação.
- `Pendencia`: inconsistência ou item a resolver em uma solicitação.

## Autenticação e Permissões

O projeto utiliza autenticação do Django REST Framework com `SessionAuthentication` e `BasicAuthentication`.

As rotas da API exigem usuário autenticado por padrão. Também foram iniciadas permissões customizadas por perfil:

- `IsEstudante`
- `IsProfessor`
- `IsCoordenador`

Essas permissões verificam se o usuário autenticado possui relação com o respectivo perfil. Regras mais específicas por objeto podem ser evoluídas em etapas futuras.

## Qualidade e Desempenho

As ViewSets utilizam `select_related` em relações `ForeignKey` e `OneToOne` para reduzir consultas repetidas em listagens.

A API também possui paginação padrão, busca e ordenação em recursos principais, especialmente solicitações, empresas, documentos e pendências.

## Restrições e Decisões Conhecidas

- SQLite é mantido para desenvolvimento local.
- PostgreSQL é recomendado para produção.
- A validação de CNPJ aceita valores com ou sem máscara e verifica os dígitos verificadores.
- As regras de transição de status ainda não foram formalizadas no model.
- O sistema expõe API REST e documentação Swagger, mas não implementa um frontend completo neste repositório.

## Histórico de Versão

| Data | Versão | Descrição | Autor(es) |
| -- | -- | -- | -- |
| 07/06/2026 | 1.0 | Revisão do DAS com a arquitetura real do Sistema Validador de Estágio | Equipe do projeto |
