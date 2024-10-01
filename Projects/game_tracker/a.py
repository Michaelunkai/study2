import sqlite3
import os

# Database file name
db_file = 'completed.db'

# Create a database and a table if it doesn't exist
def create_database():
    if not os.path.exists(db_file):
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS games (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        conn.commit()
        conn.close()

# Add games to the database
def add_game():
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    print("\nEnter the name of the game(s) you want to add (press enter without typing a name to stop):")
    while True:
        game_name = input("Game name: ").strip()
        if game_name == "":
            break
        cursor.execute("INSERT INTO games (name) VALUES (?)", (game_name,))
        conn.commit()
        print(f"Game '{game_name}' added successfully.")
    
    conn.close()

# Show all completed games in the database
def show_completed_games():
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    cursor.execute("SELECT name, added_at FROM games ORDER BY added_at ASC")
    games = cursor.fetchall()
    
    if games:
        print("\nCompleted Games (from oldest to newest):")
        for idx, game in enumerate(games, start=1):
            print(f"{idx}. {game[0]} (Added on: {game[1]})")
    else:
        print("\nNo games found in the database.")
    
    conn.close()

# Main menu to interact with the user
def main_menu():
    while True:
        print("\n-- Game Tracker Menu --")
        print("1. Add a new game")
        print("2. Show all completed games")
        print("3. Exit")
        
        choice = input("Choose an option (1-3): ").strip()
        
        if choice == '1':
            add_game()
        elif choice == '2':
            show_completed_games()
        elif choice == '3':
            print("Exiting the application. Goodbye!")
            break
        else:
            print("Invalid option. Please choose 1, 2, or 3.")

# Ensure the database is created before running the menu
if __name__ == "__main__":
    create_database()
    main_menu()
