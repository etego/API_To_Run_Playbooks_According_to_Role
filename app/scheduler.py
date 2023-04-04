import time
import schedule
from app.email_trigger import get_emails

# Your email credentials
EMAIL_USERNAME = "your_email@example.com"
EMAIL_PASSWORD = "your_email_password"

# List of allowed senders who can trigger the GET requests
ALLOWED_SENDERS = [
    "user1@example.com",
    "user2@example.com",
    # Add more allowed senders as needed
]

TOKENS = {
    "user1@example.com": "token_for_user1",
    "user2@example.com": "token_for_user2",
    # Add more tokens as needed
}

def job():
    get_emails(EMAIL_USERNAME, EMAIL_PASSWORD, ALLOWED_SENDERS, TOKENS)

if __name__ == "__main__":
    # Schedule the job to run every minute
    schedule.every(1).minutes.do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)
