"""Gera docs/US36/diagramas/{bpmn.bpmn, bpmn.svg, use-case.svg} a partir de um só desenho.

Correr: python docs/US36/diagramas/gerar.py docs/US36/diagramas
"""
import sys
from html import escape
from pathlib import Path

DESTINO = Path(sys.argv[1])
DESTINO.mkdir(parents=True, exist_ok=True)

US = "US36"
PROCESSO = "Plano das 6 opções de candidatura"
W, H = 1150, 640
POOL_X, LABEL_W, LANE_W = 30, 30, 30
TW, TH = 150, 64  # tarefas
GR, ER = 25, 18   # losango (meia diagonal), evento (raio)

LANES = [("Aluno (com sessão)", 20, 300), ("Sistema (OptaBem)", 300, 620)]

NOS = {
    "S1": ("start", 150, 110, "Carrega em «Juntar ao plano» na ficha", 0, "cima"),
    "G1": ("gateway", 290, 420, "Já está no plano ou já há 6?", 1),
    "T1": ("task", 290, 550, "Avisar que o plano está cheio (ou não mudar nada)", 1),
    "T2": ("task", 480, 420, "Juntar o curso ao fim da lista", 1),
    "T3": ("task", 680, 420, "Mostrar cada opção com a nota e a situação, os avisos e sugestões da mesma área", 1),
    "G2": ("gateway", 680, 110, "Mudar a ordem?", 0),
    "T4": ("task", 480, 210, "Subir, descer ou retirar uma opção", 0),
    "E1": ("end", 900, 110, "Leva a lista para a candidatura no site da DGES", 0, "direita"),
    "E2": ("end", 150, 550, "Volta à ficha", 1, "cima"),
}

FLUXOS = [
    ("F1", "S1", "G1", "", lambda: [bx("S1", "b"), (150, 420), bx("G1", "l")]),
    ("F2", "G1", "T1", "sim", lambda: [bx("G1", "b"), bx("T1", "t")], (296, 470)),
    ("F3", "T1", "E2", "", lambda: [bx("T1", "l"), bx("E2", "r")]),
    ("F4", "G1", "T2", "não", lambda: [bx("G1", "r"), bx("T2", "l")]),
    ("F5", "T2", "T3", "", lambda: [bx("T2", "r"), bx("T3", "l")]),
    ("F6", "T3", "G2", "", lambda: [bx("T3", "t"), bx("G2", "b")]),
    ("F7", "G2", "T4", "sim", lambda: [bx("G2", "l"), (480, 110), bx("T4", "t")], (560, 100)),
    ("F8", "T4", "T3", "", lambda: [bx("T4", "b"), (480, 340), (640, 340), (640, 388)]),
    ("F9", "G2", "E1", "não", lambda: [bx("G2", "r"), bx("E1", "l")]),
]

UW, UH = 1000, 520
ATORES = [(110, 150, "Aluno (com sessão)")]
CASOS = {"UC27": (420, 110, "UC27 Juntar um curso ao plano"), "UC28": (420, 250, "UC28 Ordenar e retirar opções"),
         "UC29": (420, 400, "UC29 Ver o plano com avisos e sugestões"), "UC18": (730, 110, "UC18 Ver a ficha de um curso (US05)")}
ASSOCIACOES = [(0, "UC27"), (0, "UC28"), (0, "UC29")]
RELACOES = [("UC27", "UC18", "«extend»")]


def bx(n, lado):
    t, cx, cy, *_ = NOS[n]
    if t == "task":
        return {"l": (cx - TW / 2, cy), "r": (cx + TW / 2, cy), "t": (cx, cy - TH / 2), "b": (cx, cy + TH / 2)}[lado]
    d = GR if t == "gateway" else ER
    return {"l": (cx - d, cy), "r": (cx + d, cy), "t": (cx, cy - d), "b": (cx, cy + d)}[lado]


def linhas(texto, largura):
    palavras, saida, atual = texto.split(), [], ""
    for p in palavras:
        if len(atual) + len(p) + 1 > largura and atual:
            saida.append(atual); atual = p
        else:
            atual = f"{atual} {p}".strip()
    return saida + [atual]


