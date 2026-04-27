import utils
from models.database import Database
from models.subject import Subject


class Student:
    def __init__(self):
        self.student_id = None

    def s_menu(self):
        while True:
            s_input = utils.c_input("        Student System (l/r/x): ").lower()

            match s_input:
                case "l":
                    self._login()
                case "r":
                    self._register()
                case "x":
                    break
                case _:
                    utils.c_print("Invalid input", "ERROR")

    def _register(self):
        utils.c_print("        Student Sign Up", "SUCCESS")

        while True:
            email = input("        Email: ")
            password = input("        Password: ")

            if not utils.validate_email(email) or not utils.validate_password(password):
                utils.c_print("        Incorrect email or password format", "ERROR")
                continue

            utils.c_print("        email and password formats acceptable", "INFO")

            # check if student already exists by email
            db = Database()
            all_data = db.list_records({"list_all": True}) or {}
            existing = next(
                (d for d in all_data.values() if d.get("email") == email),
                None
            )
            if existing:
                utils.c_print(f"        Student {existing['name']} already exists", "ERROR")
                return

            name = input("        Name: ")
            student_id = utils.randomize_student_id()

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
            db.add_record(record)
            utils.c_print(f"        Enrolling Student {name}", "INFO")
            return

    def _login(self):
        utils.c_print("        Student Sign In", "SUCCESS")

        email = input("        Email: ")
        password = input("        Password: ")

        if not utils.validate_email(email) or not utils.validate_password(password):
            utils.c_print("        Incorrect email or password format", "ERROR")
            return

        utils.c_print("        email and password formats acceptable", "INFO")

        db = Database()
        all_data = db.list_records({"list_all": True}) or {}
        match = next(
            ((sid, d) for sid, d in all_data.items()
             if d.get("email") == email and d.get("password") == password),
            None
        )

        if not match:
            utils.c_print("        Student does not exist", "ERROR")
            return

        student_id, _ = match
        self.student_id = student_id

        # hand off to Subject enrolment menu
        subject = Subject()
        subject.s_enrolment_menu(student_id)
