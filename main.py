from auth import (
    Session,
    register_user,
    register_admin,
    promote_user_to_admin,
    login_user,
    logout_user,
)
from student import (
    add_student,
    view_all_students,
    search_student_by_id,
    search_student_by_name,
    update_student,
    delete_student,
    view_own_profile,
)
from utils import print_header, print_info, print_error, get_menu_choice, pause


def admin_menu(session):
    while True:
        print_header(f"ADMIN MENU  (User: {session.username})")
        print("1. Add Student")
        print("2. View All Students")
        print("3. Search Student by ID")
        print("4. Search Student by Name")
        print("5. Update Student")
        print("6. Delete Student")
        print("7. Register New Admin")
        print("8. Promote User to Admin")
        print("9. Logout")

        choice = get_menu_choice("Select an option: ", [str(i) for i in range(1, 10)])

        try:
            if choice == "1":
                add_student()
            elif choice == "2":
                view_all_students()
            elif choice == "3":
                search_student_by_id()
            elif choice == "4":
                search_student_by_name()
            elif choice == "5":
                update_student()
            elif choice == "6":
                delete_student()
            elif choice == "7":
                register_admin(session)
            elif choice == "8":
                promote_user_to_admin(session)
            elif choice == "9":
                logout_user(session)
                pause()
                return
        except Exception as e:
            # dont want one bad input to crash the whole app
            print_error(f"An unexpected error occurred: {e}")

        pause()


def student_menu(session):
    while True:
        print_header(f"STUDENT MENU  (User: {session.username})")
        print("1. View My Profile")
        print("2. Logout")

        choice = get_menu_choice("Select an option: ", ["1", "2"])

        try:
            if choice == "1":
                view_own_profile(session.student_id)
            elif choice == "2":
                logout_user(session)
                pause()
                return
        except Exception as e:
            print_error(f"An unexpected error occurred: {e}")

        pause()


def main_menu(session):
    while True:
        print_header("STUDENT MANAGEMENT SYSTEM")
        print("1. Register (Student)")
        print("2. Login")
        print("3. Exit")

        choice = get_menu_choice("Select an option: ", ["1", "2", "3"])

        try:
            if choice == "1":
                register_user()
                pause()

            elif choice == "2":
                if login_user(session):
                    pause()
                    if session.is_admin():
                        admin_menu(session)
                    elif session.is_student():
                        student_menu(session)
                else:
                    pause()

            elif choice == "3":
                print_info("Thank you for using the Student Management System. Goodbye!")
                break

        except Exception as e:
            print_error(f"An unexpected error occurred: {e}")
            pause()


def main():
    session = Session()
    try:
        main_menu(session)
    except KeyboardInterrupt:
        print_info("\nProgram interrupted by user. Exiting safely.")
    except Exception as e:
        print_error(f"A fatal unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
