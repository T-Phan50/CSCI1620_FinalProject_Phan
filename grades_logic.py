from PyQt6.QtWidgets import *
from gradebook_ui import *
import csv


def grade_scale_mult(grade) -> str:
    """Takes in an integer input as grade, checks if input is within the range of 0-100.
    If it is, it assigns a letter grade. If not, it raises a value error"""
    if grade > 100 or grade < 0:
        raise ValueError
    elif 100 > int(grade) >= 90:
        return 'A'
    elif 90 > int(grade) >= 80:
        return 'B'
    elif 80 > int(grade) >= 70:
        return 'C'
    elif 70 > int(grade) >= 60:
        return 'D'
    else:
        return 'F'


def line_read(student_name) -> str:
    """Takes in a string input as name, checks if name was found or not in the csv file. Will output a string
    or raises error"""
    response = ''
    with open('Homework1_grades.csv', 'r') as file:
        csvfile = csv.reader(file)
        for line in csvfile:
            if line[0].lower() == student_name.lower():
                response = f"Your Grade is: {line[2]}"
                break
    if response == '':
        raise ValueError
    else:
        return response


class MainLogic(QMainWindow, Ui_MainWindow):
    """class of all logic for the gui window and its widgets"""
    def __init__(self) -> None:
        """Set up for creating the main window"""
        super().__init__()
        self.setupUi(self)

        """Setting buttons on main page to functions"""
        self.stackedWidget.setCurrentWidget(self.main_page)
        self.CancelButton_2.clicked.connect(lambda: self.close_window())
        self.OKButton.clicked.connect(lambda: self.ok_button())

        """Setting buttons on teacher page to functions"""
        self.new_submit_2.clicked.connect(lambda: self.add_stu_grade())
        self.back_but.clicked.connect(lambda: self.back_button())

        """Setting button on student page to functions"""
        self.new_submit_3.clicked.connect(lambda: self.student_page_submit())
        self.back.clicked.connect((lambda: self.back_button()))

    def ok_button(self) -> None:
        """OK button on main page is set to this function. It will open a different screen depending on which radio
        button was clicked"""
        if self.teacher_radio.isChecked():
            self.stackedWidget.setCurrentWidget(self.teacher_page)

        elif self.student_radio.isChecked():
            self.stackedWidget.setCurrentWidget(self.student_page)

    def close_window(self) -> None:
        """Assigned to the close button. Closes the window when pressed"""
        self.close_window()

    def back_button(self) -> None:
        """Assigned to back buttons, goes to the main page"""
        self.stackedWidget.setCurrentWidget(self.main_page)

    def clear(self) -> None:
        """clears the name and grade text boxes"""
        self.stu_name_2.clear()
        self.stu_grade_2.clear()

    def add_stu_grade(self) -> None:
        try:
            """assigns the text from the name and grade box to variables. Then it will check for value errors by
            checking character type and if if grade is less than 100 and greater than 0."""
            student_name = self.stu_name_2.text()
            student_grade = self.stu_grade_2.text()
            student_name = str(student_name)
            student_grade = int(student_grade)
        except ValueError:
            self.add_stu_label_2.setText("Submit a valid Name or Grade number")
        else:
            """appends the student's name, grade and assigns a letter grade to the csv file"""
            with open('Homework1_grades.csv', 'a', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=['Name', 'grade#', 'letter grade'])
                writer.writerow({'Name': student_name, 'grade#': student_grade,
                                 'letter grade': grade_scale_mult(student_grade)})
            self.clear()

    def student_page_submit(self) -> None:
        """This will attempt to set test on screen to the grade of the student whose name was inputted"""
        try:
            stu_name = self.stu_name_3.text().lower()
            self.label_3.setText(line_read(stu_name))
        except ValueError:
            """Will set text to string if not found in list"""
            self.label_3.setText('Name Not Valid or Not Found')
