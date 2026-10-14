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
├── main.py                           apresentação (/), página inicial do aluno (/inicio), privacidade
├── percurso.py                       em que passo do percurso está cada aluno (padrão State)
├── manuscrito.py                     converte palavras em traços «escritos à mão» (fontTools)
├── recursos/                         tipo de letra manuscrito Caveat, usado pelo servidor (licença OFL)
│
├── auth/                             CONTAS E INÍCIO DE SESSÃO (US01 registo, US02 sessão, US03 perfis)
│   ├── routes.py                     páginas /auth/registo, /auth/entrar, /auth/sair, /auth/confirmar
│   ├── perfis.py                     um só início de sessão: aluno ou administrador (padrões Strategy,
│   │                                 Chain of Responsibility e Factory — ver 03-arquitetura-e-padroes.md)
│   ├── services.py                   regras: registar, confirmar o email, autenticar
│   ├── validators.py                 validação do email e da palavra-passe
│   ├── repository.py                 consultas SQL à tabela users
│   ├── sessions.py                   quem tem sessão iniciada; protege as páginas privadas
│   └── tokens.py                     ligações de confirmação assinadas (24 horas)
│
├── catalogo/                         CATÁLOGO DE CURSOS (base da US04 e da US05)
│   ├── repository.py                 lê os cursos de dados/catalogo-cursos-mvp.csv (a US04 troca por SQL)
│   ├── services.py                   pesquisa sem acentos, amostra e totais
│   └── routes.py                     /cursos/pesquisa (resultados em JSON para a pesquisa ao vivo)
│
├── gestao/                           ÁREA DE GESTÃO / ADMINISTRADORES (US03)
│   ├── routes.py                     páginas /gestao/ e /gestao/administradores (/gestao/entrar leva a /auth/entrar)
│   ├── services.py                   regras: criar, autenticar e remover administradores
│   ├── repository.py                 consultas SQL à tabela admins
│   ├── sessions.py                   sessão de administrador; protege as páginas da gestão
│   └── cli.py                        comandos de terminal: create-admin, list-admins
│
├── templates/                        AS PÁGINAS (HTML)
│   ├── base.html                     moldura comum: painel do percurso (páginas de entrada) ou barra do topo
│   ├── landing.html                  apresentação pública (/): pesquisa de cursos, como funciona, para quem
│   ├── home.html                     página inicial do aluno, com «O seu percurso»
│   ├── privacy.html                  política de privacidade
│   ├── error.html                    páginas de erro (404, pedido inválido)
│   ├── macros/password.html          o ícone de olho dos campos de palavra-passe
│   ├── macros/marca.html             símbolo, ilustração do percurso, ficha de curso, escrita à mão, botão «flow»
│   ├── auth/                         registo, «confirme o seu email», confirmação, início de sessão
│   └── gestao/                       painel e lista de administradores
│
└── static/                           FICHEIROS ENVIADOS TAL COMO ESTÃO PARA O NAVEGADOR
    ├── style.css                     O ASPETO DE TODAS AS PÁGINAS (secção 4 deste guia)
    ├── fonts/                        tipos de letra (Bricolage Grotesque e Atkinson Hyperlegible Next, licença OFL)
    ├── favicon.svg                   ícone no separador do navegador
    ├── app.js                        interações: pesquisa ao vivo, escrita à mão, linha dos passos, regras da palavra-passe, números
    └── password-toggle.js            o clique no ícone de olho (mostrar/esconder a palavra-passe)

tests/                                um ficheiro por área: test_registration, test_confirmation,
                                      test_validators, test_login, test_gestao, test_perfis, test_apresentacao, test_texts…
