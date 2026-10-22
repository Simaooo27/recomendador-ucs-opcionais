# US05 — Consultar e comparar cursos: requisitos funcionais

> **Como** pessoa indecisa, **quero** consultar e comparar cursos de várias instituições, **para** perceber as diferenças antes de decidir.

| | |
|---|---|
| Épico | E2 — Catálogo |
| Prioridade | Must · 5 story points · Sprint 3 |
| Requisitos de origem | RF34 |
| Atores | Pessoa, com ou sem sessão iniciada |
| Depende de | Catálogo em `dados/catalogo-cursos-mvp.csv`, lido por `app/catalogo/repository.py` |
| Artefactos | [Use case](use-case.md) · [BPMN](bpmn.md) · [Prompt](prompt.md) |

## 1. Âmbito

**Dentro:** filtros por área, instituição e localidade na página `/cursos/`, juntamente com a pesquisa por texto que já existia; a ficha completa de cada curso; a comparação de 2 ou 3 cursos lado a lado; tudo sem sessão iniciada e sem JavaScript.

**Fora:** importar o catálogo para a base de dados (US04, no backlog); comparar opcionais ou unidades curriculares; guardar uma comparação; filtros por nota ou vagas (o catálogo tem 30 cursos e a lista mostra estes números em cada ficha).

## 2. Requisitos funcionais da US05

| ID | Requisito |
|---|---|
| **RF34.1** | A página `/cursos/` mostra o catálogo todo, ordenado por número de vagas, e um formulário com a pesquisa por texto e três listas: área, instituição e localidade. Cada lista tem «Todas» e os valores que existem no catálogo, por ordem alfabética (sem contar acentos). |
| **RF34.2** | Os filtros vão no endereço (`?q=…&area=…&instituicao=…&localidade=…`, pedido GET): a página funciona sem JavaScript e o endereço pode ser partilhado. Os filtros combinam-se (todos têm de ser respeitados). Um valor que não exista no catálogo é ignorado. |
| **RF34.3** | A página diz quantos cursos correspondem aos filtros («11 de 30 cursos»), mantém os valores escolhidos e mostra «Limpar filtros». Sem resultados, diz o que fazer («Experimente tirar um deles»). |
| **RF34.4** | Cada curso tem uma ficha em `/cursos/<curso>` com: área, nome, instituição, escola ou faculdade, localidade, vagas de 2026, nota do último colocado (1.ª fase de 2025), descrição, saídas profissionais (em lista), tipo de ensino, grau, duração, ECTS, área CNAEF e as fontes (página da DGES e página da instituição). Um dado em falta aparece como «Sem dados». Um curso que não existe dá «página não encontrada» (404). |
| **RF34.5** | O nome do curso, em todas as fichas resumidas (catálogo, página de apresentação, sugestões da conversa), é uma ligação para a ficha completa. |
| **RF34.6** | Cada ficha do catálogo tem a caixa «Comparar». O botão «Comparar os cursos marcados» leva a `/cursos/comparar?c=…&c=…`, sem JavaScript. |
| **RF34.7** | A comparação mostra 2 ou 3 cursos lado a lado, numa tabela com uma coluna por curso, pela ordem em que foram marcados. O cabeçalho de cada coluna tem o nome do curso e a instituição (há cursos com o mesmo nome em várias instituições); as linhas são: localidade, tipo de ensino, área, vagas, último colocado, duração, ECTS, descrição e saídas profissionais. |
| **RF34.8** | Com mais de 3 cursos, comparam-se os 3 primeiros e a página explica porquê. Com menos de 2, a página explica que é preciso escolher pelo menos 2 e não mostra a tabela. Cursos repetidos ou que não existem ficam de fora, com um aviso. |
| **RF34.9** | Tudo funciona sem sessão iniciada. Com sessão de aluno, a ficha e a comparação mostram também «Escolher este curso» (US31). |

## 3. Mensagens

Os textos estão em [`app/texts.py`](../../app/texts.py), secção do catálogo (`CATALOGO_*`, `FICHA_*`, `COMPARAR_*`).

