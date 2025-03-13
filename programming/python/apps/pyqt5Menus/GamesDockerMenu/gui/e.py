import sys
import os
import json
import subprocess
import requests
import re
import time
from datetime import datetime
from functools import partial

from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout,
    QScrollArea, QLineEdit, QGridLayout, QLabel, QMenu, QDialog,
    QListWidget, QListWidgetItem, QMessageBox, QInputDialog,
    QStackedWidget, QCheckBox, QTextEdit
)
from PyQt5.QtGui import QFont, QDrag, QPixmap, QImage, QIcon
from PyQt5.QtCore import Qt, QTimer, QRunnable, QThreadPool, QObject, pyqtSignal, pyqtSlot, QMimeData, QSize

from howlongtobeatpy import HowLongToBeat

# --- Optional word segmentation ---
try:
    import wordninja
except ImportError:
    wordninja = None

# ------------------------- Persistence Functions -------------------------

SETTINGS_FILE = "tag_settings.json"
TABS_CONFIG_FILE = "tabs_config.json"

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

persistent_settings = load_settings()
tabs_config = load_tabs_config()

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
    try:
        url = "https://duckduckgo.com/i.js"
        params = {"q": query, "o": "json", "iax": "images", "ia": "images"}
        headers = {"User-Agent": "Mozilla/5.0"}
        response = session.get(url, params=params, headers=headers, timeout=20)
        if response.status_code == 200:
            data = response.json()
            results = data.get("results", [])
            if results:
                image_url = results[0].get("image")
                if image_url:
                    img_response = session.get(image_url, stream=True, timeout=20)
                    if img_response.status_code == 200:
                        img = QImage()
                        img.loadFromData(img_response.content)
                        return (query, img)
    except Exception as e:
        print(f"Error fetching image for '{query}':", e)
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

# ------------------------- Docker Engine Functions -------------------------

def check_docker_engine():
    """Check if Docker engine is running by executing 'docker info'."""
    try:
        subprocess.check_output("docker info", shell=True, stderr=subprocess.STDOUT)
        return True
    except subprocess.CalledProcessError:
        return False

def start_docker_engine():
    """
    Start Docker Desktop Engine if it is not running.
    This function launches Docker Desktop from its installation directory and waits until docker info succeeds.
    """
    if check_docker_engine():
        return
    docker_desktop_path = r"C:\Program Files\Docker\Docker\Docker Desktop.exe"
    try:
        # Start Docker Desktop (non-blocking)
        subprocess.Popen([docker_desktop_path], shell=False)
        # Wait until Docker engine is ready
        timeout = 300  # seconds
        start_time = time.time()
        while not check_docker_engine():
            if time.time() - start_time > timeout:
                QMessageBox.warning(None, "Docker Start Timeout",
                                    "Docker Desktop did not start within the expected time.")
                break
            time.sleep(2)
    except Exception as e:
        print("Error starting Docker Desktop:", e)

# ------------------------- Docker Cleanup Function -------------------------

