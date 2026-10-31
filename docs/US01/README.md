# US01 — Registo com email pessoal

> **Como** aluno, **quero** registar-me com o meu email pessoal, **para** poder avaliar as UCs que fiz e receber recomendações.

| | |
|---|---|
| Estado | Feita |
| Sprint | Sprint 1 |
| Story points | 3 |
| Épico | E1 — Contas e perfis |
| Prioridade | Must |
| Requisito de origem | RF01 (ver [01-requisitos-funcionais-e-nao-funcionais.md](../geral/01-requisitos-funcionais-e-nao-funcionais.md)) |

## Definition of Done da US01

A US01 só conta como «Feita» quando todas as caixas estiverem marcadas. As primeiras são os critérios de aceitação desta story (o «Confirmation» dos três C); as outras são o mínimo que a equipa exige a todas. Verificado a 31/10/2026, com 541 testes automáticos a passar.

**Critérios de aceitação desta story**

- [x] São aceites emails pessoais (24 testes automáticos, todos a passar)
- [x] A conta só fica ativa após confirmação por email (22 testes automáticos, todos a passar)
- [x] A palavra-passe é guardada com hash (1 teste automático, a passar)
- [x] O registo exige aceitação explícita da política de privacidade (2 testes automáticos, todos a passar)
- [x] (23/10) O registo pede o nome e a pessoa é tratada por ele (11 testes automáticos, todos a passar)
- [x] (Transversal) proteção CSRF e cabeçalhos (5 testes automáticos, todos a passar)

**Mínimo da equipa**

- [x] Testes a passar: os desta story e os 541 do projeto
- [x] Código revisto por outro elemento, com atenção a RNF01, RNF02, RNF04, RNF06, RNF08, RNF09, RNF10, RNF11: o PR principal (#3) foi juntado pelo próprio autor; o Simão só juntou o #2 (textos editáveis); revisão no GitHub dispensada por decisão dos Product Owners a 31/10 (o Simão acompanhou todo o trabalho)
- [x] Código gerado por IA assinalado no [registo de uso de IA](../geral/registo-de-uso-de-ia.md)
- [x] Documentação em `docs/US01/`: requisitos.md, use-case.md, bpmn.md, prompt.md
- [x] Sem dívida técnica por registar
- [x] Funciona na demonstração: usada em todas as demonstrações seguintes (Sprint Review dos Sprints 2 e 3); o Sprint 1 não tem Sprint Review registada
- [x] Aceite pelo Product Owner: fecho do Sprint 1 (07/10)

## Documentos

| Documento | Conteúdo |
|---|---|
| [requisitos.md](requisitos.md) | Requisitos funcionais, mensagens, dados guardados e critérios de aceitação |
| [use-case.md](use-case.md) | Use case ([diagrama](diagramas/use-case.svg)) |
| [bpmn.md](bpmn.md) | Processo BPMN ([imagem](diagramas/bpmn.svg) · [ficheiro editável](diagramas/bpmn.bpmn)) |
| [prompt.md](prompt.md) | Prompt usado para gerar o código com IA |

## Código

[`app/auth/`](../../app/auth/): rotas (`routes.py`), casos de uso (`services.py`), validação (`validators.py`), ligações de confirmação (`tokens.py`) e SQL (`repository.py`). Os templates estão em [`app/templates/auth/`](../../app/templates/auth/). Os textos das páginas, mensagens e email estão em [`app/texts.py`](../../app/texts.py).

## Testes

| Ficheiro | O que testa |
|---|---|
| [`tests/test_validators.py`](../../tests/test_validators.py) | Validação do email (pessoal, com domínio opcional) e da palavra-passe |
| [`tests/test_registration.py`](../../tests/test_registration.py) | Registo, rejeições, duplicados, CSRF e cabeçalhos de segurança |
| [`tests/test_confirmation.py`](../../tests/test_confirmation.py) | Ligação de confirmação e ativação da conta |
| [`tests/test_app_factory.py`](../../tests/test_app_factory.py) | Configuração da aplicação e do envio de email |
| [`tests/test_texts.py`](../../tests/test_texts.py) | Ficheiro de textos: nada vazio e marcadores `{…}` no sítio |
| [`tests/base.py`](../../tests/base.py) | Base comum: aplicação com base de dados temporária e email simulado |

A tabela critério de aceitação → teste está na secção 5 de [requisitos.md](requisitos.md#5-critérios-de-aceitação-e-testes).
