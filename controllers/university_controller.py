from models.admin import Admin
from models.student import Student
import utils


class UniversityController:
    def __init__(self):
        self.admin = Admin()
        self.student = Student()

    def main_menu(self):
        while True:
            user_input = utils.c_input("University System: (A)dmin, (S)tudent, or X : ")

            match user_input:
                case "A":
                    self.admin.a_menu()
                case "S":
                    self.student.s_menu()
                case "X":
                    utils.c_print("Thank You", "INFO")
                    break
                case _:
                    utils.c_print("Invalid Input", "ERROR")
