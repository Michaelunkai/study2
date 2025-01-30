import sys
import os
import pandas as pd
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QScrollArea, QLabel, QWidget,
    QTableWidget, QTableWidgetItem
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
    # Ensure files are downloaded
    ensure_datasets()

    # Load title basics and ratings
    title_basics = load_dataset("title.basics.tsv.gz")
    title_ratings = load_dataset("title.ratings.tsv.gz")

    # Merge datasets
    merged_data = pd.merge(title_basics, title_ratings, on='tconst', how='inner')

    # Filter for movies with 15,000+ votes
    movies = merged_data[(merged_data['titleType'] == 'movie') & (merged_data['numVotes'] >= 15000)]
    movies = movies.dropna(subset=['primaryTitle', 'averageRating', 'numVotes', 'genres'])

    # Sort and return the top 1000 movies
    return movies.sort_values(by=['averageRating', 'numVotes'], ascending=[False, False]).head(1000)


class MainWindow(QMainWindow):
    def __init__(self, data):
        super().__init__()

        self.setWindowTitle("Top 1000 IMDb Movies (15,000+ Votes)")
        self.setGeometry(100, 100, 1400, 800)  # Set window size

        # Create a scrollable widget
        scroll = QScrollArea(self)
        widget = QWidget()
        scroll.setWidgetResizable(True)
        layout = QVBoxLayout()

        # Add a title label
        title_label = QLabel("Top 1000 IMDb Movies by Rating (15,000+ Votes)", self)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: white; margin-bottom: 20px;")
        layout.addWidget(title_label)

        # Create a table to display the top 1000 movies
        self.table = QTableWidget()
        self.table.setRowCount(len(data))
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Rank", "Movie Title", "Rating", "Votes", "Genre"])
        self.table.setColumnWidth(0, 80)
        self.table.setColumnWidth(1, 500)
        self.table.setColumnWidth(2, 150)
        self.table.setColumnWidth(3, 150)
        self.table.setColumnWidth(4, 500)

        # Populate the table
        self.populate_table(data)

        # Enable sorting by clicking on the column headers
        self.table.setSortingEnabled(True)

        # Customize table appearance
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #005f56;  /* Emerald Black */
                color: white;
                font-size: 16px;
                gridline-color: #404040;
            }
            QHeaderView::section {
                background-color: black;
                color: white;
                font-size: 18px;
                font-weight: bold;
                padding: 4px;
                border: 1px solid #808080;
            }
            QTableWidget::item {
                padding: 8px;
            }
        """)
        layout.addWidget(self.table)

        # Add layout to the widget and set the widget to the scroll area
        widget.setLayout(layout)
        scroll.setWidget(widget)

        self.setCentralWidget(scroll)

    def populate_table(self, data):
        """Populate the table with the movie data."""
        for i, (_, row) in enumerate(data.iterrows()):
            rank_item = QTableWidgetItem(str(i + 1))
            rank_item.setTextAlignment(Qt.AlignCenter)
            rank_item.setFont(QFont("Arial", 12, QFont.Bold))

            title_item = QTableWidgetItem(row['primaryTitle'])
            title_item.setFont(QFont("Arial", 12))

            rating_item = QTableWidgetItem(f"{row['averageRating']:.1f}")
            rating_item.setTextAlignment(Qt.AlignCenter)
            rating_item.setFont(QFont("Arial", 12))

            votes_item = QTableWidgetItem(f"{int(row['numVotes'])}")
            votes_item.setTextAlignment(Qt.AlignCenter)
            votes_item.setFont(QFont("Arial", 12))

            genre_item = QTableWidgetItem(row['genres'])
            genre_item.setFont(QFont("Arial", 12))

            # Add items to the table
            self.table.setItem(i, 0, rank_item)
            self.table.setItem(i, 1, title_item)
            self.table.setItem(i, 2, rating_item)
            self.table.setItem(i, 3, votes_item)
            self.table.setItem(i, 4, genre_item)

        self.table.setEditTriggers(QTableWidget.NoEditTriggers)


if __name__ == "__main__":
    # Load IMDb data
    data = load_data()

    # Run the PyQt5 application
    app = QApplication(sys.argv)
    app.setStyleSheet("QMainWindow { background-color: #005f56; }")  # Set Emerald Black background
    mainWindow = MainWindow(data)
    mainWindow.show()
    sys.exit(app.exec_())
