# US45 — Plano B: 2.ª fase: requisitos funcionais

> **Como** candidato, **quero** ver cursos das áreas do meu plano que tiveram vagas na 2.ª fase e a que a minha nota chegava, **para** ter uma alternativa se não entrar na 1.ª fase.

| | |
|---|---|
| Épico | E4 — Plano de candidatura |
| Prioridade | Could · 2 story points · Sprint 4 |
| Requisitos de origem | RF49 |
| Atores | Aluno com sessão iniciada |
| Depende de | US04 (recolha da DGES), US35 (nota), US36 (plano) |
| Artefactos | [Use case](use-case.md) · [BPMN](bpmn.md) · [Prompt](prompt.md) |

## 1. Âmbito

**Dentro:** procurar e mostrar cursos alternativos para a 2.ª fase, a partir dos dados de 2025.

**Fora:** as vagas reais da 2.ª fase de 2026 (só são conhecidas depois da 1.ª fase); a 3.ª fase.

## 2. Requisitos funcionais da US45

| ID | Requisito |
|---|---|
| **RF49.1** | A recolha (US04) lê, da tabela da DGES, as vagas, os colocados e o último colocado da 2.ª fase de 2025. |
| **RF49.2** | Só aparece com notas indicadas e pelo menos uma opção no plano. |
| **RF49.3** | Procura cursos das áreas das opções, fora do plano, do concurso nacional (RN12), que tiveram vagas na 2.ª fase e em que a pessoa cumpre provas e mínimos. |
| **RF49.4** | Um curso entra se a nota da pessoa chega ao último colocado da 2.ª fase; sem essa nota, só se ficaram vagas por preencher. |
| **RF49.5** | Mostra até 3, os mais disputados primeiro, com as vagas e o último colocado (ou «sobraram lugares»), e o aviso de que as vagas da 2.ª fase mudam todos os anos. |
| **RF49.6** | Sem nenhum curso, a secção explica porque ainda não há plano B. |

## 3. Mensagens

Os textos estão em [`app/texts.py`](../../app/texts.py).

| Situação | Mensagem |
|---|---|
| Título | Plano B: 2.ª fase |
| Introdução e aviso | Se não ficar colocado na 1.ª fase, estes cursos das mesmas áreas tiveram vagas na 2.ª fase de 2025 e a sua nota chegava ao último colocado dessa fase. As vagas da 2.ª fase são as que sobram da 1.ª: mudam todos os anos. |
| Sem plano B | Ainda não há um plano B: nenhum outro curso das áreas do seu plano teve vagas na 2.ª fase de 2025 a que a sua nota chegasse. Quando o catálogo tiver todas as licenciaturas da DGES, aparecerão mais cursos. |
| Detalhe | Vagas na 2.ª fase de 2025: {vagas} · último colocado: {ultimo} |

## 4. Dados

Colunas `vagas_2fase_2025`, `colocados_2fase_2025` e `ultimo_colocado_2fase_2025` do catálogo.

## 5. Critérios de aceitação e testes

| Critério da story (backlog) | Requisitos | Testes automáticos |
|---|---|---|
| Vagas, colocados e último colocado da 2.ª fase de 2025 (DGES). | RF49.1 | `RecolhaDaTabelaTests` (2.ª fase) |
| Só cursos fora do plano, das mesmas áreas, onde a nota da pessoa chegava ao último colocado da 2.ª fase (ou, sem essa nota, onde sobraram vagas). | RF49.2 a RF49.4 | `PlanoBTests` (2 testes); `test_o_plano_mostra_exames_que_abrem_portas_e_plano_b` (o curso já no plano fica de fora) |
| Aviso: as vagas da 2.ª fase são as que sobram da 1.ª e mudam todos os anos. | RF49.5, RF49.6 | `test_o_plano_mostra_exames_que_abrem_portas_e_plano_b` (aviso acrescentado ao teste a 27/10); `test_plano_b_vazio_explica_porque` |

## 6. Requisitos não funcionais aplicáveis

RNF06 (testes sem rede), RNF09 (uso de IA documentado), RNF11 (português de Portugal), RN11 (dados de 2025 como referência).

## 7. Decisões e questões em aberto

| # | Questão | Estado |
|---|---|---|
| 1 | Com os 174 cursos do protótipo, o plano B tem poucos resultados; melhora com a recolha completa (US48). | Aceite (dito na página) |
