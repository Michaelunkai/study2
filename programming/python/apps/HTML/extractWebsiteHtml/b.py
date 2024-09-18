import requests
from bs4 import BeautifulSoup
import os

def fetch_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as err:
        print(f"An error occurred: {err}")
    return None

def save_content(content, filename, file_type):
    if content is None:
        print(f"No content to save for {file_type} file.")
        return
    file_path = os.path.join(r"C:\users\micha\downloads", filename)
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"The {file_type} content has been saved to {file_path}")
    except IOError as e:
        print(f"Error saving {file_type} file: {e}")

def main():
    url = input("Enter the URL of the website: ")
    html_content = fetch_html(url)
    if html_content:
        save_content(html_content, "website_content.html", "HTML")
        save_content(html_content, "website_content.txt", "text")
    else:
        print("Failed to fetch content. Please check the URL and try again.")

if __name__ == "__main__":
    main()
