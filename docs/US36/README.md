# US36 — Plano das 6 opções de candidatura

> **Como** candidato, **quero** montar e ordenar a minha lista de até 6 opções, com avisos, **para** submeter na DGES uma candidatura equilibrada.

| | |
|---|---|
| Estado | Feita: aceite pelo PO a 27/10, antes do início formal do Sprint 4 (código de 23/10, documentação e testes em falta a 27/10). Revisão do Simão pendente |
| Sprint | Sprint 4 (29/10 a 05/11) |
| Story points | 5 |
| Épico | E4 — Plano de candidatura |
| Prioridade | Should |
| Requisito de origem | RF43, RN11 (ver [01-requisitos-funcionais-e-nao-funcionais.md](../geral/01-requisitos-funcionais-e-nao-funcionais.md)) |
| Depende de | US35 (nota de candidatura), US34 (notas), US31 (curso escolhido) |
| Necessária para | US40 a US45 (Sprint 4), que acrescentam informação ao plano |

## A ideia em três pontos

1. **Até 6 opções, por ordem**, como na candidatura do concurso nacional. Juntam-se a partir da ficha do curso («Juntar ao plano») e ordenam-se no plano com «Subir», «Descer» e «Retirar». Tudo funciona sem JavaScript.
2. **Cada opção mostra a nota e a situação** (US35), e o plano avisa do que convém rever antes de submeter: opções que não contam, nenhuma opção segura, a mais fácil em 1.º lugar, menos de 6 opções e pré-requisitos.
3. **Sugere cursos da mesma área** da 1.ª opção onde a pessoa fica acima ou perto do último colocado. O OptaBem ajuda a preparar a candidatura; quem a submete é a pessoa, no site da DGES.

## Experimentar

```powershell
flask --app app run --debug
```

Iniciar sessão, indicar as notas (US34), abrir duas ou três fichas de cursos e carregar em **«Juntar ao plano»**. Abrir **«Candidatura»** no menu, mudar a ordem e ler os avisos de **«Antes de submeter»**.

## Definition of Done da US36

A US36 só conta como «Feita» quando todas as caixas estiverem marcadas. As primeiras são os critérios de aceitação desta story (o «Confirmation» dos três C); as outras são o mínimo que a equipa exige a todas. Verificado a 31/10/2026, com 541 testes automáticos a passar.

**Critérios de aceitação desta story**

- [x] Juntar cursos a partir da ficha; no máximo 6, sem repetidos (3 testes automáticos, todos a passar)
- [x] Subir, descer e retirar opções (funciona sem JavaScript) (2 testes automáticos, todos a passar)
- [x] Avisos: opções que não contam, nenhuma opção segura, a mais fácil em 1.º lugar, menos de 6 opções, pré-requisitos (3 testes automáticos, todos a passar)
- [x] Sugestões de cursos da mesma área onde a pessoa fica acima ou perto (1 teste automático, a passar)
- [x] Passo «Preparar a candidatura» no percurso do início (1 teste automático, a passar)
- [x] Aviso de estimativa (1 teste automático, a passar)
- [x] Curso escolhido como 1.ª opção (1 teste automático, a passar)
- [x] Cursos do ensino privado não entram (critério acrescentado a 27/10) (1 teste automático, a passar)

**Mínimo da equipa**

- [x] Testes a passar: os desta story e os 541 do projeto
- [ ] Código revisto por outro elemento, com atenção a RNF02, RNF06, RNF09, RNF10, RNF11: o código entrou na main pelo PR #45, juntado pelo Simão, mas a revisão dele está registada como pendente. **Falta a revisão do Simão**
- [x] Código gerado por IA assinalado no [registo de uso de IA](../geral/registo-de-uso-de-ia.md)
- [x] Documentação em `docs/US36/`: requisitos.md, use-case.md, bpmn.md, prompt.md
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

Os diagramas são gerados por [`diagramas/gerar.py`](diagramas/gerar.py): mudar o desenho lá e correr `python docs/US36/diagramas/gerar.py docs/US36/diagramas`.

## Código e testes

| Onde | O quê |
|---|---|
| `app/candidatura/routes.py` | `GET /candidatura/`; `POST /candidatura/juntar/<curso>`, `retirar`, `subir`, `descer`; `_voltar` (só caminhos do próprio site) |
| `app/candidatura/services.py` | `MAX_OPCOES = 6`, `juntar`, `retirar`, `mover`, `opcoes`, `avisos`, `sugestoes`, `PlanoCheio` |
| `app/candidatura/repository.py` | SQL da tabela `planos_candidatura` (coluna `opcoes`) |
| `app/percurso/__init__.py` | 4.º passo do percurso: «Preparar a candidatura» |
| `app/templates/candidatura/plano.html` | Página do plano |
| `app/templates/macros/candidatura.html` | Macro `botao` (formulário POST com CSRF) |
| `app/texts.py` | Textos `CANDIDATURA_*` (opções, avisos, sugestões) |
| `tests/test_candidatura.py` | `AvisosTests` (3), `test_percurso_completo_notas_juntar_ordenar_e_retirar`, `test_no_maximo_6_opcoes_e_sem_repetidos`, `test_curso_inexistente_da_404`, `test_o_curso_escolhido_pode_ser_a_1a_opcao`, `test_voltar_so_aceita_caminhos_do_proprio_site` |
| `tests/test_apresentacao.py` | `test_com_curso_o_proximo_passo_e_o_plano_de_candidatura` |
