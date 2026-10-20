# US30 — Sugestão de 2 a 3 cursos no fim da conversa: requisitos funcionais

> **Como** pessoa indecisa, **quero** que a conversa termine com 2 a 3 cursos do catálogo, cada um com a explicação de porque combina comigo, **para** saber por onde começar.

| | |
|---|---|
| Épico | E11 — Orientação de curso |
| Prioridade | Must · 3 story points · Sprint 2 |
| Requisitos de origem | RF37, RF38, RNF12, RN09, RN10 |
| Atores | Aluno (com sessão iniciada), LLM (fornecedor externo) |
| Depende de | US29 (conversa de orientação); spike do LLM (validação contra o catálogo, LLM falso) |
| Artefactos | [Use case](use-case.md) · [BPMN](bpmn.md) · [Prompt](prompt.md) |

## 1. Âmbito

**Dentro:** mostrar os cursos sugeridos no fim da conversa, com os dados do catálogo e a explicação do LLM; pedir as sugestões antes das 6 respostas («Ver sugestões já»); o caso de sobrarem menos de 2 cursos (continuar a conversa ou procurar no catálogo); a página `/cursos/` com a pesquisa no catálogo, para quem tem sessão iniciada.

**Fora:** escolher um curso e registá-lo no percurso (US31); filtros, ficha do curso e comparação lado a lado (US05); sugerir unidades curriculares.

## 2. Requisitos funcionais da US30

| ID | Requisito |
|---|---|
| **RF37.1** | A sugestão aparece quando o LLM responde com o formato «sugestao»: por decisão dele (já tem informação suficiente), ao fim de 6 respostas (as instruções passam a exigi-la) ou a pedido do aluno (RF37.2). |
| **RF37.2** | Depois da primeira resposta, e enquanto a conversa decorre, há um botão «Ver sugestões já». O pedido fica na conversa como mensagem do aluno e as instruções exigem a sugestão. Se o LLM falhar, «Tentar de novo» volta a pedir as sugestões. |
| **RF37.3** | Só aparecem cursos do catálogo, sem repetidos e no máximo 3 (RN09). Os outros são descartados e ficam registados na sugestão guardada (`descartados`), sem chegar ao ecrã. A validação repete-se ao mostrar a página: um curso que saia do catálogo depois de sugerido deixa de aparecer. |
| **RF37.4** | Cada curso mostra os dados do catálogo — área, curso, instituição, localidade, vagas de 2026, nota do último colocado (1.ª fase de 2025) e ligação à página da DGES — e a explicação do LLM («Porque combina consigo»), mostrada como texto e nunca como HTML. |
| **RF37.5** | Com 2 ou 3 cursos, a página diz que nenhum curso fica escolhido e que a escolha vem a seguir (RN10). Não há botão de escolher: é a US31. |
| **RF37.6** | Com menos de 2 cursos, a página diz que o assistente não encontrou cursos suficientes e propõe «Continuar a conversa» e «Procurar no catálogo». Os cursos que sobraram continuam a aparecer. |
| **RF37.7** | «Continuar a conversa» mantém as mensagens, apaga a sugestão e volta a mostrar a caixa de resposta, sem chamar o LLM. Se já houve 6 respostas, a resposta seguinte volta a exigir a sugestão. Com 2 ou mais cursos, o botão não existe e o pedido é ignorado. |
| **RF37.8** | «Procurar no catálogo» leva a `/cursos/`: a mesma pesquisa da página de apresentação, sem JavaScript, com ou sem sessão iniciada, e uma ligação de volta à conversa. |
| **RF37.9** | O percurso da página inicial só passa a «Escolher curso» quando a conversa termina com pelo menos 2 cursos. O botão do passo passa a «Ver os cursos sugeridos». |
| **RNF12** | Mantém-se a US29: o LLM só recebe o texto da conversa e o catálogo. O pedido «Ver sugestões já» é um texto fixo da aplicação. |

## 3. Mensagens

Os textos estão em [`app/texts.py`](../../app/texts.py), secção «Conversa de orientação».

