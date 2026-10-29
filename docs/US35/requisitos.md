# US35 — Nota de candidatura a cada curso: requisitos funcionais

> **Como** candidato, **quero** ver a minha nota de candidatura a cada curso e a diferença para o último colocado, **para** perceber onde tenho hipóteses.

| | |
|---|---|
| Épico | E4 — Plano de candidatura |
| Prioridade | Must · 3 story points · Sprint 4 |
| Requisitos de origem | RF42, RN11 |
| Atores | Aluno com sessão iniciada |
| Depende de | US33, US34 |
| Artefactos | [Use case](use-case.md) · [BPMN](bpmn.md) · [Prompt](prompt.md) |

## 1. Âmbito

**Dentro:** calcular a nota de candidatura do aluno a um curso, compará-la com os mínimos e com o último colocado e mostrá-la na ficha do curso. A mesma conta serve as opções do plano (US36).

**Fora:** contingentes especiais, preferência regional e bonificações; prever a nota do último colocado de 2026; quanto falta nos exames por fazer (US40, no backlog).

## 2. Requisitos funcionais da US35

| ID | Requisito |
|---|---|
| **RF42.1** | Nota de candidatura = média do secundário × 10 × peso do secundário + média das provas do conjunto × peso das provas, numa escala de 0 a 200, com uma casa decimal. |
| **RF42.2** | Usa-se cada conjunto de provas que o aluno tem completo e fica o que dá a nota mais alta, preferindo sempre um conjunto que conte para a colocação. |
| **RF42.3** | Situação: **acima** (5 ou mais pontos acima do último colocado), **perto** (menos de 5 pontos de diferença, para cima ou para baixo) ou **abaixo**. Sem nota do último colocado, a situação é «cumpre os mínimos». |
| **RF42.4** | A opção não conta quando falta uma prova de ingresso (a página diz qual falta, no conjunto mais próximo) ou quando uma prova ou a nota final fica abaixo do mínimo do curso (a página diz qual). |
| **RF42.5** | Sem média indicada, a ficha pede as notas (US34); sem condições de acesso no catálogo, diz que a DGES não as publica. |
| **RF42.6** | A secção «A sua nota neste curso» aparece na ficha com sessão iniciada; sem sessão, a ficha convida a entrar. |
| **RF42.7** | Sempre que a página mostra uma nota de candidatura, mostra também o aviso de que é uma estimativa (RN11). |
| **RF42.8** | Num curso do ensino privado, a ficha diz que não entra no concurso nacional (a candidatura é na instituição) e não calcula a nota (RN12). *(27/10)* |

## 3. Mensagens

| Situação | Mensagem |
|---|---|
| Acima | Acima do último colocado (+7,7) |
| Perto | Perto do último colocado (−1,8) |
| Abaixo | Abaixo do último colocado (−12,0) |
| Sem último colocado | Cumpre os mínimos (sem nota do último colocado em 2025) |
| Falta prova | Falta-lhe uma prova de ingresso · Falta: História |
| Abaixo do mínimo | Abaixo da classificação mínima · Abaixo do mínimo de 95 pontos: Português |
| Conjunto usado | Conta com: História + Português |
| Sem notas | Indique as suas notas para ver a sua nota |
| Ensino privado | Ensino privado: não entra no concurso nacional (candidatura na instituição) |
| Estimativa | As contas são uma estimativa para o contingente geral da 1.ª fase, com as regras publicadas pela DGES. A nota do último colocado muda todos os anos: é uma referência, não uma garantia. |

## 4. Dados

Sem dados novos: usa as condições do catálogo (US33) e as notas do aluno (US34).

## 5. Critérios de aceitação e testes

| Critério da story (backlog) | Requisitos | Testes automáticos (`tests/test_candidatura.py`) |
|---|---|---|
| Nota = média do secundário × peso + provas × peso, com o conjunto de provas mais favorável. | RF42.1, RF42.2 | `ContasTests.test_nota_de_candidatura_com_a_formula_do_curso`, `test_usa_o_conjunto_de_provas_que_da_a_nota_mais_alta` |
| Situação: acima, perto ou abaixo; falta de prova e nota abaixo do mínimo assinaladas. | RF42.3 a RF42.5 | `ContasTests.test_perto_e_abaixo_do_ultimo_colocado`, `test_falta_prova_diz_qual_falta`, `test_prova_abaixo_do_minimo_nao_conta`, `test_sem_notas_sem_regras_e_sem_referencia` |
| Aparece na ficha de cada curso, com sessão iniciada. | RF42.6 | `test_a_ficha_mostra_as_condicoes_de_acesso_e_a_nota_do_aluno` (146,0); `test_sem_sessao_a_ficha_mostra_as_condicoes_e_pede_para_entrar` |
| Aviso visível: estimativa para o contingente geral da 1.ª fase, não uma garantia. | RF42.7 | `test_a_ficha_e_o_plano_dizem_que_a_nota_e_uma_estimativa` (acrescentado a 27/10) |
| (ensino privado, 27/10) | RF42.8 | `ContasTests.test_ensino_privado_fica_fora_do_concurso_nacional`; `test_curso_privado_nao_entra_no_plano` |

## 6. Requisitos não funcionais aplicáveis

RNF06 (contas testadas com casos de resultado conhecido, sem rede), RNF07 (as contas estão em `calculos.py`, sem Flask nem base de dados), RNF09 (uso de IA documentado), RNF10 (a situação é dita por texto, não só pela cor da etiqueta), RNF11 (português de Portugal).

## 7. Decisões e questões em aberto

| # | Questão | Estado |
|---|---|---|
| 1 | A margem de «perto» é de 5 pontos (0,5 valores). | Proposta do Claude, aceite pelo PO a 23/10 |
| 2 | Até 27/10 a ficha mostrava a nota sem o aviso de estimativa (só o plano o tinha), o que não cumpria o 4.º critério. Corrigido ao escrever esta documentação. | **Corrigido** (27/10) |
| 3 | Matemática e Matemática A contavam como o mesmo exame. | **Corrigido** (27/10): correspondência completa da DGES (US34, RF41.4) |
| 4 | Os cursos do ensino privado apareciam com «Cumpre os mínimos», como se entrassem no concurso nacional. | **Corrigido** (27/10): RN12 |
