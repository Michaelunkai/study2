import sqlite3
import tkinter as tk
from tkinter import messagebox

# Connect to SQLite database or create it if it doesn't exist
conn = sqlite3.connect('wishlist.db')

# Create a cursor object
cursor = conn.cursor()

# Define SQL queries to create tables for movies, TV shows, games, and anime
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

create_anime_table = """CREATE TABLE IF NOT EXISTS anime (
                            id INTEGER PRIMARY KEY,
                            title TEXT
                        )"""

# Execute SQL queries to create tables
cursor.execute(create_movies_table)
cursor.execute(create_tv_shows_table)
cursor.execute(create_games_table)
cursor.execute(create_anime_table)

# Commit changes to the database
conn.commit()

# Function to add a new movie to the database
def add_movie():
    titles = movie_entry.get("1.0", "end").split('\n')
    for title in titles:
        if title.strip():
            cursor.execute("INSERT INTO movies (title) VALUES (?)", (title.strip(),))
    conn.commit()
    messagebox.showinfo("Success", "Movie(s) added successfully!")

# Function to add a new TV show to the database
def add_tv_show():
    titles = tv_show_entry.get("1.0", "end").split('\n')
    for title in titles:
        if title.strip():
            cursor.execute("INSERT INTO tv_shows (title) VALUES (?)", (title.strip(),))
    conn.commit()
    messagebox.showinfo("Success", "TV show(s) added successfully!")

# Function to add a new game or multiple games to the database
def add_game():
    titles = game_entry.get("1.0", "end").split('\n')
    for title in titles:
        if title.strip():
            cursor.execute("INSERT INTO games (title) VALUES (?)", (title.strip(),))
    conn.commit()
    messagebox.showinfo("Success", "Game(s) added successfully!")

# Function to add a new anime or multiple anime to the database
def add_anime():
    titles = anime_entry.get("1.0", "end").split('\n')
    for title in titles:
        if title.strip():
            cursor.execute("INSERT INTO anime (title) VALUES (?)", (title.strip(),))
    conn.commit()
    messagebox.showinfo("Success", "Anime(s) added successfully!")

# Function to delete listings
def delete_listings(category):
    confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete all {category.replace('_', ' ')}?")
    if confirm:
        if category == "movies":
            cursor.execute("DELETE FROM movies")
        elif category == "tv_shows":
            cursor.execute("DELETE FROM tv_shows")
        elif category == "games":
            cursor.execute("DELETE FROM games")
        elif category == "anime":
            cursor.execute("DELETE FROM anime")
        
        conn.commit()
        messagebox.showinfo("Success", f"All {category.replace('_', ' ')} deleted successfully.")

# Function to delete selected items
def delete_selected_items():
    for category in items_listboxes:
        if category in items_listboxes:
            selected_indices = items_listboxes[category].curselection()
            if selected_indices:
                confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete the selected item(s)?")
                if confirm:
                    for index in selected_indices:
                        item_id = items_ids[category][index]
                        if category == "movies":
                            cursor.execute("DELETE FROM movies WHERE id=?", (item_id,))
                        elif category == "tv_shows":
                            cursor.execute("DELETE FROM tv_shows WHERE id=?", (item_id,))
                        elif category == "games":
                            cursor.execute("DELETE FROM games WHERE id=?", (item_id,))
                        elif category == "anime":
                            cursor.execute("DELETE FROM anime WHERE id=?", (item_id,))
                    conn.commit()
                    refresh_items_list(category)
                    messagebox.showinfo("Success", "Selected item(s) deleted successfully.")
                    return
    messagebox.showerror("Error", "No items found for deletion.")

# Function to refresh items list
def refresh_items_list(category):
    if category in items_listboxes:
        items_listboxes[category].delete(0, tk.END)
        items_ids[category] = []
        if category == "movies":
            cursor.execute("SELECT * FROM movies")
        elif category == "tv_shows":
            cursor.execute("SELECT * FROM tv_shows")
        elif category == "games":
            cursor.execute("SELECT * FROM games")
        elif category == "anime":
            cursor.execute("SELECT * FROM anime")
        items = cursor.fetchall()
        for item in items:
            items_listboxes[category].insert(tk.END, item[1])
            items_ids[category].append(item[0])

