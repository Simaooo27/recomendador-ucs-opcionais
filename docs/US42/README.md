# US42 — Procura do curso

> **Como** candidato, **quero** ver quantas pessoas concorreram a um curso e quantas o puseram em 1.ª opção, **para** perceber o risco da minha escolha.

| | |
|---|---|
| Estado | Feita: aceite pelo PO a 27/10, antes do início formal do Sprint 4 (código de 23/10, documentação e testes em falta a 27/10). Revisão do Simão pendente |
| Sprint | Sprint 4 (29/10 a 05/11), por decisão do PO a 27/10 |
| Story points | 2 |
| Épico | E4 — Plano de candidatura |
| Prioridade | Should |
| Requisito de origem | RF46 (ver [01-requisitos-funcionais-e-nao-funcionais.md](../geral/01-requisitos-funcionais-e-nao-funcionais.md)) |
| Depende de | US04 (recolha da DGES), US05 (ficha) |

## A ideia em três pontos

1. **Na ficha do curso, a procura na 1.ª fase de 2025:** candidatos, candidatos em 1.ª opção, vagas e colocados, da tabela de estatísticas da DGES.
2. **Uma etiqueta resume:** «Sobraram vagas na 1.ª fase», «Muito procurado» (1,5 ou mais candidatos em 1.ª opção por vaga), «Procurado» (0,75 a 1,5) ou «Pouco escolhido em 1.ª opção».
3. **Não é preciso sessão:** é informação pública sobre o curso.

## Experimentar

```powershell
.\ferramentas\arrancar.bat
```

Abrir a ficha de um curso e ver a linha **«Procura em 2025»** com a etiqueta e os números.

## Documentos

| Documento | Conteúdo |
|---|---|
| [requisitos.md](requisitos.md) | Requisitos funcionais e critérios de aceitação, com os testes de cada um |
| [use-case.md](use-case.md) | Use case ([diagrama](diagramas/use-case.svg)) |
| [bpmn.md](bpmn.md) | Processo BPMN ([imagem](diagramas/bpmn.svg) · [ficheiro editável](diagramas/bpmn.bpmn)) |
| [prompt.md](prompt.md) | Pedido feito à IA para gerar o código |

Os diagramas são gerados por [`diagramas/gerar.py`](diagramas/gerar.py): mudar o desenho lá e correr `python docs/US42/diagramas/gerar.py docs/US42/diagramas`.

## Código e testes

| Onde | O quê |
|---|---|
| `dados/recolher_dges.py` | `_tendencia_e_procura`: candidatos, 1.ª opção, vagas e colocados da 1.ª fase de 2025 |
| `app/catalogo/repository.py` | `Curso.procura` |
| `app/templates/macros/candidatura.html` | Macro `procura` |
| `app/texts.py` | Textos `FICHA_PROCURA*` |
| `tests/test_candidatura.py` | `TendenciaEProcuraTests.test_procura`, `RecolhaDaTabelaTests`, `test_a_ficha_mostra_tendencia_procura_e_quanto_precisa` |
