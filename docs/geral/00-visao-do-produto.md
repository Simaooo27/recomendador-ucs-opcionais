# Visão do produto — OptaBem

Projeto 1 · Metodologias Ágeis (Scrum) · Duarte Eusébio e Simão Almeida

**Versão 1.2 · decisão dos Product Owners · 2026-10-27** (1.0 de 13/10; 1.1 de 14/10: o LLM conduz a conversa de orientação; 1.2: o OptaBem passa a ser só um recomendador de cursos, com autorização do docente). Substitui a visão implícita até ao Sprint 1 («recomendador de opcionais para alunos de um curso»). As consequências nos requisitos estão na versão 1.9 de [01-requisitos-funcionais-e-nao-funcionais.md](01-requisitos-funcionais-e-nao-funcionais.md) e no [backlog](product-backlog.xlsx).

## 1. O problema

Escolher um percurso no ensino superior é uma sequência de decisões difíceis, tomadas com pouca informação:

1. **Que curso?** Quem está indeciso tem de escolher entre centenas de cursos em dezenas de instituições. A informação oficial (vagas, notas, provas) está espalhada e quase nunca diz *se o curso combina com a pessoa*.
2. **Consigo entrar?** Depois de escolher, a pessoa tem de perceber que provas precisa, que nota terá em cada curso e como ordenar as 6 opções da candidatura. As regras estão na DGES, mas as contas ficam por fazer.

## 2. Para quem é

| Público | Situação | Pergunta que traz ao OptaBem |
|---|---|---|
| **Indeciso** | Ainda não tem curso (pode estar no secundário, a mudar de área ou a regressar aos estudos) | «Que curso, e em que instituição, faz sentido para mim?» |
| **Candidato** | Já sabe que curso ou que área quer | «Consigo entrar? Como ordeno as minhas opções?» |

O mesmo utilizador passa de um público para o outro: um indeciso escolhe um curso e, a partir daí, prepara a candidatura.

## 3. Visão

> Para quem tem de decidir o seu percurso no ensino superior, o **OptaBem** é uma aplicação web que recomenda cursos com explicação, a partir de uma conversa sobre os interesses da pessoa, e a ajuda a preparar a candidatura com os dados oficiais da DGES. Ao contrário dos guias oficiais, que listam a oferta, o OptaBem acompanha cada decisão e diz porque é que um curso lhe pode servir e se lá consegue chegar.

## 4. O percurso como sequência de decisões

O OptaBem não atribui um percurso de uma vez: acompanha cada momento de decisão, e cada decisão fica registada (data, opções sugeridas, opção escolhida).

```mermaid
stateDiagram-v2
    [*] --> SemCurso: regista-se
    SemCurso --> SemCurso: conversa de orientação e sugestões
    SemCurso --> ComCurso: escolhe curso e instituição
    ComCurso --> ComCurso: prepara a candidatura (6 opções)
    ComCurso --> SemCurso: quer repensar o curso
```

| Momento | O que o OptaBem faz | Como decide |
|---|---|---|
| Escolher curso | Conversa em que o assistente faz perguntas sobre os interesses da pessoa (no máximo 6) e termina com 2 a 3 cursos sugeridos, cada um com explicação | Modelo de linguagem (LLM) que conduz a conversa e sugere só cursos de uma lista fechada do catálogo |
| Comparar cursos | Fichas lado a lado: descrição, saídas, vagas, nota do último colocado | Dados oficiais da DGES e das instituições |
| Preparar a candidatura | Condições de acesso de cada curso, a nota de candidatura da pessoa em cada um e a lista das 6 opções, com avisos | Regras e dados oficiais da DGES (contingente geral, 1.ª fase); estimativa, não garantia |
| Repensar | Nova conversa de orientação; as decisões anteriores ficam na linha do tempo | Igual a «Escolher curso» |

**Decisão dos Product Owners (22/10/2026):** até à entrega de 05/11, o centro do produto são os cursos. O site deixa de falar de opcionais; as opcionais ficam para uma fase seguinte.