def dkill():
    """
    Immediately stop all running containers, remove all containers and images,
    and prune the system and network. Uses PowerShell commands.
    """
    cmds = [
        'docker stop (docker ps -aq) -ErrorAction SilentlyContinue',
        'docker rm (docker ps -aq) -ErrorAction SilentlyContinue',
        'docker rmi (docker images -q) -ErrorAction SilentlyContinue',
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

# ------------------------- Tab Navigation Widget (5 per row) -------------------------

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

# ------------------------- MoveToDialog (for right-click Move To) -------------------------

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

# ------------------------- TabGridWidget (for Bulk Move/Paste) -------------------------

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
        move_to_action = menu.addAction("Move To")
        action = menu.exec_(event.globalPos())
        main_window = self.get_main_window()
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
    def __init__(self):
        super().__init__()
        # Start Docker engine if not already running.
        start_docker_engine()
        self.all_tags = self.fetch_tags()
        for tag in self.all_tags:
            tag["docker_name"] = tag["name"]
            tag["alias"] = persistent_settings.get(tag["docker_name"], {}).get("alias", tag["docker_name"])
            stored_cat = persistent_settings.get(tag["docker_name"], {}).get("category", "all")
            tag["category"] = stored_cat if any(tab["id"] == stored_cat for tab in tabs_config) else "all"
        self.setWindowTitle("michael fedro's backup&restore tool")
        self.run_processes = []
        self.game_times_cache = {}
        self.tag_buttons = {}
        self.image_cache = {}
        self.started_image_queries = set()
        self.mybackup_authorized = False
        self.tabs_config = load_tabs_config()
        self.docker_token = None
        self.active_workers = []
        self.init_ui()
        QThreadPool.globalInstance().setMaxThreadCount(10)
        QTimer.singleShot(0, self.start_game_time_queries)

    def closeEvent(self, event):
        # When the app is closing, wait for any running docker commands to finish,
        # then run dkill() to cleanup Docker and exit.
        if self.run_processes:
            while self.run_processes:
                QThreadPool.globalInstance().waitForDone(100)
        dkill()
        event.accept()

    def require_authentication(self):
        token = self.get_docker_token()
        if token is None:
            QMessageBox.warning(self, "Authentication Required", "Please enter your Docker Hub password.")
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

        tab_mgmt_layout = QHBoxLayout()
        add_tab_btn = QPushButton("Add Tab")
        add_tab_btn.clicked.connect(lambda: self.require_authentication() and self.add_tab())
        tab_mgmt_layout.addWidget(add_tab_btn)
        rename_tab_btn = QPushButton("Rename Tab")
        rename_tab_btn.clicked.connect(lambda: self.require_authentication() and self.rename_tab())
        tab_mgmt_layout.addWidget(rename_tab_btn)
        delete_tab_btn = QPushButton("Delete Tab")
        delete_tab_btn.clicked.connect(lambda: self.require_authentication() and self.delete_tab())
        tab_mgmt_layout.addWidget(delete_tab_btn)
        main_layout.addLayout(tab_mgmt_layout)

        self.tab_nav = TabNavigationWidget(self.tabs_config, parent=self)
        main_layout.addWidget(self.tab_nav)

        control_layout = QHBoxLayout()
        control_layout.setSpacing(10)

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
        control_layout.addWidget(self.search_box)

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
        delete_tag_button.clicked.connect(lambda: self.require_authentication() and self.open_delete_dialog())
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
        move_tags_button.clicked.connect(lambda: self.require_authentication() and self.open_bulk_move_dialog())
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
        bulk_paste_button.clicked.connect(lambda: self.require_authentication() and self.open_bulk_paste_move_dialog())
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
        save_txt_button.clicked.connect(lambda: self.require_authentication() and self.save_as_txt())
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
        for tag in self.all_tags:
            if tag["alias"] in self.game_times_cache:
                time_line = f"Approx Time: {self.game_times_cache[tag['alias']]}"
            else:
                time_line = "Approx Time: Loading..."
            text_lines = [tag["alias"], f"({self.format_size(tag['full_size'])})", time_line]
            display_text = "\n".join(text_lines)
            button = GameButton(display_text)
            button.tag_info = tag
            button.setIconSize(QSize(64, 64))
            self.tag_buttons.setdefault(tag["docker_name"], []).append(button)
            self.buttons.append(button)
            cat = tag.get("category", "all")
            container = self.tab_pages.get(cat, self.tab_pages.get("all"))
            row, col = positions.get(cat, [0, 0])
            container.layout.addWidget(button, row, col)
            col += 1
            if col >= 4:
                col = 0
                row += 1
            positions[cat] = [row, col]
            alias = tag["alias"]
            if alias in self.image_cache:
                button.setIcon(QIcon(self.image_cache[alias]))
            elif alias not in getattr(self, "started_image_queries", set()):
                worker = Worker(fetch_image, alias)
                worker.signals.finished.connect(lambda result, a=alias: self.handle_image_update(a, result[1]))
                self.add_worker(worker)
                QThreadPool.globalInstance().start(worker)
                if not hasattr(self, "started_image_queries"):
                    self.started_image_queries = set()
                self.started_image_queries.add(alias)

    def start_game_time_queries(self):
        for tag in self.all_tags:
            alias = tag["alias"]
            if alias not in self.game_times_cache:
                worker = Worker(fetch_game_time, alias)
                worker.signals.finished.connect(lambda result, a=alias: self.handle_game_time_update(a, result[1]))
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
        def parse_time(time_str):
            try:
                return float(time_str.split()[0])
            except:
                return 0.0
        self.all_tags.sort(key=lambda x: parse_time(self.game_times_cache.get(x["alias"], "")), reverse=descending)
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

    def run_selected_commands(self):
        if not check_docker_engine():
            QMessageBox.warning(self, "Docker Engine Not Running",
                                "Docker Desktop Engine is not running. Please start Docker Desktop and try again.")
            return
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
                f'-v "C:\\games":/games '
                f'-e DISPLAY=$DISPLAY '
                f'-v /tmp/.X11-unix:/tmp/.X11-unix '
                f'--name "{tag}" '
                f'michadockermisha/backup:"{tag}" '
                f'sh -c "apk add rsync && mkdir -p /games/{tag} && rsync -aP /home/ /games/{tag}"'
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
        if not self.require_authentication():
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
        if self.docker_token is not None:
            return self.docker_token
        password, ok = QInputDialog.getText(self, "Docker Hub Authentication",
                                            "Enter Docker Hub password:", QLineEdit.Password)
        if not (ok and password):
            return None
        username = "michadockermisha"
        login_url = "https://hub.docker.com/v2/users/login/"
        login_data = {"username": username, "password": password}
        login_response = requests.post(login_url, json=login_data)
        if login_response.status_code == 200 and login_response.json().get("token"):
            self.docker_token = login_response.json().get("token")
            return self.docker_token
        else:
            QMessageBox.warning(self, "Authentication Failed", "Incorrect Docker Hub password.")
            return None

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
    QThreadPool.globalInstance().setMaxThreadCount(10)
    docker_app = DockerApp()
    docker_app.show()
    sys.exit(app.exec_())

