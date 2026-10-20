"""Comando de terminal para experimentar o LLM com a chave real (spike da US30).

    flask --app app llm-teste --backend gemini
    flask --app app llm-teste --backend ollama

Faz 2 pedidos: o LLM faz a primeira pergunta; depois recebe uma resposta de exemplo (com um
email de propósito, para mostrar que é apagado) e tem de sugerir cursos do catálogo.
A chave é lida do .env e nunca é mostrada.
"""
from __future__ import annotations

import time

import click
from flask import current_app
from flask.cli import with_appcontext

from ..catalogo import services as catalogo
from ..llm import ErroLLM, Mensagem, criar_cliente_llm
from . import conversa

RESPOSTA_DE_EXEMPLO = (
    "Gosto de computadores e de organizar informação, e não gosto muito de Matemática. "
    "Preferia estudar no Porto. O meu email é teste@exemplo.pt."
)


@click.command("llm-teste")
@click.option("--backend", default=None, help="falso, gemini, groq ou ollama (por omissão: LLM_BACKEND do .env).")
@click.option("--modelo", default=None, help="Outro modelo do fornecedor (por omissão: LLM_MODELO ou o padrão).")
@with_appcontext
def llm_teste(backend: str | None, modelo: str | None) -> None:
    """Faz uma conversa curta de orientação com o LLM configurado."""
    config = dict(current_app.config)
    if backend:
        config["LLM_BACKEND"] = backend
    if modelo:
        config["LLM_MODELO"] = modelo
    cursos = catalogo.cursos(config)
    try:
        cliente = criar_cliente_llm(config)
        click.echo(f"LLM: {cliente.nome} (a chave não é mostrada)")
        click.echo(f"Catálogo: {len(cursos)} cursos; instruções com {len(conversa.instrucoes(cursos))} caracteres\n")

        inicio = time.monotonic()
        passo = conversa.proximo_passo(cliente, cursos, [])
        click.echo(f"1.º pedido ({time.monotonic() - inicio:.1f} s) → {_descrever(passo)}\n")

        historico = [
            Mensagem("assistente", passo.texto),
            Mensagem("utilizador", RESPOSTA_DE_EXEMPLO),
        ]
        click.echo(f"Resposta de exemplo enviada: «{RESPOSTA_DE_EXEMPLO}»")
        click.echo("(o email é substituído por «[email removido]» antes de sair do computador)\n")
        inicio = time.monotonic()
        passo = conversa.proximo_passo(cliente, cursos, historico, forcar_sugestao=True)
        click.echo(f"2.º pedido ({time.monotonic() - inicio:.1f} s) → {_descrever(passo)}")
    except ErroLLM as erro:
        raise click.ClickException(str(erro)) from None
    except RuntimeError as erro:   # LLM_BACKEND desconhecido
        raise click.ClickException(str(erro)) from None
    click.echo("\nPedidos usados: 2.")
    if cliente.nome.startswith("gemini/"):
        click.echo("Limites da sua conta: https://aistudio.google.com/rate-limit")


def _descrever(passo: conversa.Pergunta | conversa.Sugestao) -> str:
    if isinstance(passo, conversa.Pergunta):
        return f"pergunta: {passo.texto}"
    linhas = [f"sugestão: {passo.texto}"]
    for sugerido in passo.cursos:
        c = sugerido.curso
        linhas.append(f"  - {c.curso}, {c.instituicao} ({c.chave}): {sugerido.explicacao}")
    if not passo.cursos:
        linhas.append("  (nenhum curso válido)")
    if passo.descartados:
        linhas.append(f"  descartados por não estarem no catálogo (RN09): {', '.join(passo.descartados)}")
    return "\n".join(linhas)


def init_app(app) -> None:
    app.cli.add_command(llm_teste)
