"""Leitura do catálogo de cursos a partir do CSV da DGES (dados/catalogo-cursos-mvp.csv).

Só este ficheiro sabe de onde vêm os cursos. A US04 vai trocá-lo por consultas à base de
dados, com a mesma função ``todos`` (padrão Repository).
"""
from __future__ import annotations

import csv
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path


@dataclass(frozen=True)
class Curso:
    codigo_instituicao: str
    codigo_curso: str
    curso: str
    instituicao: str
    unidade_organica: str
    localidade: str
    tipo_ensino: str
    area: str
    vagas: int | None
    ultimo_colocado: str | None   # nota de candidatura, como a DGES a escreve (ex.: «138,3»)
    descricao: str
    saidas: str
    fonte: str                    # página da DGES com os dados de acesso
    # Ficha completa (US05). Têm valores por omissão para quem cria um Curso à mão.
    grau: str = ""
    duracao_semestres: int | None = None
    ects: int | None = None
    area_cnaef: str = ""          # área de estudo oficial (CNAEF), ex.: «481 Ciências informáticas»
    fonte_descricao: str = ""     # página da instituição de onde veio a descrição
    # Condições de acesso (plano de candidatura, 23/10). ``provas``: conjuntos alternativos de
    # códigos de provas de ingresso; basta ter um conjunto. Vazio = a DGES não as publica.
    provas: tuple[tuple[str, ...], ...] = ()
    peso_secundario: int | None = None    # % da média do secundário na nota de candidatura
    peso_provas: int | None = None        # % das provas de ingresso
    minimo_candidatura: int | None = None # pontos (0 a 200)
    minimo_provas: int | None = None      # pontos (0 a 200), em cada prova
    pre_requisitos: str = ""
    # Tendência e procura (23/10): 1.ª fase, contingente geral (tabela de estatísticas da DGES).
    ultimo_colocado_2023: str | None = None
    ultimo_colocado_2024: str | None = None
    vagas_1fase: int | None = None          # vagas da 1.ª fase de 2025 (as de 2026 estão em ``vagas``)
    candidatos: int | None = None           # candidatos na 1.ª fase de 2025 (em qualquer opção)
    candidatos_1opcao: int | None = None    # dos quais, com este curso em 1.ª opção
    colocados: int | None = None            # colocados na 1.ª fase de 2025
    # Plano B (23/10): 2.ª fase de 2025.
    vagas_2fase: int | None = None
    colocados_2fase: int | None = None
    ultimo_colocado_2fase: str | None = None

    @property
    def ultimo_colocado_2fase_numero(self) -> float | None:
        try:
            return float(self.ultimo_colocado_2fase.replace(",", ".")) if self.ultimo_colocado_2fase else None
        except ValueError:
            return None

    @property
    def ultimo_colocado_numero(self) -> float | None:
        """A nota do último colocado como número («138,3» -> 138.3)."""
        try:
            return float(self.ultimo_colocado.replace(",", ".")) if self.ultimo_colocado else None
        except ValueError:
            return None

    @property
    def historico(self) -> list[tuple[int, float]]:
        """Nota do último colocado (1.ª fase) por ano, só dos anos com valor: [(2023, 152.0), …]."""
        anos = ((2023, self.ultimo_colocado_2023), (2024, self.ultimo_colocado_2024), (2025, self.ultimo_colocado))
        return [(ano, float(v.replace(",", "."))) for ano, v in anos if v]

    @property
    def tendencia(self) -> str | None:
        """«sobe», «desce» ou «estavel», comparando o ano mais recente com o mais antigo (3 pontos de margem)."""
        historico = self.historico
        if len(historico) < 2:
            return None
        diferenca = historico[-1][1] - historico[0][1]
        return "sobe" if diferenca >= 3 else "desce" if diferenca <= -3 else "estavel"

    @property
    def procura(self) -> str | None:
        """Procura na 1.ª fase de 2025: «sobraram» (ficaram vagas por preencher), «muita» (1,5 ou mais
        candidatos em 1.ª opção por vaga), «media» (0,75 a 1,5) ou «pouca». ``None`` sem dados."""
        if not self.vagas_1fase or self.colocados is None or self.candidatos_1opcao is None:
            return None
        if self.colocados < self.vagas_1fase:
            return "sobraram"
        por_vaga = self.candidatos_1opcao / self.vagas_1fase
        return "muita" if por_vaga >= 1.5 else "media" if por_vaga >= 0.75 else "pouca"

    @property
    def tem_condicoes_de_acesso(self) -> bool:
        return bool(self.provas) and self.peso_secundario is not None and self.peso_provas is not None

    @property
    def lista_saidas(self) -> list[str]:
        """As saídas profissionais, que o CSV separa com «;», cada uma a começar por maiúscula
        (no CSV só a primeira tem maiúscula: «Finanças e banca; consultoria…»)."""
        return [s.strip()[:1].upper() + s.strip()[1:] for s in self.saidas.split(";") if s.strip()]

    @property
    def chave(self) -> str:
        return f"{self.codigo_instituicao}-{self.codigo_curso}"


