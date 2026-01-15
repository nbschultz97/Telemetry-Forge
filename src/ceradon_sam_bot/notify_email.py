from __future__ import annotations

import logging
import smtplib
from email.message import EmailMessage

LOGGER = logging.getLogger(__name__)


def send_email(
    smtp_host: str,
    smtp_port: int,
    smtp_user: str,
    smtp_pass: str,
    to_address: str,
    from_address: str,
    subject: str,
    body_text: str,
) -> None:
    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = from_address
    message["To"] = to_address
    message.set_content(body_text)

    LOGGER.info("Sending email digest", extra={"to": to_address})
    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.send_message(message)
