# Cerimónias Scrum: o que está registado e o que falta

Versão de 31/10/2026. Este documento junta, num só sítio, as cinco cerimónias do Scrum de cada sprint. O detalhe das decisões continua no [PROJETO.md](../../PROJETO.md#1-estado-do-projeto) e na folha «Plano de sprints» do [backlog](product-backlog.xlsx).

**O que falta, em resumo:** as **Sprint Retrospectives** não estão registadas em nenhum sprint e as **Daily Scrums** também não. Se a equipa as fez e as escreveu no Notion, basta pôr aqui a ligação. Se não as escreveu, as secções 2 e 3 têm os factos de cada sprint, para a equipa preencher só o que pensa deles. **Este documento não inventa opiniões da equipa.**

## 1. Visão geral

| Sprint | Datas | Sprint Planning | Sprint Review | Sprint Retrospective | SP planeados / feitos |
|---|---|---|---|---|---|
| Sprint 1 | até 07/10 | Sprint Goal registado; replaneado a 07/10 (24 → 10 SP) | Não registada (só «concluído a 07/10») | **Não registada** | 10 / 10 |
| Sprint 2 | 20/10 a 22/10 | 20/10 (PROJETO.md) | 22/10, pelos dois Product Owners | **Não registada** | 13 / 13 |
| Sprint 3 | 22/10 a 23/10 | 22/10 (PROJETO.md) | 23/10, pelos dois Product Owners | **Não registada** | 7 / 7 |
| Sprint 4 | 29/10 a 05/11 | 27/10 e 29/10 (alargado duas vezes) | **Por fazer (05/11)**: guião na secção 4 | **Por fazer (05/11)** | 47 a 49 / por aceitar |

Daily Scrums: não há registo em nenhum sprint. Numa equipa de dois elementos com sprints de uma semana, a conversa diária pode ter sido informal; se foi, vale a pena dizê-lo no relatório, porque é uma das cinco cerimónias.

## 2. Retrospetivas dos Sprints 1 a 3 (para preencher)

A retrospetiva responde a duas perguntas: **o que correu bem e menos bem?** e **o que melhorar no sprint seguinte?** Os factos abaixo vêm do registo do projeto; as respostas são da equipa.

### Sprint 1

Factos: tinha 24 SP planeados e a equipa fez 10, o que levou ao replaneamento de 07/10 e a fixar a velocidade em 10 SP. A US03 foi revista a 14/10 (um só início de sessão para alunos e administradores).

| O que correu bem | O que correu menos bem | O que melhorar no Sprint 2 |
|---|---|---|
| | | |

### Sprint 2

Factos: a US29 e a US30 foram feitas antes de o sprint começar, e por isso a US31 foi antecipada. A US30 foi feita duas vezes em paralelo (pelo Simão, no PR #22, e numa versão que foi descartada), por falta de combinação de quem fazia o quê. O servidor Ollama da faculdade foi testado e posto de parte.

| O que correu bem | O que correu menos bem | O que melhorar no Sprint 3 |
|---|---|---|
| | | |

### Sprint 3

Factos: 7 de 7 SP, fechado a 23/10, antes da data prevista (29/10), porque o objetivo estava cumprido. O Simão escreveu as correções da revisão da US05 (PR #38). Um teste da US17 dependia da data em que corria.

| O que correu bem | O que correu menos bem | O que melhorar no Sprint 4 |
|---|---|---|
| | | |

## 3. Retrospetiva do Sprint 4 (fazer a 05/11, logo depois da Review)

Factos para discutir:

- O Sprint 4 tem 47 SP (49 com a US48) para uma velocidade de 10. Grande parte do código foi feita antes do sprint, como protótipo, e o sprint foi alargado duas vezes (27/10 e 29/10).
- As stories foram aceites pelo PO a 27/10 e 29/10, antes da Sprint Review e, no primeiro caso, antes de o sprint começar.
- Os PR #50 a #60 foram juntados pelo próprio autor, sem revisão do Simão. Nenhum PR do projeto tem uma revisão formal no GitHub.
- O PR #58 (US48) foi juntado no ramo do PR #57 depois de o #57 já estar na `main`, e por isso não chegou à `main`; só foi detetado a 31/10.
- A verificação com o catálogo real encontrou erros que os testes não apanhavam (ensino privado no concurso nacional, equivalências das Matemáticas, US37 com o catálogo completo).

| O que correu bem | O que correu menos bem | O que melhorar numa próxima release |
|---|---|---|
| | | |

## 4. Guião da Sprint Review do Sprint 4 (05/11)

Participam os dois Product Owners, a equipa e, se possível, o docente (stakeholder). Mostra-se o produto a funcionar, sem diapositivos, pela ordem em que uma pessoa o usa. Cada story mostrada marca a caixa «Funciona na demonstração» da sua Definition of Done.

| # | O que mostrar | Stories |
|---|---|---|
| 1 | Procurar cursos no catálogo completo (1699 cursos) e abrir uma ficha com as condições de acesso, a tendência e a procura | US48, US04, US33, US41, US42 |
| 2 | Conversa com o assistente, com autorização para usar as notas, e sugestões sem cursos a que falta uma prova | US37 |
| 3 | Plano de candidatura: notas, nota de candidatura a cada curso, quanto preciso no exame, 6 opções com avisos | US34, US35, US36, US40 |
| 4 | Que exames abrem mais portas, plano B da 2.ª fase e partilhar o plano | US44, US45, US43 |
| 5 | Datas do concurso no início e no plano | US38 |
| 6 | A minha conta: exportar os dados e recuperar a palavra-passe por email | US46, US47 |
| 7 | Área de gestão: corrigir e esconder um curso do catálogo | US39 |

Decisões a tomar na Review:

- [ ] Aceitar ou não a US48 (por aceitar desde 29/10).
- [ ] Velocidade real do Sprint 4: só contam as stories com a Definition of Done completa (como no exemplo dos diapositivos, em que «quase feito» não conta).
- [ ] O que fica para uma próxima release (por exemplo, os limites do assistente com o catálogo completo, registados na US48).

Antes da Review, o Simão revê os PR que ainda não reviu (a lista está na coluna «Definition of Done» da folha «Product Backlog»).
