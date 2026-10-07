# Recomendador de UCs opcionais (OptaBem)

Aplicação web que ajuda os alunos a escolher unidades curriculares opcionais com base na experiência de colegas com percursos e gostos parecidos.

Projeto 1 de Metodologias Ágeis (Scrum) · Duarte Eusébio e Simão Almeida

| | |
|---|---|
| **Sprint atual** | Sprint 1 (em curso) |
| **No repositório** | US01 — Registo com confirmação por ligação · US02 — Iniciar e terminar sessão |
| **Testes automáticos** | 92, todos a passar |

## Índice

1. [Estado do projeto](#1-estado-do-projeto)
2. [Documentação do projeto](#2-documentação-do-projeto)
3. [Alterar textos e cores](#3-alterar-textos-e-cores)
4. [Pôr a aplicação a correr](#4-pôr-a-aplicação-a-correr)
5. [Testes](#5-testes)
6. [Organização do código](#6-organização-do-código)
7. [Como contribuir](#7-como-contribuir)

## 1. Estado do projeto

**Sprint Goal do Sprint 1:** um aluno consegue registar-se, construir o seu percurso e avaliar UCs.

| User story | Título | Sprint | Estado | Documentação |
|---|---|---|---|---|
| US01 | Registo com email institucional | Sprint 1 | Feita | [docs/US01/](docs/US01/) |
| US02 | Autenticação | Sprint 1 | Feita | [docs/US02/](docs/US02/) |
| US03 | Importar catálogo de UCs | Sprint 1 | Por fazer | — |
| US04 | Consultar catálogo de opcionais | Sprint 1 | Por fazer | — |
| US05 | Registar percurso | Sprint 1 | Por fazer | — |
| US06 | Avaliar opcional concluída | Sprint 1 | Por fazer | — |
| US07 | Avaliação rápida de obrigatórias | Sprint 1 | Por fazer | — |
| US09 | Avaliações pseudonimizadas | Sprint 2 | Por fazer | — |
| US20 | Dataset sintético | Sprint 2 | Por fazer | — |
| US11 | Recomendações de popularidade | Sprint 2 | Por fazer | — |
| US12 | Recomendações user-based | Sprint 2 | Por fazer | — |
| US15 | Excluir UCs inválidas | Sprint 2 | Por fazer | — |
| US13 | Explicação da recomendação | Sprint 3 | Por fazer | — |
| US21 | Avaliação offline do motor | Sprint 3 | Por fazer | — |
| US14 | Preferência de carga de trabalho | Sprint 3 | Por fazer | — |
| US24 | Períodos de avaliação | Sprint 3 | Por fazer | — |
| US08 | Comentário livre | Sprint 3 | Por fazer | — |
| US16 | Filtrar por semestre e ECTS | Sprint 3 | Por fazer | — |
| US22 | Fatorização de matrizes (SVD) | Sprint 4 | Por fazer | — |
| US23 | Comparação de estratégias | Sprint 4 | Por fazer | — |
| US25 | Moderar comentários | Sprint 4 | Por fazer | — |
| US10 | Exportar e apagar dados | Sprint 4 | Por fazer | — |
| US17 | Esconder UCs sem vagas | Backlog | Por fazer | — |
| US19 | Feedback sobre recomendações | Backlog | Por fazer | — |
| US26 | Painel de participação | Backlog | Por fazer | — |
| US27 | Filtragem baseada em itens | Backlog | Por fazer | — |
| US18 | Evitar conflitos de horário | Backlog | Por fazer | — |
| US28 | Lembretes de avaliação | Backlog | Por fazer | — |

Cada story tem a sua pasta `docs/USNN/` quando é desenvolvida (para já, US01 e US02).

## 2. Documentação do projeto

O índice completo está em [docs/README.md](docs/README.md). Os documentos gerais ficam em `docs/geral/` e cada user story tem a sua pasta `docs/USNN/`.

| Documento | O que contém |
|---|---|
| [Requisitos funcionais e não funcionais](docs/geral/01-requisitos-funcionais-e-nao-funcionais.md) | Todos os requisitos (RF, RNF), regras de negócio e ligação às user stories |
| [Regras de geração de código](docs/geral/02-regras-de-geracao-de-codigo.md) | Como a equipa escreve, testa e revê código (incluindo com IA) |
| [Registo de uso de IA](docs/geral/registo-de-uso-de-ia.md) | Cada utilização relevante de IA no projeto |
| [US01](docs/US01/README.md) | Requisitos, use case, BPMN, prompt e diagramas da US01 |
| [US02](docs/US02/README.md) | Requisitos, use case, BPMN, prompt e diagramas da US02 |

## 3. Alterar textos e cores

Para mudanças pequenas não é preciso mexer no código da aplicação.

| Quero mudar… | Ficheiro | Como |
|---|---|---|
| O nome da aplicação (topo e separador do navegador) | [`app/texts.py`](app/texts.py) | Muda o texto de `APP_NAME` |
| Títulos, frases, botões ou mensagens de erro | [`app/texts.py`](app/texts.py) | Procura o texto (Ctrl+F) e muda o que está entre aspas |
| O email de confirmação | [`app/texts.py`](app/texts.py) | `CONFIRMATION_EMAIL_SUBJECT` e `CONFIRMATION_EMAIL_BODY` |
| O texto da política de privacidade | [`app/texts.py`](app/texts.py) | `PRIVACY_BODY` |
| As cores | [`app/static/style.css`](app/static/style.css) | As primeiras linhas do ficheiro; cada cor tem um comentário a dizer onde aparece |
| Domínios de email aceites, versão da política, prazo da ligação | [`app/config.py`](app/config.py) | Exige cuidado: fala com quem desenvolve |

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

flask --app app init-db                # cria a base de dados (só da primeira vez)
flask --app app run --debug
```

Abre http://127.0.0.1:5000: aparece o início de sessão, com uma ligação para criar conta. Em desenvolvimento não é enviado nenhum email: a ligação de confirmação aparece **na própria página «Confirme o seu email»** (caixa amarela) e no terminal onde a aplicação está a correr.

<details>
<summary>Outras configurações (variáveis de ambiente)</summary>

A aplicação lê variáveis de ambiente (ver [`.env.example`](.env.example)). Só a `SECRET_KEY` é obrigatória.

| Variável | Para quê | Por omissão |
|---|---|---|
| `SECRET_KEY` | Assinar sessões e ligações de confirmação | obrigatória |
| `ALLOWED_EMAIL_DOMAINS` | Domínios aceites no registo (inclui subdomínios) | `iscap.ipp.pt` |
| `DATABASE_PATH` | Ficheiro SQLite | `instance/app.sqlite3` |
| `MAIL_BACKEND` | `console` (escreve o email no terminal) ou `smtp` | `console` |
| `MAIL_SERVER`, `MAIL_PORT`, `MAIL_USERNAME`, `MAIL_PASSWORD`, `MAIL_USE_TLS`, `MAIL_SENDER` | Só para `smtp` | |
| `SESSION_COOKIE_SECURE` | `true` em produção (HTTPS) | `false` |

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
| `tests/test_validators.py` | Regras do email e da palavra-passe |
| `tests/test_texts.py` | Ficheiro de textos: nada vazio e marcadores `{…}` no sítio |
| `tests/test_app_factory.py` | Arranque e configuração da aplicação |

## 6. Organização do código

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
tests/              testes automáticos
docs/               documentação (índice em docs/README.md)
  geral/            requisitos, regras de código e registo de uso de IA
  US01/             requisitos, use case, BPMN, prompt e diagramas da US01
  US02/             o mesmo para a US02
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
