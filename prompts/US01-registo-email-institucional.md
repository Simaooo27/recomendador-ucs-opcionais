# Prompt — US01: registo com email institucional

**Como usar.** Abra a ferramenta de IA com acesso ao repositório (ou anexe os ficheiros listados em «Contexto») e cole tudo o que está abaixo da linha. Depois do resultado, siga a checklist de [docs/02-regras-de-geracao-de-codigo.md](../docs/02-regras-de-geracao-de-codigo.md) (secção 10) e preencha [docs/registo-de-uso-de-ia.md](../docs/registo-de-uso-de-ia.md).

**Não inclua** emails reais de alunos, palavras-passe ou chaves no prompt.

---

## Papel

És um developer Python sénior numa equipa Scrum. Escreves código simples, testado e seguro, e dizes sempre o que assumiste.

## Contexto

Estamos a construir uma aplicação web que recomenda UCs opcionais a alunos com base nas avaliações de colegas. Esta tarefa é a **US01 — Registo com email institucional** (Sprint 1, 3 story points).

Lê, por esta ordem, antes de escreveres código:

1. `docs/03-rf-us01-registo-email-institucional.md` (o que implementar; manda sobre tudo o resto)
2. `docs/02-regras-de-geracao-de-codigo.md` (como escrever o código; obrigatório)
3. `docs/04-use-case-us01.md` e `docs/05-bpmn-us01.md` (fluxos principal e alternativos)
4. `docs/01-requisitos-funcionais-e-nao-funcionais.md` (RF01, RNF01, RNF02, RNF06, RNF08)

## Tarefa

Implementa a US01 em Flask, na estrutura descrita no documento 02:

- Formulário de registo (email, palavra-passe, repetição, aceitação da política de privacidade) e página de «confirme o seu email».
- Validação no servidor: domínio institucional configurável (por omissão `iscap.ipp.pt`, com subdomínios verdadeiros), palavra-passe (8 a 128 caracteres, uma letra e um número) e política aceite.
- Conta criada **inativa**, palavra-passe só com hash, aceitação da política gravada com versão e data.
- Email de confirmação com ligação assinada e válida 24 horas. Em desenvolvimento e nos testes o email é simulado.
- Ligação de confirmação que ativa a conta (idempotente), com respostas distintas para inválida (400) e expirada (410).
- Email já ativo: rejeitar. Email por confirmar: renovar a conta e invalidar ligações anteriores.
- Proteção CSRF em todos os `POST` e cabeçalhos de segurança.

## Restrições

- Só Flask e a biblioteca padrão. Não acrescentes dependências.
- SQLite com `sqlite3` e SQL parametrizado. Sem ORM.
- Rotas finas, regras em `services.py`, validação em funções puras, SQL só em `repository.py`.
- Identificadores em inglês; textos para o utilizador, comentários e docstrings em português de Portugal.
- Nada fora do âmbito: sem login (US02), sem pseudo-identificadores (US09), sem reenvio de ligação, sem captcha.
- Não alteres os requisitos. Se encontrares contradições ou lacunas, **assinala-as** em vez de decidir sozinho.

## Critérios de aceitação (têm de ter teste automático)

1. Só são aceites emails do domínio institucional.
2. A conta só fica ativa após confirmação por email (ou validação simulada em ambiente de teste).
3. A palavra-passe é guardada com hash.
4. O registo exige aceitação explícita da política de privacidade.

## Testes

Usa `unittest` (compatível com `pytest`). Base de dados temporária por teste, sem rede. Cobre os casos felizes, os erros e os limites: domínios parecidos (`iscap.ipp.pt.evil.com`), token adulterado, expirado, de outra chave, de utilizador inexistente e substituído, email duplicado (ativo e pendente), CSRF em falta, falha no envio do email e a palavra-passe nunca devolvida na resposta. Comando: `python -m unittest discover -s tests -t .`

## Formato da resposta

1. **Plano** em até 10 linhas, com as assunções e as dúvidas.
2. **Código completo** de cada ficheiro, com o caminho antes de cada bloco.
3. **Testes** completos.
4. **Como correr** (instalação, configuração, comandos).
5. **Rastreabilidade:** uma tabela critério de aceitação → teste.
6. **Mensagem de commit** no formato `US01: <resumo no imperativo>`.

## Verificação final (faz antes de responder)

- [ ] Cada RF01.x do documento 03 está implementado ou assinalado como não implementado.
- [ ] Cada critério de aceitação tem pelo menos um teste.
- [ ] Nenhum segredo no código; palavra-passe nunca em logs nem na resposta.
- [ ] Sem dependências novas.
- [ ] Os testes correm e passam. Se não os puderes correr, di-lo claramente.
