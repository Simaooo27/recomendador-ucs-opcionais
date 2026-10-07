# Requisitos funcionais e não funcionais

Projeto 1 · Metodologias Ágeis (Scrum) · Recomendador de UCs opcionais

**Versão 1.2 · rascunho para validação do Product Owner · 2026-10-07.** As alterações face à versão 1.0 estão na [secção 6](#6-histórico-de-alterações) e as decisões pendentes na [secção 5](#5-dependências-e-pontos-em-aberto).

Este documento reúne os requisitos do produto. Cada requisito tem um identificador estável (RF, RNF, RN) que deve ser usado nas user stories, nos commits, nos testes e nos prompts de IA. Os requisitos da US01 estão detalhados em [US01/requisitos.md](../US01/requisitos.md).

**Convenções.** RF = requisito funcional. RNF = requisito não funcional. RN = regra de negócio. Os requisitos descrevem *o quê*, não *como*; as decisões técnicas estão em [02-regras-de-geracao-de-codigo.md](02-regras-de-geracao-de-codigo.md).

## 1. Requisitos funcionais

### Módulo A — Contas e perfis

- **RF01** O sistema deve permitir o registo de alunos com email pessoal, confirmado por uma ligação enviada para esse email.
- **RF02** O sistema deve permitir autenticação, recuperação de palavra-passe e fim de sessão.
- **RF03** O aluno deve indicar o curso e o ano curricular atual.
- **RF04** O sistema deve distinguir os perfis Aluno e Administrador, com permissões distintas.

### Módulo B — Catálogo de UCs

- **RF05** O administrador deve poder importar UCs a partir de CSV (código, nome, curso, ano, semestre, ECTS, tipo obrigatória/opcional, descrição).
- **RF06** O administrador deve poder criar, editar e desativar UCs individualmente.
- **RF07** O aluno deve poder consultar o catálogo de opcionais com descrição e estatísticas agregadas (médias de interesse, carga e dificuldade), sujeitas à regra de anonimato RN04.

### Módulo C — Percurso académico

- **RF08** O aluno deve poder indicar as UCs (obrigatórias e opcionais) que concluiu e o ano letivo/semestre em que as frequentou.
- **RF09** O sistema deve impedir registos duplicados da mesma UC no mesmo ano letivo.

### Módulo D — Avaliações

- **RF10** O aluno deve poder avaliar cada UC opcional concluída em: interesse (1–5), carga de trabalho (1–5) e dificuldade (1–5).
- **RF11** O aluno deve poder avaliar UCs obrigatórias pelo menos em interesse (1–5), numa vista rápida em grelha.
- **RF12** O aluno pode acrescentar um comentário livre opcional (máx. 500 caracteres).
- **RF13** O aluno deve poder editar ou apagar as suas avaliações.
- **RF14** O administrador deve poder abrir e fechar períodos de avaliação por semestre.

### Módulo E — Privacidade

- **RF15** As avaliações devem ser guardadas associadas a um identificador pseudonimizado, separado dos dados de identificação do aluno.
- **RF16** O sistema nunca deve mostrar avaliações individuais associadas a um autor.
- **RF17** O aluno deve poder exportar e eliminar todos os seus dados.
- **RF18** O administrador deve poder ocultar comentários inapropriados ou que identifiquem pessoas.

### Módulo F — Motor de recomendação

- **RF19** O sistema deve gerar, para cada aluno, uma lista ordenada top-N de opcionais recomendadas com uma pontuação prevista de interesse.
- **RF20** Para alunos sem dados suficientes, o sistema deve usar um fallback baseado na popularidade (média bayesiana de interesse).
- **RF21** O motor deve implementar filtragem colaborativa baseada em utilizadores (similaridade entre alunos com base nas avaliações comuns).
- **RF22** O motor deve permitir, como evolução, fatorização de matrizes (ex.: SVD).
- **RF23** A estratégia usada (baseline, user-based, SVD) deve ser configurável pelo administrador.

### Módulo G — Filtros e contexto

- **RF24** O sistema deve excluir das recomendações UCs que o aluno já concluiu ou que não estão disponíveis para o seu ano/curso.
- **RF25** O aluno deve poder filtrar recomendações por semestre e ECTS.
- **RF26** O aluno deve poder indicar a preferência de carga de trabalho (leve / indiferente / exigente), que ajusta a ordenação.
- **RF27** O sistema deve poder esconder opcionais sem vagas.
- **RF28** O aluno deve poder indicar o seu horário e o sistema deve excluir opcionais em conflito.

### Módulo H — Explicação e feedback

- **RF29** Cada recomendação deve apresentar uma justificação (ex.: *"6 alunos com gostos parecidos com os teus deram, em média, 4,3 de interesse"*).
- **RF30** O aluno deve poder marcar uma recomendação como útil / não útil ou ocultá-la.

### Módulo I — Avaliação do algoritmo e administração

- **RF31** O sistema deve permitir gerar um dataset sintético para testes.
- **RF32** O sistema deve correr uma avaliação offline (divisão treino/teste) e reportar RMSE, MAE, Precision@K e cobertura para cada estratégia.
- **RF33** O administrador deve ter um painel com indicadores de participação (nº de avaliações, nº de alunos, grau de esparsidade da matriz).

## 2. Requisitos não funcionais

| ID | Categoria | Requisito |
|----|-----------|-----------|
| RNF01 | Privacidade | Cumprimento dos princípios do RGPD: minimização de dados, consentimento explícito na recolha (com registo da versão da política aceite), direito ao apagamento e à exportação. |
| RNF02 | Segurança | Palavras-passe guardadas apenas como hash (scrypt, via Werkzeug); proteção contra CSRF, SQL injection e XSS; segredos fora do código e do repositório. |
| RNF03 | Desempenho | Recomendações geradas em menos de 2 segundos para um dataset de até 500 alunos × 100 UCs. |
| RNF04 | Usabilidade | Interface responsiva, utilizável em telemóvel; avaliação de uma UC em menos de 30 segundos. |
| RNF05 | Tecnologia | Python 3.10 ou superior com Flask 3.x; SQLite pela biblioteca padrão (`sqlite3`); pandas e NumPy no motor de recomendação (scikit-surprise só para a estratégia SVD). Outras tecnologias exigem decisão da equipa (ver [02-regras-de-geracao-de-codigo.md](02-regras-de-geracao-de-codigo.md)). |
| RNF06 | Qualidade | Cada critério de aceitação tem pelo menos um teste automático (`unittest`). No motor de recomendação, os testes usam casos de resultado conhecido. Os testes correm sem rede e com um único comando. |
| RNF07 | Manutenibilidade | Motor de recomendação isolado num módulo próprio, com interface comum às várias estratégias. |
| RNF08 | Rastreabilidade | Código no Git, com commits associados às user stories (ex.: `US12: cálculo de similaridade`). |
| RNF09 | Uso de IA | O código gerado com apoio de IA é revisto, testado e assinalado; as ferramentas e os prompts relevantes são documentados no relatório. |
| RNF10 | Acessibilidade | Formulários com etiquetas associadas aos campos, erros ligados ao campo, contraste suficiente e navegação completa por teclado (referência: WCAG 2.1 nível AA, nos aspetos básicos). |
| RNF11 | Idioma | Interface e mensagens em português de Portugal. |

## 3. Regras de negócio

- **RN01** Um aluno só pode avaliar UCs que registou como concluídas no seu percurso.
- **RN02** Existe no máximo uma avaliação por aluno, por UC, por ano letivo.
- **RN03** Nunca se recomenda uma UC que o aluno já concluiu.
- **RN04** Estatísticas agregadas de uma UC só são mostradas quando há pelo menos 5 avaliações (evita identificar quem avaliou em turmas pequenas).
- **RN05** A recomendação personalizada só é usada quando o aluno tem pelo menos 3 UCs avaliadas e existem pelo menos 5 outros alunos com 2 ou mais UCs avaliadas em comum com ele; caso contrário, aplica-se o fallback de popularidade. *(Definição proposta; o Product Owner valida. A versão 1.0 dizia apenas «sobreposição suficiente».)*
- **RN06** O critério principal de recomendação é o **interesse**; carga e dificuldade funcionam como ajuste/filtro segundo a preferência do aluno.
- **RN07** As avaliações são números inteiros de 1 a 5. Interesse: 1 = nenhum, 5 = muito. Carga de trabalho: 1 = muito leve, 5 = muito pesada. Dificuldade: 1 = muito fácil, 5 = muito difícil. *(Nova.)*
- **RN08** As explicações das recomendações seguem a RN04: o número de colegas semelhantes e a média de interesse deles só se mostram quando contribuíram pelo menos 5 colegas; caso contrário, a explicação indica apenas que a UC é bem avaliada pelos colegas em geral. *(Nova; fecha uma lacuna de privacidade entre RF29 e RN04.)*

## 4. Rastreabilidade: user story → requisitos

As stories foram renumeradas a 07/10/2026 pela ordem do backlog replaneado ([product-backlog.xlsx](product-backlog.xlsx)); a coluna «ID anterior» liga aos números usados antes dessa data.

| User story | Requisitos funcionais | Sprint | ID anterior |
|---|---|---|---|
| US01 — Registo com email pessoal | RF01 (ver [detalhe](../US01/requisitos.md)) | Sprint 1 | US01 |
| US02 — Autenticação | RF02 (início e fim de sessão; ver [detalhe](../US02/requisitos.md)) | Sprint 1 | US02 |
| US03 — Perfis de aluno e administrador | RF04 (ver [detalhe](../US03/requisitos.md)) | Sprint 1 | nova |
| US04 — Importar catálogo de cursos e UCs | RF05 | Sprint 2 | US03 |
| US05 — Consultar catálogo de opcionais | RF07 | Sprint 2 | US04 |
| US06 — Registar percurso | RF08, RF09 | Sprint 2 | US05 |
| US07 — Avaliar opcional concluída | RF10, RF13 | Sprint 2 | US06 |
| US08 — Avaliação rápida de obrigatórias | RF11 | Sprint 2 | US07 |
| US09 — Avaliações pseudonimizadas | RF15, RF16 | Sprint 2 | US09 |
| US10 — Dataset sintético | RF31 | Sprint 3 | US20 |
| US11 — Recomendações de popularidade | RF20 | Sprint 3 | US11 |
| US12 — Recomendações user-based | RF19, RF21 | Sprint 3 | US12 |
| US13 — Excluir UCs inválidas | RF24 | Sprint 3 | US15 |
| US14 — Explicação da recomendação | RF29 | Sprint 3 | US13 |
| US15 — Avaliação offline do motor | RF32 | Sprint 4 | US21 |
| US16 — Períodos de avaliação | RF14 | Sprint 4 | US24 |
| US17 — Exportar e apagar dados | RF17 | Sprint 4 | US10 |
| US18 — Comentário livre | RF12 | Sprint 4 | US08 |
| US19 — Moderar comentários | RF18 | Sprint 4 | US25 |
| US20 — Filtrar por semestre e ECTS | RF25 | Sprint 4 | US16 |
| US21 — Preferência de carga de trabalho | RF26 | Backlog | US14 |
| US22 — Comparação de estratégias | RF23 | Backlog | US23 |
| US23 — Esconder UCs sem vagas | RF27 | Backlog | US17 |
| US24 — Feedback sobre recomendações | RF30 | Backlog | US19 |
| US25 — Painel de participação | RF33 | Backlog | US26 |
| US26 — Filtragem baseada em itens | sem RF associado | Backlog | US27 |
| US27 — Evitar conflitos de horário | RF28 | Backlog | US18 |
| US28 — Lembretes de avaliação | sem RF associado | Backlog | US28 |
| *(fora do plano)* — Fatorização de matrizes (SVD) | RF22 | — | US22 |

### Lacunas a resolver pelo Product Owner

- **Sem user story:** RF03 (curso e ano curricular do aluno) e RF06 (criar, editar e desativar UCs individualmente). O RF04 (perfis Aluno e Administrador) passou a ter a US03.
- **Parte sem user story:** a recuperação de palavra-passe, incluída no RF02.
- **Sem requisito:** as user stories US26 e US28 (antigas US27 e US28) não têm RF. Acrescentar o requisito ou retirar a story.

## 5. Dependências e pontos em aberto

Problemas encontrados ao rever os requisitos contra o backlog. Cada um traz uma proposta; a decisão é do Product Owner. A coluna *Estado* regista o que já foi alterado neste documento.

| # | Ponto | Porque importa | Proposta | Estado |
|---|---|---|---|---|
| 1 | A US06 (Sprint 1) exige avaliar «dentro de um período aberto», mas os períodos (RF14, US24) só chegam no Sprint 3. | A US06 não pode ficar «Done» no Sprint 1 com um critério que depende de uma story posterior. | No Sprint 1 o período está sempre aberto por omissão; o bloqueio fora de período entra com a US24. Reescrever esse critério da US06 em conformidade. | Por decidir |
| 2 | As avaliações são gravadas no Sprint 1 (US06) mas a pseudonimização só chega no Sprint 2 (US09). | Gravar avaliações ligadas ao utilizador e migrar depois é trabalho extra e arrisca expor dados entretanto. | Desde a US05/US06, guardar percurso e avaliações com um `pseudo_id` (identificador por aluno, numa tabela de mapeamento isolada). A US09 completa as regras de visualização e exportação. | Por decidir |
| 3 | O RF29 e a US13 mostram o nº de colegas semelhantes e a média deles, e a RN04 só protegia os agregados por UC. | Com poucos vizinhos, a explicação pode permitir identificar quem avaliou. | Aplicar a mesma regra de mínimo de 5 às explicações. | **Alterado:** nova RN08. Falta ajustar os critérios da US13. |
| 4 | A RN05 dizia «sobreposição suficiente», que não se pode testar. | Um requisito vago dá testes vagos e discussões na Review. | Definição numérica explícita (3 UCs avaliadas e 5 alunos com 2 ou mais UCs em comum). Os valores são ajustáveis depois de vermos dados reais. | **Alterado:** RN05 definida. Falta validação. |
| 5 | As escalas 1 a 5 não tinham significado definido. | «Carga 4» pode querer dizer coisas opostas para dois alunos; as médias perdem sentido. | Fixar o significado de cada extremo e mostrá-lo no formulário. | **Alterado:** nova RN07. |
| 6 | RF03, RF04, RF06 e a recuperação de palavra-passe (RF02) não têm user story; as US27 e US28 não têm requisito. | Requisitos sem story nunca são implementados; stories sem requisito não têm critério de origem. | Ver a lista no fim da secção 4. | Por decidir |
| 7 | A RN04 (mínimo de 5 avaliações) pode esconder quase tudo se a turma for pequena. | Numa demonstração com 20 alunos, muitas UCs ficam sem estatísticas e as explicações caem no ramo genérico. | Dataset sintético (US20) e recolha piloto cedo; o painel da US26 mostra quantas UCs já passam o mínimo. | Por decidir |
| 8 | O RNF05 previa «Django ou Flask» e PostgreSQL, mas o código da US01 usa Flask e `sqlite3`. | Os requisitos e o código não podem contar histórias diferentes. | Alinhar o RNF05 com a decisão técnica e retirar o PostgreSQL do âmbito. | **Alterado:** RNF05 (e RNF02, RNF06 pelo mesmo motivo). |
| 9 | O domínio dos emails institucionais dos alunos não está confirmado. | O RF01 depende dele. | Aceitar email pessoal; a restrição a um domínio fica como opção (`ALLOWED_EMAIL_DOMAINS`, ver [US01/requisitos.md](../US01/requisitos.md)). | **Alterado:** RF01 (versão 1.2). |

## 6. Histórico de alterações

| Versão | Data | Alterações |
|---|---|---|
| 1.0 | 2026-09-30 | Versão inicial (33 RF, 9 RNF, 6 RN), igual ao documento Word. |
| 1.1 | 2026-10-01 | RNF01, RNF02, RNF05 e RNF06 reescritos para refletirem a segurança e a tecnologia decididas. Novos RNF10 (acessibilidade) e RNF11 (idioma). RN05 com definição numérica; novas RN07 (escalas) e RN08 (privacidade nas explicações). Novas secções 5 e 6 e matriz de rastreabilidade. |
| 1.2 | 2026-10-07 | RF01: registo com email pessoal, por decisão do Product Owner (ponto 9 da secção 5). |

O ficheiro Word e o Excel do backlog continuam na versão 1.0. Depois de o Product Owner validar a 1.1, devem ser atualizados a partir deste documento.
