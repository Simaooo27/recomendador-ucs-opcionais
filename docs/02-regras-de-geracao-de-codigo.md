# Regras de geração de código com IA

Estas regras aplicam-se a **todo** o código, testes e documentação gerados com apoio de IA neste projeto (RNF09). A IA escreve o primeiro rascunho; a equipa é responsável pelo que entra no repositório. Cada prompt deve referir este documento (ver [prompts/](../prompts/)).

**Estado:** aprovado pela equipa em 2026-10-05.

| Decisão | Opção escolhida |
 |

## 1. Princípios

1. **Uma user story por prompt e por Pull Request.** Pedidos grandes geram código que ninguém consegue rever.
2. **A especificação vem primeiro.** O código implementa os requisitos em `docs/`; se o pedido contradiz um requisito, a IA deve assinalar o conflito em vez de escolher em silêncio.
3. **Nada entra sem ser lido, compreendido e testado** por um elemento da equipa que não deu o prompt.
4. **A IA não inventa requisitos.** Quando falta informação, assume o mínimo, escreve a assunção numa lista e pergunta.
5. **Menos é mais.** Sem funcionalidades, camadas ou dependências que a story não pede.

## 2. Tecnologia e dependências

| Tema | Regra |
|---|---|
| Linguagem | Python 3.10 ou superior (desenvolvido e testado em 3.12) |
| Framework web | Flask 3.x |
| Base de dados | SQLite pela biblioteca padrão (`sqlite3`), com consultas parametrizadas. Mudar para outro motor ou ORM exige decisão da equipa |
| Testes | `unittest` da biblioteca padrão (o `pytest` também os executa) |
| Motor de recomendação (sprints 2 a 4) | `pandas` e `numpy`; `scikit-surprise` só para a estratégia SVD (US22) |
| Novas dependências | Só com justificação escrita no Pull Request (para que serve, alternativa na biblioteca padrão, licença, manutenção) e atualização de `requirements.txt` |

## 3. Estrutura e responsabilidades

```
app/
  __init__.py        create_app(): configuração, extensões, blueprints
  config.py          valores por omissão e leitura de variáveis de ambiente
  db.py, schema.sql  ligação e esquema SQLite
  security.py        CSRF e cabeçalhos de segurança
  mailer.py          envio de email (console ou SMTP)
  texts.py           todos os textos que o utilizador vê (editáveis pelo Product Owner)
  <modulo>/          um pacote por área funcional (ex.: auth)
    routes.py        HTTP: lê o pedido, chama o serviço, devolve a resposta
    services.py      casos de uso: orquestra regras e persistência
    validators.py    regras de validação puras (sem Flask nem BD)
    repository.py    SQL, e só SQL
  templates/, static/
tests/               espelha a estrutura de app/
docs/, prompts/
```

- As **rotas** não contêm regras de negócio; os **serviços** não conhecem `request` nem `session`; os **repositórios** não decidem nada.
- Cada função faz uma coisa. Funções puras (validação, cálculos de similaridade) ficam separadas do acesso a dados para serem testáveis sem base de dados.
- O motor de recomendação (RNF07) vive num módulo próprio, com interface comum às estratégias.

## 4. Estilo

- PEP 8, linhas até 110 caracteres, anotações de tipo em funções públicas.
- **Identificadores em inglês; texto para o utilizador, comentários e docstrings em português de Portugal.**
- Docstring curta em todo o módulo e em funções públicas não óbvias. Comentários explicam o *porquê*, não o *quê*.
- Sem código morto, sem `print` de depuração (exceção: o email simulado do desenvolvimento), sem `TODO` sem dono.
- Mensagens de erro ao utilizador: dizem o que falhou e como corrigir; não culpam o utilizador nem expõem detalhes internos.
- Todo o texto visível ao utilizador (páginas, mensagens, emails) fica em `app/texts.py`, nunca escrito diretamente nos templates ou no código. Assim o Product Owner altera textos sem mexer na lógica.

## 5. Segurança (obrigatório, RNF02)

