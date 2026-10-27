# US33 — Condições de acesso na ficha do curso: requisitos funcionais

> **Como** pessoa a escolher curso, **quero** ver na ficha de cada curso as provas de ingresso, a fórmula de cálculo, as classificações mínimas e os pré-requisitos, **para** saber o que é preciso para entrar.

| | |
|---|---|
| Épico | E4 — Plano de candidatura |
| Prioridade | Must · 3 story points · Sprint 4 |
| Requisitos de origem | RF40 |
| Atores | Pessoa, com ou sem sessão iniciada |
| Depende de | US04 (recolha da DGES), US05 (ficha do curso) |
| Artefactos | [Use case](use-case.md) · [BPMN](bpmn.md) · [Prompt](prompt.md) |

## 1. Âmbito

**Dentro:** ler as condições de acesso das páginas da DGES e mostrá-las na ficha de cada curso.

**Fora:** a nota de candidatura do aluno (US35); contingentes especiais e preferência regional; confirmar se um pré-requisito está cumprido.

## 2. Requisitos funcionais da US33

| ID | Requisito |
|---|---|
| **RF40.1** | A recolha (US04) lê de cada página da DGES os conjuntos de provas de ingresso, a fórmula (peso da média do secundário e das provas), as classificações mínimas (nota de candidatura e cada prova) e os pré-requisitos, e escreve-os no catálogo. |
| **RF40.2** | A ficha do curso tem a secção «Condições de acesso». As provas aparecem pelo nome. Com mais de um conjunto, a ficha diz «Basta um destes conjuntos:» e lista cada conjunto («História + Português»). |
| **RF40.3** | A fórmula aparece como «50% média do secundário + 50% provas de ingresso»; os mínimos como «95 pontos na nota de candidatura e 95 em cada prova». Os pré-requisitos só aparecem quando existem. |
| **RF40.4** | Um curso sem condições de acesso no catálogo mostra uma frase a dizê-lo e a ligação para a página da DGES (na secção «Fontes»). |
| **RF40.5** | Tudo funciona sem sessão iniciada. Sem sessão, a ficha convida a iniciar sessão para calcular a nota (US35). |

## 3. Mensagens

| Situação | Mensagem |
|---|---|
| Título da secção | Condições de acesso |
| Vários conjuntos | Basta um destes conjuntos: |
| Fórmula | {secundario}% média do secundário + {provas}% provas de ingresso |
| Mínimos | {candidatura} pontos na nota de candidatura e {provas} em cada prova |
| Sem condições | A DGES ainda não tem as condições de acesso deste curso no OptaBem. Consulte a página da DGES. |
| Sem sessão | Inicie sessão para calcular a sua nota de candidatura a este curso. |

## 4. Dados

Colunas do catálogo (ver [`dados/README.md`](../../dados/README.md)): `provas_ingresso` (conjuntos separados por «|», provas de um conjunto por «+», por exemplo `18|11+18`), `peso_secundario`, `peso_provas`, `minimo_candidatura`, `minimo_provas`, `pre_requisitos`. Os nomes das provas estão em `dados/provas-ingresso.csv`. No catálogo recolhido, 4 de 174 cursos não têm provas.

## 5. Critérios de aceitação e testes

| Critério da story (backlog) | Requisitos | Testes automáticos |
|---|---|---|
| Dados lidos das páginas da DGES (a mesma recolha da US04). | RF40.1 | `CondicoesDeAcessoTests` em `tests/test_us04_catalogo_completo.py`: uma página com conjuntos alternativos, fórmula e mínimos; e todas as páginas guardadas dão as condições que estão no CSV |
| Conjuntos alternativos de provas mostrados pelo nome («Basta um destes conjuntos»). | RF40.2 | `test_sem_sessao_a_ficha_mostra_as_condicoes_e_pede_para_entrar`, `test_a_ficha_mostra_as_condicoes_de_acesso_e_a_nota_do_aluno` |
| Fórmula (peso da média e das provas) e mínimos em pontos. | RF40.3 | Sem teste próprio na página: os valores são lidos em `CondicoesDeAcessoTests` e o texto vem de `texts.py` |
| Um curso sem estes dados mostra a ligação à DGES. | RF40.4 | `test_a_ficha_mostra_as_condicoes_de_acesso_e_a_nota_do_aluno` (curso «Sem Regras») |
| Funciona sem sessão iniciada. | RF40.5 | `test_sem_sessao_a_ficha_mostra_as_condicoes_e_pede_para_entrar` |

## 6. Requisitos não funcionais aplicáveis

RNF06 (os testes usam páginas guardadas e um CSV de teste, sem rede), RNF09 (uso de IA documentado), RNF10 (as condições são uma lista de definições, `dl`, com título e valor), RNF11 (português de Portugal).

## 7. Decisões e questões em aberto

| # | Questão | Estado |
|---|---|---|
| 1 | «Matemática» (16) e «Matemática A» (19) aparecem como provas diferentes na DGES; o OptaBem conta-as como o mesmo exame. | **Por confirmar** pela equipa na DGES (ponto 16 dos requisitos) |
| 2 | Pré-requisitos (atestados, provas físicas) aparecem como texto, tal como a DGES os publica; o OptaBem não os verifica. | Aceite (aviso no plano, US36) |
