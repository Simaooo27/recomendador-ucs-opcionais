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
| `ferramentas/` | Atalhos de Windows: `configurar.bat`, `arrancar.bat`, `admin.bat` (e, se criado, `arrancar-tunel.ps1`: ver [abrir noutro dispositivo](06-aceder-noutro-dispositivo.md)). | Não |
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
├── percurso/                         O PERCURSO DO ALUNO (US31)
│   ├── __init__.py                   em que passo do percurso está cada aluno (padrão State)
│   ├── routes.py                     /percurso/ (linha do tempo) e /percurso/escolher/<curso> (confirmar a escolha)
│   ├── services.py                   regras: escolher curso, mudar de curso, curso atual, apagar a conversa
│   └── repository.py                 consultas SQL à tabela decisoes
├── candidatura/                      PLANO DE CANDIDATURA (protótipo de 23/10; US33 a US36)
│   ├── calculos.py                   as contas: nota de candidatura, provas em falta, mínimos, «quanto preciso», exames que abrem portas e plano B (funções puras)
│   ├── services.py                   regras do plano: notas, até 6 opções, subir/descer, avisos, sugestões
│   ├── routes.py                     /candidatura/ (o plano), /candidatura/notas, os botões e a partilha (/candidatura/p/<código>)
│   └── repository.py                 consultas SQL à tabela planos_candidatura
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
│   ├── services.py                   pesquisa sem acentos, amostra e totais; filtros, ficha e comparação (US05)
│   └── routes.py                     /cursos/ (filtros), /cursos/<curso> (ficha), /cursos/comparar e /cursos/pesquisa (JSON)
│
├── llm/                              LIGAÇÃO AO LLM (spike de 14/10; ver 05-spike-llm.md)
│   ├── cliente.py                    a interface que o resto do código usa (ClienteLLM, Mensagem, erros)
│   ├── adaptadores.py                Gemini, Groq e o LLM falso dos testes — o ÚNICO ficheiro que fala com fornecedores
│   ├── decoradores.py                apaga emails e números do que o utilizador escreve, antes de enviar (RNF12)
│   └── fabrica.py                    escolhe o fornecedor pela variável LLM_BACKEND do .env
│
├── orientacao/                       CONVERSA DE ORIENTAÇÃO (US29, US30)
│   ├── routes.py                     página /orientacao/ e os botões Começar, Enviar, Tentar de novo, Recomeçar
│   ├── services.py                   regras da conversa: começar, responder, tentar de novo, recomeçar
│   ├── repository.py                 consultas SQL às tabelas conversas_orientacao e pedidos_llm
│   ├── limite.py                     limite de pedidos ao LLM por aluno e por dia (Decorator à volta do ClienteLLM)
│   ├── instrucoes.md                 o que se diz ao LLM: como conduzir a conversa, regras, formato, catálogo
│   ├── conversa.py                   próximo passo (pergunta ou sugestão) e validação contra o catálogo (RN09)
│   └── cli.py                        comando flask llm-teste (experimentar com a chave real)
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
│   ├── home.html                     página inicial do aluno: «O seu percurso» e atalhos
│   ├── privacy.html                  política de privacidade
│   ├── error.html                    páginas de erro (404, pedido inválido)
│   ├── macros/password.html          o ícone de olho dos campos de palavra-passe
│   ├── macros/marca.html             símbolo, ficha de curso, botão «flow» (uma ligação simples), lupa e conta da barra do topo
│   ├── auth/                         registo, «confirme o seu email», confirmação, início de sessão,
│   │                                 «A minha conta» (conta.html) e apagar a conta (US17)
│   ├── orientacao/conversa.html      a conversa com o assistente (US29) e os cursos sugeridos (US30)
│   ├── percurso/                     confirmar a escolha do curso e a linha do tempo das decisões (US31)
│   ├── catalogo/lista.html           página /cursos/: pesquisa e filtros por área, instituição e localidade (US05)
│   ├── catalogo/ficha.html           ficha completa de um curso, /cursos/<curso> (US05)
│   ├── catalogo/comparar.html        comparação de 2 ou 3 cursos lado a lado, /cursos/comparar (US05)
│   └── gestao/                       painel e lista de administradores
│
└── static/                           FICHEIROS ENVIADOS TAL COMO ESTÃO PARA O NAVEGADOR
    ├── style.css                     O ASPETO DE TODAS AS PÁGINAS (secção 4 deste guia)
    ├── favicon.svg                   ícone no separador do navegador
    ├── app.js                        interações: pesquisa ao vivo, comparação, regras da palavra-passe, botões «a enviar», painéis da barra do topo
    └── password-toggle.js            o clique no ícone de olho (mostrar/esconder a palavra-passe)

