import sqlite3
import os
from colorama import Fore, Style, init
import textwrap

# Initialize colorama
init(autoreset=True)

# Database file names
completed_db_file = 'completed.db'
disliked_db_file = 'disliked_games.db'
favorites_db_file = 'favorites.db'

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

# Add games to the completed, disliked, or favorite database
def add_game():
    while True:
        print("\n1) Add completed game")
        print("2) Add disliked game")
        print("3) Add favorite game")
        choice = input("Choose an option (1, 2, or 3): ").strip()

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
        else:
            print("Invalid option. Please choose 1, 2, or 3.")

    create_database(db_file)

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    print(f"\nEnter the name of the {category} game(s) you want to add (press enter without typing a name to stop):")
    while True:
        game_name = input("Game name: ").strip()
        if game_name == "":
            break
        cursor.execute("INSERT INTO games (name) VALUES (?)", (game_name,))
        conn.commit()
        print(f"Game '{game_name}' added successfully to {category} games.")

    conn.close()

# Display games from a database in a nicely formatted manner with colorful genre headers
def display_games(db_file, title, color):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT name, added_at FROM games ORDER BY added_at ASC")
    games = cursor.fetchall()
    
    if games:
        title_decorated = f"{color}{title} Games:{Style.RESET_ALL}"
        print("\n" + "=" * len(title_decorated))
        print(title_decorated)
        print("=" * len(title_decorated))
        for idx, game in enumerate(games, start=1):
            print(f"{idx}. {game[0]} (Added on: {game[1]})")
    else:
        print(f"\nNo {title.lower()} games found in the database.")
    conn.close()

# Show all completed games
def show_completed_games():
    display_games(completed_db_file, "Completed", Fore.CYAN)

# Show all disliked games
def show_disliked_games():
    display_games(disliked_db_file, "Disliked", Fore.RED)

# Show all favorite games
def show_favorite_games():
    display_games(favorites_db_file, "Favorite", Fore.GREEN)

# Show all games from all databases
def show_all_games():
    print(Fore.YELLOW + "\nShowing all games from all categories...")
    show_completed_games()
    show_disliked_games()
    show_favorite_games()

# Search for a game by name in all databases
def search_game():
    search_query = input("Enter the game name or part of it to search: ").strip()

    def search_in_db(db_file, category):
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM games WHERE name LIKE ?", ('%' + search_query + '%',))
        results = cursor.fetchall()
        if results:
            print(f"\n{category} Games matching '{search_query}':")
            for idx, result in enumerate(results, start=1):
                print(f"{idx}. {result[0]}")
        else:
            print(f"No {category.lower()} games found matching '{search_query}'")
        conn.close()

    search_in_db(completed_db_file, "Completed")
    search_in_db(disliked_db_file, "Disliked")
    search_in_db(favorites_db_file, "Favorite")

# Main menu to interact with the user
def main_menu():
    while True:
        print("\n-- Game Tracker Menu --")
        print("1. Add a new game")
        print("2. Show all completed games")
        print("3. Show all disliked games")
        print("4. Show all favorite games")
        print("5. Show all games")
        print("6. Search for a game")
        print("7. Exit")

        choice = input("Choose an option (1-7): ").strip()

        if choice == '1':
            add_game()
        elif choice == '2':
            show_completed_games()
        elif choice == '3':
            show_disliked_games()
        elif choice == '4':
            show_favorite_games()
        elif choice == '5':
            show_all_games()
        elif choice == '6':
            search_game()
        elif choice == '7':
            print("Exiting the application. Goodbye!")
            break
        else:
            print("Invalid option. Please choose 1, 2, 3, 4, 5, 6, or 7.")

# Ensure all databases are created before running the menu
if __name__ == "__main__":
    create_database(completed_db_file)
    create_database(disliked_db_file)
    create_database(favorites_db_file)
    main_menu()
