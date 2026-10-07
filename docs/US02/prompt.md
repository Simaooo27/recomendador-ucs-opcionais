# Prompt — US02: autenticação

Pedido feito ao Claude (2026-10-07), a partir da secção 6.2 do relatório de análise de requisitos e das [regras de geração de código](../geral/02-regras-de-geracao-de-codigo.md).

---

Implementa a **US02 — Autenticação** («Como aluno, quero iniciar e terminar sessão, para aceder às minhas avaliações e recomendações de forma segura»), no mesmo estilo da US01 e seguindo `docs/geral/02-regras-de-geracao-de-codigo.md`.

Critérios de aceitação:
1. Login com email e palavra-passe.
2. Mensagem genérica em caso de erro.
3. O logout termina a sessão.
4. Páginas privadas redirecionam para o login.

Requisitos: os RF02.1 a RF02.8 da secção 6.2 do relatório (email normalizado como no registo; sessão nova no login; a mesma mensagem para email inexistente e palavra-passe errada; conta por confirmar não entra; logout só por `POST` com CSRF; a palavra-passe nunca volta ao navegador).

Restrições: Flask e `sqlite3`, sem dependências novas; rotas finas, regra de negócio em `services.py`, sessão num módulo próprio; todos os textos em `app/texts.py`; um teste automático por critério de aceitação, sem rede; documentação em `docs/US02/` com a estrutura da US01 (requisitos, use case, BPMN, prompt e diagramas).

---

**Revisão humana:** pendente (Simão Almeida), no Pull Request da US02.
