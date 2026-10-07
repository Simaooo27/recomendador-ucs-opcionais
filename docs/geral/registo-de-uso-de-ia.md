# Registo de uso de IA

Obrigatório (RNF09, secção 9 de [02-regras-de-geracao-de-codigo.md](02-regras-de-geracao-de-codigo.md)). Uma linha por sessão relevante. Este registo alimenta o relatório.

| Data | Quem | Ferramenta | Pedido (resumo) | O que foi gerado | Como foi validado | Revisto por | Resultado |
|---|---|---|---|---|---|---|---|
| 2026-10-01 | (preencher) | Claude | Documentos de requisitos, regras de geração de código, use case, BPMN e prompt da US01; implementação da US01 e testes | Documentos `docs/01` a `docs/05`, prompt da US01, código em `app/`, testes em `tests/`, diagramas | 62 testes automáticos a passar; teste manual do fluxo registo → ligação → ativação no servidor de desenvolvimento | (pendente: outro elemento da equipa) | Aceite com alterações a decidir na revisão |
| 2026-10-01 | (preencher) | Claude | Revisão crítica dos requisitos (Tarefa 2) contra o backlog e o código da US01 | Versão 1.1 de `docs/01`: RNF e RN alterados, secção de dependências e pontos em aberto | Comparação com os critérios de aceitação do backlog e com as decisões técnicas de `docs/02` | (pendente: Product Owner e outro elemento) | Por validar |
| 2026-10-07 | (preencher) | Claude | Reorganização da documentação por user story | Documentos movidos para `docs/geral/` e `docs/US01/` (prompt e diagramas incluídos), ligações atualizadas, índices `docs/README.md` e `docs/US01/README.md`, secção «Estado do projeto» no README, modelos de Pull Request e de issue em `.github/` | Verificação automática das ligações internas dos ficheiros `.md`; 62 testes automáticos a passar | (pendente: outro elemento da equipa) | Por validar |
| 2026-10-07 | Duarte Eusébio | Claude | Organizar o código para o Product Owner alterar textos e cores sem mexer na lógica; tornar o README mais legível | `app/texts.py` com todos os textos da interface; templates, validações e email a usá-lo; comentários nas cores do CSS; `tests/test_texts.py` (7 testes); README reorganizado com a secção «Alterar textos e cores» | 69 testes a passar; HTML de todas as páginas comparado antes e depois (igual) | (pendente: Simão Almeida) | Por validar |
| 2026-10-07 | Duarte Eusébio | Claude | US01: aceitar email pessoal em vez de só o institucional (decisão do PO) | Validação separada em formato do email e domínio opcional (`ALLOWED_EMAIL_DOMAINS` vazio por omissão); textos, testes e documentação da US01 e RF01 atualizados | 80 testes a passar, incluindo os de domínios parecidos com a restrição ligada | (pendente: Simão Almeida) | Por validar |

## Modelo para novas entradas

| Data | Quem | Ferramenta | Pedido (resumo) | O que foi gerado | Como foi validado | Revisto por | Resultado |
|---|---|---|---|---|---|---|---|
| AAAA-MM-DD | | | | | | | Aceite / Aceite com alterações / Rejeitado |
