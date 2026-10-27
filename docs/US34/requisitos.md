# US34 — Registar as minhas notas: requisitos funcionais

> **Como** candidato, **quero** indicar a minha média do secundário e as notas dos exames nacionais que fiz, **para** o OptaBem fazer as contas por mim.

| | |
|---|---|
| Épico | E4 — Plano de candidatura |
| Prioridade | Must · 2 story points · Sprint 4 |
| Requisitos de origem | RF41, RF17 |
| Atores | Aluno com sessão iniciada |
| Depende de | US02, US33 |
| Artefactos | [Use case](use-case.md) · [BPMN](bpmn.md) · [Prompt](prompt.md) |

## 1. Âmbito

**Dentro:** o formulário das notas, a validação, a conversão de valores em pontos e a gravação no plano de candidatura do aluno.

**Fora:** as contas com as notas (US35); importar as notas de outro sistema; notas de contingentes especiais ou de exames estrangeiros.

## 2. Requisitos funcionais da US34

| ID | Requisito |
|---|---|
| **RF41.1** | A página `/candidatura/notas` só abre com sessão iniciada. Tem a média do secundário e um campo por cada prova de ingresso do catálogo, por ordem alfabética do nome. |
| **RF41.2** | A média é obrigatória e tem de estar entre 9,5 e 20 valores. Aceita vírgula ou ponto. |
| **RF41.3** | Os exames são opcionais: só se preenchem os que a pessoa fez. Cada um aceita de 0 a 200 pontos ou de 0 a 20 valores; um número até 20 é convertido em pontos (14,5 → 145). |
| **RF41.4** | «Matemática» (16) e «Matemática A» (19) aparecem num só campo e contam como o mesmo exame. |
| **RF41.5** | Com erros, nada é guardado: a página volta com os valores escritos e a mensagem junto ao campo (código 422). |
| **RF41.6** | Sem erros, as notas ficam no plano de candidatura do aluno e a página leva ao plano com «Notas guardadas.». Ao voltar ao formulário, os valores guardados aparecem preenchidos. |
| **RF41.7** | As notas saem com a conta (US17) e nunca são enviadas ao LLM (RNF12). |

## 3. Mensagens

| Situação | Mensagem |
|---|---|
| Introdução | Só servem para as contas do plano. Pode mudá-las quando quiser, e saem com a conta se a apagar. |
| Ajuda da média | De 9,5 a 20 valores, por exemplo 15,2. |
| Ajuda dos exames | Preencha só os que fez, de 0 a 200 pontos (ou de 0 a 20 valores: 14,5 conta como 145). |
| Média vazia | Indique a sua média do secundário. |
| Média fora do intervalo | A média tem de estar entre 9,5 e 20 valores. |
| Exame inválido | Use um número de 0 a 200 (ou de 0 a 20). |
| Guardado | Notas guardadas. |

## 4. Dados

Tabela `planos_candidatura` (uma linha por aluno): `media` (0 a 20, vazio = ainda não indicou) e `exames` (JSON com o código da prova e a nota de 0 a 200). A mesma linha guarda as opções do plano (US36). A linha é apagada com a conta (`ON DELETE CASCADE`).

## 5. Critérios de aceitação e testes

| Critério da story (backlog) | Requisitos | Testes automáticos (`tests/test_candidatura.py`) |
|---|---|---|
| Média de 9,5 a 20 valores; exames de 0 a 200 pontos (ou de 0 a 20, convertidos). | RF41.2, RF41.3, RF41.5 | `test_notas_invalidas_nao_sao_guardadas`; `ContasTests.test_exames_em_valores_ou_em_pontos` |
| Só se preenchem os exames feitos. | RF41.3 | `test_percurso_completo_notas_juntar_ordenar_e_retirar` (só Português preenchido) |
| As notas podem ser mudadas e saem com a conta (US17). | RF41.6, RF41.7 | `test_apagar_a_conta_apaga_o_plano`; mudar as notas usa o mesmo formulário (sem teste próprio) |
| Matemática e Matemática A contam com o mesmo exame (a confirmar pela equipa na DGES). | RF41.4 | `test_o_formulario_mostra_matematica_a_uma_so_vez`; `ContasTests.test_matematica_e_matematica_a_contam_com_o_mesmo_exame` |
| (sessão iniciada) | RF41.1 | `test_e_preciso_ter_sessao` |

## 6. Requisitos não funcionais aplicáveis

RNF01 (só as notas necessárias; apagadas com a conta), RNF02 (CSRF no formulário; SQL parametrizado), RNF06 (testes sem rede), RNF09 (uso de IA documentado), RNF10 (cada campo com etiqueta; o erro ligado ao campo com `aria-describedby` e `aria-invalid`), RNF11 (português de Portugal), RNF12 (as notas nunca vão para o LLM).

## 7. Decisões e questões em aberto

| # | Questão | Estado |
|---|---|---|
| 1 | Matemática (16) e Matemática A (19) contam como o mesmo exame. | **Por confirmar** pela equipa na DGES (ponto 16 dos requisitos) |
| 2 | As notas do secundário são dados pessoais. Ficam na conta do aluno, saem com ela e só aparecem a outras pessoas pela partilha (US43), que nunca mostra a média nem os exames. | Aceite |
