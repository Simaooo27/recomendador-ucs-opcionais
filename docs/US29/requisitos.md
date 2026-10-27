# US29 — Conversa de orientação com o LLM: requisitos funcionais

> **Como** pessoa indecisa, **quero** conversar com um assistente que me vai fazendo perguntas sobre os meus interesses, **para** perceber o que procuro num curso sem preencher um questionário fixo.

| | |
|---|---|
| Épico | E3 — Orientação com o assistente (E11 até 27/10) |
| Prioridade | Must · 5 story points · Sprint 2 |
| Requisitos de origem | RF36, RNF12 |
| Atores | Aluno (com sessão iniciada), LLM (fornecedor externo) |
| Artefactos | [Use case](use-case.md) · [BPMN](bpmn.md) · [Prompt](prompt.md) |

## 1. Âmbito

**Dentro:** página da conversa para alunos com sessão iniciada; perguntas feitas pelo LLM, uma de cada vez, no máximo 6; resposta escrita pelo aluno; proteção de dados pessoais; mensagens de erro e «Tentar de novo»; recomeçar; ligação a partir da linha do tempo.

**Fora:** mostrar os cursos sugeridos (US30); escolher um curso e registar a decisão (US31); conversa sem sessão iniciada; mostrar as respostas à medida que o LLM as escreve (*streaming*).

## 2. Requisitos funcionais da US29

| ID | Requisito |
|---|---|
| **RF36.1** | A página `/orientacao/` só abre com sessão de aluno; sem sessão, leva ao início de sessão. |
| **RF36.2** | Abrir a página nunca chama o LLM. A conversa começa com o botão «Começar a conversa» (para não gastar o limite diário, partilhado por todos). |
| **RF36.3** | As perguntas são do LLM, uma de cada vez. Cada pedido leva as instruções (`app/orientacao/instrucoes.md`, com o catálogo) e a conversa toda até ali. |
| **RF36.4** | Ao fim de 6 respostas do aluno, as instruções passam a exigir a sugestão. Quando o LLM sugere, a conversa termina e deixa de haver caixa de resposta. O limite é garantido pela aplicação: se o LLM fizer outra pergunta, é tratado como resposta fora do formato (RF36.9) e nunca aparece uma 7.ª pergunta. *(20/10: antes dependia de o LLM obedecer.)* |
| **RF36.5** | A resposta é obrigatória e tem até 500 caracteres. Se não for válida, a página mostra o erro junto da caixa e mantém o texto escrito. |
| **RF36.6** | O texto do LLM é mostrado como texto, nunca como HTML. |
| **RF36.7** | O aluno pode recomeçar a conversa: a conversa guardada é apagada. |
| **RF36.8** | A conversa fica guardada no servidor (tabela `conversas_orientacao`), uma por aluno; cada aluno só vê a sua. |
| **RF36.9** | Se o LLM falhar, não responder em 15 segundos ou responder fora do formato, a página mostra uma mensagem clara, sem detalhes técnicos. A resposta do aluno fica guardada e aparece «Tentar de novo». O limite de pedidos atingido tem uma mensagem própria. O detalhe técnico fica no registo da aplicação. |
| **RF36.10** | Na página inicial, o passo atual da linha do tempo tem o botão «Começar a conversa»; quando a conversa termina com sugestões, o percurso passa a «Escolher curso» e o botão passa a «Ver os cursos sugeridos». |
| **RNF12** | O LLM nunca recebe o email, o nome ou o identificador da conta. Emails e números longos escritos pelo aluno são apagados antes de enviar e antes de guardar. A página avisa para não escrever dados pessoais e que as respostas vão para um serviço externo. |

## 3. Mensagens

Os textos estão em [`app/texts.py`](../../app/texts.py), secção «Conversa de orientação».

