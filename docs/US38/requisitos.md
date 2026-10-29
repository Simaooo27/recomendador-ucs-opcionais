# US38 — Datas do concurso no percurso: requisitos funcionais

> **Como** candidato, **quero** ver as datas das fases do concurso nacional, **para** não falhar prazos.

| | |
|---|---|
| Épico | E4 — Plano de candidatura |
| Prioridade | Could · 2 story points · Sprint 4 |
| Requisitos de origem | RF50 |
| Atores | Aluno com sessão iniciada |
| Depende de | US31 (percurso), US36 (plano) |
| Artefactos | [Use case](use-case.md) · [BPMN](bpmn.md) · [Prompt](prompt.md) |

## 1. Âmbito

**Dentro:** as datas das 3 fases do concurso nacional, no plano, e o próximo prazo no percurso.

**Fora:** lembretes por email; datas dos concursos especiais e dos exames nacionais; recolher as datas automaticamente do site da DGES.

## 2. Requisitos funcionais da US38

| ID | Requisito |
|---|---|
| **RF50.1** | As datas ficam em `dados/calendario-concurso.csv` (ano, fase, etapa, início, fim, nota), copiadas do despacho anual. O OptaBem usa o ano mais recente do ficheiro. Uma etapa desconhecida ou que acaba antes de começar dá erro ao ler o ficheiro. |
| **RF50.2** | O plano de candidatura mostra, para cada fase (1.ª, 2.ª e 3.ª), a candidatura, os resultados e a matrícula, com as notas do despacho (por exemplo, o prazo mais curto do contingente prioritário), e a ligação para o calendário oficial da DGES. |
| **RF50.3** | O próximo prazo é a etapa a decorrer hoje (se houver duas ao mesmo tempo, a que acaba primeiro) ou, se não houver, a próxima a começar. É calculado por uma função pura, testada com dias fixos. |
| **RF50.4** | O passo atual do percurso, no início, mostra o próximo prazo numa frase («Candidatura da 1.ª fase: até 06/08/2026.»), com a ligação para a DGES. No plano, a etapa a decorrer fica assinalada. |
| **RF50.5** | Depois da última data publicada, o início e o plano dizem que as datas do ano seguinte ainda não foram publicadas; o plano continua a mostrar as datas do ano que passou. Sem ficheiro, o plano manda para a DGES. |

## 3. Mensagens

Os textos estão em [`app/texts.py`](../../app/texts.py).

| Situação | Mensagem |
|---|---|
| Etapa a decorrer | Candidatura da 1.ª fase: até 06/08/2026. |
| Etapa por vir | Resultados da 1.ª fase: 23/08/2026. |
| Concurso terminado (início) | As datas do concurso de 2027 ainda não foram publicadas. |
| Concurso terminado (plano) | O concurso de 2026 já terminou. As datas de 2027 ainda não foram publicadas: costumam sair na primavera. |
| Sem ficheiro | O OptaBem ainda não tem as datas do concurso. Consulte o calendário no site da DGES. |

## 4. Dados

Ficheiro `dados/calendario-concurso.csv` (UTF-8 com BOM, como os outros ficheiros de `dados/`). Não há tabelas novas.

| Fase | Candidatura | Resultados | Matrícula |
|---|---|---|---|
| 1.ª | 20/07 a 06/08/2026 (prioritários até 27/07) | 23/08/2026 | 24/08 a 27/08/2026 |
| 2.ª | 24/08 a 02/09/2026 | 13/09/2026 | 14/09 a 16/09/2026 |
| 3.ª | 22/09 a 24/09/2026 | 30/09/2026 | 30/09 a 02/10/2026 |

Fonte: Despacho n.º 6934/2026, de 1 de junho, do Instituto para o Ensino Superior, I.P. (confirmado a 29/10/2026).

## 5. Critérios de aceitação e testes

| Critério da story (backlog) | Requisitos | Testes automáticos (`tests/test_calendario.py`) |
|---|---|---|
| Datas das 3 fases do concurso, com a ligação para a DGES. | RF50.1, RF50.2, RF50.5 | `test_tem_as_3_fases_de_2026_cada_uma_com_as_3_etapas`, `test_datas_do_despacho`, `test_mostra_o_ano_mais_recente_do_ficheiro`, `test_sem_ficheiro_o_calendario_fica_vazio`, `test_erros_no_ficheiro_sao_assinalados`, `test_o_plano_mostra_as_3_fases_e_a_ligacao_para_a_dges`, `test_o_plano_depois_do_concurso_avisa_e_continua_a_mostrar_as_datas`, `test_sem_ficheiro_o_plano_manda_para_a_dges` |
| O passo atual do percurso mostra o próximo prazo. | RF50.3, RF50.4, RF50.5 | `test_antes_do_concurso_e_a_candidatura_a_1a_fase`, `test_durante_a_candidatura_diz_ate_quando`, `test_no_ultimo_dia_ainda_esta_a_decorrer`, `test_entre_etapas_e_a_seguinte`, `test_no_dia_dos_resultados`, `test_com_duas_etapas_ao_mesmo_tempo_conta_a_que_acaba_primeiro`, `test_depois_do_concurso_diz_que_as_datas_seguintes_ainda_nao_sairam`, `test_sem_datas_nenhumas`, `test_o_passo_atual_mostra_o_proximo_prazo`, `test_depois_do_concurso_o_percurso_avisa_que_as_datas_ainda_nao_sairam` |

## 6. Requisitos não funcionais aplicáveis

RNF06 (testes sem rede nem relógio), RNF09 (uso de IA documentado), RNF11 (português de Portugal). RN11: as datas são uma ajuda; a página manda confirmar na DGES.

## 7. Decisões e questões em aberto

| # | Questão | Estado |
|---|---|---|
| 1 | Datas num ficheiro e não recolhidas do site: o despacho sai uma vez por ano e a página da DGES muda de formato. | Decidido pelo Claude, aceite pelo PO |
| 2 | Alguém da equipa tem de juntar as datas de 2027 quando o despacho for publicado (costuma ser na primavera). | Em aberto |
| 3 | Desde o visual calmo (29/10), a secção do plano fica fechada, menos quando uma etapa está a decorrer. | Feito no PR do visual calmo |
