"""Gera docs/US29/diagramas/{bpmn.bpmn, bpmn.svg, use-case.svg} a partir de um só desenho."""
import sys
from html import escape
from pathlib import Path

DESTINO = Path(sys.argv[1])
DESTINO.mkdir(parents=True, exist_ok=True)

W, H = 1600, 700
POOL_X, LABEL_W, LANE_W = 30, 30, 30
LANES = [("Aluno", 20, 200), ("Sistema (OptaBem)", 200, 530), ("LLM (fornecedor externo)", 530, 680)]
TW, TH = 150, 64  # tarefas
GR, ER = 25, 18   # losango (meia diagonal), evento (raio)

# id: (tipo, cx, cy, nome, faixa)
NOS = {
    "S1": ("start", 130, 110, "Abrir a conversa", 0),
    "T1": ("task", 260, 110, "Carregar em «Começar a conversa»", 0),
    "T2": ("task", 440, 280, "Enviar instruções, catálogo e conversa (sem dados pessoais)", 1),
    "L1": ("task", 440, 605, "Gerar a próxima pergunta ou a sugestão (JSON)", 2),
    "G1": ("gateway", 620, 280, "Resposta válida?", 1),
    "TE": ("task", 620, 390, "Mostrar o erro (a conversa fica guardada)", 1),
    "E2": ("end", 620, 470, "À espera de «Tentar de novo»", 1),
    "G2": ("gateway", 780, 280, "Pergunta ou sugestão?", 1),
    "E1": ("end", 780, 390, "Conversa terminada (cursos na US30)", 1),
    "T3": ("task", 940, 280, "Mostrar a pergunta", 1),
    "T4": ("task", 940, 110, "Escrever a resposta", 0),
    "T5": ("task", 1110, 280, "Validar, apagar emails e números e guardar a resposta", 1),
    "G3": ("gateway", 1280, 280, "6 respostas?", 1),
    "T6": ("task", 1450, 280, "Exigir a sugestão nas instruções", 1),
}

# (id, origem, destino, nome, pontos)
def bx(n, lado):
    t, cx, cy, *_ = NOS[n]
    if t == "task":
        return {"l": (cx - TW / 2, cy), "r": (cx + TW / 2, cy), "t": (cx, cy - TH / 2), "b": (cx, cy + TH / 2)}[lado]
    d = GR if t == "gateway" else ER
    return {"l": (cx - d, cy), "r": (cx + d, cy), "t": (cx, cy - d), "b": (cx, cy + d)}[lado]

LOOP_Y = 510
FLUXOS = [
    ("F1", "S1", "T1", "", [bx("S1", "r"), bx("T1", "l")]),
    ("F2", "T1", "T2", "", [bx("T1", "r"), (440, 110), bx("T2", "t")]),
    ("F3", "T2", "L1", "", [bx("T2", "b"), bx("L1", "t")]),
    ("F4", "L1", "G1", "", [bx("L1", "r"), (540, 605), (540, 280), bx("G1", "l")]),
    ("F5", "G1", "TE", "não", [bx("G1", "b"), bx("TE", "t")]),
    ("F6", "TE", "E2", "", [bx("TE", "b"), bx("E2", "t")]),
    ("F7", "G1", "G2", "sim", [bx("G1", "r"), bx("G2", "l")]),
    ("F8", "G2", "E1", "sugestão", [bx("G2", "b"), bx("E1", "t")]),
    ("F9", "G2", "T3", "pergunta", [bx("G2", "r"), bx("T3", "l")]),
    ("F10", "T3", "T4", "", [bx("T3", "t"), bx("T4", "b")]),
    ("F11", "T4", "T5", "", [bx("T4", "r"), (1110, 110), bx("T5", "t")]),
    ("F12", "T5", "G3", "", [bx("T5", "r"), bx("G3", "l")]),
    ("F13", "G3", "T6", "sim", [bx("G3", "r"), bx("T6", "l")]),
    ("F14", "T6", "T2", "", [bx("T6", "b"), (1450, LOOP_Y), (350, LOOP_Y), (350, 280), bx("T2", "l")]),
    ("F15", "G3", "T2", "não", [bx("G3", "b"), (1280, LOOP_Y), (350, LOOP_Y), (350, 280), bx("T2", "l")]),
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
     "<title>BPMN US29 — Conversa de orientação com o LLM</title>",
     '<defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#000"/></marker></defs>',
     f'<rect width="{W}" height="{H}" fill="#fff"/>',
     f'<rect x="{POOL_X}" y="20" width="{W - 50}" height="660" fill="none" stroke="#000" stroke-width="2"/>',
     f'<line x1="{POOL_X + LABEL_W}" y1="20" x2="{POOL_X + LABEL_W}" y2="680" stroke="#000" stroke-width="2"/>',
     f'<line x1="{POOL_X + LABEL_W + LANE_W}" y1="20" x2="{POOL_X + LABEL_W + LANE_W}" y2="680" stroke="#000" stroke-width="1.5"/>',
     f'<text transform="translate(45,350) rotate(-90)" text-anchor="middle" dominant-baseline="central" font-size="13" font-weight="700">Conversa de orientação (US29)</text>']
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
        if nid == "E2":
            s.append(texto_svg(cx - ER - 8, cy, nome, 18, 11, ancora="end"))
        elif nid == "E1":
            s.append(texto_svg(cx + ER + 60, cy, nome, 18, 11))
        else:
            s.append(texto_svg(cx, cy + ER + 16, nome, 16, 11))
