# Arquitetura e padrões de desenho

Projeto 1 · Metodologias Ágeis (Scrum) · OptaBem

**Versão 1.1 · 2026-10-14** (1.0 de 13/10: proposta inicial; 1.1: início de sessão único com Strategy, Chain of Responsibility e Factory). Complementa as regras de [02-regras-de-geracao-de-codigo.md](02-regras-de-geracao-de-codigo.md): aquele documento diz *como* se escreve código; este diz *como as peças se organizam e porquê*. A visão que motiva as partes novas está em [00-visao-do-produto.md](00-visao-do-produto.md).

## 1. Visão geral

```mermaid
flowchart LR
    B[Navegador] --> R[routes.py<br>HTTP]
    R --> S[services.py<br>casos de uso]
    S --> Rep[repository.py<br>SQL]
    Rep --> DB[(SQLite)]
    S --> Rec[recomendacao/<br>estratégias]
    S --> O[orientacao/<br>questionário e sugestões]
    O --> L[llm/<br>adaptadores]
    L -.-> API[(Fornecedor de LLM<br>ou modelo local)]
```

As caixas `recomendacao/`, `orientacao/` e `llm/` ainda não existem: entram com as stories indicadas na secção 4.

## 2. Tecnologias

| Tema | Escolha | Porquê |
|---|---|---|
| Linguagem | Python 3.10+ | Conhecida pelos dois elementos; boas bibliotecas de dados para o motor |
| Framework web | Flask 3.x | Pequeno e explícito: cada pedido é uma função visível, o que facilita rever código gerado com IA |
| Base de dados | SQLite (`sqlite3` da biblioteca padrão) | Um ficheiro, sem servidor para instalar; suficiente para o volume do projeto |
| Testes | `unittest` | Biblioteca padrão; corre com um único comando e sem rede |
| Motor de recomendação | `pandas` e `numpy` (a partir da US11) | Cálculos de médias e similaridades sobre matrizes |
| LLM | Atrás de uma interface própria (secção 4.2); fornecedor escolhido na US30 | Não ficar preso a um fornecedor; testes sem rede nem custos |
| Interface | HTML (Jinja), CSS e JavaScript próprios, sem React nem Tailwind | Componentes de bibliotecas React (ex.: FlowButton, HandwritingText) são **adaptados** a este formato em vez de mudar o projeto para React: a política de segurança (CSP) só aceita ficheiros do próprio site e o código fica legível para os dois elementos |
| Letras «escritas à mão» | `fontTools` no servidor (`app/manuscrito.py`) | Converte as letras em traços SVG sem carregar bibliotecas de outros sites; sem ele, a página mostra texto normal |

## 3. Padrões que o código já usa

Estes padrões existem desde o Sprint 1. Documentá-los ajuda a manter o código coerente quando a IA gera partes novas.

| Padrão | Onde | O que resolve |
|---|---|---|
| **Arquitetura em camadas** | `routes.py` → `services.py` → `repository.py` em cada pacote (`auth/`, `gestao/`) | Cada camada tem uma responsabilidade: as rotas não têm regras, os serviços não conhecem `request`, os repositórios não decidem |
| **Repository** | `app/auth/repository.py`, `app/gestao/repository.py` | Todo o SQL num só sítio; o resto do código não depende da base de dados |
| **Application Factory** | `create_app()` em `app/__init__.py` | Cada teste cria uma aplicação limpa, com a sua própria configuração e base de dados |
| **Decorator** | `login_required` (`app/auth/sessions.py`), `admin_required` (`app/gestao/sessions.py`) | Proteger páginas sem repetir a verificação em cada rota |
| **Strategy + Factory** | `Mailer` (interface), `ConsoleMailer`, `SmtpMailer` e `create_mailer()` em `app/mailer.py` | Mudar a forma de enviar emails só com uma variável (`MAIL_BACKEND`), sem tocar no registo. **É o modelo a seguir para o LLM.** |
| **Strategy** | `PerfilAluno` e `PerfilAdministrador` em `app/auth/perfis.py` | Cada perfil sabe reconhecer quem é dele, verificar a palavra-passe na sua tabela, abrir a sua sessão e para onde vai depois de entrar. A rota de início de sessão não conhece os perfis |
| **Chain of Responsibility** | `CadeiaDePerfis` em `app/auth/perfis.py` | Um só início de sessão para alunos e administradores: o pedido passa pelos perfis até um dizer «é comigo» (email → aluno; nome sem «@» → administrador). Um perfil novo entra na cadeia sem mexer nos outros |
| **Factory** | `criar_cadeia_de_perfis()` em `app/auth/perfis.py` | Monta a cadeia (que perfis existem e por que ordem) num só sítio |

