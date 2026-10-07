# Recomendador de UCs opcionais

Aplicação web que ajuda os alunos a escolher unidades curriculares opcionais com base na experiência de colegas com percursos e gostos parecidos. Projeto 1 de Metodologias Ágeis (Scrum).

**Estado:** Sprint 1, em curso. O estado de cada user story está na secção [Estado do projeto](#estado-do-projeto).

## Estado do projeto

**Sprint Goal do Sprint 1:** um aluno consegue registar-se, construir o seu percurso e avaliar UCs.

| User story | Título | Sprint | Estado | Documentação |
|---|---|---|---|---|
| US01 | Registo com email institucional | Sprint 1 | Feita | [docs/US01/](docs/US01/) |
| US02 | Autenticação | Sprint 1 | Feita (o código ainda não está no repositório) | — |
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

O código da US02 foi desenvolvido mas ainda não foi integrado neste repositório. Só a US01 tem, por enquanto, documentação em `docs/`; cada nova story terá a sua pasta `docs/USNN/`.

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
docs/           documentação (índice em docs/README.md)
  geral/        requisitos, regras de código e registo de uso de IA
  US01/         documentação da US01: requisitos, use case, BPMN, prompt e diagramas
  USNN/         uma pasta por cada nova story, com a mesma estrutura
instance/       dados locais (ignorado pelo Git)
```

## Documentação

O índice completo está em [docs/README.md](docs/README.md).

| Documento | Conteúdo |
|---|---|
| [docs/geral/01-requisitos-funcionais-e-nao-funcionais.md](docs/geral/01-requisitos-funcionais-e-nao-funcionais.md) | Requisitos funcionais, não funcionais, regras de negócio e rastreabilidade |
| [docs/geral/02-regras-de-geracao-de-codigo.md](docs/geral/02-regras-de-geracao-de-codigo.md) | Regras para gerar e rever código com IA |
| [docs/geral/registo-de-uso-de-ia.md](docs/geral/registo-de-uso-de-ia.md) | Registo de uso de IA |
| [docs/US01/](docs/US01/README.md) | US01: requisitos, use case, BPMN, prompt e diagramas |

## Como contribuir

1. Cada story tem uma issue criada com o modelo [User story](.github/ISSUE_TEMPLATE/user-story.md).
2. Um ramo por story: `feature/US02-autenticacao`.
3. A documentação da story fica em `docs/USNN/` (por exemplo, `docs/US02/`), com a mesma estrutura da [US01](docs/US01/README.md): `README.md`, `requisitos.md`, `use-case.md`, `bpmn.md`, `prompt.md` e `diagramas/`. Acrescente a pasta ao [índice](docs/README.md) e atualize a tabela de [estado do projeto](#estado-do-projeto).
4. Commits no formato `US02: <resumo no imperativo>`.
5. Pull Request com o [modelo do repositório](.github/pull_request_template.md), que inclui a checklist da secção 10 de [docs/geral/02-regras-de-geracao-de-codigo.md](docs/geral/02-regras-de-geracao-de-codigo.md), revisto por outro elemento.
6. Cada utilização relevante de IA fica anotada em [docs/geral/registo-de-uso-de-ia.md](docs/geral/registo-de-uso-de-ia.md).