tests/                                um ficheiro por área: test_registration, test_confirmation,
                                      test_validators, test_login, test_gestao, test_perfis, test_apresentacao, test_texts,
                                      test_llm, test_orientacao…
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
| Os textos da escolha de curso e da linha do tempo | `app/texts.py` | `CURSO_ESCOLHER` e os que começam por `PERCURSO_` |
| Uma cor | `app/static/style.css`, secção 1 | Mudar o código `#rrggbb` da cor (modo escuro: secção 12) |
| Largura, tamanho da letra, espaços | `app/static/style.css`, secções 3 a 8 | Ver os exemplos na secção 4 deste guia |
| O que aparece numa página (ordem dos campos, um parágrafo novo) | `app/templates/…` | O ficheiro com o nome da página; o texto vai para `texts.py` |
| O endereço da área de gestão | `.env` | `ADMIN_URL_PREFIX=outro-nome` (por omissão `gestao`) |
| Exigir outra vez o email institucional | `.env` | `ALLOWED_EMAIL_DOMAINS=iscap.ipp.pt` |
| Regras da palavra-passe, prazo da ligação | `app/config.py` | Falar primeiro com quem desenvolve (os testes dependem disto) |
| Como o LLM conduz a conversa (tom, perguntas, regras) | `app/orientacao/instrucoes.md` | Texto normal; não apagar `$catalogo` nem `$max_perguntas`. Correr os testes e `flask --app app llm-teste --backend gemini` |
| O fornecedor ou o modelo do LLM | `.env` | `LLM_BACKEND=gemini` (ou `groq`, ou `falso`) e, se preciso, `LLM_MODELO=…` |
| O número máximo de perguntas do LLM | `app/orientacao/conversa.py` | `LIMITE_PERGUNTAS` (hoje 6) |
| Quantos pedidos ao LLM cada aluno pode fazer por dia | `.env` | `ORIENTACAO_MAX_PEDIDOS_DIA=40` (`0` = sem limite) |
| As páginas do menu dos alunos | `app/templates/base.html` e `app/texts.py` | `NAV_INICIO`, `NAV_CONVERSA`, `NAV_CATALOGO`, `NAV_DECISOES` |

Depois de mudar um texto ou o CSS: guardar, recarregar a página no navegador com **Ctrl+F5** e correr os testes (secção 7).

## 4. O CSS (aspeto das páginas)

**Ficheiro:** `app/static/style.css` — é o único ficheiro de estilos e todas as páginas o usam (está ligado em `app/templates/base.html`). Começa com um índice; cada secção tem um título numerado, por isso basta `Ctrl+F` e escrever, por exemplo, `4. Texto`.

| Secção | Linha (aprox.) | O que controla |
|---|---|---|
| 1. Cores | 32 | Todas as cores: texto, fundos, faixa cinzenta, botões e ligações (preto), erros, sucesso, avisos; cantos e sombras das caixas |
| 2. Tipos de letra | 66 | A letra do sistema (a do Windows, do Mac ou do telemóvel): não há nada a descarregar |
| 3. Página e colunas | 77 | Fundo da página, tamanho base da letra, margens (`--margem`) e larguras (alunos, início, gestão e apresentação) |
| 4. Barra do topo | 117 | Marca «OptaBem», «Gestão», menu, lupa e ícone de conta (com os painéis), nome do administrador, versão telemóvel |
| 5. Páginas de entrada | 270 | A marca em cima e o formulário numa coluna centrada (criar conta, iniciar sessão, confirmar email, recuperar a palavra-passe) |
| 6. Texto | 284 | Títulos, parágrafos, ligações, listas, contorno do teclado |
| 7. Formulários | 312 | Campos, etiquetas, ajudas, erros a vermelho, caixa da política, ícone de olho |
| 8. Botões | 403 | Botão principal (em forma de pílula), «Terminar sessão» e «Remover» |
| 9. Caixas de mensagem | 455 | Caixas de erro, de sucesso e a caixa amarela de desenvolvimento |
| 10. Tabelas | 471 | Lista de administradores na gestão |
| 11. Página de apresentação | 489 | A página inicial pública: frase e pesquisa ao centro, faixa cinzenta com as fichas dos cursos, «Como funciona», «Para quem» |
| 12. O meu percurso | 695 | O início do aluno (o próximo passo em destaque, a linha do tempo e os atalhos), as secções que abrem e fecham (`.dobra`) e a conversa de orientação |
| 13. Gestão, erros e detalhes | 1009 | Números do painel, página não encontrada, regras da palavra-passe, botão «a enviar» |
| 14. Movimento | 1089 | As poucas animações que ficam (e o que acontece a quem pede menos movimento) |
| 15. Modo escuro | 1212 | Cores quando o computador está em modo escuro (fica sempre no fim) |

