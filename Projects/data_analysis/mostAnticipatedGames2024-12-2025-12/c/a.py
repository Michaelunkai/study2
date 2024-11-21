import tkinter as tk
from tkinter import ttk
from datetime import datetime

# Define a list of dictionaries, each containing details about an anticipated game
anticipated_games = [
    {
        "title": "Indiana Jones and the Great Circle",
        "release_date": "December 9, 2024",
        "developer": "MachineGames",
        "publisher": "Bethesda Softworks",
        "platforms": ["Xbox Series X/S", "PC", "PlayStation 5 (Spring 2025)"],
        "description": (
            "An action-adventure game where players embark on a thrilling journey "
            "with Indiana Jones, featuring exploration, puzzle-solving, and combat."
        )
    },
    {
        "title": "Sid Meier's Civilization VII",
        "release_date": "February 11, 2025",
        "developer": "Firaxis Games",
        "publisher": "2K Games",
        "platforms": ["PC"],
        "description": (
            "The next installment in the acclaimed turn-based strategy series, offering new civilizations, "
            "mechanics, and enhanced gameplay depth."
        )
    },
    {
        "title": "Assassin's Creed Shadows",
        "release_date": "February 14, 2025",
        "developer": "Ubisoft Quebec",
        "publisher": "Ubisoft",
        "platforms": ["PlayStation 5", "Xbox Series X/S", "PC"],
        "description": (
            "A new chapter in the Assassin's Creed franchise, set in feudal Japan, featuring a new protagonist and storyline."
        )
    },
    {
        "title": "Monster Hunter Wilds",
        "release_date": "February 28, 2025",
        "developer": "Capcom",
        "publisher": "Capcom",
        "platforms": ["To be announced"],
        "description": (
            "A new entry in the Monster Hunter series, introducing expansive wild environments, "
            "new monsters, and refined hunting mechanics."
        )
    },
    {
        "title": "Silent Hill: Rebirth",
        "release_date": "October 2025",
        "developer": "Bloober Team",
        "publisher": "Konami",
        "platforms": ["PlayStation 5", "PC"],
        "description": (
            "A reimagining of the classic survival horror game, offering psychological terror and a haunting atmosphere."
        )
    },
    {
        "title": "Elder Scrolls VI",
        "release_date": "December 2025",
        "developer": "Bethesda Game Studios",
        "publisher": "Bethesda Softworks",
        "platforms": ["To be announced"],
        "description": (
            "The next major installment in the Elder Scrolls series, promising a vast and immersive fantasy world."
        )
    },
    {
        "title": "Hogwarts Legacy: Year 2",
        "release_date": "December 2025",
        "developer": "Portkey Games",
        "publisher": "Warner Bros. Interactive Entertainment",
        "platforms": ["PlayStation 5", "Xbox Series X/S", "PC"],
        "description": (
            "A sequel to Hogwarts Legacy, where players return to the magical school for a new year of spells, "
            "adventures, and mysteries."
        )
    },
    {
        "title": "Grand Theft Auto VI",
        "release_date": "2025",
        "developer": "Rockstar Games",
        "publisher": "Rockstar Games",
        "platforms": ["PlayStation 5", "Xbox Series X/S"],
        "description": (
            "The highly anticipated next entry in the Grand Theft Auto series, expected to deliver "
            "an expansive open world with immersive storytelling and gameplay."
        )
    },
    {
        "title": "Death Stranding 2: On the Beach",
        "release_date": "2025",
        "developer": "Kojima Productions",
        "publisher": "Sony Interactive Entertainment",
        "platforms": ["PlayStation 5"],
        "description": (
            "The sequel to Hideo Kojima's enigmatic action game, continuing the story of Sam Porter Bridges "
            "in a post-apocalyptic world."
        )
    },
    {
        "title": "Doom: The Dark Ages",
        "release_date": "2025",
        "developer": "id Software",
        "publisher": "Bethesda Softworks",
        "platforms": ["PlayStation 5", "Windows", "Xbox Series X/S"],
        "description": (
            "A new installment in the Doom franchise, exploring the rise of the Doom Slayer in a dark fantasy setting."
        )
    },
    {
        "title": "Pokémon Legends: Z-A",
        "release_date": "2025",
        "developer": "Game Freak",
        "publisher": ["Nintendo", "The Pokémon Company"],
        "platforms": ["Nintendo Switch"],
        "description": (
            "A new installment in the Pokémon Legends series, set in the Kalos region, "
            "offering an open-world experience with classic Pokémon gameplay elements."
        )
    },
    {
        "title": "Hell Is Us",
        "release_date": "2025",
        "developer": "Rogue Factor",
        "publisher": "Nacon",
        "platforms": ["Microsoft Windows", "PlayStation 5", "Xbox Series X/S"],
        "description": (
            "An action-adventure game where players combat supernatural beings in a semi-open world, "
            "focusing on exploration and melee combat."
        )
    },
    {
        "title": "Borderlands 4",
        "release_date": "2025",
        "developer": "Gearbox Software",
        "publisher": "2K Games",
        "platforms": ["PlayStation 5", "Xbox Series X/S", "PC"],
        "description": (
            "The next installment in the Borderlands series, offering new characters, "
            "weapons, and an expansive storyline in the looter-shooter genre."
        )
    },
    {
        "title": "Fable",
        "release_date": "2025",
        "developer": "Playground Games",
        "publisher": "Xbox Game Studios",
        "platforms": ["Xbox Series X/S", "PC"],
        "description": (
            "A reboot of the beloved fantasy RPG series, featuring an expansive open world, "
            "humor, and player-driven storytelling."
        )
    },
    {
        "title": "Final Fantasy XVI: Eternal Realms",
        "release_date": "2025",
        "developer": "Square Enix",
        "publisher": "Square Enix",
        "platforms": ["PlayStation 5"],
        "description": (
            "A continuation of the epic Final Fantasy XVI saga, exploring new realms, "
            "characters, and adventures."
        )
    },
    {
        "title": "Metroid Prime 4",
        "release_date": "2025",
        "developer": "Retro Studios",
        "publisher": "Nintendo",
        "platforms": ["Nintendo Switch"],
        "description": (
            "The long-awaited sequel in the Metroid Prime series, delivering intense first-person action and exploration."
        )
    },
    {
        "title": "Star Wars Eclipse",
        "release_date": "2025",
        "developer": "Quantic Dream",
        "publisher": "Lucasfilm Games",
        "platforms": ["PlayStation 5", "Xbox Series X/S", "PC"],
        "description": (
            "An action-adventure game set in the High Republic era of the Star Wars universe, "
            "with branching narratives and player-driven choices."
        )
    },
    {
        "title": "Dragon Age: Dreadwolf",
        "release_date": "2025",
        "developer": "BioWare",
        "publisher": "Electronic Arts",
        "platforms": ["PlayStation 5", "Xbox Series X/S", "PC"],
        "description": (
            "The next chapter in the Dragon Age series, focusing on the mysterious Dreadwolf and the fate of Thedas."
        )
    },
    {
        "title": "Mass Effect 5",
        "release_date": "2025",
        "developer": "BioWare",
        "publisher": "Electronic Arts",
        "platforms": ["PlayStation 5", "Xbox Series X/S", "PC"],
        "description": (
            "A new entry in the Mass Effect series, promising a return to deep space exploration, "
            "galactic mysteries, and engaging character interactions."
        )
    },
    {
        "title": "Hades II",
        "release_date": "Q4 2025",
        "developer": "Supergiant Games",
        "publisher": "Supergiant Games",
        "platforms": ["PC", "PlayStation 5", "Xbox Series X/S"],
        "description": (
            "The sequel to the critically acclaimed roguelike, Hades, with new gods, challenges, "
            "and an expanded underworld."
        )
    }
]

