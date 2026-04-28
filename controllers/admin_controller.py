import utils
from models.database import Database


class AdminController:
    def __init__(self):
        self.database = Database()

    def format_database(self):
        utils.c_print("Clearing students database", "INFO")

        a_input = input("Are you sure you want to clear the database (Y)ES/(N)O: ")

        if a_input == "Y":
            self.database.remove_records({"remove_all": True})
            print("Students data cleared")
        elif a_input == "N":
            pass
        else:
            print("Invalid input")

    def group_student(self):
        utils.c_print("        Grade Grouping", "INFO")

        s_data = self.database.list_records({"list_all": True})

        if len(s_data) == 0:
            print("        < Nothing to Display >")
        else:
            group_result = sorted(
                s_data.items(), key=lambda item: item[1]["overall_grade"], reverse=True
            )

            for i in group_result:
                print(
                    "       ",
                    i[1]["overall_grade"],
                    " --> ",
                    f"[{i[1]['name']} :: {i[0]} --> GRADE: {i[1]['overall_grade']} - MARK: {i[1]['average_mark']}]",
                )

    def partition_student(self):
        utils.c_print("        PASS/FALL Partition", "INFO")
        s_data = self.database.list_records({"list_all": True})

        pass_list = []
        fail_list = []

        for sid, info in s_data.items():
            if info["overall_grade"] == "F":
                fail_list.append(
                    f"{info['name']} :: {sid} --> GRADE: {info['overall_grade']} - MARK: {info['average_mark']}"
                )
        print(f"        FAIL --> [{','.join(fail_list)}]")

        for sid, info in s_data.items():
            if info["overall_grade"] != "F":
                pass_list.append(
                    f"{info['name']} :: {sid} --> GRADE: {info['overall_grade']} - MARK: {info['average_mark']}"
                )
        print(f"        PASS --> [{','.join(pass_list)}]")

    def remove_student(self):

        s_id_get = input("        Remove by ID: ")
        test = self.database.remove_records({"student_id": s_id_get})
        if test is None:
            utils.c_print(f"        Student {s_id_get} dose not exist", "ERROR")
        else:
            print(f"        Removing Student {s_id_get} Account")

    def show_student(self):
        utils.c_print("        Student List", "INFO")

        s_data = self.database.list_records({"list_all": True})

        if len(s_data) == 0:
            print("        < Nothing to Display >")
        else:
            for sid, info in s_data.items():
                print(
                    "       ",
                    info["name"],
                    " : : ",
                    sid,
                    " --> ",
                    "Email: ",
                    info["email"],
                )
