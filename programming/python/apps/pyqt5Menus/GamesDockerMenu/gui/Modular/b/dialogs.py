import json
import subprocess
import time
from functools import partial
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QPushButton, QInputDialog, QMessageBox,
                             QLineEdit, QGridLayout, QLabel, QListWidget, QListWidgetItem,
                             QCheckBox, QTextEdit)
from PyQt5.QtCore import Qt
from persistence import save_active_users, load_active_users, load_banned_users, save_banned_users
from ui_components import TabGridWidget

def update_docker_tag_name(old_alias, new_alias):
    QMessageBox.information(None, "Info",
        "Renaming tags on Docker Hub is not supported by the API.\nOnly the local display name (alias) will be updated.")
    return True

class MyLinersDialog(QDialog):
    def __init__(self, parent=None):
        super(MyLinersDialog, self).__init__(parent)
        self.setWindowTitle("My Liners")
        self.btn_defs = [
            ("BackItUp", "wsl --distribution ubuntu --user root -- bash -lic 'backitup'"),
            ("BigiTGo", "wsl --distribution ubuntu --user root -- bash -lic 'bigitgo'"),
            ("gg", "wsl --distribution ubuntu --user root -- bash -lic 'gg'"),
            ("dcreds", "wsl --distribution ubuntu --user root -- bash -lic 'dcreds'"),
            ("savegames", "wsl --distribution ubuntu --user root -- bash -lic 'savegames'"),
            ("GameSaveRestore", "wsl --distribution ubuntu --user root -- bash -lic 'gamedg'")
        ]
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        existing_buttons = {}
        self.load_custom_buttons()
        for label, cmd in self.btn_defs:
            if label not in existing_buttons:
                btn = self.create_button(label, cmd)
                layout.addWidget(btn)
                existing_buttons[label] = btn

        add_button_btn = QPushButton("Add Custom Button")
        add_button_btn.setStyleSheet("""
            QPushButton {
                background: #16A085;
                color: white;
                padding: 8px 12px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background: #1ABC9C;
            }
        """)
        add_button_btn.clicked.connect(self.add_custom_button)
        layout.addWidget(add_button_btn)

        remove_button_btn = QPushButton("Remove Custom Button")
        remove_button_btn.setStyleSheet("""
            QPushButton {
                background: #E74C3C;
                color: white;
                padding: 8px 12px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background: #C0392B;
            }
        """)
        remove_button_btn.clicked.connect(self.remove_custom_button)
        layout.addWidget(remove_button_btn)

        self.setLayout(layout)

    def create_button(self, label, cmd):
        btn = QPushButton(label)
        btn.setStyleSheet("""
            QPushButton {
                background: #34495E;
                color: white;
                padding: 8px 12px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background: #2C3E50;
            }
        """)
        btn.clicked.connect(partial(self.run_command, cmd))
        return btn

    def run_command(self, cmd):
        try:
            subprocess.Popen(cmd, shell=True)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error running command: {e}")

    def add_custom_button(self):
        name, ok_name = QInputDialog.getText(self, "Custom Button", "Enter button name:")
        if not ok_name or not name:
            return

        cmd, ok_cmd = QInputDialog.getText(self, "Custom Command", "Enter command to execute:")
        if not ok_cmd or not cmd:
            return

        self.btn_defs.append((name, cmd))
        self.save_custom_buttons()
        btn = self.create_button(name, cmd)
        self.layout().addWidget(btn)

    def remove_custom_button(self):
        names = [label for label, _ in self.btn_defs if label not in ["BackItUp", "BigiTGo", "gg", "dcreds", "savegames", "GameSaveRestore"]]
        name, ok = QInputDialog.getItem(self, "Remove Custom Button", "Select button to remove:", names, editable=False)
        if not ok or not name:
            return
        self.btn_defs = [(label, cmd) for label, cmd in self.btn_defs if label != name]
        self.save_custom_buttons()
        self.init_ui()

    def load_custom_buttons(self):
        try:
            with open("custom_buttons.json", "r") as f:
                custom_buttons = json.load(f)
                self.btn_defs.extend(custom_buttons)
        except (FileNotFoundError, json.JSONDecodeError):
            pass

    def save_custom_buttons(self):
        try:
            with open("custom_buttons.json", "w") as f:
                json.dump(self.btn_defs, f)
        except Exception as e:
            print(f"Error saving custom buttons: {e}")

