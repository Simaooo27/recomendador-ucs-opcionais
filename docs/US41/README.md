# US41 — Tendência do último colocado

> **Como** candidato, **quero** ver como a nota do último colocado mudou de 2023 a 2025, **para** perceber se um curso está a ficar mais difícil de entrar.

| | |
|---|---|
| Estado | Feita: aceite pelo PO a 27/10, antes do início formal do Sprint 4 (código de 23/10, documentação e testes em falta a 27/10). Revisão do Simão pendente |
| Sprint | Sprint 4 (29/10 a 05/11), por decisão do PO a 27/10 |
| Story points | 2 |
| Épico | E4 — Plano de candidatura |
| Prioridade | Should |
| Requisito de origem | RF45 (ver [01-requisitos-funcionais-e-nao-funcionais.md](../geral/01-requisitos-funcionais-e-nao-funcionais.md)) |
| Depende de | US04 (recolha da DGES), US05 (ficha) |

## A ideia em três pontos

1. **Na ficha do curso, a nota do último colocado da 1.ª fase de 2023, 2024 e 2025**, lida da tabela de estatísticas da DGES.
2. **Uma etiqueta resume a tendência:** «A subir», «A descer» ou «Estável», comparando o ano mais recente com o mais antigo, com 3 pontos de margem.
3. **A etiqueta aparece também em cada opção do plano** (US36), com os anos à vista ao passar o rato.

## Experimentar

```powershell
flask --app app run --debug
```

Abrir a ficha de um curso (não é preciso sessão) e ver a linha **«Último colocado (1.ª fase)»** com os três anos e a etiqueta. Com sessão, a mesma etiqueta aparece em cada opção do plano.

## Definition of Done da US41

A US41 só conta como «Feita» quando todas as caixas estiverem marcadas. As primeiras são os critérios de aceitação desta story (o «Confirmation» dos três C); as outras são o mínimo que a equipa exige a todas. Verificado a 31/10/2026, com 541 testes automáticos a passar.

**Critérios de aceitação desta story**

- [x] Notas da 1.ª fase de 2023, 2024 e 2025 (DGES) na ficha do curso (2 testes automáticos, todos a passar)
- [x] Etiqueta «A subir», «A descer» ou «Estável» (3 pontos de margem entre o primeiro e o último ano) (1 teste automático, a passar)
- [x] A etiqueta aparece também em cada opção do plano (1 teste automático, a passar)

**Mínimo da equipa**

- [x] Testes a passar: os desta story e os 541 do projeto
- [ ] Código revisto por outro elemento, com atenção a RNF06, RNF09, RNF10, RNF11: o código entrou na main pelo PR #45, juntado pelo Simão, mas a revisão dele está registada como pendente. **Falta a revisão do Simão**
- [x] Código gerado por IA assinalado no [registo de uso de IA](../geral/registo-de-uso-de-ia.md)
- [x] Documentação em `docs/US41/`: requisitos.md, use-case.md, bpmn.md, prompt.md
- [x] Sem dívida técnica por registar
- [ ] Funciona na demonstração: a mostrar na Sprint Review do Sprint 4 (05/11)
- [x] Aceite pelo Product Owner: aceite pelo PO a 27/10

## Documentos

| Documento | Conteúdo |
|---|---|
| [requisitos.md](requisitos.md) | Requisitos funcionais e critérios de aceitação, com os testes de cada um |
| [use-case.md](use-case.md) | Use case ([diagrama](diagramas/use-case.svg)) |
| [bpmn.md](bpmn.md) | Processo BPMN ([imagem](diagramas/bpmn.svg) · [ficheiro editável](diagramas/bpmn.bpmn)) |
| [prompt.md](prompt.md) | Pedido feito à IA para gerar o código |

Os diagramas são gerados por [`diagramas/gerar.py`](diagramas/gerar.py): mudar o desenho lá e correr `python docs/US41/diagramas/gerar.py docs/US41/diagramas`.

## Código e testes

| Onde | O quê |
|---|---|
| `dados/recolher_dges.py` | `estatisticas`, `_tendencia_e_procura`: leem a tabela de estatísticas de cada curso |
| `app/catalogo/repository.py` | `Curso.historico`, `Curso.tendencia` |
| `app/templates/macros/candidatura.html` | Macro `tendencia` (completa na ficha, compacta no plano) |
| `app/texts.py` | Textos `FICHA_HISTORICO`, `FICHA_TENDENCIA_*` |
| `tests/test_candidatura.py` | `TendenciaEProcuraTests.test_tendencia_compara_o_ano_mais_recente_com_o_mais_antigo`, `RecolhaDaTabelaTests`, `test_a_ficha_mostra_tendencia_procura_e_quanto_precisa`, `test_cada_opcao_do_plano_mostra_quanto_precisa_e_a_tendencia` |
