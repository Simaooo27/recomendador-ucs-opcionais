# Prompt — US36: plano das 6 opções de candidatura

Pedido feito ao Claude (23/10/2026), seguindo as [regras de geração de código](../geral/02-regras-de-geracao-de-codigo.md).

---

**Contexto:** o PO acha que, no ensino superior português, as opcionais pesam pouco e que a decisão real de quem escolhe curso é a candidatura. Pediu para codificar primeiro o plano de candidatura (Concurso Nacional de Acesso, 6 opções) como substituto das opcionais, e só depois escrever o novo backlog.

**Pedido (resumo):** um plano com até 6 opções por ordem, a nota em cada uma e avisos que ajudem a fazer uma candidatura equilibrada.

**Decisões do Claude, aceites pelo PO:**

- Os botões são formulários (sem JavaScript), como no resto do site.
- Os avisos seguem as regras da candidatura: a pessoa fica na primeira opção em que a nota chegue, por isso pôr a mais fácil em 1.º lugar desperdiça as outras, e usar as 6 opções não prejudica as primeiras.
- Sugestões da mesma área da 1.ª opção onde a pessoa fica acima ou perto.
- O OptaBem não submete a candidatura.

**Documentação desta pasta (27/10):** escrita pelo Claude a partir do código do PR #44. Faltavam testes para os avisos de opções que não contam e de pré-requisitos e para juntar o curso escolhido como 1.ª opção; foram acrescentados.

---

**Revisão humana:** pendente (Simão Almeida).
