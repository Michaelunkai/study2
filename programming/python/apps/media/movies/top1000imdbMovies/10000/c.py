import sys
import os
import sqlite3
import pandas as pd
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QTableWidget,
    QTableWidgetItem, QLineEdit, QPushButton, QWidget, QLabel, QComboBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

# IMDb dataset URLs
DATASET_URLS = {
    "title_basics": "https://datasets.imdbws.com/title.basics.tsv.gz",
    "title_ratings": "https://datasets.imdbws.com/title.ratings.tsv.gz"
}

# Ensure required datasets are downloaded
def ensure_datasets():
    for dataset, url in DATASET_URLS.items():
        filename = f"{dataset}.tsv.gz"
        if not os.path.exists(filename):
            print(f"{filename} not found. Downloading...")
            os.system(f"wget -O {filename} {url}")
            print(f"{filename} downloaded successfully.")

# Read datasets with validation
def load_dataset(file_path):
    try:
        return pd.read_csv(file_path, sep='\t', low_memory=False, na_values='\\N')
    except Exception as e:
        print(f"Failed to load dataset: {file_path}\nError: {e}")
        sys.exit(1)

# Load and process IMDb datasets
def load_data():
    ensure_datasets()

    title_basics = load_dataset("title.basics.tsv.gz")
    title_ratings = load_dataset("title.ratings.tsv.gz")

    merged_data = pd.merge(title_basics, title_ratings, on='tconst', how='inner')

    movies = merged_data[(merged_data['titleType'] == 'movie') & (merged_data['numVotes'] >= 15000)]
    movies = movies.dropna(subset=['primaryTitle', 'averageRating', 'numVotes', 'genres', 'startYear', 'runtimeMinutes'])

    movies['startYear'] = movies['startYear'].astype(int).astype(str)

    return movies.sort_values(by=['averageRating', 'numVotes'], ascending=[False, False])

# SQLite Database setup
def setup_database():
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
    conn = sqlite3.connect("watched_movies.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO watched (movie_title) VALUES (?)", (movie_title,))
        conn.commit()
    except sqlite3.IntegrityError:
        pass
    conn.close()

def get_watched_movies():
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
        self.watched_movies = get_watched_movies()

        self.setWindowTitle("IMDb Movies - Watched Tracker")
        self.setGeometry(100, 100, 1400, 800)

        main_layout = QVBoxLayout()

        # Filter controls
        filter_layout = QHBoxLayout()
        self.start_year_input = QLineEdit()
        self.start_year_input.setPlaceholderText("Start Year")
        self.start_year_input.setFixedWidth(100)
        self.end_year_input = QLineEdit()
        self.end_year_input.setPlaceholderText("End Year")
        self.end_year_input.setFixedWidth(100)
        self.filter_button = QPushButton("Filter by Year")
        self.filter_button.clicked.connect(self.filter_by_year)

        self.view_selector = QComboBox()
        self.view_selector.addItems(["All Movies", "Watched", "Unwatched"])
        self.view_selector.currentIndexChanged.connect(self.filter_by_view)

        filter_layout.addWidget(self.start_year_input)
        filter_layout.addWidget(self.end_year_input)
        filter_layout.addWidget(self.filter_button)
        filter_layout.addWidget(self.view_selector)
        main_layout.addLayout(filter_layout)

        # Table widget
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["Rank", "Movie Title", "Rating", "Votes", "Genre", "Year", "Runtime"])
        self.populate_table(self.data)
        self.table.cellDoubleClicked.connect(self.mark_as_watched)
        main_layout.addWidget(self.table)

        # Central widget
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def populate_table(self, data):
        self.table.setRowCount(len(data))
        for i, (_, row) in enumerate(data.iterrows()):
            rank_item = QTableWidgetItem(str(i + 1))
            title_item = QTableWidgetItem(row['primaryTitle'])
            rating_item = QTableWidgetItem(f"{row['averageRating']:.1f}")
            votes_item = QTableWidgetItem(f"{int(row['numVotes'])}")
            genre_item = QTableWidgetItem(row['genres'])
            year_item = QTableWidgetItem(row['startYear'])
            runtime_item = QTableWidgetItem(f"{row['runtimeMinutes']} min")

            for item in [rank_item, title_item, rating_item, votes_item, genre_item, year_item, runtime_item]:
                item.setFont(QFont("Arial", 12))

            self.table.setItem(i, 0, rank_item)
            self.table.setItem(i, 1, title_item)
            self.table.setItem(i, 2, rating_item)
            self.table.setItem(i, 3, votes_item)
            self.table.setItem(i, 4, genre_item)
            self.table.setItem(i, 5, year_item)
            self.table.setItem(i, 6, runtime_item)

    def filter_by_year(self):
        start_year = self.start_year_input.text()
        end_year = self.end_year_input.text()

        if start_year.isdigit() and end_year.isdigit():
            filtered_data = self.data[
                (self.data['startYear'].astype(int) >= int(start_year)) &
                (self.data['startYear'].astype(int) <= int(end_year))
            ]
            self.populate_table(filtered_data)

    def filter_by_view(self):
        view = self.view_selector.currentText()
        if view == "Watched":
            filtered_data = self.data[self.data['primaryTitle'].isin(self.watched_movies)]
        elif view == "Unwatched":
            filtered_data = self.data[~self.data['primaryTitle'].isin(self.watched_movies)]
        else:
            filtered_data = self.data
        self.populate_table(filtered_data)

    def mark_as_watched(self, row, column):
        if column == 1:  # Double-clicked on movie title
            movie_title = self.table.item(row, column).text()
            add_to_watched(movie_title)
            self.watched_movies = get_watched_movies()

if __name__ == "__main__":
    setup_database()
    data = load_data()

    app = QApplication(sys.argv)
    main_window = MainWindow(data)
    main_window.show()
    sys.exit(app.exec_())
