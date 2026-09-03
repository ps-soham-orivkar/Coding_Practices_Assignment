# Employee Management Console Application

A simple, robust console application written in Python to manage employee records, designed to demonstrate coding best practices and clean architectural principles.

## How to Run the Application

### Prerequisites
- Python 3.7 or higher installed (utilizes `dataclasses` and modern type hints).

### Steps to Run
1. Open a terminal or command prompt.
2. Navigate to the project directory: `cd Coding_Practices_Assignment`
3. Run the application:
   ```bash
   python main.py
   ```

### Running Tests
To run the automated unit test suite:
```bash
python -m unittest discover tests
```

## Features Implemented
- **Add Employee:** Adds a new employee with ID, Name, Email, Department, Designation, and Joining Date.
- **View All Employees:** Displays a list of all employees (with an option to sort by name).
- **Search Employee:** Lookup an employee using their unique Employee ID.
- **Update Employee Details:** Update one or multiple fields for an existing employee.
- **Delete Employee:** Remove an employee from the system.
- **Filter by Department:** View all employees belonging to a specific department.
- **Data Persistence:** Saves and loads employee data using a JSON file (`employees.json`).

## Best Practices Followed
- **Separation of Concerns:** 
  - `models/employee.py`: Data structure defined using `@dataclass` with type hints and serialization helpers (`to_dict`, `from_dict`).
  - `repositories/employee_repository.py`: Dedicated persistence layer managing file I/O and distinguishing between missing vs corrupted/invalid files.
  - `services/employee_service.py`: Handles business logic, duplicate prevention, searching, sorting, and department filtering.
  - `utils/validators.py`: Reusable validation functions for non-empty text, email format, alphanumeric ID, and calendar dates (`YYYY-MM-DD`).
  - `main.py`: Clean presentation and console interaction layer.
- **Robust Error Handling:** 
  - Corrupted or invalid JSON data files raise descriptive errors to prevent accidental data loss. Missing files are gracefully initialized.
  - Clear user-facing error feedback on invalid inputs without application crashes.
- **Type Annotations:** Consistent typing (`typing` / built-in types) across all classes, parameters, and return types.
- **Input Validation:**
  - Employee ID: non-empty alphanumeric format.
  - Email: RFC-compliant regex format.
  - Joining Date: valid calendar date in `YYYY-MM-DD` format.
  - Name / Department / Designation: non-empty string checks.
- **Comprehensive Unit Testing:** Tests for service logic, edge cases, sorting, filtering, repository persistence, and validation utilities.

## Screenshots

### 1. Main Console
![Main Console](screenshots/Main%20Console.png)

### 2. Add Employee
![Add Employee](screenshots/Add%20Employee.png)

### 3. Show Employee
![Show Employee](screenshots/Show%20Employee.png)

### 4. Search Employee
![Search Employee](screenshots/Search%20Employee.png)

### 5. Update Employee
![Update Employee](screenshots/Update%20Employee.png)

### 6. Delete Employee
![Delete Employee](screenshots/Delete%20Employee.png)

### 7. Filter Employee by Department
![Filter Employee](screenshots/Filter%20Employee.png)

### 8. Exit
![Exit](screenshots/Exit.png)
