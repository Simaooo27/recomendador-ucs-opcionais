# Prompt — US31: escolher curso e linha do tempo do percurso

Pedido feito ao Claude (2026-10-20), seguindo as [regras de geração de código](../geral/02-regras-de-geracao-de-codigo.md).

---

**Contexto:** no Sprint Planning do Sprint 2 (20/10), o PO antecipou a US31 do Sprint 3, porque a US29 e a US30 foram feitas antes de o sprint começar (issue #27).

**Decisões do PO antes de começar:**

- Depois de escolher o curso, a conversa com o LLM é **apagada**; ficam só a data, os cursos sugeridos e o curso escolhido (ponto 15 dos requisitos).
- Confirmado com o Simão que ele não estava a fazer a US31, para não haver trabalho em duplicado (como aconteceu com a US30).

**Pedido (resumo), a partir dos critérios de aceitação do backlog:**

1. Escolher um dos cursos sugeridos, ou outro do catálogo; a escolha nunca é automática (RN10).
2. O curso e a instituição ficam no perfil (RF03).
3. Cada decisão fica registada com data, opções sugeridas e opção escolhida (RF35).
4. Linha do tempo com as decisões, da mais recente para a mais antiga.
5. Mudar de curso cria uma nova decisão.
6. Uma story por branch e por PR, testes a passar sem rede, documentação em `docs/US31/` com a estrutura das outras stories, Excel atualizado. Verificar com testes e não com capturas de ecrã.

**Decisões do Claude a confirmar pelo PO** (secção 7 de [requisitos.md](requisitos.md)):

- O curso do perfil é a decisão mais recente, sem coluna nova em `users`.
- A confirmação é uma página própria, que funciona sem JavaScript.
- O módulo `app/percurso.py` passou a pacote (`app/percurso/`), como previa a secção 5 de `03-arquitetura-e-padroes.md`; o que já existia (o padrão State) ficou em `__init__.py`, sem mudar de comportamento.

---

**Revisão humana:** pendente (Simão Almeida), no Pull Request da US31.
