import tkinter as tk
from tkinter import ttk
import sqlite3

class WishlistApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Wishlist App")
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

        # Bind event for window resizing
        self.bind("<Configure>", self.resize_wishlists)

    def create_widgets(self):
        font_style = ("Helvetica", 10, "bold")

        style = ttk.Style()
        style.configure('TButton', font=font_style, foreground="black", background="lightgrey")

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.games_frame = tk.Frame(self.notebook, bg="ivory")
        self.movies_frame = tk.Frame(self.notebook, bg="ivory")
        self.tv_shows_frame = tk.Frame(self.notebook, bg="ivory")
        self.anime_frame = tk.Frame(self.notebook, bg="ivory")

        self.notebook.add(self.games_frame, text="Games")
        self.notebook.add(self.movies_frame, text="Movies")
        self.notebook.add(self.tv_shows_frame, text="TV Shows")
        self.notebook.add(self.anime_frame, text="Anime")

        # Add widgets for games
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

        # More widgets for games...

    def resize_wishlists(self, event):
        width = self.winfo_width()
        height = self.winfo_height()
        self.notebook.config(width=width, height=height)

        for frame in [self.games_frame, self.movies_frame, self.tv_shows_frame, self.anime_frame]:
            frame.config(width=width, height=height)

    # Methods for database operations, list population, and event handlers...

if __name__ == "__main__":
    app = WishlistApp()
    app.mainloop()
