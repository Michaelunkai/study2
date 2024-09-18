import sqlite3

# Connect to SQLite database or create it if it doesn't exist
conn = sqlite3.connect('wishlist.db')

# Create a cursor object
cursor = conn.cursor()

# Define SQL queries to create tables for movies, TV shows, and games
create_movies_table = """CREATE TABLE IF NOT EXISTS movies (
                            id INTEGER PRIMARY KEY,
                            title TEXT
                        )"""

create_tv_shows_table = """CREATE TABLE IF NOT EXISTS tv_shows (
                                id INTEGER PRIMARY KEY,
                                title TEXT
                            )"""

create_games_table = """CREATE TABLE IF NOT EXISTS games (
                            id INTEGER PRIMARY KEY,
                            title TEXT
                        )"""

# Execute SQL queries to create tables
cursor.execute(create_movies_table)
cursor.execute(create_tv_shows_table)
cursor.execute(create_games_table)

# Commit changes to the database
conn.commit()

# Function to add a new movie to the database
def add_movie():
    title = input("Enter the title of the movie: ")
    cursor.execute("INSERT INTO movies (title) VALUES (?)", (title,))
    conn.commit()
    print("Movie added successfully!")

# Function to add a new TV show to the database
def add_tv_show():
    title = input("Enter the title of the TV show: ")
    cursor.execute("INSERT INTO tv_shows (title) VALUES (?)", (title,))
    conn.commit()
    print("TV show added successfully!")

# Function to add a new game or multiple games to the database
def add_game():
    game_input = input("Enter the title(s) of the game(s) (separate by spaces, commas, or each on a new line): ")
    games = [game.strip() for game in game_input.replace(',', ' ').split()]
    for game in games:
        cursor.execute("INSERT INTO games (title) VALUES (?)", (game,))
    conn.commit()
    print("Game(s) added successfully!")

# Function to delete a listing
def delete_listing():
    print("\n--- Delete Listing ---")
    print("Which category would you like to delete from?")
    print("1. Movies")
    print("2. TV Shows")
    print("3. Games")

    category_choice = input("Enter your choice: ")

    if category_choice == '1':
        cursor.execute("SELECT id, title FROM movies")
        listings = cursor.fetchall()
        if listings:
            print("\nMovies:")
            for idx, item in enumerate(listings, start=1):
                print(f"{idx}. {item[1]}")
            selection = int(input("Enter the number of the movie to delete: "))
            if selection <= len(listings):
                movie_id = listings[selection - 1][0]
                cursor.execute("DELETE FROM movies WHERE id=?", (movie_id,))
                conn.commit()
                print("Movie deleted successfully!")
            else:
                print("Invalid selection.")
        else:
            print("No movies found.")

    elif category_choice == '2':
        cursor.execute("SELECT id, title FROM tv_shows")
        listings = cursor.fetchall()
        if listings:
            print("\nTV Shows:")
            for idx, item in enumerate(listings, start=1):
                print(f"{idx}. {item[1]}")
            selection = int(input("Enter the number of the TV show to delete: "))
            if selection <= len(listings):
                tv_show_id = listings[selection - 1][0]
                cursor.execute("DELETE FROM tv_shows WHERE id=?", (tv_show_id,))
                conn.commit()
                print("TV show deleted successfully!")
            else:
                print("Invalid selection.")
        else:
            print("No TV shows found.")

    elif category_choice == '3':
        cursor.execute("SELECT id, title FROM games")
        listings = cursor.fetchall()
        if listings:
            print("\nGames:")
            for idx, item in enumerate(listings, start=1):
                print(f"{idx}. {item[1]}")
            selection = int(input("Enter the number of the game to delete: "))
            if selection <= len(listings):
                game_id = listings[selection - 1][0]
                cursor.execute("DELETE FROM games WHERE id=?", (game_id,))
                conn.commit()
                print("Game deleted successfully!")
            else:
                print("Invalid selection.")
        else:
            print("No games found.")

    else:
        print("Invalid choice!")

# Function to view wishlist items
def view_wishlist():
    print("\n--- Wishlist ---")

    # View movies
    print("\nMovies:")
    cursor.execute("SELECT * FROM movies")
    movies = cursor.fetchall()
    if movies:
        for movie in movies:
            print(f"Title: {movie[1]}")
    else:
        print("No movies found.")

    # View TV shows
    print("\nTV Shows:")
    cursor.execute("SELECT * FROM tv_shows")
    tv_shows = cursor.fetchall()
    if tv_shows:
        for tv_show in tv_shows:
            print(f"Title: {tv_show[1]}")
    else:
        print("No TV shows found.")

    # View games
    print("\nGames:")
    cursor.execute("SELECT * FROM games")
    games = cursor.fetchall()
    if games:
        for game in games:
            print(f"Title: {game[1]}")
    else:
        print("No games found.")

# Main loop to prompt user for actions
while True:
    print("\nWhat would you like to do?")
    print("1. Add new")
    print("2. View wishlist")
    print("3. Delete listing")
    print("4. Exit")

    choice = input("Enter your choice: ")

    if choice == '1':
        print("\nWhat would you like to add?")
        print("1. Movie")
        print("2. TV Show")
        print("3. Game")

        add_choice = input("Enter your choice: ")

        if add_choice == '1':
            add_movie()
        elif add_choice == '2':
            add_tv_show()
        elif add_choice == '3':
            add_game()
        else:
            print("Invalid choice!")

    elif choice == '2':
        view_wishlist()

    elif choice == '3':
        delete_listing()

    elif choice == '4':
        print("Exiting program...")
        break

    else:
        print("Invalid choice!")

# Close the database connection
conn.close()