### 3.1 Um só início de sessão (US03, revisão de 14/10/2026)

Antes, a gestão tinha uma página de entrada própria (`/gestao/entrar`). Agora todos entram em `/auth/entrar` e a aplicação decide o perfil. As contas continuam em tabelas separadas e a gestão continua sem ligações nas páginas dos alunos.

```mermaid
classDiagram
    class Perfil {
        <<interface>>
        +reconhece(identificador) bool
        +autenticar(db, identificador, palavra_passe) Entrada
        +iniciar_sessao(conta_id)
        +pagina_inicial
    }
    class PerfilAluno
    class PerfilAdministrador
    Perfil <|.. PerfilAluno
    Perfil <|.. PerfilAdministrador
    CadeiaDePerfis --> "1..*" Perfil : pergunta por ordem
    login_submit ..> CadeiaDePerfis : criar_cadeia_de_perfis()
```

```python
entrada = criar_cadeia_de_perfis().entrar(db, identificador, palavra_passe)
if entrada.outcome is LoginOutcome.SUCCESS:
    entrada.perfil.iniciar_sessao(entrada.conta_id)
    return redirect(url_for(entrada.perfil.pagina_inicial))
```

Testes: `tests/test_perfis.py` testa cada padrão isoladamente (incluindo um perfil falso, para mostrar que a cadeia aceita qualquer perfil com a mesma interface); `tests/test_gestao.py` testa o comportamento.

## 4. Padrões para as funcionalidades novas

### 4.1 Strategy — estratégias de recomendação (US11; depois US12, US22)

Várias formas de recomendar, com a mesma interface. O serviço não sabe qual está a usar.

```mermaid
classDiagram
    class EstrategiaRecomendacao {
        <<interface>>
        +recomendar(perfil, candidatos, n) list~Recomendacao~
    }
    class Popularidade
    class UserBased
    class SugestaoLLM
    EstrategiaRecomendacao <|.. Popularidade
    EstrategiaRecomendacao <|.. UserBased
    EstrategiaRecomendacao <|.. SugestaoLLM
    ServicoRecomendacao --> EstrategiaRecomendacao
```

```python
class EstrategiaRecomendacao(Protocol):
    nome: str
    def recomendar(self, perfil: Perfil, candidatos: list[Item], n: int) -> list[Recomendacao]: ...
```

Cada `Recomendacao` traz o item, uma pontuação e a explicação (US14). Ganhos: a US22 (comparar estratégias) e a US15 (avaliação offline) correm todas as estratégias pela mesma interface; acrescentar uma estratégia não mexe nas outras (RNF07).

### 4.2 Adapter — ligação ao LLM (US30)

A aplicação fala com uma interface sua. Cada adaptador traduz para um fornecedor concreto.

```mermaid
classDiagram
    class ClienteLLM {
        <<interface>>
        +completar(instrucoes, mensagem) str
    }
    class AdaptadorAnthropic
    class AdaptadorOllama
    class LLMFalso
    ClienteLLM <|.. AdaptadorAnthropic
    ClienteLLM <|.. AdaptadorOllama
    ClienteLLM <|.. LLMFalso
    SugestaoLLM --> ClienteLLM
```

- `AdaptadorAnthropic`: API externa (exige chave em `.env`, nunca no repositório).
- `AdaptadorOllama`: modelo local, sem custos e sem dados a sair do computador.
- `LLMFalso`: devolve respostas fixas; é o que os testes usam (RNF06: sem rede).

### 4.3 Factory — escolher a implementação pela configuração

Igual ao `create_mailer()`: uma função lê a configuração e devolve a implementação certa.