1. Palavras-passe **só** com hash (`werkzeug.security`). Nunca em texto, em logs, em respostas ou em mensagens de erro.
2. Todos os pedidos `POST`, `PUT`, `PATCH` e `DELETE` validam o token CSRF.
3. SQL **sempre** parametrizado. Proibido construir SQL com f-strings ou concatenação.
4. Templates com *autoescape* ativo. Proibido `|safe` e `Markup` sobre dados do utilizador.
5. Segredos (`SECRET_KEY`, credenciais SMTP) vêm do ambiente. Nunca no código nem no repositório; o `.env` está no `.gitignore`.
6. Tokens assinados, com validade e comparação em tempo constante (`hmac.compare_digest`).
7. Validação **sempre no servidor**; a validação no navegador é conforto, não proteção.
8. Logs sem dados pessoais (emails, tokens, palavras-passe).
9. Cookies de sessão `HttpOnly` e `SameSite=Lax`; `Secure` em produção.

## 6. Privacidade (RNF01, RN04)

- Recolher só os dados necessários (minimização). Cada campo novo precisa de justificação.
- As avaliações ficam ligadas a um identificador pseudonimizado (US09) e **nunca** se mostram individualmente nem em agregados com menos de 5 respostas.
- O consentimento à política de privacidade fica registado com versão e data.

## 7. Testes

1. **Cada critério de aceitação da story tem pelo menos um teste automático**, identificado na tabela de rastreabilidade do documento de requisitos da story.
2. Testes independentes entre si: base de dados temporária por teste, sem rede, sem dependência de ordem ou de relógio.
3. Testam-se os casos felizes, os casos de erro e os limites (campo vazio, comprimento máximo, valor parecido com o válido).
4. Lógica de negócio e validação: cobertura-alvo de 90% de linhas (a medir com `coverage` quando a equipa o instalar).
5. Um bug corrigido ganha primeiro um teste que falha.
6. Comando único: `python -m unittest discover -s tests -t .`

## 8. Git e rastreabilidade (RNF08)

- Ramos: `feature/US01-registo`, `fix/US01-token-expirado`.
- Commits pequenos, no imperativo, com o identificador: `US01: valida o domínio do email`.
- Um Pull Request por story, com a checklist da secção 10 preenchida. Merge só com aprovação de outro elemento.
- Nunca fazer commit de `.env`, bases de dados, dados reais de alunos ou ficheiros em `instance/`.

## 9. Uso de IA

**A IA pode:** gerar código e testes a partir de requisitos escritos, propor alternativas, rever código, explicar erros.

**A IA não pode:**
- decidir requisitos ou prioridades (é do Product Owner);
- receber dados reais de alunos, segredos ou credenciais num prompt;
- fazer commit ou merge sem revisão humana;
- ser citada como justificação: quem faz o commit responde pelo código.

**Registo obrigatório.** Cada sessão relevante fica anotada em [registo-de-uso-de-ia.md](registo-de-uso-de-ia.md): ferramenta, pedido, o que foi gerado, como foi validado e quem reviu. É material para o relatório.

## 10. Checklist de revisão (cada Pull Request)

- [ ] Os critérios de aceitação da story estão todos cumpridos e testados.
- [ ] Os testes passam localmente e não dependem de rede.
- [ ] Não há segredos, dados pessoais ou ficheiros de instância no diff.
- [ ] SQL parametrizado, CSRF nos POST, sem `|safe`.
- [ ] Sem dependências novas, ou com justificação escrita.
- [ ] Rotas finas, regras nos serviços, validação em funções puras.
- [ ] Mensagens ao utilizador claras e em português de Portugal.
- [ ] O código gerado por IA foi lido e entendido por quem submete.
- [ ] A entrada no registo de uso de IA está preenchida.
- [ ] Documentação atualizada (README, requisitos) quando o comportamento mudou.

## 11. Definition of Done

Remete para a Definition of Done da equipa: critérios verificados, código revisto por outro elemento, testes a passar, código de IA revisto e assinalado, funciona na demonstração, sem dívida técnica por registar e documentação atualizada.
