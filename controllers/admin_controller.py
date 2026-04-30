from utils import c_print, c_input 
from constants import INDENT_LVL_1, INDENT_LVL_2
from models.database import Database


class AdminController:
    def __init__(self):
        self.database = Database()

    def format_database(self):
        c_print(f"{INDENT_LVL_1}Clearing sudents database", "INFO")

        a_input = input("Are you sure you want to clear the database (Y)ES/(N)O: ")

        if a_input == "Y":
            self.database.remove_records({"remove_all": True})
            c_print(f"{INDENT_LVL_1}Students data cleared", "INFO")
        elif a_input == "N":
            pass
        else:
            c_print(f"{INDENT_LVL_1}Invalid input")

    def group_student(self):
        c_print(f"{INDENT_LVL_1}Grade Grouping", "INFO")

        s_data = self.database.list_records({"list_all": True})

        if len(s_data) == 0:
            c_print(f"{INDENT_LVL_2}< Nothing to Display >")
        else:
            group_result = sorted(
                s_data.items(), key=lambda item: item[1]["overall_grade"], reverse=True
            )

            for i in group_result:
                c_print(f"{INDENT_LVL_1}{i[1]['overall_grade']} --> [{i[1]['name']} :: {i[0]} --> GRADE: {i[1]['overall_grade']} - MARK: {i[1]['average_mark']}]")

    def partition_student(self):
        c_print(f"{INDENT_LVL_1}PASS/FALL Partition", "INFO")
        s_data = self.database.list_records({"list_all": True})

        pass_list = []
        fail_list = []

        for sid, info in s_data.items():
            if info["overall_grade"] == "F":
                fail_list.append(
                    f"{info['name']} :: {sid} --> GRADE: {info['overall_grade']} - MARK: {info['average_mark']}"
                )
        c_print(f"{INDENT_LVL_1}FAIL --> [{','.join(fail_list)}]")

        for sid, info in s_data.items():
            if info["overall_grade"] != "F":
                pass_list.append(
                    f"{info['name']} :: {sid} --> GRADE: {info['overall_grade']} - MARK: {info['average_mark']}"
                )
        c_print(f"{INDENT_LVL_1}PASS --> [{','.join(pass_list)}]")

    def remove_student(self):

        s_id_get = c_input(f"{INDENT_LVL_1}Remove by ID: ")
        test = self.database.remove_records({"student_id": s_id_get})
        if test is None:
            c_print(f"{INDENT_LVL_1}Student {s_id_get} does not exist", "ERROR")
        else:
            c_print(f"{INDENT_LVL_1}Removing Student {s_id_get} Account", "INFO")

    def show_student(self):
        c_print(f"{INDENT_LVL_1}Student List", "INFO")

        s_data = self.database.list_records({"list_all": True})

        if len(s_data) == 0:
            c_print(f"{INDENT_LVL_2}< Nothing to Display >")
        else:
            for sid, info in s_data.items():
                c_print(f"{INDENT_LVL_1}{info['name']} :: {sid} --> Email: {info['email']}")
