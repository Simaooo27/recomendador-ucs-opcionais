# Visão do produto — OptaBem

Projeto 1 · Metodologias Ágeis (Scrum) · Duarte Eusébio e Simão Almeida

**Versão 1.0 · decisão dos Product Owners · 2026-10-13.** Substitui a visão implícita até ao Sprint 1 («recomendador de opcionais para alunos de um curso»). As consequências nos requisitos estão na versão 1.3 de [01-requisitos-funcionais-e-nao-funcionais.md](01-requisitos-funcionais-e-nao-funcionais.md) e no [backlog](product-backlog.xlsx).

## 1. O problema

Escolher um percurso no ensino superior é uma sequência de decisões difíceis, tomadas com pouca informação:

1. **Antes de entrar**, quem está indeciso tem de escolher entre centenas de cursos em dezenas de instituições. A informação oficial (vagas, notas, provas) está espalhada e quase nunca diz *se o curso combina com a pessoa*.
2. **Depois de entrar**, o aluno escolhe opcionais com base em boatos e descrições genéricas, sem saber o que colegas parecidos com ele acharam.

## 2. Para quem é

| Público | Situação | Pergunta que traz ao OptaBem |
|---|---|---|
| **Indeciso** | Ainda não tem curso (pode estar no secundário, a mudar de área ou a regressar aos estudos) | «Que curso, e em que instituição, faz sentido para mim?» |
| **Aluno** | Já frequenta um curso de uma instituição do catálogo | «Que opcionais devo escolher?» |

O mesmo utilizador pode passar de um público para o outro: um indeciso escolhe um curso e, a partir daí, é aluno desse curso.

## 3. Visão

> Para quem tem de decidir o seu percurso no ensino superior, o **OptaBem** é uma aplicação web que sugere cursos e opcionais com explicação, a partir das preferências da pessoa e da experiência de outros estudantes. Ao contrário dos guias oficiais, que listam a oferta, o OptaBem acompanha cada decisão e diz porque é que uma opção lhe pode servir.

## 4. O percurso como sequência de decisões

O OptaBem não atribui um percurso de uma vez: acompanha cada momento de decisão, e cada decisão fica registada (data, opções sugeridas, opção escolhida).

```mermaid
stateDiagram-v2
    [*] --> SemCurso: regista-se
    SemCurso --> SemCurso: questionário e sugestões
    SemCurso --> ComCurso: escolhe curso e instituição
    ComCurso --> AEscolherOpcionais: chega a um semestre com opcionais
    AEscolherOpcionais --> ComCurso: escolhe opcionais
    ComCurso --> SemCurso: quer repensar o curso
```

| Momento | O que o OptaBem faz | Como decide |
|---|---|---|
| Escolher curso | Questionário curto e 2 a 3 cursos sugeridos, cada um com explicação | Modelo de linguagem (LLM) sobre uma lista fechada de cursos do catálogo |
| Comparar cursos | Fichas lado a lado: descrição, saídas, vagas, nota do último colocado | Dados oficiais da DGES e das instituições |
| Escolher opcionais | Opcionais sugeridas com explicação | Popularidade e, mais tarde, colegas com gostos parecidos |
| Repensar | Volta ao questionário com o histórico já preenchido | Igual a «Escolher curso» |

**O utilizador decide sempre.** O OptaBem sugere e explica; nunca atribui um curso ou uma opcional sem confirmação.

## 5. Âmbito desta release (MVP)

**Dentro:**

- Catálogo de **12 instituições e 30 licenciaturas** em três áreas (Ciência da Informação, Gestão, Informática), públicas e privadas, universidades e politécnicos: ver [`dados/catalogo-cursos-mvp.csv`](../../dados/catalogo-cursos-mvp.csv).
- Consulta e comparação de cursos.
- Questionário de orientação e sugestão de cursos com LLM.
- Escolha de curso e linha do tempo das decisões.
- Para quem já é aluno: percurso, avaliação de opcionais e recomendações por popularidade.

**Fora (backlog):** recomendação colaborativa (user-based e por itens), avaliação offline do motor, comentários, horários, mais instituições e áreas.

**Porque 12 instituições:** é o mínimo para haver comparação real dentro de cada área. A lista oficial vem da DGES; as descrições e os planos de estudos vêm do site de cada instituição, o que torna inviável cobrir «todas» nesta release.

## 6. Como sabemos que resulta

| Objetivo | Indicador | Meta para a demonstração |
|---|---|---|
| Sugestões de curso pertinentes | % de sugestões que o utilizador considera «faz sentido» | ≥ 70 % num teste com 10 pessoas |
| Sugestões fiáveis | Sugestões com cursos fora do catálogo que chegam ao ecrã | 0 (validação obrigatória, RN09) |
| Decisões acompanhadas | Utilizadores que escolhem um curso depois de receberem sugestões | ≥ 50 % no mesmo teste |
| Rapidez | Tempo do questionário à sugestão | < 2 minutos |

*As metas são uma proposta inicial; os Product Owners validam-nas na Sprint Review.*

## 7. Restrições e princípios

- **Privacidade:** ao LLM só seguem as respostas do questionário e o catálogo, nunca email, nome ou outros dados identificativos (RNF12).
- **Independência do fornecedor:** o LLM fica atrás de uma interface própria; mudar de fornecedor, ou correr um modelo local, não mexe no resto da aplicação. Ver [03-arquitetura-e-padroes.md](03-arquitetura-e-padroes.md).
- **Testável sem rede:** os testes usam um LLM falso de resposta conhecida (RNF06).
- **Sugestão do professor:** o uso de um LLM e de design patterns foi sugerido pelo docente da UC.

## 8. Decisões que deram origem a esta visão

| Data | Decisão | Quem |
|---|---|---|
| 2026-10-07 | Registo com email pessoal: o OptaBem não é exclusivo de uma instituição | Product Owners |
| 2026-10-13 | O utilizador pode ainda não ter curso; o OptaBem orienta também a escolha do curso | Product Owners |
| 2026-10-13 | Várias instituições (MVP com 12) para haver dados comparativos | Product Owners |
| 2026-10-13 | O percurso é atualizado em cada momento de decisão, não atribuído de uma vez | Product Owners |
| 2026-10-13 | LLM para sugerir cursos e design patterns na arquitetura, por sugestão do docente | Product Owners |
