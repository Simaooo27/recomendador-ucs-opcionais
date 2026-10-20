"""Gera docs/US31/diagramas/{bpmn.bpmn, bpmn.svg, use-case.svg} a partir de um só desenho."""
import sys
from html import escape
from pathlib import Path

DESTINO = Path(sys.argv[1])
DESTINO.mkdir(parents=True, exist_ok=True)

W, H = 1400, 700
POOL_X, LABEL_W, LANE_W = 30, 30, 30
LANES = [("Aluno", 20, 260), ("Sistema (OptaBem)", 260, 680)]
TW, TH = 150, 64  # tarefas
GR, ER = 25, 18   # losango (meia diagonal), evento (raio)

# id: (tipo, cx, cy, nome, faixa)
NOS = {
    "S1": ("start", 140, 150, "Vê os cursos sugeridos (US30) ou o catálogo", 0),
    "T1": ("task", 290, 150, "Carregar em «Escolher este curso»", 0),
    "T2": ("task", 290, 420, "Mostrar a confirmação (curso atual e aviso sobre a conversa)", 1),
    "G0": ("gateway", 450, 150, "Confirma?", 0),
    "E0": ("end", 570, 150, "Volta sem escolher", 0),
    "G1": ("gateway", 600, 420, "Já é o curso atual?", 1),
    "TE": ("task", 600, 560, "Avisar que já é o seu curso", 1),
    "E2": ("end", 760, 560, "Sem decisão nova", 1),
    "T4": ("task", 780, 420, "Registar a decisão: data, sugeridos, escolhido e origem", 1),
    "T5": ("task", 960, 420, "Apagar a conversa com o LLM (ponto 15)", 1),
    "T6": ("task", 1120, 420, "Mostrar a linha do tempo", 1),
    "T7": ("task", 1120, 150, "Ver as decisões (mais recente primeiro)", 0),
    "E1": ("end", 1255, 150, "Curso no perfil (RF03)", 0),
}

ROTULO_DIREITA = {"E0", "E1", "E2"}


# (id, origem, destino, nome, pontos)
def bx(n, lado):
    t, cx, cy, *_ = NOS[n]
    if t == "task":
        return {"l": (cx - TW / 2, cy), "r": (cx + TW / 2, cy), "t": (cx, cy - TH / 2), "b": (cx, cy + TH / 2)}[lado]
    d = GR if t == "gateway" else ER
    return {"l": (cx - d, cy), "r": (cx + d, cy), "t": (cx, cy - d), "b": (cx, cy + d)}[lado]


FLUXOS = [
    ("F1", "S1", "T1", "", [bx("S1", "r"), bx("T1", "l")]),
    ("F2", "T1", "T2", "", [bx("T1", "b"), bx("T2", "t")]),
    ("F3", "T2", "G0", "", [bx("T2", "r"), (395, 420), (395, 150), bx("G0", "l")]),
    ("F4", "G0", "E0", "não", [bx("G0", "r"), bx("E0", "l")]),
    ("F5", "G0", "G1", "sim", [bx("G0", "b"), (450, 420), bx("G1", "l")]),
    ("F6", "G1", "TE", "sim", [bx("G1", "b"), bx("TE", "t")]),
    ("F7", "TE", "E2", "", [bx("TE", "r"), bx("E2", "l")]),
    ("F8", "G1", "T4", "não", [bx("G1", "r"), bx("T4", "l")]),
    ("F9", "T4", "T5", "", [bx("T4", "r"), bx("T5", "l")]),
    ("F10", "T5", "T6", "", [bx("T5", "r"), bx("T6", "l")]),
    ("F11", "T6", "T7", "", [bx("T6", "t"), bx("T7", "b")]),
    ("F12", "T7", "E1", "", [bx("T7", "r"), bx("E1", "l")]),
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
     "<title>BPMN US31 — Escolher curso e linha do tempo</title>",
     '<defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#000"/></marker></defs>',
     f'<rect width="{W}" height="{H}" fill="#fff"/>',
     f'<rect x="{POOL_X}" y="20" width="{W - 50}" height="660" fill="none" stroke="#000" stroke-width="2"/>',
     f'<line x1="{POOL_X + LABEL_W}" y1="20" x2="{POOL_X + LABEL_W}" y2="680" stroke="#000" stroke-width="2"/>',
     f'<line x1="{POOL_X + LABEL_W + LANE_W}" y1="20" x2="{POOL_X + LABEL_W + LANE_W}" y2="680" stroke="#000" stroke-width="1.5"/>',
     f'<text transform="translate(45,350) rotate(-90)" text-anchor="middle" dominant-baseline="central" font-size="13" font-weight="700">Escolher curso (US31)</text>']
