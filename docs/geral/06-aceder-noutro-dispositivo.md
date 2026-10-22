# Abrir o OptaBem noutro dispositivo (telemóvel ou outro computador)

Versão 1.0 · 22/10/2026 · Decisão do PO

O OptaBem corre no computador de um elemento da equipa. Este guia explica como o abrir noutro computador ou no telemóvel, por exemplo para a demonstração ou para o outro elemento da equipa experimentar a conversa com o Gemini, **sem publicar o site**.

## 1. Decisão

| Opção | Resultado |
|---|---|
| **Túnel rápido do Cloudflare** (`cloudflared`) | **Escolhida.** Grátis, sem conta, sem abrir portas no router. Dá um endereço `https://….trycloudflare.com` que funciona enquanto o túnel estiver aberto. |
| Mesma rede Wi-Fi (`--host 0.0.0.0`) | Alternativa quando o telemóvel está na mesma rede que o computador. Não serve fora de casa. |
| Túnel com nome do Cloudflare | Posto de parte: dá um endereço fixo, mas exige um domínio próprio (pago). Não acrescenta nada ao objetivo. |
| Máquina virtual no Google Cloud (e2-micro) | Posto de parte: ficaria sempre online e passaria o Gemini para o plano pago, mas dá trabalho de configuração e manutenção e não conta para a avaliação. |
| Mudar de SQLite para MySQL | Não é necessário: quem entra pelo túnel usa a aplicação e a base de dados do computador onde ela corre. As contas criadas pelo túnel ficam guardadas no `instance/app.sqlite3` desse computador. |

Limitações do túnel rápido: o endereço é aleatório e muda sempre que o túnel é reaberto; só funciona enquanto o computador e a aplicação estiverem ligados; o Cloudflare indica-o para testes e desenvolvimento, não para um site em produção.

## 2. Instalar o `cloudflared` (uma vez)

No PowerShell (ou no terminal do VS Code):

```powershell
winget install --id Cloudflare.cloudflared --source winget
```

Fechar e voltar a abrir o terminal e confirmar com `cloudflared --version`.

## 3. Criar o arranque sem modo debug (uma vez)

> **Importante:** o `arrancar.bat` arranca o Flask com `--debug`. O depurador do Flask permite executar código no computador a partir de uma página de erro, por isso **nunca se abre um túnel com o modo debug ligado.**

A pasta `ferramentas/` não vai para o GitHub (ver o [Guia do código](04-guia-do-codigo.md#1-a-pasta-do-projeto)), por isso cada um cria a cópia sem debug no seu computador. Na pasta do projeto:

```powershell
(Get-Content .\ferramentas\arrancar.ps1) -replace ' --debug','' | Set-Content .\ferramentas\arrancar-tunel.ps1
```

## 4. Abrir o OptaBem pelo túnel (no VS Code)

1. Abrir a pasta do projeto no VS Code e um terminal (**Terminal → New Terminal**).
2. Arrancar a aplicação sem debug:
   ```powershell
   powershell -NoProfile -ExecutionPolicy Bypass -File .\ferramentas\arrancar-tunel.ps1
   ```
   Confirmar que aparece `Debug mode: off`.
3. Abrir um **segundo** terminal (botão **+** no painel do terminal) e abrir o túnel:
   ```powershell
   cloudflared tunnel --url http://localhost:5000
   ```
4. Copiar o endereço `https://….trycloudflare.com` que aparece na caixa e enviá-lo para o telemóvel (por mensagem ou email) em vez de o escrever à mão: é longo e é fácil errar uma letra.
5. Para terminar: `Ctrl+C` nos dois terminais (ou fechar o painel do terminal / o VS Code).

O aviso do `cloudflared` sobre o *certificate pool* pode ser ignorado: a ligação local ao Flask é `http`, o HTTPS do endereço público é tratado pelo Cloudflare.

## 5. A conversa com o Gemini através do túnel

- O pedido ao Gemini sai do computador onde a aplicação corre, com a chave do `.env` desse computador. A chave nunca passa pelo túnel nem chega ao telemóvel.
- O `.env` tem de ter `LLM_BACKEND=gemini`; depois de mudar o `.env`, reiniciar a aplicação (o túnel pode continuar aberto).
- Quem entra pelo túnel usa a mesma chave e, por isso, **a mesma quota gratuita** (limites no [spike do LLM](05-spike-llm.md#1-limites-revistos-a-20102026)).
- **Termos do Gemini:** com o plano gratuito, a aplicação não pode ser disponibilizada a utilizadores no EEE nem a menores de 18 anos ([spike do LLM](05-spike-llm.md#3-privacidade-e-termos-de-utilização)). O túnel serve só para a equipa e para a demonstração, de acordo com a decisão de 20/10 (o OptaBem é um protótipo usado pela equipa). **Não partilhar o endereço fora da equipa.**

## 6. Problemas encontrados no teste de 22/10

| Sintoma | Causa | Solução |
|---|---|---|
| O endereço não abre no telemóvel, mas abre noutro computador | Endereço mal escrito, ou a rede do telemóvel ainda não conhece o endereço | Enviar o link por mensagem e tocar nele; mudar entre Wi-Fi e dados móveis |
| Não se consegue entrar com a conta que se tem no próprio computador | Cada computador tem a sua base de dados | Criar conta no site aberto pelo túnel |
| A conversa não respondeu e, um pouco depois, já respondeu | Limite de pedidos por minuto do plano gratuito (erro 429) ou Gemini sobrecarregado (erro 503) | Esperar um minuto; se repetir, ver o código do erro no terminal da aplicação |

## 7. Ver os dados

As contas e as conversas ficam em `instance/app.sqlite3`, no computador onde a aplicação corre. No VS Code, abrir esse ficheiro com a extensão **SQLite Viewer**. As palavras-passe aparecem cifradas (hash), como deve ser.
