import re
import random
from constants import EMAIL_REGEX, PASSWORD_REGEX

COLOURS = {
    "SUCCESS": "\033[32m",  # green
    "ERROR": "\033[31m",  # red
    "INFO": "\033[33m",  # yellow
    "INPUT": "\033[36m",  # cyan
}

RESET = "\033[0m"  # default white


def c_print(text: str, level: str) -> None:
    colour = COLOURS.get(level, "")
    # Reset colour after printing
    print(f"{colour}{text}{RESET}" if colour else text)


def c_input(text: str) -> str:
    # Reset colour after prompt
    return input(f"{COLOURS['INPUT']}{text}{RESET}")


def validate_email(email: str) -> bool:
    return re.match(EMAIL_REGEX, email) is not None


def validate_password(password: str) -> bool:
    return re.match(PASSWORD_REGEX, password) is not None


def randomize_subject_id() -> str:
    return str(random.randint(1, 999)).zfill(3)


def randomize_mark() -> int:
    return random.randint(25, 100)


def randomize_student_id() -> str:
    return str(random.randint(1, 999999)).zfill(6)


def calculate_grade_from_mark(mark: int) -> str:
    # Ensure that mark is a number
    if not isinstance(mark, (int, float)):
        raise ValueError("Mark must be a number.")

    if mark >= 85:
        return "HD"
    if mark >= 75:
        return "D"
    if mark >= 65:
        return "C"
    if mark >= 50:
        return "P"
    return "F"
