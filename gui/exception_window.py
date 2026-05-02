import os
import sys
import tkinter as tk
from tkinter import ttk
from constants import LOGIN_WINDOW, EXCEPTION_WINDOW

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


class ExceptionWindow(tk.Toplevel):
    def __init__(self, parent: tk.Misc, message: str, title: str = "Exception Window"):
        super().__init__(parent)

        self.title(title)
        width, height = EXCEPTION_WINDOW.get("width"), EXCEPTION_WINDOW.get("height")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        parent.update_idletasks()
        parent_x = parent.winfo_rootx()
        parent_y = parent.winfo_rooty()
        parent_w = parent.winfo_width()
        parent_h = parent.winfo_height()
        x = parent_x + (parent_w - width) // 2
        y = parent_y + (parent_h - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")

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
