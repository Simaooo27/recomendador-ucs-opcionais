# Prompt — US43: partilhar o plano

Pedido feito ao Claude (23/10/2026), seguindo as [regras de geração de código](../geral/02-regras-de-geracao-de-codigo.md).

---

**Contexto:** a 23/10, depois de ver o protótipo do plano de candidatura (US33 a US36), o PO pediu mais ideias para o plano. O Claude propôs várias; o PO escolheu «quanto preciso no exame», a tendência do último colocado, a procura do curso e partilhar o plano e pediu para as implementar antes do sprint, para as ver a funcionar.

**Pedido (resumo):** implementar as quatro ideias escolhidas no plano de candidatura e na ficha do curso.

**Decisões do Claude, aceites pelo PO:**

- Ligação só de leitura com código aleatório, em vez de partilhar com contas, para pais e explicadores não precisarem de conta.
- Mostrar só o primeiro nome e nunca a média nem os exames (minimização, RNF01).
- Desligar apaga o código, para a ligação antiga deixar de funcionar logo.
- O PO corrigiu depois um erro: a ligação usava `localhost` em vez do endereço do túnel (PR #44).

**27/10:** o PO pôs a story no Sprint 4 (era Backlog na reestruturação da manhã), porque é parte importante do produto e o código já estava feito. A documentação desta pasta foi escrita pelo Claude a partir do código do PR #44.

---

**Revisão humana:** pendente (Simão Almeida).
