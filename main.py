import sqlite3
from tabulate import tabulate

# Connect to the database
db = sqlite3.connect("Grade-Tracker.db")
cursor = db.cursor()

# Function to ENROL student
def enrol_student():
    # Get First Name from the user
    while True:
        print("\nPlease enter the FIRST NAME of the student:")
        first_name = input("> ").strip().title()
        if not first_name:
            print("You have to enter the first name.")
        elif any(char.isdigit() for char in first_name):
            print("You may not include any integer in the first name.")
        else:
            break
    # Get Last Name from the user
    while True:
        print("\nPlease enter the LAST NAME of the student:")
        last_name = input("> ").strip().title()
        if not last_name:
            print("You have to enter the last name.")
        elif any(char.isdigit() for char in last_name):
            print("You may not include any integer in the last name.")
        else:
            break
    # Upload it to the database
    while True:
        # Give a chance to user to cancel the operation
        print(f'\nAre you sure you want to enrol {first_name} {last_name}?')
        answer = input("Yes or No > ").strip().lower()
        if answer == 'yes':
            cursor.execute("INSERT INTO student (first_name, last_name) VALUES (?, ?)", (first_name, last_name))
            db.commit()
            student_id = cursor.lastrowid
            print(f"\nCompleted! We enrol {first_name} {last_name} to our tracker. The ID of the {first_name} {last_name} is {student_id}.")
            return
        elif answer == 'no':
            print("Operation cancelled by user")
            return
        else:
            print("Please enter Yes or No")
            continue            

# Function to UNENROL student
def unenrol_student():
    # Get the student ID from the user
    while True:
        print("\nPlease enter the ID of the student that you want to enrol")
        student_id = input("> ").strip()
        try:
            student_id = int(student_id)
            break
        except:
            print("Student ID must be an integer.")
            continue
    cursor.execute("SELECT first_name, last_name FROM student WHERE student_id = ?", (student_id,))
    student = cursor.fetchone()
    if not student:
        print("Student not found.")
        return
    # Check if the user matches the person they are looking for
    while True:
        print(f"\nAre you looking for {student[0]} {student[1]}?")
        answer = input("Yes or No > ").strip().lower()
        if answer == "yes":
            break
        elif answer == "no":
            print("Please try again from the beginning")
            print("You can see the list of all students from choosing 2 on the menu.")
            return
        else:
            print("Please enter Yes or No")
            continue
    # Give a chance to a user to cancel the operation
    while True:
        print(f'\nAre you sure you want to remove {student[0]} {student[1]} (ID={student_id})?')
        print(f'If you unenrol the student, all informations would be deleted from the database and it cannot be canceled.')
        answer = input("Yes or No > ").strip().lower()
        if answer == 'yes':
            cursor.execute("DELETE FROM student_standard_grade WHERE student_id = ?", (student_id, ))
            cursor.execute("DELETE FROM student WHERE student_id = ?", (student_id, ))
            db.commit()
            print(f"\nCompleted! {student[0]} {student[1]} (ID={student_id}) has been removed from the tracker.")
            return
        elif answer == 'no':
            print("Operation cancelled by user")
            return
        else:
            print("Please enter Yes or No")
            continue

def show_all_students():
    # Select all students and print it to user
    cursor.execute("SELECT * FROM student")
    rows = cursor.fetchall()
    if rows:
        headers = [description[0] for description in cursor.description]
        print(tabulate(rows, headers = headers, tablefmt = "fancy_grid"))
    else:
        print("No students found. Please enrol student first.")

# Menu Function
def main():
    print("\nKia ora, welcome to Student Grade Tracker")
    while True:
        print("\nWhat would you like to do?")
        print("1. Enrol a new student")
        print("2. Unenrol an existing student")
        print("3. Show all Students")
        print("4. Record student's Grade")
        print("5. Remove the recorded grade")
        print("6. Standard Result Information, Pass Rate")
        print("7. Student Grade Information, Pass Rate")
        print("8. Exit")
        print("9. Help")

        answer = input("> ").strip()
        if answer == "1":
            enrol_student()
            continue
        elif answer == "2":
            unenrol_student()
            continue
        elif answer == "3":
            show_all_students()
            continue
        elif answer == "4":
            record_grade()
            continue
        elif answer == "5":
            remove_grade()
        elif answer == "6":
            standard_detail()
        elif answer == "7":
            student_detail()
        elif answer == "8":
            break
        elif answer == "8":
            print("\nNeed Help?")
            print("Please contact kangl@stu.otc.school.nz anytime you need help!")
            print("We would be happy to help in 2 working days.")
        else:
            print("INVALID INPUT")
            continue

if __name__ == "__main__":
    main()