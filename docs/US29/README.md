# US29 — Conversa de orientação com o LLM

> **Como** pessoa indecisa, **quero** conversar com um assistente que me vai fazendo perguntas sobre os meus interesses, **para** perceber o que procuro num curso sem preencher um questionário fixo.

| | |
|---|---|
| Estado | Feita (por rever) |
| Sprint | Sprint 2 (feita antes do início do sprint, por decisão do PO de 14/10) |
| Story points | 5 |
| Épico | E11 — Orientação de curso |
| Prioridade | Must |
| Requisito de origem | RF36, RNF12 (ver [01-requisitos-funcionais-e-nao-funcionais.md](../geral/01-requisitos-funcionais-e-nao-funcionais.md)) |
| Depende de | Spike do LLM ([05-spike-llm.md](../geral/05-spike-llm.md)): `app/llm/` e `app/orientacao/conversa.py` |
| Necessária para | US30 (mostrar os cursos sugeridos), US31 (escolher curso) |

## A ideia em três pontos

1. **Quem pergunta é o LLM.** As perguntas não são fixas: o assistente faz uma de cada vez, a partir das respostas anteriores, no máximo 6. Depois tem de sugerir cursos.
2. **A conversa fica no servidor**, uma por aluno, e pode ser recomeçada (apagada). Não cabe no cookie de sessão.
3. **Nada de dados pessoais.** O LLM nunca recebe o email nem o nome da conta. Emails e números longos que o aluno escreva são apagados antes de enviar **e** antes de guardar; a página avisa para não escrever o nome.

## Experimentar

```bash
flask --app app init-db                                  # cria a tabela nova (não apaga dados)
flask --app app run --debug                              # com LLM_BACKEND=gemini no .env
```

Iniciar sessão como aluno e, na página inicial, carregar em **«Começar a conversa»** (ou abrir `/orientacao/`). Com `LLM_BACKEND=falso` a página funciona, mas o assistente repete sempre a mesma pergunta simulada.

Quando a conversa termina, a página diz que as sugestões aparecem em breve: mostrar os cursos é a US30.

## Documentos

| Documento | Conteúdo |
|---|---|
| [requisitos.md](requisitos.md) | Requisitos funcionais e critérios de aceitação |
| [use-case.md](use-case.md) | Use case ([diagrama](diagramas/use-case.svg)) |
| [bpmn.md](bpmn.md) | Processo BPMN ([imagem](diagramas/bpmn.svg) · [ficheiro editável](diagramas/bpmn.bpmn)) |
| [prompt.md](prompt.md) | Pedido feito à IA para gerar o código |

Os diagramas são gerados por [`diagramas/gerar.py`](diagramas/gerar.py): mudar o desenho lá e correr `python docs/US29/diagramas/gerar.py docs/US29/diagramas`.

## Código

| Ficheiro | O que faz |
|---|---|
| [`app/orientacao/routes.py`](../../app/orientacao/routes.py) | Página `/orientacao/` e os botões Começar, Enviar, Tentar de novo e Recomeçar (só os botões chamam o LLM) |
| [`app/orientacao/services.py`](../../app/orientacao/services.py) | Regras: começar, responder (validar, apagar dados pessoais, guardar, pedir o passo seguinte), tentar de novo, recomeçar |
| [`app/orientacao/repository.py`](../../app/orientacao/repository.py) | SQL da tabela `conversas_orientacao` |
| [`app/orientacao/conversa.py`](../../app/orientacao/conversa.py) | Do spike: pedido ao LLM, limite de 6 perguntas, validação contra o catálogo |
| [`app/templates/orientacao/conversa.html`](../../app/templates/orientacao/conversa.html) | A página da conversa |
| [`app/percurso.py`](../../app/percurso.py), [`app/templates/home.html`](../../app/templates/home.html) | Botão «Começar a conversa» na linha do tempo; conversa terminada avança o percurso |
| [`app/schema.sql`](../../app/schema.sql) | Tabela `conversas_orientacao` |
| [`app/texts.py`](../../app/texts.py) | Textos (secção «Conversa de orientação») |
| [`app/static/style.css`](../../app/static/style.css) | Secção 12: mensagens, aviso, botão secundário |

## Testes

[`tests/test_conversa.py`](../../tests/test_conversa.py): 21 testes, com o LLM falso (sem rede). A tabela critério de aceitação → teste está na secção 5 de [requisitos.md](requisitos.md#5-critérios-de-aceitação-e-testes).