| Situação | Mensagem |
|---|---|
| Botão para pedir antes do fim | Ver sugestões já |
| Ajuda do botão | Se já disse o suficiente, o assistente sugere cursos agora, sem mais perguntas. |
| Pedido na conversa (enviado ao LLM) | Prefiro ver já as sugestões de curso. |
| Título | Cursos sugeridos para si |
| Explicação de cada curso | Porque combina consigo |
| 2 ou 3 cursos (RN10) | Nenhum curso fica escolhido por si. Compare-os com calma: em breve vai poder escolher um destes, ou outro do catálogo. |
| Menos de 2 cursos | O assistente não encontrou cursos suficientes no catálogo que combinem com as suas respostas. Pode continuar a conversa, para lhe dar mais pistas, ou procurar no catálogo. |
| Botões | Continuar a conversa · Procurar no catálogo |

## 4. Dados

Sem tabelas novas. A sugestão continua na coluna `sugestao` de `conversas_orientacao` (US29), em JSON: `texto`, `cursos` (identificador e explicação de cada curso aceite) e `descartados` (identificadores devolvidos pelo LLM que não estão no catálogo). Os dados dos cursos não são copiados: vêm do catálogo quando a página é mostrada.

## 5. Critérios de aceitação e testes

| Critério da story (backlog) | Requisitos | Testes automáticos (`tests/test_sugestoes.py`) |
|---|---|---|
| A sugestão aparece quando o LLM tem informação suficiente ou ao fim de 6 respostas; a pessoa pode pedi-la antes («Ver sugestões já»). | RF37.1, RF37.2 | `VerSugestoesJaTests` (4 testes); `MostrarSugestoesTests.test_a_conversa_termina_sem_caixa_de_resposta`; `test_no_maximo_seis_perguntas` em `tests/test_conversa.py` |
| Só aparecem cursos do catálogo; os outros são descartados (RN09). Se sobrarem menos de 2, a página diz isso e propõe continuar a conversa ou ver o catálogo. | RF37.3, RF37.6 a RF37.8 | `SoCursosDoCatalogoTests` (2 testes); `PoucasSugestoesTests` (7 testes) |
| Cada curso mostra os dados do catálogo (instituição, localidade, vagas, nota do último colocado, ligação à DGES) e a explicação do LLM. | RF37.4 | `MostrarSugestoesTests` (4 testes, incluindo o máximo de 3 cursos e a explicação como texto) |
| Nenhum curso é atribuído automaticamente: a escolha é feita na US31 (RN10). | RF37.5, RF37.9 | `NenhumCursoEscolhidoTests` (2 testes) |
| Os testes usam o LLM falso, incluindo respostas com cursos inventados. | — | Todos (`LLMFalso`, `LLMQueFalha`); cursos inventados em `SoCursosDoCatalogoTests` e `PoucasSugestoesTests` |

## 6. Requisitos não funcionais aplicáveis

RNF02 (CSRF em «Ver sugestões já» e «Continuar a conversa»; explicação do LLM escapada), RNF06 (testes sem rede), RNF08 (commits `US30: ...`), RNF09 (uso de IA documentado), RNF10 (ajuda do botão ligada por `aria-describedby`; aviso de poucos cursos com `role="status"`), RNF11 (português de Portugal), RNF12 (o pedido de sugestões não acrescenta dados pessoais).

## 7. Decisões e questões em aberto

| # | Questão | Estado |
|---|---|---|
| 1 | A sugestão termina a conversa da US29 (decisão do PO de 14/10, issue #15). | **Decidido** |
| 2 | «Procurar no catálogo» precisava de uma página para quem tem sessão iniciada: foi criada `/cursos/`, só com a pesquisa que já existia. Filtros, ficha e comparação continuam na US05. | Proposta do Claude, **a confirmar pelo PO** |
| 3 | O percurso só passa a «Escolher curso» com pelo menos 2 cursos sugeridos. | Proposta do Claude, **a confirmar pelo PO** |
| 4 | «Continuar a conversa» só existe com menos de 2 cursos; com 2 ou mais, só «Recomeçar». | Proposta do Claude, **a confirmar pelo PO** |
| 5 | Se o LLM fizer outra pergunta quando a sugestão foi pedida, aparece «Tentar de novo» (RF36.4 da US29). | **Resolvido** a 20/10 (correção da US29) |
| 6 | A qualidade das explicações depende das descrições do catálogo (ponto 12 dos requisitos gerais) e só se vê com o Gemini real. | Por verificar no teste do PO |
