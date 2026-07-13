import re

def is_not_empty(value):
    """Checks if a string is not empty or just whitespace."""
    if value is None:
        return False
    return bool(str(value).strip())

def is_valid_email(email):
    """Validates an email address format using a simple regex."""
    if not is_not_empty(email):
        return False
    # A basic regex for email validation
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, str(email)) is not None
