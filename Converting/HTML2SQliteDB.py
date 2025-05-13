import os
import sqlite3
from bs4 import BeautifulSoup

def html_to_sqlite(html_file, db_file):
    # Connect to the SQLite database (create if it doesn't exist)
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Create a table to store HTML data
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS html_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tag TEXT,
            attributes TEXT,
            text_content TEXT
        )
    ''')

    # Parse the HTML file
    with open(html_file, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

        # Extract and insert data into the table
        for tag in soup.find_all():
            tag_name = tag.name
            attributes = str(tag.attrs)
            text_content = tag.get_text(strip=True)

            cursor.execute(
                'INSERT INTO html_data (tag, attributes, text_content) VALUES (?, ?, ?)',
                (tag_name, attributes, text_content)
            )

    # Commit changes and close the connection
    conn.commit()
    conn.close()

def process_directory(path):
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.html'):
                html_file = os.path.join(root, file)
                db_file = os.path.join(os.getcwd(), f"{os.path.splitext(file)[0]}.db")
                print(f"Processing {html_file} into {db_file}...")
                html_to_sqlite(html_file, db_file)

if __name__ == '__main__':
    # Define the path containing HTML files
    html_path = os.getcwd()  # Use current working directory

    # Process the HTML files and create the databases
    process_directory(html_path)
    print("All HTML files have been processed and corresponding SQLite databases have been created in the current path.")
