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
import subprocess

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

    tv_shows = merged_data[
        (merged_data['titleType'] == 'tvSeries') & 
        (merged_data['numVotes'] >= 20000)
    ]
    tv_shows = tv_shows.dropna(subset=['primaryTitle', 'averageRating', 'numVotes', 'genres', 'startYear'])

    tv_shows['startYear'] = tv_shows['startYear'].astype(int).astype(str)
    tv_shows['imdbLink'] = "https://www.imdb.com/title/" + tv_shows['tconst']

    return tv_shows.sort_values(by=['averageRating', 'numVotes'], ascending=[False, False])

# SQLite Database setup
def setup_database():
    conn = sqlite3.connect("watched_tv_shows.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS watched (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            show_title TEXT UNIQUE
        )
    """)
    conn.commit()
    conn.close()

def add_to_watched(show_title):
    conn = sqlite3.connect("watched_tv_shows.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO watched (show_title) VALUES (?)", (show_title,))
        conn.commit()
    except sqlite3.IntegrityError:
        pass
    conn.close()

def get_watched_shows():
    conn = sqlite3.connect("watched_tv_shows.db")
    cursor = conn.cursor()
    cursor.execute("SELECT show_title FROM watched")
    watched_shows = [row[0] for row in cursor.fetchall()]
    conn.close()
    return watched_shows

class MainWindow(QMainWindow):
    def __init__(self, data):
        super().__init__()

        self.data = data
        self.watched_shows = get_watched_shows()

        self.setWindowTitle("IMDb TV Shows - Watched Tracker")
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
        self.view_selector.addItems(["All TV Shows", "Watched", "Unwatched"])
        self.view_selector.currentIndexChanged.connect(self.filter_data)

        filter_layout.addWidget(QLabel("Year Range:"))
        filter_layout.addWidget(self.start_year_input)
        filter_layout.addWidget(self.end_year_input)
        filter_layout.addWidget(self.view_selector)
        filter_layout.addWidget(self.filter_button)
        main_layout.addLayout(filter_layout)

        # Table widget
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "Rank", "TV Show Title", "Rating", "Votes", "Genre", "Year", "IMDb Link"
        ])
        self.table.setRowCount(len(self.data) * 2)  # Allocate more rows to show more TV shows
        self.populate_table(self.data)
        self.table.cellDoubleClicked.connect(self.handle_cell_double_click)
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
            link_item = QTableWidgetItem("IMDb Page")
            link_item.setForeground(Qt.blue)
            link_item.setData(Qt.UserRole, row['imdbLink'])

            for item in [rank_item, title_item, rating_item, votes_item, genre_item, year_item]:
                item.setFont(QFont("Arial", 12))

            self.table.setItem(i, 0, rank_item)
            self.table.setItem(i, 1, title_item)
            self.table.setItem(i, 2, rating_item)
            self.table.setItem(i, 3, votes_item)
            self.table.setItem(i, 4, genre_item)
            self.table.setItem(i, 5, year_item)
            self.table.setItem(i, 6, link_item)

    def filter_data(self):
        start_year = self.start_year_input.text()
        end_year = self.end_year_input.text()
        view = self.view_selector.currentText()

        filtered_data = self.data

        if start_year.isdigit() and end_year.isdigit():
            filtered_data = filtered_data[
                (filtered_data['startYear'].astype(int) >= int(start_year)) &
                (filtered_data['startYear'].astype(int) <= int(end_year))
            ]

        watched_titles = set(get_watched_shows())

        if view == "Watched":
            filtered_data = filtered_data[filtered_data['primaryTitle'].isin(watched_titles)]
        elif view == "Unwatched":
            filtered_data = filtered_data[~filtered_data['primaryTitle'].isin(watched_titles)]

        self.populate_table(filtered_data)

    def handle_cell_double_click(self, row, column):
        if column == 1:  # Double-clicked on TV show title
            show_title = self.table.item(row, column).text()
            add_to_watched(show_title)
            self.watched_shows = get_watched_shows()
            self.filter_data()
        elif column == 6:  # Double-clicked on IMDb Link
            imdb_link = self.table.item(row, column).data(Qt.UserRole)
            subprocess.run(["cmd.exe", "/c", "start", "chrome", imdb_link])

if __name__ == "__main__":
    setup_database()
    data = load_data()

    app = QApplication(sys.argv)
    main_window = MainWindow(data)
    main_window.show()
    sys.exit(app.exec_())
