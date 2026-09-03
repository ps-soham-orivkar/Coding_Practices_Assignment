from dataclasses import dataclass, asdict
from typing import Any, Dict


@dataclass
class Employee:
    """
    Represents an Employee entity.
    """
    employee_id: str
    name: str
    email: str
    department: str
    designation: str
    joining_date: str

    def to_dict(self) -> Dict[str, Any]:
        """Converts Employee object to dictionary for easy serialization."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Employee":
        """Creates an Employee object from a dictionary."""
        return cls(
            employee_id=str(data.get("employee_id", "")),
            name=str(data.get("name", "")),
            email=str(data.get("email", "")),
            department=str(data.get("department", "")),
            designation=str(data.get("designation", "")),
            joining_date=str(data.get("joining_date", ""))
        )

    def __str__(self) -> str:
        return (f"ID: {self.employee_id} | Name: {self.name} | "
                f"Email: {self.email} | Dept: {self.department} | "
                f"Desig: {self.designation} | Joined: {self.joining_date}")
