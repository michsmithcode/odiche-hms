import uuid

def generate_license_number():
    return f"DOC-{uuid.uuid4().hex[:8].upper()}"