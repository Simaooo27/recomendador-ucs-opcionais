# US36 — Plano das 6 opções de candidatura: requisitos funcionais

> **Como** candidato, **quero** montar e ordenar a minha lista de até 6 opções, com avisos, **para** submeter na DGES uma candidatura equilibrada.

| | |
|---|---|
| Épico | E4 — Plano de candidatura |
| Prioridade | Should · 5 story points · Sprint 4 |
| Requisitos de origem | RF43, RN11 |
| Atores | Aluno com sessão iniciada |
| Depende de | US31, US34, US35 |
| Artefactos | [Use case](use-case.md) · [BPMN](bpmn.md) · [Prompt](prompt.md) |

## 1. Âmbito

**Dentro:** juntar cursos ao plano, ordenar e retirar opções, ver cada opção com a nota e a situação, os avisos e as sugestões da mesma área, e o passo «Preparar a candidatura» no percurso.

**Fora:** submeter a candidatura (faz-se no site da DGES); quanto precisa nos exames, tendência, procura, combinações de exames, plano B e partilha, que são as US40 a US45 (também no Sprint 4) e acrescentam informação a este plano.

## 2. Requisitos funcionais da US36

| ID | Requisito |
|---|---|
| **RF43.1** | Na ficha de um curso, com sessão, o botão «Juntar ao plano» junta o curso ao fim da lista. Se já estiver no plano, a ficha diz «Já está no seu plano». |
| **RF43.2** | O plano tem no máximo 6 opções e nenhum curso repetido. Com 6, juntar outra dá «O plano já tem 6 opções: retire uma antes de juntar outra.». Um curso que não existe dá 404. |
| **RF43.3** | Em `/candidatura/`, cada opção mostra a posição («1.ª opção»), o curso, a instituição, a nota do aluno, o último colocado e a situação (US35), com os botões «Subir», «Descer» e «Retirar». |
| **RF43.4** | Os botões são formulários (POST com CSRF) e funcionam sem JavaScript. Depois de cada ação, a pessoa volta à página de onde veio (só caminhos do próprio site). |
| **RF43.5** | Avisos «Antes de submeter»: opções que não contam (falta prova ou abaixo do mínimo); nenhuma opção claramente acima do último colocado; a 1.ª opção é das mais fáceis e há opções mais difíceis depois; menos de 6 opções; opções com pré-requisitos. |
| **RF43.6** | Com notas indicadas, o plano sugere até 3 cursos da área da 1.ª opção, fora do plano, onde o aluno fica acima ou perto do último colocado. |
| **RF43.7** | Quem já escolheu um curso (US31) e tem o plano vazio vê um botão para o juntar como 1.ª opção. |
| **RF43.8** | O percurso da página inicial tem o 4.º passo, «Preparar a candidatura», que leva ao plano. |
| **RF43.9** | O plano mostra o aviso de que as contas são uma estimativa (RN11) e de que a candidatura se faz no site da DGES. |
| **RF43.10** | Os cursos do ensino privado não entram no plano: a ficha não tem «Juntar ao plano» e um pedido para os juntar é recusado com uma mensagem. Também não aparecem nas sugestões (RN12). *(27/10)* |

## 3. Mensagens

| Situação | Mensagem |
|---|---|
| Introdução | Junte até 6 cursos pela ordem em que os quer: na candidatura, fica colocado na primeira opção em que a sua nota chegue. A candidatura em si faz-se no site da DGES. |
| Plano vazio | Ainda não juntou nenhum curso. Abra a ficha de um curso no catálogo e carregue em «Juntar ao plano». |
| Juntado | {curso} juntado ao plano de candidatura. |
| Plano cheio | O plano já tem 6 opções: retire uma antes de juntar outra. |
| Ensino privado | Este curso é do ensino privado e não entra nas 6 opções do concurso nacional: a candidatura faz-se diretamente na instituição. |
| Opções que não contam | {n} opção(ões) não conta(m) para a colocação: veja o que falta em cada uma. |
| Nenhuma segura | Nenhuma opção está claramente acima do último colocado. Pense em juntar pelo menos um curso onde fique acima, para não arriscar ficar sem colocação. |
| Ordem | A 1.ª opção ({curso}) é das mais fáceis de entrar. Se ficar colocado nela, as opções seguintes já não contam: ponha primeiro os cursos de que mais gosta, mesmo que sejam mais difíceis. |
| Menos de 6 | Tem {n} opção(ões). Pode juntar mais {livres}: usar as 6 não prejudica as primeiras. |
| Pré-requisitos | Há opções com pré-requisitos (por exemplo, atestados médicos ou provas físicas): confirme-os no site da DGES. |

## 4. Dados

Tabela `planos_candidatura`, coluna `opcoes`: lista (JSON) das chaves dos cursos, pela ordem da candidatura. Um curso que deixe de estar no catálogo não aparece no plano. A linha é apagada com a conta (US17).

## 5. Critérios de aceitação e testes

| Critério da story (backlog) | Requisitos | Testes automáticos |
|---|---|---|
| Juntar cursos a partir da ficha; no máximo 6, sem repetidos. | RF43.1, RF43.2 | `test_no_maximo_6_opcoes_e_sem_repetidos`, `test_curso_inexistente_da_404`, `test_percurso_completo_notas_juntar_ordenar_e_retirar` (`tests/test_candidatura.py`) |
| Subir, descer e retirar opções (funciona sem JavaScript). | RF43.3, RF43.4 | `test_percurso_completo_notas_juntar_ordenar_e_retirar` (pedidos POST, como um navegador sem JavaScript); `test_voltar_so_aceita_caminhos_do_proprio_site` |
| Avisos: opções que não contam, nenhuma opção segura, a mais fácil em 1.º lugar, menos de 6 opções, pré-requisitos. | RF43.5 | `AvisosTests` (3 testes; o das opções que não contam e dos pré-requisitos foi acrescentado a 27/10) |
| Sugestões de cursos da mesma área onde a pessoa fica acima ou perto. | RF43.6 | `test_percurso_completo_notas_juntar_ordenar_e_retirar` («Curso Vizinho») |
| Passo «Preparar a candidatura» no percurso do início. | RF43.8 | `test_com_curso_o_proximo_passo_e_o_plano_de_candidatura` (`tests/test_apresentacao.py`) |
| (aviso de estimativa) | RF43.9 | `test_a_ficha_e_o_plano_dizem_que_a_nota_e_uma_estimativa` |
| (curso escolhido como 1.ª opção) | RF43.7 | `test_o_curso_escolhido_pode_ser_a_1a_opcao` (acrescentado a 27/10) |
| Cursos do ensino privado não entram (critério acrescentado a 27/10). | RF43.10 | `test_curso_privado_nao_entra_no_plano` |

## 6. Requisitos não funcionais aplicáveis

RNF02 (CSRF em todos os botões; o regresso só aceita caminhos do próprio site; SQL parametrizado), RNF06 (testes sem rede), RNF09 (uso de IA documentado), RNF10 (cada botão tem um rótulo com o nome do curso, por exemplo «Subir Ciência da Informação»), RNF11 (português de Portugal).

## 7. Decisões e questões em aberto

| # | Questão | Estado |
|---|---|---|
| 1 | O OptaBem não submete a candidatura: ajuda a prepará-la. | **Decidido** (PO, 23/10) |
| 2 | Se o docente achar o Sprint 4 demasiado cheio, saem primeiro as stories Could (US43 e US45), não a US36. | **Decidido** (PO, 27/10) |
