# US34 — Registar as minhas notas

> **Como** candidato, **quero** indicar a minha média do secundário e as notas dos exames nacionais que fiz, **para** o OptaBem fazer as contas por mim.

| | |
|---|---|
| Estado | Feita: aceite pelo PO a 27/10, antes do início formal do Sprint 4 (código de 23/10, documentação e testes em falta a 27/10). Revisão do Simão pendente |
| Sprint | Sprint 4 (29/10 a 05/11) |
| Story points | 2 |
| Épico | E4 — Plano de candidatura |
| Prioridade | Must |
| Requisito de origem | RF41, RF17 (ver [01-requisitos-funcionais-e-nao-funcionais.md](../geral/01-requisitos-funcionais-e-nao-funcionais.md)) |
| Depende de | US02 (sessão iniciada), US33 (lista de provas de ingresso) |
| Necessária para | US35 (nota de candidatura) e US36 (plano das 6 opções) |

## A ideia em três pontos

1. **Uma página só para as notas** (`/candidatura/notas`): a média do secundário e um campo por cada exame. Na Matemática, a pessoa indica o exame que fez (Matemática A, Matemática B ou MACS), e cada um conta para as provas que a DGES aceita. Só se preenchem os exames feitos.
2. **Aceita a nota como a pessoa a conhece:** os exames de 0 a 200 pontos ou de 0 a 20 valores («14,5» conta como 145), com vírgula ou ponto.
3. **As notas são da pessoa:** podem ser mudadas a qualquer momento e saem com a conta (US17). Nunca são enviadas ao LLM.

## Experimentar

```powershell
.\ferramentas\arrancar.bat
```

Iniciar sessão, abrir **«Candidatura»** no menu e carregar em **«Indicar as minhas notas»**. Experimentar uma média de 25 para ver o erro; depois 15,2 e um exame de Português com 14.

## Documentos

| Documento | Conteúdo |
|---|---|
| [requisitos.md](requisitos.md) | Requisitos funcionais e critérios de aceitação, com os testes de cada um |
| [use-case.md](use-case.md) | Use case ([diagrama](diagramas/use-case.svg)) |
| [bpmn.md](bpmn.md) | Processo BPMN ([imagem](diagramas/bpmn.svg) · [ficheiro editável](diagramas/bpmn.bpmn)) |
| [prompt.md](prompt.md) | Pedido feito à IA para gerar o código |

Os diagramas são gerados por [`diagramas/gerar.py`](diagramas/gerar.py): mudar o desenho lá e correr `python docs/US34/diagramas/gerar.py docs/US34/diagramas`.

## Código e testes

| Onde | O quê |
|---|---|
| `app/candidatura/routes.py` | `GET|POST /candidatura/notas`; `_provas_do_formulario` (um campo por exame, com os nomes das Matemáticas) |
| `app/candidatura/services.py` | `ler_notas` (validação), `guardar_notas`, `obter` |
| `app/candidatura/calculos.py` | `ler_numero`, `nota_de_exame` (valores → pontos), `Notas`, `ACEITA` e `NOMES_DOS_EXAMES` (correspondência das Matemáticas) |
| `app/candidatura/repository.py` | SQL da tabela `planos_candidatura` |
| `app/schema.sql` | Tabela `planos_candidatura` (apagada com a conta: `ON DELETE CASCADE`) |
| `app/templates/candidatura/notas.html` | Formulário |
| `app/texts.py` | Textos `CANDIDATURA_NOTAS_*`, `CANDIDATURA_MEDIA*`, `CANDIDATURA_EXAMES*`, `CANDIDATURA_ERRO_*` |
| `tests/test_candidatura.py` | `test_notas_invalidas_nao_sao_guardadas`, `test_o_formulario_pede_os_exames_de_matematica_pelo_nome`, `test_exames_em_valores_ou_em_pontos`, `test_matematica_a_conta_para_as_provas_16_17_e_19`, `test_matematica_b_e_macs_so_contam_para_as_suas_provas`, `test_apagar_a_conta_apaga_o_plano`, entre outros |
