import secrets

ALLOWED_SENDERS = [
    "user1@example.com",
    "user2@example.com",
    # Add more allowed senders as needed
]

def generate_token(length=32):
    return secrets.token_hex(length)

def generate_tokens_for_senders(allowed_senders):
    tokens = {}
    for sender in allowed_senders:
        token = generate_token()
        tokens[sender] = token
    return tokens

if __name__ == "__main__":
    tokens = generate_tokens_for_senders(ALLOWED_SENDERS)
    print(tokens)
