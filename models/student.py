import random
from database import Database
from validator import Validator
from subject import Subject, Enrolment

CYAN   = "\033[96m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
RED    = "\033[91m"
RESET  = "\033[0m"


class Student:

    def __init__(self, name, email, password, student_id=None, subjects=None):
        self.id       = student_id if student_id else f"{random.randint(1, 999999):06d}"
        self.name     = name
        self.email    = email
        self.password = password
        self.subjects = subjects if subjects else []

    def get_average_mark(self):
        if not self.subjects:
            return 0
        return sum(s.mark for s in self.subjects) / len(self.subjects)

    def get_status(self):
        return "PASS" if self.get_average_mark() >= 50 else "FAIL"

    def to_dict(self):
        return {
            "id":       self.id,
            "name":     self.name,
            "email":    self.email,
            "password": self.password,
            "subjects": [s.to_dict() for s in self.subjects],
        }

    @classmethod
    def from_dict(cls, data):
        subjects = [Subject.from_dict(s) for s in data.get("subjects", [])]
        return cls(data["name"], data["email"], data["password"], data["id"], subjects)
