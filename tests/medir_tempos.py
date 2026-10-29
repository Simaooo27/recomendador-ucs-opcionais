"""Mede o tempo das páginas principais com o catálogo completo (RNF03: menos de 2 segundos).

Não é um teste automático (o nome não começa por «test», por isso o ``unittest discover`` não o
corre): os tempos dependem do computador. Correr na raiz do projeto, depois do ``processar``:

    python tests/medir_tempos.py            # Windows: .venv\\Scripts\\python.exe tests\\medir_tempos.py

Usa uma base de dados temporária com um aluno, 3 exames e 6 opções no plano. Mostra, para cada
página, o primeiro pedido (catálogo ainda por ler) e a mediana de mais 5 pedidos.
"""
from __future__ import annotations

import json
import sqlite3
import statistics
import sys
import time
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

from app.catalogo import repository as catalogo_repository  # noqa: E402
from tests.base import AppTestCase  # noqa: E402

CATALOGO = str(RAIZ / "dados" / "catalogo-cursos.csv")
LIMITE_SEGUNDOS = 2.0


class MedirTempos(AppTestCase):
    config_overrides = {"CATALOGO_CSV": CATALOGO}

    def preparar(self) -> list[str]:
        cursos = catalogo_repository.todos(CATALOGO)
        publicos = [c for c in cursos if c.provas and c.ultimo_colocado and c.concurso_nacional]
        self.create_active_user()
        self.login()
        opcoes = [c.chave for c in publicos[:6]]
        ligacao = sqlite3.connect(self.db_path)
        try:
            ligacao.execute(
                "INSERT INTO planos_candidatura (user_id, media, exames, opcoes, atualizado_em) VALUES (?, ?, ?, ?, '2026-10-29')",
                (self.fetch_user()["id"], 15.2, json.dumps({"18": 143.0, "19": 157.0, "07": 130.0}), json.dumps(opcoes)),
            )
            ligacao.commit()
        finally:
            ligacao.close()
        print(f"\n{len(cursos)} cursos no catálogo\n")
        return opcoes

    def test_medir(self) -> None:
        opcoes = self.preparar()
        paginas = {
            "Início do aluno": "/inicio",
            "Catálogo (todos)": "/cursos/",
            "Catálogo (procura «gestão»)": "/cursos/?q=gestao",
            "Pesquisa ao vivo": "/cursos/pesquisa?q=eng",
            "Ficha de um curso": f"/cursos/{opcoes[0]}",
            "Comparar 3 cursos": "/cursos/comparar?" + "&".join(f"c={c}" for c in opcoes[:3]),
            "Plano de candidatura": "/candidatura/",
            "Conversa": "/orientacao/",
            "Apresentação (sem sessão)": "/",
        }
        lentas = []
        for nome, endereco in paginas.items():
            cliente = self.app.test_client() if "sem sessão" in nome else self.client
            inicio = time.perf_counter()
            resposta = cliente.get(endereco)
            primeiro = time.perf_counter() - inicio
            tempos = []
            for _ in range(5):
                inicio = time.perf_counter()
                cliente.get(endereco)
                tempos.append(time.perf_counter() - inicio)
            mediana = statistics.median(tempos)
            if max(primeiro, mediana) >= LIMITE_SEGUNDOS or resposta.status_code != 200:
                lentas.append(nome)
            print(f"{nome:30} {resposta.status_code}  1.º pedido {primeiro * 1000:6.0f} ms  mediana {mediana * 1000:6.0f} ms")
        print("\nTodas abaixo de 2 segundos." if not lentas else "\nA rever: " + ", ".join(lentas))
        self.assertEqual(lentas, [])


if __name__ == "__main__":
    unittest.main(argv=[sys.argv[0]], verbosity=0)
