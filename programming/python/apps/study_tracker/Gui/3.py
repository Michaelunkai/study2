import sqlite3
from datetime import datetime
import colorama
from typing import Optional, List, Tuple
from tabulate import tabulate

# Initialize colorama for cross-platform colored output
colorama.init(autoreset=True)

# Constants
DATABASE_NAME = 'study_tracker.db'
TABLE_NAME = 'study_logs'

# Custom type for study log
StudyLog = Tuple[int, str, str, Optional[int], Optional[str]]

class DatabaseManager:
    @staticmethod
    def create_database() -> None:
        with sqlite3.connect(DATABASE_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    subject TEXT NOT NULL,
                    duration INTEGER,
                    notes TEXT
                )
            ''')

    @staticmethod
    def add_log(subject: str, duration: Optional[int] = None, notes: Optional[str] = None) -> None:
        with sqlite3.connect(DATABASE_NAME) as conn:
            cursor = conn.cursor()
            date = datetime.now().strftime('%Y-%m-%d')
            cursor.execute(f'''
                INSERT INTO {TABLE_NAME} (date, subject, duration, notes)
                VALUES (?, ?, ?, ?)
            ''', (date, subject, duration, notes))

    @staticmethod
    def view_logs() -> List[StudyLog]:
        with sqlite3.connect(DATABASE_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute(f'SELECT * FROM {TABLE_NAME} ORDER BY date DESC, id DESC')
            return cursor.fetchall()

    @staticmethod
    def delete_log(log_id: int) -> None:
        with sqlite3.connect(DATABASE_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute(f'DELETE FROM {TABLE_NAME} WHERE id = ?', (log_id,))

class StudyTracker:
    @staticmethod
    def print_menu() -> None:
        print("\n" + "="*40)
        print(f"{colorama.Fore.CYAN}        Study Tracker Menu")
        print("="*40)
        print(f"{colorama.Fore.YELLOW}1. Add a new study log")
        print(f"{colorama.Fore.YELLOW}2. View all study logs")
        print(f"{colorama.Fore.YELLOW}3. Delete a study log")
        print(f"{colorama.Fore.YELLOW}4. Exit")
        print("="*40)

    @staticmethod
    def add_new_log() -> None:
        print("\n" + "="*40)
        print(f"{colorama.Fore.GREEN}        Add New Study Log")
        print("="*40)
        subject = input("Enter the subject: ").strip()
        if not subject:
            print(f"{colorama.Fore.RED}Subject cannot be empty. Please try again.")
            return

        try:
            duration_input = input("Enter the duration (minutes): ").strip()
            duration = int(duration_input) if duration_input else None
        except ValueError:
            print(f"{colorama.Fore.RED}Invalid duration. Please enter a number or leave it empty.")
            return

        notes = input("Enter any notes: ").strip() or None
        DatabaseManager.add_log(subject, duration, notes)
        print(f"{colorama.Fore.GREEN}Study log added successfully.")

    @staticmethod
    def view_all_logs() -> None:
        print("\n" + "="*60)
        print(f"{colorama.Fore.GREEN}                   All Study Logs")
        print("="*60)
        logs = DatabaseManager.view_logs()
        if logs:
            StudyTracker._display_logs(logs)
        else:
            print(f"{colorama.Fore.YELLOW}No logs found.")

    @staticmethod
    def _display_logs(logs: List[StudyLog]) -> None:
        grouped_logs = {}
        for log in logs:
            date = log[1]
            if date not in grouped_logs:
                grouped_logs[date] = []
            grouped_logs[date].append(log)

        for date, date_logs in grouped_logs.items():
            print(f"\n{colorama.Fore.CYAN}{' ' * 20}Date: {date}{' ' * 20}")
            print(colorama.Fore.YELLOW + "=" * 60)

            table_data = []
            for log in date_logs:
                duration = f"{log[3]} min" if log[3] is not None else "N/A"
                notes = (log[4][:30] + '...') if log[4] and len(log[4]) > 30 else (log[4] or 'N/A')
                table_data.append([log[0], log[2], duration, notes])

            headers = ["ID", "Subject", "Duration", "Notes"]
            print(tabulate(table_data, headers=headers, tablefmt="fancy_grid", colalign=("center", "left", "center", "left")))

    @staticmethod
    def delete_log() -> None:
        print("\n" + "="*40)
        print(f"{colorama.Fore.RED}        Delete Study Log")
        print("="*40)
        try:
            log_id = int(input("Enter the ID of the log to delete: "))
            DatabaseManager.delete_log(log_id)
            print(f"{colorama.Fore.GREEN}Study log deleted successfully.")
        except ValueError:
            print(f"{colorama.Fore.RED}Invalid ID. Please enter a valid number.")

    @classmethod
    def run(cls) -> None:
        DatabaseManager.create_database()
        while True:
            cls.print_menu()
            choice = input(f"{colorama.Fore.CYAN}Enter your choice: ")

            if choice == '1':
                cls.add_new_log()
            elif choice == '2':
                cls.view_all_logs()
            elif choice == '3':
                cls.delete_log()
            elif choice == '4':
                print(f"{colorama.Fore.GREEN}Exiting Study Tracker. Goodbye!")
                break
            else:
                print(f"{colorama.Fore.RED}Invalid choice. Please try again.")

if __name__ == '__main__':
    StudyTracker.run()
