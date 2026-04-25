import random
from database import Database
from validator import Validator
from subject import Subject, Enrolment

CYAN   = "\033[96m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
RED    = "\033[91m"
RESET  = "\033[0m"

class StudentController:

    def __init__(self):
        self.current_student = None

    # ── Student System menu ──────────────────────────────────────────────────

    def student_menu(self):
        while True:
            choice = input(f"        {CYAN}Student System (l/r/x): {RESET}").strip().lower()
            if choice == "l":
                self.login()
            elif choice == "r":
                self.register()
            elif choice == "x":
                break

    # ── Register ─────────────────────────────────────────────────────────────

    def register(self):
        print(f"        {GREEN}Student Sign Up{RESET}")
        while True:
            email    = input("        Email: ").strip()
            password = input("        Password: ").strip()

            if not Validator.validate_email_format(email) or not Validator.validate_password_format(password):
                print(f"        {RED}Incorrect email or password format{RESET}")
                continue

            print(f"        {YELLOW}email and password formats acceptable{RESET}")

            if Database.find_student_by_email(email):
                print(f"        {RED}Student {Validator.extract_name_from_email(email)} already exists{RESET}")
                return  # back to student menu

            name = input("        Name: ").strip()
            new_student = Student(name, email, password)
            data = Database.load_raw_data()
            data.append(new_student.to_dict())
            Database.save_raw_data(data)
            print(f"        {YELLOW}Enrolling Student {name}{RESET}")
            return

    # ── Login ────────────────────────────────────────────────────────────────

    def login(self):
        print(f"        {GREEN}Student Sign In{RESET}")
        email    = input("        Email: ").strip()
        password = input("        Password: ").strip()

        student_data = Validator.validate_login(email, password)
        if student_data:
            self.current_student = Student.from_dict(student_data)
            self.enrolment_menu()

    # ── Subject Enrolment System menu ────────────────────────────────────────

    def enrolment_menu(self):
        while True:
            choice = input(f"                {CYAN}Student Course Menu (c/e/r/s/x): {RESET}").strip().lower()
            if choice == "c":
                self.change_password()
            elif choice == "e":
                self.enrol_subject()
            elif choice == "r":
                self.remove_subject()
            elif choice == "s":
                self.show_subjects()
            elif choice == "x":
                break

    # ── Change Password ──────────────────────────────────────────────────────

    def change_password(self):
        print(f"                {GREEN}Updating Password{RESET}")
        while True:
            new_pw     = input("                New Password: ").strip()
            confirm_pw = input("                Confirm Password: ").strip()

            if new_pw != confirm_pw:
                print(f"                {RED}Password does not match - try again{RESET}")
                continue

            if not Validator.validate_password_format(new_pw):
                print(f"                {RED}Incorrect password format{RESET}")
                continue

            self.current_student.password = new_pw
            Database.update_student_data(self.current_student.to_dict())
            return

    # ── Enrol Subject ────────────────────────────────────────────────────────

    def enrol_subject(self):
        if not Validator.validate_enrolment_limit(self.current_student):
            return
        new_subject = Enrolment.enrol(self.current_student)
        Database.update_student_data(self.current_student.to_dict())
        print(f"                {YELLOW}Enrolling in Subject-{new_subject.id}{RESET}")
        print(f"                {YELLOW}You are now enrolled in {len(self.current_student.subjects)} out of 4 subjects{RESET}")

    # ── Remove Subject ───────────────────────────────────────────────────────

    def remove_subject(self):
        subject_id = input("                Remove Subject by ID: ").strip()
        if not Validator.validate_subject_exists(self.current_student, subject_id):
            print(f"               {RED}Subject {subject_id} not found{RESET}")
            return
        print(f"                {YELLOW}Droping Subject-{subject_id}{RESET}")
        Enrolment.remove(self.current_student, subject_id)
        Database.update_student_data(self.current_student.to_dict())
        print(f"                {YELLOW}You are now enrolled in {len(self.current_student.subjects)} out of 4 subjects{RESET}")

    # ── Show Subjects ─────────────────────────────────────────────────────────

    def show_subjects(self):
        count = len(self.current_student.subjects)
        print(f"                {YELLOW}Showing {count} subjects{RESET}")
        for s in self.current_student.subjects:
            print(f"                {s}")