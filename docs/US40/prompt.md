# Prompt — US40: quanto preciso no exame?

Pedido feito ao Claude (23/10/2026), seguindo as [regras de geração de código](../geral/02-regras-de-geracao-de-codigo.md).

---

**Contexto:** a 23/10, depois de ver o protótipo do plano de candidatura (US33 a US36), o PO pediu mais ideias para o plano. O Claude propôs várias; o PO escolheu «quanto preciso no exame», a tendência do último colocado, a procura do curso e partilhar o plano e pediu para as implementar antes do sprint, para as ver a funcionar.

**Pedido (resumo):** implementar as quatro ideias escolhidas no plano de candidatura e na ficha do curso.

**Decisões do Claude, aceites pelo PO:**

- Escolher sempre o conjunto de provas em que é mais fácil chegar ao último colocado.
- Respeitar o mínimo de cada prova e arredondar para cima.
- Mostrar também em valores (0 a 20), porque muitos alunos pensam assim.

**27/10:** o PO pôs a story no Sprint 4 (era Backlog na reestruturação da manhã), porque é parte importante do produto e o código já estava feito. A documentação desta pasta foi escrita pelo Claude a partir do código do PR #44. Faltava um teste para «Precisa de X em Y» no plano; foi acrescentado.

---

**Revisão humana:** pendente (Simão Almeida).
