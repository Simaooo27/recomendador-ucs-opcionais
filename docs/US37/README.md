# US37 — Assistente que conhece as minhas notas

> **Como** pessoa indecisa, **quero** que o assistente tenha em conta as provas que fiz e a minha nota, **para** não me sugerir cursos a que não posso concorrer.

| | |
|---|---|
| Estado | Feita: aceite pelo PO a 29/10 (código de 29/10, PR próprio). Revisão do Simão pendente |
| Sprint | Sprint 4 (29/10 a 05/11), por decisão do PO a 29/10 |
| Story points | 3 |
| Épico | E3 — Orientação com o assistente |
| Prioridade | Should |
| Requisitos de origem | RF36, RF41, RNF12; detalhe no RF52 (ver [01-requisitos-funcionais-e-nao-funcionais.md](../geral/01-requisitos-funcionais-e-nao-funcionais.md)) |
| Depende de | US29 (conversa com o assistente), US34 (registar as notas no plano de candidatura) |

## A ideia em três pontos

1. Ao começar a conversa, quem já indicou exames no plano de candidatura vê uma **caixa desmarcada** para autorizar o assistente a usá-los. O texto ao lado diz **exatamente o que ele recebe**. Sem exames no plano, não há caixa, só uma ligação para o plano.
2. Com autorização, cada pedido ao LLM leva **os nomes dos exames feitos e a média num intervalo de 2 valores** (por exemplo, «entre 14 e 16»). **Nunca a média exata nem a nota de cada exame** (RNF12). A autorização fica nessa conversa e sai ao recomeçar.
3. Os **cursos a que falta uma prova de ingresso não são enviados** ao assistente. Se sobrarem menos de 10, vai o catálogo inteiro e a página **assinala, em cada curso sugerido, o exame que falta**.

## Experimentar

```powershell
flask --app app run --debug
```

Com sessão, indicar dois ou três exames e a média no **plano de candidatura**. Abrir a **conversa com o assistente**, marcar a caixa e começar. Os cursos sugeridos não pedem exames que a pessoa não fez. Para ver o que o LLM recebeu sem gastar a chave, correr os testes (usam o LLM falso).

## Definition of Done da US37

A US37 só conta como «Feita» quando todas as caixas estiverem marcadas. As primeiras são os critérios de aceitação desta story (o «Confirmation» dos três C); as outras são o mínimo que a equipa exige a todas. Verificado a 31/10/2026, com 541 testes automáticos a passar.

**Critérios de aceitação desta story**

- [x] Só com autorização da pessoa, o LLM recebe as provas feitas e um intervalo de nota (nunca a média exata, RNF12) (11 testes automáticos, todos a passar)
- [x] Cursos a que falta uma prova não são sugeridos, ou vêm assinalados (7 testes automáticos, todos a passar)
- [x] Os testes usam o LLM falso (verificado no código: todos os testes desta story usam o `LLMFalso` e correm sem rede)

**Mínimo da equipa**

- [x] Testes a passar: os desta story e os 541 do projeto
- [ ] Código revisto por outro elemento, com atenção a RNF06, RNF09, RNF11, RNF12: os PR #54 e #59 foram juntados pelo próprio autor. **Falta a revisão do Simão**
- [x] Código gerado por IA assinalado no [registo de uso de IA](../geral/registo-de-uso-de-ia.md)
- [x] Documentação em `docs/US37/`: requisitos.md, use-case.md, bpmn.md, prompt.md
- [x] Sem dívida técnica por registar: limitação conhecida e registada — esta é a primeira story que envia dados do aluno ao Gemini (só com autorização e com a média num intervalo)
- [ ] Funciona na demonstração: a mostrar na Sprint Review do Sprint 4 (05/11)
- [x] Aceite pelo Product Owner: aceite pelo PO a 29/10

## Documentos

| Documento | Conteúdo |
|---|---|
| [requisitos.md](requisitos.md) | Requisitos funcionais e critérios de aceitação, com os testes de cada um |
| [use-case.md](use-case.md) | Use case ([diagrama](diagramas/use-case.svg)) |
| [bpmn.md](bpmn.md) | Processo BPMN ([imagem](diagramas/bpmn.svg) · [ficheiro editável](diagramas/bpmn.bpmn)) |
| [prompt.md](prompt.md) | Pedido feito à IA para gerar o código |

Os diagramas são gerados por [`diagramas/gerar.py`](diagramas/gerar.py): mudar o desenho lá e correr `python docs/US37/diagramas/gerar.py docs/US37/diagramas`.

## Código e testes

| Onde | O quê |
|---|---|
| `app/orientacao/notas.py` | `intervalo_da_media`, `contexto` (o texto que vai nas instruções), `cursos_para_enviar`, `em_falta_por_curso` |
| `app/candidatura/calculos.py` | `provas_em_falta`: as provas em falta sem precisar da média |
| `app/orientacao/conversa.py` | `proximo_passo(..., contexto="")` junta o contexto às instruções |
| `app/orientacao/services.py` | `comecar(..., usar_notas)`, `pode_usar_notas`, `o_que_o_assistente_recebe`, `em_falta_nas_sugestoes` |
| `app/schema.sql`, `app/db.py` | Coluna `conversas_orientacao.usar_notas` (com migração) |
| `app/orientacao/routes.py`, `templates/orientacao/conversa.html` | A caixa, o texto do que é enviado e o aviso nos cursos sugeridos |
| `app/texts.py` | Textos `ORIENTACAO_NOTAS_*` e `ORIENTACAO_FALTA_PROVA*` |
| `tests/test_assistente_notas.py` | 18 testes, com o LLM falso |
