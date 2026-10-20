# Recomendador de UCs opcionais

Aplicação web que ajuda a escolher cursos e unidades curriculares opcionais, com base nas preferências de cada pessoa e na experiência de outros estudantes. Serve quem ainda não tem curso (sugere cursos de várias instituições, com um LLM) e quem já é aluno (sugere opcionais). Ver a [visão do produto](docs/geral/00-visao-do-produto.md).

Projeto 1 de Metodologias Ágeis (Scrum) · Duarte Eusébio e Simão Almeida

| | |
|---|---|
| **Sprint atual** | Sprint 2, desde 20/10 (US29, US30 e US31; Sprint Planning de 20/10) · Sprint 1 concluído (10 SP: US01, US02, US03) |
| **No repositório** | US01 — Registo com confirmação por ligação · US02 — Iniciar e terminar sessão · US03 — Perfis de aluno e administrador |
| **Testes automáticos** | 275, todos a passar |

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
| Sprint 2 (13 SP, 8 já feitos) | Uma pessoa indecisa conversa com o assistente (LLM), recebe 2 a 3 cursos do catálogo com explicação e escolhe um, ficando a decisão registada no percurso. |
| Sprint 3 (5 SP, por completar) | Uma pessoa indecisa consulta e compara cursos de várias instituições. |
| Sprint 4 (10 SP) | Quem já é aluno regista as UCs que concluiu e avalia as opcionais que fez, com as avaliações pseudonimizadas desde o início. |

