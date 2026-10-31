# US46 — Exportar os meus dados: requisitos funcionais

> **Como** utilizador, **quero** descarregar todos os dados que o OptaBem guarda sobre mim, **para** exercer o meu direito de acesso e de portabilidade.

| | |
|---|---|
| Épico | E1 — Conta e privacidade |
| Prioridade | Should · 2 story points · Sprint 4 |
| Requisitos de origem | RF17 (exportação), RNF01 |
| Atores | Aluno com sessão iniciada |
| Depende de | US02 (sessão), US17 («A minha conta») |
| Artefactos | [Use case](use-case.md) · [BPMN](bpmn.md) · [Prompt](prompt.md) |

## 1. Âmbito

**Dentro:** descarregar, num ficheiro JSON, todos os dados que o OptaBem guarda sobre o aluno.

**Fora:** importar o ficheiro noutra conta; exportar noutros formatos (CSV, PDF); exportação pelos administradores.

## 2. Requisitos funcionais da US46

A US17 tem o RF17.1 a RF17.6 (apagar a conta); a exportação continua a numeração.

| ID | Requisito |
|---|---|
| **RF17.7** | «A minha conta» tem a secção «Os meus dados», com a ligação para `/auth/conta/exportar`. A página diz o que vai no ficheiro. Só com sessão iniciada. |
| **RF17.8** | Descarregar exige a palavra-passe da conta (POST com CSRF). Palavra-passe errada ou vazia: mensagem de erro, sem ficheiro. |
| **RF17.9** | O ficheiro é JSON (`optabem-os-meus-dados-AAAA-MM-DD.json`), descarregado sem ficar em cache (`Cache-Control: no-store`). |
| **RF17.10** | O ficheiro tem: a conta (nome, email, datas de criação e confirmação, versão e data de aceitação da política de privacidade); as decisões do percurso, da mais antiga para a mais recente; o plano de candidatura (média, exames, opções com o nome do curso, se está partilhado); a conversa de orientação, com a autorização da US37 (se a pessoa deixou o assistente usar os exames e a média); os pedidos ao assistente por dia. Uma opção que saiu do catálogo fica, sem nome. |
| **RF17.11** | O ficheiro nunca tem o hash da palavra-passe, o valor interno da confirmação do email, o código da ligação de partilha nem dados de outros utilizadores. |

## 3. Mensagens

Os textos estão em [`app/texts.py`](../../app/texts.py).

| Situação | Mensagem |
|---|---|
| Secção em «A minha conta» | Os meus dados — Descarregue tudo o que o OptaBem guarda sobre si, num ficheiro que pode abrir noutro programa. |
| Sem palavra-passe no ficheiro | A palavra-passe não vai no ficheiro: o OptaBem não a guarda, só um resumo (hash) que não permite descobri-la. |
| Palavra-passe errada | A palavra-passe não está certa. O ficheiro não foi descarregado. |

## 4. Dados

Não há tabelas novas: a exportação só lê `users`, `decisoes`, `planos_candidatura`, `conversas_orientacao` e `pedidos_llm`, sempre pelo `user_id` de quem tem a sessão.

## 5. Critérios de aceitação e testes

| Critério da story (backlog) | Requisitos | Testes automáticos (`tests/test_exportar.py`) |
|---|---|---|
| Ficheiro JSON com a conta (sem a palavra-passe), as decisões do percurso, as notas e o plano de candidatura. | RF17.9, RF17.10, RF17.11 | `test_e_um_ficheiro_json_para_descarregar_e_sem_cache`, `test_tem_a_conta_sem_a_palavra_passe`, `test_tem_as_decisoes_as_notas_o_plano_e_a_conversa`, `test_diz_se_o_assistente_foi_autorizado_a_usar_as_notas`, `test_sem_dados_ainda_o_ficheiro_tem_as_secoes_vazias`, `test_um_curso_que_saiu_do_catalogo_fica_na_lista_sem_nome`, `test_as_decisoes_vao_da_mais_antiga_para_a_mais_recente`, `test_o_codigo_da_ligacao_de_partilha_nao_vai_no_ficheiro` |
| Pede a palavra-passe antes de descarregar. | RF17.8 | `test_palavra_passe_errada_nao_descarrega`, `test_sem_palavra_passe_nao_descarrega`, `test_sem_csrf_e_recusado`, `test_a_palavra_passe_de_outra_conta_nao_serve` |
| Nunca inclui dados de outros utilizadores. | RF17.11 | `test_so_tem_os_dados_de_quem_descarrega` |
| (página e acesso) | RF17.7 | `test_a_minha_conta_tem_a_ligacao`, `test_a_pagina_diz_o_que_vai_no_ficheiro_e_pede_a_palavra_passe`, `test_sem_sessao_vai_para_o_inicio_de_sessao`, `test_a_politica_explica_como_descarregar_os_dados` |

## 6. Requisitos não funcionais aplicáveis

RNF01 (direito de acesso e portabilidade; só dados do próprio), RNF02 (palavra-passe e CSRF; sem cache), RNF06 (testes sem rede), RNF09 (uso de IA documentado), RNF11 (português de Portugal).

## 7. Decisões e questões em aberto

| # | Questão | Estado |
|---|---|---|
| 1 | Pedir a palavra-passe outra vez, mesmo com sessão iniciada: protege um computador partilhado com a sessão aberta. | Decidido (critério da story) |
| 2 | O código da ligação de partilha fica de fora: quem o tivesse via o plano. O ficheiro diz só se está partilhado. | Decidido pelo Claude, aceite pelo PO |
| 3 | A autorização para o assistente usar as notas (US37) ainda não vai no ficheiro. | Por fazer depois de juntar a US37 e a US46 |
| 4 | A política de privacidade provisória passa a falar do direito de portabilidade. | Feito |
