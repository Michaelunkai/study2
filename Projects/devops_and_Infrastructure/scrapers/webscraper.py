import requests 
from bs4 import BeautifulSoup

url = 'https://en.wikipedia.org/wiki/Main_Page'
response = requests.get(url)

if response.status_code == 200:
    # Proceed with parsing the content
    html_content = response.content
    soup = BeautifulSoup(html_content, 'html.parser')
    # Now you can start extracting data using BeautifulSoup functions
else:
    print(f"Failed to retrieve the webpage. status code: {responde.status_code}")


links = soup.find_all('a')
for link in links:
    print(link.get('href'))