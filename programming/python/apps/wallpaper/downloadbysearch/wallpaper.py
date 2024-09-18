import os
import requests
from PIL import Image
from io import BytesIO
import ctypes

def get_image_url(search_term, api_key, cse_id):
    search_url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "q": search_term,
        "cx": cse_id,
        "key": api_key,
        "searchType": "image",
        "fileType": "jpg",
        "imgSize": "large",
        "num": 1
    }
    response = requests.get(search_url, params=params)
    response.raise_for_status()
    search_results = response.json()
    if "items" in search_results and len(search_results["items"]) > 0:
        return search_results["items"][0]["link"]
    else:
        raise Exception("No images found for the search term.")

def download_image(image_url):
    response = requests.get(image_url)
    response.raise_for_status()
    image = Image.open(BytesIO(response.content))
    return image

def save_image(image, path):
    image.save(path)

def set_wallpaper(image_path):
    # Set wallpaper using ctypes
    ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 3)

def main():
    # Replace with your own Google Custom Search API key and CSE ID
    api_key = "YOUR_API_KEY_HERE"
    cse_id = "YOUR_CSE_ID_HERE"

    search_term = input("Enter the search term for the wallpaper: ")
    try:
        print("Searching for an image...")
        image_url = get_image_url(search_term, api_key, cse_id)
        print(f"Found image URL: {image_url}")

        print("Downloading the image...")
        image = download_image(image_url)

        wallpaper_path = os.path.join("C:\\Users\\micha\\pictures", "wallpaper.jpg")
        print(f"Saving the image to {wallpaper_path}...")
        save_image(image, wallpaper_path)

        print("Setting the wallpaper...")
        set_wallpaper(wallpaper_path)
        print("Wallpaper set successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
