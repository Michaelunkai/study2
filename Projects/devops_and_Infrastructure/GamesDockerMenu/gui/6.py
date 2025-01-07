import sys
import os
import json
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QScrollArea, QLineEdit,
                             QGridLayout, QDesktopWidget, QMessageBox, QInputDialog, QLabel)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import subprocess


class DockerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Docker Commands")
        self.resize_to_screen()
        self.setStyleSheet("background-color: black; font: 10pt bold; color: white;")
        self.categories = ["interactive", "mouse", "platform", "shooter", "chill", "action"]
        self.load_games()
        self.init_ui()

    def resize_to_screen(self):
        desktop_geometry = QDesktopWidget().screenGeometry()
        width = int(desktop_geometry.width() * 0.95)
        height = int(desktop_geometry.height() * 0.95)
        self.setGeometry(0, 0, width, height)

    def load_games(self):
        if os.path.exists('games_data.json'):
            with open('games_data.json', 'r') as f:
                data = json.load(f)
                self.all_games = data['all_games']
                self.category_games = data['category_games']
        else:
            self.all_games = [
                "Vampire Bloodlines", "sniperelite3", "batmantts", "theradstringclub", "elpasoelswere", "tloh", "brothers",
                "witcher3", "returnal", "harvestmoon", "thexpanse", "moonstoneisland", "planetcoaster", "sleepingdogs",
                "gtviv", "goodbyevolcanohigh", "fallout4", "oblivion", "citieskylines2", "kingdomofamalur", "wolfenstein2",
                "okamihd", "thesilentage", "divinityoriginalsin2", "theradstringclub", "cosmicshake", "plagtalerequirm",
                "sackboy", "beyond2soul", "oddworldsoulstorm", "slaytheprincess", "prisonsimulator", "videoverse",
                "singularity", "farcryprimal", "sherlockholmeschapterone", "sherlockholmestheawakened",
                "sherlockholmescrimesandpunishments", "theascent", "ancestorshumankind", "bumsimulator",
                "cafeownersimulation", "hackersimulator", "hellbladesenuasacrifice", "lifeistrangeremastered",
                "darksidersgenesis", "skaterxl", "saintsrow3", "inscryption", "brewmasterbeersimulator",
                "cheflifesimulator", "detroitbecomehuman", "houseflipper", "enterthegungeon", "deadisland2",
                "lostinplay", "godofwar", "sunsetoverdrive", "killerfrequency", "deathmustdie", "punchclub2fastforward",
                "deusexhuman", "sludgelife2", "blackskylands", "notforbroadcast", "deeprockgalactic",
                "assassinscreedvalhalla", "frostpunk", "torchlight2", "nobodysavedtheworld", "oxenfree2", "spiritfarer",
                "furi", "metalgearsolidmaster", "highlandsong", "venba", "covergence", "bombrushcyberfunk",
                "fatesamurairemnant", "trinityfusion", "evilwest", "themageseeker", "enderliles", "nocturnal",
                "octopathtraveler2", "devilmaycry4", "bramble", "neotheworldendswithyou", "thegunk", "steelrising",
                "firemblemwarriors3hopes", "strangerofparadaise", "deadspace", "lordsofthefallen", "vampyr",
                "sonicsuperstarts", "seasonalettertothefuture", "supermariowonder", "trine2", "turok", "dredge",
                "tekken8", "tchia", "doubledragongaiden", "cultofthelamb", "cosmicwheelsisterhood", "talesofvesperia",
                "torchlight2", "xenobladechronicles", "okamihd", "trianglestrategy", "tenseiv", "braverlydefault2",
                "megamanbattlenetwork", "livealive", "advancedwars", "riskofrain", "driversanfrancisco", "signalis",
                "resistance2", "tinykin", "thedarkness", "thepunisher", "legendoftianding", "nier", "soulstice",
                "bugsnax", "zeldalinktothepast", "powerwashsimulator", "artfulescape", "pcbuildingsimulator",
                "circuselectrique", "desperados3", "americanarcedia", "risen2", "sniperghostwarrior2",
                "midnightfightexpress", "readyornot", "theinvincible", "lovetooeasily", "fistforgedinshadow",
                "immortalsofaveum", "cookingsimulator", "aspacefortheunbound", "alphaprotocol", "miandthedragonprincess",
                "lateshift", "valkyriachronicles4", "darkpicturesanthology", "asduskfalls", "thebunker", "cobletcore",
                "firstdatelatetodate", "thecomplex", "sonicolors", "enslaved", "superseducer2", "islets", "fivedates",
                "marvel", "sanabi", "sunhaven", "fuga", "scarsabove", "witchfire", "exithegungeon", "weirdwest",
                "supermariorpg", "ninokuni", "firemblemengage", "firemblem3houses", "chainedechoes",
                "armoredcore6firesofrubicon", "greedfall", "eiyudenchromicle", "crisiscorefinalfantasy7",
                "talesofberseria", "ffx", "twinmirrors", "binarydomain", "anothercrabstreasure", "yakuxa3", "yakuza4",
                "wildlands", "banishers", "repellafella", "childrenofthesun", "vampiresurvivors"
            ]
            self.category_games = {
                "interactive": ["batmantts", "thexpanse", "beyond2souls", "detroitbecomehuman", "oxenfree2", "sherlockholmeschapterone", "slaytheprincess", "lifeistrangeremastered", "goodbyevolcanohigh", "sherlockholmescrimesandpunishments", "lovetooeasily", "lateshift", "miandthedragonprincess", "darkpicturesanthology", "asduskfalls", "thebunker", "firstdatelatetodate", "thecomplex", "superseducer2", "fivedates", "twinmirrors"],
                "mouse": ["hackersimulator", "thecaseofthegoldenidol", "sludgelife2", "videoverse", "returnofthemonkeyisland", "divinityoriginalsin2", "cafeownersimulation", "notforbroadcast", "slaytheprincess"],
                "shooter": ["sniperelite3", "deusexhuman", "elpasoelswhere", "theascent", "deeprockgalactic", "singularity", "evilwest", "turok", "resistance2", "thedarkness", "sniperghostwarrior2", "readyornot", "vanquish", "scarsabove", "witchfire", "binarydomain", "wildlands"],
                "chill": ["okamihd", "lostinplay", "octopathtraveler2", "skaterxl", "harvestmoon", "tloh", "planetcoaster", "brothers", "seasonalettertothefuture", "enterthegungeon", "thesilentage", "bumsimulator", "moonstoneisland", "bumsimulator", "cheflifesimulator", "sonicsuperstarts", "prisonsimulator", "inscryption", "brewmasterbeersimulator", "nobodysavedtheworld", "bramble", "punchclub2fastforward", "highlandsong", "spiritfarer", "cafeownersimulation", "frostpunk", "citieskylines2", "blackskylands", "deathmustdie", "houseflipper", "killerfrequency", "venba", "dredge", "tchia", "doubledragongaiden", "cultofthelamb", "cosmicwheelsisterhood", "okamihd", "trianglestrategy", "braverlydefault2", "livealive", "advancedwars", "signalis", "tinykin", "bugsnax", "powerwashsimulator", "artfulescape", "pcbuildingsimulator", "circuselectrique", "aspacefortheunbound", "americanarcedia", "midnightfightexpress", "theinvincible", "cookingsimulator", "aspacefortheunbound", "cobletcore", "tetriseffect", "sunhaven", "fuga", "chainedechoes", "eiyudenchromicle", "anothercrabstreasure", "repellafella", "vampiresurvivors"],
                "action": ["saintsrow3", "farcryprimal", "devilmaycry4", "godofwar", "deadspace", "fatesamurairemnant", "sunsetoverdrive", "sleepingdogs", "returnal", "kingdomofamalur", "wolfenstein2", "deadspace", "gtviv", "vampyr", "vampirebloodlines", "assassinscreedvalhalla", "neotheworldendswithyou", "thegunk", "darksidersgenesis", "steelrising", "theascent", "oblibion", "plagtalerequirm", "deadisland2", "metalgearsolidmaster", "mountandblade2bannerlord", "ancestorshumankind", "armoredcore6firesofrubicon", "furi", "witcher3", "fallout4", "oblivion", "bombrushcyberfunk", "vampirebloodlines", "firemblemwarriors3hopes", "themageseeker", "hellbladesenuasacrifice", "turok", "tekken8", "torchlight2", "talesofvesperia", "xenobladechronicles", "tenseiv", "riskofrain", "driversanfrancisco", "thedarkness", "thepunisher", "nier", "soulstice", "desperados3", "immortalsofaveum", "alphaprotocol", "valkyriachronicles4", "enslaved", "marvel", "weirdwest", "ninokuni", "firemblemengage", "firemblem3houses", "armoredcore6firesofrubicon", "greedfall", "crisiscorefinalfantasy7", "talesofberseria", "ffx", "binarydomain", "yakuxa3", "yakuza4", "wildlands", "banishers", "childrenofthesun"],
                "platform": ["sackboy", "trine2", "supermariowonder", "cosmicshake", "kazeandthewildmasks", "oddworldsoulstorm", "enderliles", "covergence", "fistforgedinshadowtorch", "sonicsuperstarts", "nocturnal", "trinityfusion", "talesofvesperia", "megamanbattlenetwork", "tinykin", "legendoftianding", "zeldalinktothepast", "artfulescape", "risen2", "fistforgedinshadow", "sonicolors", "islets", "sanabi", "exithegungeon", "supermariorpg"]
            }
        self.displayed_games = self.all_games.copy()

    def save_games(self):
        data = {
            'all_games': self.all_games,
            'category_games': self.category_games
        }
        with open('games_data.json', 'w') as f:
            json.dump(data, f)

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        self.add_category_buttons(main_layout)
        self.add_search_box(main_layout)
        self.add_add_delete_buttons(main_layout)
        self.add_game_scroll_area(main_layout)

    def add_category_buttons(self, layout):
        button_layout = QHBoxLayout()
        for category in self.categories:
            button = QPushButton(category.capitalize(), self)
            button.setStyleSheet(f"font-size: 14pt; background-color: {self.get_color(category)}; color: black;")
            button.clicked.connect(self.update_games)
            button_layout.addWidget(button)
        layout.addLayout(button_layout)

    def add_search_box(self, layout):
        self.search_box = QLineEdit(self)
        self.search_box.setPlaceholderText("Search...")
        self.search_box.setStyleSheet("padding: 10px; font-size: 20px; background-color: white;")
        self.search_box.textChanged.connect(self.filter_buttons)
        layout.addWidget(self.search_box, alignment=Qt.AlignRight)

    def add_add_delete_buttons(self, layout):
        add_delete_layout = QHBoxLayout()
        self.add_button = QPushButton("Add Game", self)
        self.add_button.setStyleSheet("font-size: 16pt; background-color: #4CAF50; color: white; padding: 10px;")
        self.add_button.setFont(QFont("Arial", 12, QFont.Bold))
        self.add_button.clicked.connect(self.add_game)
        add_delete_layout.addWidget(self.add_button)

        self.delete_button = QPushButton("Delete Game", self)
        self.delete_button.setStyleSheet("font-size: 16pt; background-color: #F44336; color: white; padding: 10px;")
        self.delete_button.setFont(QFont("Arial", 12, QFont.Bold))
        self.delete_button.clicked.connect(self.delete_game)
        add_delete_layout.addWidget(self.delete_button)

        layout.addLayout(add_delete_layout)

    def add_game_scroll_area(self, layout):
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_area.setWidget(scroll_widget)

        self.grid_layout = QGridLayout(scroll_widget)
        self.update_game_buttons()

        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        layout.addWidget(scroll_area)

    def get_color(self, category):
        colors = {
            "interactive": "red", "mouse": "green", "platform": "yellow",
            "shooter": "blue", "chill": "orange", "action": "purple"
        }
        return colors.get(category, "gray")

    def update_game_buttons(self):
        for i in reversed(range(self.grid_layout.count())):
            self.grid_layout.itemAt(i).widget().setParent(None)

        row, col = 0, 0
        for game in self.displayed_games:
            button = QPushButton(game, self)
            button.clicked.connect(lambda checked, g=game.replace(" ", "").lower(): self.run_docker_command(g))
            button.setStyleSheet("padding: 3px; border: none; color: black; background-color: red;")
            self.grid_layout.addWidget(button, row, col)
            col += 1
            if col == 4:
                col = 0
                row += 1

    def run_docker_command(self, image_name):
        formatted_image_name = image_name.replace(":", "").lower()
        docker_command = (
            f'docker run -v /mnt/c/games/{formatted_image_name}:/c/games/{formatted_image_name} '
            f'-it -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix --name {formatted_image_name} '
            f'michadockermisha/backup:{formatted_image_name} sh -c "apk add rsync && rsync -aP /home '
            f'/c/games && mv /c/games/home /c/games/{formatted_image_name}"'
        )
        subprocess.Popen(docker_command, shell=True)

    def filter_buttons(self, text):
        self.displayed_games = [game for game in self.all_games if text.lower() in game.lower()]
        self.update_game_buttons()

    def update_games(self):
        sender_button = self.sender()
        category = sender_button.text().lower()
        self.displayed_games = [game for game in self.all_games if game.lower().replace(" ", "") in self.get_category_games(category)]
        self.update_game_buttons()

    def get_category_games(self, category):
        return self.category_games.get(category, [])

    def add_game(self):
        game, ok = QInputDialog.getText(self, "Add Game", "Enter the name of the game:")
        if ok and game:
            category, ok = QInputDialog.getItem(self, "Choose Category", "Select a category:", self.categories, 0, False)
            if ok and category:
                self.all_games.append(game)
                self.category_games[category.lower()].append(game.lower().replace(" ", ""))
                self.save_games()
                QMessageBox.information(self, "Game Added", f"{game} has been added to the {category} category.")
                self.update_games()

    def delete_game(self):
        search_text, ok = QInputDialog.getText(self, "Search Game to Delete", "Enter part of the game name:")
        if ok and search_text:
            matching_games = [game for game in self.all_games if search_text.lower() in game.lower()]
            if not matching_games:
                QMessageBox.information(self, "No Games Found", "No games match your search.")
                return

            game, ok = QInputDialog.getItem(self, "Delete Game", "Choose a game to delete:", matching_games, 0, False)
            if ok and game:
                self.all_games.remove(game)
                if game in self.displayed_games:
                    self.displayed_games.remove(game)

                game_id = game.lower().replace(" ", "")
                for category in self.categories:
                    if game_id in self.category_games[category]:
                        self.category_games[category].remove(game_id)

                self.save_games()
                QMessageBox.information(self, "Game Deleted", f"{game} has been deleted from all categories.")
                self.update_games()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    docker_app = DockerApp()
    docker_app.show()
    
    sys.exit(app.exec_())