def texto_svg(x, y, texto, largura=22, tam=12, peso=400, ancora="middle"):
    ls = linhas(texto, largura)
    y0 = y - (len(ls) - 1) * (tam + 3) / 2
    return "".join(
        f'<text x="{x}" y="{y0 + i * (tam + 3):.1f}" text-anchor="{ancora}" dominant-baseline="central" '
        f'font-size="{tam}" font-weight="{peso}" fill="#000">{escape(l)}</text>'
        for i, l in enumerate(ls)
    )


FLUXOS = [(f[0], f[1], f[2], f[3], f[4](), *f[5:]) for f in FLUXOS]

# ---------- SVG do BPMN ----------
s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="Arial, Helvetica, sans-serif">',
     f"<title>BPMN {US} — {escape(PROCESSO)}</title>",
     '<defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#000"/></marker></defs>',
     f'<rect width="{W}" height="{H}" fill="#fff"/>',
     f'<rect x="{POOL_X}" y="20" width="{W - 50}" height="{H - 40}" fill="none" stroke="#000" stroke-width="2"/>',
     f'<line x1="{POOL_X + LABEL_W}" y1="20" x2="{POOL_X + LABEL_W}" y2="{H - 20}" stroke="#000" stroke-width="2"/>',
     f'<line x1="{POOL_X + LABEL_W + LANE_W}" y1="20" x2="{POOL_X + LABEL_W + LANE_W}" y2="{H - 20}" stroke="#000" stroke-width="1.5"/>',
     f'<text transform="translate(45,{H / 2}) rotate(-90)" text-anchor="middle" dominant-baseline="central" font-size="13" font-weight="700">{escape(PROCESSO)} ({US})</text>']
for nome, y0, y1 in LANES:
    if y0 > 20:
        s.append(f'<line x1="{POOL_X + LABEL_W}" y1="{y0}" x2="{W - 20}" y2="{y0}" stroke="#000" stroke-width="1.5"/>')
    s.append(f'<text transform="translate(75,{(y0 + y1) / 2}) rotate(-90)" text-anchor="middle" dominant-baseline="central" font-size="12" font-weight="700">{escape(nome)}</text>')
for fid, a, b, nome, pts, *pos in FLUXOS:
    caminho = " ".join(f"{x:.0f},{y:.0f}" for x, y in pts)
    s.append(f'<polyline points="{caminho}" fill="none" stroke="#000" stroke-width="1.5" marker-end="url(#a)"/>')
    if nome:
        if pos:   # posição do nome escolhida à mão
            s.append(f'<text x="{pos[0][0]}" y="{pos[0][1]}" font-size="11" font-style="italic">{escape(nome)}</text>')
            continue
        x, y = pts[0]
        if pts[1][0] < x:
            s.append(f'<text x="{x - 8}" y="{y - 10}" text-anchor="end" font-size="11" font-style="italic">{escape(nome)}</text>')
        else:
            dx, dy = (8, 14) if pts[1][1] > y else (14, -10)
            s.append(f'<text x="{x + dx}" y="{y + dy}" font-size="11" font-style="italic">{escape(nome)}</text>')
for nid, (tipo, cx, cy, nome, _f, *rotulo) in NOS.items():
    if tipo == "task":
        s.append(f'<rect x="{cx - TW / 2}" y="{cy - TH / 2}" width="{TW}" height="{TH}" rx="10" fill="#fff" stroke="#000" stroke-width="1.5"/>')
        s.append(texto_svg(cx, cy, nome, 22, 12))
    elif tipo == "gateway":
        s.append(f'<polygon points="{cx},{cy - GR} {cx + GR},{cy} {cx},{cy + GR} {cx - GR},{cy}" fill="#fff" stroke="#000" stroke-width="1.5"/>')
        s.append(f'<text x="{cx}" y="{cy}" text-anchor="middle" dominant-baseline="central" font-size="16" font-weight="700">×</text>')
        s.append(texto_svg(cx + GR + 6, cy - GR - 14, nome, 24, 11, ancora="start"))
    else:
        largura = 3.5 if tipo == "end" else 1.5
        s.append(f'<circle cx="{cx}" cy="{cy}" r="{ER}" fill="#fff" stroke="#000" stroke-width="{largura}"/>')
        lado = rotulo[0] if rotulo else "baixo"
        if lado == "direita":
            s.append(texto_svg(cx + ER + 8, cy, nome, 22, 11, ancora="start"))
        elif lado == "esquerda":
            s.append(texto_svg(cx - ER - 8, cy, nome, 22, 11, ancora="end"))
        elif lado == "cima":
            n_linhas = len(linhas(nome, 16))
            s.append(texto_svg(cx, cy - ER - 12 - (n_linhas - 1) * 7, nome, 16, 11))
        else:
            n_linhas = len(linhas(nome, 16))
            s.append(texto_svg(cx, cy + ER + 12 + (n_linhas - 1) * 7, nome, 16, 11))
