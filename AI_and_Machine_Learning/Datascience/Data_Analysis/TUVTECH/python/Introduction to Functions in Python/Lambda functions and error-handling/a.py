import requests
import yt_dlp
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from rich.text import Text
import asyncio
import aiohttp
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.styles import Style
import nest_asyncio
import subprocess
import time
from functools import partial
import os
import platform
import logging
from datetime import datetime
import json
from typing import List, Dict, Optional
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('game_searcher.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

# Enable nested event loops
nest_asyncio.apply()

# Set up console for better UI
console = Console()

# RAWG API configuration
RAWG_API_KEY = "a0278acb920e45e1bcc232b06f72bace"
RAWG_BASE_URL = "https://api.rawg.io/api"

# Cache configuration
CACHE_DURATION = 3600  # 1 hour
CACHE_FILE = "game_cache.json"

class Cache:
    def __init__(self, filename: str):
        self.filename = filename
        self.cache = self.load_cache()

    def load_cache(self) -> dict:
        try:
            if os.path.exists(self.filename):
                with open(self.filename, 'r') as f:
                    cache = json.load(f)
                # Clean expired entries
                now = time.time()
                cache = {k: v for k, v in cache.items() 
                        if now - v.get('timestamp', 0) < CACHE_DURATION}
                return cache
        except Exception as e:
            logging.warning(f"Cache load error: {e}")
        return {}

    def save_cache(self):
        try:
            with open(self.filename, 'w') as f:
                json.dump(self.cache, f)
        except Exception as e:
            logging.warning(f"Cache save error: {e}")

    def get(self, key: str) -> Optional[dict]:
        if key in self.cache:
            data = self.cache[key]
            if time.time() - data.get('timestamp', 0) < CACHE_DURATION:
                return data.get('value')
        return None

    def set(self, key: str, value: dict):
        self.cache[key] = {
            'value': value,
            'timestamp': time.time()
        }
        self.save_cache()

class GameSuggester:
    def __init__(self):
        self.session = aiohttp.ClientSession()
        self.cache = Cache(CACHE_FILE)
        self.last_search = ""
        self.last_fetch_time = 0
        
    async def close(self):
        await self.session.close()

    def preprocess_query(self, text: str) -> str:
        """Clean and standardize search query"""
        return text.strip().lower()

    async def get_suggestions(self, text: str) -> List[Dict]:
        """Fetch game suggestions from RAWG API with improved matching"""
        if not text or len(text) < 2:
            return []

        text = self.preprocess_query(text)
        cache_key = f"suggest_{text}"
        cached = self.cache.get(cache_key)
        if cached:
            return cached

        url = f"{RAWG_BASE_URL}/games"
        params = {
            "key": RAWG_API_KEY,
            "search": text,
            "page_size": 10,  # Increased for better matches
            "ordering": "-metacritic,-rating,-released"  # Prioritize well-rated recent games
        }

        try:
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    suggestions = []
                    for game in data.get('results', []):
                        name = game['name']
                        released = game.get('released', 'TBA')
                        rating = game.get('rating', 0)
                        metacritic = game.get('metacritic', 'N/A')
                        platforms = [p['platform']['name'] for p in game.get('platforms', [])]
                        
                        # Calculate relevance score
                        relevance = self._calculate_relevance(text, game)
                        
                        suggestions.append({
                            'name': name,
                            'display': f"{name} ({released}) - {', '.join(platforms[:3])}",
                            'rating': rating,
                            'metacritic': metacritic,
                            'relevance': relevance,
                            'platforms': platforms
                        })
                    
                    # Sort by relevance and limit results
                    suggestions.sort(key=lambda x: x['relevance'], reverse=True)
                    suggestions = suggestions[:5]
                    
                    self.cache.set(cache_key, suggestions)
                    return suggestions
                else:
                    logging.error(f"API error: {response.status}")
        except Exception as e:
            logging.error(f"Suggestion fetch error: {str(e)}")
        return []

    def _calculate_relevance(self, query: str, game: dict) -> float:
        """Calculate game relevance score based on multiple factors"""
        score = 0.0
        name_lower = game['name'].lower()
        
        # Exact match bonus
        if query == name_lower:
            score += 10.0
        # Starts with bonus
        elif name_lower.startswith(query):
            score += 5.0
        # Contains bonus
        elif query in name_lower:
            score += 3.0

        # Rating bonus
        score += game.get('rating', 0) * 0.5
        # Metacritic bonus
        score += (game.get('metacritic', 0) or 0) * 0.02
        # Recent release bonus
        if game.get('released'):
            try:
                release_date = datetime.strptime(game['released'], '%Y-%m-%d')
                years_old = (datetime.now() - release_date).days / 365
                score += max(0, 2 - years_old)  # Bonus for newer games
            except:
                pass

        return score

class GameCompleter(Completer):
    def __init__(self):
        self.suggester = GameSuggester()
        
    async def get_completions_async(self, document, complete_event):
        text = document.text_before_cursor
        suggestions = await self.suggester.get_suggestions(text)
        
        for suggestion in suggestions:
            yield Completion(
                suggestion['name'],
                start_position=-len(text),
                display=HTML(
                    f'<skyblue>{suggestion["display"]}</skyblue>'
                    f'<gray> | Metacritic: {suggestion["metacritic"]}</gray>'
                ),
                display_meta=f"Rating: {suggestion['rating']}/5"
            )
            
    def get_completions(self, document, complete_event):
        return asyncio.run_coroutine_threadsafe(
            self.get_completions_async(document, complete_event),
            asyncio.get_event_loop()
        ).result()

class GameSearcher:
    def __init__(self):
        self.session = requests.Session()
        self.cache = Cache(CACHE_FILE)
        
    def search_game(self, game_name: str) -> Optional[dict]:
        """Search for a game with improved error handling and caching"""
        cache_key = f"game_{game_name.lower()}"
        cached = self.cache.get(cache_key)
        if cached:
            return cached

        url = f"{RAWG_BASE_URL}/games"
        params = {
            "key": RAWG_API_KEY,
            "search": game_name,
            "page_size": 1,
            "search_precise": True
        }
        
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            results = response.json().get("results", [])
            if results:
                self.cache.set(cache_key, results[0])
                return results[0]
        except requests.exceptions.Timeout:
            console.print("[red]Request timed out. Please check your internet connection.[/red]")
        except requests.exceptions.RequestException as e:
            console.print(f"[red]Error searching for game: {str(e)}[/red]")
        except Exception as e:
            logging.error(f"Unexpected error in game search: {str(e)}")
        return None

    def get_gameplay_video(self, game_name: str) -> Optional[str]:
        """Get gameplay video URL with improved search strategies"""
        search_queries = [
            f"{game_name} official gameplay {datetime.now().year}",
            f"{game_name} gameplay walkthrough {datetime.now().year}",
            f"{game_name} gameplay trailer HD",
            f"{game_name} official trailer",
            f"{game_name} game review"
        ]
        
        ydl_opts = {
            'format': 'best[height<=1080]',
            'quiet': True,
            'no_warnings': True,
            'extract_flat': True,
            'default_search': 'ytsearch1:',
            'socket_timeout': 10,
        }
        
        for query in search_queries:
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(f"ytsearch1:{query}", download=False)
                    if info and 'entries' in info and info['entries']:
                        return info['entries'][0]['url']
            except Exception as e:
                logging.warning(f"Video search error for '{query}': {str(e)}")
                continue
        return None

    def play_video(self, video_url: str) -> bool:
        """Play video with expanded player support and better error handling"""
        system = platform.system().lower()
        
        # System-specific player configurations
        players = {
            'linux': [
                ['mpv', '--force-window=yes', '--really-quiet'],
                ['vlc', '--play-and-exit', '--fullscreen'],
                ['ffplay', '-autoexit', '-loglevel', 'quiet']
            ],
            'darwin': [  # macOS
                ['open', '-a', 'QuickTime Player'],
                ['open', '-a', 'VLC'],
                ['mpv', '--force-window=yes', '--really-quiet']
            ],
            'windows': [
                ['start', 'wmplayer'],
                ['start', 'vlc'],
                ['mpv', '--force-window=yes', '--really-quiet']
            ]
        }
        
        current_players = players.get(system, players['linux'])
        
        for player_cmd in current_players:
            try:
                if system == 'windows' and player_cmd[0] == 'start':
                    os.system(f'start "" "{video_url}"')
                else:
                    subprocess.run([*player_cmd, video_url], 
                                 check=True, 
                                 stderr=subprocess.DEVNULL, 
                                 stdout=subprocess.DEVNULL)
                return True
            except Exception as e:
                logging.debug(f"Player {player_cmd[0]} failed: {str(e)}")
                continue

        console.print(f"\n[yellow]No video player found. Video URL: {video_url}[/yellow]")
        return False

    def display_game_details(self, game: dict):
        """Display comprehensive game information with improved formatting"""
        # Create title with release year
        release_year = game.get("released", "TBA").split("-")[0] if game.get("released") else "TBA"
        title = f"🎮 {game.get('name', 'Unknown Game')} ({release_year})"
        
        table = Table(title=title, title_style="bold magenta", box=None)
        
        table.add_column("", style="cyan", no_wrap=True)
        table.add_column("", style="green")
        
        # Detailed information
        details = [
            ("📅 Released", game.get("released", "TBA")),
            ("⭐ Rating", f"{game.get('rating', 'N/A')}/5.0"),
            ("🎯 Metacritic", f"{game.get('metacritic', 'N/A')}/100" if game.get('metacritic') else "N/A"),
            ("🎲 Genres", ", ".join(g["name"] for g in game.get("genres", []))),
            ("💻 Platforms", ", ".join(p["platform"]["name"] for p in game.get("platforms", []))),
            ("🏢 Publishers", ", ".join(p["name"] for p in game.get("publishers", []))),
            ("👨‍💻 Developers", ", ".join(d["name"] for d in game.get("developers", [])))
        ]
        
        for attr, value in details:
            table.add_row(attr, str(value))
        
        # Create a panel with the table and description
        description = game.get("description_raw", "No description available.")
        description = Text.from_markup(f"\n[dim]{description[:500]}{'...' if len(description) > 500 else ''}[/dim]")
        
        panel = Panel(
            Table(
                table,
                Text("\n"),
                description,
                show_header=False,
                show_edge=False,
                box=None
            ),
            title="Game Details",
            border_style="blue"
        )
        
        console.print(panel)

[Previous code remains exactly the same until the main() function, then continues with:]

async def main():
    """Enhanced main function with better error handling and user experience"""
    try:
        # Initialize components
        searcher = GameSearcher()
        session = PromptSession(
            completer=GameCompleter(),
            complete_while_typing=True,
            style=Style.from_dict({
                'completion-menu.completion': 'bg:#008888 #ffffff',
                'completion-menu.completion.current': 'bg:#00aaaa #000000',
            })
        )
        
        # Clear screen and show welcome message
        console.clear()
        console.print(Panel.fit(
            "[bold blue]🎮 Advanced Game Search & Preview System[/bold blue]\n" +
            "[yellow]Start typing to see smart game suggestions. Use arrow keys to navigate.[/yellow]\n" +
            "[dim]Press Ctrl+C to cancel current operation, Ctrl+D to exit[/dim]",
            border_style="blue"
        ))
        
        while True:
            try:
                # Get input with autocompletion
                game_name = await session.prompt_async(
                    "\nEnter game name (or 'quit' to exit): "
                )
                
                if game_name.lower() in ('quit', 'exit'):
                    break
                
                # Progress bar with spinner
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    console=console
                ) as progress:
                    # Search for game
                    search_task = progress.add_task("[cyan]Searching for game...", total=1)
                    game = searcher.search_game(game_name)
                    progress.update(search_task, completed=1)

                    if game:
                        # Display game details
                        searcher.display_game_details(game)
                        
                        # Search for gameplay video
                        video_task = progress.add_task("[green]Finding gameplay video...", total=1)
                        video_url = searcher.get_gameplay_video(game["name"])
                        progress.update(video_task, completed=1)
                        
                        if video_url:
                            # Attempt to play video
                            console.print("\n[bold green]Playing gameplay video...[/bold green]")
                            if not searcher.play_video(video_url):
                                console.print(Panel(
                                    f"[yellow]Could not play video automatically.\nVideo URL: {video_url}[/yellow]",
                                    title="Video Playback",
                                    border_style="yellow"
                                ))
                        else:
                            console.print(Panel(
                                "[yellow]No gameplay video found for this game.[/yellow]",
                                title="Video Search",
                                border_style="yellow"
                            ))
                    else:
                        console.print(Panel(
                            "[red]Game not found. Please try another search.[/red]",
                            title="Search Error",
                            border_style="red"
                        ))
                
                console.print("\n" + "=" * 60 + "\n")
                
            except KeyboardInterrupt:
                console.print("\n[yellow]Search cancelled.[/yellow]")
                continue
            except EOFError:
                break
            except Exception as e:
                logging.error(f"Unexpected error: {str(e)}")
                console.print(f"[red]An unexpected error occurred: {str(e)}[/red]")
                continue
    
    finally:
        # Clean up
        try:
            # Close the suggester session if it was created
            if 'session' in locals() and hasattr(session.completer.suggester, 'session'):
                await session.completer.suggester.close()
        except Exception as e:
            logging.error(f"Error during cleanup: {str(e)}")

def setup_environment():
    """Set up the environment for the application"""
    # Create cache directory if it doesn't exist
    cache_dir = os.path.dirname(CACHE_FILE)
    if cache_dir and not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
    
    # Set up asyncio policy for Windows compatibility
    if platform.system() == 'Windows':
        if hasattr(asyncio, 'WindowsSelectorEventLoopPolicy'):
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    # Configure logging directory
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Additional platform-specific setup
    if platform.system() == 'Linux':
        # Set up proper encoding for Linux systems
        import locale
        locale.setlocale(locale.LC_ALL, '')

if __name__ == "__main__":
    try:
        # Set up the environment
        setup_environment()
        
        # Run the main application
        asyncio.run(main())
    except KeyboardInterrupt:
        console.print("\n[yellow]Application terminated by user.[/yellow]")
    except Exception as e:
        console.print(f"\n[red]Fatal error: {str(e)}[/red]")
        logging.critical(f"Fatal error: {str(e)}")
        sys.exit(1)
    finally:
        console.print("\n[green]Thank you for using the Game Search & Preview System![/green]")_
