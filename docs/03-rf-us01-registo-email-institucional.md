# US01 — Registo com email institucional: requisitos funcionais

> **Como** aluno, **quero** registar-me com o meu email institucional, **para que** apenas alunos da instituição possam avaliar e o sistema seja fiável.

| | |
|---|---|
| Épico | E1 — Contas e perfis |
| Prioridade | Must · 3 story points · Sprint 1 |
| Requisito de origem | RF01 (ver [01-requisitos-funcionais-e-nao-funcionais.md](01-requisitos-funcionais-e-nao-funcionais.md)) |
| Atores | Aluno (primário), serviço de email (secundário) |
| Artefactos | [Use case](04-use-case-us01.md) · [BPMN](05-bpmn-us01.md) · [Prompt](../prompts/US01-registo-email-institucional.md) |

## 1. Âmbito

**Dentro:** formulário de registo, validação, criação de conta **inativa**, envio do email de confirmação e ativação da conta através da ligação recebida.

**Fora (outras stories):** iniciar e terminar sessão (US02); pseudonimização das avaliações (US09); recuperação de palavra-passe (sem story); limite de tentativas e captcha (futuro); escolha de curso e ano (RF03, sem story).

## 2. Requisitos funcionais da US01

| ID | Requisito |
|---|---|
| **RF01.1** | O sistema apresenta um formulário com: email institucional, palavra-passe, repetição da palavra-passe e uma caixa para aceitar a política de privacidade. |
| **RF01.2** | O email é normalizado antes de qualquer validação ou gravação: sem espaços nas pontas e em minúsculas. |
| **RF01.3** | Só são aceites emails válidos cujo domínio seja um dos **domínios institucionais configurados** (ou um subdomínio verdadeiro de um deles). Domínios parecidos (`iscap.ipp.pt.evil.com`, `evil-iscap.ipp.pt`) são rejeitados. |
| **RF01.4** | A palavra-passe tem entre 8 e 128 caracteres, com pelo menos uma letra e um número, e coincide com a repetição. |
| **RF01.5** | Sem aceitar a política de privacidade não há registo. A aceitação fica gravada com a versão da política e a data e hora (UTC). |
| **RF01.6** | A palavra-passe é guardada **apenas como hash** (scrypt, via Werkzeug). Nunca é gravada em texto, registada em logs nem devolvida ao navegador. |
| **RF01.7** | Um registo válido cria uma conta com perfil `aluno` e estado **inativo**. Uma conta inativa não pode iniciar sessão (a verificar na US02). |
| **RF01.8** | Após o registo, o sistema envia ao email indicado uma mensagem com uma ligação de confirmação, assinada e válida durante 24 horas. |
| **RF01.9** | Abrir uma ligação válida ativa a conta e grava a data de confirmação. Abrir a mesma ligação de novo não tem efeito e informa que a conta já está ativa. |
| **RF01.10** | Uma ligação adulterada, assinada por outra chave, de um utilizador inexistente ou já substituída é rejeitada (HTTP 400). Uma ligação fora do prazo é rejeitada com HTTP 410. Em ambos os casos a conta mantém-se inativa. |
| **RF01.11** | Se o email já pertence a uma conta **ativa**, o registo é rejeitado com mensagem clara. |
| **RF01.12** | Se o email já pertence a uma conta **por confirmar**, o novo pedido atualiza a palavra-passe, gera uma nova ligação, reenvia o email e **invalida as ligações anteriores**. |
| **RF01.13** | Se o email de confirmação não puder ser enviado, o utilizador vê uma mensagem de erro (HTTP 503) e a conta fica pendente. Um novo pedido de registo recomeça o processo. |
| **RF01.14** | Em caso de dados inválidos o formulário volta a ser mostrado com o email preenchido, **sem** palavras-passe, e uma mensagem junto de cada campo com erro (HTTP 422). |
| **RF01.15** | Todos os pedidos `POST` exigem token CSRF válido; sem ele a resposta é HTTP 400 e nada é gravado. |

## 3. Mensagens ao utilizador