**Replaneamento de 14/10/2026 (decisão do PO, issue #15):** o LLM conduz a conversa de orientação (sem perguntas fixas) e passa para o Sprint 2; o plano passa a respeitar a velocidade real (10 SP por sprint). A US32 foi fundida na US29; US04, US09 e US11 passam para o backlog. Ver o [spike do LLM](docs/geral/05-spike-llm.md).

**Sprint Planning do Sprint 2 (20/10/2026, decisão do PO):** a US29 e a US30 foram feitas antes de o sprint começar, por isso entra a US31 (antecipada do Sprint 3). O ponto 14 dos requisitos fica decidido: o OptaBem é um protótipo usado pela equipa e na demonstração, com aviso de 18+ na conversa. O servidor Ollama da faculdade foi testado e posto de parte ([spike](docs/geral/05-spike-llm.md), secção 7).

| User story | Título | Sprint | Estado | Documentação |
|---|---|---|---|---|
| US01 | Registo com email pessoal | Sprint 1 | Feita | [docs/US01/](docs/US01/) |
| US02 | Autenticação | Sprint 1 | Feita | [docs/US02/](docs/US02/) |
| US03 | Perfis de aluno e administrador (revista a 14/10: um só início de sessão) | Sprint 1 | Feita | [docs/US03/](docs/US03/) |
| US29 | Conversa de orientação com o LLM (reescrita a 14/10: sem perguntas fixas) | Sprint 2 | Feita (no `main`; por aceitar na Sprint Review) | [docs/US29/](docs/US29/) |
| US30 | Sugestão de 2 a 3 cursos no fim da conversa | Sprint 2 | Feita (no `main`; por aceitar na Sprint Review) | [docs/US30/](docs/US30/) |
| US31 | Escolher curso e linha do tempo do percurso (antecipada a 20/10) | Sprint 2 | Em curso (feita, por rever; issue #27) | [docs/US31/](docs/US31/) |
| US05 | Consultar e comparar cursos | Sprint 3 | Por fazer (a pesquisa já foi feita a 14/10, e a página `/cursos/` na US30; faltam filtros, ficha e comparação) | `app/catalogo/` |
| US06 | Registar percurso | Sprint 4 | Por fazer | — |
| US07 | Avaliar opcional concluída (com pseudo_id desde o início) | Sprint 4 | Por fazer | — |
| US04 | Importar catálogo de instituições e cursos | Backlog | Por fazer | — |
| US09 | Avaliações pseudonimizadas | Backlog | Por fazer | — |
| US11 | Recomendações de popularidade | Backlog | Por fazer | — |
| US08 | Avaliação rápida de obrigatórias | Backlog | Por fazer | — |
| US10 | Dataset sintético | Backlog | Por fazer | — |
| US12 | Recomendações user-based | Backlog | Por fazer | — |
| US13 | Excluir UCs inválidas | Backlog | Por fazer | — |
| US14 | Explicação da recomendação | Backlog | Por fazer | — |
| US15 | Avaliação offline do motor | Backlog | Por fazer | — |
| US16 | Períodos de avaliação | Backlog | Por fazer | — |
| US17 | Exportar e apagar dados | Backlog | Por fazer | — |
| US18 | Comentário livre | Backlog | Por fazer | — |
| US19 | Moderar comentários | Backlog | Por fazer | — |
| US20 | Filtrar por semestre e ECTS | Backlog | Por fazer | — |
| US21 | Preferência de carga de trabalho | Backlog | Por fazer | — |
| US22 | Comparação de estratégias | Backlog | Por fazer | — |
| US23 | Esconder UCs sem vagas | Backlog | Por fazer | — |
| US24 | Feedback sobre recomendações | Backlog | Por fazer | — |
| US25 | Painel de participação | Backlog | Por fazer | — |
| US26 | Filtragem baseada em itens | Backlog | Por fazer | — |
| US27 | Evitar conflitos de horário | Backlog | Por fazer | — |
| US28 | Lembretes de avaliação | Backlog | Por fazer | — |
| US32 | Assistente LLM que conversa com o utilizador | — | Fundida na US29 (14/10) | issue #15 |

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
| [Catálogo de cursos](dados/README.md) | 30 licenciaturas de 12 instituições (DGES), para importar na US04 |
| [Registo de uso de IA](docs/geral/registo-de-uso-de-ia.md) | Cada utilização relevante de IA no projeto |
| [Product Backlog (Excel)](docs/geral/product-backlog.xlsx) | Todas as stories, plano de sprints com gráfico e resumo MoSCoW |
| [US01](docs/US01/README.md) | Requisitos, use case, BPMN, prompt e diagramas da US01 |
| [US02](docs/US02/README.md) | Requisitos, use case, BPMN, prompt e diagramas da US02 |
| [US03](docs/US03/README.md) | Administradores e área de gestão: requisitos, use case, BPMN e como criar o primeiro administrador |
| [US29](docs/US29/README.md) | Conversa de orientação com o LLM: requisitos, use case, BPMN e como experimentar |
| [US30](docs/US30/README.md) | Sugestão de 2 a 3 cursos no fim da conversa: requisitos, use case, BPMN e como experimentar |
| [US31](docs/US31/README.md) | Escolher curso e linha do tempo do percurso: requisitos, use case, BPMN e como experimentar |

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
| `SESSION_COOKIE_SECURE` | `true` em produção (HTTPS) | `false` |
| `ADMIN_URL_PREFIX` | Endereço da área de gestão (administradores) | `gestao` |
| `LLM_BACKEND` | LLM da orientação: `falso` (sem rede), `gemini` ou `groq` | `falso` |
| `LLM_MODELO` | Outro modelo do fornecedor | `gemini-3.5-flash-lite` / `openai/gpt-oss-120b` |
| `GEMINI_API_KEY`, `GROQ_API_KEY` | Chaves pessoais dos fornecedores (só no `.env`, nunca no repositório) | vazias |

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
  orientacao/       conversa de orientação conduzida pelo LLM (US29, US30) e comando llm-teste
  percurso/         em que passo está cada aluno (State) e as decisões: escolher curso, linha do tempo (US31)
  gestao/           área de gestão (administradores, US03); endereço em ADMIN_URL_PREFIX
    routes.py         entrar, sair, painel e lista de administradores
    services.py       criar, autenticar e remover administradores
    sessions.py       sessão de administrador e proteção das páginas
    cli.py            comandos create-admin e list-admins
tests/              testes automáticos
docs/               documentação (índice em docs/README.md)
dados/              catálogo de instituições e cursos (dados públicos, ver dados/README.md)
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
