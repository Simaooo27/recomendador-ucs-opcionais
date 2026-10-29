# Documentação

A documentação está organizada por user story: os documentos que valem para todo o projeto ficam em `geral/` e cada story tem a sua pasta `USNN/`, sempre com a mesma estrutura. O estado de cada story está no [PROJETO.md](../PROJETO.md#1-estado-do-projeto).

## Documentos gerais

| Documento | Conteúdo |
|---|---|
| [geral/00-visao-do-produto.md](geral/00-visao-do-produto.md) | Visão do produto: públicos, percurso como sequência de decisões, âmbito do MVP e metas |
| [geral/01-requisitos-funcionais-e-nao-funcionais.md](geral/01-requisitos-funcionais-e-nao-funcionais.md) | Requisitos funcionais, não funcionais, regras de negócio e rastreabilidade |
| [geral/02-regras-de-geracao-de-codigo.md](geral/02-regras-de-geracao-de-codigo.md) | Regras para gerar e rever código com IA, checklist de revisão e Definition of Done |
| [geral/03-arquitetura-e-padroes.md](geral/03-arquitetura-e-padroes.md) | Tecnologias, padrões de desenho existentes e previstos, estrutura dos módulos novos |
| [geral/04-guia-do-codigo.md](geral/04-guia-do-codigo.md) | Guia do código: mapa das pastas, onde mexer, CSS secção a secção, histórico de alterações |
| [geral/05-spike-llm.md](geral/05-spike-llm.md) | Spike do LLM (14/10): limites do plano gratuito, custo, privacidade, termos e viabilidade do Gemini e do Groq |
| [geral/06-aceder-noutro-dispositivo.md](geral/06-aceder-noutro-dispositivo.md) | Abrir o OptaBem no telemóvel ou noutro computador com um túnel do Cloudflare (sem modo debug) |
| [../dados/README.md](../dados/README.md) | Catálogo de instituições e cursos: colunas, fontes e lacunas |
| [geral/registo-de-uso-de-ia.md](geral/registo-de-uso-de-ia.md) | Registo de uso de IA |
| [geral/product-backlog.xlsx](geral/product-backlog.xlsx) | Product Backlog: stories, plano de sprints e resumo MoSCoW |

## Uma pasta por story

### [US01 — Registo com email pessoal](US01/README.md)

| Ficheiro | Conteúdo |
|---|---|
| [US01/README.md](US01/README.md) | Resumo da story, estado, código e testes |
| [US01/requisitos.md](US01/requisitos.md) | Requisitos funcionais e critérios de aceitação |
| [US01/use-case.md](US01/use-case.md) | Use case |
| [US01/bpmn.md](US01/bpmn.md) | Processo BPMN |
| [US01/prompt.md](US01/prompt.md) | Prompt usado para gerar o código com IA |
| [US01/diagramas/use-case.svg](US01/diagramas/use-case.svg) | Diagrama de use case |
| [US01/diagramas/bpmn.svg](US01/diagramas/bpmn.svg) | Diagrama BPMN (imagem) |
| [US01/diagramas/bpmn.bpmn](US01/diagramas/bpmn.bpmn) | Diagrama BPMN (ficheiro editável, BPMN 2.0) |

### [US02 — Autenticação](US02/README.md)

| Ficheiro | Conteúdo |
|---|---|
| [US02/README.md](US02/README.md) | Resumo da story, estado, código e testes |
| [US02/requisitos.md](US02/requisitos.md) | Requisitos funcionais e critérios de aceitação |
| [US02/use-case.md](US02/use-case.md) | Use case |
| [US02/bpmn.md](US02/bpmn.md) | Processo BPMN |
| [US02/prompt.md](US02/prompt.md) | Pedido feito à IA para gerar o código |
| [US02/diagramas/use-case.svg](US02/diagramas/use-case.svg) | Diagrama de use case |
| [US02/diagramas/bpmn.svg](US02/diagramas/bpmn.svg) | Diagrama BPMN (imagem) |
| [US02/diagramas/bpmn.bpmn](US02/diagramas/bpmn.bpmn) | Diagrama BPMN (ficheiro editável, BPMN 2.0) |

### [US03 — Perfis de aluno e administrador](US03/README.md)

| Ficheiro | Conteúdo |
|---|---|
| [US03/README.md](US03/README.md) | Resumo, como criar o primeiro administrador, código e testes |
| [US03/requisitos.md](US03/requisitos.md) | Requisitos funcionais e critérios de aceitação |
| [US03/use-case.md](US03/use-case.md) | Use case |
| [US03/bpmn.md](US03/bpmn.md) | Processos BPMN |
| [US03/prompt.md](US03/prompt.md) | Pedidos feitos à IA (incluindo a revisão do PO) |
| [US03/diagramas/use-case.svg](US03/diagramas/use-case.svg) | Diagrama de use case |
| [US03/diagramas/bpmn.svg](US03/diagramas/bpmn.svg) | Diagrama BPMN (imagem) |
| [US03/diagramas/bpmn.bpmn](US03/diagramas/bpmn.bpmn) | Diagrama BPMN (ficheiro editável, BPMN 2.0) |

### [US29 — Conversa de orientação com o LLM](US29/README.md)

| Ficheiro | Conteúdo |
|---|---|
| [US29/README.md](US29/README.md) | Resumo, como experimentar, código e testes |
| [US29/requisitos.md](US29/requisitos.md) | Requisitos funcionais e critérios de aceitação |
| [US29/use-case.md](US29/use-case.md) | Use case |
| [US29/bpmn.md](US29/bpmn.md) | Processo BPMN |
| [US29/prompt.md](US29/prompt.md) | Pedido feito à IA (incluindo a decisão do PO) |
| [US29/diagramas/use-case.svg](US29/diagramas/use-case.svg) | Diagrama de use case |
| [US29/diagramas/bpmn.svg](US29/diagramas/bpmn.svg) | Diagrama BPMN (imagem) |
| [US29/diagramas/bpmn.bpmn](US29/diagramas/bpmn.bpmn) | Diagrama BPMN (ficheiro editável, BPMN 2.0) |
| [US29/diagramas/gerar.py](US29/diagramas/gerar.py) | Script que gera os três diagramas |

### [US30 — Sugestão de 2 a 3 cursos no fim da conversa](US30/README.md)

| Ficheiro | Conteúdo |
|---|---|
| [US30/README.md](US30/README.md) | Resumo, como experimentar, código e testes |
| [US30/requisitos.md](US30/requisitos.md) | Requisitos funcionais e critérios de aceitação |
| [US30/use-case.md](US30/use-case.md) | Use case |
| [US30/bpmn.md](US30/bpmn.md) | Processo BPMN |
| [US30/prompt.md](US30/prompt.md) | Pedido feito à IA (e decisões a confirmar pelo PO) |
| [US30/diagramas/use-case.svg](US30/diagramas/use-case.svg) | Diagrama de use case |
| [US30/diagramas/bpmn.svg](US30/diagramas/bpmn.svg) | Diagrama BPMN (imagem) |
| [US30/diagramas/bpmn.bpmn](US30/diagramas/bpmn.bpmn) | Diagrama BPMN (ficheiro editável, BPMN 2.0) |
| [US30/diagramas/gerar.py](US30/diagramas/gerar.py) | Script que gera os três diagramas |

### [US31 — Escolher curso e linha do tempo do percurso](US31/README.md)

| Ficheiro | Conteúdo |
|---|---|
| [US31/README.md](US31/README.md) | Resumo, como experimentar, código e testes |
| [US31/requisitos.md](US31/requisitos.md) | Requisitos funcionais e critérios de aceitação |
| [US31/use-case.md](US31/use-case.md) | Use case |
| [US31/bpmn.md](US31/bpmn.md) | Processo BPMN |
| [US31/prompt.md](US31/prompt.md) | Pedido feito à IA (incluindo as decisões do PO) |
| [US31/diagramas/use-case.svg](US31/diagramas/use-case.svg) | Diagrama de use case |
| [US31/diagramas/bpmn.svg](US31/diagramas/bpmn.svg) | Diagrama BPMN (imagem) |
| [US31/diagramas/bpmn.bpmn](US31/diagramas/bpmn.bpmn) | Diagrama BPMN (ficheiro editável, BPMN 2.0) |
| [US31/diagramas/gerar.py](US31/diagramas/gerar.py) | Script que gera os três diagramas |

### [US05 — Consultar e comparar cursos](US05/README.md)

| Ficheiro | Conteúdo |
|---|---|
| [US05/README.md](US05/README.md) | Resumo, como experimentar, código e testes |
| [US05/requisitos.md](US05/requisitos.md) | Requisitos funcionais e critérios de aceitação |
| [US05/use-case.md](US05/use-case.md) | Use case |
| [US05/bpmn.md](US05/bpmn.md) | Processo BPMN |
| [US05/prompt.md](US05/prompt.md) | Pedido feito à IA (incluindo as decisões a confirmar) |
| [US05/diagramas/use-case.svg](US05/diagramas/use-case.svg) | Diagrama de use case |
| [US05/diagramas/bpmn.svg](US05/diagramas/bpmn.svg) | Diagrama BPMN (imagem) |
| [US05/diagramas/bpmn.bpmn](US05/diagramas/bpmn.bpmn) | Diagrama BPMN (ficheiro editável, BPMN 2.0) |
| [US05/diagramas/gerar.py](US05/diagramas/gerar.py) | Script que gera os três diagramas |

### [US17 — Apagar a minha conta](US17/README.md)

| Ficheiro | Conteúdo |
|---|---|
| [US17/README.md](US17/README.md) | Resumo, como experimentar, código e testes |
| [US17/requisitos.md](US17/requisitos.md) | Requisitos funcionais e critérios de aceitação |
| [US17/use-case.md](US17/use-case.md) | Use case |
| [US17/bpmn.md](US17/bpmn.md) | Processo BPMN |
| [US17/prompt.md](US17/prompt.md) | Pedido feito à IA (incluindo a decisão de reduzir o âmbito) |
| [US17/diagramas/use-case.svg](US17/diagramas/use-case.svg) | Diagrama de use case |
| [US17/diagramas/bpmn.svg](US17/diagramas/bpmn.svg) | Diagrama BPMN (imagem) |
| [US17/diagramas/bpmn.bpmn](US17/diagramas/bpmn.bpmn) | Diagrama BPMN (ficheiro editável, BPMN 2.0) |
| [US17/diagramas/gerar.py](US17/diagramas/gerar.py) | Script que gera os três diagramas |

### [US04 — Catálogo de licenciaturas recolhido da DGES](US04/README.md)

| Ficheiro | Conteúdo |
|---|---|
| [US04/README.md](US04/README.md) | Resumo, como experimentar, código e testes |
| [US04/requisitos.md](US04/requisitos.md) | Requisitos funcionais e critérios de aceitação |
| [US04/use-case.md](US04/use-case.md) | Use case |
| [US04/bpmn.md](US04/bpmn.md) | Processo BPMN |
| [US04/prompt.md](US04/prompt.md) | Pedido feito à IA |
| [US04/diagramas/use-case.svg](US04/diagramas/use-case.svg) | Diagrama de use case |
| [US04/diagramas/bpmn.svg](US04/diagramas/bpmn.svg) | Diagrama BPMN (imagem) |
| [US04/diagramas/bpmn.bpmn](US04/diagramas/bpmn.bpmn) | Diagrama BPMN (ficheiro editável, BPMN 2.0) |
| [US04/diagramas/gerar.py](US04/diagramas/gerar.py) | Script que gera os três diagramas |

### [US33 — Condições de acesso na ficha do curso](US33/README.md)

| Ficheiro | Conteúdo |
|---|---|
| [US33/README.md](US33/README.md) | Resumo, como experimentar, código e testes |
| [US33/requisitos.md](US33/requisitos.md) | Requisitos funcionais e critérios de aceitação |
| [US33/use-case.md](US33/use-case.md) | Use case |
| [US33/bpmn.md](US33/bpmn.md) | Processo BPMN |
| [US33/prompt.md](US33/prompt.md) | Pedido feito à IA |
| [US33/diagramas/use-case.svg](US33/diagramas/use-case.svg) | Diagrama de use case |
| [US33/diagramas/bpmn.svg](US33/diagramas/bpmn.svg) | Diagrama BPMN (imagem) |
| [US33/diagramas/bpmn.bpmn](US33/diagramas/bpmn.bpmn) | Diagrama BPMN (ficheiro editável, BPMN 2.0) |
| [US33/diagramas/gerar.py](US33/diagramas/gerar.py) | Script que gera os três diagramas |

### [US34 — Registar as minhas notas](US34/README.md)

| Ficheiro | Conteúdo |
|---|---|
| [US34/README.md](US34/README.md) | Resumo, como experimentar, código e testes |
| [US34/requisitos.md](US34/requisitos.md) | Requisitos funcionais e critérios de aceitação |
| [US34/use-case.md](US34/use-case.md) | Use case |
| [US34/bpmn.md](US34/bpmn.md) | Processo BPMN |
| [US34/prompt.md](US34/prompt.md) | Pedido feito à IA |
| [US34/diagramas/use-case.svg](US34/diagramas/use-case.svg) | Diagrama de use case |
| [US34/diagramas/bpmn.svg](US34/diagramas/bpmn.svg) | Diagrama BPMN (imagem) |
| [US34/diagramas/bpmn.bpmn](US34/diagramas/bpmn.bpmn) | Diagrama BPMN (ficheiro editável, BPMN 2.0) |
| [US34/diagramas/gerar.py](US34/diagramas/gerar.py) | Script que gera os três diagramas |

### [US35 — Nota de candidatura a cada curso](US35/README.md)

| Ficheiro | Conteúdo |
|---|---|
| [US35/README.md](US35/README.md) | Resumo, como experimentar, código e testes |
| [US35/requisitos.md](US35/requisitos.md) | Requisitos funcionais e critérios de aceitação |
| [US35/use-case.md](US35/use-case.md) | Use case |
| [US35/bpmn.md](US35/bpmn.md) | Processo BPMN |
| [US35/prompt.md](US35/prompt.md) | Pedido feito à IA |
| [US35/diagramas/use-case.svg](US35/diagramas/use-case.svg) | Diagrama de use case |
| [US35/diagramas/bpmn.svg](US35/diagramas/bpmn.svg) | Diagrama BPMN (imagem) |
| [US35/diagramas/bpmn.bpmn](US35/diagramas/bpmn.bpmn) | Diagrama BPMN (ficheiro editável, BPMN 2.0) |
| [US35/diagramas/gerar.py](US35/diagramas/gerar.py) | Script que gera os três diagramas |

### [US36 — Plano das 6 opções de candidatura](US36/README.md)

| Ficheiro | Conteúdo |
|---|---|
| [US36/README.md](US36/README.md) | Resumo, como experimentar, código e testes |
| [US36/requisitos.md](US36/requisitos.md) | Requisitos funcionais e critérios de aceitação |
| [US36/use-case.md](US36/use-case.md) | Use case |
| [US36/bpmn.md](US36/bpmn.md) | Processo BPMN |
| [US36/prompt.md](US36/prompt.md) | Pedido feito à IA |
| [US36/diagramas/use-case.svg](US36/diagramas/use-case.svg) | Diagrama de use case |
| [US36/diagramas/bpmn.svg](US36/diagramas/bpmn.svg) | Diagrama BPMN (imagem) |
| [US36/diagramas/bpmn.bpmn](US36/diagramas/bpmn.bpmn) | Diagrama BPMN (ficheiro editável, BPMN 2.0) |
| [US36/diagramas/gerar.py](US36/diagramas/gerar.py) | Script que gera os três diagramas |

### [US40 — Quanto preciso no exame?](US40/README.md)

| Ficheiro | Conteúdo |
|---|---|
| [US40/README.md](US40/README.md) | Resumo, como experimentar, código e testes |
| [US40/requisitos.md](US40/requisitos.md) | Requisitos funcionais e critérios de aceitação |
| [US40/use-case.md](US40/use-case.md) | Use case |
| [US40/bpmn.md](US40/bpmn.md) | Processo BPMN |
| [US40/prompt.md](US40/prompt.md) | Pedido feito à IA |
| [US40/diagramas/use-case.svg](US40/diagramas/use-case.svg) | Diagrama de use case |
| [US40/diagramas/bpmn.svg](US40/diagramas/bpmn.svg) | Diagrama BPMN (imagem) |
| [US40/diagramas/bpmn.bpmn](US40/diagramas/bpmn.bpmn) | Diagrama BPMN (ficheiro editável, BPMN 2.0) |
| [US40/diagramas/gerar.py](US40/diagramas/gerar.py) | Script que gera os três diagramas |

### [US41 — Tendência do último colocado](US41/README.md)

| Ficheiro | Conteúdo |
|---|---|
| [US41/README.md](US41/README.md) | Resumo, como experimentar, código e testes |
| [US41/requisitos.md](US41/requisitos.md) | Requisitos funcionais e critérios de aceitação |
| [US41/use-case.md](US41/use-case.md) | Use case |
| [US41/bpmn.md](US41/bpmn.md) | Processo BPMN |
| [US41/prompt.md](US41/prompt.md) | Pedido feito à IA |
| [US41/diagramas/use-case.svg](US41/diagramas/use-case.svg) | Diagrama de use case |
| [US41/diagramas/bpmn.svg](US41/diagramas/bpmn.svg) | Diagrama BPMN (imagem) |
| [US41/diagramas/bpmn.bpmn](US41/diagramas/bpmn.bpmn) | Diagrama BPMN (ficheiro editável, BPMN 2.0) |
| [US41/diagramas/gerar.py](US41/diagramas/gerar.py) | Script que gera os três diagramas |

### [US42 — Procura do curso](US42/README.md)

| Ficheiro | Conteúdo |
|---|---|
| [US42/README.md](US42/README.md) | Resumo, como experimentar, código e testes |
| [US42/requisitos.md](US42/requisitos.md) | Requisitos funcionais e critérios de aceitação |
| [US42/use-case.md](US42/use-case.md) | Use case |
| [US42/bpmn.md](US42/bpmn.md) | Processo BPMN |
| [US42/prompt.md](US42/prompt.md) | Pedido feito à IA |
| [US42/diagramas/use-case.svg](US42/diagramas/use-case.svg) | Diagrama de use case |
| [US42/diagramas/bpmn.svg](US42/diagramas/bpmn.svg) | Diagrama BPMN (imagem) |
| [US42/diagramas/bpmn.bpmn](US42/diagramas/bpmn.bpmn) | Diagrama BPMN (ficheiro editável, BPMN 2.0) |
| [US42/diagramas/gerar.py](US42/diagramas/gerar.py) | Script que gera os três diagramas |

### [US44 — Que exames me abrem mais portas?](US44/README.md)

| Ficheiro | Conteúdo |
|---|---|
| [US44/README.md](US44/README.md) | Resumo, como experimentar, código e testes |
| [US44/requisitos.md](US44/requisitos.md) | Requisitos funcionais e critérios de aceitação |
| [US44/use-case.md](US44/use-case.md) | Use case |
| [US44/bpmn.md](US44/bpmn.md) | Processo BPMN |
| [US44/prompt.md](US44/prompt.md) | Pedido feito à IA |
| [US44/diagramas/use-case.svg](US44/diagramas/use-case.svg) | Diagrama de use case |
| [US44/diagramas/bpmn.svg](US44/diagramas/bpmn.svg) | Diagrama BPMN (imagem) |
| [US44/diagramas/bpmn.bpmn](US44/diagramas/bpmn.bpmn) | Diagrama BPMN (ficheiro editável, BPMN 2.0) |
| [US44/diagramas/gerar.py](US44/diagramas/gerar.py) | Script que gera os três diagramas |

### [US43 — Partilhar o plano](US43/README.md)

| Ficheiro | Conteúdo |
|---|---|
| [US43/README.md](US43/README.md) | Resumo, como experimentar, código e testes |
| [US43/requisitos.md](US43/requisitos.md) | Requisitos funcionais e critérios de aceitação |
| [US43/use-case.md](US43/use-case.md) | Use case |
| [US43/bpmn.md](US43/bpmn.md) | Processo BPMN |
| [US43/prompt.md](US43/prompt.md) | Pedido feito à IA |
| [US43/diagramas/use-case.svg](US43/diagramas/use-case.svg) | Diagrama de use case |
| [US43/diagramas/bpmn.svg](US43/diagramas/bpmn.svg) | Diagrama BPMN (imagem) |
| [US43/diagramas/bpmn.bpmn](US43/diagramas/bpmn.bpmn) | Diagrama BPMN (ficheiro editável, BPMN 2.0) |
| [US43/diagramas/gerar.py](US43/diagramas/gerar.py) | Script que gera os três diagramas |

### [US45 — Plano B: 2.ª fase](US45/README.md)

| Ficheiro | Conteúdo |
|---|---|
| [US45/README.md](US45/README.md) | Resumo, como experimentar, código e testes |
| [US45/requisitos.md](US45/requisitos.md) | Requisitos funcionais e critérios de aceitação |
| [US45/use-case.md](US45/use-case.md) | Use case |
| [US45/bpmn.md](US45/bpmn.md) | Processo BPMN |
| [US45/prompt.md](US45/prompt.md) | Pedido feito à IA |
| [US45/diagramas/use-case.svg](US45/diagramas/use-case.svg) | Diagrama de use case |
| [US45/diagramas/bpmn.svg](US45/diagramas/bpmn.svg) | Diagrama BPMN (imagem) |
| [US45/diagramas/bpmn.bpmn](US45/diagramas/bpmn.bpmn) | Diagrama BPMN (ficheiro editável, BPMN 2.0) |
| [US45/diagramas/gerar.py](US45/diagramas/gerar.py) | Script que gera os três diagramas |

### [US37 — Assistente que conhece as minhas notas](US37/README.md)

| Ficheiro | Conteúdo |
|---|---|
| [US37/README.md](US37/README.md) | Resumo, como experimentar, código e testes |
| [US37/requisitos.md](US37/requisitos.md) | Requisitos funcionais e critérios de aceitação |
| [US37/use-case.md](US37/use-case.md) | Use case |
| [US37/bpmn.md](US37/bpmn.md) | Processo BPMN |
| [US37/prompt.md](US37/prompt.md) | Pedido feito à IA |
| [US37/diagramas/use-case.svg](US37/diagramas/use-case.svg) | Diagrama de use case |
| [US37/diagramas/bpmn.svg](US37/diagramas/bpmn.svg) | Diagrama BPMN (imagem) |
| [US37/diagramas/bpmn.bpmn](US37/diagramas/bpmn.bpmn) | Diagrama BPMN (ficheiro editável, BPMN 2.0) |
| [US37/diagramas/gerar.py](US37/diagramas/gerar.py) | Script que gera os três diagramas |

### [US38 — Datas do concurso nacional](US38/README.md)

| Ficheiro | Conteúdo |
|---|---|
| [US38/README.md](US38/README.md) | Resumo, como experimentar, código e testes |
| [US38/requisitos.md](US38/requisitos.md) | Requisitos funcionais e critérios de aceitação |
| [US38/use-case.md](US38/use-case.md) | Use case |
| [US38/bpmn.md](US38/bpmn.md) | Processo BPMN |
| [US38/prompt.md](US38/prompt.md) | Pedido feito à IA |
| [US38/diagramas/use-case.svg](US38/diagramas/use-case.svg) | Diagrama de use case |
| [US38/diagramas/bpmn.svg](US38/diagramas/bpmn.svg) | Diagrama BPMN (imagem) |
| [US38/diagramas/bpmn.bpmn](US38/diagramas/bpmn.bpmn) | Diagrama BPMN (ficheiro editável, BPMN 2.0) |
| [US38/diagramas/gerar.py](US38/diagramas/gerar.py) | Script que gera os três diagramas |

### [US39 — Corrigir e esconder cursos do catálogo](US39/README.md)

| Ficheiro | Conteúdo |
|---|---|
| [US39/README.md](US39/README.md) | Resumo, como experimentar, código e testes |
| [US39/requisitos.md](US39/requisitos.md) | Requisitos funcionais e critérios de aceitação |
| [US39/use-case.md](US39/use-case.md) | Use case |
| [US39/bpmn.md](US39/bpmn.md) | Processo BPMN |
| [US39/prompt.md](US39/prompt.md) | Pedido feito à IA |
| [US39/diagramas/use-case.svg](US39/diagramas/use-case.svg) | Diagrama de use case |
| [US39/diagramas/bpmn.svg](US39/diagramas/bpmn.svg) | Diagrama BPMN (imagem) |
| [US39/diagramas/bpmn.bpmn](US39/diagramas/bpmn.bpmn) | Diagrama BPMN (ficheiro editável, BPMN 2.0) |
| [US39/diagramas/gerar.py](US39/diagramas/gerar.py) | Script que gera os três diagramas |

### [US46 — Exportar os meus dados](US46/README.md)

| Ficheiro | Conteúdo |
|---|---|
| [US46/README.md](US46/README.md) | Resumo, como experimentar, código e testes |
| [US46/requisitos.md](US46/requisitos.md) | Requisitos funcionais e critérios de aceitação |
| [US46/use-case.md](US46/use-case.md) | Use case |
| [US46/bpmn.md](US46/bpmn.md) | Processo BPMN |
| [US46/prompt.md](US46/prompt.md) | Pedido feito à IA |
| [US46/diagramas/use-case.svg](US46/diagramas/use-case.svg) | Diagrama de use case |
| [US46/diagramas/bpmn.svg](US46/diagramas/bpmn.svg) | Diagrama BPMN (imagem) |
| [US46/diagramas/bpmn.bpmn](US46/diagramas/bpmn.bpmn) | Diagrama BPMN (ficheiro editável, BPMN 2.0) |
| [US46/diagramas/gerar.py](US46/diagramas/gerar.py) | Script que gera os três diagramas |

### [US47 — Recuperar a palavra-passe](US47/README.md)

| Ficheiro | Conteúdo |
|---|---|
| [US47/README.md](US47/README.md) | Resumo, como experimentar, código e testes |
| [US47/requisitos.md](US47/requisitos.md) | Requisitos funcionais e critérios de aceitação |
| [US47/use-case.md](US47/use-case.md) | Use case |
| [US47/bpmn.md](US47/bpmn.md) | Processo BPMN |
| [US47/prompt.md](US47/prompt.md) | Pedido feito à IA |
| [US47/diagramas/use-case.svg](US47/diagramas/use-case.svg) | Diagrama de use case |
| [US47/diagramas/bpmn.svg](US47/diagramas/bpmn.svg) | Diagrama BPMN (imagem) |
| [US47/diagramas/bpmn.bpmn](US47/diagramas/bpmn.bpmn) | Diagrama BPMN (ficheiro editável, BPMN 2.0) |
| [US47/diagramas/gerar.py](US47/diagramas/gerar.py) | Script que gera os três diagramas |
### [US48 — Recolha completa das licenciaturas](US48/README.md)

| Ficheiro | Conteúdo |
|---|---|
| [US48/README.md](US48/README.md) | O que foi feito, dados e verificação |
| [US48/requisitos.md](US48/requisitos.md) | Critérios de aceitação e como foram verificados |
| [US48/prompt.md](US48/prompt.md) | Pedido feito à IA |

## Nova story

Crie `docs/USNN/` com a mesma estrutura da US01: `README.md`, `requisitos.md`, `use-case.md`, `bpmn.md`, `prompt.md` e `diagramas/`. Acrescente a pasta a este índice e atualize a tabela de estado no [PROJETO.md](../PROJETO.md#1-estado-do-projeto).
