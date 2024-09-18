import sqlite3
import paramiko
import os
import tempfile
import sys
from datetime import datetime
from typing import Optional, List, Tuple
import random

# SSH connection details
HOSTNAME = '54.173.176.93'
USERNAME = 'ubuntu'
KEY_PATH = r"C:\backup\windowsapps\Credentials\AWS\key.pem"
REMOTE_DB_PATH = '/home/ubuntu/study_tracker/study_tracker.db'

# Function to download the remote database file
def get_remote_db():
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=HOSTNAME, username=USERNAME, key_filename=KEY_PATH)

        sftp = ssh.open_sftp()
        local_path = os.path.join(tempfile.gettempdir(), 'study_tracker_remote.db')
        sftp.get(REMOTE_DB_PATH, local_path)

        sftp.close()
        ssh.close()

        return local_path
    except Exception as e:
        print(f"Failed to get remote database: {str(e)}")
        sys.exit(1)

# Function to upload the modified database back to the remote server
def upload_remote_db(local_path):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=HOSTNAME, username=USERNAME, key_filename=KEY_PATH)

        sftp = ssh.open_sftp()
        sftp.put(local_path, REMOTE_DB_PATH)

        sftp.close()
        ssh.close()
    except Exception as e:
        print(f"Failed to upload database: {str(e)}")

# Get the remote database
db_path = get_remote_db()

# Connect to the downloaded SQLite database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# SQL table and log structure
StudyLog = Tuple[int, str, str, Optional[int], Optional[str]]

class DatabaseManager:
    @staticmethod
    def create_database() -> None:
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS study_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                subject TEXT NOT NULL,
                duration INTEGER,
                notes TEXT
            )
        """)
        conn.commit()

    @staticmethod
    def add_log(subject: str, duration: Optional[int] = None, notes: Optional[str] = None) -> None:
        date = datetime.now().strftime("%Y-%m-%d")
        cursor.execute(f"""
            INSERT INTO study_logs (date, subject, duration, notes)
            VALUES (?, ?, ?, ?)
        """, (date, subject, duration, notes))
        conn.commit()
        upload_remote_db(db_path)  # Upload the updated database back to the server
        print(f"Study log added: {subject}, {duration} minutes, {notes}")

    @staticmethod
    def view_logs() -> List[StudyLog]:
        cursor.execute(f"""
            SELECT * FROM study_logs
            ORDER BY date DESC, id DESC
        """)
        logs = cursor.fetchall()

        if logs:
            previous_day = None
            print(f"{'ID':<5} {'Date':<12} {'Subject':<15} {'Duration':<10} {'Notes'}")
            print("=" * 50)
            for log in logs:
                current_day = log[1]

                # Change background color for each day
                if current_day != previous_day:
                    print(f"\033[48;5;{get_day_color_code(current_day)}m", end="")

                # Handle None values and format the output
                log_id = log[0]
                log_date = log[1]
                log_subject = log[2]
                log_duration = log[3] if log[3] is not None else "N/A"
                log_notes = log[4] if log[4] is not None else "No notes"
                
                print(f"{log_id:<5} {log_date:<12} {log_subject:<15} {log_duration:<10} {log_notes}")

                previous_day = current_day

            print("\033[0m")  # Reset terminal color after output
        else:
            print("No study logs found.")
        return logs

    @staticmethod
    def delete_log(log_id: int) -> None:
        cursor.execute(f"DELETE FROM study_logs WHERE id = ?", (log_id,))
        conn.commit()
        upload_remote_db(db_path)  # Upload the updated database back to the server
        print(f"Log with ID {log_id} deleted.")

def get_day_color_code(day: str) -> int:
    """
    This function generates a unique color code for each day.
    Terminal colors range from 0 to 255 (for 256-color terminals).
    """
    random.seed(day)  # Ensure same day has the same color
    return random.randint(16, 231)  # Use 16-231 for vibrant colors

def add_study_log():
    subject = input("Enter the subject: ")
    duration = input("Enter the duration in minutes (optional): ")
    notes = input("Enter any notes (optional): ")

    if not subject:
        print("Subject cannot be empty.")
        return

    try:
        duration = int(duration) if duration else None
    except ValueError:
        print("Invalid duration. Please enter a valid number.")
        return

    DatabaseManager.add_log(subject, duration, notes)

def delete_study_log():
    log_id = input("Enter the ID of the log to delete: ")
    try:
        log_id = int(log_id)
        DatabaseManager.delete_log(log_id)
    except ValueError:
        print("Invalid ID. Please enter a valid number.")

def show_menu():
    print("\nStudy Tracker Menu")
    print("====================")
    print("1. Add Study Log")
    print("2. View Study Logs")
    print("3. Delete Study Log")
    print("4. Exit")

def main():
    DatabaseManager.create_database()

    while True:
        show_menu()
        choice = input("Enter your choice: ")

        if choice == "1":
            add_study_log()
        elif choice == "2":
            DatabaseManager.view_logs()
        elif choice == "3":
            delete_study_log()
        elif choice == "4":
            print("Exiting Study Tracker.")
            conn.close()
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
