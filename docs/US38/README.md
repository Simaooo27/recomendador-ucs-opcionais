# US38 — Datas do concurso no percurso

> **Como** candidato, **quero** ver as datas das fases do concurso nacional, **para** não falhar prazos.

| | |
|---|---|
| Estado | Feita: aceite pelo PO a 29/10 (código de 29/10, PR próprio). Revisão do Simão pendente |
| Sprint | Sprint 4 (29/10 a 05/11), por decisão do PO a 29/10 |
| Story points | 2 |
| Épico | E4 — Plano de candidatura |
| Prioridade | Could |
| Requisito de origem | RF50 (ver [01-requisitos-funcionais-e-nao-funcionais.md](../geral/01-requisitos-funcionais-e-nao-funcionais.md)) |
| Depende de | US31 (percurso), US36 (plano) |

## A ideia em três pontos

1. As datas das **3 fases do Concurso Nacional de Acesso** (candidatura, resultados, matrícula) estão em `dados/calendario-concurso.csv`, copiadas do despacho anual (o de 2026 é o Despacho n.º 6934/2026). A equipa junta as linhas de cada ano novo.
2. O **plano de candidatura** mostra as 3 fases, com a etapa a decorrer assinalada e a ligação para o calendário oficial da DGES.
3. O **passo atual do percurso**, no início, mostra o **próximo prazo** («Candidatura da 1.ª fase: até 06/08/2026»). Depois do concurso, diz que as datas do ano seguinte ainda não foram publicadas.

## Experimentar

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\ferramentas\arrancar.ps1
```

Iniciar sessão e ver o próximo prazo no início, por baixo do passo atual. Abrir o plano de candidatura e ir a **«Datas do concurso nacional»**. Hoje (depois de 02/10/2026) aparece que as datas de 2027 ainda não foram publicadas.

## Documentos

| Documento | Conteúdo |
|---|---|
| [requisitos.md](requisitos.md) | Requisitos funcionais e critérios de aceitação, com os testes de cada um |
| [use-case.md](use-case.md) | Use case ([diagrama](diagramas/use-case.svg)) |
| [bpmn.md](bpmn.md) | Processo BPMN ([imagem](diagramas/bpmn.svg) · [ficheiro editável](diagramas/bpmn.bpmn)) |
| [prompt.md](prompt.md) | Pedido feito à IA para gerar o código |

Os diagramas são gerados por [`diagramas/gerar.py`](diagramas/gerar.py): mudar o desenho lá e correr `python docs/US38/diagramas/gerar.py docs/US38/diagramas`.

## Código e testes

| Onde | O quê |
|---|---|
| `dados/calendario-concurso.csv` | As datas de 2026 (ano, fase, etapa, início, fim, nota) |
| `app/candidatura/calendario.py` | `ler` (ano mais recente), `proximo_prazo` (função pura), `frase_do_prazo` |
| `app/config.py` | `CALENDARIO_CSV` |
| `app/main.py`, `app/templates/home.html` | Próximo prazo no passo atual do percurso |
| `app/candidatura/routes.py`, `app/templates/candidatura/plano.html` | Secção «Datas do concurso nacional» |
| `app/texts.py` | Textos `CALENDARIO_*` e `HOME_PRAZO_*` |
| `tests/test_calendario.py` | 18 testes, com dias fixos (sem depender do relógio) |
