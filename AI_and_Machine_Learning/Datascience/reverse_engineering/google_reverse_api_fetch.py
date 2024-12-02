import requests

# Define the URL found from the Network tab
url = "https://www.google.com/search"

# Define the headers copied from the cURL command
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    # Add any other headers that were in the cURL command
}

# Define the parameters (query string) for the search
params = {
    "q": "OpenAI",  # The search query
    "hl": "en",     # Language (optional)
    "gl": "us",     # Country (optional)
    # Add any other parameters found in the request
}

# Send the GET request to Google's search API
response = requests.get(url, headers=headers, params=params)

# Print the raw HTML or JSON response (depending on the API)
print(response.text)