**Exemplos de alterações comuns:**

| Para… | Na secção | Mudar |
|---|---|---|
| Botões e ligações de outra cor | 1 | `--accent: #171717;` e `--link`; `--accent-hover` é a cor ao passar o rato |
| Cor da faixa cinzenta | 1 | `--band: #efefef;` |
| Fundo da página branco | 1 | `--page: #f9f9f9;` para `#ffffff` |
| Cantos menos arredondados | 1 | `--radius: 12px;` e `--radius-cartao: 16px;` para, por exemplo, `4px` |
| Coluna dos alunos mais larga | 3 | `.conteudo { max-width: 40rem; }` |
| Letra maior em todas as páginas | 3 | `body { font-size: 1.0625rem; }` para `1.15rem` |
| Títulos maiores | 6 | `h1 { font-size: clamp(…); }` |
| Outro tipo de letra | 2 | `--font-display` (títulos) e `--font-text` (texto); um tipo de letra que não seja do sistema tem de ficar em `app/static/` (ver os cuidados) |
| Desligar as animações | 14 | Apagar os blocos `@media (prefers-reduced-motion: no-preference) { … }` |

**Cuidados:**
- `rem` é uma medida relativa ao tamanho da letra (1rem ≈ 16 píxeis); prefira-a a píxeis para a página continuar a funcionar no telemóvel.
- Se mudar cores na secção 1, veja também a secção 15 (modo escuro), que tem as suas próprias cores.
- Desde 29/10 a aplicação usa a letra do sistema. Para voltar a ter um tipo de letra próprio, os ficheiros têm de ficar em `app/static/`, porque a política de segurança não deixa carregar letras de outros sites.
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
| 14/10 | Spike do LLM: Gemini e Groq atrás de `ClienteLLM` (Adapter, Factory, Decorator), conversa de orientação sem páginas, comando `llm-teste` | `app/llm/`, `app/orientacao/`, `docs/geral/05-spike-llm.md` | PR #17 |
| 14/10 | US29: página da conversa de orientação com o LLM | `app/orientacao/`, `app/templates/orientacao/`, `docs/US29/` | PR #19 |
| 20/10 | US30: cursos sugeridos no fim da conversa, «Ver sugestões já», página `/cursos/` | `app/orientacao/`, `app/catalogo/`, `docs/US30/` | PR #22 |
| 20/10 | Revisão: correções ao spike e aos requisitos; US29 garante o limite de 6 perguntas | `docs/geral/`, `app/orientacao/conversa.py`, `app/llm/adaptadores.py` | PR #23 e #24 |
| 20/10 | Servidor Ollama da faculdade: ligado, testado e retirado (fica o Gemini) | `docs/geral/05-spike-llm.md`, secção 7 | PR #25 e #26 |
| 20/10 | Sprint Planning do Sprint 2: US31 antecipada; ponto 14 decidido | Excel, `PROJETO.md`, requisitos | PR #28 |
| 20/10 | US31: escolher curso e linha do tempo das decisões; `app/percurso.py` passou a pacote | `app/percurso/`, `app/templates/percurso/`, `app/schema.sql`, `docs/US31/` | PR da US31 |
| 22/10 | Abrir o OptaBem no telemóvel ou noutro computador (túnel do Cloudflare, sem modo debug) | `docs/geral/06-aceder-noutro-dispositivo.md` | PR #30 |
| 22/10 | Sprint Review do Sprint 2: US29, US30 e US31 aceites; até 05/11 os cursos são o centro e as opcionais passam para segundo plano | `PROJETO.md`, `docs/geral/product-backlog.xlsx`, `docs/US29/` a `docs/US31/` | PR do fecho do Sprint 2 |
| 22/10 | As opcionais saem do site (decisão dos PO): textos, linha do tempo com 3 passos, política de privacidade provisória | `app/texts.py`, `app/percurso/__init__.py`, `tests/test_apresentacao.py` | PR #32 e #33 |
| 22/10 | Sprint Planning do Sprint 3: US05 e US17; US06 e US07 para o backlog; sprints de uma semana até 05/11 | `docs/geral/product-backlog.xlsx`, `PROJETO.md` | PR do Sprint Planning do Sprint 3 |
| 22/10 | US05: filtros no catálogo, ficha completa de cada curso e comparação de até 3 cursos | `app/catalogo/`, `app/templates/catalogo/`, `docs/US05/` | PR da US05 |
| 22/10 | US17: apagar a minha conta e todos os dados (confirmação pela palavra-passe); guia do túnel sem comentários no `.env` | `app/auth/`, `app/templates/auth/apagar.html`, `home.html`, `docs/US17/`, `06-aceder-noutro-dispositivo.md` | PR da US17 |
| 22/10 | Barra do topo presa ao topo em todas as páginas; na apresentação, secções (Cursos, Como funciona, Para quem) e um só «Entrar» e «Criar conta» | `app/templates/base.html`, `landing.html`, `app/static/style.css` (secções 4 e 11) | PR do menu fixo |
| 23/10 | Sprint Review do Sprint 3: US05 e US17 aceites; teste da US17 deixa de depender da data | `PROJETO.md`, `docs/geral/product-backlog.xlsx`, `docs/US05/`, `docs/US17/`, `tests/test_apagar_conta.py` | PR do fecho do Sprint 3 |
| 23/10 | Nome no registo e tratamento pelo nome; terminar sessão volta à página inicial | `app/auth/`, `app/db.py` (migração), `app/templates/home.html`, `auth/conta.html`, `docs/US01/`, `docs/US02/` | PR #43 |
| 23/10 | Protótipo do plano de candidatura (substitui as opcionais): condições de acesso na ficha, notas, nota por curso, 6 opções; «As minhas decisões» sai do menu | `app/candidatura/`, `app/templates/candidatura/`, `macros/candidatura.html`, `catalogo/ficha.html`, `dados/recolher_dges.py`, `dados/provas-ingresso.csv` | PR #44 |
| 23/10 | Quanto preciso no exame, tendência do último colocado, procura do curso e partilhar o plano (US40 a US43); gestão ativa contas por confirmar | `app/candidatura/`, `app/catalogo/repository.py`, `catalogo/ficha.html`, `candidatura/partilhado.html`, `app/gestao/`, `dados/recolher_dges.py` | PR #43 e #44 |
| 23/10 | Que exames me abrem mais portas (US44) e plano B da 2.ª fase (US45) | `app/candidatura/calculos.py`, `services.py`, `templates/candidatura/plano.html`, `dados/recolher_dges.py` | PR #44 |
| 23/10 | Revisão estética (pedido do PO): barra do topo encostada às margens, com lupa e ícone de conta; pesquisa da apresentação numa só caixa; pesquisa pelo início das palavras e sem a escola; ilustração da entrada alinhada com o formulário; início com o percurso numa caixa e atalhos; página «A minha conta» com «Apagar a conta»; comparação de cursos com caixas, grupos de linhas e textos sem palavras partidas | `app/templates/` (`base.html`, `landing.html`, `home.html`, `auth/conta.html`, `macros/marca.html`), `app/static/style.css`, `app/static/app.js`, `app/catalogo/services.py`, `app/auth/routes.py`, `docs/US17/` | PR da revisão estética |
| 29/10 | Visual calmo (pedido do PO): menos texto à vista e uma ação principal por página; letra do sistema (saem os tipos de letra, a escrita à mão e o `fonttools`); no início, o próximo passo em destaque; no plano e na ficha, as secções secundárias abrem e fecham | `app/static/style.css`, `app/static/app.js`, `app/templates/` (`base.html`, `home.html`, `landing.html`, `macros/marca.html`, `candidatura/plano.html`, `catalogo/ficha.html`), `requirements.txt` | PR do visual calmo |

**Para ver exatamente o que mudou numa alteração:** no GitHub, abra **Pull requests → Closed**, escolha o PR e veja o separador **Files changed** (verde = acrescentado, vermelho = retirado). Para o histórico de um ficheiro: abra o ficheiro no GitHub e carregue em **History**.

## 7. Como verificar que está tudo bem

1. **Testes automáticos** (no terminal do VS Code, na pasta do projeto):
   ```
   .venv\Scripts\python.exe -m unittest discover -s tests -t .
   ```
   No fim tem de aparecer `OK`. Se aparecer `FAILED`, o nome do teste diz o que deixou de funcionar.
2. **A aplicação:** `flask --app app run --debug` (no Windows, também o atalho `.\ferramentas\arrancar.bat`, que só existe no computador de cada um) e abrir http://127.0.0.1:5000. Alunos e administradores entram na mesma página: com o email (aluno) ou com o nome de utilizador (administrador). Para a abrir no telemóvel ou noutro computador, ver [abrir noutro dispositivo](06-aceder-noutro-dispositivo.md) (nunca com o modo debug).
3. **Os documentos:** os requisitos de cada story têm, na secção 5, a tabela critério de aceitação → teste que o verifica.
