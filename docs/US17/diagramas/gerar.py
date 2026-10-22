"""Gera docs/US17/diagramas/{bpmn.bpmn, bpmn.svg, use-case.svg} a partir de um só desenho.

Correr: python docs/US17/diagramas/gerar.py docs/US17/diagramas
"""
import sys
from html import escape
from pathlib import Path

DESTINO = Path(sys.argv[1])
DESTINO.mkdir(parents=True, exist_ok=True)

W, H = 1150, 560
POOL_X, LABEL_W, LANE_W = 30, 30, 30
LANES = [("Aluno (com sessão)", 20, 260), ("Sistema (OptaBem)", 260, 540)]
TW, TH = 150, 64  # tarefas
GR, ER = 25, 18   # losango (meia diagonal), evento (raio)

# id: (tipo, cx, cy, nome, faixa)
NOS = {
    "S1": ("start", 125, 110, "Na página inicial", 0),
    "T1": ("task", 260, 110, "Carregar em «Apagar a minha conta e todos os meus dados»", 0),
    "T2": ("task", 260, 380, "Mostrar o que vai ser apagado e pedir a palavra-passe", 1),
    "T3": ("task", 480, 110, "Escrever a palavra-passe e confirmar", 0),
    "G1": ("gateway", 480, 380, "Palavra-passe certa?", 1),
    "T4": ("task", 660, 380, "Apagar a conta, a conversa, as decisões e os pedidos ao LLM", 1),
    "T5": ("task", 840, 380, "Terminar a sessão e avisar na página de apresentação", 1),
    "E1": ("end", 970, 380, "Conta e dados apagados", 1),
    "T6": ("task", 480, 480, "Avisar que a palavra-passe não está certa (nada é apagado)", 1),
    "C1": ("task", 680, 110, "Cancelar e voltar ao início", 0),
    "E2": ("end", 840, 110, "Nada muda", 0),
}


def bx(n, lado):
    t, cx, cy, *_ = NOS[n]
    if t == "task":
        return {"l": (cx - TW / 2, cy), "r": (cx + TW / 2, cy), "t": (cx, cy - TH / 2), "b": (cx, cy + TH / 2)}[lado]
    d = GR if t == "gateway" else ER
    return {"l": (cx - d, cy), "r": (cx + d, cy), "t": (cx, cy - d), "b": (cx, cy + d)}[lado]


# (id, origem, destino, nome, pontos)
FLUXOS = [
    ("F1", "S1", "T1", "", [bx("S1", "r"), bx("T1", "l")]),
    ("F2", "T1", "T2", "", [bx("T1", "b"), bx("T2", "t")]),
    ("F3", "T2", "T3", "", [bx("T2", "r"), (395, 380), (395, 110), bx("T3", "l")]),
    ("F4", "T3", "G1", "", [bx("T3", "b"), bx("G1", "t")]),
    ("F5", "G1", "T4", "sim", [bx("G1", "r"), bx("T4", "l")]),
    ("F6", "G1", "T6", "não", [bx("G1", "b"), bx("T6", "t")]),
    ("F7", "T6", "T3", "", [bx("T6", "l"), (360, 480), (360, 165), (445, 165), (445, 142)]),
    ("F8", "T4", "T5", "", [bx("T4", "r"), bx("T5", "l")]),
    ("F9", "T5", "E1", "", [bx("T5", "r"), bx("E1", "l")]),
    ("F10", "T3", "C1", "ou", [bx("T3", "r"), bx("C1", "l")]),
    ("F11", "C1", "E2", "", [bx("C1", "r"), bx("E2", "l")]),
]


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


# ---------- SVG do BPMN ----------
s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="Arial, Helvetica, sans-serif">',
     "<title>BPMN US17 — Apagar a minha conta</title>",
     '<defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#000"/></marker></defs>',
     f'<rect width="{W}" height="{H}" fill="#fff"/>',
     f'<rect x="{POOL_X}" y="20" width="{W - 50}" height="{H - 40}" fill="none" stroke="#000" stroke-width="2"/>',
     f'<line x1="{POOL_X + LABEL_W}" y1="20" x2="{POOL_X + LABEL_W}" y2="{H - 20}" stroke="#000" stroke-width="2"/>',
     f'<line x1="{POOL_X + LABEL_W + LANE_W}" y1="20" x2="{POOL_X + LABEL_W + LANE_W}" y2="{H - 20}" stroke="#000" stroke-width="1.5"/>',
     f'<text transform="translate(45,{H / 2}) rotate(-90)" text-anchor="middle" dominant-baseline="central" font-size="13" font-weight="700">Apagar a minha conta (US17)</text>']
