# US46 — Use case: exportar os meus dados

![Diagrama de use case da US46](diagramas/use-case.svg)

## 1. Atores

| Ator | Tipo | Descrição |
|---|---|---|
| Aluno | Primário | Conta de aluno com sessão iniciada. |

## 2. Lista de use cases

| ID | Nome | Relações |
|---|---|---|
| UC38 | Descarregar os meus dados | — |

## 3. UC38 — Descarregar os meus dados

| | |
|---|---|
| **Objetivo** | Ter uma cópia de tudo o que o OptaBem guarda sobre o aluno. |
| **Pré-condições** | Sessão iniciada. |
| **Pós-condições** | O aluno tem o ficheiro JSON. Nada muda na base de dados. |
| **Requisitos** | RF17.7 a RF17.11 |

**Fluxo principal:** (1) em «A minha conta», o aluno carrega em «Descarregar os meus dados»; (2) o sistema mostra o que vai no ficheiro e pede a palavra-passe; (3) o aluno escreve-a e carrega em «Descarregar»; (4) o sistema junta os dados do aluno e devolve o ficheiro.

**Alternativos:** palavra-passe errada ou vazia → mensagem de erro, sem ficheiro (volta ao passo 3). Sem sessão → início de sessão.

## 4. Rastreabilidade

| Use case | Requisitos | Código | Testes |
|---|---|---|---|
| UC38 | RF17.7 a RF17.11 | `auth/routes.py` (`export_form`, `export_submit`), `auth/exportar.py`, `services.confirma_password` | `tests/test_exportar.py` |
