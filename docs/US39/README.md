# US39 — Corrigir e esconder cursos do catálogo (gestão)

> **Como** administrador, **quero** corrigir a descrição e as saídas profissionais de um curso, ou escondê-lo, **para** o catálogo não ter erros sem mexer no ficheiro.

| | |
|---|---|
| Estado | Feita: aceite pelo PO a 29/10 (código de 29/10, PR próprio). Revisão do Simão pendente |
| Sprint | Sprint 4 (29/10 a 05/11), por decisão do PO a 29/10 |
| Story points | 5 |
| Épico | E2 — Catálogo de cursos |
| Prioridade | Should |
| Requisitos de origem | RF04, RF05; detalhe no RF51 (ver [01-requisitos-funcionais-e-nao-funcionais.md](../geral/01-requisitos-funcionais-e-nao-funcionais.md)) |
| Depende de | US03 (área de gestão), US04 (catálogo da DGES) |

## A ideia em três pontos

1. Na gestão, **«Catálogo»** lista os cursos (com procura e filtro «corrigidos» ou «escondidos»). Cada curso abre uma página para **corrigir a descrição e as saídas profissionais** (uma por linha) ou **esconder o curso**, com o texto da DGES ao lado.
2. As correções ficam **na base de dados, por cima do ficheiro da DGES**: a recolha seguinte reescreve o CSV, mas não as apaga. **«Repor os dados da DGES»** volta ao texto do ficheiro. Um curso escondido sai do catálogo, da pesquisa, da conversa com o assistente e do plano (onde fica um aviso para o retirar).
3. Fica **registado quem alterou o quê e quando**. As tabelas e as páginas **não têm dados de alunos**.

## Experimentar

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\ferramentas\arrancar.ps1
```

Entrar como administrador, ir a **Gestão › Catálogo** e abrir um curso. Mudar a descrição e carregar em **«Guardar»**; abrir a ficha do curso como aluno (ou sem sessão) e ver o texto novo. Voltar, marcar **«Esconder este curso»** e ver que a ficha dá «página não encontrada». **«Repor os dados da DGES»** desfaz tudo; o histórico fica.

## Documentos

| Documento | Conteúdo |
|---|---|
| [requisitos.md](requisitos.md) | Requisitos funcionais e critérios de aceitação, com os testes de cada um |
| [use-case.md](use-case.md) | Use case ([diagrama](diagramas/use-case.svg)) |
| [bpmn.md](bpmn.md) | Processo BPMN ([imagem](diagramas/bpmn.svg) · [ficheiro editável](diagramas/bpmn.bpmn)) |
| [prompt.md](prompt.md) | Pedido feito à IA para gerar o código |

Os diagramas são gerados por [`diagramas/gerar.py`](diagramas/gerar.py): mudar o desenho lá e correr `python docs/US39/diagramas/gerar.py docs/US39/diagramas`.

## Código e testes

| Onde | O quê |
|---|---|
| `app/schema.sql` | Tabelas `correcoes_cursos` e `historico_catalogo` |
| `app/catalogo/correcoes_repository.py` | O SQL das correções e do histórico |
| `app/catalogo/services.py` | `cursos` aplica as correções (o único ponto por onde a aplicação lê o catálogo); `aplicar_correcoes`, `corrigido` (funções puras), `cursos_para_gestao` |
| `app/gestao/services.py` | `guardar_correcao`, `repor_curso`, `historico_do_curso` |
| `app/gestao/routes.py` | `GET /gestao/cursos`, `GET`/`POST /gestao/cursos/<chave>`, `POST /gestao/cursos/<chave>/repor` |
| `app/candidatura/routes.py`, `templates/candidatura/plano.html` | Aviso no plano para opções que saíram do catálogo |
| `app/templates/gestao/cursos.html`, `gestao/curso.html` | Páginas da gestão; «Catálogo» no menu e no painel |
| `app/texts.py` | Textos `ADMIN_CURSO*` e `CANDIDATURA_INDISPONIVE*` |
| `tests/test_gestao_catalogo.py` | 25 testes |
