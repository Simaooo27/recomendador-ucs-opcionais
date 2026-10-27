# US41 — Tendência do último colocado

> **Como** candidato, **quero** ver como a nota do último colocado mudou de 2023 a 2025, **para** perceber se um curso está a ficar mais difícil de entrar.

| | |
|---|---|
| Estado | Protótipo (código feito antes do Sprint 4, no PR #44; por aceitar na Sprint Review) |
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
.\ferramentas\arrancar.bat
```

Abrir a ficha de um curso (não é preciso sessão) e ver a linha **«Último colocado (1.ª fase)»** com os três anos e a etiqueta. Com sessão, a mesma etiqueta aparece em cada opção do plano.

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
