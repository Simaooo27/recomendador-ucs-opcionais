# Prompt — US37: assistente que conhece as minhas notas

Pedido feito ao Claude (29/10/2026), seguindo as [regras de geração de código](../geral/02-regras-de-geracao-de-codigo.md).

---

**Contexto:** a 29/10, o PO pediu ao Claude para fazer o código que faltava no product backlog, sem mexer no GitHub enquanto o Simão podia estar a trabalhar lá. A US37 estava no Backlog, com a nota de que os termos do Gemini excluem menores de 18.

**Pedido (resumo):** implementar as stories do backlog que ainda não tinham código (US37, US38, US39, US46 e US47), uma por ramo, com testes para cada critério de aceitação.

**Decisões do Claude, aceites pelo PO:**

- A autorização é uma caixa desmarcada ao começar a conversa, com o texto exato do que é enviado, e vale só para essa conversa.
- A média vai num intervalo de 2 valores e os exames só pelo nome; a nota de cada exame nunca sai do OptaBem.
- Quem filtra os cursos com prova em falta é o OptaBem, antes de enviar o catálogo, e não o LLM. Abaixo de 10 cursos, vai tudo e o aviso aparece no curso sugerido.
- Os testes usam o catálogo da DGES, porque o do MVP não tem provas de ingresso.

**29/10:** o PO testou no seu computador e decidiu pôr a story no Sprint 4 como «Feito». A documentação desta pasta foi escrita pelo Claude a partir do código.

---

**Revisão humana:** pendente (Simão Almeida).
