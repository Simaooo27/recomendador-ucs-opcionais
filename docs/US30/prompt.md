# Prompt — US30: sugestão de 2 a 3 cursos no fim da conversa

Pedido feito ao Claude (2026-10-20), seguindo as [regras de geração de código](../geral/02-regras-de-geracao-de-codigo.md).

---

**Contexto:** o Simão partilhou o quadro do Notion e o repositório e pediu ajuda para continuar o projeto. Antes de começar, o Claude reparou que os PR #18 (replaneamento de 14/10) e #19 (US29) tinham sido aceites para ramos intermédios e não para o `main`, e abriu o PR #20 para os levar ao `main`. A story seguinte no plano é a US30, que fecha o Sprint 2.

**Pedido (resumo):** «ajuda-me a continuar a desenvolver o meu projeto». O Claude propôs e implementou a US30 a partir dos critérios de aceitação do backlog:

1. Mostrar os cursos sugeridos no fim da conversa, com os dados do catálogo (instituição, localidade, vagas, nota do último colocado, ligação à DGES) e a explicação do LLM.
2. Botão «Ver sugestões já», para pedir a sugestão antes das 6 respostas.
3. Só cursos do catálogo (RN09); com menos de 2, dizer isso e propor continuar a conversa ou ver o catálogo.
4. Nenhum curso escolhido automaticamente (RN10): a escolha fica para a US31.
5. Testes com o LLM falso, incluindo cursos inventados; documentação em `docs/US30/` com a estrutura das outras stories; ramo e PR próprios.

**Decisões do Claude a confirmar pelo PO:**

- «Procurar no catálogo» precisava de uma página: quem tem sessão iniciada não vê a apresentação (`/`). Foi criada `/cursos/`, só com a pesquisa que já existia (sem filtros, ficha nem comparação, que continuam na US05).
- O percurso só passa a «Escolher curso» com pelo menos 2 cursos sugeridos; o botão desse passo passou de «Continuar a conversa» para «Ver os cursos sugeridos».
- «Continuar a conversa» só existe quando há menos de 2 cursos.

---

**Revisão humana:** pendente (Simão Almeida e Duarte Eusébio), no Pull Request da US30.