| Situação | Mensagem |
|---|---|
| Introdução do catálogo | Filtre por área, instituição ou localidade, abra a ficha de cada curso e compare até 3 cursos lado a lado. |
| Contagem | Todos os 30 cursos do catálogo · 11 de 30 cursos |
| Sem resultados | Nenhum curso corresponde a estes filtros. Experimente tirar um deles. |
| Ajuda da comparação | Marque 2 ou 3 cursos e carregue em «Comparar os cursos marcados». |
| Menos de 2 cursos | Para comparar, escolha pelo menos 2 cursos do catálogo. |
| Mais de 3 cursos | Só se comparam 3 cursos de cada vez: ficaram os primeiros 3 que marcou. |
| Cursos que não existem | Alguns cursos não foram encontrados no catálogo e ficaram de fora. |
| Tabela no telemóvel | Deslize a tabela para o lado para ver todos os cursos. |

## 4. Dados

Sem tabelas novas. A ficha usa colunas do CSV que já existiam e não eram lidas: `grau`, `duracao_semestres`, `ects`, `area_cnaef` e `fonte_descricao`. As saídas profissionais vêm separadas por «;» na coluna `saidas_profissionais`.

## 5. Critérios de aceitação e testes

| Critério da story (backlog) | Requisitos | Testes automáticos (`tests/test_catalogo.py`) |
|---|---|---|
| Filtros por área, instituição e localidade. | RF34.1 a RF34.3 | `FiltrosTests` (9 testes: cada filtro, filtros combinados, valor selecionado, valor inválido ignorado, sem resultados, ordem das opções) |
| Ficha de cada curso com descrição, saídas profissionais, vagas, nota do último colocado e ligação à fonte. | RF34.4, RF34.5 | `FichaTests` (4 testes); `test_resposta_json_tem_os_campos_da_ficha` em `tests/test_apresentacao.py` (ligação na página de apresentação) |
| Comparação de até 3 cursos lado a lado. | RF34.6 a RF34.8 | `CompararTests` (6 testes: caixa em cada ficha, 3 e 2 cursos, mais de 3, menos de 2, repetidos e inexistentes); `CompararMelhoriasTests` (4 testes: instituição no cabeçalho, barra presa ao topo, contagem dos marcados, palavras sem cortes) |
| Funciona sem sessão iniciada. | RF34.9 | `SemSessaoTests.test_todas_as_paginas_abrem_sem_sessao`; `FichaTests.test_escolher_so_aparece_com_sessao` |

## 6. Requisitos não funcionais aplicáveis

RNF02 (sem formulários POST novos; todos os valores do endereço passam pelo escape do Jinja e os filtros só aceitam valores do catálogo), RNF06 (testes sem rede), RNF09 (uso de IA documentado), RNF10 (filtros com etiquetas, tabela com cabeçalhos de linha e de coluna, a caixa da tabela recebe o foco do teclado para deslizar), RNF11 (português de Portugal). Verificado no navegador a 1280 px e 390 px, em modo claro e escuro, sem deslocamento horizontal da página.

## 7. Decisões e questões em aberto

| # | Questão | Estado |
|---|---|---|
| 1 | A US05 dependia da US04 (catálogo na base de dados). Como o catálogo é lido do CSV desde 14/10, deixa de depender. | **Decidido** (Sprint Planning de 22/10) |
| 2 | Sem filtros, a página mostra o catálogo todo (30 cursos). Se o catálogo crescer muito, será preciso paginar. | Proposta do Claude, **a confirmar pelo PO** |
| 3 | A comparação aceita até 3 cursos (RF34). No telemóvel, a tabela desliza para o lado dentro da sua caixa, com o nome da linha sempre visível. | Proposta do Claude, **a confirmar pelo PO** |
| 4 | Os cursos sugeridos na conversa (US30) ainda não se comparam diretamente nem aparecem lado a lado: abre-se a ficha de cada um, ou marcam-se no catálogo. A revisão de 22/10 (PR #36) pediu-o para a US05, mas não faz parte dos critérios de aceitação. | Por decidir pelo PO (pode entrar como melhoria no Sprint 4) |
