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

Formato: UTF-8 com BOM (abre diretamente no Excel), separador vírgula.

### O que falta ou exige atenção

- **Gestão da Universidade de Aveiro:** sem descrição nem saídas (o site da UA não estava acessível na recolha).
- **Sem saídas profissionais:** Gestão do Iscte e Engenharia Informática da Universidade de Aveiro.
- **Sem nota do último colocado:** os três cursos da Universidade Portucalense, Gestão do ISCAP e Sistemas de Informação para a Gestão da ESTG (a DGES não mostra o valor).
- A DGES classifica as licenciaturas em Engenharia Informática na área CNAEF «523 Eletrónica e Automação»; o valor foi mantido tal como está na fonte.
- As descrições são a base das sugestões do LLM (US30): devem ser revistas pelos Product Owners antes dessa story.

### Acrescentar instituições ou cursos

Acrescentar linhas com as mesmas colunas. Os dados de acesso estão na página «Guia da Candidatura» de cada curso na DGES (`https://www.dges.gov.pt/guias/detcursopi.asp?codc=<curso>&code=<instituição>`); a descrição e as saídas vêm do site da instituição, escritas por palavras nossas.
