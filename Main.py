import os
import re
from datetime import datetime

class_file = "class_timetable.txt"
exam_file = "exam_schedule.txt"
report_file_name = "report.txt"

VALID_DAYS = [
    "Monday", "Tuesday", "Wednesday", "Thursday",
    "Friday", "Saturday", "Sunday"
]

def load_data(file):
    """Reads data from a file and converts each line into a list of values."""
    if os.path.exists(file):
        with open(file, "r") as f:
            return [line.strip().split(",") for line in f.readlines() if line.strip()]
    return []


def save_data(file, data):
    """Writes list data back to a file to ensure persistence."""
    with open(file, "w") as f:
        for item in data:
            f.write(",".join(item) + "\n")


class_timetable = load_data(class_file)
exam_schedule = load_data(exam_file)

def get_non_empty_input(prompt):
    """Keeps asking until the user provides a non-blank value."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Input cannot be empty. Please try again.")


def get_course_code(prompt):
    """Course code must be alphanumeric, e.g. CS101, SE-204."""
    while True:
        code = input(prompt).strip().upper()
        if re.fullmatch(r"[A-Z0-9\-]{2,15}", code):
            return code
        print("Invalid course code. Use letters/numbers only (e.g., CS101).")


def get_valid_day(prompt):
    while True:
        day = input(prompt).strip().title()
        if day in VALID_DAYS:
            return day
        print(f"Invalid day. Choose from: {', '.join(VALID_DAYS)}")


def get_valid_time(prompt):
    """Accepts times like 10:00 AM / 02:30 PM."""
    while True:
        time_str = input(prompt).strip().upper()
        try:
            datetime.strptime(time_str, "%I:%M %p")
            return time_str
        except ValueError:
            print("Invalid time format. Use HH:MM AM/PM (e.g., 10:00 AM).")


def get_valid_date(prompt):
    """Accepts dates like 25/12/2025 (DD/MM/YYYY)."""
    while True:
        date_str = input(prompt).strip()
        try:
            datetime.strptime(date_str, "%d/%m/%Y")
            return date_str
        except ValueError:
            print("Invalid date format. Use DD/MM/YYYY (e.g., 25/12/2025).")


def get_room_number(prompt):
    while True:
        room = input(prompt).strip().upper()
        if re.fullmatch(r"[A-Z0-9\-]{1,10}", room):
            return room
        print("Invalid room number. Use letters/numbers only (e.g., A101).")


def course_code_exists(code):
    """Verification: checks if a course code already exists in either list."""
    for cls in class_timetable:
        if cls[0] == code:
            return True
    for exam in exam_schedule:
        if exam[0] == code:
            return True
    return False


def get_valid_menu_choice(prompt, valid_choices):
    while True:
        choice = input(prompt).strip()
        if choice in valid_choices:
            return choice
        print(f"Invalid choice. Please enter one of: {', '.join(valid_choices)}")

def display_menu():
    print("\n===== UCP Class Timetable & Exam Management System =====")
    print("1. Add Class Schedule")
    print("2. View Class Timetable")
    print("3. Add Exam Schedule")
    print("4. View Exam Schedule")
    print("5. Update Class or Exam Details")
    print("6. Search Timetable or Exam")
    print("7. Detect Schedule Clashes")
    print("8. Generate Reports")
    print("9. Exit")

def add_class():
    print("\n--- Add Class Schedule ---")
    course_code = get_course_code("Enter Course Code: ")

    if course_code_exists(course_code):
        confirm = input(
            f"Course code '{course_code}' already exists. Add anyway? (y/n): "
        ).strip().lower()
        if confirm != "y":
            print("Class entry cancelled.")
            return

    course_name = get_non_empty_input("Enter Course Name: ")
    instructor = get_non_empty_input("Enter Instructor Name: ")
    day = get_valid_day("Enter Day (e.g., Monday): ")
    time = get_valid_time("Enter Time (e.g., 10:00 AM): ")
    room = get_room_number("Enter Room Number: ")

    for cls in class_timetable:
        if cls[3] == day and cls[4] == time and cls[5] == room:
            print("Warning: This room is already booked at this day/time!")
            confirm = input("Add anyway? (y/n): ").strip().lower()
            if confirm != "y":
                print("Class entry cancelled.")
                return
            break

    class_timetable.append([course_code, course_name, instructor, day, time, room])
    save_data(class_file, class_timetable)
    print("Class added successfully and saved!")

def view_class_timetable():
    print("\n===== Class Timetable =====")
    if not class_timetable:
        print("No classes scheduled.")
    else:
        for cls in class_timetable:
            if len(cls) < 6:
                continue  # skip corrupted rows
            print(f"Course: {cls[0]} - {cls[1]} | Instructor: {cls[2]} | "
                  f"Day: {cls[3]} | Time: {cls[4]} | Room: {cls[5]}")

def add_exam():
    print("\n--- Add Exam Schedule ---")
    course_code = get_course_code("Enter Course Code: ")

    exam_date = get_valid_date("Enter Exam Date (DD/MM/YYYY): ")
    start_time = get_valid_time("Enter Start Time: ")
    end_time = get_valid_time("Enter End Time: ")

    while datetime.strptime(end_time, "%I:%M %p") <= datetime.strptime(start_time, "%I:%M %p"):
        print("End time must be after start time.")
        end_time = get_valid_time("Enter End Time: ")

    hall_number = get_room_number("Enter Exam Hall Number: ")

    for exam in exam_schedule:
        if exam[1] == exam_date and exam[2] == start_time and exam[4] == hall_number:
            print("Warning: This hall is already booked at this date/time!")
            confirm = input("Add anyway? (y/n): ").strip().lower()
            if confirm != "y":
                print("Exam entry cancelled.")
                return
            break

    exam_schedule.append([course_code, exam_date, start_time, end_time, hall_number])
    save_data(exam_file, exam_schedule)
    print("Exam added successfully and saved!")

def view_exam_schedule():
    print("\n===== Exam Schedule =====")
    if not exam_schedule:
        print("No exams scheduled.")
    else:
        for exam in exam_schedule:
            if len(exam) < 5:
                continue  # skip corrupted rows
            print(f"Course Code: {exam[0]} | Date: {exam[1]} | "
                  f"Time: {exam[2]} - {exam[3]} | Hall: {exam[4]}")

def update_details():
    print("\n--- Update Class or Exam Details ---")
    course_code = get_course_code("Enter Course Code to Update: ")

    for cls in class_timetable:
        if cls[0] == course_code:
            print("Class found. Leave a field blank to keep its current value.")
            new_day = input(f"Enter New Day [{cls[3]}]: ").strip().title()
            if new_day:
                if new_day not in VALID_DAYS:
                    print("Invalid day entered. Update cancelled for this field.")
                else:
                    cls[3] = new_day

            new_time = input(f"Enter New Time [{cls[4]}]: ").strip().upper()
            if new_time:
                try:
                    datetime.strptime(new_time, "%I:%M %p")
                    cls[4] = new_time
                except ValueError:
                    print("Invalid time format. Update cancelled for this field.")

            new_room = input(f"Enter New Room [{cls[5]}]: ").strip().upper()
            if new_room:
                if re.fullmatch(r"[A-Z0-9\-]{1,10}", new_room):
                    cls[5] = new_room
                else:
                    print("Invalid room format. Update cancelled for this field.")

            save_data(class_file, class_timetable)
            print("Class details updated and saved!")
            return

    for exam in exam_schedule:
        if exam[0] == course_code:
            print("Exam found. Leave a field blank to keep its current value.")
            new_date = input(f"Enter New Exam Date [{exam[1]}]: ").strip()
            if new_date:
                try:
                    datetime.strptime(new_date, "%d/%m/%Y")
                    exam[1] = new_date
                except ValueError:
                    print("Invalid date format. Update cancelled for this field.")

            new_start = input(f"Enter New Start Time [{exam[2]}]: ").strip().upper()
            new_end = input(f"Enter New End Time [{exam[3]}]: ").strip().upper()
            try:
                start_check = new_start if new_start else exam[2]
                end_check = new_end if new_end else exam[3]
                start_dt = datetime.strptime(start_check, "%I:%M %p")
                end_dt = datetime.strptime(end_check, "%I:%M %p")
                if end_dt <= start_dt:
                    print("End time must be after start time. Times not updated.")
                else:
                    if new_start:
                        exam[2] = new_start
                    if new_end:
                        exam[3] = new_end
            except ValueError:
                print("Invalid time format. Times not updated.")

            new_hall = input(f"Enter New Exam Hall [{exam[4]}]: ").strip().upper()
            if new_hall:
                if re.fullmatch(r"[A-Z0-9\-]{1,10}", new_hall):
                    exam[4] = new_hall
                else:
                    print("Invalid hall format. Update cancelled for this field.")

            save_data(exam_file, exam_schedule)
            print("Exam details updated and saved!")
            return

    print("Course not found!")

def search_schedule():
    print("\n--- Search Timetable or Exam ---")
    search_key = get_non_empty_input("Enter Course Code: ").strip().upper()
    found = False

    for cls in class_timetable:
        if search_key in cls or search_key == cls[0]:
            print(f"Class Found: {cls[0]} - {cls[1]} | Instructor: {cls[2]} | "
                  f"Day: {cls[3]} | Time: {cls[4]} | Room: {cls[5]}")
            found = True

    for exam in exam_schedule:
        if search_key in exam or search_key == exam[0]:
            print(f"Exam Found: {exam[0]} | Date: {exam[1]} | "
                  f"Time: {exam[2]} - {exam[3]} | Hall: {exam[4]}")
            found = True

    if not found:
        print("No matching records found!")

def detect_clashes():
    print("\n--- Detect Schedule Clashes ---")
    clash_found = False

    for i in range(len(class_timetable)):
        for j in range(i + 1, len(class_timetable)):
            if (class_timetable[i][3] == class_timetable[j][3] and
                    class_timetable[i][4] == class_timetable[j][4] and
                    class_timetable[i][5] == class_timetable[j][5]):
                print(f"Class Clash Detected: {class_timetable[i][1]} and "
                      f"{class_timetable[j][1]} on {class_timetable[i][3]} at "
                      f"{class_timetable[i][4]} in Room {class_timetable[i][5]}")
                clash_found = True

    for i in range(len(exam_schedule)):
        for j in range(i + 1, len(exam_schedule)):
            if (exam_schedule[i][1] == exam_schedule[j][1] and
                    exam_schedule[i][2] == exam_schedule[j][2] and
                    exam_schedule[i][4] == exam_schedule[j][4]):
                print(f"Exam Clash Detected: {exam_schedule[i][0]} and "
                      f"{exam_schedule[j][0]} on {exam_schedule[i][1]} at "
                      f"{exam_schedule[i][2]} in Hall {exam_schedule[i][4]}")
                clash_found = True

    if not clash_found:
        print("No clashes found!")

def generate_reports():
    with open(report_file_name, "w") as report_file:
        report_file.write("===== Class Timetable =====\n")
        if not class_timetable:
            report_file.write("No classes scheduled.\n")
        for cls in class_timetable:
            report_file.write(f"Course: {cls[0]} - {cls[1]} | Instructor: {cls[2]} | "
                               f"Day: {cls[3]} | Time: {cls[4]} | Room: {cls[5]}\n")

        report_file.write("\n===== Exam Schedule =====\n")
        if not exam_schedule:
            report_file.write("No exams scheduled.\n")
        for exam in exam_schedule:
            report_file.write(f"Course Code: {exam[0]} | Date: {exam[1]} | "
                               f"Time: {exam[2]} - {exam[3]} | Hall: {exam[4]}\n")

    print(f"Reports generated and saved in '{report_file_name}'!")

def main():
    valid_options = [str(i) for i in range(1, 10)]
    while True:
        display_menu()
        option = get_valid_menu_choice("Enter your choice: ", valid_options)

        if option == '1':
            add_class()
        elif option == '2':
            view_class_timetable()
        elif option == '3':
            add_exam()
        elif option == '4':
            view_exam_schedule()
        elif option == '5':
            update_details()
        elif option == '6':
            search_schedule()
        elif option == '7':
            detect_clashes()
        elif option == '8':
            generate_reports()
        elif option == '9':
            print("Exiting the system. Goodbye!")
            break

if __name__ == "__main__":
    main()