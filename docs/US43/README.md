# US43 — Partilhar o plano

> **Como** candidato, **quero** partilhar o meu plano com quem me ajuda a decidir (pais, explicador), com uma ligação só de leitura, **para** pedir opinião sem dar a minha palavra-passe.

| | |
|---|---|
| Estado | Feita: aceite pelo PO a 27/10, antes do início formal do Sprint 4 (código de 23/10, documentação e testes em falta a 27/10). Revisão do Simão pendente |
| Sprint | Sprint 4 (29/10 a 05/11), por decisão do PO a 27/10 |
| Story points | 3 |
| Épico | E4 — Plano de candidatura |
| Prioridade | Could |
| Requisito de origem | RF47, RF17 (ver [01-requisitos-funcionais-e-nao-funcionais.md](../geral/01-requisitos-funcionais-e-nao-funcionais.md)) |
| Depende de | US36 (plano) |

## A ideia em três pontos

1. **«Criar ligação de partilha»** no plano dá um endereço com um código aleatório (`/candidatura/p/<código>`). Quem o tem vê o plano sem iniciar sessão.
2. **Só o necessário:** o primeiro nome, as opções, a nota de candidatura e a situação em cada uma. Nunca o email, a média nem as notas dos exames.
3. **«Deixar de partilhar»** apaga o código: a ligação deixa de funcionar de imediato. A página partilhada não é indexada pelos motores de pesquisa.

## Experimentar

```powershell
flask --app app run --debug
```

Com sessão, abrir o plano e carregar em **«Criar ligação de partilha»**. Abrir a ligação numa janela privada (sem sessão). Voltar ao plano, carregar em **«Deixar de partilhar»** e ver que a ligação dá «página não encontrada».

## Definition of Done da US43

A US43 só conta como «Feita» quando todas as caixas estiverem marcadas. As primeiras são os critérios de aceitação desta story (o «Confirmation» dos três C); as outras são o mínimo que a equipa exige a todas. Verificado a 31/10/2026, com 541 testes automáticos a passar.

**Critérios de aceitação desta story**

- [x] Ligação com um código aleatório; quem a tem vê o plano sem iniciar sessão (2 testes automáticos, todos a passar)
- [x] Mostra o primeiro nome, as opções, a nota de candidatura e a situação; nunca o email, a média nem os exames (1 teste automático, a passar)
- [x] «Deixar de partilhar» invalida a ligação de imediato (2 testes automáticos, todos a passar)
- [x] A página não é indexada pelos motores de pesquisa (1 teste automático, a passar)
- [x] Segurança (1 teste automático, a passar)

**Mínimo da equipa**

- [x] Testes a passar: os desta story e os 541 do projeto
- [ ] Código revisto por outro elemento, com atenção a RNF01, RNF02, RNF06, RNF09, RNF11: o código entrou na main pelo PR #45, juntado pelo Simão, mas a revisão dele está registada como pendente. **Falta a revisão do Simão**
- [x] Código gerado por IA assinalado no [registo de uso de IA](../geral/registo-de-uso-de-ia.md)
- [x] Documentação em `docs/US43/`: requisitos.md, use-case.md, bpmn.md, prompt.md
- [x] Sem dívida técnica por registar
- [ ] Funciona na demonstração: a mostrar na Sprint Review do Sprint 4 (05/11)
- [x] Aceite pelo Product Owner: aceite pelo PO a 27/10

## Documentos

| Documento | Conteúdo |
|---|---|
| [requisitos.md](requisitos.md) | Requisitos funcionais e critérios de aceitação, com os testes de cada um |
| [use-case.md](use-case.md) | Use case ([diagrama](diagramas/use-case.svg)) |
| [bpmn.md](bpmn.md) | Processo BPMN ([imagem](diagramas/bpmn.svg) · [ficheiro editável](diagramas/bpmn.bpmn)) |
| [prompt.md](prompt.md) | Pedido feito à IA para gerar o código |

Os diagramas são gerados por [`diagramas/gerar.py`](diagramas/gerar.py): mudar o desenho lá e correr `python docs/US43/diagramas/gerar.py docs/US43/diagramas`.

## Código e testes

| Onde | O quê |
|---|---|
| `app/candidatura/routes.py` | `POST /candidatura/partilhar`, `POST /candidatura/deixar-de-partilhar`, `GET /candidatura/p/<codigo>` |
| `app/candidatura/services.py` | `partilhar`, `deixar_de_partilhar`, `plano_partilhado`, `PlanoPartilhado` |
| `app/candidatura/repository.py` | `por_partilha`, `mudar_partilha`, `partilha` |
| `app/schema.sql` | Coluna `partilha` (única) em `planos_candidatura` |
| `app/templates/candidatura/partilhado.html` | Página só de leitura (`noindex`) |
| `app/texts.py` | Textos `PARTILHA_*` |
| `tests/test_candidatura.py` | `test_partilhar_mostra_o_plano_sem_dados_pessoais_e_desligar_invalida`, `test_codigo_de_partilha_errado_da_404`, `test_partilhar_exige_csrf` |
| `tests/test_site_publico.py` | `test_ligacao_de_partilha_tem_o_endereco_do_tunel` |
