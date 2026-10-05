"""Envio de email.

- ``console``: não envia nada; escreve a mensagem no registo da aplicação e
  guarda-a em ``outbox``. Serve para desenvolvimento e para os testes
  ("validação simulada em ambiente de teste"). Não usar em produção.
- ``smtp``: envia por SMTP, com as credenciais vindas do ambiente.
"""
from __future__ import annotations

import smtplib
import sys
from dataclasses import dataclass
from email.message import EmailMessage
from typing import Protocol


@dataclass(frozen=True)
class Message:
    to: str
    subject: str
    body: str


class Mailer(Protocol):
    def send(self, message: Message) -> None: ...


class ConsoleMailer:
    def __init__(self, *, echo: bool = True) -> None:
        self.outbox: list[Message] = []
        self._echo = echo

    def send(self, message: Message) -> None:
        self.outbox.append(message)
        if self._echo:
            print(
                f"\n--- Email simulado ---\nPara: {message.to}\nAssunto: {message.subject}\n\n"
                f"{message.body}--- Fim do email ---\n",
                file=sys.stderr,
                flush=True,
            )


class SmtpMailer:
    def __init__(self, *, server: str, port: int, use_tls: bool, username: str, password: str, sender: str) -> None:
        self._server, self._port, self._use_tls = server, port, use_tls
        self._username, self._password, self._sender = username, password, sender

    def send(self, message: Message) -> None:
        email = EmailMessage()
        email["From"] = self._sender
        email["To"] = message.to
        email["Subject"] = message.subject
        email.set_content(message.body)
        with smtplib.SMTP(self._server, self._port, timeout=10) as smtp:
            if self._use_tls:
                smtp.starttls()
            if self._username:
                smtp.login(self._username, self._password)
            smtp.send_message(email)


def create_mailer(config: dict) -> Mailer:
    backend = config.get("MAIL_BACKEND", "console")
    if backend == "console":
        return ConsoleMailer(echo=config.get("MAIL_CONSOLE_ECHO", True))
    if backend == "smtp":
        if not config.get("MAIL_SERVER"):
            raise RuntimeError("MAIL_BACKEND=smtp exige MAIL_SERVER.")
        return SmtpMailer(
            server=config["MAIL_SERVER"],
            port=config["MAIL_PORT"],
            use_tls=config["MAIL_USE_TLS"],
            username=config["MAIL_USERNAME"],
            password=config["MAIL_PASSWORD"],
            sender=config["MAIL_SENDER"],
        )
    raise RuntimeError(f"MAIL_BACKEND desconhecido: {backend!r} (use 'console' ou 'smtp').")
