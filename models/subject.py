from controllers.enrolment_controller import EnrolmentController
import utils


class Subject:
    def __init__(self):
        pass

    def s_enrolment_menu(self, student_id):
        subject = EnrolmentController()
        while True:
            s_enrolment_input = utils.c_input(
                "Student Course Menu (c/e/r/s/x) :"
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
                    print("Invalid input")
