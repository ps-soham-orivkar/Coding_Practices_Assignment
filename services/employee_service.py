from typing import Any, Dict, List, Optional
from models.employee import Employee
from repositories.employee_repository import EmployeeRepository
from utils.validators import (
    is_not_empty,
    is_valid_date,
    is_valid_email,
    is_valid_employee_id,
)


class EmployeeService:
    """
    Handles business logic for managing employees.
    Persistence is delegated to an EmployeeRepository.
    """

    def __init__(
        self,
        repository: Optional[EmployeeRepository] = None,
        data_file: str = "employees.json"
    ) -> None:
        self.repository: EmployeeRepository = (
            repository if repository is not None else EmployeeRepository(data_file=data_file)
        )
        self.employees: List[Employee] = []
        self.load_data()

    def load_data(self) -> None:
        """Loads employee records from the repository."""
        self.employees = self.repository.load_employees()

    def save_data(self) -> None:
        """Persists current employee records via the repository."""
        self.repository.save_employees(self.employees)

    def _find_index_by_id(self, employee_id: str) -> int:
        """Helper method to find the index of an employee by ID."""
        for index, emp in enumerate(self.employees):
            if emp.employee_id == employee_id:
                return index
        return -1

    def _validate_employee_data(
        self,
        employee_id: Optional[str] = None,
        name: Optional[str] = None,
        email: Optional[str] = None,
        department: Optional[str] = None,
        designation: Optional[str] = None,
        joining_date: Optional[str] = None,
        is_update: bool = False
    ) -> None:
        """Validates employee field formats and values."""
        if employee_id is not None:
            if not is_valid_employee_id(employee_id):
                raise ValueError("Employee ID must be non-empty and alphanumeric.")

        if name is not None or not is_update:
            if not is_not_empty(name):
                raise ValueError("Employee Name cannot be empty.")

        if email is not None or not is_update:
            if not is_valid_email(email):
                raise ValueError("Invalid email format.")

        if department is not None or not is_update:
            if not is_not_empty(department):
                raise ValueError("Department cannot be empty.")

        if designation is not None or not is_update:
            if not is_not_empty(designation):
                raise ValueError("Designation cannot be empty.")

        if joining_date is not None or not is_update:
            if not is_valid_date(joining_date):
                raise ValueError("Invalid Joining Date. Expected format: YYYY-MM-DD (valid calendar date).")

    def add_employee(self, employee: Employee) -> bool:
        """
        Validates and adds a new employee.
        Raises ValueError if validation fails or ID already exists.
        """
        self._validate_employee_data(
            employee_id=employee.employee_id,
            name=employee.name,
            email=employee.email,
            department=employee.department,
            designation=employee.designation,
            joining_date=employee.joining_date,
            is_update=False
        )

        # Prevent duplicate employee IDs
        if self.search_employee_by_id(employee.employee_id) is not None:
            raise ValueError(f"Employee with ID '{employee.employee_id}' already exists.")

        self.employees.append(employee)
        self.save_data()
        return True

    def get_all_employees(self, sort_by_name: bool = False) -> List[Employee]:
        """Returns all employees, optionally sorted by name (case-insensitive)."""
        if sort_by_name:
            return sorted(self.employees, key=lambda emp: emp.name.lower())
        return list(self.employees)

    def search_employee_by_id(self, employee_id: str) -> Optional[Employee]:
        """Searches for an employee by ID and returns the Employee object or None."""
        index = self._find_index_by_id(employee_id)
        if index != -1:
            return self.employees[index]
        return None

    def update_employee(self, employee_id: str, updated_data: Dict[str, Any]) -> bool:
        """
        Updates an existing employee's details.
        updated_data is a dictionary containing fields to update.
        Raises ValueError if employee not found or validation fails.
        """
        emp = self.search_employee_by_id(employee_id)
        if not emp:
            raise ValueError(f"Employee with ID '{employee_id}' not found.")

        # Validate fields provided for update
        if "name" in updated_data and not is_not_empty(updated_data["name"]):
            raise ValueError("Employee Name cannot be empty.")

        if "email" in updated_data and not is_valid_email(updated_data["email"]):
            raise ValueError("Invalid email format.")

        if "department" in updated_data and not is_not_empty(updated_data["department"]):
            raise ValueError("Department cannot be empty.")

        if "designation" in updated_data and not is_not_empty(updated_data["designation"]):
            raise ValueError("Designation cannot be empty.")

        if "joining_date" in updated_data and not is_valid_date(updated_data["joining_date"]):
            raise ValueError("Invalid Joining Date. Expected format: YYYY-MM-DD (valid calendar date).")

        # Apply updates
        emp.name = updated_data.get("name", emp.name)
        emp.email = updated_data.get("email", emp.email)
        emp.department = updated_data.get("department", emp.department)
        emp.designation = updated_data.get("designation", emp.designation)
        emp.joining_date = updated_data.get("joining_date", emp.joining_date)

        self.save_data()
        return True

    def delete_employee(self, employee_id: str) -> bool:
        """Deletes an employee by ID. Raises ValueError if not found."""
        index = self._find_index_by_id(employee_id)
        if index != -1:
            del self.employees[index]
            self.save_data()
            return True
        raise ValueError(f"Employee with ID '{employee_id}' not found.")

    def filter_employees_by_department(self, department: str) -> List[Employee]:
        """Returns a list of employees belonging to a specific department."""
        dept_clean = department.strip().lower()
        return [emp for emp in self.employees if emp.department.strip().lower() == dept_clean]
