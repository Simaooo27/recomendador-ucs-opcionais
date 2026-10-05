# Recomendador de UCs opcionais

Aplicação web que ajuda os alunos a escolher unidades curriculares opcionais com base na experiência de colegas com percursos e gostos parecidos. Projeto 1 de Metodologias Ágeis (Scrum).

**Estado:** Sprint 1, em curso. Está implementada a **US01 (registo com email institucional)**. As restantes stories estão no Product Backlog.

## Requisitos

- Python 3.10 ou superior (testado em 3.12)
- Git

## Instalação

```bash
git clone <URL-do-repositório>
cd recomendador-ucs-opcionais

python -m venv .venv
source .venv/bin/activate          # Windows (PowerShell): .venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Configuração

A aplicação lê variáveis de ambiente (ver `.env.example`). A única obrigatória é `SECRET_KEY`.

```bash
export SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")
# Windows (PowerShell):
#   $env:SECRET_KEY = python -c "import secrets; print(secrets.token_hex(32))"
```

| Variável | Para quê | Por omissão |
|---|---|---|
| `SECRET_KEY` | Assinar sessões e ligações de confirmação | obrigatória |
| `ALLOWED_EMAIL_DOMAINS` | Domínios aceites no registo (inclui subdomínios) | `iscap.ipp.pt` |
| `DATABASE_PATH` | Ficheiro SQLite | `instance/app.sqlite3` |
| `MAIL_BACKEND` | `console` (escreve o email no terminal) ou `smtp` | `console` |
| `MAIL_SERVER`, `MAIL_PORT`, `MAIL_USERNAME`, `MAIL_PASSWORD`, `MAIL_USE_TLS`, `MAIL_SENDER` | Só para `smtp` | |
| `SESSION_COOKIE_SECURE` | `true` em produção (HTTPS) | `false` |

## Executar

```bash
flask --app app init-db        # cria as tabelas (só na primeira vez)
flask --app app run --debug
```

Abra http://127.0.0.1:5000. Com `MAIL_BACKEND=console`, a ligação de confirmação aparece **no terminal** onde a aplicação está a correr.

## Testes

```bash
python -m unittest discover -s tests -t . -v
```

Também funciona com `pytest` (`pip install -r requirements-dev.txt`). Os testes não precisam de rede nem de configuração.

## Estrutura

```
app/            código da aplicação (Flask)
tests/          testes automáticos
docs/           requisitos, regras de código, use case, BPMN, registo de IA
prompts/        prompts usados para gerar código com IA
instance/       dados locais (ignorado pelo Git)
```

## Documentação

| Documento | Conteúdo |
|---|---|
| [docs/01](docs/01-requisitos-funcionais-e-nao-funcionais.md) | Requisitos funcionais, não funcionais, regras de negócio e rastreabilidade |
| [docs/02](docs/02-regras-de-geracao-de-codigo.md) | Regras para gerar e rever código com IA |
| [docs/03](docs/03-rf-us01-registo-email-institucional.md) | Requisitos da US01 e critérios de aceitação |
| [docs/04](docs/04-use-case-us01.md) | Use case da US01 |
| [docs/05](docs/05-bpmn-us01.md) | Processo BPMN da US01 |
| [docs/registo-de-uso-de-ia.md](docs/registo-de-uso-de-ia.md) | Registo de uso de IA |
| [prompts/](prompts/) | Prompts |

## Como contribuir

1. Um ramo por story: `feature/US02-autenticacao`.
2. Commits no formato `US02: <resumo no imperativo>`.
3. Pull Request com a checklist da secção 10 de [docs/02](docs/02-regras-de-geracao-de-codigo.md), revisto por outro elemento.
4. Cada utilização relevante de IA fica anotada em [docs/registo-de-uso-de-ia.md](docs/registo-de-uso-de-ia.md).
