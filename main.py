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
            print("You can see the list of all students from choosing 3 on the menu.")
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

def record_grade():
    # Get the student ID from the user
    while True:
        print("\nPlease enter the ID of the student that you want to enter the grade.")
        student_id = input("> ").strip()
        try:
            student_id = int(student_id)
            break
        except:
            print("Student ID must be an integer.")
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
            print("You can see the list of all students from choosing 3 on the menu.")
            return
        else:
            print("Please enter Yes or No")
            continue
    # Get the standard number from the user
    while True:
        print("\nPlease enter the number of the standard")
        standard_number = input("> ").strip()
        try:
            standard_number = int(standard_number)
            # Look for the NZQA standard in the database
            cursor.execute("SELECT standard_type, level, domain, title, credits, assessment_type FROM standard WHERE standard_number = ?", (standard_number,))
            standard = cursor.fetchone()
            if not standard:
                print("Standard not found.")
                continue
            st_type, level, domain, title, credits, assess_type = standard
            # Check if the user matches the standard they are looking for
            print(f"\nDo you mean {st_type} Standard - Level {level} {domain} - {title} - {credits} {assess_type} Credit(s)?")
            answer = input("Yes or No > ").strip().lower()
            if answer == "yes":
                break
            if answer == "no":
                print("Please try again")
                continue
            else:
                print("Please enter Yes or No")
                continue
        except:
            print("Standard No. must be an integer.")
    # Check if the student already has the grade of that standard
    cursor.execute("SELECT score FROM student_standard_grade WHERE student_id = ? AND standard_number = ?", (student_id, standard_number))
    exist = cursor.fetchone()
    if exist:
        current_score = exist[0]
        cursor.execute("SELECT name FROM grade WHERE score = ?", (current_score, ))
        current_name = cursor.fetchone()[0]
        print(f"\nWarning: {student[0]} {student[1]} already has a score of {current_score}, {current_name} for standard {standard_number}.")
        while True:
            # Ask user to replace or not
            print("Do you want to replace it with a new score?")
            answer = input("Yes or No > ").strip().lower()
            if answer == 'yes':
                while True:
                    print('\nPlease enter the new score (0 to 8)')
                    score = input("> ").strip()
                    try:
                        score = int(score)
                        if 0 <= score <= 8:
                            break
                        else:
                            print("Score must be between 0 and 8")
                            continue
                    except:
                        print('Score must be an integer')
                cursor.execute("UPDATE student_standard_grade SET score = ? WHERE student_id = ? ND standard_number = ?", (score, student_id, standard_number))
                db.commit()
            elif answer == 'no':
                print("Operation cancelled by user")
                return
            else:
                print("Please enter Yes or No")
    else:
        # Get the score from the user
        while True:
            print("\nPlease enter the score (0 to 8)")
            score = input("> ").strip()
            try:
                score = int(score)
                if score < 0 or score > 8:
                    print("Score must between 0 to 8")
                else:
                    break
            except:
                print("Score must be an integer.")
        cursor.execute("INSERT INTO student_standard_grade (student_id, standard_number, score) VALUES (?, ?, ?)", (student_id, standard_number, score))
        db.commit()
        # Automatically bring the name of the grade based on the score
        cursor.execute("SELECT name FROM grade WHERE score = ?", (score,))
        result = cursor.fetchone()
        grade_name = result[0]
        # Print the result
        print(f"\nCompleted! {student[0]} {student[1]} got {score}, which means {grade_name} in {standard_number}, {title}")

def remove_grade():
    # Get the student ID from the user
    while True:
        print("\nPlease enter the ID of the student that you want to remove the grade.")
        student_id = input("> ").strip()
        try:
            student_id = int(student_id)
            break
        except:
            print("Student ID must be an integer.")
    cursor.execute("SELECT first_name, last_name FROM student WHERE student_id = ?", (student_id,))
    student = cursor.fetchone()
    if not student:
        print("Student not found.")
        return
    # Check if the user matches the person they are looking for.
    while True:
        print(f"\nAre you looking for {student[0]} {student[1]}?")
        answer = input("Yes or No > ").strip().lower()
        if answer == "yes":
            break
        elif answer == "no":
            print("Please try again from the beginning")
            print("You can see the list of all students from choosing 3 on the menu.")
            return
        else:
            print("Please enter Yes or No")
            continue
    # Get the standard number from the user
    while True:
        print("\nPlease enter the number of the standard")
        standard_number = input("> ").strip()
        try:
            standard_number = int(standard_number)
            # Look for the NZQA standard in the database
            cursor.execute("SELECT standard_type, level, domain, title, credits, assessment_type FROM standard WHERE standard_number = ?", (standard_number,))
            standard = cursor.fetchone()
            if not standard:
                print("Standard not found.")
                continue
            st_type, level, domain, title, credits, assess_type = standard
            # Check if the user matches the standard they are looking for
            print(f"\nDo you mean {st_type} Standard - Level {level} {domain} - {title} - {credits} {assess_type} Credit(s)?")
            answer = input("Yes or No > ").strip().lower()
            if answer == "yes":
                break
            if answer == "no":
                print("Please try again")
                continue
            else:
                print("Please enter Yes or No")
                continue
        except:
            print("Standard No. must be an integer.")
    cursor.execute("SELECT score FROM student_standard_grade WHERE student_id = ? AND standard_number = ?", (student_id, standard_number, ))
    exist = cursor.fetchone()
    if not exist:
        print(f"\n{student[0]} {student[1]} does not have any grade recorded for standard {standard_number} yet.")
        print("Please try again after the student's grade is recorded")
        return
    else:
        score = exist[0]
        cursor.execute("SELECT name FROM grade WHERE score = ?", (score, ))
        grade_name = cursor.fetchone()[0]
        print(f"\nWe found the record that {student[0]} {student[1]} has {score}, which means {grade_name} for standard {standard_number}!")
        while True:
            print(f'\nAre you sure you want to remove {student[0]} {student[1]} grade for standard {standard_number}?')
            print(f'If you remove the record, it cannot be canceled.')
            answer = input("Yes or No > ").strip().lower()
            if answer == "yes":
                cursor.execute("DELETE FROM student_standard_grade WHERE student_id = ? AND standard_number = ?", (student_id, standard_number, ))
                db.commit()
                print("\nCompleted! The grade record of the student has been removed.")
            elif answer == "no":
                print("Operation cancelled by user")
                return
            else:
                print("Please enter Yes or No")
                continue

