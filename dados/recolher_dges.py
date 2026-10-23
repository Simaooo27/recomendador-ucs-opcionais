"""Recolha do catálogo completo de licenciaturas a partir do site público da DGES (US04).

O site da DGES não tem exportação em massa: cada curso tem uma página própria
(«Guia da Candidatura»). Este script descarrega essas páginas devagar (1 pedido por
segundo), guarda-as tal como vieram em ``dados/dges_html/`` (fora do Git) e só depois
as lê. Assim, se for interrompido, retoma onde parou, e ler as páginas outra vez não
volta a pedir nada ao site.

Corre no computador de um dos membros da equipa (precisa de acesso à internet):

    python dados/recolher_dges.py amostra       # 2 índices e 5 cursos, ~10 segundos
    python dados/recolher_dges.py descarregar   # todos os cursos, 20 a 30 minutos

Só usa a biblioteca padrão do Python (não é preciso instalar nada).
"""
from __future__ import annotations

import re
import string
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

BASE = "https://www.dges.gov.pt/guias/"
PASTA = Path(__file__).resolve().parent / "dges_html"
ESPERA = 1.0   # segundos entre pedidos, para não sobrecarregar o site da DGES
CABECALHOS = {
    # Identifica o pedido como um trabalho académico, com contacto do projeto.
    "User-Agent": "OptaBem/1.0 (projeto academico ISCAP; https://github.com/Simaooo27/recomendador-ucs-opcionais)",
}
# Ligações para a página de um curso: detcursopi.asp?codc=<curso>&code=<instituição>
LIGACAO_CURSO = re.compile(r"detcursopi\.asp\?codc=([A-Za-z0-9]+)&(?:amp;)?code=([0-9]+)", re.I)


def _pedir(endereco: str) -> bytes:
    pedido = urllib.request.Request(endereco, headers=CABECALHOS)
    with urllib.request.urlopen(pedido, timeout=30) as resposta:
        return resposta.read()


def _guardar(caminho: Path, endereco: str, forcar: bool = False) -> tuple[bytes, bool]:
    """Devolve o conteúdo da página e se foi preciso pedi-la (False = já estava guardada)."""
    if caminho.exists() and not forcar:
        return caminho.read_bytes(), False
    for tentativa in range(3):
        try:
            conteudo = _pedir(endereco)
            break
        except (urllib.error.URLError, TimeoutError) as erro:
            if tentativa == 2:
                raise
            print(f"  erro ({erro}); nova tentativa daqui a 5 s")
            time.sleep(5)
    caminho.parent.mkdir(parents=True, exist_ok=True)
    caminho.write_bytes(conteudo)
    time.sleep(ESPERA)
    return conteudo, True


def indice(letra: str) -> list[tuple[str, str]]:
    """Pares (código do curso, código da instituição) que aparecem no índice de uma letra."""
    conteudo, _ = _guardar(PASTA / "indices" / f"{letra}.html", f"{BASE}indcurso.asp?letra={letra}")
    texto = conteudo.decode("latin-1")   # só se procuram códigos: a codificação exata não importa aqui
    vistos: dict[tuple[str, str], None] = {}
    for codc, code in LIGACAO_CURSO.findall(texto):
        vistos[(codc.upper(), code)] = None
    return list(vistos)


def curso(codc: str, code: str) -> bool:
    """Descarrega a página de um curso. Devolve True se foi preciso pedi-la ao site."""
    _, pedida = _guardar(PASTA / "cursos" / f"{codc}-{code}.html", f"{BASE}detcursopi.asp?codc={codc}&code={code}")
    return pedida


def amostra() -> None:
    pares = []
    for letra in "AG":
        encontrados = indice(letra)
        print(f"Índice {letra}: {len(encontrados)} cursos")
        pares += encontrados
    for codc, code in pares[:5]:
        curso(codc, code)
        print(f"  curso {codc}-{code}")
    print(f"\nAmostra guardada em {PASTA}")


def descarregar() -> None:
    pares: list[tuple[str, str]] = []
    for letra in string.ascii_uppercase:
        encontrados = indice(letra)
        print(f"Índice {letra}: {len(encontrados)} cursos")
        pares += encontrados
    pares = list(dict.fromkeys(pares))
    print(f"\n{len(pares)} cursos no total. A descarregar (1 por segundo; pode interromper com Ctrl+C e retomar).")
    novos = 0
    for numero, (codc, code) in enumerate(pares, 1):
        if curso(codc, code):
            novos += 1
        if numero % 50 == 0 or numero == len(pares):
            print(f"  {numero}/{len(pares)} ({novos} descarregados agora)")
    print(f"\nFeito. Páginas em {PASTA}")


if __name__ == "__main__":
    acoes = {"amostra": amostra, "descarregar": descarregar}
    if len(sys.argv) != 2 or sys.argv[1] not in acoes:
        print(__doc__)
        sys.exit(1)
    acoes[sys.argv[1]]()
