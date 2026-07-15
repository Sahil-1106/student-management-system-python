# Student Management System (Python CLI Capstone Project)

A command line Student Management System built in Python for my capstone project.
Admins can manage student records (add, view, search, update, delete) and students
can log in to check their own profile. Everything is menu driven and data is stored
in JSON files so it persists between runs.

## Features

- Register / Login / Logout with SHA-256 password hashing
- Only admins can create other admins (register new admin or promote an existing student account) - no one can just sign up as admin
- Password policy - min 8 chars, 1 upper, 1 lower, 1 digit, 1 special char
- Student CRUD - add, view all, search by id, search by name, update, delete
- Role based menus (admin gets full access, student only sees their own profile)
- JSON persistence, auto creates files if missing, backs up the file if it somehow gets corrupted instead of just crashing
- Basic input validation everywhere (empty fields, age range, duplicate IDs etc)

## Project Structure

```
student-management-system/
├── main.py           -> entry point, menus or routing between admin/student
├── auth.py            -> login/register/logout, password hashing, session
├── student.py          -> add/view/search/update/delete student
├── file_handler.py     -> reading and writing the json files
├── utils.py            -> small helper functions (prompts, validation etc)
├── users.json
├── students.json
├── README.md
└── requirements.txt
```

## System Design

The system is split into 5 modules so each file has one job and nothing is too tangled together:

- **main.py** - this is basically the controller. it decides which menu to show depending on who is logged in (admin/student) and calls functions from the other modules. it doesn't really contain any business logic itself, just routing + a try/except around each action so the whole program doesn't crash from one bad input.
- **auth.py** - handles everything related to accounts. registration (student only, self-service), login, logout, hashing passwords with SHA-256, and a small `Session` class that just keeps track of who's currently logged in and what role they have. admin creation lives here too but its locked behind `session.is_admin()` checks.
- **student.py** - all the CRUD stuff for student records. doesn't know or care about authentication, it just operates on the students list assuming whoever called it is already allowed to.
- **file_handler.py** - the only place that actually touches the json files. everything else goes through this so if i ever wanted to swap json for a real database later, this is the only file that would need to change.
- **utils.py** - random helper functions used everywhere, mostly around getting valid input from the user and printing consistent looking messages.

Data flow is basically: main.py -> auth.py/student.py -> file_handler.py -> users.json/students.json, and back up again.

### Module Diagram

```
                         +------------------+
                         |     main.py      |
                         |  (menus/routing) |
                         +---------+--------+
                                   |
              +--------------------+--------------------+
              |                    |                     |
        +-----v-----+       +------v------+       +------v------+
        |  auth.py  |       | student.py  |       |  utils.py   |
        | register  |       |  add/view   |       |  prompts +  |
        | login     |       |  search     |       |  validation |
        | logout    |       |  update     |       +-------------+
        | Session   |       |  delete     |
        +-----+-----+       +------+------+
              |                    |
              +---------+----------+
                        |
                 +------v-------+
                 | file_handler |
                 |  load/save   |
                 |  json data   |
                 +------+-------+
                        |
              +---------+----------+
              |                    |
        +-----v-----+       +------v------+
        | users.json|       |students.json|
        +-----------+       +-------------+
```

### Login / Role Flow

```
   Start
     |
     v
[Main Menu] --1--> Register (creates STUDENT account only)
     |
     2
     |
     v
  Login ---> wrong creds --> back to Main Menu
     |
   correct
     |
     v
  role == admin? ----yes----> [Admin Menu] (full CRUD + create/promote admins)
     |
     no
     |
     v
 [Student Menu] (view own profile only)
```

## Getting Started

Needs Python 3.8+, no external packages, everything used is from the standard library (json, hashlib, os, re, string, shutil, datetime).

Run it with:
```bash
python main.py
```

### Sample Login

There's a seeded admin account so you can log in right away:

| Username | Password  | Role  |
|----------|-----------|-------|
| admin    | Admin@123 | admin |

Sample students are already in `students.json` (S001-S004) so you can register a student account against one of these IDs to test the student side:

| Student ID | Name    | Course                  |
|------------|---------|--------------------------|
| S001       | Sahil   | Computer Science         |
| S002       | Prattay | Information Technology   |
| S003       | Pawas   | Data Science             |
| S004       | Kanishk | Electronics Engineering  |

## Usage

1. From the main menu, Register creates a student account - you need an existing Student ID for it to link to (an admin has to add that record first).
2. Login with username/password.
3. If you're an admin you get the full menu - add/view/search/update/delete students, plus register a new admin or promote an existing user to admin.
4. If you're a student you only get to view your own profile.
5. Logout takes you back to the main menu.

Note: since public registration can't make admins anymore, the app ships with one seeded admin account so there's always at least one admin around to create/promote more.

## Data Model

**students.json**
```json
{
    "student_id": "S001",
    "name": "Sahil",
    "age": 20,
    "course": "Computer Science"
}
```

**users.json**
```json
{
    "username": "admin",
    "password_hash": "<sha256 hex digest>",
    "role": "admin",
    "student_id": null
}
```

## Validation / Error Handling

- empty fields get rejected and re-asked
- passwords need to follow the policy (8+ chars, upper, lower, digit, special char)
- age has to be a real number between 1-120
- can't add duplicate student IDs
- can't register duplicate usernames
- a student ID can only be linked to one account
- admin creation/promotion only works if you're already logged in as admin
- missing json files get auto created, corrupted ones get backed up with a timestamp instead of wiping data
- most menu actions are wrapped in try/except in main.py so a weird input doesn't kill the whole program
