# Prompt — US45: plano B: 2.ª fase

Pedido feito ao Claude (23/10/2026), seguindo as [regras de geração de código](../geral/02-regras-de-geracao-de-codigo.md).

---

**Contexto:** a 23/10, depois de ver o protótipo do plano de candidatura (US33 a US36), o PO pediu mais ideias para o plano. O Claude propôs várias; o PO escolheu «que exames me abrem mais portas» e o plano B da 2.ª fase e pediu para as implementar antes do sprint, para as ver a funcionar.

**Pedido (resumo):** implementar as duas ideias escolhidas no plano de candidatura.

**Decisões do Claude, aceites pelo PO:**

- Usar os dados da 2.ª fase de 2025 como referência, com aviso.
- Só cursos das mesmas áreas e fora do plano, para ser uma alternativa e não uma repetição.
- O PO encontrou um erro depois do primeiro teste: a secção não aparecia por um nome repetido no template; foi corrigido (PR #44).

**27/10:** o PO pôs a story no Sprint 4 (era Backlog na reestruturação da manhã), porque é parte importante do produto e o código já estava feito. A documentação desta pasta foi escrita pelo Claude a partir do código do PR #44. O teste da página passou a verificar também o aviso das vagas.

---

**Revisão humana:** pendente (Simão Almeida).
