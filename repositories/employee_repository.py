import json
import os
from typing import List
from models.employee import Employee


class EmployeeRepository:
    """
    Handles file persistence for employee records in JSON format.
    Distinguishes between missing files and corrupted/invalid files.
    """

    def __init__(self, data_file: str = "employees.json") -> None:
        self.data_file = data_file

    def load_employees(self) -> List[Employee]:
        """
        Loads employees from the JSON data file.

        - If the file does not exist, returns an empty list.
        - If the file is corrupted or contains invalid JSON structure, raises a ValueError.
        """
        if not os.path.exists(self.data_file):
            return []

        # If file is empty (0 bytes), treat as empty list
        if os.path.getsize(self.data_file) == 0:
            return []

        try:
            with open(self.data_file, "r", encoding="utf-8") as file:
                data = json.load(file)
        except (json.JSONDecodeError, UnicodeDecodeError) as err:
            raise ValueError(f"Corrupted or unreadable JSON file '{self.data_file}': {err}") from err

        if not isinstance(data, list):
            raise ValueError(f"Corrupted data format in '{self.data_file}': expected a JSON list.")

        employees: List[Employee] = []
        for index, emp_data in enumerate(data):
            if not isinstance(emp_data, dict):
                raise ValueError(
                    f"Corrupted record at index {index} in '{self.data_file}': expected a dictionary."
                )
            employees.append(Employee.from_dict(emp_data))

        return employees

    def save_employees(self, employees: List[Employee]) -> None:
        """
        Saves the list of employees to the JSON data file.
        """
        data = [emp.to_dict() for emp in employees]
        with open(self.data_file, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
