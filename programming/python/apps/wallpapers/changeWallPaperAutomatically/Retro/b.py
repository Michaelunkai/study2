import requests
import ctypes
import time
import os
import random
from datetime import datetime

# For getting screen resolution
import ctypes
user32 = ctypes.windll.user32

# Configure logging
def log_message(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")
    with open("cyberpunk_wallpaper_changer.log", "a") as log_file:
        log_file.write(f"[{timestamp}] {message}\n")

# Get the current screen resolution
def get_screen_resolution():
    width = user32.GetSystemMetrics(0)
    height = user32.GetSystemMetrics(1)
    return width, height

# Get resolution and create appropriate filters
screen_width, screen_height = get_screen_resolution()
log_message(f"Detected screen resolution: {screen_width}x{screen_height}")

# Calculate aspect ratio
aspect_ratio = screen_width / screen_height
aspect_ratio_string = "16x10" if abs(aspect_ratio - 16/10) < 0.1 else "16x9"

# Instead of strict resolution matching, use a minimum resolution approach
# This will ensure we get images that are at least as large as your screen
min_width = screen_width
min_height = screen_height
min_resolution = f"{min_width}x{min_height}"

# Wallpaper sources with more flexible resolution requirements
WALLPAPER_SOURCES = [
    {
        'name': 'Wallhaven Cyberpunk',
        'url': 'https://wallhaven.cc/api/v1/search',
        'params': {
            'q': 'cyberpunk OR neon city OR retrowave OR synthwave',
            'categories': '111',  # General + Anime + People
            'purity': '100',      # SFW only
            'sorting': 'random',
            'ratios': aspect_ratio_string,  # Match aspect ratio rather than exact resolution
            'atleast': min_resolution,  # Get images at least as large as the screen
            'colors': '291b3b,7c54a5,330033,000000',  # Purple, dark purple, black
        },
        'processor': lambda data: data['data'][0]['path'] if data.get('data') and len(data.get('data', [])) > 0 else None
    },
    {
        'name': 'Wallhaven Dark Tech',
        'url': 'https://wallhaven.cc/api/v1/search',
        'params': {
            'q': 'dark tech OR retrocomputing OR vaporwave',
            'categories': '111',
            'purity': '100',
            'sorting': 'random',
            'ratios': aspect_ratio_string,  # Match aspect ratio
            'atleast': min_resolution,  # Minimum resolution
            'colors': '291b3b,7c54a5,330033,000000,550055', # Purple tones and black
        },
        'processor': lambda data: data['data'][0]['path'] if data.get('data') and len(data.get('data', [])) > 0 else None
    },
    {
        'name': 'Reddit Cyberpunk',
        'url': 'https://www.reddit.com/r/Cyberpunk/hot.json',
        'params': {
            'limit': 100
        },
        'headers': {
            'User-Agent': 'CyberpunkWallpaperChanger/1.0'
        },
        'processor': lambda data: next(
            (post['data']['url'] for post in data['data']['children'] 
             if post['data']['url'].lower().endswith(('.jpg', '.jpeg', '.png')) 
             and not post['data'].get('over_18', False)),
            None
        )
    },
    {
        'name': 'Reddit Outrun',
        'url': 'https://www.reddit.com/r/outrun/hot.json',
        'params': {
            'limit': 100
        },
        'headers': {
            'User-Agent': 'CyberpunkWallpaperChanger/1.0'
        },
        'processor': lambda data: next(
            (post['data']['url'] for post in data['data']['children'] 
             if post['data']['url'].lower().endswith(('.jpg', '.jpeg', '.png'))
             and not post['data'].get('over_18', False)),
            None
        )
    },
    {
        'name': 'Cyberpunk Wallpaper Websites',
        'url': 'https://wallhaven.cc/api/v1/search',
        'params': {
            'q': 'cyberpunk',
            'categories': '100',
            'purity': '100',
            'sorting': 'random',
            'atleast': min_resolution,
        },
        'processor': lambda data: data['data'][0]['path'] if data.get('data') and len(data.get('data', [])) > 0 else None
    }
]

# Path to save the downloaded wallpaper image
IMAGE_PATH = os.path.join(os.getcwd(), "cyberpunk_wallpaper.jpg")

# Cache to store previously fetched wallpapers to avoid API rate limits
# This is crucial for the 5-second update interval
WALLPAPER_CACHE = []
MAX_CACHE_SIZE = 20

def initialize_wallpaper_cache():
    """Pre-fetch some wallpapers to fill the cache for fast updates"""
    log_message("Initializing wallpaper cache...")
    cache_dir = os.path.join(os.getcwd(), "wallpaper_cache")
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
    
    # Fill cache initially with 5 wallpapers
    for i in range(min(5, MAX_CACHE_SIZE)):
        try:
            # Try to fetch a new wallpaper
            image_path = os.path.join(cache_dir, f"wallpaper_cache_{i}.jpg")
            if fetch_wallpaper(save_path=image_path):
                WALLPAPER_CACHE.append(image_path)
                log_message(f"Added wallpaper {i+1} to cache")
        except Exception as e:
            log_message(f"Cache initialization error: {str(e)}")
    
    log_message(f"Cache initialized with {len(WALLPAPER_CACHE)} wallpapers")

def set_wallpaper(image_path):
    """Set the Windows desktop wallpaper."""
    try:
        SPI_SETDESKWALLPAPER = 20
        ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, image_path, 3)
        log_message("Cyberpunk wallpaper set successfully")
        return True
    except Exception as e:
        log_message(f"Failed to set wallpaper: {str(e)}")
        return False

