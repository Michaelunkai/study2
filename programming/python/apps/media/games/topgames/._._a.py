import sys
import os
import sqlite3
import pandas as pd
import subprocess
from urllib.parse import quote
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QTableWidget,
    QTableWidgetItem, QPushButton, QWidget, QLabel, QComboBox,
    QMessageBox, QHeaderView, QLineEdit
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPalette, QColor

###############################################################################
#                              CONSTANTS                                      #
###############################################################################

# Paths to the databases
CURRENT_PATH = os.getcwd()
COMBINED_DB_FILE = os.path.join(CURRENT_PATH, "combined.db")  # The main SQLite database file
PLAYED_DB_FILE = os.path.join(CURRENT_PATH, "played.db")      # The SQLite database file for played games

# Name of the table containing game data
TABLE_NAME = "games"

# Path to the Chrome executable
CHROME_PATH = r"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"  # Update this path if necessary

###############################################################################
#                             PLAYED GAME STORE                               #
###############################################################################

class PlayedGameStore:
    def __init__(self, db_file=PLAYED_DB_FILE):
        self.db_file = db_file
        try:
            self.conn = sqlite3.connect(self.db_file)
            self.create_table()
        except sqlite3.Error as e:
            raise Exception(f"Failed to connect to {self.db_file}: {e}")

    def create_table(self):
        create_table_query = """
        CREATE TABLE IF NOT EXISTS played_games (
            title TEXT PRIMARY KEY
        )
        """
        cursor = self.conn.cursor()
        cursor.execute(create_table_query)
        self.conn.commit()

    def mark_as_played(self, titles):
        cursor = self.conn.cursor()
        for title in titles:
            try:
                cursor.execute("INSERT INTO played_games (title) VALUES (?)", (title,))
            except sqlite3.IntegrityError:
                pass
        self.conn.commit()

    def is_played(self, title):
        cursor = self.conn.cursor()
        cursor.execute("SELECT 1 FROM played_games WHERE title = ?", (title,))
        return cursor.fetchone() is not None

    def close(self):
        self.conn.close()

###############################################################################
#                              LOAD GAMES DATA                                #
###############################################################################

def load_games_data():
    conn = None
    try:
        conn = sqlite3.connect(COMBINED_DB_FILE)
        query = f"""
        SELECT title, critic_score, platform, genre, release_year
        FROM {TABLE_NAME}
        """
        df = pd.read_sql_query(query, conn)
    except sqlite3.Error as e:
        raise Exception(f"Failed to connect to {COMBINED_DB_FILE}: {e}")
    finally:
        if conn:
            conn.close()

    # Drop rows with missing essential data
    df = df.dropna(subset=["title", "critic_score"])

    # Convert numeric columns to appropriate types
    df["critic_score"] = pd.to_numeric(df["critic_score"], errors="coerce").fillna(0)
    df["release_year"] = pd.to_numeric(df["release_year"], errors="coerce").fillna(0).astype(int)

    # Sort by critic_score descending
    df = df.sort_values(by="critic_score", ascending=False).reset_index(drop=True)

    return df

###############################################################################
#                              MAIN WINDOW                                    #
###############################################################################

