# US44 — Que exames me abrem mais portas?

> **Como** candidato, **quero** saber que combinação de exames nacionais me deixa concorrer a mais cursos do meu plano, **para** decidir que exames fazer.

| | |
|---|---|
| Estado | Protótipo (código feito antes do Sprint 4, no PR #44; por aceitar na Sprint Review) |
| Sprint | Sprint 4 (29/10 a 05/11), por decisão do PO a 27/10 |
| Story points | 3 |
| Épico | E4 — Plano de candidatura |
| Prioridade | Should |
| Requisito de origem | RF48 (ver [01-requisitos-funcionais-e-nao-funcionais.md](../geral/01-requisitos-funcionais-e-nao-funcionais.md)) |
| Depende de | US33 (provas de cada curso), US36 (plano) |

## A ideia em três pontos

1. **No plano, com 2 ou mais opções, a secção «Que exames lhe abrem mais portas?»** mostra as combinações de até 3 exames nacionais que servem para mais opções.
2. **As 3 melhores, por ordem:** primeiro a que serve para mais opções, depois a que tem menos exames, depois a que tem mais exames já feitos.
3. **Para cada combinação**, diz para que opções não dá e que exames a pessoa já fez. Matemática e Matemática A contam como o mesmo exame.

## Experimentar

```powershell
.\ferramentas\arrancar.bat
```

Com sessão, juntar ao plano 2 ou 3 cursos com provas diferentes e ver a secção **«Que exames lhe abrem mais portas?»**.

## Documentos

| Documento | Conteúdo |
|---|---|
| [requisitos.md](requisitos.md) | Requisitos funcionais e critérios de aceitação, com os testes de cada um |
| [use-case.md](use-case.md) | Use case ([diagrama](diagramas/use-case.svg)) |
| [bpmn.md](bpmn.md) | Processo BPMN ([imagem](diagramas/bpmn.svg) · [ficheiro editável](diagramas/bpmn.bpmn)) |
| [prompt.md](prompt.md) | Pedido feito à IA para gerar o código |

Os diagramas são gerados por [`diagramas/gerar.py`](diagramas/gerar.py): mudar o desenho lá e correr `python docs/US44/diagramas/gerar.py docs/US44/diagramas`.

## Código e testes

| Onde | O quê |
|---|---|
| `app/candidatura/calculos.py` | `exames_que_abrem_portas`, `Combinacao`, `MAX_EXAMES = 3` |
| `app/candidatura/services.py` | `exames_do_plano` |
| `app/templates/candidatura/plano.html` | Secção das combinações |
| `app/texts.py` | Textos `EXAMES_*` |
| `tests/test_candidatura.py` | `ExamesQueAbremPortasTests` (3), `test_o_plano_mostra_exames_que_abrem_portas_e_plano_b` |
