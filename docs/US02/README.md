# US02 — Autenticação

> **Como** aluno, **quero** iniciar e terminar sessão, **para** aceder às minhas avaliações e recomendações de forma segura.

| | |
|---|---|
| Estado | Feita |
| Sprint | Sprint 1 |
| Story points | 2 |
| Épico | E1 — Contas e perfis |
| Prioridade | Must |
| Requisito de origem | RF02, parte de início e fim de sessão (ver [01-requisitos-funcionais-e-nao-funcionais.md](../geral/01-requisitos-funcionais-e-nao-funcionais.md)) |
| Depende de | [US01](../US01/README.md): só contas confirmadas podem entrar |

## Documentos

| Documento | Conteúdo |
|---|---|
| [requisitos.md](requisitos.md) | Requisitos funcionais, mensagens e critérios de aceitação |
| [use-case.md](use-case.md) | Use case ([diagrama](diagramas/use-case.svg)) |
| [bpmn.md](bpmn.md) | Processo BPMN ([imagem](diagramas/bpmn.svg) · [ficheiro editável](diagramas/bpmn.bpmn)) |
| [prompt.md](prompt.md) | Pedido feito à IA para gerar o código |

## Código

| Ficheiro | O que faz |
|---|---|
| [`app/auth/services.py`](../../app/auth/services.py) | `authenticate`: verifica email e palavra-passe |
| [`app/auth/sessions.py`](../../app/auth/sessions.py) | Guarda e lê o utilizador na sessão; `login_required` para páginas privadas |
| [`app/auth/routes.py`](../../app/auth/routes.py) | `GET/POST /auth/entrar` e `POST /auth/sair` |
| [`app/main.py`](../../app/main.py) | Página inicial do aluno (`/inicio`, privada) |
| [`app/templates/auth/login.html`](../../app/templates/auth/login.html), [`app/templates/home.html`](../../app/templates/home.html) | Páginas de início de sessão e inicial |
| [`app/texts.py`](../../app/texts.py) | Textos (secções «Iniciar sessão» e «Página inicial do aluno») |

## Testes

[`tests/test_login.py`](../../tests/test_login.py): 20 testes. A tabela critério de aceitação → teste está na secção 5 de [requisitos.md](requisitos.md#5-critérios-de-aceitação-e-testes).
