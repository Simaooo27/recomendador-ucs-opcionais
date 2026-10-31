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

## Definition of Done da US02

A US02 só conta como «Feita» quando todas as caixas estiverem marcadas. As primeiras são os critérios de aceitação desta story (o «Confirmation» dos três C); as outras são o mínimo que a equipa exige a todas. Verificado a 31/10/2026, com 541 testes automáticos a passar.

**Critérios de aceitação desta story**

- [x] Login com email e palavra-passe (7 testes automáticos, todos a passar)
- [x] Mensagem genérica em caso de erro (4 testes automáticos, todos a passar)
- [x] O logout termina a sessão (3 testes automáticos, todos a passar)
- [x] Páginas privadas redirecionam para o login (5 testes automáticos, todos a passar)
- [x] (Transversal) segurança (1 teste automático, a passar)
- [x] (Pedido do PO) mostrar a palavra-passe (4 testes automáticos, todos a passar)

**Mínimo da equipa**

- [x] Testes a passar: os desta story e os 541 do projeto
- [ ] Código revisto por outro elemento, com atenção a RNF02, RNF04, RNF06, RNF08, RNF09, RNF10, RNF11: os PR #4 e #5 foram juntados pelo próprio autor. **Falta a revisão do Simão**
- [x] Código gerado por IA assinalado no [registo de uso de IA](../geral/registo-de-uso-de-ia.md)
- [x] Documentação em `docs/US02/`: requisitos.md, use-case.md, bpmn.md, prompt.md
- [x] Sem dívida técnica por registar
- [x] Funciona na demonstração: usada em todas as demonstrações seguintes (Sprint Review dos Sprints 2 e 3); o Sprint 1 não tem Sprint Review registada
- [x] Aceite pelo Product Owner: fecho do Sprint 1 (07/10)

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
