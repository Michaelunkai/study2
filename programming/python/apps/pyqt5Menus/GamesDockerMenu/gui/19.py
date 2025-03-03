import sys
import os
import json
import subprocess
import requests
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout,
    QScrollArea, QLineEdit, QGridLayout, QLabel, QFrame,
    QMenu, QDialog, QListWidget, QListWidgetItem, QMessageBox, QInputDialog,
    QTabWidget, QCheckBox
)
from PyQt5.QtGui import QFont, QDrag, QCursor, QPalette, QColor, QPixmap, QImage, QIcon
from PyQt5.QtCore import Qt, QTimer, QRunnable, QThreadPool, QObject, pyqtSignal, pyqtSlot, QMimeData, QPoint, QSize
from howlongtobeatpy import HowLongToBeat

# --- Persistence functions for tag settings (alias and category) ---
SETTINGS_FILE = "tag_settings.json"

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r") as f:
                return json.load(f)
        except Exception as e:
            print("Error loading settings file:", e)
    return {}

def save_settings(settings):
    try:
        with open(SETTINGS_FILE, "w") as f:
            json.dump(settings, f)
    except Exception as e:
        print("Error saving settings file:", e)

persistent_settings = load_settings()

# --- Worker Signals and Worker class using QRunnable ---
class WorkerSignals(QObject):
    finished = pyqtSignal(object)  # emits a tuple

