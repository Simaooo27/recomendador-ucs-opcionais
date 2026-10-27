# Prompt — US33: condições de acesso na ficha do curso

Pedido feito ao Claude (23/10/2026), seguindo as [regras de geração de código](../geral/02-regras-de-geracao-de-codigo.md).

---

**Contexto:** o PO decidiu que o plano de candidatura ao concurso nacional ocupa o lugar das opcionais e pediu para ver a ideia em código antes de reescrever o backlog.

**Pedido (resumo):** codificar primeiro o plano de candidatura (6 opções), a começar pelo que é preciso para entrar em cada curso, com os dados da DGES que a recolha da US04 já descarrega.

**Decisões do Claude, aceites pelo PO:**

- As condições são lidas das páginas da DGES já guardadas, na mesma recolha da US04.
- As provas aparecem pelo nome, com os conjuntos alternativos («Basta um destes conjuntos»).
- «Matemática» e «Matemática A» contam como o mesmo exame (a confirmar pela equipa na DGES).

**Documentação desta pasta e testes de 27/10:** escritos pelo Claude a partir do código do PR #44. Ao escrever a documentação, faltavam testes para a leitura das provas nas páginas da DGES e para a ficha sem sessão; foram acrescentados (`CondicoesDeAcessoTests` e `test_sem_sessao_a_ficha_mostra_as_condicoes_e_pede_para_entrar`).

---

**Revisão humana:** pendente (Simão Almeida).
