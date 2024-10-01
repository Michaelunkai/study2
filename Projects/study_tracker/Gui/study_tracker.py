import sqlite3
from datetime import datetime

# Step 1: Create the SQLite Database
def create_database():
    conn = sqlite3.connect('study_tracker.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS study_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            subject TEXT NOT NULL,
            duration INTEGER,
            notes TEXT
        )
    ''')
    conn.commit()
    conn.close()

create_database()

# Step 2: Functions to Manage Study Logs
def add_log(subject, duration=None, notes=None):
    conn = sqlite3.connect('study_tracker.db')
    c = conn.cursor()
    date = datetime.now().strftime('%Y-%m-%d')
    c.execute('''
        INSERT INTO study_logs (date, subject, duration, notes)
        VALUES (?, ?, ?, ?)
    ''', (date, subject, duration, notes))
    conn.commit()
    conn.close()

def view_logs():
    conn = sqlite3.connect('study_tracker.db')
    c = conn.cursor()
    c.execute('SELECT * FROM study_logs ORDER BY id DESC')
    logs = c.fetchall()
    conn.close()
    return logs

def delete_log(log_id):
    conn = sqlite3.connect('study_tracker.db')
    c = conn.cursor()
    c.execute('DELETE FROM study_logs WHERE id = ?', (log_id,))
    conn.commit()
    conn.close()

# Step 3: Command-Line Interface
def main():
    create_database()
    while True:
        print("\n" + "="*30)
        print("        Study Tracker Menu")
        print("="*30)
        print("1. Add a new study log")
        print("2. View all study logs")
        print("3. Delete a study log")
        print("4. Exit")
        print("="*30)
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            print("\n" + "="*30)
            print("        Add New Study Log")
            print("="*30)
            subject = input("Enter the subject: ")
            if not subject.strip():
                print("Subject cannot be empty. Please try again.")
                continue
            try:
                duration = input("Enter the duration (minutes): ")
                duration = int(duration) if duration.strip() else None
            except ValueError:
                print("Invalid duration. Please enter a number or leave it empty.")
                continue
            notes = input("Enter any notes: ")
            notes = notes.strip() if notes else None
            add_log(subject, duration, notes)
            print("Study log added successfully.")
        
        elif choice == '2':
            print("\n" + "="*30)
            print("        All Study Logs")
            print("="*30)
            logs = view_logs()
            if logs:
                for log in logs:
                    log_display = f"ID: {log[0]}, Date: {log[1]}, Subject: {log[2]}, Duration: {log[3]} minutes, Notes: {log[4]}"
                    print(f"\033[91m{log_display}\033[0m")
            else:
                print("No logs found.")
        
        elif choice == '3':
            print("\n" + "="*30)
            print("        Delete Study Log")
            print("="*30)
            try:
                log_id = int(input("Enter the ID of the log to delete: "))
                delete_log(log_id)
                print("Study log deleted successfully.")
            except ValueError:
                print("Invalid ID. Please enter a valid number.")
        
        elif choice == '4':
            print("Exiting Study Tracker. Goodbye!")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()
