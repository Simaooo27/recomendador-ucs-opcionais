# US30 — Sugestão de 2 a 3 cursos no fim da conversa

> **Como** pessoa indecisa, **quero** que a conversa termine com 2 a 3 cursos do catálogo, cada um com a explicação de porque combina comigo, **para** saber por onde começar.

| | |
|---|---|
| Estado | Feita (aceite na Sprint Review do Sprint 2, 22/10) |
| Sprint | Sprint 2 |
| Story points | 3 |
| Épico | E3 — Orientação com o assistente (E11 até 27/10) |
| Prioridade | Must |
| Requisito de origem | RF37, RF38, RNF12, RN09, RN10 (ver [01-requisitos-funcionais-e-nao-funcionais.md](../geral/01-requisitos-funcionais-e-nao-funcionais.md)) |
| Depende de | [US29](../US29/README.md) (conversa de orientação) e o spike do LLM ([05-spike-llm.md](../geral/05-spike-llm.md)) |
| Necessária para | US31 (escolher um dos cursos sugeridos) |

## A ideia em três pontos

1. **No fim da conversa aparecem 2 a 3 cursos**, com os dados do catálogo e o motivo dado pelo assistente. A pessoa pode pedi-los antes das 6 respostas («Ver sugestões já»).
2. **Só cursos do catálogo.** Os que o LLM inventar são descartados antes de chegar ao ecrã (RN09). Se sobrarem menos de 2, a página diz isso e propõe continuar a conversa ou procurar no catálogo.
3. **Nada é escolhido automaticamente** (RN10). A escolha do curso é a US31.

## Experimentar

```bash
flask --app app run --debug                              # com LLM_BACKEND=gemini no .env
```

Iniciar sessão como aluno, abrir `/orientacao/`, responder a uma ou duas perguntas e carregar em **«Ver sugestões já»**. Com `LLM_BACKEND=falso` (sem chave), o assistente faz uma pergunta simulada e, depois da primeira resposta, sugere sem cursos: serve para ver o caso de poucos cursos. Para ver cursos sugeridos sem rede, correr os testes (`tests/test_sugestoes.py`).

## Definition of Done da US30

A US30 só conta como «Feita» quando todas as caixas estiverem marcadas. As primeiras são os critérios de aceitação desta story (o «Confirmation» dos três C); as outras são o mínimo que a equipa exige a todas. Verificado a 31/10/2026, com 541 testes automáticos a passar.

**Critérios de aceitação desta story**

- [x] A sugestão aparece quando o LLM tem informação suficiente ou ao fim de 6 respostas; a pessoa pode pedi-la antes («Ver sugestões já») (7 testes automáticos, todos a passar)
- [x] Só aparecem cursos do catálogo; os outros são descartados (RN09). Se sobrarem menos de 2, a página diz isso e propõe continuar a conversa ou ver o catálogo (9 testes automáticos, todos a passar)
- [x] Cada curso mostra os dados do catálogo (instituição, localidade, vagas, nota do último colocado, ligação à DGES) e a explicação do LLM (4 testes automáticos, todos a passar)
- [x] Nenhum curso é atribuído automaticamente: a escolha é feita na US31 (RN10) (2 testes automáticos, todos a passar)
- [x] Os testes usam o LLM falso, incluindo respostas com cursos inventados (9 testes automáticos, todos a passar)

**Mínimo da equipa**

- [x] Testes a passar: os desta story e os 541 do projeto
- [x] Código revisto por outro elemento, com atenção a RNF02, RNF06, RNF08, RNF09, RNF10, RNF11, RNF12: código do Simão (PR #22), revisto e juntado pelo Duarte
- [x] Código gerado por IA assinalado no [registo de uso de IA](../geral/registo-de-uso-de-ia.md)
- [x] Documentação em `docs/US30/`: requisitos.md, use-case.md, bpmn.md, prompt.md
- [x] Sem dívida técnica por registar: limitação conhecida e registada — as sugestões apoiam-se no nome e na área do curso: só 29 cursos têm descrição escrita pela equipa
- [x] Funciona na demonstração: Sprint Review do Sprint 2 (22/10), testada pelos dois Product Owners
- [x] Aceite pelo Product Owner: Sprint Review do Sprint 2 (22/10)

## Documentos

| Documento | Conteúdo |
|---|---|
| [requisitos.md](requisitos.md) | Requisitos funcionais e critérios de aceitação |
| [use-case.md](use-case.md) | Use case ([diagrama](diagramas/use-case.svg)) |
| [bpmn.md](bpmn.md) | Processo BPMN ([imagem](diagramas/bpmn.svg) · [ficheiro editável](diagramas/bpmn.bpmn)) |
| [prompt.md](prompt.md) | Pedido feito à IA para gerar o código |

Os diagramas são gerados por [`diagramas/gerar.py`](diagramas/gerar.py): mudar o desenho lá e correr `python docs/US30/diagramas/gerar.py docs/US30/diagramas`.

## Código

| Ficheiro | O que faz |
|---|---|
| [`app/orientacao/services.py`](../../app/orientacao/services.py) | `pedir_sugestao` («Ver sugestões já»), `cursos_sugeridos` (volta a validar contra o catálogo), `continuar_conversa`; `tem_sugestao` só com 2 ou mais cursos |
| [`app/orientacao/routes.py`](../../app/orientacao/routes.py) | Botões `POST /orientacao/sugerir` e `POST /orientacao/continuar` |
| [`app/orientacao/conversa.py`](../../app/orientacao/conversa.py) | `MIN_CURSOS_SUGERIDOS`; a validação contra o catálogo é a do spike |
| [`app/templates/orientacao/conversa.html`](../../app/templates/orientacao/conversa.html) | Os cursos sugeridos, o aviso de poucos cursos e o botão «Ver sugestões já» |
| [`app/templates/macros/marca.html`](../../app/templates/macros/marca.html) | A ficha do curso (`cartao_curso`) aceita a explicação do assistente |
| [`app/catalogo/routes.py`](../../app/catalogo/routes.py), [`app/templates/catalogo/lista.html`](../../app/templates/catalogo/lista.html) | Página `/cursos/` com a pesquisa no catálogo |
| [`app/texts.py`](../../app/texts.py) | Textos (secções «Conversa de orientação» e «Página do catálogo») |
| [`app/static/style.css`](../../app/static/style.css) | Secção 12: cursos sugeridos, explicação, «Ver sugestões já» e página do catálogo |

## Testes

[`tests/test_sugestoes.py`](../../tests/test_sugestoes.py): 20 testes, com o LLM falso (sem rede). A tabela critério de aceitação → teste está na secção 5 de [requisitos.md](requisitos.md#5-critérios-de-aceitação-e-testes).
