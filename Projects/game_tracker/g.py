import sqlite3
import os
import platform
import subprocess

# Database file names
completed_db_file = 'completed.db'
disliked_db_file = 'disliked_games.db'
favorites_db_file = 'favorites.db'
backlog_db_file = 'backlog.db'

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

# Add games to the completed, disliked, favorite, or backlog database
def add_game():
    while True:
        print("\n1) Add completed game")
        print("2) Add disliked game")
        print("3) Add favorite game")
        print("4) Add backlog game")
        choice = input("Choose an option (1, 2, 3, or 4): ").strip()

        if choice == '1':
            db_file = completed_db_file
            category = "completed"
            break
        elif choice == '2':
            db_file = disliked_db_file
            category = "disliked"
            break
        elif choice == '3':
            db_file = favorites_db_file
            category = "favorite"
            break
        elif choice == '4':
            db_file = backlog_db_file
            category = "backlog"
            break
        else:
            print("Invalid option. Please choose 1, 2, 3, or 4.")

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

# Show all games from a specific database
def show_games_from_db(db_file, title):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    cursor.execute("SELECT name, added_at FROM games ORDER BY added_at ASC")
    games = cursor.fetchall()

    if games:
        print(f"\n{title} Games:")
        print("=" * (len(title) + 6))
        for idx, game in enumerate(games, start=1):
            print(f"{idx}. {game[0]} (Added on: {game[1]})")
    else:
        print(f"\nNo {title.lower()} games found in the database.")

    conn.close()

# Clear terminal screen
def clear_terminal():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

# Show all games from all categories
def show_all_games():
    print("\nShowing all games from all categories...\n")
    show_games_from_db(completed_db_file, "Completed")
    show_games_from_db(disliked_db_file, "Disliked")
    show_games_from_db(favorites_db_file, "Favorite")
    show_games_from_db(backlog_db_file, "Backlog")

# Search for a game by name in all databases
def search_game():
    search_query = input("Enter the game name or part of it to search: ").strip()

    print("\nSearching in completed games...")
    show_games_from_search(completed_db_file, search_query)

    print("\nSearching in disliked games...")
    show_games_from_search(disliked_db_file, search_query)

    print("\nSearching in favorite games...")
    show_games_from_search(favorites_db_file, search_query)

    print("\nSearching in backlog games...")
    show_games_from_search(backlog_db_file, search_query)

# Show games matching search query from a database
def show_games_from_search(db_file, search_query):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM games WHERE name LIKE ?", ('%' + search_query + '%',))
    results = cursor.fetchall()

    if results:
        for idx, result in enumerate(results, start=1):
            print(f"{idx}. {result[0]}")
    else:
        print(f"No games found matching '{search_query}'")

    conn.close()

# Main menu to interact with the user
def main_menu():
    while True:
        print("\n-- Game Tracker Menu --")
        print("1. Add a new game")
        print("2. Show all completed games")
        print("3. Show all disliked games")
        print("4. Show all favorite games")
        print("5. Show all backlog games")
        print("6. Show all games")
        print("7. Search for a game")
        print("8. Clear terminal")
        print("9. Exit")

        choice = input("Choose an option (1-9): ").strip()

        if choice == '1':
            add_game()
        elif choice == '2':
            show_games_from_db(completed_db_file, "Completed")
        elif choice == '3':
            show_games_from_db(disliked_db_file, "Disliked")
        elif choice == '4':
            show_games_from_db(favorites_db_file, "Favorite")
        elif choice == '5':
            show_games_from_db(backlog_db_file, "Backlog")
        elif choice == '6':
            show_all_games()
        elif choice == '7':
            search_game()
        elif choice == '8':
            clear_terminal()
        elif choice == '9':
            print("Exiting the application. Goodbye!")
            break
        else:
            print("Invalid option. Please choose 1-9.")

# Ensure all databases are created before running the menu
if __name__ == "__main__":
    create_database(completed_db_file)
    create_database(disliked_db_file)
    create_database(favorites_db_file)
    create_database(backlog_db_file)
    main_menu()
