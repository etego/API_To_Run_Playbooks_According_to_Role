import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from config import Config

def send_email(recipient, subject, body):
    # Create a multipart message
    msg = MIMEMultipart()
    msg['From'] = Config.EMAIL_SENDER
    msg['To'] = recipient
    msg['Subject'] = subject

    # Attach the body text to the message
    msg.attach(MIMEText(body, 'plain'))

    # Send the email
    try:
        with smtplib.SMTP(Config.EMAIL_SERVER, Config.EMAIL_PORT) as server:
            server.starttls()
            server.login(Config.EMAIL_SENDER, Config.EMAIL_PASSWORD)
            server.send_message(msg)
            print(f"Email sent to {recipient}")
    except Exception as e:
        print(f"Error sending email: {e}")

def send_email_to_triggers(playbook_name, output, allowed_senders):
    subject = f"{playbook_name} Output"
    for recipient in allowed_senders:
        send_email(recipient, subject, output)