from datetime import datetime
import re
from typing import Optional


def is_not_empty(value: Optional[str]) -> bool:
    """Checks if a string is not empty or just whitespace."""
    if value is None:
        return False
    return bool(str(value).strip())


def is_valid_email(email: Optional[str]) -> bool:
    """Validates an email address format using regex."""
    if not is_not_empty(email):
        return False
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, str(email).strip()) is not None


def is_valid_employee_id(emp_id: Optional[str]) -> bool:
    """
    Validates employee ID format.
    Must be a non-empty alphanumeric string (optionally containing hyphens or underscores).
    """
    if not is_not_empty(emp_id):
        return False
    pattern = r"^[a-zA-Z0-9_-]+$"
    return re.match(pattern, str(emp_id).strip()) is not None


def is_valid_date(date_str: Optional[str], date_format: str = "%Y-%m-%d") -> bool:
    """
    Validates that a date string matches the expected format (default: YYYY-MM-DD)
    and represents a valid calendar date.
    """
    if not is_not_empty(date_str):
        return False
    try:
        datetime.strptime(str(date_str).strip(), date_format)
        return True
    except ValueError:
        return False
