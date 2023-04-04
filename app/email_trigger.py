import imaplib
import email
from email.header import decode_header
from app.playbooks import run_playbook
from app.email import send_email

def get_emails(username, password, allowed_senders, tokens):
    # Connect to the email server using IMAP
    mail = imaplib.IMAP4_SSL("imap.gmail.com")  # Change this to your email provider's IMAP server
    mail.login(username, password)
    mail.select("inbox")

    # Search for unread emails in the inbox
    _, message_numbers = mail.search(None, "UNSEEN")
    message_numbers = message_numbers[0].split(b' ')

    for num in message_numbers:
        # Fetch the email data
        _, msg_data = mail.fetch(num, "(RFC822)")
        msg = email.message_from_bytes(msg_data[0][1])

        # Decode the email subject
        subject = decode_header(msg["Subject"])[0][0].decode()

        # Get the sender's email address
        from_email = email.utils.parseaddr(msg["From"])[1]

        # Check if the sender's email is in the list of allowed senders
        if from_email not in allowed_senders:
            continue
       # Check if the token in the email body is valid
        user_token = tokens.get(from_email)
        if user_token and not check_token(msg, user_token):
            continue
        # Process the email based on the subject
        if subject.lower() == "get1":
            # Run playbook1 and send the output via email
            output = run_playbook("playbook1")
            send_email(from_email, "Playbook 1 Output", output)
        elif subject.lower() == "get2":
            # Run playbook2 and send the output via email
            output = run_playbook("playbook2")
            send_email(from_email, "Playbook 2 Output", output)
        # Add more GET request handling here as needed

    # Close the mailbox and logout from the email server
    mail.close()
    mail.logout()

def check_token(msg, token):
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))
            if content_type == "text/plain" and "attachment" not in content_disposition:
                body = part.get_payload(decode=True).decode()
                if token in body:
                    return True
    else:
        body = msg.get_payload(decode=True).decode()
        if token in body:
            return True

    return False
