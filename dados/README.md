# Dados do catálogo

Ficheiros de dados públicos usados pelo OptaBem. Não há aqui dados de utilizadores: esses ficam em `instance/`, fora do Git.

## `catalogo-cursos-mvp.csv`

Catálogo do MVP: **30 licenciaturas de 12 instituições**, em três áreas (Ciência da Informação 5, Gestão 11, Informática 14). É o ficheiro que a US04 vai importar. Recolhido a 2026-10-13 (ver o [registo de uso de IA](../docs/geral/registo-de-uso-de-ia.md)).

| Coluna | Conteúdo | Fonte |
|---|---|---|
| `instituicao`, `unidade_organica`, `tipo_ensino`, `localidade` | Onde é lecionado o curso | DGES |
| `codigo_instituicao_dges`, `codigo_curso_dges` | Códigos do concurso nacional; o par identifica o curso | DGES |
| `curso`, `grau`, `duracao_semestres`, `ects` | Identificação do curso | DGES |
| `area_optabem` | Área usada no OptaBem para comparar cursos | Equipa |
| `vagas_2026` | Vagas do concurso nacional para 2026-2027 | DGES |
| `ultimo_colocado_1fase_2025` | Nota de candidatura do último colocado, contingente geral, 1.ª fase de 2025 (vazio quando a DGES não a mostra) | DGES |
| `area_cnaef` | Área de educação e formação, tal como a DGES a indica | DGES |
| `descricao`, `saidas_profissionais` | Resumo escrito pela equipa a partir do site da instituição | Ver `fonte_descricao` |
| `fonte_dados_acesso`, `fonte_descricao` | Ligações para confirmar cada linha | — |

`catalogo-cursos.csv` (catálogo completo, US04 e US48) tem as mesmas colunas e, desde 23/10, as **condições de acesso** usadas no plano de candidatura (lidas por `recolher_dges.py processar`):

| Coluna | Conteúdo | Fonte |
|---|---|---|
| `provas_ingresso` | Conjuntos alternativos de provas, por código: `09\|17+18` = Geografia, **ou** Mat. Apl. Ciências Soc. **e** Português. Basta um conjunto. Vazio quando a DGES manda consultar a instituição | DGES |
| `peso_secundario`, `peso_provas` | Percentagem da média do secundário e das provas na nota de candidatura | DGES |
| `minimo_candidatura`, `minimo_provas` | Classificações mínimas, em pontos (0 a 200) | DGES |
| `pre_requisitos` | Tipo e grupo de pré-requisitos (por exemplo, «Seleção: Grupo F - Capacidade visual e motora») | DGES |

| `ultimo_colocado_1fase_2023`, `ultimo_colocado_1fase_2024` | Nota do último colocado (contingente geral, 1.ª fase) nos dois anos anteriores, para a tendência | DGES |
| `vagas_1fase_2025`, `candidatos_1fase_2025`, `candidatos_1opcao_1fase_2025`, `colocados_1fase_2025` | Procura na 1.ª fase de 2025: vagas, candidatos (em qualquer opção), candidatos com o curso em 1.ª opção e colocados | DGES |

| `vagas_2fase_2025`, `colocados_2fase_2025`, `ultimo_colocado_2fase_2025` | 2.ª fase de 2025: vagas, colocados e nota do último colocado (plano B) | DGES |

`provas-ingresso.csv` tem o código e o nome de cada prova de ingresso (`18,Português`), também escrito pelo `processar`.

Formato: UTF-8 com BOM (abre diretamente no Excel), separador vírgula.

### O que falta ou exige atenção