def standard_detail():
    # Get the standard number from the user
    while True:
        print("\nPlease enter the number of the standard that you want to see the data")
        standard_number = input("> ").strip()
        try:
            standard_number = int(standard_number)
            # Look for the NZQA standard in the database
            cursor.execute("SELECT standard_type, level, domain, title, credits, assessment_type FROM standard WHERE standard_number = ?", (standard_number,))
            standard = cursor.fetchone()
            if not standard:
                print("Standard not found.")
                continue
            st_type, level, domain, title, credits, assess_type = standard
            # Check if the user matches the standard they are looking for
            print(f"\nDo you mean {st_type} Standard - Level {level} {domain} - {standard_number} {title} - {credits} {assess_type} Credit(s)?")
            answer = input("Yes or No > ").strip().lower()
            if answer == "yes":
                break
            if answer == "no":
                print("Please try again")
                continue
            else:
                print("Please enter Yes or No")
                continue
        except:
            print("Standard No. must be an integer.")
    # Ask user what data that user wants to get
    while True:
        print(f"\nWhat would you like to do for Standard: {standard_number} - {title}")
        print("1. See all students who got Excellence")
        print("2. See all students who got Merit")
        print("3. See all students who got Achievement")
        print("4. See all students who got Not Achieved")
        print("5. See all students who did not submit the assessment")
        print("6. Pass rate of this standard")
        answer = input("> ").strip()
        if answer in {"1", "2", "3", "4", "5", "6"}:
            break
        else:
            print("INVALID INPUT, please enter the integer between 1 - 6")
    # If user choose the data of the students' grade list
    if answer in {"1", "2", "3", "4", "5"}:
        # Define the low and high grade scale, and name of the grade
        if answer == "1":
            low, high, grad = 7, 8, "Excellence"
        if answer == "2":
            low, high, grad = 5, 6, "Merit"
        if answer == "3":
            low, high, grad = 3, 4, "Achievement"
        if answer == "4":
            low, high, grad = 1, 2, "Not Achieved"
        if answer == "5":
            low, high, grad = 0, 0, "Not Submitted"
        # Find the students from the database
        cursor.execute("""SELECT
                       student_standard_grade.student_id, 
                       student.first_name, 
                       student.last_name, 
                       student_standard_grade.score, 
                       grade.name 
                       FROM student_standard_grade 
                       JOIN student 
                       ON student.student_id = student_standard_grade.student_id 
                       JOIN grade 
                       ON grade.score = student_standard_grade.score 
                       WHERE student_standard_grade.standard_number = ? 
                       AND student_standard_grade.score 
                       BETWEEN ? AND ?""", (standard_number, low, high))
        rows = cursor.fetchall()
        # Print the students from the database
        if rows:
            headers = ["ID", "First Name", "Last Name", "Score", "grade"]
            print(f'\nstudents who got {grad} on Standard {standard_number}:')
            print(tabulate(rows, headers=headers, tablefmt="fancy_grid"))
        else:
            print(f"\nNo students found with {grad} on Standard {standard_number}.")
    # If use choose the pass rate data
    if answer == "6":
        cursor.execute("SELECT COUNT(*) FROM student_standard_grade WHERE standard_number = ?", (standard_number,))
        total_attempted = cursor.fetchone()[0]
        if total_attempted == 0:
            print(f"\nNo one has attempted Standard {standard_number} yet.")
        else:
            cursor.execute("SELECT COUNT(*) FROM student_standard_grade WHERE standard_number = ? AND score >= 3", (standard_number, ))
            total_passed = cursor.fetchone()[0]
            pass_rate = round(total_passed / total_attempted * 100, 2)
            print(f"\nPass rate for Standard {standard_number}: {pass_rate}%, ({total_passed}/{total_attempted})")

