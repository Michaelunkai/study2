import sys
import os
import time
import subprocess
from functools import partial

# Import all required PyQt5 widgets (including QPushButton)
from PyQt5.QtWidgets import (
    QWidget, QApplication, QVBoxLayout, QHBoxLayout, QFileDialog, QLabel,
    QLineEdit, QStackedWidget, QScrollArea, QMessageBox, QInputDialog, QPushButton
)
from PyQt5.QtGui import QFont, QPixmap, QImage
from PyQt5.QtCore import Qt, QTimer, QThreadPool

# Local modules
from persistence import load_settings, save_settings, load_tabs_config, load_banned_users, load_active_users, save_active_users, clear_session
from docker_ops import start_docker_engine, dkill, check_docker_engine
from network_ops import fetch_game_time, fetch_image
from workers import Worker, DockerPullWorker
from ui_components import TagContainerWidget, TabNavigationWidget, GameButton
from dialogs import MyLinersDialog, BulkMoveDialog, BulkPasteMoveDialog, DeleteTagDialog, UserDashboardDialog
from utils import parse_date, pixmap_to_base64

# Global persistent settings and tab configuration
persistent_settings = load_settings()
tabs_config = load_tabs_config()
banned_users = load_banned_users()

def load_time_data(file_path):
    time_data = {}
    try:
        with open(file_path, "r", encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if "–" in line:
                    parts = line.split("–")
                    tag = parts[0].strip().lower()
                    time_val = parts[1].strip()
                    time_data[tag] = time_val
    except Exception as e:
        print(f"Error loading time data: {e}")
    return time_data

time_data = load_time_data("time.txt")

class DockerApp(QWidget):
    def __init__(self, login_password, is_admin, username):
        super(DockerApp, self).__init__()
        self.login_password = login_password
        self.is_admin = is_admin
        self.username = username

        start_docker_engine()
        if self.is_admin:
            self.docker_token = self.perform_docker_login()
        else:
            self.docker_token = None

        self.all_tags = self.fetch_tags()
        for tag in self.all_tags:
            tag["docker_name"] = tag["name"]
            tag["alias"] = persistent_settings.get(tag["docker_name"], {}).get("alias", tag["docker_name"])
            stored_cat = persistent_settings.get(tag["docker_name"], {}).get("category", "all")
            tag["category"] = stored_cat if any(tab["id"] == stored_cat for tab in tabs_config) else "all"
            tag["approx_time"] = time_data.get(tag["alias"].lower(), "N/A")

        self.setWindowTitle("michael fedro's backup & restore tool")
        self.game_times_cache = {}
        self.tag_buttons = {}
        self.image_cache = {}
        self.started_image_queries = set()
        self.tabs_config = load_tabs_config()
        self.active_workers = []
        self.init_ui()

        QThreadPool.globalInstance().setMaxThreadCount(10)
        QTimer.singleShot(10, self.start_game_time_queries)
        self.add_active_user()

        self.banned_timer = QTimer()
        self.banned_timer.timeout.connect(self.check_banned)
        self.banned_timer.start(3000)
        self.run_processes = []
        self.setAttribute(Qt.WA_DeleteOnClose, True)

    def perform_docker_login(self):
        docker_login_cmd = f"docker login -u michadockermisha -p {self.login_password}"
        login_cmd = f'wsl --distribution ubuntu --user root -- bash -lic "{docker_login_cmd}"'
        subprocess.call(login_cmd, shell=True)
        return None

    def add_active_user(self):
        users = load_active_users()
        users[self.username] = {"login_time": time.time()}
        save_active_users(users)

    def remove_active_user(self):
        users = load_active_users()
        if self.username in users:
            del users[self.username]
            save_active_users(users)

    def check_banned(self):
        banned = load_banned_users()
        if self.username in banned:
            QMessageBox.warning(self, "Kicked", "You have been kicked from the app by the admin.")
            self.close()

    def closeEvent(self, event):
        dkill()
        self.remove_active_user()
        event.accept()
        sys.exit(0)

    def require_admin(self):
        if not self.is_admin:
            QMessageBox.warning(self, "Insufficient Privileges", "This operation requires admin privileges.")
            return False
        return True

    def add_worker(self, worker):
        self.active_workers.append(worker)
        worker.signals.finished.connect(lambda _: self.active_workers.remove(worker))

    def fetch_tags(self):
        url = "https://hub.docker.com/v2/repositories/michadockermisha/backup/tags?page_size=100"
        tag_list = []
        import requests
        while url:
            try:
                response = requests.get(url)
                data = response.json()
                for item in data.get("results", []):
                    tag_list.append({
                        "name": item["name"],
                        "full_size": item.get("full_size", 0),
                        "last_updated": item.get("last_updated", "")
                    })
                url = data.get("next")
            except Exception as e:
                print("Error fetching tags:", e)
                break
        tag_list.sort(key=lambda x: x["name"].lower())
        return tag_list

    def format_size(self, size):
        for unit in ["B", "KB", "MB", "GB", "TB"]:
            if size < 1024:
                return f"{size:.1f}{unit}"
            size /= 1024
        return f"{size:.1f}PB"

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(12, 12, 12, 12)

        # Top bar section
        top_bar = QHBoxLayout()
        browse_btn = QPushButton("Browse Path")
        browse_btn.setStyleSheet("""
            QPushButton {
                background: #2980B9;
                color: white;
                padding: 8px 12px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #3498DB;
            }
        """)
        browse_btn.clicked.connect(self.select_destination_path)
        top_bar.addWidget(browse_btn)
        top_bar.addStretch()
        disconnect_btn = QPushButton("Disconnect")
        disconnect_btn.setStyleSheet("""
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
        disconnect_btn.clicked.connect(self.disconnect)
        top_bar.addWidget(disconnect_btn)

        if self.is_admin:
            kick_btn = QPushButton("Kick User")
            kick_btn.setStyleSheet("""
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
            kick_btn.clicked.connect(self.kick_user)
            top_bar.addWidget(kick_btn)

            dashboard_btn = QPushButton("User Dashboard")
            dashboard_btn.setStyleSheet("""
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
            dashboard_btn.clicked.connect(self.open_user_dashboard)
            top_bar.addWidget(dashboard_btn)

            myliners_btn = QPushButton("myLiners")
            myliners_btn.setStyleSheet("""
                QPushButton {
                    background: #9B59B6;
                    color: white;
                    padding: 8px 12px;
                    border-radius: 6px;
                }
                QPushButton:hover {
                    background: #AF7AC5;
                }
            """)
            myliners_btn.clicked.connect(self.open_myliners)
            top_bar.addWidget(myliners_btn)

            clear_terminal_btn = QPushButton("Clear Terminal")
            clear_terminal_btn.setStyleSheet("""
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
            clear_terminal_btn.clicked.connect(self.clear_terminal)
            top_bar.addWidget(clear_terminal_btn)
        else:
            clear_terminal_btn = QPushButton("Clear Terminal")
            clear_terminal_btn.setStyleSheet("""
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
            clear_terminal_btn.clicked.connect(self.clear_terminal)
            top_bar.addWidget(clear_terminal_btn)

        exit_button = QPushButton("Exit")
        exit_button.setStyleSheet("""
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
        exit_button.clicked.connect(lambda: sys.exit(0))
        top_bar.addWidget(exit_button)

        main_layout.addLayout(top_bar)

        # Title
        title = QLabel("michael fedro's backup & restore tool")
        title.setStyleSheet("font-size: 28px; font-weight: bold; color: #F1C40F;")
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)

        # Tab management buttons
        tab_mgmt_layout = QHBoxLayout()
        add_tab_btn = QPushButton("Add Tab")
        add_tab_btn.setStyleSheet("""
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
        add_tab_btn.clicked.connect(lambda: self.require_admin() and self.add_tab())
        tab_mgmt_layout.addWidget(add_tab_btn)

        rename_tab_btn = QPushButton("Rename Tab")
        rename_tab_btn.setStyleSheet("""
            QPushButton {
                background: #8E44AD;
                color: white;
                padding: 8px 12px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background: #9B59B6;
            }
        """)
        rename_tab_btn.clicked.connect(lambda: self.require_admin() and self.rename_tab())
        tab_mgmt_layout.addWidget(rename_tab_btn)

        delete_tab_btn = QPushButton("Delete Tab")
        delete_tab_btn.setStyleSheet("""
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
        delete_tab_btn.clicked.connect(lambda: self.require_admin() and self.delete_tab())
        tab_mgmt_layout.addWidget(delete_tab_btn)

        main_layout.addLayout(tab_mgmt_layout)

        # Tab navigation widget
        self.tab_nav = TabNavigationWidget(self.tabs_config, parent=self)
        main_layout.addWidget(self.tab_nav)

        # Control bar
        control_layout = QHBoxLayout()
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search tags...")
        self.search_box.setStyleSheet("padding: 8px; border: 2px solid #1ABC9C; border-radius: 6px;")
        self.search_box.textChanged.connect(self.filter_buttons)
        control_layout.addWidget(self.search_box)

        sort_button = QPushButton("Sort")
        sort_button.setStyleSheet("""
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
        from PyQt5.QtWidgets import QMenu
        sort_menu = QMenu(self)
        sort_menu.addAction("Heaviest to Lightest", lambda: self.sort_tags(descending=True))
        sort_menu.addAction("Lightest to Lightest", lambda: self.sort_tags(descending=False))
        sort_menu.addAction("Sort by HowLong: Longest to Shortest", lambda: self.sort_tags_by_time(descending=True))
        sort_menu.addAction("Sort by HowLong: Shortest to Longest", lambda: self.sort_tags_by_time(descending=False))
        sort_menu.addAction("Sort by Date: Newest to Oldest", lambda: self.sort_tags_by_date(descending=True))
        sort_menu.addAction("Sort by Date: Oldest to Newest", lambda: self.sort_tags_by_date(descending=False))
        sort_button.setMenu(sort_menu)
        control_layout.addWidget(sort_button)

        run_selected = QPushButton("Run Selected")
        run_selected.setStyleSheet("""
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
        run_selected.clicked.connect(self.run_selected_commands)
        control_layout.addWidget(run_selected)

        delete_tag_button = QPushButton("Delete Docker Tag")
        delete_tag_button.setStyleSheet("""
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
        delete_tag_button.clicked.connect(lambda: self.require_admin() and self.open_delete_dialog())
        control_layout.addWidget(delete_tag_button)

        move_tags_button = QPushButton("Move Tags")
        move_tags_button.setStyleSheet("""
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
        move_tags_button.clicked.connect(lambda: self.require_admin() and self.open_bulk_move_dialog())
        control_layout.addWidget(move_tags_button)

        bulk_paste_button = QPushButton("Bulk Paste Move")
        bulk_paste_button.setStyleSheet("""
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
        bulk_paste_button.clicked.connect(lambda: self.require_admin() and self.open_bulk_paste_move_dialog())
        control_layout.addWidget(bulk_paste_button)

        save_txt_button = QPushButton("Save as .txt")
        save_txt_button.setStyleSheet("""
            QPushButton {
                background: #8E44AD;
                color: white;
                padding: 8px 12px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background: #9B59B6;
            }
        """)
        save_txt_button.clicked.connect(self.handle_save_txt)
        control_layout.addWidget(save_txt_button)

        main_layout.addLayout(control_layout)

        # Create tag pages (one for each tab)
        self.stacked = QStackedWidget()
        self.tab_pages = {}
        for tab in self.tabs_config:
            container = TagContainerWidget(tab["id"], parent=self)
            self.tab_pages[tab["id"]] = container
            from PyQt5.QtWidgets import QScrollArea
            scroll = QScrollArea()
            scroll.setWidgetResizable(True)
            scroll.setWidget(container)
            self.stacked.addWidget(scroll)
        main_layout.addWidget(self.stacked)

        self.create_tag_buttons()
        self.setLayout(main_layout)

    def open_myliners(self):
        dialog = MyLinersDialog(self)
        dialog.exec_()

    def disconnect(self):
        clear_session()
        QMessageBox.information(self, "Disconnected", "You have been disconnected.")
        self.close()

    def kick_user(self):
        username, ok = QInputDialog.getText(self, "Kick User", "Enter username to ban:")
        if ok and username:
            username = username.strip().lower()
            if username not in banned_users:
                banned_users.append(username)
                from persistence import save_banned_users
                save_banned_users(banned_users)
                QMessageBox.information(self, "User Kicked", f"User '{username}' has been banned.")
            else:
                QMessageBox.information(self, "Already Banned", f"User '{username}' is already banned.")

    def open_user_dashboard(self):
        if not self.require_admin():
            return
        dashboard = UserDashboardDialog(parent=self)
        dashboard.exec_()

    def set_current_tab(self, tab_id):
        for i, tab in enumerate(self.tabs_config):
            if tab["id"] == tab_id:
                self.stacked.setCurrentIndex(i)
                break

    def add_tab(self):
        new_name, ok = QInputDialog.getText(self, "Add Tab", "Enter new tab name:")
        if not (ok and new_name):
            return
        new_id = new_name.lower().replace(" ", "_")
        if any(tab["id"] == new_id for tab in self.tabs_config):
            QMessageBox.warning(self, "Error", "A tab with that identifier already exists.")
            return
        self.tabs_config.append({"id": new_id, "name": new_name})
        from persistence import save_tabs_config
        save_tabs_config(self.tabs_config)
        container = TagContainerWidget(new_id, parent=self)
        self.tab_pages[new_id] = container
        from PyQt5.QtWidgets import QScrollArea
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(container)
        self.stacked.addWidget(scroll)
        self.tab_nav.update_tabs(self.tabs_config)
        self.create_tag_buttons()

    def rename_tab(self):
        current_index = self.stacked.currentIndex()
        current_tab = self.tabs_config[current_index]
        new_name, ok = QInputDialog.getText(self, "Rename Tab", "Enter new tab name:", QLineEdit.Normal, current_tab["name"])
        if not (ok and new_name):
            return
        self.tabs_config[current_index]["name"] = new_name
        from persistence import save_tabs_config
        save_tabs_config(self.tabs_config)
        self.tab_nav.update_tabs(self.tabs_config)
        self.create_tag_buttons()

    def delete_tab(self):
        current_index = self.stacked.currentIndex()
        current_tab = self.tabs_config[current_index]
        if current_tab["id"] == "all":
            QMessageBox.warning(self, "Error", "You cannot delete the 'All' tab.")
            return
        reply = QMessageBox.question(self, "Delete Tab", f"Delete tab '{current_tab['name']}'?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply != QMessageBox.Yes:
            return
        del self.tabs_config[current_index]
        from persistence import save_tabs_config
        save_tabs_config(self.tabs_config)
        self.tab_nav.update_tabs(self.tabs_config)
        widget_to_remove = self.stacked.widget(current_index)
        self.stacked.removeWidget(widget_to_remove)
        widget_to_remove.deleteLater()
        self.create_tag_buttons()

    def handle_save_txt(self):
        current_index = self.stacked.currentIndex()
        current_tab = self.tabs_config[current_index]
        if current_tab["id"] == "mybackup" and not self.is_admin:
            QMessageBox.warning(self, "Access Denied", "Only admin can download tags from the mybackup tab.")
            return
        self.save_as_txt()

    def open_bulk_move_dialog(self):
        from dialogs import BulkMoveDialog
        dialog = BulkMoveDialog(self.all_tags, self.tabs_config, parent=self)
        if dialog.exec_():
            for tag in self.all_tags:
                persistent = persistent_settings.get(tag["docker_name"], {})
                persistent["category"] = tag["category"]
                persistent_settings[tag["docker_name"]] = persistent
            save_settings(persistent_settings)
            self.create_tag_buttons()

    def open_bulk_paste_move_dialog(self):
        from dialogs import BulkPasteMoveDialog
        dialog = BulkPasteMoveDialog(self.all_tags, self.tabs_config, parent=self)
        if dialog.exec_():
            for tag in self.all_tags:
                persistent = persistent_settings.get(tag["docker_name"], {})
                persistent["category"] = tag["category"]
                persistent_settings[tag["docker_name"]] = persistent
            save_settings(persistent_settings)
            self.create_tag_buttons()

    def save_as_txt(self):
        downloads = os.path.join(os.path.expanduser("~"), "Downloads")
        if not os.path.exists(downloads):
            downloads = os.path.expanduser("~")
        filepath = os.path.join(downloads, "tags.txt")
        output = []
        for tab in self.tabs_config:
            output.append(f"Tab: {tab['name']}")
            for tag in self.all_tags:
                if tag.get("category", "all") == tab["id"]:
                    output.append(tag["alias"])
            output.append("")
        try:
            with open(filepath, "w") as f:
                f.write("\n".join(output))
            QMessageBox.information(self, "Save as .txt", f"Tags saved to {filepath}")
        except Exception as e:
            QMessageBox.warning(self, "Save as .txt", f"Error saving tags: {e}")

    def create_tag_buttons(self):
        for container in self.tab_pages.values():
            for i in reversed(range(container.layout.count())):
                widget = container.layout.itemAt(i).widget()
                if widget:
                    widget.setParent(None)
        self.buttons = []
        self.tag_buttons = {}
        positions = {}
        for tab in self.tabs_config:
            positions[tab["id"]] = [0, 0]
        self.started_image_queries = set()
        for tag in self.all_tags:
            current_tab_name = "All"
            for tab in self.tabs_config:
                if tab["id"] == tag.get("category", "all"):
                    current_tab_name = tab["name"]
                    break
            time_line = f"Approx Time: {tag['approx_time']}"
            text_lines = [
                tag["alias"],
                f"({self.format_size(tag['full_size'])})",
                time_line,
                f"Tab: {current_tab_name}"
            ]
            display_text = "\n".join(text_lines)
            for target_cat in ["all", tag.get("category", "all")]:
                if target_cat in self.tab_pages:
                    button = GameButton(display_text)
                    button.tag_info = tag
                    from workers import ImageWorker
                    worker = ImageWorker(tag["alias"])
                    worker.signals.finished.connect(partial(self.handle_image_update, tag["alias"], button))
                    QThreadPool.globalInstance().start(worker)
                    self.tag_buttons.setdefault(tag["docker_name"], []).append(button)
                    self.buttons.append(button)
                    container = self.tab_pages[target_cat]
                    row, col = positions.get(target_cat, [0, 0])
                    container.layout.addWidget(button, row, col)
                    col += 1
                    if col >= 4:
                        col = 0
                        row += 1
                    positions[target_cat] = [row, col]

    def start_game_time_queries(self):
        for tag in self.all_tags:
            alias = tag["alias"]
            from workers import Worker
            if alias not in self.game_times_cache:
                worker = Worker(fetch_game_time, alias)
                worker.signals.finished.connect(partial(self.handle_game_time_update, alias))
                self.add_worker(worker)
                QThreadPool.globalInstance().start(worker)

    def handle_game_time_update(self, alias, time_info):
        self.game_times_cache[alias] = time_info
        for docker_name, buttons in self.tag_buttons.items():
            for button in buttons:
                if button.tag_info["alias"] == alias:
                    lines = button.text().splitlines()
                    if len(lines) >= 3:
                        lines[2] = f"Approx Time: {time_info}" if time_info != "N/A" else "Approx Time: N/A"
                    else:
                        lines.append(f"Approx Time: {time_info}" if time_info != "N/A" else "Approx Time: N/A")
                    button.setText("\n".join(lines))

    def handle_image_update(self, alias, button, result):
        image = result[1] if isinstance(result, tuple) else result
        if not image.isNull():
            scaled_image = image.scaled(button.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
            pixmap = QPixmap.fromImage(scaled_image)
            self.image_cache[alias] = pixmap
            b64 = pixmap_to_base64(pixmap)
            base_style = button.styleSheet()
            bg_style = f"background-image: url(data:image/png;base64,{b64}); background-position: center; background-repeat: no-repeat;"
            button.setStyleSheet(base_style + bg_style)
        else:
            button.setStyleSheet(button.styleSheet() + "background-image: none;")

    def sort_tags(self, descending=True):
        self.all_tags.sort(key=lambda x: x["full_size"], reverse=descending)
        self.create_tag_buttons()

    def sort_tags_by_time(self, descending=True):
        def parse_time(time_str):
            try:
                if "-" in time_str or "–" in time_str:
                    parts = time_str.replace("~", "").replace("hrs", "").strip()
                    parts = parts.replace("–", "-").split("-")
                    return float(parts[1].strip())
                else:
                    return float(time_str.replace("~", "").replace("hrs", "").strip())
            except:
                return 0.0
        self.all_tags.sort(key=lambda x: parse_time(time_data.get(x["alias"].lower(), "0")), reverse=descending)
        self.create_tag_buttons()

    def sort_tags_by_date(self, descending=True):
        self.all_tags.sort(key=lambda x: parse_date(x.get("last_updated", "")), reverse=descending)
        self.create_tag_buttons()

    def filter_buttons(self, text):
        for button in self.buttons:
            if text.lower() in button.tag_info["alias"].lower():
                button.setVisible(True)
            else:
                button.setVisible(False)

    def select_destination_path(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.DirectoryOnly)
        dialog.setOption(QFileDialog.ShowDirsOnly, True)
        if dialog.exec_():
            selected_dir = dialog.selectedFiles()[0]
            wsl_path = selected_dir.replace('\\', '/').replace('C:', '/mnt/c')
            return wsl_path
        return None

    def run_selected_commands(self):
        if not check_docker_engine():
            QMessageBox.warning(self, "Docker Engine Not Running",
                                "Docker Engine is not running in WSL. Please start Docker in your Ubuntu WSL distribution and try again.")
            return
        selected_buttons = [btn for btn in self.buttons if btn.isChecked()]
        if not selected_buttons:
            QMessageBox.information(self, "No Selection", "Please select at least one tag to run.")
            return
        destination_path = self.select_destination_path()
        if not destination_path:
            return
        reply = QMessageBox.question(self, "Confirm Path",
                                   f"Selected destination path:\n{destination_path}\n\nProceed with the operation?",
                                   QMessageBox.Yes | QMessageBox.No)
        if reply != QMessageBox.Yes:
            return
        pool = QThreadPool.globalInstance()
        for btn in selected_buttons:
            tag = btn.tag_info["docker_name"]
            pull_worker = DockerPullWorker(tag)
            pool.start(pull_worker)
        for btn in selected_buttons:
            tag = btn.tag_info["docker_name"]
            docker_cmd = (
                f"docker run -d --pull=always --rm --cpus=4 --memory=8g --memory-swap=12g "
                f"-v '{destination_path}':/games -e DISPLAY=\\$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix "
                f"--name '{tag}' michadockermisha/backup:'{tag}' "
                f"sh -c 'apk add rsync pigz && mkdir -p /games/{tag} && "
                f"rsync -aP --compress-level=1 --compress --numeric-ids --inplace --delete-during --info=progress2 /home/ /games/{tag}'"
            )
            run_cmd = f'wsl --distribution ubuntu --user root -- bash -lic "{docker_cmd}"'
            try:
                subprocess.Popen(run_cmd, shell=True)
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Error starting command for {tag}: {e}")
            btn.setChecked(False)
        QMessageBox.information(self, "Run Initiated", 
                              f"All selected commands have been initiated.\nFiles will be copied to: {destination_path}")

    def open_delete_dialog(self):
        if not self.require_admin():
            return
        dialog = DeleteTagDialog(self.all_tags, parent=self)
        dialog.exec_()

    def update_tag_category(self, docker_name, new_category):
        for tag in self.all_tags:
            if tag["docker_name"] == docker_name:
                tag["category"] = new_category
                temp = persistent_settings.get(docker_name, {})
                temp["category"] = new_category
                persistent_settings[docker_name] = temp
                save_settings(persistent_settings)
        self.create_tag_buttons()

    def handle_tag_move(self, docker_name, new_category):
        self.update_tag_category(docker_name, new_category)

    def handle_tag_rename(self, docker_name, new_alias):
        for tag in self.all_tags:
            if tag["docker_name"] == docker_name:
                tag["alias"] = new_alias
                temp = persistent_settings.get(docker_name, {})
                temp["alias"] = new_alias
                persistent_settings[docker_name] = temp
        self.create_tag_buttons()

    def refresh_tags(self):
        self.all_tags = self.fetch_tags()
        for tag in self.all_tags:
            tag["docker_name"] = tag["name"]
            stored_alias = persistent_settings.get(tag["docker_name"], {}).get("alias", tag["name"])
            stored_cat = persistent_settings.get(tag["docker_name"], {}).get("category", "all")
            tag["alias"] = stored_alias
            tag["category"] = stored_cat if any(tab["id"] == stored_cat for tab in self.tabs_config) else "all"
        self.create_tag_buttons()

    def get_docker_token(self):
        if not self.is_admin:
            QMessageBox.warning(self, "Insufficient Privileges", "Admin privileges are required for this operation.")
            return None
        if self.docker_token is not None:
            return self.docker_token
        login_url = "https://hub.docker.com/v2/users/login/"
        login_data = {"username": "michadockermisha", "password": self.login_password}
        import requests
        login_response = requests.post(login_url, json=login_data)
        if login_response.status_code == 200 and login_response.json().get("token"):
            self.docker_token = login_response.json().get("token")
            return self.docker_token
        else:
            QMessageBox.warning(self, "Authentication Failed", "Incorrect Docker Hub password.")
            return None

    def clear_terminal(self):
        cmd = 'powershell -NoProfile -Command "Clear-Host; [System.Console]::Clear(); cls"'
        try:
            subprocess.Popen(cmd, shell=True)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error clearing terminal: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    font = QFont("Segoe UI", 12)
    app.setFont(font)
    docker_app = DockerApp("dummy_password", True, "michadockermisha")
    docker_app.show()
    sys.exit(app.exec_())

