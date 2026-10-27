# Prompt — US35: nota de candidatura a cada curso

Pedido feito ao Claude (23/10/2026), seguindo as [regras de geração de código](../geral/02-regras-de-geracao-de-codigo.md).

---

**Contexto e pedido:** os mesmos da [US33](../US33/prompt.md): codificar o plano de candidatura antes de reescrever o backlog, para o PO ver a ideia.

**Decisões do Claude, aceites pelo PO:**

- As contas ficam em funções puras (`app/candidatura/calculos.py`), testadas com casos de resultado conhecido.
- Usa-se o conjunto de provas que dá a nota mais alta, preferindo um que conte para a colocação.
- Margem de 5 pontos para «perto do último colocado».
- A nota é sempre apresentada como estimativa (contingente geral, 1.ª fase).

**Documentação desta pasta (27/10):** escrita pelo Claude a partir do código do PR #44. Ao comparar o código com os critérios, a ficha mostrava a nota sem o aviso de estimativa; o aviso foi acrescentado à ficha, com um teste.

---

**Revisão humana:** pendente (Simão Almeida).