class MainWindow(QMainWindow):
    def __init__(self, data, store):
        super().__init__()
        self.data = data
        self.store = store
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("🎮 Game Tracker")
        self.setGeometry(150, 150, 1200, 600)

        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(15, 15, 15, 15)

        self.setup_filters(main_layout)
        self.setup_action_buttons(main_layout)
        self.setup_table(main_layout)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Default to show all games
        self.view_selector.setCurrentText("All Games")
        self.filter_data()

    def setup_filters(self, main_layout):
        filter_layout = QHBoxLayout()
        filter_layout.setSpacing(10)

        control_font = QFont("Segoe UI", 10)

        search_label = QLabel("Search:")
        search_label.setFont(control_font)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter game title...")
        self.search_input.setFont(control_font)
        self.search_input.setFixedWidth(300)
        self.search_input.textChanged.connect(self.filter_data)

        view_label = QLabel("View:")
        view_label.setFont(control_font)

        self.view_selector = QComboBox()
        self.view_selector.setFixedWidth(150)
        self.view_selector.setFont(control_font)
        self.view_selector.addItems(["All Games", "Played", "Unplayed"])
        self.view_selector.currentIndexChanged.connect(self.filter_data)

        filter_layout.addWidget(search_label)
        filter_layout.addWidget(self.search_input)
        filter_layout.addWidget(view_label)
        filter_layout.addWidget(self.view_selector)
        filter_layout.addStretch()

        main_layout.addLayout(filter_layout)

    def setup_action_buttons(self, main_layout):
        button_layout = QHBoxLayout()
        btn_font = QFont("Segoe UI", 10)

        self.copy_button = QPushButton("📋 Copy Selected Titles")
        self.copy_button.setFixedHeight(35)
        self.copy_button.setFont(btn_font)
        self.copy_button.clicked.connect(self.copy_selected_titles)

        self.mark_played_button = QPushButton("✅ Mark Selected as Played")
        self.mark_played_button.setFixedHeight(35)
        self.mark_played_button.setFont(btn_font)
        self.mark_played_button.clicked.connect(self.mark_selected_as_played)

        button_layout.addWidget(self.copy_button)
        button_layout.addWidget(self.mark_played_button)
        button_layout.addStretch()

        main_layout.addLayout(button_layout)

    def setup_table(self, main_layout):
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "#", "Title", "Critic Score", "Platform", "Genre"
        ])
        self.table.setShowGrid(False)
        self.table.verticalHeader().setVisible(False)

        # Use a single color for all rows
        self.table.setAlternatingRowColors(False)

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        header.setDefaultAlignment(Qt.AlignCenter)
        header.setFont(QFont("Segoe UI", 10, QFont.Bold))

        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.MultiSelection)
        self.table.cellDoubleClicked.connect(self.handle_cell_double_click)

        main_layout.addWidget(self.table)

    def populate_table(self, df):
        self.table.setRowCount(len(df))
        for i, row in df.iterrows():
            idx_item = QTableWidgetItem(str(i + 1))
            idx_item.setTextAlignment(Qt.AlignCenter)
            title_item = QTableWidgetItem(row["title"])
            score_item = QTableWidgetItem(f"{row['critic_score']:.1f}")
            score_item.setTextAlignment(Qt.AlignCenter)
            platform_item = QTableWidgetItem(row["platform"])
            genre_item = QTableWidgetItem(row["genre"])

            # Strike through if played
            if self.store.is_played(row["title"]):
                font = QFont("Segoe UI", 10)
                font.setStrikeOut(True)
                title_item.setFont(font)

            items = [idx_item, title_item, score_item, platform_item, genre_item]
            for col, item in enumerate(items):
                self.table.setItem(i, col, item)

    def filter_data(self):
        try:
            df = self.data.copy()
            search_query = self.search_input.text().strip().lower()
            if search_query:
                df = df[df["title"].str.lower().str.contains(search_query)]

            view = self.view_selector.currentText()
            if view == "Played":
                df = df[df["title"].apply(self.store.is_played)]
            elif view == "Unplayed":
                df = df[~df["title"].apply(self.store.is_played)]

            df = df.sort_values(by="critic_score", ascending=False).reset_index(drop=True)
            self.populate_table(df)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")

    def copy_selected_titles(self):
        selected_rows = self.table.selectionModel().selectedRows()
        if selected_rows:
            selected_titles = [self.table.item(row.row(), 1).text() for row in selected_rows]
            QApplication.clipboard().setText("\n".join(selected_titles))
            QMessageBox.information(self, "Success", "Copied selected titles to clipboard.")
        else:
            QMessageBox.warning(self, "No Selection", "Please select at least one title to copy.")

    def mark_selected_as_played(self):
        selected_rows = self.table.selectionModel().selectedRows()
        if selected_rows:
            selected_titles = [self.table.item(row.row(), 1).text() for row in selected_rows]
            self.store.mark_as_played(selected_titles)
            QMessageBox.information(self, "Success", "Marked selected titles as played.")
            self.filter_data()
        else:
            QMessageBox.warning(self, "No Selection", "Please select at least one title to mark as played.")

    def handle_cell_double_click(self, row, column):
        try:
            if column == 1:
                title = self.table.item(row, 1).text()
                if self.store.is_played(title):
                    QMessageBox.information(self, "Already Played", f"'{title}' is already marked as played.")
                else:
                    self.store.mark_as_played([title])
                    QMessageBox.information(self, "Success", f"Marked '{title}' as played.")
                    self.filter_data()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")

###############################################################################
#                                DARK THEME                                   #
###############################################################################

def set_dark_theme(app):
    app.setStyle("Fusion")
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(45, 45, 45))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(30, 30, 30))
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(45, 45, 45))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.Highlight, QColor(0, 120, 215))
    palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(palette)

###############################################################################
#                                   MAIN                                      #
###############################################################################

if __name__ == "__main__":
    app = QApplication(sys.argv)
    set_dark_theme(app)

    try:
        games_data = load_games_data()
    except Exception as e:
        QMessageBox.critical(None, "Error", f"Failed to load game data: {e}")
        sys.exit(1)

    try:
        store = PlayedGameStore()
    except Exception as e:
        QMessageBox.critical(None, "Error", f"Failed to initialize PlayedGameStore: {e}")
        sys.exit(1)

    window = MainWindow(games_data, store)
    window.show()

    exit_code = app.exec_()
    store.close()
    sys.exit(exit_code)
