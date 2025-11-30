import uuid

def generate_employee_id(prefix, number):
    """
    Generates an employee ID like: DR-00001
    """
    return f"{prefix}-{str(number).zfill(5)}"


# def generate_employee_id(prefix: str, user_uuid):
#     return f"{prefix}-{str(user_uuid)[:6].upper()}"
