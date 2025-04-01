import requests
import ctypes
import time
import os

# Unsplash API credentials (provided by you)
CLIENT_ID = "VYh9HIzAIzjI6dX_yvP6zblNd8It0wSATTKbA1Bz4-Q"
CLIENT_SECRET = "LJG3wdfxvV-q-YhZsBCY5efXxJB3JkUySI5HBUN7OqA"  # Not required for this endpoint

# API endpoint for a random photo with a query for video game wallpapers in landscape
UNSPLASH_URL = "https://api.unsplash.com/photos/random"
PARAMS = {
    "query": "video game wallpaper",  # strictly video game related
    "orientation": "landscape",
    "client_id": CLIENT_ID
}

# Path to save the downloaded wallpaper image
IMAGE_PATH = os.path.join(os.getcwd(), "wallpaper.jpg")

def set_wallpaper(image_path):
    """
    Set the Windows desktop wallpaper using the SystemParametersInfoW API.
    """
    SPI_SETDESKWALLPAPER = 20
    result = ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, image_path, 3)
    if not result:
        print("Error: Unable to set wallpaper.")

def fetch_random_wallpaper():
    """
    Fetch a random video game wallpaper image URL from Unsplash and download it.
    """
    try:
        response = requests.get(UNSPLASH_URL, params=PARAMS, timeout=10)
        response.raise_for_status()
        data = response.json()
        # Get the URL for a high-resolution image; 'full' is typically high quality.
        image_url = data.get("urls", {}).get("full")
        if not image_url:
            print("No image URL found in response.")
            return False
        
        print(f"Downloading image from: {image_url}")
        image_response = requests.get(image_url, stream=True, timeout=20)
        image_response.raise_for_status()
        with open(IMAGE_PATH, "wb") as f:
            for chunk in image_response.iter_content(1024):
                f.write(chunk)
        return True
    except Exception as e:
        print(f"Error fetching wallpaper: {e}")
        return False

def main():
    print("Starting video game wallpaper changer. Press Ctrl+C to exit.")
    while True:
        if fetch_random_wallpaper():
            set_wallpaper(IMAGE_PATH)
            print("Wallpaper updated.")
        else:
            print("Skipping wallpaper update due to an error.")
        # Wait 15 seconds before updating
        time.sleep(15)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting wallpaper changer.")
