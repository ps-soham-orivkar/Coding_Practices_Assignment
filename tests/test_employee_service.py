import os
import unittest
from models.employee import Employee
from repositories.employee_repository import EmployeeRepository
from services.employee_service import EmployeeService


class TestEmployeeService(unittest.TestCase):
    def setUp(self):
        # Use a dummy file for testing so we don't affect real data
        self.test_file = "test_employees.json"
        self.repository = EmployeeRepository(data_file=self.test_file)
        self.service = EmployeeService(repository=self.repository)
        # Clear any existing test data
        self.service.employees = []
        self.service.save_data()

    def tearDown(self):
        # Clean up test file after each test
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_add_valid_employee(self):
        emp = Employee("E001", "Alice", "alice@example.com", "IT", "Developer", "2023-01-01")
        result = self.service.add_employee(emp)
        self.assertTrue(result)
        self.assertEqual(len(self.service.employees), 1)

    def test_add_duplicate_employee_id(self):
        emp1 = Employee("E001", "Alice", "alice@example.com", "IT", "Developer", "2023-01-01")
        self.service.add_employee(emp1)

        emp2 = Employee("E001", "Bob", "bob@example.com", "HR", "Manager", "2023-02-01")
        with self.assertRaises(ValueError) as context:
            self.service.add_employee(emp2)
        self.assertIn("already exists", str(context.exception))

    def test_add_employee_invalid_id(self):
        # Empty ID
        emp_empty = Employee("", "Alice", "alice@example.com", "IT", "Dev", "2023-01-01")
        with self.assertRaises(ValueError) as context:
            self.service.add_employee(emp_empty)
        self.assertIn("Employee ID must be non-empty", str(context.exception))

        # ID with invalid characters
        emp_invalid = Employee("E 001", "Alice", "alice@example.com", "IT", "Dev", "2023-01-01")
        with self.assertRaises(ValueError) as context:
            self.service.add_employee(emp_invalid)
        self.assertIn("Employee ID must be non-empty", str(context.exception))

    def test_add_employee_empty_name(self):
        emp = Employee("E002", "   ", "alice@example.com", "IT", "Developer", "2023-01-01")
        with self.assertRaises(ValueError) as context:
            self.service.add_employee(emp)
        self.assertIn("Employee Name cannot be empty", str(context.exception))

    def test_add_employee_invalid_email(self):
        emp = Employee("E002", "Alice", "invalid-email", "IT", "Developer", "2023-01-01")
        with self.assertRaises(ValueError) as context:
            self.service.add_employee(emp)
        self.assertIn("Invalid email format", str(context.exception))

    def test_add_employee_empty_department(self):
        emp = Employee("E002", "Alice", "alice@example.com", "  ", "Developer", "2023-01-01")
        with self.assertRaises(ValueError) as context:
            self.service.add_employee(emp)
        self.assertIn("Department cannot be empty", str(context.exception))

    def test_add_employee_empty_designation(self):
        emp = Employee("E002", "Alice", "alice@example.com", "IT", "", "2023-01-01")
        with self.assertRaises(ValueError) as context:
            self.service.add_employee(emp)
        self.assertIn("Designation cannot be empty", str(context.exception))

    def test_add_employee_invalid_joining_date(self):
        # Invalid format
        emp_bad_format = Employee("E002", "Alice", "alice@example.com", "IT", "Dev", "01/01/2023")
        with self.assertRaises(ValueError) as context:
            self.service.add_employee(emp_bad_format)
        self.assertIn("Invalid Joining Date", str(context.exception))

        # Invalid calendar day
        emp_bad_day = Employee("E003", "Bob", "bob@example.com", "IT", "Dev", "2023-02-30")
        with self.assertRaises(ValueError) as context:
            self.service.add_employee(emp_bad_day)
        self.assertIn("Invalid Joining Date", str(context.exception))

    def test_search_employee_by_id(self):
        emp = Employee("E003", "Charlie", "charlie@example.com", "Sales", "Executive", "2022-01-01")
        self.service.add_employee(emp)

        found = self.service.search_employee_by_id("E003")
        self.assertIsNotNone(found)
        self.assertEqual(found.name, "Charlie")

        not_found = self.service.search_employee_by_id("NON_EXISTENT")
        self.assertIsNone(not_found)

    def test_update_employee_success(self):
        emp = Employee("E004", "David", "david@example.com", "Finance", "Analyst", "2021-01-01")
        self.service.add_employee(emp)

        updated = self.service.update_employee("E004", {
            "name": "David Smith",
            "department": "Accounting",
            "email": "david.smith@example.com",
            "designation": "Senior Analyst",
            "joining_date": "2021-06-15"
        })
        self.assertTrue(updated)

        refreshed = self.service.search_employee_by_id("E004")
        self.assertEqual(refreshed.name, "David Smith")
        self.assertEqual(refreshed.department, "Accounting")
        self.assertEqual(refreshed.email, "david.smith@example.com")
        self.assertEqual(refreshed.designation, "Senior Analyst")
        self.assertEqual(refreshed.joining_date, "2021-06-15")

    def test_update_employee_partial(self):
        emp = Employee("E005", "Emma", "emma@example.com", "HR", "Recruiter", "2020-05-10")
        self.service.add_employee(emp)

        self.service.update_employee("E005", {"designation": "Lead Recruiter"})
        refreshed = self.service.search_employee_by_id("E005")
        self.assertEqual(refreshed.designation, "Lead Recruiter")
        self.assertEqual(refreshed.name, "Emma")  # unchanged

    def test_update_employee_not_found(self):
        with self.assertRaises(ValueError) as context:
            self.service.update_employee("E999", {"name": "Ghost"})
        self.assertIn("not found", str(context.exception))

    def test_update_employee_invalid_fields(self):
        emp = Employee("E006", "Frank", "frank@example.com", "Legal", "Advisor", "2020-01-01")
        self.service.add_employee(emp)

        with self.assertRaises(ValueError) as context:
            self.service.update_employee("E006", {"email": "bad-email"})
        self.assertIn("Invalid email format", str(context.exception))

        with self.assertRaises(ValueError) as context:
            self.service.update_employee("E006", {"name": "   "})
        self.assertIn("Employee Name cannot be empty", str(context.exception))

        with self.assertRaises(ValueError) as context:
            self.service.update_employee("E006", {"department": "  "})
        self.assertIn("Department cannot be empty", str(context.exception))

        with self.assertRaises(ValueError) as context:
            self.service.update_employee("E006", {"designation": ""})
        self.assertIn("Designation cannot be empty", str(context.exception))

        with self.assertRaises(ValueError) as context:
            self.service.update_employee("E006", {"joining_date": "2020-15-99"})
        self.assertIn("Invalid Joining Date", str(context.exception))

    def test_delete_employee(self):
        emp = Employee("E007", "Grace", "grace@example.com", "Finance", "Analyst", "2021-01-01")
        self.service.add_employee(emp)

        self.assertTrue(self.service.delete_employee("E007"))
        self.assertEqual(len(self.service.employees), 0)

        with self.assertRaises(ValueError) as context:
            self.service.delete_employee("E007")
        self.assertIn("not found", str(context.exception))

    def test_get_all_employees_and_sorting(self):
        emp_z = Employee("E1", "Zack", "zack@example.com", "IT", "Dev", "2022-01-01")
        emp_a = Employee("E2", "adam", "adam@example.com", "IT", "Dev", "2022-01-01")
        emp_m = Employee("E3", "Mary", "mary@example.com", "HR", "Manager", "2022-01-01")

        self.service.add_employee(emp_z)
        self.service.add_employee(emp_a)
        self.service.add_employee(emp_m)

        unsorted_list = self.service.get_all_employees(sort_by_name=False)
        self.assertEqual([e.name for e in unsorted_list], ["Zack", "adam", "Mary"])

        sorted_list = self.service.get_all_employees(sort_by_name=True)
        self.assertEqual([e.name for e in sorted_list], ["adam", "Mary", "Zack"])

    def test_filter_employees_by_department(self):
        emp1 = Employee("E1", "Alice", "alice@example.com", "IT", "Dev", "2022-01-01")
        emp2 = Employee("E2", "Bob", "bob@example.com", "HR", "Manager", "2022-01-01")
        emp3 = Employee("E3", "Charlie", "charlie@example.com", "it", "QA", "2022-01-01")

        self.service.add_employee(emp1)
        self.service.add_employee(emp2)
        self.service.add_employee(emp3)

        it_employees = self.service.filter_employees_by_department("IT")
        self.assertEqual(len(it_employees), 2)
        self.assertEqual({e.employee_id for e in it_employees}, {"E1", "E3"})

        unknown_dept = self.service.filter_employees_by_department("Marketing")
        self.assertEqual(len(unknown_dept), 0)

    def test_employee_model_methods(self):
        emp = Employee("E100", "John", "john@example.com", "Eng", "Architect", "2021-05-01")
        emp_dict = emp.to_dict()
        self.assertEqual(emp_dict["employee_id"], "E100")
        self.assertEqual(emp_dict["name"], "John")

        reconstructed = Employee.from_dict(emp_dict)
        self.assertEqual(reconstructed.employee_id, "E100")
        self.assertEqual(reconstructed.name, "John")

        str_rep = str(emp)
        self.assertIn("ID: E100", str_rep)
        self.assertIn("Name: John", str_rep)


if __name__ == "__main__":
    unittest.main()
