from models.admin import Admin
from models.student import Student
from utils import c_input, c_print
from constants import INDENT_LVL_0


class UniversityController:
    def __init__(self):
        self.admin = Admin()
        self.student = Student()

    def main_menu(self):
        while True:
            user_input = c_input(
                f"{INDENT_LVL_0}University System: (A)dmin, (S)tudent, or X : "
            )

            match user_input:
                case "A":
                    self.admin.a_menu()
                case "S":
                    self.student.s_menu()
                case "X":
                    c_print(f"{INDENT_LVL_0}Thank You", "INFO")
                    break
                case _:
                    c_print(f"{INDENT_LVL_0}Invalid Input", "ERROR")
