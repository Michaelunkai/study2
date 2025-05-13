import sys
import os
import subprocess
import requests
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout,
    QScrollArea, QLineEdit, QGridLayout, QDesktopWidget, QLabel, QFrame,
    QMenu, QDialog, QListWidget, QListWidgetItem, QMessageBox, QInputDialog
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QTimer

# Styled button used for control layouts.
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

# Each tag is represented by a checkable button.
class GameButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setCheckable(True)
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
            QPushButton:checked {
                background-color: #3498DB;
            }
            QPushButton:hover {
                background-color: #34495E;
                border: 2px solid #3498DB;
            }
            QPushButton:pressed {
                background-color: #2980B9;
            }
        """)

# Dialog for deleting tags (supports multi‑selection).
class DeleteTagDialog(QDialog):
    def __init__(self, all_tags, parent=None):
        super().__init__(parent)
        self.all_tags = all_tags  # List of dictionaries with tag info.
        self.setWindowTitle("Delete Tag")
        self.setMinimumSize(400, 400)
        self.init_ui()

    def format_size(self, size):
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024:
                return f"{size:.1f}{unit}"
            size /= 1024
        return f"{size:.1f}PB"

    def init_ui(self):
        layout = QVBoxLayout(self)
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search tag to delete...")
        layout.addWidget(self.search_box)
        self.list_widget = QListWidget()
        # Allow multi-selection (non‑contiguous selection is allowed).
        self.list_widget.setSelectionMode(QListWidget.MultiSelection)
        layout.addWidget(self.list_widget)
        # Sort tags lightest to heaviest.
        sorted_tags = sorted(self.all_tags, key=lambda x: x['full_size'])
        for tag_info in sorted_tags:
            display_text = f"{tag_info['name']} ({self.format_size(tag_info['full_size'])})"
            item = QListWidgetItem(display_text)
            item.setData(Qt.UserRole, tag_info)
            self.list_widget.addItem(item)
        self.search_box.textChanged.connect(self.filter_list)
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
            tag_info = item.data(Qt.UserRole)
            tag_name = tag_info['name']
            item.setHidden(text.lower() not in tag_name.lower())

    def delete_selected(self):
        selected_items = self.list_widget.selectedItems()
        if not selected_items:
            QMessageBox.information(self, "No Selection", "Please select at least one tag to delete.")
            return
        tags = [item.data(Qt.UserRole)['name'] for item in selected_items]
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

        username = "michadockermisha"  # Replace with your Docker Hub username.
        repo = "backup"               # Replace with your repository.
        # Log in to obtain a JWT token.
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
        # Delete each selected tag.
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
            # Remove deleted tags from the list.
            for tag in successes:
                items = self.list_widget.findItems(tag, Qt.MatchContains)
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

# Main application window.
class DockerApp(QWidget):
    def __init__(self):
        super().__init__()
        # Fetch all tags (including full_size) from Docker Hub (handles pagination).
        self.all_tags = self.fetch_tags()
        self.setWindowTitle("Docker Tag Launcher")
        # List to hold running processes for the "Run Selected" commands.
        self.run_processes = []
        self.init_ui()

    def fetch_tags(self):
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
                url = data.get("next")
            except Exception as e:
                print("Error fetching tags:", e)
                break
        tag_list.sort(key=lambda x: x['name'].lower())
        return tag_list

    def format_size(self, size):
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024:
                return f"{size:.1f}{unit}"
            size /= 1024
        return f"{size:.1f}PB"

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)
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
        # "Run Selected" button.
        run_selected = QPushButton("Run Selected")
        run_selected.setStyleSheet("""
            QPushButton {
                background-color: #27AE60;
                border: none;
                border-radius: 8px;
                padding: 12px;
                color: white;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #2ECC71;
            }
            QPushButton:pressed {
                background-color: #1E8449;
            }
        """)
        run_selected.clicked.connect(self.run_selected_commands)
        control_layout.addWidget(run_selected)
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
        # Container for tag buttons in a scrollable area.
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
        self.grid_layout = QGridLayout(scroll_widget)
        self.grid_layout.setSpacing(10)
        self.create_tag_buttons()
        container.setLayout(QVBoxLayout())
        container.layout().addWidget(scroll_area)
        main_layout.addWidget(container)

    def create_tag_buttons(self):
        for i in reversed(range(self.grid_layout.count())):
            widget = self.grid_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        self.buttons = []
        row, col = 0, 0
        for tag_info in self.all_tags:
            display_text = f"{tag_info['name']} ({self.format_size(tag_info['full_size'])})"
            button = GameButton(display_text)
            button.tag_info = tag_info
            self.grid_layout.addWidget(button, row, col)
            col += 1
            if col == 4:
                col = 0
                row += 1
            self.buttons.append(button)

    def sort_tags(self, descending=True):
        self.all_tags.sort(key=lambda x: x['full_size'], reverse=descending)
        self.create_tag_buttons()

    def filter_buttons(self, text):
        for button in self.buttons:
            tag_name = button.tag_info['name']
            button.setVisible(text.lower() in tag_name.lower())

    def run_selected_commands(self):
        selected_buttons = [btn for btn in self.buttons if btn.isChecked()]
        if not selected_buttons:
            QMessageBox.information(self, "No Selection", "Please select at least one tag to run.")
            return
        processes = []
        for btn in selected_buttons:
            tag = btn.tag_info['name']
            # Updated docker command:
            # It now creates its own folder and rsyncs directly into /mnt/c/games/<tag>
            docker_command = (
                f'docker run '
                f'--rm '
                f'-v /mnt/c/games:/mnt/c/games '
                f'-e DISPLAY=$DISPLAY '
                f'-v /tmp/.X11-unix:/tmp/.X11-unix '
                f'--name "{tag}" '
                f'michadockermisha/backup:"{tag}" '
                f'sh -c "apk add rsync && mkdir -p /mnt/c/games/{tag} && rsync -aP /home/ /mnt/c/games/{tag}"'
            )
            proc = subprocess.Popen(docker_command, shell=True)
            processes.append((tag, proc))
        # Disable the Run Selected button until all finish.
        sender = self.sender()
        sender.setEnabled(False)
        self.run_processes = processes
        self.run_timer = QTimer()
        self.run_timer.timeout.connect(lambda: self.check_run_processes(sender))
        self.run_timer.start(500)

    def check_run_processes(self, run_button):
        still_running = []
        for tag, proc in self.run_processes:
            if proc.poll() is None:
                still_running.append((tag, proc))
        if not still_running:
            self.run_timer.stop()
            run_button.setEnabled(True)
            QMessageBox.information(self, "Run Complete", "All selected commands have finished.")
        self.run_processes = still_running

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
