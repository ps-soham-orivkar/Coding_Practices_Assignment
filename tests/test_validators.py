import unittest
from utils.validators import (
    is_not_empty,
    is_valid_date,
    is_valid_email,
    is_valid_employee_id,
)


class TestValidators(unittest.TestCase):
    def test_is_not_empty(self):
        self.assertTrue(is_not_empty("hello"))
        self.assertTrue(is_not_empty("  hello  "))
        self.assertFalse(is_not_empty(""))
        self.assertFalse(is_not_empty("   "))
        self.assertFalse(is_not_empty(None))

    def test_is_valid_email(self):
        self.assertTrue(is_valid_email("test@example.com"))
        self.assertTrue(is_valid_email("first.last@domain.co.in"))
        self.assertTrue(is_valid_email("user+filter@example.org"))
        self.assertFalse(is_valid_email("invalid-email"))
        self.assertFalse(is_valid_email("@example.com"))
        self.assertFalse(is_valid_email("user@"))
        self.assertFalse(is_valid_email("user@domain"))
        self.assertFalse(is_valid_email(""))
        self.assertFalse(is_valid_email(None))

    def test_is_valid_employee_id(self):
        self.assertTrue(is_valid_employee_id("E001"))
        self.assertTrue(is_valid_employee_id("EMP-100"))
        self.assertTrue(is_valid_employee_id("emp_42"))
        self.assertFalse(is_valid_employee_id(""))
        self.assertFalse(is_valid_employee_id("   "))
        self.assertFalse(is_valid_employee_id("E#001"))
        self.assertFalse(is_valid_employee_id("EMP 100"))
        self.assertFalse(is_valid_employee_id(None))

    def test_is_valid_date(self):
        self.assertTrue(is_valid_date("2023-01-15"))
        self.assertTrue(is_valid_date("2024-02-29"))  # leap year
        self.assertFalse(is_valid_date("2023-02-29"))  # non-leap year
        self.assertFalse(is_valid_date("2023-13-01"))  # invalid month
        self.assertFalse(is_valid_date("15-01-2023"))  # wrong format
        self.assertFalse(is_valid_date("2023/01/15"))  # wrong separator
        self.assertFalse(is_valid_date("invalid-date"))
        self.assertFalse(is_valid_date(""))
        self.assertFalse(is_valid_date(None))


if __name__ == "__main__":
    unittest.main()
