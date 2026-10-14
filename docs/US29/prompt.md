# Prompt — US29: conversa de orientação com o LLM

Pedidos feitos ao Claude (2026-10-14), seguindo as [regras de geração de código](../geral/02-regras-de-geracao-de-codigo.md).

---

**Contexto:** depois do spike do LLM (PR #17), o PO perguntou que sentido fazia ter o LLM ligado se não o podia experimentar. O Claude reconheceu que o spike só provava a viabilidade e propôs duas opções: uma conversa no terminal ou fazer já a US29.

**Decisão do PO:** «acho que faz sentido esta parte do LLM ser já, considerando que o utilizador tem que responder ao questionário feito pelo LLM para depois a aplicação ter informação suficiente para fazer a ligação entre gostos e cursos/UCs.»

**Pedido (resumo):** implementa a US29 sobre a base do spike:

1. Página da conversa para alunos com sessão iniciada; o LLM faz as perguntas, uma de cada vez, no máximo 6.
2. RNF12: aviso de privacidade na página; o LLM nunca recebe dados da conta; emails e números apagados antes de enviar.
3. Mensagens de erro claras e «Tentar de novo» sem perder a conversa; recomeçar.
4. Uma story por branch e por PR, testes a passar sem rede, documentação em `docs/US29/` com a estrutura das outras stories. Verificar com testes e não com capturas de ecrã.

**Nota do Claude ao PO:** por agora o LLM só liga gostos a **cursos**; as UCs ainda não estão no catálogo (entram com a US06).

---

**Revisão humana:** pendente (Simão Almeida), no Pull Request da US29.
