# Spike: LLM na conversa de orientação

**14/10/2026** · Decisão do PO (issue #15): o LLM conduz a conversa, descobre os interesses e sugere 2 a 3 cursos do catálogo, com explicação. Fornecedor: Google Gemini (plano gratuito), Groq como reserva.

**Pergunta do spike:** dá para fazer isto de graça, sem pôr em causa a privacidade, e só com cursos do catálogo?

**Resposta curta:** tecnicamente sim, e para desenvolver e demonstrar chega. Mas o plano gratuito do Gemini **não pode ser usado com utilizadores reais em Portugal**, e os termos excluem menores de 18 anos, o que choca com o público do OptaBem (secção 3). Isto é uma decisão do PO, não técnica.

## 1. Limites (revistos a 20/10/2026)

A Google não publica os números do plano gratuito: cada conta vê os seus em [AI Studio → Rate limit](https://aistudio.google.com/rate-limit). Os valores do Gemini abaixo **não são oficiais**: vêm de uma medição independente de 02/09/2026, lida na própria resposta de erro 429, e foram medidos no `gemini-3.6-flash`. O Flash mais recente, `gemini-3.8-flash` (20/10), pode ter outros limites. Antes de decidir, o PO confirma os da sua conta no AI Studio. Os limites são **por projeto** (todos os utilizadores do OptaBem partilham-nos) e o dia recomeça à meia-noite da Califórnia (por volta das 8h em Lisboa).

Cada pedido leva as instruções com o catálogo (14 769 caracteres, cerca de 4 mil tokens) mais a conversa. Uma conversa completa são até 7 pedidos (6 perguntas e a sugestão).

| Modelo | Pedidos/min | Pedidos/dia | Conversas completas por dia |
|---|---|---|---|
| Gemini Flash (`gemini-3.6-flash`; o mais recente é o `gemini-3.8-flash`) | 5 | 20 | **2 a 3** — não serve |
| Gemini Flash-Lite (`gemini-3.5-flash-lite`) | 15 | 500 | cerca de 70 |
| Groq (`openai/gpt-oss-120b`) | 30 (mas 8 mil tokens/min) | 1000 (mas 200 mil tokens/dia) | cerca de 5, e só 1 pedido por minuto |

Por isso o modelo por omissão é o **Flash-Lite**, não o Flash, ao contrário do que o PO decidiu a 14/10: falta o PO confirmar (secção 5) depois de comparar os dois com `llm-teste --modelo`. Muda-se com `LLM_MODELO` no `.env`. O Groq, com o catálogo inteiro em cada pedido, só serve de reserva para uma demonstração; para ser reserva a sério, o catálogo tem de ir mais curto (sem descrições, ou só os cursos que passaram os filtros, como diz a secção 6 de [03-arquitetura-e-padroes.md](03-arquitetura-e-padroes.md)).

## 2. Custo

Plano gratuito: 0 €. Se for preciso passar ao pago: no Flash-Lite, a 0,30 $ por milhão de tokens de entrada e 2,50 $ de saída, uma conversa (~35 mil tokens de entrada, ~2 mil de saída) custa **cerca de 1,5 cêntimos**; 100 conversas, cerca de 1,6 $. O Flash (`gemini-3.6-flash` e `gemini-3.8-flash`) custa 2,5 vezes mais na entrada (0,75 $; 3,75 $ de saída) e o preço duplica a 01/01/2027.

## 3. Privacidade e termos de utilização

| | Gemini, plano gratuito | Groq |
|---|---|---|
| O que fazem com o que enviamos | Fora da Europa, o plano gratuito é usado para melhorar os produtos da Google, com revisão humana. **No EEE (Portugal), Suíça e Reino Unido aplicam-se as regras de dados do plano pago, mesmo no gratuito**: não é usado para isso. Pedem na mesma para não enviar dados pessoais | Por omissão não guardam; podem registar até 30 dias para abuso; há opção de retenção zero |
| Utilizadores no EEE (Portugal) | «You may use only Paid Services» ao disponibilizar a aplicação a utilizadores do EEE, Suíça ou Reino Unido | Nada nos Termos de Utilização; o contrato do GroqCloud não foi lido |
| Idade | Quem usa a API tem de ter 18 anos, e a aplicação não pode ser dirigida a menores de 18 nem ter probabilidade de ser usada por eles | Nada encontrado |

**O que o código garante (RNF12):** a conversa nunca recebe a conta (email, nome, identificador); o decorator `ProtegerDadosPessoais` apaga emails e números longos (telemóvel, NIF, cartão de cidadão, IBAN, código postal) do que a pessoa escreve. **Limite:** não reconhece nomes próprios escritos no texto; a página da conversa (US29) tem de avisar para não os escrever.

**O que o código garante (RN09):** só aparecem cursos cujo identificador existe no catálogo; o resto é descartado e contado. O identificador é `instituição-curso`, porque o código de curso da DGES repete-se entre instituições (ex.: 9694 no Porto e em Coimbra).

## 4. Viabilidade

| Aspeto | Conclusão |
|---|---|
| Técnica | **Sim.** `ClienteLLM`, `LLMFalso`, adaptadores Gemini e Groq, fábrica por `LLM_BACKEND`, 41 testes sem rede |
| Para desenvolver e demonstrar | **Sim**, com o Flash-Lite |
| Com utilizadores reais em Portugal | **Não no plano gratuito do Gemini.** Pago (≈1,5 cênt./conversa) ou Groq com catálogo encurtado (contrato por confirmar) |
| Com menores de 18 anos | **Não pelos termos do Gemini.** O público «pessoa a escolher licenciatura» inclui alunos do secundário |
| Por saber | A qualidade das perguntas e sugestões em português e se o modelo cumpre sempre o formato JSON. É isso que o teste do PO mostra |

## 5. Decisões para o PO

1. **Idade:** a conversa com LLM é só para maiores de 18 (e os menores usam a pesquisa e a comparação da US05), ou muda-se de fornecedor? **Decidido a 20/10:** aviso de 18+ na conversa, sem verificação (protótipo).
2. **Âmbito do plano gratuito:** só para a equipa e para a demonstração na aula, assumido no relatório como protótipo? **Decidido a 20/10:** sim (ponto 14 dos requisitos, opção a).
3. **Flash-Lite em vez de Flash:** confirmar, depois de comparar os dois com `flask --app app llm-teste --backend gemini` e `… --modelo gemini-3.8-flash`, e de ver os limites da conta no AI Studio.

## 6. Como repetir o teste (no computador do PO)

Na pasta do projeto, depois de `pip install -r requirements.txt` (entrou o `python-dotenv`, para o comando ler o `.env`):

```
flask --app app llm-teste --backend gemini
```

Faz 2 pedidos e mostra: a primeira pergunta do LLM, e a sugestão de cursos depois de uma resposta de exemplo (com um email de propósito, que é apagado antes de sair do computador). Nunca mostra a chave. Se aparecer «limite de pedidos atingido», ver os limites da conta no AI Studio; se aparecer «modelo não existe», experimentar `--modelo gemini-3.1-flash-lite`.

**Fontes:** [limites](https://ai.google.dev/gemini-api/docs/rate-limits) e [preços](https://ai.google.dev/gemini-api/docs/pricing) do Gemini; [termos da API do Gemini](https://ai.google.dev/gemini-api/terms); [medição de 02/09/2026](https://aiplug.work/en/blog/gemini-free-tier-limits); [limites](https://console.groq.com/docs/rate-limits) e [dados](https://console.groq.com/docs/your-data) do Groq; [termos de utilização do Groq](https://groq.com/terms-of-use).

## 7. Servidor Ollama da faculdade: testado e posto de parte (20/10/2026)

O docente recomendou um servidor Ollama da faculdade, partilhado pelos alunos. Foi ligado ao OptaBem (PR #25) e testado pelo PO no seu computador com o comando `llm-teste`, com o modelo `qwen3:4b`, lado a lado com o Gemini:

| | Ollama (`qwen3:4b`) | Gemini Flash-Lite |
|---|---|---|
| 1.ª pergunta | 6 a 7 s; em português do Brasil («O que você gosta de fazer…»), apesar de as instruções pedirem PT-PT | 3 s, em PT-PT |
| Sugestão de cursos | Com o limite de 15 s: não chegou a tempo. Com 60 s: fez outra pergunta em vez de sugerir (a aplicação recusou-a, como manda o RF36.4) | 1 s; 2 cursos do catálogo adequados à resposta de exemplo, com explicação |

**Decisão do PO (20/10):** o servidor da faculdade não cumpre o RNF12 (resposta em menos de 15 s) nem obedece ao pedido de sugestão com este modelo, por isso o adaptador foi retirado (PR de reversão do #25). Fica o **Gemini**, com o Groq como reserva. O ponto 14 dos requisitos (termos do Gemini) continua por decidir. Se for preciso voltar a experimentar, o adaptador está no histórico do Git (commit `a18cb33`).

**Revisão de 20/10/2026:** o Flash mais recente passou a ser o `gemini-3.8-flash`; corrigido o que a Google faz com os dados no EEE (aplicam-se as regras do plano pago, mesmo no gratuito); os limites da secção 1 assinalados como não oficiais. Confirmado nas páginas de [modelos](https://ai.google.dev/gemini-api/docs/latest-model), [preços](https://ai.google.dev/pricing), [limites](https://ai.google.dev/gemini-api/docs/rate-limits) e [termos](https://ai.google.dev/terms).
