# US31 — Escolher curso e linha do tempo do percurso: requisitos funcionais

> **Como** utilizador, **quero** escolher um dos cursos sugeridos (ou outro do catálogo) e ver as decisões que fui tomando, **para** acompanhar o meu percurso.

| | |
|---|---|
| Épico | E3 — Orientação com o assistente (E11 até 27/10) |
| Prioridade | Must · 5 story points · Sprint 2 (antecipada do Sprint 3 no Sprint Planning de 20/10) |
| Requisitos de origem | RF03, RF35, RF39, RN10 |
| Atores | Aluno (com sessão iniciada) |
| Artefactos | [Use case](use-case.md) · [BPMN](bpmn.md) · [Prompt](prompt.md) |
| Issue | #27 |

## 1. Âmbito

**Dentro:** escolher um curso a partir dos cursos sugeridos (US30) ou da página do catálogo (`/cursos/`); página de confirmação antes de registar; tabela de decisões; curso atual no perfil e na página inicial; linha do tempo das decisões; mudar de curso; apagar a conversa com o LLM depois de escolher.

**Fora:** escolher opcionais (US06 em diante); editar ou apagar decisões antigas; apagar a conta e os dados (US17); comparar cursos lado a lado (US05).

## 2. Requisitos funcionais da US31

| ID | Requisito |
|---|---|
| **RF39.1** | Cada ficha de curso sugerido (US30) e, com sessão iniciada, cada ficha da página `/cursos/` tem a ligação «Escolher este curso». Sem sessão, a ligação não aparece (nem na página de apresentação). |
| **RF39.2** | A ligação abre uma página de confirmação com a ficha do curso, o curso atual (se houver) e o aviso de que a conversa com o assistente vai ser apagada. **Abrir esta página não regista nada** (RN10): só o botão «Confirmar a escolha» (POST, com CSRF) o faz. |
| **RF39.3** | Só se escolhem cursos do catálogo: um identificador que não existe dá «página não encontrada» (404), na confirmação e no registo. |
| **RF35.1** | Cada escolha confirmada cria uma decisão com: a data e hora, o curso e a instituição (como estavam no catálogo nesse momento), os cursos que o assistente tinha sugerido nessa altura (lista vazia se não havia sugestões) e a origem («sugestão», se o curso estava entre os sugeridos; «catálogo», se não). |
| **RF03.1** | O curso do perfil é o da decisão mais recente. A página inicial mostra-o no passo «Escolher curso», com a ligação «Ver as minhas decisões», e o percurso fica concluído (desde 22/10 não há o passo «Escolher opcionais», por decisão dos PO). |
| **RF35.2** | A página `/percurso/` mostra a linha do tempo: as decisões da mais recente para a mais antiga, a mais recente marcada como «Curso atual», cada uma com a data, a origem e os cursos sugeridos (com o escolhido realçado). Cada aluno só vê as suas. |
| **RF39.4** | Mudar de curso: a partir da linha do tempo, nova conversa com o assistente ou procurar no catálogo. Escolher um curso diferente cria uma decisão nova; escolher o curso atual não cria e a página diz porquê. |
| **RF39.5** | Depois de escolher, a conversa com o LLM é apagada; ficam só os dados da decisão (ponto 15 dos requisitos, decisão do PO de 20/10). |

## 3. Mensagens

Os textos estão em [`app/texts.py`](../../app/texts.py), secção «Escolher curso e linha do tempo das decisões».

| Situação | Mensagem |
|---|---|
| Ligação na ficha | Escolher este curso |
| Confirmação | Confirme a sua escolha. Pode mudar de curso mais tarde: cada mudança fica registada. |
| Com curso atual | O seu curso atual é {curso}, {instituicao}. Ao confirmar, passa a ser este. |
| Aviso (ponto 15) | Ao confirmar, a sua conversa com o assistente é apagada. Ficam guardados só a data, os cursos sugeridos e o curso que escolheu. |
| Escolha registada | Escolha registada: {curso}, {instituicao}. |
| O mesmo curso | Esse curso já é o seu curso atual: não foi registada uma nova decisão. |
| Página inicial | Escolheu {curso}, {instituicao}. · Ver as minhas decisões |
| Sem decisões | Ainda não escolheu nenhum curso. |

## 4. Dados

Tabela nova `decisoes`: `user_id` (apagada com a conta), `curso_chave`, `curso`, `instituicao`, `origem` (`sugestao` ou `catalogo`), `sugeridos` (JSON com o identificador, o curso e a instituição de cada curso sugerido), `decidida_em` (UTC). O nome do curso e da instituição ficam guardados para a linha do tempo não mudar se o catálogo mudar. Para bases de dados já existentes basta correr `flask --app app init-db`.

## 5. Critérios de aceitação e testes

| Critério da story (backlog) | Requisitos | Testes automáticos (`tests/test_escolha.py`) |
|---|---|---|
| A escolha nunca é automática: o utilizador confirma (RN10). | RF39.1 a RF39.3 | `EscolhaConfirmadaTests` (3 testes), `AcessoTests` (3 testes, incluindo CSRF e cursos fora do catálogo), `CatalogoTests` (2 testes) |
| Depois de escolher, o curso e a instituição ficam no perfil (RF03). | RF03.1 | `CursoNoPerfilTests` (2 testes) |
| Cada decisão fica registada com data, opções sugeridas e opção escolhida (RF35). | RF35.1, RF39.5 | `DecisaoRegistadaTests` (5 testes, incluindo a conversa apagada) |
| Linha do tempo com as decisões, da mais recente para a mais antiga. | RF35.2 | `LinhaDoTempoTests` (2 testes) |
| O utilizador pode mudar de curso, o que cria uma nova decisão. | RF39.4 | `MudarDeCursoTests` (3 testes) |

## 6. Requisitos não funcionais aplicáveis

RNF01 (a conversa com o LLM é apagada depois da escolha; as decisões são apagadas com a conta), RNF02 (CSRF no botão de confirmar; SQL parametrizado), RNF06 (testes sem rede), RNF08 (commits `US31: ...`), RNF09 (uso de IA documentado), RNF10 (data em `<time>`; a decisão atual identificada por texto, não só pela cor), RNF11 (português de Portugal).

## 7. Decisões e questões em aberto

| # | Questão | Estado |
|---|---|---|
| 1 | Depois de escolher, a conversa com o LLM é apagada (ponto 15 dos requisitos). | **Decidido** pelo PO (20/10/2026) |
| 2 | O curso do perfil é a decisão mais recente, em vez de uma coluna nova na tabela `users`: assim não há duas fontes para a mesma informação. | Proposta do Claude, a confirmar pelo PO |
| 3 | A confirmação é uma página própria (GET mostra, POST regista), em vez de uma janela de confirmação no navegador: funciona sem JavaScript e torna a regra RN10 visível. | Proposta do Claude, a confirmar pelo PO |
| 4 | As decisões não podem ser apagadas nem editadas pelo aluno (o histórico é o objetivo). Apagar tudo fica com o apagamento da conta (US17, backlog). | Aceite para o MVP |
| 5 | A data da decisão é guardada e mostrada em UTC. No horário de verão, uma decisão tomada entre a meia-noite e a uma da manhã de Lisboa aparece com a data do dia anterior; no inverno, Lisboa está em UTC e não há diferença. Converter exigiria a biblioteca `tzdata` no Windows; não compensa para o MVP. | Aceite, por registar como dívida técnica |
