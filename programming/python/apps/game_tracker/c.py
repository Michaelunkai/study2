import sqlite3
import os

# Database file names
liked_db_file = 'liked_games.db'
disliked_db_file = 'disliked_games.db'

# Create a database and a table if it doesn't exist
def create_database(db_file):
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

# Add games to the liked or disliked database
def add_game():
    # Let user choose 1) Add liked game or 2) Add disliked game
    while True:
        print("\n1) Add liked game")
        print("2) Add disliked game")
        choice = input("Choose an option (1 or 2): ").strip()

        if choice == '1':
            db_file = liked_db_file
            category = "liked"
            break
        elif choice == '2':
            db_file = disliked_db_file
            category = "disliked"
            break
        else:
            print("Invalid option. Please choose 1 or 2.")

    # Ensure the appropriate database is created
    create_database(db_file)

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Now allow the user to add the game(s)
    print(f"\nEnter the name of the {category} game(s) you want to add (press enter without typing a name to stop):")
    while True:
        game_name = input("Game name: ").strip()
        if game_name == "":
            break
        cursor.execute("INSERT INTO games (name) VALUES (?)", (game_name,))
        conn.commit()
        print(f"Game '{game_name}' added successfully to {category} games.")

    conn.close()

# Show all liked games
def show_liked_games():
    conn = sqlite3.connect(liked_db_file)
    cursor = conn.cursor()

    cursor.execute("SELECT name, added_at FROM games ORDER BY added_at ASC")
    games = cursor.fetchall()

    if games:
        print("\nLiked Games (from oldest to newest):")
        for idx, game in enumerate(games, start=1):
            print(f"{idx}. {game[0]} (Added on: {game[1]})")
    else:
        print("\nNo liked games found in the database.")

    conn.close()

# Show all disliked games
def show_disliked_games():
    conn = sqlite3.connect(disliked_db_file)
    cursor = conn.cursor()

    cursor.execute("SELECT name, added_at FROM games ORDER BY added_at ASC")
    games = cursor.fetchall()

    if games:
        print("\nDisliked Games (from oldest to newest):")
        for idx, game in enumerate(games, start=1):
            print(f"{idx}. {game[0]} (Added on: {game[1]})")
    else:
        print("\nNo disliked games found in the database.")

    conn.close()

# Search for a game by name in both databases
def search_game():
    search_query = input("Enter the game name or part of it to search: ").strip()

    print("\nSearching in liked games...")
    conn = sqlite3.connect(liked_db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM games WHERE name LIKE ?", ('%' + search_query + '%',))
    results = cursor.fetchall()

    if results:
        for idx, result in enumerate(results, start=1):
            print(f"{idx}. {result[0]}")
    else:
        print(f"No liked games found matching '{search_query}'")
    conn.close()

    print("\nSearching in disliked games...")
    conn = sqlite3.connect(disliked_db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM games WHERE name LIKE ?", ('%' + search_query + '%',))
    results = cursor.fetchall()

    if results:
        for idx, result in enumerate(results, start=1):
            print(f"{idx}. {result[0]}")
    else:
        print(f"No disliked games found matching '{search_query}'")
    conn.close()

# Main menu to interact with the user
def main_menu():
    while True:
        print("\n-- Game Tracker Menu --")
        print("1. Add a new game")
        print("2. Show all liked games")
        print("3. Show all disliked games")
        print("4. Search for a game")
        print("5. Exit")

        choice = input("Choose an option (1-5): ").strip()

        if choice == '1':
            add_game()
        elif choice == '2':
            show_liked_games()
        elif choice == '3':
            show_disliked_games()
        elif choice == '4':
            search_game()
        elif choice == '5':
            print("Exiting the application. Goodbye!")
            break
        else:
            print("Invalid option. Please choose 1, 2, 3, 4, or 5.")

# Ensure both databases are created before running the menu
if __name__ == "__main__":
    create_database(liked_db_file)
    create_database(disliked_db_file)
    main_menu()
