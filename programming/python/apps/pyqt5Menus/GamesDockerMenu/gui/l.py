import sys
import os
import json
import subprocess
import requests
import re
import time
import base64
from datetime import datetime
from functools import partial

from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout,
    QScrollArea, QLineEdit, QGridLayout, QLabel, QMenu, QDialog,
    QListWidget, QListWidgetItem, QMessageBox, QInputDialog,
    QStackedWidget, QCheckBox, QTextEdit
)
from PyQt5.QtGui import QFont, QDrag, QPixmap, QImage, QIcon
from PyQt5.QtCore import Qt, QTimer, QRunnable, QThreadPool, QObject, pyqtSignal, pyqtSlot, QMimeData, QSize, QBuffer, QIODevice

from howlongtobeatpy import HowLongToBeat

# --- Optional word segmentation ---
try:
    import wordninja
except ImportError:
    wordninja = None

# ------------------------- Persistence Functions -------------------------

SETTINGS_FILE = "tag_settings.json"
TABS_CONFIG_FILE = "tabs_config.json"
BANNED_USERS_FILE = "banned_users.json"

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

DEFAULT_TABS_CONFIG = [
    {"id": "all", "name": "All"},
    {"id": "finished", "name": "Finished"},
    {"id": "mybackup", "name": "MyBackup"},
    {"id": "not_for_me", "name": "Not for me right now"}
]

def load_tabs_config():
    if os.path.exists(TABS_CONFIG_FILE):
        try:
            with open(TABS_CONFIG_FILE, "r") as f:
                return json.load(f)
        except Exception as e:
            print("Error loading tabs config:", e)
    return DEFAULT_TABS_CONFIG

def save_tabs_config(config):
    try:
        with open(TABS_CONFIG_FILE, "w") as f:
            json.dump(config, f)
    except Exception as e:
        print("Error saving tabs config:", e)

def load_banned_users():
    if os.path.exists(BANNED_USERS_FILE):
        try:
            with open(BANNED_USERS_FILE, "r") as f:
                return json.load(f)
        except Exception as e:
            print("Error loading banned users:", e)
    return []

def save_banned_users(banned):
    try:
        with open(BANNED_USERS_FILE, "w") as f:
            json.dump(banned, f)
    except Exception as e:
        print("Error saving banned users:", e)

persistent_settings = load_settings()
tabs_config = load_tabs_config()
banned_users = load_banned_users()

# ------------------------- Word Segmentation Helper -------------------------

def normalize_game_title(tag):
    if " " in tag:
        return tag
    if any(c.isupper() for c in tag[1:]):
        return re.sub(r'(?<!^)(?=[A-Z])', ' ', tag).strip()
    if wordninja is not None:
        return " ".join(wordninja.split(tag))
    return tag.title()

# ------------------------- HTTP Session with Retries -------------------------

from requests.adapters import HTTPAdapter, Retry

session = requests.Session()
retries = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
adapter = HTTPAdapter(max_retries=retries)
session.mount("http://", adapter)
session.mount("https://", adapter)

# ------------------------- Worker Classes -------------------------

class WorkerSignals(QObject):
    finished = pyqtSignal(object)

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

# ------------------------- Helper Functions -------------------------

def fetch_game_time(alias):
    normalized = normalize_game_title(alias)
    try:
        results = HowLongToBeat().search(normalized)
        if results:
            main_time = getattr(results[0], 'gameplay_main', None) or getattr(results[0], 'main_story', None)
            if main_time:
                return (alias, f"{main_time} hours")
            extra_time = getattr(results[0], 'gameplay_main_extra', None) or getattr(results[0], 'main_extra', None)
            if extra_time:
                return (alias, f"{extra_time} hours")
    except Exception as e:
        print(f"Error searching HowLongToBeat for '{normalized}': {e}")
    return (alias, "N/A")

