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
                "ChicoryAcolorfulTale"  # Added the problematic game
            ]
            self.category_games = {
                "interactive": ["batmantts", "thexpanse", "beyond2souls", "detroitbecomehuman", "oxenfree2",
                                "sherlockholmeschapterone", "slaytheprincess", "lifeistrangeremastered",
                                "goodbyevolcanohigh", "sherlockholmescrimesandpunishments", "lovetooeasily",
                                "lateshift", "miandthedragonprincess", "darkpicturesanthology", "asduskfalls",
                                "thebunker", "firstdatelatetodate", "thecomplex", "superseducer2", "fivedates",
                                "twinmirrors"],
                "mouse": ["hackersimulator", "thecaseofthegoldenidol", "sludgelife2", "videoverse",
                          "returnofthemonkeyisland", "divinityoriginalsin2", "cafeownersimulation",
                          "notforbroadcast", "slaytheprincess"],
                "shooter": ["sniperelite3", "deusexhuman", "elpasoelswere", "theascent", "deeprockgalactic",
                            "singularity", "evilwest", "turok", "resistance2", "thedarkness", "sniperghostwarrior2",
                            "readyornot", "vanquish", "scarsabove", "witchfire", "binarydomain", "wildlands"],
                "chill": ["okamihd", "lostinplay", "octopathtraveler2", "skaterxl", "harvestmoon", "tloh",
                          "planetcoaster", "brothers", "seasonalettertothefuture", "enterthegungeon", "thesilentage",
                          "bumsimulator", "moonstoneisland", "bumsimulator", "cheflifesimulator", "sonicsuperstarts",
                          "prisonsimulator", "inscryption", "brewmasterbeersimulator", "nobodysavedtheworld",
                          "bramble", "punchclub2fastforward", "highlandsong", "spiritfarer", "cafeownersimulation",
                          "frostpunk", "citieskylines2", "blackskylands", "deathmustdie", "houseflipper",
                          "killerfrequency", "venba", "dredge", "tchia", "doubledragongaiden", "cultofthelamb",
                          "cosmicwheelsisterhood", "okamihd", "trianglestrategy", "braverlydefault2", "livealive",
                          "advancedwars", "signalis", "tinykin", "bugsnax", "powerwashsimulator", "artfulescape",
                          "pcbuildingsimulator", "circuselectrique", "aspacefortheunbound", "americanarcedia",
                          "midnightfightexpress", "theinvincible", "cookingsimulator", "aspacefortheunbound",
                          "cobletcore", "tetriseffect", "sunhaven", "fuga", "chainedechoes", "eiyudenchromicle",
                          "anothercrabstreasure", "repellafella", "vampiresurvivors"],
                "action": ["saintsrow3", "farcryprimal", "devilmaycry4", "godofwar", "deadspace",
                           "fatesamurairemnant", "sunsetoverdrive", "sleepingdogs", "returnal",
                           "kingdomofamalur", "wolfenstein2", "deadspace", "gtviv", "vampyr", "vampirebloodlines",
                           "assassinscreedvalhalla", "neotheworldendswithyou", "thegunk", "darksidersgenesis",
                           "steelrising", "theascent", "oblibion", "plagtalerequirm", "deadisland2",
                           "metalgearsolidmaster", "mountandblade2bannerlord", "ancestorshumankind",
                           "armoredcore6firesofrubicon", "furi", "witcher3", "fallout4", "oblivion",
                           "bombrushcyberfunk", "vampirebloodlines", "firemblemwarriors3hopes",
                           "themageseeker", "hellbladesenuasacrifice", "turok", "tekken8", "torchlight2",
                           "talesofvesperia", "xenobladechronicles", "tenseiv", "riskofrain",
                           "driversanfrancisco", "thedarkness", "thepunisher", "nier", "soulstice",
                           "desperados3", "immortalsofaveum", "alphaprotocol", "valkyriachronicles4",
                           "enslaved", "marvel", "weirdwest", "ninokuni", "firemblemengage",
                           "firemblem3houses", "armoredcore6firesofrubicon", "greedfall",
                           "crisiscorefinalfantasy7", "talesofberseria", "ffx", "binarydomain",
                           "yakuxa3", "yakuza4", "wildlands", "banishers", "childrenofthesun"],
                "platform": ["SackBoy", "Trine2", "SuperMarioWonder", "CosmicShake", "KazeAndTheWildMasks",
                             "OddWorldSoulstorm", "EnderLiles", "Covergence", "FistForgedInShadowTorch",
                             "SonicSuperStarts", "Nocturnal", "TrinityFusion", "TalesOfVesperia",
                             "MegaManBattleNetwork", "Tinykin", "LegendOfTianding", "ZeldaLinkToThePast",
                             "ArtfulEscape", "Risen2", "FistForgedInShadow", "SoniColors", "Islets",
                             "Sanabi", "ExitTheGungeon", "SuperMarioRPG"]
            }
        self.displayed_games = self.all_games.copy()

    def save_games(self):
        data = {
            'all_games': self.all_games,
            'category_games': self.category_games
        }
        with open('games_data.json', 'w') as f:
            json.dump(data, f, indent=4)

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
            print(game)

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
                    print(original_game)
        else:
            print("Invalid category. Please try again.")

    def search_games(self):
        search_text = input("Enter part of the game name to search: ").strip().lower()
        matching_games = [game for game in self.all_games if search_text in game.lower()]

        if matching_games:
            print("\nMatching Games:")
            for game in matching_games:
                print(game)
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
            self.all_games.remove(game_to_delete)

            game_id = self.format_game_id(game_to_delete)
            for category in self.categories:
                if game_id in self.category_games[category]:
                    self.category_games[category].remove(game_id)

            self.save_games()
            print(f"'{game_to_delete}' has been deleted.")
        else:
            print("Invalid choice. Please try again.")

    def run_game(self):
        game_input = input("Enter the name of the game to run: ").strip()

        if not game_input:
            print("No game name entered. Please try again.")
            return

        # Attempt to find the game with exact match (case-insensitive)
        matched_games = [game for game in self.all_games if game.lower() == game_input.lower()]

        if not matched_games:
            # If exact match not found, try partial match
            matched_games = [game for game in self.all_games if game_input.lower() in game.lower()]

            if not matched_games:
                print("Game not found. Please try again.")
                return

        if len(matched_games) > 1:
            print("\nMultiple matching games found:")
            for i, game in enumerate(matched_games, start=1):
                print(f"{i}. {game}")
            choice = input("Choose a game to run: ").strip()

            if choice.isdigit() and 1 <= int(choice) <= len(matched_games):
                selected_game = matched_games[int(choice) - 1]
            else:
                print("Invalid choice. Please try again.")
                return
        else:
            selected_game = matched_games[0]

        # Prepare the formatted image name for volume path
        formatted_image_name = self.format_game_id(selected_game)

        # Docker image and container names should retain original casing
        docker_image_name = selected_game.replace(" ", "").replace(":", "").replace("'", "").replace("-", "").replace(".", "").replace(",", "")
        docker_container_name = docker_image_name

        docker_command = (
            f'docker run -v /srv/samba/shared/{formatted_image_name}:/c/games/{selected_game} '
            f'-it -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix --name {docker_container_name} '
            f'michadockermisha/backup:{docker_image_name} sh -c "apk add rsync && rsync -aP /home /c/games && mv /c/games/home /c/games/{selected_game}"'
        )
        print(f"Running Docker command: {docker_command}")
        try:
            subprocess.Popen(docker_command, shell=True)
            print(f"'{selected_game}' is now running in Docker.")
        except Exception as e:
            print(f"Failed to run Docker command: {e}")

    def get_original_game_name(self, game_id):
        """Helper method to retrieve the original game name from game_id."""
        for game in self.all_games:
            if self.format_game_id(game) == game_id:
                return game
        return None

    def format_game_id(self, game_name):
        """Helper method to format the game name for internal use (lowercase, no spaces)."""
        return ''.join(e for e in game_name.lower() if e.isalnum())

if __name__ == '__main__':
    DockerAppCLI()
