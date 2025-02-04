import sys
import os
import json
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QHBoxLayout, 
                           QVBoxLayout, QScrollArea, QLineEdit, QGridLayout, 
                           QDesktopWidget, QLabel, QFrame)
from PyQt5.QtGui import QColor, QFont, QPalette
from PyQt5.QtCore import Qt
import subprocess

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

class GameButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
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
            QPushButton:hover {
                background-color: #34495E;
                border: 2px solid #3498DB;
            }
            QPushButton:pressed {
                background-color: #2980B9;
            }
        """)

class DockerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.load_games_data()
        self.setWindowTitle("Game Launcher")
        
        desktop_geometry = QDesktopWidget().screenGeometry()
        width = int(desktop_geometry.width() * 19 / 20)
        height = int(desktop_geometry.height() * 19 / 20)
        self.setGeometry(0, 0, width, height)
        
        # Set dark theme
        self.setStyleSheet("""
            QWidget {
                background-color: #1E1E1E;
                color: white;
            }
            QScrollArea {
                border: none;
                background-color: #1E1E1E;
            }
            QScrollBar:vertical {
                border: none;
                background: #2C2C2C;
                width: 14px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #3E3E3E;
                min-height: 20px;
                border-radius: 7px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
        """)
        
        self.init_ui()

    def load_games_data(self):
        try:
            with open('games_data.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
                self.all_games = data.get('all_games', [])
                self.game_categories = data.get('category_games', {})
        except FileNotFoundError:
            print("Error: games_data.json not found")
            self.all_games = []
            self.game_categories = {}
        except json.JSONDecodeError:
            print("Error: Invalid JSON format in games_data.json")
            self.all_games = []
            self.game_categories = {}

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Title
        title = QLabel("Game Launcher")
        title.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                font-weight: bold;
                padding: 10px;
            }
        """)
        main_layout.addWidget(title, alignment=Qt.AlignCenter)

        # Category buttons container
        category_container = QFrame()
        category_container.setStyleSheet("""
            QFrame {
                background-color: #252525;
                border-radius: 10px;
                padding: 10px;
            }
        """)
        button_layout = QHBoxLayout(category_container)
        button_layout.setSpacing(10)

        # Category buttons with new colors
        self.category_buttons = {
            'interactive': ('Interactive', '#E74C3C'),  # Red
            'mouse': ('Mouse', '#2ECC71'),             # Green
            'platform': ('Platform', '#3498DB'),       # Blue
            'shooter': ('Shooter', '#9B59B6'),         # Purple
            'chill': ('Chill', '#F1C40F'),            # Yellow
            'action': ('Action', '#E67E22')           # Orange
        }

        for category, (label, color) in self.category_buttons.items():
            button = StyledButton(label, color)
            button.clicked.connect(self.update_games)
            button.category = category
            button_layout.addWidget(button)

        main_layout.addWidget(category_container)

        # Search box with modern styling
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search games...")
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
        main_layout.addWidget(self.search_box)

        # Games grid container
        games_container = QFrame()
        games_container.setStyleSheet("""
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

        self.game_layout = QGridLayout(scroll_widget)
        self.game_layout.setSpacing(10)
        self.create_game_buttons()

        games_container.setLayout(QVBoxLayout())
        games_container.layout().addWidget(scroll_area)
        main_layout.addWidget(games_container)

    def create_game_buttons(self):
        for i in reversed(range(self.game_layout.count())): 
            self.game_layout.itemAt(i).widget().setParent(None)
        
        self.buttons = []
        row, col = 0, 0
        
        for game in self.all_games:
            button = GameButton(game)
            button.clicked.connect(lambda checked, g=game: self.run_docker_command(g))
            
            self.game_layout.addWidget(button, row, col)
            col += 1
            if col == 4:
                col = 0
                row += 1
            
            self.buttons.append(button)

    def run_docker_command(self, image_name):
        # Convert to lowercase only for the docker command, preserve original name for display
        formatted_image_name = image_name.lower().replace(" ", "").replace(":", "")
        wsl_command = "wsl -d kali-linux"
        docker_command = f'docker run -v /mnt/c/games/{formatted_image_name}:/c/games/{formatted_image_name} -it -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix --name {formatted_image_name} michadockermisha/backup:{formatted_image_name} sh -c "apk add rsync && rsync -aP /home /c/games && mv /c/games/home /c/games/{formatted_image_name}"'
        full_command = f"{wsl_command} && {docker_command}"
        subprocess.Popen(full_command, shell=True)

    def filter_buttons(self, text):
        for button in self.buttons:
            button.setVisible(text.lower() in button.text().lower())

    def update_games(self):
        sender_button = self.sender()
        category = sender_button.category
        specified_titles = self.game_categories.get(category, [])
        
        for button in self.buttons:
            # Case-insensitive comparison
            button_game = button.text().lower().replace(" ", "")
            category_games = [title.lower().replace(" ", "") for title in specified_titles]
            button.setVisible(button_game in category_games)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # Set application-wide font
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    docker_app = DockerApp()
    docker_app.show()
    sys.exit(app.exec_())
