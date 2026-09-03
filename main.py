import sys
from typing import Dict
from models.employee import Employee
from services.employee_service import EmployeeService


def print_menu() -> None:
    """Displays the main application menu."""
    print("\n--- Employee Management Console ---")
    print("1. Add Employee")
    print("2. View All Employees")
    print("3. Search Employee by ID")
    print("4. Update Employee Details")
    print("5. Delete Employee")
    print("6. Filter Employees by Department")
    print("7. Exit")
    print("-----------------------------------")


def get_user_input(prompt: str) -> str:
    """Utility function to get input and handle whitespace clean up."""
    return input(prompt).strip()


def add_employee_flow(service: EmployeeService) -> None:
    """Flow for adding a new employee with interactive validation."""
    print("\n--- Add New Employee ---")
    emp_id = get_user_input("Enter Employee ID: ")
    name = get_user_input("Enter Name: ")
    email = get_user_input("Enter Email: ")
    department = get_user_input("Enter Department: ")
    designation = get_user_input("Enter Designation: ")
    joining_date = get_user_input("Enter Joining Date (YYYY-MM-DD): ")

    new_employee = Employee(emp_id, name, email, department, designation, joining_date)
    try:
        service.add_employee(new_employee)
        print("Success: Employee added successfully!")
    except ValueError as e:
        print(f"Error: {e}")


def view_all_employees_flow(service: EmployeeService) -> None:
    """Flow for listing all employees, optionally sorted."""
    print("\n--- All Employees ---")
    sort_choice = get_user_input("Sort by name? (y/n): ")
    sort_by_name = sort_choice.lower() == 'y'

    employees = service.get_all_employees(sort_by_name)
    if not employees:
        print("No employees found.")
    else:
        for emp in employees:
            print(emp)


def search_employee_flow(service: EmployeeService) -> None:
    """Flow for searching an employee by ID."""
    print("\n--- Search Employee ---")
    emp_id = get_user_input("Enter Employee ID to search: ")
    emp = service.search_employee_by_id(emp_id)
    if emp:
        print("Employee Found:")
        print(emp)
    else:
        print("Error: Employee not found.")


def update_employee_flow(service: EmployeeService) -> None:
    """Flow for updating fields of an existing employee."""
    print("\n--- Update Employee ---")
    emp_id = get_user_input("Enter Employee ID to update: ")
    emp = service.search_employee_by_id(emp_id)

    if not emp:
        print("Error: Employee not found.")
        return

    print("Leave field blank to keep current value.")
    name = get_user_input(f"Enter New Name [{emp.name}]: ")
    email = get_user_input(f"Enter New Email [{emp.email}]: ")
    department = get_user_input(f"Enter New Department [{emp.department}]: ")
    designation = get_user_input(f"Enter New Designation [{emp.designation}]: ")
    joining_date = get_user_input(f"Enter New Joining Date [{emp.joining_date}]: ")

    updated_data: Dict[str, str] = {}
    if name:
        updated_data['name'] = name
    if email:
        updated_data['email'] = email
    if department:
        updated_data['department'] = department
    if designation:
        updated_data['designation'] = designation
    if joining_date:
        updated_data['joining_date'] = joining_date

    if not updated_data:
        print("No updates provided.")
        return

    try:
        service.update_employee(emp_id, updated_data)
        print("Success: Employee updated successfully!")
    except ValueError as e:
        print(f"Error: {e}")


def delete_employee_flow(service: EmployeeService) -> None:
    """Flow for deleting an employee."""
    print("\n--- Delete Employee ---")
    emp_id = get_user_input("Enter Employee ID to delete: ")
    try:
        service.delete_employee(emp_id)
        print("Success: Employee deleted successfully!")
    except ValueError as e:
        print(f"Error: {e}")


def filter_employees_flow(service: EmployeeService) -> None:
    """Flow for filtering employees by department."""
    print("\n--- Filter Employees by Department ---")
    department = get_user_input("Enter Department Name: ")
    employees = service.filter_employees_by_department(department)

    if not employees:
        print(f"No employees found in department: {department}")
    else:
        print(f"Employees in {department}:")
        for emp in employees:
            print(emp)


def main() -> None:
    """Main application entry point."""
    try:
        service = EmployeeService()
    except ValueError as err:
        print(f"Initialization Error: {err}")
        print("Please resolve the data file issue before starting the application.")
        sys.exit(1)

    while True:
        print_menu()
        choice = get_user_input("Select an option (1-7): ")

        if choice == '1':
            add_employee_flow(service)
        elif choice == '2':
            view_all_employees_flow(service)
        elif choice == '3':
            search_employee_flow(service)
        elif choice == '4':
            update_employee_flow(service)
        elif choice == '5':
            delete_employee_flow(service)
        elif choice == '6':
            filter_employees_flow(service)
        elif choice == '7':
            print("Exiting application. Goodbye!")
            sys.exit(0)
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
