import json
import os
import shutil
from datetime import datetime

USERS_FILE = "users.json"
STUDENTS_FILE = "students.json"

# handles reading/writing the json files, also deals with missing/corrupt files


def _load_json_file(filepath):
    if not os.path.exists(filepath):
        _save_json_file(filepath, [])
        return []

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                return []
            data = json.loads(content)
            if not isinstance(data, list):
                raise ValueError("Root JSON element must be a list of records.")
            return data
    except (json.JSONDecodeError, ValueError) as e:
        # if the file is corrupted i dont want to lose everything so backup first
        backup_name = f"{filepath}.corrupt.{datetime.now().strftime('%Y%m%d%H%M%S')}.bak"
        try:
            shutil.copy(filepath, backup_name)
        except OSError:
            backup_name = None

        print(f"\n[WARNING] '{filepath}' contains invalid JSON ({e}).")
        if backup_name:
            print(f"[WARNING] A backup of the corrupted file was saved as '{backup_name}'.")
        print(f"[WARNING] Starting with an empty dataset for '{filepath}'.\n")

        _save_json_file(filepath, [])
        return []


def _save_json_file(filepath, data):
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        return True
    except OSError as e:
        print(f"\n[ERROR] Could not save data to '{filepath}': {e}")
        return False


def load_users():
    return _load_json_file(USERS_FILE)

def save_users(users):
    return _save_json_file(USERS_FILE, users)

def load_students():
    return _load_json_file(STUDENTS_FILE)

def save_students(students):
    return _save_json_file(STUDENTS_FILE, students)
