# US39 — Corrigir e esconder cursos do catálogo: requisitos funcionais

> **Como** administrador, **quero** corrigir a descrição e as saídas profissionais de um curso, ou escondê-lo, **para** o catálogo não ter erros sem mexer no ficheiro.

| | |
|---|---|
| Épico | E2 — Catálogo de cursos |
| Prioridade | Should · 5 story points · Sprint 4 |
| Requisitos de origem | RF04 (perfis), RF05 (catálogo); detalhe no RF51 |
| Atores | Administrador; aluno ou visitante (vê o resultado) |
| Depende de | US03 (gestão), US04 (catálogo da DGES) |
| Artefactos | [Use case](use-case.md) · [BPMN](bpmn.md) · [Prompt](prompt.md) |

## 1. Âmbito

**Dentro:** corrigir a descrição e as saídas profissionais, esconder e voltar a mostrar um curso, repor os dados da DGES e o histórico das alterações.

**Fora:** editar os outros campos (vagas, notas, provas, que vêm da DGES); acrescentar cursos à mão; um editor genérico das tabelas da base de dados (sugestão de um colega a 23/10, recusada porque daria aos administradores os dados dos alunos).

## 2. Requisitos funcionais da US39

| ID | Requisito |
|---|---|
| **RF51.1** | Só administradores: `/gestao/cursos` (lista com procura e filtro «todos», «corrigidos ou escondidos», «escondidos») e `/gestao/cursos/<chave>` (corrigir). Sem sessão de administrador, vai para o início de sessão. Todos os POST com CSRF. Curso inexistente: 404. |
| **RF51.2** | A página do curso permite mudar a descrição (até 3000 caracteres) e as saídas profissionais (uma por linha, até 1500 caracteres) e marcar «Esconder este curso», com o texto da DGES ao lado. Um campo vazio, ou igual ao da DGES, deixa de ser correção. Os outros campos do pedido são ignorados. |
| **RF51.3** | As correções ficam na tabela `correcoes_cursos`, por cima do ficheiro da DGES: uma recolha nova reescreve o CSV mas não as apaga. «Repor os dados da DGES» apaga a correção. |
| **RF51.4** | O catálogo que a aplicação usa (ficha, pesquisa, comparação, conversa com o assistente, plano) aplica as correções e deixa de fora os cursos escondidos. Uma opção do plano que deixou de estar no catálogo aparece num aviso, com «Retirar». |
| **RF51.5** | Cada alteração (descrição, saídas, escondido, visível, reposto) fica na tabela `historico_catalogo` com o nome do administrador e a hora, e aparece na página do curso. Guardar sem mudar nada não regista. O registo fica mesmo que o administrador seja removido. |
| **RF51.6** | As tabelas das correções não têm ligação aos alunos (nem `user_id`, nem email, nem chaves estrangeiras), e as páginas do catálogo na gestão não mostram dados de alunos. |

## 3. Mensagens

Os textos estão em [`app/texts.py`](../../app/texts.py).

| Situação | Mensagem |
|---|---|
| Introdução | Os cursos vêm da DGES. Aqui pode corrigir a descrição e as saídas profissionais, ou esconder um curso. As correções ficam por cima dos dados da DGES: a recolha seguinte não as apaga. |
| Guardado | Correção guardada. |
| Sem alterações | Nada mudou. |
| Reposto | O curso voltou aos dados da DGES. |
| Texto longo | O texto não pode ter mais de {maximo} caracteres. |
| Aviso no plano do aluno | Estas opções já não estão no catálogo do OptaBem e não contam para a nota nem para os avisos. Confirme na DGES e retire-as do plano. |

## 4. Dados

| Tabela | Colunas |
|---|---|
| `correcoes_cursos` | `curso_chave` (chave), `descricao`, `saidas` (vazio = texto da DGES), `escondido`, `alterado_por`, `alterado_em` |
| `historico_catalogo` | `id`, `curso_chave`, `alteracao` (códigos separados por vírgula), `alterado_por`, `alterado_em` |

## 5. Critérios de aceitação e testes

| Critério da story (backlog) | Requisitos | Testes automáticos (`tests/test_gestao_catalogo.py`) |
|---|---|---|
| Só na área de gestão. | RF51.1 | `test_sem_sessao_e_alunos_nao_entram`, `test_sem_csrf_e_recusado`, `test_a_gestao_tem_a_ligacao_para_o_catalogo`, `test_lista_e_procura_os_cursos`, `test_curso_inexistente_da_404` |
| As correções ficam na base de dados, por cima dos dados da DGES (a recolha seguinte não as apaga). | RF51.2, RF51.3, RF51.4 | `test_corrigir_a_descricao_muda_a_ficha_e_o_catalogo_da_aplicacao`, `test_saidas_uma_por_linha`, `test_guardar_o_formulario_como_vem_so_muda_o_que_se_editou`, `test_campo_vazio_ou_igual_ao_da_dges_nao_e_correcao`, `test_texto_demasiado_longo_e_recusado`, `test_o_texto_e_mostrado_sem_html`, `test_um_curso_escondido_desaparece_para_os_alunos`, `test_no_plano_do_aluno_fica_um_aviso_para_o_retirar`, `test_continua_na_gestao_assinalado`, `test_voltar_a_mostrar`, `test_a_correcao_sobrevive_a_uma_recolha_nova`, `test_repor_mostra_o_texto_da_recolha_nova` |
| Fica registado quem alterou e quando. | RF51.5 | `test_regista_o_administrador_e_a_hora`, `test_a_pagina_do_curso_mostra_o_historico`, `test_guardar_sem_mudar_nada_nao_regista`, `test_repor_tambem_fica_registado`, `test_o_registo_fica_mesmo_se_o_administrador_for_removido` |
| Sem acesso aos dados dos alunos. | RF51.6 | `test_as_paginas_do_catalogo_nao_mostram_dados_de_alunos`, `test_as_tabelas_das_correcoes_nao_tem_ligacao_aos_alunos`, `test_o_formulario_so_altera_descricao_saidas_e_visibilidade` |

## 6. Requisitos não funcionais aplicáveis

RNF01 (sem dados de alunos), RNF02 (só administradores; CSRF; texto mostrado sem HTML), RNF03 (o catálogo lê as correções a cada pedido: medir com o catálogo completo, US48), RNF06 (testes sem rede), RNF09 (uso de IA documentado), RNF11 (português de Portugal).

## 7. Decisões e questões em aberto

| # | Questão | Estado |
|---|---|---|
| 1 | Só a descrição, as saídas e a visibilidade: os números vêm da DGES e devem ser corrigidos lá (na recolha). | Decidido pelo Claude, aceite pelo PO |
| 2 | As correções são aplicadas num só sítio (`catalogo.services.cursos`), para o curso mudar em todas as páginas e na conversa com o assistente. | Feito |
| 3 | Na verificação visual, guardar o formulário sem mexer nas saídas registava-as como corrigidas (a caixa vinha com maiúsculas que a ficha acrescenta). Corrigido, com um teste que falhava antes. | Corrigido (29/10) |
| 4 | Com o catálogo completo (US48), confirmar que as páginas continuam abaixo de 2 segundos (RNF03). Se não, guardar o catálogo corrigido em memória enquanto não houver alterações. | Em aberto |
