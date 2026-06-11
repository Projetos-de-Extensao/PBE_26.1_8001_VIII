---
id: documento_de_visao
title: Documento de Visão
---

## Introdução

Este documento apresenta a visão do Sistema Validador de Estágio, um sistema voltado ao apoio do processo de cadastro, análise e validação de solicitações de estágio acadêmico.

O projeto tem como foco organizar os dados principais envolvidos na validação de estágio, incluindo estudante, empresa parceira, solicitação, documentos e pendências identificadas durante a análise.

## Nome do Sistema

Sistema Validador de Estágio.

## Objetivo do Sistema

O objetivo do sistema é apoiar a validação de estágios por meio de uma API que centraliza informações de estudantes, empresas parceiras, solicitações de estágio, documentos enviados e pendências.

A solução busca reduzir erros manuais, melhorar a rastreabilidade das análises e facilitar o acompanhamento do status de cada solicitação.

## Problema

O processo de validação de estágio pode envolver diferentes informações e documentos, como dados do estudante, dados da empresa, carga horária, duração do contrato, supervisor, seguro obrigatório e documentos comprobatórios.

Quando essas informações ficam dispersas ou são controladas manualmente, torna-se mais difícil acompanhar o status da solicitação, identificar pendências e garantir que todos os dados necessários foram informados.

## Usuários Principais

### Estudante

Usuário que solicita a validação do estágio, informa dados relacionados ao contrato e envia documentos necessários para análise.

### Professor

Usuário que pode acompanhar solicitações e apoiar a análise acadêmica do estágio conforme as regras do curso.

### Coordenador

Usuário responsável por acompanhar, analisar e decidir sobre solicitações de estágio, podendo aprovar, recusar ou registrar pendências.

### Empresa Parceira

Organização vinculada à solicitação de estágio. Seus dados incluem nome, CNPJ e supervisor responsável.

## Funcionalidades Principais

- Cadastro e gerenciamento de usuários do sistema.
- Cadastro de perfis de estudante, professor e coordenador.
- Cadastro de empresas parceiras com CNPJ e supervisor.
- Criação de solicitações de estágio.
- Registro de carga horária, duração do contrato, supervisor e seguro obrigatório.
- Controle de status da solicitação de estágio.
- Envio e acompanhamento de documentos relacionados à solicitação.
- Registro e acompanhamento de pendências.
- Exposição dos dados por API REST.
- Proteção das rotas da API por autenticação e permissões iniciais por perfil.

## Escopo do Projeto

O escopo atual contempla o backend do Sistema Validador de Estágio, implementado em Django e Django REST Framework.

O sistema oferece models, serializers, ViewSets e rotas REST para os dados centrais do domínio. Também inclui documentação da API com OpenAPI/Swagger por meio do drf-spectacular.

## Restrições Conhecidas

- O banco SQLite é adequado para desenvolvimento, mas não é recomendado para produção.
- As regras de validação ainda são básicas e devem evoluir conforme regras institucionais mais detalhadas forem definidas.
- As permissões por perfil existem de forma inicial, sem regras complexas por objeto.
- A validação de CNPJ aceita valores com ou sem máscara e verifica os dígitos verificadores.
- O projeto atual não contempla um frontend completo dentro deste repositório.

## Visão Geral do Fluxo de Validação

1. O estudante informa os dados do estágio e cria uma solicitação.
2. A solicitação é associada a uma empresa parceira.
3. O estudante envia documentos relacionados à solicitação.
4. O professor ou coordenador acompanha os dados cadastrados.
5. O coordenador analisa a solicitação, seus documentos e eventuais inconsistências.
6. O coordenador pode aprovar, recusar ou indicar pendências.
7. As pendências ficam registradas para acompanhamento e resolução.

## Versionamento

| Data | Versão | Descrição | Autor(es) |
| -- | -- | -- | -- |
| 07/06/2026 | 1.0 | Revisão do documento com o contexto real do Sistema Validador de Estágio | Equipe do projeto |
