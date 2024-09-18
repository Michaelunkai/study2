import requests

url = 'https://www.example.com'
response = requests.get(url)

with open('filename.html', 'w', encoding='utf-8') as file:
    file.write(response.text)
