# US04 — Catálogo de licenciaturas recolhido da DGES

> **Como** pessoa indecisa, **quero** procurar num catálogo de licenciaturas recolhido da DGES, e não só numa amostra escrita à mão, **para** ver cursos de muitas instituições com dados oficiais.

| | |
|---|---|
| Estado | Protótipo (código feito antes do Sprint 4, no PR #44; por aceitar na Sprint Review) |
| Sprint | Sprint 4 (29/10 a 05/11) |
| Story points | 5 |
| Épico | E2 — Catálogo de cursos |
| Prioridade | Must |
| Requisito de origem | RF05, RNF03 (ver [01-requisitos-funcionais-e-nao-funcionais.md](../geral/01-requisitos-funcionais-e-nao-funcionais.md)) |
| Depende de | Catálogo do MVP (`dados/catalogo-cursos-mvp.csv`), cujas descrições se mantêm |
| Necessária para | Condições de acesso (US33) e todo o plano de candidatura (US34 a US36) |
| Dividida a 27/10 | A recolha de **todas** as licenciaturas passou para a US48 (Backlog): o código é o mesmo, mas correr a recolha completa exige o computador ligado uma noite inteira |

## A ideia em três pontos

1. **Um script da equipa recolhe as páginas públicas da DGES** («Guia da Candidatura»), devagar (um pedido a cada 2 segundos) e de forma retomável, e escreve `dados/catalogo-cursos.csv`. A aplicação nunca vai à internet: só lê o CSV.
2. **O catálogo cresce de 30 para 174 cursos** (os 30 do MVP e os cursos das páginas já recolhidas), com vagas, nota do último colocado e condições de acesso. Os cursos do MVP mantêm a descrição e as saídas escritas pela equipa.
3. **A aplicação aguenta um catálogo grande:** a lista de cursos tem páginas de 24, e acima de 150 cursos o assistente (LLM) recebe primeiro só as áreas e depois só os cursos dessas áreas, para o pedido não ficar enorme.

## Experimentar

```powershell
.\ferramentas\arrancar.bat
```

Abrir http://127.0.0.1:5000/cursos/ e ver a contagem («… de 174 cursos») e a navegação entre páginas no fim da lista. Para refazer o CSV a partir das páginas já guardadas (sem pedir nada à DGES):

```powershell
python dados/recolher_dges.py processar
```

## Documentos

| Documento | Conteúdo |
|---|---|
| [requisitos.md](requisitos.md) | Requisitos funcionais e critérios de aceitação, com os testes de cada um |
| [use-case.md](use-case.md) | Use case ([diagrama](diagramas/use-case.svg)) |
| [bpmn.md](bpmn.md) | Processo BPMN ([imagem](diagramas/bpmn.svg) · [ficheiro editável](diagramas/bpmn.bpmn)) |
| [prompt.md](prompt.md) | Pedido feito à IA para gerar o código |

Os diagramas são gerados por [`diagramas/gerar.py`](diagramas/gerar.py): mudar o desenho lá e correr `python docs/US04/diagramas/gerar.py docs/US04/diagramas`.

## Código e testes

| Onde | O quê |
|---|---|
| `dados/recolher_dges.py` | Ações `amostra`, `mvp`, `descarregar` (retomável) e `processar` (lê as páginas guardadas e escreve o CSV). Só usa a biblioteca padrão |
| `dados/catalogo-cursos.csv` | O catálogo recolhido (174 cursos); `dados/provas-ingresso.csv` tem o nome de cada prova |
| `dados/README.md` | Colunas do CSV, fontes e limitações dos dados |
| `app/config.py` | `CATALOGO_CSV`: usa o catálogo recolhido se existir, senão o do MVP |
| `app/catalogo/services.py` | `paginar` e `POR_PAGINA = 24` |
| `app/orientacao/conversa.py` | Filtro por área: `MAX_CURSOS_DIRETO = 150`, `MAX_CURSOS_ENVIADOS = 80` |
| `tests/test_us04_catalogo_completo.py` | `LeituraDaPaginaTests` (6) e `FiltroPorAreaTests` (9) |
| `tests/test_catalogo.py` | `PaginacaoTests` (4) |
