import requests
from bs4 import BeautifulSoup

url = 'https://example.com'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
headlines = soup.find_all('h2')

print('Headline:')
for idx, headline in enumerate(headlines, start=1):
    print(f"{idx}. {headline.text.strip(0)}")