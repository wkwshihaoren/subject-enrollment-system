from utils import (
    c_print,
    c_input,
    validate_email,
    validate_password,
    randomize_student_id,
)
from constants import INDENT_LVL_1
from models.database import Database


class StudentController:
    def __init__(self):
        self.database = Database()

    def register(self):
        c_print(f"{INDENT_LVL_1}Student Sign Up", "SUCCESS")

        while True:
            email = c_input(f"{INDENT_LVL_1}Email: ", "DEFAULT")
            password = c_input(f"{INDENT_LVL_1}Password: ", "DEFAULT")

            if not validate_email(email) or not validate_password(password):
                c_print(f"{INDENT_LVL_1}Incorrect email or password format", "ERROR")
                continue

            c_print(f"{INDENT_LVL_1}Email and password formats acceptable", "INFO")

            all_data = self.database.list_records({"list_all": True}) or {}
            existing = next(
                (d for d in all_data.values() if d.get("email") == email), None
            )
            if existing:
                c_print(
                    f"{INDENT_LVL_1}Student {existing['name']} already exists", "ERROR"
                )
                return

            name = c_input(f"{INDENT_LVL_1}Name: ", "DEFAULT")
            student_id = randomize_student_id()

            record = {
                student_id: {
                    "name": name,
                    "email": email,
                    "password": password,
                    "enrolments": [],
                    "average_mark": 0,
                    "overall_grade": "F",
                }
            }
            self.database.add_record(record)
            c_print(f"{INDENT_LVL_1}Enrolling Student {name}", "INFO")
            return

    def login(self):
        c_print(f"{INDENT_LVL_1}Student Sign In", "SUCCESS")

        while True:
            email = c_input(f"{INDENT_LVL_1}Email: ", "DEFAULT")
            password = c_input(f"{INDENT_LVL_1}Password: ", "DEFAULT")

            if not validate_email(email) or not validate_password(password):
                c_print(f"{INDENT_LVL_1}Incorrect email or password format", "ERROR")
                continue

            c_print(f"{INDENT_LVL_1}Email and password formats acceptable", "INFO")

            all_data = self.database.list_records({"list_all": True}) or {}
            match = next(
                (
                    (sid, d)
                    for sid, d in all_data.items()
                    if d.get("email") == email and d.get("password") == password
                ),
                None,
            )

            if not match:
                c_print(f"{INDENT_LVL_1}Student does not exist", "ERROR")
                return None

            student_id, _ = match
            return student_id