# Function to parse release dates for sorting
def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%B %d, %Y")
    except ValueError:
        try:
            return datetime.strptime(date_str, "%B %Y")
        except ValueError:
            return datetime.max

# Sort games by release date
anticipated_games.sort(key=lambda game: parse_date(game["release_date"]))

# Create the main window
root = tk.Tk()
root.title("Top 20 Most Anticipated Games (2024-2025)")

# Create a treeview to display the game data
tree = ttk.Treeview(root, columns=("Title", "Release Date", "Developer", "Publisher", "Platforms", "Description"), show="headings")
tree.heading("Title", text="Title")
tree.heading("Release Date", text="Release Date")
tree.heading("Developer", text="Developer")
tree.heading("Publisher", text="Publisher")
tree.heading("Platforms", text="Platforms")
tree.heading("Description", text="Description")
tree.column("Title", width=150)
tree.column("Release Date", width=100)
tree.column("Developer", width=150)
tree.column("Publisher", width=150)
tree.column("Platforms", width=200)
tree.column("Description", width=400)

# Add game data to the treeview
for game in anticipated_games:
    publisher = ", ".join(game["publisher"]) if isinstance(game["publisher"], list) else game["publisher"]
    platforms = ", ".join(game["platforms"])
    tree.insert("", "end", values=(game["title"], game["release_date"], game["developer"], publisher, platforms, game["description"]))

# Pack the treeview into the window
tree.pack(fill="both", expand=True)

# Run the main event loop
root.mainloop()
