import re
import constants
import utils
from models.database import Database


class EnrolmentController:
    def __init__(self):
        self.database = Database()

    # student_enrolment_menu
    def change_pass(self, student_id):
        utils.c_print("Updating Password", "INFO")
        while True:
            new_password = input("                New Password: ")

            if re.match(constants.PASSWORD_REGEX, new_password):
                while True:
                    confirm_new_password = input("                Confirm Password: ")

                    if new_password != confirm_new_password:
                        utils.c_print(
                            "                Password does not match - try again",
                            "ERROR",
                        )
                    else:
                        self.database.update_password(
                            {"student_id": student_id, "new_password": new_password}
                        )
                        break
                break
            else:
                utils.c_print("                Incorrect password format", "ERROR")

    def enrol(self, student_id):

        get_student_data = self.database.list_records({"student_id": student_id})[
            student_id
        ]["enrolments"]

        get_student_subject = {
            get_student_data["subject_id"] for get_student_data in get_student_data
        }
        if len(get_student_subject) < 4:
            # Generate non-repetitive subject_id
            while True:
                subject_id = utils.randomize_subject_id()
                if subject_id not in get_student_subject:
                    break

            radom_mark = utils.randomize_mark()
            new_subject = {
                "subject_name": "Subject",
                "subject_id": subject_id,
                "mark": radom_mark,
                "grade": utils.calculate_grade_from_mark(radom_mark),
            }
            # print(new_subject)
            self.database.add_enrolment(
                {"student_id": student_id, "enrolment": new_subject}
            )
            utils.c_print(f"                Enrolling in Subject-{subject_id}", "INFO")
            utils.c_print(
                f"                You are now enrooled in {len(get_student_subject) + 1} out of 4 subjects",
                "INFO",
            )

            # re-calculated the overall mark and save
            new_get_student_data = self.database.list_records(
                {"student_id": student_id}
            )[student_id]["enrolments"]

            get_all_subject_grade = [i["mark"] for i in new_get_student_data]
            if not get_all_subject_grade:
                average_mark = 0
            else:
                average_mark = round(
                    sum(get_all_subject_grade) / len(get_all_subject_grade), 2
                )
                overall_grade = utils.calculate_grade_from_mark(round(average_mark))

            self.database.update_mark_grade(
                {
                    "student_id": student_id,
                    "get_average_mark": average_mark,
                    "get_overall_grade": overall_grade,
                }
            )
        else:
            utils.c_print(
                "                Student are allowed to enrol in 4 subjects only",
                "ERROR",
            )

    def remove(self, student_id):

        get_subject_id = input("                Remove Subject by ID:")

        res_subject = self.database.remove_enrolment(
            {"student_id": student_id, "subject_id": get_subject_id}
        )[student_id]["enrolments"]

        len_subject = len(res_subject)

        utils.c_print(f"                Droping Subject-{get_subject_id}", "INFO")

        utils.c_print(
            f"                You are now enrolled in {len_subject} out of 4 subjects",
            "INFO",
        )

        # re-calculated the overall mark and save
        new_get_student_data = self.database.list_records({"student_id": student_id})[
            student_id
        ]["enrolments"]

        get_all_subject_grade = [i["mark"] for i in new_get_student_data]

        if not get_all_subject_grade:
            average_mark = 0
        else:
            average_mark = round(
                sum(get_all_subject_grade) / len(get_all_subject_grade), 2
            )
        overall_grade = utils.calculate_grade_from_mark(round(average_mark))

        self.database.update_mark_grade(
            {
                "student_id": student_id,
                "get_average_mark": average_mark,
                "get_overall_grade": overall_grade,
            }
        )

    def show(self, student_id):

        get_student_subject_data = self.database.list_records(
            {"student_id": student_id}
        )[student_id]["enrolments"]
        len_subject = len(get_student_subject_data)

        utils.c_print(f"                Showing {len_subject} subjects", "INFO")

        for i in get_student_subject_data:
            print(
                f"                [ {i['subject_name']} :: {i['subject_id']} -- mark = {i['mark']} -- grade = {i['grade']} ]"
            )
