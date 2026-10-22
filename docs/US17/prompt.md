# Prompt — US17: apagar a minha conta

Pedido feito ao Claude (2026-10-22), seguindo as [regras de geração de código](../geral/02-regras-de-geracao-de-codigo.md).

---

**Contexto:** a US17 subiu para o Sprint 3 no Sprint Planning de 22/10 («exportar e apagar todos os meus dados»). Antes de começar, o PO perguntou se era absolutamente crucial. O Claude respondeu que não. Mesmo assim, a política de privacidade já prometia estes direitos, o curso é de Ciências da Informação e o ponto 11 dos requisitos recomendava pelo menos o apagamento. Por isso, propôs uma versão mínima.

**Pedido (resumo):** «podemos fazer isso do apagar conta, penso que seja mais inteligente que um full on exportar dados». O Claude implementou:

1. A ligação «Apagar a minha conta e todos os meus dados» no fim da página inicial.
2. Uma página que diz o que é apagado e pede a palavra-passe como confirmação.
3. O apagamento da conta, da conversa, das decisões e do registo de pedidos ao LLM, com o fim da sessão e um aviso.
4. A política de privacidade provisória corrigida (deixa de prometer a exportação).
5. Testes sem rede e documentação em `docs/US17/`.

**Decisões do Claude a confirmar pelo PO:** a confirmação é a palavra-passe (e não uma caixa «tenho a certeza»); o registo de pedidos ao LLM também é apagado.

**No mesmo PR:** a correção do guia do túnel (`06-aceder-noutro-dispositivo.md`, secção 4.1). O exemplo do `.env` tinha comentários na mesma linha, que o `arrancar.ps1` lê como parte do valor.

---

**Revisão humana:** pendente (Simão Almeida), no Pull Request da US17.
