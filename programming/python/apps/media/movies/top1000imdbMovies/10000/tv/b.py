import sys
import os
import sqlite3
import pandas as pd
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QTableWidget,
    QTableWidgetItem, QLineEdit, QPushButton, QWidget, QLabel, QComboBox,
    QMessageBox
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
            os.system(f"wget -O {filename} {url}")
            print(f"{filename} downloaded successfully.")

def load_dataset(file_path):
    """Load a dataset with error handling"""
    try:
        return pd.read_csv(file_path, sep='\t', low_memory=False, na_values='\\N')
    except Exception as e:
        print(f"Failed to load dataset: {file_path}\nError: {e}")
        sys.exit(1)

def setup_database():
    """Initialize SQLite database for tracking watched TV series"""
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

def add_to_watched(show_titles):
    """Add multiple TV series to watched list"""
    conn = sqlite3.connect("watched_tv_shows.db")
    cursor = conn.cursor()
    try:
        for title in show_titles:
            try:
                cursor.execute("INSERT INTO watched (show_title) VALUES (?)", (title,))
            except sqlite3.IntegrityError:
                # If the show is already in the watched list, skip it
                continue
        conn.commit()
    finally:
        conn.close()

def get_watched_shows():
    """Get list of watched TV series"""
    conn = sqlite3.connect("watched_tv_shows.db")
    cursor = conn.cursor()
    cursor.execute("SELECT show_title FROM watched")
    watched_shows = [row[0] for row in cursor.fetchall()]
    conn.close()
    return watched_shows

def get_unique_genres(shows_df):
    """Extract unique genres from the TV shows dataset"""
    all_genres = set()
    for genres in shows_df['genres'].str.split(','):
        if isinstance(genres, list):
            all_genres.update(genres)
    return sorted(list(all_genres))

def load_data():
    """Load and process IMDb datasets to focus on TV series"""
    ensure_datasets()

    title_basics = load_dataset("title.basics.tsv.gz")
    title_ratings = load_dataset("title.ratings.tsv.gz")

    merged_data = pd.merge(title_basics, title_ratings, on='tconst', how='inner')

    # Filter for TV series (tvSeries) with at least 20000 votes
    tv_shows = merged_data[
        (merged_data['titleType'] == 'tvSeries') &
        (merged_data['numVotes'] >= 20000)
    ]

    # Drop rows without essential data
    tv_shows = tv_shows.dropna(
        subset=['primaryTitle', 'averageRating', 'numVotes', 'genres', 'startYear']
    )

    # We can also filter out incomplete or less relevant data (optional)
    # For demonstration, we keep all valid entries.

    # Convert startYear to string, build IMDb link
    tv_shows['startYear'] = tv_shows['startYear'].astype(int).astype(str)
    tv_shows['imdbLink'] = "https://www.imdb.com/title/" + tv_shows['tconst']

    # Sort by rating and vote count in descending order
    return tv_shows.sort_values(by=['averageRating', 'numVotes'], ascending=[False, False])