s.append("</svg>")
(DESTINO / "bpmn.svg").write_text("".join(s), encoding="utf-8")

# ---------- BPMN 2.0 (editável) ----------
TAG = {"start": "startEvent", "end": "endEvent", "task": "task", "gateway": "exclusiveGateway"}
x = ['<?xml version="1.0" encoding="UTF-8"?>',
     '<bpmn:definitions xmlns:bpmn="http://www.omg.org/spec/BPMN/20100524/MODEL" xmlns:bpmndi="http://www.omg.org/spec/BPMN/20100524/DI" '
     f'xmlns:dc="http://www.omg.org/spec/DD/20100524/DC" xmlns:di="http://www.omg.org/spec/DD/20100524/DI" id="Definitions_{US}" targetNamespace="http://bpmn.io/schema/bpmn">',
     f'  <bpmn:collaboration id="Collaboration_{US}">',
     f'    <bpmn:participant id="Participant_{US}" name="{escape(PROCESSO)} ({US})" processRef="Process_{US}" />',
     "  </bpmn:collaboration>",
     f'  <bpmn:process id="Process_{US}" isExecutable="false">',
     f'    <bpmn:laneSet id="LaneSet_{US}">']
for i, (nome, *_r) in enumerate(LANES):
    x.append(f'      <bpmn:lane id="Lane_{US}_{i}" name="{escape(nome)}">')
    x += [f"        <bpmn:flowNodeRef>{n}</bpmn:flowNodeRef>" for n, v in NOS.items() if v[4] == i]
    x.append("      </bpmn:lane>")
x.append("    </bpmn:laneSet>")
for nid, (tipo, _cx, _cy, nome, _f, *_r) in NOS.items():
    x.append(f'    <bpmn:{TAG[tipo]} id="{nid}" name="{escape(nome)}">')
    x += [f"      <bpmn:incoming>{f[0]}</bpmn:incoming>" for f in FLUXOS if f[2] == nid]
    x += [f"      <bpmn:outgoing>{f[0]}</bpmn:outgoing>" for f in FLUXOS if f[1] == nid]
    x.append(f"    </bpmn:{TAG[tipo]}>")
for fid, a, b, nome, *_p in FLUXOS:
    x.append(f'    <bpmn:sequenceFlow id="{fid}" name="{escape(nome)}" sourceRef="{a}" targetRef="{b}" />')
x += ["  </bpmn:process>", f'  <bpmndi:BPMNDiagram id="Diagram_{US}">', f'    <bpmndi:BPMNPlane id="Plane_{US}" bpmnElement="Collaboration_{US}">',
      f'      <bpmndi:BPMNShape id="Participant_{US}_di" bpmnElement="Participant_{US}" isHorizontal="true"><dc:Bounds x="{POOL_X}" y="20" width="{W - 50}" height="{H - 40}" /></bpmndi:BPMNShape>']
for i, (nome, y0, y1) in enumerate(LANES):
    x.append(f'      <bpmndi:BPMNShape id="Lane_{US}_{i}_di" bpmnElement="Lane_{US}_{i}" isHorizontal="true"><dc:Bounds x="{POOL_X + LABEL_W}" y="{y0}" width="{W - 50 - LABEL_W}" height="{y1 - y0}" /></bpmndi:BPMNShape>')
for nid, (tipo, cx, cy, *_r) in NOS.items():
    w, h = (TW, TH) if tipo == "task" else ((2 * GR, 2 * GR) if tipo == "gateway" else (2 * ER, 2 * ER))
    marcador = ' isMarkerVisible="true"' if tipo == "gateway" else ""
    x.append(f'      <bpmndi:BPMNShape id="{nid}_di" bpmnElement="{nid}"{marcador}><dc:Bounds x="{cx - w / 2:.0f}" y="{cy - h / 2:.0f}" width="{w}" height="{h}" /></bpmndi:BPMNShape>')