**Decisão do PO (23/10/2026):** depois da escolha do curso, o percurso continua com o **plano de candidatura** ao Concurso Nacional de Acesso (no ensino superior português a escolha de opcionais pesa pouco; a candidatura é a decisão real de quem está a escolher curso).

**Reestruturação (27/10/2026, com autorização do docente):** o OptaBem deixa de ser também um recomendador de opcionais. Os requisitos e as stories das opcionais saem do produto e ficam arquivados (anexo A dos requisitos e folha «Arquivo (opcionais)» do backlog).

**O utilizador decide sempre.** O OptaBem sugere e explica; nunca atribui um curso sem confirmação, nem submete a candidatura.

## 5. Âmbito desta release (MVP)

**Dentro:**

- Catálogo de licenciaturas recolhido das páginas da DGES (US04): no protótipo, 174 cursos com condições de acesso; as 30 licenciaturas do MVP (12 instituições, três áreas) mantêm as descrições escritas pela equipa ([`dados/README.md`](../../dados/README.md)).
- Consulta e comparação de cursos.
- Conversa de orientação conduzida por um LLM e sugestão de 2 a 3 cursos do catálogo.
- Escolha de curso e linha do tempo das decisões.
- Plano de candidatura: condições de acesso, notas do candidato, nota de candidatura a cada curso e as 6 opções com avisos (US33 a US36).
- Apagar a conta e todos os dados.

**Fora (backlog):** quanto preciso no exame, tendência e procura dos cursos, combinações de exames, plano B da 2.ª fase e partilhar o plano (código feito como protótipo, por aceitar); assistente que conhece as notas; exportar os dados; recuperar a palavra-passe; gestão do catálogo; datas do concurso.

**Fora do produto (arquivado a 27/10):** tudo o que era das opcionais — percurso por UCs, avaliações, recomendação colaborativa, comentários e horários.

## 6. Como sabemos que resulta

| Objetivo | Indicador | Meta para a demonstração |
|---|---|---|
| Sugestões de curso pertinentes | % de sugestões que o utilizador considera «faz sentido» | ≥ 70 % num teste com 10 pessoas |
| Sugestões fiáveis | Sugestões com cursos fora do catálogo que chegam ao ecrã | 0 (validação obrigatória, RN09) |
| Decisões acompanhadas | Utilizadores que escolhem um curso depois de receberem sugestões | ≥ 50 % no mesmo teste |
| Rapidez | Tempo da primeira pergunta à sugestão (até 6 perguntas) | < 4 minutos (proposta de 14/10; era 2 minutos com o questionário fixo) |

*As metas são uma proposta inicial; os Product Owners validam-nas na Sprint Review.*

## 7. Restrições e princípios

- **Privacidade:** ao LLM só seguem o texto da conversa (sem emails nem números longos, que são apagados antes de enviar) e o catálogo, nunca email, nome ou identificadores da conta (RNF12). Fornecedor, limites e termos: [05-spike-llm.md](05-spike-llm.md).
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
| 2026-10-14 | Sem perguntas fixas: o LLM conduz a conversa e associa as respostas a cursos do catálogo (issue #15). Fornecedor: Google Gemini (plano gratuito), Groq como reserva | Product Owner (Duarte Eusébio) |
| 2026-10-20 | O OptaBem é um protótipo usado pela equipa e na demonstração (termos do Gemini) | Product Owner (Duarte Eusébio) |
| 2026-10-22 | Até à entrega de 05/11, o centro do produto são os cursos; as opcionais saem do site | Product Owners |
| 2026-10-23 | O plano de candidatura ao concurso nacional ocupa o lugar das opcionais; o catálogo vem da DGES por recolha | Product Owner (Duarte Eusébio) |
| 2026-10-27 | O OptaBem passa a ser só um recomendador de cursos; as opcionais ficam arquivadas (autorizado pelo docente) | Product Owner (Duarte Eusébio) |
