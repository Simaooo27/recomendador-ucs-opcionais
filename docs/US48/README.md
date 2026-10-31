# US48 — Recolha completa das licenciaturas (DGES)

> **Como** pessoa indecisa, **quero** que o catálogo tenha todas as licenciaturas e mestrados integrados do concurso nacional, **para** não deixar de fora um curso que me sirva.

| | |
|---|---|
| Estado | Recolha feita a 29/10, por aceitar pelo PO. Revisão do Simão pendente |
| Sprint | Backlog (o PO decide se entra no Sprint 4) |
| Story points | 2 |
| Épico | E2 — Catálogo de cursos |
| Prioridade | Should |
| Requisitos de origem | RF05, RNF03 |
| Depende de | US04 (o script de recolha) |

## O que foi feito

1. O PO correu `python dados/recolher_dges.py descarregar` no seu computador. A recolha foi interrompida aos 1200 cursos e retomada no mesmo dia: o script salta as páginas já guardadas. Depois correu `processar`.
2. O `dados/catalogo-cursos.csv` passou de 174 para **1699 cursos**; os 174 anteriores ficaram iguais. Os números, e porque faltam notas e provas em alguns cursos, estão no [`dados/README.md`](../../dados/README.md#recolha-completa-us48-29102026).
3. A aplicação e os testes foram verificados com o catálogo completo. Os testes da US37 dependiam do catálogo de 174 cursos e foram corrigidos (PR #54). Na mesma verificação apareceu um erro real na US37, também corrigido nesse PR: os 42 cursos privados sem provas de ingresso chegavam para aplicar o filtro das notas.

Não há use case nem BPMN próprios: a story não muda o que a pessoa faz no site, só a quantidade de cursos. O processo da recolha é o da [US04](../US04/bpmn.md).

## Documentos

| Documento | Conteúdo |
|---|---|
| [requisitos.md](requisitos.md) | Critérios de aceitação e como foram verificados |
| [prompt.md](prompt.md) | O que foi pedido à IA |

## Código e dados

| Onde | O quê |
|---|---|
| `dados/catalogo-cursos.csv`, `dados/provas-ingresso.csv` | O catálogo completo e os nomes das provas, escritos por `processar` |
| `dados/README.md` | Contagens, o que falta e porquê, e os limites que ficam |
| `tests/medir_tempos.py` | Mede o tempo das páginas principais (RNF03); não corre com os testes automáticos |