def download_image(image_url, save_path=None):
    """Download image from URL and save locally."""
    target_path = save_path if save_path else IMAGE_PATH
    
    try:
        log_message(f"Downloading image from: {image_url}")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(image_url, headers=headers, stream=True, timeout=30)
        response.raise_for_status()
        
        with open(target_path, 'wb') as f:
            for chunk in response.iter_content(8192):
                f.write(chunk)
        return True
    except Exception as e:
        log_message(f"Failed to download image: {str(e)}")
        return False

def verify_image_resolution(image_path):
    """Verify that the downloaded image is large enough for the screen."""
    try:
        # Using PIL to check image dimensions
        from PIL import Image
        with Image.open(image_path) as img:
            width, height = img.size
            log_message(f"Downloaded image resolution: {width}x{height}")
            
            # Check if image is at least as large as the screen
            if width >= screen_width and height >= screen_height:
                return True
            else:
                log_message(f"Image too small: {width}x{height}, need at least {screen_width}x{screen_height}")
                return False
    except ImportError:
        log_message("PIL not installed. Skipping resolution verification.")
        return True  # Skip verification if PIL is not available
    except Exception as e:
        log_message(f"Image verification error: {str(e)}")
        return True  # Fail open to avoid blocking wallpapers

def is_likely_cyberpunk_style(image_path):
    """Basic check to verify if image likely fits the cyberpunk/dark aesthetic."""
    # For fast updates, we trust our source filters
    return True

def fetch_wallpaper(save_path=None):
    """Fetch wallpaper from available sources."""
    random.shuffle(WALLPAPER_SOURCES)  # Randomize source order
    
    for source in WALLPAPER_SOURCES:
        try:
            log_message(f"Attempting source: {source['name']}")
            
            # Make the API request
            headers = source.get('headers', {})
            response = requests.get(source['url'], params=source['params'], headers=headers, timeout=15)
            
            response.raise_for_status()
            data = response.json()
            
            # Process the response
            image_url = source['processor'](data)
            if not image_url:
                log_message(f"No suitable image found from {source['name']}")
                continue
                
            # Download and validate the wallpaper
            if download_image(image_url, save_path):
                target_path = save_path if save_path else IMAGE_PATH
                # For cache initialization, we skip verification to speed things up
                if save_path or verify_image_resolution(target_path):
                    if save_path or is_likely_cyberpunk_style(target_path):
                        log_message(f"Found suitable cyberpunk/dark style wallpaper from {source['name']}")
                        return True
                    else:
                        log_message(f"Image doesn't match desired aesthetic")
                        continue
                else:
                    log_message(f"Image doesn't meet resolution requirements")
                    continue
                    
        except Exception as e:
            log_message(f"Error with {source['name']}: {str(e)}")
            continue
            
    return False

def handle_wallpaper_fallback():
    """If all sources fail, try using a more relaxed approach."""
    log_message("Attempting fallback method with less strict requirements")
    
    # Simplified wallhaven search with fewer requirements
    try:
        url = "https://wallhaven.cc/api/v1/search"
        params = {
            'q': 'cyberpunk neon',
            'categories': '111',
            'purity': '100',
            'sorting': 'random',
        }
        
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        if data.get('data') and len(data['data']) > 0:
            image_url = data['data'][0]['path']
            if download_image(image_url):
                log_message("Successfully downloaded fallback wallpaper")
                return True
    except Exception as e:
        log_message(f"Fallback method failed: {str(e)}")
    
    return False