def _inteiro(valor: str) -> int | None:
    valor = (valor or "").strip()
    return int(valor) if valor.isdigit() else None


def _conjuntos(valor: str) -> tuple[tuple[str, ...], ...]:
    """«09|17+18» -> (("09",), ("17", "18"))."""
    return tuple(tuple(p for p in c.split("+") if p) for c in (valor or "").split("|") if c.strip())


@lru_cache(maxsize=4)
def _ler(caminho: str, modificado: float) -> tuple[Curso, ...]:
    with open(caminho, encoding="utf-8-sig", newline="") as ficheiro:
        linhas = list(csv.DictReader(ficheiro))
    return tuple(
        Curso(
            codigo_instituicao=l["codigo_instituicao_dges"].strip(),
            codigo_curso=l["codigo_curso_dges"].strip(),
            curso=l["curso"].strip(),
            instituicao=l["instituicao"].strip(),
            unidade_organica=l["unidade_organica"].strip(),
            localidade=l["localidade"].strip(),
            tipo_ensino=l["tipo_ensino"].strip(),
            area=l["area_optabem"].strip(),
            vagas=_inteiro(l["vagas_2026"]),
            ultimo_colocado=l["ultimo_colocado_1fase_2025"].strip() or None,
            descricao=l["descricao"].strip(),
            saidas=l["saidas_profissionais"].strip(),
            fonte=l["fonte_dados_acesso"].strip(),
            grau=(l.get("grau") or "").strip(),
            duracao_semestres=_inteiro(l.get("duracao_semestres", "")),
            ects=_inteiro(l.get("ects", "")),
            area_cnaef=(l.get("area_cnaef") or "").strip(),
            fonte_descricao=(l.get("fonte_descricao") or "").strip(),
            provas=_conjuntos(l.get("provas_ingresso", "")),
            peso_secundario=_inteiro(l.get("peso_secundario", "")),
            peso_provas=_inteiro(l.get("peso_provas", "")),
            minimo_candidatura=_inteiro(l.get("minimo_candidatura", "")),
            minimo_provas=_inteiro(l.get("minimo_provas", "")),
            pre_requisitos=(l.get("pre_requisitos") or "").strip(),
            ultimo_colocado_2023=(l.get("ultimo_colocado_1fase_2023") or "").strip() or None,
            ultimo_colocado_2024=(l.get("ultimo_colocado_1fase_2024") or "").strip() or None,
            vagas_1fase=_inteiro(l.get("vagas_1fase_2025", "")),
            candidatos=_inteiro(l.get("candidatos_1fase_2025", "")),
            candidatos_1opcao=_inteiro(l.get("candidatos_1opcao_1fase_2025", "")),
            colocados=_inteiro(l.get("colocados_1fase_2025", "")),
            vagas_2fase=_inteiro(l.get("vagas_2fase_2025", "")),
            colocados_2fase=_inteiro(l.get("colocados_2fase_2025", "")),
            ultimo_colocado_2fase=(l.get("ultimo_colocado_2fase_2025") or "").strip() or None,
        )
        for l in linhas
        if l.get("curso", "").strip()
    )


def todos(caminho: str | Path) -> tuple[Curso, ...]:
    """Todos os cursos do ficheiro. Volta a ler o ficheiro se ele for alterado."""
    caminho = Path(caminho)
    if not caminho.exists():
        return ()
    return _ler(str(caminho), caminho.stat().st_mtime)


def nomes_das_provas(caminho_catalogo: str | Path) -> dict[str, str]:
    """Código -> nome das provas de ingresso (dados/provas-ingresso.csv, ao lado do catálogo)."""
    caminho = Path(caminho_catalogo).with_name("provas-ingresso.csv")
    if not caminho.exists():
        return {}
    return dict(_ler_provas(str(caminho), caminho.stat().st_mtime))


@lru_cache(maxsize=2)
def _ler_provas(caminho: str, modificado: float) -> tuple[tuple[str, str], ...]:
    with open(caminho, encoding="utf-8-sig", newline="") as ficheiro:
        return tuple((l["codigo"].strip(), l["nome"].strip()) for l in csv.DictReader(ficheiro) if l.get("codigo"))
