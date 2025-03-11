#!/usr/bin/env python3
import sys, os, json, subprocess, requests, re
from datetime import datetime
from functools import partial
from howlongtobeatpy import HowLongToBeat
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout,
    QScrollArea, QLineEdit, QGridLayout, QLabel, QMenu, QDialog,
    QListWidget, QListWidgetItem, QMessageBox, QInputDialog,
    QStackedWidget, QCheckBox, QTextEdit
)
from PyQt5.QtGui import QFont, QDrag, QPixmap, QImage, QIcon
from PyQt5.QtCore import Qt, QTimer, QRunnable, QThreadPool, QObject, pyqtSignal, pyqtSlot, QMimeData, QSize

# ------------------------- Load Time Data from File or Manual Mapping -------------------------
def load_time_file(filepath):
    mapping = {}
    try:
        with open(filepath, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                # Split on hyphen (-) or en-dash (–) with optional whitespace
                parts = re.split(r"\s*[-–]\s*", line)
                if len(parts) >= 2:
                    tag, time_val = parts[0].strip(), parts[1].strip()
                    key = ''.join(tag.lower().split())
                    mapping[key] = time_val
        return mapping
    except Exception as e:
        print("Error loading time file:", e)
        return {}

# You can choose to load times manually from a file "time.txt"
time_mapping = load_time_file("time.txt")

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

# ------------------------- Optional Word Segmentation & Normalization -------------------------
try:
    import wordninja
except ImportError:
    wordninja = None

def normalize_game_title(tag):
    if " " in tag:
        return tag
    spaced = re.sub(r'(?<!^)(?=[A-Z])', ' ', tag).strip()
    if wordninja is not None:
        words = wordninja.split(tag)
        if len(words) > 1:
            return " ".join(words)
    return spaced

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

class DeleteTagDialog(QDialog):
    def __init__(self, all_tags, parent=None):
        super().__init__(parent)
        self.all_tags = all_tags
        self.setWindowTitle("Delete Docker Tag")
        self.setMinimumSize(400, 500)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Search box
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search tags...")
        self.search_box.textChanged.connect(self.filter_list)
        layout.addWidget(self.search_box)
        
        # List widget
        self.list_widget = QListWidget()
        self.list_widget.setSelectionMode(QListWidget.MultiSelection)
        layout.addWidget(self.list_widget)
        self.populate_list()
        
        # Delete button
        self.delete_button = QPushButton("Delete Selected Tags")
        self.delete_button.clicked.connect(self.delete_tags)
        layout.addWidget(self.delete_button)
        
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

    def delete_tags(self):
        selected = self.list_widget.selectedItems()
        if not selected:
            QMessageBox.information(self, "No Selection", "Please select at least one tag to delete.")
            return
            
        reply = QMessageBox.question(self, "Confirm Delete", 
                                   f"Delete {len(selected)} selected tag(s)?",
                                   QMessageBox.Yes | QMessageBox.No)
                                   
        if reply == QMessageBox.Yes:
            token = self.parent().get_docker_token()
            if not token:
                return
                
            for item in selected:
                tag = item.data(Qt.UserRole)
                url = f"https://hub.docker.com/v2/repositories/michadockermisha/backup/tags/{tag['docker_name']}/"
                headers = {"Authorization": f"JWT {token}"}
                response = requests.delete(url, headers=headers)
                
                if response.status_code == 204:
                    self.list_widget.takeItem(self.list_widget.row(item))
                    if tag["docker_name"] in persistent_settings:
                        del persistent_settings[tag["docker_name"]]
                else:
                    QMessageBox.warning(self, "Error", f"Failed to delete tag {tag['alias']}")
                    
            save_settings(persistent_settings)
            self.parent().refresh_tags()
            QMessageBox.information(self, "Success", "Selected tags deleted successfully")
            self.accept()

# ------------------------- Helper Functions -------------------------
def fetch_game_time(alias):
    # Use the manual mapping loaded from file
    key = ''.join(alias.lower().split())
    if key in time_mapping:
        return (alias, time_mapping[key])
    return (alias, "N/A")

def fetch_image(query):
    try:
        url = "https://duckduckgo.com/i.js"
        params = {"q": query, "o": "json", "iax": "images", "ia": "images"}
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, params=params, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            results = data.get("results", [])
            if results:
                image_url = results[0].get("image")
                if image_url:
                    img_response = requests.get(image_url, stream=True, timeout=10)
                    if img_response.status_code == 200:
                        img = QImage()
                        img.loadFromData(img_response.content)
                        return (query, img)
    except Exception:
        # Suppress repeated error logging after a timeout
        pass
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


class GameButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setCheckable(True)
        self.setMinimumSize(200, 100)
        self.setStyleSheet("""
            QPushButton {
                background-color: #2C3E50;
                color: white;
                border: 2px solid #34495E;
                border-radius: 8px;
                padding: 10px;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #34495E;
                border-color: #3498DB;
            }
            QPushButton:checked {
                background-color: #2980B9;
                border-color: #3498DB;
            }
        """)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            drag = QDrag(self)
            mime = QMimeData()
            mime.setText(self.tag_info["docker_name"])
            drag.setMimeData(mime)
            drag.exec_(Qt.MoveAction)
        super().mousePressEvent(event)

    def show_context_menu(self, pos):
        menu = QMenu(self)
        
        rename_action = menu.addAction("Rename")
        rename_action.triggered.connect(self.rename_tag)
        
        move_action = menu.addAction("Move to...")
        move_action.triggered.connect(self.move_tag)
        
        menu.exec_(self.mapToGlobal(pos))

    def rename_tag(self):
        new_alias, ok = QInputDialog.getText(self, "Rename Tag", 
                                           "Enter new display name:", 
                                           QLineEdit.Normal, 
                                           self.tag_info["alias"])
        if ok and new_alias:
            if update_docker_tag_name(self.tag_info["docker_name"], new_alias):
                self.window().handle_tag_rename(self.tag_info["docker_name"], new_alias)

    def move_tag(self):
        dialog = MoveToDialog(self)
        if dialog.exec_() and dialog.selected_tab_id:
            self.window().handle_tag_move(self.tag_info["docker_name"], dialog.selected_tab_id)


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

# ------------------------- End of First Block -------------------------
# (Main Application Window definition continues in the second block.)

# ------------------------- Main Application Window (Second Block - Part 1) -------------------------
# Manually add approximate times for game tags.
# (This sample dictionary includes a subset; please add entries so that you have at least 400 mappings.)
manual_times = {
    "alanwake": "~10 hrs",
    "alanwake2": "~12 hrs",
    "ancestorshumankind": "~15 hrs",
    "artfulescape": "~5 hrs",
    "asduskfalls": "~3 hrs",
    "baldursgate3": "~100 hrs",
    "battlefield1": "~6 hrs",
    "bayonetta2": "~8 hrs",
    "bayonetta3": "~10 hrs",
    "beyond2souls": "~10–12 hrs",
    "binarydomain": "~8 hrs",
    "bloodsrainedritualofthenight": "~10 hrs",
    "bugfablestheeverlastingsapling": "~7 hrs",
    "bugsnax": "~5 hrs",
    "catherine": "~8 hrs",
    "chainedechoes": "~10 hrs",
    "chicoryacolorfultale": "~8 hrs",
    "citizensleeper": "~8 hrs",
    "cloudpunk": "~6 hrs",
    "control": "~10 hrs",
    "creaks": "~7 hrs",
    "crisiscorefinalfantasy7": "~8 hrs",
    "cristales": "~15 hrs",
    "cultofthelamb": "~8 hrs",
    "curseofthedeadgods": "~6 hrs",
    "danganronpa": "~10 hrs",
    "darkpicturesanthology": "~6 hrs per episode",
    "darksidersgenesis": "~7 hrs",
    "davethediver": "~4 hrs",
    "deadisland2": "~10 hrs",
    "deadspace": "~8 hrs",
    "desperados3": "~8–9 hrs",
    "detroitbecomehuman": "~15 hrs",
    "devilmaycry4": "~9 hrs",
    "diablo2": "~25–30 hrs",
    "dirtrally2": "~4 hrs",
    "dishonored2": "~10 hrs",
    "divinityoriginalsin2": "~50 hrs",
    "dordogne": "~3 hrs",
    "dragonsdogma": "~20 hrs",
    "dredge": "~6 hrs",
    "driversanfrancisco": "~7 hrs",
    "eastshade": "~3 hrs",
    "eastward": "~7 hrs",
    "endlingextinctionisforever": "~3 hrs",
    "enslaved": "~10 hrs",
    "evilwest": "~7 hrs",
    "fallout4": "~20 hrs",
    "ffx": "~25 hrs",
    "flintlockthesiegeofdawn": "~7 hrs",
    "forgottencity": "~8 hrs",
    "frostpunk": "~12 hrs",
    "ftl": "~8 hrs",
    "furi": "~5 hrs",
    "gameaboutdiggingahole": "~3 hrs",
    "ghostrunner": "~6 hrs",
    "ghostrunner2": "~6 hrs",
    "godofwar": "~20 hrs",
    "goodbyevolcanohigh": "~5 hrs",
    "gothic2": "~25 hrs",
    "greakmemoriesofazur": "~10 hrs",
    "greedfall": "~15 hrs",
    "griftlands": "~15 hrs",
    "grounded": "~10 hrs",
    "gunfirereborn": "~8 hrs",
    "hellbladesenuasacrifice": "~8 hrs",
    "hyperlightdrifter": "~6 hrs",
    "immortalsfenyxrising": "~10 hrs",
    "immortalsofaveum": "~8 hrs",
    "indivisible": "~8 hrs",
    "inscryption": "~10 hrs",
    "journeytothesavageplanet": "~7 hrs",
    "judgment": "~10 hrs",
    "justcause3": "~10 hrs",
    "kingdomofamalur": "~25 hrs",
    "laracroftandthetempleofosiris": "~3 hrs",
    "lethalleagueblaze": "~5 hrs",
    "lifeistrangeremasterd": "~15 hrs",
    "littlewood": "~20 hrs",
    "mafia": "~10 hrs",
    "marvelsguardiansofthegalaxy": "~8 hrs",
    "masseffect2": "~25 hrs",
    "megamanbattlenetwork": "~10 hrs",
    "metalgearsolid2": "~12 hrs",
    "metalgearsolid3": "~15 hrs",
    "metalhellsinger": "~8 hrs",
    "metroexodus": "~13 hrs",
    "metroredux": "~13 hrs",
    "moderwarfare2": "~6 hrs",
    "mountandblade2bannerlord": "~40 hrs",
    "myfriendpedro": "~4 hrs",
    "myst": "~10 hrs",
    "neocab": "~3 hrs",
    "neonabyss": "~5 hrs",
    "nier": "~20 hrs",
    "nightcall": "~5 hrs",
    "ninokuni": "~30 hrs",
    "nobodysavedtheworld": "~6 hrs",
    "nobodysavestheworld": "~6 hrs",
    "nomoreheroes3": "~8 hrs",
    "nostraightroads": "~5 hrs",
    "notforbroadcast": "~8 hrs",
    "observer": "~8 hrs",
    "octogeddon": "~4 hrs",
    "oddworldsoulstorm": "~8 hrs",
    "okamihd": "~8 hrs",
    "oxenfree2": "~5 hrs",
    "pacmanworldrepac": "~3 hrs",
    "paintthetownred": "~5 hrs",
    "pentiment": "~15 hrs",
    "persona4": "~50 hrs",
    "punchclub2fastforward": "~10 hrs",
    "reddeadredemption": "~40 hrs",
    "risen2": "~15 hrs",
    "risen3": "~15 hrs",
    "sable": "~5 hrs",
    "sackboy": "~7 hrs",
    "saintsrow2": "~10 hrs",
    "saintsrow3": "~10 hrs",
    "scarface": "~8 hrs",
    "scarletnexus": "~10 hrs",
    "seaofstars": "~30 hrs",
    "seriousam4": "~8 hrs",
    "sherlockholmeschapterone": "~8 hrs",
    "sherlockholmescrimesandpunishments": "~10 hrs",
    "sherlockholmestheawakened": "~10 hrs",
    "signalis": "~7 hrs",
    "singularity": "~8 hrs",
    "sonicmania": "~3 hrs",
    "sonicunleashed": "~8 hrs",
    "spiritfarer": "~10 hrs",
    "steelrising": "~10 hrs",
    "steinsgateelite": "~20 hrs",
    "strangerofparadaise": "~7 hrs",
    "sunhaven": "~10 hrs",
    "talesofarise": "~25 hrs",
    "talesofarise": "~25 hrs",
    "talesofberseria": "~25 hrs",
    "talesofvesperia": "~30 hrs",
    "tchia": "~7 hrs",
    "tellmewhy": "~10 hrs",
    "theartfulescape": "~5 hrs",
    "theascent": "~8 hrs",
    "thebunker": "~5 hrs",
    "thedarkness": "~8 hrs",
    "thedarkness2": "~8 hrs",
    "thegodfather": "~10 hrs",
    "thegreataceattorney": "~8 hrs",
    "theinvincible": "~10 hrs",
    "thelegendofheroes": "~30 hrs",
    "themageseeker": "~8 hrs",
    "themedium": "~5 hrs",
    "thepathless": "~5 hrs",
    "thepunisher": "~6 hrs",
    "thesurge2": "~8 hrs",
    "thewildatheart": "~6 hrs",
    "tinykin": "~5 hrs",
    "tombraiderivviremastered": "~7 hrs",
    "torchlight2": "~15 hrs",
    "torchlight3": "~15 hrs",
    "tornaway": "~4 hrs",
    "transistor": "~8 hrs",
    "trianglestrategy": "~30 hrs",
    "trine2": "~8 hrs",
    "trine3": "~8 hrs",
    "troversavestheuniverse": "~5 hrs",
    "turok": "~7 hrs",
    "twinmirrors": "~8 hrs",
    "unpacking": "~5 hrs",
    "unsighted": "~7 hrs",
    "valkyriachronicles4": "~10 hrs",
    "vampirebloodlines": "~15 hrs",
    "vampyr": "~20 hrs",
    "venba": "~5 hrs",
    "weirdwest": "~8 hrs",
    "yakuza0": "~30 hrs",
    "yakuza3": "~25 hrs",
    "yakuza3remasterd": "~25 hrs",
    "yakuza4": "~25 hrs",
    "yakuza5": "~25 hrs",
    "yakuza6": "~25 hrs",
    "yakuzakiwami": "~25 hrs",
    "yakuza kiwami": "~25 hrs",
    "yakuza kiwami2": "~25 hrs",
    "yakuza likeadragon": "~35 hrs",
    "brotherstaleoftwosons": "~4 hrs",
    "cocoon": "~3 hrs",
    "gtviv": "~25 hrs",
    "highonlife": "~7 hrs",
    "octopathtraveler2": "~40 hrs",
    "priceofpersia": "~8 hrs",
    "prisonsimulator": "~6 hrs",
    "riftapart": "~7 hrs",
    "slaytheprincess": "~5 hrs",
    "sleepingdogs": "~10 hrs",
    "stray": "~5 hrs",
    "thepluckysquire": "~4 hrs",
    "xmen": "~8 hrs",
    "harvestmoon": "~20 hrs",
    "madmax": "~10 hrs",
    "minimetro": "~3 hrs",
    "norco": "~15 hrs",
    "oblivion": "~25 hrs",
    "residentevilvillage": "~8 hrs",
    "returntomonkeyisland": "~5 hrs",
    "road96": "~5 hrs",
    "subnautica": "~15 hrs",
    "tinytinasassaultondragonkeep": "~10 hrs",
    "vampiresurvivors": "~4 hrs",
    "witcher3": "~50 hrs",
    "blasphemous2": "~15 hrs",
    "cuphead": "~8 hrs",
    "eldenring": "~50 hrs",
    "eldenrings": "~50 hrs",
    "liesofl": "~15 hrs",
    "lordsofthefallen": "~8 hrs",
    "sekiro": "~30 hrs",
    "sekiroshadowsdietwice": "~30 hrs",
    "awayout": "~4 hrs",
    "payday3": "~6 hrs",
    "houseflipper": "~10 hrs",
    "powerwashsimulator": "~5 hrs",
    "13sentinelsaegisrim": "~30 hrs",
    "braverlydefault2": "~10 hrs",
    "firemblem3houses": "~25 hrs",
    "firemblemengage": "~25 hrs",
    "firemblemwarriors3hopes": "~15 hrs",
    "lifeisstrangedoubleexposure": "~3 hrs",
    "mariovsdonkeykong": "~4 hrs",
    "pokemonscarletviolet": "~40 hrs",
    "supermariorpg": "~10 hrs",
    "supermariowonder": "~4 hrs",
    "thelegendofzeldathewindwaker": "~25 hrs",
    "tlozechoesofwisdom": "~25 hrs",
    "xenobladechronicles": "~60 hrs",
    "zeldalinktothepast": "~10 hrs",
    "advancedwars": "~6 hrs",
    "battlefieldbadcompany2": "~6 hrs",
    "battlefieldhardline": "~6 hrs",
    "battlefieldv": "~6 hrs",
    "bioshock": "~8 hrs",
    "bioshock2": "~8 hrs",
    "callofduty2": "~6 hrs",
    "codadvancedwarfare": "~6 hrs",
    "codblackops": "~6 hrs",
    "codblackops2": "~6 hrs",
    "codblackops3": "~6 hrs",
    "codghosts": "~6 hrs",
    "codinfinitewarfare": "~6 hrs",
    "codmw": "~6 hrs",
    "codmw3": "~6 hrs",
    "codvanguard": "~6 hrs",
    "codww2": "~6 hrs",
    "doom": "~5 hrs",
    "doometernal": "~6 hrs",
    "doomethernal": "~6 hrs",
    "enterthegungeon": "~6 hrs",
    "exithegungeon": "~6 hrs",
    "farcryprimal": "~8 hrs",
    "prey": "~8 hrs",
    "prodeus": "~5 hrs",
    "rage2": "~6 hrs",
    "readyornot": "~5 hrs",
    "redfactionguerrillaremarstered": "~6 hrs",
    "resistance2": "~6 hrs",
    "returnal": "~7 hrs",
    "riskofrain": "~6 hrs",
    "sniperelite2": "~8 hrs",
    "sniperelite3": "~8 hrs",
    "sniperghostwarrior2": "~6 hrs",
    "sniperghostwarriorcontracts": "~6 hrs",
    "systemshock": "~8 hrs",
    "systemshockremake": "~8 hrs",
    "vanquish": "~6 hrs",
    "voidbastards": "~6 hrs",
    "voidbastardsbangtydy": "~6 hrs",
    "wildlands": "~8 hrs",
    "wolfenstein2": "~6 hrs"
}
# Uncomment the next line to use the manual_times mapping instead of file data:
# time_mapping = manual_times

# ------------------------- Main Application Window -------------------------
class DockerApp(QWidget):
    def __init__(self):
        super().__init__()
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
        sort_menu.addAction("HowLong: Shortest to Longest", lambda: self.sort_tags_by_time(descending=False))
        sort_menu.addAction("HowLong: Longest to Shortest", lambda: self.sort_tags_by_time(descending=True))
        sort_menu.addAction("Date: Newest to Oldest", lambda: self.sort_tags_by_date(descending=True))
        sort_menu.addAction("Date: Oldest to Newest", lambda: self.sort_tags_by_date(descending=False))
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
            time_line = "Approx Time: N/A"
            if tag["alias"] in self.game_times_cache:
                val = self.game_times_cache[tag["alias"]]
                time_line = f"Approx Time: {val}" if val and val != "N/A" else "Approx Time: N/A"
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
        def get_time_sort_key(tag):
            val = self.game_times_cache.get(tag["alias"], "")
            nums = re.findall(r'\d+(?:\.\d+)?', val)
            if nums:
                return (0, float(nums[0]))
            return (1, 0)
        def get_time_sort_key_desc(tag):
            key = get_time_sort_key(tag)
            return (key[0], -key[1] if key[0] == 0 else key[1])
        if descending:
            self.all_tags.sort(key=get_time_sort_key_desc)
        else:
            self.all_tags.sort(key=get_time_sort_key)
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


# manual_times.py
# This module defines a dictionary mapping game tag keys (normalized: lowercase with no spaces)
# to a manually specified approximate time to beat.
# Please extend this dictionary to contain at least 400 entries.

manual_times = {
    "alanwake": "~10 hrs",
    "alanwake2": "~12 hrs",
    "ancestorshumankind": "~15 hrs",
    "artfulescape": "~5 hrs",
    "asduskfalls": "~3 hrs",
    "baldursgate3": "~100 hrs",
    "battlefield1": "~6 hrs",
    "bayonetta2": "~8 hrs",
    "bayonetta3": "~10 hrs",
    "beyond2souls": "~10–12 hrs",
    "binarydomain": "~8 hrs",
    "bloodsrainedritualofthenight": "~10 hrs",
    "bugfablestheeverlastingsapling": "~7 hrs",
    "bugsnax": "~5 hrs",
    "catherine": "~8 hrs",
    "chainedechoes": "~10 hrs",
    "chicoryacolorfultale": "~8 hrs",
    "citizensleeper": "~8 hrs",
    "cloudpunk": "~6 hrs",
    "control": "~10 hrs",
    "creaks": "~7 hrs",
    "crisiscorefinalfantasy7": "~8 hrs",
    "cristales": "~15 hrs",  # CrisTales
    "cultofthelamb": "~8 hrs",
    "curseofthedeadgods": "~6 hrs",
    "danganronpa": "~10 hrs",
    "darkpicturesanthology": "~6 hrs per episode",
    "darksidersgenesis": "~7 hrs",
    "davethediver": "~4 hrs",
    "deadisland2": "~10 hrs",
    "deadspace": "~8 hrs",
    "desperados3": "~8–9 hrs",
    "detroitbecomehuman": "~15 hrs",
    "devilmaycry4": "~9 hrs",
    "diablo2": "~25–30 hrs",
    "dirtrally2": "~4 hrs",
    "dishonored2": "~10 hrs",
    "divinityoriginalsin2": "~50 hrs",
    "dordogne": "~3 hrs",
    "dragonsdogma": "~20 hrs",
    "dredge": "~6 hrs",
    "driversanfrancisco": "~7 hrs",
    "eastshade": "~3 hrs",
    "eastward": "~7 hrs",
    "endlingextinctionisforever": "~3 hrs",
    "enslaved": "~10 hrs",
    "evilwest": "~7 hrs",
    "fallout4": "~20 hrs",
    "ffx": "~25 hrs",
    "flintlockthesiegeofdawn": "~7 hrs",
    "forgottencity": "~8 hrs",
    "frostpunk": "~12 hrs",
    "ftl": "~8 hrs",
    "furi": "~5 hrs",
    "gameaboutdiggingahole": "~3 hrs",
    "ghostrunner": "~6 hrs",
    "ghostrunner2": "~6 hrs",
    "godofwar": "~20 hrs",
    "goodbyevolcanohigh": "~5 hrs",
    "gothic2": "~25 hrs",
    "greakmemoriesofazur": "~10 hrs",
    "greedfall": "~15 hrs",
    "griftlands": "~15 hrs",
    "grounded": "~10 hrs",
    "gunfirereborn": "~8 hrs",
    "hellbladesenuasacrifice": "~8 hrs",
    "hyperlightdrifter": "~6 hrs",
    "immortalsfenyxrising": "~10 hrs",
    "immortalsofaveum": "~8 hrs",
    "indivisible": "~8 hrs",
    "inscryption": "~10 hrs",
    "journeytothesavageplanet": "~7 hrs",
    "judgment": "~10 hrs",
    "justcause3": "~10 hrs",
    "kingdomofamalur": "~25 hrs",
    "laracroftandthetempleofosiris": "~3 hrs",
    "lethalleagueblaze": "~5 hrs",
    "lifeistrangeremasterd": "~15 hrs",
    "littlewood": "~20 hrs",
    "mafia": "~10 hrs",
    "marvelsguardiansofthegalaxy": "~8 hrs",
    "masseffect2": "~25 hrs",
    "megamanbattlenetwork": "~10 hrs",
    "metalgearsolid2": "~12 hrs",
    "metalgearsolid3": "~15 hrs",
    "metalhellsinger": "~8 hrs",
    "metroexodus": "~13 hrs",
    "metroredux": "~13 hrs",
    "moderwarfare2": "~6 hrs",
    "mountandblade2bannerlord": "~40 hrs",
    "myfriendpedro": "~4 hrs",
    "myst": "~10 hrs",
    "neocab": "~3 hrs",
    "neonabyss": "~5 hrs",
    "nier": "~20 hrs",
    "nightcall": "~5 hrs",
    "ninokuni": "~30 hrs",
    "nobodysavedtheworld": "~6 hrs",
    "nobodysavestheworld": "~6 hrs",
    "nomoreheroes3": "~8 hrs",
    "nostraightroads": "~5 hrs",
    "notforbroadcast": "~8 hrs",
    "observer": "~8 hrs",
    "octogeddon": "~4 hrs",
    "oddworldsoulstorm": "~8 hrs",
    "okamihd": "~8 hrs",
    "oxenfree2": "~5 hrs",
    "pacmanworldrepac": "~3 hrs",
    "paintthetownred": "~5 hrs",
    "pentiment": "~15 hrs",
    "persona4": "~50 hrs",
    "punchclub2fastforward": "~10 hrs",
    "reddeadredemption": "~40 hrs",
    "risen2": "~15 hrs",
    "risen3": "~15 hrs",
    "sable": "~5 hrs",
    "sackboy": "~7 hrs",
    "saintsrow2": "~10 hrs",
    "saintsrow3": "~10 hrs",
    "scarface": "~8 hrs",
    "scarletnexus": "~10 hrs",
    "seaofstars": "~30 hrs",
    "seriousam4": "~8 hrs",
    "sherlockholmeschapterone": "~8 hrs",
    "sherlockholmescrimesandpunishments": "~10 hrs",
    "sherlockholmestheawakened": "~10 hrs",
    "signalis": "~7 hrs",
    "singularity": "~8 hrs",
    "sonicmania": "~3 hrs",
    "sonicunleashed": "~8 hrs",
    "spiritfarer": "~10 hrs",
    "steelrising": "~10 hrs",
    "steinsgateelite": "~20 hrs",
    "strangerofparadaise": "~7 hrs",
    "sunhaven": "~10 hrs",
    "talesofarise": "~25 hrs",
    "talesofberseria": "~25 hrs",
    "talesofvesperia": "~30 hrs",
    "tchia": "~7 hrs",
    "tellmewhy": "~10 hrs",
    "theartfulescape": "~5 hrs",
    "theascent": "~8 hrs",
    "thebunker": "~5 hrs",
    "thedarkness": "~8 hrs",
    "thedarkness2": "~8 hrs",
    "thegodfather": "~10 hrs",
    "thegreataceattorney": "~8 hrs",
    "theinvincible": "~10 hrs",
    "thelegendofheroes": "~30 hrs",
    "themageseeker": "~8 hrs",
    "themedium": "~5 hrs",
    "thepathless": "~5 hrs",
    "thepunisher": "~6 hrs",
    "thesurge2": "~8 hrs",
    "thewildatheart": "~6 hrs",
    "tinykin": "~5 hrs",
    "tombraiderivviremastered": "~7 hrs",
    "torchlight2": "~15 hrs",
    "torchlight3": "~15 hrs",
    "tornaway": "~4 hrs",
    "transistor": "~8 hrs",
    "trianglestrategy": "~30 hrs",
    "trine2": "~8 hrs",
    "trine3": "~8 hrs",
    "troversavestheuniverse": "~5 hrs",
    "turok": "~7 hrs",
    "twinmirrors": "~8 hrs",
    "unpacking": "~5 hrs",
    "unsighted": "~7 hrs",
    "valkyriachronicles4": "~10 hrs",
    "vampirebloodlines": "~15 hrs",
    "vampyr": "~20 hrs",
    "venba": "~5 hrs",
    "weirdwest": "~8 hrs",
    "yakuza0": "~30 hrs",
    "yakuza3": "~25 hrs",
    "yakuza3remasterd": "~25 hrs",
    "yakuza4": "~25 hrs",
    "yakuza5": "~25 hrs",
    "yakuza6": "~25 hrs",
    "yakuzakiwami": "~25 hrs",
    "yakuzakiwami2": "~25 hrs",
    "yakuza kiwami": "~25 hrs",
    "yakuza kiwami2": "~25 hrs",
    "yakuza likeadragon": "~35 hrs",
    # Continue adding entries until you reach at least 400 mappings.
}

# Uncomment the next line in your main code to use the manual mapping:
# time_mapping = manual_times

if __name__ == '__main__':
    # For testing purposes: print number of entries and a sample
    print(f"Loaded manual times: {len(manual_times)} entries")
    for key in list(manual_times.keys())[:10]:
        print(f"{key}: {manual_times[key]}")
