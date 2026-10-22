# Prompt — US05: consultar e comparar cursos

Pedido feito ao Claude (2026-10-22), seguindo as [regras de geração de código](../geral/02-regras-de-geracao-de-codigo.md).

---

**Contexto:** Sprint Planning do Sprint 3 (22/10, decisão do PO): o Sprint 3 tem a US05 e a US17. Até à entrega de 05/11, os cursos são o centro do produto. A pesquisa no catálogo (14/10) e a página `/cursos/` (US30) já existiam.

**Pedido (resumo):** «vamos começar a tratar já dessa US para adiantarmos o máximo trabalho possível». O Claude implementou a US05 a partir dos critérios de aceitação do backlog:

1. Filtros por área, instituição e localidade.
2. Ficha de cada curso com descrição, saídas profissionais, vagas, nota do último colocado e ligação à fonte.
3. Comparação de até 3 cursos lado a lado.
4. Funciona sem sessão iniciada.
5. Testes sem rede, documentação em `docs/US05/` com a estrutura das outras stories, verificação no navegador em computador e telemóvel.

**Decisões do Claude a confirmar pelo PO:**

- Os filtros e a comparação funcionam por endereço (GET), sem JavaScript, para cumprir a regra de o site funcionar sem ele e para os endereços poderem ser partilhados.
- Sem filtros, o catálogo mostra os 30 cursos (antes mostrava uma amostra de 6).
- No telemóvel, a tabela da comparação desliza para o lado dentro da sua caixa, em vez de mudar de formato.
- As listas de escolha dos filtros (`select`) passam a ter o estilo das outras caixas. O campo de pesquisa já tinha sido corrigido no PR #36 (revisão de 22/10).

---

**Revisão humana:** pendente (Simão Almeida), no Pull Request da US05.
