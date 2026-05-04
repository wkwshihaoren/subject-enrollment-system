import utils
import tkinter as tk
from tkinter import ttk, messagebox
from gui.exception_window import ExceptionWindow
from models.database import Database
from constants import MAX_ENROLMENTS, ENROLMENT_WINDOW


class EnrolmentWindow(tk.Toplevel):
    def __init__(self, parent: tk.Misc, student_id: str):
        super().__init__(parent)

        self.parent = parent
        self.student_id = student_id
        self.database = Database()

        self.title("GUIUniApp - Enrolment Window")
        self.geometry(
            f"{ENROLMENT_WINDOW.get('width')}x{ENROLMENT_WINDOW.get('height')}"
        )
        self.resizable(False, False)

        self.subject_window = None

        self.create_widgets()
        self.refresh_status()

        self.protocol("WM_DELETE_WINDOW", self.close_window)

    def create_widgets(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        main_frame = ttk.Frame(self, padding=20)
        main_frame.grid(row=0, column=0)

        title_label = ttk.Label(
            main_frame,
            text="Random Enrolment",
            font=("Times New Roman", 16, "bold"),
        )
        title_label.grid(row=0, column=0, pady=(0, 10))

        instruction_label = ttk.Label(
            main_frame,
            text=(
                "Click 'Enrol' to randomly enrol in a new subject.\n"
                "A student can enrol in a maximum of four subjects."
            ),
            wraplength=400,
            justify="center",
        )
        instruction_label.grid(row=1, column=0, pady=(0, 10))

        self.student_info_var = tk.StringVar()
        student_info_label = ttk.Label(
            main_frame,
            textvariable=self.student_info_var,
            justify="center",
        )
        student_info_label.grid(row=2, column=0, pady=(0, 8))

        self.status_var = tk.StringVar()
        status_label = ttk.Label(
            main_frame,
            textvariable=self.status_var,
            font=("Times New Roman", 11, "bold"),
        )
        status_label.grid(row=3, column=0, pady=(0, 10))

        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0)

        enrol_button = ttk.Button(
            button_frame,
            text="Enrol",
            command=self.enrol,
        )
        enrol_button.grid(row=0, column=0, padx=5)

        show_button = ttk.Button(
            button_frame,
            text="Show Subjects",
            command=self.show_subjects,
        )
        show_button.grid(row=0, column=1, padx=5)

        refresh_button = ttk.Button(
            button_frame,
            text="Refresh",
            command=self.refresh_status,
        )
        refresh_button.grid(row=0, column=2, padx=5)

        close_button = ttk.Button(
            button_frame,
            text="Logout",
            command=self.close_window,
        )
        close_button.grid(row=0, column=3, padx=5)

    def get_student(self) -> dict | None:
        data = self.database.list_records({"student_id": self.student_id}) or {}
        return data.get(self.student_id)

    def refresh_status(self):
        student = self.get_student()

        if student is None:
            self.student_info_var.set("Student data could not be found.")
            self.status_var.set("")
            return

        name = student.get("name", "")
        email = student.get("email", "")
        enrolments = student.get("enrolments", [])
        average_mark = student.get("average_mark", 0)
        overall_grade = student.get("overall_grade", "F")

        self.student_info_var.set(
            f"Student: {name}\t\tID: {self.student_id}\n"
            f"Email: {email}\n"
            f"Average Mark: {average_mark}\t\tOverall Grade: {overall_grade}"
        )

        self.status_var.set(f"Enrollment status: {len(enrolments)}/{MAX_ENROLMENTS}")

    def show_subjects(self):
        from gui.subject_window import SubjectWindow

        if self.subject_window is not None and self.subject_window.winfo_exists():
            self.subject_window.lift()
            self.subject_window.refresh_rows()
            return

        self.subject_window = SubjectWindow(self, self.student_id)

    def enrol(self):
        student = self.get_student()

        if student is None:
            ExceptionWindow(
                self,
                "Student data could not be found.",
                "Data Error",
            )
            return

        enrolments = student.get("enrolments", [])

        if len(enrolments) >= MAX_ENROLMENTS:
            ExceptionWindow(
                self,
                "You can only enrol in up to 4 subjects.",
                "Enrolment Error",
            )
            return

        existing_subject_ids = {subject.get("subject_id") for subject in enrolments}

        while True:
            subject_id = utils.randomize_subject_id()
            if subject_id not in existing_subject_ids:
                break

        subject_name = "Subject"
        mark = utils.randomize_mark()
        grade = utils.calculate_grade_from_mark(mark)

        new_subject = {
            "subject_name": subject_name,
            "subject_id": subject_id,
            "mark": mark,
            "grade": grade,
        }

        self.database.add_enrolment(
            {
                "student_id": self.student_id,
                "enrolment": new_subject,
            }
        )

        self.update_average_and_grade()
        self.refresh_status()

        if self.subject_window is not None and self.subject_window.winfo_exists():
            self.subject_window.refresh_rows()

        messagebox.showinfo(
            "Enrolment Successful",
            f"Enrolled in {subject_name} (ID: {subject_id})\n"
            f"Mark: {mark}    Grade: {grade}",
        )

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

    def close_window(self):
        self.destroy()
        self.parent.deiconify()
