import controllers.admin_controller


class Admin:
    def __init__(self):
        self.admin_controller = controllers.admin_controller.AdminController()

    def a_menu(self):
        while True:
            s_input = input("Admin System (c/g/p/r/s/x) :").lower()

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
                    print("Invalid input")


admin = Admin()
admin.a_menu()
