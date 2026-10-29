"""Contas do plano de candidatura (Concurso Nacional de Acesso, contingente geral, 1.ª fase).

Funções puras, sem Flask nem base de dados. As regras, como a DGES as publica para cada curso:

- **Provas de ingresso:** o curso aceita um ou mais conjuntos de exames nacionais; basta ter um
  conjunto. A classificação das provas é a média dos exames do conjunto (0 a 200 pontos).
- **Fórmula:** nota de candidatura = média do secundário × peso + provas × peso (0 a 200 pontos).
  A média do secundário (0 a 20 valores) conta ×10.
- **Mínimos:** cada prova e a nota de candidatura têm de chegar ao mínimo do curso.
- **Último colocado:** a nota do último a entrar em 2025 serve de referência, não de garantia.

Fica de fora (dito na página): contingentes especiais, preferência regional, pré-requisitos e
cursos com regras próprias. Usa-se sempre o conjunto de provas que dá a nota mais alta.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from itertools import combinations
from enum import Enum
from typing import Mapping

from ..catalogo.repository import Curso

# Diferença (em pontos, de 0 a 200) para o último colocado abaixo da qual a situação é «perto».
MARGEM = 5.0

# As notas guardam-se por exame nacional. Nas outras disciplinas, cada prova de ingresso faz-se com um
# só exame e usa-se o código da prova. Nas Matemáticas não (correspondência publicada pela DGES para
# 2026, confirmada a 27/10):
#   prova 16 «Matemática»                    <- exame 635 (Matemática A) ou 735 (Matemática B)
#   prova 17 «Matemática Aplicada às C. S.»   <- exame 635, 735 ou 835 (MACS)
#   prova 19 «Matemática A»                  <- exame 635
# Os exames guardam-se com o código da prova que só eles fazem: Matemática A em «19», Matemática B
# em «16» e MACS em «17». ACEITA diz que exames guardados servem para cada prova.
ACEITA = {"16": ("19", "16"), "17": ("19", "16", "17"), "19": ("19",)}

# Como se chamam os exames no formulário e no plano (as provas mantêm o nome da DGES na ficha).
NOMES_DOS_EXAMES = {
    "19": "Matemática A (exame 635)",
    "16": "Matemática B (exame 735)",
    "17": "Matemática Aplicada às Ciências Sociais (exame 835)",
}
NOMES_CURTOS_DOS_EXAMES = {"19": "Matemática A", "16": "Matemática B", "17": "MACS"}


def exames_que_servem(prova: str) -> tuple[str, ...]:
    """Os exames (pelo código com que se guardam) que dão a prova de ingresso ``prova``."""
    return ACEITA.get(prova, (prova,))


class Situacao(str, Enum):
    ACIMA = "acima"                   # nota ≥ último colocado + margem
    PERTO = "perto"                   # a menos de MARGEM pontos do último colocado
    ABAIXO = "abaixo"                 # mais de MARGEM pontos abaixo
    SEM_REFERENCIA = "sem_referencia" # cumpre os mínimos, mas o curso não tem nota do último colocado
    ABAIXO_DO_MINIMO = "abaixo_do_minimo"
    FALTA_PROVA = "falta_prova"       # não tem nenhum conjunto de provas completo
    SEM_NOTAS = "sem_notas"           # o aluno ainda não indicou a média do secundário
    SEM_REGRAS = "sem_regras"         # a DGES não publica as condições deste curso
    FORA_DO_CONCURSO = "fora_do_concurso"  # ensino privado: candidatura na instituição, não no concurso nacional

    @property
    def conta(self) -> bool:
        """True se a opção pode dar colocação (cumpre provas e mínimos)."""
        return self in (Situacao.ACIMA, Situacao.PERTO, Situacao.ABAIXO, Situacao.SEM_REFERENCIA)


@dataclass(frozen=True)
class Notas:
    media: float | None = None                          # média do secundário, 0 a 20
    exames: Mapping[str, float] = field(default_factory=dict)   # exame (código, ver ACEITA) -> 0 a 200

    def exame(self, codigo: str) -> float | None:
        """A nota da prova de ingresso ``codigo``: a mais alta dos exames que a dão (ver ACEITA)."""
        notas = [self.exames[e] for e in exames_que_servem(codigo) if e in self.exames]
        return max(notas) if notas else None


@dataclass(frozen=True)
class Simulacao:
    situacao: Situacao
    nota: float | None = None                  # nota de candidatura (0 a 200), uma casa decimal
    conjunto: tuple[str, ...] = ()             # provas usadas na conta
    diferenca: float | None = None             # nota − último colocado
    em_falta: tuple[str, ...] = ()             # provas que faltam para o conjunto mais próximo
    abaixo_do_minimo: tuple[str, ...] = ()     # provas com nota abaixo do mínimo ("" = a nota final)


def ler_numero(texto: str) -> float | None:
    """«14,5» ou «14.5» -> 14.5; vazio ou inválido -> None."""
    texto = (texto or "").strip().replace(",", ".")
    try:
        return float(texto) if texto else None
    except ValueError:
        return None


def nota_de_exame(texto: str) -> float | None:
    """Os exames dão-se de 0 a 200, mas muita gente pensa em valores: «14,5» conta como 145."""
    valor = ler_numero(texto)
    if valor is None:
        return None
    return round(valor * 10, 1) if valor <= 20 else valor


def simular(curso: Curso, notas: Notas) -> Simulacao:
    """A nota de candidatura do aluno a um curso e a comparação com o último colocado."""
    if not curso.concurso_nacional:
        return Simulacao(Situacao.FORA_DO_CONCURSO)
    if not curso.tem_condicoes_de_acesso:
        return Simulacao(Situacao.SEM_REGRAS)
    if notas.media is None:
        return Simulacao(Situacao.SEM_NOTAS)

    completos, mais_proximo = [], None
    for conjunto in curso.provas:
        faltam = tuple(p for p in conjunto if notas.exame(p) is None)
        if not faltam:
            completos.append(conjunto)
        elif mais_proximo is None or len(faltam) < len(mais_proximo):
            mais_proximo = faltam
    if not completos:
        return Simulacao(Situacao.FALTA_PROVA, em_falta=mais_proximo or ())

    minimo_prova = curso.minimo_provas or 0
    melhor: Simulacao | None = None
    for conjunto in completos:
        valores = [notas.exame(p) for p in conjunto]
        baixas = tuple(p for p, v in zip(conjunto, valores) if v < minimo_prova)
        provas = sum(valores) / len(valores)
        nota = round(notas.media * 10 * curso.peso_secundario / 100 + provas * curso.peso_provas / 100, 1)
        if baixas:
            candidato = Simulacao(Situacao.ABAIXO_DO_MINIMO, nota, conjunto, abaixo_do_minimo=baixas)
        elif curso.minimo_candidatura is not None and nota < curso.minimo_candidatura:
            candidato = Simulacao(Situacao.ABAIXO_DO_MINIMO, nota, conjunto, abaixo_do_minimo=("",))
        else:
            candidato = _comparar(curso, nota, conjunto)
        # Prefere um conjunto que conte; entre iguais, o de nota mais alta.
        if melhor is None or (candidato.situacao.conta, candidato.nota) > (melhor.situacao.conta, melhor.nota):
            melhor = candidato
    return melhor


def _comparar(curso: Curso, nota: float, conjunto: tuple[str, ...]) -> Simulacao:
    referencia = curso.ultimo_colocado_numero
    if referencia is None:
        return Simulacao(Situacao.SEM_REFERENCIA, nota, conjunto)
    diferenca = round(nota - referencia, 1)
    if diferenca >= MARGEM:
        situacao = Situacao.ACIMA
    elif diferenca > -MARGEM:
        situacao = Situacao.PERTO
    else:
        situacao = Situacao.ABAIXO
    return Simulacao(situacao, nota, conjunto, diferenca)


@dataclass(frozen=True)
class Necessidade:
    """Quanto precisa nas provas que faltam para chegar a uma nota (US «quanto preciso no exame?»)."""
    pontos: float                 # nota necessária em cada prova em falta (0 a 200)
    conjunto: tuple[str, ...]     # o conjunto de provas em que é mais fácil lá chegar
    em_falta: tuple[str, ...]     # as provas desse conjunto que ainda não fez
    alvo: float                   # a nota de candidatura a atingir
    alvo_e_o_ultimo: bool         # True = último colocado; False = só a nota mínima do curso
    maximo: float = 200.0         # a nota mais alta possível com esta média (200 em todas as provas)

    @property
    def possivel(self) -> bool:
        return self.pontos <= 200


def nota_necessaria(curso: Curso, notas: Notas) -> Necessidade | None:
    """A nota que precisa em cada prova que ainda não fez para chegar ao último colocado (ou, sem
    essa referência, à nota mínima do curso), no conjunto de provas em que é mais fácil.

    Usa a média do secundário indicada e as provas já feitas. Se faltar mais de uma prova no
    conjunto, supõe a mesma nota em todas. ``None`` sem média, sem regras ou quando já fez as
    provas de todos os conjuntos (aí a ``simular`` já diz a nota).
    """
    if not curso.concurso_nacional or not curso.tem_condicoes_de_acesso or notas.media is None or not curso.peso_provas:
        return None
    referencia = curso.ultimo_colocado_numero
    alvo = referencia if referencia is not None else float(curso.minimo_candidatura or 0)
    if curso.minimo_candidatura is not None:
        alvo = max(alvo, float(curso.minimo_candidatura))
    parte_secundario = notas.media * 10 * curso.peso_secundario / 100
    melhor: Necessidade | None = None
    for conjunto in curso.provas:
        feitas = [notas.exame(p) for p in conjunto if notas.exame(p) is not None]
        faltam = tuple(p for p in conjunto if notas.exame(p) is None)
        if not faltam:
            continue
        media_provas = (alvo - parte_secundario) / (curso.peso_provas / 100)
        pontos = (media_provas * len(conjunto) - sum(feitas)) / len(faltam)
        pontos = max(pontos, float(curso.minimo_provas or 0))
        pontos = math.ceil(round(pontos * 10, 6)) / 10   # arredonda para cima: 124,01 -> 124,1
        maximo = round(parte_secundario + 200 * curso.peso_provas / 100, 1)
        candidato = Necessidade(pontos, conjunto, faltam, alvo, referencia is not None, maximo)
        # O conjunto que pede a nota mais baixa; entre iguais, o que tem menos provas por fazer.
        if melhor is None or (candidato.pontos, len(candidato.em_falta)) < (melhor.pontos, len(melhor.em_falta)):
            melhor = candidato
    return melhor


# -- Que exames me abrem mais portas? (23/10) ------------------------------------------------------

MAX_EXAMES = 3   # quase ninguém faz mais de 3 exames nacionais como provas de ingresso


@dataclass(frozen=True)
class Combinacao:
    provas: tuple[str, ...]          # códigos dos exames da combinação
    abre: tuple[Curso, ...]          # cursos a que estes exames dão para concorrer
    nao_abre: tuple[Curso, ...]
    ja_feitas: tuple[str, ...]       # exames da combinação que a pessoa já indicou


def exames_que_abrem_portas(cursos, notas: Notas, limite: int = 3) -> list[Combinacao]:
    """As combinações de até 3 exames que dão para concorrer a mais cursos da lista.

    Os exames são os de ``ACEITA`` (Matemática A, B e MACS) e, nas outras disciplinas, o da prova.
    Um curso fica «aberto» se a combinação dá todas as provas de um dos seus conjuntos.
    Ficam só as combinações mínimas (sem exames a mais para o mesmo resultado), ordenadas por
    número de cursos abertos, depois por número de exames e, por fim, pelos exames já feitos.
    """
    com_regras = [c for c in cursos if c.tem_condicoes_de_acesso and c.concurso_nacional]
    if len(com_regras) < 2:
        return []
    codigos = sorted({e for c in com_regras for conj in c.provas for p in conj for e in exames_que_servem(p)})
    feitos = set(notas.exames)

    def da(conjunto, escolhidos) -> bool:
        return all(any(e in escolhidos for e in exames_que_servem(p)) for p in conjunto)

    candidatas = []
    for tamanho in range(1, MAX_EXAMES + 1):
        for combo in combinations(codigos, tamanho):
            escolhidos = frozenset(combo)
            abre = tuple(c for c in com_regras if any(da(conj, escolhidos) for conj in c.provas))
            if abre:
                candidatas.append((escolhidos, abre))
    # Mínimas: retira as que têm uma combinação mais pequena com os mesmos cursos abertos.
    minimas = [
        (combo, abre) for combo, abre in candidatas
        if not any(outra < combo and set(a.chave for a in abre) <= set(o.chave for o in outros)
                   for outra, outros in candidatas)
    ]
    minimas.sort(key=lambda par: (-len(par[1]), len(par[0]), -len(par[0] & feitos), sorted(par[0])))
    resultado, vistos = [], set()
    for combo, abre in minimas:
        chaves = frozenset(c.chave for c in abre)
        if chaves in vistos:              # outra combinação abre exatamente os mesmos cursos
            continue
        vistos.add(chaves)
        resultado.append(Combinacao(
            tuple(sorted(combo)), abre, tuple(c for c in com_regras if c.chave not in chaves),
            tuple(sorted(combo & feitos)),
        ))
        if len(resultado) == limite:
            break
    return resultado


# -- Plano B: 2.ª fase (23/10) ----------------------------------------------------------------------

def chega_na_2a_fase(curso: Curso, notas: Notas) -> Simulacao | None:
    """A simulação, se em 2025 o curso teve vagas na 2.ª fase e a nota da pessoa chegava ao último
    colocado dessa fase (ou, sem essa nota, se sobraram vagas e a pessoa cumpre os mínimos)."""
    if not curso.vagas_2fase:
        return None
    simulacao = simular(curso, notas)
    if not simulacao.situacao.conta or simulacao.nota is None:
        return None
    referencia = curso.ultimo_colocado_2fase_numero
    if referencia is None:
        sobraram = curso.colocados_2fase is not None and curso.colocados_2fase < curso.vagas_2fase
        return simulacao if sobraram else None
    return simulacao if simulacao.nota >= referencia else None
