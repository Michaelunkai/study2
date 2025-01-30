import sys
import os
import sqlite3
import pandas as pd
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QTableWidget,
    QTableWidgetItem, QLineEdit, QPushButton, QWidget, QLabel, QComboBox,
    QMenu, QAction, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import subprocess
from datetime import datetime

# IMDb dataset URLs
DATASET_URLS = {
    "title_basics": "https://datasets.imdbws.com/title.basics.tsv.gz",
    "title_ratings": "https://datasets.imdbws.com/title.ratings.tsv.gz"
}

def ensure_datasets():
    """Download datasets if they don't exist"""
    for dataset, url in DATASET_URLS.items():
        filename = f"{dataset}.tsv.gz"
        if not os.path.exists(filename):
            print(f"{filename} not found. Downloading...")
            subprocess.run(['wget', url, '-O', filename], check=True)
            print(f"{filename} downloaded successfully.")

def load_dataset(file_path):
    """Load a dataset with error handling"""
    try:
        return pd.read_csv(file_path, sep='\t', low_memory=False, na_values='\\N')
    except Exception as e:
        print(f"Failed to load dataset: {file_path}\nError: {e}")
        sys.exit(1)

def setup_database():
    """Initialize SQLite database for tracking watched movies"""
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

def add_to_watched(movie_titles):
    """Add multiple movies to watched list"""
    conn = sqlite3.connect("watched_movies.db")
    cursor = conn.cursor()
    try:
        for title in movie_titles:
            try:
                cursor.execute("INSERT INTO watched (movie_title) VALUES (?)", (title,))
            except sqlite3.IntegrityError:
                continue  # Skip if movie already in watched list
        conn.commit()
    finally:
        conn.close()

def get_watched_movies():
    """Get list of watched movies"""
    conn = sqlite3.connect("watched_movies.db")
    cursor = conn.cursor()
    cursor.execute("SELECT movie_title FROM watched")
    watched_movies = [row[0] for row in cursor.fetchall()]
    conn.close()
    return watched_movies

def get_unique_genres(movies_df):
    """Extract unique genres from the dataset"""
    all_genres = set()
    for genres in movies_df['genres'].str.split(','):
        if isinstance(genres, list):
            all_genres.update(genres)
    return sorted(list(all_genres))

def load_data():
    """Load and process IMDb datasets"""
    ensure_datasets()

    title_basics = load_dataset("title.basics.tsv.gz")
    title_ratings = load_dataset("title.ratings.tsv.gz")

    merged_data = pd.merge(title_basics, title_ratings, on='tconst', how='inner')

    # Filter for movies from 1990-2025 by default
    current_year = datetime.now().year
    movies = merged_data[
        (merged_data['titleType'] == 'movie') &
        (merged_data['numVotes'] >= 30000) &
        (merged_data['startYear'].astype(float) >= 1990) &
        (merged_data['startYear'].astype(float) <= 2025)
    ]

    # Clean and process the data
    movies = movies.dropna(subset=['primaryTitle', 'averageRating', 'numVotes', 'genres', 'startYear', 'runtimeMinutes'])
    movies = movies[~movies['genres'].str.contains('India', na=False, case=False)]
    movies['startYear'] = movies['startYear'].astype(int).astype(str)
    movies['imdbLink'] = "https://www.imdb.com/title/" + movies['tconst']

    return movies.sort_values(by=['averageRating', 'numVotes'], ascending=[False, False])

