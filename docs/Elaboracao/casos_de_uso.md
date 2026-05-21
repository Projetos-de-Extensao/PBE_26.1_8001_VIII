---
id: validador_estagio
title: Diagrama de Casos de Uso - Sistema Validador de Estágio
---

## Casos de uso

```plantuml
@startuml Sistema_Validador_Estagio

left to right direction
skinparam actorStyle awesome

actor Aluno
actor Empresa
actor "Coordenador (Faculdade)" as Faculdade
actor Sistema

rectangle "Sistema Validador de Estágio" {

  ' -------- CASOS DE USO PRINCIPAIS --------
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

  ' -------- RELACIONAMENTOS ATORES --------
  Aluno --> UC01
  Empresa --> UC02
  Faculdade --> UC05
  Sistema --> UC03
  Sistema --> UC04

  ' -------- RELACIONAMENTOS INTERNOS --------
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

## Detalhamento dos Casos de Uso

### UC01 – Submeter dados do estágio
**Ator:** Aluno  
**Objetivo:** Permitir que o discente insira as informações relativas ao seu plano de estágio para início do processo de validação.  
**Pré-requisito:** Aluno devidamente matriculado e autenticado no sistema.

**Fluxo Principal:**
1. O aluno preenche o formulário com dados da empresa, vigência, carga horária e supervisor.
2. O aluno anexa o Termo de Compromisso de Estágio (TCE).
3. O sistema salva os dados e inicia o fluxo de validação.

**Pós-requisito:** Solicitação registrada com status "Aguardando Validação".

---

### UC02 – Confirmar dados do estágio
**Ator:** Empresa  
**Objetivo:** Validar e confirmar que os dados submetidos pelo aluno condizem com a oferta de estágio da empresa.  
**Pré-requisito:** Dados submetidos pelo aluno no UC01.

**Fluxo Principal:**
1. A empresa recebe notificação de nova solicitação.
2. O representante acessa os dados e o documento.
3. A empresa confirma a veracidade das informações.

**Regras de Negócio:**
* O estágio só prossegue para validação automática após a confirmação formal da empresa parceira.

---

### UC03 – Executar validação automática
**Ator:** Sistema  
**Objetivo:** Processar as regras normativas e legais sem intervenção humana imediata.

**Fluxo Principal:**
1. O sistema verifica a carga horária (limite de 6 horas diárias / 30 semanais).
2. O sistema verifica a duração do contrato e a vigência da apólice de seguro.
3. O sistema checa a presença de todos os campos obrigatórios e assinatura do supervisor.
4. O sistema cruza as atividades do estágio com a grade curricular (compatibilidade).

**Pós-requisito:** Relatório de conformidade gerado.

---

### UC04 – Gerar resultado da validação
**Ator:** Sistema  
**Objetivo:** Definir o destino da solicitação com base no score de conformidade obtido no UC03.

**Fluxo Principal:**
1. O sistema analisa os erros e alertas encontrados.
2. **Se 100% conforme:** Executa Aprovação automática.
3. **Se houver inconsistências leves ou necessidade de julgamento:** Executa Encaminhar para análise manual.

**Regras de Negócio:**
* Inconsistências críticas (ex: falta de seguro) impedem a aprovação automática.

---

### UC05 – Analisar manualmente solicitação
**Ator:** Coordenador (Faculdade)  
**Objetivo:** Resolver casos excepcionais ou pedidos que não atingiram os critérios de automação.  
**Pré-requisito:** Solicitação encaminhada para análise manual (UC04_2).

**Fluxo Principal:**
1. O coordenador visualiza o parecer gerado pelo sistema.
2. Verifica os documentos anexados.
3. Decide pela **Aprovação**, **Indeferimento** ou **Solicitação de Ajuste** pelo aluno.

**Pós-requisito:** Status final da solicitação atualizado.

## Informações do Documento
| Data | Versão | Descrição | Autor(es) |
| :--- | :--- | :--- | :--- |
| 16/04/2026 | 1.0 | Elaboração do documento para o Sistema Validador de Estágio | Fabricio Fagner |
| 17/04/2026 | 2.0 | Atualizando documentaçao | Lucas Calil |