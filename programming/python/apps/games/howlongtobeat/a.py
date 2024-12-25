import pandas as pd
import os
import subprocess
import requests
from bs4 import BeautifulSoup
from youtube_search import YoutubeSearch
from datetime import datetime

# Load dataset
def load_dataset():
    file_path = "/root/howlongtobeat_dataset/games.csv"
    if not os.path.exists(file_path):
        print("Dataset file not found! Ensure the dataset is downloaded and extracted.")
        exit(1)
    return pd.read_csv(file_path)

def search_game_in_dataset(df, game_name):
    if 'title' not in df.columns or 'release_na' not in df.columns:
        print("Error: The dataset does not contain the required columns. Please check the dataset format.")
        exit(1)
    df['release_na'] = pd.to_datetime(df['release_na'], errors='coerce')
    results = df[df['title'].str.contains(game_name, case=False, na=False)].sort_values(by='release_na', ascending=False)
    return results

def search_latest_games(game_name):
    search_url = f"https://www.metacritic.com/search/game/{game_name}/results"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(search_url, headers=headers)
    if response.status_code != 200:
        print("Failed to retrieve latest game data.")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    game_list = []
    for item in soup.select('.result_wrap')[:5]:  # Limit to top 5 results
        title_tag = item.select_one('.product_title a')
        date_tag = item.select_one('.release_date .data')
        if title_tag and date_tag:
            game_title = title_tag.text.strip()
            release_date = date_tag.text.strip()
            game_list.append((game_title, release_date))
    return game_list

def get_gameplay_video(game_name):
    search_query = f"{game_name} gameplay"
    results = YoutubeSearch(search_query, max_results=1).to_dict()
    if results:
        return f"https://www.youtube.com/watch?v={results[0]['id']}"
    return None

def display_game_info(game):
    print(f"\nTitle: {game['title']}\nRelease Date: {game.get('release_na', 'Unknown')}\nMain Story: {game.get('main_story', 'N/A')} hours\nMain + Extras: {game.get('main_plus_extras', 'N/A')} hours\nCompletionist: {game.get('completionist', 'N/A')} hours\nAll Styles: {game.get('all_styles', 'N/A')} hours")

def display_online_game_info(game):
    title, release_date = game
    print(f"\nTitle: {title}\nRelease Date: {release_date}")

def main():
    print("Loading HowLongToBeat dataset...")
    df = load_dataset()

    while True:
        print("\n--- Game Search App ---")
        game_name = input("Enter the game name to search (or 'exit' to quit): ").strip()
        if game_name.lower() == 'exit':
            print("Exiting application. Goodbye!")
            break

        results = search_game_in_dataset(df, game_name)
        if results.empty:
            print(f"No results found in local dataset for '{game_name}'. Searching online for latest games...")
            latest_games = search_latest_games(game_name)
            if latest_games:
                print("\nFound latest games online:")
                for idx, (game_title, release_date) in enumerate(latest_games, 1):
                    print(f"{idx}: {game_title} ({release_date})")

                choice = input("Enter the number of the game to view details, or 'skip' to continue: ").strip()
                if choice.isdigit() and 1 <= int(choice) <= len(latest_games):
                    selected_game = latest_games[int(choice) - 1]
                    display_online_game_info(selected_game)

                    video_url = get_gameplay_video(selected_game[0])
                    if video_url:
                        print(f"\nGameplay Video for {selected_game[0]}: {video_url}")
                        open_video = input("Do you want to open the video in your browser? (yes/no): ").strip().lower()
                        if open_video == 'yes':
                            subprocess.run(["cmd.exe", "/c", "start", "chrome", video_url], check=True)
                    else:
                        print("No gameplay video found.")
            else:
                print("No latest games found online.")
        else:
            print(f"\nFound {len(results)} results:")
            for idx, (_, row) in enumerate(results.iterrows(), 1):
                release_date = row.get('release_na', 'Unknown')
                if isinstance(release_date, pd.Timestamp):
                    release_date = release_date.strftime('%Y-%m-%d')
                print(f"{idx}: {row['title']} ({release_date})")

            try:
                choice = int(input("\nEnter the number of the game you want to view details for: "))
                if choice < 1 or choice > len(results):
                    raise ValueError
                selected_game = results.iloc[choice - 1]
                display_game_info(selected_game)

                video_url = get_gameplay_video(selected_game['title'])
                if video_url:
                    print(f"\nGameplay Video: {video_url}")
                    open_video = input("Do you want to open the video in your browser? (yes/no): ").strip().lower()
                    if open_video == 'yes':
                        subprocess.run(["cmd.exe", "/c", "start", "chrome", video_url], check=True)
                else:
                    print("No gameplay video found.")
            except (ValueError, IndexError):
                print("Invalid selection. Please try again.")

if __name__ == "__main__":
    main()