def fetch_image(query):
    api_key = "a0278acb920e45e1bcc232b06f72bace"
    url = "https://api.rawg.io/api/games"
    params = {
        "key": api_key,
        "search": query,
        "page_size": 1
    }
    try:
        response = session.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            results = data.get("results", [])
            if results:
                image_url = results[0].get("background_image")
                if image_url:
                    img_response = session.get(image_url, stream=True, timeout=10)
                    if img_response.status_code == 200:
                        img = QImage()
                        img.loadFromData(img_response.content)
                        if not img.isNull():
                            return (query, img)
    except Exception as e:
        print(f"RAWG image fetch error for '{query}':", e)
    return (query, QImage())

def update_docker_tag_name(old_alias, new_alias):
    QMessageBox.information(None, "Info",
        "Renaming tags on Docker Hub is not supported by the API.\nOnly the local display name (alias) will be updated.")
    return True

def parse_date(date_str):
    try:
        return datetime.fromisoformat(date_str.replace("Z", ""))
    except Exception:
        return datetime.min

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

def pixmap_to_base64(pixmap):
    buffer = QBuffer()
    buffer.open(QIODevice.WriteOnly)
    pixmap.save(buffer, "PNG")
    b64_data = base64.b64encode(buffer.data()).decode('utf-8')
    buffer.close()
    return b64_data

# ------------------------- Docker Engine Functions -------------------------

def check_docker_engine():
    try:
        subprocess.check_output("docker info", shell=True, stderr=subprocess.STDOUT)
        return True
    except subprocess.CalledProcessError:
        return False

def start_docker_engine():
    if check_docker_engine():
        return
    docker_desktop_path = r"C:\Program Files\Docker\Docker\Docker Desktop.exe"
    try:
        subprocess.Popen([docker_desktop_path], shell=False)
        timeout = 300
        start_time = time.time()
        while not check_docker_engine():
            if time.time() - start_time > timeout:
                QMessageBox.warning(None, "Docker Start Timeout",
                                    "Docker Desktop did not start within the expected time.")
                break
            time.sleep(2)
    except Exception as e:
        print("Error starting Docker Desktop:", e)

def dkill():
    cmds = [
        'docker stop $(docker ps -aq)',
        'docker rm $(docker ps -aq)',
        'docker rmi $(docker images -q)',
        'docker system prune -a --volumes --force',
        'docker network prune --force'
    ]
    for cmd in cmds:
        try:
            subprocess.call(['powershell', '-Command', cmd])
        except Exception as e:
            print(f"Error running cleanup command '{cmd}':", e)

# ------------------------- TagContainerWidget -------------------------

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

# ------------------------- Tab Navigation Widget -------------------------

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
                    background-color: #34495E;
                    color: white;
                    padding: 6px;
                    border: none;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #2C3E50;
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

# ------------------------- MoveToDialog -------------------------

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
        for tab in tabs_config:
            btn = QPushButton(tab["name"])
            btn.setCheckable(True)
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

# ------------------------- TabGridWidget -------------------------

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
        for tab in tabs_config:
            if tab["id"] == "all":
                continue
            btn = QPushButton(tab["name"])
            btn.setCheckable(True)
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

# ------------------------- BulkMoveDialog -------------------------

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
        self.search_box.textChanged.connect(self.filter_list)
        layout.addWidget(self.search_box)
        self.list_widget = QListWidget()
        self.list_widget.setSelectionMode(QListWidget.MultiSelection)
        layout.addWidget(self.list_widget)
        self.populate_list()
        layout.addWidget(QLabel("Move selected tags to:"))
        self.tab_grid = TabGridWidget()
        layout.addWidget(self.tab_grid)
        self.move_button = QPushButton("Move Selected")
        self.move_button.clicked.connect(self.move_tags)
        layout.addWidget(self.move_button)
        self.setLayout(layout)
    def populate_list(self):
        self.list_widget.clear()
        for tag in self.all_tags:
            item = QListWidgetItem(tag["alias"])
            item.setData(Qt.UserRole, tag)
            self.list_widget.addItem(item)
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

