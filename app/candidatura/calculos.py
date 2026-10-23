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

from dataclasses import dataclass, field
from enum import Enum
from typing import Mapping

from ..catalogo.repository import Curso

# Diferença (em pontos, de 0 a 200) para o último colocado abaixo da qual a situação é «perto».
MARGEM = 5.0

# Provas que a DGES lista com dois códigos e que se fazem com o mesmo exame nacional:
# quem indica a nota de uma, tem-na na outra. A CONFIRMAR pela equipa no site da DGES.
EQUIVALENTES = {"16": "19"}


class Situacao(str, Enum):
    ACIMA = "acima"                   # nota ≥ último colocado + margem
    PERTO = "perto"                   # a menos de MARGEM pontos do último colocado
    ABAIXO = "abaixo"                 # mais de MARGEM pontos abaixo
    SEM_REFERENCIA = "sem_referencia" # cumpre os mínimos, mas o curso não tem nota do último colocado
    ABAIXO_DO_MINIMO = "abaixo_do_minimo"
    FALTA_PROVA = "falta_prova"       # não tem nenhum conjunto de provas completo
    SEM_NOTAS = "sem_notas"           # o aluno ainda não indicou a média do secundário
    SEM_REGRAS = "sem_regras"         # a DGES não publica as condições deste curso

    @property
    def conta(self) -> bool:
        """True se a opção pode dar colocação (cumpre provas e mínimos)."""
        return self in (Situacao.ACIMA, Situacao.PERTO, Situacao.ABAIXO, Situacao.SEM_REFERENCIA)


@dataclass(frozen=True)
class Notas:
    media: float | None = None                          # média do secundário, 0 a 20
    exames: Mapping[str, float] = field(default_factory=dict)   # código da prova -> 0 a 200

    def exame(self, codigo: str) -> float | None:
        if codigo in self.exames:
            return self.exames[codigo]
        for um, outro in EQUIVALENTES.items():
            if codigo == um and outro in self.exames:
                return self.exames[outro]
            if codigo == outro and um in self.exames:
                return self.exames[um]
        return None


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
