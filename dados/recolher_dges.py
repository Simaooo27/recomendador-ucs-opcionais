"""Recolha do catálogo completo de licenciaturas a partir do site público da DGES (US04).

O site da DGES não tem exportação em massa: cada curso tem uma página própria
(«Guia da Candidatura»). Este script descarrega essas páginas devagar (1 pedido por
segundo), guarda-as tal como vieram em ``dados/dges_html/`` (fora do Git) e só depois
as lê. Assim, se for interrompido, retoma onde parou, e ler as páginas outra vez não
volta a pedir nada ao site.

Corre no computador de um dos membros da equipa (precisa de acesso à internet):

    python dados/recolher_dges.py amostra       # 2 índices e 5 cursos, ~10 segundos
    python dados/recolher_dges.py descarregar   # todos os cursos, 20 a 30 minutos
    python dados/recolher_dges.py processar     # lê as páginas guardadas e escreve o CSV

``processar`` escreve ``dados/catalogo-cursos.csv`` com as mesmas colunas de
``catalogo-cursos-mvp.csv``. Os cursos que já estão no ficheiro do MVP mantêm a
instituição, a área, a descrição e as saídas escritas pela equipa; os outros ficam
com os dados da DGES e sem descrição.

Só usa a biblioteca padrão do Python (não é preciso instalar nada).
"""
from __future__ import annotations

import csv
import html
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
        except urllib.error.HTTPError as erro:
            if erro.code < 500 or tentativa == 2:   # 4xx não melhora a tentar outra vez
                raise
            print(f"  erro ({erro}); nova tentativa daqui a 5 s")
            time.sleep(5)
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


def letras_existentes() -> list[str]:
    """As letras que têm índice no site (lidas das ligações do índice A). A DGES não tem índice
    para algumas letras (K, U, W, …) e responde com erro 500 se forem pedidas."""
    conteudo, _ = _guardar(PASTA / "indices" / "A.html", f"{BASE}indcurso.asp?letra=A")
    letras = re.findall(r"indcurso\.asp\?letra=([A-Z])", conteudo.decode("latin-1"))
    return sorted(set(letras) | {"A"}) or list(string.ascii_uppercase)


def curso(codc: str, code: str) -> bool | None:
    """Descarrega a página de um curso. True se foi pedida ao site, False se já estava guardada,
    None se o site deu erro (fica registado e a recolha continua)."""
    try:
        _, pedida = _guardar(PASTA / "cursos" / f"{codc}-{code}.html", f"{BASE}detcursopi.asp?codc={codc}&code={code}")
    except urllib.error.URLError as erro:
        print(f"  ! curso {codc}-{code}: {erro} (fica de fora; volte a correr para tentar outra vez)")
        return None
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
    for letra in letras_existentes():
        try:
            encontrados = indice(letra)
        except urllib.error.URLError as erro:
            print(f"Índice {letra}: erro ({erro}); fica de fora")
            continue
        print(f"Índice {letra}: {len(encontrados)} cursos")
        pares += encontrados
    pares = list(dict.fromkeys(pares))
    print(f"\n{len(pares)} cursos no total. A descarregar (1 por segundo; pode interromper com Ctrl+C e retomar).")
    novos, falhados = 0, 0
    for numero, (codc, code) in enumerate(pares, 1):
        resultado = curso(codc, code)
        novos += resultado is True
        falhados += resultado is None
        if numero % 50 == 0 or numero == len(pares):
            print(f"  {numero}/{len(pares)} ({novos} descarregados agora)")
    print(f"\nFeito. Páginas em {PASTA}")
    if falhados:
        print(f"{falhados} cursos deram erro: volte a correr «descarregar» para tentar só esses.")


# ---------------------------------------------------------------------------
# Leitura das páginas guardadas
# ---------------------------------------------------------------------------

MVP = Path(__file__).resolve().parent / "catalogo-cursos-mvp.csv"
SAIDA = Path(__file__).resolve().parent / "catalogo-cursos.csv"
COLUNAS = [
    "instituicao", "unidade_organica", "tipo_ensino", "localidade", "codigo_instituicao_dges",
    "codigo_curso_dges", "curso", "area_optabem", "grau", "duracao_semestres", "ects", "vagas_2026",
    "ultimo_colocado_1fase_2025", "area_cnaef", "descricao", "saidas_profissionais",
    "fonte_dados_acesso", "fonte_descricao",
]
# Graus que entram no catálogo (o índice da DGES escreve-os entre parênteses retos).
GRAUS = {"Lic-1º cic": "Licenciatura (1.º ciclo)", "MI": "Mestrado integrado"}

