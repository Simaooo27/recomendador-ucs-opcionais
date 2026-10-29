# US46 — Exportar os meus dados

> **Como** utilizador, **quero** descarregar todos os dados que o OptaBem guarda sobre mim, **para** exercer o meu direito de acesso e de portabilidade.

| | |
|---|---|
| Estado | Feita: aceite pelo PO a 29/10 (código de 29/10, PR próprio). Revisão do Simão pendente |
| Sprint | Sprint 4 (29/10 a 05/11), por decisão do PO a 29/10 |
| Story points | 2 |
| Épico | E1 — Conta e privacidade |
| Prioridade | Should |
| Requisito de origem | RF17 (exportação), RNF01 (ver [01-requisitos-funcionais-e-nao-funcionais.md](../geral/01-requisitos-funcionais-e-nao-funcionais.md)) |
| Depende de | US02 (sessão); US17 (página «A minha conta») |

## A ideia em três pontos

1. Em **«A minha conta» › «Os meus dados»**, a ligação **«Descarregar os meus dados»** abre uma página que diz o que vai no ficheiro.
2. Para descarregar, **pede a palavra-passe**. O ficheiro (JSON) tem a conta, as decisões do percurso, o plano de candidatura, a conversa de orientação e os pedidos ao assistente.
3. **Fica de fora** o que não é um dado da pessoa e facilitaria um ataque à conta: o hash da palavra-passe, o valor interno da confirmação do email e o código da ligação de partilha (o ficheiro diz só se o plano está partilhado). **Nunca** há dados de outros utilizadores.

## Experimentar

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\ferramentas\arrancar.ps1
```

Iniciar sessão, abrir **«A minha conta»** (ícone de conta, no topo) e carregar em **«Descarregar os meus dados»**. Escrever a palavra-passe e abrir o ficheiro descarregado (`optabem-os-meus-dados-AAAA-MM-DD.json`) num editor de texto.

## Documentos

| Documento | Conteúdo |
|---|---|
| [requisitos.md](requisitos.md) | Requisitos funcionais e critérios de aceitação, com os testes de cada um |
| [use-case.md](use-case.md) | Use case ([diagrama](diagramas/use-case.svg)) |
| [bpmn.md](bpmn.md) | Processo BPMN ([imagem](diagramas/bpmn.svg) · [ficheiro editável](diagramas/bpmn.bpmn)) |
| [prompt.md](prompt.md) | Pedido feito à IA para gerar o código |

Os diagramas são gerados por [`diagramas/gerar.py`](diagramas/gerar.py): mudar o desenho lá e correr `python docs/US46/diagramas/gerar.py docs/US46/diagramas`.

## Código e testes

| Onde | O quê |
|---|---|
| `app/auth/exportar.py` | `dados_do_utilizador` (junta tudo o que é do aluno), `nome_do_ficheiro` |
| `app/auth/routes.py` | `GET` e `POST /auth/conta/exportar` (`export_form`, `export_submit`) |
| `app/auth/services.py` | `confirma_password` |
| `app/orientacao/repository.py` | `pedidos_do_utilizador` |
| `app/templates/auth/exportar.html`, `auth/conta.html` | Página da exportação; secção «Os meus dados» em «A minha conta» |
| `app/texts.py` | Textos `EXPORTAR_*` e `CONTA_EXPORTAR_*`; política de privacidade provisória |
| `tests/test_exportar.py` | 16 testes |
