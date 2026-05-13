from controllers.student_controller import StudentController
from utils import c_print, c_input
from constants import INDENT_LVL_1
from models.subject import Subject


class Student:
    def __init__(self):
        self.student_id = None
        self.student_controller = StudentController()

    def s_menu(self):
        while True:
            s_input = c_input(f"{INDENT_LVL_1}Student System (l/r/x): ").lower()

            match s_input:
                case "l":
                    self._login()
                case "r":
                    self._register()
                case "x":
                    break
                case _:
                    c_print(f"{INDENT_LVL_1}Invalid input", "ERROR")

    def _register(self):
        self.student_controller.register()

    def _login(self):
        student_id = self.student_controller.login()
        if student_id is None:
            return
        self.student_id = student_id
        subject = Subject()
        subject.s_enrolment_menu(student_id)
