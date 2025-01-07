import sys
import os
import pandas as pd
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QScrollArea, QLabel, QWidget,
    QTableWidget, QTableWidgetItem, QLineEdit, QPushButton, QHBoxLayout
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

# Suppress DeprecationWarning for sipPyTypeDict
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

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
    movies = movies.dropna(subset=['primaryTitle', 'averageRating', 'numVotes', 'genres', 'startYear', 'runtimeMinutes'])

    # Convert startYear to string to avoid TypeError
    movies['startYear'] = movies['startYear'].astype(int).astype(str)

    # Sort and return the movies
    return movies.sort_values(by=['averageRating', 'numVotes'], ascending=[False, False])


class MainWindow(QMainWindow):
    def __init__(self, data):
        super().__init__()

        self.data = data

        self.setWindowTitle("Top IMDb Movies (15,000+ Votes)")
        self.setGeometry(100, 100, 1400, 800)  # Set window size

        # Create a main layout
        main_layout = QVBoxLayout()

        # Add filters
        filter_layout = QHBoxLayout()
        self.start_year_input = QLineEdit()
        self.start_year_input.setPlaceholderText("Start Year")
        self.start_year_input.setFixedWidth(100)
        self.end_year_input = QLineEdit()
        self.end_year_input.setPlaceholderText("End Year")
        self.end_year_input.setFixedWidth(100)
        filter_button = QPushButton("Filter by Year")
        filter_button.clicked.connect(self.filter_by_year)

        filter_layout.addWidget(self.start_year_input)
        filter_layout.addWidget(self.end_year_input)
        filter_layout.addWidget(filter_button)
        main_layout.addLayout(filter_layout)

        # Add a title label
        title_label = QLabel("Top IMDb Movies by Rating (15,000+ Votes)", self)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: white; margin-bottom: 20px;")
        main_layout.addWidget(title_label)

        # Create a scrollable table
        self.table = QTableWidget()
        self.table.setRowCount(len(self.data))
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["Rank", "Movie Title", "Rating", "Votes", "Genre", "Year", "Runtime (min)"])
        self.table.setColumnWidth(0, 80)
        self.table.setColumnWidth(1, 500)
        self.table.setColumnWidth(2, 150)
        self.table.setColumnWidth(3, 150)
        self.table.setColumnWidth(4, 300)
        self.table.setColumnWidth(5, 100)
        self.table.setColumnWidth(6, 150)

        # Populate the table
        self.populate_table(self.data)

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
        main_layout.addWidget(self.table)

        # Create a central widget
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def populate_table(self, data):
        """Populate the table with the movie data."""
        self.table.setRowCount(len(data))
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

            year_item = QTableWidgetItem(row['startYear'])
            year_item.setTextAlignment(Qt.AlignCenter)
            year_item.setFont(QFont("Arial", 12))

            runtime_item = QTableWidgetItem(f"{row['runtimeMinutes']} min")
            runtime_item.setTextAlignment(Qt.AlignCenter)
            runtime_item.setFont(QFont("Arial", 12))

            # Add items to the table
            self.table.setItem(i, 0, rank_item)
            self.table.setItem(i, 1, title_item)
            self.table.setItem(i, 2, rating_item)
            self.table.setItem(i, 3, votes_item)
            self.table.setItem(i, 4, genre_item)
            self.table.setItem(i, 5, year_item)
            self.table.setItem(i, 6, runtime_item)

        self.table.setEditTriggers(QTableWidget.NoEditTriggers)

    def filter_by_year(self):
        """Filter the table by year range."""
        start_year = self.start_year_input.text()
        end_year = self.end_year_input.text()

        # Validate inputs
        if not start_year.isdigit() or not end_year.isdigit():
            self.populate_table(self.data)  # Reset to original data
            return

        start_year = int(start_year)
        end_year = int(end_year)

        filtered_data = self.data[
            (self.data['startYear'].astype(int) >= start_year) &
            (self.data['startYear'].astype(int) <= end_year)
        ]
        self.populate_table(filtered_data)


if __name__ == "__main__":
    # Load IMDb data
    data = load_data()

    # Run the PyQt5 application
    app = QApplication(sys.argv)
    app.setStyleSheet("QMainWindow { background-color: #005f56; }")  # Set Emerald Black background
    mainWindow = MainWindow(data)
    mainWindow.show()
    sys.exit(app.exec_())
