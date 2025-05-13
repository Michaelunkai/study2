from howlongtobeatpy import HowLongToBeat
import difflib
import requests
from PIL import Image
from io import BytesIO
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box

API_KEY = "ec6dc2f95cmsh684f88e61fc1401p1b3a93jsn8f45e1822620"
console = Console()

def search_hltb(game_name):
    results = HowLongToBeat().search(game_name)
    if not results:
        return None
    names = [r.game_name for r in results]
    matches = difflib.get_close_matches(game_name, names, n=3, cutoff=0.4)
    if not matches:
        return None
    if len(matches) == 1:
        return next(g for g in results if g.game_name == matches[0])
    console.print("\nMultiple matches found:", style="bold cyan")
    for i, name in enumerate(matches):
        console.print(f"{i + 1}. {name}")
    try:
        choice = int(input("Choose the correct one (1/2/3): ").strip())
        if 1 <= choice <= len(matches):
            return next(g for g in results if g.game_name == matches[choice - 1])
    except:
        return None
    return None

def fetch_opencritic(game_name):
    search_url = "https://opencritic-api.p.rapidapi.com/game/search"
    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": "opencritic-api.p.rapidapi.com"
    }
    params = {"criteria": game_name}
    res = requests.get(search_url, headers=headers, params=params)
    if res.status_code != 200 or not res.json():
        return None
    game = res.json()[0]
    game_id = game['id']
    details_url = f"https://opencritic-api.p.rapidapi.com/game/{game_id}"
    details_res = requests.get(details_url, headers=headers)
    if details_res.status_code != 200:
        return None
    return details_res.json()

def show_game_image(image_url):
    try:
        img_data = requests.get(image_url).content
        img = Image.open(BytesIO(img_data)).resize((50, 25))
        console.print("[bold magenta]Game Art:[/bold magenta]")
        console.print()
        console.print(Image.fromarray(img.convert('RGB')), overflow="ignore")
    except Exception as e:
        console.print(f"[red]Image error:[/red] {e}")

def main():
    while True:
        game_name = input("\nEnter game name (or 'exit'): ").strip()
        if game_name.lower() in ["exit", "quit"]:
            break

        hltb = search_hltb(game_name)
        oc = fetch_opencritic(game_name)

        if not hltb:
            console.print("❌ [red]No match found in HowLongToBeat.[/red]")
            continue

        console.rule(f"[bold green]{hltb.game_name}[/bold green]", characters="=")
        
        table = Table(title="Game Completion Times", box=box.ROUNDED)
        table.add_column("Type")
        table.add_column("Hours", justify="right")
        table.add_row("Main Story", f"{hltb.main_story or 'N/A'}")
        table.add_row("Main + Extra", f"{hltb.main_extra or 'N/A'}")
        table.add_row("Completionist", f"{hltb.completionist or 'N/A'}")
        console.print(table)

        if oc:
            score = oc.get("topCriticScore")
            rec_percent = oc.get("percentRecommended")
            oc_name = oc.get("name")
            art = oc.get("backgroundImage")
            summary = f"⭐ Critic Score: {score}\n✅ Recommended: {rec_percent}%"
            console.print(Panel(summary, title="OpenCritic", subtitle=oc_name, style="cyan"))

            if art:
                show_game_image(art)
        else:
            console.print("[yellow]No OpenCritic data found.[/yellow]")

if __name__ == "__main__":
    main()
