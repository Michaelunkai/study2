import sqlite3
import paramiko
import os
import tempfile
import sys
import requests
from bs4 import BeautifulSoup
from PyQt5 import QtWidgets, QtGui, QtCore

# SSH connection details
HOSTNAME = '54.173.176.93'
USERNAME = 'ubuntu'
KEY_PATH = '/home/ubuntu/key.pem'
REMOTE_DB_PATH = '/home/ubuntu/wishlist/wishlist.db'


def get_remote_db():
    """Retrieve the remote SQLite database file via SFTP."""
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=HOSTNAME, username=USERNAME, key_filename=KEY_PATH)

        sftp = ssh.open_sftp()
        local_path = os.path.join(tempfile.gettempdir(), 'wishlist_remote.db')
        sftp.get(REMOTE_DB_PATH, local_path)

        sftp.close()
        ssh.close()

        return local_path
    except Exception as e:
        QtWidgets.QMessageBox.critical(None, "Error", f"Failed to get remote database: {str(e)}")
        sys.exit(1)


def upload_remote_db(local_path):
    """Upload the local SQLite database file to the remote server via SFTP."""
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=HOSTNAME, username=USERNAME, key_filename=KEY_PATH)

        sftp = ssh.open_sftp()
        sftp.put(local_path, REMOTE_DB_PATH)

        sftp.close()
        ssh.close()
    except Exception as e:
        QtWidgets.QMessageBox.critical(None, "Error", f"Failed to upload database: {str(e)}")