class MainWindow(QMainWindow):
    def __init__(self, data):
        super().__init__()
        self.data = data
        self.watched_shows = get_watched_shows()
        self.selected_titles = set()  # Store selected TV show titles
        self.setup_ui()

    def setup_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("IMDb TV Series - Watched Tracker")
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

        # Apply an initial filter to show Unwatched TV series by default
        self.view_selector.setCurrentText("Unwatched")
        self.filter_data()

    def setup_filters(self, main_layout):
        """Setup filter controls"""
        filter_layout = QHBoxLayout()
        filter_layout.setSpacing(1)

        control_height = 18
        control_font = QFont("Arial", 7)

        # Year filter (Default range: 1990 to 2025)
        year_label = QLabel("Year:")
        self.start_year_input = QLineEdit("1990")
        self.start_year_input.setPlaceholderText("Start")
        self.start_year_input.setFixedWidth(50)

        self.end_year_input = QLineEdit("2025")
        self.end_year_input.setPlaceholderText("End")
        self.end_year_input.setFixedWidth(50)

        # Genre filter
        genre_label = QLabel("Genre:")
        self.genre_selector = QComboBox()
        self.genre_selector.addItems(["All Genres"] + get_unique_genres(self.data))
        self.genre_selector.setFixedWidth(120)

        # View selector (All, Watched, Unwatched)
        self.view_selector = QComboBox()
        self.view_selector.addItems(["All TV Shows", "Watched", "Unwatched"])
        self.view_selector.setFixedWidth(110)

        # Filter button
        self.filter_button = QPushButton("Filter")
        self.filter_button.setFixedWidth(50)
        self.filter_button.clicked.connect(self.filter_data)

        # Apply common properties to each filter widget
        for widget in [
            year_label, self.start_year_input, self.end_year_input,
            genre_label, self.genre_selector, self.view_selector,
            self.filter_button
        ]:
            widget.setFixedHeight(control_height)
            widget.setFont(control_font)

        # Add them to layout
        filter_layout.addWidget(year_label)
        filter_layout.addWidget(self.start_year_input)
        filter_layout.addWidget(self.end_year_input)
        filter_layout.addWidget(genre_label)
        filter_layout.addWidget(self.genre_selector)
        filter_layout.addWidget(self.view_selector)
        filter_layout.addWidget(self.filter_button)
        filter_layout.addStretch()

        main_layout.addLayout(filter_layout)

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

        # Bulk Watch button (demonstrates the same bulk-watch feature)
        self.bulk_watch_button = QPushButton("Bulk Watch Selected")
        self.bulk_watch_button.setFixedHeight(18)
        self.bulk_watch_button.setFont(QFont("Arial", 7))
        self.bulk_watch_button.clicked.connect(self.mark_selected_as_watched)

        button_layout.addWidget(self.copy_button)
        button_layout.addWidget(self.mark_watched_button)
        button_layout.addWidget(self.bulk_watch_button)
        button_layout.addStretch()

        main_layout.addLayout(button_layout)

    def copy_selected_titles(self):
        """Copy selected TV series titles to clipboard"""
        if self.selected_titles:
            titles_text = "\n".join(sorted(self.selected_titles))
            clipboard = QApplication.clipboard()
            clipboard.setText(titles_text)
            QMessageBox.information(self, "Success", f"Copied {len(self.selected_titles)} titles to clipboard")
        else:
            QMessageBox.warning(self, "No Selection", "Please select TV shows to copy")

    def mark_selected_as_watched(self):
        """Mark selected TV series as watched"""
        if self.selected_titles:
            add_to_watched(self.selected_titles)
            self.watched_shows = get_watched_shows()
            QMessageBox.information(self, "Success", f"Marked {len(self.selected_titles)} TV shows as watched")
            self.filter_data()
        else:
            QMessageBox.warning(self, "No Selection", "Please select TV shows to mark as watched")

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
        self.table.setSelectionMode(QTableWidget.MultiSelection)

        # Column widths
        column_widths = [30, 450, 35, 60, 160, 40, 40, 25]
        for i, width in enumerate(column_widths):
            self.table.setColumnWidth(i, width)

        # Row height and fonts
        self.table.verticalHeader().setDefaultSectionSize(11)
        self.title_font = QFont("Arial", 7, QFont.Bold)
        self.regular_font = QFont("Arial", 7)

        # Populate the table with data
        self.populate_table(self.data)

        # Connect signals
        self.table.cellDoubleClicked.connect(self.handle_cell_double_click)
        self.table.itemSelectionChanged.connect(self.update_selected_titles)

        main_layout.addWidget(self.table)

    def update_selected_titles(self):
        """Update the set of selected TV show titles"""
        self.selected_titles.clear()
        for item in self.table.selectedItems():
            if item.column() == 1:  # Title column
                self.selected_titles.add(item.text())

    def populate_table(self, data):
        """Populate table with TV series data"""
        self.table.setRowCount(len(data))
        for i, (_, row) in enumerate(data.iterrows()):
            # Some TV series might lack runtimeMinutes; default to 'N/A' if missing
            runtime = str(row['runtimeMinutes']) + "m" if 'runtimeMinutes' in row and pd.notnull(row['runtimeMinutes']) else "N/A"

            items = [
                QTableWidgetItem(str(i + 1)),                       # #
                QTableWidgetItem(row['primaryTitle']),              # Title
                QTableWidgetItem(f"{row['averageRating']:.1f}"),    # ★
                QTableWidgetItem(f"{int(row['numVotes']/1000)}K"),  # Votes
                QTableWidgetItem(row['genres'].replace(',', ' ')),  # Genre
                QTableWidgetItem(row['startYear']),                 # Year
                QTableWidgetItem(runtime),                           # Len
                QTableWidgetItem("→")                               # Link arrow
            ]

            alignments = [
                Qt.AlignCenter, Qt.AlignLeft, Qt.AlignCenter, Qt.AlignRight,
                Qt.AlignLeft, Qt.AlignCenter, Qt.AlignCenter, Qt.AlignCenter
            ]

            for col, (item, alignment) in enumerate(zip(items, alignments)):
                item.setTextAlignment(alignment)
                item.setFont(self.title_font if col == 1 else self.regular_font)
                # For the link arrow, store the IMDb link in user data and color it blue
                if col == 7:
                    item.setForeground(Qt.blue)
                    item.setData(Qt.UserRole, row['imdbLink'])
                self.table.setItem(i, col, item)

    def filter_data(self):
        """Apply filters to the TV series data"""
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
        watched_titles = set(get_watched_shows())
        if view == "Watched":
            filtered_data = filtered_data[filtered_data['primaryTitle'].isin(watched_titles)]
        elif view == "Unwatched":
            filtered_data = filtered_data[~filtered_data['primaryTitle'].isin(watched_titles)]

        self.populate_table(filtered_data)

    def handle_cell_double_click(self, row, column):
        """Handle double-click events on table cells"""
        # If user double-clicks on the Title column, mark that TV show as watched
        if column == 1:
            show_title = self.table.item(row, column).text()
            add_to_watched([show_title])
            self.watched_shows = get_watched_shows()
            self.filter_data()
        # If user double-clicks on the link arrow, open the IMDb page in Chrome
        elif column == 7:
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
