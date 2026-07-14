import os
import re
import string

# just some helper stuff i use everywhere so i dont repeat myself

def clear_screen():
    os.system("cls" if os.name=="nt" else "clear")

def print_header(title):
    print("\n"+"="*50)
    print(title.center(50))
    print("="*50)

def print_divider():
    print("-" * 50)

def pause():
    input("\nPress Enter to continue...")


def print_success(msg):
    print(f"\n[SUCCESS] {msg}")

def print_error(msg):
    print(f'\n[ERROR] {msg}')

def print_info(msg):
    print(f"\n[INFO] {msg}")


def confirm_action(prompt="Are you sure?"):
    ans = input(prompt + " (y/n): ").strip().lower()
    return ans in ("y", "yes")


def get_non_empty_input(prompt):
    # keep asking till they actually type something
    while True:
        val = input(prompt).strip()
        if val:
            return val
        print_error("This field cannot be empty. Please try again.")


def get_valid_age(prompt="Enter Age: "):
    while True:
        raw = input(prompt).strip()
        if not raw:
            print_error("Age cannot be empty.")
            continue
        try:
            age = int(raw)
        except ValueError:
            print_error("Age must be a whole number (e.g. 21).")
            continue

        if age <= 0 or age > 120:
            print_error("Please enter a realistic age between 1 and 120.")
            continue
        return age


PASSWORD_SPECIAL_CHARS = string.punctuation

PASSWORD_POLICY_DESCRIPTION = "Password must be at least 8 characters long and include at least 1 uppercase letter, 1 lowercase letter, 1 digit, and 1 special character (e.g. !@#$%^&*)."

def validate_password_strength(password):
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not re.search(r"[A-Z]", password):
        return False,"Password must include at least 1 uppercase letter."
    if not re.search(r"[a-z]", password):
        return False, "Password must include at least 1 lowercase letter."
    if not re.search(r"[0-9]", password):
        return False, "Password must include at least 1 digit."
    if not any(c in PASSWORD_SPECIAL_CHARS for c in password):
        return False, "Password must include at least 1 special character (e.g. !@#$%^&*)."
    return True, ""


def get_valid_password(prompt="Choose a Password: "):
    print_info(PASSWORD_POLICY_DESCRIPTION)
    while True:
        pwd = input(prompt).strip()
        ok, reason = validate_password_strength(pwd)
        if ok:
            return pwd
        print_error(reason)


def get_menu_choice(prompt, valid_choices):
    valid_choices = set(valid_choices)
    while True:
        choice = input(prompt).strip()
        if choice in valid_choices:
            return choice
        print_error("Invalid option. Please choose one of: " + ", ".join(sorted(valid_choices)))
