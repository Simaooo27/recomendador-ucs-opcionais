# OptaBem — recomendador de cursos

Aplicação web que recomenda cursos do ensino superior com explicação, a partir de uma conversa com um assistente (LLM), e ajuda a preparar a candidatura ao concurso nacional com os dados da DGES. Ver a [visão do produto](docs/geral/00-visao-do-produto.md). O repositório mantém o nome antigo (`recomendador-ucs-opcionais`): até 27/10 o projeto incluía também a recomendação de opcionais, que foi arquivada.

Projeto 1 de Metodologias Ágeis (Scrum) · Duarte Eusébio e Simão Almeida

| | |
|---|---|
| **Sprint atual** | Sprint 3 concluído a 23/10 (7 SP: US05, US17) · Sprint 2 concluído a 22/10 (13 SP) · Sprint 1 concluído (10 SP) · Sprint 4 (29/10 a 05/11) proposto a 27/10: US04 e US33 a US36, 18 SP, a confirmar com o docente · Entrega a 05/11 |
| **No repositório** | US01 — Registo com confirmação por ligação · US02 — Iniciar e terminar sessão · US03 — Perfis de aluno e administrador · US29 — Conversa de orientação com o LLM · US30 — Sugestão de cursos · US31 — Escolher curso e linha do tempo · US05 — Consultar e comparar cursos · US17 — Apagar a minha conta |
| **Testes automáticos** | 337, todos a passar |

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
| Sprint 4 (29/10 a 05/11, proposto a 27/10) | Quem escolheu um curso prepara a candidatura: vê as condições de acesso de cada curso, indica as suas notas, vê a sua nota de candidatura em cada curso e ordena as 6 opções; o catálogo passa a ter as licenciaturas da DGES (US04 e US33 a US36, 18 SP; a confirmar no Sprint Planning de 29/10 com o docente). O código fecha por volta de 03/11. |

