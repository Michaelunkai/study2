import sys
import sqlite3
import datetime
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QLineEdit, QComboBox, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem
from PyQt5.QtGui import QFont, QIcon


class ExpenseTracker:
    def __init__(self, database_name):
        self.conn = sqlite3.connect(database_name)
        self.cur = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cur.execute('''CREATE TABLE IF NOT EXISTS expenses 
                            (id INTEGER PRIMARY KEY, 
                            amount REAL, 
                            category TEXT, 
                            date DATE)''')
        self.conn.commit()

    def add_expense(self, amount, category):
        date = datetime.datetime.now().date()
        self.cur.execute('''INSERT INTO expenses (amount, category, date) VALUES (?, ?, ?)''',
                         (amount, category, date))
        self.conn.commit()

    def get_expenses(self):
        self.cur.execute('''SELECT amount, category, date FROM expenses''')  # Select only required columns
        return self.cur.fetchall()

    def get_total_expenses(self):
        self.cur.execute('''SELECT SUM(amount) FROM expenses''')
        return self.cur.fetchone()[0]

    def get_expenses_by_category(self, category):
        self.cur.execute('''SELECT amount, category, date FROM expenses WHERE category = ?''', (category,))
        return self.cur.fetchall()


class ExpenseTrackerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Expense Tracker")
        self.setWindowIcon(QIcon('icon.png'))  # Replace 'icon.png' with the path to your icon file
        self.setGeometry(50, 50, 850, 1200)  # Adjusted geometry for a moderate size

        self.expense_tracker = ExpenseTracker("expenses.db")

        self.layout = QVBoxLayout()

        self.label_amount = QLabel("Amount:")
        self.label_amount.setFont(QFont("Lobster", 14, QFont.Bold))  # Increased font size
        self.amount_input = QLineEdit()
        self.layout.addWidget(self.label_amount)
        self.layout.addWidget(self.amount_input)

        self.label_category = QLabel("Category:")
        self.label_category.setFont(QFont("Lobster", 14, QFont.Bold))  # Increased font size
        self.category_input = QComboBox()
        self.category_input.addItems(["Cigarettes", "Weed", "food", "dog food", "outside" , "other"])
        font = QFont("Lobster", 14)  # Increased font size
        self.category_input.setFont(font)
        self.layout.addWidget(self.label_category)
        self.layout.addWidget(self.category_input)

        self.add_button = QPushButton("Add Expense")
        self.add_button.clicked.connect(self.add_expense)
        self.add_button.setFont(QFont("Lobster", 12, QFont.Bold))  # Set Lobster font with size 12 and bold
        self.layout.addWidget(self.add_button)

        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(3)  # Adjusted column count
        self.table_widget.setHorizontalHeaderLabels(["Amount", "Category", "Date"])  # Adjusted header labels
        self.layout.addWidget(self.table_widget)

        self.update_table()

        self.central_widget = QWidget()
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

    def add_expense(self):
        amount = float(self.amount_input.text())
        category = self.category_input.currentText()
        self.expense_tracker.add_expense(amount, category)
        self.amount_input.clear()
        self.update_table()

    def update_table(self):
        expenses = self.expense_tracker.get_expenses()
        self.table_widget.setRowCount(len(expenses))
        for i, expense in enumerate(expenses):
            for j, value in enumerate(expense):
                item = QTableWidgetItem(str(value))
                self.table_widget.setItem(i, j, item)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ExpenseTrackerApp()
    window.show()
    sys.exit(app.exec_())
