# US48 — Recolha completa das licenciaturas: critérios de aceitação

| Critério da story (backlog) | Como foi verificado | Resultado |
|---|---|---|
| O script da US04 corre até ao fim sobre todas as instituições do concurso nacional. | `descarregar` e `processar` corridos pelo PO a 29/10; 1704 páginas guardadas, das quais 5 de outros graus ficam de fora | 1699 cursos |
| O `dados/README.md` diz quantos cursos ficaram e quantos não têm condições de acesso ou nota do último colocado. | Contagens feitas a partir do CSV; uma página guardada aberta para confirmar que a nota em falta também falta na DGES; as 1704 páginas cruzadas com o `tipo_ensino` para confirmar a regra do ensino privado (RN12) | 664 sem nota de 2025, 42 sem provas, com o motivo de cada grupo |
| A aplicação e os testes continuam a funcionar com o catálogo completo (RNF03: páginas em menos de 2 s). | Testes automáticos com o catálogo completo, no `main` e com todos os PR do Sprint 4 juntos; `tests/medir_tempos.py` | Testes a passar (depois da correção da US37); páginas no máximo cerca de 70 ms |

## Questões em aberto

| # | Questão | Estado |
|---|---|---|
| 1 | Na conversa, cada área envia no máximo 80 cursos ao assistente; 7 áreas têm mais. Os cursos pequenos só chegam se a pessoa disser a localidade. | Em aberto: aceitar ou subir o limite (mais custo por pedido ao Gemini) |
| 2 | Só 29 cursos têm descrição escrita pela equipa; nos outros, as sugestões do assistente apoiam-se no nome e na área. | Em aberto (ponto 12 dos requisitos) |
| 3 | Os tempos foram medidos num computador de desenvolvimento, sem rede. No computador do PO e pelo túnel podem ser maiores. | Repetir com `tests/medir_tempos.py` |
