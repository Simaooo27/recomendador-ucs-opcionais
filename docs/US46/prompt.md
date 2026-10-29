# Prompt — US46: exportar os meus dados

Pedido feito ao Claude (29/10/2026), seguindo as [regras de geração de código](../geral/02-regras-de-geracao-de-codigo.md).

---

**Contexto:** a 29/10, o PO pediu ao Claude para fazer o código que faltava no product backlog, sem mexer no GitHub enquanto o Simão podia estar a trabalhar lá, para o rever depois. A US46 estava no Backlog desde 27/10, com a parte do RF17 que saiu da US17 a 22/10.

**Pedido (resumo):** implementar as stories do backlog que ainda não tinham código (US37, US38, US39, US46 e US47), uma por ramo, com testes para cada critério de aceitação.

**Decisões do Claude, aceites pelo PO:**

- Ficheiro JSON, porque é o formato que outro programa lê sem conversões (portabilidade).
- Ficam de fora o hash da palavra-passe, o valor interno da confirmação e o código da ligação de partilha: não são dados da pessoa e facilitariam um ataque à conta.
- Uma opção do plano que saiu do catálogo fica no ficheiro, sem nome: é um dado da pessoa.

**29/10:** o PO testou no seu computador e decidiu pôr a story no Sprint 4 como «Feito». A documentação desta pasta foi escrita pelo Claude a partir do código.

---

**Revisão humana:** pendente (Simão Almeida).
