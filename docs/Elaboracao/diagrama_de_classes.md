

```markdown
---
id: sistema_validador_estagio
title: Documentação Técnica - Sistema Validador de Estágio
---

## 1. Diagrama de Casos de Uso

```plantuml
@startuml Sistema_Validador_Estagio

left to right direction
skinparam actorStyle awesome

actor Aluno
actor Empresa
actor "Coordenador (Faculdade)" as Faculdade
actor Sistema

rectangle "Sistema Validador de Estágio" {

  usecase (UC01: Submeter dados do estágio) as UC01
  usecase (UC02: Confirmar dados do estágio) as UC02
  usecase (UC03: Executar validação automática) as UC03
  
  usecase (Validar carga horária) as UC03_1
  usecase (Validar duração do estágio) as UC03_2
  usecase (Validar documentação obrigatória) as UC03_3
  usecase (Validar existência de supervisor) as UC03_4
  usecase (Validar seguro obrigatório) as UC03_5
  usecase (Sugerir compatibilidade com curso) as UC03_6

  usecase (UC04: Gerar resultado da validação) as UC04
  usecase (Aprovação automática) as UC04_1
  usecase (Encaminhar para análise manual) as UC04_2

  usecase (UC05: Analisar manualmente solicitação) as UC05

  Aluno --> UC01
  Empresa --> UC02
  Faculdade --> UC05
  Sistema --> UC03
  Sistema --> UC04

  UC01 --> UC03
  
  UC03 --> UC03_1 : <<include>>
  UC03 --> UC03_2 : <<include>>
  UC03 --> UC03_3 : <<include>>
  UC03 --> UC03_4 : <<include>>
  UC03 --> UC03_5 : <<include>>
  UC03 --> UC03_6 : <<include>>
  
  UC03 --> UC04
  
  UC04 ..> UC04_1 : <<extend>>
  UC04 ..> UC04_2 : <<extend>>
  
  UC04_2 --> UC05
}

@enduml

```

### 1.1 Visão Geral e Dinâmica do Sistema

O diagrama de casos de uso estrutura o fluxo do **Sistema Validador de Estágio**, integrando discentes, o setor corporativo e a instituição de ensino.

* **Papel dos Atores**:
* **Aluno**: Inicia o processo inserindo dados do contrato e documentos iniciais.
* **Empresa**: Atua como agente de conformidade, validando a exatidão das informações.
* **Sistema**: Núcleo de processamento lógico que verifica normas regulatórias e toma decisões de roteamento.
* **Coordenador**: Trata exceções e casos que exigem discernimento humano para aprovação ou indeferimento.



---

## 2. Diagrama de Classes

```plantuml
@startuml Diagrama_Classes_Validador_Estagio

skinparam classAttributeIconSize 0
skinparam classFontStyle bold

class Usuario {
  - nome: String
  - emailInstitucional: String
  - senhaHash: String
  - statusAtivacao: Boolean
  + autenticar(): Boolean
}

class Estudante {
  + abrirSolicitacao(): void
  + enviarDocumento(): void
  + consultarStatus(): void
  + visualizarPendencias(): void
}

class Professor {
  + avaliarRelatorio(): void
  + emitirParecer(): void
  + atribuirConceito(): void
}

class Coordenador {
  + visualizarIndicadores(): void
  + analisarExcecao(): void
  + registrarDecisao(): void
}

class EmpresaParceira {
  - nomeOrganizacao: String
  - cnpj: String
  + confirmarDados(): void
  + realizarAssinatura(): void
}

class SolicitacaoEstagio {
  - id: Long
  - dataAbertura: Date
  - statusAtual: String
  - scoreConformidade: Float
  + iniciarProcesso(): void
  + atualizarStatus(): void
}

class Documento {
  - id: Long
  - tipo: String
  - nomeArquivo: String
  - dataEnvio: Date
  - status: String
  + anexar(): void
  + validarAssinatura(): void
}

class ValidacaoAutomatica {
  + executarValidacao(solicitacao: SolicitacaoEstagio): void
  + detectarInconsistencias(): void
  + calcularScore(): Float
}

class Pendencia {
  - id: Long
  - descricao: String
  - estadoResolucao: String
}

Usuario <|-- Estudante
Usuario <|-- Professor
Usuario <|-- Coordenador

Estudante "1" -- "0..*" SolicitacaoEstagio : solicita >
EmpresaParceira "1" -- "0..*" SolicitacaoEstagio : confirma >
SolicitacaoEstagio "1" *-- "1..*" Documento : contém >
SolicitacaoEstagio "1" *-- "0..*" Pendencia : possui >
ValidacaoAutomatica "1" ..> "1" SolicitacaoEstagio : analisa >

@enduml

```

### 2.1 Descrição das Classes

* **Usuario**: Classe base com dados comuns de autenticação (nome, e-mail institucional, senha).
* **Estudante**: Aluno que solicita a validação, envia documentos e consulta status.
* **Professor**: Docente responsável pela análise acadêmica e atribuição de conceitos.
* **Coordenador**: Responsável pelo acompanhamento gerencial e análise de exceções.
* **SolicitacaoEstagio**: Classe central que armazena a data de abertura, status atual e score de conformidade.
* **ValidacaoAutomatica**: Módulo que aplica regras legais aos documentos e detecta inconsistências.

---

## 3. Versionamento

| Data | Versão | Descrição | Autor(es) |
| --- | --- | --- | --- |
| 16/04/2026 | 1.0 | Definição inicial das classes e casos de uso principais | Lucas Calil |
| 17/04/2026 | 1.1 | Inclusão de validação automática e notificações | Lucas Calil |
| 15/05/2026 | 2.0 | Ajustes finais nos relacionamentos e consolidação | Marco Antonio e Lucas Calil |

```

```