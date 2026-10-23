# US17 — Apagar a minha conta: requisitos funcionais

> **Como** aluno, **quero** apagar a minha conta e todos os meus dados, **para** exercer o meu direito ao apagamento.

| | |
|---|---|
| Épico | E4 — Privacidade |
| Prioridade | Must · 2 story points · Sprint 3 |
| Requisitos de origem | RF17 (apagamento), RNF01 |
| Atores | Aluno com sessão iniciada |
| Artefactos | [Use case](use-case.md) · [BPMN](bpmn.md) · [Prompt](prompt.md) |

## 1. Âmbito

**Dentro:** apagar a conta do aluno e todos os dados ligados a ela, com confirmação pela palavra-passe; terminar a sessão; corrigir a política de privacidade provisória para não prometer o que não existe.

**Fora:** exportar os dados (fica no backlog, decisão do PO de 22/10); apagar contas de administradores ou de outros alunos; recuperar uma conta apagada.

## 2. Requisitos funcionais da US17

| ID | Requisito |
|---|---|
| **RF17.1** | A página «A minha conta» (/auth/conta, no menu do ícone de conta da barra do topo) tem a ligação «Apagar a minha conta e todos os meus dados». Alterado a 23/10 (revisão estética, decisão do PO): antes ficava no fim da página inicial. |
| **RF17.2** | A página `/auth/conta/apagar` (só com sessão de aluno) diz que a ação não pode ser desfeita e enumera o que é apagado: a conta e o email, a conversa de orientação, as decisões do percurso e o registo de pedidos ao assistente. Abrir a página não apaga nada. |
| **RF17.3** | A confirmação pede a palavra-passe atual. Com a palavra-passe errada ou vazia, nada é apagado e a página diz porquê (422). O pedido tem proteção CSRF. |
| **RF17.4** | Com a palavra-passe certa, a conta é apagada e, com ela, todas as linhas ligadas: `conversas_orientacao`, `decisoes` e `pedidos_llm` (`ON DELETE CASCADE`). Os dados de outros alunos não mudam. |
| **RF17.5** | Depois de apagar, a sessão termina e a página de apresentação mostra «A sua conta e todos os seus dados foram apagados.». O mesmo email pode voltar a registar-se. |
| **RF17.6** | A política de privacidade provisória explica como apagar a conta e deixa de prometer a exportação. |

## 3. Mensagens

| Situação | Mensagem |
|---|---|
| Ligação em «A minha conta» | Apagar a minha conta e todos os meus dados |
| Introdução | Esta ação não pode ser desfeita. São apagados para sempre: (lista) |
| Campo | Para confirmar, escreva a sua palavra-passe |
| Palavra-passe errada | A palavra-passe não está certa. A conta não foi apagada. |
| Depois de apagar | A sua conta e todos os seus dados foram apagados. |

## 4. Dados

Sem tabelas novas. A conversa, as decisões e os pedidos ao LLM já referiam `users(id)` com `ON DELETE CASCADE`, e a ligação à base de dados liga `PRAGMA foreign_keys`. O apagamento é um só `DELETE` em `users`, numa transação.

## 5. Critérios de aceitação e testes

| Critério (âmbito de 22/10) | Requisitos | Testes automáticos (`tests/test_apagar_conta.py`) |
|---|---|---|
| Apagar remove a conta, a conversa e as decisões (e os pedidos ao LLM). | RF17.4, RF17.5 | `ApagarTudoTests` (4 testes: todos os dados, fim da sessão e aviso, outros alunos intactos, voltar a registar o email) |
| A ação de apagar pede confirmação. | RF17.2, RF17.3 | `ConfirmacaoTests` (4 testes: palavra-passe errada, vazia, sem CSRF, abrir a página não apaga); `PaginaTests` (3 testes) |
| A política de privacidade é verdadeira. | RF17.6 | `PoliticaDePrivacidadeTests` |
| ~~Exportação em JSON/CSV.~~ | — | Fora do âmbito: backlog (22/10) |

## 6. Requisitos não funcionais aplicáveis

RNF01 (direito ao apagamento), RNF02 (CSRF no POST; a palavra-passe nunca volta à página), RNF06 (testes sem rede), RNF09 (uso de IA documentado), RNF10 (erro ligado ao campo com `aria-describedby`; aviso com `role="status"`), RNF11 (português de Portugal). Verificado no navegador a 1280 px e 390 px, em claro e escuro.

## 7. Decisões e questões em aberto

| # | Questão | Estado |
|---|---|---|
| 1 | Só o apagamento; a exportação fica no backlog. | **Decidido** pelo PO (22/10) |
| 2 | A confirmação é a palavra-passe (e não uma caixa «tenho a certeza»): evita apagar por engano ou com o computador de outra pessoa com a sessão aberta. | Proposta do Claude, **a confirmar pelo PO** |
| 3 | O registo de pedidos ao LLM (PR #36) também é apagado: é um dado ligado à conta. | Proposta do Claude, **a confirmar pelo PO** |
