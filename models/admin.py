import controllers.admin_controller
from utils import c_print, c_input
from constants import INDENT_LVL_1


class Admin:
    def __init__(self):
        self.admin_controller = controllers.admin_controller.AdminController()

    def a_menu(self):
        while True:
            s_input = c_input(f"{INDENT_LVL_1}Admin System (c/g/p/r/s/x): ").lower()

            match s_input:
                case "c":
                    self.admin_controller.format_database()

                case "g":
                    self.admin_controller.group_student()

                case "p":
                    self.admin_controller.partition_student()

                case "r":
                    self.admin_controller.remove_student()

                case "s":
                    self.admin_controller.show_student()

                case "x":
                    break

                case _:
                    c_print(f"{INDENT_LVL_1}Invalid input")
