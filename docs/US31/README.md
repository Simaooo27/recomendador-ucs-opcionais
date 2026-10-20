# US31 — Escolher curso e linha do tempo do percurso

> **Como** utilizador, **quero** escolher um dos cursos sugeridos (ou outro do catálogo) e ver as decisões que fui tomando, **para** acompanhar o meu percurso.

| | |
|---|---|
| Estado | Feita (por rever) |
| Sprint | Sprint 2 (antecipada do Sprint 3 a 20/10) |
| Story points | 5 |
| Épico | E11 — Orientação de curso |
| Prioridade | Must |
| Requisito de origem | RF03, RF35, RF39, RN10 (ver [01-requisitos-funcionais-e-nao-funcionais.md](../geral/01-requisitos-funcionais-e-nao-funcionais.md)) |
| Depende de | [US30](../US30/README.md) (cursos sugeridos) e a página `/cursos/` |
| Issue | #27 |

## A ideia em três pontos

1. **Escolher exige confirmar** (RN10). «Escolher este curso», nos cursos sugeridos ou no catálogo, abre uma página de confirmação; só o botão «Confirmar a escolha» regista.
2. **Cada escolha é uma decisão**, com data, cursos sugeridos nessa altura, curso escolhido e origem. O curso do perfil é o da decisão mais recente; mudar de curso cria uma decisão nova.
3. **Depois de escolher, a conversa com o LLM é apagada** (decisão do PO, ponto 15). Fica só a decisão.

## Experimentar

```bash
flask --app app init-db          # cria a tabela nova «decisoes» (não apaga dados)
flask --app app run --debug
```

Iniciar sessão como aluno, ter uma conversa até aos cursos sugeridos (ou abrir `/cursos/`), carregar em **«Escolher este curso»** e confirmar. A página inicial passa a mostrar o curso; **«Ver as minhas decisões»** abre a linha do tempo (`/percurso/`).

## Documentos

| Documento | Conteúdo |
|---|---|
| [requisitos.md](requisitos.md) | Requisitos funcionais e critérios de aceitação |
| [use-case.md](use-case.md) | Use case ([diagrama](diagramas/use-case.svg)) |
| [bpmn.md](bpmn.md) | Processo BPMN ([imagem](diagramas/bpmn.svg) · [ficheiro editável](diagramas/bpmn.bpmn)) |
| [prompt.md](prompt.md) | Pedido feito à IA para gerar o código |

Os diagramas são gerados por [`diagramas/gerar.py`](diagramas/gerar.py): mudar o desenho lá e correr `python docs/US31/diagramas/gerar.py docs/US31/diagramas`.

## Código

| Ficheiro | O que faz |
|---|---|
| [`app/percurso/__init__.py`](../../app/percurso/__init__.py) | Em que passo do percurso está cada aluno (padrão State); com curso escolhido, passa a «com curso» e mostra o curso |
| [`app/percurso/services.py`](../../app/percurso/services.py) | Regras: escolher (só cursos do catálogo, não repetir o curso atual, guardar os sugeridos, apagar a conversa), curso atual, linha do tempo |
| [`app/percurso/repository.py`](../../app/percurso/repository.py) | SQL da tabela `decisoes` |
| [`app/percurso/routes.py`](../../app/percurso/routes.py) | `/percurso/` (linha do tempo) e `/percurso/escolher/<chave>` (confirmar e registar) |
| [`app/templates/percurso/`](../../app/templates/percurso/) | Páginas de confirmação e da linha do tempo |
| [`app/templates/macros/marca.html`](../../app/templates/macros/marca.html) | A ficha do curso (`cartao_curso`) aceita `escolher=true` |
| [`app/main.py`](../../app/main.py) | A página inicial recebe o curso atual |
| [`app/schema.sql`](../../app/schema.sql) | Tabela `decisoes` |
| [`app/texts.py`](../../app/texts.py) | Textos (secção «Escolher curso e linha do tempo das decisões») |
| [`app/static/style.css`](../../app/static/style.css) | Secção 12: botão «Escolher este curso», confirmação e linha do tempo |

## Testes

[`tests/test_escolha.py`](../../tests/test_escolha.py): 20 testes, sem rede. A tabela critério de aceitação → teste está na secção 5 de [requisitos.md](requisitos.md#5-critérios-de-aceitação-e-testes).