# ------------------------- BulkPasteMoveDialog -------------------------

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
        layout.addWidget(self.text_edit)
        layout.addWidget(QLabel("Move pasted tags to:"))
        self.tab_grid = TabGridWidget()
        layout.addWidget(self.tab_grid)
        move_button = QPushButton("Move Pasted Tags")
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

# ------------------------- GameButton -------------------------
# Each button fetches an image based on its tag name and sets that image as its background.
class GameButton(QPushButton):
    dragThreshold = 10
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
                min-height: 200px;
                min-width: 200px;
                text-align: center;
                padding-top: 120px;
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
                    worker.signals.finished.connect(partial(main_window.handle_game_time_update, new_alias))
                    main_window.add_worker(worker)
                    QThreadPool.globalInstance().start(worker)
        elif action == move_to_action:
            dialog = MoveToDialog(parent=main_window)
            if dialog.exec_():
                target_tab_id = dialog.selected_tab_id
                if target_tab_id:
                    main_window.handle_tag_move(self.tag_info["docker_name"], target_tab_id)

# ------------------------- ImageWorker -------------------------

class ImageWorker(QRunnable):
    def __init__(self, query):
        super().__init__()
        self.query = query
        self.signals = WorkerSignals()
    @pyqtSlot()
    def run(self):
        result = fetch_image(self.query)
        self.signals.finished.emit(result)

# ------------------------- DeleteTagDialog -------------------------

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
        username = "michadockermisha"
        repo = "backup"
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

# ------------------------- Main Application Window -------------------------

