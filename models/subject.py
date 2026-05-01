from controllers.enrolment_controller import EnrolmentController
from utils import c_print, c_input
from constants import INDENT_LVL_2


class Subject:
    def __init__(self):
        pass

    def s_enrolment_menu(self, student_id):
        subject = EnrolmentController()
        while True:
            s_enrolment_input = c_input(
                f"{INDENT_LVL_2}Student Course Menu (c/e/r/s/x): "
            ).lower()

            match s_enrolment_input:
                case "c":
                    subject.change_pass(student_id)

                case "e":
                    subject.enrol(student_id)

                case "r":
                    subject.remove(student_id)

                case "s":
                    subject.show(student_id)

                case "x":
                    break

                case _:
                    c_print(f"{INDENT_LVL_2}Invalid input", "ERROR")
