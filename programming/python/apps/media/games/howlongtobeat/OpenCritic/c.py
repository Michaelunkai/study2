import difflib
import requests
import tempfile
import os
from howlongtobeatpy import HowLongToBeat
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text
from rich import box

# rich now has an Image class to render images in supported terminals
try:
    from rich.image import Image as RichImage
except ImportError:
    RichImage = None

# Your RapidAPI/OpenCritic API Key and Host
API_KEY = "ec6dc2f95cmsh684f88e61fc1401p1b3a93jsn8f45e1822620"
OC_HOST = "opencritic-api.p.rapidapi.com"

console = Console()


def get_oc_search_results(game_query):
    """
    Searches OpenCritic for a given game query.
    Returns a list of game dictionaries (the raw JSON results).
    """
    search_url = "https://opencritic-api.p.rapidapi.com/game/search"
    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": OC_HOST
    }
    params = {"criteria": game_query}
    try:
        response = requests.get(search_url, headers=headers, params=params, timeout=10)
        if response.status_code == 200:
            results = response.json()
            if isinstance(results, list) and results:
                return results
            else:
                console.print("[red]No OpenCritic results found.[/red]")
        else:
            console.print(f"[red]OpenCritic search error: {response.status_code}[/red]")
    except Exception as e:
        console.print(f"[red]Exception during OC search: {e}[/red]")
    return []


