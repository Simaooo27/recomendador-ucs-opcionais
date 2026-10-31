# US05 — Consultar e comparar cursos

> **Como** pessoa indecisa, **quero** consultar e comparar cursos de várias instituições, **para** perceber as diferenças antes de decidir.

| | |
|---|---|
| Estado | Feita (aceite na Sprint Review do Sprint 3, 23/10) |
| Sprint | Sprint 3 (22/10 a 29/10) |
| Story points | 5 |
| Épico | E2 — Catálogo |
| Prioridade | Must |
| Requisito de origem | RF34 (ver [01-requisitos-funcionais-e-nao-funcionais.md](../geral/01-requisitos-funcionais-e-nao-funcionais.md)) |
| Depende de | Catálogo lido do CSV (`app/catalogo/`, desde 14/10). Já não depende da US04 |
| Necessária para | Comparar os cursos sugeridos (US30) e escolher um deles ou outro (US31) |

## A ideia em três pontos

1. **Filtrar o catálogo** por área, instituição e localidade, além da pesquisa por texto. Os filtros vão no endereço (`/cursos/?area=Gestão&localidade=Porto`): funcionam sem JavaScript e podem ser partilhados.
2. **Ficha completa de cada curso** (`/cursos/<curso>`): descrição, saídas profissionais, vagas, nota do último colocado, dados do curso e as fontes. O nome do curso em qualquer ficha leva lá.
3. **Comparar 2 ou 3 cursos lado a lado** (`/cursos/comparar`): marca-se a caixa «Comparar» nas fichas e carrega-se no botão. Tudo funciona sem sessão iniciada; com sessão aparece também «Escolher este curso» (US31).

## Experimentar

```powershell
flask --app app run --debug
```

Abrir http://127.0.0.1:5000/cursos/ (não é preciso iniciar sessão), escolher uma área e uma localidade e carregar em **«Aplicar filtros»**. Abrir uma ficha pelo nome do curso. Voltar, marcar **«Comparar»** em 2 ou 3 fichas e carregar em **«Comparar os cursos marcados»**.

## Definition of Done da US05

A US05 só conta como «Feita» quando todas as caixas estiverem marcadas. As primeiras são os critérios de aceitação desta story (o «Confirmation» dos três C); as outras são o mínimo que a equipa exige a todas. Verificado a 31/10/2026, com 541 testes automáticos a passar.

**Critérios de aceitação desta story**

- [x] Filtros por área, instituição e localidade (9 testes automáticos, todos a passar)
- [x] Ficha de cada curso com descrição, saídas profissionais, vagas, nota do último colocado e ligação à fonte (5 testes automáticos, todos a passar)
- [x] Comparação de até 3 cursos lado a lado (10 testes automáticos, todos a passar)
- [x] Funciona sem sessão iniciada (2 testes automáticos, todos a passar)

**Mínimo da equipa**

- [x] Testes a passar: os desta story e os 541 do projeto
- [x] Código revisto por outro elemento, com atenção a RNF02, RNF06, RNF09, RNF10, RNF11: PR #37 juntado pelo Simão, que escreveu as correções da revisão (PR #38)
- [x] Código gerado por IA assinalado no [registo de uso de IA](../geral/registo-de-uso-de-ia.md)
- [x] Documentação em `docs/US05/`: requisitos.md, use-case.md, bpmn.md, prompt.md
- [x] Sem dívida técnica por registar
- [x] Funciona na demonstração: Sprint Review do Sprint 3 (23/10), testada pelos dois Product Owners
- [x] Aceite pelo Product Owner: Sprint Review do Sprint 3 (23/10)

## Documentos

| Documento | Conteúdo |
|---|---|
| [requisitos.md](requisitos.md) | Requisitos funcionais e critérios de aceitação, com os testes de cada um |
| [use-case.md](use-case.md) | Use case ([diagrama](diagramas/use-case.svg)) |
| [bpmn.md](bpmn.md) | Processo BPMN ([imagem](diagramas/bpmn.svg) · [ficheiro editável](diagramas/bpmn.bpmn)) |
| [prompt.md](prompt.md) | Pedido feito à IA para gerar o código |

Os diagramas são gerados por [`diagramas/gerar.py`](diagramas/gerar.py): mudar o desenho lá e correr `python docs/US05/diagramas/gerar.py docs/US05/diagramas`.

## Código e testes

| Onde | O quê |
|---|---|
| `app/catalogo/repository.py` | `Curso` passa a ter os campos da ficha (grau, duração, ECTS, área CNAEF, fonte da descrição) e `lista_saidas` |
| `app/catalogo/services.py` | `opcoes`, `ler_filtros`, `filtrar`, `por_chave`, `comparar` (máximo de 3, `MAX_COMPARAR`) |
| `app/catalogo/routes.py` | `GET /cursos/` (filtros), `GET /cursos/<chave>` (ficha), `GET /cursos/comparar` (comparação) |
| `app/templates/catalogo/` | `lista.html`, `ficha.html`, `comparar.html` |
| `app/templates/macros/marca.html` | `cartao_curso`: nome do curso com ligação à ficha; caixa «Comparar» (`comparar=true`) |
| `app/static/style.css` | Secção 7 (caixa de pesquisa e listas de escolha) e secção 12 (filtros, ficha, comparação) |
| `app/static/app.js` | A pesquisa da página de apresentação preenche também a ligação para a ficha |
| `app/texts.py` | Textos `CATALOGO_*`, `FICHA_*` e `COMPARAR_*` |
| `tests/test_catalogo.py` | 24 testes (filtros, ficha, comparação e melhorias da revisão do #37, sem sessão) |