class MainWindow(QMainWindow):
    def __init__(self, data):
        super().__init__()
        self.data = data
        self.watched_movies = get_watched_movies()
        self.selected_titles = set()  # Store selected movie titles
        self.setup_ui()

    def setup_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("IMDb Movies - Watched Tracker")
        self.setGeometry(100, 100, 1800, 1200)

        main_layout = QVBoxLayout()
        main_layout.setSpacing(1)
        main_layout.setContentsMargins(1, 1, 1, 1)

        # Add filter controls
        self.setup_filters(main_layout)

        # Add action buttons
        self.setup_action_buttons(main_layout)

        # Add table
        self.setup_table(main_layout)

        # Set central widget
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Apply initial filter for unwatched movies
        self.view_selector.setCurrentText("Unwatched")
        self.filter_data()

    def setup_action_buttons(self, main_layout):
        """Setup buttons for bulk actions"""
        button_layout = QHBoxLayout()
        
        # Copy button
        self.copy_button = QPushButton("Copy Selected Titles")
        self.copy_button.setFixedHeight(18)
        self.copy_button.setFont(QFont("Arial", 7))
        self.copy_button.clicked.connect(self.copy_selected_titles)
        
        # Mark as Watched button
        self.mark_watched_button = QPushButton("Mark Selected as Watched")
        self.mark_watched_button.setFixedHeight(18)
        self.mark_watched_button.setFont(QFont("Arial", 7))
        self.mark_watched_button.clicked.connect(self.mark_selected_as_watched)

        # New Bulk Watch button
        # (This performs the same action as the "Mark Selected as Watched" button,
        #  but is provided separately to illustrate the added bulk watch feature.)
        self.bulk_watch_button = QPushButton("Bulk Watch Selected")
        self.bulk_watch_button.setFixedHeight(18)
        self.bulk_watch_button.setFont(QFont("Arial", 7))
        self.bulk_watch_button.clicked.connect(self.mark_selected_as_watched)

        # Add buttons to layout
        button_layout.addWidget(self.copy_button)
        button_layout.addWidget(self.mark_watched_button)
        button_layout.addWidget(self.bulk_watch_button)
        button_layout.addStretch()
        main_layout.addLayout(button_layout)

    def copy_selected_titles(self):
        """Copy selected movie titles to clipboard"""
        if self.selected_titles:
            titles_text = "\n".join(sorted(self.selected_titles))
            clipboard = QApplication.clipboard()
            clipboard.setText(titles_text)
            QMessageBox.information(self, "Success", f"Copied {len(self.selected_titles)} titles to clipboard")
        else:
            QMessageBox.warning(self, "No Selection", "Please select movies to copy")

    def mark_selected_as_watched(self):
        """Mark selected movies as watched"""
        if self.selected_titles:
            add_to_watched(self.selected_titles)
            self.watched_movies = get_watched_movies()
            QMessageBox.information(self, "Success", f"Marked {len(self.selected_titles)} movies as watched")
            self.filter_data()
        else:
            QMessageBox.warning(self, "No Selection", "Please select movies to mark as watched")

    def setup_filters(self, main_layout):
        """Setup filter controls"""
        filter_layout = QHBoxLayout()
        filter_layout.setSpacing(1)

        control_height = 18
        control_font = QFont("Arial", 7)

        # Year filter
        year_label = QLabel("Year:")
        self.start_year_input = QLineEdit("1990")  # Set default start year
        self.start_year_input.setPlaceholderText("Start")
        self.start_year_input.setFixedWidth(50)

        self.end_year_input = QLineEdit("2025")  # Set default end year
        self.end_year_input.setPlaceholderText("End")
        self.end_year_input.setFixedWidth(50)

        # Genre filter
        genre_label = QLabel("Genre:")
        self.genre_selector = QComboBox()
        self.genre_selector.addItems(["All Genres"] + get_unique_genres(self.data))
        self.genre_selector.setFixedWidth(120)

        # View selector
        self.view_selector = QComboBox()
        self.view_selector.addItems(["All Movies", "Watched", "Unwatched"])
        self.view_selector.setFixedWidth(100)

        # Filter button
        self.filter_button = QPushButton("Filter")
        self.filter_button.setFixedWidth(50)
        self.filter_button.clicked.connect(self.filter_data)

        # Apply common properties to all controls
        for widget in [
            year_label, self.start_year_input, self.end_year_input, 
            genre_label, self.genre_selector, self.view_selector, 
            self.filter_button
        ]:
            widget.setFixedHeight(control_height)
            widget.setFont(control_font)

        # Add widgets to layout
        filter_layout.addWidget(year_label)
        filter_layout.addWidget(self.start_year_input)
        filter_layout.addWidget(self.end_year_input)
        filter_layout.addWidget(genre_label)
        filter_layout.addWidget(self.genre_selector)
        filter_layout.addWidget(self.view_selector)
        filter_layout.addWidget(self.filter_button)
        filter_layout.addStretch()

        main_layout.addLayout(filter_layout)

    def setup_table(self, main_layout):
        """Setup the main table"""
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "#", "Title", "★", "Votes", "Genre", "Year", "Len", "→"
        ])

        # Table properties
        self.table.setShowGrid(False)
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        self.table.horizontalHeader().setFixedHeight(12)
        self.table.horizontalHeader().setFont(QFont("Arial", 7, QFont.Bold))
        self.table.setSelectionMode(QTableWidget.MultiSelection)  # Enable multi-selection

        # Column widths
        column_widths = [30, 450, 35, 60, 160, 40, 40, 25]
        for i, width in enumerate(column_widths):
            self.table.setColumnWidth(i, width)

        # Row height and fonts
        self.table.verticalHeader().setDefaultSectionSize(11)
        self.title_font = QFont("Arial", 7, QFont.Bold)
        self.regular_font = QFont("Arial", 7)

        self.populate_table(self.data)
        self.table.cellDoubleClicked.connect(self.handle_cell_double_click)
        self.table.itemSelectionChanged.connect(self.update_selected_titles)
        main_layout.addWidget(self.table)

    def update_selected_titles(self):
        """Update the set of selected movie titles"""
        self.selected_titles.clear()
        for item in self.table.selectedItems():
            if item.column() == 1:  # Title column
                self.selected_titles.add(item.text())

    def populate_table(self, data):
        """Populate table with movie data"""
        self.table.setRowCount(len(data))
        for i, (_, row) in enumerate(data.iterrows()):
            items = [
                QTableWidgetItem(str(i + 1)),
                QTableWidgetItem(row['primaryTitle']),
                QTableWidgetItem(f"{row['averageRating']:.1f}"),
                QTableWidgetItem(f"{int(row['numVotes']/1000)}K"),
                QTableWidgetItem(row['genres'].replace(',', ' ')),
                QTableWidgetItem(row['startYear']),
                QTableWidgetItem(f"{row['runtimeMinutes']}m"),
                QTableWidgetItem("→")
            ]

            alignments = [
                Qt.AlignCenter, Qt.AlignLeft, Qt.AlignCenter, Qt.AlignRight,
                Qt.AlignLeft, Qt.AlignCenter, Qt.AlignCenter, Qt.AlignCenter
            ]

            for col, (item, alignment) in enumerate(zip(items, alignments)):
                item.setTextAlignment(alignment)
                item.setFont(self.title_font if col == 1 else self.regular_font)
                if col == 7:
                    item.setForeground(Qt.blue)
                    item.setData(Qt.UserRole, row['imdbLink'])
                self.table.setItem(i, col, item)

    def filter_data(self):
        """Apply filters to the data"""
        filtered_data = self.data.copy()

        # Year filter
        start_year = self.start_year_input.text()
        end_year = self.end_year_input.text()
        if start_year.isdigit() and end_year.isdigit():
            filtered_data = filtered_data[
                (filtered_data['startYear'].astype(int) >= int(start_year)) &
                (filtered_data['startYear'].astype(int) <= int(end_year))
            ]

        # Genre filter
        selected_genre = self.genre_selector.currentText()
        if selected_genre != "All Genres":
            filtered_data = filtered_data[filtered_data['genres'].str.contains(selected_genre, na=False)]

        # Watched/Unwatched filter
        view = self.view_selector.currentText()
        watched_titles = set(get_watched_movies())
        if view == "Watched":
            filtered_data = filtered_data[filtered_data['primaryTitle'].isin(watched_titles)]
        elif view == "Unwatched":
            filtered_data = filtered_data[~filtered_data['primaryTitle'].isin(watched_titles)]

        self.populate_table(filtered_data)

    def handle_cell_double_click(self, row, column):
        """Handle double-click events on table cells"""
        if column == 1:  # Title column
            movie_title = self.table.item(row, column).text()
            add_to_watched([movie_title])
            self.watched_movies = get_watched_movies()
            self.filter_data()
        elif column == 7:  # IMDb link column
            imdb_link = self.table.item(row, column).data(Qt.UserRole)
            try:
                chrome_path = r"C:\\backup\\windowsapps\\installed\\Chrome\\Application\\chrome.exe"
                subprocess.run(["cmd.exe", "/c", "start", chrome_path, imdb_link], check=True)
            except Exception as e:
                print(f"Failed to open link: {e}")

if __name__ == "__main__":
    # Initialize database and load data
    setup_database()
    data = load_data()

    # Start application
    app = QApplication(sys.argv)
    main_window = MainWindow(data)
    main_window.show()
    sys.exit(app.exec_())
