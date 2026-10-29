# US35 — Nota de candidatura a cada curso

> **Como** candidato, **quero** ver a minha nota de candidatura a cada curso e a diferença para o último colocado, **para** perceber onde tenho hipóteses.

| | |
|---|---|
| Estado | Feita: aceite pelo PO a 27/10, antes do início formal do Sprint 4 (código de 23/10, documentação e testes em falta a 27/10). Revisão do Simão pendente |
| Sprint | Sprint 4 (29/10 a 05/11) |
| Story points | 3 |
| Épico | E4 — Plano de candidatura |
| Prioridade | Must |
| Requisito de origem | RF42, RN11 (ver [01-requisitos-funcionais-e-nao-funcionais.md](../geral/01-requisitos-funcionais-e-nao-funcionais.md)) |
| Depende de | US33 (condições de acesso) e US34 (notas do aluno) |
| Necessária para | US36 (plano das 6 opções) |

## A ideia em três pontos

1. **Na ficha de cada curso, com sessão, aparece «A sua nota neste curso»:** a nota de candidatura (0 a 200) calculada com a fórmula do curso e o conjunto de provas que dá a nota mais alta.
2. **A situação diz onde a pessoa está:** acima do último colocado (5 ou mais pontos), perto (menos de 5 de diferença) ou abaixo. Quando não conta, diz porquê: falta uma prova (e qual) ou a nota fica abaixo de um mínimo.
3. **É uma estimativa** para o contingente geral da 1.ª fase, e a página di-lo sempre que mostra uma nota.

## Experimentar

```powershell
.\ferramentas\arrancar.bat
```

Iniciar sessão, indicar as notas (US34) e abrir a ficha de alguns cursos e procurar a secção **«A sua nota neste curso»**.

## Documentos

| Documento | Conteúdo |
|---|---|
| [requisitos.md](requisitos.md) | Requisitos funcionais e critérios de aceitação, com os testes de cada um |
| [use-case.md](use-case.md) | Use case ([diagrama](diagramas/use-case.svg)) |
| [bpmn.md](bpmn.md) | Processo BPMN ([imagem](diagramas/bpmn.svg) · [ficheiro editável](diagramas/bpmn.bpmn)) |
| [prompt.md](prompt.md) | Pedido feito à IA para gerar o código |

Os diagramas são gerados por [`diagramas/gerar.py`](diagramas/gerar.py): mudar o desenho lá e correr `python docs/US35/diagramas/gerar.py docs/US35/diagramas`.

## Código e testes

| Onde | O quê |
|---|---|
| `app/candidatura/calculos.py` | `simular`, `_comparar`, `Situacao`, `Simulacao`, `MARGEM = 5` (funções puras, sem Flask nem base de dados) |
| `app/catalogo/routes.py` | A ficha calcula a simulação quando há sessão |
| `app/templates/macros/candidatura.html` | Macro `situacao` |
| `app/templates/catalogo/ficha.html` | Secção «A sua nota neste curso» e aviso de estimativa |
| `app/texts.py` | Textos `CANDIDATURA_SITUACAO_*`, `CANDIDATURA_FALTA`, `CANDIDATURA_MINIMO_*`, `CANDIDATURA_CONJUNTO_USADO`, `CANDIDATURA_AVISO_ESTIMATIVA` |
| `tests/test_candidatura.py` | `ContasTests` (8 testes), `test_a_ficha_mostra_as_condicoes_de_acesso_e_a_nota_do_aluno`, `test_a_ficha_e_o_plano_dizem_que_a_nota_e_uma_estimativa` |
