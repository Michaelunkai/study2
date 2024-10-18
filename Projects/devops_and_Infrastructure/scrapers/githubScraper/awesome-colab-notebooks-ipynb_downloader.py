import requests
from bs4 import BeautifulSoup
import os

# URL of the GitHub page
url = "https://github.com/amrzv/awesome-colab-notebooks?tab=readme-ov-file"

# Directory path to save the .ipynb files
download_dir = r"C:\Users\micha\Downloads"

def get_ipynb_links(url):
    """
    Extracts links to .ipynb files from the GitHub page.
    
    Args:
        url (str): URL of the GitHub page
    
    Returns:
        list: List of links to .ipynb files
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    ipynb_links = []
    
    # Find all links on the page
    for link in soup.find_all('a'):
        href = link.get('href')
        
        # Check if the link points to a .ipynb file
        if href and href.endswith('.ipynb'):
            ipynb_links.append(href)
    
    return ipynb_links

def download_ipynb(ipynb_links, download_dir):
    """
    Downloads .ipynb files from the extracted links and saves them to the specified directory.
    
    Args:
        ipynb_links (list): List of links to .ipynb files
        download_dir (str): Directory path to save the .ipynb files
    """
    for link in ipynb_links:
        # Extract the filename from the link
        filename = link.split('/')[-1]
        
        # Construct the full path to save the file
        file_path = os.path.join(download_dir, filename)
        
        # Download the file
        response = requests.get(link)
        with open(file_path, 'wb') as file:
            file.write(response.content)
        
        print(f"Downloaded {filename} to {download_dir}")

def main():
    ipynb_links = get_ipynb_links(url)
    download_ipynb(ipynb_links, download_dir)

if __name__ == "__main__":
    main()