def get_oc_game_details(game_id):
    """
    Fetches detailed info from OpenCritic for a given game id.
    (Using the endpoint that retrieves game details.)
    Returns a dictionary with all available details.
    """
    details_url = f"https://opencritic-api.p.rapidapi.com/game/{game_id}"
    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": OC_HOST
    }
    try:
        response = requests.get(details_url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            console.print(f"[red]Failed to fetch details (status: {response.status_code}).[/red]")
    except Exception as e:
        console.print(f"[red]Exception during fetching details: {e}[/red]")
    return {}


def get_hltb_results(game_query):
    """
    Uses howlongtobeatpy to search for the game and return a list of results.
    """
    try:
        results = HowLongToBeat().search(game_query)
        return results
    except Exception as e:
        console.print(f"[red]HLTB search error: {e}[/red]")
    return []


def choose_oc_game(oc_results):
    """
    If multiple OpenCritic results are returned, display them in a list and ask user which one they want.
    Returns the chosen game dictionary.
    """
    if not oc_results:
        return None

    # Create a list of game names for fuzzy matching
    names = [game.get("name", "Unknown") for game in oc_results]
    if len(oc_results) == 1:
        return oc_results[0]

    console.print("\n[bold cyan]Multiple OpenCritic games found:[/bold cyan]")
    table = Table(title="Search Results (OpenCritic)", box=box.SIMPLE)
    table.add_column("Index", justify="center")
    table.add_column("Game Title", style="yellow")
    table.add_column("Release Date", style="green")
    table.add_column("Platforms", style="magenta")

    for i, game in enumerate(oc_results):
        title = game.get("name", "N/A")
        release = str(game.get("releaseDate", "N/A"))
        platforms = ", ".join(game.get("platforms", [])) if game.get("platforms") else "N/A"
        table.add_row(str(i + 1), title, release, platforms)

    console.print(table)
    while True:
        choice = Prompt.ask("Choose the correct game number (or type 'exit' to cancel)")
        if choice.lower() in ["exit", "quit"]:
            return None
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(oc_results):
                return oc_results[idx]
        except Exception:
            pass
        console.print("[red]Invalid choice. Try again.[/red]")


def match_hltb_result(oc_game_name, hltb_results):
    """
    Tries to find the best matching HLTB result based on the chosen OpenCritic game name.
    Returns the best matching HLTB result or None.
    """
    if not hltb_results:
        return None

    hltb_names = [r.game_name for r in hltb_results]
    matches = difflib.get_close_matches(oc_game_name, hltb_names, n=1, cutoff=0.4)
    if matches:
        # Return the first match from hltb_results that exactly matches the fuzzy match name
        for res in hltb_results:
            if res.game_name == matches[0]:
                return res
    return None


def display_oc_details(oc_details):
    """
    Displays all available OpenCritic details in a well-formatted panel.
    """
    # Gather various details with defaults
    title = oc_details.get("name", "N/A")
    release_date = oc_details.get("releaseDate", "N/A")
    platforms = ", ".join(oc_details.get("platforms", [])) if oc_details.get("platforms") else "N/A"
    developer = oc_details.get("developer", "N/A")
    publisher = oc_details.get("publisher", "N/A")
    genre = ", ".join(oc_details.get("genre", [])) if oc_details.get("genre") else "N/A"
    oc_score = oc_details.get("topCriticScore", "N/A")
    recommended = oc_details.get("percentRecommended", "N/A")
    review_count = oc_details.get("reviewCount", "N/A")
    description = oc_details.get("description", "No description available.")
    background_image = oc_details.get("backgroundImage")

    info_text = Text()
    info_text.append(f"Title: {title}\n", style="bold yellow")
    info_text.append(f"Release Date: {release_date}\n", style="green")
    info_text.append(f"Platforms: {platforms}\n", style="magenta")
    info_text.append(f"Developer: {developer}\n", style="cyan")
    info_text.append(f"Publisher: {publisher}\n", style="cyan")
    info_text.append(f"Genre: {genre}\n", style="bright_blue")
    info_text.append(f"Critic Score: {oc_score}\n", style="bold")
    info_text.append(f"Recommended by {recommended}% of critics\n", style="bold")
    info_text.append(f"Review Count: {review_count}\n", style="bold")
    info_text.append("\nDescription:\n", style="underline")
    info_text.append(f"{description}\n")

    panel = Panel(info_text, title="OpenCritic Details", border_style="blue", expand=False)
    console.print(panel)
    
    return background_image


def display_hltb_details(hltb_result):
    """
    Displays HowLongToBeat details in a table.
    """
    table = Table(title="HowLongToBeat Estimates", box=box.ROUNDED)
    table.add_column("Type", justify="center", style="bold")
    table.add_column("Hours", justify="right", style="bright_magenta")

    main_story = hltb_result.main_story if hltb_result.main_story is not None else "N/A"
    main_extra = hltb_result.main_extra if hltb_result.main_extra is not None else "N/A"
    completionist = hltb_result.completionist if hltb_result.completionist is not None else "N/A"

    table.add_row("Main Story", str(main_story))
    table.add_row("Main + Extra", str(main_extra))
    table.add_row("Completionist", str(completionist))
    console.print(table)


def display_wallpaper(image_url):
    """
    Downloads and displays the game wallpaper using Rich Image, if supported.
    """
    if not image_url:
        console.print("[yellow]No wallpaper image available.[/yellow]")
        return

    try:
        # Download image data
        response = requests.get(image_url, timeout=10)
        if response.status_code == 200:
            # Use a temporary file to hold the image
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
                tmp_file.write(response.content)
                tmp_file.flush()
                tmp_filename = tmp_file.name

            if RichImage:
                rich_img = RichImage.from_path(tmp_filename)
                console.print(Panel(rich_img, title="Game Wallpaper", border_style="magenta"))
            else:
                console.print("[yellow]Rich image rendering not available.[/yellow]")
            os.unlink(tmp_filename)
        else:
            console.print("[red]Failed to download wallpaper image.[/red]")
    except Exception as e:
        console.print(f"[red]Error displaying wallpaper: {e}[/red]")


def main():
    console.rule("[bold green]Game Insight Toolkit[/bold green]", style="green")
    while True:
        game_query = Prompt.ask("\nEnter game name (or type 'exit' to quit)")
        if game_query.lower() in ["exit", "quit"]:
            console.print("\n[bold]Goodbye![/bold]")
            break

        # Get OpenCritic search results
        oc_results = get_oc_search_results(game_query)
        if not oc_results:
            console.print("[red]No results from OpenCritic. Try another query.[/red]")
            continue

        # Let the user choose from OpenCritic results
        chosen_oc = choose_oc_game(oc_results)
        if chosen_oc is None:
            continue

        # Using chosen OpenCritic game's id, fetch more detailed info:
        game_id = chosen_oc.get("id")
        oc_details = get_oc_game_details(game_id)
        if not oc_details:
            console.print("[red]Could not retrieve detailed OpenCritic info.[/red]")
            continue

        # Display the complete OpenCritic info
        wallpaper_url = display_oc_details(oc_details)

        # Now, search HowLongToBeat data for the game
        hltb_results = get_hltb_results(game_query)
        if not hltb_results:
            console.print("[yellow]No HowLongToBeat results found.[/yellow]")
        else:
            # Try matching the chosen OC game name with HLTB results:
            matched_hltb = match_hltb_result(oc_details.get("name", ""), hltb_results)
            if matched_hltb:
                display_hltb_details(matched_hltb)
            else:
                # If no clear fuzzy match, list available HLTB games and let the user choose.
                console.print("\n[bold cyan]Multiple HowLongToBeat matches found:[/bold cyan]")
                table = Table(title="HowLongToBeat Search Results", box=box.MINIMAL_DOUBLE_HEAD)
                table.add_column("Index", justify="center")
                table.add_column("Game Title", style="yellow")
                table.add_column("Main Story", justify="right", style="green")
                for idx, game in enumerate(hltb_results[:5]):  # show up to 5 results
                    table.add_row(str(idx + 1), game.game_name, str(game.main_story or "N/A"))
                console.print(table)
                choice = Prompt.ask("Choose HLTB result number (or type 'skip' to continue)", default="skip")
                if choice.lower() not in ["skip", "exit", "quit"]:
                    try:
                        idx = int(choice) - 1
                        if 0 <= idx < len(hltb_results):
                            display_hltb_details(hltb_results[idx])
                    except Exception:
                        console.print("[red]Invalid selection for HLTB data.[/red]")

        # Display wallpaper image if available
        display_wallpaper(wallpaper_url)


if __name__ == "__main__":
    main()

