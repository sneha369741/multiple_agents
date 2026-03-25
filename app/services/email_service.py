import smtplib
import os

def send_email(message):
    server = smtplib.SMTP(os.getenv("SMTP_SERVER"), int(os.getenv("SMTP_PORT")))
    server.starttls()
    server.login(os.getenv("ALERT_EMAIL"), os.getenv("ALERT_PASSWORD"))
    server.sendmail(os.getenv("ALERT_EMAIL"), os.getenv("ALERT_EMAIL"), message)
    server.quit()
