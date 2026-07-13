import json
import os
from models.employee import Employee
from utils.validators import is_not_empty, is_valid_email

class EmployeeService:
    """
    Handles business logic and data persistence for employees.
    """
    def __init__(self, data_file="employees.json"):
        self.data_file = data_file
        self.employees = []
        self.load_data()

    def load_data(self):
        """Loads employee data from the JSON file."""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as file:
                    data = json.load(file)
                    self.employees = [Employee.from_dict(emp_data) for emp_data in data]
            except json.JSONDecodeError:
                # Handle empty or corrupted file
                self.employees = []
        else:
            self.employees = []

    def save_data(self):
        """Saves current employee list to the JSON file."""
        with open(self.data_file, 'w') as file:
            data = [emp.to_dict() for emp in self.employees]
            json.dump(data, file, indent=4)

    def _find_index_by_id(self, employee_id):
        """Helper method to find the index of an employee by ID."""
        for index, emp in enumerate(self.employees):
            if emp.employee_id == employee_id:
                return index
        return -1

    def add_employee(self, employee):
        """
        Validates and adds a new employee.
        Raises ValueError if validation fails or ID already exists.
        """
        # Basic Validation
        if not is_not_empty(employee.employee_id):
            raise ValueError("Employee ID cannot be empty.")
        if not is_not_empty(employee.name):
            raise ValueError("Employee Name cannot be empty.")
        if not is_valid_email(employee.email):
            raise ValueError("Invalid email format.")

        # Prevent duplicate employee IDs
        if self.search_employee_by_id(employee.employee_id) is not None:
            raise ValueError(f"Employee with ID '{employee.employee_id}' already exists.")

        self.employees.append(employee)
        self.save_data()
        return True

    def get_all_employees(self, sort_by_name=False):
        """Returns all employees, optionally sorted by name."""
        if sort_by_name:
            return sorted(self.employees, key=lambda emp: emp.name.lower())
        return self.employees

    def search_employee_by_id(self, employee_id):
        """Searches for an employee by ID and returns the object or None."""
        index = self._find_index_by_id(employee_id)
        if index != -1:
            return self.employees[index]
        return None

    def update_employee(self, employee_id, updated_data):
        """
        Updates an existing employee's details.
        updated_data is a dictionary with fields to update.
        Raises ValueError if employee not found or validation fails.
        """
        emp = self.search_employee_by_id(employee_id)
        if not emp:
            raise ValueError(f"Employee with ID '{employee_id}' not found.")

        # Validate provided updates
        if 'name' in updated_data and not is_not_empty(updated_data['name']):
            raise ValueError("Employee Name cannot be empty.")
        if 'email' in updated_data and not is_valid_email(updated_data['email']):
            raise ValueError("Invalid email format.")

        # Apply updates
        emp.name = updated_data.get('name', emp.name)
        emp.email = updated_data.get('email', emp.email)
        emp.department = updated_data.get('department', emp.department)
        emp.designation = updated_data.get('designation', emp.designation)
        emp.joining_date = updated_data.get('joining_date', emp.joining_date)

        self.save_data()
        return True

    def delete_employee(self, employee_id):
        """Deletes an employee by ID. Raises ValueError if not found."""
        index = self._find_index_by_id(employee_id)
        if index != -1:
            del self.employees[index]
            self.save_data()
            return True
        raise ValueError(f"Employee with ID '{employee_id}' not found.")

    def filter_employees_by_department(self, department):
        """Returns a list of employees belonging to a specific department."""
        return [emp for emp in self.employees if emp.department.lower() == department.lower()]
