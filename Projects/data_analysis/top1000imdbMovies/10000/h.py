import sys
import os
import sqlite3
import subprocess
import requests
import gzip
import shutil
import pandas as pd
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QTableWidget,
    QTableWidgetItem, QLineEdit, QPushButton, QWidget, QLabel, QComboBox,
    QMenu, QAction
)
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QFont, QCursor, QClipboard

# IMDb dataset URLs
DATASET_URLS = {
    "title_basics": "https://datasets.imdbws.com/title.basics.tsv.gz",
    "title_ratings": "https://datasets.imdbws.com/title.ratings.tsv.gz"
}

# Directory to store datasets
DATA_DIR = "datasets"

def ensure_datasets():
    """
    Ensure that required IMDb datasets are downloaded and extracted.
    """
    os.makedirs(DATA_DIR, exist_ok=True)
    for dataset, url in DATASET_URLS.items():
        compressed_path = os.path.join(DATA_DIR, f"{dataset}.tsv.gz")
        extracted_path = os.path.join(DATA_DIR, f"{dataset}.tsv")
        
        if not os.path.exists(extracted_path):
            if not os.path.exists(compressed_path):
                print(f"Downloading {dataset}...")
                try:
                    response = requests.get(url, stream=True)
                    response.raise_for_status()
                    with open(compressed_path, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            f.write(chunk)
                    print(f"Downloaded {compressed_path}")
                except requests.RequestException as e:
                    print(f"Failed to download {url}: {e}")
                    sys.exit(1)
            # Extract the gzip file
            print(f"Extracting {compressed_path}...")
            try:
                with gzip.open(compressed_path, 'rb') as f_in:
                    with open(extracted_path, 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
                print(f"Extracted to {extracted_path}")
            except OSError as e:
                print(f"Failed to extract {compressed_path}: {e}")
                sys.exit(1)

def load_dataset(file_path):
    """
    Load a TSV dataset into a pandas DataFrame with proper error handling.
    """
    try:
        print(f"Loading dataset from {file_path}...")
        return pd.read_csv(file_path, sep='\t', low_memory=False, na_values='\\N')
    except Exception as e:
        print(f"Failed to load dataset: {file_path}\nError: {e}")
        sys.exit(1)

def load_data():
    """
    Load and process IMDb datasets, returning a filtered DataFrame of movies.
    """
    ensure_datasets()

    title_basics_path = os.path.join(DATA_DIR, "title.basics.tsv")
    title_ratings_path = os.path.join(DATA_DIR, "title.ratings.tsv")
    
    title_basics = load_dataset(title_basics_path)
    title_ratings = load_dataset(title_ratings_path)

    print("Merging datasets...")
    merged_data = pd.merge(title_basics, title_ratings, on='tconst', how='inner')

    print("Filtering for movies with at least 30,000 votes...")
    movies = merged_data[
        (merged_data['titleType'] == 'movie') &
        (merged_data['numVotes'] >= 30000)
    ]
    movies = movies.dropna(subset=['primaryTitle', 'averageRating', 'numVotes', 'genres', 'startYear', 'runtimeMinutes'])

    # Exclude Indian movies based on genres (assuming 'India' is part of genres)
    print("Excluding Indian movies...")
    movies = movies[~movies['genres'].str.contains('India', na=False, case=False)]

    # Convert startYear to string for consistent display
    movies['startYear'] = movies['startYear'].astype(int).astype(str)
    # Create IMDb link
    movies['imdbLink'] = "https://www.imdb.com/title/" + movies['tconst']

    # Sort by averageRating descending and numVotes descending
    print("Sorting movies by rating and votes...")
    return movies.sort_values(by=['averageRating', 'numVotes'], ascending=[False, False])

def setup_database():
    """
    Set up the SQLite database to store watched movies.
    """
    conn = sqlite3.connect("watched_movies.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS watched (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            movie_title TEXT UNIQUE
        )
    """)
    conn.commit()
    conn.close()

def add_to_watched(movie_title):
    """
    Add a movie title to the watched list in the database.
    """
    conn = sqlite3.connect("watched_movies.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO watched (movie_title) VALUES (?)", (movie_title,))
        conn.commit()
        print(f"Added '{movie_title}' to watched list.")
    except sqlite3.IntegrityError:
        print(f"'{movie_title}' is already in the watched list.")
    finally:
        conn.close()

def get_watched_movies():
    """
    Retrieve the list of watched movies from the database.
    """
    conn = sqlite3.connect("watched_movies.db")
    cursor = conn.cursor()
    cursor.execute("SELECT movie_title FROM watched")
    watched_movies = [row[0] for row in cursor.fetchall()]
    conn.close()
    return watched_movies

class MainWindow(QMainWindow):
    def __init__(self, data):
        super().__init__()

        self.data = data
        self.watched_movies = set(get_watched_movies())

        self.setWindowTitle("IMDb Movies - Watched Tracker")
        self.setGeometry(100, 100, 1600, 800)

        main_layout = QVBoxLayout()

        # Filter controls
        filter_layout = QHBoxLayout()
        self.start_year_input = QLineEdit()
        self.start_year_input.setPlaceholderText("Start Year")
        self.start_year_input.setFixedWidth(100)
        self.end_year_input = QLineEdit()
        self.end_year_input.setPlaceholderText("End Year")
        self.end_year_input.setFixedWidth(100)
        self.filter_button = QPushButton("Apply Filters")
        self.filter_button.clicked.connect(self.filter_data)

        self.view_selector = QComboBox()
        self.view_selector.addItems(["All Movies", "Watched", "Unwatched"])
        self.view_selector.currentIndexChanged.connect(self.filter_data)

        filter_layout.addWidget(QLabel("Year Range:"))
        filter_layout.addWidget(self.start_year_input)
        filter_layout.addWidget(self.end_year_input)
        filter_layout.addWidget(QLabel("View:"))
        filter_layout.addWidget(self.view_selector)
        filter_layout.addWidget(self.filter_button)
        filter_layout.addStretch()
        main_layout.addLayout(filter_layout)

        # Table widget
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "Rank", "Movie Title", "Rating", "Votes", "Genre", "Year", "Runtime", "IMDb Link"
        ])
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.MultiSelection)  # Enable multiple selection
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.open_context_menu)
        self.populate_table(self.data)
        self.table.cellDoubleClicked.connect(self.handle_cell_double_click)
        self.table.setSortingEnabled(True)  # Enable sorting by clicking headers
        main_layout.addWidget(self.table)

        # Central widget
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def populate_table(self, data):
        """
        Populate the table widget with movie data.
        """
        self.table.setRowCount(len(data))
        for i, (_, row) in enumerate(data.iterrows()):
            rank_item = QTableWidgetItem(str(i + 1))
            title_item = QTableWidgetItem(row['primaryTitle'])
            rating_item = QTableWidgetItem(f"{row['averageRating']:.1f}")
            votes_item = QTableWidgetItem(f"{int(row['numVotes'])}")
            genre_item = QTableWidgetItem(row['genres'])
            year_item = QTableWidgetItem(row['startYear'])
            runtime_item = QTableWidgetItem(f"{row['runtimeMinutes']} min")
            link_item = QTableWidgetItem("IMDb Page")
            link_item.setForeground(Qt.blue)
            link_item.setFont(QFont("Arial", 12, QFont.Bold))
            link_item.setToolTip(row['imdbLink'])
            link_item.setData(Qt.UserRole, row['imdbLink'])

            # Highlight watched movies
            if row['primaryTitle'] in self.watched_movies:
                title_item.setForeground(Qt.gray)
                rank_item.setForeground(Qt.gray)
                rating_item.setForeground(Qt.gray)
                votes_item.setForeground(Qt.gray)
                genre_item.setForeground(Qt.gray)
                year_item.setForeground(Qt.gray)
                runtime_item.setForeground(Qt.gray)
                link_item.setForeground(Qt.gray)

            for item in [rank_item, title_item, rating_item, votes_item, genre_item, year_item, runtime_item, link_item]:
                item.setFont(QFont("Arial", 12))

            self.table.setItem(i, 0, rank_item)
            self.table.setItem(i, 1, title_item)
            self.table.setItem(i, 2, rating_item)
            self.table.setItem(i, 3, votes_item)
            self.table.setItem(i, 4, genre_item)
            self.table.setItem(i, 5, year_item)
            self.table.setItem(i, 6, runtime_item)
            self.table.setItem(i, 7, link_item)

        self.table.resizeColumnsToContents()
        self.table.horizontalHeader().setStretchLastSection(True)

    def filter_data(self):
        """
        Filter the movie data based on user inputs and update the table.
        """
        start_year = self.start_year_input.text().strip()
        end_year = self.end_year_input.text().strip()
        view = self.view_selector.currentText()

        filtered_data = self.data

        # Apply year range filter
        if start_year.isdigit() and end_year.isdigit():
            start = int(start_year)
            end = int(end_year)
            if start > end:
                start, end = end, start  # Swap if start_year > end_year
            filtered_data = filtered_data[
                (filtered_data['startYear'].astype(int) >= start) &
                (filtered_data['startYear'].astype(int) <= end)
            ]

        # Apply view filter
        if view == "Watched":
            filtered_data = filtered_data[filtered_data['primaryTitle'].isin(self.watched_movies)]
        elif view == "Unwatched":
            filtered_data = filtered_data[~filtered_data['primaryTitle'].isin(self.watched_movies)]

        self.populate_table(filtered_data)

    def handle_cell_double_click(self, row, column):
        """
        Handle double-click events on table cells.
        """
        if column == 1:  # Movie Title column
            movie_title = self.table.item(row, column).text()
            add_to_watched(movie_title)
            self.watched_movies = set(get_watched_movies())
            self.filter_data()
        elif column == 7:  # IMDb Link column
            imdb_link = self.table.item(row, column).data(Qt.UserRole)
            self.open_imdb_link(imdb_link)

    def open_imdb_link(self, url):
        """
        Open the IMDb link using Chrome via cmd.exe on Windows.
        Defaults to the standard method on other platforms.
        """
        if sys.platform.startswith('win'):
            try:
                subprocess.run(["cmd.exe", "/c", "start", "chrome", url], check=True)
                print(f"Opened {url} in Chrome.")
            except subprocess.CalledProcessError as e:
                print(f"Failed to open {url} in Chrome: {e}")
        elif sys.platform.startswith('darwin'):
            subprocess.run(["open", "-a", "Google Chrome", url])
        else:
            subprocess.run(["xdg-open", url])

    def open_context_menu(self, position: QPoint):
        """
        Open a context menu when the user right-clicks on the table.
        """
        selected_items = self.table.selectedItems()
        if not selected_items:
            return

        menu = QMenu()

        copy_action = QAction("Copy Selected Movie Titles", self)
        copy_action.triggered.connect(self.copy_selected_movie_titles)
        menu.addAction(copy_action)

        menu.exec_(QCursor.pos())

    def copy_selected_movie_titles(self):
        """
        Copy the titles of selected movies to the clipboard.
        """
        selected_rows = set()
        for item in self.table.selectedItems():
            selected_rows.add(item.row())

        movie_titles = []
        for row in selected_rows:
            title_item = self.table.item(row, 1)  # Movie Title is in column 1
            if title_item:
                movie_titles.append(title_item.text())

        if movie_titles:
            clipboard: QClipboard = QApplication.clipboard()
            clipboard.setText("\n".join(movie_titles))
            print("Selected movie titles copied to clipboard.")

if __name__ == "__main__":
    setup_database()
    data = load_data()

    app = QApplication(sys.argv)
    main_window = MainWindow(data)
    main_window.show()
    sys.exit(app.exec_())