for nome, y0, y1 in LANES:
    if y0 > 20:
        s.append(f'<line x1="{POOL_X + LABEL_W}" y1="{y0}" x2="{W - 20}" y2="{y0}" stroke="#000" stroke-width="1.5"/>')
    s.append(f'<text transform="translate(75,{(y0 + y1) / 2}) rotate(-90)" text-anchor="middle" dominant-baseline="central" font-size="12" font-weight="700">{escape(nome)}</text>')
for fid, a, b, nome, pts in FLUXOS:
    caminho = " ".join(f"{x:.0f},{y:.0f}" for x, y in pts)
    s.append(f'<polyline points="{caminho}" fill="none" stroke="#000" stroke-width="1.5" marker-end="url(#a)"/>')
    if nome:
        x, y = pts[0]
        if pts[1][0] < x:   # fluxo para a esquerda: o nome fica à esquerda da origem
            s.append(f'<text x="{x - 8}" y="{y - 10}" text-anchor="end" font-size="11" font-style="italic">{escape(nome)}</text>')
        else:
            dx, dy = (8, 14) if pts[1][1] > y else (14, -10)
            s.append(f'<text x="{x + dx}" y="{y + dy}" font-size="11" font-style="italic">{escape(nome)}</text>')
for nid, (tipo, cx, cy, nome, _) in NOS.items():
    if tipo == "task":
        s.append(f'<rect x="{cx - TW / 2}" y="{cy - TH / 2}" width="{TW}" height="{TH}" rx="10" fill="#fff" stroke="#000" stroke-width="1.5"/>')
        s.append(texto_svg(cx, cy, nome, 22, 12))
    elif tipo == "gateway":
        s.append(f'<polygon points="{cx},{cy - GR} {cx + GR},{cy} {cx},{cy + GR} {cx - GR},{cy}" fill="#fff" stroke="#000" stroke-width="1.5"/>')
        s.append(f'<text x="{cx}" y="{cy}" text-anchor="middle" dominant-baseline="central" font-size="16" font-weight="700">×</text>')
        s.append(texto_svg(cx + GR + 6, cy - GR - 14, nome, 24, 11, ancora="start"))   # ao lado, para não tapar os fluxos
    else:
        largura = 3.5 if tipo == "end" else 1.5
        s.append(f'<circle cx="{cx}" cy="{cy}" r="{ER}" fill="#fff" stroke="#000" stroke-width="{largura}"/>')
        if nid in ("E1", "E2"):
            s.append(texto_svg(cx + ER + 8, cy, nome, 22, 11, ancora="start"))
        else:
            n_linhas = len(linhas(nome, 12))
            s.append(texto_svg(cx, cy + ER + 12 + (n_linhas - 1) * 7, nome, 12, 11))   # por baixo, sem tocar no círculo
s.append("</svg>")
(DESTINO / "bpmn.svg").write_text("".join(s), encoding="utf-8")

# ---------- BPMN 2.0 (editável) ----------
TAG = {"start": "startEvent", "end": "endEvent", "task": "task", "gateway": "exclusiveGateway"}
x = ['<?xml version="1.0" encoding="UTF-8"?>',
     '<bpmn:definitions xmlns:bpmn="http://www.omg.org/spec/BPMN/20100524/MODEL" xmlns:bpmndi="http://www.omg.org/spec/BPMN/20100524/DI" '
     'xmlns:dc="http://www.omg.org/spec/DD/20100524/DC" xmlns:di="http://www.omg.org/spec/DD/20100524/DI" id="Definitions_US17" targetNamespace="http://bpmn.io/schema/bpmn">',
     '  <bpmn:collaboration id="Collaboration_US17">',
     '    <bpmn:participant id="Participant_US17" name="Apagar a minha conta (US17)" processRef="Process_US17" />',
     "  </bpmn:collaboration>",
     '  <bpmn:process id="Process_US17" isExecutable="false">',
     '    <bpmn:laneSet id="LaneSet_US17">']
for i, (nome, *_r) in enumerate(LANES):
    x.append(f'      <bpmn:lane id="Lane_US17_{i}" name="{escape(nome)}">')
    x += [f"        <bpmn:flowNodeRef>{n}</bpmn:flowNodeRef>" for n, v in NOS.items() if v[4] == i]
    x.append("      </bpmn:lane>")
x.append("    </bpmn:laneSet>")
for nid, (tipo, *_r, nome, _f) in NOS.items():
    x.append(f'    <bpmn:{TAG[tipo]} id="{nid}" name="{escape(nome)}">')
    x += [f"      <bpmn:incoming>{f[0]}</bpmn:incoming>" for f in FLUXOS if f[2] == nid]
    x += [f"      <bpmn:outgoing>{f[0]}</bpmn:outgoing>" for f in FLUXOS if f[1] == nid]
    x.append(f"    </bpmn:{TAG[tipo]}>")
