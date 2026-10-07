# Prompt — US03: perfis de aluno e administrador

Pedido feito ao Claude (2026-10-07), depois do replaneamento do Sprint 1, seguindo as [regras de geração de código](../geral/02-regras-de-geracao-de-codigo.md).

---

**Primeira versão** (substituída): administrador como conta de aluno promovida por comando (`promote-admin`).

**Revisão do Product Owner:** o administrador não deve ser uma conta de aluno nem precisar de email; quem atribui administradores deve ser um administrador; e a área de administração não deve estar à vista dos alunos. «Faz a alternativa que consideres mais real.»

**Pedido final:** implementa a US03 com administradores independentes:

1. Tabela própria `admins` (nome de utilizador, palavra-passe em hash, quem criou, última entrada), sem email; o registo público cria só alunos.
2. O primeiro administrador é criado no terminal (`flask --app app create-admin`, sem mostrar a palavra-passe); os seguintes são criados e removidos por um administrador na área de gestão; ninguém se remove a si próprio.
3. Área de gestão escondida: endereço configurável (`/gestao` por omissão), sem ligações nas páginas dos alunos, páginas com `noindex`, início de sessão próprio com mensagem genérica.
4. Todos os textos em `app/texts.py`, um teste automático por critério, documentação em `docs/US03/` com a estrutura das outras stories.

---

**Revisão humana:** pendente (Simão Almeida), no Pull Request da US03.