def student_detail():
    # Get the student ID from the user
    while True:
        print("\nPlease enter the ID of the student that you want to see the data")
        student_id = input("> ").strip()
        try:
            student_id = int(student_id)
            break
        except:
            print("Student ID must be an integer.")
    cursor.execute("SELECT first_name, last_name FROM student WHERE student_id = ?", (student_id,))
    student = cursor.fetchone()
    if not student:
        print("Student not found.")
        return
    # Check if the user matches the person they are looking for.
    while True:
        print(f"\nAre you looking for {student[0]} {student[1]}?")
        answer = input("Yes or No > ").strip().lower()
        if answer == "yes":
            break
        elif answer == "no":
            print("Please try again from the beginning")
            print("You can see the list of all students from choosing 3 on the menu.")
            return
        else:
            print("Please enter Yes or No")
            continue
    while True:
        print(f"\nWhat would you like to do for {student[0]} {student[1]}?")
        print("1. View All Standards Results")
        print("2. View All Achievement Standards Results")
        print("3. View All Unit Standards results")
        print("4. View Student's All Standards Pass Rate")
        answer = input("> ").strip()
        if answer in {"1", "2", "3", "4"}:
            break
        else:
            print("INVALID INPUT, please enter the integer between 1 - 4")
    if answer == "1":
        cursor.execute("""SELECT
                       student_standard_grade.standard_number,
                       standard.standard_type,
                       standard.level
                       standard.domain
                       standard.title
                       student_standard_grade.score
                       grade.name
                       FROM student_standard_grade
                       JOIN standard
                       ON student_standard_grade.standard_number = standard.standard_number
                       JOIN grade
                       ON student_standard_grade.score = grade.score
                       WHERE student_standard_grade.student_id = ?
                       ORDER BY student_standard_grade.standard_number""", (student_id, ))
        result = cursor.fetchall()
        if result:
            headers = ["Standard No.", "Type", "Level", "Domain", "Title", "Score", "Grade"]
            print(tabulate(result, headers = headers, tablefmt = "fancy_grid"))
        else:
            print("No standards result found for this student.")
            return
    elif answer == "2":
        cursor.execute("""SELECT
                       student_standard_grade.standard_number,
                       standard.standard_type,
                       standard.level
                       standard.domain
                       standard.title
                       student_standard_grade.score
                       grade.name
                       FROM student_standard_grade
                       JOIN standard
                       ON student_standard_grade.standard_number = standard.standard_number
                       JOIN grade
                       ON student_standard_grade.score = grade.score
                       WHERE student_standard_grade.student_id = ?
                       AND standard.standard_type = 'Achievement Standard'
                       ORDER BY student_standard_grade.standard_number""", (student_id, ))
        result = cursor.fetchall()
        if result:
            headers = ["Standard No.", "Type", "Level", "Domain", "Title", "Score", "Grade"]
            print(tabulate(result, headers = headers, tablefmt = "fancy_grid"))
        else:
            print("No Achievement Standards result found for this student.")
            return
    elif answer == "3":
        cursor.execute("""SELECT
                       student_standard_grade.standard_number,
                       standard.standard_type,
                       standard.level
                       standard.domain
                       standard.title
                       student_standard_grade.score
                       grade.name
                       FROM student_standard_grade
                       JOIN standard
                       ON student_standard_grade.standard_number = standard.standard_number
                       JOIN grade
                       ON student_standard_grade.score = grade.score
                       WHERE student_standard_grade.student_id = ?
                       AND standard.standard_type = 'Unit Standard'
                       ORDER BY student_standard_grade.standard_number""", (student_id, ))
        result = cursor.fetchall()
        if result:
            headers = ["Standard No.", "Type", "Level", "Domain", "Title", "Score", "Grade"]
            print(tabulate(result, headers = headers, tablefmt = "fancy_grid"))
        else:
            print("No Unit Standards result found for this student.")
            return
    elif answer == "4":
        cursor.execute("SELECT COUNT(*) FROM student_standard_grade WHERE student_id = ?", (student_id, ))
        total_attempted = cursor.fetchone()[0]
        if total_attempted == 0:
            print("This student has not attempted any standards yet.")
            return
        cursor.execute("SELECT COUNT(*) FROM student_standard_grade WHERE student_id = ? AND score >= 3", (student_id, ))
        total_passed = cursor.fetchone()[0]
        pass_rate = round(total_passed / total_attempted * 100, 2)
        print(f"\nPass rate of {student[0]} {student[1]}: {pass_rate}%, ({total_passed}/{total_attempted})")

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
            continue
        elif answer == "6":
            standard_detail()
            continue
        elif answer == "7":
            student_detail()
            continue
        elif answer == "8":
            break
        elif answer == "9":
            print("\nNeed Help?")
            print("Please contact kangl@stu.otc.school.nz anytime you need help")
            print("We would be happy to help in 2 businesses days.")
        else:
            print("INVALID INPUT")
            continue

if __name__ == "__main__":
    main()