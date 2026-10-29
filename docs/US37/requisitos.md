# US37 — Assistente que conhece as minhas notas: requisitos funcionais

> **Como** pessoa indecisa, **quero** que o assistente tenha em conta as provas que fiz e a minha nota, **para** não me sugerir cursos a que não posso concorrer.

| | |
|---|---|
| Épico | E3 — Orientação com o assistente |
| Prioridade | Should · 3 story points · Sprint 4 |
| Requisitos de origem | RF36 (conversa), RF41 (exames e média), RNF12 (o que vai para o LLM); detalhe no RF52 |
| Atores | Aluno com sessão; LLM (Gemini) |
| Depende de | US29 (conversa), US34 (exames no plano) |
| Artefactos | [Use case](use-case.md) · [BPMN](bpmn.md) · [Prompt](prompt.md) |

## 1. Âmbito

**Dentro:** a autorização ao começar a conversa, o envio dos nomes dos exames e de um intervalo da média, tirar do catálogo enviado os cursos com prova em falta, e assinalar a prova em falta nos cursos sugeridos.

**Fora:** enviar a nota de cada exame ou a média exata; ter em conta notas mínimas ou a nota do último colocado (isso fica no plano e na ficha, com a conta feita pelo OptaBem e não pelo LLM); usar as notas na conversa sem sessão.

## 2. Requisitos funcionais da US37

| ID | Requisito |
|---|---|
| **RF52.1** | Ao começar a conversa, quem tem exames no plano de candidatura vê uma caixa **desmarcada** para autorizar o uso das notas, com o texto do que o assistente recebe (os nomes dos exames e o intervalo da média). Sem exames no plano, não há caixa: há uma ligação para o plano. Pedir a autorização sem exames não liga nada. |
| **RF52.2** | Com autorização, todos os pedidos ao LLM dessa conversa levam os nomes dos exames feitos e a média do secundário num intervalo de 2 valores, entre 10 e 20 (sem média indicada, só os exames). Nunca a média exata, nem a nota de cada exame, nem o email, nem o nome (RNF12). Sem autorização, o LLM não recebe nada das notas. |
| **RF52.3** | A autorização fica guardada na conversa (coluna `usar_notas`) e a página diz que está ligada. Recomeçar a conversa tira-a. |
| **RF52.4** | Com autorização, o catálogo enviado ao LLM deixa de ter os cursos a que falta uma prova de ingresso. Se sobrarem menos de 10 cursos, vai o catálogo inteiro (para a conversa não ficar sem opções). Uma sugestão do LLM fora do catálogo enviado é descartada (como na US30). |
| **RF52.5** | Quando o catálogo foi enviado sem esse filtro, cada curso sugerido a que falta uma prova traz o aviso «Atenção: para concorrer a este curso falta-lhe o exame de …». Sem autorização, não se assinala nada. |

## 3. Mensagens

Os textos estão em [`app/texts.py`](../../app/texts.py).

| Situação | Mensagem |
|---|---|
| Caixa | Usar os exames que fiz e a minha média, para o assistente não me sugerir cursos a que não posso concorrer |
| O que é enviado | O assistente recebe só isto: os exames que fez ({exames}) e a sua média do secundário {media}. Nunca recebe a média exata nem a nota de cada exame. |
| Sem exames no plano | Se indicar os exames que fez no plano de candidatura, o assistente pode tê-los em conta (só se autorizar). |
| Autorização ligada | Nesta conversa, o assistente sabe os exames que fez e a sua média aproximada. Para deixar de os usar, recomece a conversa. |
| Prova em falta | Atenção: para concorrer a este curso falta-lhe o exame de {provas}. |

## 4. Dados

| Tabela | Coluna nova |
|---|---|
| `conversas_orientacao` | `usar_notas` (0 ou 1; 0 por omissão; a migração acrescenta-a às bases de dados antigas) |

## 5. Critérios de aceitação e testes

| Critério da story (backlog) | Requisitos | Testes automáticos (`tests/test_assistente_notas.py`) |
|---|---|---|
| Só com autorização da pessoa, o LLM recebe as provas feitas e um intervalo de nota (nunca a média exata, RNF12). | RF52.1, RF52.2, RF52.3 | `test_intervalo_da_media_de_2_valores`, `test_o_contexto_tem_os_exames_e_o_intervalo_mas_nunca_as_notas`, `test_sem_exames_nao_ha_contexto`, `test_sem_media_vai_so_a_lista_de_exames`, `test_sem_notas_no_plano_nao_ha_caixa_mas_ha_a_ligacao_para_o_plano`, `test_com_exames_a_caixa_diz_o_que_o_assistente_recebe`, `test_sem_autorizacao_o_llm_nao_recebe_nada_das_notas`, `test_com_autorizacao_todos_os_pedidos_levam_as_provas_e_o_intervalo`, `test_a_media_exata_nunca_vai_para_o_llm`, `test_pedir_a_autorizacao_sem_exames_no_plano_nao_liga_nada`, `test_recomecar_tira_a_autorizacao` |
| Cursos a que falta uma prova não são sugeridos, ou vêm assinalados. | RF52.4, RF52.5 | `test_provas_em_falta`, `test_o_catalogo_enviado_nao_tem_cursos_com_prova_em_falta`, `test_com_poucos_cursos_possiveis_vai_o_catalogo_inteiro`, `test_os_cursos_com_prova_em_falta_nao_vao_para_o_llm`, `test_um_curso_com_prova_em_falta_que_o_llm_invente_e_descartado`, `test_sem_filtro_o_curso_vem_assinalado_com_a_prova_que_falta`, `test_sem_autorizacao_nao_se_assinala_nada` |
| Os testes usam o LLM falso. | RNF06 | Todos os testes acima usam `LLMFalso` e correm sem rede |

Os testes usam o catálogo da DGES (`dados/catalogo-cursos.csv`), porque o catálogo do MVP não tem provas de ingresso.

## 6. Requisitos não funcionais aplicáveis

RNF06 (testes sem rede), RNF09 (uso de IA documentado), RNF11 (português de Portugal), RNF12 (o que vai para o LLM: aqui é a primeira vez que vão dados do aluno, por isso só com autorização e sem valores exatos).

## 7. Decisões e questões em aberto

| # | Questão | Estado |
|---|---|---|
| 1 | Um intervalo de 2 valores, e não a média exata: chega para o assistente perceber o nível da pessoa e não identifica a nota. | Decidido pelo Claude, aceite pelo PO |
| 2 | Tirar os cursos com prova em falta, em vez de pedir ao LLM para os evitar: é o OptaBem que faz a conta, e o LLM não pode sugerir o que não recebe. Abaixo de 10 cursos, vai tudo e o aviso aparece no curso. | Decidido pelo Claude, aceite pelo PO |
| 3 | A conversa é para maiores de 18 (ponto 14 dos requisitos), e muitos candidatos têm 17 anos. A US37 envia mais dados do aluno, o que torna este limite mais importante se o OptaBem deixar de ser um protótipo. | Em aberto (fica no relatório) |
| 4 | A exportação dos dados (US46) ainda não inclui a autorização `usar_notas`: acrescentar depois de os dois ramos estarem na `main`. | Em aberto |
