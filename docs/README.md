# Documentação

A documentação está organizada por user story: os documentos que valem para todo o projeto ficam em `geral/` e cada story tem a sua pasta `USNN/`, sempre com a mesma estrutura. O estado de cada story está no [README da raiz](../README.md#estado-do-projeto).

## Documentos gerais

| Documento | Conteúdo |
|---|---|
| [geral/01-requisitos-funcionais-e-nao-funcionais.md](geral/01-requisitos-funcionais-e-nao-funcionais.md) | Requisitos funcionais, não funcionais, regras de negócio e rastreabilidade |
| [geral/02-regras-de-geracao-de-codigo.md](geral/02-regras-de-geracao-de-codigo.md) | Regras para gerar e rever código com IA, checklist de revisão e Definition of Done |
| [geral/registo-de-uso-de-ia.md](geral/registo-de-uso-de-ia.md) | Registo de uso de IA |
| [geral/product-backlog.xlsx](geral/product-backlog.xlsx) | Product Backlog: stories, plano de sprints e resumo MoSCoW |

## Uma pasta por story

### [US01 — Registo com email pessoal](US01/README.md)

| Ficheiro | Conteúdo |
|---|---|
| [US01/README.md](US01/README.md) | Resumo da story, estado, código e testes |
| [US01/requisitos.md](US01/requisitos.md) | Requisitos funcionais e critérios de aceitação |
| [US01/use-case.md](US01/use-case.md) | Use case |
| [US01/bpmn.md](US01/bpmn.md) | Processo BPMN |
| [US01/prompt.md](US01/prompt.md) | Prompt usado para gerar o código com IA |
| [US01/diagramas/use-case.svg](US01/diagramas/use-case.svg) | Diagrama de use case |
| [US01/diagramas/bpmn.svg](US01/diagramas/bpmn.svg) | Diagrama BPMN (imagem) |
| [US01/diagramas/bpmn.bpmn](US01/diagramas/bpmn.bpmn) | Diagrama BPMN (ficheiro editável, BPMN 2.0) |

## Nova story

Crie `docs/USNN/` com a mesma estrutura da US01: `README.md`, `requisitos.md`, `use-case.md`, `bpmn.md`, `prompt.md` e `diagramas/`. Acrescente a pasta a este índice e atualize a tabela de estado no [README da raiz](../README.md#estado-do-projeto).
