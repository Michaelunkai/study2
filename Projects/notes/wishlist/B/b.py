import tkinter as tk
from tkinter import ttk
import sqlite3

class WishlistApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Wishlist App")
        self.geometry("500x400")
        self.configure(bg="ivory")

        self.create_widgets()

        # Connect to the SQLite database
        self.conn = sqlite3.connect("wishlist.db")
        self.create_tables()

        # Initialize lists to store items
        self.games_list = []
        self.movies_list = []
        self.tv_shows_list = []
        self.anime_list = []

        # Populate lists from the database
        self.populate_lists()

    def create_widgets(self):
        font_style = ("Helvetica", 10, "bold")

        style = ttk.Style()
        style.configure('TButton', font=font_style, foreground="black", background="lightgrey")

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        self.notebook.bind("<Button-1>", self.resize_wishlists)

        self.games_frame = tk.Frame(self.notebook, bg="ivory")
        self.movies_frame = tk.Frame(self.notebook, bg="ivory")
        self.tv_shows_frame = tk.Frame(self.notebook, bg="ivory")
        self.anime_frame = tk.Frame(self.notebook, bg="ivory")

        self.notebook.add(self.games_frame, text="Games")
        self.notebook.add(self.movies_frame, text="Movies")
        self.notebook.add(self.tv_shows_frame, text="TV Shows")
        self.notebook.add(self.anime_frame, text="Anime")

        # Add widgets for adding and removing items to games
        self.add_game_label = tk.Label(self.games_frame, text="Add a game:", bg="ivory")
        self.add_game_label.grid(row=0, column=0, padx=5, pady=5)

        self.game_entry = tk.Entry(self.games_frame)
        self.game_entry.grid(row=0, column=1, padx=5, pady=5)

        self.add_game_button = ttk.Button(self.games_frame, text="Add Game", command=self.add_game)
        self.add_game_button.grid(row=0, column=2, padx=5, pady=5)

        self.games_listbox = tk.Listbox(self.games_frame)
        self.games_listbox.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")

        self.remove_game_button = ttk.Button(self.games_frame, text="Remove Game", command=self.remove_game)
        self.remove_game_button.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")

        # Add widgets for adding and removing items to movies
        self.add_movie_label = tk.Label(self.movies_frame, text="Add a movie:", bg="ivory")
        self.add_movie_label.grid(row=0, column=0, padx=5, pady=5)

        self.movie_entry = tk.Entry(self.movies_frame)
        self.movie_entry.grid(row=0, column=1, padx=5, pady=5)

        self.add_movie_button = ttk.Button(self.movies_frame, text="Add Movie", command=self.add_movie)
        self.add_movie_button.grid(row=0, column=2, padx=5, pady=5)

        self.movies_listbox = tk.Listbox(self.movies_frame)
        self.movies_listbox.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")

        self.remove_movie_button = ttk.Button(self.movies_frame, text="Remove Movie", command=self.remove_movie)
        self.remove_movie_button.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")

        # Add widgets for adding and removing items to TV shows
        self.add_tv_show_label = tk.Label(self.tv_shows_frame, text="Add a TV show:", bg="ivory")
        self.add_tv_show_label.grid(row=0, column=0, padx=5, pady=5)

        self.tv_show_entry = tk.Entry(self.tv_shows_frame)
        self.tv_show_entry.grid(row=0, column=1, padx=5, pady=5)

        self.add_tv_show_button = ttk.Button(self.tv_shows_frame, text="Add TV Show", command=self.add_tv_show)
        self.add_tv_show_button.grid(row=0, column=2, padx=5, pady=5)

        self.tv_shows_listbox = tk.Listbox(self.tv_shows_frame)
        self.tv_shows_listbox.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")

        self.remove_tv_show_button = ttk.Button(self.tv_shows_frame, text="Remove TV Show", command=self.remove_tv_show)
        self.remove_tv_show_button.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")

        # Add widgets for adding and removing items to anime
        self.add_anime_label = tk.Label(self.anime_frame, text="Add an anime:", bg="ivory")
        self.add_anime_label.grid(row=0, column=0, padx=5, pady=5)

        self.anime_entry = tk.Entry(self.anime_frame)
        self.anime_entry.grid(row=0, column=1, padx=5, pady=5)

        self.add_anime_button = ttk.Button(self.anime_frame, text="Add Anime", command=self.add_anime)
        self.add_anime_button.grid(row=0, column=2, padx=5, pady=5)

        self.anime_listbox = tk.Listbox(self.anime_frame)
        self.anime_listbox.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")

        self.remove_anime_button = ttk.Button(self.anime_frame, text="Remove Anime", command=self.remove_anime)
        self.remove_anime_button.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")

    def resize_wishlists(self, event):
        width = self.winfo_width()
        height = self.winfo_height()
        self.notebook.config(width=width, height=height)

    def create_tables(self):
        c = self.conn.cursor()

        # Create tables if they don't exist
        c.execute('''CREATE TABLE IF NOT EXISTS games (id INTEGER PRIMARY KEY, name TEXT)''')
        c.execute('''CREATE TABLE IF NOT EXISTS movies (id INTEGER PRIMARY KEY, name TEXT)''')
        c.execute('''CREATE TABLE IF NOT EXISTS tv_shows (id INTEGER PRIMARY KEY, name TEXT)''')
        c.execute('''CREATE TABLE IF NOT EXISTS anime (id INTEGER PRIMARY KEY, name TEXT)''')

        self.conn.commit()

    def populate_lists(self):
        # Populate games list
        c = self.conn.cursor()
        c.execute("SELECT name FROM games")
        self.games_list = [row[0] for row in c.fetchall()]
        self.update_listbox(self.games_list, self.games_listbox)

        # Populate movies list
        c.execute("SELECT name FROM movies")
        self.movies_list = [row[0] for row in c.fetchall()]
        self.update_listbox(self.movies_list, self.movies_listbox)

        # Populate TV shows list
        c.execute("SELECT name FROM tv_shows")
        self.tv_shows_list = [row[0] for row in c.fetchall()]
        self.update_listbox(self.tv_shows_list, self.tv_shows_listbox)

        # Populate anime list
        c.execute("SELECT name FROM anime")
        self.anime_list = [row[0] for row in c.fetchall()]
        self.update_listbox(self.anime_list, self.anime_listbox)

    def add_game(self):
        game = self.game_entry.get()
        if game:
            self.games_list.append(game)
            self.update_listbox(self.games_list, self.games_listbox)
            self.add_to_database("games", game)

    def remove_game(self):
        selected_index = self.games_listbox.curselection()
        if selected_index:
            game = self.games_list[selected_index[0]]
            self.games_list.pop(selected_index[0])
            self.update_listbox(self.games_list, self.games_listbox)
            self.remove_from_database("games", game)

    def add_movie(self):
        movie = self.movie_entry.get()
        if movie:
            self.movies_list.append(movie)
            self.update_listbox(self.movies_list, self.movies_listbox)
            self.add_to_database("movies", movie)

    def remove_movie(self):
        selected_index = self.movies_listbox.curselection()
        if selected_index:
            movie = self.movies_list[selected_index[0]]
            self.movies_list.pop(selected_index[0])
            self.update_listbox(self.movies_list, self.movies_listbox)
            self.remove_from_database("movies", movie)

    def add_tv_show(self):
        tv_show = self.tv_show_entry.get()
        if tv_show:
            self.tv_shows_list.append(tv_show)
            self.update_listbox(self.tv_shows_list, self.tv_shows_listbox)
            self.add_to_database("tv_shows", tv_show)

    def remove_tv_show(self):
        selected_index = self.tv_shows_listbox.curselection()
        if selected_index:
            tv_show = self.tv_shows_list[selected_index[0]]
            self.tv_shows_list.pop(selected_index[0])
            self.update_listbox(self.tv_shows_list, self.tv_shows_listbox)
            self.remove_from_database("tv_shows", tv_show)

    def add_anime(self):
        anime = self.anime_entry.get()
        if anime:
            self.anime_list.append(anime)
            self.update_listbox(self.anime_list, self.anime_listbox)
            self.add_to_database("anime", anime)

    def remove_anime(self):
        selected_index = self.anime_listbox.curselection()
        if selected_index:
            anime = self.anime_list[selected_index[0]]
            self.anime_list.pop(selected_index[0])
            self.update_listbox(self.anime_list, self.anime_listbox)
            self.remove_from_database("anime", anime)

    def add_to_database(self, table, item):
        c = self.conn.cursor()
        c.execute(f"INSERT INTO {table} (name) VALUES (?)", (item,))
        self.conn.commit()

    def remove_from_database(self, table, item):
        c = self.conn.cursor()
        c.execute(f"DELETE FROM {table} WHERE name=?", (item,))
        self.conn.commit()

    def update_listbox(self, items, listbox):
        listbox.delete(0, tk.END)
        for item in items:
            listbox.insert(tk.END, item)

if __name__ == "__main__":
    app = WishlistApp()
    app.mainloop()