def create_backup_folder():
    """Create a folder to store backup wallpapers."""
    backup_folder = os.path.join(os.getcwd(), "wallpaper_backups")
    if not os.path.exists(backup_folder):
        os.makedirs(backup_folder)
    return backup_folder

def backup_current_wallpaper():
    """Save a copy of the current wallpaper before replacing it."""
    if os.path.exists(IMAGE_PATH):
        backup_folder = create_backup_folder()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = os.path.join(backup_folder, f"wallpaper_{timestamp}.jpg")
        try:
            with open(IMAGE_PATH, 'rb') as src, open(backup_path, 'wb') as dst:
                dst.write(src.read())
            log_message(f"Backed up previous wallpaper to {backup_path}")
        except Exception as e:
            log_message(f"Failed to backup wallpaper: {str(e)}")

def refill_cache_if_needed():
    """Add new images to the cache in the background"""
    if len(WALLPAPER_CACHE) < MAX_CACHE_SIZE // 2:
        log_message("Cache running low, fetching more wallpapers")
        cache_dir = os.path.join(os.getcwd(), "wallpaper_cache")
        
        # Add up to 3 new wallpapers to the cache
        for i in range(3):
            try:
                cache_item = os.path.join(cache_dir, f"wallpaper_cache_{len(WALLPAPER_CACHE)}.jpg")
                if fetch_wallpaper(save_path=cache_item):
                    WALLPAPER_CACHE.append(cache_item)
                    log_message(f"Added new wallpaper to cache (total: {len(WALLPAPER_CACHE)})")
            except Exception as e:
                log_message(f"Error adding to cache: {str(e)}")

def get_next_wallpaper():
    """Get the next wallpaper from cache or fetch a new one"""
    # Try to use the cache first
    if WALLPAPER_CACHE:
        next_wallpaper = WALLPAPER_CACHE.pop(0)
        log_message(f"Using cached wallpaper (remaining: {len(WALLPAPER_CACHE)})")
        
        # Copy the cached wallpaper to the main image path
        try:
            with open(next_wallpaper, 'rb') as src, open(IMAGE_PATH, 'wb') as dst:
                dst.write(src.read())
            return True
        except Exception as e:
            log_message(f"Error using cached wallpaper: {str(e)}")
    
    # If cache is empty or failed, fetch directly
    return fetch_wallpaper()

def main():
    log_message("Fast Cyberpunk/Dark/Purple/Retro Wallpaper Changer started")
    log_message(f"Finding wallpapers with cyberpunk aesthetics for resolution {screen_width}x{screen_height}")
    log_message("Wallpaper will update every 5 seconds")
    
    # Updated interval to 5 seconds
    interval = 5  # 5 seconds instead of 30 minutes
    
    # Initialize the cache for faster updates
    initialize_wallpaper_cache()
    
    # Counter for cache refill check (don't check every 5 seconds)
    refill_counter = 0
    
    while True:
        try:
            # Skip backup for fast updates to reduce disk writes
            if refill_counter % 12 == 0:  # Every ~1 minute
                backup_current_wallpaper()
            
            success = get_next_wallpaper()
            
            # If cache and normal fetch both fail, try fallback
            if not success:
                log_message("Failed to get wallpaper, trying fallback method")
                success = handle_wallpaper_fallback()
            
            if success:
                if set_wallpaper(IMAGE_PATH):
                    log_message("Successfully updated to new cyberpunk wallpaper!")
                else:
                    log_message("Failed to set wallpaper (download may have succeeded)")
            else:
                log_message("All attempts failed, will retry")
            
            # Check if cache needs refilling (not every iteration to avoid API rate limits)
            refill_counter += 1
            if refill_counter % 12 == 0:  # Check every ~1 minute
                refill_cache_if_needed()
            
            # Wait 5 seconds before next update
            time.sleep(interval)
            
        except KeyboardInterrupt:
            log_message("Shutting down by user request")
            break
        except Exception as e:
            log_message(f"Unexpected error: {str(e)}")
            time.sleep(2)  # Shorter retry time for fast mode

if __name__ == "__main__":
    main()
