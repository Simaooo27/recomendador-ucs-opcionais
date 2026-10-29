# Prompt — US39: corrigir e esconder cursos do catálogo

Pedido feito ao Claude (29/10/2026), seguindo as [regras de geração de código](../geral/02-regras-de-geracao-de-codigo.md).

---

**Contexto:** a 29/10, o PO pediu ao Claude para fazer o código que faltava no product backlog, sem mexer no GitHub enquanto o Simão podia estar a trabalhar lá. A US39 estava no Backlog desde 23/10, a partir da sugestão de um colega (editar a base de dados na área de gestão), reescrita com uma necessidade concreta.

**Pedido (resumo):** implementar as stories do backlog que ainda não tinham código (US37, US38, US39, US46 e US47), uma por ramo, com testes para cada critério de aceitação.

**Decisões do Claude, aceites pelo PO:**

- As correções ficam numa tabela própria e são aplicadas sobre o ficheiro da DGES no único ponto por onde a aplicação lê o catálogo, para uma recolha nova não as apagar e para o curso mudar em todas as páginas.
- Só a descrição, as saídas profissionais e a visibilidade: os números vêm da DGES.
- O histórico guarda o nome do administrador (e não o identificador), para ficar mesmo que a conta dele seja removida.
- Depois de o PO perguntar o que faltava para a aplicação funcionar sem erros, o plano passou a avisar quando uma opção foi escondida, em vez de ela desaparecer.

**29/10:** o PO testou no seu computador e decidiu pôr a story no Sprint 4 como «Feito». A documentação desta pasta foi escrita pelo Claude a partir do código.

---

**Revisão humana:** pendente (Simão Almeida).
