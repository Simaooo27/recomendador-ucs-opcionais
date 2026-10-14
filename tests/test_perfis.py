"""Início de sessão único: padrões Strategy, Chain of Responsibility e Factory (app/auth/perfis.py)."""
from app.auth.perfis import (
    CadeiaDePerfis,
    Entrada,
    PerfilAdministrador,
    PerfilAluno,
    criar_cadeia_de_perfis,
)
from app.auth.services import LoginOutcome
from app.db import get_db
from tests.base import AppTestCase


class PerfilFalso:
    """Perfil de teste: mostra que a cadeia aceita qualquer perfil com a mesma interface."""

    nome = "falso"
    pagina_inicial = "main.privacy"

    def __init__(self, prefixo):
        self.prefixo = prefixo
        self.chamado = False

    def reconhece(self, identificador):
        return identificador.startswith(self.prefixo)

    def autenticar(self, db, identificador, palavra_passe):
        self.chamado = True
        return Entrada(LoginOutcome.SUCCESS, 1, self)

    def iniciar_sessao(self, conta_id):
        pass


class StrategyTests(AppTestCase):
    """Cada perfil reconhece os seus identificadores."""

    def test_aluno_reconhece_emails(self):
        self.assertTrue(PerfilAluno().reconhece("aluno@gmail.com"))
        self.assertFalse(PerfilAluno().reconhece("gestor"))

    def test_administrador_reconhece_nomes_sem_arroba(self):
        self.assertTrue(PerfilAdministrador().reconhece("gestor"))
        self.assertFalse(PerfilAdministrador().reconhece("aluno@gmail.com"))

    def test_cada_perfil_tem_a_sua_pagina_inicial(self):
        self.assertEqual(PerfilAluno().pagina_inicial, "main.home")
        self.assertEqual(PerfilAdministrador().pagina_inicial, "gestao.dashboard")


class ChainOfResponsibilityTests(AppTestCase):
    """A cadeia passa o pedido ao primeiro perfil que o reconhece."""

    def test_primeiro_perfil_que_reconhece_trata_o_pedido(self):
        a, b = PerfilFalso("a"), PerfilFalso("b")
        with self.app.app_context():
            entrada = CadeiaDePerfis([a, b]).entrar(get_db(), "beta", "x")
        self.assertIs(entrada.perfil, b)
        self.assertFalse(a.chamado)

    def test_sem_perfil_que_reconheca_e_credenciais_invalidas(self):
        with self.app.app_context():
            entrada = CadeiaDePerfis([PerfilFalso("a")]).entrar(get_db(), "zeta", "x")
        self.assertIs(entrada.outcome, LoginOutcome.INVALID_CREDENTIALS)
        self.assertIsNone(entrada.perfil)

    def test_espacos_a_volta_do_identificador_sao_ignorados(self):
        falso = PerfilFalso("a")
        with self.app.app_context():
            CadeiaDePerfis([falso]).entrar(get_db(), "  alfa ", "x")
        self.assertTrue(falso.chamado)


class FactoryTests(AppTestCase):
    def test_cadeia_tem_alunos_e_administradores(self):
        perfis = [perfil.nome for perfil in criar_cadeia_de_perfis()._perfis]
        self.assertEqual(perfis, ["aluno", "administrador"])
