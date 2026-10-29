# US45 — Plano B: 2.ª fase

> **Como** candidato, **quero** ver cursos das áreas do meu plano que tiveram vagas na 2.ª fase e a que a minha nota chegava, **para** ter uma alternativa se não entrar na 1.ª fase.

| | |
|---|---|
| Estado | Feita: aceite pelo PO a 27/10, antes do início formal do Sprint 4 (código de 23/10, documentação e testes em falta a 27/10). Revisão do Simão pendente |
| Sprint | Sprint 4 (29/10 a 05/11), por decisão do PO a 27/10 |
| Story points | 2 |
| Épico | E4 — Plano de candidatura |
| Prioridade | Could |
| Requisito de origem | RF49 (ver [01-requisitos-funcionais-e-nao-funcionais.md](../geral/01-requisitos-funcionais-e-nao-funcionais.md)) |
| Depende de | US04 (recolha da DGES), US35 (nota), US36 (plano) |

## A ideia em três pontos

1. **No plano, a secção «Plano B: 2.ª fase»** mostra até 3 cursos das mesmas áreas das opções, fora do plano, que tiveram vagas na 2.ª fase de 2025 e a que a nota da pessoa chegava.
2. **Primeiro os mais disputados** (último colocado da 2.ª fase mais alto). Sem nota do último colocado dessa fase, só conta se sobraram vagas.
3. **Com um aviso:** as vagas da 2.ª fase são as que sobram da 1.ª e mudam todos os anos. Sem resultados, a página explica porquê.

## Experimentar

```powershell
.\ferramentas\arrancar.bat
```

Com sessão, indicar as notas, juntar cursos ao plano e ver a secção **«Plano B: 2.ª fase»** no fim do plano.

## Documentos

| Documento | Conteúdo |
|---|---|
| [requisitos.md](requisitos.md) | Requisitos funcionais e critérios de aceitação, com os testes de cada um |
| [use-case.md](use-case.md) | Use case ([diagrama](diagramas/use-case.svg)) |
| [bpmn.md](bpmn.md) | Processo BPMN ([imagem](diagramas/bpmn.svg) · [ficheiro editável](diagramas/bpmn.bpmn)) |
| [prompt.md](prompt.md) | Pedido feito à IA para gerar o código |

Os diagramas são gerados por [`diagramas/gerar.py`](diagramas/gerar.py): mudar o desenho lá e correr `python docs/US45/diagramas/gerar.py docs/US45/diagramas`.

## Código e testes

| Onde | O quê |
|---|---|
| `dados/recolher_dges.py` | `_tendencia_e_procura`: vagas, colocados e último colocado da 2.ª fase de 2025 |
| `app/candidatura/calculos.py` | `chega_na_2a_fase` |
| `app/candidatura/services.py` | `plano_b` |
| `app/templates/candidatura/plano.html` | Secção do plano B |
| `app/texts.py` | Textos `PLANO_B_*` |
| `tests/test_candidatura.py` | `PlanoBTests` (2), `RecolhaDaTabelaTests`, `test_o_plano_mostra_exames_que_abrem_portas_e_plano_b`, `test_plano_b_vazio_explica_porque` |
