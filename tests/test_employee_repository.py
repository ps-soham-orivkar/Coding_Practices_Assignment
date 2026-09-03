import os
import unittest
from models.employee import Employee
from repositories.employee_repository import EmployeeRepository


class TestEmployeeRepository(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_repo_employees.json"
        self.repository = EmployeeRepository(data_file=self.test_file)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_load_from_missing_file(self):
        # When the file does not exist, return empty list
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        employees = self.repository.load_employees()
        self.assertEqual(employees, [])

    def test_load_from_empty_file(self):
        with open(self.test_file, "w", encoding="utf-8") as f:
            f.write("")
        employees = self.repository.load_employees()
        self.assertEqual(employees, [])

    def test_save_and_load_valid_employees(self):
        emp1 = Employee("E001", "Alice", "alice@example.com", "IT", "Developer", "2023-01-15")
        emp2 = Employee("E002", "Bob", "bob@example.com", "HR", "Manager", "2023-02-20")
        
        self.repository.save_employees([emp1, emp2])
        self.assertTrue(os.path.exists(self.test_file))

        loaded = self.repository.load_employees()
        self.assertEqual(len(loaded), 2)
        self.assertEqual(loaded[0].employee_id, "E001")
        self.assertEqual(loaded[0].name, "Alice")
        self.assertEqual(loaded[1].employee_id, "E002")

    def test_load_corrupted_json_syntax(self):
        with open(self.test_file, "w", encoding="utf-8") as f:
            f.write("{ invalid json structure")
        
        with self.assertRaises(ValueError) as context:
            self.repository.load_employees()
        self.assertIn("Corrupted or unreadable JSON file", str(context.exception))

    def test_load_non_list_json(self):
        with open(self.test_file, "w", encoding="utf-8") as f:
            f.write('{"key": "value"}')
        
        with self.assertRaises(ValueError) as context:
            self.repository.load_employees()
        self.assertIn("expected a JSON list", str(context.exception))

    def test_load_invalid_item_in_list(self):
        with open(self.test_file, "w", encoding="utf-8") as f:
            f.write('["not_a_dictionary"]')
        
        with self.assertRaises(ValueError) as context:
            self.repository.load_employees()
        self.assertIn("expected a dictionary", str(context.exception))


if __name__ == "__main__":
    unittest.main()
