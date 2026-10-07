# Recomendador de UCs opcionais (OptaBem)

Aplicação web que ajuda os alunos a escolher unidades curriculares opcionais com base na experiência de colegas com percursos e gostos parecidos.

Projeto 1 de Metodologias Ágeis (Scrum) · Duarte Eusébio e Simão Almeida

| | |
|---|---|
| **Sprint atual** | Sprint 1 (em curso) |
| **Feito** | US01 — Registo com email e confirmação por ligação |
| **A seguir** | US02 — Autenticação (iniciar e terminar sessão) |
| **Testes automáticos** | 69, todos a passar |

## Índice

1. [Documentação do projeto](#1-documentação-do-projeto)
2. [Alterar textos e cores](#2-alterar-textos-e-cores)
3. [Pôr a aplicação a correr](#3-pôr-a-aplicação-a-correr)
4. [Testes](#4-testes)
5. [Organização do código](#5-organização-do-código)
6. [Regras da equipa](#6-regras-da-equipa)

## 1. Documentação do projeto

| Documento | O que contém |
|---|---|
| [Requisitos funcionais e não funcionais](docs/01-requisitos-funcionais-e-nao-funcionais.md) | Todos os requisitos (RF, RNF), regras de negócio e ligação às user stories |
| [Requisitos da US01](docs/03-rf-us01-registo-email-institucional.md) | Detalhe do registo, critérios de aceitação e testes que os verificam |
| [Use case da US01](docs/04-use-case-us01.md) | Diagrama e descrição dos casos de uso do registo |
| [BPMN da US01](docs/05-bpmn-us01.md) | Diagrama do processo de registo e confirmação |
| [Regras de geração de código](docs/02-regras-de-geracao-de-codigo.md) | Como a equipa escreve, testa e revê código (incluindo com IA) |
| [Registo de uso de IA](docs/registo-de-uso-de-ia.md) | Cada utilização relevante de IA no projeto |
| [Prompts](prompts/) | Prompts usados para gerar código com IA |

Os diagramas estão em [`docs/diagrams/`](docs/diagrams/).

## 2. Alterar textos e cores

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
- depois de guardar, recarrega a página no navegador e corre os testes (secção 4). Se um marcador entre chavetas tiver sido apagado por engano, um teste avisa.

## 3. Pôr a aplicação a correr

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

Abre http://127.0.0.1:5000. Em desenvolvimento não é enviado nenhum email: a ligação de confirmação aparece **no terminal** onde a aplicação está a correr.

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

## 4. Testes

```bash
python -m unittest discover -s tests -t . -v
```

Os testes não precisam de rede nem de configuração. Também correm com `pytest` (`pip install -r requirements-dev.txt`).

| Ficheiro | O que verifica |
|---|---|
| `tests/test_registration.py` | Formulário de registo, contas duplicadas, falha no envio do email, CSRF |
| `tests/test_confirmation.py` | Ligação de confirmação: válida, repetida, adulterada, expirada |
| `tests/test_validators.py` | Regras do email e da palavra-passe |
| `tests/test_texts.py` | Ficheiro de textos: nada vazio e marcadores `{…}` no sítio |
| `tests/test_app_factory.py` | Arranque e configuração da aplicação |

## 5. Organização do código

```
app/
  texts.py          todos os textos que o utilizador vê
  static/style.css  aspeto e cores
  templates/        páginas HTML (usam os textos de texts.py)
  auth/             registo e confirmação de email (US01)
    routes.py         recebe os pedidos do navegador e devolve as páginas
    services.py       regras do registo e da confirmação
    validators.py     validação do email e da palavra-passe
    repository.py     acesso à base de dados
    tokens.py         ligações de confirmação assinadas
  config.py         configuração (variáveis de ambiente)
  db.py, schema.sql base de dados SQLite
  security.py       proteção CSRF e cabeçalhos de segurança
  mailer.py         envio de email (terminal ou SMTP)
  main.py           página inicial e política de privacidade
tests/              testes automáticos
docs/               requisitos, use cases, BPMN e regras da equipa
prompts/            prompts usados com IA
```

## 6. Regras da equipa

1. Um ramo por story: `feature/US02-autenticacao`.
2. Commits no formato `US02: <resumo no imperativo>`.
3. Pull Request com a checklist da secção 10 das [regras de código](docs/02-regras-de-geracao-de-codigo.md), revisto pelo outro elemento antes do merge.
4. Cada utilização relevante de IA fica no [registo de uso de IA](docs/registo-de-uso-de-ia.md).
