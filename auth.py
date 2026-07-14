import hashlib

import file_handler
from utils import (
    get_non_empty_input,
    get_valid_password,
    get_menu_choice,
    print_error,
    print_success,
    print_info,
    print_divider,
    confirm_action,
)


class Session:
    # basically just keeps track of who is logged in right now
    def __init__(self):
        self.username = None
        self.role = None
        self.student_id = None

    def start(self, username, role, student_id=None):
        self.username = username
        self.role = role
        self.student_id = student_id

    def end(self):
        self.username = None
        self.role = None
        self.student_id = None

    def is_logged_in(self):
        return self.username is not None

    def is_admin(self):
        return self.role == "admin"

    def is_student(self):
        return self.role == "student"


def hash_password(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def _find_user(users, username):
    uname_lower = username.lower()
    for u in users:
        if u["username"].lower() == uname_lower:
            return u
    return None


def register_user():
    # public registration - only students, admins get added separately
    users = file_handler.load_users()

    print_info("--- Student Registration ---")
    username = get_non_empty_input("Choose a Username: ")

    if _find_user(users, username):
        print_error(f"Username '{username}' is already taken. Please try again.")
        return

    password = get_valid_password("Choose a Password: ")

    students = file_handler.load_students()
    student_id = get_non_empty_input("Enter your existing Student ID (created by an admin): ").upper()
    matching_student = next((s for s in students if s["student_id"].upper() == student_id), None)
    if not matching_student:
        print_error("No student record found with that ID. Ask an admin to add your record first, then register again.")
        return

    already_linked = any(u.get("role") == "student" and u.get("student_id", "").upper() == student_id for u in users)
    if already_linked:
        print_error("An account is already registered for this Student ID.")
        return

    new_user = {
        "username": username,
        "password_hash": hash_password(password),
        "role": "student",
        "student_id": student_id,
    }
    users.append(new_user)

    if file_handler.save_users(users):
        print_success(f"Account '{username}' registered successfully as student.")
    else:
        print_error("Registration failed while saving data. Please try again.")


def register_admin(session):
    # only an admin can add another admin, that was a requirement
    if not session.is_admin():
        print_error("Only an admin can register a new admin account.")
        return

    users = file_handler.load_users()

    print_info("--- Register New Admin ---")
    username = get_non_empty_input("New Admin Username: ")

    if _find_user(users, username):
        print_error(f"Username '{username}' is already taken. Please try again.")
        return

    password = get_valid_password("New Admin Password: ")

    new_admin = {
        "username": username,
        "password_hash": hash_password(password),
        "role": "admin",
        "student_id": None,
    }
    users.append(new_admin)

    if file_handler.save_users(users):
        print_success(f"Admin account '{username}' created successfully.")
    else:
        print_error("Failed to save the new admin account. Please try again.")


def promote_user_to_admin(session):
    if not session.is_admin():
        print_error("Only an admin can promote a user to admin.")
        return

    users = file_handler.load_users()
    promotable = [u for u in users if u.get("role") != "admin"]

    print_info("--- Promote User to Admin ---")
    if not promotable:
        print_error("There are no non-admin accounts available to promote.")
        return

    print_divider()
    for u in promotable:
        print(f"Username: {u['username']}  |  Role: {u['role']}")
    print_divider()

    username = get_non_empty_input("Enter the username to promote to admin: ")
    target_user = _find_user(promotable, username)

    if not target_user:
        print_error(f"No non-admin account found with username '{username}'.")
        return

    if not confirm_action(f"Promote '{target_user['username']}' to admin?"):
        print_info("Promotion cancelled.")
        return

    target_user["role"] = "admin"

    if file_handler.save_users(users):
        print_success(f"'{target_user['username']}' has been promoted to admin.")
    else:
        print_error("Failed to save the promotion. Please try again.")


def login_user(session):
    users = file_handler.load_users()

    print_info("--- User Login ---")
    username = get_non_empty_input("Username: ")
    password = get_non_empty_input("Password: ")

    user = _find_user(users, username)
    if not user or user["password_hash"] != hash_password(password):
        print_error("Invalid username or password.")
        return False

    session.start(user["username"], user["role"], user.get("student_id"))
    print_success(f"Welcome, {user['username']}! Logged in as {user['role']}.")
    return True


def logout_user(session):
    if session.is_logged_in():
        print_info(f"Goodbye, {session.username}. You have been logged out.")
        session.end()
    else:
        print_error("No user is currently logged in.")
