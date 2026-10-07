# US02 — Autenticação: requisitos funcionais

> **Como** aluno, **quero** iniciar e terminar sessão, **para** aceder às minhas avaliações e recomendações de forma segura.

| | |
|---|---|
| Épico | E1 — Contas e perfis |
| Prioridade | Must · 2 story points · Sprint 1 |
| Requisito de origem | RF02 (início e fim de sessão) |
| Atores | Aluno |
| Artefactos | [Use case](use-case.md) · [BPMN](bpmn.md) · [Prompt](prompt.md) |

## 1. Âmbito

**Dentro:** início de sessão com email e palavra-passe, fim de sessão e proteção das páginas privadas.

**Fora:** recuperação de palavra-passe (prevista no RF02, ainda sem story); limite de tentativas e captcha (futuro); «lembrar-me» (sessão termina ao fechar o navegador).

## 2. Requisitos funcionais da US02

| ID | Requisito |
|---|---|
| **RF02.1** | O formulário de início de sessão pede email e palavra-passe e exige token CSRF válido. |
| **RF02.2** | O email é normalizado da mesma forma que no registo (RF01.2): sem espaços nas pontas e em minúsculas. |
| **RF02.3** | Com credenciais corretas e conta ativa, o sistema começa uma sessão nova (os dados de sessão anteriores e o token CSRF são descartados) e mostra a página inicial do aluno. |
| **RF02.4** | Com email inexistente, palavra-passe errada ou campos vazios, o sistema mostra sempre a mesma mensagem («Email ou palavra-passe incorretos.», HTTP 401), sem indicar qual falhou. A verificação demora o mesmo tempo quando o email não existe. |
| **RF02.5** | Com a palavra-passe correta mas a conta por confirmar, a sessão não é iniciada e o aluno é informado de que tem de confirmar o email (HTTP 403). Com a palavra-passe errada, aplica-se o RF02.4. |
| **RF02.6** | Terminar sessão apaga a sessão e volta à página de início de sessão. Só por `POST` com token CSRF (um `GET` não termina a sessão). |
| **RF02.7** | Quem abre uma página privada sem sessão é redirecionado para o início de sessão. Uma sessão de uma conta que deixou de existir ou de estar ativa é terminada. |
| **RF02.8** | A palavra-passe nunca é devolvida ao navegador nem registada em logs; em caso de erro, o formulário volta só com o email. |
| **RF02.9** | A página inicial (`/`) leva à área do aluno com sessão iniciada e ao início de sessão sem ela. As páginas de registo e de início de sessão têm ligações uma para a outra. |

## 3. Mensagens ao utilizador

Os textos em uso estão em [`app/texts.py`](../../app/texts.py).

| Situação | Mensagem |
|---|---|
| Credenciais erradas ou campos vazios | Email ou palavra-passe incorretos. |
| Conta por confirmar | Ainda não confirmou o seu email. Abra a ligação que lhe enviámos para ativar a conta. |
| Sessão iniciada (página inicial) | Olá, *email* |

## 4. Dados

Não há tabelas novas. A sessão guarda apenas o `user_id` (cookie assinado com a `SECRET_KEY`, `HttpOnly` e `SameSite=Lax`).

## 5. Critérios de aceitação e testes

| Critério da story | Requisitos | Testes automáticos (`tests/test_login.py`) |
|---|---|---|
| Login com email e palavra-passe. | RF02.1 a RF02.3, RF02.5 | `SuccessfulLoginTests` (5 testes: sessão criada, email normalizado, sessão renovada, redirecionamentos, botão «Terminar sessão»); `InactiveAccountTests` (2) |
| Mensagem genérica em caso de erro. | RF02.4, RF02.8 | `FailedLoginTests` (4 testes: palavra-passe errada, email inexistente, campos vazios, palavra-passe nunca devolvida) |
| O logout termina a sessão. | RF02.6 | `LogoutTests` (3 testes: termina a sessão, exige CSRF, `GET` não permitido) |
| Páginas privadas redirecionam para o login. | RF02.7, RF02.9 | `PrivatePageTests` (3 testes); `LoginFormTests` (2 testes) |
| (Transversal) segurança | RF02.1, RNF02 | `LoginSecurityTests` (CSRF no login) |

## 6. Requisitos não funcionais aplicáveis

RNF02 (hash, CSRF, sessão renovada no login, mensagem que não revela contas), RNF04 (responsivo), RNF06 (testes automáticos), RNF08 (commits `US02: ...`), RNF09 (uso de IA documentado), RNF10 (acessibilidade: erro ligado aos campos com `aria-describedby`) e RNF11 (português de Portugal).

## 7. Decisões e questões em aberto

| # | Questão | Estado |
|---|---|---|
| 1 | Limite de tentativas falhadas (proteção contra adivinhar palavras-passe). | Fora do Sprint 1; a propor como story |
| 2 | Recuperação de palavra-passe (RF02) não tem story. | Por decidir pelo PO |
| 3 | A página inicial (`/inicio`) é provisória: vai mostrar o catálogo (US04) e as recomendações. | Aceite |
| 4 | A página `/` passou a levar ao início de sessão (antes levava ao registo). | Aceite |
