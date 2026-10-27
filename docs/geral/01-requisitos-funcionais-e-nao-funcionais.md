# Requisitos funcionais e não funcionais

Projeto 1 · Metodologias Ágeis (Scrum) · OptaBem

**Versão 1.9 · rascunho para validação do Product Owner · 2026-10-27.** O OptaBem é um **recomendador de cursos**: orienta quem ainda está a escolher curso, compara cursos de várias instituições e ajuda a preparar a candidatura ao concurso nacional (ver a [visão do produto](00-visao-do-produto.md)). A 27/10, com autorização do docente, os requisitos das opcionais saíram do produto e estão no [anexo A](#anexo-a--requisitos-das-opcionais-arquivados-a-27102026). As alterações estão na [secção 6](#6-histórico-de-alterações) e as decisões pendentes na [secção 5](#5-dependências-e-pontos-em-aberto).

Este documento reúne os requisitos do produto. Cada requisito tem um identificador estável (RF, RNF, RN) que deve ser usado nas user stories, nos commits, nos testes e nos prompts de IA. Os identificadores arquivados não são reutilizados, por isso a numeração tem saltos. Os requisitos de cada story estão detalhados em `docs/USNN/requisitos.md`.

**Convenções.** RF = requisito funcional. RNF = requisito não funcional. RN = regra de negócio. Os requisitos descrevem *o quê*, não *como*; as decisões técnicas estão em [02-regras-de-geracao-de-codigo.md](02-regras-de-geracao-de-codigo.md).

## 1. Requisitos funcionais

### Módulo A — Contas e privacidade

- **RF01** O sistema deve permitir o registo com email pessoal e nome, confirmado por uma ligação enviada para esse email.
- **RF02** O sistema deve permitir iniciar e terminar sessão e recuperar a palavra-passe.
- **RF03** O utilizador pode ter um curso e uma instituição no perfil, ou ainda não ter curso. *(Alterado na 1.9: sai o ano curricular, que só servia as opcionais.)*
- **RF04** O sistema deve distinguir os perfis Aluno e Administrador, com permissões distintas.
- **RF17** O utilizador deve poder exportar e apagar todos os seus dados. *(A 22/10 a US17 ficou só com o apagamento; a exportação é a US46.)*

### Módulo B — Catálogo de instituições e cursos

- **RF05** O catálogo tem as licenciaturas e os mestrados integrados do concurso nacional (código DGES, instituição, localidade, vagas, nota do último colocado, área, condições de acesso, descrição, saídas profissionais e fontes). É recolhido das páginas públicas da DGES por um script que a equipa corre no seu computador. *(Alterado na 1.9: antes era importado por CSV pelo administrador, com as UCs de cada curso.)*
- **RF34** Qualquer utilizador deve poder consultar e filtrar os cursos do catálogo (por área, instituição e localidade) e comparar até 3 cursos lado a lado.

### Módulo C — Percurso

- **RF35** O sistema deve registar cada decisão do percurso (escolha ou mudança de curso) com data, opções sugeridas e opção escolhida, e mostrá-las numa linha do tempo. *(Alterado na 1.9: sai a escolha de opcionais.)*

### Módulo J — Orientação de curso

- **RF36** O utilizador sem curso deve poder ter uma conversa de orientação conduzida por um LLM, que lhe faz uma pergunta de cada vez (no máximo 6) para descobrir os seus interesses, o tipo de trabalho que imagina e as preferências de localidade e regime. As perguntas não são fixas. A conversa pode ser recomeçada.
- **RF37** No fim da conversa (quando o LLM tem informação suficiente, ao fim de 6 respostas ou a pedido do utilizador), o sistema deve sugerir 2 a 3 cursos do catálogo, cada um com os dados do catálogo e uma explicação em linguagem simples ligada ao que a pessoa disse.
- **RF38** O fornecedor do LLM deve ser configurável (Google Gemini, Groq e um modelo falso para testes), sem alterar o resto da aplicação.
- **RF39** O utilizador deve poder escolher um dos cursos sugeridos, ou outro do catálogo, passando a ter esse curso no perfil (RF03).

### Módulo K — Plano de candidatura

- **RF40** A ficha de cada curso deve mostrar as condições de acesso publicadas pela DGES: conjuntos alternativos de provas de ingresso, fórmula da nota de candidatura (pesos da média do secundário e das provas), classificações mínimas e pré-requisitos.
- **RF41** O utilizador com sessão iniciada deve poder indicar a média do secundário (9,5 a 20) e as notas dos exames nacionais que fez (0 a 200), e mudá-las quando quiser.
- **RF42** O sistema deve calcular a nota de candidatura do utilizador a cada curso, com o conjunto de provas mais favorável, e compará-la com a nota do último colocado (acima, perto ou abaixo), assinalando provas em falta e notas abaixo do mínimo. É uma estimativa para o contingente geral da 1.ª fase.
- **RF43** O utilizador deve poder montar e ordenar uma lista de até 6 opções de candidatura e receber avisos (opções que não contam, nenhuma opção segura, a mais fácil em 1.º lugar, menos de 6 opções, pré-requisitos). O OptaBem não submete a candidatura.
- **RF44** Na ficha de cada curso, o sistema deve dizer a nota que o utilizador precisa nas provas que ainda não fez para chegar ao último colocado (ou à nota mínima), no conjunto de provas em que é mais fácil, respeitando o mínimo de cada prova, e avisar quando nem 200 pontos chegam.
- **RF45** A ficha deve mostrar a nota do último colocado da 1.ª fase de 2023 a 2025 e se está a subir, a descer ou estável.
- **RF46** A ficha deve mostrar a procura na 1.ª fase de 2025: candidatos, candidatos em 1.ª opção, vagas e colocados, com uma etiqueta simples.
- **RF47** O utilizador deve poder criar e desligar uma ligação só de leitura para o seu plano, que mostra o primeiro nome, as opções, a nota de candidatura e a situação, e nunca o email, a média nem as notas dos exames.
- **RF48** Com 2 ou mais opções no plano, o sistema deve mostrar as combinações de até 3 exames nacionais que dão para concorrer a mais opções, dizendo para que opções não dão e que exames a pessoa já fez.
- **RF49** O sistema deve mostrar cursos das áreas do plano, fora dele, que tiveram vagas na 2.ª fase do ano anterior e a que a nota da pessoa chegava (plano B).
- **RF50** O percurso deve mostrar as datas das fases do concurso nacional, com a ligação para a DGES, e o próximo prazo. *(Nova na 1.9, para a US38.)*

## 2. Requisitos não funcionais

| ID | Categoria | Requisito |
|----|-----------|-----------|
| RNF01 | Privacidade | Cumprimento dos princípios do RGPD: minimização de dados, consentimento explícito na recolha (com registo da versão da política aceite), direito ao apagamento e à exportação. |
| RNF02 | Segurança | Palavras-passe guardadas apenas como hash (scrypt, via Werkzeug); proteção contra CSRF, SQL injection e XSS; segredos fora do código e do repositório. |
| RNF03 | Desempenho | A lista e a ficha dos cursos e o plano de candidatura respondem em menos de 2 segundos com o catálogo completo da DGES. A resposta do LLM segue o RNF12. *(Alterado na 1.9: era o tempo das recomendações de opcionais.)* |
| RNF04 | Usabilidade | Interface responsiva, utilizável em telemóvel. *(Alterado na 1.9: sai a meta de avaliar uma UC em 30 segundos.)* |
| RNF05 | Tecnologia | Python 3.10 ou superior com Flask 3.x; SQLite pela biblioteca padrão (`sqlite3`). Outras tecnologias exigem decisão da equipa (ver [02-regras-de-geracao-de-codigo.md](02-regras-de-geracao-de-codigo.md)). *(Alterado na 1.9: saem pandas, NumPy e scikit-surprise, que eram do motor de opcionais.)* |
| RNF06 | Qualidade | Cada critério de aceitação tem pelo menos um teste automático (`unittest`). As contas da candidatura são testadas com casos de resultado conhecido. Os testes correm sem rede e com um único comando. |
| RNF07 | Manutenibilidade | O acesso ao LLM e as contas da candidatura ficam em módulos próprios, que não dependem do Flask (`app/llm`, `app/candidatura/calculos.py`). *(Alterado na 1.9: era o motor de recomendação de opcionais.)* |
| RNF08 | Rastreabilidade | Código no Git, com commits associados às user stories (ex.: `US35: nota de candidatura a cada curso`). |
| RNF09 | Uso de IA | O código gerado com apoio de IA é revisto, testado e assinalado; as ferramentas e os prompts relevantes são documentados no relatório. |
| RNF10 | Acessibilidade | Formulários com etiquetas associadas aos campos, erros ligados ao campo, contraste suficiente e navegação completa por teclado (referência: WCAG 2.1 nível AA, nos aspetos básicos). |
| RNF11 | Idioma | Interface e mensagens em português de Portugal. |
| RNF12 | Uso de LLM | Ao LLM só são enviados o texto da conversa e dados do catálogo, nunca email, nome ou identificadores da conta. Emails e números longos (telemóvel, NIF, cartão de cidadão, IBAN) escritos pelo utilizador são apagados antes de cada envio; a página avisa para não escrever dados pessoais, porque nomes no meio do texto não são detetáveis. Chaves de API ficam fora do código e do repositório e nunca aparecem em mensagens de erro. Os testes usam um LLM falso e correm sem rede. Cada resposta do LLM tem de chegar em menos de 15 segundos ou o utilizador recebe uma mensagem clara. |

## 3. Regras de negócio

- **RN09** Só podem ser mostrados ao utilizador cursos que existem no catálogo: qualquer curso devolvido pelo LLM que não exista é descartado antes de chegar ao ecrã.
- **RN10** As sugestões nunca atribuem um curso automaticamente: o utilizador confirma sempre a escolha. *(Alterado na 1.9: sai «ou uma opcional».)*
- **RN11** A nota de candidatura e a diferença para o último colocado são sempre apresentadas como estimativa (contingente geral, 1.ª fase), nunca como garantia de entrada. *(Nova na 1.9; já era critério das US35 e US36.)*

As RN01 a RN08 eram das opcionais e estão no [anexo A](#anexo-a--requisitos-das-opcionais-arquivados-a-27102026).

## 4. Rastreabilidade: user story → requisitos

A partir de 13/10/2026 os números das stories ficam fixos: as stories novas recebem o número seguinte e os números das stories arquivadas não são reutilizados. A ordem de trabalho é a do [backlog](product-backlog.xlsx). As stories das opcionais (US06 a US16, US18 a US28) e a US32 (fundida na US29) estão na folha «Arquivo (opcionais)» do backlog.

| User story | Épico | Requisitos | Sprint | Estado |
|---|---|---|---|---|
| US01 — Registo com email pessoal | E1 | RF01 (ver [detalhe](../US01/requisitos.md)) | Sprint 1 | Feita |
| US02 — Autenticação | E1 | RF02 (início e fim de sessão; ver [detalhe](../US02/requisitos.md)) | Sprint 1 | Feita |
| US03 — Perfis de aluno e administrador | E1 | RF04 (ver [detalhe](../US03/requisitos.md)) | Sprint 1 | Feita |
| US29 — Conversa de orientação com o LLM | E3 | RF36, RNF12 | Sprint 2 | Feita |
| US30 — Sugestão de 2 a 3 cursos no fim da conversa | E3 | RF37, RF38, RNF12, RN09, RN10 | Sprint 2 | Feita |
| US31 — Escolher curso e linha do tempo do percurso | E3 | RF03, RF35, RF39, RN10 | Sprint 2 | Feita |
| US05 — Consultar e comparar cursos | E2 | RF34 | Sprint 3 | Feita |
| US17 — Apagar a minha conta | E1 | RF17 (apagamento) | Sprint 3 | Feita |
| US04 — Catálogo de licenciaturas recolhido da DGES | E2 | RF05 | Sprint 4 | Protótipo |
| US33 — Condições de acesso na ficha do curso | E4 | RF40 | Sprint 4 | Protótipo |
| US34 — Registar as minhas notas | E4 | RF41, RF17 | Sprint 4 | Protótipo |
| US35 — Nota de candidatura a cada curso | E4 | RF42, RN11 | Sprint 4 | Protótipo |
| US36 — Plano das 6 opções de candidatura | E4 | RF43, RN11 | Sprint 4 | Protótipo |
| US40 — Quanto preciso no exame? | E4 | RF44 | Backlog | Protótipo |
| US41 — Tendência do último colocado | E4 | RF45 | Backlog | Protótipo |
| US42 — Procura do curso | E4 | RF46 | Backlog | Protótipo |
| US44 — Que exames me abrem mais portas? | E4 | RF48 | Backlog | Protótipo |
| US37 — Assistente que conhece as minhas notas | E3 | RF37, RF41, RNF12 | Backlog | Por fazer |
| US46 — Exportar os meus dados | E1 | RF17 (exportação), RNF01 | Backlog | Por fazer |
| US47 — Recuperar a palavra-passe | E1 | RF02 (recuperação) | Backlog | Por fazer |
| US48 — Recolha completa das licenciaturas (DGES) | E2 | RF05, RNF03 | Backlog | Por fazer |
| US39 — Corrigir e esconder cursos do catálogo (gestão) | E2 | RF04, RF05 | Backlog | Por fazer |
| US43 — Partilhar o plano | E4 | RF47, RF17 | Backlog | Protótipo |
| US45 — Plano B: 2.ª fase | E4 | RF49 | Backlog | Protótipo |
| US38 — Datas do concurso no percurso | E4 | RF50 | Backlog | Por fazer |

**Épicos (desde 27/10):** E1 Conta e privacidade · E2 Catálogo de cursos · E3 Orientação com o assistente · E4 Plano de candidatura. **Protótipo** = código feito antes do sprint, ainda não aceite numa Sprint Review.

### Lacunas a resolver pelo Product Owner

Desde 27/10 todos os requisitos têm story e todas as stories têm requisito: a recuperação da palavra-passe (RF02) passou a ser a US47, a exportação (RF17) a US46 e a US38 tem o RF50. As lacunas antigas (RF06, US26 e US28) eram das opcionais e foram arquivadas.

## 5. Dependências e pontos em aberto

Problemas encontrados ao rever os requisitos contra o backlog. Cada um traz uma proposta; a decisão é do Product Owner. A coluna *Estado* regista o que já foi alterado neste documento. Os pontos 1 a 7 eram das opcionais e estão no [anexo A](#anexo-a--requisitos-das-opcionais-arquivados-a-27102026); a numeração mantém-se porque outros documentos citam os pontos pelo número.

| # | Ponto | Porque importa | Proposta | Estado |
|---|---|---|---|---|
| 8 | O RNF05 previa «Django ou Flask» e PostgreSQL, mas o código da US01 usa Flask e `sqlite3`. | Os requisitos e o código não podem contar histórias diferentes. | Alinhar o RNF05 com a decisão técnica e retirar o PostgreSQL do âmbito. | **Alterado:** RNF05 (e RNF02, RNF06 pelo mesmo motivo). |
| 9 | O domínio dos emails institucionais dos alunos não está confirmado. | O RF01 depende dele. | Aceitar email pessoal; a restrição a um domínio fica como opção (`ALLOWED_EMAIL_DOMAINS`, ver [US01/requisitos.md](../US01/requisitos.md)). | **Alterado:** RF01 (versão 1.2). |
| 10 | O plano de sprints soma 13, 13 e 18 SP para os Sprints 2 a 4, e a velocidade real do Sprint 1 foi 10 SP. | Um plano acima da velocidade falha no fim de cada sprint e desmotiva. | Planear a 10 SP por sprint. | **Alterado (14/10):** Sprints 2 a 4 com 8, 10 e 10 SP. **27/10:** o Sprint 4 volta a ter 18 SP (US04, US33 a US36), com o código feito antes como protótipo; as US40 a US45 ficam no backlog. A confirmar com o docente a 29/10. |
| 11 | A exportação e o apagamento de dados (RF17) ficavam no backlog. | O RNF01 (RGPD) exige estes direitos. | Antes da demonstração com utilizadores reais, implementar pelo menos o apagamento de conta; ou usar só contas de teste. | **Decidido (22/10):** a US17 ficou com o apagamento (Sprint 3). **27/10:** a exportação passa a ser a US46 (backlog). |
| 12 | A qualidade das sugestões depende das descrições dos cursos no catálogo. | Descrições vagas levam o LLM a sugestões genéricas. | Os Product Owners reveem as descrições do catálogo do MVP; com o catálogo completo (US04), os cursos sem descrição usam os dados da DGES. | Por decidir |
| 13 | Um assistente LLM que conversa com o utilizador (US32), em vez de só um questionário e uma lista de sugestões. | Pode tornar a orientação mais natural, mas aumenta custo, riscos de respostas fora do catálogo e dados pessoais enviados ao fornecedor. | Os Product Owners avaliam o âmbito antes de estimar. | **Alterado (14/10):** o LLM conduz a conversa; US32 fundida na US29; RF36 a RF38 e RNF12 reescritos. Custo e privacidade avaliados no [spike](05-spike-llm.md). |
| 14 | Os termos da API do Gemini excluem aplicações dirigidas a menores de 18 ou com probabilidade de serem usadas por eles, e só permitem o plano pago com utilizadores no EEE (Portugal). | O público «pessoa a escolher licenciatura» inclui alunos do secundário com 16 ou 17 anos; e o plano escolhido é o gratuito. | (a) Assumir o OptaBem como protótipo usado só pela equipa e na demonstração; (b) conversa com LLM só para maiores de 18; (c) plano pago ou outro fornecedor. Ver o [spike](05-spike-llm.md), secção 5. | **Decidido (20/10):** opção (a). O OptaBem é um protótipo usado pela equipa e na demonstração, com aviso de 18+ na conversa; fica escrito no relatório. |
| 15 | A conversa tem de ser guardada entre pedidos, e não cabe no cookie de sessão (limite de 4 KB). | Guardá-la no servidor é guardar texto livre escrito pelo utilizador (RNF01). | Guardar no servidor só enquanto a conversa decorre e apagar ao recomeçar ou depois da escolha (US31). | **Decidido (20/10, US31):** a conversa fica no servidor enquanto decorre e é apagada ao recomeçar e depois da escolha do curso. |
| 16 | «Matemática» (código 16) e «Matemática A» (19) contam com o mesmo exame no protótipo do plano de candidatura. | Se estiver errado, a nota de candidatura e os avisos ficam errados em vários cursos. | A equipa confirma na DGES antes de aceitar a US34 e a US35. | Por decidir |

## 6. Histórico de alterações

| Versão | Data | Alterações |
|---|---|---|
| 1.0 | 2026-09-30 | Versão inicial (33 RF, 9 RNF, 6 RN), igual ao documento Word. |
| 1.1 | 2026-10-01 | RNF01, RNF02, RNF05 e RNF06 reescritos para refletirem a segurança e a tecnologia decididas. Novos RNF10 (acessibilidade) e RNF11 (idioma). RN05 com definição numérica; novas RN07 (escalas) e RN08 (privacidade nas explicações). Novas secções 5 e 6 e matriz de rastreabilidade. |
| 1.2 | 2026-10-07 | RF01: registo com email pessoal, por decisão do Product Owner (ponto 9 da secção 5). |
| 1.3 | 2026-10-13 | Nova [visão do produto](00-visao-do-produto.md). RF03, RF05 e RF07 alterados; novos RF34 a RF39 (comparar cursos, linha do tempo, orientação de curso com LLM), RNF12 (uso de LLM), RN09 e RN10. Rastreabilidade com as stories novas US29 a US31 e o novo plano de sprints. Pontos 10 a 12 da secção 5. |
| 1.4 | 2026-10-14 | Decisão do PO (issue #15): o LLM conduz a conversa de orientação. RF36, RF37, RF38 e RNF12 reescritos; US29 e US30 reescritas e US32 fundida na US29; plano a 10 SP por sprint (pontos 10 e 13 fechados); novos pontos 14 (termos do Gemini) e 15 (guardar a conversa). Spike em [05-spike-llm.md](05-spike-llm.md). |
| 1.5 | 2026-10-20 | Sprint Planning do Sprint 2: ponto 14 decidido (protótipo da equipa, opção a); US31 antecipada para o Sprint 2. |
| 1.6 | 2026-10-20 | US31: ponto 15 decidido (a conversa é apagada depois da escolha do curso). Detalhe em [US31/requisitos.md](../US31/requisitos.md). |
| 1.7 | 2026-10-22 | Sprint 3: US05 sem dependência da US04; US17 reduzida ao apagamento da conta e ponto 11 decidido. Detalhe em [US05/requisitos.md](../US05/requisitos.md) e [US17/requisitos.md](../US17/requisitos.md). |
| 1.8 | 2026-10-23 | Plano de candidatura (decisão do PO, com o protótipo do PR #44): novo módulo K (RF40 a RF49) e stories US33 a US45; US04 reescrita (catálogo da DGES por recolha); as stories das opcionais passam a Won't (fase 2). Detalhe da US01 (nome no registo) e da US02 (terminar sessão volta à página inicial). |
| 1.9 | 2026-10-27 | Reestruturação autorizada pelo docente: o OptaBem é só um recomendador de cursos. Os módulos D a I, os RF06 a RF16 (exceto o RF17) e RF18 a RF33, as RN01 a RN08 e os pontos 1 a 7 passam para o anexo A. RF01, RF03, RF05, RF35, RNF03 a RNF08 e RN10 alterados; novos RF50 e RN11 e ponto 16. Stories novas US46 (exportar dados) e US47 (recuperar a palavra-passe); US04 dividida (a recolha de todas as licenciaturas passa a ser a US48); épicos E1 a E4; o Sprint 4 fica com a US04 e as US33 a US36. |

O Excel do backlog acompanha esta versão. O ficheiro Word continua na versão 1.0.

## Anexo A — Requisitos das opcionais (arquivados a 27/10/2026)

Até 23/10 o OptaBem era também um recomendador de UCs opcionais. A 27/10, com autorização do docente, estes requisitos saíram do produto, porque: o OptaBem serve quem ainda está a escolher curso, e essa pessoa não tem opcionais para escolher; no ensino superior português a decisão com consequências é a candidatura, não as opcionais; e recomendar opcionais exige avaliações de muitos alunos do mesmo curso, que um protótipo da equipa nunca teria. Ficam aqui, com o texto da versão 1.8, para a rastreabilidade. As stories correspondentes estão na folha «Arquivo (opcionais)» do [backlog](product-backlog.xlsx), com o motivo de cada uma.

**Catálogo de UCs e percurso**

- **RF06** O administrador deve poder criar, editar e desativar UCs individualmente.
- **RF07** O aluno deve poder consultar o catálogo de opcionais do seu curso com descrição e estatísticas agregadas (médias de interesse, carga e dificuldade), sujeitas à regra de anonimato RN04.
- **RF08** O aluno deve poder indicar as UCs (obrigatórias e opcionais) que concluiu e o ano letivo/semestre em que as frequentou.
- **RF09** O sistema deve impedir registos duplicados da mesma UC no mesmo ano letivo.

**Avaliações e privacidade das avaliações**

- **RF10** O aluno deve poder avaliar cada UC opcional concluída em: interesse (1–5), carga de trabalho (1–5) e dificuldade (1–5).
- **RF11** O aluno deve poder avaliar UCs obrigatórias pelo menos em interesse (1–5), numa vista rápida em grelha.
- **RF12** O aluno pode acrescentar um comentário livre opcional (máx. 500 caracteres).
- **RF13** O aluno deve poder editar ou apagar as suas avaliações.
- **RF14** O administrador deve poder abrir e fechar períodos de avaliação por semestre.
- **RF15** As avaliações devem ser guardadas associadas a um identificador pseudonimizado, separado dos dados de identificação do aluno.
- **RF16** O sistema nunca deve mostrar avaliações individuais associadas a um autor.
- **RF18** O administrador deve poder ocultar comentários inapropriados ou que identifiquem pessoas.

**Motor de recomendação, filtros e explicação**

- **RF19** O sistema deve gerar, para cada aluno, uma lista ordenada top-N de opcionais recomendadas com uma pontuação prevista de interesse.
- **RF20** Para alunos sem dados suficientes, o sistema deve usar um fallback baseado na popularidade (média bayesiana de interesse).
- **RF21** O motor deve implementar filtragem colaborativa baseada em utilizadores (similaridade entre alunos com base nas avaliações comuns).
- **RF22** O motor deve permitir, como evolução, fatorização de matrizes (ex.: SVD).
- **RF23** A estratégia usada (baseline, user-based, SVD) deve ser configurável pelo administrador.
- **RF24** O sistema deve excluir das recomendações UCs que o aluno já concluiu ou que não estão disponíveis para o seu ano/curso.
- **RF25** O aluno deve poder filtrar recomendações por semestre e ECTS.
- **RF26** O aluno deve poder indicar a preferência de carga de trabalho (leve / indiferente / exigente), que ajusta a ordenação.
- **RF27** O sistema deve poder esconder opcionais sem vagas.
- **RF28** O aluno deve poder indicar o seu horário e o sistema deve excluir opcionais em conflito.
- **RF29** Cada recomendação deve apresentar uma justificação (ex.: *"6 alunos com gostos parecidos com os teus deram, em média, 4,3 de interesse"*).
- **RF30** O aluno deve poder marcar uma recomendação como útil / não útil ou ocultá-la.
- **RF31** O sistema deve permitir gerar um dataset sintético para testes.
- **RF32** O sistema deve correr uma avaliação offline (divisão treino/teste) e reportar RMSE, MAE, Precision@K e cobertura para cada estratégia.
- **RF33** O administrador deve ter um painel com indicadores de participação (nº de avaliações, nº de alunos, grau de esparsidade da matriz).

**Regras de negócio**

- **RN01** Um aluno só pode avaliar UCs que registou como concluídas no seu percurso.
- **RN02** Existe no máximo uma avaliação por aluno, por UC, por ano letivo.
- **RN03** Nunca se recomenda uma UC que o aluno já concluiu.
- **RN04** Estatísticas agregadas de uma UC só são mostradas quando há pelo menos 5 avaliações.
- **RN05** A recomendação personalizada só é usada quando o aluno tem pelo menos 3 UCs avaliadas e existem pelo menos 5 outros alunos com 2 ou mais UCs avaliadas em comum com ele; caso contrário, aplica-se o fallback de popularidade.
- **RN06** O critério principal de recomendação é o interesse; carga e dificuldade funcionam como ajuste/filtro segundo a preferência do aluno.
- **RN07** As avaliações são números inteiros de 1 a 5 (interesse, carga de trabalho e dificuldade, com o significado de cada extremo definido).
- **RN08** As explicações das recomendações só mostram o número de colegas semelhantes e a média deles quando contribuíram pelo menos 5 colegas.

**Pontos em aberto que eram das opcionais (secção 5 até à versão 1.8)**

| # | Ponto | Estado a 27/10 |
|---|---|---|
| 1 | Avaliar «dentro de um período aberto» antes de existirem períodos (RF14). | Arquivado sem decisão. |
| 2 | Gravar avaliações com `pseudo_id` desde o início. | Arquivado sem decisão. |
| 3 | Mínimo de 5 colegas nas explicações. | Resolvido na 1.1 (RN08) e arquivado. |
| 4 | Definição numérica da RN05. | Resolvido na 1.1 e arquivado. |
| 5 | Significado das escalas de 1 a 5. | Resolvido na 1.1 (RN07) e arquivado. |
| 6 | Requisitos sem story e stories sem requisito. | Fechado na 1.9 (secção 4). |
| 7 | A RN04 pode esconder quase tudo numa turma pequena. | Arquivado: foi um dos motivos para tirar as opcionais. |
