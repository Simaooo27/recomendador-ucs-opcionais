## User story

<!-- Identificador e título, com ligação para a issue e para docs/USNN/. Ex.: US02 — Autenticação (closes #12) -->

## O que muda

<!-- Resumo das alterações: código, testes e documentação. -->

## Como testar

<!-- Comandos e passos para verificar a story. -->

```bash
python -m unittest discover -s tests -t .
```

## Checklist de revisão

Secção 10 de [docs/geral/02-regras-de-geracao-de-codigo.md](../docs/geral/02-regras-de-geracao-de-codigo.md).

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
