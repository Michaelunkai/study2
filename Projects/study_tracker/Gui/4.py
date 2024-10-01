import sqlite3
from datetime import datetime, timedelta
import colorama
from typing import Optional, List, Tuple, Dict
from tabulate import tabulate
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.styles import Style
from prompt_toolkit.formatted_text import HTML
import matplotlib.pyplot as plt
from collections import defaultdict

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
    def view_logs(days: int = 7) -> List[StudyLog]:
        with sqlite3.connect(DATABASE_NAME) as conn:
            cursor = conn.cursor()
            start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
            cursor.execute(f'''
                SELECT * FROM {TABLE_NAME} 
                WHERE date >= ? 
                ORDER BY date DESC, id DESC
            ''', (start_date,))
            return cursor.fetchall()

    @staticmethod
    def delete_log(log_id: int) -> None:
        with sqlite3.connect(DATABASE_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute(f'DELETE FROM {TABLE_NAME} WHERE id = ?', (log_id,))

    @staticmethod
    def get_subjects() -> List[str]:
        with sqlite3.connect(DATABASE_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute(f'SELECT DISTINCT subject FROM {TABLE_NAME}')
            return [row[0] for row in cursor.fetchall()]

class StudyTracker:
    style = Style.from_dict({
        'completion-menu.completion': 'bg:#008888 #ffffff',
        'completion-menu.completion.current': 'bg:#00aaaa #000000',
        'scrollbar.background': 'bg:#88aaaa',
        'scrollbar.button': 'bg:#222222',
    })

    @staticmethod
    def print_menu() -> None:
        print("\n" + "═" * 60)
        print(f"{colorama.Fore.CYAN}╔{'═' * 58}╗")
        print(f"{colorama.Fore.CYAN}║{' ' * 21}Study Tracker Menu{' ' * 21}║")
        print(f"{colorama.Fore.CYAN}╚{'═' * 58}╝")
        print(f"{colorama.Fore.YELLOW}1. Add a new study log")
        print(f"{colorama.Fore.YELLOW}2. View study logs")
        print(f"{colorama.Fore.YELLOW}3. Delete a study log")
        print(f"{colorama.Fore.YELLOW}4. View study statistics")
        print(f"{colorama.Fore.YELLOW}5. Exit")
        print("═" * 60)

    @classmethod
    def add_new_log(cls) -> None:
        print("\n" + "═" * 60)
        print(f"{colorama.Fore.GREEN}╔{'═' * 58}╗")
        print(f"{colorama.Fore.GREEN}║{' ' * 22}Add New Study Log{' ' * 21}║")
        print(f"{colorama.Fore.GREEN}╚{'═' * 58}╝")

        subject_completer = WordCompleter(DatabaseManager.get_subjects(), ignore_case=True)
        subject = prompt(
            HTML('<ansigreen>Enter the subject: </ansigreen>'),
            completer=subject_completer,
            style=cls.style
        ).strip()

        if not subject:
            print(f"{colorama.Fore.RED}Subject cannot be empty. Please try again.")
            return

        try:
            duration = int(prompt(HTML('<ansigreen>Enter the duration (minutes): </ansigreen>')))
        except ValueError:
            print(f"{colorama.Fore.RED}Invalid duration. Please enter a number.")
            return

        notes = prompt(HTML('<ansigreen>Enter any notes: </ansigreen>')).strip() or None
        DatabaseManager.add_log(subject, duration, notes)
        print(f"{colorama.Fore.GREEN}Study log added successfully.")

    @staticmethod
    def view_logs() -> None:
        print("\n" + "═" * 80)
        print(f"{colorama.Fore.GREEN}╔{'═' * 78}╗")
        print(f"{colorama.Fore.GREEN}║{' ' * 32}Study Logs{' ' * 33}║")
        print(f"{colorama.Fore.GREEN}╚{'═' * 78}╝")

        try:
            days = int(prompt(HTML('<ansigreen>Enter number of days to view (default 7): </ansigreen>')) or 7)
        except ValueError:
            print(f"{colorama.Fore.RED}Invalid input. Using default of 7 days.")
            days = 7

        logs = DatabaseManager.view_logs(days)
        if logs:
            StudyTracker._display_logs(logs)
        else:
            print(f"{colorama.Fore.YELLOW}No logs found for the specified period.")

    @staticmethod
    def _display_logs(logs: List[StudyLog]) -> None:
        grouped_logs = defaultdict(list)
        for log in logs:
            grouped_logs[log[1]].append(log)

        for date, date_logs in grouped_logs.items():
            print(f"\n{colorama.Fore.CYAN}{'─' * 30} Date: {date} {'─' * 30}")

            table_data = []
            for log in date_logs:
                duration = f"{log[3]} min" if log[3] is not None else "N/A"
                notes = (log[4][:30] + '...') if log[4] and len(log[4]) > 30 else (log[4] or 'N/A')
                table_data.append([log[0], log[2], duration, notes])

            headers = ["ID", "Subject", "Duration", "Notes"]
            print(tabulate(table_data, headers=headers, tablefmt="fancy_grid", colalign=("center", "left", "center", "left")))

    @staticmethod
    def delete_log() -> None:
        print("\n" + "═" * 60)
        print(f"{colorama.Fore.RED}╔{'═' * 58}╗")
        print(f"{colorama.Fore.RED}║{' ' * 22}Delete Study Log{' ' * 21}║")
        print(f"{colorama.Fore.RED}╚{'═' * 58}╝")

        try:
            log_id = int(prompt(HTML('<ansired>Enter the ID of the log to delete: </ansired>')))
            DatabaseManager.delete_log(log_id)
            print(f"{colorama.Fore.GREEN}Study log deleted successfully.")
        except ValueError:
            print(f"{colorama.Fore.RED}Invalid ID. Please enter a valid number.")

    @staticmethod
    def view_statistics() -> None:
        print("\n" + "═" * 60)
        print(f"{colorama.Fore.MAGENTA}╔{'═' * 58}╗")
        print(f"{colorama.Fore.MAGENTA}║{' ' * 20}Study Statistics{' ' * 21}║")
        print(f"{colorama.Fore.MAGENTA}╚{'═' * 58}╝")

        logs = DatabaseManager.view_logs(30)  # Get last 30 days of logs
        if not logs:
            print(f"{colorama.Fore.YELLOW}No logs found for the last 30 days.")
            return

        subject_duration = defaultdict(int)
        dates = set()
        for log in logs:
            subject_duration[log[2]] += log[3] or 0
            dates.add(log[1])

        total_duration = sum(subject_duration.values())
        study_days = len(dates)

        print(f"{colorama.Fore.CYAN}Total study time: {total_duration} minutes")
        print(f"{colorama.Fore.CYAN}Number of study days: {study_days}")
        print(f"{colorama.Fore.CYAN}Average study time per day: {total_duration / study_days:.2f} minutes")

        # Create a pie chart
        plt.figure(figsize=(10, 7))
        plt.pie(subject_duration.values(), labels=subject_duration.keys(), autopct='%1.1f%%', startangle=90)
        plt.axis('equal')
        plt.title('Study Time Distribution by Subject')
        plt.show()

    @classmethod
    def run(cls) -> None:
        DatabaseManager.create_database()
        while True:
            cls.print_menu()
            choice = prompt(HTML('<ansicyan>Enter your choice: </ansicyan>'))

            if choice == '1':
                cls.add_new_log()
            elif choice == '2':
                cls.view_logs()
            elif choice == '3':
                cls.delete_log()
            elif choice == '4':
                cls.view_statistics()
            elif choice == '5':
                print(f"{colorama.Fore.GREEN}Thank you for using Study Tracker. Goodbye!")
                break
            else:
                print(f"{colorama.Fore.RED}Invalid choice. Please try again.")

if __name__ == '__main__':
    StudyTracker.run()
