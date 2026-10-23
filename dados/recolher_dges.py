"""Recolha do catálogo completo de licenciaturas a partir do site público da DGES (US04).

O site da DGES não tem exportação em massa: cada curso tem uma página própria
(«Guia da Candidatura»). Este script descarrega essas páginas devagar (1 pedido por
segundo), guarda-as tal como vieram em ``dados/dges_html/`` (fora do Git) e só depois
as lê. Assim, se for interrompido, retoma onde parou, e ler as páginas outra vez não
volta a pedir nada ao site.

Corre no computador de um dos membros da equipa (precisa de acesso à internet):

    python dados/recolher_dges.py amostra       # 2 índices e 5 cursos, ~10 segundos
    python dados/recolher_dges.py mvp           # só os ~30 cursos do MVP, ~1 minuto
    python dados/recolher_dges.py descarregar   # todos os cursos, cerca de 1 hora
    python dados/recolher_dges.py processar     # lê as páginas guardadas e escreve o CSV

``processar`` escreve ``dados/catalogo-cursos.csv`` com as colunas de
``catalogo-cursos-mvp.csv`` e, desde 23/10, as condições de acesso (provas de ingresso,
fórmula e classificações mínimas) usadas no plano de candidatura. Os cursos que já estão no ficheiro do MVP mantêm a
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
ESPERA = 2.0   # segundos entre pedidos, para não sobrecarregar o site da DGES
PAUSAS = (10, 30, 60)   # segundos de espera antes de cada nova tentativa, quando o site não responde
PAUSA_LONGA = 120       # depois de vários cursos seguidos com erro, o site pode estar a travar pedidos
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
    for tentativa in range(len(PAUSAS) + 1):
        try:
            conteudo = _pedir(endereco)
            break
        except urllib.error.HTTPError as erro:
            if erro.code < 500 or tentativa == len(PAUSAS):   # 4xx não melhora a tentar outra vez
                raise
            print(f"  erro ({erro.code}); nova tentativa daqui a {PAUSAS[tentativa]} s")
            time.sleep(PAUSAS[tentativa])
        except OSError as erro:   # sem ligação, tempo esgotado, ligação cortada (inclui URLError)
            if tentativa == len(PAUSAS):
                raise
            print(f"  o site não respondeu; nova tentativa daqui a {PAUSAS[tentativa]} s")
            time.sleep(PAUSAS[tentativa])
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
    except OSError as erro:
        print(f"  ! curso {codc}-{code}: sem resposta ({type(erro).__name__}); fica de fora por agora")
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


def mvp() -> None:
    """Descarrega só as páginas dos cursos do MVP (dados/catalogo-cursos-mvp.csv): cerca de 30 pedidos.

    Serve para ter as condições de acesso destes cursos sem esperar pela recolha completa.
    """
    with open(MVP, encoding="utf-8-sig", newline="") as ficheiro:
        pares = [(l["codigo_curso_dges"], l["codigo_instituicao_dges"]) for l in csv.DictReader(ficheiro)]
    for codc, code in pares:
        estado = curso(codc, code)
        print(f"  curso {codc}-{code}: {'descarregado' if estado else 'já estava guardado' if estado is False else 'falhou'}")
    print("\nAgora corra: python dados/recolher_dges.py processar")


def descarregar() -> None:
    pares: list[tuple[str, str]] = []
    for letra in letras_existentes():
        try:
            encontrados = indice(letra)
        except OSError as erro:
            print(f"Índice {letra}: sem resposta ({type(erro).__name__}); fica de fora")
            continue
        print(f"Índice {letra}: {len(encontrados)} cursos")
        pares += encontrados
    pares = list(dict.fromkeys(pares))
    em_falta = sum(1 for codc, code in pares if not (PASTA / "cursos" / f"{codc}-{code}.html").exists())
    print(f"\n{len(pares)} cursos no total, {em_falta} por descarregar. Um de 2 em 2 segundos; pode interromper com Ctrl+C e retomar.")
    novos, falhados, seguidos = 0, 0, 0
    for numero, (codc, code) in enumerate(pares, 1):
        resultado = curso(codc, code)
        novos += resultado is True
        falhados += resultado is None
        seguidos = seguidos + 1 if resultado is None else 0
        if seguidos == 3:
            print(f"  3 cursos seguidos sem resposta: pausa de {PAUSA_LONGA // 60} minutos antes de continuar")
            time.sleep(PAUSA_LONGA)
            seguidos = 0
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
# Código e nome de cada prova de ingresso, como a DGES os escreve («18», «Português»).
PROVAS = Path(__file__).resolve().parent / "provas-ingresso.csv"
COLUNAS = [
    "instituicao", "unidade_organica", "tipo_ensino", "localidade", "codigo_instituicao_dges",
    "codigo_curso_dges", "curso", "area_optabem", "grau", "duracao_semestres", "ects", "vagas_2026",
    "ultimo_colocado_1fase_2025", "area_cnaef", "descricao", "saidas_profissionais",
    "fonte_dados_acesso", "fonte_descricao",
    # Condições de acesso (plano de candidatura, 23/10): ver ``_provas_ingresso``.
    "provas_ingresso", "peso_secundario", "peso_provas", "minimo_candidatura", "minimo_provas",
    "pre_requisitos",
    # Tendência e procura (23/10), da tabela «Dados Estatísticos de Candidaturas Anteriores», 1.ª fase.
    "ultimo_colocado_1fase_2023", "ultimo_colocado_1fase_2024",
    "vagas_1fase_2025", "candidatos_1fase_2025", "candidatos_1opcao_1fase_2025", "colocados_1fase_2025",
]
# Graus que entram no catálogo (o índice da DGES escreve-os entre parênteses retos).
GRAUS = {"Lic-1º cic": "Licenciatura (1.º ciclo)", "Mest Integ": "Mestrado integrado"}

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


def _seccao(pagina: str, titulo: str) -> str:
    """O HTML entre «<h2>titulo</h2>» e o título seguinte (ou a âncora seguinte)."""
    encontrado = re.search(r"<h2>" + re.escape(titulo) + r"</h2>(.*?)(?:<h2>|<a name)", pagina, re.S)
    return encontrado.group(1) if encontrado else ""


_PROVA = re.compile(r"^(\d{2})\s+\S")
_ESCOLHER = {"Uma das seguintes provas:": 1, "Duas das seguintes provas:": 2}


def _combinacoes(lista: list[str], quantas: int) -> list[list[str]]:
    from itertools import combinations
    return [list(c) for c in combinations(lista, quantas)]


def _provas_ingresso(pagina: str) -> str:
    """As provas de ingresso como conjuntos alternativos: «09|18|17+18» quer dizer «Geografia, ou
    Português, ou Matemática Aplicada às Ciências Sociais e Português». Basta um conjunto.

    A DGES escreve-as de quatro formas, todas convertidas para conjuntos:
    - «Um dos seguintes conjuntos:» e conjuntos separados por «ou»;
    - uma lista simples (são precisas todas);
    - «Duas das seguintes provas:» (todos os pares possíveis);
    - «18 Português e Uma das seguintes provas: …» (Português com cada uma das outras).
    Devolve "" quando a página manda consultar a instituição.
    """
    linhas = [_texto(l) for l in _seccao(pagina, "Provas de Ingresso").split("<br>")]
    linhas = [l for l in linhas if l]
    if not linhas or not any(_PROVA.match(l) for l in linhas):
        return ""
    if linhas[0] == "Um dos seguintes conjuntos:":
        conjuntos, atual = [], []
        for linha in linhas[1:] + ["ou"]:
            if linha == "ou":
                if atual:
                    conjuntos.append(atual)
                atual = []
            elif _PROVA.match(linha):
                atual.append(linha[:2])
    else:
        # Partes separadas por «e»; cada parte é obrigatória (todas as provas) ou «escolher N de».
        partes, atual, escolher = [], [], 0
        for linha in linhas + ["e"]:
            if linha == "e":
                if atual:
                    partes.append(_combinacoes(atual, escolher) if escolher else [atual])
                atual, escolher = [], 0
            elif linha in _ESCOLHER:
                escolher = _ESCOLHER[linha]
            elif _PROVA.match(linha):
                atual.append(linha[:2])
        conjuntos = [[]]
        for opcoes in partes:
            conjuntos = [c + o for c in conjuntos for o in opcoes]
    vistos, unicos = set(), []
    for conjunto in conjuntos:
        chave = "+".join(sorted(set(conjunto)))
        if chave and chave not in vistos:
            vistos.add(chave)
            unicos.append(chave)
    return "|".join(unicos)


def nomes_das_provas(pagina: str) -> dict[str, str]:
    """Código -> nome das provas de ingresso da página («18  Português» -> {"18": "Português"})."""
    linhas = [_texto(l) for l in _seccao(pagina, "Provas de Ingresso").split("<br>")]
    return {l[:2]: l[2:].strip() for l in linhas if _PROVA.match(l)}


def _pontos(texto: str, nome: str) -> str:
    """«Nota de candidatura: 95 pontos» ou «Média do secundário: 50%» -> «95» / «50»."""
    encontrado = re.search(re.escape(nome) + r":\s*(\d+)", _texto(texto))
    return encontrado.group(1) if encontrado else ""


def _pre_requisitos(pagina: str) -> str:
    """«Tipo: Seleção<br>Grupo A - Comunicação interpessoal» -> «Seleção: Grupo A - Comunicação interpessoal»."""
    seccao = _seccao(pagina, "Pré-Requisitos")
    if not seccao:
        return ""
    tipo = re.search(r"Tipo:\s*([^<]*)", seccao)
    # «Grupo - -» é a forma de a DGES dizer que não há grupo: não conta.
    grupos = [_texto(g) for g in re.findall(r"<span class='vislink'>(.*?)</span>", seccao, re.S)]
    grupos = [g for g in grupos if re.search(r"[A-Za-zÀ-ú]{2}", g.replace("Grupo", ""))]
    inicio = _texto(tipo.group(1)) if tipo else ""
    if not inicio and not grupos:
        return ""
    return (inicio or "Pré-requisito") + (": " + "; ".join(grupos) if grupos else "")


def estatisticas_1fase(pagina: str) -> dict[str, dict[int, str]]:
    """Linha da tabela de estatísticas -> {ano: valor da 1.ª fase}.

    As linhas «Candidatos» e «Colocados» aparecem duas vezes (o título do grupo, vazio, e o total):
    fica a que tem números. «em 1ª Opção» também aparece duas vezes: a 1.ª é dos candidatos, a 2.ª
    dos colocados (guardadas como «em 1ª Opção» e «colocados em 1ª Opção»).
    """
    tabela = re.search(r"Dados Estatísticos de Candidaturas Anteriores</h2>(.*?)</table>", pagina, re.S)
    if not tabela:
        return {}
    anos = [int(a) for a in re.findall(r'<th colspan="2" class="th1">(\d{4})</th>', tabela.group(1))]
    linhas: dict[str, dict[int, str]] = {}
    for linha in re.findall(r"<tr>(.*?)</tr>", tabela.group(1), re.S):
        celulas = [_texto(c) for c in re.findall(r"<t[hd][^>]*>(.*?)</t[hd]>", linha, re.S)]
        if len(celulas) < 1 + 2 * len(anos) or not anos:
            continue
        nome, valores = celulas[0], celulas[1:]
        primeira_fase = {ano: valores[2 * i] for i, ano in enumerate(anos)}
        if not any(primeira_fase.values()):
            continue                       # título de grupo («Candidatos», «Colocados»)
        if nome in linhas:
            nome = "colocados " + nome     # o 2.º «em 1ª Opção» é dos colocados
        linhas[nome] = primeira_fase
    return linhas


def _numero(valor: str) -> str:
    """«138,3» ou «46» como estão; tudo o resto (vazio, «-») -> ""."""
    return valor if re.fullmatch(r"\d+(,\d)?", valor or "") else ""


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
    cidade = _texto(encontrado.group(1)).lower()
    pequenas = ("a", "de", "do", "da", "dos", "das", "e")

    def maiuscula(palavra: str, primeira: bool) -> str:
        return palavra if palavra in pequenas and not primeira else palavra.capitalize()

    # «IDANHA-A-NOVA» -> «Idanha-a-Nova»; «SÃO MAMEDE DE INFESTA» -> «São Mamede de Infesta»
    return " ".join(
        "-".join(maiuscula(parte, i == 0 and j == 0) for j, parte in enumerate(palavra.split("-")))
        for i, palavra in enumerate(cidade.split())
    )


# Nomes de instituições que têm « - » no próprio nome: não se partem.
NOMES_COM_TRACO = ("Iscte - Instituto Universitário de Lisboa",)


def _instituicao(nome: str) -> tuple[str, str]:
    """«Universidade do Porto - Faculdade de Letras» -> («Universidade do Porto», «Faculdade de Letras»)."""
    for inteiro in NOMES_COM_TRACO:
        if nome.lower().startswith(inteiro.lower()):   # a DGES escreve «ISCTE» e «Iscte»
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
        "provas_ingresso": _provas_ingresso(pagina),
        "peso_secundario": _pontos(_seccao(pagina, "Fórmula de Cálculo"), "Média do secundário"),
        "peso_provas": _pontos(_seccao(pagina, "Fórmula de Cálculo"), "Provas de ingresso"),
        "minimo_candidatura": _pontos(_seccao(pagina, "Classificações Mínimas"), "Nota de candidatura"),
        "minimo_provas": _pontos(_seccao(pagina, "Classificações Mínimas"), "Provas de ingresso"),
        "pre_requisitos": _pre_requisitos(pagina),
        **_tendencia_e_procura(pagina),
    }


def _tendencia_e_procura(pagina: str) -> dict[str, str]:
    linhas = estatisticas_1fase(pagina)
    ultimo = linhas.get("Nota de Candidatura do Último Colocado pelo Contingente Geral", {})
    return {
        "ultimo_colocado_1fase_2023": _numero(ultimo.get(2023, "")),
        "ultimo_colocado_1fase_2024": _numero(ultimo.get(2024, "")),
        "vagas_1fase_2025": _numero(linhas.get("Vagas", {}).get(2025, "")),
        "candidatos_1fase_2025": _numero(linhas.get("Candidatos", {}).get(2025, "")),
        "candidatos_1opcao_1fase_2025": _numero(linhas.get("em 1ª Opção", {}).get(2025, "")),
        "colocados_1fase_2025": _numero(linhas.get("Colocados", {}).get(2025, "")),
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
    equipa: dict[str, dict[str, str]] = {}
    if MVP.exists():
        with open(MVP, encoding="utf-8-sig", newline="") as ficheiro:
            for linha in csv.DictReader(ficheiro):
                equipa[f"{linha['codigo_curso_dges']}-{linha['codigo_instituicao_dges']}"] = linha
    linhas, ignorados = [], {}
    provas: dict[str, str] = {}
    if PROVAS.exists():
        with open(PROVAS, encoding="utf-8-sig", newline="") as ficheiro:
            provas = {l["codigo"]: l["nome"] for l in csv.DictReader(ficheiro)}
    for pagina_html in sorted((PASTA / "cursos").glob("*.html")):
        codc, code = pagina_html.stem.split("-", 1)
        grau = graus.get(codc, "")
        if grau and grau not in GRAUS:
            ignorados[grau] = ignorados.get(grau, 0) + 1
            continue
        texto = pagina_html.read_text(encoding="latin-1")
        provas.update(nomes_das_provas(texto))
        linha = ler_curso(texto, codc, code)
        da_equipa = equipa.get(f"{codc}-{code}")
        if da_equipa:   # o que a equipa escreveu e verificou à mão tem prioridade
            # A área não: é a mesma regra para todos, para os filtros serem coerentes.
            for coluna in ("instituicao", "unidade_organica", "localidade", "descricao",
                           "saidas_profissionais", "fonte_descricao"):
                linha[coluna] = da_equipa[coluna]
        linhas.append(linha)
        equipa.pop(f"{codc}-{code}", None)
    # Os cursos do MVP cujas páginas ainda não foram descarregadas ficam como estavam (com a área
    # pela mesma regra), para o catálogo nunca perder cursos a meio de uma recolha.
    for da_equipa in equipa.values():
        linha = {coluna: da_equipa.get(coluna, "") for coluna in COLUNAS}
        linha["area_optabem"] = _area(linha["curso"], linha["area_cnaef"])
        linhas.append(linha)
    linhas.sort(key=lambda l: (l["curso"], l["instituicao"], l["unidade_organica"]))
    with open(SAIDA, "w", encoding="utf-8-sig", newline="") as ficheiro:
        escritor = csv.DictWriter(ficheiro, fieldnames=COLUNAS)
        escritor.writeheader()
        escritor.writerows(linhas)
    with open(PROVAS, "w", encoding="utf-8-sig", newline="") as ficheiro:
        escritor = csv.writer(ficheiro)
        escritor.writerow(["codigo", "nome"])
        escritor.writerows(sorted(provas.items()))
    sem_nota = sum(1 for l in linhas if not l["ultimo_colocado_1fase_2025"])
    sem_provas = sum(1 for l in linhas if not l.get("provas_ingresso"))
    com_descricao = sum(1 for l in linhas if l["descricao"])
    print(f"{len(linhas)} cursos em {SAIDA.name} ({com_descricao} com descrição; {sem_nota} sem nota do último colocado; "
          f"{sem_provas} sem provas de ingresso).")
    if ignorados:
        print("Fora do catálogo (outros graus): " + ", ".join(f"{g}: {n}" for g, n in sorted(ignorados.items())))


if __name__ == "__main__":
    acoes = {"amostra": amostra, "mvp": mvp, "descarregar": descarregar, "processar": processar}
    if len(sys.argv) != 2 or sys.argv[1] not in acoes:
        print(__doc__)
        sys.exit(1)
    acoes[sys.argv[1]]()
