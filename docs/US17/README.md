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

1. **Em «A minha conta» (ícone de conta na barra do topo) há «Apagar a minha conta e todos os meus dados»** (desde 23/10; antes ficava no fim da página inicial). A página seguinte diz exatamente o que se perde.
2. **Confirma-se com a palavra-passe.** Com a palavra-passe errada, nada é apagado.
3. **Apaga tudo de uma vez:** a conta, a conversa de orientação, as decisões do percurso e o registo de pedidos ao LLM. A sessão termina e a página de apresentação confirma que os dados foram apagados.

**Decisão do PO (22/10):** a story original também pedia a exportação dos dados. Ficou só o apagamento, que é o essencial para o RGPD e era a recomendação do ponto 11 dos requisitos. A exportação fica no backlog.

## Experimentar

Iniciar sessão como aluno, abrir o ícone de conta na barra do topo, escolher «A minha conta» e carregar em **«Apagar a minha conta e todos os meus dados»**.

## Definition of Done da US17

A US17 só conta como «Feita» quando todas as caixas estiverem marcadas. As primeiras são os critérios de aceitação desta story (o «Confirmation» dos três C); as outras são o mínimo que a equipa exige a todas. Verificado a 31/10/2026, com 541 testes automáticos a passar.

**Critérios de aceitação desta story**

- [x] Apagar remove a conta, a conversa e as decisões (e os pedidos ao LLM) (4 testes automáticos, todos a passar)
- [x] A ação de apagar pede confirmação (10 testes automáticos, todos a passar)
- [x] A política de privacidade é verdadeira (2 testes automáticos, todos a passar)
- Fora do âmbito desta story: Exportação em JSON/CSV (decisão registada em requisitos.md; passou a ser a US46)

**Mínimo da equipa**

- [x] Testes a passar: os desta story e os 541 do projeto
- [x] Código revisto por outro elemento, com atenção a RNF01, RNF02, RNF06, RNF09, RNF10, RNF11: PR #39 juntado pelo Simão
- [x] Código gerado por IA assinalado no [registo de uso de IA](../geral/registo-de-uso-de-ia.md)
- [x] Documentação em `docs/US17/`: requisitos.md, use-case.md, bpmn.md, prompt.md
- [x] Sem dívida técnica por registar
- [x] Funciona na demonstração: Sprint Review do Sprint 3 (23/10), testada pelos dois Product Owners
- [x] Aceite pelo Product Owner: Sprint Review do Sprint 3 (23/10)

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
| `app/templates/auth/conta.html` | Página «A minha conta» (/auth/conta), com a ligação para apagar (desde 23/10; antes era uma secção no fim de `home.html`) |
| `app/templates/base.html` | Avisos com margens na página de apresentação |
| `app/texts.py` | Textos `HOME_CONTA_*` e `APAGAR_*`; política de privacidade provisória |
| `tests/test_apagar_conta.py` | 12 testes |
