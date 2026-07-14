import file_handler
from utils import (
    get_non_empty_input,
    get_valid_age,
    print_success,
    print_error,
    print_info,
    print_divider,
    confirm_action,
)


def _find_by_id(students, student_id):
    student_id = student_id.upper()
    for i, s in enumerate(students):
        if s["student_id"].upper() == student_id:
            return i, s
    return None, None


def _print_student(s):
    print_divider()
    print(f"Student ID : {s['student_id']}")
    print(f"Name       : {s['name']}")
    print(f"Age        : {s['age']}")
    print(f"Course     : {s['course']}")


def add_student():
    students = file_handler.load_students()

    print_info("--- Add New Student ---")
    student_id = get_non_empty_input("Enter Student ID: ").upper()

    index, existing = _find_by_id(students, student_id)
    if existing:
        print_error(f"A student with ID '{student_id}' already exists.")
        return

    name = get_non_empty_input("Enter Student Name: ")
    age = get_valid_age("Enter Student Age: ")
    course = get_non_empty_input("Enter Course: ")

    new_student = {"student_id": student_id, "name": name, "age": age, "course": course}
    students.append(new_student)

    if file_handler.save_students(students):
        print_success(f"Student '{name}' (ID: {student_id}) added successfully.")
    else:
        print_error("Failed to save the new student record.")


def view_all_students():
    students = file_handler.load_students()

    print_info("--- All Students ---")
    if not students:
        print_error("No student records found.")
        return

    for s in students:
        _print_student(s)
    print_divider()
    print(f"Total Students: {len(students)}")


def search_student_by_id():
    students = file_handler.load_students()

    student_id = get_non_empty_input("Enter Student ID to search: ")
    _, student = _find_by_id(students, student_id)

    if student:
        print_info("--- Student Found ---")
        _print_student(student)
    else:
        print_error(f"No student found with ID '{student_id}'.")


def search_student_by_name():
    students = file_handler.load_students()

    query = get_non_empty_input("Enter Student Name to search: ").lower()
    matches = [s for s in students if query in s["name"].lower()]

    if matches:
        print_info(f"--- {len(matches)} Match(es) Found ---")
        for s in matches:
            _print_student(s)
    else:
        print_error(f"No student found with name matching '{query}'.")


def update_student():
    students = file_handler.load_students()

    student_id = get_non_empty_input("Enter Student ID to update: ")
    index, student = _find_by_id(students, student_id)

    if not student:
        print_error(f"No student found with ID '{student_id}'.")
        return

    print_info("--- Updating Student (press Enter to keep current value) ---")
    _print_student(student)

    new_name = input(f"New Name [{student['name']}]: ").strip()
    new_age_raw = input(f"New Age [{student['age']}]: ").strip()
    new_course = input(f"New Course [{student['course']}]: ").strip()

    if new_name:
        student["name"] = new_name

    if new_age_raw:
        try:
            new_age = int(new_age_raw)
            if 1 <= new_age <= 120:
                student["age"] = new_age
            else:
                print_error("Age out of realistic range; keeping previous age.")
        except ValueError:
            print_error("Invalid age entered; keeping previous age.")

    if new_course:
        student["course"] = new_course

    students[index] = student

    if file_handler.save_students(students):
        print_success(f"Student '{student['student_id']}' updated successfully.")
    else:
        print_error("Failed to save the updated student record.")


def delete_student():
    students = file_handler.load_students()

    student_id = get_non_empty_input("Enter Student ID to delete: ")
    index, student = _find_by_id(students, student_id)

    if not student:
        print_error(f"No student found with ID '{student_id}'.")
        return

    _print_student(student)
    if confirm_action(f"Are you sure you want to delete student '{student['student_id']}'?"):
        students.pop(index)
        if file_handler.save_students(students):
            print_success("Student record deleted successfully.")
        else:
            print_error("Failed to save changes after deletion.")
    else:
        print_info("Deletion cancelled.")


def view_own_profile(student_id):
    students = file_handler.load_students()
    _, student = _find_by_id(students, student_id)

    print_info("--- My Profile ---")
    if student:
        _print_student(student)
    else:
        print_error("Your linked student record could not be found. Please contact an administrator.")