# Áreas do OptaBem: os dois primeiros algarismos da área CNAEF (grandes grupos de formação).
AREAS_CNAEF = {
    "14": "Educação", "21": "Artes", "22": "Humanidades", "31": "Ciências sociais",
    "32": "Comunicação e jornalismo", "34": "Gestão", "38": "Direito",
    "42": "Ciências da vida", "44": "Ciências físicas", "46": "Matemática e estatística",
    "48": "Informática", "52": "Engenharia", "54": "Indústria e produção",
    "58": "Arquitetura e construção", "62": "Agricultura e pescas", "64": "Veterinária",
    "72": "Saúde", "76": "Serviços sociais", "81": "Turismo, desporto e serviços",
    "84": "Transportes", "85": "Ambiente", "86": "Segurança",
}
# Subgrupos que ficam com área própria (os nomes das três áreas do MVP mantêm-se).
AREAS_CNAEF_DETALHE = {"322": "Ciência da Informação"}
# Cursos de informática que a CNAEF põe noutros grupos (ex.: Engenharia Informática em
# «523 Eletrónica e Automação»): ficam em «Informática» para os filtros fazerem sentido.
PALAVRAS_INFORMATICA = ("informática", "computadores", "computação", "software", "sistemas de informação",
                        "ciência de dados", "inteligência artificial", "cibersegurança")


def _texto(fragmento: str) -> str:
    """HTML para texto simples: tira as etiquetas e junta os espaços."""
    sem_etiquetas = re.sub(r"<[^>]+>", " ", fragmento)
    return re.sub(r"\s+", " ", html.unescape(sem_etiquetas)).strip()


def _campo(pagina: str, nome: str) -> str:
    """Valor de uma linha «Nome: valor<br>» das características do curso."""
    encontrado = re.search(re.escape(nome) + r":\s*(.*?)<br", pagina, re.S)
    return _texto(encontrado.group(1)) if encontrado else ""


def _div(pagina: str, classe: str) -> str:
    encontrado = re.search(r'<div class="' + classe + r'">(.*?)</div>', pagina, re.S)
    return _texto(encontrado.group(1)) if encontrado else ""


def _ultimo_colocado(pagina: str) -> str:
    """Nota do último colocado, contingente geral, 1.ª fase do ano mais recente da tabela."""
    linha = re.search(r"Nota de Candidatura do Último Colocado pelo Contingente Geral</th>(.*?)</tr>", pagina, re.S)
    if not linha:
        return ""
    celulas = [_texto(c) for c in re.findall(r"<td[^>]*>(.*?)</td>", linha.group(1), re.S)]
    anos = re.findall(r'<th colspan="2" class="th1">(\d{4})</th>', pagina)
    if len(celulas) < 2 or not anos:
        return ""
    primeira_fase = celulas[2 * (len(anos) - 1)] if len(celulas) >= 2 * len(anos) else ""
    return primeira_fase if re.fullmatch(r"\d{2,3},\d", primeira_fase) else ""


def _tipo_ensino(texto: str) -> str:
    """«Ensino Superior Público Universitário» -> «Público universitário»; sem «Público» é privado."""
    publico = "Público" if "Público" in texto else "Privado"
    if "Politécnico" in texto:
        return f"{publico} politécnico"
    return f"{publico} universitário" if "Universit" in texto else publico


def _localidade(pagina: str) -> str:
    """A cidade do código postal da morada («3810-193 AVEIRO» -> «Aveiro»)."""
    encontrado = re.search(r"\b\d{4}-\d{3}\s+([^<]+)<br", pagina)
    if not encontrado:
        return ""
    cidade = _texto(encontrado.group(1))
    return " ".join(p if p in ("de", "do", "da", "dos", "das", "e") else p.capitalize() for p in cidade.lower().split())


# Nomes de instituições que têm « - » no próprio nome: não se partem.
NOMES_COM_TRACO = ("Iscte - Instituto Universitário de Lisboa",)


def _instituicao(nome: str) -> tuple[str, str]:
    """«Universidade do Porto - Faculdade de Letras» -> («Universidade do Porto», «Faculdade de Letras»)."""
    for inteiro in NOMES_COM_TRACO:
        if nome.startswith(inteiro):
            resto = nome[len(inteiro):].lstrip(" -")
            return inteiro, resto
    if " - " in nome:
        instituicao, unidade = nome.split(" - ", 1)
        return instituicao.strip(), unidade.strip()
    return nome.strip(), ""


# Cursos de gestão da informação e documentação ficam em «Ciência da Informação» (como no MVP).
PALAVRAS_CIENCIA_INFORMACAO = ("gestão de informação", "gestão da informação", "documentação", "ciência da informação")


def _area(curso: str, area_cnaef: str) -> str:
    if any(p in curso.lower() for p in PALAVRAS_CIENCIA_INFORMACAO):
        return "Ciência da Informação"
    if any(p in curso.lower() for p in PALAVRAS_INFORMATICA):
        return "Informática"
    if area_cnaef[:3] in AREAS_CNAEF_DETALHE:
        return AREAS_CNAEF_DETALHE[area_cnaef[:3]]
    return AREAS_CNAEF.get(area_cnaef[:2], area_cnaef.split(" ", 1)[-1] if area_cnaef else "")


