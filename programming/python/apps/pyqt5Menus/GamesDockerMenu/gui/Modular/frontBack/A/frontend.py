import sys
import os
import time
import base64
from functools import partial
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout,
    QScrollArea, QLineEdit, QGridLayout, QLabel, QMenu, QDialog,
    QListWidget, QListWidgetItem, QMessageBox, QInputDialog,
    QStackedWidget, QCheckBox, QTextEdit, QFileDialog
)
from PyQt5.QtGui import QFont, QDrag, QPixmap, QImage, QIcon
from PyQt5.QtCore import Qt, QTimer, QRunnable, QThreadPool, QObject, pyqtSignal, pyqtSlot, QMimeData, QSize, QBuffer, QIODevice
from backend import *

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

    @pyqtSlot()
    def run(self):
        try:
            result = self.fn(*self.args, **self.kwargs)
            if self.is_running:
                self.signals.finished.emit(result)
        except Exception as e:
            print(f"Worker error: {e}")
        finally:
            self.is_running = False

class DockerPullWorker(QRunnable):
    def __init__(self, tag):
        super().__init__()
        self.tag = tag
        self.is_running = True

    @pyqtSlot()
    def run(self):
        try:
            pull_docker_image(self.tag)
        except Exception as e:
            print(f"DockerPullWorker error: {e}")
        finally:
            self.is_running = False

class ImageWorker(QRunnable):
    def __init__(self, query, button):
        super().__init__()
        self.query = query
        self.button = button
        self.signals = WorkerSignals()
        self.is_running = True

    @pyqtSlot()
    def run(self):
        try:
            if self.button and not self.button.isHidden() and self.button.parent():
                result = fetch_image(self.query)
                if self.is_running and self.button and self.signals:
                    self.signals.finished.emit(result)
        except Exception as e:
            print(f"ImageWorker error: {e}")
        finally:
            self.is_running = False

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

class TagContainerWidget(QWidget):
    def __init__(self, type_name, parent=None):
        super().__init__(parent)
        self.type_name = type_name
        self.setAcceptDrops(True)
        self.layout = QGridLayout(self)
        self.layout.setSpacing(10)
        self.setLayout(self.layout)

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dragMoveEvent(self, event):
        event.acceptProposedAction()

    def dropEvent(self, event):
        docker_name = event.mimeData().text()
        main_window = self.window()
        if main_window and hasattr(main_window, "update_tag_category"):
            main_window.update_tag_category(docker_name, self.type_name)
        event.acceptProposedAction()

