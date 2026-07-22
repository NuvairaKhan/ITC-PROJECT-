University Class Timetable & Exam Management System
A command-line Python application built for the Introduction to Computing Lab course at the University of Central Punjab (UCP), Lahore. It lets users manage class timetables and exam schedules adding, viewing, updating, searching, and generating reports with all data persisted to text files.

Topics Covered
•	File Handling
•	Lists (Arrays)
•	Loops
•	Built-in Functions
•	Conditionals (if-else statements)

Features
•	Add Class Schedule — enter course code, name, instructor, day, time, and room
•	View Class Timetable — displays all scheduled classes
•	Add Exam Schedule — enter course code, exam date, start/end time, and hall number
•	View Exam Schedule — displays all scheduled exams
•	Update Class or Exam Details — search by course code and edit existing entries
•	Search Timetable or Exam — look up records by course code
•	Detect Schedule Clashes — flags overlapping classes (same day/time/room) or exams (same date/time/hall)
•	Generate Reports — exports the full timetable and exam schedule to report.txt
•	Input Validation — course codes, days, times, dates, and room/hall numbers are all checked before being saved, and duplicate/clashing entries prompt for confirmation

Project Structure
├── Main.py                         # Main application script
├── class_timetable.txt        # Auto-generated: stores class schedule data
├── exam_schedule.txt        # Auto-generated: stores exam schedule data
├── report.txt                       # Auto-generated: output of "Generate Reports"
└── README.md
The .txt data files are created automatically the first time you add a class or exam — you don't need to create them manually.
Requirements
•	Python 3.x (no external libraries required — uses only the standard library: os, re, datetime)

Installation & Usage
1.	Clone the repository
2.	git clone https://github.com/NuvairaKhan/ITC-PROJECT-.git
3.	cd ITC-PROJECT-
4.	Run the program
5.	python Main.py
or, on some systems:
python3 Main.py
6.	Follow the on-screen menu
7.	===== UCP Class Timetable & Exam Management System =====
8.	1. Add Class Schedule
9.	2. View Class Timetable
10.	3. Add Exam Schedule
11.	4. View Exam Schedule
12.	5. Update Class or Exam Details
13.	6. Search Timetable or Exam
14.	7. Detect Schedule Clashes
15.	8. Generate Reports
16.	9. Exit
Enter the number corresponding to the action you want to perform.

Input Formats
Field	Expected Format	Example
Course Code	Letters/numbers/hyphens	CS101, SE-204
Day	Full weekday name	Monday
Time	HH:MM AM/PM	10:00 AM
Exam Date	DD/MM/YYYY	25/12/2025
Room/Hall	Letters/numbers	A101

Validation & Safety
•	Empty inputs are rejected and re-prompted
•	Course codes, days, times, and dates are checked against expected formats
•	Duplicate course codes and clashing room/day/time or hall/date/time slots trigger a confirmation prompt before saving
•	Exam end time is validated to be later than the start time
•	Corrupted or incomplete rows in the data files are safely skipped when displaying data, rather than crashing the program

Sample Report Output
Running Generate Reports creates a report.txt file like:
===== Class Timetable =====
Course: CS101 - Programming Fundamentals | Instructor: Dr. Ahmed | Day: Monday | Time: 10:00 AM | Room: A101

===== Exam Schedule =====
Course Code: CS101 | Date: 25/12/2025 | Time: 09:00 AM - 11:00 AM | Hall: H1

License
This project was developed for academic purposes as part of a lab course assignment. Feel free to fork and adapt it for learning purposes.
