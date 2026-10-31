# US47 — Recuperar a palavra-passe: requisitos funcionais

> **Como** utilizador que se esqueceu da palavra-passe, **quero** receber uma ligação para definir uma nova, **para** não perder a conta.

| | |
|---|---|
| Épico | E1 — Conta e privacidade |
| Prioridade | Should · 3 story points · Sprint 4 |
| Requisitos de origem | RF02 (recuperação) |
| Atores | Pessoa sem sessão que já tem conta |
| Depende de | US01 (conta e email), US02 (sessão) |
| Artefactos | [Use case](use-case.md) · [BPMN](bpmn.md) · [Prompt](prompt.md) |

## 1. Âmbito

**Dentro:** pedir a ligação por email, escolher a palavra-passe nova e terminar as sessões abertas.

**Fora:** mudar a palavra-passe com sessão iniciada (sabendo a atual); recuperar contas de administrador (são criadas no terminal ou na gestão, US03); limitar o número de pedidos por email.

## 2. Requisitos funcionais da US47

A US02 tem o RF02.1 a RF02.10 (iniciar e terminar sessão); a recuperação continua a numeração.

| ID | Requisito |
|---|---|
| **RF02.11** | O início de sessão tem a ligação «Esqueceu-se da palavra-passe?» para `/auth/recuperar`, que pede o email (POST com CSRF). Um email mal escrito é assinalado; o email é normalizado (minúsculas, sem espaços). |
| **RF02.12** | A resposta é a mesma («Veja o seu email»), com o mesmo endereço, quer haja quer não conta ativa com esse email, e também quando o envio falha. Só contas ativas recebem a ligação. A ligação nunca aparece na página nem no cookie de sessão. |
| **RF02.13** | A ligação é um token assinado, com sal diferente do da confirmação do email, que expira ao fim de 1 hora (`RESET_TOKEN_MAX_AGE_SECONDS`). Ligações adulteradas, expiradas ou de outro tipo dão uma página de erro com «Pedir outra ligação». |
| **RF02.14** | A ligação só serve uma vez: o token leva uma impressão da palavra-passe atual (um HMAC do hash, não o hash), que deixa de bater certo quando a palavra-passe muda. Duas ligações pedidas seguidas servem as duas até uma ser usada. |
| **RF02.15** | A palavra-passe nova segue as regras do registo (`password_errors`). Com erro, a ligação continua a servir. A página não fica em cache e não envia o endereço a outros sites. |
| **RF02.16** | Depois de mudar a palavra-passe, todas as sessões abertas dessa conta terminam no pedido seguinte (a sessão guarda a mesma impressão); as sessões de outras contas continuam. A pessoa volta ao início de sessão com «Palavra-passe mudada». |
| **RF02.17** | Cada conta recebe no máximo 3 emails de recuperação por hora (`RECUPERACAO_MAX_POR_HORA`; 0 = sem limite). Passado o limite, não se envia nada e a resposta é a mesma, para não revelar que a conta existe nem que o limite foi atingido. O limite é por conta: os pedidos para outra conta não contam. |

## 3. Mensagens

Os textos estão em [`app/texts.py`](../../app/texts.py).

| Situação | Mensagem |
|---|---|
| Depois de pedir | Se houver uma conta ativa com esse email, enviámos-lhe uma ligação para escolher uma palavra-passe nova. A ligação serve uma só vez e durante 1 hora. |
| Página da palavra-passe nova | Depois de a mudar, todas as sessões abertas da sua conta terminam, em qualquer dispositivo. |
| Mudada | Palavra-passe mudada. Inicie sessão com a palavra-passe nova. |
| Ligação usada ou inválida | A ligação não é válida ou já foi usada. Cada ligação só serve uma vez. |
| Ligação expirada | A ligação só serve durante 1 hora. Peça outra. |

## 4. Dados

