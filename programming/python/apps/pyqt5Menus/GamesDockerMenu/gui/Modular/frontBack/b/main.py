import sys
import time
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QDialog,
    QLineEdit, QPushButton, QMessageBox, QInputDialog
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QTimer, QThreadPool
from backend import (
    start_docker_engine, dkill, fetch_tags, load_settings, save_settings,
    load_time_data, perform_docker_login, get_docker_token,
    load_active_users, save_active_users, load_banned_users, save_banned_users, clear_session,
    parse_date, load_tabs_config, load_session, save_session
)
from docker_commands import DockerCommands
from background_images import BackgroundImages
from tabs import Tabs
from tags import Tags
from buttons import Buttons, MyLinersDialog, UserDashboardDialog, GameButton

class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setFixedSize(300, 150)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.username_input.setStyleSheet("padding: 6px; border-radius: 4px;")
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet("padding: 6px; border-radius: 4px;")
        layout.addWidget(self.password_input)

        login_btn = QPushButton("Login")
        login_btn.setStyleSheet("""
            QPushButton {
                background: #27AE60;
                color: white;
                padding: 8px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background: #2ECC71;
            }
        """)
        login_btn.clicked.connect(self.accept)
        layout.addWidget(login_btn)
        self.setLayout(layout)

class DockerApp(QWidget):
    def __init__(self, login_password, is_admin, username):
        super().__init__()
        self.login_password = login_password
        self.is_admin = is_admin
        self.username = username
        start_docker_engine()
        self.docker_token = perform_docker_login(login_password) if is_admin else None
        self.all_tags = fetch_tags()
        self.persistent_settings = load_settings()
        self.time_data = load_time_data("time.txt")
        for tag in self.all_tags:
            tag["docker_name"] = tag["name"]
            tag["alias"] = self.persistent_settings.get(tag["docker_name"], {}).get("alias", tag["docker_name"])
            stored_cat = self.persistent_settings.get(tag["docker_name"], {}).get("category", "all")
            tag["category"] = stored_cat if any(tab["id"] == stored_cat for tab in load_tabs_config()) else "all"
            tag["approx_time"] = self.time_data.get(tag["alias"].lower(), "N/A")
        self.setWindowTitle("michael fedro's backup & restore tool")
        self.game_times_cache = {}
        self.tag_buttons = {}
        self.active_workers = []
        self.buttons = []
        self.docker_commands = DockerCommands(self)
        self.background_images = BackgroundImages(self)
        self.tabs = Tabs(self)
        self.tags = Tags(self)
        self.button_manager = Buttons(self)
        self.init_ui()
        QThreadPool.globalInstance().setMaxThreadCount(10)
        self.add_active_user()
        self.banned_timer = QTimer()
        self.banned_timer.timeout.connect(self.check_banned)
        self.banned_timer.start(3000)
        self.setAttribute(Qt.WA_DeleteOnClose, True)

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.addLayout(self.button_manager.create_top_bar_buttons())
        title = QLabel("michael fedro's backup & restore tool")
        title.setStyleSheet("font-size: 28px; font-weight: bold; color: #F1C40F;")
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)
        tab_mgmt_layout = QHBoxLayout()
        for btn in self.tabs.create_tab_management_buttons():
            tab_mgmt_layout.addWidget(btn)
        main_layout.addLayout(tab_mgmt_layout)
        main_layout.addWidget(self.tabs.create_tab_navigation())
        control_layout = QHBoxLayout()
        control_layout.addWidget(self.tags.create_search_box())
        control_layout.addWidget(self.button_manager.create_sort_button())
        control_layout.addWidget(self.docker_commands.create_run_button())
        for btn in self.tags.create_tag_management_buttons():
            control_layout.addWidget(btn)
        main_layout.addLayout(control_layout)
        main_layout.addWidget(self.tabs.create_tab_pages())
        self.setLayout(main_layout)
        self.create_tag_buttons()
        QTimer.singleShot(10, self.start_game_time_queries)

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
        for worker in self.active_workers[:]:
            worker.is_running = False
            try:
                worker.signals.finished.disconnect()
            except TypeError:
                pass
        self.active_workers.clear()
        QThreadPool.globalInstance().waitForDone()
        event.accept()

    def require_admin(self):
        if not self.is_admin:
            QMessageBox.warning(self, "Insufficient Privileges", "This operation requires admin privileges.")
            return False
        return True

    def add_worker(self, worker):
        self.active_workers.append(worker)
        worker.signals.finished.connect(lambda result: self.on_worker_finished(worker, result))

    def on_worker_finished(self, worker, result):
        if worker in self.active_workers:
            worker.is_running = False
            try:
                worker.signals.finished.disconnect()
            except TypeError:
                pass
            self.active_workers.remove(worker)

    def format_size(self, size):
        for unit in ["B", "KB", "MB", "GB", "TB"]:
            if size < 1024:
                return f"{size:.1f}{unit}"
            size /= 1024
        return f"{size:.1f}PB"

    def create_tag_buttons(self):
        for worker in self.active_workers[:]:
            worker.is_running = False
            try:
                worker.signals.finished.disconnect()
            except TypeError:
                pass
        self.active_workers.clear()

        for container in self.tabs.tab_pages.values():
            for i in reversed(range(container.layout.count())):
                widget = container.layout.itemAt(i).widget()
                if widget:
                    widget.setParent(None)
                    widget.deleteLater()

        self.buttons = []
        self.tag_buttons = {}
        positions = {tab["id"]: [0, 0] for tab in self.tabs.tabs_config}

        for tag in self.all_tags:
            current_tab_name = "All"
            for tab in self.tabs.tabs_config:
                if tag.get("category", "all") == tab["id"]:
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
                if target_cat in self.tabs.tab_pages:
                    button = GameButton(display_text)
                    button.tag_info = tag
                    self.tag_buttons.setdefault(tag["docker_name"], []).append(button)
                    self.buttons.append(button)
                    container = self.tabs.tab_pages[target_cat]
                    row, col = positions.get(target_cat, [0, 0])
                    container.layout.addWidget(button, row, col)
                    col += 1
                    if col >= 4:
                        col = 0
                        row += 1
                    positions[target_cat] = [row, col]
                    self.background_images.start_image_worker(tag["alias"], button)

    def start_game_time_queries(self):
        from backend import fetch_game_time
        from PyQt5.QtCore import QRunnable, pyqtSignal, QObject

        class WorkerSignals(QObject):
            finished = pyqtSignal(object)

        class Worker(QRunnable):
            def __init__(self, fn, *args, **kwargs):
                super().__init__()
                self.fn = fn
                self.args = args
                self.kwargs = kwargs
                self.signals = WorkerSignals()
                self.is_running = True

            def run(self):
                try:
                    if self.is_running:
                        result = self.fn(*self.args, **self.kwargs)
                        self.signals.finished.emit(result)
                except Exception as e:
                    print(f"Worker error: {e}")
                finally:
                    self.is_running = False

        for tag in self.all_tags:
            alias = tag["alias"]
            if alias not in self.game_times_cache:
                worker = Worker(fetch_game_time, alias)
                worker.signals.finished.connect(lambda result, a=alias: self.handle_game_time_update(a, result))
                self.add_worker(worker)
                QThreadPool.globalInstance().start(worker)

    def handle_game_time_update(self, alias, time_info):
        if isinstance(time_info, tuple):
            time_info = time_info[1] if len(time_info) > 1 else "N/A"
        self.game_times_cache[alias] = time_info
        for docker_name, buttons in self.tag_buttons.items():
            for button in buttons:
                if button.tag_info["alias"] == alias and button.parent():
                    lines = button.text().splitlines()
                    if len(lines) >= 3:
                        lines[2] = f"Approx Time: {time_info}"
                    else:
                        lines.append(f"Approx Time: {time_info}")
                    button.setText("\n".join(lines))

    def sort_tags(self, descending=True):
        self.all_tags.sort(key=lambda x: x["full_size"], reverse=descending)
        self.create_tag_buttons()

    def sort_tags_by_time(self, descending=True):
        def parse_time(time_str):
            try:
                time_str = time_str.lower().replace("approx time: ", "").replace("hours", "").strip()
                if "-" in time_str or "–" in time_str:
                    time_str = time_str.replace("–", "-").split("-")[1].strip()
                return float(time_str)
            except:
                return 0.0
        self.all_tags.sort(key=lambda x: parse_time(x.get("approx_time", "0")), reverse=descending)
        self.create_tag_buttons()

    def sort_tags_by_date(self, descending=True):
        self.all_tags.sort(key=lambda x: parse_date(x.get("last_updated", "")), reverse=descending)
        self.create_tag_buttons()

    def filter_buttons(self, text):
        for button in self.buttons:
            if button.parent():
                button.setVisible(text.lower() in button.tag_info["alias"].lower())

    def handle_save_txt(self):
        current_index = self.tabs.stacked.currentIndex()
        current_tab = self.tabs.tabs_config[current_index]
        if current_tab["id"] == "mybackup" and not self.is_admin:
            QMessageBox.warning(self, "Access Denied", "Only admin can download tags from the mybackup tab.")
            return
        self.save_as_txt()

    def save_as_txt(self):
        import os
        downloads = os.path.join(os.path.expanduser("~"), "Downloads")
        if not os.path.exists(downloads):
            downloads = os.path.expanduser("~")
        filepath = os.path.join(downloads, "tags.txt")
        output = []
        for tab in self.tabs.tabs_config:
            output.append(f"Tab: {tab['name']}")
            for tag in self.all_tags:
                if tag.get("category", "all") == tab["id"]:
                    output.append(tag["alias"])
            output.append("")
        try:
            with open(filepath, "w", encoding='utf-8') as f:
                f.write("\n".join(output))
            QMessageBox.information(self, "Save as .txt", f"Tags saved to {filepath}")
        except Exception as e:
            QMessageBox.warning(self, "Save as .txt", f"Error saving tags: {e}")

    def open_myliners(self):
        dialog = MyLinersDialog(self)
        dialog.exec_()

    def disconnect(self):
        clear_session()
        QMessageBox.information(self, "Disconnected", "You have been logged out.")
        self.close()

    def kick_user(self):
        username, ok = QInputDialog.getText(self, "Kick User", "Enter username to ban:")
        if ok and username:
            username = username.strip().lower()
            banned = load_banned_users()
            if username not in banned:
                banned.append(username)
                save_banned_users(banned)
                QMessageBox.information(self, "User Kicked", f"User '{username}' has been banned.")
            else:
                QMessageBox.information(self, "Already Banned", f"User '{username}' is already banned.")

    def open_user_dashboard(self):
        if not self.require_admin():
            return
        dashboard = UserDashboardDialog(parent=self)
        dashboard.exec_()

    def update_tag_category(self, docker_name, new_category):
        for tag in self.all_tags:
            if tag["docker_name"] == docker_name:
                tag["category"] = new_category
                persistent = self.persistent_settings.get(docker_name, {})
                persistent["category"] = new_category
                self.persistent_settings[docker_name] = persistent
                save_settings(self.persistent_settings)
        self.create_tag_buttons()

    def handle_tag_move(self, docker_name, new_category):
        self.update_tag_category(docker_name, new_category)

    def handle_tag_rename(self, docker_name, new_alias):
        for tag in self.all_tags:
            if tag["docker_name"] == docker_name:
                tag["alias"] = new_alias
                persistent = self.persistent_settings.get(docker_name, {})
                persistent["alias"] = new_alias
                self.persistent_settings[docker_name] = persistent
        save_settings(self.persistent_settings)
        self.create_tag_buttons()

    def update_tag_categories(self):
        save_settings(self.persistent_settings)
        self.create_tag_buttons()

    def refresh_tags(self):
        self.all_tags = fetch_tags()
        for tag in self.all_tags:
            tag["docker_name"] = tag["name"]
            stored_alias = self.persistent_settings.get(tag["docker_name"], {}).get("alias", tag["name"])
            stored_cat = self.persistent_settings.get(tag["docker_name"], {}).get("category", "all")
            tag["alias"] = stored_alias
            tag["category"] = stored_cat if any(tab["id"] == stored_cat for tab in self.tabs.tabs_config) else "all"
            tag["approx_time"] = self.time_data.get(tag["alias"].lower(), "N/A")
        self.create_tag_buttons()

    def get_docker_token(self):
        if not self.is_admin:
            QMessageBox.warning(self, "Insufficient Privileges", "Admin privileges are required for this operation.")
            return None
        if self.docker_token is True:
            token = get_docker_token(self.login_password)
            if token:
                return token
            else:
                QMessageBox.warning(self, "Authentication Failed", "Incorrect Docker Hub password.")
                return None
        return None

    def clear_terminal(self):
        from backend import clear_terminal
        clear_terminal()

    def logout(self):
        clear_session()
        self.disconnect()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    background_images = BackgroundImages(None)
    background_images.apply_background(app)
    
    # Check for existing session
    session = load_session()
    if session and session.get('username') and session.get('password'):
        username = session['username']
        password = session['password']
        
        # Verify if user is banned
        banned_users = load_banned_users()
        if username in banned_users:
            QMessageBox.warning(None, "Access Denied", "You are banned from using this app.")
            sys.exit(1)
            
        # Verify Docker Hub credentials for admin
        is_admin = username == "misha" and perform_docker_login(password)
        window = DockerApp(password, is_admin, username)
        window.showMaximized()
        sys.exit(app.exec_())
    
    # No session found, show login dialog
    login_dialog = LoginDialog()
    if login_dialog.exec_():
        username = login_dialog.username_input.text().strip().lower()
        password = login_dialog.password_input.text()
        
        if not username:
            QMessageBox.warning(None, "Login Failed", "Username cannot be empty.")
            sys.exit(1)
            
        banned_users = load_banned_users()
        if username in banned_users:
            QMessageBox.warning(None, "Access Denied", "You are banned from using this app.")
            sys.exit(1)
            
        # For admin user, verify Docker Hub credentials
        is_admin = False
        if username == "misha":
            is_admin = perform_docker_login(password)
            if not is_admin:
                QMessageBox.warning(None, "Login Failed", "Invalid Docker Hub credentials.")
                sys.exit(1)
        
        # Save session for next time
        save_session({
            'username': username,
            'password': password
        })
        
        window = DockerApp(password, is_admin, username)
        window.showMaximized()
        sys.exit(app.exec_())
