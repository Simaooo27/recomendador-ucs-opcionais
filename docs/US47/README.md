# US47 — Recuperar a palavra-passe

> **Como** utilizador que se esqueceu da palavra-passe, **quero** receber uma ligação para definir uma nova, **para** não perder a conta.

| | |
|---|---|
| Estado | Feita: aceite pelo PO a 29/10 (código de 29/10, PR próprio; testada pelo PO com email real). Revisão no GitHub dispensada pelos PO a 31/10 |
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
flask --app app run --debug
```

No início de sessão, carregar em **«Esqueceu-se da palavra-passe?»** e escrever o email de uma conta ativa. Com `MAIL_BACKEND=smtp` no `.env` (ver [`PROJETO.md`](../../PROJETO.md)), a ligação chega ao email; sem isso, aparece no terminal da aplicação. Abrir a ligação, escolher a palavra-passe nova e voltar a abrir a mesma ligação: já não serve.

## Definition of Done da US47

A US47 só conta como «Feita» quando todas as caixas estiverem marcadas. As primeiras são os critérios de aceitação desta story (o «Confirmation» dos três C); as outras são o mínimo que a equipa exige a todas. Verificado a 31/10/2026, com 541 testes automáticos a passar.

**Critérios de aceitação desta story**

- [x] Ligação de uso único, que expira ao fim de 1 hora (9 testes automáticos, todos a passar)
- [x] A mensagem é a mesma quer a conta exista quer não (7 testes automáticos, todos a passar)
- [x] Depois de mudar a palavra-passe, as sessões abertas terminam (4 testes automáticos, todos a passar)
- [x] Ninguém consegue usar o site para encher a caixa de correio de outra pessoa (acrescentado a 31/10) (4 testes automáticos, todos a passar)
- [x] Segurança e acesso (3 testes automáticos, todos a passar)

**Mínimo da equipa**

- [x] Testes a passar: os desta story e os 541 do projeto
- [x] Código revisto por outro elemento, com atenção a RNF02, RNF06, RNF09, RNF11: o PR #51 foi juntado pelo próprio autor; revisão no GitHub dispensada por decisão dos Product Owners a 31/10 (o Simão acompanhou todo o trabalho)
- [x] Código gerado por IA assinalado no [registo de uso de IA](../geral/registo-de-uso-de-ia.md)
- [x] Documentação em `docs/US47/`: requisitos.md, use-case.md, bpmn.md, prompt.md
- [x] Sem dívida técnica por registar
- [ ] Funciona na demonstração: a mostrar na Sprint Review do Sprint 4 (05/11)
- [x] Aceite pelo Product Owner: aceite pelo PO a 29/10

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