docs/
├── geral/                            requisitos, regras de código, este guia, backlog (Excel), registo de IA
└── US01/, US02/, US03/               uma pasta por story: requisitos, use case, BPMN, prompt, diagramas
```

**Regra de organização** (definida em `docs/geral/02-regras-de-geracao-de-codigo.md`): as `routes` só recebem o pedido e devolvem a página; as regras estão nos `services`; o SQL está só nos `repository`; os textos estão só em `texts.py`; o aspeto está só em `style.css`.

## 3. Onde mexer para…

| Quero mudar… | Ficheiro | Como |
|---|---|---|
| Um texto do ecrã (título, botão, mensagem, email) | `app/texts.py` | Procurar o texto com Ctrl+F e mudar só o que está entre aspas |
| O nome na barra do topo e no painel verde | `app/texts.py` | `BRAND_NAME` (hoje «OptaBem») |
| O nome no separador do navegador | `app/texts.py` | `APP_NAME` |
| A frase grande do painel verde | `app/texts.py` | `BRAND_TAGLINE` e `BRAND_SUPPORT` |
| Os textos da pesquisa, os passos e «Para quem é» | `app/texts.py` | `LANDING_SEARCH_*`, `LANDING_RESULTS_*`, `LANDING_STEPS`, `LANDING_FOR` |
| Os cursos que aparecem na pesquisa | `dados/catalogo-cursos-mvp.csv` | Acrescentar ou corrigir linhas; a página lê o ficheiro de novo quando ele muda |
| Os passos de «O seu percurso» | `app/texts.py` | `HOME_PATH_STEPS` |
| Uma cor | `app/static/style.css`, secção 1 | Mudar o código `#rrggbb` da cor (modo escuro: secção 12) |
| Largura, tamanho da letra, espaços | `app/static/style.css`, secções 3 a 8 | Ver os exemplos na secção 4 deste guia |
| O que aparece numa página (ordem dos campos, um parágrafo novo) | `app/templates/…` | O ficheiro com o nome da página; o texto vai para `texts.py` |
| O endereço da área de gestão | `.env` | `ADMIN_URL_PREFIX=outro-nome` (por omissão `gestao`) |
| Exigir outra vez o email institucional | `.env` | `ALLOWED_EMAIL_DOMAINS=iscap.ipp.pt` |
| Regras da palavra-passe, prazo da ligação | `app/config.py` | Falar primeiro com quem desenvolve (os testes dependem disto) |

Depois de mudar um texto ou o CSS: guardar, recarregar a página no navegador com **Ctrl+F5** e correr os testes (secção 7).

## 4. O CSS (aspeto das páginas)

**Ficheiro:** `app/static/style.css` — é o único ficheiro de estilos e todas as páginas o usam (está ligado em `app/templates/base.html`). Começa com um índice; cada secção tem um título numerado, por isso basta `Ctrl+F` e escrever, por exemplo, `4. Texto`.

| Secção | Linha (aprox.) | O que controla |
|---|---|---|
| 1. Cores | 32 | Todas as cores: texto, fundos, verde dos botões, verde-escuro do painel, amarelo do caminho escolhido, erros, sucesso |
| 2. Tipos de letra | 59 | Letra dos títulos (Bricolage Grotesque) e do texto (Atkinson Hyperlegible Next), em `app/static/fonts/` |
| 3. Página e colunas | 93 | Fundo da página, tamanho base da letra, largura da coluna (alunos e gestão) |
| 4. Barra do topo | 119 | Marca «OptaBem», «Gestão», menu, nome do administrador, «Terminar sessão», versão telemóvel |
| 5. Páginas de entrada | 195 | Painel verde com o percurso (criar conta, iniciar sessão, confirmar email) e a coluna do formulário |
| 6. Texto | 268 | Títulos, parágrafos, ligações, listas, contorno do teclado |
| 7. Formulários | 297 | Campos, etiquetas, ajudas, erros a vermelho, caixa da política, ícone de olho |
| 8. Botões | 368 | Botão principal, «Terminar sessão» e «Remover» |
| 9. Caixas de mensagem | 420 | Caixas de erro, de sucesso e a caixa amarela de desenvolvimento |
| 10. Tabelas | 436 | Lista de administradores na gestão |
| 11. Página de apresentação | 447 | A página inicial pública: caixa de pesquisa, nota escrita à mão, fichas dos cursos, botão «flow» (círculo e setas), «Como funciona», «Para quem é» |
| 12. O meu percurso | 747 | A linha do tempo da página inicial do aluno |
| 13. Gestão, erros e detalhes | 793 | Números do painel, página não encontrada, regras da palavra-passe, botão «a enviar» |
| 14. Movimento | 873 | Todas as animações (e o que acontece a quem pede menos movimento) |
| 15. Modo escuro | 914 | Cores quando o computador está em modo escuro (fica sempre no fim) |

