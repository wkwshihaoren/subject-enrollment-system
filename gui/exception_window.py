import os
import sys
import tkinter as tk
from tkinter import ttk

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


class ExceptionWindow(tk.Toplevel):
    def __init__(self, parent: tk.Misc, message: str, title: str = "Exception Window"):
        super().__init__(parent)

        self.title(title)
        self.geometry("390x180")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        main_frame = ttk.Frame(self, padding=20)
        main_frame.grid(row=0, column=0, sticky="nsew")

        title_label = ttk.Label(
            main_frame,
            text=title,
            font=("Times New Roman", 15, "bold"),
            foreground="red",
        )
        title_label.grid(row=0, column=0, pady=(0, 10))

        message_label = ttk.Label(
            main_frame,
            text=message,
            font=("Times New Roman", 11),
            wraplength=320,
            justify="center",
        )
        message_label.grid(row=1, column=0, pady=(0, 15))

        close_button = ttk.Button(
            main_frame,
            text="Close",
            command=self.destroy,
        )
        close_button.grid(row=2, column=0)

        self.focus()