# Function to view wishlist items
def view_wishlist():
    # Create a new window for displaying wishlist items
    view_window = tk.Toplevel(root)
    view_window.title("View Wishlist")
    view_window.configure(background="black")

    # Set the width and height of the view window
    view_window_width = 1000
    view_window_height = 600
    view_window.geometry(f"{view_window_width}x{view_window_height}")

    # Calculate the width for each listbox frame
    frame_width = (view_window_width - 60) // 4

    def remove_all_items(category):
        confirm = messagebox.askyesno("Confirm Remove All", f"Are you sure you want to remove all {category.replace('_', ' ')}?")
        if confirm:
            if category == "movies":
                cursor.execute("DELETE FROM movies")
            elif category == "tv_shows":
                cursor.execute("DELETE FROM tv_shows")
            elif category == "games":
                cursor.execute("DELETE FROM games")
            elif category == "anime":
                cursor.execute("DELETE FROM anime")
            
            conn.commit()
            refresh_items_list(category)
            messagebox.showinfo("Success", f"All {category.replace('_', ' ')} removed successfully.")

    # Create a frame for movies
    movie_frame = tk.Frame(view_window, bg="black", width=frame_width)
    movie_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)

    # Query all movies
    cursor.execute("SELECT * FROM movies")
    movies = cursor.fetchall()
    if movies:
        movie_label = tk.Label(movie_frame, text="Movies", font=("Helvetica", 16, "bold"), fg="red", bg="black")
        movie_label.pack()
        movie_list = tk.Listbox(movie_frame, height=20, width=30, bg="black", fg="white", selectmode=tk.MULTIPLE)
        for movie in movies:
            movie_list.insert(tk.END, movie[1])
        movie_list.pack(fill=tk.BOTH, expand=True)
        movie_scroll = tk.Scrollbar(movie_frame, orient=tk.VERTICAL)
        movie_scroll.config(command=movie_list.yview)
        movie_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        movie_list.config(yscrollcommand=movie_scroll.set)
        items_listboxes["movies"] = movie_list
        refresh_items_list("movies")

        # Create Remove All button for movies
        remove_movie_button = tk.Button(movie_frame, text="Remove All", command=lambda: remove_all_items("movies"), font=("Helvetica", 10), fg="red", bg="black")
        remove_movie_button.pack(pady=5)

    else:
        movie_label = tk.Label(movie_frame, text="No movies found", bg="black", fg="white")
        movie_label.pack()

    # Create a frame for TV shows
    tv_show_frame = tk.Frame(view_window, bg="black", width=frame_width)
    tv_show_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)

    # Query all TV shows
    cursor.execute("SELECT * FROM tv_shows")
    tv_shows = cursor.fetchall()
    if tv_shows:
        tv_label = tk.Label(tv_show_frame, text="TV Shows", font=("Helvetica", 16, "bold"), fg="red", bg="black")
        tv_label.pack()
        tv_list = tk.Listbox(tv_show_frame, height=20, width=30, bg="black", fg="white", selectmode=tk.MULTIPLE)
        for tv_show in tv_shows:
            tv_list.insert(tk.END, tv_show[1])
        tv_list.pack(fill=tk.BOTH, expand=True)
        tv_scroll = tk.Scrollbar(tv_show_frame, orient=tk.VERTICAL)
        tv_scroll.config(command=tv_list.yview)
        tv_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        tv_list.config(yscrollcommand=tv_scroll.set)
        items_listboxes["tv_shows"] = tv_list
        refresh_items_list("tv_shows")

        # Create Remove All button for TV shows
        remove_tv_button = tk.Button(tv_show_frame, text="Remove All", command=lambda: remove_all_items("tv_shows"), font=("Helvetica", 10), fg="red", bg="black")
        remove_tv_button.pack(pady=5)

    else:
        tv_label = tk.Label(tv_show_frame, text="No TV shows found", bg="black", fg="white")
        tv_label.pack()

    # Create a frame for games
    game_frame = tk.Frame(view_window, bg="black", width=frame_width)
    game_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)

    # Query all games
    cursor.execute("SELECT * FROM games")
    games = cursor.fetchall()
    if games:
        game_label = tk.Label(game_frame, text="Games", font=("Helvetica", 16, "bold"), fg="red", bg="black")
        game_label.pack()
        game_list = tk.Listbox(game_frame, height=20, width=30, bg="black", fg="white", selectmode=tk.MULTIPLE)
        for game in games:
            game_list.insert(tk.END, game[1])
        game_list.pack(fill=tk.BOTH, expand=True)
        game_scroll = tk.Scrollbar(game_frame, orient=tk.VERTICAL)
        game_scroll.config(command=game_list.yview)
        game_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        game_list.config(yscrollcommand=game_scroll.set)
        items_listboxes["games"] = game_list
        refresh_items_list("games")

        # Create Remove All button for games
        remove_game_button = tk.Button(game_frame, text="Remove All", command=lambda: remove_all_items("games"), font=("Helvetica", 10), fg="red", bg="black")
        remove_game_button.pack(pady=5)

    else:
        game_label = tk.Label(game_frame, text="No games found", bg="black", fg="white")
        game_label.pack()

    # Create a frame for anime
    anime_frame = tk.Frame(view_window, bg="black", width=frame_width)
    anime_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)

    # Query all anime
    cursor.execute("SELECT * FROM anime")
    anime = cursor.fetchall()
    if anime:
        anime_label = tk.Label(anime_frame, text="Anime", font=("Helvetica", 16, "bold"), fg="red", bg="black")
        anime_label.pack()
        anime_list = tk.Listbox(anime_frame, height=20, width=30, bg="black", fg="white", selectmode=tk.MULTIPLE)
        for ani in anime:
            anime_list.insert(tk.END, ani[1])
        anime_list.pack(fill=tk.BOTH, expand=True)
        anime_scroll = tk.Scrollbar(anime_frame, orient=tk.VERTICAL)
        anime_scroll.config(command=anime_list.yview)
        anime_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        anime_list.config(yscrollcommand=anime_scroll.set)
        items_listboxes["anime"] = anime_list
        refresh_items_list("anime")

        # Create Remove All button for anime
        remove_anime_button = tk.Button(anime_frame, text="Remove All", command=lambda: remove_all_items("anime"), font=("Helvetica", 10), fg="red", bg="black")
        remove_anime_button.pack(pady=5)

    else:
        anime_label = tk.Label(anime_frame, text="No anime found", bg="black", fg="white")
        anime_label.pack()

