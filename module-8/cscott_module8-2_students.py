'''
Clint Scott
2025_0420
CSD325 Advanced Python
Module 8.2 Assignment – JSON Practice
'''

import json

# Constants
STUDENT_JSON_FILE = 'student.json'
NEW_STUDENT = {
    "F_Name": "Clint",
    "L_Name": "Scott",
    "Student_ID": 99999,
    "Email": "99999@xmail.com" #not my real email address
}

def load_students(filename):
    """
    Load student data from a JSON file.

    Args:
        filename (str): Path to the JSON file.

    Returns:
        list: A list of student dictionaries.
    """
    with open(filename, 'r') as file:
        return json.load(file)

def print_students(students):
    """
    Print student data in a formatted string for each entry.

    Args:
        students (list): List of student dictionaries.
    """
    for student in students:
        print(f"{student['L_Name']}, {student['F_Name']} : ID = {student['Student_ID']} , Email = {student['Email']}")

def save_students(filename, students):
    """
    Save the student list to a JSON file.

    Args:
        filename (str): Path to the JSON file.
        students (list): List of student dictionaries to save.
    """
    with open(filename, 'w') as file:
        json.dump(students, file, indent=4)

def main():
    """
    Main function that loads, updates, and saves the student list.
    """
    # Load the original student list from the file
    students = load_students(STUDENT_JSON_FILE)

    print("Original Student List:")
    print_students(students)

    # Append the new student to the list
    students.append(NEW_STUDENT)

    print("\nUpdated Student List:")
    print_students(students)

    # Save the updated list back to the JSON file
    save_students(STUDENT_JSON_FILE, students)

    print(f"\n{STUDENT_JSON_FILE} has been updated with the new student data.")

if __name__ == "__main__":
    main()
