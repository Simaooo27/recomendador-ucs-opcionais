# Guia do código

Para quem precisa de encontrar, verificar ou alterar alguma coisa no projeto sem conhecer o código todo. Todos os caminhos são relativos à pasta do projeto (no computador do Duarte: `C:\Users\duart\Desktop\222`).

**Atalhos úteis no VS Code:** `Ctrl+P` abre um ficheiro pelo nome (ex.: escrever `style.css`); `Ctrl+F` procura dentro do ficheiro aberto; `Ctrl+Shift+F` procura em todo o projeto (ex.: um texto que aparece no ecrã).

## Índice

1. [A pasta do projeto](#1-a-pasta-do-projeto)
2. [Mapa das pastas e ficheiros](#2-mapa-das-pastas-e-ficheiros)
3. [Onde mexer para…](#3-onde-mexer-para)
4. [O CSS (aspeto das páginas)](#4-o-css-aspeto-das-páginas)
5. [Como um pedido percorre o código](#5-como-um-pedido-percorre-o-código)
6. [Quem escreveu o quê e quando](#6-quem-escreveu-o-quê-e-quando)
7. [Como verificar que está tudo bem](#7-como-verificar-que-está-tudo-bem)

## 1. A pasta do projeto

A pasta do projeto (`222`) é o repositório Git: o que está nela é o que está no [GitHub](https://github.com/Simaooo27/recomendador-ucs-opcionais), mais algumas pastas que existem só em cada computador.

| Pasta | O que é | Vai para o GitHub? |
|---|---|---|
| **`app/`** | **Todo o código da aplicação.** É esta pasta que controla o que a aplicação faz e mostra. | Sim |
| `tests/` | Testes automáticos (verificam que o código faz o que os requisitos dizem). | Sim |
| `docs/` | Documentação: requisitos, use cases, BPMN, backlog, este guia. | Sim |
| `.github/` | Modelos de issue (user story) e de Pull Request. | Sim |
| `.venv/` | Python e bibliotecas instalados no teu computador. | Não (cada um cria o seu) |
| `.env` | Configuração e chave secreta (`SECRET_KEY`). | **Nunca** (o repositório é público) |
| `instance/` | Base de dados com as contas de teste. | Não (dados pessoais) |
| `ferramentas/` | Atalhos de Windows: `configurar.bat`, `arrancar.bat`, `admin.bat`. | Não |
| `.git/` | Histórico do Git. | — |

## 2. Mapa das pastas e ficheiros

```
app/                                  TODO O CÓDIGO DA APLICAÇÃO
├── __init__.py                       arranque: junta configuração, base de dados, segurança e páginas
├── config.py                         configuração (lida do .env): domínios de email, endereço da gestão…
├── texts.py                          TODOS os textos que aparecem no ecrã e nos emails
├── schema.sql                        tabelas da base de dados (users, admins)
├── db.py                             ligação à base de dados SQLite
├── security.py                       proteção CSRF dos formulários e cabeçalhos de segurança
├── mailer.py                         envio de email (no terminal em desenvolvimento, ou SMTP)
├── main.py                           página inicial do aluno (/inicio) e política de privacidade
│
├── auth/                             CONTAS DOS ALUNOS (US01 registo, US02 sessão)
│   ├── routes.py                     páginas /auth/registo, /auth/entrar, /auth/sair, /auth/confirmar
│   ├── services.py                   regras: registar, confirmar o email, autenticar
│   ├── validators.py                 validação do email e da palavra-passe
│   ├── repository.py                 consultas SQL à tabela users
│   ├── sessions.py                   quem tem sessão iniciada; protege as páginas privadas
│   └── tokens.py                     ligações de confirmação assinadas (24 horas)
│
├── gestao/                           ÁREA DE GESTÃO / ADMINISTRADORES (US03)
│   ├── routes.py                     páginas /gestao/entrar, /gestao/, /gestao/administradores
│   ├── services.py                   regras: criar, autenticar e remover administradores
│   ├── repository.py                 consultas SQL à tabela admins
│   ├── sessions.py                   sessão de administrador; protege as páginas da gestão
│   └── cli.py                        comandos de terminal: create-admin, list-admins
│
├── templates/                        AS PÁGINAS (HTML)
│   ├── base.html                     moldura comum: barra do topo, menu, painel central
│   ├── home.html                     página inicial do aluno
│   ├── privacy.html                  política de privacidade
│   ├── error.html                    páginas de erro (404, pedido inválido)
│   ├── macros/password.html          o ícone de olho dos campos de palavra-passe
│   ├── auth/                         registo, «confirme o seu email», confirmação, início de sessão
│   └── gestao/                       início de sessão da gestão, painel, lista de administradores
│
└── static/                           FICHEIROS ENVIADOS TAL COMO ESTÃO PARA O NAVEGADOR
    ├── style.css                     O ASPETO DE TODAS AS PÁGINAS (secção 4 deste guia)
    └── password-toggle.js            o clique no ícone de olho (mostrar/esconder a palavra-passe)

tests/                                um ficheiro por área: test_registration, test_confirmation,
                                      test_validators, test_login, test_gestao, test_texts…
docs/
├── geral/                            requisitos, regras de código, este guia, backlog (Excel), registo de IA
└── US01/, US02/, US03/               uma pasta por story: requisitos, use case, BPMN, prompt, diagramas
```

**Regra de organização** (definida em `docs/geral/02-regras-de-geracao-de-codigo.md`): as `routes` só recebem o pedido e devolvem a página; as regras estão nos `services`; o SQL está só nos `repository`; os textos estão só em `texts.py`; o aspeto está só em `style.css`.

## 3. Onde mexer para…

| Quero mudar… | Ficheiro | Como |
|---|---|---|
| Um texto do ecrã (título, botão, mensagem, email) | `app/texts.py` | Procurar o texto com Ctrl+F e mudar só o que está entre aspas |
| O nome da aplicação | `app/texts.py` | `APP_NAME` |
| Uma cor | `app/static/style.css`, secção 1 | Mudar o código `#rrggbb` da cor (modo escuro: secção 9) |
| Largura do painel, tamanho da letra, espaços | `app/static/style.css`, secções 2 a 5 | Ver os exemplos na secção 4 deste guia |
| O que aparece numa página (ordem dos campos, um parágrafo novo) | `app/templates/…` | O ficheiro com o nome da página; o texto vai para `texts.py` |
| O endereço da área de gestão | `.env` | `ADMIN_URL_PREFIX=outro-nome` (por omissão `gestao`) |
| Exigir outra vez o email institucional | `.env` | `ALLOWED_EMAIL_DOMAINS=iscap.ipp.pt` |
| Regras da palavra-passe, prazo da ligação | `app/config.py` | Falar primeiro com quem desenvolve (os testes dependem disto) |

Depois de mudar um texto ou o CSS: guardar, recarregar a página no navegador com **Ctrl+F5** e correr os testes (secção 7).

## 4. O CSS (aspeto das páginas)

**Ficheiro:** `app/static/style.css` — é o único ficheiro de estilos e todas as páginas o usam (está ligado em `app/templates/base.html`). Começa com um índice; cada secção tem um título numerado, por isso basta `Ctrl+F` e escrever, por exemplo, `4. Texto`.

| Secção | Linha (aprox.) | O que controla |
|---|---|---|
| 1. Cores | 26 | Todas as cores (texto, fundo, barra do topo, botões, erros, sucesso) e o tipo de letra |
| 2. Página e painel | 51 | Fundo da página, largura do painel central (alunos e gestão), cantos e margens |
| 3. Barra do topo | 81 | Barra azul, menu, etiqueta do perfil, botão «Terminar sessão», versão telemóvel |
| 4. Texto | 123 | Títulos, parágrafos, ligações, listas, contorno do teclado |
| 5. Formulários | 144 | Campos, etiquetas, ajudas, erros a vermelho, caixa da política, ícone de olho |
| 6. Botões | 201 | Botão principal e botão pequeno «Remover» |
| 7. Caixas de mensagem | 223 | Caixas de erro, de sucesso e a caixa amarela de desenvolvimento |
| 8. Tabelas | 239 | Lista de administradores na gestão |
| 9. Modo escuro | 250 | Cores quando o computador está em modo escuro (fica sempre no fim) |

**Exemplos de alterações comuns:**

| Para… | Na secção | Mudar |
|---|---|---|
| Barra do topo e botões de outra cor | 1 | `--accent: #1f3864;` para outra cor; `--accent-hover` é a cor ao passar o rato |
| Fundo da página branco | 1 | `--page: #f3f5f8;` para `#ffffff` |
| Painel dos alunos mais largo | 2 | `main { max-width: 32rem; }` para, por exemplo, `40rem` |
| Letra maior em todas as páginas | 2 | `body { font-size: 1rem; }` para `1.1rem` |
| Cantos menos arredondados | 2 | `.panel { border-radius: 0.5rem; }` para `0.2rem` |
| Títulos maiores | 4 | `h1 { font-size: 1.5rem; }` |
| Outro tipo de letra | 1 | `font-family: …` (ex.: `Georgia, serif`) |

**Cuidados:**
- `rem` é uma medida relativa ao tamanho da letra (1rem ≈ 16 píxeis); prefira-a a píxeis para a página continuar a funcionar no telemóvel.
- Se mudar cores na secção 1, veja também a secção 9 (modo escuro), que tem as suas próprias cores.
- Não mude a ordem das secções: o modo escuro tem de ficar no fim para se sobrepor ao resto.
- Não escreva estilos dentro dos ficheiros HTML (`style="…"`): a política de segurança da aplicação (CSP, em `app/security.py`) bloqueia-os. Tudo vai para `style.css`.

## 5. Como um pedido percorre o código

Exemplo: o aluno carrega em «Criar conta».

1. O navegador envia o formulário para `/auth/registo`.
2. `app/security.py` confirma o token CSRF (proteção contra formulários falsos).
3. `app/auth/routes.py` (`register_submit`) lê o pedido e chama o serviço.
4. `app/auth/services.py` (`register_student`) aplica as regras: valida com `validators.py`, guarda com `repository.py` (SQL em `schema.sql`).
5. A rota envia o email (`app/mailer.py`) e mostra a página `templates/auth/pending.html`.
6. A página usa `templates/base.html` (moldura), os textos de `app/texts.py` e o aspeto de `app/static/style.css`.

Os outros fluxos seguem o mesmo caminho: início de sessão em `auth/routes.py` → `auth/services.py` → `auth/sessions.py`; gestão em `gestao/routes.py` → `gestao/services.py` → `gestao/sessions.py`.

## 6. Quem escreveu o quê e quando

Todo o código foi gerado com apoio de IA (Claude) a partir dos requisitos e segundo as regras de `docs/geral/02-regras-de-geracao-de-codigo.md`; cada alteração entrou por Pull Request revisto e aceite pela equipa. O detalhe de cada utilização de IA está em [registo-de-uso-de-ia.md](registo-de-uso-de-ia.md) e o pedido feito para cada story em `docs/USNN/prompt.md`.

| Quando | O quê | Onde ficou | Como ver |
|---|---|---|---|
| 01–05/10 | US01 inicial (registo e confirmação), requisitos, regras de código, use case e BPMN da US01 | `app/` (exceto `gestao/`), `tests/`, `docs/` | Commits iniciais do Simão |
| 07/10 · PR #1 | Documentação organizada por story | `docs/geral/`, `docs/US01/`, `.github/` | PR #1 |
| 07/10 · PR #2 | Textos num só ficheiro; CSS comentado; README | `app/texts.py`, `app/templates/`, `app/static/style.css` | PR #2 |
| 07/10 · PR #3 | Registo com email pessoal | `app/auth/validators.py`, `app/config.py`, `app/texts.py` | PR #3 |
| 07/10 · PR #4 | US02: iniciar e terminar sessão; ligação de confirmação na página em desenvolvimento | `app/auth/sessions.py`, `app/auth/routes.py`, `app/templates/auth/login.html`, `home.html`, `docs/US02/` | PR #4 |
| 07/10 · PR #5 | Ícone para mostrar a palavra-passe | `app/templates/macros/password.html`, `app/static/password-toggle.js` | PR #5 |
| 07/10 · PR #6 | Replaneamento do Sprint 1 e Product Backlog | `docs/geral/product-backlog.xlsx`, README | PR #6 |
| 07/10 · PR #7 | US03: administradores e área de gestão | `app/gestao/`, `app/templates/gestao/`, `app/schema.sql`, `docs/US03/` | PR #7 |
| 08/10 · PR #8 | Sprint 1 concluído | README, `docs/US02/`, `docs/US03/`, Excel | PR #8 |
| 08/10 | CSS organizado em secções; este guia | `app/static/style.css`, `docs/geral/03-guia-do-codigo.md` | PR deste guia |

**Para ver exatamente o que mudou numa alteração:** no GitHub, abra **Pull requests → Closed**, escolha o PR e veja o separador **Files changed** (verde = acrescentado, vermelho = retirado). Para o histórico de um ficheiro: abra o ficheiro no GitHub e carregue em **History**.

## 7. Como verificar que está tudo bem

1. **Testes automáticos** (no terminal do VS Code, na pasta do projeto):
   ```
   .venv\Scripts\python.exe -m unittest discover -s tests -t .
   ```
   No fim tem de aparecer `OK`. Se aparecer `FAILED`, o nome do teste diz o que deixou de funcionar.
2. **A aplicação:** `.\ferramentas\arrancar.bat` e abrir http://127.0.0.1:5000 (alunos) e http://127.0.0.1:5000/gestao/entrar (gestão).
3. **Os documentos:** os requisitos de cada story têm, na secção 5, a tabela critério de aceitação → teste que o verifica.