| Situação | Mensagem |
|---|---|
| Aviso (sempre visível) | Não escreva dados pessoais, como o nome, o email ou o telefone. As suas respostas são enviadas a um serviço externo de inteligência artificial, sem o seu email nem o seu nome. |
| Idade | Por agora, esta conversa destina-se a maiores de 18 anos. *(ponto 14 dos requisitos, decidido a 20/10)* |
| Resposta vazia | Escreva uma resposta antes de enviar. |
| Resposta longa | A resposta pode ter até 500 caracteres. Encurte-a um pouco. |
| LLM falhou | Não foi possível falar com o assistente. A sua conversa está guardada: tente de novo. |
| Limite atingido | O assistente está com muitos pedidos neste momento. Tente de novo dentro de um minuto; se continuar, o limite diário foi atingido e volta a funcionar amanhã. |
| Conversa terminada | O assistente já tem informação suficiente. As sugestões de curso vão aparecer aqui em breve. *(substituída pela US30)* |

## 4. Dados

Tabela nova `conversas_orientacao`: `user_id` (chave; apagada com a conta), `mensagens` (JSON com o papel e o texto de cada mensagem, já sem emails nem números longos), `sugestao` (JSON da sugestão final, para a US30), `atualizada_em`. Para bases de dados já existentes basta correr `flask --app app init-db`.

## 5. Critérios de aceitação e testes

| Critério da story (backlog) | Requisitos | Testes automáticos (`tests/test_conversa.py`) |
|---|---|---|
| As perguntas não são fixas: o LLM faz uma de cada vez, a partir das respostas anteriores, no máximo 6. | RF36.2 a RF36.6 | `ConversaConduzidaPeloLLMTests` (7 testes, incluindo `test_o_limite_nao_depende_de_o_llm_obedecer`) |
| A página avisa para não escrever dados pessoais; emails e números longos são apagados antes de enviar, e o LLM nunca recebe email, nome ou identificadores da conta (RNF12). | RNF12, RF36.8 | `DadosPessoaisTests` (4 testes); `AcessoTests.test_abrir_a_pagina_nao_chama_o_llm` |
| Disponível com sessão iniciada. | RF36.1 | `AcessoTests` (4 testes, incluindo CSRF) |
| Se o LLM falhar, atingir o limite ou demorar mais de 15 s, aparece uma mensagem clara e a pessoa pode tentar de novo sem perder a conversa. | RF36.9 | `FalhasDoLLMTests` (5 testes); o tempo limite de 15 s é `LLM_TIMEOUT` (`tests/test_llm.py`) |
| A pessoa pode recomeçar a conversa. | RF36.7 | `RecomecarTests` |
| Os testes usam o LLM falso e correm sem rede. | RNF06 | todos; a base dos testes força `LLM_BACKEND=falso` |
| *(da linha do tempo)* | RF36.10 | `AcessoTests.test_a_pagina_inicial_leva_a_conversa`, `PercursoTests` |

## 6. Requisitos não funcionais aplicáveis

RNF02 (CSRF em todos os botões, texto do LLM escapado), RNF06 (testes sem rede), RNF08 (commits `US29: ...`), RNF09 (uso de IA documentado), RNF10 (caixa de resposta com etiqueta, erro e ajuda ligados por `aria-describedby`; autor de cada mensagem escrito, não só por cor), RNF11 (português de Portugal), RNF12.

## 7. Decisões e questões em aberto

| # | Questão | Estado |
|---|---|---|
| 1 | Sem perguntas fixas: o LLM conduz a conversa (issue #15). | **Decidido** pelo PO (14/10/2026) |
| 2 | Idade mínima: os termos do Gemini excluem menores de 18. A página só avisa; não há verificação. | **Decidido** a 20/10 (ponto 14 dos requisitos, opção a): protótipo usado pela equipa e na demonstração |
| 3 | Guardar a conversa no servidor enquanto decorre; apagar ao recomeçar. Falta decidir se se apaga depois da escolha de curso (US31). | Parcial (ponto 15 dos requisitos) |
| 4 | Nomes próprios escritos no meio do texto não são detetados (só emails e números). | Aceite, com aviso na página |
| 5 | Se o LLM continuar a perguntar depois das 6 respostas (não cumprir a instrução), a pergunta é recusada e aparece «Tentar de novo» (RF36.4). | **Resolvido** a 20/10 (encontrado na revisão) |
| 6 | Sem *streaming*: a resposta aparece de uma vez, com o botão em «a enviar» enquanto se espera. | Aceite para o MVP |
