import tkinter as tk
from tkinter import ttk, messagebox
import utils
from gui.exception_window import ExceptionWindow
from models.database import Database
from constants import SUBJECT_WINDOW


class SubjectWindow(tk.Toplevel):
    def __init__(self, parent: tk.Misc, student_id: str):
        super().__init__(parent)

        self.parent = parent
        self.student_id = student_id
        self.database = Database()

        self.title("GUIUniApp - Subject Window")
        self.geometry(f"{SUBJECT_WINDOW.get('width')}x{SUBJECT_WINDOW.get('height')}")
        self.resizable(False, False)

        self.create_widgets()
        self.refresh_rows()

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding=16)
        main_frame.grid(row=0, column=0, sticky="nsew")

        title_label = ttk.Label(
            main_frame,
            text="Current Enrolment",
            font=("Times New Roman", 16, "bold"),
        )
        title_label.grid(row=0, column=0, pady=(0, 12))

        self.student_info_var = tk.StringVar()
        student_info_label = ttk.Label(
            main_frame,
            textvariable=self.student_info_var,
            font=("Times New Roman", 11),
            justify="center",
        )
        student_info_label.grid(row=1, column=0, pady=(0, 10))

        columns = ("subject_id", "subject_name", "mark", "grade")

        self.tree = ttk.Treeview(
            main_frame,
            columns=columns,
            show="headings",
            height=8,
        )
        self.tree.grid(row=2, column=0, pady=(0, 12))

        self.tree.heading("subject_id", text="Subject ID")
        self.tree.heading("mark", text="Mark")
        self.tree.heading("grade", text="Grade")

        self.tree.column("subject_id", width=100, anchor="center")
        self.tree.column("mark", width=90, anchor="center")
        self.tree.column("grade", width=90, anchor="center")

        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0)

        refresh_button = ttk.Button(
            button_frame,
            text="Refresh",
            command=self.refresh_rows,
        )
        refresh_button.grid(row=0, column=0, padx=5)

        unenroll_button = ttk.Button(
            button_frame,
            text="Withdraw",
            command=self.unenroll_selected,
        )
        unenroll_button.grid(row=0, column=1, padx=5)

        close_button = ttk.Button(
            button_frame,
            text="Close",
            command=self.destroy,
        )
        close_button.grid(row=0, column=2, padx=5)

    def get_student(self) -> dict | None:
        data = self.database.list_records({"student_id": self.student_id}) or {}
        return data.get(self.student_id)

    def refresh_rows(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        student = self.get_student()

        if student is None:
            self.student_info_var.set("Student data could not be found.")
            return

        name = student.get("name", "")
        email = student.get("email", "")
        enrolments = student.get("enrolments", [])
        average_mark = student.get("average_mark", 0)
        overall_grade = student.get("overall_grade", "F")

        self.student_info_var.set(
            f"Student: {name}    ID: {self.student_id}\n"
            f"Email: {email}\n"
            f"Average Mark: {average_mark}    Overall Grade: {overall_grade}"
        )

        if not enrolments:
            self.tree.insert(
                "",
                "end",
                values=("", "No enrolled subjects", "", ""),
            )
            return

        for subject in enrolments:
            self.tree.insert(
                "",
                "end",
                values=(
                    subject.get("subject_id", ""),
                    subject.get("subject_name", ""),
                    subject.get("mark", ""),
                    subject.get("grade", ""),
                ),
            )

    def unenroll_selected(self):
        selected_item = self.tree.selection()

        if not selected_item:
            ExceptionWindow(
                self,
                "Please select a subject to unenroll from.",
                "Selection Error",
            )
            return

        subject_id = self.tree.item(selected_item, "values")[0]

        if not subject_id:
            ExceptionWindow(
                self,
                "Unable to unenroll from the selected subject.",
                "Unenroll Error",
            )
            return

        student = self.get_student()

        if student is None:
            ExceptionWindow(
                self,
                "Student data could not be found.",
                "Data Error",
            )
            return

        self.database.remove_enrolment(
            {"student_id": self.student_id, "subject_id": subject_id}
        )

        self.update_average_and_grade()

        messagebox.showinfo(
            "Unenrollment Successful",
            "Subject removed from student's enrolments.",
        )

        self.refresh_rows()

    def update_average_and_grade(self):
        student = self.get_student()

        if student is None:
            return

        enrolments = student.get("enrolments", [])

        if not enrolments:
            average_mark = 0
        else:
            marks = [subject.get("mark", 0) for subject in enrolments]
            average_mark = round(sum(marks) / len(marks), 2)

        overall_grade = utils.calculate_grade_from_mark(round(average_mark))

        self.database.update_mark_grade(
            {
                "student_id": self.student_id,
                "get_average_mark": average_mark,
                "get_overall_grade": overall_grade,
            }
        )
