import sys
import os
import json
import subprocess

class DockerAppCLI:
    def __init__(self):
        self.categories = ["interactive", "mouse", "platform", "shooter", "chill", "action"]
        self.load_games()
        self.main_menu()

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

    def main_menu(self):
        while True:
            print("\nMain Menu:")
            print("1. Show all games")
            print("2. Filter games by category")
            print("3. Search games")
            print("4. Add a game")
            print("5. Delete a game")
            print("6. Run a game")
            print("7. Exit")

            choice = input("Enter your choice: ")

            if choice == '1':
                self.show_all_games()
            elif choice == '2':
                self.filter_by_category()
            elif choice == '3':
                self.search_games()
            elif choice == '4':
                self.add_game()
            elif choice == '5':
                self.delete_game()
            elif choice == '6':
                self.run_game()
            elif choice == '7':
                sys.exit(0)
            else:
                print("Invalid choice. Please try again.")

    def show_all_games(self):
        print("\nAll Games:")
        for game in self.all_games:
            print(game)

    def filter_by_category(self):
        print("\nCategories:")
        for i, category in enumerate(self.categories, start=1):
            print(f"{i}. {category.capitalize()}")

        choice = input("Choose a category: ")

        if choice.isdigit() and 1 <= int(choice) <= len(self.categories):
            selected_category = self.categories[int(choice) - 1]
            games = self.category_games.get(selected_category, [])
            print(f"\nGames in category '{selected_category}':")
            for game in games:
                print(game)
        else:
            print("Invalid category. Please try again.")

    def search_games(self):
        search_text = input("Enter part of the game name to search: ").lower()
        matching_games = [game for game in self.all_games if search_text in game.lower()]

        if matching_games:
            print("\nMatching Games:")
            for game in matching_games:
                print(game)
        else:
            print("No matching games found.")

    def add_game(self):
        game = input("Enter the name of the game to add: ")

        if game:
            print("\nCategories:")
            for i, category in enumerate(self.categories, start=1):
                print(f"{i}. {category.capitalize()}")

            category_choice = input("Choose a category: ")

            if category_choice.isdigit() and 1 <= int(category_choice) <= len(self.categories):
                selected_category = self.categories[int(category_choice) - 1]
                self.all_games.append(game)
                self.category_games[selected_category].append(game.lower().replace(" ", ""))
                self.save_games()
                print(f"{game} has been added to the {selected_category} category.")
            else:
                print("Invalid category. Please try again.")
        else:
            print("No game name entered. Please try again.")

    def delete_game(self):
        search_text = input("Enter part of the game name to delete: ").lower()
        matching_games = [game for game in self.all_games if search_text in game.lower()]

        if not matching_games:
            print("No matching games found.")
            return

        print("\nMatching Games:")
        for i, game in enumerate(matching_games, start=1):
            print(f"{i}. {game}")

        choice = input("Choose a game to delete: ")

        if choice.isdigit() and 1 <= int(choice) <= len(matching_games):
            game_to_delete = matching_games[int(choice) - 1]
            self.all_games.remove(game_to_delete)

            game_id = game_to_delete.lower().replace(" ", "")
            for category in self.categories:
                if game_id in self.category_games[category]:
                    self.category_games[category].remove(game_id)

            self.save_games()
            print(f"{game_to_delete} has been deleted.")
        else:
            print("Invalid choice. Please try again.")

    def run_game(self):
        game_name = input("Enter the name of the game to run: ").lower().replace(" ", "")

        if game_name not in [game.lower().replace(" ", "") for game in self.all_games]:
            print("Game not found. Please try again.")
            return

        formatted_image_name = game_name.replace(":", "").lower()
        docker_command = (
            f'docker run -v /srv/samba/shared/{formatted_image_name}:/c/games/{formatted_image_name} '
            f'-it -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix --name {formatted_image_name} '
            f'michadockermisha/backup:{formatted_image_name} sh -c "apk add rsync && rsync -aP /home '
            f'/c/games && mv /c/games/home /c/games/{formatted_image_name}"'
        )
        print(f"Running Docker command: {docker_command}")
        subprocess.Popen(docker_command, shell=True)

if __name__ == '__main__':
    DockerAppCLI()
