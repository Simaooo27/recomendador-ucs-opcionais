# US48 — Recolha completa das licenciaturas (DGES)

> **Como** pessoa indecisa, **quero** que o catálogo tenha todas as licenciaturas e mestrados integrados do concurso nacional, **para** não deixar de fora um curso que me sirva.

| | |
|---|---|
| Estado | Recolha feita a 29/10; na main desde 31/10. Por aceitar pelo PO na Sprint Review. Revisão do Simão pendente |
| Sprint | Sprint 4 (entrou a 31/10, a pedido do PO) |
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

## Definition of Done da US48

A US48 só conta como «Feita» quando todas as caixas estiverem marcadas. As primeiras são os critérios de aceitação desta story (o «Confirmation» dos três C); as outras são o mínimo que a equipa exige a todas. Verificado a 31/10/2026, com 541 testes automáticos a passar.

**Critérios de aceitação desta story**

- [x] O script da US04 corre até ao fim sobre todas as instituições do concurso nacional (verificado à mão pelo PO a 29/10: 1704 páginas guardadas, 1699 cursos)
- [x] O `dados/README.md` diz quantos cursos ficaram e quantos não têm condições de acesso ou nota do último colocado (verificado à mão: 664 cursos sem nota de 2025 e 42 sem provas, com o motivo de cada grupo)
- [x] A aplicação e os testes continuam a funcionar com o catálogo completo (RNF03: páginas em menos de 2 s) (verificado a 31/10: todos os testes a passar com o catálogo completo; a página mais lenta abriu em 53 ms com `tests/medir_tempos.py`)

**Mínimo da equipa**

- [x] Testes a passar: os desta story e os 541 do projeto
- [ ] Código revisto por outro elemento: o PR #58 foi juntado pelo próprio autor. **Falta a revisão do Simão**
- [x] Código gerado por IA assinalado no [registo de uso de IA](../geral/registo-de-uso-de-ia.md)
- [x] Documentação em `docs/US48/`: requisitos.md, prompt.md (sem use case nem BPMN: a story não muda o que a pessoa faz no site)
- [x] Sem dívida técnica por registar: limitação conhecida e registada — o assistente só recebe 80 cursos por área (7 áreas têm mais) e só 29 cursos têm descrição; tempos medidos sem rede
- [ ] Funciona na demonstração: a mostrar na Sprint Review do Sprint 4 (05/11)
- [ ] Aceite pelo Product Owner: recolha feita a 29/10; falta o PO aceitá-la (e decidir se conta no Sprint 4)

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