class MoveToDialog(QDialog):
    def __init__(self, tabs_config, parent=None):
        super(MoveToDialog, self).__init__(parent)
        self.setWindowTitle("Select Target Tab")
        self.selected_tab_id = None
        self.tabs_config = tabs_config
        self.init_ui()
    def init_ui(self):
        layout = QGridLayout(self)
        col = 0
        row = 0
        for tab in self.tabs_config:
            btn = QPushButton(tab["name"])
            btn.setCheckable(True)
            btn.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                stop:0 #34495E, stop:1 #2C3E50);
                    color: #F1C40F;
                    padding: 6px 10px;
                    border-radius: 4px;
                }
                QPushButton:checked {
                    background: #F39C12;
                }
            """)
            btn.clicked.connect(partial(self.select_tab, tab["id"], btn))
            layout.addWidget(btn, row, col)
            col += 1
            if col >= 5:
                col = 0
                row += 1
        self.setLayout(layout)
    def select_tab(self, tab_id, btn):
        self.selected_tab_id = tab_id
        for widget in self.findChildren(QPushButton):
            if widget is not btn:
                widget.setChecked(False)
        self.accept()

class BulkMoveDialog(QDialog):
    def __init__(self, all_tags, tabs_config, parent=None):
        super(BulkMoveDialog, self).__init__(parent)
        self.all_tags = all_tags
        self.tabs_config = tabs_config
        self.setWindowTitle("Bulk Move Tags")
        self.setMinimumSize(400, 500)
        self.init_ui()
    def init_ui(self):
        layout = QVBoxLayout(self)
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search tags...")
        self.search_box.setStyleSheet("padding: 6px; border-radius: 4px;")
        self.search_box.textChanged.connect(self.filter_list)
        layout.addWidget(self.search_box)
        self.list_widget = QListWidget()
        self.list_widget.setStyleSheet("padding: 4px;")
        self.list_widget.setSelectionMode(QListWidget.MultiSelection)
        layout.addWidget(self.list_widget)
        self.populate_list()
        layout.addWidget(QLabel("Move selected tags to:"))
        self.tab_grid = TabGridWidget(self.tabs_config)
        layout.addWidget(self.tab_grid)
        self.move_button = QPushButton("Move Selected")
        self.move_button.setStyleSheet("""
            QPushButton {
                background: #27AE60;
                color: white;
                padding: 8px 12px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background: #2ECC71;
            }
        """)
        self.move_button.clicked.connect(self.move_tags)
        layout.addWidget(self.move_button)
        self.setLayout(layout)
    def populate_list(self):
        self.list_widget.clear()
        for tag in self.all_tags:
            item = QListWidgetItem(tag["alias"])
            self.list_widget.addItem(item)
            item.setData(Qt.UserRole, tag)
    def filter_list(self, text):
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            tag = item.data(Qt.UserRole)
            item.setHidden(text.lower() not in tag["alias"].lower())
    def move_tags(self):
        selected = self.list_widget.selectedItems()
        if not selected:
            QMessageBox.information(self, "No Selection", "Please select at least one tag to move.")
            return
        if not self.tab_grid.selected_tab_id:
            QMessageBox.information(self, "No Tab Selected", "Please select a target tab from the grid.")
            return
        target_tab_id = self.tab_grid.selected_tab_id
        for item in selected:
            tag = item.data(Qt.UserRole)
            tag["category"] = target_tab_id
        QMessageBox.information(self, "Bulk Move", "Selected tags moved.")
        self.accept()

class BulkPasteMoveDialog(QDialog):
    def __init__(self, all_tags, tabs_config, parent=None):
        super(BulkPasteMoveDialog, self).__init__(parent)
        self.all_tags = all_tags
        self.tabs_config = tabs_config
        self.setWindowTitle("Bulk Paste Move Tags")
        self.setMinimumSize(400, 400)
        self.init_ui()
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Paste tag names (one per line):"))
        self.text_edit = QTextEdit()
        self.text_edit.setStyleSheet("padding: 6px; border: 1px solid #ccc; border-radius: 4px;")
        layout.addWidget(self.text_edit)
        layout.addWidget(QLabel("Move pasted tags to:"))
        self.tab_grid = TabGridWidget(self.tabs_config)
        layout.addWidget(self.tab_grid)
        move_button = QPushButton("Move Pasted Tags")
        move_button.setStyleSheet("""
            QPushButton {
                background: #F39C12;
                color: white;
                padding: 8px 12px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background: #F1C40F;
            }
        """)
        move_button.clicked.connect(self.move_pasted_tags)
        layout.addWidget(move_button)
        self.setLayout(layout)
    def move_pasted_tags(self):
        lines = self.text_edit.toPlainText().splitlines()
        pasted = [line.strip().lower() for line in lines if line.strip()]
        if not pasted:
            QMessageBox.information(self, "No Input", "Please paste at least one tag name.")
            return
        if not self.tab_grid.selected_tab_id:
            QMessageBox.information(self, "No Tab Selected", "Please select a target tab from the grid.")
            return
        target_tab_id = self.tab_grid.selected_tab_id
        moved = 0
        for tag in self.all_tags:
            if tag["alias"].lower() in pasted:
                tag["category"] = target_tab_id
                moved += 1
        QMessageBox.information(self, "Bulk Paste Move", f"Moved {moved} tag(s) to selected tab.")
        self.accept()

class DeleteTagDialog(QDialog):
    def __init__(self, all_tags, parent=None):
        super(DeleteTagDialog, self).__init__(parent)
        self.all_tags = all_tags
        self.setWindowTitle("Delete Tag")
        self.setMinimumSize(400, 400)
        self.init_ui()
    def format_size(self, size):
        for unit in ["B", "KB", "MB", "GB", "TB"]:
            if size < 1024:
                return f"{size:.1f}{unit}"
            size /= 1024
        return f"{size:.1f}PB"
    def init_ui(self):
        layout = QVBoxLayout(self)
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search tag to delete...")
        self.search_box.setStyleSheet("padding: 6px; border-radius: 4px;")
        layout.addWidget(self.search_box)
        self.dup_checkbox = QCheckBox("Show only duplicate tags")
        layout.addWidget(self.dup_checkbox)
        self.dup_checkbox.stateChanged.connect(self.populate_list)
        self.list_widget = QListWidget()
        self.list_widget.setStyleSheet("padding: 4px;")
        self.list_widget.setSelectionMode(QListWidget.MultiSelection)
        layout.addWidget(self.list_widget)
        self.populate_list()
        self.search_box.textChanged.connect(self.filter_list)
        self.delete_button = QPushButton("Delete Selected")
        self.delete_button.setStyleSheet("""
            QPushButton {
                background: #C0392B;
                color: white;
                padding: 8px 12px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background: #E74C3C;
            }
        """)
        self.delete_button.clicked.connect(self.delete_selected)
        layout.addWidget(self.delete_button)
        self.setLayout(layout)
    def populate_list(self):
        self.list_widget.clear()
        only_duplicates = self.dup_checkbox.isChecked()
        alias_counts = {}
        for tag in self.all_tags:
            alias = tag["alias"]
            alias_counts[alias] = alias_counts.get(alias, 0) + 1
        for tag in self.all_tags:
            if only_duplicates and alias_counts[tag["alias"]] <= 1:
                continue
            display_text = f"{tag['alias']} ({self.format_size(tag['full_size'])})"
            item = QListWidgetItem(display_text)
            item.setData(Qt.UserRole, tag)
            self.list_widget.addItem(item)
    def filter_list(self, text):
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            tag = item.data(Qt.UserRole)
            item.setHidden(text.lower() not in tag["alias"].lower())
    def delete_selected(self):
        selected_items = self.list_widget.selectedItems()
        if not selected_items:
            QMessageBox.information(self, "No Selection", "Please select at least one tag to delete.")
            return
        tags = [item.data(Qt.UserRole)["docker_name"] for item in selected_items]
        reply = QMessageBox.question(
            self, "Confirm Delete",
            "Are you sure you want to delete the following tags from Docker Hub?\n" + "\n".join(tags),
            QMessageBox.Yes | QMessageBox.No
        )
        if reply != QMessageBox.Yes:
            return
        parent = self.parent()
        token = parent.get_docker_token() if parent and hasattr(parent, "get_docker_token") else None
        if not token:
            return
        username = "michadockermisha"
        repo = "backup"
        headers = {"Authorization": f"JWT {token}"}
        successes = []
        failures = []
        import requests
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
        if parent and hasattr(parent, "refresh_tags"):
            parent.refresh_tags()

class UserDashboardDialog(QDialog):
    def __init__(self, parent=None):
        super(UserDashboardDialog, self).__init__(parent)
        self.setWindowTitle("User Dashboard")
        self.setMinimumSize(400, 300)
        self.init_ui()
    def init_ui(self):
        layout = QVBoxLayout(self)
        self.user_list = QListWidget()
        self.user_list.setStyleSheet("padding: 4px;")
        layout.addWidget(self.user_list)
        add_user_btn = QPushButton("Add New User")
        add_user_btn.setStyleSheet("""
            QPushButton {
                background: #27AE60;
                color: white;
                padding: 8px 12px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background: #2ECC71;
            }
        """)
        add_user_btn.clicked.connect(self.add_new_user)
        layout.addWidget(add_user_btn)
        kick_button = QPushButton("Kick Selected User")
        kick_button.setStyleSheet("""
            QPushButton {
                background: #C0392B;
                color: white;
                padding: 8px 12px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background: #E74C3C;
            }
        """)
        kick_button.clicked.connect(self.kick_selected)
        layout.addWidget(kick_button)
        refresh_button = QPushButton("Refresh")
        refresh_button.setStyleSheet("""
            QPushButton {
                background: #2980B9;
                color: white;
                padding: 8px 12px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background: #3498DB;
            }
        """)
        refresh_button.clicked.connect(self.populate_users)
        layout.addWidget(refresh_button)
        self.setLayout(layout)
        self.populate_users()
    def populate_users(self):
        self.user_list.clear()
        from persistence import load_active_users
        users = load_active_users()
        for username in users:
            item = QListWidgetItem(username)
            self.user_list.addItem(item)
    def kick_selected(self):
        selected = self.user_list.currentItem()
        if not selected:
            QMessageBox.information(self, "No Selection", "Please select a user to kick.")
            return
        username = selected.text()
        from persistence import load_banned_users, save_banned_users, load_active_users, save_active_users
        banned = load_banned_users()
        if username not in banned:
            banned.append(username)
            save_banned_users(banned)
        users = load_active_users()
        if username in users:
            del users[username]
            save_active_users(users)
        QMessageBox.information(self, "User Kicked", f"User '{username}' has been kicked.")
        self.populate_users()
    def add_new_user(self):
        new_user, ok = QInputDialog.getText(self, "Add New User", "Enter new username:")
        if ok and new_user:
            new_user = new_user.strip().lower()
            from persistence import load_active_users, save_active_users
            users = load_active_users()
            if new_user in users:
                QMessageBox.information(self, "User Exists", f"User '{new_user}' already exists.")
                return
            users[new_user] = {"login_time": time.time()}
            save_active_users(users)
            QMessageBox.information(self, "User Added", f"User '{new_user}' has been added.")
            self.populate_users()

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton
class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super(LoginDialog, self).__init__(parent)
        self.setWindowTitle("Login")
        self.login_password = None
        self.is_admin = False
        self.username = None
        self.init_ui()
    def init_ui(self):
        layout = QVBoxLayout(self)
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet("padding: 8px; border: 2px solid #1ABC9C; border-radius: 6px;")
        layout.addWidget(self.password_input)
        login_button = QPushButton("Login")
        login_button.setStyleSheet("""
            QPushButton {
                background: #16A085;
                color: white;
                padding: 8px 12px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background: #1ABC9C;
            }
        """)
        login_button.clicked.connect(self.handle_login)
        layout.addWidget(login_button)
        self.setLayout(layout)
    def handle_login(self):
        entered = self.password_input.text().strip()
        if not entered:
            QMessageBox.warning(self, "Login Failed", "Password is required.")
            return
        if entered != "123456":
            self.is_admin = True
            self.login_password = entered
            self.username = "michadockermisha"
            self.accept()
        else:
            username, ok = QInputDialog.getText(self, "Username Required", "Enter username:")
            if not (ok and username):
                QMessageBox.warning(self, "Login Failed", "Username is required for normal users.")
                return
            if username.strip().lower() != "meir":
                QMessageBox.warning(self, "Login Failed", "Only user 'meir' is allowed for normal user privileges.")
                return
            from persistence import load_banned_users
            banned = load_banned_users()
            if username.strip().lower() in banned:
                QMessageBox.warning(self, "Access Denied", "This user has been banned from using the app.")
                return
            self.is_admin = False
            self.login_password = entered
            self.username = username.strip().lower()
            self.accept()
