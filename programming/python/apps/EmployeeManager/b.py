import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QMessageBox, QVBoxLayout, QHBoxLayout, QGroupBox
import sqlite3

class Employee:
    def __init__(self, name, emp_id, department, salary):
        self.name = name
        self.emp_id = emp_id
        self.department = department
        self.salary = salary

class EmployeeManagerGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Employee Management System")
        self.setStyleSheet("background-color: #FFFAF0; font-family: Lobster; font-size: 12pt; font-weight: bold;")

        # Connect to SQLite database
        self.conn = sqlite3.connect('employee_data.db')
        self.c = self.conn.cursor()
        self.create_table()

        self.employees = []

        self.create_widgets()

    def create_table(self):
        self.c.execute('''CREATE TABLE IF NOT EXISTS employees (
                            name TEXT,
                            emp_id TEXT PRIMARY KEY,
                            department TEXT,
                            salary REAL
                            )''')
        self.conn.commit()

    def create_widgets(self):
        # Labels and Entry Fields
        self.name_label = QLabel("Name:")
        self.name_entry = QLineEdit()

        self.id_label = QLabel("ID:")
        self.id_entry = QLineEdit()

        self.department_label = QLabel("Department:")
        self.department_entry = QLineEdit()

        self.salary_label = QLabel("Salary:")
        self.salary_entry = QLineEdit()

        # Buttons
        self.add_button = QPushButton("Add Employee")
        self.remove_button = QPushButton("Remove Employee")
        self.display_button = QPushButton("Display Employees")

        # Group boxes for layout
        input_group = QGroupBox("Employee Information")
        input_layout = QVBoxLayout()
        input_layout.addWidget(self.name_label)
        input_layout.addWidget(self.name_entry)
        input_layout.addWidget(self.id_label)
        input_layout.addWidget(self.id_entry)
        input_layout.addWidget(self.department_label)
        input_layout.addWidget(self.department_entry)
        input_layout.addWidget(self.salary_label)
        input_layout.addWidget(self.salary_entry)
        input_group.setLayout(input_layout)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.remove_button)
        button_layout.addWidget(self.display_button)

        main_layout = QVBoxLayout()
        main_layout.addWidget(input_group)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

        # Button connections
        self.add_button.clicked.connect(self.add_employee)
        self.remove_button.clicked.connect(self.remove_employee)
        self.display_button.clicked.connect(self.display_employees)

    def add_employee(self):
        name = self.name_entry.text()
        emp_id = self.id_entry.text()
        department = self.department_entry.text()
        salary_entry_value = self.salary_entry.text()
        
        if not salary_entry_value:
            QMessageBox.warning(self, "Error", "Please enter a salary.")
            return
        
        try:
            salary = float(salary_entry_value)
        except ValueError:
            QMessageBox.warning(self, "Error", "Invalid salary. Please enter a valid number.")
            return
        
        # Check if employee with the same emp_id already exists
        self.c.execute("SELECT * FROM employees WHERE emp_id=?", (emp_id,))
        existing_employee = self.c.fetchone()
        if existing_employee:
            QMessageBox.warning(self, "Error", f"Employee with ID {emp_id} already exists. Please enter a different ID.")
            return

        employee = Employee(name, emp_id, department, salary)
        self.employees.append(employee)
        self.save_to_database(employee)
        QMessageBox.information(self, "Success", "Employee added successfully.")

    def remove_employee(self):
        emp_id = self.id_entry.text()
        for employee in self.employees:
            if employee.emp_id == emp_id:
                self.employees.remove(employee)
                self.delete_from_database(emp_id)
                QMessageBox.information(self, "Success", f"Employee with ID {emp_id} removed successfully.")
                return
        QMessageBox.warning(self, "Error", f"Employee with ID {emp_id} not found.")

    def display_employees(self):
        self.c.execute("SELECT * FROM employees")
        rows = self.c.fetchall()
        if rows:
            employee_info = ""
            for row in rows:
                employee_info += f"Name: {row[0]}, ID: {row[1]}, Department: {row[2]}, Salary: {row[3]}\n\n"
            QMessageBox.information(self, "Employee Data", employee_info)
        else:
            QMessageBox.information(self, "Employee Data", "No employees found.")


    def save_to_database(self, employee):
        self.c.execute("INSERT INTO employees (name, emp_id, department, salary) VALUES (?, ?, ?, ?)",
                       (employee.name, employee.emp_id, employee.department, employee.salary))
        self.conn.commit()

    def delete_from_database(self, emp_id):
        self.c.execute("DELETE FROM employees WHERE emp_id=?", (emp_id,))
        self.conn.commit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EmployeeManagerGUI()
    window.show()
    sys.exit(app.exec_())
