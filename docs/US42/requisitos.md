# US42 — Procura do curso: requisitos funcionais

> **Como** candidato, **quero** ver quantas pessoas concorreram a um curso e quantas o puseram em 1.ª opção, **para** perceber o risco da minha escolha.

| | |
|---|---|
| Épico | E4 — Plano de candidatura |
| Prioridade | Should · 2 story points · Sprint 4 |
| Requisitos de origem | RF46 |
| Atores | Pessoa, com ou sem sessão iniciada |
| Depende de | US04 (recolha da DGES), US05 (ficha) |
| Artefactos | [Use case](use-case.md) · [BPMN](bpmn.md) · [Prompt](prompt.md) |

## 1. Âmbito

**Dentro:** ler a procura da 1.ª fase de 2025 e mostrá-la na ficha com uma etiqueta.

**Fora:** procura de anos anteriores; procura nas outras fases.

## 2. Requisitos funcionais da US42

| ID | Requisito |
|---|---|
| **RF46.1** | A recolha (US04) lê da tabela da DGES, na 1.ª fase de 2025: vagas, candidatos, candidatos em 1.ª opção e colocados. |
| **RF46.2** | Se ficaram vagas por preencher (colocados < vagas), a etiqueta é «Sobraram vagas na 1.ª fase». |
| **RF46.3** | Caso contrário, conta os candidatos em 1.ª opção por vaga: 1,5 ou mais é «Muito procurado», de 0,75 a 1,5 é «Procurado», abaixo é «Pouco escolhido em 1.ª opção». |
| **RF46.4** | A ficha mostra a etiqueta e a frase com os números. Sem dados, não mostra nada. |

## 3. Mensagens

Os textos estão em [`app/texts.py`](../../app/texts.py).

| Situação | Mensagem |
|---|---|
| Título | Procura em 2025 |
| Sobraram | Sobraram vagas na 1.ª fase |
| Muita | Muito procurado |
| Média | Procurado |
| Pouca | Pouco escolhido em 1.ª opção |
| Números | {candidatos} candidatos para {vagas} vagas; {primeira} puseram-no em 1.ª opção e ficaram {colocados} colocados. |

## 4. Dados

Colunas `vagas_1fase_2025`, `candidatos_1fase_2025`, `candidatos_1opcao_1fase_2025` e `colocados_1fase_2025` do catálogo.

## 5. Critérios de aceitação e testes

| Critério da story (backlog) | Requisitos | Testes automáticos |
|---|---|---|
| Candidatos, candidatos em 1.ª opção, vagas e colocados da 1.ª fase de 2025 (DGES), na ficha do curso. | RF46.1, RF46.4 | `RecolhaDaTabelaTests` (distingue as duas linhas «em 1.ª opção» da tabela); `test_a_ficha_mostra_tendencia_procura_e_quanto_precisa` |
| Etiqueta: «Sobraram vagas», «Muito procurado», «Procurado» ou «Pouco escolhido em 1.ª opção». | RF46.2, RF46.3 | `TendenciaEProcuraTests.test_procura` (as quatro etiquetas e sem dados) |

## 6. Requisitos não funcionais aplicáveis

RNF06 (testes sem rede), RNF09 (uso de IA documentado), RNF10 (a etiqueta é texto, não só cor), RNF11 (português de Portugal).

## 7. Decisões e questões em aberto

| # | Questão | Estado |
|---|---|---|
| 1 | Os limites 0,75 e 1,5 candidatos em 1.ª opção por vaga são uma proposta. | Proposta do Claude, aceite pelo PO a 23/10 |
