import sqlite3
import paramiko
import os
import tempfile
import sys
from datetime import datetime
from typing import Optional, Tuple

# SSH connection details
HOSTNAME = '54.173.176.93'
USERNAME = 'ubuntu'
KEY_PATH = r"C:\backup\windowsapps\Credentials\AWS\key.pem"
REMOTE_DB_PATH = '/home/ubuntu/study_tracker/study_tracker.db'

# Function to download the remote database file using a faster connection setup
def get_remote_db():
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=HOSTNAME, username=USERNAME, key_filename=KEY_PATH, look_for_keys=False, timeout=10)

        sftp = ssh.open_sftp()
        local_path = os.path.join(tempfile.gettempdir(), 'study_tracker_remote.db')
        sftp.get(REMOTE_DB_PATH, local_path)

        sftp.close()
        ssh.close()

        return local_path
    except Exception as e:
        print(f"Failed to get remote database: {str(e)}")
        sys.exit(1)

# Function to upload the modified database back to the remote server using a faster connection setup
def upload_remote_db(local_path):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=HOSTNAME, username=USERNAME, key_filename=KEY_PATH, look_for_keys=False, timeout=10)

        sftp = ssh.open_sftp()
        sftp.put(local_path, REMOTE_DB_PATH)

        sftp.close()
        ssh.close()
    except Exception as e:
        print(f"Failed to upload database: {str(e)}")

# Get the remote database
db_path = get_remote_db()

# Connect to the downloaded SQLite database
conn = sqlite3.connect(db_path, isolation_level=None, check_same_thread=False)
cursor = conn.cursor()

# SQL table and log structure
StudyLog = Tuple[int, str, str, Optional[int], Optional[str]]

class DatabaseManager:
    @staticmethod
    def create_database() -> None:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS study_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                subject TEXT NOT NULL,
                duration INTEGER,
                notes TEXT
            )
        """)

    @staticmethod
    def add_log(subject: str, duration: Optional[int] = None, notes: Optional[str] = None) -> None:
        date = datetime.now().strftime("%Y-%m-%d")
        cursor.execute("""
            INSERT INTO study_logs (date, subject, duration, notes)
            VALUES (?, ?, ?, ?)
        """, (date, subject, duration, notes))
        upload_remote_db(db_path)
        print(f"Study log added: {subject}, {duration} minutes, {notes}")

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

def main():
    DatabaseManager.create_database()
    add_study_log()

if __name__ == "__main__":
    main()