**Exemplos de alterações comuns:**

| Para… | Na secção | Mudar |
|---|---|---|
| Botões e ligações de outra cor | 1 | `--accent: #0e6b57;`; `--accent-hover` é a cor ao passar o rato |
| Painel das páginas de entrada de outra cor | 1 | `--forest: #0f2e27;` |
| Cor do caminho escolhido na ilustração | 1 | `--marigold: #f2b33d;` |
| Fundo da página branco | 1 | `--page: #eef3f0;` para `#ffffff` |
| Cantos menos arredondados | 1 | `--radius: 10px;` para, por exemplo, `4px` |
| Coluna dos alunos mais larga | 3 | `.conteudo { max-width: 40rem; }` |
| Letra maior em todas as páginas | 3 | `body { font-size: 1.0625rem; }` para `1.15rem` |
| Títulos maiores | 6 | `h1 { font-size: clamp(…); }` |
| Outro tipo de letra | 2 | `--font-display` (títulos) e `--font-text` (texto) |
| Desligar as animações | 14 | Apagar os blocos `@media (prefers-reduced-motion: no-preference) { … }` |
| Cor da nota escrita à mão | 11 | `.procura-nota { color: … }` |
| Cor do círculo do botão «flow» | 11 | `--flow-cor` em `.flow-button` (e em `.flow-button-claro`) |

**Cuidados:**
- `rem` é uma medida relativa ao tamanho da letra (1rem ≈ 16 píxeis); prefira-a a píxeis para a página continuar a funcionar no telemóvel.
- Se mudar cores na secção 1, veja também a secção 15 (modo escuro), que tem as suas próprias cores.
- Os tipos de letra estão na própria aplicação (`app/static/fonts/`), porque a política de segurança não deixa carregar letras de outros sites.
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

Os outros fluxos seguem o mesmo caminho: início de sessão em `auth/routes.py` → `auth/perfis.py` (escolhe aluno ou administrador) → `auth/services.py` ou `gestao/services.py` → `auth/sessions.py` ou `gestao/sessions.py`; gestão em `gestao/routes.py` → `gestao/services.py` → `gestao/sessions.py`.

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
| 08/10 · PR #9 | CSS organizado em secções; este guia | `app/static/style.css`, `docs/geral/04-guia-do-codigo.md` | PR #9 |
| 13/10 · PR #10 | Nova visão do produto, padrões de desenho previstos, catálogo de cursos | `docs/geral/00-…`, `docs/geral/03-…`, `dados/` | PR #10 |
| 14/10 | Um só início de sessão (Strategy, Chain of Responsibility, Factory); novo aspeto visual | `app/auth/perfis.py`, `app/templates/`, `app/static/` | PR do início de sessão único |

**Para ver exatamente o que mudou numa alteração:** no GitHub, abra **Pull requests → Closed**, escolha o PR e veja o separador **Files changed** (verde = acrescentado, vermelho = retirado). Para o histórico de um ficheiro: abra o ficheiro no GitHub e carregue em **History**.

## 7. Como verificar que está tudo bem

1. **Testes automáticos** (no terminal do VS Code, na pasta do projeto):
   ```
   .venv\Scripts\python.exe -m unittest discover -s tests -t .
   ```
   No fim tem de aparecer `OK`. Se aparecer `FAILED`, o nome do teste diz o que deixou de funcionar.
2. **A aplicação:** `.\ferramentas\arrancar.bat` e abrir http://127.0.0.1:5000. Alunos e administradores entram na mesma página: com o email (aluno) ou com o nome de utilizador (administrador).
3. **Os documentos:** os requisitos de cada story têm, na secção 5, a tabela critério de aceitação → teste que o verifica.
