from PyQt5.QtWidgets import QPushButton, QHBoxLayout, QVBoxLayout, QMenu, QInputDialog, QMessageBox, QDialog, QListWidget, QListWidgetItem
from PyQt5.QtGui import QDrag
from PyQt5.QtCore import Qt, QMimeData
from functools import partial
from backend import update_docker_tag_name, load_custom_buttons, save_custom_buttons
import subprocess

class GameButton(QPushButton):
    dragThreshold = 10

    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setCheckable(True)
        self.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                             stop:0 #2C3E50, stop:1 #34495E);
                color: gold;
                font-size: 24px;
                padding: 20px;
                border: 2px solid #1ABC9C;
                border-radius: 10px;
                min-height: 200px;
                min-width: 200px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                             stop:0 #1ABC9C, stop:1 #16A085);
                border: 2px solid #F39C12;
            }
            QPushButton:pressed {
                background: #2980B9;
            }
        """)
        self._drag_start_pos = None
        self.tag_info = None

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_start_pos = event.pos()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton and self._drag_start_pos:
            if (event.pos() - self._drag_start_pos).manhattanLength() >= self.dragThreshold:
                mimeData = QMimeData()
                mimeData.setText(self.tag_info["docker_name"])
                drag = QDrag(self)
                drag.setMimeData(mimeData)
                drag.exec_(Qt.MoveAction)
                return
        super().mouseMoveEvent(event)

    def contextMenuEvent(self, event):
        menu = QMenu(self)
        change_action = menu.addAction("Change Tag Name")
        move_to_action = menu.addAction("Move To")
        action = menu.exec_(event.globalPos())
        main_window = self.parent()
        while main_window and not hasattr(main_window, "handle_tag_move"):
            main_window = main_window.parent()
        if not main_window:
            return
        token = main_window.get_docker_token() if main_window else None
        if not token:
            return
        if action == change_action:
            new_alias, ok = QInputDialog.getText(self, "Change Tag Name",
                                                 "Enter new tag name:", text=self.tag_info["alias"])
            if ok and new_alias:
                old_alias = self.tag_info["alias"]
                if update_docker_tag_name(old_alias, new_alias):
                    self.tag_info["alias"] = new_alias
                    persistent = main_window.persistent_settings.get(self.tag_info["docker_name"], {})
                    persistent["alias"] = new_alias
                    main_window.persistent_settings[self.tag_info["docker_name"]] = persistent
                    from backend import save_settings
                    save_settings(main_window.persistent_settings)
                    lines = self.text().splitlines()
                    lines[0] = new_alias
                    self.setText("\n".join(lines))
                    if main_window and hasattr(main_window, "handle_tag_rename"):
                        main_window.handle_tag_rename(self.tag_info["docker_name"], new_alias)
                    from backend import fetch_game_time
                    from PyQt5.QtCore import QRunnable, pyqtSignal, QObject
                    class Worker(QRunnable):
                        def __init__(self, fn, *args):
                            super().__init__()
                            self.fn = fn
                            self.args = args
                            self.signals = QObject()
                            self.signals.finished = pyqtSignal(object)
                            self.is_running = True

                        def run(self):
                            try:
                                if self.is_running:
                                    result = self.fn(*self.args)
                                    self.signals.finished.emit(result)
                            except Exception as e:
                                print(f"Worker error: {e}")
                            finally:
                                self.is_running = False
                    worker = Worker(fetch_game_time, new_alias)
                    worker.signals.finished.connect(partial(main_window.handle_game_time_update, new_alias))
                    main_window.add_worker(worker)
                    from PyQt5.QtCore import QThreadPool
                    QThreadPool.globalInstance().start(worker)
        elif action == move_to_action:
            from tabs import MoveToDialog
            dialog = MoveToDialog(parent=main_window)
            if dialog.exec_():
                target_tab_id = dialog.selected_tab_id
                if target_tab_id:
                    main_window.handle_tag_move(self.tag_info["docker_name"], target_tab_id)

class MyLinersDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("My Liners")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        self.btn_defs = [
            ("BackItUp", "wsl --distribution ubuntu --user root -- bash -lic 'backitup'"),
            ("BigiTGo", "wsl --distribution ubuntu --user root -- bash -lic 'bigitgo'"),
            ("gg", "wsl --distribution ubuntu --user root -- bash -lic 'gg'"),
            ("dcreds", "wsl --distribution ubuntu --user root -- bash -lic 'dcreds'"),
            ("savegames", "wsl --distribution ubuntu --user root -- bash -lic 'savegames'"),
            ("GameSaveRestore", "wsl --distribution ubuntu --user root -- bash -lic 'gamedg'")
        ]
        self.btn_defs.extend(load_custom_buttons())
        existing_buttons = {}
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
        save_custom_buttons(self.btn_defs)
        btn = self.create_button(name, cmd)
        self.layout().addWidget(btn)

    def remove_custom_button(self):
        names = [label for label, _ in self.btn_defs if label not in ["BackItUp", "BigiTGo", "gg", "dcreds", "savegames", "GameSaveRestore"]]
        name, ok = QInputDialog.getItem(self, "Remove Custom Button", "Select button to remove:", names, editable=False)
        if not ok or not name:
            return
        self.btn_defs = [(label, cmd) for label, cmd in self.btn_defs if label != name]
        save_custom_buttons(self.btn_defs)
        self.init_ui()

class UserDashboardDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
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
        from backend import load_active_users
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
        from backend import load_banned_users, save_banned_users, load_active_users, save_active_users
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
            from backend import load_active_users, save_active_users
            import time
            users = load_active_users()
            if new_user in users:
                QMessageBox.information(self, "User Exists", f"User '{new_user}' already exists.")
                return
            users[new_user] = {"login_time": time.time()}
            save_active_users(users)
            QMessageBox.information(self, "User Added", f"User '{new_user}' has been added.")
            self.populate_users()

class Buttons:
    def __init__(self, parent):
        self.parent = parent

    def create_top_bar_buttons(self):
        layout = QHBoxLayout()
        layout.addWidget(self.parent.docker_commands.create_browse_button())
        layout.addStretch()
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
        disconnect_btn.clicked.connect(self.parent.disconnect)
        layout.addWidget(disconnect_btn)
        if self.parent.is_admin:
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
            kick_btn.clicked.connect(self.parent.kick_user)
            layout.addWidget(kick_btn)
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
            dashboard_btn.clicked.connect(self.parent.open_user_dashboard)
            layout.addWidget(dashboard_btn)
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
            myliners_btn.clicked.connect(self.parent.open_myliners)
            layout.addWidget(myliners_btn)
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
            clear_terminal_btn.clicked.connect(self.parent.clear_terminal)
            layout.addWidget(clear_terminal_btn)
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
            clear_terminal_btn.clicked.connect(self.parent.clear_terminal)
            layout.addWidget(clear_terminal_btn)
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
        import sys
        exit_button.clicked.connect(lambda: sys.exit(0))
        layout.addWidget(exit_button)
        return layout

    def create_sort_button(self):
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
        sort_menu = QMenu(self.parent)
        sort_menu.addAction("Heaviest to Lightest", lambda: self.parent.sort_tags(descending=True))
        sort_menu.addAction("Lightest to Lightest", lambda: self.parent.sort_tags(descending=False))
        sort_menu.addAction("Sort by HowLong: Longest to Shortest", lambda: self.parent.sort_tags_by_time(descending=True))
        sort_menu.addAction("Sort by HowLong: Shortest to Longest", lambda: self.parent.sort_tags_by_time(descending=False))
        sort_menu.addAction("Sort by Date: Newest to Oldest", lambda: self.parent.sort_tags_by_date(descending=True))
        sort_menu.addAction("Sort by Date: Oldest to Newest", lambda: self.parent.sort_tags_by_date(descending=False))
        sort_button.setMenu(sort_menu)
        return sort_button
