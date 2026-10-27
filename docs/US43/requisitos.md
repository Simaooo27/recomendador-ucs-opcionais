# US43 — Partilhar o plano: requisitos funcionais

> **Como** candidato, **quero** partilhar o meu plano com quem me ajuda a decidir (pais, explicador), com uma ligação só de leitura, **para** pedir opinião sem dar a minha palavra-passe.

| | |
|---|---|
| Épico | E4 — Plano de candidatura |
| Prioridade | Could · 3 story points · Sprint 4 |
| Requisitos de origem | RF47, RF17 |
| Atores | Aluno com sessão (partilha); quem recebe a ligação, sem conta (vê) |
| Depende de | US36 (plano) |
| Artefactos | [Use case](use-case.md) · [BPMN](bpmn.md) · [Prompt](prompt.md) |

## 1. Âmbito

**Dentro:** criar e desligar uma ligação só de leitura para o plano, e a página que a mostra.

**Fora:** comentários de quem recebe; partilhar com contas do OptaBem; escolher que opções partilhar.

## 2. Requisitos funcionais da US43

| ID | Requisito |
|---|---|
| **RF47.1** | No plano, «Criar ligação de partilha» gera um código aleatório (pelo menos 16 bytes) e mostra a ligação completa, com o endereço por onde o site foi aberto (também pelo túnel). Se já houver um código, reutiliza-o. |
| **RF47.2** | `/candidatura/p/<código>` abre sem sessão e mostra o primeiro nome, as opções por ordem, a nota de candidatura e a situação de cada uma, com o aviso de estimativa. |
| **RF47.3** | A página partilhada nunca mostra o email, a média do secundário nem as notas dos exames. |
| **RF47.4** | «Deixar de partilhar» apaga o código; a ligação antiga passa a dar 404. Um código errado também dá 404. |
| **RF47.5** | A página partilhada pede para não ser indexada (`noindex`), não fica em cache (`no-store`) e não envia o endereço a outros sites (`Referrer-Policy: no-referrer`). |
| **RF47.6** | Criar e desligar a ligação são pedidos POST com CSRF. O código sai com a conta (US17). |

## 3. Mensagens

Os textos estão em [`app/texts.py`](../../app/texts.py).

| Situação | Mensagem |
|---|---|
| Explicação | Crie uma ligação para mostrar o plano a quem o ajuda a decidir (pais, explicador, um colega). Quem a abrir vê o seu primeiro nome, as opções, a nota de candidatura e a situação em cada uma. Não vê o seu email, a média nem as notas dos exames. |
| Criada | Ligação de partilha criada. |
| Desligada | A ligação deixou de funcionar. |
| Título da página | Plano de candidatura de {nome} |
| Convite | Também está a escolher curso? Experimente o OptaBem. |

## 4. Dados

Coluna `partilha` (texto único, vazio = não partilhado) na tabela `planos_candidatura`, apagada com a conta.

## 5. Critérios de aceitação e testes

| Critério da story (backlog) | Requisitos | Testes automáticos |
|---|---|---|
| Ligação com um código aleatório; quem a tem vê o plano sem iniciar sessão. | RF47.1, RF47.2 | `test_partilhar_mostra_o_plano_sem_dados_pessoais_e_desligar_invalida`; `test_ligacao_de_partilha_tem_o_endereco_do_tunel` |
| Mostra o primeiro nome, as opções, a nota de candidatura e a situação; nunca o email, a média nem os exames. | RF47.2, RF47.3 | `test_partilhar_mostra_o_plano_sem_dados_pessoais_e_desligar_invalida` |
| «Deixar de partilhar» invalida a ligação de imediato. | RF47.4 | `test_partilhar_mostra_o_plano_sem_dados_pessoais_e_desligar_invalida`; `test_codigo_de_partilha_errado_da_404` |
| A página não é indexada pelos motores de pesquisa. | RF47.5 | `test_partilhar_mostra_o_plano_sem_dados_pessoais_e_desligar_invalida` (`noindex` e `no-referrer`) |
| (segurança) | RF47.6 | `test_partilhar_exige_csrf` |

## 6. Requisitos não funcionais aplicáveis

RNF01 (a pessoa escolhe partilhar e pode desligar; só os dados necessários), RNF02 (código aleatório, CSRF, sem cache nem referrer), RNF06 (testes sem rede), RNF09 (uso de IA documentado), RNF11 (português de Portugal).

## 7. Decisões e questões em aberto

| # | Questão | Estado |
|---|---|---|
| 1 | Qualquer pessoa com a ligação vê o plano: é a mesma lógica de um documento partilhado por ligação. | Aceite (dito na página) |
| 2 | A política de privacidade provisória foi atualizada com a partilha (23/10). | Feito |
