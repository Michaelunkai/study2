import sqlite3
import os

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
        choice = input("Choose an option (1-4): ").strip()

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

# Delete games from the completed, disliked, favorite, or backlog database
def delete_game():
    while True:
        print("\n1) Delete from completed games")
        print("2) Delete from disliked games")
        print("3) Delete from favorite games")
        print("4) Delete from backlog games")
        choice = input("Choose an option (1-4): ").strip()

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

    create_database(db_file)

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    game_name = input(f"\nEnter the name of the {category} game you want to delete: ").strip()
    cursor.execute("DELETE FROM games WHERE name = ?", (game_name,))
    conn.commit()

    if cursor.rowcount > 0:
        print(f"Game '{game_name}' deleted successfully from {category} games.")
    else:
        print(f"Game '{game_name}' not found in {category} games.")

    conn.close()

# Show all completed games
def show_completed_games():
    conn = sqlite3.connect(completed_db_file)
    cursor = conn.cursor()

    cursor.execute("SELECT name, added_at FROM games ORDER BY added_at ASC")
    games = cursor.fetchall()

    if games:
        print("\nCompleted Games (from oldest to newest):")
        for idx, game in enumerate(games, start=1):
            print(f"{idx}. {game[0]} (Added on: {game[1]})")
    else:
        print("\nNo completed games found in the database.")

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

# Show all favorite games
def show_favorite_games():
    conn = sqlite3.connect(favorites_db_file)
    cursor = conn.cursor()

    cursor.execute("SELECT name, added_at FROM games ORDER BY added_at ASC")
    games = cursor.fetchall()

    if games:
        print("\nFavorite Games (from oldest to newest):")
        for idx, game in enumerate(games, start=1):
            print(f"{idx}. {game[0]} (Added on: {game[1]})")
    else:
        print("\nNo favorite games found in the database.")

    conn.close()

# Show all backlog games
def show_backlog_games():
    conn = sqlite3.connect(backlog_db_file)
    cursor = conn.cursor()

    cursor.execute("SELECT name, added_at FROM games ORDER BY added_at ASC")
    games = cursor.fetchall()

    if games:
        print("\nBacklog Games (from oldest to newest):")
        for idx, game in enumerate(games, start=1):
            print(f"{idx}. {game[0]} (Added on: {game[1]})")
    else:
        print("\nNo backlog games found in the database.")

    conn.close()

# Show all games from all databases
def show_all_games():
    print("\nShowing all games from all categories...")

    # Show completed games
    show_completed_games()

    # Show disliked games
    show_disliked_games()

    # Show favorite games
    show_favorite_games()

    # Show backlog games
    show_backlog_games()

# Clear terminal screen
def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

# Search for a game by name in all databases
def search_game():
    search_query = input("Enter the game name or part of it to search: ").strip()

    print("\nSearching in completed games...")
    conn = sqlite3.connect(completed_db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM games WHERE name LIKE ?", ('%' + search_query + '%',))
    results = cursor.fetchall()

    if results:
        for idx, result in enumerate(results, start=1):
            print(f"{idx}. {result[0]}")
    else:
        print(f"No completed games found matching '{search_query}'")
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

    print("\nSearching in favorite games...")
    conn = sqlite3.connect(favorites_db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM games WHERE name LIKE ?", ('%' + search_query + '%',))
    results = cursor.fetchall()

    if results:
        for idx, result in enumerate(results, start=1):
            print(f"{idx}. {result[0]}")
    else:
        print(f"No favorite games found matching '{search_query}'")
    conn.close()

    print("\nSearching in backlog games...")
    conn = sqlite3.connect(backlog_db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM games WHERE name LIKE ?", ('%' + search_query + '%',))
    results = cursor.fetchall()

    if results:
        for idx, result in enumerate(results, start=1):
            print(f"{idx}. {result[0]}")
    else:
        print(f"No backlog games found matching '{search_query}'")
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
        print("8. Delete a game")
        print("9. Clear terminal")
        print("10. Exit")

        choice = input("Choose an option (1-10): ").strip()

        if choice == '1':
            add_game()
        elif choice == '2':
            show_completed_games()
        elif choice == '3':
            show_disliked_games()
        elif choice == '4':
            show_favorite_games()
        elif choice == '5':
            show_backlog_games()
        elif choice == '6':
            show_all_games()
        elif choice == '7':
            search_game()
        elif choice == '8':
            delete_game()
        elif choice == '9':
            clear_terminal()
        elif choice == '10':
            print("Exiting the application. Goodbye!")
            break
        else:
            print("Invalid option. Please choose between 1-10.")

# Ensure all databases are created before running the menu
if __name__ == "__main__":
    create_database(completed_db_file)
    create_database(disliked_db_file)
    create_database(favorites_db_file)
    create_database(backlog_db_file)
    main_menu()