- **Gestão da Universidade de Aveiro:** sem descrição nem saídas (o site da UA não estava acessível na recolha).
- **Sem saídas profissionais:** Gestão do Iscte e Engenharia Informática da Universidade de Aveiro.
- **Sem nota do último colocado:** os três cursos da Universidade Portucalense, Gestão do ISCAP e Sistemas de Informação para a Gestão da ESTG (a DGES não mostra o valor).
- A DGES classifica as licenciaturas em Engenharia Informática na área CNAEF «523 Eletrónica e Automação»; o valor foi mantido tal como está na fonte.
- As descrições são a base das sugestões do LLM (US30): devem ser revistas pelos Product Owners antes dessa story.
- **Ensino privado:** a candidatura é feita na instituição e não entra nas 6 opções do concurso nacional. O CSV não tem uma coluna «concurso»; a aplicação usa o `tipo_ensino` (`Curso.concurso_nacional`). Na recolha completa (29/10) isto bate certo nas 1704 páginas guardadas: 451 dos 493 cursos privados têm «Concurso: Institucional» e os outros 42 (todos da Universidade Católica) mandam pedir as condições à universidade; nenhum curso público está fora do concurso. Se a recolha passar a guardar o campo «Concurso», usar esse.
- **Sem nota do último colocado em 2025:** ver a secção seguinte. Nestes cursos o plano diz só se a pessoa cumpre os mínimos.
- **Matemáticas (27/10):** as provas de ingresso 16 «Matemática», 17 «MACS» e 19 «Matemática A» fazem-se com exames diferentes (635, 735, 835); a correspondência está em `ACEITA`, em `app/candidatura/calculos.py`.

## Recolha completa (US48, 29/10/2026)

Recolha de todas as licenciaturas e mestrados integrados do concurso nacional, feita pelo PO no seu computador com `recolher_dges.py descarregar` (interrompida aos 1200 cursos e retomada) e `processar`. Os 174 cursos da recolha anterior continuam iguais; os outros foram acrescentados.

| | Cursos |
|---|---|
| **Total no `catalogo-cursos.csv`** | **1699** (1645 licenciaturas e 54 mestrados integrados) |
| Ensino público (608 politécnico, 598 universitário) | 1206 |
| Ensino privado (298 universitário, 195 politécnico; fora do concurso nacional) | 493 |
| Páginas guardadas que ficaram de fora (outros graus: preparatórios) | 5 |
| Áreas do OptaBem | 24 (a maior é Gestão, com 248 cursos) |
| Com descrição e saídas escritas pela equipa (os do MVP) | 29 |

**Sem nota do último colocado em 2025: 664 cursos.** Não é um erro da recolha: a DGES não mostra o valor (verificado numa página guardada, em que a coluna de 2025 está vazia).

- 493 do ensino privado: não entram no concurso nacional.
- 70 públicos com dados da 1.ª fase de 2025, mas sem colocados pelo contingente geral (33 sem nenhum colocado).
- 101 públicos sem dados de 2025 na DGES (por exemplo, cursos novos); 14 destes também não têm vagas para 2026.

**Sem provas de ingresso: 42 cursos,** todos da Universidade Católica (a DGES manda consultar a universidade).

**Tempos das páginas (RNF03):** com os 1699 cursos, todas as páginas principais respondem bem abaixo de 2 segundos (no máximo cerca de 70 ms no 1.º pedido, medido a 29/10 num computador de desenvolvimento). Para repetir a medição no próprio computador: `python tests/medir_tempos.py`.

**Limites que ficam:** na conversa com o assistente, cada área envia no máximo 80 cursos (`MAX_CURSOS_ENVIADOS`), por ordem: com descrição, na localidade referida, com mais vagas. Em 7 áreas (Gestão, Saúde, Artes, Informática, Engenharia, Ciências sociais, Turismo) há mais cursos do que isso, por isso os cursos pequenos só chegam ao assistente se a pessoa disser a localidade. Só 29 cursos têm descrição; nos outros, o assistente só tem o nome, a área e os dados da DGES.

### Acrescentar instituições ou cursos

Acrescentar linhas com as mesmas colunas. Os dados de acesso estão na página «Guia da Candidatura» de cada curso na DGES (`https://www.dges.gov.pt/guias/detcursopi.asp?codc=<curso>&code=<instituição>`); a descrição e as saídas vêm do site da instituição, escritas por palavras nossas.