**Replaneamento de 14/10/2026 (decisão do PO, issue #15):** o LLM conduz a conversa de orientação (sem perguntas fixas) e passa para o Sprint 2; o plano passa a respeitar a velocidade real (10 SP por sprint). A US32 foi fundida na US29; US04, US09 e US11 passam para o backlog. Ver o [spike do LLM](docs/geral/05-spike-llm.md).

**Sprint Planning do Sprint 2 (20/10/2026, decisão do PO):** a US29 e a US30 foram feitas antes de o sprint começar, por isso entra a US31 (antecipada do Sprint 3). O ponto 14 dos requisitos fica decidido: o OptaBem é um protótipo usado pela equipa e na demonstração, com aviso de 18+ na conversa. O servidor Ollama da faculdade foi testado e posto de parte ([spike](docs/geral/05-spike-llm.md), secção 7).

**Sprint Review do Sprint 2 (22/10/2026, decisão dos Product Owners):** 13 de 13 SP. O percurso completo (conversa com o Gemini real, sugestões, escolha do curso e linha do tempo) foi testado pelos dois Product Owners, também noutro computador através de um túnel ([abrir noutro dispositivo](docs/geral/06-aceder-noutro-dispositivo.md)), e as três stories foram aceites. Os Product Owners decidiram também que, até à entrega de 05/11, o centro do produto são os cursos e as opcionais passam para segundo plano: nesta release o percurso termina na escolha do curso. O plano dos Sprints 3 e 4 vai ser revisto no próximo Sprint Planning.

**Sprint Planning do Sprint 3 (22/10/2026, decisão do PO):** sprints de uma semana até à entrega (Sprint 3 de 22/10 a 29/10, Sprint 4 de 29/10 a 05/11). O Sprint 3 tem a US05 e a US17, que sobe do backlog e passa a Must porque o OptaBem já guarda conversas e decisões de pessoas (reduzida no mesmo dia ao apagamento da conta; a exportação fica no backlog). A US06 e a US07 (opcionais) saem do Sprint 4 para o backlog. A story do Sprint 4 fica por decidir com o docente (preparar o percurso depois da escolha do curso, ou perguntas e respostas por curso). A revisão de 22/10 (segurança do túnel, menu do aluno e textos) fica adiada; até lá, o túnel é só para a equipa.

**Sprint Review do Sprint 3 (23/10/2026, decisão dos Product Owners):** 7 de 7 SP. A US05 (filtros, ficha e comparação, com as melhorias da revisão do PR #37) e a US17 (apagar a conta) foram testadas pelos dois Product Owners e aceites. O sprint fecha antes de 29/10 porque o objetivo foi cumprido; entrou também, sem story, o menu fixo no topo (PR #40). Um teste da US17 dependia da data em que corria e foi corrigido no fecho. O Sprint 4 fica por planear, com a story a decidir com o docente.

**Replaneamento de 23/10/2026 (decisão do PO, com o protótipo do PR #44):** o **plano de candidatura** ao Concurso Nacional de Acesso substitui as opcionais (épico E12): condições de acesso na ficha (US33), notas do candidato (US34), nota de candidatura a cada curso (US35) e as 6 opções com avisos (US36), mais US37 e US38 no backlog. A US04 foi reescrita (catálogo da DGES por recolha) e entra no Sprint 4; a US39 (gestão do catálogo) nasce da sugestão de um colega de editar a base de dados na área de gestão. As 22 stories das opcionais passam a *Won't* (fase 2). O Sprint 4 fica com 18 SP planeados, acima da velocidade (10): o código das US33 a US36 foi feito antes do sprint, como protótipo; se for demais, a US36 sai primeiro. Sem story: o registo pede o nome, terminar sessão volta à página inicial, a gestão ativa contas por confirmar e «As minhas decisões» sai do menu (PR #43 e #44). No mesmo dia entraram as US40 a US43 (quanto preciso no exame, tendência, procura e partilhar o plano): e, ao fim do dia, as US44 (que exames me abrem mais portas) e US45 (plano B da 2.ª fase). O Sprint 4 passa a 32 SP planeados, muito acima da velocidade (10): o código foi feito antes do sprint, como protótipo, e no Sprint Planning de 29/10 decide-se o que entra; o resto volta ao backlog. Falta a documentação por story.

**Reestruturação do backlog (27/10/2026, autorizada pelo docente; decisão do PO):** o OptaBem passa a ser só um recomendador de cursos. As 22 stories das opcionais e a US32 (fundida) saem do Product Backlog para a folha «Arquivo (opcionais)», com o motivo de cada uma; os requisitos correspondentes passam para o anexo A dos [requisitos](docs/geral/01-requisitos-funcionais-e-nao-funcionais.md) (versão 1.9). Épicos novos: E1 Conta e privacidade, E2 Catálogo de cursos, E3 Orientação com o assistente, E4 Plano de candidatura. O Sprint 4 fica com o essencial (US04 e US33 a US36, 18 SP); as US40 a US45 voltam ao backlog com o código pronto, no estado novo «Protótipo». Stories novas no backlog: US46 (exportar os meus dados) e US47 (recuperar a palavra-passe). A US04 foi dividida: fica o catálogo com os 174 cursos já recolhidos da DGES, e a recolha de todas as licenciaturas passa a ser a US48, porque exige o computador ligado uma noite inteira. Mesmo assim, o Sprint 4 passa a velocidade (18 para 10 SP), o que só se justifica porque o código foi feito antes, como protótipo.

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
| US04 | Catálogo de licenciaturas recolhido da DGES (dividida a 27/10) | Sprint 4 | Protótipo | PR #44 |
| US33 | Condições de acesso na ficha do curso | Sprint 4 | Protótipo | PR #44 |
| US34 | Registar as minhas notas | Sprint 4 | Protótipo | PR #44 |
| US35 | Nota de candidatura a cada curso | Sprint 4 | Protótipo | PR #44 |
| US36 | Plano das 6 opções de candidatura | Sprint 4 | Protótipo | PR #44 |
| US40 | Quanto preciso no exame? | Backlog | Protótipo | PR #44 |
| US41 | Tendência do último colocado | Backlog | Protótipo | PR #44 |
| US42 | Procura do curso | Backlog | Protótipo | PR #44 |
| US44 | Que exames me abrem mais portas? | Backlog | Protótipo | PR #44 |
| US37 | Assistente que conhece as minhas notas | Backlog | Por fazer | — |
| US46 | Exportar os meus dados | Backlog | Por fazer | — |
| US47 | Recuperar a palavra-passe | Backlog | Por fazer | — |
| US48 | Recolha completa das licenciaturas (DGES) | Backlog | Por fazer | — |
| US39 | Corrigir e esconder cursos do catálogo (gestão) | Backlog | Por fazer | — |
| US43 | Partilhar o plano | Backlog | Protótipo | PR #44 |
| US45 | Plano B: 2.ª fase | Backlog | Protótipo | PR #44 |
| US38 | Datas do concurso no percurso | Backlog | Por fazer | — |

*Protótipo* = código feito antes do sprint, ainda não aceite numa Sprint Review. As stories das opcionais (US06 a US16, US18 a US28) e a US32 (fundida na US29) estão na folha «Arquivo (opcionais)» do [backlog](docs/geral/product-backlog.xlsx).

Cada story tem a sua pasta `docs/USNN/` quando é desenvolvida (para já, US01 a US03 e US29 a US31).

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
| `MAIL_SERVER`, `MAIL_PORT`, `MAIL_USERNAME`, `MAIL_PASSWORD`, `MAIL_USE_TLS`, `MAIL_SENDER` | Só para `smtp` | |
| `SHOW_DEV_CONFIRMATION_LINK` | Com `console`, mostrar a ligação de confirmação na página. `false` no túnel: fica só no terminal | `true` |
| `SESSION_COOKIE_SECURE` | `true` em produção ou pelo túnel (HTTPS); com isto ligado, a aplicação recusa o modo debug | `false` |
| `ADMIN_URL_PREFIX` | Endereço da área de gestão (administradores) | `gestao` |
| `LLM_BACKEND` | LLM da orientação: `falso` (sem rede), `gemini` ou `groq` | `falso` |
| `LLM_MODELO` | Outro modelo do fornecedor | `gemini-3.5-flash-lite` / `openai/gpt-oss-120b` |
| `GEMINI_API_KEY`, `GROQ_API_KEY` | Chaves pessoais dos fornecedores (só no `.env`, nunca no repositório) | vazias |
| `ORIENTACAO_MAX_PEDIDOS_DIA` | Pedidos ao LLM por aluno e por dia (`0` = sem limite) | `40` |

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
