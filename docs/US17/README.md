# US17 — Apagar a minha conta

> **Como** aluno, **quero** apagar a minha conta e todos os meus dados, **para** exercer o meu direito ao apagamento.

| | |
|---|---|
| Estado | Feita (aceite na Sprint Review do Sprint 3, 23/10) |
| Sprint | Sprint 3 (22/10 a 29/10) |
| Story points | 2 (era 3; âmbito reduzido a 22/10) |
| Épico | E4 — Privacidade |
| Prioridade | Must |
| Requisito de origem | RF17 (só o apagamento) e RNF01 (ver [01-requisitos-funcionais-e-nao-funcionais.md](../geral/01-requisitos-funcionais-e-nao-funcionais.md)) |
| Depende de | US02 (sessão iniciada) |

## A ideia em três pontos

1. **Na página inicial há «Apagar a minha conta e todos os meus dados».** A página seguinte diz exatamente o que se perde.
2. **Confirma-se com a palavra-passe.** Com a palavra-passe errada, nada é apagado.
3. **Apaga tudo de uma vez:** a conta, a conversa de orientação, as decisões do percurso e o registo de pedidos ao LLM. A sessão termina e a página de apresentação confirma que os dados foram apagados.

**Decisão do PO (22/10):** a story original também pedia a exportação dos dados. Ficou só o apagamento, que é o essencial para o RGPD e era a recomendação do ponto 11 dos requisitos. A exportação fica no backlog.

## Experimentar

Iniciar sessão como aluno, descer até ao fim da página inicial («A sua conta») e carregar em **«Apagar a minha conta e todos os meus dados»**.

## Documentos

| Documento | Conteúdo |
|---|---|
| [requisitos.md](requisitos.md) | Requisitos funcionais e critérios de aceitação, com os testes de cada um |
| [use-case.md](use-case.md) | Use case ([diagrama](diagramas/use-case.svg)) |
| [bpmn.md](bpmn.md) | Processo BPMN ([imagem](diagramas/bpmn.svg) · [ficheiro editável](diagramas/bpmn.bpmn)) |
| [prompt.md](prompt.md) | Pedido feito à IA para gerar o código |

Os diagramas são gerados por [`diagramas/gerar.py`](diagramas/gerar.py): `python docs/US17/diagramas/gerar.py docs/US17/diagramas`.

## Código e testes

| Onde | O quê |
|---|---|
| `app/auth/routes.py` | `GET` e `POST /auth/conta/apagar` (só com sessão de aluno; o POST tem CSRF) |
| `app/auth/services.py` | `delete_account`: verifica a palavra-passe e apaga |
| `app/auth/repository.py` | `delete_user`: um só `DELETE`; o resto sai por `ON DELETE CASCADE` (`app/schema.sql`) |
| `app/templates/auth/apagar.html` | Página de confirmação |
| `app/templates/home.html` | Secção «A sua conta», no fim da página inicial |
| `app/templates/base.html` | Avisos com margens na página de apresentação |
| `app/texts.py` | Textos `HOME_CONTA_*` e `APAGAR_*`; política de privacidade provisória |
| `tests/test_apagar_conta.py` | 12 testes |