class Worker(QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super().__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()
    @pyqtSlot()
    def run(self):
        result = self.fn(*self.args, **self.kwargs)
        self.signals.finished.emit(result)

# --- Functions for fetching game time and image ---
def fetch_game_time(alias):
    time_val = ""
    try:
        results = HowLongToBeat().search(alias)
        if results:
            main_time = getattr(results[0], 'gameplay_main', None) or getattr(results[0], 'main_story', None)
            if main_time:
                time_val = f"{main_time} hours"
            else:
                extra_time = getattr(results[0], 'gameplay_main_extra', None) or getattr(results[0], 'main_extra', None)
                if extra_time:
                    time_val = f"{extra_time} hours"
    except Exception as e:
        print(f"Error searching howlongtobeat for '{alias}': {e}")
    return (alias, time_val)

def fetch_image(query):
    try:
        url = "https://duckduckgo.com/i.js"
        params = {"q": query, "o": "json", "iax": "images", "ia": "images"}
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, params=params, headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            results = data.get("results", [])
            if results:
                image_url = results[0].get("image")
                if image_url:
                    img_response = requests.get(image_url, stream=True, timeout=5)
                    if img_response.status_code == 200:
                        img = QImage()
                        img.loadFromData(img_response.content)
                        return (query, img)
    except Exception as e:
        print(f"Error fetching image for '{query}':", e)
    return (query, QImage())

# --- Dummy function to "update" Docker Hub tag name ---
def update_docker_tag_name(old_alias, new_alias):
    QMessageBox.information(None, "Info",
        "Renaming tags on Docker Hub is not supported by the API.\n"
        "Only the local display name (alias) will be updated.")
    return True

# --- Custom widget for drag-and-drop containers ---
class TagContainerWidget(QWidget):
    def __init__(self, type_name, parent=None):
        super().__init__(parent)
        self.type_name = type_name  # "all", "finished", "mybackup", or "not_for_me"
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

# --- Styled Button Class ---
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

# --- Game Button Class with Context Menu for renaming and moving ---
class GameButton(QPushButton):
    dragThreshold = 10  # pixels
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
                min-height: 70px;
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
        self._drag_start_pos = None
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_start_pos = event.pos()
        super().mousePressEvent(event)
    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            if (event.pos() - self._drag_start_pos).manhattanLength() >= self.dragThreshold:
                mimeData = QMimeData()
                mimeData.setText(self.tag_info["docker_name"])
                drag = QDrag(self)
                drag.setMimeData(mimeData)
                drag.exec_(Qt.MoveAction)
                return
        super().mouseMoveEvent(event)
    def get_main_window(self):
        parent = self.parent()
        while parent:
            if hasattr(parent, "handle_tag_move"):
                return parent
            parent = parent.parent()
        return None
    def contextMenuEvent(self, event):
        menu = QMenu(self)
        change_action = menu.addAction("Change Tag Name")
        move_menu = menu.addMenu("Move To")
        move_all = move_menu.addAction("All")
        move_finished = move_menu.addAction("Finished")
        move_mybackup = move_menu.addAction("MyBackup")
        move_not_for_me = move_menu.addAction("not for me right now")
        action = menu.exec_(event.globalPos())
        main_window = self.get_main_window()
        if action == change_action:
            new_alias, ok = QInputDialog.getText(self, "Change Tag Name",
                                                   "Enter new tag name:", QLineEdit.Normal, self.tag_info["alias"])
            if ok and new_alias:
                old_alias = self.tag_info["alias"]
                if update_docker_tag_name(old_alias, new_alias):
                    self.tag_info["alias"] = new_alias
                    persistent = persistent_settings.get(self.tag_info["docker_name"], {})
                    persistent["alias"] = new_alias
                    persistent_settings[self.tag_info["docker_name"]] = persistent
                    save_settings(persistent_settings)
                    lines = self.text().splitlines()
                    lines[0] = new_alias
                    self.setText("\n".join(lines))
                    if main_window and hasattr(main_window, "handle_tag_rename"):
                        main_window.handle_tag_rename(self.tag_info["docker_name"], new_alias)
                    worker = Worker(fetch_game_time, new_alias)
                    if main_window and hasattr(main_window, "handle_game_time_update"):
                        worker.signals.finished.connect(main_window.handle_game_time_update)
                    QThreadPool.globalInstance().start(worker)
        elif action == move_all:
            if main_window and hasattr(main_window, "handle_tag_move"):
                main_window.handle_tag_move(self.tag_info["docker_name"], "all")
        elif action == move_finished:
            if main_window and hasattr(main_window, "handle_tag_move"):
                main_window.handle_tag_move(self.tag_info["docker_name"], "finished")
        elif action == move_mybackup:
            if main_window and hasattr(main_window, "handle_tag_move"):
                main_window.handle_tag_move(self.tag_info["docker_name"], "mybackup")
        elif action == move_not_for_me:
            if main_window and hasattr(main_window, "handle_tag_move"):
                main_window.handle_tag_move(self.tag_info["docker_name"], "not_for_me")

# --- Image Worker using QRunnable ---
class ImageWorker(QRunnable):
    def __init__(self, query):
        super().__init__()
        self.query = query
        self.signals = WorkerSignals()
    @pyqtSlot()
    def run(self):
        try:
            url = "https://duckduckgo.com/i.js"
            params = {"q": self.query, "o": "json", "iax": "images", "ia": "images"}
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(url, params=params, headers=headers, timeout=5)
            if response.status_code == 200:
                data = response.json()
                results = data.get("results", [])
                if results:
                    image_url = results[0].get("image")
                    if image_url:
                        img_response = requests.get(image_url, stream=True, timeout=5)
                        if img_response.status_code == 200:
                            img = QImage()
                            img.loadFromData(img_response.content)
                            self.signals.finished.emit((self.query, img))
                            return
        except Exception as e:
            print(f"Error fetching image for '{self.query}':", e)
        self.signals.finished.emit((self.query, QImage()))

# --- Dialog for Deleting Tags with Duplicate Filter Option ---
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
        layout.addWidget(self.search_box)
        self.dup_checkbox = QCheckBox("Show only duplicate tags")
        layout.addWidget(self.dup_checkbox)
        self.dup_checkbox.stateChanged.connect(self.populate_list)
        self.list_widget = QListWidget()
        self.list_widget.setSelectionMode(QListWidget.MultiSelection)
        layout.addWidget(self.list_widget)
        self.populate_list()
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
        password, ok = QInputDialog.getText(self, "Docker Hub Authentication",
                                            "Enter Docker Hub password:", QLineEdit.Password)
        if not (ok and password):
            return
        username = "michadockermisha"
        repo = "backup"
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
        if self.parent() and hasattr(self.parent(), "refresh_tags"):
            self.parent().refresh_tags()

# --- Main Application Window ---
class DockerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.all_tags = self.fetch_tags()
        for tag in self.all_tags:
            tag["docker_name"] = tag["name"]
            tag["alias"] = persistent_settings.get(tag["docker_name"], {}).get("alias", tag["docker_name"])
            tag["category"] = persistent_settings.get(tag["docker_name"], {}).get("category", "all")
        self.setWindowTitle("michael fedro's backup&restore tool")
        self.run_processes = []
        self.game_times_cache = {}  # Keyed by alias
        self.tag_buttons = {}       # Mapping docker_name -> list of GameButton widgets.
        self.image_cache = {}       # Keyed by alias
        self.started_image_queries = set()
        self.mybackup_authorized = False
        self.previous_tab_index = 0
        self.init_ui()
        QThreadPool.globalInstance().setMaxThreadCount(10)
        QTimer.singleShot(0, self.start_game_time_queries)
    def fetch_tags(self):
        url = "https://hub.docker.com/v2/repositories/michadockermisha/backup/tags?page_size=100"
        tag_list = []
        while url:
            try:
                response = requests.get(url)
                data = response.json()
                for item in data.get("results", []):
                    tag_list.append({
                        "name": item["name"],
                        "full_size": item.get("full_size", 0)
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
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)
        title = QLabel("michael fedro's backup&restore tool")
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
        action_time_long = sort_menu.addAction("Sort by Time: Longest to Shortest")
        action_time_short = sort_menu.addAction("Sort by Time: Shortest to Longest")
        action_heavy.triggered.connect(lambda: self.sort_tags(descending=True))
        action_light.triggered.connect(lambda: self.sort_tags(descending=False))
        action_time_long.triggered.connect(lambda: self.sort_tags_by_time(descending=True))
        action_time_short.triggered.connect(lambda: self.sort_tags_by_time(descending=False))
        sort_button.setMenu(sort_menu)
        control_layout.addWidget(sort_button)
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
        self.tabs = QTabWidget()
        self.all_container = TagContainerWidget("all", parent=self)
        all_scroll = QScrollArea()
        all_scroll.setWidgetResizable(True)
        all_scroll.setWidget(self.all_container)
        self.tabs.addTab(all_scroll, "All")
        self.finished_container = TagContainerWidget("finished", parent=self)
        finished_scroll = QScrollArea()
        finished_scroll.setWidgetResizable(True)
        finished_scroll.setWidget(self.finished_container)
        self.tabs.addTab(finished_scroll, "Finished")
        self.mybackup_container = TagContainerWidget("mybackup", parent=self)
        mybackup_scroll = QScrollArea()
        mybackup_scroll.setWidgetResizable(True)
        mybackup_scroll.setWidget(self.mybackup_container)
        self.tabs.addTab(mybackup_scroll, "MyBackup")
        self.not_for_me_container = TagContainerWidget("not_for_me", parent=self)
        not_for_me_scroll = QScrollArea()
        not_for_me_scroll.setWidgetResizable(True)
        not_for_me_scroll.setWidget(self.not_for_me_container)
        self.tabs.addTab(not_for_me_scroll, "not for me right now")
        palette = self.tabs.palette()
        palette.setColor(QPalette.WindowText, QColor("red"))
        self.tabs.setPalette(palette)
        main_layout.addWidget(self.tabs)
        self.tabs.currentChanged.connect(self.on_tab_changed)
        self.previous_tab_index = 0
        self.create_tag_buttons()
    def create_tag_buttons(self):
        for container in (self.all_container, self.finished_container, self.mybackup_container, self.not_for_me_container):
            for i in reversed(range(container.layout.count())):
                widget = container.layout.itemAt(i).widget()
                if widget:
                    widget.setParent(None)
        self.buttons = []
        self.tag_buttons = {}
        pos = {"all": [0, 0], "finished": [0, 0], "mybackup": [0, 0], "not_for_me": [0, 0]}
        for tag in self.all_tags:
            text_lines = [tag["alias"], f"({self.format_size(tag['full_size'])})"]
            if tag["alias"] in self.game_times_cache and self.game_times_cache[tag["alias"]]:
                text_lines.append(f"Approx Time: {self.game_times_cache[tag['alias']]}")
            display_text = "\n".join(text_lines)
            button = GameButton(display_text)
            button.tag_info = tag
            button.setIconSize(QSize(64, 64))
            self.tag_buttons.setdefault(tag["docker_name"], []).append(button)
            self.buttons.append(button)
            cat = tag.get("category", "all")
            container = {"all": self.all_container, "finished": self.finished_container,
                         "mybackup": self.mybackup_container, "not_for_me": self.not_for_me_container}.get(cat, self.all_container)
            row, col = pos[cat]
            container.layout.addWidget(button, row, col)
            col += 1
            if col == 4:
                col = 0
                row += 1
            pos[cat] = [row, col]
            alias = tag["alias"]
            if alias in self.image_cache:
                button.setIcon(QIcon(self.image_cache[alias]))
            elif alias not in getattr(self, "started_image_queries", set()):
                worker = Worker(fetch_image, alias)
                worker.signals.finished.connect(lambda result: self.handle_image_update(*result))
                QThreadPool.globalInstance().start(worker)
                if not hasattr(self, "started_image_queries"):
                    self.started_image_queries = set()
                self.started_image_queries.add(alias)
    def start_game_time_queries(self):
        for tag in self.all_tags:
            alias = tag["alias"]
            if alias not in self.game_times_cache:
                worker = Worker(fetch_game_time, alias)
                worker.signals.finished.connect(lambda result: self.handle_game_time_update(*result))
                QThreadPool.globalInstance().start(worker)
    def handle_game_time_update(self, alias, time_info):
        self.game_times_cache[alias] = time_info
        for docker_name, buttons in self.tag_buttons.items():
            for button in buttons:
                if button.tag_info["alias"] == alias:
                    lines = button.text().splitlines()
                    if len(lines) == 2 and time_info:
                        lines.append(f"Approx Time: {time_info}")
                    elif len(lines) >= 3:
                        if time_info:
                            lines[2] = f"Approx Time: {time_info}"
                        else:
                            lines = lines[:2]
                    button.setText("\n".join(lines))
    def handle_image_update(self, alias, image):
        if not image.isNull():
            pixmap = QPixmap.fromImage(image)
            self.image_cache[alias] = pixmap
            for docker_name, buttons in self.tag_buttons.items():
                for button in buttons:
                    if button.tag_info["alias"] == alias:
                        button.setIcon(QIcon(pixmap))
        else:
            self.image_cache[alias] = QPixmap()
    def sort_tags(self, descending=True):
        self.all_tags.sort(key=lambda x: x["full_size"], reverse=descending)
        self.create_tag_buttons()
    def sort_tags_by_time(self, descending=True):
        self.all_tags.sort(key=lambda x: parse_time(self.game_times_cache.get(x["alias"], "")), reverse=descending)
        self.create_tag_buttons()
    def filter_buttons(self, text):
        for button in self.buttons:
            if text.lower() in button.tag_info["alias"].lower():
                button.setVisible(True)
            else:
                button.setVisible(False)
    def run_selected_commands(self):
        selected_buttons = [btn for btn in self.buttons if btn.isChecked()]
        if not selected_buttons:
            QMessageBox.information(self, "No Selection", "Please select at least one tag to run.")
            return
        processes = []
        for btn in selected_buttons:
            tag = btn.tag_info["docker_name"]
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
    def update_tag_category(self, docker_name, new_category):
        for tag in self.all_tags:
            if tag["docker_name"] == docker_name:
                tag["category"] = new_category
                persistent = persistent_settings.get(docker_name, {})
                persistent["category"] = new_category
                persistent_settings[docker_name] = persistent
                save_settings(persistent_settings)
        self.create_tag_buttons()
    def handle_tag_move(self, docker_name, new_category):
        self.update_tag_category(docker_name, new_category)
    def handle_tag_rename(self, docker_name, new_alias):
        for tag in self.all_tags:
            if tag["docker_name"] == docker_name:
                tag["alias"] = new_alias
                persistent = persistent_settings.get(docker_name, {})
                persistent["alias"] = new_alias
                persistent_settings[docker_name] = persistent
                save_settings(persistent_settings)
        self.create_tag_buttons()
    def refresh_tags(self):
        self.all_tags = self.fetch_tags()
        for tag in self.all_tags:
            tag["docker_name"] = tag["name"]
            tag["alias"] = persistent_settings.get(tag["docker_name"], {}).get("alias", tag["name"])
            tag["category"] = persistent_settings.get(tag["docker_name"], {}).get("category", "all")
        self.create_tag_buttons()
    def on_tab_changed(self, index):
        current_tab_text = self.tabs.tabText(index)
        if current_tab_text == "MyBackup" and not self.mybackup_authorized:
            password, ok = QInputDialog.getText(self, "MyBackup Access",
                                                  "Enter your Docker Hub password:",
                                                  QLineEdit.Password)
            username = "michadockermisha"
            login_url = "https://hub.docker.com/v2/users/login/"
            login_data = {"username": username, "password": password} if ok else {}
            if ok:
                login_response = requests.post(login_url, json=login_data)
                if login_response.status_code == 200 and login_response.json().get("token"):
                    self.mybackup_authorized = True
                else:
                    QMessageBox.warning(self, "Access Denied", "Incorrect password.")
                    self.tabs.setCurrentIndex(self.previous_tab_index)
                    return
            else:
                self.tabs.setCurrentIndex(self.previous_tab_index)
                return
        self.previous_tab_index = index

if __name__ == '__main__':
    app = QApplication(sys.argv)
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    QThreadPool.globalInstance().setMaxThreadCount(10)
    docker_app = DockerApp()
    docker_app.show()
    sys.exit(app.exec_())
