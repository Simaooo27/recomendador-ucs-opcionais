# US41 — Tendência do último colocado: requisitos funcionais

> **Como** candidato, **quero** ver como a nota do último colocado mudou de 2023 a 2025, **para** perceber se um curso está a ficar mais difícil de entrar.

| | |
|---|---|
| Épico | E4 — Plano de candidatura |
| Prioridade | Should · 2 story points · Sprint 4 |
| Requisitos de origem | RF45 |
| Atores | Pessoa, com ou sem sessão (na ficha); aluno com sessão (no plano) |
| Depende de | US04 (recolha da DGES), US05 (ficha) |
| Artefactos | [Use case](use-case.md) · [BPMN](bpmn.md) · [Prompt](prompt.md) |

## 1. Âmbito

**Dentro:** ler o último colocado da 1.ª fase de 2023 a 2025 e mostrar os valores e a tendência na ficha e no plano.

**Fora:** prever o último colocado de 2026; outros contingentes ou fases.

## 2. Requisitos funcionais da US41

| ID | Requisito |
|---|---|
| **RF45.1** | A recolha (US04) lê, da tabela de estatísticas da DGES, a nota do último colocado pelo contingente geral na 1.ª fase de 2023, 2024 e 2025. |
| **RF45.2** | A ficha mostra os anos que têm valor, do mais antigo para o mais recente. |
| **RF45.3** | Com 2 ou mais anos, a etiqueta compara o mais recente com o mais antigo: «A subir» (3 ou mais pontos acima), «A descer» (3 ou mais abaixo) ou «Estável». Com menos de 2 anos não há etiqueta. |
| **RF45.4** | A etiqueta aparece também em cada opção do plano; os anos ficam no texto de ajuda. |
| **RF45.5** | A tendência não se diz só pela cor: há uma seta e a palavra. |

## 3. Mensagens

Os textos estão em [`app/texts.py`](../../app/texts.py).

| Situação | Mensagem |
|---|---|
| Título | Último colocado (1.ª fase) |
| Subir | A subir |
| Descer | A descer |
| Estável | Estável |

## 4. Dados

Colunas `ultimo_colocado_1fase_2023` e `ultimo_colocado_1fase_2024` do catálogo (a de 2025 já existia).

## 5. Critérios de aceitação e testes

| Critério da story (backlog) | Requisitos | Testes automáticos |
|---|---|---|
| Notas da 1.ª fase de 2023, 2024 e 2025 (DGES) na ficha do curso. | RF45.1, RF45.2 | `RecolhaDaTabelaTests.test_le_a_1a_fase_de_cada_ano_e_distingue_as_duas_linhas_em_1a_opcao`; `test_a_ficha_mostra_tendencia_procura_e_quanto_precisa` |
| Etiqueta «A subir», «A descer» ou «Estável» (3 pontos de margem entre o primeiro e o último ano). | RF45.3 | `TendenciaEProcuraTests.test_tendencia_compara_o_ano_mais_recente_com_o_mais_antigo` |
| A etiqueta aparece também em cada opção do plano. | RF45.4 | `test_cada_opcao_do_plano_mostra_quanto_precisa_e_a_tendencia` (acrescentado a 27/10) |

## 6. Requisitos não funcionais aplicáveis

RNF06 (a leitura da tabela é testada com HTML fixo, sem rede), RNF09 (uso de IA documentado), RNF10 (seta escondida dos leitores de ecrã e palavra escrita), RNF11 (português de Portugal).

## 7. Decisões e questões em aberto

| # | Questão | Estado |
|---|---|---|
| 1 | A margem de 3 pontos para «Estável» é uma proposta. | Proposta do Claude, aceite pelo PO a 23/10 |
