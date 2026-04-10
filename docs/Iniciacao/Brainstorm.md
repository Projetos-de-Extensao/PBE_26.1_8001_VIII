---
id: brainstorm
title: Brainstorm
---
 
## Introdução
<p align = "justify">
O brainstorm é uma técnica de elicitação de requisitos que consiste em reunir a equipe e discutir sobre diversos tópicos gerais do projeto apresentados no documento problema de negócio. No brainstorm o diálogo é incentivado e críticas são evitadas para permitir que todos colaborem com suas próprias ideias.
</p>
 
## Metodologia
<p align = "justify">
A equipe se reuniu para debater ideias gerais sobre o projeto do Sistema de Validação de Estágios via chamada de voz no Discord. A reunião começou às 14:00 e terminou às 15:30, onde o desenvolvedor líder foi o moderador, direcionando a equipe com questões pré-elaboradas focadas na Lei do Estágio e regras do IBMEC, e transcrevendo as respostas para o documento.
</p>
 
## Brainstorm
 
## Versão 1.0
 
## Perguntas
 
### 1. Qual o objetivo principal da nossa API (sistema back-end)?
 
<p align = "justify">
<b>Desenvolvedor 1</b> - O principal objetivo é receber os dados dos contratos de estágio e conferir automaticamente se estão dentro da lei.
</p>
 
<p align = "justify">
<b>Desenvolvedor 2</b> - A aplicação precisa barrar qualquer erro logo de cara, para evitar dores de cabeça para a faculdade e para a empresa.
</p>
 
<p align = "justify">
<b>Desenvolvedor 3</b> - A plataforma deve se integrar com o sistema acadêmico do IBMEC (o SIA) para automatizar a aprovação das horas dos alunos de forma segura.
</p>
 
---
 
### 2. Como será o processo para validar um novo Termo de Compromisso de Estágio (TCE)?
 
<p align = "justify">
<b>Desenvolvedor 1</b> - O sistema vai receber o documento e a primeira coisa é checar as datas. O estágio na mesma empresa não pode passar de 2 anos.
</p>

<p align = "justify">
<b>Desenvolvedor 2</b> - Tem que conferir as horas também. O limite máximo permitido pela lei é de 6 horas por dia e 30 horas na semana. Se passar disso, o sistema reprova.
</p>

<p align = "justify">
<b>Desenvolvedor 3</b> - O back-end também vai olhar se o estágio é obrigatório ou não. Se for não obrigatório, o sistema vai exigir que tenha o valor da bolsa e o auxílio-transporte preenchidos no contrato.
</p>
 
---
 
### 3. Como o sistema vai lidar com relatórios e o dia a dia do estagiário?
 
<p align = "justify">
<b>Desenvolvedor 1</b> - A lei exige que a empresa mande um relatório de atividades a cada 6 meses no máximo. O sistema precisa criar alertas para cobrar isso.
</p>
 
<p align = "justify">
<b>Desenvolvedor 2</b> - Para o IBMEC validar as horas no final, o sistema vai verificar se o relatório foi entregue e se tem todas as assinaturas digitais certinhas.
</p>
 
<p align = "justify">
<b>Desenvolvedor 3</b> - E na hora que o aluno registrar as horas da semana, a API tem que somar tudo. Se o aluno tentar colocar mais horas do que o curso permite, a gente bloqueia.
</p>
 
---
 
### 4. Quais informações seriam importantes para o setor de Carreiras do IBMEC visualizar?
 
<p align = "justify">
<b>Desenvolvedor 1</b> - Eles precisam de uma lista mostrando quais contratos foram aprovados e quais foram bloqueados com o motivo do erro (ex: "Passou de 30h semanais").
</p>
 
<p align = "justify">
<b>Desenvolvedor 2</b> - O setor de carreiras precisa fazer uma validação prévia. Então o sistema manda os dados limpos e checados para eles darem o "OK" final antes de iniciar.
</p>
 
<p align = "justify">
<b>Desenvolvedor 3</b> - Seria legal avisar a faculdade quais alunos já se formaram, porque quem já formou não pode continuar estagiando.
</p>

---
 
### 5. O que o sistema faz se faltar alguma informação obrigatória da Lei ou do IBMEC?
<p align = "justify">
<b>Desenvolvedor 1</b> - Se faltar, por exemplo, o número da apólice de seguro contra acidentes (que é obrigatório), o sistema retorna um erro claro pedindo para preencher.
</p>

<p align = "justify">
<b>Desenvolvedor 2</b> - O contrato fica com o status de "Pendente de Correção" no banco de dados e não segue para a assinatura da instituição de ensino até ser arrumado.
</p>
 
---
 
### Requisitos elicitados
 
|ID|Descrição|
|----|-------------|
|BS01| O sistema deve validar se a jornada diária do estágio é menor ou igual a 6 horas.|
|BS02| O sistema deve validar se a jornada semanal do estágio é menor ou igual a 30 horas.|
|BS03| O sistema deve bloquear contratos que tenham duração superior a 2 anos na mesma concedente.|
|BS04| O sistema deve exigir o preenchimento de bolsa e auxílio-transporte caso o estágio seja classificado como "não obrigatório".|
|BS05| O sistema deve exigir que o contrato possua o número da apólice de seguro contra acidentes.|
|BS06| O sistema deve checar o status de matrícula do aluno via integração (alunos formados não podem estagiar).|
|BS07| O sistema deve emitir um alerta exigindo a entrega do relatório de avaliação a cada 6 meses.|
|BS08| O sistema deve recusar o lançamento de horas excedentes em relação ao que foi assinado no Termo de Compromisso.|
|BS09| O sistema deve verificar a presença das assinaturas digitais da empresa, aluno e instituição antes de aprovar relatórios.|
|BS10| O sistema deve retornar mensagens de erro específicas (explicando a regra violada) quando um dado inserido for inválido.|
 
## Conclusão
<p align = "justify">
Através da aplicação da técnica de brainstorm focada nas regras de negócio e limites legais, foi possível elicitar os principais requisitos funcionais para a construção da lógica do back-end de validação de estágios.
</p>

## Referências Bibliográficas
 
- Presidência da República. Lei nº 11.788, de 25 de setembro de 2008.
- Regulamento de Estágio - IBMEC.
- BARBOSA, S. D. J; DA SILVA, B. S. Interação humano-computador. Elsevier, 2010.
 
## Autor(es)
| Data | Versão | Descrição | Autor(es) |
| -- | -- | -- | -- |
| 10/04/2026 | 1.0 | Criação do documento | Lucas Calil  |