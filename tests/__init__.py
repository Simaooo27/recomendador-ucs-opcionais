"""Testes do OptaBem.

Os testes usam o catálogo pequeno do MVP (30 cursos com descrição), para os resultados não
mudarem quando o catálogo completo da DGES for atualizado. Os testes do catálogo completo
(US04) criam o seu próprio catálogo.
"""
import os
from pathlib import Path

os.environ["CATALOGO_CSV"] = str(Path(__file__).resolve().parent.parent / "dados" / "catalogo-cursos-mvp.csv")
