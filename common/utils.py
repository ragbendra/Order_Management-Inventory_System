import uuid

def generate_idempotency_key():
    return str(uuid.uuid4())
