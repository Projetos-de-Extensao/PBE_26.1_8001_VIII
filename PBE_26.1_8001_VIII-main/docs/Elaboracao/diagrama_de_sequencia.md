---
id: diagrama_de_sequencia
title: Diagrama de Sequência
---

# Diagrama de Sequência

Este documento apresenta fluxos principais do Sistema Validador de Estágio usando diagramas de sequência em Mermaid.

## 1. Estudante cria solicitação de estágio

```mermaid
sequenceDiagram
    actor Estudante
    participant API
    participant SolicitacaoEstagio

    Estudante->>API: Envia dados da solicitação de estágio
    API->>API: Valida estudante, empresa e status
    API->>SolicitacaoEstagio: Cria solicitação com status ABERTO
    SolicitacaoEstagio-->>API: Retorna solicitação criada
    API-->>Estudante: Retorna dados da solicitação
```

## 2. Estudante envia documento

```mermaid
sequenceDiagram
    actor Estudante
    participant API
    participant SolicitacaoEstagio
    participant Documento

    Estudante->>API: Envia documento da solicitação
    API->>SolicitacaoEstagio: Consulta solicitação vinculada
    SolicitacaoEstagio-->>API: Retorna solicitação
    API->>Documento: Registra arquivo e tipo do documento
    Documento-->>API: Retorna documento com status ENVIADO
    API-->>Estudante: Confirma envio do documento
```

## 3. Coordenador analisa solicitação

```mermaid
sequenceDiagram
    actor Coordenador
    participant API
    participant SolicitacaoEstagio
    participant Documento
    participant Pendencia

    Coordenador->>API: Solicita detalhes da solicitação
    API->>SolicitacaoEstagio: Busca dados da solicitação
    API->>Documento: Busca documentos vinculados
    API->>Pendencia: Busca pendências vinculadas
    SolicitacaoEstagio-->>API: Retorna dados principais
    Documento-->>API: Retorna documentos
    Pendencia-->>API: Retorna pendências
    API-->>Coordenador: Exibe informações para análise
```

## 4. Coordenador aprova solicitação

```mermaid
sequenceDiagram
    actor Coordenador
    participant API
    participant SolicitacaoEstagio

    Coordenador->>API: Altera status para APROVADO
    API->>API: Valida status permitido
    API->>SolicitacaoEstagio: Atualiza status_atual
    SolicitacaoEstagio-->>API: Retorna solicitação aprovada
    API-->>Coordenador: Confirma aprovação
```

## 5. Coordenador rejeita solicitação ou cria pendência

```mermaid
sequenceDiagram
    actor Coordenador
    participant API
    participant SolicitacaoEstagio
    participant Pendencia

    alt Solicitação recusada
        Coordenador->>API: Altera status para RECUSADO
        API->>SolicitacaoEstagio: Atualiza status_atual
        SolicitacaoEstagio-->>API: Retorna solicitação recusada
        API-->>Coordenador: Confirma recusa
    else Solicitação com pendência
        Coordenador->>API: Registra pendência da solicitação
        API->>Pendencia: Cria pendência ABERTA
        API->>SolicitacaoEstagio: Atualiza status para PENDENTE
        Pendencia-->>API: Retorna pendência criada
        SolicitacaoEstagio-->>API: Retorna solicitação pendente
        API-->>Coordenador: Confirma registro da pendência
    end
```
