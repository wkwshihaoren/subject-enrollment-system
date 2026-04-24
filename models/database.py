import os
import pickle
from constants import DATA_FILE


class Database:
    def __init__(self):
        self.data_file_path = DATA_FILE

        # Ensure the data directory initializes with the data file
        os.makedirs(os.path.dirname(self.data_file_path), exist_ok=True)

        if (
            not os.path.exists(self.data_file_path)
            or os.path.getsize(self.data_file_path) == 0
        ):
            with open(self.data_file_path, "wb") as file:
                # seed with an empty dictionary to avoid EOFError on the first read/write
                pickle.dump({}, file)

    # Add new student record on register
    def add_record(self, inputData) -> dict | Exception:
        try:
            # Read existing data first
            with open(self.data_file_path, "rb") as file:
                existing_data = pickle.load(file)

            new_data = {**existing_data, **inputData}
            # Overwrite students.data file with the latest data (existing + new)
            with open(self.data_file_path, "wb") as file:
                pickle.dump(new_data, file)
                # Return the newly added student data for confirmation
                student_id = list(inputData.keys())[0]
                return student_id
        except Exception as e:
            print(f"Error writing to file: {e}")
            return e

    # Update student's record with new enrolment
    def add_enrolment(self, input_data) -> None:
        student_id = input_data.get("student_id")
        new_enrolment = input_data.get("enrolment")

        with open(self.data_file_path, "rb") as file:
            data = pickle.load(file)

            student_data = data[student_id]
            enrolments = student_data.get("enrolments", [])
            enrolments.append(new_enrolment)

            student_data["enrolments"] = enrolments
            data[student_id] = student_data

        # Write the updated data back to the file
        with open(self.data_file_path, "wb") as file:
            pickle.dump(data, file)

    # Read single student record or all records
    def list_records(self, input_data) -> dict | Exception:
        try:
            studentId, listAllRecords = (
                input_data.get("student_id"),
                input_data.get("list_all", False),
            )
            with open(self.data_file_path, "rb") as file:
                data = pickle.load(file)

                if listAllRecords:
                    return data
                else:
                    student_data = data.get(studentId, None)
                    return {studentId: student_data}
        except Exception as e:
            print(f"Error reading from file: {e}")
            return e

    # Update Password for a student
    def update_password(self, input_data) -> None:
        student_id = input_data.get("student_id")
        new_password = input_data.get("new_password")

        with open(self.data_file_path, "rb") as file:
            data = pickle.load(file)

            student_data = data[student_id]
            student_data["password"] = new_password
            data[student_id] = student_data

        # Write the updated data back to the file
        with open(self.data_file_path, "wb") as file:
            pickle.dump(data, file)

    # Remove single enrolment of a student
    def remove_enrolment(self, input_data) -> None:
        student_id = input_data.get("student_id")
        subject_id = input_data.get("subject_id")

        with open(self.data_file_path, "rb") as file:
            data = pickle.load(file)

            student_data = data[student_id]
            enrolments = student_data.get("enrolments", [])

            # Removal process: only keep enrolments that do not match the subject_id to be removed
            updated_enrolments = [
                enrolment
                for enrolment in enrolments
                if enrolment.get("subject") != subject_id
            ]

            student_data["enrolments"] = updated_enrolments
            data[student_id] = student_data

        # Write the updated data back to the file
        with open(self.data_file_path, "wb") as file:
            pickle.dump(data, file)

    # Remove student records (for Admins)
    def remove_records(self, data) -> None:
        try:
            student_id, remove_all = (
                data.get("student_id"),
                data.get("remove_all", False),
            )
            if remove_all:
                with open(self.data_file_path, "wb") as file:
                    pickle.dump({}, file)
                    return

            with open(self.data_file_path, "wb") as file:
                data = pickle.load(file)

            del data[student_id]
            with open(self.data_file_path, "wb") as file:
                pickle.dump(data, file)

            return data

        except Exception as e:
            print(f"Error reading from file: {e}")
            return
