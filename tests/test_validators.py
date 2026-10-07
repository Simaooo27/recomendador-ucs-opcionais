"""Regras de validação (puras): email (pessoal por omissão, domínio opcional) e palavra-passe."""
import unittest

from app.auth.validators import (
    RegistrationInput,
    is_allowed_domain,
    is_valid_email,
    normalize_email,
    validate_registration,
)

DOMAINS = ["iscap.ipp.pt"]


def is_institutional_email(email, domains):
    """Equivalente à regra antiga: email válido e do domínio configurado."""
    return is_valid_email(email) and is_allowed_domain(email, domains)


def _validate(domains=(), **overrides):
    data = {
        "email": "aluno@gmail.com",
        "password": "palavra-passe-1",
        "password_confirm": "palavra-passe-1",
        "accepted_privacy": True,
    }
    data.update(overrides)
    return validate_registration(
        RegistrationInput(**data), allowed_domains=list(domains), min_length=8, max_length=128
    )


class PersonalEmailTests(unittest.TestCase):
    """Sem restrição de domínio (por omissão): aceita qualquer email válido."""

    def test_aceita_emails_pessoais(self):
        for email in ("aluno@gmail.com", "aluno@outlook.pt", "nome.apelido@sapo.pt", "aluno@iscap.ipp.pt"):
            with self.subTest(email=email):
                self.assertTrue(is_valid_email(email))
                self.assertTrue(is_allowed_domain(email, []))

    def test_rejeita_emails_mal_formados(self):
        for email in ("", "aluno", "aluno@", "@gmail.com", "a@b@gmail.com", "al uno@gmail.com", "aluno@gmail"):
            with self.subTest(email=email):
                self.assertFalse(is_valid_email(email))

    def test_rejeita_email_demasiado_longo(self):
        self.assertFalse(is_valid_email("a" * 250 + "@gmail.com"))


class RestrictedDomainTests(unittest.TestCase):
    """Com ALLOWED_EMAIL_DOMAINS definido: só esses domínios (opção para o email institucional)."""

    def test_aceita_dominio_institucional(self):
        self.assertTrue(is_institutional_email("aluno@iscap.ipp.pt", DOMAINS))

    def test_ignora_maiusculas_e_espacos(self):
        self.assertTrue(is_institutional_email("  Aluno@ISCAP.ipp.PT ", DOMAINS))

    def test_aceita_subdominio_verdadeiro(self):
        self.assertTrue(is_institutional_email("aluno@alunos.iscap.ipp.pt", DOMAINS))

    def test_rejeita_dominios_externos(self):
        for email in ("aluno@gmail.com", "aluno@ipp.pt", "aluno@outlook.pt"):
            with self.subTest(email=email):
                self.assertFalse(is_institutional_email(email, DOMAINS))

    def test_rejeita_dominios_parecidos(self):
        for email in (
            "aluno@iscap.ipp.pt.evil.com",
            "aluno@evil-iscap.ipp.pt",
            "aluno@xiscap.ipp.pt",
            "aluno@iscap.ipp.pt.",
        ):
            with self.subTest(email=email):
                self.assertFalse(is_institutional_email(email, DOMAINS))

    def test_rejeita_emails_mal_formados(self):
        for email in ("", "aluno", "aluno@", "@iscap.ipp.pt", "a@b@iscap.ipp.pt", "al uno@iscap.ipp.pt"):
            with self.subTest(email=email):
                self.assertFalse(is_institutional_email(email, DOMAINS))

    def test_rejeita_email_demasiado_longo(self):
        self.assertFalse(is_institutional_email("a" * 250 + "@iscap.ipp.pt", DOMAINS))

    def test_varios_dominios_permitidos(self):
        domains = ["iscap.ipp.pt", "ipp.pt"]
        self.assertTrue(is_institutional_email("x@ipp.pt", domains))

    def test_normalize_email(self):
        self.assertEqual(normalize_email("  Aluno@ISCAP.ipp.pt "), "aluno@iscap.ipp.pt")


class RegistrationValidationTests(unittest.TestCase):
    def test_dados_validos_nao_tem_erros(self):
        self.assertEqual(_validate(), {})

    def test_email_mal_formado_tem_mensagem_propria(self):
        self.assertIn("email válido", _validate(email="aluno@")["email"])

    def test_email_obrigatorio(self):
        self.assertIn("email", _validate(email=""))

    def test_email_externo_mostra_dominio_aceite(self):
        errors = _validate(domains=DOMAINS, email="aluno@gmail.com")
        self.assertIn("@iscap.ipp.pt", errors["email"])

    def test_palavra_passe_curta(self):
        self.assertIn("pelo menos 8", _validate(password="ab1", password_confirm="ab1")["password"])

    def test_palavra_passe_sem_numero(self):
        errors = _validate(password="apenasletras", password_confirm="apenasletras")
        self.assertIn("password", errors)

    def test_palavra_passe_sem_letra(self):
        errors = _validate(password="12345678", password_confirm="12345678")
        self.assertIn("password", errors)

    def test_palavra_passe_demasiado_longa(self):
        long_password = "a1" * 70
        errors = _validate(password=long_password, password_confirm=long_password)
        self.assertIn("mais de 128", errors["password"])

    def test_confirmacao_diferente(self):
        self.assertIn("password_confirm", _validate(password_confirm="outra-coisa-1"))

    def test_politica_de_privacidade_obrigatoria(self):
        self.assertIn("accepted_privacy", _validate(accepted_privacy=False))

    def test_varios_erros_em_simultaneo(self):
        errors = _validate(email="x@", password="1", password_confirm="1", accepted_privacy=False)
        self.assertEqual(set(errors), {"email", "password", "accepted_privacy"})


if __name__ == "__main__":
    unittest.main()