# Main window
root = tk.Tk()
root.title("Michael Fedro's Wishlist Manager")
root.configure(background="black")

# Labels
movie_label = tk.Label(root, text="Movie(s):", font=("Helvetica", 12, "bold"), fg="red", bg="black")
movie_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
tv_show_label = tk.Label(root, text="TV Show(s):", font=("Helvetica", 12, "bold"), fg="red", bg="black")
tv_show_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
game_label = tk.Label(root, text="Game(s):", font=("Helvetica", 12, "bold"), fg="red", bg="black")
game_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
anime_label = tk.Label(root, text="Anime(s):", font=("Helvetica", 12, "bold"), fg="red", bg="black")
anime_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")

# Entry widgets
movie_entry = tk.Text(root, height=5, width=30)
movie_entry.grid(row=0, column=1, padx=5, pady=5)
tv_show_entry = tk.Text(root, height=5, width=30)
tv_show_entry.grid(row=1, column=1, padx=5, pady=5)
game_entry = tk.Text(root, height=5, width=30)
game_entry.grid(row=2, column=1, padx=5, pady=5)
anime_entry = tk.Text(root, height=5, width=30)
anime_entry.grid(row=3, column=1, padx=5, pady=5)

# Buttons
add_button = tk.Button(root, text="Add Movie", width=15, command=add_movie)
add_button.grid(row=0, column=2, padx=5, pady=5, sticky="w")
add_button = tk.Button(root, text="Add TV Show", width=15, command=add_tv_show)
add_button.grid(row=1, column=2, padx=5, pady=5, sticky="w")
add_button = tk.Button(root, text="Add Game", width=15, command=add_game)
add_button.grid(row=2, column=2, padx=5, pady=5, sticky="w")
add_button = tk.Button(root, text="Add Anime", width=15, command=add_anime)
add_button.grid(row=3, column=2, padx=5, pady=5, sticky="w")

# View button
view_button = tk.Button(root, text="See Wishlist", command=view_wishlist, font=("Helvetica", 12, "bold"), fg="red", bg="black")
view_button.grid(row=4, column=0, columnspan=3, pady=10, sticky="we")

# Delete button
delete_button = tk.Button(root, text="Delete Items", command=delete_selected_items, font=("Helvetica", 12, "bold"), fg="red", bg="black")
delete_button.grid(row=5, column=0, columnspan=3, pady=10, sticky="we")

# Dictionary to hold listboxes for each category
items_listboxes = {}
# Dictionary to hold item ids for each category
items_ids = {}

# Start the GUI
root.mainloop()

# Close the database connection
conn.close()