| Variável | Valores | Por omissão |
|---|---|---|
| `LLM_BACKEND` | `falso`, `anthropic`, `ollama` | `falso` |
| `LLM_MODELO` | nome do modelo do fornecedor | depende do fornecedor |
| `ESTRATEGIA_RECOMENDACAO` | `popularidade`, `user_based` | `popularidade` |

Com `falso` por omissão, quem clona o projeto consegue correr tudo sem chaves nem custos.

### 4.4 Decorator — validar, registar e guardar em cache (US30, US31)

Comportamentos que envolvem o LLM sem alterar os adaptadores:

| Decorator | Faz |
|---|---|
| `ValidarContraCatalogo` | Descarta cursos que não estão no catálogo (RN09). Se nenhum sobrar, devolve um resultado vazio com aviso |
| `RegistarSugestao` | Grava a sugestão (respostas, cursos sugeridos, data) para a linha do tempo do percurso (US31) |
| `CacheRespostas` | Respostas iguais ao mesmo catálogo devolvem a sugestão guardada, sem nova chamada |

A validação é obrigatória e fica sempre entre o LLM e o ecrã.

### 4.5 Chain of Responsibility — filtros antes de recomendar (US13, US20)

Cada filtro recebe a lista de candidatos e devolve-a reduzida: área, instituição, já concluída (RN03), curso e ano, semestre e ECTS. Acrescentar um filtro não obriga a mudar os outros, e cada um testa-se isoladamente.

### 4.6 State — o percurso do utilizador (US31)

O utilizador está num de três estados (sem curso, com curso, a escolher opcionais; ver o diagrama em [00-visao-do-produto.md](00-visao-do-produto.md#4-o-percurso-como-sequência-de-decisões)). Cada estado define o que a página inicial mostra e que transições são permitidas. Na prática, começa por uma coluna `estado` e uma função que decide a página; só vale a pena criar classes por estado se as regras crescerem.

## 5. Estrutura prevista

```
app/
  catalogo/        US04, US05 — instituições, cursos e UCs (routes, services, repository)
  orientacao/      US29, US30 — questionário e sugestão de cursos
  percurso/        US06, US31 — decisões e UCs concluídas
  recomendacao/    US11 em diante
    estrategias.py   interface e estratégias (Strategy)
    filtros.py       cadeia de filtros (Chain of Responsibility)
    fabrica.py       escolha da estratégia (Factory)
  llm/             US30
    cliente.py       interface ClienteLLM
    adaptadores.py   Anthropic, Ollama, Falso (Adapter)
    decoradores.py   validar, registar, cache (Decorator)
    fabrica.py       create_cliente_llm() (Factory)
```

Cada pasta nasce com a story que a usa: nada de pacotes vazios «para o futuro» (princípio 5 de [02-regras-de-geracao-de-codigo.md](02-regras-de-geracao-de-codigo.md)).

## 6. O pedido ao LLM (US30)

1. A aplicação **filtra primeiro** os cursos candidatos (cadeia de filtros).
2. Envia ao LLM: instruções fixas, as respostas do questionário e a lista de candidatos (código DGES, nome, instituição, descrição, saídas). Nunca email, nome ou identificadores do utilizador (RNF12).
3. Pede uma resposta em JSON: códigos dos cursos escolhidos e uma explicação curta para cada um.
4. Os decorators validam contra o catálogo, registam a sugestão e guardam em cache.
5. O utilizador vê 2 a 3 cursos com explicação e escolhe (RN10).

As instruções enviadas ao LLM ficam num ficheiro de texto versionado, para poderem ser revistas como qualquer outro código.

## 7. Como verificar que o código respeita estes padrões

- Os testes das estratégias e dos adaptadores usam a interface, não a classe concreta.
- Nenhum ficheiro fora de `app/llm/adaptadores.py` importa a biblioteca de um fornecedor.
- A checklist do Pull Request (secção 10 de [02-regras-de-geracao-de-codigo.md](02-regras-de-geracao-de-codigo.md)) inclui: «a funcionalidade nova segue os padrões de 03-arquitetura-e-padroes.md, ou o PR explica porque não».
