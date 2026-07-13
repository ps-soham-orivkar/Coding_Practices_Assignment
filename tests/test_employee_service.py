import unittest
import os
from models.employee import Employee
from services.employee_service import EmployeeService

class TestEmployeeService(unittest.TestCase):
    def setUp(self):
        # Use a dummy file for testing so we don't mess up real data
        self.test_file = "test_employees.json"
        self.service = EmployeeService(data_file=self.test_file)
        # Clear any existing test data
        self.service.employees = []
        self.service.save_data()

    def tearDown(self):
        # Clean up the test file after each test
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_add_valid_employee(self):
        emp = Employee("E001", "Alice", "alice@example.com", "IT", "Dev", "2023-01-01")
        result = self.service.add_employee(emp)
        self.assertTrue(result)
        self.assertEqual(len(self.service.employees), 1)

    def test_add_duplicate_employee_id(self):
        emp1 = Employee("E001", "Alice", "alice@example.com", "IT", "Dev", "2023-01-01")
        self.service.add_employee(emp1)
        
        emp2 = Employee("E001", "Bob", "bob@example.com", "HR", "Manager", "2023-02-01")
        with self.assertRaises(ValueError) as context:
            self.service.add_employee(emp2)
        
        self.assertTrue("already exists" in str(context.exception))

    def test_add_employee_invalid_email(self):
        emp = Employee("E002", "Alice", "invalid-email", "IT", "Dev", "2023-01-01")
        with self.assertRaises(ValueError) as context:
            self.service.add_employee(emp)
        
        self.assertTrue("Invalid email format" in str(context.exception))

    def test_search_employee_by_id(self):
        emp = Employee("E003", "Charlie", "charlie@example.com", "Sales", "Exec", "2022-01-01")
        self.service.add_employee(emp)
        
        found = self.service.search_employee_by_id("E003")
        self.assertIsNotNone(found)
        self.assertEqual(found.name, "Charlie")

    def test_delete_employee(self):
        emp = Employee("E004", "David", "david@example.com", "Finance", "Analyst", "2021-01-01")
        self.service.add_employee(emp)
        
        self.service.delete_employee("E004")
        self.assertEqual(len(self.service.employees), 0)

if __name__ == '__main__':
    unittest.main()
