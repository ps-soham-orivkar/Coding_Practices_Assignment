class Employee:
    """
    Represents an Employee entity.
    """
    def __init__(self, employee_id, name, email, department, designation, joining_date):
        self.employee_id = employee_id
        self.name = name
        self.email = email
        self.department = department
        self.designation = designation
        self.joining_date = joining_date

    def to_dict(self):
        """Converts Employee object to dictionary for easy serialization."""
        return {
            "employee_id": self.employee_id,
            "name": self.name,
            "email": self.email,
            "department": self.department,
            "designation": self.designation,
            "joining_date": self.joining_date
        }

    @classmethod
    def from_dict(cls, data):
        """Creates an Employee object from a dictionary."""
        return cls(
            employee_id=data.get("employee_id"),
            name=data.get("name"),
            email=data.get("email"),
            department=data.get("department"),
            designation=data.get("designation"),
            joining_date=data.get("joining_date")
        )

    def __str__(self):
        return (f"ID: {self.employee_id} | Name: {self.name} | "
                f"Email: {self.email} | Dept: {self.department} | "
                f"Desig: {self.designation} | Joined: {self.joining_date}")
