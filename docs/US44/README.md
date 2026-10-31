# US44 — Que exames me abrem mais portas?

> **Como** candidato, **quero** saber que combinação de exames nacionais me deixa concorrer a mais cursos do meu plano, **para** decidir que exames fazer.

| | |
|---|---|
| Estado | Feita: aceite pelo PO a 27/10, antes do início formal do Sprint 4 (código de 23/10, documentação e testes em falta a 27/10). Revisão do Simão pendente |
| Sprint | Sprint 4 (29/10 a 05/11), por decisão do PO a 27/10 |
| Story points | 3 |
| Épico | E4 — Plano de candidatura |
| Prioridade | Should |
| Requisito de origem | RF48 (ver [01-requisitos-funcionais-e-nao-funcionais.md](../geral/01-requisitos-funcionais-e-nao-funcionais.md)) |
| Depende de | US33 (provas de cada curso), US36 (plano) |

## A ideia em três pontos

1. **No plano, com 2 ou mais opções, a secção «Que exames lhe abrem mais portas?»** mostra as combinações de até 3 exames nacionais que servem para mais opções.
2. **As 3 melhores, por ordem:** primeiro a que serve para mais opções, depois a que tem menos exames, depois a que tem mais exames já feitos.
3. **Para cada combinação**, diz para que opções não dá e que exames a pessoa já fez. Nas Matemáticas, as combinações são de exames (Matemática A, B ou MACS), cada um a contar para as provas que a DGES aceita.

## Experimentar

```powershell
flask --app app run --debug
```

Com sessão, juntar ao plano 2 ou 3 cursos com provas diferentes e ver a secção **«Que exames lhe abrem mais portas?»**.

## Definition of Done da US44

A US44 só conta como «Feita» quando todas as caixas estiverem marcadas. As primeiras são os critérios de aceitação desta story (o «Confirmation» dos três C); as outras são o mínimo que a equipa exige a todas. Verificado a 31/10/2026, com 541 testes automáticos a passar.

**Critérios de aceitação desta story**

- [x] Combinações de até 3 exames, a partir dos conjuntos de provas das opções do plano (2 ou mais opções) (2 testes automáticos, todos a passar)
- [x] Mostra as 3 melhores: a que serve para mais opções primeiro, depois a com menos exames (1 teste automático, a passar)
- [x] Diz para que opções não dá e que exames da combinação a pessoa já fez (1 teste automático, a passar)
- [x] Os exames de Matemática contam para as provas que a DGES aceita (critério reescrito a 27/10) (2 testes automáticos, todos a passar)

**Mínimo da equipa**

- [x] Testes a passar: os desta story e os 541 do projeto
- [ ] Código revisto por outro elemento, com atenção a RNF03, RNF06, RNF07, RNF09, RNF11: o código entrou na main pelo PR #45, juntado pelo Simão, mas a revisão dele está registada como pendente. **Falta a revisão do Simão**
- [x] Código gerado por IA assinalado no [registo de uso de IA](../geral/registo-de-uso-de-ia.md)
- [x] Documentação em `docs/US44/`: requisitos.md, use-case.md, bpmn.md, prompt.md
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

Os diagramas são gerados por [`diagramas/gerar.py`](diagramas/gerar.py): mudar o desenho lá e correr `python docs/US44/diagramas/gerar.py docs/US44/diagramas`.

## Código e testes

| Onde | O quê |
|---|---|
| `app/candidatura/calculos.py` | `exames_que_abrem_portas`, `Combinacao`, `MAX_EXAMES = 3` |
| `app/candidatura/services.py` | `exames_do_plano` |
| `app/templates/candidatura/plano.html` | Secção das combinações |
| `app/texts.py` | Textos `EXAMES_*` |
| `tests/test_candidatura.py` | `ExamesQueAbremPortasTests` (3), `test_o_plano_mostra_exames_que_abrem_portas_e_plano_b` |
