import os
import sys
import utils
import tkinter as tk
from tkinter import ttk, messagebox
from gui.exception_window import ExceptionWindow
from models.database import Database
from constants import MAX_ENROLMENTS

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

os.chdir(PROJECT_ROOT)


class EnrolmentWindow(tk.Toplevel):
    def __init__(self, parent: tk.Misc, student_id: str):
        super().__init__(parent)

        self.parent = parent
        self.student_id = student_id
        self.database = Database()

        self.title("GUIUniApp - Enrolment Window")
        self.geometry("540x430")
        self.resizable(False, False)

        self.SUBJECT_CATALOG = utils.randomize_subject_catalog()
        self.subject_codes = list(self.SUBJECT_CATALOG.keys())
        self.subject_window = None

        self.create_widgets()
        self.refresh_status()

        self.protocol("WM_DELETE_WINDOW", self.close_window)

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding=20)
        main_frame.grid(row=0, column=0, sticky="nsew")

        title_label = ttk.Label(
            main_frame,
            text="Subjects Catalog",
            font=("Times New Roman", 16, "bold"),
        )
        title_label.grid(row=0, column=0, pady=(0, 10))

        instruction_label = ttk.Label(
            main_frame,
            text=(
                "Select subject(s) to enrol.\n"
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

        self.subject_listbox = tk.Listbox(
            main_frame,
            selectmode=tk.MULTIPLE,
            width=42,
            height=10,
            exportselection=False,
        )
        self.subject_listbox.grid(row=4, column=0, pady=(0, 15))

        for code, name in self.SUBJECT_CATALOG.items():
            self.subject_listbox.insert(tk.END, f"{code} - {name}")

        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0)

        enrol_button = ttk.Button(
            button_frame,
            text="Enrol",
            command=self.enrol_selected,
        )
        enrol_button.grid(row=0, column=0, padx=5)

        show_button = ttk.Button(
            button_frame,
            text="Show Subjects",
            command=self.show_subjects,
        )
        show_button.grid(row=0, column=1, padx=5)

        clear_button = ttk.Button(
            button_frame,
            text="Clear Selection",
            command=self.clear_selection,
        )
        clear_button.grid(row=0, column=2, padx=5)

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

    def clear_selection(self):
        self.subject_listbox.selection_clear(0, tk.END)

    def show_subjects(self):
        from gui.subject_window import SubjectWindow

        if self.subject_window is not None and self.subject_window.winfo_exists():
            self.subject_window.lift()
            self.subject_window.refresh_rows()
            return

        self.subject_window = SubjectWindow(self, self.student_id)

    def enrol_selected(self):
        student = self.get_student()

        if student is None:
            ExceptionWindow(
                self,
                "Student data could not be found.",
                "Data Error",
            )
            return

        selected_indices = self.subject_listbox.curselection()
        selected_codes = [self.subject_codes[index] for index in selected_indices]

        if not selected_codes:
            ExceptionWindow(
                self,
                "Please select at least one subject.",
                "Enrolment Error",
            )
            return

        enrolments = student.get("enrolments", [])
        existing_subject_ids = {subject.get("subject_id") for subject in enrolments}

        for code in selected_codes:
            if code in existing_subject_ids:
                ExceptionWindow(
                    self,
                    f"Subject {code} is already enrolled.",
                    "Enrolment Error",
                )
                return

        if len(enrolments) + len(selected_codes) > MAX_ENROLMENTS:
            ExceptionWindow(
                self,
                "You can only enrol in up to 4 subjects.",
                "Enrolment Error",
            )
            return

        for code in selected_codes:
            mark = utils.randomize_mark()
            grade = utils.calculate_grade_from_mark(mark)

            new_subject = {
                "subject_name": self.SUBJECT_CATALOG[code],
                "subject_id": code,
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
        self.clear_selection()

        if self.subject_window is not None and self.subject_window.winfo_exists():
            self.subject_window.refresh_rows()

        messagebox.showinfo(
            "Enrolment Successful",
            "Subject(s) added to students.data.",
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
