import smtplib, ssl
from email.message import EmailMessage

SMTP_HOST = "smtp.gmail.com"   # dla innych dostawców: ich host
SMTP_PORT = 465                # 465 = SSL, 587 = STARTTLS
USERNAME = "qertal123@gmail.com"
PASSWORD = "XXXXXXXXXXXXX"

msg = EmailMessage()
msg["From"] = USERNAME
msg["To"] = "qertal123@gmail.com"
msg["Subject"] = "Test z Pythona"
msg.set_content("Cześć! To jest wiadomość wysłana przez Python SMTP.")

context = ssl.create_default_context()
with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, context=context) as server:
    server.login(USERNAME, PASSWORD)
    server.send_message(msg)
