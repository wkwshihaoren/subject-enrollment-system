import pickle
import constants


class AdminController:
    def __init__(self):
        pass

    def format_database(self):
        print("Clearing students database")

        a_input = input("Are you sure you want to clear the database (Y)ES/(N)O: ")

        if a_input == "Y":
            with open(constants.DATA_FILE, "wb") as f:
                pickle.dump({}, f)
            print("Clearing students database")
        elif a_input == "N":
            pass
        else:
            print("Invalid input")

    def group_student(self):
        print("Grade Grouping")

        with open(constants.DATA_FILE, "rb") as file:
            s_data = pickle.load(file)
        if len(s_data) == 0:
            print("        < Nothing to Display >")
        else:
            group_result = sorted(
                s_data.items(), key=lambda item: item[1]["overall_grade"], reverse=True
            )

            for i in group_result:
                print(
                    i[1]["overall_grade"],
                    " --> ",
                    f"[{i[1]['name']} :: {i[0]} --> GRADE: {i[1]['overall_grade']} - MARK: {i[1]['average_mark']}]",
                )

    def partition_student(self):
        print("PASS/FALL Partition")
        with open(constants.DATA_FILE, "rb") as file:
            s_data = pickle.load(file)
        # pass_list = {k:v for k,v in s_data.items() if v["overall_grade"] != "F"}
        # print("FALL --> ", end="")

        pass_list = []
        fail_list = []

        for sid, info in s_data.items():
            if info["overall_grade"] == "F":
                fail_list.append(
                    f"{info['name']} :: {sid} --> GRADE: {info['overall_grade']} - MARK: {info['average_mark']}"
                )
        print(f"FAIL --> [{','.join(pass_list)}]")

        for sid, info in s_data.items():
            if info["overall_grade"] != "F":
                pass_list.append(
                    f"{info['name']} :: {sid} --> GRADE: {info['overall_grade']} - MARK: {info['average_mark']}"
                )
        print(f"PASS --> [{','.join(pass_list)}]")

    def remove_student(self):
        pass
        # s_id_get = input("Remove by ID: ")
        # with open(constants.DATA_FILE, "rb") as file:
        #     s_data = pickle.load(file)

    def show_student(self):
        print("Student List")

        with open(constants.DATA_FILE, "rb") as file:
            s_data = pickle.load(file)
        if len(s_data) == 0:
            print("        < Nothing to Display >")
        else:
            for sid, info in s_data.items():
                print(info["name"], " : : ", sid, " --> ", "Email: ", info["email"])


# student_data = {
#     "001": {
#         "name": "Test Test1",
#         "password": "Wangjing123",
#         "email": "Test.Test1@university.com",
#         "courses": [
#             {"subject": "541", "mark": 55, "grade": "P"},
#             {"subject": "455", "mark": 57, "grade": "P"},
#             {"subject": "742", "mark": 55, "grade": "P"},
#             {"subject": "744", "mark": 59, "grade": "P"}
#         ],
#         "average_mark": 55.50,
#         "overall_grade": "P"},
#     "002": {
#         "name": "Test Test2",
#         "password": "Wangjing234",
#         "email": "Test.Test2@university.com",
#         "courses": [
#             {"subject": "541", "mark": 55, "grade": "P"},
#             {"subject": "455", "mark": 57, "grade": "P"},
#             {"subject": "742", "mark": 55, "grade": "P"}
#         ],
#         "average_mark": 55.67,
#         "overall_grade": "P"},
#     "003": {
#         "name": "Test Test3",
#         "password": "Wangjing345",
#         "email": "Test.Test3@university.com",
#         "courses": [
#             {"subject": "541", "mark": 55, "grade": "P"},
#             {"subject": "455", "mark": 57, "grade": "P"},
#             {"subject": "742", "mark": 55, "grade": "P"}
#         ],
#         "average_mark": 55.67,
#         "overall_grade": "P"},
#
# }
# with open(constants.DATA_FILE, "wb") as file:
#     pickle.dump(student_data, file)
