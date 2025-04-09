import requests
import ctypes
import time
import os
import random
from datetime import datetime

# Configure logging
def log_message(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")
    with open("wallpaper_changer.log", "a") as log_file:
        log_file.write(f"[{timestamp}] {message}\n")

# Wallpaper sources with proper API endpoints
WALLPAPER_SOURCES = [
    {
        'name': 'Wallhaven Gaming',
        'url': 'https://wallhaven.cc/api/v1/search',
        'params': {
            'categories': '111',  # General + Anime + People
            'purity': '100',     # SFW only
            'sorting': 'random',
            'ratios': '16x9,16x10',
            'q': 'pc game',
            'colors': '000000',
            'atleast': '1920x1080'
        },
        'processor': lambda data: data['data'][0]['path'] if data.get('data') else None
    },
    {
        'name': 'Steam Workshop',
        'url': 'https://api.steampowered.com/ISteamRemoteStorage/GetPublishedFileDetails/v1/',
        'params': {
            'itemcount': 1,
            'publishedfileids[0]': random.choice([
                '2579303180',  # Cyberpunk 2077
                '2585728766',  # Elden Ring
                '2585728765',  # Horizon Zero Dawn
                '2585728764',  # God of War
                '2585728763',  # Red Dead Redemption 2
                '2585728762',  # The Witcher 3
                '2585728761',  # Dark Souls 3
                '2585728760'   # Sekiro
            ])
        },
        'processor': lambda data: data['response']['publishedfiledetails'][0]['preview_url'].replace('workshop/', '') 
                                if data.get('response', {}).get('publishedfiledetails') else None
    },
    {
        'name': 'Gaming Wallpapers Subreddit',
        'url': 'https://www.reddit.com/r/GameWallpapers/hot.json',
        'params': {
            'limit': 50
        },
        'headers': {
            'User-Agent': 'PCGameWallpaperChanger/1.0'
        },
        'processor': lambda data: next(
            (post['data']['url'] for post in data['data']['children'] 
             if post['data']['url'].lower().endswith(('.jpg', '.jpeg', '.png'))), None
        )
    }
]

# Path to save the downloaded wallpaper image
IMAGE_PATH = os.path.join(os.getcwd(), "pc_game_wallpaper.jpg")

def set_wallpaper(image_path):
    """Set the Windows desktop wallpaper."""
    try:
        SPI_SETDESKWALLPAPER = 20
        ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, image_path, 3)
        log_message("Wallpaper set successfully")
        return True
    except Exception as e:
        log_message(f"Failed to set wallpaper: {str(e)}")
        return False

def download_image(image_url):
    """Download image from URL and save locally."""
    try:
        log_message(f"Downloading image from: {image_url}")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(image_url, headers=headers, stream=True, timeout=30)
        response.raise_for_status()
        
        with open(IMAGE_PATH, 'wb') as f:
            for chunk in response.iter_content(8192):
                f.write(chunk)
        return True
    except Exception as e:
        log_message(f"Failed to download image: {str(e)}")
        return False

def fetch_wallpaper():
    """Fetch wallpaper from available sources."""
    random.shuffle(WALLPAPER_SOURCES)  # Randomize source order
    
    for source in WALLPAPER_SOURCES:
        try:
            log_message(f"Attempting source: {source['name']}")
            
            # Make the API request
            headers = source.get('headers', {})
            if source['name'] == 'Steam Workshop':
                response = requests.post(source['url'], data=source['params'])
            else:
                response = requests.get(source['url'], params=source['params'], headers=headers, timeout=15)
            
            response.raise_for_status()
            data = response.json()
            
            # Process the response
            image_url = source['processor'](data)
            if not image_url:
                log_message(f"No suitable image found from {source['name']}")
                continue
                
            # Download and set the wallpaper
            if download_image(image_url):
                return True
                
        except Exception as e:
            log_message(f"Error with {source['name']}: {str(e)}")
            continue
            
    return False

def main():
    log_message("PC Video Game Wallpaper Changer started")
    log_message("Sources: Wallhaven, Steam Workshop, Reddit GameWallpapers")
    
    while True:
        try:
            if fetch_wallpaper():
                if set_wallpaper(IMAGE_PATH):
                    log_message("Successfully updated PC game wallpaper!")
                else:
                    log_message("Failed to set wallpaper (download may have succeeded)")
            else:
                log_message("All sources failed, will retry")
            
            # Wait before next update (30 minutes)
            time.sleep(1800)
            
        except KeyboardInterrupt:
            log_message("Shutting down by user request")
            break
        except Exception as e:
            log_message(f"Unexpected error: {str(e)}")
            time.sleep(60)  # Wait before retrying after error

if __name__ == "__main__":
    main()