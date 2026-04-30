EMAIL_REGEX = r"^[a-zA-Z0-9]+\.[a-zA-Z0-9]+@university\.com$"
PASSWORD_REGEX = r"^[A-Z][A-Za-z]{5,}\d{3,}$"
DATA_FILE = "data/students.data"

COLOURS = {
    "DEFAULT": "\033[37m",  # white
    "SUCCESS": "\033[32m",  # green
    "ERROR": "\033[31m",  # red
    "INFO": "\033[33m",  # yellow
    "INPUT": "\033[36m",  # cyan
    "INPUT_WARN": "\033[31m",  # red
}

RESET = "\033[0m"  # default white

INDENT_LVL_0 = " " * 0
INDENT_LVL_1 = " " * 8
INDENT_LVL_2 = " " * 16