| Situação | Mensagem |
|---|---|
| Email vazio | Indique o seu email institucional. |
| Email fora do domínio | Use o seu email institucional (terminado em @iscap.ipp.pt). |
| Palavra-passe vazia | Escolha uma palavra-passe. |
| Palavra-passe curta | A palavra-passe deve ter pelo menos 8 caracteres. |
| Palavra-passe longa | A palavra-passe não pode ter mais de 128 caracteres. |
| Sem letra ou sem número | A palavra-passe deve incluir pelo menos uma letra e um número. |
| Repetição diferente | As palavras-passe não coincidem. |
| Política não aceite | É necessário aceitar a política de privacidade para criar a conta. |
| Email já ativo | Já existe uma conta com este email. Se é a sua, inicie sessão. |
| Falha no envio | Não foi possível enviar o email de confirmação. Tente de novo dentro de alguns minutos. |
| Confirmação feita | O seu email foi confirmado e a conta está ativa. |
| Ligação inválida | Não foi possível confirmar o email com esta ligação. |
| Ligação expirada | Esta ligação já não é válida. |

## 4. Dados guardados

Tabela `users`: `id`, `email` (único, sem distinção de maiúsculas), `password_hash`, `role` (`aluno` ou `admin`), `is_active`, `confirmation_nonce`, `privacy_policy_version`, `privacy_accepted_at`, `created_at`, `confirmed_at`.

O `confirmation_nonce` muda a cada registo; faz parte do token e é o que invalida ligações antigas (RF01.12). A separação entre identidade e avaliações (`pseudo_id`, `MapaIdentidade`) é da US09.

## 5. Critérios de aceitação e testes

| Critério da story | Requisitos | Testes automáticos |
|---|---|---|
| Só são aceites emails do domínio institucional. | RF01.2, RF01.3 | `tests/test_validators.py` (`InstitutionalEmailTests`); `tests/test_registration.py` (`RejectedRegistrationTests`: email fora do domínio, domínio parecido) |
| A conta só fica ativa após confirmação por email. | RF01.7 a RF01.10, RF01.12 | `tests/test_confirmation.py` (todos); `tests/test_registration.py` (`SuccessfulRegistrationTests`: conta inativa, email com ligação; `DuplicateRegistrationTests`) |
| A palavra-passe é guardada com hash. | RF01.6 | `tests/test_registration.py` (`SuccessfulRegistrationTests.test_palavra_passe_guardada_com_hash`) |
| O registo exige aceitação explícita da política de privacidade. | RF01.5 | `tests/test_registration.py` (`RejectedRegistrationTests.test_exige_aceitacao_da_politica_de_privacidade`; `SuccessfulRegistrationTests.test_guarda_aceitacao_da_politica_com_versao_e_data`) |
| (Transversal) proteção CSRF e cabeçalhos | RF01.15, RNF02 | `tests/test_registration.py` (`CsrfTests`, `SecurityHeadersTests`) |

## 6. Requisitos não funcionais aplicáveis

RNF01 (privacidade: consentimento registado, só os dados necessários), RNF02 (hash, CSRF, SQL parametrizado), RNF04 (formulário responsivo), RNF06 (testes automáticos), RNF08 (commits `US01: ...`), RNF09 (uso de IA documentado), RNF10 (acessibilidade) e RNF11 (português de Portugal).

## 7. Decisões e questões em aberto

| # | Questão | Estado |
|---|---|---|
| 1 | **Domínio dos emails dos alunos.** O valor por omissão é `iscap.ipp.pt`, com subdomínios. Confirmar o domínio real dos alunos. Muda-se em `ALLOWED_EMAIL_DOMAINS` sem alterar código. | A confirmar pela equipa |
| 2 | Texto final da política de privacidade (a página atual é provisória). | A escrever |
| 3 | Regras da palavra-passe (8 a 128 caracteres, letra e número). | Proposta; PO a validar |
| 4 | Prazo da ligação: 24 horas. | Proposta; PO a validar |
| 5 | Dizer que um email já tem conta permite descobrir quem está registado. Optou-se pela clareza. Rever se a equipa preferir uma mensagem genérica. | Decisão a confirmar |
| 6 | Quem regista o email de outra pessoa não consegue ativá-la, mas pode bloquear temporariamente esse email até a pessoa se registar de novo (RF01.12 resolve). | Aceite |
