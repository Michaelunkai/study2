import os
import sqlite3

def convert_to_db(root_folder, db_path):
    # Connect (or create) the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create a table to store filesystem data if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS filesystem (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            path TEXT NOT NULL,
            is_dir BOOLEAN NOT NULL,
            data BLOB
        )
    ''')

    # Walk through all files and folders in the root directory
    for root, dirs, files in os.walk(root_folder):
        # Insert directory info
        for directory in dirs:
            dir_path = os.path.join(root, directory)
            cursor.execute(
                'INSERT INTO filesystem (path, is_dir, data) VALUES (?, ?, ?)',
                (dir_path, True, None)
            )

        # Insert file info
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'rb') as f:
                    file_data = f.read()
                cursor.execute(
                    'INSERT INTO filesystem (path, is_dir, data) VALUES (?, ?, ?)',
                    (file_path, False, file_data)
                )
            except Exception as e:
                print(f"Failed to read {file_path}: {e}")

    # Commit changes and close the connection
    conn.commit()
    conn.close()

if __name__ == "__main__":
    root_directory = r"C:\users\micha\downloads"
    database_path = "downloads_data.db"  # Database file will be created in the current directory
    convert_to_db(root_directory, database_path)
    print(f"Database created successfully as {database_path}")
