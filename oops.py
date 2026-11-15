import csv
from abc import ABC, abstractmethod

FILE = "students.csv"


class Student(ABC):

    def __init__(self, student_id, name, marks):
        self.student_id = student_id
        self.name = name
        self.marks = marks

    @abstractmethod
    def get_grade(self):
        pass

    def show(self):
        percentage = self.marks / 5
        print(self.student_id, self.name, self.marks,
              f"{percentage:.1f}%", self.get_grade())


class RegularStudent(Student):

    def get_grade(self):
        percentage = self.marks / 5
        if percentage >= 90:
            return "A"
        elif percentage >= 75:
            return "B"
        elif percentage >= 50:
            return "C"
        else:
            return "Fail"


class StudentManager:

    def load(self):
        try:
            with open(FILE, "r", newline="") as f:
                return list(csv.reader(f))[1:]   
        except FileNotFoundError:
            return []

    def save(self, rows):
        with open(FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Name", "Marks"])
            writer.writerows(rows)

    
    def add_student(self):
        rows = self.load()
        student_id = input("Enter ID: ")

        for row in rows:
            if row[0] == student_id:
                print("ID already exists!")
                return

        name = input("Enter name: ")
        marks = float(input("Enter marks out of 500: "))

        if marks < 0 or marks > 500:
            print("Marks must be between 0 and 500!")
            return

        rows.append([student_id, name, marks])
        self.save(rows)
        print("Student added!")

    def view_students(self):
        rows = self.load()
        if not rows:
            print("No records found!")
            return

        for row in rows:
            RegularStudent(row[0], row[1], float(row[2])).show()

    def search_student(self):
        student_id = input("Enter ID to search: ")

        for row in self.load():
            if row[0] == student_id:
                RegularStudent(row[0], row[1], float(row[2])).show()
                return

        print("Student not found!")

    def update_student(self):
        rows = self.load()
        student_id = input("Enter ID to update: ")

        for row in rows:
            if row[0] == student_id:
                row[1] = input("Enter new name: ")
                row[2] = float(input("Enter new marks out of 500: "))
                self.save(rows)
                print("Student updated!")
                return

        print("Student not found!")

    def delete_student(self):
        rows = self.load()
        student_id = input("Enter ID to delete: ")

        new_rows = [row for row in rows if row[0] != student_id]

        if len(new_rows) == len(rows):
            print("Student not found!")
            return

        self.save(new_rows)
        print("Student deleted!")


manager = StudentManager()

while True:
    print("\n--- STUDENT MANAGEMENT SYSTEM ---")
    print("1. Add Student")
    print("2. View Students")
    print("3. Search Student")
    print("4. Update Student")
    print("5. Delete Student")
    print("6. Exit")

    choice = input("Enter your choice: ")

    try:
        if choice == "1":
            manager.add_student()
        elif choice == "2":
            manager.view_students()
        elif choice == "3":
            manager.search_student()
        elif choice == "4":
            manager.update_student()
        elif choice == "5":
            manager.delete_student()
        elif choice == "6":
            print("Thank you!")
            break
        else:
            print("Invalid choice!")
    except ValueError:
        print("Please enter a valid number for marks!")