for fid, _a, _b, _n, pts, *_r in FLUXOS:
    x.append(f'      <bpmndi:BPMNEdge id="{fid}_di" bpmnElement="{fid}">' + "".join(f'<di:waypoint x="{px:.0f}" y="{py:.0f}" />' for px, py in pts) + "</bpmndi:BPMNEdge>")
x += ["    </bpmndi:BPMNPlane>", "  </bpmndi:BPMNDiagram>", "</bpmn:definitions>", ""]
(DESTINO / "bpmn.bpmn").write_text("\n".join(x), encoding="utf-8")

# ---------- Use case ----------
u = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {UW} {UH}" width="{UW}" height="{UH}" font-family="Arial, Helvetica, sans-serif">',
     f"<title>Use case {US}</title>",
     '<defs><marker id="o" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="9" markerHeight="9" orient="auto"><path d="M1,1 L9,5 L1,9" fill="none" stroke="#000" stroke-width="1.5"/></marker></defs>',
     f'<rect width="{UW}" height="{UH}" fill="#fff"/>',
     f'<rect x="230" y="28" width="{UW - 260}" height="{UH - 60}" rx="8" fill="#fff" stroke="#000" stroke-width="2"/>',
     texto_svg(230 + (UW - 260) / 2, 52, "Sistema: OptaBem", 60, 14, 700)]


def ator(cx, cy, nome):
    return (f'<g stroke="#000" stroke-width="2.4" fill="none"><circle cx="{cx}" cy="{cy}" r="20"/><line x1="{cx}" y1="{cy + 20}" x2="{cx}" y2="{cy + 78}"/>'
            f'<line x1="{cx - 38}" y1="{cy + 42}" x2="{cx + 38}" y2="{cy + 42}"/><line x1="{cx}" y1="{cy + 78}" x2="{cx - 32}" y2="{cy + 120}"/>'
            f'<line x1="{cx}" y1="{cy + 78}" x2="{cx + 32}" y2="{cy + 120}"/></g>' + texto_svg(cx, cy + 148, nome, 16, 14, 700))


def borda(caso, para):
    """Ponto da elipse do caso na direção de ``para`` (rx 115, ry 38)."""
    import math
    cx, cy, _n = CASOS[caso]
    ang = math.atan2(para[1] - cy, para[0] - cx)
    t = 1 / math.sqrt((math.cos(ang) / 115) ** 2 + (math.sin(ang) / 38) ** 2)
    return cx + t * math.cos(ang), cy + t * math.sin(ang)


for cx, cy, nome in ATORES:
    u.append(ator(cx, cy, nome))
for _k, (cx, cy, nome) in CASOS.items():
    u.append(f'<ellipse cx="{cx}" cy="{cy}" rx="115" ry="38" fill="#fff" stroke="#000" stroke-width="2"/>' + texto_svg(cx, cy, nome, 20, 13))
for i_ator, caso in ASSOCIACOES:
    ax, ay, _n = ATORES[i_ator]
    mao = (ax + 40, ay + 60)
    x2, y2 = borda(caso, mao)
    u.append(f'<line x1="{mao[0]}" y1="{mao[1]}" x2="{x2:.0f}" y2="{y2:.0f}" stroke="#000" stroke-width="1.5"/>')
for origem, destino, rotulo in RELACOES:
    x1, y1 = borda(origem, CASOS[destino][:2])
    x2, y2 = borda(destino, CASOS[origem][:2])
    u.append(f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" stroke="#000" stroke-width="1.5" stroke-dasharray="6 4" marker-end="url(#o)"/>')
    u.append(f'<text x="{(x1 + x2) / 2 + 6:.0f}" y="{(y1 + y2) / 2 - 12:.0f}" font-size="11" font-style="italic">{escape(rotulo)}</text>')
u.append("</svg>")
(DESTINO / "use-case.svg").write_text("".join(u), encoding="utf-8")
print("diagramas gerados em", DESTINO)
