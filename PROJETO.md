# OptaBem — recomendador de cursos

Aplicação web que recomenda cursos do ensino superior com explicação, a partir de uma conversa com um assistente (LLM), e ajuda a preparar a candidatura ao concurso nacional com os dados da DGES. Ver a [visão do produto](docs/geral/00-visao-do-produto.md). O repositório mantém o nome antigo (`recomendador-ucs-opcionais`): até 27/10 o projeto incluía também a recomendação de opcionais, que foi arquivada.

Projeto 1 de Metodologias Ágeis (Scrum) · Duarte Eusébio e Simão Almeida

| | |
|---|---|
| **Sprint atual** | Sprint 3 concluído a 23/10 (7 SP: US05, US17) · Sprint 2 concluído a 22/10 (13 SP) · Sprint 1 concluído (10 SP) · Sprint 4 (29/10 a 05/11): US04, US33 a US36 e US40 a US45 (aceites pelo PO a 27/10) e US37 a US39, US46 e US47 (aceites a 29/10), 47 SP; revisão do Simão pendente · Entrega a 05/11 |
| **No repositório** | US01 — Registo com confirmação por ligação · US02 — Iniciar e terminar sessão · US03 — Perfis de aluno e administrador · US29 — Conversa de orientação com o LLM · US30 — Sugestão de cursos · US31 — Escolher curso e linha do tempo · US05 — Consultar e comparar cursos · US17 — Apagar a minha conta · Sprint 4 (aceites pelo PO a 27/10): US04, US33 a US36 e US40 a US45 · Sprint 4 (aceites pelo PO a 29/10, PR #50 a #54): US37, US38, US39, US46 e US47 |
| **Testes automáticos** | 436, todos a passar |

## Índice

1. [Estado do projeto](#1-estado-do-projeto)
2. [Documentação do projeto](#2-documentação-do-projeto)
3. [Alterar textos e cores](#3-alterar-textos-e-cores)
4. [Pôr a aplicação a correr](#4-pôr-a-aplicação-a-correr)
5. [Testes](#5-testes)
6. [Organização do código](#6-organização-do-código)
7. [Como contribuir](#7-como-contribuir)

## 1. Estado do projeto

**Sprint Goal do Sprint 1:** um aluno cria conta, entra e sai, e há um administrador com permissões próprias.

**Sprint 1 concluído a 07/10/2026:** 10 de 10 SP. As três stories estão no `main`, com testes e documentação.

**Replaneamento de 13/10/2026 (decisão dos Product Owners, com sugestões do docente):** o OptaBem passa a orientar também quem ainda não tem curso, com um catálogo de várias instituições e sugestões de curso feitas por um LLM. Entram as stories US29 a US31 e o resto do plano foi reordenado. Os números das stories ficam fixos a partir desta data; a tabela segue a ordem de trabalho. O detalhe está no [backlog](docs/geral/product-backlog.xlsx) e na [visão do produto](docs/geral/00-visao-do-produto.md).

| Sprint | Sprint Goal |
|---|---|
| Sprint 2 (13 SP, concluído a 22/10) | Uma pessoa indecisa conversa com o assistente (LLM), recebe 2 a 3 cursos do catálogo com explicação e escolhe um, ficando a decisão registada no percurso. |
| Sprint 3 (7 SP, concluído a 23/10) | Uma pessoa indecisa filtra, consulta e compara cursos de várias instituições, e pode apagar a sua conta e todos os seus dados. |
| Sprint 4 (29/10 a 05/11; alargado a 29/10) | Quem escolheu um curso prepara a candidatura: vê as condições de acesso, a tendência e a procura de cada curso, indica as suas notas, vê a sua nota em cada curso e quanto precisa nos exames, ordena as 6 opções, descobre que exames lhe abrem mais portas, tem um plano B para a 2.ª fase e pode partilhar o plano; o catálogo passa a ter as licenciaturas recolhidas da DGES (US04, US33 a US36 e US40 a US45, 32 SP). A 29/10 entram a exportação dos dados, a recuperação da palavra-passe por email, a correção do catálogo na gestão, as datas do concurso e um assistente que conhece as notas (US37 a US39, US46 e US47, mais 15 SP): 47 SP. O código fecha por volta de 03/11. |

**Replaneamento de 14/10/2026 (decisão do PO, issue #15):** o LLM conduz a conversa de orientação (sem perguntas fixas) e passa para o Sprint 2; o plano passa a respeitar a velocidade real (10 SP por sprint). A US32 foi fundida na US29; US04, US09 e US11 passam para o backlog. Ver o [spike do LLM](docs/geral/05-spike-llm.md).

**Sprint Planning do Sprint 2 (20/10/2026, decisão do PO):** a US29 e a US30 foram feitas antes de o sprint começar, por isso entra a US31 (antecipada do Sprint 3). O ponto 14 dos requisitos fica decidido: o OptaBem é um protótipo usado pela equipa e na demonstração, com aviso de 18+ na conversa. O servidor Ollama da faculdade foi testado e posto de parte ([spike](docs/geral/05-spike-llm.md), secção 7).

**Sprint Review do Sprint 2 (22/10/2026, decisão dos Product Owners):** 13 de 13 SP. O percurso completo (conversa com o Gemini real, sugestões, escolha do curso e linha do tempo) foi testado pelos dois Product Owners, também noutro computador através de um túnel ([abrir noutro dispositivo](docs/geral/06-aceder-noutro-dispositivo.md)), e as três stories foram aceites. Os Product Owners decidiram também que, até à entrega de 05/11, o centro do produto são os cursos e as opcionais passam para segundo plano: nesta release o percurso termina na escolha do curso. O plano dos Sprints 3 e 4 vai ser revisto no próximo Sprint Planning.

**Sprint Planning do Sprint 3 (22/10/2026, decisão do PO):** sprints de uma semana até à entrega (Sprint 3 de 22/10 a 29/10, Sprint 4 de 29/10 a 05/11). O Sprint 3 tem a US05 e a US17, que sobe do backlog e passa a Must porque o OptaBem já guarda conversas e decisões de pessoas (reduzida no mesmo dia ao apagamento da conta; a exportação fica no backlog). A US06 e a US07 (opcionais) saem do Sprint 4 para o backlog. A story do Sprint 4 fica por decidir com o docente (preparar o percurso depois da escolha do curso, ou perguntas e respostas por curso). A revisão de 22/10 (segurança do túnel, menu do aluno e textos) fica adiada; até lá, o túnel é só para a equipa.

**Sprint Review do Sprint 3 (23/10/2026, decisão dos Product Owners):** 7 de 7 SP. A US05 (filtros, ficha e comparação, com as melhorias da revisão do PR #37) e a US17 (apagar a conta) foram testadas pelos dois Product Owners e aceites. O sprint fecha antes de 29/10 porque o objetivo foi cumprido; entrou também, sem story, o menu fixo no topo (PR #40). Um teste da US17 dependia da data em que corria e foi corrigido no fecho. O Sprint 4 fica por planear, com a story a decidir com o docente.

**Replaneamento de 23/10/2026 (decisão do PO, com o protótipo do PR #44):** o **plano de candidatura** ao Concurso Nacional de Acesso substitui as opcionais (épico E12): condições de acesso na ficha (US33), notas do candidato (US34), nota de candidatura a cada curso (US35) e as 6 opções com avisos (US36), mais US37 e US38 no backlog. A US04 foi reescrita (catálogo da DGES por recolha) e entra no Sprint 4; a US39 (gestão do catálogo) nasce da sugestão de um colega de editar a base de dados na área de gestão. As 22 stories das opcionais passam a *Won't* (fase 2). O Sprint 4 fica com 18 SP planeados, acima da velocidade (10): o código das US33 a US36 foi feito antes do sprint, como protótipo; se for demais, a US36 sai primeiro. Sem story: o registo pede o nome, terminar sessão volta à página inicial, a gestão ativa contas por confirmar e «As minhas decisões» sai do menu (PR #43 e #44). No mesmo dia entraram as US40 a US43 (quanto preciso no exame, tendência, procura e partilhar o plano): e, ao fim do dia, as US44 (que exames me abrem mais portas) e US45 (plano B da 2.ª fase). O Sprint 4 passa a 32 SP planeados, muito acima da velocidade (10): o código foi feito antes do sprint, como protótipo, e no Sprint Planning de 29/10 decide-se o que entra; o resto volta ao backlog. Falta a documentação por story.

**Reestruturação do backlog (27/10/2026, autorizada pelo docente; decisão do PO):** o OptaBem passa a ser só um recomendador de cursos. As 22 stories das opcionais e a US32 (fundida) saem do Product Backlog para a folha «Arquivo (opcionais)», com o motivo de cada uma; os requisitos correspondentes passam para o anexo A dos [requisitos](docs/geral/01-requisitos-funcionais-e-nao-funcionais.md) (versão 1.9). Épicos novos: E1 Conta e privacidade, E2 Catálogo de cursos, E3 Orientação com o assistente, E4 Plano de candidatura. O Sprint 4 fica com o essencial (US04 e US33 a US36, 18 SP); as US40 a US45 voltam ao backlog com o código pronto, no estado novo «Protótipo». Stories novas no backlog: US46 (exportar os meus dados) e US47 (recuperar a palavra-passe). A US04 foi dividida: fica o catálogo com os 174 cursos já recolhidos da DGES, e a recolha de todas as licenciaturas passa a ser a US48, porque exige o computador ligado uma noite inteira. Mesmo assim, o Sprint 4 passa a velocidade (18 para 10 SP), o que só se justifica porque o código foi feito antes, como protótipo.

**Sprint 4 alargado (27/10/2026, mais tarde; decisão do PO):** as US40 a US45 voltam ao Sprint 4, porque são partes importantes do produto e o código já está feito. O Sprint 4 passa a 32 SP para uma velocidade de 10: não é um planeamento realista de trabalho novo, e só se defende porque o código foi feito antes do sprint, como protótipo; no sprint sobra documentação, testes, revisão e aceitação. A documentação das stories do Sprint 4 está em `docs/USNN/`.

**Verificação e aceitação do Sprint 4 (27/10/2026, decisão do PO):** antes de aceitar, as 11 stories foram verificadas com o catálogo real (174 cursos). Encontraram-se e corrigiram-se dois erros: os cursos do ensino privado entravam no plano do concurso nacional (nova RN12) e as Matemáticas só ligavam a prova 16 à 19 (correspondência completa da DGES: a Matemática A dá as provas 16, 17 e 19, a Matemática B a 16 e a 17, o MACS a 17). Depois disso, o PO aceitou as 11 stories (32 de 32 SP). A aceitação aconteceu antes da data de início marcada para o sprint (29/10) e com a revisão do Simão ainda pendente.

**Sprint 4 alargado de novo (29/10/2026, decisão do PO):** a 29/10, o Claude fez o código das stories do backlog que ainda não o tinham (US37, US38, US39, US46 e US47), uma por ramo, com testes para cada critério e a documentação em `docs/USNN/` (PR #50 a #54). O PO testou-as no seu computador, com o envio real de emails, e pô-las no Sprint 4 como «Feito»: 47 SP para uma velocidade de 10. Não é um planeamento à velocidade: o código foi feito pela IA num dia, e o trabalho da equipa é rever, testar e aceitar; fica no relatório. A US48 fica no Backlog. Sem story: textos antigos das opcionais (PR #55) e o visual calmo, com menos texto à vista e a letra do sistema (PR #56, a juntar por último).

| User story | Título | Sprint | Estado | Documentação |
|---|---|---|---|---|
| US01 | Registo com email pessoal (desde 23/10 pede também o nome) | Sprint 1 | Feita | [docs/US01/](docs/US01/) |
| US02 | Autenticação | Sprint 1 | Feita | [docs/US02/](docs/US02/) |
| US03 | Perfis de aluno e administrador (revista a 14/10: um só início de sessão) | Sprint 1 | Feita | [docs/US03/](docs/US03/) |
| US29 | Conversa de orientação com o LLM (reescrita a 14/10: sem perguntas fixas) | Sprint 2 | Feita | [docs/US29/](docs/US29/) |
| US30 | Sugestão de 2 a 3 cursos no fim da conversa | Sprint 2 | Feita | [docs/US30/](docs/US30/) |
| US31 | Escolher curso e linha do tempo do percurso (antecipada a 20/10; fora do menu desde 23/10) | Sprint 2 | Feita | [docs/US31/](docs/US31/) |
| US05 | Consultar e comparar cursos | Sprint 3 | Feita | [docs/US05/](docs/US05/) |
| US17 | Apagar a minha conta (reduzida a 22/10: a exportação fica no backlog) | Sprint 3 | Feita | [docs/US17/](docs/US17/) |
| US04 | Catálogo de licenciaturas recolhido da DGES (dividida a 27/10) | Sprint 4 | Feita (aceite pelo PO a 27/10) | [docs/US04/](docs/US04/) · PR #44 |
| US33 | Condições de acesso na ficha do curso | Sprint 4 | Feita (aceite pelo PO a 27/10) | [docs/US33/](docs/US33/) · PR #44 |
| US34 | Registar as minhas notas | Sprint 4 | Feita (aceite pelo PO a 27/10) | [docs/US34/](docs/US34/) · PR #44 |
| US35 | Nota de candidatura a cada curso | Sprint 4 | Feita (aceite pelo PO a 27/10) | [docs/US35/](docs/US35/) · PR #44 |
| US36 | Plano das 6 opções de candidatura | Sprint 4 | Feita (aceite pelo PO a 27/10) | [docs/US36/](docs/US36/) · PR #44 |
| US40 | Quanto preciso no exame? | Sprint 4 | Feita (aceite pelo PO a 27/10) | [docs/US40/](docs/US40/) · PR #44 |
| US41 | Tendência do último colocado | Sprint 4 | Feita (aceite pelo PO a 27/10) | [docs/US41/](docs/US41/) · PR #44 |
| US42 | Procura do curso | Sprint 4 | Feita (aceite pelo PO a 27/10) | [docs/US42/](docs/US42/) · PR #44 |
| US44 | Que exames me abrem mais portas? | Sprint 4 | Feita (aceite pelo PO a 27/10) | [docs/US44/](docs/US44/) · PR #44 |
| US43 | Partilhar o plano | Sprint 4 | Feita (aceite pelo PO a 27/10) | [docs/US43/](docs/US43/) · PR #44 |
| US45 | Plano B: 2.ª fase | Sprint 4 | Feita (aceite pelo PO a 27/10) | [docs/US45/](docs/US45/) · PR #44 |
| US37 | Assistente que conhece as minhas notas | Sprint 4 | Feita (aceite pelo PO a 29/10) | [docs/US37/](docs/US37/) · PR #54 |
| US46 | Exportar os meus dados | Sprint 4 | Feita (aceite pelo PO a 29/10) | [docs/US46/](docs/US46/) · PR #50 |
| US47 | Recuperar a palavra-passe | Sprint 4 | Feita (aceite pelo PO a 29/10) | [docs/US47/](docs/US47/) · PR #51 |
| US39 | Corrigir e esconder cursos do catálogo (gestão) | Sprint 4 | Feita (aceite pelo PO a 29/10) | [docs/US39/](docs/US39/) · PR #53 |
| US38 | Datas do concurso no percurso | Sprint 4 | Feita (aceite pelo PO a 29/10) | [docs/US38/](docs/US38/) · PR #52 |
| US48 | Recolha completa das licenciaturas (DGES) | Backlog | Por fazer | — |

*Protótipo* = código feito antes do sprint, ainda não aceite numa Sprint Review. As stories das opcionais (US06 a US16, US18 a US28) e a US32 (fundida na US29) estão na folha «Arquivo (opcionais)» do [backlog](docs/geral/product-backlog.xlsx).

Cada story tem a sua pasta `docs/USNN/` quando é desenvolvida (para já, US01 a US05, US17, US29 a US31, US33 a US47, exceto a US48).

## 2. Documentação do projeto

O índice completo está em [docs/README.md](docs/README.md). Os documentos gerais ficam em `docs/geral/` e cada user story tem a sua pasta `docs/USNN/`.

| Documento | O que contém |
|---|---|
| [Visão do produto](docs/geral/00-visao-do-produto.md) | Para quem é o OptaBem, o percurso como sequência de decisões, âmbito do MVP e metas |
| [Requisitos funcionais e não funcionais](docs/geral/01-requisitos-funcionais-e-nao-funcionais.md) | Todos os requisitos (RF, RNF), regras de negócio e ligação às user stories |
| [Regras de geração de código](docs/geral/02-regras-de-geracao-de-codigo.md) | Como a equipa escreve, testa e revê código (incluindo com IA) |
| [Arquitetura e padrões de desenho](docs/geral/03-arquitetura-e-padroes.md) | Tecnologias e porquê, padrões que o código já usa e os previstos (Strategy, Adapter, Factory, Decorator…) |
| [Guia do código](docs/geral/04-guia-do-codigo.md) | Onde está cada coisa (incluindo o CSS), onde mexer para alterar, quem escreveu o quê |
| [Spike do LLM](docs/geral/05-spike-llm.md) | Gemini e Groq: limites do plano gratuito, custo, privacidade, termos e viabilidade (14/10) |
| [Abrir noutro dispositivo](docs/geral/06-aceder-noutro-dispositivo.md) | Usar o OptaBem no telemóvel ou noutro computador com um túnel do Cloudflare, sem modo debug (22/10) |
| [Catálogo de cursos](dados/README.md) | Catálogo do MVP (30 licenciaturas) e catálogo completo recolhido da DGES (US04), com as condições de acesso do plano de candidatura |
| [Registo de uso de IA](docs/geral/registo-de-uso-de-ia.md) | Cada utilização relevante de IA no projeto |
| [Product Backlog (Excel)](docs/geral/product-backlog.xlsx) | Todas as stories, plano de sprints com gráfico e resumo MoSCoW |
| [US01](docs/US01/README.md) | Requisitos, use case, BPMN, prompt e diagramas da US01 |
| [US02](docs/US02/README.md) | Requisitos, use case, BPMN, prompt e diagramas da US02 |
| [US03](docs/US03/README.md) | Administradores e área de gestão: requisitos, use case, BPMN e como criar o primeiro administrador |
| [US29](docs/US29/README.md) | Conversa de orientação com o LLM: requisitos, use case, BPMN e como experimentar |
| [US30](docs/US30/README.md) | Sugestão de 2 a 3 cursos no fim da conversa: requisitos, use case, BPMN e como experimentar |
| [US31](docs/US31/README.md) | Escolher curso e linha do tempo do percurso: requisitos, use case, BPMN e como experimentar |
| [US05](docs/US05/README.md) | Consultar e comparar cursos: filtros, ficha completa e comparação de até 3 cursos |
| [US17](docs/US17/README.md) | Apagar a minha conta e todos os dados, com confirmação pela palavra-passe |
| [US04](docs/US04/README.md) | Catálogo recolhido da DGES: script de recolha, paginação e filtro por área no assistente |
| [US33](docs/US33/README.md) | Condições de acesso na ficha do curso |
| [US34](docs/US34/README.md) | Registar as minhas notas (média e exames) |
| [US35](docs/US35/README.md) | Nota de candidatura a cada curso e situação face ao último colocado |
| [US36](docs/US36/README.md) | Plano das 6 opções de candidatura, com avisos e sugestões |
| [US40](docs/US40/README.md) | Quanto preciso no exame? |
| [US41](docs/US41/README.md) | Tendência do último colocado (2023 a 2025) |
| [US42](docs/US42/README.md) | Procura do curso (1.ª fase de 2025) |
| [US44](docs/US44/README.md) | Que exames me abrem mais portas? |
| [US43](docs/US43/README.md) | Partilhar o plano com uma ligação só de leitura |
| [US45](docs/US45/README.md) | Plano B: 2.ª fase |
| [US37](docs/US37/README.md) | Assistente que conhece as minhas notas (só com autorização) |
| [US38](docs/US38/README.md) | Datas do concurso nacional no início e no plano |
| [US39](docs/US39/README.md) | Corrigir e esconder cursos do catálogo na gestão |
| [US46](docs/US46/README.md) | Exportar os meus dados num ficheiro JSON |
| [US47](docs/US47/README.md) | Recuperar a palavra-passe por email |

## 3. Alterar textos e cores

Para mudanças pequenas não é preciso mexer no código da aplicação.

| Quero mudar… | Ficheiro | Como |
|---|---|---|
| O nome da aplicação (topo e separador do navegador) | [`app/texts.py`](app/texts.py) | Muda o texto de `APP_NAME` |
| Títulos, frases, botões ou mensagens de erro | [`app/texts.py`](app/texts.py) | Procura o texto (Ctrl+F) e muda o que está entre aspas |
| O email de confirmação | [`app/texts.py`](app/texts.py) | `CONFIRMATION_EMAIL_SUBJECT` e `CONFIRMATION_EMAIL_BODY` |
| O texto da política de privacidade | [`app/texts.py`](app/texts.py) | `PRIVACY_BODY` |
| As cores | [`app/static/style.css`](app/static/style.css) | As primeiras linhas do ficheiro; cada cor tem um comentário a dizer onde aparece |
| Exigir um domínio de email (ex.: só institucional), versão da política, prazo da ligação | [`app/config.py`](app/config.py) | Exige cuidado: fala com quem desenvolve |

Ao editar `app/texts.py`:

- muda **só o que está entre aspas**, nunca o nome em maiúsculas à esquerda;
- palavras entre chavetas, como `{email}` ou `{horas}`, são preenchidas pela aplicação: podem mudar de sítio na frase, mas não podem ser apagadas;
- depois de guardar, recarrega a página no navegador e corre os testes (secção 5). Se um marcador entre chavetas tiver sido apagado por engano, um teste avisa.

## 4. Pôr a aplicação a correr

Precisas de **Python 3.10 ou superior** e de **Git**.

```bash
git clone https://github.com/Simaooo27/recomendador-ucs-opcionais.git
cd recomendador-ucs-opcionais

python -m venv .venv
source .venv/bin/activate              # Windows (PowerShell): .venv\Scripts\Activate.ps1
pip install -r requirements.txt

export SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")
# Windows (PowerShell): $env:SECRET_KEY = python -c "import secrets; print(secrets.token_hex(32))"

flask --app app init-db                # cria as tabelas (pode repetir: não apaga dados; repetir quando há tabelas novas)
flask --app app run --debug
```

Abre http://127.0.0.1:5000: aparece o início de sessão, com uma ligação para criar conta. Em desenvolvimento não é enviado nenhum email: a ligação de confirmação aparece **na própria página «Confirme o seu email»** (caixa amarela) e no terminal onde a aplicação está a correr.

**Administradores (US03):** têm contas próprias, sem email, numa área que não aparece nas páginas dos alunos. O primeiro cria-se no terminal e depois entra-se na mesma página dos alunos, http://127.0.0.1:5000/auth/entrar, com o nome de utilizador no campo do email (ver [docs/US03/](docs/US03/README.md)):

```bash
flask --app app create-admin    # pede o nome e a palavra-passe
```

**Enviar emails a sério (confirmação de conta e recuperação da palavra-passe, US47):** por omissão os emails só aparecem no terminal. Para os enviar, usar uma conta de email da equipa (por exemplo, uma conta Gmail com a verificação em dois passos ligada e uma **palavra-passe de aplicação**, criada nas definições de segurança da conta Google) e acrescentar ao `.env`:

```ini
MAIL_BACKEND=smtp
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=conta.da.equipa@gmail.com
MAIL_PASSWORD=a-palavra-passe-de-aplicacao
MAIL_SENDER=conta.da.equipa@gmail.com
SHOW_DEV_CONFIRMATION_LINK=false
```

Depois de mudar o `.env`, parar a aplicação (Ctrl+C) e voltar a arrancá-la. A palavra-passe de aplicação fica só no `.env`, que não vai para o repositório; nunca a colar em mensagens, issues ou pedidos à IA.

<details>
<summary>Outras configurações (variáveis de ambiente)</summary>

A aplicação lê variáveis de ambiente (ver [`.env.example`](.env.example)). Só a `SECRET_KEY` é obrigatória. O comando `flask` lê-as também do ficheiro `.env`.

Para experimentar o LLM com a chave real (2 pedidos; a chave nunca é mostrada): `flask --app app llm-teste --backend gemini`.

| Variável | Para quê | Por omissão |
|---|---|---|
| `SECRET_KEY` | Assinar sessões e ligações de confirmação | obrigatória |
| `ALLOWED_EMAIL_DOMAINS` | Restringe o registo a estes domínios (inclui subdomínios). Vazio = qualquer email | vazio |
| `DATABASE_PATH` | Ficheiro SQLite | `instance/app.sqlite3` |
| `MAIL_BACKEND` | `console` (escreve o email no terminal) ou `smtp` | `console` |
| `MAIL_SERVER`, `MAIL_PORT`, `MAIL_USERNAME`, `MAIL_PASSWORD`, `MAIL_USE_TLS`, `MAIL_SENDER` | Só para `smtp` (ver «Enviar emails a sério», acima) | |
| `SHOW_DEV_CONFIRMATION_LINK` | Com `console`, mostrar a ligação de confirmação na página. `false` no túnel: fica só no terminal | `true` |
| `SESSION_COOKIE_SECURE` | `true` em produção ou pelo túnel (HTTPS); com isto ligado, a aplicação recusa o modo debug | `false` |
| `ADMIN_URL_PREFIX` | Endereço da área de gestão (administradores) | `gestao` |
| `LLM_BACKEND` | LLM da orientação: `falso` (sem rede), `gemini` ou `groq` | `falso` |
| `LLM_MODELO` | Outro modelo do fornecedor | `gemini-3.5-flash-lite` / `openai/gpt-oss-120b` |
| `GEMINI_API_KEY`, `GROQ_API_KEY` | Chaves pessoais dos fornecedores (só no `.env`, nunca no repositório) | vazias |
| `ORIENTACAO_MAX_PEDIDOS_DIA` | Pedidos ao LLM por aluno e por dia (`0` = sem limite) | `40` |
| `CALENDARIO_CSV` | Datas do concurso nacional (US38) | `dados/calendario-concurso.csv` |

</details>

## 5. Testes

```bash
python -m unittest discover -s tests -t . -v
```

Os testes não precisam de rede nem de configuração. Também correm com `pytest` (`pip install -r requirements-dev.txt`).

| Ficheiro | O que verifica |
|---|---|
| `tests/test_registration.py` | Formulário de registo, contas duplicadas, falha no envio do email, CSRF |
| `tests/test_confirmation.py` | Ligação de confirmação: válida, repetida, adulterada, expirada |
| `tests/test_login.py` | Iniciar e terminar sessão, mensagem genérica, páginas privadas |
| `tests/test_gestao.py` | Administradores: contas separadas, primeiro administrador, área de gestão escondida |
| `tests/test_validators.py` | Regras do email e da palavra-passe |
| `tests/test_texts.py` | Ficheiro de textos: nada vazio e marcadores `{…}` no sítio |
| `tests/test_app_factory.py` | Arranque e configuração da aplicação |
| `tests/test_llm.py` | Ligação ao LLM: fábrica, adaptadores Gemini e Groq (sem rede), chave nunca exposta, dados pessoais apagados |
| `tests/test_orientacao.py` | Conversa de orientação: formato das respostas, só cursos do catálogo (RN09), limite de perguntas, comando `llm-teste` |
| `tests/test_conversa.py` | Página da conversa (US29): sessão, perguntas do LLM, dados pessoais, falhas e «Tentar de novo», recomeçar |
| `tests/test_sugestoes.py` | Cursos sugeridos (US30): dados do catálogo e explicação, só cursos do catálogo, «Ver sugestões já», poucos cursos, página `/cursos/` |
| `tests/test_site_publico.py` | Site aberto pelo túnel: modo debug recusado, ligação de confirmação escondida (página e cookie), limite de pedidos ao LLM por aluno e por dia |
| `tests/test_navegacao.py` | Menu dos alunos e página atual marcada, logótipo com ligação, saudação, passos concluídos, estilo do campo de pesquisa |
| `tests/test_escolha.py` | Escolher curso (US31): confirmação, curso no perfil, decisões com data e sugeridos, conversa apagada, linha do tempo, mudar de curso |

## 6. Organização do código

Explicação completa, ficheiro a ficheiro, no [Guia do código](docs/geral/04-guia-do-codigo.md).

```
app/
  texts.py          todos os textos que o utilizador vê
  static/style.css  aspeto e cores
  templates/        páginas HTML (usam os textos de texts.py)
  auth/             contas: registo e confirmação (US01), iniciar e terminar sessão (US02)
    routes.py         recebe os pedidos do navegador e devolve as páginas
    services.py       regras do registo, da confirmação e da autenticação
    sessions.py       quem tem a sessão iniciada; proteção das páginas privadas
    validators.py     validação do email e da palavra-passe
    repository.py     acesso à base de dados
    tokens.py         ligações de confirmação assinadas
  config.py         configuração (variáveis de ambiente)
  db.py, schema.sql base de dados SQLite
  security.py       proteção CSRF e cabeçalhos de segurança
  mailer.py         envio de email (terminal ou SMTP)
  main.py           página inicial do aluno e política de privacidade
  llm/              ligação ao LLM (Gemini, Groq, falso), escolhido por LLM_BACKEND
  orientacao/       conversa de orientação conduzida pelo LLM (US29, US30), limite de pedidos por aluno e comando llm-teste
  percurso/         em que passo está cada aluno (State) e as decisões: escolher curso, linha do tempo (US31)
  candidatura/      plano de candidatura (protótipo de 23/10): contas da nota de candidatura e as 6 opções
  gestao/           área de gestão (administradores, US03); endereço em ADMIN_URL_PREFIX
    routes.py         entrar, sair, painel e lista de administradores
    services.py       criar, autenticar e remover administradores
    sessions.py       sessão de administrador e proteção das páginas
    cli.py            comandos create-admin e list-admins
tests/              testes automáticos
docs/               documentação (índice em docs/README.md)
dados/              catálogo de instituições e cursos (dados públicos, ver dados/README.md) e recolha da DGES (recolher_dges.py)
ferramentas/        arrancar o site no Windows (arrancar.ps1, arrancar-tunel.ps1, configurar.ps1, admin.ps1)
  geral/            visão, requisitos, regras de código, arquitetura e registo de uso de IA
  US01/             requisitos, use case, BPMN, prompt e diagramas da US01
  US02/             o mesmo para a US02
  US03/             o mesmo para a US03
  USNN/             uma pasta por cada nova story, com a mesma estrutura
.github/            modelos de issue (user story) e de Pull Request
instance/           dados locais (ignorado pelo Git)
```

## 7. Como contribuir

1. Cada story tem uma issue criada com o modelo [User story](.github/ISSUE_TEMPLATE/user-story.md).
2. Um ramo por story: `feature/US02-autenticacao`.
3. A documentação da story fica em `docs/USNN/` (por exemplo, `docs/US02/`), com a mesma estrutura da [US01](docs/US01/README.md): `README.md`, `requisitos.md`, `use-case.md`, `bpmn.md`, `prompt.md` e `diagramas/`. Acrescente a pasta ao [índice](docs/README.md) e atualize a tabela de [estado do projeto](#1-estado-do-projeto).
4. Commits no formato `US02: <resumo no imperativo>`.
5. Pull Request com o [modelo do repositório](.github/pull_request_template.md), que inclui a checklist da secção 10 de [docs/geral/02-regras-de-geracao-de-codigo.md](docs/geral/02-regras-de-geracao-de-codigo.md), revisto por outro elemento.
6. Textos visíveis ao utilizador vão sempre para [`app/texts.py`](app/texts.py), nunca escritos diretamente nos templates.
7. Cada utilização relevante de IA fica anotada em [docs/geral/registo-de-uso-de-ia.md](docs/geral/registo-de-uso-de-ia.md).
