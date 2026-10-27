# Prompt — US04: catálogo de licenciaturas recolhido da DGES

Pedidos feitos ao Claude (23/10/2026), seguindo as [regras de geração de código](../geral/02-regras-de-geracao-de-codigo.md).

---

**Contexto:** até 23/10 a US04 previa que o administrador importasse um CSV na área de gestão. Um colega sugeriu recolher os cursos diretamente da DGES; o PO decidiu avançar com a recolha, primeiro o código e só depois a atualização da story e da documentação.

**Pedido (resumo):** recolher as licenciaturas do site público da DGES sem sobrecarregar o site e sem a aplicação depender da internet; manter as descrições escritas pela equipa; preparar a aplicação para um catálogo de centenas de cursos.

**Decisões do Claude, aceites pelo PO:**

- O script corre no computador da equipa e guarda as páginas antes de as ler, para retomar se for interrompido e para ler outra vez sem voltar a pedir nada à DGES.
- Um pedido a cada 2 segundos, com identificação do projeto no cabeçalho do pedido.
- Lista com páginas de 24 cursos e filtro por área no assistente acima de 150 cursos.

**Decisão do PO (27/10):** a recolha de todas as licenciaturas passa para a US48, porque exige o computador ligado uma noite inteira.

**Documentação desta pasta:** escrita pelo Claude a 27/10, a partir do código do PR #44.

---

**Revisão humana:** pendente (Simão Almeida).