def search_1337x(title, category=None):
    """Fetch top torrents from 1337x based on seeders for the given title."""
    base_url = "https://www.1337x.to"
    search_url = f"{base_url}/search/{title}/1/"
    torrents = []

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        }
        response = requests.get(search_url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        rows = soup.select("table.table-list tbody tr")

        for row in rows:
            columns = row.find_all("td")
            if len(columns) < 5:
                continue

            torrent_title = columns[0].select_one("a:nth-child(2)").get_text(strip=True)
            link = base_url + columns[0].select_one("a:nth-child(2)")["href"]
            seeders = int(columns[1].get_text(strip=True))

            if category == "movies" or category == "tv_shows":
                if "1080p" in torrent_title.lower() and "ita" not in torrent_title.lower() and "hindi" not in torrent_title.lower():
                    torrents.append((torrent_title, link, seeders))
            elif category == "anime":
                torrents.append((torrent_title, link, seeders))

        torrents.sort(key=lambda x: x[2], reverse=True)
    except Exception as e:
        QtWidgets.QMessageBox.critical(None, "Error", f"Failed to fetch torrents: {str(e)}")
        return []

    return torrents


def get_magnet_link(torrent_url):
    """Retrieve the magnet link from the torrent's page on 1337x.to."""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        }
        response = requests.get(torrent_url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        magnet_link = soup.select_one('a[href^="magnet:"]')['href']
        return magnet_link
    except Exception as e:
        QtWidgets.QMessageBox.critical(None, "Error", f"Failed to fetch magnet link: {str(e)}")
        return None


def download_torrent(link):
    """Open a magnet link in qBittorrent."""
    magnet_link = get_magnet_link(link)
    if magnet_link:
        try:
            os.system(f"qbittorrent {magnet_link}")
        except Exception as e:
            QtWidgets.QMessageBox.critical(None, "Error", f"Failed to open torrent: {str(e)}")
    else:
        QtWidgets.QMessageBox.warning(None, "Error", "Magnet link not found or invalid.")


class WishlistManager(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Wishlist Manager")
        self.db_path = get_remote_db()
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self.items_ids = {}
        self.init_db()
        self.init_ui()

    def init_db(self):
        """Create tables in the database if they do not exist."""
        tables = {
            "movies": "CREATE TABLE IF NOT EXISTS movies (id INTEGER PRIMARY KEY, title TEXT)",
            "tv_shows": "CREATE TABLE IF NOT EXISTS tv_shows (id INTEGER PRIMARY KEY, title TEXT)",
            "games": "CREATE TABLE IF NOT EXISTS games (id INTEGER PRIMARY KEY, title TEXT)",
            "anime": "CREATE TABLE IF NOT EXISTS anime (id INTEGER PRIMARY KEY, title TEXT)"
        }
        for create_table_sql in tables.values():
            self.cursor.execute(create_table_sql)
        self.conn.commit()

    def init_ui(self):
        """Initialize the user interface."""
        main_layout = QtWidgets.QVBoxLayout(self)
        self.text_inputs = {}
        self.list_views = {}
        categories = ["movies", "tv_shows", "games", "anime"]

        grid_layout = QtWidgets.QGridLayout()
        row = 0

        for category in categories:
            group_box = QtWidgets.QGroupBox(category.capitalize())
            group_layout = QtWidgets.QVBoxLayout()

            text_input = QtWidgets.QTextEdit()
            text_input.setMaximumHeight(50)
            self.text_inputs[category] = text_input
            group_layout.addWidget(text_input)

            button_layout = QtWidgets.QHBoxLayout()
            add_button = QtWidgets.QPushButton(f"Add {category.capitalize()}")
            add_button.clicked.connect(lambda _, cat=category: self.add_item(cat))
            button_layout.addWidget(add_button)

            choose_all_button = QtWidgets.QPushButton("Choose All")
            choose_all_button.clicked.connect(lambda _, cat=category: self.choose_all_items(cat))
            button_layout.addWidget(choose_all_button)

            remove_all_button = QtWidgets.QPushButton("Remove All")
            remove_all_button.clicked.connect(lambda _, cat=category: self.delete_listings(cat))
            button_layout.addWidget(remove_all_button)

            remove_selected_button = QtWidgets.QPushButton("Remove Selected")
            remove_selected_button.clicked.connect(lambda _, cat=category: self.delete_selected_items(cat))
            button_layout.addWidget(remove_selected_button)

            group_layout.addLayout(button_layout)

            list_view = QtWidgets.QListWidget()
            list_view.setMaximumHeight(150)
            list_view.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
            list_view.itemSelectionChanged.connect(self.refresh_marked_items)
            self.list_views[category] = list_view
            group_layout.addWidget(list_view)

            group_box.setLayout(group_layout)
            grid_layout.addWidget(group_box, row % 2, row // 2)
            row += 1

        main_layout.addLayout(grid_layout)

        view_button = QtWidgets.QPushButton("Search & Download")
        view_button.clicked.connect(self.search_and_download)
        main_layout.addWidget(view_button)

        self.refresh_all_categories()

    def add_item(self, category):
        """Add new items to the specified category."""
        titles = self.text_inputs[category].toPlainText().split('\n')
        for title in titles:
            if title.strip():
                self.cursor.execute(f"INSERT INTO {category} (title) VALUES (?)", (title.strip(),))
        self.conn.commit()
        upload_remote_db(self.db_path)
        self.refresh_items_list(category)
        self.text_inputs[category].clear()

    def delete_listings(self, category):
        """Delete all items from the specified category."""
        reply = QtWidgets.QMessageBox.question(self, "Confirm Delete", f"Are you sure you want to delete all {category.replace('_', ' ')}?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            self.cursor.execute(f"DELETE FROM {category}")
            self.conn.commit()
            upload_remote_db(self.db_path)
            self.refresh_items_list(category)

    def delete_selected_items(self, category):
        """Delete selected items from the specified category."""
        list_widget = self.list_views[category]
        selected_items = list_widget.selectedItems()
        if not selected_items:
            QtWidgets.QMessageBox.warning(self, "Error", "No items selected for deletion.")
            return
        reply = QtWidgets.QMessageBox.question(self, "Confirm Delete", "Are you sure you want to delete the selected item(s)?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            for item in selected_items:
                item_id = self.items_ids[category][list_widget.row(item)]
                self.cursor.execute(f"DELETE FROM {category} WHERE id=?", (item_id,))
            self.conn.commit()
            upload_remote_db(self.db_path)
            self.refresh_items_list(category)

    def choose_all_items(self, category):
        """Select all items in the specified category."""
        list_widget = self.list_views[category]
        for index in range(list_widget.count()):
            list_widget.item(index).setSelected(True)

    def refresh_all_categories(self):
        """Refresh all categories to display current database data."""
        for category in self.list_views.keys():
            self.refresh_items_list(category)

    def refresh_items_list(self, category):
        """Refresh the list view for the specified category."""
        list_widget = self.list_views[category]
        list_widget.clear()
        self.items_ids[category] = []
        self.cursor.execute(f"SELECT * FROM {category}")
        for item in self.cursor.fetchall():
            list_widget.addItem(item[1])
            self.items_ids[category].append(item[0])

    def refresh_marked_items(self):
        """Refresh the set of marked items."""
        self.marked_items = set()
        for category, list_widget in self.list_views.items():
            for item in list_widget.selectedItems():
                self.marked_items.add((category, item.text()))

    def search_and_download(self):
        """Search and automatically download the best torrents for selected items."""
        for category, list_widget in self.list_views.items():
            if category == "games":
                continue  # Skip games for automatic download

            for item in list_widget.selectedItems():
                title = item.text()
                torrents = search_1337x(title, category)
                if torrents:
                    best_torrent = torrents[0]  # Automatically choose the best torrent
                    _, link, _ = best_torrent
                    download_torrent(link)


app = QtWidgets.QApplication(sys.argv)
window = WishlistManager()
window.show()
sys.exit(app.exec_())
