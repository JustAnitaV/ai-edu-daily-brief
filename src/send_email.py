import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(subject: str, html_body: str) -> None:
    email_host = os.getenv("EMAIL_HOST")
    email_port = int(os.getenv("EMAIL_PORT", "587"))
    email_username = os.getenv("EMAIL_USERNAME")
    email_password = os.getenv("EMAIL_PASSWORD")
    email_to = os.getenv("EMAIL_TO")

    if not all([email_host, email_port, email_username, email_password, email_to]):
        raise RuntimeError("Missing one or more email environment variables.")

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = email_username
    msg["To"] = email_to

    html_part = MIMEText(html_body, "html", "utf-8")
    msg.attach(html_part)

    with smtplib.SMTP(email_host, email_port) as server:
        server.starttls()
        server.login(email_username, email_password)
        server.sendmail(email_username, email_to, msg.as_string())
