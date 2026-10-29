# US47 — Recuperar a palavra-passe

> **Como** utilizador que se esqueceu da palavra-passe, **quero** receber uma ligação para definir uma nova, **para** não perder a conta.

| | |
|---|---|
| Estado | Feita: aceite pelo PO a 29/10 (código de 29/10, PR próprio; testada pelo PO com email real). Revisão do Simão pendente |
| Sprint | Sprint 4 (29/10 a 05/11), por decisão do PO a 29/10 |
| Story points | 3 |
| Épico | E1 — Conta e privacidade |
| Prioridade | Should |
| Requisito de origem | RF02 (recuperação) (ver [01-requisitos-funcionais-e-nao-funcionais.md](../geral/01-requisitos-funcionais-e-nao-funcionais.md)) |
| Depende de | US01 (conta e email), US02 (sessão) |

## A ideia em três pontos

1. **«Esqueceu-se da palavra-passe?»**, no início de sessão, pede o email e responde sempre **«Veja o seu email»**, quer a conta exista quer não. Só contas ativas recebem a ligação, por email; a ligação nunca aparece na página.
2. A ligação **serve uma só vez e durante 1 hora**. O token leva uma impressão da palavra-passe atual: quando a palavra-passe muda, a impressão deixa de bater certo e a ligação deixa de servir.
3. Ao mudar a palavra-passe, **todas as sessões abertas da conta terminam**, em qualquer dispositivo (a sessão guarda a mesma impressão).

## Experimentar

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\ferramentas\arrancar.ps1
```

No início de sessão, carregar em **«Esqueceu-se da palavra-passe?»** e escrever o email de uma conta ativa. Com `MAIL_BACKEND=smtp` no `.env` (ver [`PROJETO.md`](../../PROJETO.md)), a ligação chega ao email; sem isso, aparece no terminal da aplicação. Abrir a ligação, escolher a palavra-passe nova e voltar a abrir a mesma ligação: já não serve.

## Documentos

| Documento | Conteúdo |
|---|---|
| [requisitos.md](requisitos.md) | Requisitos funcionais e critérios de aceitação, com os testes de cada um |
| [use-case.md](use-case.md) | Use case ([diagrama](diagramas/use-case.svg)) |
| [bpmn.md](bpmn.md) | Processo BPMN ([imagem](diagramas/bpmn.svg) · [ficheiro editável](diagramas/bpmn.bpmn)) |
| [prompt.md](prompt.md) | Pedido feito à IA para gerar o código |

Os diagramas são gerados por [`diagramas/gerar.py`](diagramas/gerar.py): mudar o desenho lá e correr `python docs/US47/diagramas/gerar.py docs/US47/diagramas`.

## Código e testes

| Onde | O quê |
|---|---|
| `app/auth/routes.py` | `GET`/`POST /auth/recuperar`, `/auth/recuperar/enviado`, `GET`/`POST /auth/recuperar/<token>` |
| `app/auth/services.py` | `pedir_recuperacao`, `verificar_recuperacao`, `recuperar_password` |
| `app/auth/tokens.py` | `impressao_da_password`, `make_reset_token`, `read_reset_token` (sal próprio) |
| `app/auth/sessions.py` | A sessão guarda a impressão da palavra-passe e termina quando ela muda |
| `app/auth/validators.py` | `password_errors` (as mesmas regras do registo) |
| `app/auth/repository.py` | `update_password` |
| `app/config.py` | `RESET_TOKEN_MAX_AGE_SECONDS` (1 hora) |
| `app/templates/auth/recuperar*.html`, `auth/login.html` | Páginas da recuperação; ligação no início de sessão |
| `app/texts.py` | Textos `RECUPERAR_*` e `LOGIN_FORGOT` |
| `tests/test_recuperar_password.py` | 23 testes |