def ler_curso(pagina: str, codc: str, code: str) -> dict[str, str]:
    instituicao, unidade = _instituicao(_div(pagina, "cab2"))
    curso = _div(pagina, "cab1")
    area_cnaef = _campo(pagina, "Área CNAEF")
    duracao_texto = _campo(pagina, "Duração")
    duracao = re.search(r"(\d+)", duracao_texto)
    semestres = int(duracao.group(1)) * (2 if "Ano" in duracao_texto else 1) if duracao else None
    grau = _campo(pagina, "Grau")
    return {
        "instituicao": instituicao,
        "unidade_organica": unidade,
        "tipo_ensino": _tipo_ensino(_campo(pagina, "Tipo de Ensino")),
        "localidade": _localidade(pagina),
        "codigo_instituicao_dges": code,
        "codigo_curso_dges": codc,
        "curso": curso,
        "area_optabem": _area(curso, area_cnaef),
        "grau": "Mestrado integrado" if "Integrado" in grau else ("Licenciatura (1.º ciclo)" if "Licenciatura" in grau else grau),
        "duracao_semestres": str(semestres) if semestres else "",
        "ects": _campo(pagina, "ECTS"),
        "vagas_2026": re.sub(r"\D", "", _campo(pagina, "Vagas para 2026-2027")),
        "ultimo_colocado_1fase_2025": _ultimo_colocado(pagina),
        "area_cnaef": area_cnaef,
        "descricao": "",
        "saidas_profissionais": "",
        "fonte_dados_acesso": f"{BASE}detcursopi.asp?codc={codc}&code={code}",
        "fonte_descricao": "",
    }


def graus_do_indice(texto: str) -> dict[str, str]:
    """Código do curso -> grau abreviado, a partir das caixas do índice («[Lic-1º cic]»)."""
    graus = {}
    for codc, grau in re.findall(r"<div class='lin-area-c1'>([^<]+)</div><div class='lin-area-c2'>[^<]*</div><div class='lin-area-c3'>\[([^\]]+)\]", texto):
        graus[codc.strip().upper()] = grau.strip()
    return graus


def processar() -> None:
    graus: dict[str, str] = {}
    for indice_html in sorted((PASTA / "indices").glob("*.html")):
        graus.update(graus_do_indice(indice_html.read_text(encoding="latin-1")))
    equipa = {}
    if MVP.exists():
        with open(MVP, encoding="utf-8-sig", newline="") as ficheiro:
            for linha in csv.DictReader(ficheiro):
                equipa[f"{linha['codigo_curso_dges']}-{linha['codigo_instituicao_dges']}"] = linha
    linhas, ignorados = [], {}
    for pagina_html in sorted((PASTA / "cursos").glob("*.html")):
        codc, code = pagina_html.stem.split("-", 1)
        grau = graus.get(codc, "")
        if grau and grau not in GRAUS:
            ignorados[grau] = ignorados.get(grau, 0) + 1
            continue
        linha = ler_curso(pagina_html.read_text(encoding="latin-1"), codc, code)
        da_equipa = equipa.get(f"{codc}-{code}")
        if da_equipa:   # o que a equipa escreveu e verificou à mão tem prioridade
            # A área não: é a mesma regra para todos, para os filtros serem coerentes.
            for coluna in ("instituicao", "unidade_organica", "localidade", "descricao",
                           "saidas_profissionais", "fonte_descricao"):
                linha[coluna] = da_equipa[coluna]
        linhas.append(linha)
    linhas.sort(key=lambda l: (l["curso"], l["instituicao"], l["unidade_organica"]))
    with open(SAIDA, "w", encoding="utf-8-sig", newline="") as ficheiro:
        escritor = csv.DictWriter(ficheiro, fieldnames=COLUNAS)
        escritor.writeheader()
        escritor.writerows(linhas)
    sem_nota = sum(1 for l in linhas if not l["ultimo_colocado_1fase_2025"])
    print(f"{len(linhas)} cursos em {SAIDA.name} ({len(equipa)} do MVP com descrição; {sem_nota} sem nota do último colocado).")
    if ignorados:
        print("Fora do catálogo (outros graus): " + ", ".join(f"{g}: {n}" for g, n in sorted(ignorados.items())))


if __name__ == "__main__":
    acoes = {"amostra": amostra, "descarregar": descarregar, "processar": processar}
    if len(sys.argv) != 2 or sys.argv[1] not in acoes:
        print(__doc__)
        sys.exit(1)
    acoes[sys.argv[1]]()
