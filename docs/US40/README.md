# US40 — Quanto preciso no exame?

> **Como** candidato, **quero** saber que nota preciso nos exames que ainda não fiz para chegar ao último colocado de um curso, **para** saber quanto tenho de estudar.

| | |
|---|---|
| Estado | Feita: aceite pelo PO a 27/10, antes do início formal do Sprint 4 (código de 23/10, documentação e testes em falta a 27/10). Revisão do Simão pendente |
| Sprint | Sprint 4 (29/10 a 05/11), por decisão do PO a 27/10 |
| Story points | 2 |
| Épico | E4 — Plano de candidatura |
| Prioridade | Should |
| Requisito de origem | RF44 (ver [01-requisitos-funcionais-e-nao-funcionais.md](../geral/01-requisitos-funcionais-e-nao-funcionais.md)) |
| Depende de | US34 (notas), US35 (nota de candidatura) |

## A ideia em três pontos

1. **Na ficha do curso, «Quanto precisa no exame?»:** com a média do secundário e os exames já feitos, a nota que precisa nas provas que faltam para chegar ao último colocado de 2025.
2. **Escolhe o caminho mais fácil:** de todos os conjuntos de provas do curso, usa aquele em que precisa de menos; respeita o mínimo de cada prova e, sem último colocado, usa a nota mínima do curso.
3. **Diz quando não dá:** se nem 200 pontos chegam, diz qual é a nota máxima possível. No plano (US36), cada opção a que falta uma prova mostra «Precisa de X em Y».

## Experimentar

```powershell
.\ferramentas\arrancar.bat
```

Iniciar sessão, indicar só a média do secundário (US34) e abrir a ficha de um curso: a secção **«Quanto precisa no exame?»** aparece por baixo da nota.

## Documentos

| Documento | Conteúdo |
|---|---|
| [requisitos.md](requisitos.md) | Requisitos funcionais e critérios de aceitação, com os testes de cada um |
| [use-case.md](use-case.md) | Use case ([diagrama](diagramas/use-case.svg)) |
| [bpmn.md](bpmn.md) | Processo BPMN ([imagem](diagramas/bpmn.svg) · [ficheiro editável](diagramas/bpmn.bpmn)) |
| [prompt.md](prompt.md) | Pedido feito à IA para gerar o código |

Os diagramas são gerados por [`diagramas/gerar.py`](diagramas/gerar.py): mudar o desenho lá e correr `python docs/US40/diagramas/gerar.py docs/US40/diagramas`.

## Código e testes

| Onde | O quê |
|---|---|
| `app/candidatura/calculos.py` | `nota_necessaria`, `Necessidade` (funções puras) |
| `app/candidatura/services.py` | `opcoes` junta a necessidade a cada opção do plano |
| `app/catalogo/routes.py` | A ficha calcula a necessidade com sessão |
| `app/templates/macros/candidatura.html` | Macro `necessidade` |
| `app/texts.py` | Textos `FICHA_PRECISA*` e `CANDIDATURA_PRECISA` |
| `tests/test_candidatura.py` | `QuantoPrecisaTests` (5), `test_a_ficha_mostra_tendencia_procura_e_quanto_precisa`, `test_cada_opcao_do_plano_mostra_quanto_precisa_e_a_tendencia` |
