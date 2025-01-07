import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QScrollArea, QLineEdit, QGridLayout, QDesktopWidget
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt
import subprocess

class DockerApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Docker Commands")

        # Set the window size to *** of the screen
        desktop_geometry = QDesktopWidget().screenGeometry()
        width = int(desktop_geometry.width() * 19 / 20)
        height = int(desktop_geometry.height() * 19 / 20)
        self.setGeometry(0, 0, width, height)

        self.setStyleSheet("background-color: black; font: 10pt bold; color: black;")

        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)

        # Create a horizontal layout for the buttons
        button_layout = QHBoxLayout()

        # Add interactive button
        self.interactive_button = QPushButton("Interactive", self)
        self.interactive_button.setStyleSheet("font-size: 14pt; background-color: red; color: black;")
        self.interactive_button.clicked.connect(self.update_games)
        button_layout.addWidget(self.interactive_button)

        # Add mouse button
        self.mouse_button = QPushButton("mouse", self)
        self.mouse_button.setStyleSheet("font-size: 14pt; background-color: green; color: black;")
        self.mouse_button.clicked.connect(self.update_games)
        button_layout.addWidget(self.mouse_button)

        # Add platform button
        self.platform_button = QPushButton("platofrm", self)
        self.platform_button.setStyleSheet("font-size: 14pt; background-color: green; color: black;")
        self.platform_button.clicked.connect(self.update_games)
        button_layout.addWidget(self.platform_button)

        # Add shooter button
        self.shooter_button = QPushButton("Shooter", self)
        self.shooter_button.setStyleSheet("font-size: 14pt; background-color: blue; color: black;")
        self.shooter_button.clicked.connect(self.update_games)
        button_layout.addWidget(self.shooter_button)

        # Add chill button
        self.chill_button = QPushButton("Chill", self)
        self.chill_button.setStyleSheet("font-size: 14pt; background-color: orange; color: black;")
        self.chill_button.clicked.connect(self.update_games)
        button_layout.addWidget(self.chill_button)

        # Add action button
        self.action_button = QPushButton("action", self)
        self.action_button.setStyleSheet("font-size: 14pt; background-color: purple; color: black;")
        self.action_button.clicked.connect(self.update_games)
        button_layout.addWidget(self.action_button)

        # Add the button layout to the main layout
        main_layout.addLayout(button_layout)

        # Add search box
        self.search_box = QLineEdit(self)
        self.search_box.setPlaceholderText("Search...")
        self.search_box.setStyleSheet("padding: 10px; font-size: 20px; background-color: white;")
        self.search_box.textChanged.connect(self.filter_buttons)
        main_layout.addWidget(self.search_box, alignment=Qt.AlignRight)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_area.setWidget(scroll_widget)

        layout = QVBoxLayout(scroll_widget)

        self.buttons = []

        self.all_games = [
            "firemblemengage", "firemblem3houses", "chainedechoes"
        ]

        self.displayed_games = self.all_games  # Initially, all games are displayed

        grid_layout = QGridLayout()
        row, col = 0, 0
        for game in self.displayed_games:
            button = QPushButton(game, self)
            button.clicked.connect(lambda checked, g=game.replace(" ", "").lower(): self.run_docker_command(g))

            # Change grey color to another color (black)
            button.setStyleSheet("padding: 3px; border: none; color: black; background-color: red;")

            grid_layout.addWidget(button, row, col)
            col += 1
            if col == 4:
                col = 0
                row += 1

            self.buttons.append(button)

        layout.addLayout(grid_layout)
        scroll_area.setVerticalScrollBarPolicy(0x1)
        main_layout.addWidget(scroll_area)

    def run_docker_command(self, image_name):
        formatted_image_name = image_name.replace(":", "").lower()
        # WSL command to switch to Kali Linux
        wsl_command = "wsl -d kali-linux"
        # Docker command within WSL
        docker_command = f'docker run -v /mnt/c/games/{formatted_image_name}:/c/games/{formatted_image_name} -it -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix --name {formatted_image_name} michadockermisha/backup:{formatted_image_name} sh -c "apk add rsync && rsync -aP /home /c/games && mv /c/games/home /c/games/{formatted_image_name}"'
        # Joining commands and executing using subprocess
        full_command = f"{wsl_command} && {docker_command}"
        subprocess.Popen(full_command, shell=True)

    def filter_buttons(self, text):
        for button in self.buttons:
            button.setVisible(text.lower() in button.text().lower())

    def update_games(self):
        sender_button = self.sender()
        if sender_button == self.interactive_button:
            specified_titles = ["batmantts"]
        elif sender_button == self.mouse_button:
            specified_titles = []
        elif sender_button == self.chill_button:
            specified_titles = []
        elif sender_button == self.action_button:
            specified_titles = []
        elif sender_button == self.platform_button:
            specified_titles = []

        self.displayed_games = [game for game in self.all_games if game.lower().replace(" ", "") in specified_titles]

        for button in self.buttons:
            button.setVisible(button.text().lower().replace(" ", "") in specified_titles)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    docker_app = DockerApp()
    docker_app.show()
    sys.exit(app.exec_())

