# US03 — Perfis de aluno e administrador: requisitos funcionais

> **Como** administrador, **quero** ter uma conta própria, separada das contas dos alunos e numa área escondida, **para** gerir a aplicação sem que os alunos vejam ou consigam usar essas funções.

| | |
|---|---|
| Épico | E1 — Contas e perfis |
| Prioridade | Must · 5 story points · Sprint 1 |
| Requisito de origem | RF04 |
| Atores | Equipa (instala a aplicação), Administrador, Aluno |
| Artefactos | [Use case](use-case.md) · [BPMN](bpmn.md) · [Prompt](prompt.md) |

## 1. Âmbito

**Dentro:** contas de administrador separadas dos alunos, criação do primeiro administrador no terminal, início e fim de sessão na área de gestão, criação e remoção de administradores pela própria gestão, área escondida das páginas dos alunos.

**Fora:** recuperar a palavra-passe de um administrador (outro administrador remove e volta a criar a conta; se não houver nenhum, a equipa usa o terminal); limite de tentativas; as funções de gestão em si (US04, US16, US19).

## 2. Requisitos funcionais da US03

| ID | Requisito |
|---|---|
| **RF04.1** | Os administradores têm contas próprias (tabela `admins`), com nome de utilizador e palavra-passe, **sem email**. Não são contas de aluno e não entram pelo início de sessão dos alunos. |
| **RF04.2** | O registo público cria sempre contas de aluno; não há forma de, a partir dele, criar um administrador. |
| **RF04.3** | O comando `flask --app app create-admin` cria um administrador. Pede o nome e a palavra-passe (duas vezes, sem a mostrar no ecrã). Serve para o **primeiro** administrador; fica registado como «criado no terminal». |
| **RF04.4** | Nome de utilizador: 3 a 30 caracteres (letras minúsculas, números, ponto, hífen ou sublinhado), único sem distinguir maiúsculas. Palavra-passe: as mesmas regras dos alunos (RF01.4), guardada só como hash. |
| **RF04.5** | A área de gestão tem início de sessão próprio (`/gestao/entrar`), com a mesma mensagem genérica para nome inexistente e palavra-passe errada. Regista a data da última entrada. |
| **RF04.6** | As páginas da gestão, sem sessão de administrador, levam ao início de sessão da gestão. Uma sessão de aluno não dá acesso. A sessão de um administrador removido termina no pedido seguinte. |
| **RF04.7** | A área de gestão está **escondida**: nenhuma página dos alunos tem ligações para ela; o endereço é configurável (`ADMIN_URL_PREFIX`, por omissão `/gestao`); as páginas pedem para não ser indexadas (`noindex`). |
| **RF04.8** | Um administrador vê a lista de administradores (nome, data de criação, quem o criou, última entrada) e cria outros administradores, com as regras do RF04.4. |
| **RF04.9** | Um administrador remove outros administradores, mas **não a si próprio** (assim fica sempre pelo menos um). |
| **RF04.10** | Com sessão de administrador, a barra do topo mostra «Gestão», «Painel», «Administradores», o nome do administrador e «Terminar sessão». |

## 3. Mensagens

Os textos em uso estão em [`app/texts.py`](../../app/texts.py), secção «Área de gestão».

| Situação | Mensagem |
|---|---|
| Credenciais erradas | Nome de utilizador ou palavra-passe incorretos. |
| Nome inválido | Use 3 a 30 caracteres: letras minúsculas, números, ponto, hífen ou sublinhado. |
| Nome repetido | Já existe um administrador com este nome. |
| Criado / removido | Administrador «*nome*» criado. / Administrador «*nome*» removido. |
| Remover-se a si próprio | Não pode remover a sua própria conta. Peça a outro administrador. |
| Terminal: criado | Administrador «*nome*» criado. Entre em /gestao/entrar. |

## 4. Dados

Tabela nova `admins`: `id`, `username` (único, sem distinção de maiúsculas), `password_hash`, `created_at`, `created_by` (nome de quem o criou; vazio = terminal), `last_login_at`. Para bases de dados já existentes basta correr `flask --app app init-db` (cria só o que falta).

A coluna `role` da tabela `users` mantém-se (todos os alunos ficam `aluno`) mas deixa de ser usada para administradores.

## 5. Critérios de aceitação e testes

| Critério da story | Requisitos | Testes automáticos (`tests/test_gestao.py`) |
|---|---|---|
| Os administradores têm contas próprias, sem email e separadas dos alunos. | RF04.1, RF04.2, RF04.4 | `SeparateAccountsTests` (5 testes) |
| O primeiro administrador é criado no terminal. | RF04.3, RF04.4 | `FirstAdminCommandTests` (5 testes, incl. a palavra-passe não aparecer no ecrã) |
| A gestão tem início de sessão próprio, com mensagem genérica. | RF04.5, RF04.6 | `AdminLoginTests` (6 testes) |
| A área de gestão está escondida dos alunos. | RF04.6, RF04.7 | `HiddenAreaTests` (5 testes) |
| Um administrador cria e remove outros administradores. | RF04.8, RF04.9, RF04.10 | `ManageAdminsTests` (8 testes) |

## 6. Requisitos não funcionais aplicáveis

RNF02 (hash, CSRF em todos os formulários, mensagem genérica, contas separadas), RNF06 (testes automáticos), RNF08 (commits `US03: ...`), RNF09 (uso de IA documentado), RNF10 (tabela com cabeçalhos, campos com etiqueta e erro ligado) e RNF11 (português de Portugal).

## 7. Decisões e questões em aberto

| # | Questão | Estado |
|---|---|---|
| 1 | Administradores como contas independentes, sem email, em vez de alunos promovidos. | **Decidido** pelo PO (07/10/2026) |
| 2 | Área de gestão escondida, num endereço configurável e sem ligações nas páginas dos alunos. Esconder o endereço não substitui a autenticação: é uma camada extra. | **Decidido** pelo PO (07/10/2026) |
| 3 | O primeiro administrador tem de ser criado fora da aplicação (terminal), por quem a instala. | Aceite |
| 4 | Limite de tentativas no início de sessão da gestão. | Fora do Sprint 1; a propor como story |
