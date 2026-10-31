# Prompt — US48: recolha completa das licenciaturas

Pedido feito ao Claude (29/10/2026), seguindo as [regras de geração de código](../geral/02-regras-de-geracao-de-codigo.md).

---

**Contexto:** o código da recolha já existia (US04). O site da DGES recusa pedidos vindos do ambiente do Claude, por isso a recolha tinha de correr no computador de um elemento da equipa.

**Pedidos do PO:** «queres fazer o download dos cursos enquanto estudo?»; depois, «o download parou nos 1200 pq tive que sair, como faço para continuar?»; por fim, a mensagem final do `processar` (1699 cursos).

**O que o Claude fez:** deu os comandos para retomar; verificou os números contra páginas guardadas no computador do PO; correu os testes com o catálogo completo e corrigiu o que falhou na US37; mediu os tempos das páginas; escreveu o `dados/README.md` e esta pasta.

---

**Revisão humana:** pendente (PO: aceitar a story; Simão Almeida: rever o PR).