class DockerApp(QWidget):
    PROCESS_TIMEOUT = 600  # seconds (10 minutes)
    def __init__(self, login_password, is_admin):
        super().__init__()
        self.login_password = login_password  # For admin, this is the Docker password.
        self.is_admin = is_admin
        if self.is_admin:
            self.username = "michadockermisha"
        else:
            self.username = "meir"
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
        self.setWindowTitle("michael fedro's backup&restore tool")
        self.run_processes = []  # list of tuples: (tag, process, start_time)
        self.game_times_cache = {}
        self.tag_buttons = {}
        self.image_cache = {}  # holds QPixmap objects
        self.started_image_queries = set()
        self.tabs_config = load_tabs_config()
        self.active_workers = []
        self.init_ui()
        QThreadPool.globalInstance().setMaxThreadCount(10)
        QTimer.singleShot(0, self.start_game_time_queries)
    def perform_docker_login(self):
        login_cmd = ["docker", "login", "-u", "michadockermisha", "-p", self.login_password]
        subprocess.call(login_cmd, shell=False)
        return None
    def closeEvent(self, event):
        if self.run_processes:
            while self.run_processes:
                QThreadPool.globalInstance().waitForDone(100)
        dkill()
        event.accept()
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
        main_layout.setContentsMargins(10, 10, 10, 10)
        top_bar = QHBoxLayout()
        top_bar.addStretch()
        if self.is_admin:
            kick_btn = QPushButton("Kick User")
            kick_btn.setStyleSheet("""
                QPushButton {
                    background-color: #C0392B;
                    border: none;
                    border-radius: 5px;
                    padding: 8px;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #E74C3C;
                }
                QPushButton:pressed {
                    background-color: #A93226;
                }
            """)
            kick_btn.clicked.connect(self.kick_user)
            top_bar.addWidget(kick_btn)
        exit_button = QPushButton("Exit")
        exit_button.setStyleSheet("""
            QPushButton {
                background-color: #E74C3C;
                border: none;
                border-radius: 5px;
                padding: 8px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #C0392B;
            }
            QPushButton:pressed {
                background-color: #A93226;
            }
        """)
        exit_button.clicked.connect(QApplication.instance().quit)
        top_bar.addWidget(exit_button)
        main_layout.addLayout(top_bar)
        title = QLabel("michael fedro's backup&restore tool")
        title.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                padding: 10px;
            }
        """)
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)
        # ------------------ Additional Filter Inputs ------------------
        filter_layout = QHBoxLayout()
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search tags...")
        self.search_box.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                font-size: 16px;
                border: 2px solid #3E3E3E;
                border-radius: 8px;
            }
            QLineEdit:focus {
                border: 2px solid #3498DB;
            }
        """)
        self.search_box.textChanged.connect(self.filter_buttons)
        filter_layout.addWidget(self.search_box)
        self.size_min_input = QLineEdit()
        self.size_min_input.setPlaceholderText("Min Size (GB)")
        self.size_min_input.textChanged.connect(self.filter_buttons)
        filter_layout.addWidget(self.size_min_input)
        self.size_max_input = QLineEdit()
        self.size_max_input.setPlaceholderText("Max Size (GB)")
        self.size_max_input.textChanged.connect(self.filter_buttons)
        filter_layout.addWidget(self.size_max_input)
        self.time_min_input = QLineEdit()
        self.time_min_input.setPlaceholderText("Min Time (hrs)")
        self.time_min_input.textChanged.connect(self.filter_buttons)
        filter_layout.addWidget(self.time_min_input)
        self.time_max_input = QLineEdit()
        self.time_max_input.setPlaceholderText("Max Time (hrs)")
        self.time_max_input.textChanged.connect(self.filter_buttons)
        filter_layout.addWidget(self.time_max_input)
        main_layout.addLayout(filter_layout)
        # ------------------ End Filter Inputs ------------------
        tab_mgmt_layout = QHBoxLayout()
        add_tab_btn = QPushButton("Add Tab")
        add_tab_btn.clicked.connect(lambda: self.require_admin() and self.add_tab())
        tab_mgmt_layout.addWidget(add_tab_btn)
        rename_tab_btn = QPushButton("Rename Tab")
        rename_tab_btn.clicked.connect(lambda: self.require_admin() and self.rename_tab())
        tab_mgmt_layout.addWidget(rename_tab_btn)
        delete_tab_btn = QPushButton("Delete Tab")
        delete_tab_btn.clicked.connect(lambda: self.require_admin() and self.delete_tab())
        tab_mgmt_layout.addWidget(delete_tab_btn)
        main_layout.addLayout(tab_mgmt_layout)
        self.tab_nav = TabNavigationWidget(self.tabs_config, parent=self)
        main_layout.addWidget(self.tab_nav)
        control_layout = QHBoxLayout()
        control_layout.setSpacing(10)
        sort_button = QPushButton("Sort")
        sort_button.setStyleSheet("""
            QPushButton {
                border: none;
                border-radius: 8px;
                padding: 12px;
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
        sort_menu.addAction("Heaviest to Lightest", lambda: self.sort_tags(descending=True))
        sort_menu.addAction("Lightest to Heaviest", lambda: self.sort_tags(descending=False))
        sort_menu.addAction("Sort by HowLong: Longest to Shortest", lambda: self.sort_tags_by_time(descending=True))
        sort_menu.addAction("Sort by HowLong: Shortest to Longest", lambda: self.sort_tags_by_time(descending=False))
        sort_menu.addAction("Sort by Date: Newest to Oldest", lambda: self.sort_tags_by_date(descending=True))
        sort_menu.addAction("Sort by Date: Oldest to Newest", lambda: self.sort_tags_by_date(descending=False))
        sort_button.setMenu(sort_menu)
        control_layout.addWidget(sort_button)
        run_selected = QPushButton("Run Selected")
        run_selected.setStyleSheet("""
            QPushButton {
                border: none;
                border-radius: 8px;
                padding: 12px;
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
        delete_tag_button = QPushButton("Delete Docker Tag")
        delete_tag_button.setStyleSheet("""
            QPushButton {
                border: none;
                border-radius: 8px;
                padding: 12px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #E74C3C;
            }
            QPushButton:pressed {
                background-color: #A93226;
            }
        """)
        delete_tag_button.clicked.connect(lambda: self.require_admin() and self.open_delete_dialog())
        control_layout.addWidget(delete_tag_button)
        move_tags_button = QPushButton("Move Tags")
        move_tags_button.setStyleSheet("""
            QPushButton {
                border: none;
                border-radius: 8px;
                padding: 12px;
                font-size: 14px;
                background-color: #27AE60;
            }
            QPushButton:hover {
                background-color: #2ECC71;
            }
            QPushButton:pressed {
                background-color: #1E8449;
            }
        """)
        move_tags_button.clicked.connect(lambda: self.require_admin() and self.open_bulk_move_dialog())
        control_layout.addWidget(move_tags_button)
        bulk_paste_button = QPushButton("Bulk Paste Move")
        bulk_paste_button.setStyleSheet("""
            QPushButton {
                border: none;
                border-radius: 8px;
                padding: 12px;
                font-size: 14px;
                background-color: #F39C12;
            }
            QPushButton:hover {
                background-color: #F1C40F;
            }
            QPushButton:pressed {
                background-color: #D68910;
            }
        """)
        bulk_paste_button.clicked.connect(lambda: self.require_admin() and self.open_bulk_paste_move_dialog())
        control_layout.addWidget(bulk_paste_button)
        save_txt_button = QPushButton("Save as .txt")
        save_txt_button.setStyleSheet("""
            QPushButton {
                border: none;
                border-radius: 8px;
                padding: 12px;
                font-size: 14px;
                background-color: #8E44AD;
            }
            QPushButton:hover {
                background-color: #9B59B6;
            }
            QPushButton:pressed {
                background-color: #71368A;
            }
        """)
        save_txt_button.clicked.connect(lambda: self.require_admin() and self.save_as_txt())
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
    def kick_user(self):
        username, ok = QInputDialog.getText(self, "Kick User", "Enter username to ban:")
        if ok and username:
            username = username.strip().lower()
            if username not in banned_users:
                banned_users.append(username)
                save_banned_users(banned_users)
                QMessageBox.information(self, "User Kicked", f"User '{username}' has been banned from using the app.")
            else:
                QMessageBox.information(self, "Already Banned", f"User '{username}' is already banned.")
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
    def open_bulk_move_dialog(self):
        dialog = BulkMoveDialog(self.all_tags, parent=self)
        if dialog.exec_():
            for tag in self.all_tags:
                persistent = persistent_settings.get(tag["docker_name"], {})
                persistent["category"] = tag["category"]
                persistent_settings[tag["docker_name"]] = persistent
            save_settings(persistent_settings)
            self.create_tag_buttons()
    def open_bulk_paste_move_dialog(self):
        dialog = BulkPasteMoveDialog(self.all_tags, parent=self)
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
        # Retrieve filter criteria
        try:
            size_min = float(self.size_min_input.text()) if self.size_min_input.text() else None
        except:
            size_min = None
        try:
            size_max = float(self.size_max_input.text()) if self.size_max_input.text() else None
        except:
            size_max = None
        try:
            time_min = float(self.time_min_input.text()) if self.time_min_input.text() else None
        except:
            time_min = None
        try:
            time_max = float(self.time_max_input.text()) if self.time_max_input.text() else None
        except:
            time_max = None

        for button in self.buttons:
            tag = button.tag_info
            visible = True
            # Filter by search text (alias)
            if text and text.lower() not in tag["alias"].lower():
                visible = False
            # Filter by size (convert full_size bytes to GB)
            size_gb = tag["full_size"] / (1024**3)
            if size_min is not None and size_gb < size_min:
                visible = False
            if size_max is not None and size_gb > size_max:
                visible = False
            # Filter by time
            t_str = tag["approx_time"].strip()
            if t_str == "N/A":
                if time_min is not None or time_max is not None:
                    visible = False
            else:
                try:
                    t = float(t_str.replace("hours", "").strip())
                except:
                    t = None
                if t is not None:
                    if time_min is not None and t < time_min:
                        visible = False
                    if time_max is not None and t > time_max:
                        visible = False
            button.setVisible(visible)
    def run_selected_commands(self):
        if not check_docker_engine():
            QMessageBox.warning(self, "Docker Engine Not Running",
                                "Docker Desktop Engine is not running. Please start Docker Desktop and try again.")
            return
        selected_buttons = [btn for btn in self.buttons if btn.isChecked()]
        if not selected_buttons:
            QMessageBox.information(self, "No Selection", "Please select at least one tag to run.")
            return
        current_time = time.time()
        for btn in selected_buttons:
            tag = btn.tag_info["docker_name"]
            docker_command = (
                f'docker run '
                f'--rm '
                f'--cpus=4 '
                f'--memory=8g '
                f'--memory-swap=12g '
                f'-v "C:\\games":/games '
                f'-e DISPLAY=$DISPLAY '
                f'-v /tmp/.X11-unix:/tmp/.X11-unix '
                f'--name "{tag}" '
                f'michadockermisha/backup:"{tag}" '
                f'sh -c "apk add rsync pigz && mkdir -p /games/{tag} && '
                f'rsync -aP --compress-level=1 --compress --numeric-ids '
                f'--inplace --delete-during --info=progress2 '
                f'/home/ /games/{tag}"'
            )
            proc = subprocess.Popen(docker_command, shell=True)
            self.run_processes.append((tag, proc, current_time))
            btn.setChecked(False)
        if not hasattr(self, 'run_timer') or not self.run_timer.isActive():
            self.run_timer = QTimer()
            self.run_timer.timeout.connect(self.check_run_processes)
            self.run_timer.start(500)
    def check_run_processes(self):
        still_running = []
        now = time.time()
        for tag, proc, start_time in self.run_processes:
            if now - start_time > self.PROCESS_TIMEOUT:
                proc.kill()
                QMessageBox.warning(self, "Process Timeout", f"Process for tag {tag} exceeded the timeout and was killed.")
                continue
            if proc.poll() is None:
                still_running.append((tag, proc, start_time))
        self.run_processes = still_running
        if not self.run_processes:
            self.run_timer.stop()
            QMessageBox.information(self, "Run Complete", "All selected commands have finished.")
    def open_delete_dialog(self):
        if not self.require_admin():
            return
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
        login_response = requests.post(login_url, json=login_data)
        if login_response.status_code == 200 and login_response.json().get("token"):
            self.docker_token = login_response.json().get("token")
            return self.docker_token
        else:
            QMessageBox.warning(self, "Authentication Failed", "Incorrect Docker Hub password.")
            return None

# ------------------------- Login Dialog -------------------------

class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Login")
        self.login_password = None
        self.is_admin = False
        self.init_ui()
    def init_ui(self):
        layout = QVBoxLayout(self)
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter password")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)
        login_button = QPushButton("Login")
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
            self.accept()
        else:
            username, ok = QInputDialog.getText(self, "Username Required", "Enter username:")
            if not (ok and username):
                QMessageBox.warning(self, "Login Failed", "Username is required for normal users.")
                return
            if username.strip().lower() != "meir":
                QMessageBox.warning(self, "Login Failed", "Only user 'meir' is allowed for normal user privileges.")
                return
            if username.strip().lower() in banned_users:
                QMessageBox.warning(self, "Access Denied", "This user has been banned from using the app.")
                return
            self.is_admin = False
            self.login_password = entered
            self.accept()

# ------------------------- Main -------------------------

if __name__ == '__main__':
    app = QApplication(sys.argv)
    font = QFont("Segoe UI", 12, QFont.Bold)
    app.setFont(font)
    app.setStyleSheet("""
        QWidget {
            background-color: black;
            color: white;
        }
        QMenu, QInputDialog, QMessageBox {
            background-color: black;
            color: white;
        }
    """)
    login = LoginDialog()
    if login.exec_() == QDialog.Accepted:
        docker_app = DockerApp(login.login_password, login.is_admin)
        docker_app.show()
        sys.exit(app.exec_())
    else:
        sys.exit(0)
