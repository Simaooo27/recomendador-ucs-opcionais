"""Texto «escrito à mão»: converte uma palavra em traços SVG que o navegador desenha.

Adaptação do componente HandwritingText (React) ao OptaBem, que não usa React nem pode
carregar bibliotecas de outros sites (política de segurança, app/security.py):

- As letras são convertidas em traços aqui, no servidor, com o fontTools, a partir do
  tipo de letra manuscrito Caveat (app/recursos/caveat-600.ttf, licença OFL).
- Cada contorno é um <path> próprio, para o traço poder avançar letra a letra; por baixo
  fica uma cópia preenchida da palavra inteira, que aparece no fim (a «tinta").
- O movimento está em app/static/app.js e app/static/style.css (secção 11).

Se o fontTools não estiver instalado, ``desenhar`` devolve ``None`` e a página mostra o
texto normal: nunca fica nada em branco.
"""
from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

_FONTE = Path(__file__).parent / "recursos" / "caveat-600.ttf"


@dataclass(frozen=True)
class Desenho:
    viewbox: str                 # "x y largura altura" para o atributo viewBox
    completo: str                # todos os contornos num só caminho (para a tinta)
    contornos: tuple[str, ...]   # um caminho por contorno (para o traço)
    proporcao: float             # largura / altura, para o CSS reservar o espaço certo


def _numero(valor: float) -> str:
    """Coordenadas sem casas decimais: a diferença não se vê e a página fica mais leve."""
    return str(round(valor))


@lru_cache(maxsize=1)
def _fonte():
    from fontTools.ttLib import TTFont

    return TTFont(str(_FONTE))


@lru_cache(maxsize=128)
def desenhar(texto: str) -> Desenho | None:
    """Traços SVG de ``texto`` no tipo de letra manuscrito, ou ``None`` se não for possível."""
    texto = (texto or "").strip()
    if not texto:
        return None
    try:
        from fontTools.pens.boundsPen import BoundsPen
        from fontTools.pens.svgPathPen import SVGPathPen
        from fontTools.pens.transformPen import TransformPen

        fonte = _fonte()
    except (ImportError, OSError):
        return None

    glifos = fonte.getGlyphSet()
    mapa = fonte.getBestCmap()
    larguras = fonte["hmtx"]
    espaco = larguras[mapa.get(32, ".notdef")][0] if 32 in mapa else 200

    caminhos: list[str] = []
    limites = BoundsPen(glifos)
    x = 0.0
    for letra in texto:
        nome = mapa.get(ord(letra))
        if nome is None:  # letra sem desenho no tipo de letra: deixa um espaço
            x += espaco
            continue
        # O SVG tem o eixo y para baixo; o tipo de letra, para cima: inverte-se.
        transformacao = (1, 0, 0, -1, x, 0)
        caneta = SVGPathPen(glifos, _numero)
        glifos[nome].draw(TransformPen(caneta, transformacao))
        glifos[nome].draw(TransformPen(limites, transformacao))
        comandos = caneta.getCommands()
        if comandos:
            caminhos.append(comandos)
        x += larguras[nome][0]

    if not caminhos or limites.bounds is None:
        return None

    contornos = tuple(
        "M" + parte for caminho in caminhos for parte in caminho.split("M") if parte.strip()
    )
    x1, y1, x2, y2 = limites.bounds
    margem = 40  # espaço para a espessura do traço
    largura, altura = x2 - x1 + 2 * margem, y2 - y1 + 2 * margem
    return Desenho(
        viewbox=f"{x1 - margem:.0f} {y1 - margem:.0f} {largura:.0f} {altura:.0f}",
        completo=" ".join(caminhos),
        contornos=contornos,
        proporcao=round(largura / altura, 4),
    )