for nome, y0, y1 in LANES:
    if y0 > 20:
        s.append(f'<line x1="{POOL_X + LABEL_W}" y1="{y0}" x2="{W - 20}" y2="{y0}" stroke="#000" stroke-width="1.5"/>')
    s.append(f'<text transform="translate(75,{(y0 + y1) / 2}) rotate(-90)" text-anchor="middle" dominant-baseline="central" font-size="12" font-weight="700">{escape(nome)}</text>')
for fid, a, b, nome, pts in FLUXOS:
    caminho = " ".join(f"{x:.0f},{y:.0f}" for x, y in pts)
    s.append(f'<polyline points="{caminho}" fill="none" stroke="#000" stroke-width="1.5" marker-end="url(#a)"/>')
    if nome:
        x, y = pts[0]
        dx, dy = (8, 14) if pts[1][1] > y else (14, -10)
        s.append(f'<text x="{x + dx}" y="{y + dy}" font-size="11" font-style="italic">{escape(nome)}</text>')
for nid, (tipo, cx, cy, nome, _) in NOS.items():
    if tipo == "task":
        s.append(f'<rect x="{cx - TW / 2}" y="{cy - TH / 2}" width="{TW}" height="{TH}" rx="10" fill="#fff" stroke="#000" stroke-width="1.5"/>')
        s.append(texto_svg(cx, cy, nome, 22, 12))
    elif tipo == "gateway":
        s.append(f'<polygon points="{cx},{cy - GR} {cx + GR},{cy} {cx},{cy + GR} {cx - GR},{cy}" fill="#fff" stroke="#000" stroke-width="1.5"/>')
        s.append(f'<text x="{cx}" y="{cy}" text-anchor="middle" dominant-baseline="central" font-size="16" font-weight="700">×</text>')
        s.append(texto_svg(cx, cy - GR - 16, nome, 24, 11))
    else:
        largura = 3.5 if tipo == "end" else 1.5
        s.append(f'<circle cx="{cx}" cy="{cy}" r="{ER}" fill="#fff" stroke="#000" stroke-width="{largura}"/>')
        if nid in ROTULO_DIREITA:
            s.append(texto_svg(cx + ER + 8, cy, nome, 16, 11, ancora="start"))
        else:
            s.append(texto_svg(cx, cy + ER + 22, nome, 18, 11))
s.append("</svg>")
(DESTINO / "bpmn.svg").write_text("".join(s), encoding="utf-8")

# ---------- BPMN 2.0 (editável) ----------
TAG = {"start": "startEvent", "end": "endEvent", "task": "task", "gateway": "exclusiveGateway"}
x = ['<?xml version="1.0" encoding="UTF-8"?>',
     '<bpmn:definitions xmlns:bpmn="http://www.omg.org/spec/BPMN/20100524/MODEL" xmlns:bpmndi="http://www.omg.org/spec/BPMN/20100524/DI" '
     'xmlns:dc="http://www.omg.org/spec/DD/20100524/DC" xmlns:di="http://www.omg.org/spec/DD/20100524/DI" id="Definitions_US31" targetNamespace="http://bpmn.io/schema/bpmn">',
     '  <bpmn:collaboration id="Collaboration_US31">',
     '    <bpmn:participant id="Participant_US31" name="Escolher curso (US31)" processRef="Process_US31" />',
     "  </bpmn:collaboration>",
     '  <bpmn:process id="Process_US31" isExecutable="false">',
     '    <bpmn:laneSet id="LaneSet_US31">']
for i, (nome, *_r) in enumerate(LANES):
    x.append(f'      <bpmn:lane id="Lane_US31_{i}" name="{escape(nome)}">')
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
x += ["  </bpmn:process>", '  <bpmndi:BPMNDiagram id="Diagram_US31">', '    <bpmndi:BPMNPlane id="Plane_US31" bpmnElement="Collaboration_US31">',
      f'      <bpmndi:BPMNShape id="Participant_US31_di" bpmnElement="Participant_US31" isHorizontal="true"><dc:Bounds x="{POOL_X}" y="20" width="{W - 50}" height="660" /></bpmndi:BPMNShape>']