class TabNavigationWidget(QWidget):
    def __init__(self, tabs_config, parent=None):
        super().__init__(parent)
        self.tabs_config = tabs_config
        self.init_ui()

    def init_ui(self):
        self.layout = QGridLayout(self)
        self.layout.setSpacing(5)
        self.setLayout(self.layout)
        self.create_tab_buttons()

    def create_tab_buttons(self):
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        self.buttons = {}
        col = 0
        row = 0
        for tab in self.tabs_config:
            btn = QPushButton(tab["name"])
            btn.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                stop:0 #2C3E50, stop:1 #34495E);
                    color: white;
                    padding: 8px 12px;
                    border: 1px solid #1ABC9C;
                    border-radius: 6px;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                stop:0 #1ABC9C, stop:1 #16A085);
                }
            """)
            btn.clicked.connect(partial(self.tab_clicked, tab["id"]))
            self.layout.addWidget(btn, row, col)
            self.buttons[tab["id"]] = btn
            col += 1
            if col >= 5:
                col = 0
                row += 1

    def tab_clicked(self, tab_id):
        self.parent().set_current_tab(tab_id)

    def update_tabs(self, tabs_config):
        self.tabs_config = tabs_config
        self.create_tab_buttons()

class MoveToDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Target Tab")
        self.selected_tab_id = None
        self.init_ui()

    def init_ui(self):
        layout = QGridLayout(self)
        layout.setSpacing(5)
        col = 0
        row = 0
        for tab in load_tabs_config():
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

class TabGridWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QGridLayout(self)
        self.layout.setSpacing(5)
        self.setLayout(self.layout)
        self.selected_tab_id = None
        self.create_tab_buttons()

    def create_tab_buttons(self):
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        col = 0
        row = 0
        self.buttons = {}
        for tab in load_tabs_config():
            if tab["id"] == "all":
                continue
            btn = QPushButton(tab["name"])
            btn.setCheckable(True)
            btn.setStyleSheet("""
                QPushButton {
                    background: #16A085;
                    color: white;
                    padding: 6px 10px;
                    border-radius: 4px;
                }
                QPushButton:checked {
                    background: #1ABC9C;
                }
            """)
            btn.clicked.connect(partial(self.tab_clicked, tab["id"]))
            self.layout.addWidget(btn, row, col)
            self.buttons[tab["id"]] = btn
            col += 1
            if col >= 5:
                col = 0
                row += 1

    def tab_clicked(self, tid):
        self.selected_tab_id = tid
        for k, b in self.buttons.items():
            if k != tid:
                b.setChecked(False)

class BulkMoveDialog(QDialog):
    def __init__(self, all_tags, parent=None):
        super().__init__(parent)
        self.all_tags = all_tags
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
        self.tab_grid = TabGridWidget()
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
    def __init__(self, all_tags, parent=None):
        super().__init__(parent)
        self.all_tags = all_tags
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
        self.tab_grid = TabGridWidget()
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
                                                 "Enter new tag name:", QLineEdit.Normal, self.tag_info["alias"])
            if ok and new_alias:
                old_alias = self.tag_info["alias"]
                if update_docker_tag_name(old_alias, new_alias):
                    self.tag_info["alias"] = new_alias
                    persistent = load_settings().get(self.tag_info["docker_name"], {})
                    persistent["alias"] = new_alias
                    settings = load_settings()
                    settings[self.tag_info["docker_name"]] = persistent
                    save_settings(settings)
                    lines = self.text().splitlines()
                    lines[0] = new_alias
                    self.setText("\n".join(lines))
                    if main_window and hasattr(main_window, "handle_tag_rename"):
                        main_window.handle_tag_rename(self.tag_info["docker_name"], new_alias)
                    worker = Worker(fetch_game_time, new_alias)
                    worker.signals.finished.connect(partial(main_window.handle_game_time_update, new_alias))
                    main_window.add_worker(worker)
                    QThreadPool.globalInstance().start(worker)
        elif action == move_to_action:
            dialog = MoveToDialog(parent=main_window)
            if dialog.exec_():
                target_tab_id = dialog.selected_tab_id
                if target_tab_id:
                    main_window.handle_tag_move(self.tag_info["docker_name"], target_tab_id)

class DeleteTagDialog(QDialog):
    def __init__(self, all_tags, parent=None):
        super().__init__(parent)
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
        token = self.parent().get_docker_token()
        if not token:
            return
        successes = []
        failures = []
        for tag in tags:
            if delete_docker_tag(token, tag):
                successes.append(tag)
            else:
                failures.append(tag)
        message = ""
        if successes:
            message += "Successfully deleted:\n" + "\n".join(successes) + "\n\n"
            for tag in successes:
                items = self.list_widget.findItems(tag, Qt.MatchContains)
                for item in items:
                    row = self.list_widget.row(item)
                    self.list_widget.takeItem(row)
        if failures:
            message += "Failed to delete:\n" + "\n".join(failures)
        QMessageBox.information(self, "Deletion Summary", message or "No tags deleted.")
        if self.parent() and hasattr(self.parent(), "refresh_tags"):
            self.parent().refresh_tags()

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
            users = load_active_users()
            if new_user in users:
                QMessageBox.information(self, "User Exists", f"User '{new_user}' already exists.")
                return
            users[new_user] = {"login_time": time.time()}
            save_active_users(users)
            QMessageBox.information(self, "User Added", f"User '{new_user}' has been added.")
            self.populate_users()

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
        self.image_cache = {}
        self.active_workers = []
        self.tabs_config = load_tabs_config()
        self.init_ui()
        QThreadPool.globalInstance().setMaxThreadCount(10)
        self.add_active_user()
        self.banned_timer = QTimer()
        self.banned_timer.timeout.connect(self.check_banned)
        self.banned_timer.start(3000)
        self.run_processes = []
        self.setAttribute(Qt.WA_DeleteOnClose, True)

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
        sys.exit(0)

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

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(12, 12, 12, 12)
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
        title = QLabel("michael fedro's backup & restore tool")
        title.setStyleSheet("font-size: 28px; font-weight: bold; color: #F1C40F;")
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)
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
        self.tab_nav = TabNavigationWidget(self.tabs_config, parent=self)
        main_layout.addWidget(self.tab_nav)
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
        self.stacked = QStackedWidget()
        self.tab_pages = {}
        for tab in self.tabs_config:
            container = TagContainerWidget(tab["id"], parent=self)
            self.tab_pages[tab["id"]] = container
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
        save_tabs_config(self.tabs_config)
        container = TagContainerWidget(new_id, parent=self)
        self.tab_pages[new_id] = container
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
        dialog = BulkMoveDialog(self.all_tags, parent=self)
        if dialog.exec_():
            for tag in self.all_tags:
                persistent = self.persistent_settings.get(tag["docker_name"], {})
                persistent["category"] = tag["category"]
                self.persistent_settings[tag["docker_name"]] = persistent
            save_settings(self.persistent_settings)
            self.create_tag_buttons()

    def open_bulk_paste_move_dialog(self):
        dialog = BulkPasteMoveDialog(self.all_tags, parent=self)
        if dialog.exec_():
            for tag in self.all_tags:
                persistent = self.persistent_settings.get(tag["docker_name"], {})
                persistent["category"] = tag["category"]
                self.persistent_settings[tag["docker_name"]] = persistent
            save_settings(self.persistent_settings)
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
        # Stop existing workers
        for worker in self.active_workers[:]:
            worker.is_running = False
            try:
                worker.signals.finished.disconnect()
            except TypeError:
                pass
        self.active_workers.clear()

        # Clear existing buttons
        for container in self.tab_pages.values():
            for i in reversed(range(container.layout.count())):
                widget = container.layout.itemAt(i).widget()
                if widget:
                    widget.setParent(None)
                    widget.deleteLater()

        self.buttons = []
        self.tag_buttons = {}
        positions = {}
        for tab in self.tabs_config:
            positions[tab["id"]] = [0, 0]

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
                    worker = ImageWorker(tag["alias"], button)
                    worker.signals.finished.connect(partial(self.handle_image_update, tag["alias"], button))
                    self.add_worker(worker)
                    QThreadPool.globalInstance().start(worker)

        QTimer.singleShot(10, self.start_game_time_queries)

    def start_game_time_queries(self):
        for tag in self.all_tags:
            alias = tag["alias"]
            if alias not in self.game_times_cache:
                worker = Worker(fetch_game_time, alias)
                worker.signals.finished.connect(partial(self.handle_game_time_update, alias))
                self.add_worker(worker)
                QThreadPool.globalInstance().start(worker)

    def handle_game_time_update(self, alias, time_info):
        self.game_times_cache[alias] = time_info
        for docker_name, buttons in self.tag_buttons.items():
            for button in buttons:
                if button.tag_info["alias"] == alias and button.parent():
                    lines = button.text().splitlines()
                    if len(lines) >= 3:
                        lines[2] = f"Approx Time: {time_info}" if time_info != "N/A" else "Approx Time: N/A"
                    else:
                        lines.append(f"Approx Time: {time_info}" if time_info != "N/A" else "Approx Time: N/A")
                    button.setText("\n".join(lines))

    def handle_image_update(self, alias, button, result):
        if not button or not button.parent():
            return
        image_data = result[1] if isinstance(result, tuple) else result
        if image_data:
            image = QImage()
            image.loadFromData(image_data)
            if not image.isNull():
                scaled_image = image.scaled(button.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
                pixmap = QPixmap.fromImage(scaled_image)
                self.image_cache[alias] = pixmap
                buffer = QBuffer()
                buffer.open(QIODevice.WriteOnly)
                pixmap.save(buffer, "PNG")
                b64_data = base64.b64encode(buffer.data()).decode('utf-8')
                buffer.close()
                base_style = button.styleSheet()
                bg_style = f"background-image: url(data:image/png;base64,{b64_data}); background-position: center; background-repeat: no-repeat;"
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
        self.all_tags.sort(key=lambda x: parse_time(self.time_data.get(x["alias"].lower(), "0")), reverse=descending)
        self.create_tag_buttons()

    def sort_tags_by_date(self, descending=True):
        self.all_tags.sort(key=lambda x: parse_date(x.get("last_updated", "")), reverse=descending)
        self.create_tag_buttons()

    def filter_buttons(self, text):
        for button in self.buttons:
            if button.parent():
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
        selected_buttons = [btn for btn in self.buttons if btn.isChecked() and btn.parent()]
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
            run_docker_command(tag, destination_path)
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
        self.create_tag_buttons()

    def refresh_tags(self):
        self.all_tags = fetch_tags()
        for tag in self.all_tags:
            tag["docker_name"] = tag["name"]
            stored_alias = self.persistent_settings.get(tag["docker_name"], {}).get("alias", tag["name"])
            stored_cat = self.persistent_settings.get(tag["docker_name"], {}).get("category", "all")
            tag["alias"] = stored_alias
            tag["category"] = stored_cat if any(tab["id"] == stored_cat for tab in self.tabs_config) else "all"
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
        cmd = 'powershell -NoProfile -Command "Clear-Host; [System.Console]::Clear(); cls"'
        try:
            subprocess.Popen(cmd, shell=True)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error clearing terminal: {e}")

class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
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
            if username.strip().lower() in load_banned_users():
                QMessageBox.warning(self, "Access Denied", "This user has been banned from using the app.")
                return
            self.is_admin = False
            self.login_password = entered
            self.username = username.strip().lower()
            self.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(f"""
        QWidget {{
            background-image: url(b.png);
            background-repeat: no-repeat;
            background-position: center;
            color: white;
        }}
        QMenu, QInputDialog, QMessageBox {{
            background-image: url(b.png);
            background-repeat: no-repeat;
            background-position: center;
            color: white;
        }}
    """)
    font = QFont("Segoe UI", 12, QFont.Bold)
    app.setFont(font)
    session_data = load_session()
    if session_data is None:
        login = LoginDialog()
        if login.exec_() == QDialog.Accepted:
            session_data = {
                "username": login.username,
                "login_password": login.login_password,
                "is_admin": login.is_admin
            }
            save_session(session_data)
        else:
            sys.exit(0)
    docker_app = DockerApp(session_data["login_password"], session_data["is_admin"], session_data["username"])
    docker_app.show()
    sys.exit(app.exec_())