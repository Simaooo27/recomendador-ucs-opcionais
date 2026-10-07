# US01 — Registo com email institucional

> **Como** aluno, **quero** registar-me com o meu email institucional, **para que** apenas alunos da instituição possam avaliar e o sistema seja fiável.

| | |
|---|---|
| Estado | Feita |
| Sprint | Sprint 1 |
| Story points | 3 |
| Épico | E1 — Contas e perfis |
| Prioridade | Must |
| Requisito de origem | RF01 (ver [01-requisitos-funcionais-e-nao-funcionais.md](../geral/01-requisitos-funcionais-e-nao-funcionais.md)) |

## Documentos

| Documento | Conteúdo |
|---|---|
| [requisitos.md](requisitos.md) | Requisitos funcionais, mensagens, dados guardados e critérios de aceitação |
| [use-case.md](use-case.md) | Use case ([diagrama](diagramas/use-case.svg)) |
| [bpmn.md](bpmn.md) | Processo BPMN ([imagem](diagramas/bpmn.svg) · [ficheiro editável](diagramas/bpmn.bpmn)) |
| [prompt.md](prompt.md) | Prompt usado para gerar o código com IA |

## Código

[`app/auth/`](../../app/auth/): rotas (`routes.py`), casos de uso (`services.py`), validação (`validators.py`), ligações de confirmação (`tokens.py`) e SQL (`repository.py`). Os templates estão em [`app/templates/auth/`](../../app/templates/auth/).

## Testes

| Ficheiro | O que testa |
|---|---|
| [`tests/test_validators.py`](../../tests/test_validators.py) | Validação do email institucional e da palavra-passe |
| [`tests/test_registration.py`](../../tests/test_registration.py) | Registo, rejeições, duplicados, CSRF e cabeçalhos de segurança |
| [`tests/test_confirmation.py`](../../tests/test_confirmation.py) | Ligação de confirmação e ativação da conta |
| [`tests/test_app_factory.py`](../../tests/test_app_factory.py) | Configuração da aplicação e do envio de email |
| [`tests/base.py`](../../tests/base.py) | Base comum: aplicação com base de dados temporária e email simulado |

A tabela critério de aceitação → teste está na secção 5 de [requisitos.md](requisitos.md#5-critérios-de-aceitação-e-testes).
