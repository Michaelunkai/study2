import os
import requests
from PIL import Image
from io import BytesIO
import ctypes
import time
import json

def load_seen_urls(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return set(json.load(file))
    return set()

def save_seen_urls(file_path, seen_urls):
    with open(file_path, 'w') as file:
        json.dump(list(seen_urls), file)

def get_image_url(search_term, api_key, cse_id, seen_urls, start_index=1):
    search_url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "q": search_term,
        "cx": cse_id,
        "key": api_key,
        "searchType": "image",
        "fileType": "jpg",
        "imgSize": "large",
        "num": 10,  # Get more results to increase the chance of finding a new image
        "start": start_index  # Specify the start index for the search results
    }
    response = requests.get(search_url, params=params)
    response.raise_for_status()
    search_results = response.json()
    
    for item in search_results.get("items", []):
        image_url = item.get("link")
        if image_url not in seen_urls:
            seen_urls.add(image_url)
            return image_url
    
    return None  # Return None if no new image is found

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

    seen_urls_file = "seen_urls.json"
    seen_urls = load_seen_urls(seen_urls_file)
    count = 1
    start_index = 1

    while True:
        try:
            print(f"Searching for an image... (Attempt {count})")
            image_url = get_image_url(search_term, api_key, cse_id, seen_urls, start_index)
            
            if image_url is None:
                print("No new images found, fetching the next set of results...")
                start_index += 10
                continue

            print(f"Found image URL: {image_url}")

            print("Downloading the image...")
            image = download_image(image_url)

            wallpaper_path = os.path.join("C:\\Users\\micha\\pictures", f"wallpaper{count}.jpg")
            print(f"Saving the image to {wallpaper_path}...")
            save_image(image, wallpaper_path)

            print("Setting the wallpaper...")
            set_wallpaper(wallpaper_path)
            print("Wallpaper set successfully!")

            save_seen_urls(seen_urls_file, seen_urls)

            count += 1
            start_index = 1  # Reset start_index after a successful attempt
            print("Waiting for 10 seconds before changing wallpaper again...")
            time.sleep(10)

        except Exception as e:
            print(f"An error occurred: {e}")
            print("Waiting for 10 seconds before retrying...")
            time.sleep(10)

if __name__ == "__main__":
    main()
