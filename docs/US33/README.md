# US33 — Condições de acesso na ficha do curso

> **Como** pessoa a escolher curso, **quero** ver na ficha de cada curso as provas de ingresso, a fórmula de cálculo, as classificações mínimas e os pré-requisitos, **para** saber o que é preciso para entrar.

| | |
|---|---|
| Estado | Feita: aceite pelo PO a 27/10, antes do início formal do Sprint 4 (código de 23/10, documentação e testes em falta a 27/10). Revisão no GitHub dispensada pelos PO a 31/10 |
| Sprint | Sprint 4 (29/10 a 05/11) |
| Story points | 3 |
| Épico | E4 — Plano de candidatura |
| Prioridade | Must |
| Requisito de origem | RF40 (ver [01-requisitos-funcionais-e-nao-funcionais.md](../geral/01-requisitos-funcionais-e-nao-funcionais.md)) |
| Depende de | US04 (as condições vêm da mesma recolha da DGES) e US05 (a ficha do curso) |
| Necessária para | US35 (nota de candidatura) e US36 (plano das 6 opções) |

## A ideia em três pontos

1. **A ficha de cada curso ganha a secção «Condições de acesso»:** as provas de ingresso, a fórmula da nota de candidatura (peso da média do secundário e das provas), as classificações mínimas e os pré-requisitos.
2. **Os conjuntos alternativos de provas aparecem pelo nome** («Basta um destes conjuntos: Português · História + Português»), em vez dos códigos da DGES.
3. **Funciona sem sessão.** Um curso de que a DGES não publica condições mostra isso e a ligação para a página da DGES.

## Experimentar

```powershell
flask --app app run --debug
```

Abrir http://127.0.0.1:5000/cursos/, entrar na ficha de um curso e procurar a secção **«Condições de acesso»**, por baixo dos dados do curso.

## Definition of Done da US33

A US33 só conta como «Feita» quando todas as caixas estiverem marcadas. As primeiras são os critérios de aceitação desta story (o «Confirmation» dos três C); as outras são o mínimo que a equipa exige a todas. Verificado a 31/10/2026, com 541 testes automáticos a passar.

**Critérios de aceitação desta story**

- [x] Dados lidos das páginas da DGES (a mesma recolha da US04) (2 testes automáticos, todos a passar)
- [x] Conjuntos alternativos de provas mostrados pelo nome («Basta um destes conjuntos») (2 testes automáticos, todos a passar)
- [x] Fórmula (peso da média e das provas) e mínimos em pontos (2 testes automáticos, todos a passar)
- [x] Um curso sem estes dados mostra a ligação à DGES (1 teste automático, a passar)
- [x] Funciona sem sessão iniciada (1 teste automático, a passar)

**Mínimo da equipa**

- [x] Testes a passar: os desta story e os 541 do projeto
- [x] Código revisto por outro elemento, com atenção a RNF06, RNF09, RNF10, RNF11: o código entrou na main pelo PR #45, juntado pelo Simão; revisão no GitHub dispensada por decisão dos Product Owners a 31/10 (o Simão acompanhou todo o trabalho)
- [x] Código gerado por IA assinalado no [registo de uso de IA](../geral/registo-de-uso-de-ia.md)
- [x] Documentação em `docs/US33/`: requisitos.md, use-case.md, bpmn.md, prompt.md
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

Os diagramas são gerados por [`diagramas/gerar.py`](diagramas/gerar.py): mudar o desenho lá e correr `python docs/US33/diagramas/gerar.py docs/US33/diagramas`.

## Código e testes

| Onde | O quê |
|---|---|
| `dados/recolher_dges.py` | `_provas_ingresso`, `nomes_das_provas`, `_pontos`, `_pre_requisitos`: leem as condições das páginas da DGES |
| `dados/provas-ingresso.csv` | Código e nome de cada prova de ingresso |
| `app/catalogo/repository.py` | `Curso.provas`, `peso_secundario`, `peso_provas`, `minimo_candidatura`, `minimo_provas`, `pre_requisitos`, `tem_condicoes_de_acesso`; `nomes_das_provas` |
| `app/templates/macros/candidatura.html` | Macros `condicoes` e `provas` |
| `app/templates/catalogo/ficha.html` | Secção «Condições de acesso» |
| `app/texts.py` | Textos `FICHA_ACESSO`, `FICHA_PROVAS*`, `FICHA_FORMULA*`, `FICHA_MINIMOS*`, `FICHA_PRE_REQUISITOS`, `FICHA_SEM_ACESSO` |
| `tests/test_us04_catalogo_completo.py` | `CondicoesDeAcessoTests` (2 testes, acrescentados a 27/10) |
| `tests/test_candidatura.py` | `test_a_ficha_mostra_as_condicoes_de_acesso_e_a_nota_do_aluno`, `test_sem_sessao_a_ficha_mostra_as_condicoes_e_pede_para_entrar` |
