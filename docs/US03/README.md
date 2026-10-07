# US03 — Perfis de aluno e administrador

> **Como** administrador, **quero** ter uma conta própria, separada das contas dos alunos e numa área escondida, **para** gerir a aplicação sem que os alunos vejam ou consigam usar essas funções.

| | |
|---|---|
| Estado | Feita (em revisão) |
| Sprint | Sprint 1 |
| Story points | 5 |
| Épico | E1 — Contas e perfis |
| Prioridade | Must |
| Requisito de origem | RF04 (ver [01-requisitos-funcionais-e-nao-funcionais.md](../geral/01-requisitos-funcionais-e-nao-funcionais.md)) |
| Necessária para | US04 (importar catálogo), US16 (períodos de avaliação), US19 (moderar comentários) |

## A ideia em três pontos

1. **Os administradores não são alunos.** Têm uma tabela própria (`admins`), entram com **nome de utilizador** e palavra-passe e não têm email. O registo público só cria alunos.
2. **A área de gestão está escondida.** Fica num endereço próprio (por omissão `/gestao`, configurável em `ADMIN_URL_PREFIX`), nenhuma página dos alunos tem ligações para lá e as páginas pedem para não ser indexadas pelos motores de busca.
3. **Quem cria administradores é um administrador.** Só o **primeiro** é criado no terminal, por quem instala a aplicação (alguém tem de existir antes de haver administradores). Os seguintes são criados (e removidos) na área de gestão.

## Documentos

| Documento | Conteúdo |
|---|---|
| [requisitos.md](requisitos.md) | Requisitos funcionais e critérios de aceitação |
| [use-case.md](use-case.md) | Use case ([diagrama](diagramas/use-case.svg)) |
| [bpmn.md](bpmn.md) | Processos BPMN ([imagem](diagramas/bpmn.svg) · [ficheiro editável](diagramas/bpmn.bpmn)) |
| [prompt.md](prompt.md) | Pedido feito à IA para gerar o código |

## Criar o primeiro administrador

Na pasta do projeto, com a configuração carregada (`SECRET_KEY`):

```bash
flask --app app init-db         # cria a tabela nova (não apaga dados)
flask --app app create-admin    # pede o nome e a palavra-passe (não aparece no ecrã)
flask --app app list-admins     # mostra os administradores
```

Depois, entrar em `http://127.0.0.1:5000/gestao/entrar`.

## Código

| Ficheiro | O que faz |
|---|---|
| [`app/schema.sql`](../../app/schema.sql) | Tabela `admins` (nome, hash da palavra-passe, quem criou, última entrada) |
| [`app/gestao/services.py`](../../app/gestao/services.py) | Criar, autenticar e remover administradores (regras e validação) |
| [`app/gestao/sessions.py`](../../app/gestao/sessions.py) | Sessão de administrador e `admin_required` |
| [`app/gestao/routes.py`](../../app/gestao/routes.py) | Páginas da gestão: entrar, sair, painel, administradores |
| [`app/gestao/cli.py`](../../app/gestao/cli.py) | Comandos `create-admin` e `list-admins` |
| [`app/templates/gestao/`](../../app/templates/gestao/) | Páginas da área de gestão |
| [`app/config.py`](../../app/config.py) | `ADMIN_URL_PREFIX` (endereço da área) |
| [`app/texts.py`](../../app/texts.py) | Textos (secção «Área de gestão») |

## Testes

[`tests/test_gestao.py`](../../tests/test_gestao.py): 29 testes. A tabela critério de aceitação → teste está na secção 5 de [requisitos.md](requisitos.md#5-critérios-de-aceitação-e-testes).
