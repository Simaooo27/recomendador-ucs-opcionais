# Prompt — US47: recuperar a palavra-passe

Pedido feito ao Claude (29/10/2026), seguindo as [regras de geração de código](../geral/02-regras-de-geracao-de-codigo.md).

---

**Contexto:** a 29/10, o PO pediu ao Claude para fazer o código que faltava no product backlog, sem mexer no GitHub enquanto o Simão podia estar a trabalhar lá. A US47 estava no Backlog desde 27/10, para a parte do RF02 que não tinha story, com a nota «precisa de o site enviar emails reais».

**Pedido (resumo):** implementar as stories do backlog que ainda não tinham código (US37, US38, US39, US46 e US47), uma por ramo, com testes para cada critério de aceitação.

**Decisões do Claude, aceites pelo PO:**

- Uso único sem guardar o token no servidor: o token leva uma impressão da palavra-passe atual, que muda quando a palavra-passe muda.
- A mesma impressão na sessão faz terminar todas as sessões abertas quando a palavra-passe muda. Efeito aceite: quando a story entrar, as sessões abertas terminam uma vez.
- A ligação nunca aparece na página, mesmo em desenvolvimento (ao contrário da confirmação do email): pelo túnel, dava para mudar a palavra-passe de outra pessoa.
- As regras da palavra-passe passaram para uma função única (`password_errors`), usada no registo e na recuperação.

**29/10:** o PO configurou o envio de emails por SMTP (Gmail) e testou a confirmação da conta e a recuperação com o seu email; depois pôs a story no Sprint 4 como «Feito». A documentação desta pasta foi escrita pelo Claude a partir do código.

---

**Revisão humana:** pendente (Simão Almeida).
