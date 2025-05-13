import sys
import os
import json
import subprocess
import requests

class DockerAppCLI:
    def __init__(self):
        self.categories = ["interactive", "mouse", "platform", "shooter", "chill", "action"]
        self.load_games()
        # Fetch Docker Hub tags info (normalized tag -> full_size)
        self.tag_sizes = self.fetch_docker_tags()
        self.main_menu()

    def load_games(self):
        if os.path.exists('games_data.json'):
            with open('games_data.json', 'r') as f:
                data = json.load(f)
                self.all_games = data['all_games']
                self.category_games = data['category_games']
        else:
            self.all_games = [
                "Vampire Bloodlines", "SniperElite3", "BatmanTTs", "TheRadStringClub", "ElPasoElswere", "TLOH", "Brothers",
                "Witcher3", "Returnal", "HarvestMoon", "TheXpanse", "MoonstoneIsland", "PlanetCoaster", "SleepingDogs",
                "GTVIV", "GoodbyeVolcanoHigh", "Fallout4", "Oblivion", "CitiesSkylines2", "KingdomOfAmlur", "Wolfenstein2",
                "OkamiHD", "TheSilentAge", "DivinityOriginalSin2", "TheRadStringClub", "CosmicShake", "PlagtalerEquirm",
                "SackBoy", "Beyond2Soul", "OddWorldSoulstorm", "SlayThePrincess", "PrisonSimulator", "VideoVerse",
                "Singularity", "FarCryPrimal", "SherlockHolmesChapterOne", "SherlockHolmesTheAwakened",
                "SherlockHolmesCrimesAndPunishments", "TheAscent", "AncestorsHumankind", "BumSimulator",
                "CafeOwnerSimulation", "HackerSimulator", "HellbladeSenuaSacrifice", "LifeIsStrangeremastered",
                "DarksidersGenesis", "SkaterXL", "SaintsRow3", "Inscryption", "BrewmasterBeerSimulator",
                "ChefLifeSimulator", "DetroitBecomeHuman", "HouseFlipper", "EnterTheGungeon", "DeadIsland2",
                "LostInPlay", "GodOfWar", "SunsetOverdrive", "KillerFrequency", "DeathMustDie", "PunchClub2FastForward",
                "DeusExHuman", "SludgeLife2", "BlackSkylands", "NotForBroadcast", "DeepRockGalactic",
                "AssassinsCreedValhalla", "Frostpunk", "Torchlight2", "NobodySavedTheWorld", "Oxenfree2", "SpiritFarer",
                "Furi", "MetalGearSolidMaster", "HighlandSong", "Venba", "Covergence", "BomBrushCyberFunk",
                "FateSamuraiRemnant", "TrinityFusion", "EvilWest", "TheMageSeeker", "EnderLiles", "Nocturnal",
                "OctopathTraveler2", "DevilMayCry4", "Bramble", "NeoTheWorldEndsWithYou", "TheGunk", "SteelRising",
                "FireEmblemWarriors3Hopes", "StrangerOfParadaise", "DeadSpace", "LordsOfTheFallen", "Vampyr",
                "SonicSuperStars", "SeasonALetterToTheFuture", "SuperMarioWonder", "Trine2", "Turok", "Dredge",
                "Tekken8", "Tchia", "DoubleDragonAiden", "CultOfTheLamb", "CosmicWheelSisterhood", "TalesOfVesperia",
                "Torchlight2", "XenoBladeChronicles", "OkamiHD", "TriangleStrategy", "TenseIV", "BraverlyDefault2",
                "MegaManBattleNetwork", "LiveAlive", "AdvancedWars", "RiskOfRain", "DriverSanFrancisco", "Signalis",
                "Resistance2", "Tinykin", "TheDarkness", "ThePunisher", "LegendOfTianding", "Nier", "Soulstice",
                "Bugsnax", "ZeldaLinkToThePast", "PowerWashSimulator", "ArtfulEscape", "PCBuildingSimulator",
                "CircusElectrique", "Desperados3", "AmericanaRcedia", "Risen2", "SniperGhostWarrior2",
                "MidnightFightExpress", "ReadyOrNot", "TheInvincible", "LoveTooEasily", "FistForgedInShadow",
                "ImmortalsofAveum", "CookingSimulator", "ASpaceForTheUnbound", "AlphaProtocol", "MIAndTheDragonPrincess",
                "LateShift", "ValkyriaChronicles4", "DarkPicturesAnthology", "AsDuskFalls", "TheBunker", "CobletCore",
                "FirstDateLateToDate", "TheComplex", "SoniColors", "Enslaved", "SuperSeducer2", "Islets", "FiveDates",
                "Marvel", "Sanabi", "Sunhaven", "Fuga", "ScarsAbove", "WitchFire", "ExitTheGungeon", "WeirdWest",
                "SuperMarioRPG", "NinoKuni", "FireEmblemEngage", "FireEmblem3Houses", "ChainedEchoes",
                "ArmoredCore6FiresOfRubicon", "GreedFall", "EiyudeNchronicle", "CrisisCoreFinalFantasy7",
                "TalesOfBerseria", "FFX", "TwinMirrors", "BinaryDomain", "AnotherCrabsTreasure", "Yakuza3A",
                "Yakuza4", "Wildlands", "Banishers", "RepellaFella", "ChildrenOfTheSun", "VampireSurvivors",
                "ChicoryAcolorfulTale"
            ]
            self.category_games = {category: [] for category in self.categories}

    def save_games(self):
        data = {
            'all_games': self.all_games,
            'category_games': self.category_games
        }
        with open('games_data.json', 'w') as f:
            json.dump(data, f, indent=4)

    def fetch_docker_tags(self):
        """
        Fetch tags from Docker Hub along with their full_size.
        Returns a dictionary mapping normalized tag name to full_size in bytes.
        """
        url = "https://hub.docker.com/v2/repositories/michadockermisha/backup/tags?page_size=100"
        try:
            response = requests.get(url)
            data = response.json()
            tag_sizes = {}
            for item in data.get('results', []):
                tag_name = item['name']
                full_size = item.get('full_size', 0)
                # Normalize the tag name similar to format_game_id
                normalized = ''.join(e for e in tag_name.lower() if e.isalnum())
                tag_sizes[normalized] = full_size
            return tag_sizes
        except Exception as e:
            print("Error fetching docker tags:", e)
            return {}

    def format_size(self, size):
        """
        Convert a size in bytes into a human-readable string.
        """
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024:
                return f"{size:.1f}{unit}"
            size /= 1024
        return f"{size:.1f}PB"

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

            choice = input("Enter your choice: ").strip()

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
                print("Exiting the application.")
                sys.exit(0)
            else:
                print("Invalid choice. Please try again.")

    def show_all_games(self):
        print("\nAll Games:")
        for game in self.all_games:
            normalized_id = self.format_game_id(game)
            size_str = ""
            if normalized_id in self.tag_sizes:
                size_str = f" ({self.format_size(self.tag_sizes[normalized_id])})"
            print(f"{game}{size_str}")

    def filter_by_category(self):
        print("\nCategories:")
        for i, category in enumerate(self.categories, start=1):
            print(f"{i}. {category.capitalize()}")

        choice = input("Choose a category: ").strip()

        if choice.isdigit() and 1 <= int(choice) <= len(self.categories):
            selected_category = self.categories[int(choice) - 1]
            games = self.category_games.get(selected_category, [])
            print(f"\nGames in category '{selected_category.capitalize()}':")
            for game_id in games:
                original_game = self.get_original_game_name(game_id)
                if original_game:
                    normalized_id = self.format_game_id(original_game)
                    size_str = ""
                    if normalized_id in self.tag_sizes:
                        size_str = f" ({self.format_size(self.tag_sizes[normalized_id])})"
                    print(f"{original_game}{size_str}")
        else:
            print("Invalid category. Please try again.")

    def search_games(self):
        search_text = input("Enter part of the game name to search: ").strip().lower()
        matching_games = [game for game in self.all_games if search_text in game.lower()]

        if matching_games:
            print("\nMatching Games:")
            for game in matching_games:
                normalized_id = self.format_game_id(game)
                size_str = ""
                if normalized_id in self.tag_sizes:
                    size_str = f" ({self.format_size(self.tag_sizes[normalized_id])})"
                print(f"{game}{size_str}")
        else:
            print("No matching games found.")

    def add_game(self):
        game = input("Enter the name of the game to add: ").strip()

        if game:
            print("\nCategories:")
            for i, category in enumerate(self.categories, start=1):
                print(f"{i}. {category.capitalize()}")

            category_choice = input("Choose a category: ").strip()

            if category_choice.isdigit() and 1 <= int(category_choice) <= len(self.categories):
                selected_category = self.categories[int(category_choice) - 1]
                self.all_games.append(game)
                game_id = self.format_game_id(game)
                if game_id not in self.category_games[selected_category]:
                    self.category_games[selected_category].append(game_id)
                self.save_games()
                print(f"'{game}' has been added to the '{selected_category.capitalize()}' category.")
            else:
                print("Invalid category. Please try again.")
        else:
            print("No game name entered. Please try again.")

    def delete_game(self):
        search_text = input("Enter part of the game name to delete: ").strip().lower()
        matching_games = [game for game in self.all_games if search_text in game.lower()]

        if not matching_games:
            print("No matching games found.")
            return

        print("\nMatching Games:")
        for i, game in enumerate(matching_games, start=1):
            print(f"{i}. {game}")

        choice = input("Choose a game to delete: ").strip()

        if choice.isdigit() and 1 <= int(choice) <= len(matching_games):
            game_to_delete = matching_games[int(choice) - 1]
            game_id = self.format_game_id(game_to_delete)
            # Attempt to delete the tag from Docker Hub
            if self.delete_docker_tag(game_id):
                print(f"Tag '{game_id}' deleted from Docker Hub.")
            else:
                print(f"Failed to delete tag '{game_id}' from Docker Hub.")
            # Remove locally
            self.all_games.remove(game_to_delete)
            for category in self.categories:
                if game_id in self.category_games[category]:
                    self.category_games[category].remove(game_id)
            self.save_games()
            print(f"'{game_to_delete}' has been deleted locally.")
        else:
            print("Invalid choice. Please try again.")

    def delete_docker_tag(self, tag):
        """
        Deletes the given tag from Docker Hub.
        Requires the environment variable DOCKERHUB_TOKEN to be set.
        """
        dockerhub_token = os.environ.get("DOCKERHUB_TOKEN")
        if not dockerhub_token:
            print("DOCKERHUB_TOKEN not set. Cannot delete tag from Docker Hub.")
            return False
        url = f"https://hub.docker.com/v2/repositories/michadockermisha/backup/tags/{tag}/"
        headers = {"Authorization": f"JWT {dockerhub_token}"}
        try:
            response = requests.delete(url, headers=headers)
            if response.status_code == 204:
                return True
            else:
                print(f"Failed to delete tag. Status: {response.status_code}, {response.text}")
                return False
        except Exception as e:
            print("Error deleting tag from Docker Hub:", e)
            return False

    def run_game(self):
        games_to_run = []

        while True:
            game_input = input("Enter the name of the game to run (or 'y' to start): ").strip()
            if game_input.lower() == 'y':
                if not games_to_run:
                    print("No games selected to run. Exiting run mode.")
                break

            matched_games = [game for game in self.all_games if game.lower() == game_input.lower()]
            if not matched_games:
                matched_games = [game for game in self.all_games if game_input.lower() in game.lower()]

            if not matched_games:
                print("Game not found. Please try again.")
                continue

            if len(matched_games) > 1:
                print("\nMultiple matching games found:")
                for i, game in enumerate(matched_games, start=1):
                    print(f"{i}. {game}")
                choice = input("Choose a game to add: ").strip()
                if choice.isdigit() and 1 <= int(choice) <= len(matched_games):
                    selected_game = matched_games[int(choice) - 1]
                else:
                    print("Invalid choice. Please try again.")
                    continue
            else:
                selected_game = matched_games[0]

            games_to_run.append(selected_game)

        for game in games_to_run:
            self.run_docker_game(game)

    def run_docker_game(self, game):
        # Use the normalized game name as the Docker image tag and container name
        formatted_image_name = self.format_game_id(game)
        docker_container_name = formatted_image_name

        docker_command = (
            f'docker run -v /srv/samba/shared/{formatted_image_name}:/c/games/{game} '
            f'-it -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix --name {docker_container_name} '
            f'michadockermisha/backup:{formatted_image_name} sh -c "apk add rsync && rsync -aP /home /c/games && '
            f'mv /c/games/home /c/games/{game}"'
        )

        print(f"Running Docker command for '{game}': {docker_command}")
        try:
            subprocess.run(docker_command, shell=True, check=True)
            print(f"'{game}' has finished running.")
        except subprocess.CalledProcessError as e:
            print(f"Error running '{game}': {e}")

    def get_original_game_name(self, game_id):
        for game in self.all_games:
            if self.format_game_id(game) == game_id:
                return game
        return None

    def format_game_id(self, game_name):
        return ''.join(e for e in game_name.lower() if e.isalnum())

if __name__ == '__main__':
    DockerAppCLI()
