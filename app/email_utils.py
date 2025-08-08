# app/email_utils.py
import os
import smtplib
from email.message import EmailMessage

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER")            # username for SMTP (or API user)
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")    # password or app-password or API token
FROM_EMAIL = os.getenv("FROM_EMAIL", SMTP_USER or "no-reply@example.com")

def send_welcome_email(to_email: str):
    """Send a plain text welcome email synchronously. Intended to be run as a background task."""
    msg = EmailMessage()
    msg["Subject"] = "Welcome to MyApp 🎉"
    msg["From"] = FROM_EMAIL
    msg["To"] = to_email
    msg.set_content(
        f"Hi,\n\nThanks for registering at MyApp. We're excited to have you.\n\n— The MyApp Team"
    )

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=30) as server:
            server.ehlo()
            # Use STARTTLS for common ports (587, 25, 2525)
            if SMTP_PORT in (587, 25, 2525):
                server.starttls()
                server.ehlo()
            if SMTP_USER and SMTP_PASSWORD:
                server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)
            # For production you would log success to a file or monitoring system.
    except Exception as e:
        # For demo purposes we just print. Replace with proper logging in prod.
        print("Failed to send email:", e)
