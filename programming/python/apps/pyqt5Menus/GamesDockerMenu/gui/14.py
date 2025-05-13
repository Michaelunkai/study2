import sys
import os
import subprocess
import requests
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout,
    QScrollArea, QLineEdit, QGridLayout, QDesktopWidget, QLabel, QFrame,
    QMenu, QDialog, QListWidget, QMessageBox, QInputDialog
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QTimer

class StyledButton(QPushButton):
    def __init__(self, text, color, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                border: none;
                border-radius: 5px;
                padding: 10px;
                color: white;
                font-weight: bold;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background-color: {color}99;
                border: 2px solid white;
            }}
            QPushButton:pressed {{
                background-color: {color}77;
            }}
        """)

class GameButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("""
            QPushButton {
                background-color: #2C3E50;
                border: none;
                border-radius: 8px;
                padding: 15px;
                color: white;
                font-size: 12px;
                min-height: 50px;
                text-align: center;
            }
            QPushButton:hover {
                background-color: #34495E;
                border: 2px solid #3498DB;
            }
            QPushButton:pressed {
                background-color: #2980B9;
            }
        """)

class DeleteTagDialog(QDialog):
    def __init__(self, all_tags, parent=None):
        super().__init__(parent)
        self.all_tags = all_tags  # List of dictionaries with tag info.
        self.setWindowTitle("Delete Tag")
        self.setMinimumSize(400, 400)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search tag to delete...")
        layout.addWidget(self.search_box)
        self.list_widget = QListWidget()
        # Allow multi-selection.
        self.list_widget.setSelectionMode(QListWidget.ExtendedSelection)
        layout.addWidget(self.list_widget)
        # Populate list widget with tag names.
        for tag_info in self.all_tags:
            self.list_widget.addItem(tag_info['name'])
        self.search_box.textChanged.connect(self.filter_list)
        
        # Add a "Delete Selected" button.
        self.delete_button = QPushButton("Delete Selected")
        self.delete_button.setStyleSheet("""
            QPushButton {
                background-color: #C0392B;
                border: none;
                border-radius: 8px;
                padding: 12px;
                color: white;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #E74C3C;
            }
            QPushButton:pressed {
                background-color: #A93226;
            }
        """)
        self.delete_button.clicked.connect(self.delete_selected)
        layout.addWidget(self.delete_button)

    def filter_list(self, text):
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            item.setHidden(text.lower() not in item.text().lower())

    def delete_selected(self):
        selected_items = self.list_widget.selectedItems()
        if not selected_items:
            QMessageBox.information(self, "No Selection", "Please select at least one tag to delete.")
            return
        tags = [item.text() for item in selected_items]
        reply = QMessageBox.question(
            self, "Confirm Delete",
            "Are you sure you want to delete the following tags from Docker Hub?\n" + "\n".join(tags),
            QMessageBox.Yes | QMessageBox.No
        )
        if reply != QMessageBox.Yes:
            return
        # Ask for Docker Hub password.
        password, ok = QInputDialog.getText(
            self, "Docker Hub Authentication",
            "Enter Docker Hub password:", QLineEdit.Password
        )
        if not (ok and password):
            return

        # Replace with your Docker Hub username and repository name.
        username = "michadockermisha"
        repo = "backup"
        # Log in to obtain an authentication token.
        login_url = "https://hub.docker.com/v2/users/login/"
        login_data = {"username": username, "password": password}
        login_response = requests.post(login_url, json=login_data)
        if login_response.status_code != 200:
            QMessageBox.warning(self, "Error", f"Failed to log in:\n{login_response.text}")
            return
        token = login_response.json().get("token")
        if not token:
            QMessageBox.warning(self, "Error", "Login succeeded but no token was returned.")
            return
        headers = {"Authorization": f"JWT {token}"}
        successes = []
        failures = []
        for tag in tags:
            delete_url = f"https://hub.docker.com/v2/repositories/{username}/{repo}/tags/{tag}/"
            delete_response = requests.delete(delete_url, headers=headers)
            if delete_response.status_code == 204:
                successes.append(tag)
            else:
                failures.append((tag, delete_response.status_code, delete_response.text))
        message = ""
        if successes:
            message += "Successfully deleted:\n" + "\n".join(successes) + "\n\n"
            # Remove successfully deleted items from the list widget.
            for tag in successes:
                items = self.list_widget.findItems(tag, Qt.MatchExactly)
                for item in items:
                    row = self.list_widget.row(item)
                    self.list_widget.takeItem(row)
        if failures:
            message += "Failed to delete:\n" + "\n".join([f"{tag} (Status {status})" for tag, status, _ in failures])
            QMessageBox.warning(self, "Deletion Summary", message)
        else:
            QMessageBox.information(self, "Deletion Summary", message)
        # Notify parent to refresh its tag list.
        if self.parent() and hasattr(self.parent(), "refresh_tags"):
            self.parent().refresh_tags()

class DockerApp(QWidget):
    def __init__(self):
        super().__init__()
        # Fetch all tags and their sizes from Docker Hub (handles pagination)
        self.all_tags = self.fetch_tags()
        self.setWindowTitle("Docker Tag Launcher")

        # Queues for docker commands.
        self.download_queue = []
        self.active_downloads = []

        # QTimer to check download status every second.
        self.timer = QTimer()
        self.timer.timeout.connect(self.process_downloads)
        self.timer.start(1000)

        # Set window geometry based on desktop size.
        desktop_geometry = QDesktopWidget().screenGeometry()
        width = int(desktop_geometry.width() * 19 / 20)
        height = int(desktop_geometry.height() * 19 / 20)
        self.setGeometry(0, 0, width, height)

        # Dark theme styling.
        self.setStyleSheet("""
            QWidget {
                background-color: #1E1E1E;
                color: white;
            }
            QScrollArea {
                border: none;
                background-color: #1E1E1E;
            }
            QScrollBar:vertical {
                border: none;
                background: #2C2C2C;
                width: 14px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #3E3E3E;
                min-height: 20px;
                border-radius: 7px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
        """)

        self.init_ui()

    def fetch_tags(self):
        """
        Fetch every tag available from the Docker Hub repository along with its size.
        This method handles pagination to ensure all tags are retrieved.
        """
        url = "https://hub.docker.com/v2/repositories/michadockermisha/backup/tags?page_size=100"
        tag_list = []
        while url:
            try:
                response = requests.get(url)
                data = response.json()
                for item in data.get('results', []):
                    tag_list.append({
                        'name': item['name'],
                        'full_size': item.get('full_size', 0)
                    })
                url = data.get("next")  # Next page URL if available.
            except Exception as e:
                print("Error fetching tags:", e)
                break
        tag_list.sort(key=lambda x: x['name'].lower())
        return tag_list

    def format_size(self, size):
        """
        Convert a size in bytes into a human-readable string.
        """
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024:
                return f"{size:.1f}{unit}"
            size /= 1024
        return f"{size:.1f}PB"

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Title label.
        title = QLabel("Docker Tag Launcher")
        title.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                font-weight: bold;
                padding: 10px;
            }
        """)
        main_layout.addWidget(title, alignment=Qt.AlignCenter)

        # Horizontal layout for search, sort, and delete controls.
        control_layout = QHBoxLayout()
        control_layout.setSpacing(10)

        # Search box.
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search tags...")
        self.search_box.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                font-size: 16px;
                background-color: #252525;
                border: 2px solid #3E3E3E;
                border-radius: 8px;
                color: white;
            }
            QLineEdit:focus {
                border: 2px solid #3498DB;
            }
        """)
        self.search_box.textChanged.connect(self.filter_buttons)
        control_layout.addWidget(self.search_box)

        # Sort button.
        sort_button = QPushButton("Sort")
        sort_button.setStyleSheet("""
            QPushButton {
                background-color: #3E3E3E;
                border: none;
                border-radius: 8px;
                padding: 12px;
                color: white;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #4E4E4E;
            }
            QPushButton:pressed {
                background-color: #2E2E2E;
            }
        """)
        sort_menu = QMenu(self)
        action_heavy = sort_menu.addAction("Heaviest to Lightest")
        action_light = sort_menu.addAction("Lightest to Heaviest")
        action_heavy.triggered.connect(lambda: self.sort_tags(descending=True))
        action_light.triggered.connect(lambda: self.sort_tags(descending=False))
        sort_button.setMenu(sort_menu)
        control_layout.addWidget(sort_button)

        # "Delete Tag" button.
        delete_button = QPushButton("Delete Tag")
        delete_button.setStyleSheet("""
            QPushButton {
                background-color: #C0392B;
                border: none;
                border-radius: 8px;
                padding: 12px;
                color: white;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #E74C3C;
            }
            QPushButton:pressed {
                background-color: #A93226;
            }
        """)
        delete_button.clicked.connect(self.open_delete_dialog)
        control_layout.addWidget(delete_button)

        main_layout.addLayout(control_layout)

        # Container for tag buttons inside a scrollable area.
        container = QFrame()
        container.setStyleSheet("""
            QFrame {
                background-color: #252525;
                border-radius: 10px;
                padding: 15px;
            }
        """)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_area.setWidget(scroll_widget)

        # Grid layout for tag buttons.
        self.grid_layout = QGridLayout(scroll_widget)
        self.grid_layout.setSpacing(10)
        self.create_tag_buttons()

        container.setLayout(QVBoxLayout())
        container.layout().addWidget(scroll_area)
        main_layout.addWidget(container)

    def create_tag_buttons(self):
        for i in reversed(range(self.grid_layout.count())):
            widget = self.grid_layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)
        self.buttons = []
        row, col = 0, 0
        for tag_info in self.all_tags:
            display_text = f"{tag_info['name']} ({self.format_size(tag_info['full_size'])})"
            button = GameButton(display_text)
            button.clicked.connect(lambda checked, t=tag_info: self.queue_docker_command(t))
            self.grid_layout.addWidget(button, row, col)
            col += 1
            if col == 4:
                col = 0
                row += 1
            self.buttons.append(button)

    def sort_tags(self, descending=True):
        self.all_tags.sort(key=lambda x: x['full_size'], reverse=descending)
        self.create_tag_buttons()

    def queue_docker_command(self, tag_info):
        tag = tag_info['name']
        docker_command = (
            f'docker run '
            f'--rm '
            f'-v /mnt/c/games:/mnt/c/games '
            f'-e DISPLAY=$DISPLAY '
            f'-v /tmp/.X11-unix:/tmp/.X11-unix '
            f'--name "{tag}" '
            f'michadockermisha/backup:"{tag}" '
            f'sh -c "apk add rsync && rsync -aP /home /mnt/c/games && mv /mnt/c/games/home /mnt/c/games/{tag}"'
        )
        self.download_queue.append(docker_command)
        print(f"Queued: {tag}")

    def process_downloads(self):
        while len(self.active_downloads) < 3 and self.download_queue:
            cmd = self.download_queue.pop(0)
            process = subprocess.Popen(cmd, shell=True)
            self.active_downloads.append((cmd, process))
            print(f"Started: {cmd}")
        still_active = []
        for (cmd, proc) in self.active_downloads:
            ret = proc.poll()
            if ret is None:
                still_active.append((cmd, proc))
            else:
                if ret == 0:
                    print(f"Success: {cmd}")
                else:
                    print(f"Failed: {cmd} -- re-queueing!")
                    self.download_queue.append(cmd)
        self.active_downloads = still_active

    def filter_buttons(self, text):
        for button in self.buttons:
            button.setVisible(text.lower() in button.text().lower())

    def open_delete_dialog(self):
        dialog = DeleteTagDialog(self.all_tags, parent=self)
        dialog.exec_()

    def refresh_tags(self):
        self.all_tags = self.fetch_tags()
        self.create_tag_buttons()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    docker_app = DockerApp()
    docker_app.show()
    sys.exit(app.exec_())