Tabela `pedidos_recuperacao` (conta e data de cada email enviado), só para o limite do RF02.17: os registos com mais de 1 hora são apagados no envio seguinte e todos saem com a conta (US17). Não vai na exportação dos dados (US46), tal como o hash da palavra-passe, porque é uma proteção da conta. O token não fica guardado no servidor: é assinado com a `SECRET_KEY` e leva o identificador da conta e a impressão da palavra-passe. A sessão passa a guardar também essa impressão.

## 5. Critérios de aceitação e testes

| Critério da story (backlog) | Requisitos | Testes automáticos (`tests/test_recuperar_password.py`) |
|---|---|---|
| Ligação de uso único, que expira ao fim de 1 hora. | RF02.13, RF02.14, RF02.15 | `test_a_ligacao_abre_o_formulario_sem_cache`, `test_muda_a_palavra_passe`, `test_a_ligacao_so_serve_uma_vez`, `test_pedir_outra_ligacao_nao_invalida_a_primeira_enquanto_nao_for_usada`, `test_expira_ao_fim_de_1_hora`, `test_antes_de_1_hora_ainda_serve`, `test_ligacao_adulterada_nao_serve`, `test_o_token_de_confirmacao_nao_serve_para_recuperar`, `test_a_palavra_passe_nova_segue_as_regras_do_registo` |
| A mensagem é a mesma quer a conta exista quer não. | RF02.11, RF02.12 | `test_a_resposta_e_igual_com_e_sem_conta`, `test_conta_existente_recebe_o_email_com_a_ligacao`, `test_conta_por_confirmar_nao_recebe_ligacao`, `test_falha_no_envio_nao_revela_que_a_conta_existe`, `test_a_ligacao_nunca_aparece_na_pagina`, `test_maiusculas_e_espacos_no_email_tambem_servem`, `test_email_mal_escrito_e_assinalado` |
| Depois de mudar a palavra-passe, as sessões abertas terminam. | RF02.16 | `test_as_sessoes_abertas_noutros_dispositivos_terminam`, `test_a_sessao_do_proprio_navegador_tambem_termina`, `test_as_sessoes_de_outras_contas_continuam`, `test_a_sessao_nao_guarda_o_hash_da_palavra_passe` |
| Ninguém consegue usar o site para encher a caixa de correio de outra pessoa (acrescentado a 31/10). | RF02.17 | `test_no_maximo_3_emails_por_conta_por_hora`, `test_passado_o_limite_a_resposta_e_a_mesma`, `test_uma_hora_depois_volta_a_poder_pedir`, `test_o_limite_e_por_conta` |
| (segurança e acesso) | RF02.11, RF02.15 | `test_o_inicio_de_sessao_tem_a_ligacao`, os dois `test_sem_csrf_e_recusado` |

## 6. Requisitos não funcionais aplicáveis

RNF02 (tokens assinados, com validade e comparação em tempo constante; não revelar que emails têm conta; CSRF), RNF06 (testes sem rede, com o email simulado e o relógio substituído), RNF09 (uso de IA documentado), RNF11 (português de Portugal).

## 7. Decisões e questões em aberto

| # | Questão | Estado |
|---|---|---|
| 1 | O critério da story dizia que precisava de emails reais. A 29/10 o PO configurou o envio por SMTP (Gmail com palavra-passe de aplicação) e testou a confirmação e a recuperação com o seu email. | Resolvido (29/10) |
| 2 | Sem emails reais, a ligação aparece no terminal da aplicação, mas nunca na página: pelo túnel, isso deixaria mudar a palavra-passe de outra pessoa. | Decidido pelo Claude, aceite pelo PO |
| 3 | Quando esta story entrar, quem tiver uma sessão aberta é desligado uma vez (as sessões antigas não têm a impressão). | Aceite |
| 4 | Não havia limite de pedidos por email: alguém podia mandar muitos emails de recuperação para o mesmo endereço. A 31/10 passou a haver um limite de 3 por conta e por hora (RF02.17). | Resolvido (31/10) |