for i, (nome, y0, y1) in enumerate(LANES):
    x.append(f'      <bpmndi:BPMNShape id="Lane_US31_{i}_di" bpmnElement="Lane_US31_{i}" isHorizontal="true"><dc:Bounds x="{POOL_X + LABEL_W}" y="{y0}" width="{W - 50 - LABEL_W}" height="{y1 - y0}" /></bpmndi:BPMNShape>')
for nid, (tipo, cx, cy, *_r) in NOS.items():
    w, h = (TW, TH) if tipo == "task" else ((2 * GR, 2 * GR) if tipo == "gateway" else (2 * ER, 2 * ER))
    marcador = ' isMarkerVisible="true"' if tipo == "gateway" else ""
    x.append(f'      <bpmndi:BPMNShape id="{nid}_di" bpmnElement="{nid}"{marcador}><dc:Bounds x="{cx - w / 2:.0f}" y="{cy - h / 2:.0f}" width="{w}" height="{h}" /></bpmndi:BPMNShape>')
for fid, _a, _b, _n, pts in FLUXOS:
    x.append(f'      <bpmndi:BPMNEdge id="{fid}_di" bpmnElement="{fid}">' + "".join(f'<di:waypoint x="{px:.0f}" y="{py:.0f}" />' for px, py in pts) + "</bpmndi:BPMNEdge>")
x += ["    </bpmndi:BPMNPlane>", "  </bpmndi:BPMNDiagram>", "</bpmn:definitions>", ""]
(DESTINO / "bpmn.bpmn").write_text("\n".join(x), encoding="utf-8")

# ---------- Use case ----------
UW, UH = 1000, 560
u = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {UW} {UH}" width="{UW}" height="{UH}" font-family="Arial, Helvetica, sans-serif">',
     "<title>Use case US31</title>",
     '<defs><marker id="o" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="9" markerHeight="9" orient="auto"><path d="M1,1 L9,5 L1,9" fill="none" stroke="#000" stroke-width="1.5"/></marker></defs>',
     f'<rect width="{UW}" height="{UH}" fill="#fff"/>',
     '<rect x="230" y="28" width="560" height="500" rx="8" fill="#fff" stroke="#000" stroke-width="2"/>',
     texto_svg(510, 52, "Sistema: OptaBem", 60, 14, 700)]

def ator(cx, cy, nome):
    return (f'<g stroke="#000" stroke-width="2.4" fill="none"><circle cx="{cx}" cy="{cy}" r="20"/><line x1="{cx}" y1="{cy + 20}" x2="{cx}" y2="{cy + 78}"/>'
            f'<line x1="{cx - 38}" y1="{cy + 42}" x2="{cx + 38}" y2="{cy + 42}"/><line x1="{cx}" y1="{cy + 78}" x2="{cx - 32}" y2="{cy + 120}"/>'
            f'<line x1="{cx}" y1="{cy + 78}" x2="{cx + 32}" y2="{cy + 120}"/></g>' + texto_svg(cx, cy + 148, nome, 16, 14, 700))

u.append(ator(110, 190, "Aluno"))
CASOS = {"UC14": (400, 140, "UC14 Escolher um curso"), "UC15": (400, 290, "UC15 Ver a linha do tempo das decisões"),
         "UC16": (400, 430, "UC16 Mudar de curso"), "INC1": (640, 220, "Confirmar a escolha (RN10)"),
         "INC2": (640, 380, "Registar a decisão e apagar a conversa")}
for _k, (cx, cy, nome) in CASOS.items():
    u.append(f'<ellipse cx="{cx}" cy="{cy}" rx="110" ry="38" fill="#fff" stroke="#000" stroke-width="2"/>' + texto_svg(cx, cy, nome, 20, 13))
for cx, cy in ((290, 140), (290, 290), (290, 430)):
    u.append(f'<line x1="150" y1="250" x2="{cx}" y2="{cy}" stroke="#000" stroke-width="1.5"/>')
for (x1, y1), (x2, y2), (lx, ly) in (((505, 155), (545, 200), (532, 172)), ((470, 172), (575, 345), (545, 285)),
                                    ((505, 420), (560, 410), (500, 448))):
    u.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#000" stroke-width="1.5" stroke-dasharray="6 4" marker-end="url(#o)"/>')
    u.append(f'<text x="{lx}" y="{ly}" font-size="11" font-style="italic">«include»</text>')
u.append("</svg>")
(DESTINO / "use-case.svg").write_text("".join(u), encoding="utf-8")
print("diagramas gerados em", DESTINO)
