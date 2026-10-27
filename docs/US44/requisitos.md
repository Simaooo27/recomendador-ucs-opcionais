# US44 — Que exames me abrem mais portas?: requisitos funcionais

> **Como** candidato, **quero** saber que combinação de exames nacionais me deixa concorrer a mais cursos do meu plano, **para** decidir que exames fazer.

| | |
|---|---|
| Épico | E4 — Plano de candidatura |
| Prioridade | Should · 3 story points · Sprint 4 |
| Requisitos de origem | RF48 |
| Atores | Aluno com sessão iniciada |
| Depende de | US33 (provas de cada curso), US36 (plano) |
| Artefactos | [Use case](use-case.md) · [BPMN](bpmn.md) · [Prompt](prompt.md) |

## 1. Âmbito

**Dentro:** calcular as combinações de exames a partir das opções do plano e mostrá-las.

**Fora:** sugerir cursos fora do plano para uma combinação; datas dos exames.

## 2. Requisitos funcionais da US44

| ID | Requisito |
|---|---|
| **RF48.1** | Só aparece com 2 ou mais opções do plano que tenham condições de acesso. |
| **RF48.2** | Experimenta combinações de 1 a 3 exames, com os exames que aparecem nos conjuntos de provas das opções. Um curso fica aberto se um dos seus conjuntos está todo dentro da combinação. |
| **RF48.3** | Ficam só as combinações mínimas (sem exames a mais para os mesmos cursos), sem repetir combinações que abrem exatamente os mesmos cursos. |
| **RF48.4** | Mostra as 3 melhores: a que abre mais opções primeiro; depois a com menos exames; depois a com mais exames já feitos. |
| **RF48.5** | Para cada combinação, diz para quantas opções dá (ou «todas»), para quais não dá e que exames a pessoa já fez. |
| **RF48.6** | Matemática (16) e Matemática A (19) contam como o mesmo exame. |

## 3. Mensagens

Os textos estão em [`app/texts.py`](../../app/texts.py).

| Situação | Mensagem |
|---|---|
| Título | Que exames lhe abrem mais portas? |
| Introdução | Com estes exames nacionais, pode concorrer a mais opções do seu plano. Ajuda a decidir que exames fazer. |
| Quantas | Dá para {n} de {total} opções |
| Todas | Dá para todas as opções do plano. |
| Não dá | Não dá para: {cursos} |
| Já fez | Já fez: {provas} |

## 4. Dados

Sem dados novos: usa as provas de cada curso (US33) e os exames do aluno (US34).

## 5. Critérios de aceitação e testes

| Critério da story (backlog) | Requisitos | Testes automáticos |
|---|---|---|
| Combinações de até 3 exames, a partir dos conjuntos de provas das opções do plano (2 ou mais opções). | RF48.1, RF48.2 | `ExamesQueAbremPortasTests.test_precisa_de_pelo_menos_dois_cursos_com_regras`; `test_o_plano_mostra_exames_que_abrem_portas_e_plano_b` |
| Mostra as 3 melhores: a que serve para mais opções primeiro, depois a com menos exames. | RF48.3, RF48.4 | `ExamesQueAbremPortasTests.test_escolhe_a_combinacao_que_serve_para_mais_cursos` |
| Diz para que opções não dá e que exames da combinação a pessoa já fez. | RF48.5 | `ExamesQueAbremPortasTests.test_escolhe_a_combinacao_que_serve_para_mais_cursos` (`nao_abre`, `ja_feitas`) |
| Matemática e Matemática A contam como o mesmo exame. | RF48.6 | `ExamesQueAbremPortasTests.test_matematica_16_e_19_contam_como_a_mesma` |

## 6. Requisitos não funcionais aplicáveis

RNF03 (no máximo 3 exames por combinação, para a conta ser rápida), RNF06 (testes com resultado conhecido), RNF07 (conta em `calculos.py`), RNF09 (uso de IA documentado), RNF11 (português de Portugal).

## 7. Decisões e questões em aberto

| # | Questão | Estado |
|---|---|---|
| 1 | Matemática e Matemática A contam como o mesmo exame. | **Por confirmar** (ponto 16 dos requisitos) |