for fid, a, b, nome, _p in FLUXOS:
    x.append(f'    <bpmn:sequenceFlow id="{fid}" name="{escape(nome)}" sourceRef="{a}" targetRef="{b}" />')
x += ["  </bpmn:process>", '  <bpmndi:BPMNDiagram id="Diagram_US17">', '    <bpmndi:BPMNPlane id="Plane_US17" bpmnElement="Collaboration_US17">',
      f'      <bpmndi:BPMNShape id="Participant_US17_di" bpmnElement="Participant_US17" isHorizontal="true"><dc:Bounds x="{POOL_X}" y="20" width="{W - 50}" height="{H - 40}" /></bpmndi:BPMNShape>']
for i, (nome, y0, y1) in enumerate(LANES):
    x.append(f'      <bpmndi:BPMNShape id="Lane_US17_{i}_di" bpmnElement="Lane_US17_{i}" isHorizontal="true"><dc:Bounds x="{POOL_X + LABEL_W}" y="{y0}" width="{W - 50 - LABEL_W}" height="{y1 - y0}" /></bpmndi:BPMNShape>')
for nid, (tipo, cx, cy, *_r) in NOS.items():
    w, h = (TW, TH) if tipo == "task" else ((2 * GR, 2 * GR) if tipo == "gateway" else (2 * ER, 2 * ER))
    marcador = ' isMarkerVisible="true"' if tipo == "gateway" else ""
    x.append(f'      <bpmndi:BPMNShape id="{nid}_di" bpmnElement="{nid}"{marcador}><dc:Bounds x="{cx - w / 2:.0f}" y="{cy - h / 2:.0f}" width="{w}" height="{h}" /></bpmndi:BPMNShape>')
for fid, _a, _b, _n, pts in FLUXOS:
    x.append(f'      <bpmndi:BPMNEdge id="{fid}_di" bpmnElement="{fid}">' + "".join(f'<di:waypoint x="{px:.0f}" y="{py:.0f}" />' for px, py in pts) + "</bpmndi:BPMNEdge>")
x += ["    </bpmndi:BPMNPlane>", "  </bpmndi:BPMNDiagram>", "</bpmn:definitions>", ""]
(DESTINO / "bpmn.bpmn").write_text("\n".join(x), encoding="utf-8")

# ---------- Use case ----------
UW, UH = 900, 330
u = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {UW} {UH}" width="{UW}" height="{UH}" font-family="Arial, Helvetica, sans-serif">',
     "<title>Use case US17</title>",
     '<defs><marker id="o" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="9" markerHeight="9" orient="auto"><path d="M1,1 L9,5 L1,9" fill="none" stroke="#000" stroke-width="1.5"/></marker></defs>',
     f'<rect width="{UW}" height="{UH}" fill="#fff"/>',
     '<rect x="230" y="28" width="600" height="270" rx="8" fill="#fff" stroke="#000" stroke-width="2"/>',
     texto_svg(530, 52, "Sistema: OptaBem", 60, 14, 700)]


def ator(cx, cy, nome):
    return (f'<g stroke="#000" stroke-width="2.4" fill="none"><circle cx="{cx}" cy="{cy}" r="20"/><line x1="{cx}" y1="{cy + 20}" x2="{cx}" y2="{cy + 78}"/>'
            f'<line x1="{cx - 38}" y1="{cy + 42}" x2="{cx + 38}" y2="{cy + 42}"/><line x1="{cx}" y1="{cy + 78}" x2="{cx - 32}" y2="{cy + 120}"/>'
            f'<line x1="{cx}" y1="{cy + 78}" x2="{cx + 32}" y2="{cy + 120}"/></g>' + texto_svg(cx, cy + 148, nome, 16, 14, 700))


u.append(ator(110, 110, "Aluno (com sessão)"))
CASOS = {"UC20": (400, 190, "UC20 Apagar a minha conta"), "INC": (680, 190, "Confirmar com a palavra-passe")}
for _k, (cx, cy, nome) in CASOS.items():
    u.append(f'<ellipse cx="{cx}" cy="{cy}" rx="115" ry="40" fill="#fff" stroke="#000" stroke-width="2"/>' + texto_svg(cx, cy, nome, 20, 13))
u.append('<line x1="150" y1="170" x2="285" y2="190" stroke="#000" stroke-width="1.5"/>')
u.append('<line x1="515" y1="190" x2="563" y2="190" stroke="#000" stroke-width="1.5" stroke-dasharray="6 4" marker-end="url(#o)"/>')
u.append('<text x="512" y="178" font-size="11" font-style="italic">«include»</text>')
u.append("</svg>")
(DESTINO / "use-case.svg").write_text("".join(u), encoding="utf-8")
print("diagramas gerados em", DESTINO)
