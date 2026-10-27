# US40 — Quanto preciso no exame?: requisitos funcionais

> **Como** candidato, **quero** saber que nota preciso nos exames que ainda não fiz para chegar ao último colocado de um curso, **para** saber quanto tenho de estudar.

| | |
|---|---|
| Épico | E4 — Plano de candidatura |
| Prioridade | Should · 2 story points · Sprint 4 |
| Requisitos de origem | RF44 |
| Atores | Aluno com sessão iniciada |
| Depende de | US34 (notas), US35 (nota de candidatura) |
| Artefactos | [Use case](use-case.md) · [BPMN](bpmn.md) · [Prompt](prompt.md) |

## 1. Âmbito

**Dentro:** calcular e mostrar a nota necessária nas provas em falta, na ficha e em cada opção do plano.

**Fora:** dizer que exames fazer (US44); notas de exames de anos anteriores; melhorias de nota.

## 2. Requisitos funcionais da US40

| ID | Requisito |
|---|---|
| **RF44.1** | Com a média do secundário indicada, a ficha mostra a nota que o aluno precisa em cada prova em falta para chegar à nota do último colocado de 2025 (ou, sem essa referência, à nota mínima de candidatura do curso). |
| **RF44.2** | Conta com os exames já feitos do conjunto. Com mais de uma prova em falta, supõe a mesma nota em todas e di-lo. |
| **RF44.3** | Usa o conjunto de provas que pede a nota mais baixa; em caso de empate, o que tem menos provas por fazer. |
| **RF44.4** | A nota pedida nunca fica abaixo do mínimo de cada prova; é arredondada para cima, com uma casa decimal, em pontos e em valores. |
| **RF44.5** | Se nem 200 pontos chegam, a ficha diz qual é a nota de candidatura máxima possível com aquela média. |
| **RF44.6** | Sem média, a ficha pede-a; se o aluno já tem todas as provas de um conjunto, não há conta (a nota é a da US35). |
| **RF44.7** | No plano, cada opção a que falta uma prova mostra «Precisa de X em Y». |

## 3. Mensagens

Os textos estão em [`app/texts.py`](../../app/texts.py).

| Situação | Mensagem |
|---|---|
| Título | Quanto precisa no exame? |
| Possível | Para chegar a {alvo} ({referencia}), precisa de {pontos} pontos ({valores} valores) em {provas}. |
| Várias provas | Faltando mais de uma prova, a conta supõe a mesma nota em todas. |
| Impossível | Com a sua média, mesmo com 200 pontos nas provas a nota fica em {maximo}, abaixo de {alvo} ({referencia}). |
| Sem média | Indique a sua média do secundário para saber quanto precisa nos exames. |
| No plano | Precisa de {pontos} em {provas} |

## 4. Dados

Sem dados novos: usa as condições de acesso (US33) e as notas do aluno (US34).

## 5. Critérios de aceitação e testes

| Critério da story (backlog) | Requisitos | Testes automáticos |
|---|---|---|
| Na ficha do curso, com a média do secundário indicada. | RF44.1, RF44.6 | `test_a_ficha_mostra_tendencia_procura_e_quanto_precisa` (108,0 pontos); `QuantoPrecisaTests.test_sem_media_ou_com_tudo_feito_nao_ha_conta` |
| Usa os exames já feitos e escolhe o conjunto de provas em que é mais fácil lá chegar. | RF44.2, RF44.3 | `QuantoPrecisaTests.test_nota_necessaria_para_chegar_ao_ultimo_colocado`, `test_conta_com_a_prova_ja_feita_do_conjunto` |
| Respeita o mínimo de cada prova; sem último colocado, usa a nota mínima do curso. | RF44.4 | `QuantoPrecisaTests.test_conta_com_a_prova_ja_feita_do_conjunto` (mínimo de 95), `test_sem_referencia_usa_a_nota_minima` |
| Diz quando nem 200 pontos chegam. | RF44.5 | `QuantoPrecisaTests.test_avisa_quando_nem_200_chegam` |
| No plano, as opções a que falta uma prova mostram quanto precisa. | RF44.7 | `test_cada_opcao_do_plano_mostra_quanto_precisa_e_a_tendencia` (acrescentado a 27/10) |

## 6. Requisitos não funcionais aplicáveis

RNF06 (contas testadas com casos de resultado conhecido), RNF07 (contas em `calculos.py`), RNF09 (uso de IA documentado), RNF11 (português de Portugal).

## 7. Decisões e questões em aberto

| # | Questão | Estado |
|---|---|---|
| 1 | A conta é para chegar ao último colocado de 2025, que muda todos os anos (RN11). | Aceite: o texto diz qual é a referência |
| 2 | Com várias provas em falta, supõe a mesma nota em todas. | Aceite: a página di-lo |
