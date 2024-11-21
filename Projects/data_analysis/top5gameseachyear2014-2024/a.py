# Import necessary libraries
import pandas as pd
from tabulate import tabulate

# Create a dictionary with the data
games_data = {
    "2014": [
        {"title": "Dragon Age: Inquisition", "developer": "BioWare", "publisher": "Electronic Arts", "awards": ["The Game Awards: Game of the Year", "D.I.C.E. Awards: Game of the Year"]},
        {"title": "Middle-earth: Shadow of Mordor", "developer": "Monolith Productions", "publisher": "Warner Bros. Interactive Entertainment", "awards": ["Game Developers Choice Awards: Game of the Year"]},
        {"title": "Bayonetta 2", "developer": "PlatinumGames", "publisher": "Nintendo", "awards": ["The Game Awards: Best Action Game"]},
        {"title": "Hearthstone: Heroes of Warcraft", "developer": "Blizzard Entertainment", "publisher": "Blizzard Entertainment", "awards": ["D.I.C.E. Awards: Mobile Game of the Year"]},
        {"title": "Mario Kart 8", "developer": "Nintendo EAD", "publisher": "Nintendo", "awards": ["The Game Awards: Best Family Game"]}
    ],
    "2015": [
        {"title": "The Witcher 3: Wild Hunt", "developer": "CD Projekt Red", "publisher": "CD Projekt", "awards": ["The Game Awards: Game of the Year", "D.I.C.E. Awards: Game of the Year"]},
        {"title": "Bloodborne", "developer": "FromSoftware", "publisher": "Sony Computer Entertainment", "awards": ["Game Developers Choice Awards: Best Design"]},
        {"title": "Metal Gear Solid V: The Phantom Pain", "developer": "Kojima Productions", "publisher": "Konami", "awards": ["The Game Awards: Best Action/Adventure"]},
        {"title": "Fallout 4", "developer": "Bethesda Game Studios", "publisher": "Bethesda Softworks", "awards": ["D.I.C.E. Awards: Game of the Year"]},
        {"title": "Rocket League", "developer": "Psyonix", "publisher": "Psyonix", "awards": ["The Game Awards: Best Independent Game"]}
    ],
    "2016": [
        {"title": "Overwatch", "developer": "Blizzard Entertainment", "publisher": "Blizzard Entertainment", "awards": ["The Game Awards: Game of the Year", "D.I.C.E. Awards: Game of the Year"]},
        {"title": "Uncharted 4: A Thief's End", "developer": "Naughty Dog", "publisher": "Sony Interactive Entertainment", "awards": ["The Game Awards: Best Narrative"]},
        {"title": "Doom", "developer": "id Software", "publisher": "Bethesda Softworks", "awards": ["The Game Awards: Best Action Game"]},
        {"title": "Inside", "developer": "Playdead", "publisher": "Playdead", "awards": ["Game Developers Choice Awards: Game of the Year"]},
        {"title": "Titanfall 2", "developer": "Respawn Entertainment", "publisher": "Electronic Arts", "awards": ["The Game Awards: Best Action Game"]}
    ],
    "2017": [
        {"title": "The Legend of Zelda: Breath of the Wild", "developer": "Nintendo EPD", "publisher": "Nintendo", "awards": ["The Game Awards: Game of the Year", "D.I.C.E. Awards: Game of the Year"]},
        {"title": "Super Mario Odyssey", "developer": "Nintendo EPD", "publisher": "Nintendo", "awards": ["The Game Awards: Best Family Game"]},
        {"title": "Persona 5", "developer": "P-Studio", "publisher": "Atlus", "awards": ["The Game Awards: Best Role Playing Game"]},
        {"title": "Horizon Zero Dawn", "developer": "Guerrilla Games", "publisher": "Sony Interactive Entertainment", "awards": ["D.I.C.E. Awards: Outstanding Achievement in Story"]},
        {"title": "Cuphead", "developer": "Studio MDHR", "publisher": "Studio MDHR", "awards": ["The Game Awards: Best Independent Game"]}
    ],
    "2018": [
        {"title": "God of War", "developer": "Santa Monica Studio", "publisher": "Sony Interactive Entertainment", "awards": ["The Game Awards: Game of the Year", "D.I.C.E. Awards: Game of the Year"]},
        {"title": "Red Dead Redemption 2", "developer": "Rockstar Games", "publisher": "Rockstar Games", "awards": ["The Game Awards: Best Narrative"]},
        {"title": "Marvel's Spider-Man", "developer": "Insomniac Games", "publisher": "Sony Interactive Entertainment", "awards": ["D.I.C.E. Awards: Outstanding Achievement in Animation"]},
        {"title": "Celeste", "developer": "Maddy Makes Games", "publisher": "Maddy Makes Games", "awards": ["The Game Awards: Best Independent Game"]},
        {"title": "Monster Hunter: World", "developer": "Capcom", "publisher": "Capcom", "awards": ["The Game Awards: Best Role Playing Game"]}
    ],
    "2019": [
        {"title": "Sekiro: Shadows Die Twice", "developer": "FromSoftware", "publisher": "Activision", "awards": ["The Game Awards: Game of the Year", "D.I.C.E. Awards: Game of the Year"]},
        {"title": "Death Stranding", "developer": "Kojima Productions", "publisher": "Sony Interactive Entertainment", "awards": ["The Game Awards: Best Game Direction"]},
        {"title": "Control", "developer": "Remedy Entertainment", "publisher": "505 Games", "awards": ["D.I.C.E. Awards: Action Game of the Year"]},
        {"title": "Resident Evil 2", "developer": "Capcom", "publisher": "Capcom", "awards": ["The Game Awards: Best Action/Adventure"]},
        {"title": "Disco Elysium", "developer": "ZA/UM", "publisher": "ZA/UM", "awards": ["The Game Awards: Best Independent Game"]}
    ],
    "2020": [
        {"title": "The Last of Us Part II", "developer": "Naughty Dog", "publisher": "Sony Interactive Entertainment", "awards": ["The Game Awards: Game of the Year"]},
        {"title": "Hades", "developer": "Supergiant Games", "publisher": "Supergiant Games", "awards": ["The Game Awards: Best Independent Game"]},
        {"title": "Ghost of Tsushima", "developer": "Sucker Punch Productions", "publisher": "Sony Interactive Entertainment", "awards": ["The Game Awards: Player's Voice"]},
        {"title": "Animal Crossing: New Horizons", "developer": "Nintendo", "publisher": "Nintendo", "awards": ["D.I.C.E. Awards: Game of the Year"]},
        {"title": "Doom Eternal", "developer": "id Software", "publisher": "Bethesda Softworks", "awards": ["The Game Awards: Best Action Game"]}
    ],
    "2021": [
        {"title": "It Takes Two", "developer": "Hazelight Studios", "publisher": "Electronic Arts", "awards": ["The Game Awards: Game of the Year"]},
        {"title": "Resident Evil Village", "developer": "Capcom", "publisher": "Capcom", "awards": ["The Game Awards: Best Performance"]},
        {"title": "Metroid Dread", "developer": "MercurySteam", "publisher": "Nintendo", "awards": ["The Game Awards: Best Action/Adventure"]},
        {"title": "Deathloop", "developer": "Arkane Studios", "publisher": "Bethesda Softworks", "awards": ["The Game Awards: Best Game Direction"]},
        {"title": "Forza Horizon 5", "developer": "Playground Games", "publisher": "Xbox Game Studios", "awards": ["The Game Awards: Best Sports/Racing Game"]}
    ],
    "2022": [
        {"title": "Elden Ring", "developer": "FromSoftware", "publisher": "Bandai Namco Entertainment", "awards": ["The Game Awards: Game of the Year"]},
        {"title": "God of War Ragnarök", "developer": "Santa Monica Studio", "publisher": "Sony Interactive Entertainment", "awards": ["The Game Awards: Best Narrative"]},
        {"title": "Horizon Forbidden West", "developer": "Guerrilla Games", "publisher": "Sony Interactive Entertainment", "awards": ["D.I.C.E. Awards: Outstanding Achievement in Story"]},
        {"title": "Stray", "developer": "BlueTwelve Studio", "publisher": "Annapurna Interactive", "awards": ["The Game Awards: Best Independent Game"]},
        {"title": "Xenoblade Chronicles 3", "developer": "Monolith Soft", "publisher": "Nintendo", "awards": ["The Game Awards: Best Role Playing Game"]}
    ],
    "2023": [
        {"title": "The Legend of Zelda: Tears of the Kingdom", "developer": "Nintendo EPD", "publisher": "Nintendo", "awards": ["The Game Awards: Game of the Year (Nominated)"]},
        {"title": "Baldur's Gate 3", "developer": "Larian Studios", "publisher": "Larian Studios", "awards": ["The Game Awards: Best Role Playing Game (Nominated)"]},
        {"title": "Starfield", "developer": "Bethesda Game Studios", "publisher": "Xbox Game Studios", "awards": ["The Game Awards: Best Game Direction (Nominated)"]},
        {"title": "Armored Core VI: Fires of Rubicon", "developer": "FromSoftware", "publisher": "Bandai Namco Entertainment", "awards": ["The Game Awards: Best Action Game (Nominated)"]},
        {"title": "Final Fantasy XVI", "developer": "Square Enix", "publisher": "Square Enix", "awards": ["The Game Awards: Best Performance (Nominated)"]}
    ],
    "2024": [
        {"title": "Avowed", "developer": "Obsidian Entertainment", "publisher": "Xbox Game Studios", "awards": ["Upcoming Release"]},
        {"title": "Hellblade II: Senua's Saga", "developer": "Ninja Theory", "publisher": "Xbox Game Studios", "awards": ["Upcoming Release"]},
        {"title": "Everwild", "developer": "Rare", "publisher": "Xbox Game Studios", "awards": ["Upcoming Release"]},
        {"title": "Fable", "developer": "Playground Games", "publisher": "Xbox Game Studios", "awards": ["Upcoming Release"]},
        {"title": "The Outer Worlds 2", "developer": "Obsidian Entertainment", "publisher": "Private Division", "awards": ["Upcoming Release"]}
    ]
}

# Function to create a formatted chart-like output
def create_chart(data):
    chart = []
    for year, games in data.items():
        for game in games:
            chart.append([
                year,
                game["title"],
                game["developer"],
                game["publisher"],
                ", ".join(game["awards"])
            ])
    headers = ["Year", "Title", "Developer", "Publisher", "Awards"]
    print(tabulate(chart, headers=headers, tablefmt="grid"))

# Output the analysis in chart format
create_chart(games_data)
