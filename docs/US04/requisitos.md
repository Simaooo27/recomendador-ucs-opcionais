# US04 — Catálogo de licenciaturas recolhido da DGES: requisitos funcionais

> **Como** pessoa indecisa, **quero** procurar num catálogo de licenciaturas recolhido da DGES, e não só numa amostra escrita à mão, **para** ver cursos de muitas instituições com dados oficiais.

| | |
|---|---|
| Épico | E2 — Catálogo de cursos |
| Prioridade | Must · 5 story points · Sprint 4 |
| Requisitos de origem | RF05, RNF03 |
| Atores | Equipa (corre a recolha); pessoa, com ou sem sessão (usa o catálogo) |
| Depende de | `dados/catalogo-cursos-mvp.csv` (descrições da equipa) |
| Artefactos | [Use case](use-case.md) · [BPMN](bpmn.md) · [Prompt](prompt.md) |

## 1. Âmbito

**Dentro:** o script de recolha (`dados/recolher_dges.py`), o CSV com os cursos já recolhidos (174), as colunas das condições de acesso, a lista de cursos com páginas e o filtro por área no assistente quando o catálogo passa de 150 cursos.

**Fora:** correr a recolha de todas as licenciaturas do concurso nacional (US48, Backlog); guardar o catálogo na base de dados (só é preciso para a US39); a área de gestão importar o CSV (era a versão da US04 até 23/10).

## 2. Requisitos funcionais da US04

| ID | Requisito |
|---|---|
| **RF05.1** | Os cursos vêm das páginas públicas da DGES. O script pede no máximo uma página a cada 2 segundos, identifica-se como projeto académico e guarda cada página tal como veio em `dados/dges_html/`. |
| **RF05.2** | A recolha é retomável: uma página já guardada não volta a ser pedida, e um erro de rede tenta de novo com pausas crescentes. |
| **RF05.3** | `processar` lê só as páginas guardadas (sem rede) e escreve `dados/catalogo-cursos.csv` com as colunas do catálogo do MVP e as condições de acesso (provas, fórmula, mínimos, pré-requisitos), a tendência e a procura. |
| **RF05.4** | Os cursos que estão no catálogo do MVP mantêm a instituição, a área, a descrição e as saídas profissionais escritas pela equipa. Os outros ficam com os dados da DGES e sem descrição. |
| **RF05.5** | A aplicação usa o catálogo recolhido quando existe e, se não existir, o do MVP. Nunca acede à internet para mostrar cursos. |
| **RF05.6** | A lista `/cursos/` mostra 24 cursos por página, com «página X de Y» e ligações para a anterior e a seguinte que mantêm os filtros. Um número de página inválido mostra a primeira ou a última. |
| **RF05.7** | Com mais de 150 cursos, o assistente faz a sugestão em dois passos: primeiro pede as áreas que combinam com a pessoa e depois recebe só os cursos dessas áreas (no máximo 80). Cursos de outras áreas devolvidos pelo LLM são descartados (RN09). |

## 3. Dados

`dados/catalogo-cursos.csv`: as colunas estão descritas em [`dados/README.md`](../../dados/README.md). Nenhuma tabela nova na base de dados.

## 4. Critérios de aceitação e testes

| Critério da story (backlog) | Requisitos | Testes automáticos |
|---|---|---|
| Os cursos vêm das páginas públicas da DGES, por um script que corre no computador da equipa, devagar e retomável. | RF05.1 a RF05.3 | `LeituraDaPaginaTests` (6 testes: campos da ficha, nota da 1.ª fase do ano mais recente, ensino privado sem nota, áreas, instituições, localidades) em `tests/test_us04_catalogo_completo.py`. O descarregamento em si não tem teste automático (precisa de rede). |
| O catálogo tem os cursos já recolhidos (174), com vagas, nota do último colocado e condições de acesso. | RF05.3, RF05.5 | `CondicoesDeAcessoTests` (US33) compara cada página guardada com o CSV |
| As descrições escritas pela equipa mantêm-se. | RF05.4 | Sem teste automático: verificado a 27/10 no CSV (os 30 cursos do MVP estão no catálogo recolhido com a descrição da equipa; um deles já não tinha descrição no MVP) |
| Lista de cursos com paginação (24 por página). | RF05.6 | `PaginacaoTests` (4 testes) em `tests/test_catalogo.py` |
| Acima de 150 cursos, o assistente recebe só os cursos das áreas escolhidas. | RF05.7 | `FiltroPorAreaTests` (9 testes) em `tests/test_us04_catalogo_completo.py` |

## 5. Requisitos não funcionais aplicáveis

RNF03 (a lista pagina para continuar rápida com o catálogo completo), RNF05 (o script só usa a biblioteca padrão), RNF06 (os testes leem texto fixo, sem rede), RNF09 (uso de IA documentado), RNF12 (o filtro por área envia ao LLM menos dados, nunca dados da conta).

## 6. Decisões e questões em aberto

| # | Questão | Estado |
|---|---|---|
| 1 | O catálogo vem da DGES por recolha, em vez de o administrador importar um CSV (sugestão de um colega). | **Decidido** (PO, 23/10) |
| 2 | A recolha de todas as licenciaturas exige o computador ligado uma noite inteira; passa para a US48. | **Decidido** (PO, 27/10) |
| 3 | A pasta `dados/dges_html/` está no `.gitignore`, mas 165 ficheiros dessa pasta foram para o repositório no PR #44. Ou se tiram do Git (o CSV chega para a aplicação), ou se tira a linha do `.gitignore` e se assume que ficam como fonte dos testes da US33. | Por decidir pela equipa |
| 4 | Os cursos fora do MVP não têm descrição: as sugestões do assistente para esses cursos baseiam-se só no nome e na área. | Aceite para esta release (ponto 12 dos requisitos) |
