import tkinter as tk
from tkinter import messagebox
import sqlite3

class Employee:
    def __init__(self, name, emp_id, department, salary):
        self.name = name
        self.emp_id = emp_id
        self.department = department
        self.salary = salary

class EmployeeManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Employee Management System")
        self.root.configure(bg="#FFFAF0")  # Cream color background

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
        # Font style
        font_style = ('Lobster', 12, 'bold')

        # Labels
        tk.Label(self.root, text="Name:", bg="#FFFAF0", font=font_style).grid(row=0, column=0, sticky="e")
        tk.Label(self.root, text="ID:", bg="#FFFAF0", font=font_style).grid(row=1, column=0, sticky="e")
        tk.Label(self.root, text="Department:", bg="#FFFAF0", font=font_style).grid(row=2, column=0, sticky="e")
        tk.Label(self.root, text="Salary:", bg="#FFFAF0", font=font_style).grid(row=3, column=0, sticky="e")

        # Entry fields
        self.name_entry = tk.Entry(self.root, font=font_style)
        self.name_entry.grid(row=0, column=1)
        self.id_entry = tk.Entry(self.root, font=font_style)
        self.id_entry.grid(row=1, column=1)
        self.department_entry = tk.Entry(self.root, font=font_style)
        self.department_entry.grid(row=2, column=1)
        self.salary_entry = tk.Entry(self.root, font=font_style)
        self.salary_entry.grid(row=3, column=1)

        # Buttons
        tk.Button(self.root, text="Add Employee", command=self.add_employee, font=font_style).grid(row=4, column=0, columnspan=2, pady=10)
        tk.Button(self.root, text="Remove Employee", command=self.remove_employee, font=font_style).grid(row=5, column=0, columnspan=2, pady=10)
        tk.Button(self.root, text="Display Employees", command=self.display_employees, font=font_style).grid(row=6, column=0, columnspan=2, pady=10)
        tk.Button(self.root, text="Exit", command=self.root.quit, font=font_style).grid(row=7, column=0, columnspan=2, pady=10)

    def add_employee(self):
        name = self.name_entry.get()
        emp_id = self.id_entry.get()
        department = self.department_entry.get()
        salary_entry_value = self.salary_entry.get()
        
        if salary_entry_value == "":
            messagebox.showerror("Error", "Please enter a salary.")
            return
        
        try:
            salary = float(salary_entry_value)
        except ValueError:
            messagebox.showerror("Error", "Invalid salary. Please enter a valid number.")
            return
        
        # Check if employee with the same emp_id already exists
        self.c.execute("SELECT * FROM employees WHERE emp_id=?", (emp_id,))
        existing_employee = self.c.fetchone()
        if existing_employee:
            messagebox.showerror("Error", f"Employee with ID {emp_id} already exists. Please enter a different ID.")
            return

        employee = Employee(name, emp_id, department, salary)
        self.employees.append(employee)
        self.save_to_database(employee)
        messagebox.showinfo("Success", "Employee added successfully.")

    def remove_employee(self):
        emp_id = self.id_entry.get()
        for employee in self.employees:
            if employee.emp_id == emp_id:
                self.employees.remove(employee)
                self.delete_from_database(emp_id)
                messagebox.showinfo("Success", f"Employee with ID {emp_id} removed successfully.")
                return
        messagebox.showerror("Error", f"Employee with ID {emp_id} not found.")

    def display_employees(self):
        self.c.execute("SELECT * FROM employees")
        rows = self.c.fetchall()
        if rows:
            employee_info = ""
            for row in rows:
                employee_info += f"Name: {row[0]}, ID: {row[1]}, Department: {row[2]}, Salary: {row[3]}\n"
            messagebox.showinfo("Employee Data", employee_info)
        else:
            messagebox.showinfo("Employee Data", "No employees found.")

    def save_to_database(self, employee):
        self.c.execute("INSERT INTO employees (name, emp_id, department, salary) VALUES (?, ?, ?, ?)",
                       (employee.name, employee.emp_id, employee.department, employee.salary))
        self.conn.commit()

    def delete_from_database(self, emp_id):
        self.c.execute("DELETE FROM employees WHERE emp_id=?", (emp_id,))
        self.conn.commit()

def main():
    root = tk.Tk()
    app = EmployeeManagerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