s.append("</svg>")
(DESTINO / "bpmn.svg").write_text("".join(s), encoding="utf-8")

# ---------- BPMN 2.0 (editável) ----------
TAG = {"start": "startEvent", "end": "endEvent", "task": "task", "gateway": "exclusiveGateway"}
x = ['<?xml version="1.0" encoding="UTF-8"?>',
     '<bpmn:definitions xmlns:bpmn="http://www.omg.org/spec/BPMN/20100524/MODEL" xmlns:bpmndi="http://www.omg.org/spec/BPMN/20100524/DI" '
     'xmlns:dc="http://www.omg.org/spec/DD/20100524/DC" xmlns:di="http://www.omg.org/spec/DD/20100524/DI" id="Definitions_US29" targetNamespace="http://bpmn.io/schema/bpmn">',
     '  <bpmn:collaboration id="Collaboration_US29">',
     '    <bpmn:participant id="Participant_US29" name="Conversa de orientação (US29)" processRef="Process_US29" />',
     "  </bpmn:collaboration>",
     '  <bpmn:process id="Process_US29" isExecutable="false">',
     '    <bpmn:laneSet id="LaneSet_US29">']
for i, (nome, *_r) in enumerate(LANES):
    x.append(f'      <bpmn:lane id="Lane_US29_{i}" name="{escape(nome)}">')
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
x += ["  </bpmn:process>", '  <bpmndi:BPMNDiagram id="Diagram_US29">', '    <bpmndi:BPMNPlane id="Plane_US29" bpmnElement="Collaboration_US29">',
      f'      <bpmndi:BPMNShape id="Participant_US29_di" bpmnElement="Participant_US29" isHorizontal="true"><dc:Bounds x="{POOL_X}" y="20" width="{W - 50}" height="660" /></bpmndi:BPMNShape>']
for i, (nome, y0, y1) in enumerate(LANES):
    x.append(f'      <bpmndi:BPMNShape id="Lane_US29_{i}_di" bpmnElement="Lane_US29_{i}" isHorizontal="true"><dc:Bounds x="{POOL_X + LABEL_W}" y="{y0}" width="{W - 50 - LABEL_W}" height="{y1 - y0}" /></bpmndi:BPMNShape>')
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
     "<title>Use case US29</title>",
     '<defs><marker id="o" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="9" markerHeight="9" orient="auto"><path d="M1,1 L9,5 L1,9" fill="none" stroke="#000" stroke-width="1.5"/></marker></defs>',
     f'<rect width="{UW}" height="{UH}" fill="#fff"/>',
     '<rect x="230" y="28" width="560" height="500" rx="8" fill="#fff" stroke="#000" stroke-width="2"/>',
     texto_svg(510, 52, "Sistema: OptaBem", 60, 14, 700)]

def ator(cx, cy, nome):
    return (f'<g stroke="#000" stroke-width="2.4" fill="none"><circle cx="{cx}" cy="{cy}" r="20"/><line x1="{cx}" y1="{cy + 20}" x2="{cx}" y2="{cy + 78}"/>'
            f'<line x1="{cx - 38}" y1="{cy + 42}" x2="{cx + 38}" y2="{cy + 42}"/><line x1="{cx}" y1="{cy + 78}" x2="{cx - 32}" y2="{cy + 120}"/>'
            f'<line x1="{cx}" y1="{cy + 78}" x2="{cx + 32}" y2="{cy + 120}"/></g>' + texto_svg(cx, cy + 148, nome, 16, 14, 700))

u.append(ator(110, 190, "Aluno"))
u.append(ator(895, 190, "LLM (fornecedor externo)"))
CASOS = {"UC08": (400, 140, "UC08 Conversar com o assistente"), "UC09": (400, 290, "UC09 Tentar de novo"),
         "UC10": (400, 430, "UC10 Recomeçar a conversa"), "INC1": (640, 220, "Apagar dados pessoais"),
         "INC2": (640, 360, "Pedir o próximo passo ao LLM")}
for _k, (cx, cy, nome) in CASOS.items():
    u.append(f'<ellipse cx="{cx}" cy="{cy}" rx="110" ry="38" fill="#fff" stroke="#000" stroke-width="2"/>' + texto_svg(cx, cy, nome, 20, 13))
for cx, cy in ((290, 140), (290, 290), (290, 430)):
    u.append(f'<line x1="150" y1="250" x2="{cx}" y2="{cy}" stroke="#000" stroke-width="1.5"/>')
u.append('<line x1="750" y1="360" x2="855" y2="250" stroke="#000" stroke-width="1.5"/>')
for (x1, y1), (x2, y2), (lx, ly) in (((505, 155), (545, 200), (532, 172)), ((480, 170), (575, 330), (452, 236)),
                                    ((505, 285), (540, 345), (530, 312))):
    u.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#000" stroke-width="1.5" stroke-dasharray="6 4" marker-end="url(#o)"/>')
    u.append(f'<text x="{lx}" y="{ly}" font-size="11" font-style="italic">«include»</text>')
u.append("</svg>")
(DESTINO / "use-case.svg").write_text("".join(u), encoding="utf-8")
print("diagramas gerados em", DESTINO)
