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

Tecnologias Sugeridas:

Back-end: Python / django 

Estrutura do Projeto
project/
├── frontend/
├── backend/
├── docs/
└── README.md
Exemplo de Validação
Se aluno_apto = true
e carga_horaria <= limite
e area_relacionada = true
e documentos_ok = true
→ aprovado
senão → pendente ou reprovado

Benefícios
padronização da validação
agilidade na análise
redução de erros
transparência no processo

Status

Em desenvolvimento.

## Instalação 
**Linguagens**: Python, Django<br>
**Tecnologias**: Github, Visual Studio Code<br>
 os pré-requisitos para rodar o seu projeto são UX, Engenharia de Dados, POO.

